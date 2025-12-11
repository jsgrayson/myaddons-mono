import unittest
import os
import json
from wishlist_manager import WishlistManager

class TestWishlistManager(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_wishlist.json'
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.manager = WishlistManager(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_and_get(self):
        success, msg = self.manager.add_item(123, "Test Pet", 4, "P/P")
        self.assertTrue(success)
        
        wishlist = self.manager.get_wishlist()
        self.assertEqual(len(wishlist), 1)
        self.assertEqual(wishlist[0]['speciesId'], 123)
        self.assertEqual(wishlist[0]['breedId'], 4)

    def test_duplicate(self):
        self.manager.add_item(123, "Test Pet", 4, "P/P")
        success, msg = self.manager.add_item(123, "Test Pet", 4, "P/P")
        self.assertFalse(success)
        self.assertEqual(msg, "Item already in wishlist")

    def test_check_match(self):
        self.manager.add_item(123, "Test Pet", 4, "P/P")
        
        match, item = self.manager.check_match(123, 4)
        self.assertTrue(match)
        self.assertEqual(item['petName'], "Test Pet")
        
        match, item = self.manager.check_match(123, 5) # Wrong breed
        self.assertFalse(match)
        
        match, item = self.manager.check_match(999, 4) # Wrong species
        self.assertFalse(match)

    def test_remove(self):
        self.manager.add_item(123, "Test Pet", 4, "P/P")
        success = self.manager.remove_item(123, 4)
        self.assertTrue(success)
        self.assertEqual(len(self.manager.get_wishlist()), 0)
        
        success = self.manager.remove_item(999, 9) # Non-existent
        self.assertFalse(success)

if __name__ == '__main__':
    unittest.main()
