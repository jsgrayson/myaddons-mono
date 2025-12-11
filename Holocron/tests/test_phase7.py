import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock networkx to avoid import error
sys.modules['networkx'] = MagicMock()

from server import app, solve_dependency

class TestPhase7(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('server.get_db_connection')
    def test_solve_dependency_simple(self, mock_get_db):
        # Scenario: Quest C requires B, B requires A.
        # User has A. Missing B. Target is C.
        # Expected: Next step is B.
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock DB responses for solve_dependency(C)
        # 1. Get dependencies for C -> Returns B
        # 2. Get dependencies for B -> Returns A
        # 3. Get title for B -> "Quest B"
        
        # Mock DB state
        self.last_query = ""
        self.last_params = ()

        def execute_side_effect(query, params=None):
            self.last_query = query
            self.last_params = params

        def fetchall_side_effect():
            if "SELECT required_quest_id" in self.last_query:
                if self.last_params[0] == 'C': return [('B',)]
                if self.last_params[0] == 'B': return [('A',)]
                if self.last_params[0] == 'A': return []
            return []

        def fetchone_side_effect():
            if "SELECT title" in self.last_query:
                if self.last_params[0] == 'B': return ('Quest B',)
            return None

        mock_cursor.execute.side_effect = execute_side_effect
        mock_cursor.fetchall.side_effect = fetchall_side_effect
        mock_cursor.fetchone.side_effect = fetchone_side_effect

        # Test
        completed = {'A'}
        result = solve_dependency('C', completed)
        
        self.assertEqual(result, ('B', 'Quest B'))

    @patch('server.get_db_connection')
    def test_codex_route(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock Campaigns
        mock_cursor.fetchall.return_value = [
            (1, "Test Campaign", [101, 102, 103])
        ]
        
        # We need to mock the internal calls of solve_dependency too, or just let it fail gracefully/return None if mocked poorly.
        # For this test, let's assume solve_dependency returns None (no blocker found) or we mock the DB to return no dependencies.
        
        response = self.app.get('/codex')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Campaign', response.data)

if __name__ == '__main__':
    unittest.main()
