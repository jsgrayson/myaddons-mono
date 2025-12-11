import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock
from museum_engine import MuseumEngine
from warden_engine import WardenEngine

class TestMuseumEngine(unittest.TestCase):
    def setUp(self):
        self.warden = WardenEngine()
        self.engine = MuseumEngine(self.warden)
        
    def test_scan_containers_finds_items(self):
        # Setup: Mock DB has items, scan_containers uses internal mock data
        # In a real test we'd mock the container data source, but here it's hardcoded in the engine for now
        
        items = self.engine.scan_containers()
        
        # We expect to find Quantum Steed (190000), Ashes (200000), Caged Woof (190001)
        self.assertTrue(len(items) >= 3)
        
        # Verify specific item details
        steed = next((i for i in items if i['item_id'] == 190000), None)
        self.assertIsNotNone(steed)
        self.assertEqual(steed['name'], "Reins of the Quantum Steed")
        self.assertEqual(steed['character'], "Main-Character")
        self.assertEqual(steed['location'], "Bag")
        
    def test_get_shadow_collection(self):
        report = self.engine.get_shadow_collection()
        
        self.assertEqual(report['status'], "Found Unlearned Items")
        self.assertTrue(report['total_items'] >= 3)

if __name__ == '__main__':
    unittest.main()
