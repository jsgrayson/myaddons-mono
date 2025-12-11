import sys
import os
import json
import unittest
from unittest.mock import MagicMock, patch

# Mock networkx before importing server
sys.modules['networkx'] = MagicMock()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app

class TestPhase6(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('server.get_db_connection')
    @patch('server.nx') # Patch the nx object inside server module
    def test_calculate_distance(self, mock_nx, mock_get_db):
        # Setup mock graph
        mock_graph = MagicMock()
        mock_nx.DiGraph.return_value = mock_graph
        
        # Mock shortest path return values
        mock_nx.shortest_path.return_value = [84, 1670, 125]
        mock_nx.shortest_path_length.return_value = 30
        
        # Mock node attributes (for name lookup)
        mock_graph.nodes = {
            84: {'name': 'Stormwind'},
            1670: {'name': 'Oribos'},
            125: {'name': 'Dalaran'}
        }

        # Mock DB response
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock Zones (Nodes)
        # zone_id, name
        mock_cursor.fetchall.side_effect = [
            [
                (84, 'Stormwind'),
                (1670, 'Oribos'),
                (125, 'Dalaran')
            ],
            # Mock Connections (Edges)
            # source, dest, time
            [
                (84, 1670, 10), # SW -> Oribos
                (1670, 125, 20) # Oribos -> Dalaran (hypothetical path)
            ]
        ]

        # Test SW (84) -> Dalaran (125) via Oribos (1670)
        # Expected cost: 10 + 20 = 30
        response = self.app.get('/api/distance?from=84&to=125')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['travel_time_seconds'], 30)
        self.assertEqual(data['path'], ['Stormwind', 'Oribos', 'Dalaran'])

if __name__ == '__main__':
    unittest.main()
