"""
Turn System for Pet Battle Simulator

Handles turn order determination based on speed and priority.
Implements the rules for who acts first in each round.
"""

from typing import List, Tuple, Optional
import random
from .battle_state import Pet, Ability, Team, TurnAction, PetFamily
from .racial_passives import RacialPassives


class TurnSystem:
    """Manages turn order and action execution sequencing"""
    
    def __init__(self, rng_seed: Optional[int] = None):
        """Initialize with optional RNG seed for reproducibility"""
        self.rng = random.Random(rng_seed)
    
    def get_effective_speed(self, pet: Pet, ability: Ability) -> int:
        """
        Calculate effective speed for this turn
        
        Base speed modified by:
        - Pet's current speed stat (with buffs)
        - Ability speed modifier
        - Status effects (stun = 0 speed)
        """
        # Check if stunned/frozen
        for buff in pet.active_buffs:
            if buff.type.value in ['stun', 'frozen', 'sleep']:
                return -1  # Acts last
        
        # Get buffed speed
        base_speed = pet.get_effective_speed()
        
        # Apply Flying racial passive (+50% speed if above 50% HP)
        if pet.family == PetFamily.FLYING:
            speed_mult = RacialPassives.apply_flying_passive(pet)
            base_speed = int(base_speed * speed_mult)
        
        # Apply ability speed modifier
        effective_speed = base_speed + ability.speed
        
        return max(0, effective_speed)
    
    def determine_turn_order(
        self,
        player_pet: Pet,
        player_action: TurnAction,
        enemy_pet: Pet,
        enemy_action: TurnAction
    ) -> List[Tuple[str, TurnAction]]:
        """
        Determine who acts first this turn
        
        Returns list of (actor, action) tuples in execution order
        
        Rules:
        1. Swaps always happen first (before attacks)
        2. Priority abilities go before normal abilities regardless of speed
        3. Higher speed acts first
        4. If tied, 50/50 random
        """
        player_tuple = ('player', player_action)
        enemy_tuple = ('enemy', enemy_action)
        
        # Rule 1: Swaps first
        player_is_swap = player_action.action_type == 'swap'
        enemy_is_swap = enemy_action.action_type == 'swap'
        
        if player_is_swap and enemy_is_swap:
            # Both swapping - player goes first (game rule)
            return [player_tuple, enemy_tuple]
        elif player_is_swap:
            return [player_tuple, enemy_tuple]
        elif enemy_is_swap:
            return [enemy_tuple, player_tuple]
        
        # Rule 2: Priority abilities
        player_priority = 0
        enemy_priority = 0
        
        if player_action.ability:
            player_priority = player_action.ability.priority
        if enemy_action.ability:
            enemy_priority = enemy_action.ability.priority
            
        # DEBUG: Print priorities
        # print(f"DEBUG: Turn Order Check - Player Prio: {player_priority}, Enemy Prio: {enemy_priority}")
        # if player_action.ability: print(f"DEBUG: Player Ability: {player_action.ability.name} (Prio: {player_action.ability.priority})")
        # if enemy_action.ability: print(f"DEBUG: Enemy Ability: {enemy_action.ability.name} (Prio: {enemy_action.ability.priority})")
        
        if player_priority > enemy_priority:
            return [player_tuple, enemy_tuple]
        elif enemy_priority > player_priority:
            return [enemy_tuple, player_tuple]
        
        # Rule 3 & 4: Speed check (with tiebreaker)
        if player_action.ability and enemy_action.ability:
            player_speed = self.get_effective_speed(player_pet, player_action.ability)
            enemy_speed = self.get_effective_speed(enemy_pet, enemy_action.ability)
            
            if player_speed > enemy_speed:
                return [player_tuple, enemy_tuple]
            elif enemy_speed > player_speed:
                return [enemy_tuple, player_tuple]
            else:
                # Tied - 50/50 random
                if self.rng.random() < 0.5:
                    return [player_tuple, enemy_tuple]
                else:
                    return [enemy_tuple, player_tuple]
        
        # Default: player first
        return [player_tuple, enemy_tuple]
    
    def can_act(self, pet: Pet) -> bool:
        """Check if pet can take action this turn"""
        # Dead pets can't act
        if not pet.stats.is_alive():
            return False
        
        # Check for status effects that prevent action
        for buff in pet.active_buffs:
            if buff.type.value in ['stun', 'frozen', 'sleep']:
                return False
        
        return True
    
    def get_available_abilities(self, pet: Pet) -> List[Ability]:
        """Get list of abilities pet can use this turn"""
        if not self.can_act(pet):
            return []
        
        available = []
        for ability in pet.abilities:
            if pet.can_use_ability(ability):
                available.append(ability)
        
        return available
