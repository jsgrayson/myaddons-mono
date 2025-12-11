import random
from genetic.genome import TeamGenome, PetGene, StrategyGene

# Mock ability DB
ability_db = {
    1: [10],  # Species 1 has only 1 ability (Should crash current code)
    2: [20, 21, 22, 23, 24, 25],
    3: [30, 31, 32, 33, 34, 35]
}

# Create a random genome
print("Creating random genome...")
try:
    genome = TeamGenome.random([1, 2, 3], ability_db)
    print("Random creation success")
    
    print("Attempting mutation...")
    genome.mutate([1, 2, 3], ability_db, mutation_rate=1.0)
    print("Mutation success")
except Exception as e:
    print(f"CRASHED: {e}")
    import traceback
    traceback.print_exc()
