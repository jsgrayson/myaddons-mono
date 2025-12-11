#!/usr/bin/env python3
"""
Pet Image Helper - Maps pet species IDs to Wowhead icon names
"""

import json

class PetImageHelper:
    """
    Provides pet icon URLs using Wowhead's image CDN
    """
    
    def __init__(self, species_path: str = "species_data.json"):
        self.species_data = {}
        self.icon_cache = {}
        
        try:
            with open(species_path, 'r') as f:
                self.species_data = json.load(f)
            print(f"✓ PetImageHelper loaded {len(self.species_data)} species")
        except FileNotFoundError:
            print(f"⚠️  Warning: {species_path} not found")
    
    def get_icon_url(self, pet_name_or_id: str, size: str = "large") -> str:
        """
        Get Wowhead icon URL for a pet.
        
        Args:
            pet_name_or_id: Pet name or species ID
            size: "small", "medium", or "large"
            
        Returns:
            URL to pet icon image
        """
        # Map size to Wowhead path
        size_map = {
            "small": "small",
            "medium": "medium", 
            "large": "large"
        }
        
        # Default icon if not found
        default_icon = f"https://wow.zamimg.com/images/wow/icons/{size_map.get(size, 'large')}/inv_pet_achievement_captureawildpet.jpg"
        
        # For now, return default icon
        # TODO: Build actual species_id -> icon_name mapping
        return default_icon
    
    def get_pet_portrait(self, pet_name: str, size: int = 60) -> str:
        """
        Generate HTML for pet portrait with icon
        
        Args:
            pet_name: Name of the pet
            size: Size in pixels
            
        Returns:
            HTML img tag
        """
        icon_url = self.get_icon_url(pet_name)
        return f'<img src="{icon_url}" alt="{pet_name}" width="{size}" height="{size}" style="border-radius: 8px; border: 2px solid rgba(0,212,255,0.3);">'

if __name__ == "__main__":
    helper = PetImageHelper()
    print("\nTesting icon URLs:")
    print(f"Ikky: {helper.get_icon_url('Ikky')}")
    print(f"HTML: {helper.get_pet_portrait('Ikky', 48)}")
