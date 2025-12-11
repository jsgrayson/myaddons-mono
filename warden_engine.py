#!/usr/bin/env python3
"""
The Warden - Account Health & Monitoring
Tracks gold, resources, and generates alerts for the Goblin module.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import datetime

@dataclass
class StockpileItem:
    item_id: int
    name: str
    current_quantity: int
    threshold: int
    icon: str

class WardenEngine:
    """
    Monitors account health, gold, and resource stockpiles.
    """
    
    def __init__(self):
        self.gold_ledger = {} # Character -> Gold amount
        self.stockpiles = {}  # ItemID -> StockpileItem
        self.alerts = []
        
    def load_mock_data(self):
        """Load mock account data"""
        # Mock Gold
        self.gold_ledger = {
            "Main-Character": 154000,
            "Alt-Druid": 23000,
            "Bank-Alt": 500000
        }
        
        # Mock Stockpiles (Crafting Mats)
        self.stockpiles = {
            198765: StockpileItem(198765, "Draconium Ore", 45, 100, "inv_ore_draconium"),
            198766: StockpileItem(198766, "Khaz'gorite Ore", 120, 50, "inv_ore_khazgorite"),
            200111: StockpileItem(200111, "Resonant Crystal", 5, 20, "inv_crystal_resonant")
        }
        
        print(f"✓ Warden loaded: {self.get_total_gold():,}g across {len(self.gold_ledger)} characters")

    def get_total_gold(self) -> int:
        """Return total account gold"""
        return sum(self.gold_ledger.values())

    def get_account_summary(self) -> Dict:
        """Return high-level account summary"""
        total_gold = self.get_total_gold()
        return {
            "total_gold": total_gold,
            "gold_formatted": f"{total_gold:,}g",
            "breakdown": self.gold_ledger,
            "wealth_status": self._get_wealth_status(total_gold)
        }
        
    def _get_wealth_status(self, gold: int) -> str:
        if gold > 1000000: return "Goblin Lord"
        if gold > 500000: return "Wealthy"
        if gold > 100000: return "Comfortable"
        return "Peon"

    def check_stockpiles(self) -> List[Dict]:
        """Check all stockpiles against thresholds"""
        status_list = []
        for item in self.stockpiles.values():
            is_low = item.current_quantity < item.threshold
            status_list.append({
                "name": item.name,
                "current": item.current_quantity,
                "threshold": item.threshold,
                "is_low": is_low,
                "deficit": item.threshold - item.current_quantity if is_low else 0
            })
        return status_list

    def get_alerts(self) -> List[Dict]:
        """Generate alerts for low resources"""
        alerts = []
        
        # Check Gold
        if self.get_total_gold() < 50000:
            alerts.append({
                "type": "Gold",
                "severity": "High",
                "message": "Total gold reserves are low (<50k)"
            })
            
        # Check Stockpiles
        for item in self.stockpiles.values():
            if item.current_quantity < item.threshold:
                alerts.append({
                    "type": "Stockpile",
                    "severity": "Medium",
                    "message": f"Low stock: {item.name} ({item.current_quantity}/{item.threshold})"
                })
                
        return alerts
