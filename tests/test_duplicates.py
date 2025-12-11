import unittest
import json
import os
from app import app

class TestDuplicates(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Backup existing pets
        if os.path.exists('my_pets.json'):
            os.rename('my_pets.json', 'my_pets.json.bak')
            
    def tearDown(self):
        # Restore backup
        if os.path.exists('my_pets.json.bak'):
            os.rename('my_pets.json.bak', 'my_pets.json')
        elif os.path.exists('my_pets.json'):
            os.remove('my_pets.json')

    def test_duplicate_detection(self):
        # Create mock data with duplicates
        mock_data = {
            "pets": [
                {"speciesId": 100, "name": "Pet A", "level": 25, "quality": 3}, # Keeper
                {"speciesId": 100, "name": "Pet A", "level": 1, "quality": 1},  # Duplicate
                {"speciesId": 200, "name": "Pet B", "level": 25, "quality": 3}, # Unique
                {"speciesId": 300, "name": "Pet C", "level": 10, "quality": 2}, # Duplicate 1
                {"speciesId": 300, "name": "Pet C", "level": 25, "quality": 3}, # Keeper
                {"speciesId": 300, "name": "Pet C", "level": 1, "quality": 1}   # Duplicate 2
            ]
        }
        
        with open('my_pets.json', 'w') as f:
            json.dump(mock_data, f)
            
        # Call API
        res = self.app.get('/api/collection/duplicates')
        data = res.json
        
        self.assertEqual(len(data), 2) # Species 100 and 300
        
        # Check Species 300 (should be first due to count=3)
        group_c = data[0]
        self.assertEqual(group_c['speciesId'], 300)
        self.assertEqual(group_c['count'], 3)
        self.assertEqual(group_c['pets'][0]['level'], 25) # Best pet first
        
        # Check Species 100
        group_a = data[1]
        self.assertEqual(group_a['speciesId'], 100)
        self.assertEqual(group_a['count'], 2)
        self.assertEqual(group_a['pets'][0]['level'], 25)

    def test_no_duplicates(self):
        mock_data = {
            "pets": [
                {"speciesId": 100, "name": "Pet A", "level": 25},
                {"speciesId": 200, "name": "Pet B", "level": 25}
            ]
        }
        with open('my_pets.json', 'w') as f:
            json.dump(mock_data, f)
            
        res = self.app.get('/api/collection/duplicates')
        self.assertEqual(len(res.json), 0)

if __name__ == '__main__':
    unittest.main()
