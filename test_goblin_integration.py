import unittest
import os
import json
import time
from market_manager import MarketManager
from goblin_integrator import GoblinIntegrator

class TestGoblinIntegration(unittest.TestCase):
    def setUp(self):
        self.test_market_file = 'test_market_data.json'
        self.test_goblin_file = 'price_list.json' # Updated filename
        
        # Cleanup
        if os.path.exists(self.test_market_file): os.remove(self.test_market_file)
        if os.path.exists(self.test_goblin_file): os.remove(self.test_goblin_file)
        
        self.market_manager = MarketManager(self.test_market_file)
        self.integrator = GoblinIntegrator(
            self.market_manager, 
            watch_dir='.', 
            goblin_filename=self.test_goblin_file
        )
        self.integrator.start()

    def test_file_update(self):
        # Mock Collection: User owns Pet A (123) but not Pet B (456) or C (789)
        self.market_manager.set_collection([{'speciesId': 123}])

        # Create dummy Goblin data with AI fields
        data = [
            {
                "speciesId": 123, 
                "price": 5000, 
                "name": "Owned Deal",
                "marketValue": 10000,
                "discount": 50,
                "isDeal": True,
                "level": 25
            },
            {
                "speciesId": 456, 
                "price": 10000, 
                "name": "Missing Deal",
                "marketValue": 20000,
                "discount": 50,
                "isDeal": True,
                "level": 25
            },
            {
                "speciesId": 789, 
                "price": 100, 
                "name": "Lvl 1 Flip",
                "marketValue": 5000,
                "discount": 98,
                "isDeal": True,
                "level": 1
            }
        ]
        
        # Write file
        with open(self.test_goblin_file, 'w') as f:
            json.dump(data, f)
            
        # Wait for watchdog (it's async)
        time.sleep(1)
        
        # 1. Check Standard Deals
        deals = self.market_manager.get_deals()
        self.assertEqual(len(deals), 3)
        
        # 2. Check Missing Deals (Should only be 456 and 789)
        missing = self.market_manager.get_missing_deals()
        self.assertEqual(len(missing), 2)
        self.assertEqual(missing[0]['speciesId'], 789) # Sorted by discount
        self.assertEqual(missing[1]['speciesId'], 456)
        
        # 3. Check Arbitrage Flips (Should only be 789 - Lvl 1)
        flips = self.market_manager.get_arbitrage_flips()
        self.assertEqual(len(flips), 1)
        self.assertEqual(flips[0]['speciesId'], 789)
        self.assertEqual(flips[0]['level'], 1)
        
        print("✅ Goblin Integration Verified: Missing & Arbitrage logic working")

if __name__ == '__main__':
    unittest.main()
