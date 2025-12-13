
import unittest
import sys
import os
import json
from flask import Flask

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app, sanity_state

class TestApiContract(unittest.TestCase):
    
    def setUp(self):
        self.client = app.test_client()
        # Reset state
        sanity_state.clear()
        
    def test_get_sanity_status_schema(self):
        """Verify GET /api/v1/sanity/status response shape"""
        
        # Seed some state
        sanity_state["TestChar"]["TestAddon"] = {
            "reported": {"status": "OK", "timestamp": "2025-01-01T00:00:00Z"},
            "snapshot": {"inv_count": 10}
        }
        
        resp = self.client.get('/api/v1/sanity/status')
        self.assertEqual(resp.status_code, 200)
        
        data = resp.get_json()
        
        # 1. Root keys
        self.assertIn("overall", data)
        self.assertIn("characters", data)
        self.assertIn(data["overall"], ["OK", "WARN", "FAIL"])
        
        # 2. Character structure
        self.assertIn("TestChar", data["characters"])
        char_entry = data["characters"]["TestChar"]
        self.assertIn("overall", char_entry)
        self.assertIn("addons", char_entry)
        
        # 3. Addon structure
        self.assertIn("TestAddon", char_entry["addons"])
        addon_entry = char_entry["addons"]["TestAddon"]
        
        # 4. Reason Schema
        self.assertIn("status", addon_entry)
        self.assertIn("reasons", addon_entry)
        self.assertIsInstance(addon_entry["reasons"], list)
        
        # Test reason structure if present (sanity check manually added reason)
        # Mock a WARN state
        from datetime import datetime, timezone
        now_iso = datetime.now(timezone.utc).isoformat()
        
        sanity_state["TestChar"]["DeepPockets"] = {
             "reported": {"status": "OK", "timestamp": now_iso},
             "snapshot": {"inv_count": 0},
             "prev_snapshot": {"inv_count": 100}
        }
        
        resp = self.client.get('/api/v1/sanity/status')
        data = resp.get_json()
        dp_reasons = data["characters"]["TestChar"]["addons"]["DeepPockets"]["reasons"]
        
        self.assertTrue(len(dp_reasons) > 0)
        first_reason = dp_reasons[0]
        
        # CRITICAL: Verify contract {code, message}
        self.assertIn("code", first_reason)
        self.assertIn("message", first_reason)
        self.assertIsInstance(first_reason["code"], str)
        self.assertIsInstance(first_reason["message"], str)
        self.assertEqual(first_reason["code"], "DP_INV_ZERO_AFTER_NONZERO")

if __name__ == '__main__':
    unittest.main()
