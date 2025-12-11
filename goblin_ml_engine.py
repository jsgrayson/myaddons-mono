"""
goblin_ml_engine.py - Machine Learning Engine for GoblinAI

Implements intelligent auto-group generation based on market analysis.

Features:
1. Cluster items by profitability patterns
2. Identify high-volume vs high-margin opportunities
3. Detect seasonal/weekend price spikes
4. Auto-create optimized trading groups
5. Recommend operations per group

Usage:
    from goblin_ml_engine import GoblinMLEngine
    
    ml = GoblinMLEngine()
    groups = ml.generate_auto_groups(scan_data)
"""

import json
import numpy as np
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from datetime import datetime, timedelta

# ============================================================================
# Auto-Group Generation Engine
# ============================================================================

class GoblinMLEngine:
    def __init__(self):
        self.min_profit_threshold = 1000  # 10 silver minimum
        self.high_volume_threshold = 100  # Sales per day
        self.high_margin_threshold = 0.5  # 50% profit margin
        
    def generate_auto_groups(self, market_data: List[Dict]) -> List[Dict]:
        """
        Generate optimized trading groups from market data
        
        Args:
            market_data: List of item opportunities from goblin_engine
        
        Returns:
            List of auto-generated groups with items and operations
        """
        groups = []
        
        # Classify items
        instant_flips = []
        volume_trades = []
        craft_profits = []
        transmog_slow = []
        material_stockpile = []
        
        for item in market_data:
            profit = item.get('profit', 0)
            margin = item.get('profit_margin', 0)
            sale_rate = item.get('sale_rate', 0)
            volume = item.get('num_auctions', 0)
            
            # Skip unprofitable items
            if profit < self.min_profit_threshold:
                continue
            
            # Classify
            if margin > 0.5 and sale_rate > 0.8:
                instant_flips.append(item)
            elif volume > self.high_volume_threshold and margin > 0.1:
                volume_trades.append(item)
            elif item.get('is_craftable', False) and profit > 5000:
                craft_profits.append(item)
            elif margin > 0.8 and sale_rate < 0.3:
                transmog_slow.append(item)
            elif self._is_material(item):
                material_stockpile.append(item)
        
        # Create groups
        if instant_flips:
            groups.append({
                "name": "Instant Profit Flips",
                "items": [item['item_id'] for item in instant_flips[:20]],
                "operation": "aggressive_undercut",
                "reason": "High margin (>50%), fast sales (>80%)",
                "priority": 1,
                "post_frequency": "immediately",
            })
        
        if volume_trades:
            groups.append({
                "name": "Volume Trading",
                "items": [item['item_id'] for item in volume_trades[:30]],
                "operation": "volume_pricing",
                "reason": "High turnover, consistent demand",
                "priority": 2,
                "post_frequency": "hourly",
            })
        
        if craft_profits:
            groups.append({
                "name": "Profitable Crafts",
                "items": [item['item_id'] for item in craft_profits[:15]],
                "operation": "craft_and_sell",
                "reason": "Crafting profit >50g per item",
                "priority": 3,
                "post_frequency": "daily",
            })
        
        if transmog_slow:
            groups.append({
                "name": "Transmog Slow Burn",
                "items": [item['item_id'] for item in transmog_slow[:25]],
                "operation": "patient_sale",
                "reason": "High margin, low volume - be patient",
                "priority": 4,
                "post_frequency": "weekly",
            })
        
        if material_stockpile:
            groups.append({
                "name": "Material Stockpile",
                "items": [item['item_id'] for item in material_stockpile[:20]],
                "operation": "hold_for_spike",
                "reason": "Materials with predicted price increases",
                "priority": 5,
                "post_frequency": "wait",
            })
        
        return groups
    
    def _is_material(self, item: Dict) -> bool:
        """Check if item is a crafting material"""
        # Simplified check - in production, use item class
        material_keywords = ['ore', 'herb', 'leather', 'cloth', 'dust', 'essence']
        name = item.get('name', '').lower()
        return any(keyword in name for keyword in material_keywords)
    
    def recommend_operation(self, group_type: str) -> Dict:
        """
        Generate operation settings for a group type
        
        Returns operation with pricing rules
        """
        operations = {
            "aggressive_undercut": {
                "minPrice": "90% DBMarket",
                "normalPrice": "105% DBMarket",
                "maxPrice": "120% DBMarket",
                "undercut": 1,  # 1 copper
                "duration": 12,  # hours
                "stackSize": 1,
            },
            "volume_pricing": {
                "minPrice": "95% DBMarket",
                "normalPrice": "110% DBMarket",
                "maxPrice": "150% DBMarket",
                "undercut": 5,  # 5 copper
                "duration": 24,
                "stackSize": 200,  # Bulk stacks
            },
            "craft_and_sell": {
                "minPrice": "120% Crafting",
                "normalPrice": "150% Crafting",
                "maxPrice": "200% Crafting",
                "undercut": 1,
                "duration": 48,
                "stackSize": 1,
            },
            "patient_sale": {
                "minPrice": "200% DBMarket",
                "normalPrice": "300% DBMarket",
                "maxPrice": "500% DBMarket",
                "undercut": 0,  # Don't undercut
                "duration": 48,
                "stackSize": 1,
            },
            "hold_for_spike": {
                "minPrice": "150% DBMarket",
                "normalPrice": "200% DBMarket",
                "maxPrice": "300% DBMarket",
                "undercut": 1,
                "duration": 48,
                "stackSize": 200,
            }
        }
        
        return operations.get(group_type, operations["volume_pricing"])
    
    def predict_price_trend(self, item_id: int, price_history: List[Dict]) -> Dict:
        """
        Predict price trend using simple time-series analysis
        
        Args:
            item_id: Item to analyze
            price_history: List of {timestamp, price} dicts
        
        Returns:
            {trend: "rising"|"falling"|"stable", confidence: 0-1}
        """
        if len(price_history) < 7:
            return {"trend": "unknown", "confidence": 0.0}
        
        # Sort by timestamp
        sorted_history = sorted(price_history, key=lambda x: x['timestamp'])
        
        # Get prices
        prices = [p['price'] for p in sorted_history]
        
        # Calculate moving averages
        recent_avg = np.mean(prices[-7:])  # Last 7 data points
        older_avg = np.mean(prices[:7])    # First 7 data points
        
        # Calculate trend
        change = (recent_avg - older_avg) / older_avg
        
        if change > 0.15:
            trend = "rising"
            confidence = min(abs(change), 1.0)
        elif change < -0.15:
            trend = "falling"
            confidence = min(abs(change), 1.0)
        else:
            trend = "stable"
            confidence = 0.7
        
        return {
            "trend": trend,
            "confidence": confidence,
            "change_percent": change * 100,
        }
    
    def detect_weekend_spike_items(self, scan_data: List[Dict]) -> List[int]:
        """
        Identify items that spike in price on weekends
        
        Returns:
            List of item IDs with weekend spike patterns
        """
        weekend_items = []
        
        # This would analyze historical data to find patterns
        # For MVP, return items in certain categories known for weekend activity
        
        weekend_categories = [
            'consumables',  # Players raid on weekends
            'crafted_gear',  # Players prep for weekly reset
            'enchants',      # Players optimize gear
        ]
        
        for item in scan_data:
            # Simplified check
            if item.get('category') in weekend_categories:
                weekend_items.append(item['item_id'])
        
        return weekend_items[:20]
    
    def calculate_optimal_posting_time(self, item_id: int, sale_history: List[Dict]) -> str:
        """
        Calculate best time to post auctions for maximum profit
        
        Returns:
            Time recommendation like "Tuesday 6pm-9pm"
        """
        if not sale_history:
            return "Anytime"
        
        # Analyze sale timestamps
        hour_sales = defaultdict(int)
        day_sales = defaultdict(int)
        
        for sale in sale_history:
            dt = datetime.fromtimestamp(sale['timestamp'])
            hour_sales[dt.hour] += 1
            day_sales[dt.strftime("%A")] += 1
        
        # Find peak hour
        peak_hour = max(hour_sales.items(), key=lambda x: x[1])[0] if hour_sales else 18
        
        # Find peak day
        peak_day = max(day_sales.items(), key=lambda x: x[1])[0] if day_sales else "Tuesday"
        
        return f"{peak_day} {peak_hour}:00-{peak_hour+2}:00"

# ============================================================================
# Integration with GoblinAI Backend
# ============================================================================

def generate_auto_groups_endpoint(market_analysis: List[Dict]) -> Dict:
    """
    Flask endpoint handler for auto-group generation
    
    Usage in server.py:
        @app.route('/api/goblin/auto_groups')
        def goblin_auto_groups():
            analysis = goblin_engine.analyze_market()
            return generate_auto_groups_endpoint(analysis['opportunities'])
    """
    ml_engine = GoblinMLEngine()
    
    # Generate groups
    groups = ml_engine.generate_auto_groups(market_analysis)
    
    # Add operation details to each group
    for group in groups:
        operation_type = group['operation']
        group['operation_details'] = ml_engine.recommend_operation(operation_type)
    
    return {
        "groups": groups,
        "generated_at": datetime.now().isoformat(),
        "total_items": sum(len(g['items']) for g in groups),
    }

# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    # Test data
    test_market = [
        {
            "item_id": 210814,
            "name": "Algari Mana Potion",
            "profit": 75000,
            "profit_margin": 0.67,
            "sale_rate": 0.92,
            "num_auctions": 150,
            "is_craftable": True,
        },
        {
            "item_id": 211515,
            "name": "Null Stone",
            "profit": 170000,
            "profit_margin": 0.94,
            "sale_rate": 0.45,
            "num_auctions": 25,
            "is_craftable": False,
        },
    ]
    
    ml = GoblinMLEngine()
    groups = ml.generate_auto_groups(test_market)
    
    print("Auto-Generated Groups:")
    print(json.dumps(groups, indent=2))
