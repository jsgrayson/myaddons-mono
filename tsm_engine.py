#!/usr/bin/env python3
"""
TSM Brain - Pricing Intelligence
Parses TradeSkillMaster data to provide accurate market values.
"""

from typing import Dict, Optional
import os
from utils.lua_parser import LuaParser

class TSMEngine:
    """
    Parses TSM SavedVariables to extract pricing data.
    """
    
    def __init__(self):
        self.prices = {} # ItemID -> Market Value (int)
        self.parser = LuaParser()
        
    def load_data(self):
        """
        Load TSM data from SavedVariables.
        For now, we will load mock data since we don't have the actual TSM file structure yet.
        In a real scenario, this would parse 'TradeSkillMaster.lua'.
        """
        print("Loading TSM pricing data...")
        
        # Mock TSM Data (ItemID -> Price in copper)
        # 1g = 10000 copper
        self.prices = {
            198765: 450000,  # Draconium Ore: 45g
            198766: 1200000, # Khaz'gorite Ore: 120g
            200111: 2000000, # Resonant Crystal: 200g
            194820: 150000,  # Hochenblume: 15g
            191304: 5000000, # Elemental Potion of Ultimate Power: 500g
        }
        
        print(f"✓ TSM Brain loaded: {len(self.prices)} item prices")

    def get_price(self, item_id: int, source: str = "dbmarket") -> int:
        """
        Get price for an item.
        source: 'dbmarket', 'dbregionmarketavg', etc. (Ignored in mock)
        Returns price in gold (float) for simplicity in this MVP.
        """
        price_copper = self.prices.get(item_id, 0)
        return price_copper / 10000.0

    def get_market_value(self, item_id: int) -> float:
        """Helper for standard market value"""
        return self.get_price(item_id, "dbmarket")
