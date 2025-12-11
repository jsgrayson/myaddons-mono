import json
import time
import sys
import random
from genetic.evolution import EvolutionEngine
from genetic.fitness import FitnessEvaluator
from simulator import Team, Pet, Ability, PetFamily, PetQuality, PetStats
from simulator.script_generator import TDScriptGenerator

# --- 1. Data Loading ---
print("Loading Data...")
try:
    with open('abilities.json') as f:
        ability_data = json.load(f)
    species_abilities = {int(k): v for k, v in ability_data.get('species_abilities', {}).items()}
    abilities_db = ability_data.get('abilities', {})
except FileNotFoundError:
    print("Error: abilities.json not found.")
    exit(1)

try:
    with open('species_data.json') as f:
        species_db = json.load(f)
except FileNotFoundError:
    species_db = {}

# --- 2. Boss Team ---
def create_boss_team():
    grizzle = Pet(979, "Grizzle (Boss)", PetFamily.BEAST, PetQuality.EPIC, PetStats(1700, 1700, 320, 270), [
        Ability(1, "Bash", 25, 100, 0, 0, PetFamily.BEAST),
        Ability(2, "Hibernate", 0, 100, 0, 4, PetFamily.BEAST),
        Ability(3, "Rampage", 35, 95, 0, 0, PetFamily.BEAST)])
    beakmaster = Pet(978, "Beakmaster (Boss)", PetFamily.MECHANICAL, PetQuality.EPIC, PetStats(1500, 1500, 290, 300), [
        Ability(4, "Batter", 10, 100, 0, 0, PetFamily.MECHANICAL),
        Ability(5, "Shock and Awe", 25, 100, 0, 3, PetFamily.MECHANICAL),
        Ability(6, "Wind-Up", 50, 90, 0, 2, PetFamily.MECHANICAL)])
    bloom = Pet(977, "Bloom (Boss)", PetFamily.ELEMENTAL, PetQuality.EPIC, PetStats(1400, 1400, 340, 250), [
        Ability(7, "Lash", 20, 100, 0, 0, PetFamily.ELEMENTAL),
        Ability(8, "Soothing Mists", 0, 100, 0, 3, PetFamily.ELEMENTAL),
        Ability(9, "Entangling Roots", 15, 100, 0, 4, PetFamily.ELEMENTAL)])
    return Team([grizzle, beakmaster, bloom])

target_team = create_boss_team()
print(f"Target: Major Payne (3 Epic Pets)")

# --- 3. Evolution Setup ---
evaluator = FitnessEvaluator(target_team, abilities_db, species_db, target_name="Major Payne")
engine = EvolutionEngine(evaluator, population_size=100, mutation_rate=0.5, elitism_rate=0.1)
available_species = list(species_abilities.keys())

print("Initializing Population (Smart Draft)...")
engine.initialize_population(available_species, species_abilities, npc_name="Major Payne")

print("\nStarting UNLIMITED Evolution (Press Ctrl+C to stop)...")
start_time = time.time()
gen = 0

try:
    while True:
        gen += 1
        result = engine.evolve_generation(available_species)
        best = result['best_fitness']
        status = result.get('win_status', '???')
        
        if gen == 1 or gen % 10 == 0 or best > 14000:
            top = result['top_genomes'][0]
            names = [species_db.get(str(p.species_id), {}).get('name', str(p.species_id)) for p in top.pets]
            print(f"\nGen {gen}: {best:.0f} ({status}) | Team: {names}")
        else:
            print(f"{best:.0f}", end=" | ", flush=True)

        # Score > 15,000 means Consistent Wins (due to num_battles=3)
        if best > 15000: 
            print(f"\n\nVICTORY DETECTED at Generation {gen}!")
            break

except KeyboardInterrupt:
    print("\n\nSimulation stopped by user.")

# --- 5. REPLAY & VERIFY ---
print("\n--- VERIFYING VICTORY (Hunting for Winning Seed) ---")
final_result = {}
attempts = 0
success = False

# Try 20 times to find the seed where it wins
while attempts < 20:
    attempts += 1
    final_result = evaluator.play_battle(engine.best_genome)
    if final_result['winner'] == 'player':
        print(f"Verified WIN on attempt {attempts}!")
        success = True
        break
    else:
        print(f"Attempt {attempts} failed (Bad RNG). Retrying...")

if success:
    print(f"\nResult: {final_result['winner'].upper()} (Turns: {final_result['turns']})")
    print("\n--- TD SCRIPT ---")
    script = TDScriptGenerator.generate_script(final_result['events'])
    print(script)
else:
    print("\n[WARNING] Could not reproduce victory. Strategy might be unstable.")

print("---------------------------")