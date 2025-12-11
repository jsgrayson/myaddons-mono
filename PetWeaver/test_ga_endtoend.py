"""
Quick end-to-end test of the genetic algorithm system
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulator import BattleSimulator, Team, Pet, PetStats, Ability, PetFamily, PetQuality
from genetic.genome import TeamGenome, PetGene
from genetic.fitness import FitnessEvaluator

print("Creating target NPC team...")
# Create a simple 1-pet NPC team
npc_pet = Pet(
    species_id=1,
    name="NPC Pet",
    family=PetFamily.BEAST,
    quality=PetQuality.RARE,
    stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=300),
    abilities=[
        Ability(1, "Bite", 20, 100, 0, 0, PetFamily.BEAST),
        Ability(2, "Claw", 15, 100, 0, 0, PetFamily.BEAST),
        Ability(3, "Tackle", 25, 95, 1, 0, PetFamily.BEAST)
    ]
)
target_team = Team([npc_pet])

print("Creating player team genome...")
# Create a simple genome
gene = PetGene(
    species_id=2,
    abilities=[1, 2, 3]  # Ability IDs
)
genome = TeamGenome(pets=[gene])

print("Initializing fitness evaluator...")
evaluator = FitnessEvaluator(
    target_team=target_team,
    ability_db={},
    species_db={},
    target_name="Test NPC"
)

print("Running genetic algorithm simulation (3 battles)...")
try:
    fitness_score = evaluator.evaluate(genome, num_battles=3)
    print(f"✅ SUCCESS! Fitness score: {fitness_score:.2f}")
    print("✅ Genetic algorithm end-to-end test PASSED!")
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
