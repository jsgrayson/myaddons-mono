import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import time
from watchdog.events import FileSystemEvent

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bridge import SavedVariablesHandler

class TestBridge(unittest.TestCase):
    @patch('bridge.requests.post')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="lua content")
    def test_process_lua_file(self, mock_file, mock_post):
        handler = SavedVariablesHandler()
        
        # Mock successful server response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        handler.process_lua_file("/path/to/DataStore.lua", "DataStore.lua")

        # Verify file was read
        mock_file.assert_called_with("/path/to/DataStore.lua", 'r', encoding='utf-8')
        
        # Verify post was called with correct payload
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json']['source'], "DataStore")
        self.assertEqual(kwargs['json']['data'], "lua content")

    @patch('bridge.SavedVariablesHandler.process_lua_file')
    def test_on_modified_matching_file(self, mock_process):
        handler = SavedVariablesHandler()
        event = FileSystemEvent("/path/to/DataStore.lua")
        event.is_directory = False
        
        handler.on_modified(event)
        
        mock_process.assert_called_once_with("/path/to/DataStore.lua", "DataStore.lua")

    @patch('bridge.SavedVariablesHandler.process_lua_file')
    def test_on_modified_ignored_file(self, mock_process):
        handler = SavedVariablesHandler()
        event = FileSystemEvent("/path/to/RandomFile.txt")
        event.is_directory = False
        
        handler.on_modified(event)
        
        mock_process.assert_not_called()

if __name__ == '__main__':
    unittest.main()
