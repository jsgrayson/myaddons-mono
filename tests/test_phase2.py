import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app
from indexer import generate_lua_index

class TestPhase2(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('server.get_db_connection')
    def test_search_endpoint(self, mock_get_db):
        # Mock DB response
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock fetchall return value: name, count, container_type, container_index, character_name
        mock_cursor.fetchall.return_value = [
            ("Sulfuron Hammer", 1, "Bag", 1, "MainChar"),
            ("Sulfuron Hammer", 1, "Bank", 2, "AltChar")
        ]

        response = self.app.get('/search?q=Sulfuron')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sulfuron Hammer', response.data)
        self.assertIn(b'MainChar', response.data)
        self.assertIn(b'AltChar', response.data)

    @patch('indexer.get_db_connection')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_indexer_generation(self, mock_file, mock_get_db):
        # Mock DB response
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock fetchall: item_id, name, container_type, count
        mock_cursor.fetchall.return_value = [
            (12345, "Test Item", "Bag", 5),
            (12345, "Test Item", "Bank", 10),
            (67890, "Other Item", "GuildBank", 20)
        ]

        generate_lua_index("test_index.lua")

        # Verify file write
        mock_file.assert_called_with("test_index.lua", "w")
        handle = mock_file()
        
        # Check if content was written (simplified check)
        # We expect calls to write parts of the Lua table
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        
        self.assertIn('HolocronDB = {', written_content)
        self.assertIn('[12345] = {', written_content)
        self.assertIn('name = "Test Item"', written_content)
        self.assertIn('total = 15', written_content) # 5 + 10
        self.assertIn('["Bag"] = 5', written_content)
        self.assertIn('["Bank"] = 10', written_content)
        self.assertIn('[67890] = {', written_content)

if __name__ == '__main__':
    unittest.main()
