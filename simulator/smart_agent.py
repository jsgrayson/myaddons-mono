from typing import Optional, List, Dict
from .battle_state import BattleState, TurnAction, Pet, Ability, BuffType, PetFamily
from .damage_calculator import DamageCalculator
from .special_encounters import SpecialEncounterHandler

class SmartAgent:
    def __init__(self, difficulty: float = 1.0, actor_id: str = 'enemy'):
        self.difficulty = difficulty
        self.actor_id = actor_id
        self.damage_calc = DamageCalculator()

    def decide(self, state: BattleState) -> TurnAction:
        action = self._level_1_survival(state)
        if action: return action
        action = self._level_2_strategy(state)
        if action: return action
        return self._level_3_damage(state)

    def _level_1_survival(self, state: BattleState) -> Optional[TurnAction]:
        # Determine active pets based on actor_id
        if self.actor_id == 'enemy':
            my_team = state.enemy_team
            opp_team = state.player_team
        else:
            my_team = state.player_team
            opp_team = state.enemy_team

        active_pet = my_team.get_active_pet()
        if not active_pet or not active_pet.stats.is_alive():
            return self._swap_to_best_pet(state)
        
        if active_pet.name == "Rocko":
            smash = next((ab for ab in active_pet.abilities if ab.name == "Smash"), None)
            if smash and active_pet.can_use_ability(smash): return TurnAction(self.actor_id, 'ability', ability=smash)

        return None

    def _level_2_strategy(self, state: BattleState) -> Optional[TurnAction]:
        if self.actor_id == 'enemy':
            my_team = state.enemy_team
            opp_team = state.player_team
        else:
            my_team = state.player_team
            opp_team = state.enemy_team

        active_pet = my_team.get_active_pet()
        enemy_active = opp_team.get_active_pet()
        if not enemy_active: return None
        
        if active_pet.stats.speed > enemy_active.stats.speed:
            kill_ability = self._find_kill_ability(active_pet, enemy_active)
            if kill_ability: return TurnAction(self.actor_id, 'ability', ability=kill_ability)
        
        return None

    def _level_3_damage(self, state: BattleState) -> TurnAction:
        if self.actor_id == 'enemy':
            my_team = state.enemy_team
            opp_team = state.player_team
        else:
            my_team = state.player_team
            opp_team = state.enemy_team

        active_pet = my_team.get_active_pet()
        enemy_active = opp_team.get_active_pet()
        
        best_score = -1
        best_ability = None
        
        available = [ab for ab in active_pet.abilities if active_pet.can_use_ability(ab)]
        if not available: return TurnAction(self.actor_id, 'pass')
             
        for ability in available:
            # Base score is raw power
            score = ability.power
            
            # Cooldown Bonus (Weighted Lower)
            # Only reward if ability does damage OR has special utility
            if ability.cooldown > 0:
                if ability.power > 0:
                     score += (ability.cooldown * 10) # +10 pts per turn, not +50
                else:
                     # Non-damaging CD move (Buff/Debuff)
                     # Check if we already have it? (Simulator checks utility before calling this)
                     score += 5 # Small bias towards using utility
            
            if score > best_score:
                best_score = score
                best_ability = ability
                
        return TurnAction(self.actor_id, 'ability', ability=best_ability)

    def _swap_to_best_pet(self, state: BattleState) -> TurnAction:
        if self.actor_id == 'enemy':
            my_team = state.enemy_team
        else:
            my_team = state.player_team

        best_idx = -1
        best_hp = -1
        for i, pet in enumerate(my_team.pets):
            if pet.stats.is_alive() and i != my_team.active_pet_index:
                if pet.stats.current_hp > best_hp:
                    best_hp = pet.stats.current_hp
                    best_idx = i
        return TurnAction(self.actor_id, 'swap', target_pet_index=best_idx) if best_idx != -1 else TurnAction(self.actor_id, 'pass')

    def _find_kill_ability(self, attacker: Pet, defender: Pet) -> Optional[Ability]:
        for ab in attacker.abilities:
            if attacker.can_use_ability(ab):
                if ab.power >= defender.stats.current_hp: return ab
        return None

    def _find_highest_damage_ability(self, attacker: Pet, defender: Pet) -> Optional[Ability]:
        best = None
        best_dmg = -1
        for ab in attacker.abilities:
            if attacker.can_use_ability(ab):
                if ab.power > best_dmg:
                    best_dmg = ab.power
                    best = ab
        return best


def create_smart_enemy_agent(difficulty: float = 1.0, ability_priorities: Optional[Dict[int, List[int]]] = None):
    """
    Create an enemy agent with optional ability priority synergy.
    
    Args:
        difficulty: AI difficulty (not currently used, kept for compatibility)
        ability_priorities: Dict mapping pet_index -> list of ability IDs in priority order
                           e.g., {1: [6, 5]} means Beakmaster should prefer Wind-Up (6) over Shock and Awe (5)
    
    Returns:
        A decision function that can be passed to create_npc_agent
    """
    base_agent = SmartAgent(difficulty=difficulty, actor_id='enemy')
    
    if not ability_priorities:
        # No priorities = use base SmartAgent
        return base_agent.decide
    
    def synergy_decide(state: BattleState) -> TurnAction:
        """Enhanced decision with ability synergy priorities"""
        # Use base agent for survival/strategy layers
        action = base_agent._level_1_survival(state)
        if action: return action
        
        action = base_agent._level_2_strategy(state)
        if action: return action
        
        # Custom Level 3: Apply priority-based synergy
        active_pet = state.enemy_team.get_active_pet()
        if not active_pet: return TurnAction('enemy', 'pass')
        
        pet_idx = state.enemy_team.active_pet_index
        priority_list = ability_priorities.get(pet_idx, [])
        
        if priority_list:
            # Try abilities in priority order (for combos like Wind-Up -> Shock and Awe)
            for ability_id in priority_list:
                for ab in active_pet.abilities:
                    if ab.id == ability_id and active_pet.can_use_ability(ab):
                        return TurnAction('enemy', 'ability', ability=ab)
        
        # Fallback to base damage logic
        return base_agent._level_3_damage(state)
    
    return synergy_decide