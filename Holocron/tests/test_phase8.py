import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock networkx
sys.modules['networkx'] = MagicMock()

from server import app

class TestPhase8(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('server.get_db_connection')
    def test_diplomat_route(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock Factions
        # faction_id, name, paragon_threshold
        mock_cursor.fetchall.return_value = [
            (2600, 'Council of Dornogal', 10000),
            (2601, 'The Assembly of the Deeps', 10000)
        ]

        response = self.app.get('/diplomat')
        self.assertEqual(response.status_code, 200)
        
        # Check for Faction Name
        self.assertIn(b'Council of Dornogal', response.data)
        
        # Check for Sniper Recommendation (Mocked in server.py to appear if percent > 80)
        # In server.py, Dornogal (2600) is hardcoded to 8500 (85%), so it should trigger the sniper.
        self.assertIn(b'Reputation Sniper', response.data)
        self.assertIn(b'Protect the Core', response.data)

if __name__ == '__main__':
    unittest.main()
