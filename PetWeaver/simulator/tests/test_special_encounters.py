"""
Test Special Encounter Mechanics

Verifies that gimmick fight mechanics work correctly.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator.battle_state import Pet, PetStats, Ability, PetFamily, PetQuality, BattleState, Team, TurnAction, Buff, BuffType
from simulator.special_encounters import SpecialEncounterHandler
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


def test_rocko_immunity_active():
    """Rocko: Immune for first 10 turns"""
    rocko = create_pet("Rocko", PetFamily.ELEMENTAL)
    
    # Turn 1
    is_immune = SpecialEncounterHandler.apply_rocko_immunity(rocko, 1)
    assert is_immune == True, "Rocko should be immune on turn 1"
    
    # Turn 10
    is_immune = SpecialEncounterHandler.apply_rocko_immunity(rocko, 10)
    assert is_immune == True, "Rocko should be immune on turn 10"
    assert rocko.stats.current_hp > 0, "Rocko should be alive"


def test_rocko_immunity_expired():
    """Rocko: Dies on turn 11"""
    rocko = create_pet("Rocko", PetFamily.ELEMENTAL)
    
    # Turn 11
    is_immune = SpecialEncounterHandler.apply_rocko_immunity(rocko, 11)
    
    assert is_immune == False, "Rocko should not be immune on turn 11"
    assert rocko.stats.current_hp == 0, "Rocko should die on turn 11"


def test_gorespine_gore_new():
    """Gorespine: Applies Gore Stack buff"""
    gorespine = create_pet("Gorespine", PetFamily.BEAST)
    
    SpecialEncounterHandler.apply_gorespine_gore(gorespine, 1)
    
    assert len(gorespine.active_buffs) == 1
    buff = gorespine.active_buffs[0]
    assert buff.type == BuffType.DOT
    assert buff.stacks == 1
    assert buff.magnitude == 10


def test_gorespine_gore_stack():
    """Gorespine: Stacks Gore buff"""
    gorespine = create_pet("Gorespine", PetFamily.BEAST)
    
    # First application
    SpecialEncounterHandler.apply_gorespine_gore(gorespine, 1)
    
    # Second application
    SpecialEncounterHandler.apply_gorespine_gore(gorespine, 2)
    
    assert len(gorespine.active_buffs) == 1
    buff = gorespine.active_buffs[0]
    assert buff.stacks == 2
    assert buff.magnitude == 20  # 10 + 10


def test_life_exchange():
    """Life Exchange: Swaps HP percentages"""
    # Attacker: 1000/1000 HP (100%)
    attacker = create_pet("Attacker", PetFamily.HUMANOID, hp=1000)
    
    # Defender: 200/1000 HP (20%)
    defender = create_pet("Defender", PetFamily.DRAGONKIN, hp=1000)
    defender.stats.current_hp = 200
    
    SpecialEncounterHandler.apply_life_exchange(attacker, defender)
    
    # Attacker should now have 20% HP (200)
    assert attacker.stats.current_hp == 200
    
    # Defender should now have 100% HP (1000)
    assert defender.stats.current_hp == 1000


def test_mind_games():
    """Mind Games: Damages team for 25% MAX HP (Standard Strategy Choice)"""
    # Create team
    # Pet1: 1000 HP (Current 800)
    pet1 = create_pet("Pet1", PetFamily.HUMANOID, hp=1000)
    pet1.stats.current_hp = 800
    
    # Pet2: 2000 HP (Current 2000)
    pet2 = create_pet("Pet2", PetFamily.BEAST, hp=2000)
    
    team = Team(pets=[pet1, pet2], active_pet_index=0)
    
    SpecialEncounterHandler.apply_mind_games(team, pet1)
    
    # Pet1: Takes 25% of Max HP (250)
    # 800 - 250 = 550
    assert pet1.stats.current_hp == 550, f"Pet1 should take 250 damage (25% of 1000), got {pet1.stats.current_hp}"
    
    # Pet2: Takes 25% of Max HP (500)
    # 2000 - 500 = 1500
    assert pet2.stats.current_hp == 1500, f"Pet2 should take 500 damage (25% of 2000), got {pet2.stats.current_hp}"
    
    # Check NO stun on active pet (since we chose damage)
    assert len(pet1.active_buffs) == 0, "Active pet should NOT be stunned"


def test_toxic_skin():
    """Toxic Skin: Reflects damage"""
    attacker = create_pet("Attacker", PetFamily.HUMANOID, hp=1000)
    
    # Deal 100 damage
    reflected = SpecialEncounterHandler.apply_toxic_skin(attacker, 100)
    
    # Should reflect 25% = 25 damage
    assert reflected == 25
    assert attacker.stats.current_hp == 975  # 1000 - 25


def test_bone_prison():
    """Bone Prison: Stuns target"""
    pet = create_pet("Target", PetFamily.UNDEAD)
    
    SpecialEncounterHandler.apply_bone_prison(pet)
    
    assert len(pet.active_buffs) == 1
    assert pet.active_buffs[0].type == BuffType.STUN
    assert pet.active_buffs[0].duration == 2


def test_shell_shield():
    """Shell Shield: Reduces damage"""
    pet = create_pet("Shielded", PetFamily.ELEMENTAL)
    
    SpecialEncounterHandler.apply_shell_shield(pet)
    
    assert len(pet.active_buffs) == 1
    assert pet.active_buffs[0].type == BuffType.STAT_MOD
    assert pet.active_buffs[0].stat_affected == 'damage_taken'
    assert pet.active_buffs[0].magnitude == 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
