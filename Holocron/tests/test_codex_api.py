import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock networkx to avoid import issues
sys.modules['networkx'] = MagicMock()

from server import app


class TestCodexAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_blocker_requires_quest(self):
        response = self.app.get('/api/codex/blocker')
        self.assertEqual(response.status_code, 400)

    @patch('server.solve_dependency')
    @patch('server.get_db_connection')
    def test_blocker_with_numeric_quest(self, mock_get_db, mock_solver):
        mock_solver.return_value = (200, 'Unlock Mechagon')
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        response = self.app.get('/api/codex/blocker?quest=200&completed=1,2')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['blocking_quest_id'], 200)
        self.assertEqual(data['state'], 'ready')
        self.assertIn('Unlock Mechagon', data['message'])

    @patch('server.get_db_connection')
    def test_blocker_completed_short_circuit(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        response = self.app.get('/api/codex/blocker?quest=200&completed=200')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['state'], 'complete')
        self.assertIn('already completed', data['message'])


if __name__ == '__main__':
    unittest.main()
