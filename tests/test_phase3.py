import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app

class TestPhase3(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('server.get_db_connection')
    def test_liquidation_route(self, mock_get_db):
        # Mock DB response
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock view_liquidatable_assets
        # name, count, market_value, total_value, container_type, character_name
        mock_cursor.fetchall.side_effect = [
            [
                ("High Value Item", 1, 500000, 500000, "Bank", "MainChar"),
                ("Another Item", 10, 10000, 100000, "Bag", "AltChar")
            ],
            [
                ("Duplicate Pet", 5)
            ]
        ]

        response = self.app.get('/liquidation')
        self.assertEqual(response.status_code, 200)
        
        # Check for assets
        self.assertIn(b'High Value Item', response.data)
        self.assertIn(b'50g', response.data) # Formatted value (500000 / 10000)
        
        # Check for pets
        self.assertIn(b'Duplicate Pet', response.data)
        self.assertIn(b'5', response.data)

if __name__ == '__main__':
    unittest.main()
