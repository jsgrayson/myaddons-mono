"""
Damage Calculator for Pet Battle Simulator

Implements WoW pet battle damage formulas including:
- Base damage calculation
- Family effectiveness (strong/weak/neutral)
- Quality modifiers
- Critical hits, dodges, misses
- Weather effects
"""

from typing import Optional, Tuple
import random
import math
from .battle_state import Pet, Ability, PetFamily, PetQuality, Buff, BuffType
from .racial_passives import RacialPassives


# Family effectiveness matrix: [attacker_family][defender_family] = multiplier
FAMILY_EFFECTIVENESS = {
    PetFamily.HUMANOID: {
        PetFamily.DRAGONKIN: 1.5,  # Strong vs Dragonkin
        PetFamily.BEAST: 0.67,     # Weak vs Beast
    },
    PetFamily.DRAGONKIN: {
        PetFamily.MAGIC: 1.5,
        PetFamily.UNDEAD: 0.67,
    },
    PetFamily.FLYING: {
        PetFamily.AQUATIC: 1.5,
        PetFamily.DRAGONKIN: 0.67,
    },
    PetFamily.UNDEAD: {
        PetFamily.HUMANOID: 1.5,
        PetFamily.CRITTER: 0.67,
    },
    PetFamily.CRITTER: {
        PetFamily.UNDEAD: 1.5,
        PetFamily.HUMANOID: 0.67,
    },
    PetFamily.MAGIC: {
        PetFamily.FLYING: 1.5,
        PetFamily.MECHANICAL: 0.67,
    },
    PetFamily.ELEMENTAL: {
        PetFamily.MECHANICAL: 1.5,
        PetFamily.CRITTER: 0.67,
    },
    PetFamily.BEAST: {
        PetFamily.CRITTER: 1.5,
        PetFamily.FLYING: 0.67,
    },
    PetFamily.AQUATIC: {
        PetFamily.ELEMENTAL: 1.5,
        PetFamily.MAGIC: 0.67,
    },
    PetFamily.MECHANICAL: {
        PetFamily.BEAST: 1.5,
        PetFamily.ELEMENTAL: 0.67,
    },
}

# Quality damage modifiers
QUALITY_MODIFIERS = {
    PetQuality.POOR: 0.8,
    PetQuality.COMMON: 0.9,
    PetQuality.UNCOMMON: 0.95,
    PetQuality.RARE: 1.0,
    PetQuality.EPIC: 1.05,
    PetQuality.LEGENDARY: 1.1,
}


class DamageCalculator:
    """Calculates damage for pet battle abilities"""
    
    def __init__(self, rng_seed: Optional[int] = None):
        """Initialize with optional RNG seed for reproducibility"""
        self.rng = random.Random(rng_seed)
    
    def get_family_multiplier(self, attacker_family: PetFamily, defender_family: PetFamily) -> float:
        """Get damage multiplier based on family matchup"""
        family_matrix = FAMILY_EFFECTIVENESS.get(attacker_family, {})
        return family_matrix.get(defender_family, 1.0)
    
    def get_quality_multiplier(self, quality: PetQuality) -> float:
        """Get damage multiplier based on pet quality"""
        return QUALITY_MODIFIERS.get(quality, 1.0)
    
    def check_hit(self, ability: Ability, attacker: Pet, defender: Pet, weather: Optional[Buff] = None) -> bool:
        """Determine if ability hits (based on accuracy)"""
        # Natural 100% accuracy
        # Note: Even 100% accuracy moves can be dodged, so we don't return early.
        # Only "Always Hits" (accuracy > 100 usually implies this in some systems, but here we stick to formula)
        # if ability.accuracy >= 100:
        #     return True
        
        # Check dodge buffs on defender
        dodge_chance = 0.0
        # if ability.name == "Rampage":
        #     print(f"\n=== RAMPAGE CHECK ===")
        #     print(f"Defender: {defender.name}, Active buffs: {[b.name for b in defender.active_buffs]}")
        #     for b in defender.active_buffs:
        #         print(f"  Buff: {b.name}, Type: {b.type}, Duration: {b.duration}")
        
        for buff in defender.active_buffs:
            # DEBUG: Print buffs
            #print(f"DEBUG: Checking buff {buff.name} (Type: {buff.type}) on {defender.name}")
            if buff.type == BuffType.STAT_MOD and buff.stat_affected == 'dodge':
                dodge_chance += buff.magnitude
            elif buff.type == BuffType.INVULNERABILITY:
                # if ability.name == "Rampage":
                #     print(f"  → INVULNERABILITY DETECTED! Returning False")
                return False
        
        # Check accuracy buffs on attacker
        accuracy_mod = 0.0
        for buff in attacker.active_buffs:
            if buff.type == BuffType.STAT_MOD and buff.stat_affected == 'accuracy':
                accuracy_mod += buff.magnitude
        
        # Check weather accuracy modifiers
        weather_mod = 0.0
        if weather and weather.type == BuffType.WEATHER:
            weather_name = getattr(weather, 'stat_affected', None)
            
            # Weather accuracy effects
            weather_accuracy = {
                'call_darkness': -0.10,  # -10% accuracy
                'darkness': -0.10,       # Standard Darkness
            }
            
            if weather_name in weather_accuracy:
                # Elemental pets ignore weather effects
                if attacker.family != PetFamily.ELEMENTAL:
                    weather_mod = weather_accuracy[weather_name]
        
        # Roll for hit
        hit_roll = self.rng.randint(1, 100)
        
        # Calculate threshold: Accuracy - Dodge - WeatherPenalty
        # Note: weather_mod is negative for penalty, so we add it? 
        # Formula: Chance = Accuracy + WeatherMod - Dodge
        # Example: 90% acc + (-10%) weather - 0% dodge = 80% chance
        # Calculate threshold: Accuracy - Dodge - WeatherPenalty + AccuracyBuffs
        # Note: weather_mod is negative for penalty, so we add it? 
        # Formula: Chance = Accuracy + WeatherMod - Dodge + AccuracyMod
        # Example: 90% acc + (-10%) weather - 0% dodge + 50% buff = 130% chance
        threshold = ability.accuracy + (weather_mod * 100) - (dodge_chance * 100) + (accuracy_mod * 100)
        
        return hit_roll <= threshold
    
    def check_crit(self, attacker: Pet) -> bool:
        """Determine if attack crits (5% base + crit buffs)"""
        crit_chance = 0.05  # 5% base
        
        for buff in attacker.active_buffs:
            if buff.type == BuffType.STAT_MOD and buff.stat_affected == 'crit':
                crit_chance += buff.magnitude
        
        return self.rng.random() < crit_chance
    
    def apply_weather_modifier(self, damage: int, ability: Ability, attacker: Pet, weather: Optional[Buff]) -> int:
        """Apply weather modifiers to damage"""
        if not weather or weather.type != BuffType.WEATHER:
            return damage
        
        # Get weather name from stat_affected field
        weather_name = getattr(weather, 'stat_affected', None)
        
        # Pandaren Spirit weather effects + standard weather
        weather_effects = {
            # Pandaren Spirits
            'tidal_wave': {PetFamily.AQUATIC: 1.25},
            'scorched_earth': {PetFamily.ELEMENTAL: 1.25},
            'call_lightning': {PetFamily.MECHANICAL: 1.25, PetFamily.FLYING: 1.25},
            # Call Darkness has no damage bonus
            
            # Standard weather (for completeness)
            'sunny_day': {PetFamily.BEAST: 1.25},
            'moonlight': {PetFamily.MAGIC: 1.25},
            'darkness': {PetFamily.UNDEAD: 1.25},
            'mudslide': {PetFamily.CRITTER: 1.25},
            'blizzard': {PetFamily.ELEMENTAL: 1.25},
            'sandstorm': {PetFamily.FLYING: 1.25},
            'cleansing_rain': {PetFamily.AQUATIC: 1.25},
        }
        
        if weather_name in weather_effects:
            family_bonuses = weather_effects[weather_name]
            if attacker.family in family_bonuses:
                multiplier = family_bonuses[attacker.family]
                damage = int(damage * multiplier)
        
        return damage
    
    def calculate_damage(
        self,
        ability: Ability,
        attacker: Pet,
        defender: Pet,
        weather: Optional[Buff] = None
    ) -> Tuple[int, dict]:
        """
        Calculate final damage for an ability
        
        Returns:
            (damage: int, details: dict) where details contains breakdown
        """
        details = {
            'hit': False,
            'crit': False,
            'base_damage': 0,
            'final_damage': 0,
            'family_multiplier': 1.0,
            'quality_multiplier': 1.0,
            'weather_multiplier': 1.0,
            'racial_multiplier': 1.0,
        }
        
        # Check if ability hits
        if not self.check_hit(ability, attacker, defender, weather):
            details['hit'] = False
            return 0, details
        
        details['hit'] = True
        
        # If ability has no power, it deals no damage (unless it's a special case handled elsewhere)
        if ability.power == 0:
            return 0, details
        
        # Base damage formula: ability_power * (pet_power / 20)
        attacker_power = attacker.get_effective_power()
        base_damage = ability.power * (attacker_power / 20.0)
        details['base_damage'] = int(base_damage)
        
        # Apply family effectiveness
        family_mult = self.get_family_multiplier(ability.family, defender.family)
        details['family_multiplier'] = family_mult
        base_damage *= family_mult
        
        # Apply racial passive damage modifiers (Beast +25%, Critter +50% conditional, Dragonkin +50% conditional)
        racial_mult = RacialPassives.get_damage_modifier(attacker)
        details['racial_multiplier'] = racial_mult
        base_damage *= racial_mult
        
        # Consume Dragonkin buff if it was used
        if attacker.family == PetFamily.DRAGONKIN and attacker.dragonkin_buff_ready:
            RacialPassives.consume_dragonkin_buff(attacker)
        
        # Quality multiplier is NOT applied here because attacker.power (from PetStats)
        # already includes the quality modifier. Applying it again would be double-dipping.
        details['quality_multiplier'] = 1.0
        
        # Check for crit (+50% damage)
        is_crit = self.check_crit(attacker)
        details['crit'] = is_crit
        if is_crit:
            base_damage *= 1.5
        
        # Apply weather modifiers
        base_damage = self.apply_weather_modifier(int(base_damage), ability, attacker, weather)
        
        # Random variance (±5%)
        variance = self.rng.uniform(0.95, 1.05)
        final_damage = int(base_damage * variance)
        
        # Apply damage reduction/amplification buffs on defender
        damage_reduction = 1.0
        flat_damage_mod = 0
        
        for buff in defender.active_buffs:
            if buff.type == BuffType.STAT_MOD:
                if buff.stat_affected == 'damage_taken':
                    # Howl (2.0) and Shell Shield (0.5) are handled here multiplicatively
                    damage_reduction *= buff.magnitude
                elif buff.stat_affected == 'damage_taken_mult':
                    # Shattered Defenses (Hunting Party)
                    damage_reduction *= buff.magnitude
                elif buff.stat_affected == 'damage_taken_flat':
                    # Black Claw
                    flat_damage_mod += buff.magnitude

        final_damage = int(final_damage * damage_reduction)
        final_damage += int(flat_damage_mod)
        
        # Check for Decoy/Block
        blocked = False
        for buff in defender.active_buffs:
            if buff.type == BuffType.BLOCK:
                blocked = True
                buff.stacks -= 1
                if buff.stacks <= 0:
                    defender.active_buffs.remove(buff)
                details['blocked'] = True
                return 0, details

        # ❌ REMOVED: Duplicate damage_reduction application (was line 288)
        # Damage reduction already applied on line 274
        
        
        # Apply Magic racial passive (damage cap at 35% max HP)
        if defender.family == PetFamily.MAGIC:
            # Pass ability.hits to handle multi-hit cap correctly
            hits = getattr(ability, 'hits', 1)
            final_damage = RacialPassives.apply_magic_passive(defender, final_damage, hits)
        
        # Minimum 1 damage if hit
        final_damage = max(1, final_damage)
        # Final rounding (Module 6: Round DOWN)
        final_damage = math.floor(final_damage)
        
        # Check for False Swipe / Cannot Kill
        if getattr(ability, 'cannot_kill', False):
            # Ensure damage leaves at least 1 HP
            if final_damage >= defender.stats.current_hp:
                final_damage = max(0, defender.stats.current_hp - 1)
        
        details['final_damage'] = final_damage
        
        return final_damage, details
    
    def calculate_healing(
        self,
        ability: Ability,
        healer: Pet
    ) -> int:
        """Calculate healing for a healing ability"""
        # Healing formula: ability_power * (pet_power / 20)
        healer_power = healer.get_effective_power()
        base_heal = ability.power * (healer_power / 20.0)
        
        # Healing buffs
        healing_mult = 1.0
        for buff in healer.active_buffs:
            if buff.type == BuffType.STAT_MOD and buff.stat_affected == 'healing':
                healing_mult *= buff.magnitude
        
        # Apply Aquatic racial passive (+25% healing)
        healing_mult *= RacialPassives.get_healing_modifier(healer)
        
        final_heal = int(base_heal * healing_mult)
        return max(1, final_heal)
