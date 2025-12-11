import unittest
import json
import os
from app import app
from combat_manager import CombatManager, COMBAT_LOG_FILE

class TestCombatLog(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Backup existing log
        if os.path.exists(COMBAT_LOG_FILE):
            os.rename(COMBAT_LOG_FILE, COMBAT_LOG_FILE + '.bak')
            
        self.manager = CombatManager()
            
    def tearDown(self):
        # Restore backup
        if os.path.exists(COMBAT_LOG_FILE + '.bak'):
            os.rename(COMBAT_LOG_FILE + '.bak', COMBAT_LOG_FILE)
        elif os.path.exists(COMBAT_LOG_FILE):
            os.remove(COMBAT_LOG_FILE)

    def test_logging_and_stats(self):
        # Log 3 battles: Win, Win, Loss
        self.manager.log_battle("WIN", "Enemy A", "Team 1", 10)
        self.manager.log_battle("WIN", "Enemy B", "Team 1", 12)
        self.manager.log_battle("LOSS", "Enemy C", "Team 1", 8)
        
        # Check Stats
        stats = self.manager.get_stats()
        self.assertEqual(stats['total'], 3)
        self.assertEqual(stats['wins'], 2)
        self.assertEqual(stats['losses'], 1)
        self.assertEqual(stats['win_rate'], 66) # int(2/3 * 100)
        self.assertEqual(stats['avg_rounds'], 10.0) # (10+12+8)/3
        
        # Check History (Newest first)
        history = self.manager.get_history()
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]['result'], "LOSS")
        self.assertEqual(history[0]['enemy'], "Enemy C")

    def test_api_endpoints(self):
        # Log via API
        payload = {
            "result": "WIN",
            "enemy": "API Enemy",
            "myTeam": "API Team",
            "rounds": 15
        }
        res = self.app.post('/api/combat/log', json=payload)
        self.assertEqual(res.status_code, 200)
        
        # Verify History API
        res = self.app.get('/api/combat/history')
        data = res.json
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['enemy'], "API Enemy")
        
        # Verify Stats API
        res = self.app.get('/api/combat/stats')
        stats = res.json
        self.assertEqual(stats['total'], 1)
        self.assertEqual(stats['win_rate'], 100)

if __name__ == '__main__':
    unittest.main()
