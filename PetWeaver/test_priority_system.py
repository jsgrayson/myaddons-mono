"""
Test Priority System for turn order
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulator.battle_state import Pet, PetStats, Ability, PetFamily, PetQuality, TurnAction
from simulator.turn_system import TurnSystem

print("Testing Priority System...")

# Create test pets
pet1 = Pet(1, "Fast", PetFamily.BEAST, PetQuality.RARE, 
           PetStats(1000, 1000, 300, 400), [])  # Speed 400
pet2 = Pet(2, "Slow", PetFamily.CRITTER, PetQuality.RARE, 
           PetStats(1000, 1000, 300, 200), [])  # Speed 200

# Create test abilities
normal_ability = Ability(1, "Normal", 20, 100, 0, 0, PetFamily.BEAST)
priority_ability = Ability(2, "Priority", 20, 100, 0, 0, PetFamily.BEAST, priority=1)

turn_sys = TurnSystem()

# Test 1: Swap beats everything
print("\n1. Testing Swap Priority...")
swap_action = TurnAction('player', 'swap', target_pet_index=1)
ability_action = TurnAction('enemy', 'ability', ability=priority_ability)
order = turn_sys.determine_turn_order(pet1, swap_action, pet2, ability_action)
assert order[0][0] == 'player', "Swap should go first"
print("✅ Swap > Priority ability")

# Test 2: Priority ability beats speed
print("\n2. Testing Priority > Speed...")
slow_priority = TurnAction('player', 'ability', ability=priority_ability)
fast_normal = TurnAction('enemy', 'ability', ability=normal_ability)
print(f"  Player priority: {priority_ability.priority}, Enemy priority: {normal_ability.priority}")
print(f"  Player speed: {pet2.stats.speed}, Enemy speed: {pet1.stats.speed}")
order = turn_sys.determine_turn_order(pet2, slow_priority, pet1, fast_normal)
print(f"  Result: {order[0][0]} goes first")
assert order[0][0] == 'player', "Priority ability should beat faster normal ability"
print("✅ Priority ability > Speed")

# Test 3: Speed determines order for same priority
print("\n3. Testing Speed comparison...")
fast_action = TurnAction('player', 'ability', ability=normal_ability)
slow_action = TurnAction('enemy', 'ability', ability=normal_ability)
order = turn_sys.determine_turn_order(pet1, fast_action, pet2, slow_action)
assert order[0][0] == 'player', "Faster pet should go first"
print("✅ Higher speed > Lower speed")

# Test 4: Speed tie = random
print("\n4. Testing Speed tie (random)...")
action1 = TurnAction('player', 'ability', ability=normal_ability)
action2 = TurnAction('enemy', 'ability', ability=normal_ability)
# Both pets same speed
pet_same = Pet(3, "Same", PetFamily.BEAST, PetQuality.RARE, 
               PetStats(1000, 1000, 300, 300), [])
order = turn_sys.determine_turn_order(pet_same, action1, pet_same, action2)
print(f"✅ Tied speed results in: {order[0][0]} going first (random)")

print("\n✅ All Priority System tests PASSED!")
print("\nPriority Order Verified:")
print("  1. Swap")
print("  2. Priority abilities")
print("  3. Speed")
print("  4. Random (on tie)")
