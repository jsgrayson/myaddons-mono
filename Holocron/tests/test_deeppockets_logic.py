import unittest
from deeppockets_engine import DeepPocketsEngine

class TestDeepPockets(unittest.TestCase):
    def setUp(self):
        self.engine = DeepPocketsEngine()
        # Setup mock data
        self.engine.item_locations = {
            101: [
                {"character": "Main", "container": "Bag1", "count": 5},
                {"character": "Alt1", "container": "Bank", "count": 10}
            ],
            102: [
                {"character": "Alt1", "container": "Bag1", "count": 20}
            ],
            103: [
                {"character": "Main", "container": "Bag1", "count": 1}
            ]
        }
        self.engine.prices = {
            101: 100.0, # High value
            102: 0.5,   # Low value
            103: 50.0   # Medium value
        }

    def test_search_inventory_by_id(self):
        results = self.engine.search_inventory("101")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["character"], "Main")

    def test_get_remote_stash(self):
        # Item 102 is only on Alt1, so it should appear
        # Item 101 is on Main and Alt1, so it should NOT appear (as per current logic "not on main")
        # Item 103 is only on Main, so it should NOT appear
        
        stash = self.engine.get_remote_stash("Main")
        self.assertEqual(len(stash), 1)
        self.assertEqual(stash[0]["item_id"], 102)
        self.assertEqual(stash[0]["count"], 20)
        self.assertEqual(stash[0]["character"], "Alt1")

    def test_incinerator_value_density(self):
        bag_items = [
            {"item_id": 101, "count": 1}, # 100g
            {"item_id": 102, "count": 10}, # 5g total (0.5 * 10)
            {"item_id": 103, "count": 1}  # 50g
        ]
        
        candidates = self.engine.calculate_value_density(bag_items)
        
        # Should be sorted by total slot value: 
        # 1. Item 102 (5g)
        # 2. Item 103 (50g)
        # 3. Item 101 (100g)
        
        self.assertEqual(candidates[0]["item_id"], 102)
        self.assertEqual(candidates[0]["slot_value"], 5.0)
        
        self.assertEqual(candidates[1]["item_id"], 103)
        self.assertEqual(candidates[2]["item_id"], 101)

if __name__ == '__main__':
    unittest.main()
