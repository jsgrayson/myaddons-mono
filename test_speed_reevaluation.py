"""
Test Speed Re-evaluation - verify speed buffs are recalculated each round
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulator.battle_state import Pet, PetStats, Ability, PetFamily, PetQuality, Buff, BuffType, TurnAction
from simulator.turn_system import TurnSystem

print("Testing Speed Re-evaluation...")

# Create two pets
fast_pet = Pet(1, "Fast", PetFamily.BEAST, PetQuality.RARE,
               PetStats(1000, 1000, 300, 300), [])  # Speed 300
slow_pet = Pet(2, "Slow", PetFamily.CRITTER, PetQuality.RARE,
               PetStats(1000, 1000, 300, 100), [])  # Speed 100

turn_sys = TurnSystem()
normal_ability = Ability(1, "Normal", 20, 100, 0, 0, PetFamily.BEAST)

# Test 1: Initially, fast pet should go first
print("\n1. Initial state (no buffs):")
fast_action = TurnAction('player', 'ability', ability=normal_ability)
slow_action = TurnAction('enemy', 'ability', ability=normal_ability)
order = turn_sys.determine_turn_order(fast_pet, fast_action, slow_pet, slow_action)
assert order[0][0] == 'player', "Fast pet should go first initially"
print(f"  ✅ Fast pet (speed={fast_pet.get_effective_speed()}) goes before Slow pet (speed={slow_pet.get_effective_speed()})")

# Test 2: Add speed BUFF to slow pet (+50%)
print("\n2. After adding +50% speed buff to Slow pet:")
speed_buff = Buff(
    type=BuffType.STAT_MOD,
    name="Speed Up",
    duration=3,
    magnitude=1.5,  # 150% of base speed
    stat_affected='speed',
    source_ability="Test"
)
slow_pet.active_buffs.append(speed_buff)

# Recalculate - slow pet should now be faster
order = turn_sys.determine_turn_order(fast_pet, fast_action, slow_pet, slow_action)
slow_effective_speed = slow_pet.get_effective_speed()  # Should be 100 * 1.5 = 150
print(f"  Fast pet speed: {fast_pet.get_effective_speed()}")
print(f"  Slow pet speed (buffed): {slow_effective_speed}")

# Fast pet still faster (300 > 150)
assert order[0][0] == 'player', "Fast pet should still go first (300 > 150)"
print(f"  ✅ Speed recalculated: Slow pet now has {slow_effective_speed} speed")

# Test 3: Add STRONGER buff that makes slow pet faster
print("\n3. Increasing buff to +300% speed:")
speed_buff.magnitude = 4.0  # 400% of base speed
slow_effective_speed = slow_pet.get_effective_speed()  # Should be 100 * 4.0 = 400

order = turn_sys.determine_turn_order(fast_pet, fast_action, slow_pet, slow_action)
print(f"  Fast pet speed: {fast_pet.get_effective_speed()}")
print(f"  Slow pet speed (buffed): {slow_effective_speed}")

# Now slow pet should go first (400 > 300)
assert order[0][0] == 'enemy', "Buffed Slow pet should now go first (400 > 300)"
print(f"  ✅ Slow pet (now {slow_effective_speed} speed) goes BEFORE Fast pet!")

# Test 4: Remove buff - speed should return to normal
print("\n4. After removing buff:")
slow_pet.active_buffs.clear()
slow_effective_speed = slow_pet.get_effective_speed()  # Should be back to 100

order = turn_sys.determine_turn_order(fast_pet, fast_action, slow_pet, slow_action)
assert order[0][0] == 'player', "Fast pet should go first again after buff removed"
assert slow_effective_speed == 100, "Slow pet speed should return to 100"
print(f"  ✅ Slow pet speed reset to {slow_effective_speed} (buff removed)")

print("\n✅ All Speed Re-evaluation tests PASSED!")
print("\nVerified:")
print("  • Speed is recalculated dynamically each round")
print("  • Speed buffs are properly applied")
print("  • Turn order changes based on current speed")
print("  • Speed resets when buffs are removed")
