"""
Racial Passive System for Pet Battle Simulator

Implements the racial passive abilities for all 10 pet families.
These are core mechanics that apply to every pet based on their family type.

References:
- Undead: Revive for 1 turn when killed (Shadowlands mechanic)
- Magic: Cannot take more than 35% max HP in one hit
- Mechanical: Revive once per battle to 20% HP
- And 7 others...
"""

from typing import Optional
from .battle_state import Pet, PetFamily


class RacialPassives:
    """Handles racial passive abilities for all 10 pet families"""
    
    @staticmethod
    def apply_beast_passive(pet: Pet) -> float:
        """
        Beast: +25% damage dealt when below 50% health
        
        Args:
            pet: The beast pet
            
        Returns:
            Damage multiplier (1.25 if below 50% HP, 1.0 otherwise)
        """
        if pet.stats.current_hp < (pet.stats.max_hp * 0.5):
            return 1.25
        return 1.0
    
    @staticmethod
    def apply_critter_passive(pet: Pet) -> float:
        """
        Critter: Immune to stun, root, and sleep effects.
        
        Note: This method returns damage modifier (which is 0 for Critter usually, or handled elsewhere).
        Wait, the previous implementation was: "Immune to CC".
        The damage part was removed in the new spec?
        Old spec: "+50% damage above 50% HP" (This was standard WoW logic).
        New spec: "Immune to stun, root, and sleep effects."
        
        We need to keep the damage part if it's still valid, but the user explicitly listed "Immune to stun..."
        The table in the prompt says:
        | Critter | Critter | Immune to stun, root, and sleep effects. |
        
        It does NOT mention the damage bonus.
        However, standard WoW Critter passive IS immunity to CC.
        The "damage bonus" I implemented earlier might have been a misunderstanding or from a different version?
        Actually, standard WoW Critter passive is "Immune to CC".
        The "damage bonus" I implemented was likely incorrect or from a mod.
        I will REMOVE the damage bonus and implement the CC immunity check.
        
        But this method returns a float (damage mod).
        I should change it to return 1.0 (no damage mod) and handle CC immunity in buff_tracker.
        """
        return 1.0
    
    @staticmethod
    def check_dragonkin_trigger(pet: Pet, previous_hp: int) -> bool:
        """
        Dragonkin: Deals 50% extra damage the round after reducing an enemy below 25% health.
        
        Args:
            pet: The Dragonkin pet (attacker)
            previous_hp: The defender's HP before the attack
            
        Note: This is checked AFTER damage is dealt. We need to know if the target FELL below 25%.
        But wait, the spec says "reducing an enemy below 25%".
        So we check if previous_hp > 25% max and current_hp <= 25% max.
        """
        # This method is called with the DEFENDER as 'pet' in simulator.py currently?
        # Let's check simulator.py usage.
        # Simulator calls: check_dragonkin_trigger(defender, previous_hp)
        # So 'pet' here is the defender.
        
        threshold = pet.stats.max_hp * 0.25
        current_hp = pet.stats.current_hp
        
        return previous_hp > threshold and current_hp <= threshold
    
    @staticmethod
    def apply_dragonkin_passive(pet: Pet) -> float:
        """
        Dragonkin: +50% damage on next attack (if buff is ready)
        
        Args:
            pet: The dragonkin pet
            
        Returns:
            Damage multiplier (1.5 if buff ready, 1.0 otherwise)
        """
        if hasattr(pet, 'dragonkin_buff_ready') and pet.dragonkin_buff_ready:
            return 1.5
        return 1.0
    
    @staticmethod
    def consume_dragonkin_buff(pet: Pet):
        """
        Consume the dragonkin damage buff after it's been used
        
        Args:
            pet: The dragonkin pet
        """
        if hasattr(pet, 'dragonkin_buff_ready'):
            pet.dragonkin_buff_ready = False
    
    @staticmethod
    def apply_flying_passive(pet: Pet) -> float:
        """
        Flying: +50% speed when above 50% HP
        
        Args:
            pet: The flying pet
            
        Returns:
            Speed multiplier (1.5 if above 50% HP, 1.0 otherwise)
        """
        if pet.stats.current_hp > (pet.stats.max_hp * 0.5):
            return 1.5
        return 1.0
    
    @staticmethod
    def apply_humanoid_passive(pet: Pet, damage_dealt: int) -> int:
        """
        Humanoid: Recover 4% of max HP when dealing damage
        
        Args:
            pet: The humanoid pet that dealt damage
            damage_dealt: Amount of damage dealt
            
        Returns:
            Amount of HP healed
        """
        heal_amount = int(pet.stats.max_hp * 0.04)
        actual_heal = pet.stats.heal(heal_amount)
        return actual_heal
    
    @staticmethod
    def apply_magic_passive(pet: Pet, incoming_damage: int, hits: int = 1) -> int:
        """
        Magic: Cannot take more than 35% of max HP in one hit
        
        Args:
            pet: The magic pet receiving damage
            incoming_damage: Total damage before cap
            hits: Number of hits in the ability
            
        Returns:
            Capped damage amount
        """
        # Cap applies PER HIT.
        # So total cap = (35% max HP) * hits
        cap_per_hit = int(pet.stats.max_hp * 0.35)
        total_cap = cap_per_hit * hits
        
        return min(incoming_damage, total_cap)
    
    @staticmethod
    def apply_aquatic_passive() -> float:
        """
        Aquatic: Harmful Damage Over Time effects are reduced by 50%.
        
        Note: The previous implementation was "+25% healing".
        The new spec says "DoT reduced by 50%".
        It does NOT mention healing.
        Standard WoW Aquatic passive IS "DoT reduced by 50%".
        I will remove the healing bonus and implement DoT reduction.
        
        This method was returning healing modifier.
        I'll change it to return 1.0 (no healing mod).
        """
        return 1.0
    
    @staticmethod
    def apply_elemental_passive() -> bool:
        """
        Elemental: Immune to weather damage (DoTs from weather)
        
        Returns:
            True (immune to weather damage)
        """
        return True
    
    @staticmethod
    def apply_undead_passive(pet: Pet) -> bool:
        """
        Undead: Revive for 1 turn when killed
        
        This is THE SHADOWLANDS MECHANIC - when an Undead pet dies,
        it comes back for one final attack before truly dying.
        
        Args:
            pet: The undead pet that just died
            
        Returns:
            True if pet should revive, False otherwise
        """
        # Check if this pet has already used its revive
        if not hasattr(pet, 'has_used_undead_revive'):
            pet.has_used_undead_revive = False
        
        if not pet.has_used_undead_revive:
            # Mark that we're in revive mode
            pet.has_undead_revive = True
            pet.revive_turns_remaining = 1
            pet.has_used_undead_revive = True
            return True
        
        return False
    
    @staticmethod
    def apply_mechanical_passive(pet: Pet) -> bool:
        """
        Mechanical: Comes back to life once per battle, returning to 25% health.
        
        Returns:
            True if revived, False otherwise
        """
        if not hasattr(pet, 'has_used_mechanical_revive'):
            pet.has_used_mechanical_revive = False
            
        if not pet.has_used_mechanical_revive:
            # Revive to 25% HP
            pet.stats.current_hp = int(pet.stats.max_hp * 0.25)
            pet.has_used_mechanical_revive = True
            return True
        
        return False
    
    @staticmethod
    def get_damage_modifier(pet: Pet) -> float:
        """
        Get the damage modifier for a pet based on its racial passive
        
        Args:
            pet: The attacking pet
            
        Returns:
            Damage multiplier to apply
        """
        if pet.family == PetFamily.BEAST:
            return RacialPassives.apply_beast_passive(pet)
        
        if pet.family == PetFamily.CRITTER:
            return RacialPassives.apply_critter_passive(pet)
        
        if pet.family == PetFamily.DRAGONKIN:
            return RacialPassives.apply_dragonkin_passive(pet)
        
        # Default: no modifier
        return 1.0
    
    @staticmethod
    def get_speed_modifier(pet: Pet) -> float:
        """
        Get the speed modifier for a pet based on its racial passive
        
        Args:
            pet: The pet to check
            
        Returns:
            Speed multiplier to apply
        """
        if pet.family == PetFamily.FLYING:
            return RacialPassives.apply_flying_passive(pet)
        
        # Default: no modifier
        return 1.0
    
    @staticmethod
    def get_healing_modifier(pet: Pet) -> float:
        """
        Get the healing modifier for a pet based on its racial passive
        
        Args:
            pet: The pet receiving/giving healing
            
        Returns:
            Healing multiplier to apply
        """
        if pet.family == PetFamily.AQUATIC:
            return RacialPassives.apply_aquatic_passive()
        
        # Default: no modifier
        return 1.0
