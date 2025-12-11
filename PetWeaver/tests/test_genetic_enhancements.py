import unittest
import random
from genetic.evolution import EvolutionEngine
from genetic.genome import TeamGenome, PetGene, StrategyGene

class MockEvaluator:
    def __init__(self):
        self.target_team = None
        self.species_db = {}
        self.ability_db = {}
    
    def evaluate(self, genome):
        # Simple fitness: sum of species IDs (just for testing)
        return sum(p.species_id for p in genome.pets)

class TestGeneticEnhancements(unittest.TestCase):
    def setUp(self):
        self.evaluator = MockEvaluator()
        self.engine = EvolutionEngine(self.evaluator, population_size=10, mutation_rate=0.5, elitism_rate=0.2)
        self.engine.ability_db = {1: [1], 2: [2], 3: [3], 4: [4], 5: [5]}
        self.available_species = [1, 2, 3, 4, 5]
        
        # Create a dummy population
        self.engine.population = []
        for i in range(10):
            # Create genomes with distinct species IDs so we can track them
            # Genome i has species [i, i, i] (modulo 5)
            sid = (i % 5) + 1
            genome = TeamGenome()
            genome.pets = [
                PetGene(species_id=sid, abilities=[1, 1, 1]),
                PetGene(species_id=sid, abilities=[1, 1, 1]),
                PetGene(species_id=sid, abilities=[1, 1, 1])
            ]
            genome.fitness = i * 10 # distinct fitness
            self.engine.population.append(genome)
            
        # Set best genome manually
        self.engine.best_genome = self.engine.population[-1] # The one with fitness 90
        
        # Initialize slot pools manually for testing
        self.engine.slot_pools = [self.available_species, self.available_species, self.available_species]

    def test_tournament_selection(self):
        """Test that tournament selection picks better individuals"""
        # With k=3, it's very likely to pick a high fitness individual
        # The max fitness is 90. The avg is 45.
        
        selected = [self.engine._tournament_select(k=3) for _ in range(100)]
        avg_selected_fitness = sum(g.fitness for g in selected) / 100
        
        # Average of random selection would be ~45. Tournament should be significantly higher.
        self.assertGreater(avg_selected_fitness, 60, "Tournament selection should favor higher fitness")

    def test_crossover_diversity(self):
        """Test that crossover produces mixed children"""
        parent_a = self.engine.population[0] # Species [1, 1, 1]
        parent_b = self.engine.population[1] # Species [2, 2, 2]
        
        # Force a crossover where we get a mix
        # Since crossover is random 50/50 per slot, we might get [1, 2, 1] etc.
        # We run it multiple times to ensure we get at least one mix
        mixed = False
        for _ in range(20):
            child = parent_a.crossover(parent_b)
            p1 = child.pets[0].species_id
            p2 = child.pets[1].species_id
            p3 = child.pets[2].species_id
            
            if (p1 != p2) or (p1 != p3) or (p2 != p3):
                mixed = True
                break
        
        self.assertTrue(mixed, "Crossover should eventually produce a child with mixed genes from parents")

    def test_lock_enforcement(self):
        """Test that locked slots are preserved even after crossover/mutation"""
        # Lock slot 0 requires win_status to be 'W..'
        
        # Ensure the best genome in the population has the locked species and correct win status
        best_idx = max(range(len(self.engine.population)), key=lambda i: self.engine.population[i].fitness)
        self.engine.population[best_idx].pets[0].species_id = 999
        self.engine.population[best_idx].fitness = 9999
        self.engine.population[best_idx].win_status = "WLL" # Locks slot 0
        
        # Run evolution step
        self.engine.evolve_generation(self.available_species)
        
        # Check that ALL individuals in new population have species 999 in slot 0
        for genome in self.engine.population:
            self.assertEqual(genome.pets[0].species_id, 999, "Locked slot 0 should be preserved in all children")
            
    def test_elitism(self):
        """Test that top individuals are preserved"""
        # Top fitness was 90
        top_fitness_before = max(g.fitness for g in self.engine.population)
        
        self.engine.evolve_generation(self.available_species)
        
        top_fitness_after = max(g.fitness for g in self.engine.population)
        self.assertEqual(top_fitness_after, top_fitness_before, "Elitism should preserve the best fitness")

if __name__ == '__main__':
    unittest.main()
