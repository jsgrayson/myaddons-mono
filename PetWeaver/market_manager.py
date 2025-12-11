import json
import os
from datetime import datetime
from typing import List, Dict, Optional

MARKET_FILE = 'market_data.json'

class MarketManager:
    def __init__(self, data_file: str = MARKET_FILE):
        self.data_file = data_file
        self.market_data = self._load_data()
        
    def _load_data(self) -> Dict:
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
        
    def _save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.market_data, f, indent=2)
            
    def update_price(self, species_id: int, price: int, pet_name: str = "Unknown", 
                    market_value: float = 0.0, discount: float = 0.0, is_deal: bool = False, level: int = 0):
        """
        Update price history and AI data for a pet.
        """
        sid = str(species_id)
        if sid not in self.market_data:
            self.market_data[sid] = {
                "name": pet_name,
                "history": [],
                "current_price": 0,
                "market_value": 0,
                "discount": 0,
                "is_deal": False,
                "level": 0,
                "last_updated": None
            }
            
        # Update metadata
        self.market_data[sid]["name"] = pet_name
        self.market_data[sid]["current_price"] = price
        self.market_data[sid]["market_value"] = market_value
        self.market_data[sid]["discount"] = discount
        self.market_data[sid]["is_deal"] = is_deal
        self.market_data[sid]["level"] = level
        self.market_data[sid]["last_updated"] = datetime.now().isoformat()
        
        # Add to history (keep last 10 entries)
        history_entry = {
            "price": price,
            "timestamp": datetime.now().isoformat()
        }
        self.market_data[sid]["history"].append(history_entry)
        if len(self.market_data[sid]["history"]) > 10:
            self.market_data[sid]["history"] = self.market_data[sid]["history"][-10:]
            
        self._save_data()
        
    def get_market_value(self, species_id: int) -> float:
        """Calculate market value based on history average"""
        sid = str(species_id)
        if sid not in self.market_data:
            return 0.0
            
        history = self.market_data[sid]["history"]
        if not history:
            return 0.0
            
        total = sum(entry["price"] for entry in history)
        return total / len(history)
        
    def set_collection(self, collection_data: List[Dict]):
        """Set the user's collection for cross-referencing"""
        self.collection_species = set()
        for pet in collection_data:
            # Handle both raw Blizzard API format and internal format
            sid = pet.get('species', {}).get('id') or pet.get('speciesId')
            if sid:
                self.collection_species.add(int(sid))

    def get_deals(self) -> List[Dict]:
        """Return pets flagged as deals by Goblin AI."""
        deals = []
        for sid, data in self.market_data.items():
            if data.get("is_deal", False):
                deals.append(self._format_deal(sid, data))
        deals.sort(key=lambda x: x["discount"], reverse=True)
        return deals

    def get_missing_deals(self) -> List[Dict]:
        """Return deals for pets not in the user's collection"""
        if not hasattr(self, 'collection_species'):
            return []
            
        deals = []
        for sid, data in self.market_data.items():
            if data.get("is_deal", False) and int(sid) not in self.collection_species:
                deals.append(self._format_deal(sid, data))
        deals.sort(key=lambda x: x["discount"], reverse=True)
        return deals

    def get_arbitrage_flips(self) -> List[Dict]:
        """
        Identify Level 1 pets that are cheap relative to Level 25 market value.
        Logic: Lvl 1 Price < (Lvl 25 Market Value * 0.4)
        """
        flips = []
        for sid, data in self.market_data.items():
            # Only look at Level 1s
            if data.get("level", 0) != 1:
                continue
                
            price = data["current_price"]
            mv = data.get("market_value", 0)
            
            # Simple heuristic: If Lvl 1 price is < 40% of MV (assuming MV is usually for 25s)
            # This relies on Goblin providing a generic MV or specific MV.
            # If Goblin provides MV specific to the item, this might not work as intended 
            # unless we compare to a separate "Level 25 MV".
            # For now, we'll trust Goblin's "is_deal" flag combined with Level 1 check
            # OR we can just look for deep discounts on Level 1s.
            
            if data.get("is_deal", False) and data.get("discount", 0) > 60:
                 flips.append(self._format_deal(sid, data))
                 
        flips.sort(key=lambda x: x["discount"], reverse=True)
        return flips

    def _format_deal(self, sid, data):
        return {
            "speciesId": int(sid),
            "name": data["name"],
            "price": data["current_price"],
            "marketValue": data.get("market_value", 0),
            "discount": data.get("discount", 0),
            "level": data.get("level", 0),
            "lastUpdated": data["last_updated"]
        }

    def get_all_data(self) -> Dict:
        return self.market_data
