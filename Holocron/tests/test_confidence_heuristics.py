
import unittest
import sys
import os
from datetime import datetime, timezone, timedelta

# Add parent dir to path to import server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import apply_heuristics

class TestConfidenceHeuristics(unittest.TestCase):
    
    def test_ok_baseline(self):
        """Case A: Normal fluctuations -> OK"""
        curr = {"inv_count": 118}
        prev = {"inv_count": 120}
        now = datetime.now(timezone.utc)
        ts = now.isoformat()
        
        status, reasons = apply_heuristics("DeepPockets", curr, prev, ts)
        self.assertEqual(status, "OK")
        self.assertEqual(reasons, [])

    def test_massive_drop(self):
        """Case B: >80% drop -> WARN"""
        curr = {"inv_count": 30}
        prev = {"inv_count": 200}
        now = datetime.now(timezone.utc)
        ts = now.isoformat()
        
        status, reasons = apply_heuristics("DeepPockets", curr, prev, ts)
        self.assertEqual(status, "WARN")
        self.assertTrue(any(r["code"] == "DP_INV_DROP_80" for r in reasons))

    def test_drop_to_zero_after_nonzero(self):
        """Case C: Drop to 0 after nonzero -> WARN"""
        curr = {"inv_count": 0}
        prev = {"inv_count": 120}
        now = datetime.now(timezone.utc)
        ts = now.isoformat()
        
        status, reasons = apply_heuristics("DeepPockets", curr, prev, ts)
        self.assertEqual(status, "WARN")
        self.assertTrue(any(r["code"] == "DP_INV_ZERO_AFTER_NONZERO" for r in reasons))

    def test_staleness(self):
        """Case D: Staleness > 24h -> WARN"""
        curr = {"inv_count": 100}
        prev = {"inv_count": 100}
        # 25 hours ago
        past = datetime.now(timezone.utc) - timedelta(hours=25)
        ts = past.isoformat()
        
        status, reasons = apply_heuristics("DeepPockets", curr, prev, ts)
        self.assertEqual(status, "WARN")
        self.assertTrue(any(r["code"] == "SANITY_STALE_24H" for r in reasons))

    def test_petweaver_mismatch(self):
        """Case E: Pets present but no strats -> WARN"""
        curr = {"owned_pet_count": 50, "strategy_count": 0}
        prev = {}
        now = datetime.now(timezone.utc)
        ts = now.isoformat()
        
        status, reasons = apply_heuristics("PetWeaver", curr, prev, ts)
        self.assertEqual(status, "WARN")
        self.assertTrue(any(r["code"] == "PW_PETS_NO_STRATS" for r in reasons))

    def test_skillweaver_mismatch(self):
        """Case E2: Spec active but no modules -> WARN"""
        curr = {"active_spec_present": True, "module_count": 0}
        prev = {}
        now = datetime.now(timezone.utc)
        ts = now.isoformat()
        
        status, reasons = apply_heuristics("SkillWeaver", curr, prev, ts)
        self.assertEqual(status, "WARN")
        self.assertTrue(any(r["code"] == "SW_SPEC_NO_MODULES" for r in reasons))

if __name__ == '__main__':
    unittest.main()
