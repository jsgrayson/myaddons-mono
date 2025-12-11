import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app

class TestPhase5Extended(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('server.get_db_connection')
    def test_navigator_route_extended(self, mock_get_db):
        # Mock DB response
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock fetchall: instance_name, drop_name, drop_type, expansion, instance_type
        mock_cursor.fetchall.return_value = [
            ("Icecrown Citadel", "Invincible", "Mount", "WotLK", "Raid"),
            ("Scarlet Monastery", "Horseman's Reins", "Mount", "Classic", "Holiday"),
            ("Shadowfang Keep", "X-45 Heartbreaker", "Mount", "Classic", "Holiday")
        ]

        response = self.app.get('/navigator')
        self.assertEqual(response.status_code, 200)
        
        # Check for Raid
        self.assertIn(b'Icecrown Citadel', response.data)
        
        # Check for Holidays
        self.assertIn(b'Scarlet Monastery', response.data)
        self.assertIn(b'Shadowfang Keep', response.data)
        
        # Check for Toggle UI elements
        self.assertIn(b'id="toggleRaid"', response.data)
        self.assertIn(b'id="toggleHoliday"', response.data)
        self.assertIn(b'filterActivities()', response.data)

if __name__ == '__main__':
    unittest.main()
