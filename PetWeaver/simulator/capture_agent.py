from .smart_agent import SmartAgent
from .battle_state import TurnAction, BattleState

class CaptureAgent(SmartAgent):
    """
    Specialized agent for capturing pets.
    Prioritizes lowering enemy HP to <35% without killing.
    """
    
    def get_action(self, state: BattleState) -> TurnAction:
        active_pet = state.player_team.get_active_pet()
        enemy_pet = state.enemy_team.get_active_pet()
        
        if not active_pet or not enemy_pet:
            return TurnAction(actor='player', action_type='pass')
            
        # Calculate enemy HP percentage
        hp_pct = (enemy_pet.stats.current_hp / enemy_pet.stats.max_hp) * 100
        capture_threshold = 35.0
        
        # 1. If in capture range, maintain status quo (don't kill)
        if hp_pct < capture_threshold:
            # Check if we have a non-damaging move
            non_damaging_moves = []
            for ability in active_pet.abilities:
                if active_pet.can_use_ability(ability):
                    # Heals, buffs, or 0 power moves
                    if ability.power == 0 or ability.is_heal:
                        non_damaging_moves.append(ability)
                        
            if non_damaging_moves:
                # Use random non-damaging move
                return TurnAction(actor='player', action_type='ability', ability=non_damaging_moves[0])
            
            # If all moves deal damage, try swapping
            living_pets = [i for i, p in enumerate(state.player_team.pets) 
                          if p.stats.is_alive() and i != state.player_team.active_pet_index]
            if living_pets:
                return TurnAction(actor='player', action_type='swap', target_pet_index=living_pets[0])
                
            # If must attack, try to find one that won't kill (unlikely if power > 0)
            # Or just PASS
            return TurnAction(actor='player', action_type='pass')
            
        # 2. If above threshold, attack carefully
        else:
            # Calculate damage for all available abilities
            safe_abilities = []
            best_ability = None
            max_safe_damage = -1
            
            for ability in active_pet.abilities:
                if active_pet.can_use_ability(ability):
                    # Calculate BASE damage first (no variance/crit)
                    # We need to peek into damage calculator or estimate it
                    # Since calculate_damage returns final randomized damage, we'll run it once
                    # and assume worst case (Crit + Max Variance)
                    
                    # Standard damage (avg)
                    avg_dmg, _ = self.damage_calculator.calculate_damage(active_pet, enemy_pet, ability, state.weather)
                    
                    # Estimate Max Crit Damage
                    # Variance is +/- 5% (1.05)
                    # Crit is 1.5x
                    # So Max = Avg * 1.05 * 1.5 approx? 
                    # Actually calculate_damage includes variance.
                    # Let's assume the returned value is "normal hit".
                    # Max possible = (Avg / 0.95) * 1.05 * 1.5 = Avg * 1.66 roughly
                    
                    max_possible_dmg = int(avg_dmg * 1.7) 
                    
                    # Check if lethal
                    will_kill_guaranteed = avg_dmg >= enemy_pet.stats.current_hp
                    could_kill_crit = max_possible_dmg >= enemy_pet.stats.current_hp
                    
                    # If it has "cannot_kill" flag (False Swipe), it's always safe
                    if getattr(ability, 'cannot_kill', False):
                        safe_abilities.append((ability, avg_dmg))
                        if avg_dmg > max_safe_damage:
                            max_safe_damage = avg_dmg
                            best_ability = ability
                            
                    # Otherwise, only use if it won't kill even on crit
                    elif not could_kill_crit:
                        safe_abilities.append((ability, avg_dmg))
                        if avg_dmg > max_safe_damage:
                            max_safe_damage = avg_dmg
                            best_ability = ability
                            
            if best_ability:
                return TurnAction(actor='player', action_type='ability', ability=best_ability)
                
            # If no safe attacks (all will kill), try non-damaging
            non_damaging_moves = [a for a in active_pet.abilities 
                                 if active_pet.can_use_ability(a) and a.power == 0]
            if non_damaging_moves:
                return TurnAction(actor='player', action_type='ability', ability=non_damaging_moves[0])
                
            # If forced to kill or pass... PASS to avoid killing
            return TurnAction(actor='player', action_type='pass')
