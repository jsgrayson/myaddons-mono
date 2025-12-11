"""
Buff Tracker for Pet Battle Simulator

Manages active buffs, debuffs, DoTs, HoTs, and other timed effects.
Handles duration tracking, stacking, and tick processing.
"""

from typing import List, Dict, Optional
from .battle_state import Pet, Buff, BuffType, PetFamily


class BuffTracker:
    """Tracks and processes all active buffs/debuffs in battle"""
    
    @staticmethod
    def add_buff(pet: Pet, buff: Buff, weather: Optional[Buff] = None) -> bool:
        """
        Add a buff to a pet
        
        Returns True if buff was added, False if it stacked or was blocked
        """
        # Check if buff already exists (for stacking)
        for existing_buff in pet.active_buffs:
            if (existing_buff.type == buff.type and 
                existing_buff.stat_affected == buff.stat_affected and
                existing_buff.source_ability == buff.source_ability):
                
                # Stack if stackable
                if existing_buff.stacks < 3:  # Max 3 stacks for most buffs
                    existing_buff.stacks += 1
                    existing_buff.magnitude += buff.magnitude
                    existing_buff.duration = buff.duration  # Refresh duration
                    return True
                else:
                    # Already at max stacks, refresh duration
                    existing_buff.duration = buff.duration
                    return False
        
        # Critter Immunity Check (Stun, Root, Sleep)
        if pet.family == PetFamily.CRITTER:
            if buff.type in [BuffType.STUN, BuffType.ROOT, BuffType.SLEEP]:
                return False
        
        # CC Immunity Clock Check (Module 6)
        if buff.type in [BuffType.STUN, BuffType.ROOT, BuffType.SLEEP]:
            for active_buff in pet.active_buffs:
                if active_buff.type == BuffType.IMMUNITY and active_buff.stat_affected == buff.type.value:
                    return False
        
        # Cleansing Rain Logic: Reduces DoT duration by 1 round
        if buff.type == BuffType.DOT and weather and weather.name == "Cleansing Rain":
            buff.duration = max(0, buff.duration - 1)
            if buff.duration == 0:
                return False # Prevent adding if duration becomes 0

        # New buff, add it
        # print(f"DEBUG: Adding buff {buff.name} to {pet.name} (ID: {id(pet)})")
        pet.active_buffs.append(buff)
        # print(f"DEBUG: Buffs on {pet.name} after add: {[b.name for b in pet.active_buffs]}")
        return True
    
    @staticmethod
    def remove_buff(pet: Pet, buff: Buff):
        """Remove a specific buff from pet"""
        if buff in pet.active_buffs:
            print(f"DEBUG: Removing buff {buff.name} from {pet.name}")
            pet.active_buffs.remove(buff)
    
    @staticmethod
    def clear_buffs_by_type(pet: Pet, buff_type: BuffType):
        """Remove all buffs of a specific type"""
        print(f"DEBUG: Clearing buffs of type {buff_type} from {pet.name}")
        pet.active_buffs = [b for b in pet.active_buffs if b.type != buff_type]
    
    @staticmethod
    def process_weather_damage(weather: str, pet: Pet) -> List[Dict]:
        """
        Apply weather DoT damage at start of cleanup phase
        
        Args:
            weather: Weather effect name (e.g., 'scorched_earth', 'call_lightning')
            pet: Pet to apply weather damage to
            
        Returns:
            List of damage events
        """
        events = []
        
        # Weather DoT effects
        weather_dots = {
            'scorched_earth': {
                'damage': 35,
                'damage_type': 'Dragonkin',
                'immune_family': PetFamily.ELEMENTAL
            },
            'call_lightning': {
                'damage': 30,
                'damage_type': 'Elemental',
                'immune_family': None
            }
        }
        
        weather_effect = weather_dots.get(weather)
        if not weather_effect:
            return events
            
        # Check immunity (Elementals immune to Scorched Earth)
        if weather_effect['immune_family'] and pet.family == weather_effect['immune_family']:
            return events
            
        # Apply weather damage
        damage = weather_effect['damage']
        actual_damage = pet.stats.take_damage(damage)
        events.append({
            'type': 'weather_damage',
            'amount': actual_damage,
            'source': weather,
            'damage_type': weather_effect['damage_type']
        })
        
        return events
    
    @staticmethod
    def process_dots(pet: Pet) -> List[Dict]:
        """Process Damage Over Time effects"""
        events = []
        for buff in pet.active_buffs:
            if buff.type == BuffType.DOT:
                damage = int(buff.magnitude * buff.stacks)
                
                # Aquatic Passive: Reduces DoT damage by 50%
                if str(pet.family) == 'PetFamily.AQUATIC' or getattr(pet.family, 'name', '') == 'AQUATIC':
                     damage = int(damage * 0.5)
                
                actual_damage = pet.stats.take_damage(damage)
                events.append({
                    'type': 'dot_damage',
                    'amount': actual_damage,
                    'source': buff.source_ability
                })
        return events

    @staticmethod
    def process_hots(pet: Pet) -> List[Dict]:
        """Process Healing Over Time effects"""
        events = []
        for buff in pet.active_buffs:
            if buff.type == BuffType.HOT:
                heal = int(buff.magnitude * buff.stacks)
                actual_heal = pet.stats.heal(heal)
                events.append({
                    'type': 'hot_heal',
                    'amount': actual_heal,
                    'source': buff.source_ability
                })
        return events

    @staticmethod
    def decrement_durations(pet: Pet) -> List[Dict]:
        """Decrement buff durations and handle expiration"""
        # print(f"DEBUG: decrement_durations called for {pet.name}")
        events = []
        buffs_to_remove = []
        
        for buff in list(pet.active_buffs):
            still_active = buff.tick()
            if not still_active:
                buffs_to_remove.append(buff)
                events.append({
                    'type': 'buff_expired',
                    'buff': buff
                })
                
                # Trigger Delayed Effects (Geyser/Whirlpool) on expiration
                if buff.type == BuffType.DELAYED_EFFECT:
                    print(f"DEBUG: Triggering delayed effect for {buff.source_ability}")
                    # Deal Damage
                    damage = int(buff.magnitude)
                    actual_damage = pet.stats.take_damage(damage)
                    events.append({
                        'type': 'delayed_damage',
                        'amount': actual_damage,
                        'source': buff.source_ability
                    })
                    
                    # Apply CC if applicable
                    if "Geyser" in str(buff.source_ability):
                        print("DEBUG: Applying Geyser Stun")
                        stun_buff = Buff(
                            type=BuffType.STUN,
                            name="Stunned",
                            duration=1,
                            magnitude=0,
                            source_ability="Geyser",
                            stat_affected='none'
                        )
                        added = BuffTracker.add_buff(pet, stun_buff)
                        print(f"DEBUG: Stun added? {added}")
                        events.append({'type': 'cc_applied', 'cc': 'Stun', 'source': 'Geyser'})
                        
                    elif "Whirlpool" in str(buff.source_ability):
                        root_buff = Buff(
                            type=BuffType.ROOT,
                            name="Rooted",
                            duration=2,
                            magnitude=0,
                            source_ability="Whirlpool",
                            stat_affected='none'
                        )
                        BuffTracker.add_buff(pet, root_buff)
                        events.append({'type': 'cc_applied', 'cc': 'Root', 'source': 'Whirlpool'})

        # Remove expired buffs
        for buff in buffs_to_remove:
            pet.active_buffs.remove(buff)
            
        return events
    
    @staticmethod
    def tick_all_buffs(pet: Pet) -> List[Dict]:
        """Legacy wrapper for backward compatibility. Executes cleanup phase in order: DoTs, HoTs, then decrement durations."""
        events: List[Dict] = []
        events.extend(BuffTracker.process_dots(pet))
        events.extend(BuffTracker.process_hots(pet))
        events.extend(BuffTracker.decrement_durations(pet))
        return events

    @staticmethod
    def apply_weather_effect(pet: Pet, weather_buff: Optional[Buff]) -> List[Dict]:
        """
        Apply weather passive effects to pet
        
        Pandaren Spirit weather effects (3 of 4 have TWO components):
        1. Damage multiplier for specific families
        2. DoT damage each round
        
        Exception: Call Darkness only reduces healing + affects accuracy
        """
        if not weather_buff or weather_buff.type != BuffType.WEATHER:
            return []
        
        events = []
        
        # Weather-specific effects (Pandaren Spirits)
        # Format: {weather_name: {family_bonus, dot_damage, dot_family, special_effects}}
        weather_effects = {
            'tidal_wave': {
                'damage_bonus_family': 'Aquatic',  # +25% Aquatic damage
                'damage_bonus': 0.25,
                'healing_bonus': 0.25,  # +25% healing (Aquatic passive stacks)
                'dot_damage': 0,  # Tidal Wave doesn't have persistent DoT
            },
            'scorched_earth': {
                'damage_bonus_family': 'Elemental',  # +25% Elemental damage
                'damage_bonus': 0.25,
                'dot_damage': 35,  # 35 Dragonkin damage per round
                'dot_family': 'Dragonkin',
                'immune_family': 'Elemental',  # Elementals immune to the DoT
            },
            'call_lightning': {
                'damage_bonus_family': ['Mechanical', 'Flying'],  # +25% for both
                'damage_bonus': 0.25,
                'dot_damage': 30,  # Estimated ~30 damage per round
                'dot_family': 'Elemental',
            },
            'call_darkness': {
                'healing_reduction': -0.50,  # -50% healing
                'hit_chance_bonus': -0.10,  # -10% accuracy (standard Darkness)
                'dot_damage': 0,  # Call Darkness doesn't do persistent DoT (just initial hit)
            },
            'cleansing_rain': {
                'damage_bonus_family': 'Aquatic', # +25% Aquatic damage
                'damage_bonus': 0.25,
                'dot_duration_reduction': 1, # Reduces DoT duration by 1 round
                'dot_damage': 0,
            }
        }
        
        # Apply effects (simplified - would need full implementation)
        return events
    
    @staticmethod
    def get_stat_modifier(pet: Pet, stat_name: str) -> float:
        """
        Calculate total modifier for a stat from all buffs
        
        Args:
            pet: Pet to check
            stat_name: 'power', 'speed', 'damage_taken', etc.
        
        Returns:
            Multiplier (1.0 = no change)
        """
        total_modifier = 1.0
        
        for buff in pet.active_buffs:
            if buff.type == BuffType.STAT_MOD and buff.stat_affected == stat_name:
                # Multiplicative stacking
                total_modifier *= buff.magnitude
        
        return total_modifier
    
    @staticmethod
    def has_immunity(pet: Pet, damage_type: str) -> bool:
        """Check if pet is immune to a damage type"""
        for buff in pet.active_buffs:
            if buff.type == BuffType.SHIELD and buff.stat_affected == damage_type:
                return True
        return False
    
    @staticmethod
    def consume_shield(pet: Pet, damage: int) -> int:
        """
        Apply damage to shields first
        
        Returns remaining damage after shields
        """
        remaining_damage = damage
        buffs_to_remove = []
        
        for buff in pet.active_buffs:
            # Decoy / Block Logic (Blocks next 1 instance)
            if buff.type == BuffType.BLOCK:
                # Blocks 1 instance completely
                remaining_damage = 0
                buff.stacks -= 1
                if buff.stacks <= 0:
                    buffs_to_remove.append(buff)
                break  # Stop processing other shields if blocked completely
                
            if buff.type == BuffType.SHIELD and remaining_damage > 0:
                shield_amount = int(buff.magnitude)
                
                if shield_amount >= remaining_damage:
                    # Shield absorbs all damage
                    buff.magnitude -= remaining_damage
                    remaining_damage = 0
                    
                    # Remove shield if depleted
                    if buff.magnitude <= 0:
                        buffs_to_remove.append(buff)
                else:
                    # Shield breaks, some damage gets through
                    remaining_damage -= shield_amount
                    buffs_to_remove.append(buff)
        
        # Remove broken shields
        for buff in buffs_to_remove:
            pet.active_buffs.remove(buff)
        
        return remaining_damage
