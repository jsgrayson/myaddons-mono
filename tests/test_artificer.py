import unittest
from unittest.mock import MagicMock
from artificer_engine import ArtificerEngine

class TestArtificer(unittest.TestCase):
    def setUp(self):
        self.mock_goblin = MagicMock()
        self.mock_deeppockets = MagicMock()
        self.engine = ArtificerEngine(self.mock_goblin, self.mock_deeppockets)

    def test_concentration_value(self):
        # Test data is mocked inside engine for now
        results = self.engine.calculate_concentration_value()
        
        # We expect Elemental Potion to be top value
        # (1200 - 400) / 150 = 5.33 g/p
        # Plate Helm: (5000 - 2000) / 300 = 10 g/p
        # Enchant: (1200 - 150) / 200 = 5.25 g/p
        
        # Wait, Plate Helm is 10 g/p, so it should be first.
        self.assertEqual(results[0]["recipe_id"], 2002) # Helm
        self.assertEqual(results[0]["gold_per_concentration"], 10.0)

    def test_supply_chain(self):
        # Recipe 370607 needs:
        # 1. Hochenblume (194820) x 2 -> Total 20
        # 2. Resonant Crystal (200111) x 1 -> Total 10
        
        def search_side_effect(query):
            if query == "194820": # Hochenblume
                return [
                    {"character": "Alt1", "container": "Bank", "count": 15},
                    {"character": "Main", "container": "Bag1", "count": 0}
                ]
            elif query == "200111": # Crystal
                return [
                    {"character": "Main", "container": "Bag1", "count": 0}
                ] # None on alts
            return []

        self.mock_deeppockets.search_inventory.side_effect = search_side_effect
        
        result = self.engine.solve_supply_chain(370607, 10)
        
        # Should generate:
        # 1. Mail task for 15 Hochenblume from Alt1
        # 2. Shopping list for 5 Hochenblume
        # 3. Shopping list for 10 Crystals (since none on alts)
        
        self.assertEqual(len(result["mail_tasks"]), 1)
        self.assertEqual(result["mail_tasks"][0]["from"], "Alt1")
        self.assertEqual(result["mail_tasks"][0]["item_id"], 194820)
        self.assertEqual(result["mail_tasks"][0]["count"], 15)
        
        self.assertEqual(len(result["shopping_list"]), 2)
        # Verify shopping list contents
        shopping_map = {item["item_id"]: item["count"] for item in result["shopping_list"]}
        self.assertEqual(shopping_map[194820], 5)
        self.assertEqual(shopping_map[200111], 10)

if __name__ == '__main__':
    unittest.main()
