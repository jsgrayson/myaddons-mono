import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add parent directory to path to import server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app

class TestHolocronServer(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('server.get_db_connection')
    def test_health_check(self, mock_get_db):
        # Mock successful DB connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'healthy')

    @patch('server.get_db_connection')
    def test_upload_data_success(self, mock_get_db):
        # Mock DB interaction (though currently commented out in server.py)
        mock_conn = MagicMock()
        mock_get_db.return_value = mock_conn

        payload = {
            "source": "DataStore_Containers",
            "data": "some lua content"
        }
        
        response = self.app.post('/upload', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Processed DataStore_Containers data', response.json['message'])

    def test_upload_data_missing_fields(self):
        payload = {"source": "DataStore"} # Missing data
        response = self.app.post('/upload', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
