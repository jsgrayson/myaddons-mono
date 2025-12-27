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

        if condition_name == "not_combat":
            return not state.get('combat', False)
        
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

        # --- COMBO POINTS / HOLY POWER / SHARDS / ESSENCE (Pixel 8) ---
        secondary_keys = ["combo_points", "holy_power", "shards", "essence", "soul_fragments", "chi", "arcane_charges", "insanity"]
        for key in secondary_keys:
            if key in condition_name:
                try:
                    # Handle both "key_gte_X" and "key_lt_X" and "key_eq_X"
                    parts = condition_name.split("_")
                    thresh = int(parts[-1])
                    val = state.get('secondary_power', 0)
                    
                    if "_gte_" in condition_name or "_4_plus" in condition_name:
                        return val >= thresh
                    if "_lt_" in condition_name:
                        return val < thresh
                    if "_eq_" in condition_name:
                        return val == thresh
                except:
                    return True

        # --- ROGUE STEALTH ---
        if "stealth" in condition_name or "subterfuge" in condition_name:
            if "not_" in condition_name:
                return not state.get('stealthed', False)
            return state.get('stealthed', False)
        
        # --- RANGE CHECKS (P6 broadcasts distance in yards * 4.25) ---
        # Range is decoded to approximate yards
        range_val = state.get('range', 40)  # Default to max range
        
        if condition_name == "in_melee_range":
            return range_val <= 8  # Melee range ~5-8 yards
        
        if condition_name == "out_of_melee_range":
            return range_val > 8  # Not in melee
        
        if condition_name == "in_charge_range":
            return range_val >= 8 and range_val <= 25  # Charge range 8-25 yards
        
        if condition_name == "in_ranged_range":
            return range_val <= 40  # Standard caster range
        
        # --- CHARGE CHECKS (P16 broadcasts charges for key ability) ---
        if condition_name == "has_charges":
            return state.get('spell_charges', 0) > 0
        
        if condition_name == "no_charges":
            return state.get('spell_charges', 0) == 0
        
        # --- PROC CONDITIONS (P14/P15 are per-spec procs) ---
        if condition_name == "overpower_proc" or condition_name == "tactician_proc":
            return state.get('mb_reset_proc', False)  # P14 is reused for Overpower proc on Arms
        
        if condition_name == "sudden_death":
            return state.get('mf_insanity_proc', False)  # P15 is reused for Sudden Death on Arms
        
        # --- SECONDARY CHARGES (P26) ---
        if condition_name == "has_secondary_charges":
            return state.get('secondary_charges', 0) > 0

        # --- GENERIC BUFF/DEBUFF/COOLDOWN FALLBACKS ---
        # Since we lack specific auremetry pixels for buffs/debuffs/CDs in the current engine,
        # we treat "ready" checks as True (letting the game handle CD errors)
        # and "needed" checks as True (to ensure rotation flow).
        
        # TIME-TO-KILL CHECK: Don't refresh DoTs on dying targets
        # Only apply if we have valid target HP data
        TTK_THRESHOLD = 15.0  # Don't refresh if target HP < 15%
        target_hp = state.get('thp', 100)
        target_valid = state.get('target_valid', True)
        ttk_block = target_valid and target_hp > 0 and target_hp < TTK_THRESHOLD
        if "refresh_dot_vt" in condition_name:
            # Shadow Priest VT maps to Dot Slot 0 (P11)
            # Skip refresh if target is dying
            if ttk_block:
                return False
            # Refresh at pandemic (<=6s remaining for safety margin)
            dots = state.get('dots', [0.0, 0.0, 0.0])
            return dots[0] <= 6.0 if len(dots) > 0 else True
            
        if "refresh_dot_swp" in condition_name:
            # Shadow Priest SWP maps to Dot Slot 1 (P12)
            if ttk_block:
                return False
            # Refresh at pandemic (<=6s remaining)
            dots = state.get('dots', [0.0, 0.0, 0.0])
            return dots[1] <= 6.0 if len(dots) > 1 else True

        # --- INDEXED DOT REFRESH (Universal) ---
        # Format: "refresh_dot:0", "refresh_dot:1", "refresh_dot:2"
        if "refresh_dot:" in condition_name:
            # Skip refresh if target is dying
            if ttk_block:
                return False
            try:
                idx = int(condition_name.split(':')[-1])
                dots = state.get('dots', [])
                if idx < len(dots):
                    # Use 4.5s as default pandemic window
                    return dots[idx] <= 4.5
            except:
                pass
            return True  # Default to True if can't parse (safer to cast than miss)

        # --- GENERIC DOT REFRESH (Fallback) ---
        if "refresh_dot" in condition_name or "dot_missing" in condition_name:
            if ttk_block:
                return False
            # Check first dot slot as fallback
            dots = state.get('dots', [0.0])
            if len(dots) > 0:
                return dots[0] < 4.5
            # Fallback to target_dot_remaining for backwards compat
            return state.get('target_dot_remaining', 0) < 4.5
        
        # --- HOT REFRESH (Healers) ---
        # Format: "refresh_hot:0", "refresh_hot:1" - uses same dot tracking slots
        if "refresh_hot:" in condition_name:
            try:
                idx = int(condition_name.split(':')[-1])
                hots = state.get('dots', [])  # HoTs share the same tracking slots
                if idx < len(hots):
                    return hots[idx] <= 4.5  # Pandemic window
            except:
                pass
            return True
        
        # --- CHI (Monk) ---
        if condition_name.startswith("chi_gte_"):
            try:
                threshold = int(condition_name.split("_")[-1])
                return state.get('secondary_power', 0) >= threshold
            except:
                return True
        
        # --- TEACHINGS OF THE MONASTERY (Mistweaver Fistweaving) ---
        if condition_name == "teachings_stacks_high":
            # Cast Blackout Kick when we have high stacks
            return state.get('teachings_stacks', 0) >= 3
        
        # --- TARGET HP CONDITIONS ---
        if condition_name == "target_hp_lt_35":
            return state.get('thp', 100) < 35

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
        
        # --- EXECUTE PHASE ---
        # Execute threshold is configurable per-spec (talents like Massacre = 35%, Searing Touch = 30%)
        if condition_name == "execute_range":
            # Read spec-specific threshold from state (set by StateEngine from spec config)
            threshold = state.get('execute_threshold', 20)
            return state.get('thp', 100) < threshold
        
        # --- EXECUTE OR PROC (e.g., Paladin Hammer of Wrath with Avenging Wrath) ---
        if condition_name == "execute_range_or_proc":
            threshold = state.get('execute_threshold', 20)
            # Either in execute range OR has sudden death proc (P15)
            # OR has avenging wrath active (Ret Paladin)
            return (state.get('thp', 100) < threshold) or \
                   state.get('sudden_death_proc', False) or \
                   state.get('avenging_wrath_active', False)
        
        # --- VOIDFORM (Shadow Priest) ---
        if condition_name == "voidform_active":
            # TODO: Need addon pixel for Voidform buff
            # For now, check if high insanity (proxy for voidform)
            return state.get('power', 0) > 85
        
        # --- BURST ALIGNMENT ---
        if condition_name == "burst_aligned":
            # Use CDs when high resource or target nearly full HP (pull)
            power = state.get('power', 0)
            target_hp = state.get('thp', 100)
            return power > 80 or target_hp > 95
        
        # --- SURVIVAL ---
        if condition_name == "survival_critical":
            return state.get('hp', 100) < 40
        
        # --- INTERRUPT TIMING ---
        if condition_name == "interruptible_late_stage":
            return state.get('interruptible', False)
        
        # --- MULTI-TARGET / AOE ---
        if condition_name == "multi_target":
            # Check if there are 2+ enemy nameplates visible
            plates = state.get('total_hostile_plates', 1)
            return plates >= 2
        
        if "nearby_enemies_gte_" in condition_name:
            try:
                thresh = int(condition_name.split("_")[-1])
                return state.get('nearby_enemies_count', 0) >= thresh
            except: return True
        
        # --- COMBO POINTS / HOLY POWER ---
        # These use secondary_power which tracks combo points, holy power, chi, etc.
        if condition_name.startswith("combo_points_gte_") or condition_name.startswith("holy_power_gte_"):
            try:
                threshold = int(condition_name.split("_")[-1])
                return state.get('secondary_power', 0) >= threshold
            except:
                return True
        
        # --- SHARDS (Warlock) ---
        if condition_name.startswith("shards_gte_"):
            try:
                threshold = int(condition_name.split("_")[-1])
                return state.get('power', 0) >= threshold
            except:
                return True
        
        # --- STEALTH (Rogue) ---
        if condition_name == "stealth":
            return state.get('stealthed', False)
            
        return True

