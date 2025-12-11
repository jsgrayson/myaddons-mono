import unittest
from simulator.queue_manager import QueueManager

class TestQueueManager(unittest.TestCase):
    def setUp(self):
        self.qm = QueueManager({}, {})

    def test_optimal_carry_team_selection(self):
        # Test 1: Flying Enemy (Should pick Magic/Dragonkin counter? My logic uses hardcoded Iron Starlette for now or specific map)
        # My map: Flying -> Iron Starlette (1155)
        target = {'npc_pets': [{'family': 'Flying'}, {'family': 'Beast'}]}
        leveling_pet = {'name': 'Leveling Pet', 'level': 1}
        
        team = self.qm.get_optimal_carry_team(leveling_pet, target)
        
        self.assertEqual(team['leveling_slot'], 0)
        self.assertEqual(len(team['pets']), 3)
        self.assertEqual(team['pets'][0]['name'], 'Leveling Pet')
        
        # Check Carry 1 (Counter to Flying)
        # In my code: Flying -> Iron Starlette
        self.assertEqual(team['pets'][1]['name'], "Iron Starlette")
        
        # Check Carry 2 (Counter to Beast)
        # In my code: Beast -> Iron Starlette
        self.assertEqual(team['pets'][2]['name'], "Iron Starlette")

    def test_bandage_efficiency(self):
        # Initial state
        self.assertEqual(self.qm.calculate_bandage_efficiency(), 100.0)
        
        # Add a perfect win (100% HP)
        self.qm.record_result({'win': True, 'hp_remaining': 100})
        self.assertEqual(self.qm.calculate_bandage_efficiency(), 100.0)
        
        # Add a scrape win (10% HP)
        # Loss = 90. Avg Loss = (0 + 90) / 2 = 45. Efficiency = 55.
        self.qm.record_result({'win': True, 'hp_remaining': 10})
        self.assertEqual(self.qm.calculate_bandage_efficiency(), 55.0)
        
        # Add a loss (0 HP, 100 penalty)
        # Loss = 100. Avg Loss = (0 + 90 + 100) / 3 = 63.33. Efficiency = 36.66
        self.qm.record_result({'win': False, 'hp_remaining': 0})
        self.assertAlmostEqual(self.qm.calculate_bandage_efficiency(), 36.66, places=1)

if __name__ == '__main__':
    unittest.main()
