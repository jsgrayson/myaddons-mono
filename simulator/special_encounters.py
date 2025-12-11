"""
Special Encounter Handler for Pet Battle Simulator

Handles unique gimmick fight mechanics that are specific to certain encounters.
These are NOT racial passives - they are fight-specific mechanics.

Examples:
- Rocko: Immune for 10 rounds, then dies
- Life Exchange: Swap health percentages
- Gore Stacks: Increasing DoT
- Mind Games: 5-round stun + % health damage
"""

from typing import Optional
from .battle_state import Pet, Team, Buff, BuffType, PetFamily


class SpecialEncounterHandler:
    """Handles gimmick fight mechanics"""
    
    # Encounter registry: Maps species IDs to their special mechanics functions
    SPECIAL_MECHANICS = {
        # Original entries, now mapping to methods directly
        1811: 'rocko_immunity',  # Rocko (This one is special, handled by apply_rocko_immunity directly)
        1187: 'gore_stacks',     # Gorespine
        1400: 'bone_prison',     # Jawbone (Bastion)
        1300: 'life_exchange',   # Dah'da (Wrathion) - Tentative
        # New entries (if any, mapping to methods)
        # Example: 157989: apply_some_new_mechanic,
    }
    
    @staticmethod
    def has_special_mechanic(pet: Pet) -> Optional[str]:
        """Check if a pet has a special mechanic"""
        return SpecialEncounterHandler.SPECIAL_MECHANICS.get(pet.species_id)
    
    @staticmethod
    def apply_rocko_immunity(pet: Pet, turn: int) -> bool:
        """
        Rocko: Immune to all damage for 10 rounds, then dies automatically
        
        Args:
            pet: Rocko pet
            turn: Current battle turn number
            
        Returns:
            True if Rocko is immune this turn, False otherwise
        """
        if turn <= 10:
            return True  # Immune
        else:
            # Auto-die on turn 11
            pet.stats.current_hp = 0
            return False
    
    @staticmethod
    def apply_gorespine_gore(pet: Pet, turn: int):
        """
        Gorespine: Gore Stacks - Increasing DoT each round
        
        Applies or increases a stacking DoT buff
        """
        # Find existing Gore Stack buff
        gore_buff = None
        for buff in pet.active_buffs:
            if buff.type == BuffType.DOT and buff.source_ability == 99999:  # Special Gore ID
                gore_buff = buff
                break
        
        if gore_buff:
            # Increase stacks
            gore_buff.stacks += 1
            # gore_buff.magnitude += 10  # REMOVED: BuffTracker multiplies by stacks automatically
        else:
            # Create new Gore Stack
            gore_buff = Buff(
                type=BuffType.DOT,
                duration=999,  # Permanent (until pet dies)
                magnitude=10,  # 10 damage base
                source_ability=99999,  # Special Gore ID
                stacks=1
            )
            pet.active_buffs.append(gore_buff)
    
    @staticmethod
    def apply_life_exchange(attacker: Pet, defender: Pet):
        """
        Dah'da (Wrathion encounter): Life Exchange - Swap health percentages
        
        Args:
            attacker: Pet casting Life Exchange
            defender: Target pet
        """
        # Calculate current health percentages
        attacker_pct = attacker.stats.current_hp / attacker.stats.max_hp
        defender_pct = defender.stats.current_hp / defender.stats.max_hp
        
        # Swap them
        attacker.stats.current_hp = int(attacker.stats.max_hp * defender_pct)
        defender.stats.current_hp = int(defender.stats.max_hp * attacker_pct)
    
    @staticmethod
    def apply_mind_games(team: Team, active_pet: Pet):
        """
        Mind Games of Addius: Damage entire team for % of MAX HP
        
        Note: This is actually a choice mechanic (Damage vs Stun vs Lockout).
        We implement the standard strategy choice: 25% Max HP damage to team.
        """
        # Damage all pets for 25% of their MAX HP
        for pet in team.pets:
            if pet.stats.is_alive():
                damage = int(pet.stats.max_hp * 0.25)
                pet.stats.take_damage(damage)
    
    @staticmethod
    def apply_bone_prison(pet: Pet):
        """
        Jawbone (Bastion): Bone Prison - Stun target
        
        Args:
            pet: Pet to stun
        """
        stun_buff = Buff(
            type=BuffType.STUN,
            duration=2,  # 2 rounds
            magnitude=1.0,
            source_ability=77777  # Special Bone Prison ID
        )
        pet.active_buffs.append(stun_buff)
    
    @staticmethod
    def apply_toxic_skin(attacker: Pet, damage_dealt: int) -> int:
        """
        Glitterdust (Ardenweald): Toxic Skin - Reflect damage back to attacker
        
        Args:
            attacker: Pet that dealt damage
            damage_dealt: Amount of damage dealt
            
        Returns:
            Reflected damage amount
        """
        reflected = int(damage_dealt * 0.25)  # 25% reflection
        actual_reflected = attacker.stats.take_damage(reflected)
        return actual_reflected
    
    @staticmethod
    def apply_shell_shield(pet: Pet, duration: int = 3):
        """
        Diamond (Seeker Zusshi): Shell Shield - Reduce damage by 50% for 3 rounds
        
        Args:
            pet: Pet to shield
            duration: Duration in rounds
        """
        shield_buff = Buff(
            type=BuffType.STAT_MOD,
            duration=duration,
            magnitude=0.5,  # 50% damage reduction
            stat_affected='damage_taken',
            source_ability=66666  # Special Shell Shield ID
        )
        pet.active_buffs.append(shield_buff)
    
    @staticmethod
    def apply_healing_reduction(pet: Pet, reduction_pct: float = 0.5, duration: int = 3):
        """
        Apply healing reduction debuff (common in Shadowlands encounters)
        
        Args:
            pet: Pet to debuff
            reduction_pct: Percentage to reduce healing (0.5 = 50% reduction)
            duration: Duration in rounds
        """
        healing_debuff = Buff(
            type=BuffType.STAT_MOD,
            duration=duration,
            magnitude=reduction_pct,  # 50% healing reduction by default
            stat_affected='healing_received',
            source_ability=88888,  # Special Healing Reduction ID
            name="Healing Reduction"
        )
        pet.active_buffs.append(healing_debuff)
    
    @staticmethod
    def apply_massive_team_heal(team: Team, heal_amount: int):
        """
        The Impossible Boss: Massive team healing every few turns
        
        Args:
            team: Team to heal
            heal_amount: Amount to heal each pet
        """
        for pet in team.pets:
            if pet.stats.is_alive():
                pet.stats.heal(heal_amount)
    @staticmethod
    def apply_unit_17_passive(simulator, pet: Pet, enemy_team: Team):
        """
        Unit 17 Passive: Takes 50% reduced damage.
        Implemented as a permanent 50% damage reduction buff.
        """
        # Check if already applied
        if any(b.name == "Unit 17 Passive" for b in pet.active_buffs):
            return

        # Create a permanent buff that reduces damage taken
        passive_buff = Buff(
            type=BuffType.STAT_MOD,
            name="Unit 17 Passive",
            duration=999,  # Permanent
            magnitude=0.5, # 50% reduction (multiplier)
            stat_affected='damage_taken',
            source_ability=99998,
            source_pet_index=pet.index if hasattr(pet, 'index') else 0,
            snapshot_hp=pet.stats.current_hp
        )
        # Note: stat_multipliers is not a direct init arg for Buff, it uses magnitude + stat_affected
        # But for complex buffs we might need more. 
        # The Buff class in battle_state.py handles simple stat mods via magnitude.
        # If stat_affected is 'damage_taken', magnitude should be the multiplier (e.g. 0.5 for 50% taken, or 0.5 reduction?)
        # Usually 0.5 means 50% damage taken (reduction). 
        # Let's assume magnitude is the multiplier for damage taken.
        
        pet.active_buffs.append(passive_buff)
        if hasattr(simulator, 'log_event'):
            simulator.log_event(f"{pet.name} gains Unit 17 Passive (50% Damage Reduction)!")

# Map pet names to their special mechanic functions
SPECIAL_MECHANICS_BY_NAME = {
    "Unit 17": SpecialEncounterHandler.apply_unit_17_passive
}
