#!/usr/bin/env python3
"""
The Quartermaster - Predictive Restocking System
Manages consumable stock levels and generates mail jobs for Bank Alts.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class MailJob:
    source: str
    target: str
    item_id: int
    item_name: str
    quantity: int
    priority: str  # "High", "Normal"

class QuartermasterEngine:
    """
    Engine for managing logistics and supply chains.
    """
    
    def __init__(self, warden_engine):
        self.warden = warden_engine
        self.bank_alt_name = "Bank-Alt" # Default Bank Alt
        
        # Define "Par" levels for key consumables (TWW Season 3)
        # These override Warden thresholds if present, or serve as a separate config
        self.par_levels = {
            "Main-Character": {
                191341: {"name": "Phial of Tepid Versatility", "par": 20},
                191383: {"name": "Elemental Potion of Ultimate Power", "par": 40},
                197735: {"name": "Refreshing Healing Potion", "par": 20},
                197784: {"name": "Grand Banquet of the Kalu'ak", "par": 20} 
            }
        }

    def generate_mail_jobs(self) -> List[Dict]:
        """
        Analyze inventory and generate mail jobs to restock characters.
        """
        jobs = []
        
        # 1. Check Stockpiles from Warden (General Resources)
        # Warden tracks "StockpileItems" which already have thresholds
        for item_id, item in self.warden.stockpiles.items():
            if item.current_quantity < item.threshold:
                deficit = item.threshold - item.current_quantity
                jobs.append({
                    "source": self.bank_alt_name,
                    "target": "Main-Character", # Assuming Main needs the mats
                    "item_id": item_id,
                    "item_name": item.name,
                    "quantity": deficit,
                    "priority": "Normal"
                })
                
        # 2. Check Character Specific Par Levels (Consumables)
        # In a real scenario, we'd need character-specific inventory data.
        # For now, we'll assume the 'stockpiles' in Warden might represent the Main's inventory
        # or we use mock data if Warden doesn't have it.
        
        # Since Warden.stockpiles is currently our only source of "Inventory" truth in this mock setup,
        # we will rely on it. If we had a full DataStore dump per character, we'd iterate that here.
        
        return jobs

    def get_logistics_report(self) -> Dict:
        """
        Return a summary of logistics status.
        """
        jobs = self.generate_mail_jobs()
        return {
            "status": "Healthy" if not jobs else "Restocking Needed",
            "pending_jobs": len(jobs),
            "jobs": jobs
        }
