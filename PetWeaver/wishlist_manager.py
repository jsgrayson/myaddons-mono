import json
import os
from datetime import datetime

class WishlistManager:
    def __init__(self, filepath='wishlist.json'):
        self.filepath = filepath
        self.wishlist = self._load_wishlist()

    def _load_wishlist(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _save_wishlist(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.wishlist, f, indent=2)

    def get_wishlist(self):
        return self.wishlist

    def add_item(self, species_id, pet_name, breed_id, breed_name):
        # Check for duplicates
        for item in self.wishlist:
            if str(item['speciesId']) == str(species_id) and str(item['breedId']) == str(breed_id):
                return False, "Item already in wishlist"

        new_item = {
            "speciesId": int(species_id),
            "petName": pet_name,
            "breedId": int(breed_id),
            "breedName": breed_name,
            "addedAt": datetime.now().isoformat()
        }
        self.wishlist.append(new_item)
        self._save_wishlist()
        return True, "Item added"

    def remove_item(self, species_id, breed_id):
        initial_len = len(self.wishlist)
        self.wishlist = [
            item for item in self.wishlist 
            if not (str(item['speciesId']) == str(species_id) and str(item['breedId']) == str(breed_id))
        ]
        if len(self.wishlist) < initial_len:
            self._save_wishlist()
            return True
        return False

    def check_match(self, species_id, breed_id):
        """Check if a found pet matches any wishlist item"""
        for item in self.wishlist:
            if str(item['speciesId']) == str(species_id) and str(item['breedId']) == str(breed_id):
                return True, item
        return False, None
