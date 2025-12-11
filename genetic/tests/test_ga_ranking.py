
import unittest
from unittest.mock import MagicMock
from genetic.evolution import EvolutionEngine
from genetic.genome import TeamGenome, PetGene
from genetic.fitness import FitnessEvaluator

class MockFitnessEvaluator:
    def evaluate(self, genome):
        # Return the pre-set fitness if available, else 0
        return getattr(genome, '_test_fitness', 0)

class TestGARanking(unittest.TestCase):
    def test_ranking_logic(self):
        # Setup
        evaluator = MockFitnessEvaluator()
        engine = EvolutionEngine(evaluator, population_size=5, elitism_rate=0.0)
        
        # Create dummy population
        engine.population = []
        for i in range(5):
            genome = TeamGenome()
            genome._test_fitness = i * 10  # 0, 10, 20, 30, 40
            # Add dummy pets with abilities to avoid errors if accessed
            genome.pets = [
                PetGene(1, abilities=[1, 2, 3]), 
                PetGene(1, abilities=[1, 2, 3]), 
                PetGene(1, abilities=[1, 2, 3])
            ]
            engine.population.append(genome)
            
        # Run one generation
        # We need to pass available_species and ability_db, but they won't be used 
        # because we are mocking evaluate and not doing mutation/crossover yet
        # Wait, evolve_generation DOES do crossover/mutation which requires these.
        # But we only care about the sorting which happens BEFORE reproduction.
        # However, the function returns 'top_genomes' which is what we want to check.
        # And it replaces the population.
        
        # To avoid complex mocking of mutation/crossover, we can just check the sorting 
        # by inspecting the code or by mocking the reproduction part too?
        # Or we can just let it run, assuming mutation doesn't crash with empty DB.
        
        # Let's try to run it.
        available_species = [1]
        ability_db = {1: [1, 2, 3, 4, 5, 6]}
        
        # We need to make sure _tournament_select doesn't crash.
        # It uses random.sample on population.
        
        # Run
        stats = engine.evolve_generation(available_species)
        
        # Check top_genomes
        top_genomes = stats['top_genomes']
        
        # Should be sorted descending: 40, 30, 20
        self.assertEqual(len(top_genomes), 3)
        self.assertEqual(top_genomes[0]._test_fitness, 40)
        self.assertEqual(top_genomes[1]._test_fitness, 30)
        self.assertEqual(top_genomes[2]._test_fitness, 20)
        
        # Verify the order is strictly descending
        fitness_values = [g.fitness for g in top_genomes]
        self.assertEqual(fitness_values, [40, 30, 20])
        
        print("Ranking test passed!")

if __name__ == '__main__':
    unittest.main()
