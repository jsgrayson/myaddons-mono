import unittest
from genetic.evolution import EvolutionEngine
from genetic.fitness import FitnessEvaluator
from simulator.strategy_manager import StrategyManager
from simulator.battle_state import PetFamily

class MockEvaluator(FitnessEvaluator):
    def evaluate(self, genome):
        return 100

class TestGASeeding(unittest.TestCase):
    def setUp(self):
        # Pass dummy arguments to satisfy FitnessEvaluator.__init__
        self.evaluator = MockEvaluator(target_team=None, ability_db={}, species_db={})
        self.engine = EvolutionEngine(self.evaluator, population_size=10)
        
        # Mock ability DB
        self.ability_db = {
            71163: [1, 2, 3], # Val'kyr
            115589: [4, 5, 6], # Ikky
            69651: [7, 8, 9], # Zandalari
            12345: [10, 11, 12], # Random
            99999: [13, 14, 15] # Random
        }
        
        # Mock Strategy Manager
        self.strategy_manager = StrategyManager("strategies_cleaned.json")
        # Mock get_recommended_team to return a known team
        self.strategy_manager.get_recommended_team = lambda name: [12345, 99999, 0]
        
    def test_seeding_logic(self):
        available_species = [71163, 115589, 69651, 12345, 99999]
        
        self.engine.initialize_population(
            available_species, 
            self.ability_db, 
            npc_name="Test Boss", 
            strategy_manager=self.strategy_manager
        )
        
        # Check population size
        self.assertEqual(len(self.engine.population), 10)
        
        # Check for Encounter-Specific Seed (12345, 99999)
        # We added 3 copies
        encounter_seeds = 0
        for genome in self.engine.population:
            pids = [p.species_id for p in genome.pets]
            # Check exact match including empty slot (which won't be in random teams)
            # Note: seed has 0, but genome.pets only contains PetGene objects for non-empty slots?
            # Let's check how from_team_ids works. It skips 0s.
            # So genome.pets will have length 2.
            # Random teams have length 3.
            if len(genome.pets) == 2 and pids[0] == 12345 and pids[1] == 99999:
                encounter_seeds += 1
        self.assertEqual(encounter_seeds, 3, "Should have 3 copies of encounter seed")
        
        # Check for Universal Meta Seed (71163, 115589, 69651)
        # We added 2 copies
        meta_seeds = 0
        for genome in self.engine.population:
            pids = [p.species_id for p in genome.pets]
            if pids == [71163, 115589, 69651]:
                meta_seeds += 1
        self.assertEqual(meta_seeds, 2, "Should have 2 copies of meta seed")

if __name__ == '__main__':
    unittest.main()
