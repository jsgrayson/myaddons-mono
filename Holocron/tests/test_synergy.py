import unittest
from unittest.mock import MagicMock
from synergy_engine import SynergyEngine

class TestSynergy(unittest.TestCase):
    def setUp(self):
        self.mock_goblin = MagicMock()
        self.mock_deeppockets = MagicMock()
        self.engine = SynergyEngine(self.mock_goblin, self.mock_deeppockets)

    def test_economy_of_scale(self):
        # Item 198765 (Draconium Ore)
        # Mock Goblin Price
        mock_price = MagicMock()
        mock_price.market_value = 50
        self.mock_goblin.prices.get.return_value = mock_price
        
        # Mock DeepPockets Inventory (Has stock)
        self.mock_deeppockets.search_inventory.return_value = [
            {"character": "BankAlt", "container": "Bank", "count": 100}
        ]
        
        result = self.engine.economy_of_scale(198765)
        
        self.assertEqual(result["action"], "USE_STOCK")
        self.assertEqual(result["stock_count"], 100)
        self.assertEqual(result["potential_savings"], 5000) # 100 * 50

    def test_economy_of_scale_no_stock(self):
        # Mock DeepPockets Inventory (Empty)
        self.mock_deeppockets.search_inventory.return_value = []
        
        result = self.engine.economy_of_scale(12345)
        
        self.assertEqual(result["action"], "BUY")
        self.assertEqual(result["stock_count"], 0)

    def test_zookeeper(self):
        # Mock DeepPockets search for Cinder Kitten (89587)
        # Found on Main and Alt1
        self.mock_deeppockets.search_inventory.return_value = [
            {"character": "Main", "container": "Bag1", "count": 1},
            {"character": "Alt1", "container": "Bag1", "count": 1}
        ]
        
        result = self.engine.the_zookeeper()
        
        # Should recommend mailing Alt1's kitten to Banker
        # Main's kitten is not mailed because we only mail if total > 1?
        # My logic was: "If total > 1, mail all from non-Banker to Banker"
        
        self.assertEqual(result["total_duplicates_found"], 2)
        self.assertEqual(len(result["tasks"]), 2) # Both Main and Alt1 are not "Banker"
        
        # Verify tasks
        chars = [t["from"] for t in result["tasks"]]
        self.assertIn("Main", chars)
        self.assertIn("Alt1", chars)

if __name__ == '__main__':
    unittest.main()
