class ConditionEngine:
    @staticmethod
    def evaluate(condition_name, state):
        """
        Evaluates a string condition from the JSON spec against the current game state.
        Now covers ALL spec conditions with best-effort state mapping.
        """
        # --- UNIVERSAL BASICS ---
        if condition_name == "target_valid":
            return state.get('thp', 0) > 0 # Target HP > 0 implies valid target
            
        if condition_name == "combat_check":
            return state.get('combat', False)
        
        if condition_name == "interruptible":
            return state.get('interruptible', False)

        if condition_name == "target_in_range":
             # Range pixel: usually 0-255 scaling to yards. >10 usually means "in melee/cast range"
             return state.get('range', 0) > 10

        # --- HEALTH CHECKS ---
        if "health_lt_" in condition_name:
            # Parse "health_lt_70" -> 70
            try:
                thresh = int(condition_name.split("_")[-1])
                return state.get('hp', 100) < thresh
            except: return True

        if "health_gt_" in condition_name:
            try:
                thresh = int(condition_name.split("_")[-1])
                return state.get('hp', 100) > thresh
            except: return True
            
        # --- EXECUTE PHASES ---
        if "execute_range" in condition_name or "target_health_lt_20" in condition_name:
            return state.get('thp', 100) < 20

        if "target_health_lt_35" in condition_name:
            return state.get('thp', 100) < 35
        
        if "target_health_lt_80" in condition_name: # Venthyr/First Strike
            return state.get('thp', 100) > 80

        # --- RESOURCE CHECKS ---
        if "_gte_" in condition_name and ("power" in condition_name or "rage" in condition_name or "energy" in condition_name or "focus" in condition_name or "runic" in condition_name or "maelstrom" in condition_name or "insanity" in condition_name or "astral" in condition_name or "fury" in condition_name or "pain" in condition_name):
             # Generic resource check: "rage_gte_40"
            try:
                thresh = int(condition_name.split("_")[-1])
                return state.get('power', 0) >= thresh
            except: return True

        if "_lt_" in condition_name and ("power" in condition_name or "rage" in condition_name or "energy" in condition_name or "focus" in condition_name):
             # Generic resource check: "rage_lt_40"
            try:
                thresh = int(condition_name.split("_")[-1])
                return state.get('power', 0) < thresh
            except: return True

        # --- COMBO POINTS / HOLY POWER / SHARDS / ESSENCE (Pixel 8 'sec') ---
        if "combo_points" in condition_name or "holy_power" in condition_name or "shards" in condition_name or "essence" in condition_name or "soul_fragments" in condition_name:
             # "combo_points_gte_5"
             try:
                thresh = int(condition_name.split("_")[-1])
                val = state.get('sec', 0)
                
                if "_gte_" in condition_name or "_4_plus" in condition_name:
                    return val >= thresh
                if "_lt_" in condition_name:
                    return val < thresh
                if "_eq_" in condition_name:
                    return val == thresh
             except: return True

        # --- ROGUE STEALTH ---
        if "stealth" in condition_name or "subterfuge" in condition_name:
            if "not_" in condition_name:
                return not state.get('stealthed', False)
            return state.get('stealthed', False)

        # --- GENERIC BUFF/DEBUFF/COOLDOWN FALLBACKS ---
        # Since we lack specific auremetry pixels for buffs/debuffs/CDs in the current engine,
        # we treat "ready" checks as True (letting the game handle CD errors)
        # and "needed" checks as True (to ensure rotation flow).
        
        if "refresh_dot_vt" in condition_name:
            # Shadow Priest VT maps to Dot Slot 0 (P11)
            # Refresh at pandemic (<6s remaining for safety margin)
            return state.get('dots', [0.0])[0] < 6.0
            
        if "refresh_dot_swp" in condition_name:
            # Shadow Priest SWP maps to Dot Slot 1 (P12)
            # Refresh at pandemic (<6s remaining)
            return state.get('dots', [0.0, 0.0])[1] < 6.0

        if "refresh_dot:" in condition_name:
            # Generic dot indexing (e.g. refresh_dot:3)
            try:
                idx = int(condition_name.split(':')[-1])
                dots = state.get('dots', [])
                if idx < len(dots):
                    return dots[idx] < 4.5
            except:
                pass
            return False

        if "refresh_dot" in condition_name or "dot_" in condition_name:
            # SHADOW PRIEST / AFFLICTION / FERAL / ASSASSINATION
            # Use the dedicated multidot pixel (P11) if available
            dot_rem = state.get('target_dot_remaining', 0)
            
            # Pandemic window is usually 30% of base duration.
            # VT: 21s * 0.3 = 6.3s
            # SWP: 20s * 0.3 = 6.0s
            # For simplicity, 4.5s is a safe universal pandemic threshold that prevents double-casting
            return dot_rem < 4.5

        keywords = ["buff_", "debuff_", "cooldown_", "charges_", "totem_", "flare_"]
        for k in keywords:
            if k in condition_name:
                # OPTIMIZATION: If it's a "missing" check, we return True (assume missing to prompt cast).
                # If it's an "active" check, we might block.
                # BUT blocking prevents usage. Safer to return True and let the user cast it.
                # EXCEPT: "cooldown_remains" -> if we think it's on CD, we shouldn't spam.
                # But we don't know if it's on CD.
                
                # SPECIAL CASE: Mitigation/Heal checks - only if HP low
                if "mitigation" in condition_name or "heal" in condition_name:
                    if state.get('hp', 100) > 80: return False # Don't use def/heal if healthy
                    
                return True

        if "proc_" in condition_name:
            # Assume procs are active to not miss opportunities, or rely on 'sec' if mapped?
            return True

        # --- SPECIFIC OVERRIDES ---
        if condition_name == "aoe_range": 
            return state.get('range', 0) < 8
            
        return True

