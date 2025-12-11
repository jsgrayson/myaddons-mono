"""
Battle State Model for Pet Battle Simulator

This module defines the core data structures for representing a pet battle
at any point in time. It provides immutable state snapshots for simulation.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple, Union
from enum import Enum
import copy


class PetFamily(Enum):
    """Pet families with their type IDs"""
    HUMANOID = 1
    DRAGONKIN = 2
    FLYING = 3
    UNDEAD = 4
    CRITTER = 5
    MAGIC = 6
    ELEMENTAL = 7
    BEAST = 8
    AQUATIC = 9
    MECHANICAL = 10


class PetQuality(Enum):
    """Pet quality tiers"""
    POOR = 0
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5


class BuffType(Enum):
    """Types of buffs/debuffs"""
    STAT_MOD = "stat_modifier"  # +/- to stats
    DOT = "damage_over_time"
    HOT = "heal_over_time"
    SHIELD = "shield"
    STUN = "stun"
    WEATHER = "weather"
    AURA = "aura"
    IMMUNITY = "immunity"
    BLOCK = "block"
    ROOT = "root"
    SLEEP = "sleep"
    DELAYED_EFFECT = "delayed_effect"
    INVULNERABILITY = "invulnerability"


@dataclass
class PetStats:
    """Base stats for a pet"""
    max_hp: int
    current_hp: int
    power: int
    speed: int
    breed_id: int = 0  # 3=H/H, 4=P/P, etc.
    
    def is_alive(self) -> bool:
        return self.current_hp > 0
    
    def take_damage(self, amount: int) -> int:
        """Apply damage and return actual damage dealt"""
        actual_damage = min(amount, self.current_hp)
        self.current_hp = max(0, self.current_hp - amount)
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """Heal and return actual healing done"""
        actual_heal = min(amount, self.max_hp - self.current_hp)
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return actual_heal

    def clone(self) -> 'PetStats':
        """Fast copy"""
        return PetStats(
            max_hp=self.max_hp,
            current_hp=self.current_hp,
            power=self.power,
            speed=self.speed,
            breed_id=self.breed_id
        )


@dataclass
class Ability:
    """Pet ability definition"""
    id: int
    name: str
    power: int  # Base damage/healing
    accuracy: int  # 0-100
    speed: int  # Speed modifier
    cooldown: int  # Turns before can use again
    family: PetFamily
    hits: int = 1  # Multi-hit abilities
    priority: int = 0  # Higher = goes first regardless of speed
    
    # Effect modifiers
    is_dot: bool = False
    dot_duration: int = 0
    is_heal: bool = False
    stat_buffs: Dict[str, Tuple[float, int]] = field(default_factory=dict)  # stat: (multiplier, duration)
    
    # Complex effects
    bonus_damage_percent: float = 0.0  # e.g. 0.5 for +50%
    bonus_condition: Optional[str] = None  # e.g. 'weather_sunny', 'target_webbed'
    delayed_turns: int = 0  # e.g. 3 for Geyser/Whirlpool
    effect_type: Optional[str] = None  # e.g. 'stun', 'swap', 'heal_team'
    effect_chance: int = 100  # Percent chance for effect
    cannot_kill: bool = False  # If True, damage cannot reduce HP below 1 (False Swipe)
    
    def __hash__(self):
        return hash(self.id)


@dataclass
class Buff:
    """Active buff/debuff on a pet"""
    type: BuffType
    duration: int  # Rounds remaining
    magnitude: float  # Multiplier or flat amount
    name: str = "Unknown"
    stat_affected: Optional[str] = None  # 'power', 'speed', 'damage_taken'
    source_ability: Optional[Union[int, str]] = None  # Ability ID or Name that applied this
    stacks: int = 1  # Some buffs stack
    source_pet_index: Optional[int] = None  # Index of pet that applied this (for Haunt/Life Exchange)
    snapshot_hp: Optional[int] = None  # HP snapshot (for Haunt resurrection)
    
    def tick(self) -> bool:
        """Decrement duration, return True if still active"""
        self.duration -= 1
        return self.duration > 0

    def clone(self) -> 'Buff':
        """Fast copy"""
        return Buff(
            type=self.type,
            duration=self.duration,
            magnitude=self.magnitude,
            name=self.name,
            stat_affected=self.stat_affected,
            source_ability=self.source_ability,
            stacks=self.stacks,
            source_pet_index=self.source_pet_index,
            snapshot_hp=self.snapshot_hp
        )





@dataclass
class Pet:
    """Complete pet state"""
    species_id: int
    name: str
    family: PetFamily
    quality: PetQuality
    stats: PetStats
    abilities: List[Ability]
    
    # Combat state
    active_buffs: List[Buff] = field(default_factory=list)
    ability_cooldowns: Dict[int, int] = field(default_factory=dict)  # ability_id: turns_remaining



    # Racial passive state tracking
    has_undead_revive: bool = False  # Currently in revive state (1 extra turn)
    revive_turns_remaining: int = 0  # Turns remaining for Undead revive
    has_used_undead_revive: bool = False  # Has used Undead revive (once per pet)
    has_used_mechanical_revive: bool = False  # Has used Mechanical revive (once per battle)
    dragonkin_buff_ready: bool = False  # Dragonkin +50% damage buff ready
    
    def can_use_ability(self, ability: Ability) -> bool:
        """Check if ability is off cooldown"""
        return self.ability_cooldowns.get(ability.id, 0) == 0
    
    def use_ability(self, ability: Ability):
        """Mark ability as used (set cooldown)"""
        if ability.cooldown > 0:
            self.ability_cooldowns[ability.id] = ability.cooldown
    
    def tick_cooldowns(self):
        """Decrement all cooldowns"""
        for ability_id in list(self.ability_cooldowns.keys()):
            self.ability_cooldowns[ability_id] -= 1
            if self.ability_cooldowns[ability_id] <= 0:
                del self.ability_cooldowns[ability_id]
    
    def get_effective_speed(self) -> int:
        """Calculate speed with buffs applied"""
        speed = self.stats.speed
        for buff in self.active_buffs:
            if buff.stat_affected == 'speed':
                speed = int(speed * buff.magnitude)
            
            # Speed Vulnerability: Underground/Flying pets have 0 speed
            if buff.name in ["Underground", "Flying"]:
                return 0
                
        return speed
    
    def get_effective_power(self) -> int:
        """Calculate power with buffs applied"""
        power = self.stats.power
        for buff in self.active_buffs:
            if buff.stat_affected == 'power':
                power = int(power * buff.magnitude)
        return power

    def clone(self) -> 'Pet':
        """Fast copy"""
        new_pet = Pet(
            species_id=self.species_id,
            name=self.name,
            family=self.family,
            quality=self.quality,
            stats=self.stats.clone(),
            abilities=self.abilities  # Abilities are immutable/shared
        )
        # Copy mutable state
        new_pet.active_buffs = [b.clone() for b in self.active_buffs]
        new_pet.ability_cooldowns = self.ability_cooldowns.copy()
        
        # Copy racial state
        new_pet.has_undead_revive = self.has_undead_revive
        new_pet.revive_turns_remaining = self.revive_turns_remaining
        new_pet.has_used_undead_revive = self.has_used_undead_revive
        new_pet.has_used_mechanical_revive = self.has_used_mechanical_revive
        new_pet.dragonkin_buff_ready = self.dragonkin_buff_ready
        
        return new_pet


@dataclass
class Team:
    """A team of 3 pets"""
    pets: List[Pet]
    active_pet_index: int = 0
    
    def get_active_pet(self) -> Optional[Pet]:
        if 0 <= self.active_pet_index < len(self.pets):
            return self.pets[self.active_pet_index]
        return None

    def copy(self) -> 'Team':
        """Create a deep copy of the team"""
        return self.clone()

    def clone(self) -> 'Team':
        """Fast copy"""
        return Team(
            pets=[p.clone() for p in self.pets],
            active_pet_index=self.active_pet_index
        )
    
    def has_living_pets(self) -> bool:
        """Check if any pets are alive"""
        return any(pet.stats.is_alive() for pet in self.pets)
    
    def get_first_living_pet_index(self) -> Optional[int]:
        """Find first living pet"""
        for i, pet in enumerate(self.pets):
            if pet.stats.is_alive():
                return i
        return None


@dataclass
class BattleState:
    """Complete battle state at a point in time"""
    player_team: Team
    enemy_team: Team
    turn_number: int = 1
    weather: Optional[Buff] = None  # Active weather effect
    rng_seed: int = 0  # For reproducible RNG
    
    def copy(self) -> 'BattleState':
        """Create deep copy for branching simulations"""
        return self.clone()

    def clone(self) -> 'BattleState':
        """Fast copy"""
        new_state = BattleState(
            player_team=self.player_team.clone(),
            enemy_team=self.enemy_team.clone(),
            turn_number=self.turn_number,
            rng_seed=self.rng_seed
        )
        if self.weather:
            new_state.weather = self.weather.clone()
        return new_state
    
    def is_battle_over(self) -> bool:
        """Check if battle has ended"""
        return not self.player_team.has_living_pets() or not self.enemy_team.has_living_pets()
    
    def get_winner(self) -> Optional[str]:
        """Return winner if battle is over"""
        if not self.is_battle_over():
            return None
        if self.player_team.has_living_pets():
            return "player"
        if self.enemy_team.has_living_pets():
            return "enemy"
        return "draw"


@dataclass
class TurnAction:
    """An action taken during a turn"""
    actor: str  # 'player' or 'enemy'
    action_type: str  # 'ability', 'swap', 'pass'
    ability: Optional[Ability] = None
    target_pet_index: Optional[int] = None  # For swaps
    
    def __repr__(self):
        if self.action_type == 'ability' and self.ability:
            return f"{self.actor} uses {self.ability.name}"
        elif self.action_type == 'swap':
            return f"{self.actor} swaps to pet {self.target_pet_index}"
        return f"{self.actor} passes"
