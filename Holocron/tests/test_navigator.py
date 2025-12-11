import unittest
from unittest.mock import MagicMock
from pathfinder_engine import PathfinderEngine

class TestNavigator(unittest.TestCase):
    def setUp(self):
        self.mock_deeppockets = MagicMock()
        # Initialize with mock DB url (not used since we load mock data)
        self.engine = PathfinderEngine("mock_url", self.mock_deeppockets)
        self.engine.load_mock_data()

    def test_tsp_optimization(self):
        # Start at Stormwind (84)
        # Destinations: 
        # - Oribos (1670) - 15s away
        # - Dragon Isles (1978) - 120s away
        
        # Optimal path should be 84 -> 1670 -> 1978 (if we assume 1670 is closer or connected)
        # Actually, in my mock data:
        # 84 <-> 1670 (15s)
        # 84 <-> 1978 (120s)
        # 1670 is NOT connected to 1978 directly.
        
        # So from 84:
        # Nearest is 1670 (15s).
        # From 1670, can we go to 1978? No direct edge.
        # My find_shortest_path handles multi-hop? Yes, Dijkstra.
        # Path 1670 -> 84 -> 1978 is 15s + 120s = 135s.
        
        # If we went 84 -> 1978 first (120s).
        # Then 1978 -> 84 -> 1670 (120s + 15s) = 135s.
        
        # Total time 84->1670->1978 = 15 + 135 = 150s.
        # Total time 84->1978->1670 = 120 + 135 = 255s.
        
        # So 1670 should be first.
        
        result = self.engine.optimize_route(84, [1978, 1670])
        
        self.assertTrue(result["success"])
        route = result["route_order"]
        # Route includes start: [84, 1670, 1978]
        self.assertEqual(route[1], 1670)
        self.assertEqual(route[2], 1978)

    def test_bank_stop_insertion(self):
        # Mock DeepPockets to say we have item 194820 in Bank
        self.mock_deeppockets.search_inventory.return_value = [
            {"character": "Main", "container": "Bank", "count": 5}
        ]
        
        # Quest 123 requires 194820
        bank_stops = self.engine.check_quest_items([123])
        
        self.assertIn(-1, bank_stops) # -1 is our mock bank zone

if __name__ == '__main__':
    unittest.main()
