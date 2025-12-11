from dojo_engine import DojoEngine
import time

print("Initializing Dojo...")
dojo = DojoEngine(population_size=4)
dojo.initialize_population()
print(f"Population initialized: {len(dojo.population)} teams")

print("Running Generation 1...")
stats = dojo.run_generation()
print(f"Gen 1 Stats: {stats}")

print("Running Generation 2...")
stats = dojo.run_generation()
print(f"Gen 2 Stats: {stats}")

print("Dojo Test Complete!")
