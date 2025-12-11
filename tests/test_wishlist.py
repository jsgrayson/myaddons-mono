import unittest
import json
import os
from app import app, WISHLIST_FILE

class TestWishlist(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Backup existing wishlist if any
        if os.path.exists(WISHLIST_FILE):
            os.rename(WISHLIST_FILE, WISHLIST_FILE + '.bak')
            
    def tearDown(self):
        # Restore backup
        if os.path.exists(WISHLIST_FILE + '.bak'):
            os.rename(WISHLIST_FILE + '.bak', WISHLIST_FILE)
        elif os.path.exists(WISHLIST_FILE):
            os.remove(WISHLIST_FILE)

    def test_add_and_get_wishlist(self):
        # Add item
        payload = {
            "speciesId": 71163,
            "petName": "Unborn Val'kyr",
            "breedId": 3,
            "breedName": "H/H"
        }
        res = self.app.post('/api/wishlist', json=payload)
        self.assertEqual(res.status_code, 200)
        
        # Get wishlist
        res = self.app.get('/api/wishlist')
        data = res.json
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['petName'], "Unborn Val'kyr")
        self.assertEqual(data[0]['breedName'], "H/H")

    def test_duplicate_prevention(self):
        payload = {
            "speciesId": 71163,
            "petName": "Unborn Val'kyr",
            "breedId": 3,
            "breedName": "H/H"
        }
        self.app.post('/api/wishlist', json=payload)
        
        # Try adding again
        res = self.app.post('/api/wishlist', json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn("already in wishlist", res.json['message'])

    def test_delete_item(self):
        payload = {
            "speciesId": 71163,
            "petName": "Unborn Val'kyr",
            "breedId": 3,
            "breedName": "H/H"
        }
        self.app.post('/api/wishlist', json=payload)
        
        # Delete
        res = self.app.delete('/api/wishlist', json={"speciesId": 71163, "breedId": 3})
        self.assertEqual(res.status_code, 200)
        
        # Verify empty
        res = self.app.get('/api/wishlist')
        self.assertEqual(len(res.json), 0)

    def test_scan_alert(self):
        # Add item to wishlist
        payload = {
            "speciesId": 71163,
            "petName": "Unborn Val'kyr",
            "breedId": 3,
            "breedName": "H/H"
        }
        self.app.post('/api/wishlist', json=payload)
        
        # Scan matching pet
        scan_payload = {"speciesId": 71163, "breedId": 3}
        res = self.app.post('/api/scan_wild_pet', json=scan_payload)
        self.assertTrue(res.json['alert'])
        self.assertIn("WISHLIST ALERT", res.json['message'])
        
        # Scan non-matching pet (wrong breed)
        scan_payload = {"speciesId": 71163, "breedId": 4}
        res = self.app.post('/api/scan_wild_pet', json=scan_payload)
        self.assertFalse(res.json['alert'])
        
        # Scan non-matching pet (wrong species)
        scan_payload = {"speciesId": 99999, "breedId": 3}
        res = self.app.post('/api/scan_wild_pet', json=scan_payload)
        self.assertFalse(res.json['alert'])

if __name__ == '__main__':
    unittest.main()
