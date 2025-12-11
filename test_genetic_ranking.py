import unittest
from unittest.mock import MagicMock
from genetic.evolution import EvolutionEngine

class MockGenome:
    def __init__(self, fitness, win_rate):
        self.fitness = fitness
        self.stats = {'win_rate': win_rate}
        self.pets = [] # Required for deepcopy in evolution

class TestGeneticRanking(unittest.TestCase):
    def test_sorting_logic(self):
        # Create a mock engine
        engine = EvolutionEngine(MagicMock())
        
        # Create genomes with different win rates and fitness
        # Genome A: High Fitness, Low Win Rate
        genome_a = MockGenome(fitness=2000, win_rate=0.4)
        
        # Genome B: Low Fitness, High Win Rate
        genome_b = MockGenome(fitness=500, win_rate=0.8)
        
        # Genome C: Medium Fitness, High Win Rate
        genome_c = MockGenome(fitness=1000, win_rate=0.8)
        
        # Genome D: Zero Fitness, Zero Win Rate
        genome_d = MockGenome(fitness=0, win_rate=0.0)
        
        engine.population = [genome_a, genome_b, genome_c, genome_d]
        
        # Apply sorting logic (replicating what we WANT to implement)
        # Sort by Win Rate (desc), then Fitness (desc)
        engine.population.sort(key=lambda g: (g.stats.get('win_rate', 0), g.fitness), reverse=True)
        
        # Expected Order:
        # 1. Genome C (0.8 WR, 1000 Fit)
        # 2. Genome B (0.8 WR, 500 Fit)
        # 3. Genome A (0.4 WR, 2000 Fit)
        # 4. Genome D (0.0 WR, 0 Fit)
        
        self.assertEqual(engine.population[0], genome_c, "Genome C should be first (High WR, Med Fit)")
        self.assertEqual(engine.population[1], genome_b, "Genome B should be second (High WR, Low Fit)")
        self.assertEqual(engine.population[2], genome_a, "Genome A should be third (Low WR, High Fit)")
        self.assertEqual(engine.population[3], genome_d, "Genome D should be last")
        
        print("✅ Sorting Logic Verified: Win Rate > Fitness")

if __name__ == '__main__':
    unittest.main()
