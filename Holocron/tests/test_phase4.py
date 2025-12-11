import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app

class TestPhase4(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('server.get_db_connection')
    def test_generate_jobs_endpoint(self, mock_get_db):
        # Mock DB response
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock view_liquidatable_assets
        # name, count, character_name
        mock_cursor.fetchall.return_value = [
            ("High Value Item", 1, "MainChar"),
            ("Another Item", 10, "AltChar")
        ]

        response = self.app.post('/api/generate_jobs')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['jobs_created'], 2)

if __name__ == '__main__':
    unittest.main()
