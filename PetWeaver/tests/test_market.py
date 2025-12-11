import unittest
import json
import os
from app import app
from market_manager import MarketManager, MARKET_FILE

class TestMarketWatcher(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Backup existing market data
        if os.path.exists(MARKET_FILE):
            os.rename(MARKET_FILE, MARKET_FILE + '.bak')
            
        self.manager = MarketManager()
            
    def tearDown(self):
        # Restore backup
        if os.path.exists(MARKET_FILE + '.bak'):
            os.rename(MARKET_FILE + '.bak', MARKET_FILE)
        elif os.path.exists(MARKET_FILE):
            os.remove(MARKET_FILE)

    def test_price_update_and_average(self):
        # Update price 3 times: 100, 200, 300
        self.manager.update_price(123, 100, "Test Pet")
        self.manager.update_price(123, 200, "Test Pet")
        self.manager.update_price(123, 300, "Test Pet")
        
        # Check average (should be 200)
        avg = self.manager.get_market_value(123)
        self.assertEqual(avg, 200.0)
        
        # Check current price
        data = self.manager.get_all_data()
        self.assertEqual(data['123']['current_price'], 300)

    def test_deal_detection(self):
        # Establish market value of 1000
        for _ in range(5):
            self.manager.update_price(999, 1000, "Valuable Pet")
            
        # Post a low price (400 = 60% off)
        self.manager.update_price(999, 400, "Valuable Pet")
        
        # Check deals with 50% threshold
        deals = self.manager.get_deals(0.5)
        self.assertEqual(len(deals), 1)
        self.assertEqual(deals[0]['speciesId'], 999)
        self.assertEqual(deals[0]['discount'], 55) # (1 - 400/900)*100 = 55.5%
        
        # Post a high price (1200)
        self.manager.update_price(999, 1200, "Valuable Pet")
        deals = self.manager.get_deals(0.5)
        self.assertEqual(len(deals), 0)

    def test_api_endpoints(self):
        # Update via API
        payload = {"speciesId": 777, "petName": "API Pet", "price": 5000}
        res = self.app.post('/api/market/update', json=payload)
        self.assertEqual(res.status_code, 200)
        
        # Verify data
        res = self.app.get('/api/market/data')
        data = res.json
        self.assertIn('777', data)
        self.assertEqual(data['777']['current_price'], 5000)
        
        # Test Deals API (should be empty initially)
        res = self.app.get('/api/market/deals')
        self.assertEqual(len(res.json), 0)

if __name__ == '__main__':
    unittest.main()
