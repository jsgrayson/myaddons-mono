
import unittest
import os
import json
from simulator.strategy_manager import StrategyManager

class TestStrategyManager(unittest.TestCase):
    def setUp(self):
        # Create a dummy strategies file
        self.test_file = "test_strategies.json"
        self.data = {
            "Test Expansion": {
                "Test Category": [
                    {
                        "encounter_name": "Test NPC",
                        "url": "http://example.com",
                        "strategies": [
                            {
                                "name": "Test Strat",
                                "script": "use(123)",
                                "pet_slots": [
                                    [{"id": 1}],
                                    [{"id": 2}],
                                    [{"id": 3}]
                                ]
                            }
                        ]
                    }
                ]
            }
        }
        with open(self.test_file, "w") as f:
            json.dump(self.data, f)
            
        self.manager = StrategyManager(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_get_strategy_exact_match(self):
        strat = self.manager.get_strategy("Test NPC")
        self.assertIsNotNone(strat)
        self.assertEqual(strat['encounter_name'], "Test NPC")
        self.assertEqual(strat['strategy_name'], "Test Strat")
        self.assertIn("Test NPC:1:2:3:use(123)", strat['rematch_string'])

    def test_get_strategy_fuzzy_match(self):
        strat = self.manager.get_strategy("test npc") # Lowercase
        self.assertIsNotNone(strat)
        self.assertEqual(strat['encounter_name'], "Test NPC")

    def test_get_strategy_not_found(self):
        strat = self.manager.get_strategy("Unknown NPC")
        self.assertIsNone(strat)

if __name__ == '__main__':
    unittest.main()
