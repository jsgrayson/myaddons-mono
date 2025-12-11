"""
Test Racial Passive Abilities

Verifies that all 10 pet family racial passives work correctly.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator.battle_state import Pet, PetStats, Ability, PetFamily, PetQuality, BattleState, Team, TurnAction
from simulator.racial_passives import RacialPassives
from simulator.simulator import BattleSimulator


def create_pet(name: str, family: PetFamily, hp: int = 1000, power: int = 200, speed: int = 100) -> Pet:
    """Helper to create a pet for testing"""
    return Pet(
        species_id=1,
        name=name,
        family=family,
        quality=PetQuality.RARE,
        stats=PetStats(max_hp=hp, current_hp=hp, power=power, speed=speed),
        abilities=[]
    )


def test_beast_passive():
    """Beast: +25% damage"""
    beast_pet = create_pet("Beast", PetFamily.BEAST)
    modifier = RacialPassives.apply_beast_passive()
    assert modifier == 1.25, "Beast should get +25% damage"


def test_critter_passive_above_50():
    """Critter: No damage bonus (only CC immunity per spec)"""
    critter = create_pet("Critter", PetFamily.CRITTER, hp=1000)
    critter.stats.current_hp = 600  # Above 50%
    modifier = RacialPassives.apply_critter_passive(critter)
    assert modifier == 1.0, "Critter has no damage bonus per spec"


def test_critter_passive_below_50():
    """Critter: Normal damage when below 50% HP"""
    critter = create_pet("Critter", PetFamily.CRITTER, hp=1000)
    critter.stats.current_hp = 400  # Below 50%
    modifier = RacialPassives.apply_critter_passive(critter)
    assert modifier == 1.0, "Critter below 50% HP should get normal damage"


def test_flying_passive_above_50():
    """Flying: +50% speed when above 50% HP"""
    flying = create_pet("Flying", PetFamily.FLYING, hp=1000)
    flying.stats.current_hp = 600  # Above 50%
    modifier = RacialPassives.apply_flying_passive(flying)
    assert modifier == 1.5, "Flying above 50% HP should get +50% speed"


def test_flying_passive_below_50():
    """Flying: Normal speed when below 50% HP"""
    flying = create_pet("Flying", PetFamily.FLYING, hp=1000)
    flying.stats.current_hp = 400  # Below 50%
    modifier = RacialPassives.apply_flying_passive(flying)
    assert modifier == 1.0, "Flying below 50% HP should get normal speed"


def test_humanoid_passive():
    """Humanoid: Heal 4% of max HP when dealing damage"""
    humanoid = create_pet("Humanoid", PetFamily.HUMANOID, hp=1000)
    humanoid.stats.current_hp = 500  # Below max
    
    heal_amount = RacialPassives.apply_humanoid_passive(humanoid, 100)
    
    # Should heal 4% of 1000 = 40 HP
    assert heal_amount == 40, "Humanoid should heal 4% of max HP"
    assert humanoid.stats.current_hp == 540, "HP should increase by 40"


def test_magic_passive_damage_cap():
    """Magic: Cannot take more than 35% max HP in one hit"""
    magic_pet = create_pet("Magic", PetFamily.MAGIC, hp=1000)
    
    # Try to deal 500 damage (50% of max HP)
    capped_damage = RacialPassives.apply_magic_passive(magic_pet, 500)
    
    # Should be capped at 35% = 350
    assert capped_damage == 350, "Magic pet should cap damage at 35% max HP"


def test_magic_passive_normal_damage():
    """Magic: Normal damage if below 35% threshold"""
    magic_pet = create_pet("Magic", PetFamily.MAGIC, hp=1000)
    
    # Deal 200 damage (20% of max HP, below cap)
    capped_damage = RacialPassives.apply_magic_passive(magic_pet, 200)
    
    assert capped_damage == 200, "Magic pet should not cap damage below 35%"


def test_aquatic_passive():
    """Aquatic: No healing bonus (only DoT reduction per spec)"""
    modifier = RacialPassives.apply_aquatic_passive()
    assert modifier == 1.0, "Aquatic has no healing bonus per spec"


def test_elemental_passive():
    """Elemental: Immune to weather damage"""
    immune = RacialPassives.apply_elemental_passive()
    assert immune == True, "Elemental should be immune to weather damage"


def test_undead_passive_first_time():
    """Undead: Revive for 1 turn when killed (first time)"""
    undead = create_pet("Undead", PetFamily.UNDEAD)
    undead.stats.current_hp = 0  # Dead
    
    revived = RacialPassives.apply_undead_passive(undead)
    
    assert revived == True, "Undead should revive first time"
    assert undead.has_undead_revive == True
    assert undead.revive_turns_remaining == 1
    assert undead.has_used_undead_revive == True


def test_undead_passive_second_time():
    """Undead: Cannot revive twice"""
    undead = create_pet("Undead", PetFamily.UNDEAD)
    undead.has_used_undead_revive = True  # Already used revive
    
    revived = RacialPassives.apply_undead_passive(undead)
    
    assert revived == False, "Undead should not revive second time"


def test_mechanical_passive_first_time():
    """Mechanical: Revive to 25% HP once"""
    mechanical = create_pet("Mechanical", PetFamily.MECHANICAL, hp=1000)
    mechanical.stats.current_hp = 0  # Dead
    
    revived = RacialPassives.apply_mechanical_passive(mechanical)
    
    assert revived == True, "Mechanical should revive first time"
    assert mechanical.stats.current_hp == 250, "Should revive to 25% HP (250/1000)"
    assert mechanical.has_used_mechanical_revive == True


def test_mechanical_passive_second_time():
    """Mechanical: Cannot revive twice"""
    mechanical = create_pet("Mechanical", PetFamily.MECHANICAL, hp=1000)
    mechanical.has_used_mechanical_revive = True  # Already used revive
    
    revived = RacialPassives.apply_mechanical_passive(mechanical)
    
    assert revived == False, "Mechanical should not revive second time"


def test_dragonkin_trigger():
    """Dragonkin: Buff triggers when falling below 25% HP"""
    dragonkin = create_pet("Dragonkin", PetFamily.DRAGONKIN, hp=1000)
    
    # Pet falls from 300 HP to 200 HP (crossing 25% threshold)
    dragonkin.stats.current_hp = 200
    triggered = RacialPassives.check_dragonkin_trigger(dragonkin, previous_hp=300)
    
    assert triggered == True, "Dragonkin buff should trigger when falling below 25%"


def test_dragonkin_no_trigger():
    """Dragonkin: Buff doesn't trigger when already below 50%"""
    dragonkin = create_pet("Dragonkin", PetFamily.DRAGONKIN, hp=1000)
    dragonkin.stats.current_hp = 300
    
    # Pet falls from 400 HP to 300 HP (both below 50%)
    triggered = RacialPassives.check_dragonkin_trigger(dragonkin, previous_hp=400)
    
    assert triggered == False, "Dragonkin buff should not trigger if already below 50%"


def test_dragonkin_passive_buff_ready():
    """Dragonkin: +50% damage when buff is ready"""
    dragonkin = create_pet("Dragonkin", PetFamily.DRAGONKIN)
    dragonkin.dragonkin_buff_ready = True
    
    modifier = RacialPassives.apply_dragonkin_passive(dragonkin)
    
    assert modifier == 1.5, "Dragonkin with ready buff should get +50% damage"


def test_dragonkin_passive_no_buff():
    """Dragonkin: Normal damage when buff not ready"""
    dragonkin = create_pet("Dragonkin", PetFamily.DRAGONKIN)
    dragonkin.dragonkin_buff_ready = False
    
    modifier = RacialPassives.apply_dragonkin_passive(dragonkin)
    
    assert modifier == 1.0, "Dragonkin without buff should get normal damage"


if __name__ == "__main__":
    # Run all tests
    pytest.main([__file__, "-v"])
