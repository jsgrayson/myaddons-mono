#!/usr/bin/env python3
"""Minimal test to find the hang issue"""
import json

print("Step 1: Loading abilities.json...")
with open('abilities.json') as f:
    ability_data = json.load(f)
species_abilities = {int(k): v for k, v in ability_data.get('species_abilities', {}).items()}
abilities_db = ability_data.get('abilities', {})
print(f"  ✓ Loaded {len(species_abilities)} species")

print("Step 2: Loading species_data.json...")
with open('species_data.json') as f:
    species_db = json.load(f)
print(f"  ✓ Loaded {len(species_db)} species data")

print("Step 3: Importing simulator...")
from simulator import Team, Pet, Ability, PetFamily, PetQuality, PetStats
print("  ✓ Simulator imported")

print("Step 4: Creating boss team...")
grizzle = Pet(979, "Grizzle", PetFamily.BEAST, PetQuality.EPIC, PetStats(1700, 1700, 320, 270), [
    Ability(1, "Bash", 25, 100, 0, 0, PetFamily.BEAST)
])
target_team = Team([grizzle])
print("  ✓ Boss team created")

print("Step 5: Importing genetic modules...")
from genetic.fitness import FitnessEvaluator
from genetic.evolution import EvolutionEngine
print("  ✓ Genetic modules imported")

print("Step 6: Creating evaluator...")
evaluator = FitnessEvaluator(target_team, abilities_db, species_db, target_name="Test")
print("  ✓ Evaluator created")

print("Step 7: Creating engine...")
engine = EvolutionEngine(evaluator, population_size=10, mutation_rate=0.5, elitism_rate=0.1)
print("  ✓ Engine created")

print("Step 8: Initializing population...")
engine.initialize_population(
    list(species_db.keys()),
    species_abilities,
    seed_teams=[[1155, 845, 1194]]
)
print("  ✓ Population initialized")

print("\n✓ ALL STEPS COMPLETED - NO HANG!")
