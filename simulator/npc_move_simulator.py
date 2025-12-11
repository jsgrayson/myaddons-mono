"""
Enhanced NPC Move Order Simulator

Combines:
1. Enhanced AI scripts (priority, HP conditionals, rotation)
2. Cooldown-aware fallback logic
3. Never-pass guarantee
"""

def simulate_npc_move_order_enhanced(pet_data, enhanced_ai=None, observations=None, max_rounds=15, current_hp=None, max_hp=None):
    """
    Generate move order using enhanced AI when available.
    
    Priority:
    1. Enhanced AI priority abilities [round=X]
    2. Enhanced AI HP conditionals
    3. Enhanced AI general rotation
    4. Cooldown-based fallback (3 > 2 > 1)
    5. Force Slot 1 if nothing usable
    """
    move_order = []
    abilities = pet_data['abilities']
    cooldowns = {ab['id']: 0 for ab in abilities}
    observations = observations or {}
    
    # Current HP tracking (if not provided, assume full health)
    if current_hp is None:
        current_hp = max_hp or 1500
    if max_hp is None:
        max_hp = current_hp
    
    # Sort abilities by priority for fallback
    sorted_abilities = sorted(abilities, key=lambda x: abilities.index(x), reverse=True)

    for round_num in range(1, max_rounds + 1):
        selected_ability = None
        usable = [ab for ab in abilities if cooldowns[ab['id']] == 0]
        
        # 1. Try Enhanced AI Script Logic
        if enhanced_ai:
            # A. Priority abilities [round=N]
            for priority in enhanced_ai.get('priority_abilities', []):
                if f'[round={round_num}]' in priority['condition']:
                    matching = next((ab for ab in usable if ab['id'] == priority['id']), None)
                    if matching:
                        selected_ability = matching
                        break
            
            # B. HP conditionals (if not found in priority)
            if not selected_ability:
                for hp_cond in enhanced_ai.get('hp_conditionals', []):
                    condition = hp_cond['condition']
                    
                    import re
                    hp_match = re.search(r'enemy\.hp([><=]+)(\d+)', condition)
                    if hp_match:
                        operator = hp_match.group(1)
                        threshold = int(hp_match.group(2))
                        
                        check_passed = False
                        if operator == '>' and current_hp > threshold:
                            check_passed = True
                        elif operator == '<' and current_hp < threshold:
                            check_passed = True
                        elif operator == '<=' and current_hp <= threshold:
                            check_passed = True
                        elif operator == '>=' and current_hp >= threshold:
                            check_passed = True
                        
                        if check_passed:
                            matching = next((ab for ab in usable if ab['id'] == hp_cond['id']), None)
                            if matching:
                                selected_ability = matching
                                break
            
            # C. General rotation
            if not selected_ability:
                for ability in enhanced_ai.get('general_rotation', []):
                    matching = next((ab for ab in usable if ab['id'] == ability['id']), None)
                    if matching:
                        selected_ability = matching
                        break
        
        # 2. Fallback: Observation-based hints
        if not selected_ability:
            obs = observations.get(round_num, [])
            is_nuke_turn = "nuke" in obs
            
            if usable:
                if is_nuke_turn:
                    selected_ability = max(usable, key=lambda x: x.get('cooldown', 0))
                else:
                    selected_ability = usable[0]
        
        # 3. CRITICAL FIX: NEVER PASS
        if not selected_ability:
            if not usable and abilities:
                # Force Slot 1 (Basic Attack)
                selected_ability = abilities[0]
            elif not abilities:
                move_order.append("Pass")
                continue
            else:
                selected_ability = usable[0]
        
        # Execute
        move_order.append(selected_ability['name'])
        
        # Tick Cooldowns
        for ab_id in cooldowns:
            if cooldowns[ab_id] > 0:
                cooldowns[ab_id] -= 1
        
        # Set new cooldown
        cooldowns[selected_ability['id']] = selected_ability.get('cooldown', 0)
    
    return move_order
