import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock
from quartermaster_engine import QuartermasterEngine
from warden_engine import WardenEngine, StockpileItem

class TestQuartermasterEngine(unittest.TestCase):
    def setUp(self):
        self.warden = WardenEngine()
        self.engine = QuartermasterEngine(self.warden)
        
    def test_generate_mail_jobs_with_deficit(self):
        # Setup: Create a deficit in Warden stockpiles
        # Item 123: Need 100, Have 50 -> Deficit 50
        self.warden.stockpiles = {
            123: StockpileItem(123, "Test Item", 50, 100, "icon")
        }
        
        jobs = self.engine.generate_mail_jobs()
        
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['item_id'], 123)
        self.assertEqual(jobs[0]['quantity'], 50)
        self.assertEqual(jobs[0]['source'], "Bank-Alt")
        self.assertEqual(jobs[0]['target'], "Main-Character")
        
    def test_generate_mail_jobs_no_deficit(self):
        # Setup: No deficit
        # Item 123: Need 100, Have 150
        self.warden.stockpiles = {
            123: StockpileItem(123, "Test Item", 150, 100, "icon")
        }
        
        jobs = self.engine.generate_mail_jobs()
        
        self.assertEqual(len(jobs), 0)
        
    def test_get_logistics_report(self):
        self.warden.stockpiles = {
            123: StockpileItem(123, "Test Item", 50, 100, "icon")
        }
        
        report = self.engine.get_logistics_report()
        
        self.assertEqual(report['status'], "Restocking Needed")
        self.assertEqual(report['pending_jobs'], 1)
        self.assertEqual(len(report['jobs']), 1)

if __name__ == '__main__':
    unittest.main()
