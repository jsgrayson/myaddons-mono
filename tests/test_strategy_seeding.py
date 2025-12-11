import unittest
import json
import os
import shutil
from simulator.strategy_manager import StrategyManager
from genetic.evolution import EvolutionEngine
from genetic.genome import TeamGenome

class MockEvaluator:
    def __init__(self):
        # Create a dummy target team for build_slot_pools
        from simulator import Team, Pet, PetStats, PetFamily, PetQuality, Ability
        self.target_team = Team([
            Pet(999, "Dummy Enemy", PetFamily.BEAST, PetQuality.RARE, PetStats(1000, 1000, 100, 100), [])
        ])
        self.species_db = {}
        self.ability_db = {}
    
    def evaluate(self, genome):
        return 1000 # Dummy fitness

class TestStrategySeeding(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_strategies.json"
        self.strategies = {
            "Pandaria": {
                "Beasts of Fable": [
                    {
                        "encounter_name": "Major Payne",
                        "url": "http://example.com",
                        "strategies": [
                            {
                                "name": "Meta Strat",
                                "pet_slots": [
                                    [{"id": 1155}], # Iron Starlette
                                    [{"id": 845}],  # Fel Flame
                                    [{"id": 1194}]  # Emperor Crab
                                ],
                                "script": "use(Wind-Up)"
                            }
                        ]
                    }
                ]
            }
        }
        with open(self.test_file, 'w') as f:
            json.dump(self.strategies, f)
            
        self.manager = StrategyManager("strategies_master.json")
        self.evaluator = MockEvaluator()
        self.engine = EvolutionEngine(self.evaluator, population_size=10)
        
        # Mock DBs
        self.ability_db = {"1155": [1, 2, 3], "845": [4, 5, 6], "1194": [7, 8, 9]}
        self.species = ["1155", "845", "1194", "9999"]

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_seeding_dos_ryga(self):
        self._test_specific_encounter("Dos-Ryga", expected_count=3)

    def test_seeding_tiun(self):
        self._test_specific_encounter("Ti'un the Wanderer", expected_count=2)

    def test_seeding_kafi(self):
        self._test_specific_encounter("Kafi", expected_count=2)

    def test_seeding_unknown_npc(self):
        target_name = "Nonexistent NPC"
        print(f"\nTesting Unknown NPC: {target_name}...")
        
        # 1. Fetch Recommendation
        recommended_ids = self.manager.get_recommended_team(target_name)
        print(f"Result for unknown: {recommended_ids}")
        self.assertIsNone(recommended_ids)
        
        # 2. Seed Evolution Engine (should handle None/Empty)
        seed_teams = [recommended_ids] if recommended_ids else []
        
        print("Initializing population (expecting random)...")
        self.engine.initialize_population(
            self.species,
            self.ability_db,
            seed_teams=seed_teams
        )
        
        # 3. Verify Population
        # Should have created a population
        self.assertEqual(len(self.engine.population), 10)
        # First genome should NOT be None
        self.assertIsNotNone(self.engine.population[0])
        print("SUCCESS: Handled unknown NPC gracefully!")

    def _test_specific_encounter(self, target_name, expected_count):
        print(f"\nTesting Encounter: {target_name}...")
        recommended_ids = self.manager.get_recommended_team(target_name)
        self.assertIsNotNone(recommended_ids, f"Should find strategy for {target_name}")
        
        # Filter out None/0 to get actual pets
        valid_ids = [pid for pid in recommended_ids if pid]
        self.assertEqual(len(valid_ids), expected_count, f"Expected {expected_count} pets for {target_name}, got {valid_ids}")
        
        seed_teams = [recommended_ids]
        self.engine.initialize_population(
            self.species,
            self.ability_db,
            seed_teams=seed_teams
        )
        
        seeded_genome = self.engine.population[0]
        pet_ids = [p.species_id for p in seeded_genome.pets]
        # Filter out None/0
        actual_ids = [pid for pid in pet_ids if pid] 
        
        self.assertEqual(actual_ids, valid_ids)
        print(f"SUCCESS: Verified {target_name} -> {valid_ids}")

if __name__ == '__main__':
    unittest.main()
