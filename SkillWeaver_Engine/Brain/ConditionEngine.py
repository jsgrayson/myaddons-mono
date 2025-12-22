class ConditionEngine:
    @staticmethod
    def evaluate(condition_name, state):
        """
        Evaluates a string condition from the JSON spec against the current game state.
        """
        # --- UNIVERSAL CONDITIONS ---
        if condition_name == "target_valid":
            return state.get('thp', 0) > 0
            
        if condition_name == "combat_check":
            return state.get('combat', False)

        # --- ROGUE CONDITIONS (Assassination, Outlaw, Subtlety) ---
        if condition_name == "combo_points_4_plus":
            return state.get('sec', 0) >= 4
            
        if condition_name == "energy_pool_check":
            return state.get('power', 0) > 50

        if condition_name == "stealth_check_ambush":
            # If we don't have a stealth pixel, assume true in combat for now
            return True

        # --- WARLOCK CONDITIONS (Destruction) ---
        if condition_name == "shards_builder":
            return state.get('sec', 0) < 5
            
        if condition_name == "backdraft_gate_spender":
            # Chaos Bolt logic: only cast if shards > 1
            return state.get('sec', 0) >= 2

        # --- FALLBACKS ---
        # If we don't have telemetry for a specific aura (e.g. Pandemic),
        # we return True to avoid blocking the basic rotation flow.
        if "pandemic_gate" in condition_name:
            return True
        if "stealth_check" in condition_name:
            return True
        if "burst_window" in condition_name:
            return state.get('combat', False)
            
        return True
