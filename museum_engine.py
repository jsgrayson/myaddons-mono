#!/usr/bin/env python3
"""
The Museum - Shadow Collection Tracker
Tracks appearances, mounts, and pets that are collected but not learned.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ShadowItem:
    item_id: int
    name: str
    type: str # "Mount", "Pet", "Cosmetic"
    character: str
    location: str # "Bag", "Bank"

class MuseumEngine:
    """
    Engine for tracking the Shadow Collection.
    """
    
    def __init__(self, warden_engine):
        self.warden = warden_engine
        
        # Known Collectibles DB (Mock)
        # In a real app, this would be a massive DB of all collectables
        self.collectibles_db = {
            190000: {"name": "Reins of the Quantum Steed", "type": "Mount"},
            190001: {"name": "Caged Woof", "type": "Pet"},
            190002: {"name": "Ensemble: Vestments of the Eternal Traveler", "type": "Cosmetic"},
            200000: {"name": "Ashes of Al'ar", "type": "Mount"}, # Classic example
        }

    def scan_containers(self) -> List[Dict]:
        """
        Scan all character containers for unlearned collectibles.
        """
        shadow_items = []
        
        # Mock Container Data (since we don't have full DataStore_Containers parsing yet)
        # In reality, we would iterate self.warden.get_all_containers()
        mock_containers = {
            "Main-Character": {
                "Bag": [190000, 12345, 67890], # Contains Quantum Steed
                "Bank": [200000] # Contains Ashes of Al'ar
            },
            "Bank-Alt": {
                "Bag": [190001], # Contains Caged Woof
                "Bank": []
            }
        }
        
        for char_name, containers in mock_containers.items():
            for location, items in containers.items():
                for item_id in items:
                    if item_id in self.collectibles_db:
                        info = self.collectibles_db[item_id]
                        shadow_items.append({
                            "item_id": item_id,
                            "name": info['name'],
                            "type": info['type'],
                            "character": char_name,
                            "location": location
                        })
                        
        return shadow_items

    def get_shadow_collection(self) -> Dict:
        """
        Return the full shadow collection report.
        """
        items = self.scan_containers()
        return {
            "total_items": len(items),
            "items": items,
            "status": "Found Unlearned Items" if items else "Clean"
        }
