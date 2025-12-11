from typing import Callable, Optional, List
from .battle_state import BattleState, TurnAction
from .npc_move_loader import get_move_orders
from .smart_agent import SmartAgent

try:
    from .npc_ai_loader import load_encounter_ai
    AI_LOADER_AVAILABLE = True
except ImportError:
    AI_LOADER_AVAILABLE = False
    print("⚠️  NPC AI Loader not available, using fallback logic")

_NPC_PRIORITIES_CACHE = None

def create_npc_agent(npc_name: str, default_ai: Optional[Callable[[BattleState], TurnAction]] = None, priority_script: Optional[List] = None) -> Callable[[BattleState], TurnAction]:
    """
    Creates an NPC agent with Enhanced AI Script Support.
    Now uses real enemy AI scripts when available.
    """
    move_orders = get_move_orders()
    npc_moves = move_orders.get(npc_name, {})
    
    # Try to load enhanced AI for this encounter
    enhanced_ai = None
    if AI_LOADER_AVAILABLE:
        enhanced_ai = load_encounter_ai(npc_name)
        if enhanced_ai:
            print(f"✅ Using enhanced AI for: {npc_name}")
    
    if default_ai is None:
        smart_agent = SmartAgent(difficulty=1.0)
        default_ai = smart_agent.decide

    # Load extracted priorities if available (Cached)
    # Only load if we don't have an injected script
    global _NPC_PRIORITIES_CACHE
    if not priority_script and _NPC_PRIORITIES_CACHE is None:
        import json
        import os
        _NPC_PRIORITIES_CACHE = {}
        try:
            if os.path.exists('npc_ai_priorities.json'):
                with open('npc_ai_priorities.json', 'r') as f:
                    _NPC_PRIORITIES_CACHE = json.load(f)
                    print(f"✅ Loaded {len(_NPC_PRIORITIES_CACHE)} AI priority scripts")
        except Exception as e:
            print(f"⚠️ Failed to load AI priorities: {e}")
    
    npc_priorities = _NPC_PRIORITIES_CACHE or {}

    def npc_agent(state: BattleState) -> TurnAction:
        enemy_team = state.enemy_team
        active_pet = enemy_team.get_active_pet()
        
        # 0. DEATH CHECK (Critical Fix)
        if active_pet and not active_pet.stats.is_alive():
            for i, p in enumerate(enemy_team.pets):
                if p.stats.is_alive():
                    return TurnAction(actor='enemy', action_type='swap', target_pet_index=i)
            return TurnAction(actor='enemy', action_type='pass')

        if not active_pet:
            return TurnAction(actor='enemy', action_type='pass')

        player_pet = state.player_team.get_active_pet()
        current_round = state.turn_number

        # 1. CHECK EXTRACTED PRIORITIES (NEW)
        # Use injected script if available, otherwise check cache
        script_to_use = priority_script
        
        if not script_to_use:
            # Construct key for current team: "id1,id2,id3"
            team_key = ",".join(str(p.species_id) for p in enemy_team.pets)
            script_to_use = npc_priorities.get(team_key)
        
        if script_to_use:
            # Evaluate script
            for step in script_to_use:
                # Check condition
                condition_met = True
                if step.get('condition'):
                    cond = step['condition']
                    # Simple condition parsing
                    if 'round=' in cond:
                        try:
                            req_round = int(cond.split('round=')[1].split(']')[0].strip())
                            if current_round != req_round: condition_met = False
                        except: pass
                    
                    # Add more condition parsing here as needed (e.g., hp checks)
                    # For now, round checks are the most critical for fixed rotations
                
                if condition_met:
                    if step['type'] == 'ability':
                        ability_id = step['id']
                        matching = next((ab for ab in active_pet.abilities if ab.id == ability_id), None)
                        if matching and active_pet.can_use_ability(matching):
                            return TurnAction(actor='enemy', action_type='ability', ability=matching)
                    
                    elif step['type'] == 'change':
                        target = step['target']
                        target_idx = -1
                        if target == 'next':
                            # Find next alive pet
                            for i in range(len(enemy_team.pets)):
                                if i != enemy_team.active_pet_index and enemy_team.pets[i].stats.is_alive():
                                    target_idx = i
                                    break
                        elif target.startswith('#'):
                            try:
                                # #1 is index 0, #2 is index 1, etc.
                                idx = int(target.replace('#', '')) - 1
                                if 0 <= idx < len(enemy_team.pets) and enemy_team.pets[idx].stats.is_alive():
                                    target_idx = idx
                            except: pass
                        
                        if target_idx != -1:
                            return TurnAction(actor='enemy', action_type='swap', target_pet_index=target_idx)
                    
                    elif step['type'] == 'pass':
                        return TurnAction(actor='enemy', action_type='pass')

        # Special AI for Enok the Stinky
        if npc_name == "Enok the Stinky":
            # Rotation: 1. Bash Punch (119), 2. Whirlpool (506), 3. Healing Wrap (Custom/420 placeholder)
            # Cycle: 1, 2, 3, 1, 2, 3...
            cycle_pos = (current_round - 1) % 3
            
            # Map cycle position to ability slot (0-indexed)
            # Slot 0: Punch (119)
            # Slot 1: Whirlpool (506)
            # Slot 2: Healing Wrap (We need to ensure this is in slot 2)
            
            target_slot = 0
            if cycle_pos == 1: target_slot = 1
            elif cycle_pos == 2: target_slot = 2
            
            if target_slot < len(active_pet.abilities):
                ability = active_pet.abilities[target_slot]
                if active_pet.can_use_ability(ability):
                    return TurnAction(actor='enemy', action_type='ability', ability=ability)
        if enhanced_ai:
            # A. Priority abilities [round=1]
            for priority in enhanced_ai.get('priority_abilities', []):
                if f'[round={current_round}]' in priority['condition']:
                    matching = next((ab for ab in active_pet.abilities if ab.id == priority['id']), None)
                    if matching and active_pet.can_use_ability(matching):
                        return TurnAction(actor='enemy', action_type='ability', ability=matching)
            
            # B. HP-based conditionals
            for hp_cond in enhanced_ai.get('hp_conditionals', []):
                condition = hp_cond['condition']
                
                # Parse HP condition (e.g., "[enemy.hp>1000]")
                import re
                hp_match = re.search(r'enemy\.hp([><=]+)(\d+)', condition)
                if hp_match:
                    operator = hp_match.group(1)
                    threshold = int(hp_match.group(2))
                    
                    # Check if condition is met
                    check_passed = False
                    if operator == '>' and active_pet.stats.current_hp > threshold:
                        check_passed = True
                    elif operator == '<' and active_pet.stats.current_hp < threshold:
                        check_passed = True
                    elif operator == '<=' and active_pet.stats.current_hp <= threshold:
                        check_passed = True
                    elif operator == '>=' and active_pet.stats.current_hp >= threshold:
                        check_passed = True
                    
                    if check_passed:
                        matching = next((ab for ab in active_pet.abilities if ab.id == hp_cond['id']), None)
                        if matching and active_pet.can_use_ability(matching):
                            return TurnAction(actor='enemy', action_type='ability', ability=matching)
            
            # C. General rotation (use first available)
            for ability in enhanced_ai.get('general_rotation', []):
                matching = next((ab for ab in active_pet.abilities if ab.id == ability['id']), None)
                if matching and active_pet.can_use_ability(matching):
                    return TurnAction(actor='enemy', action_type='ability', ability=matching)

        # 2. Fallback: Check Scripted Move (legacy)
        pet_moves = npc_moves.get(enemy_team.active_pet_index, {})
        predicted_name = pet_moves.get(current_round)
        
        if predicted_name:
            matching = next((ab for ab in active_pet.abilities if ab.name == predicted_name), None)
            if matching and active_pet.can_use_ability(matching):
                return TurnAction(actor='enemy', action_type='ability', ability=matching)

        # 3. Priority Logic (legacy fallback)
        
        # A. Kill Shot
        for abil in active_pet.abilities:
            if active_pet.can_use_ability(abil):
                if abil.power >= player_pet.stats.current_hp:
                     return TurnAction(actor='enemy', action_type='ability', ability=abil)
        
        # B. Cooldowns (Smart Check)
        if len(active_pet.abilities) > 2:
            slot3 = active_pet.abilities[2]
            if active_pet.can_use_ability(slot3):
                if "Heal" in slot3.name and active_pet.stats.current_hp > active_pet.stats.max_hp * 0.9: pass
                else: return TurnAction(actor='enemy', action_type='ability', ability=slot3)

        if len(active_pet.abilities) > 1:
            slot2 = active_pet.abilities[1]
            if active_pet.can_use_ability(slot2):
                if "Heal" in slot2.name and active_pet.stats.current_hp > active_pet.stats.max_hp * 0.9: pass
                else: return TurnAction(actor='enemy', action_type='ability', ability=slot2)

        # C. Spam Slot 1
        slot1 = active_pet.abilities[0]
        return TurnAction(actor='enemy', action_type='ability', ability=slot1)

    return npc_agent
