"""
Market Manipulation Detection - Identify price fixing, resets, and artificial scarcity
"""
import pandas as pd
import numpy as np
from loguru import logger
from typing import List, Dict

class ManipulationDetector:
    """Detect potential market manipulation and high-risk/high-reward events."""
    
    def __init__(self):
        self.reset_threshold = 2.0  # Price jumps > 200%
        self.scarcity_threshold = 0.2 # Supply drops to < 20% of average
        
    def detect_market_resets(self, price_history: pd.DataFrame) -> List[Dict]:
        """
        Detect recent market resets (someone bought everything and reposted higher).
        
        Logic:
        1. Sudden price spike (> 200%)
        2. Sudden volume drop (supply cleared)
        3. New listings appear at higher price
        """
        alerts = []
        
        # Group by item
        for item_id, group in price_history.groupby('item_id'):
            if len(group) < 5: continue
            
            # Sort by time
            group = group.sort_values('timestamp')
            
            # Check last 2 data points
            current = group.iloc[-1]
            previous = group.iloc[-2]
            
            price_change = current['price'] / previous['price']
            volume_change = current['quantity'] / previous['quantity'] if previous['quantity'] > 0 else 1.0
            
            if price_change > self.reset_threshold:
                # Potential reset
                confidence = 0.0
                
                if volume_change < 0.5:
                    # Supply dropped significantly before price hike (classic reset)
                    confidence = 0.9
                else:
                    # Price just jumped, maybe organic?
                    confidence = 0.6
                
                alerts.append({
                    'type': 'MARKET_RESET',
                    'item_id': item_id,
                    'price_jump_pct': round((price_change - 1) * 100),
                    'confidence': confidence,
                    'timestamp': current['timestamp'],
                    'action': 'SELL', # Sell into the reset
                    'message': f"Market Reset Detected! Price jumped {round((price_change - 1) * 100)}%"
                })
                
        return alerts

    def detect_artificial_scarcity(self, price_history: pd.DataFrame) -> List[Dict]:
        """
        Detect items being monopolized (one seller controlling supply).
        
        Requires seller data (from addon scan).
        """
        alerts = []
        # This requires seller name data which we might not have in basic history
        # Placeholder for logic:
        # If top_seller_share > 80% AND price > historical_avg * 1.5 -> Monopoly
        return alerts

    def detect_dumping(self, price_history: pd.DataFrame) -> List[Dict]:
        """
        Detect panic selling or dumping (price crashing).
        """
        alerts = []
        for item_id, group in price_history.groupby('item_id'):
            if len(group) < 5: continue
            group = group.sort_values('timestamp')
            
            current = group.iloc[-1]
            previous = group.iloc[-2]
            
            price_change = current['price'] / previous['price']
            
            if price_change < 0.5: # 50% drop
                alerts.append({
                    'type': 'PRICE_CRASH',
                    'item_id': item_id,
                    'drop_pct': round((1 - price_change) * 100),
                    'confidence': 0.8,
                    'timestamp': current['timestamp'],
                    'action': 'BUY', # Potential snipe if overreaction
                    'message': f"Price Crash! Dropped {round((1 - price_change) * 100)}%"
                })
        return alerts

    def analyze_market(self, price_history: pd.DataFrame) -> List[Dict]:
        """Run all detection algorithms."""
        all_alerts = []
        all_alerts.extend(self.detect_market_resets(price_history))
        all_alerts.extend(self.detect_dumping(price_history))
        
        logger.info(f"Manipulation detection found {len(all_alerts)} alerts")
        return all_alerts
