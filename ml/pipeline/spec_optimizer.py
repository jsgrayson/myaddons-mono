"""
Spec Optimizer - Recommend profitable specializations based on market demand
"""
import os
import json
import pandas as pd
from loguru import logger
from typing import Dict, List, Any
from datetime import datetime

class SpecOptimizer:
    """Analyze market to recommend profitable profession specializations."""
    
    def __init__(self):
        self.auction_prices = {}
        
    def load_market_data(self):
        """Load current market prices."""
        raw_dir = os.path.join(os.path.dirname(__file__), "../data/raw")
        
        import glob
        all_files = sorted(glob.glob(os.path.join(raw_dir, "blizzard_*.csv")))
        
        if not all_files:
            logger.error("No auction data available")
            return
        
        latest_file = all_files[-1]
        df = pd.read_csv(latest_file)
        
        # Calculate average prices and volumes
        self.market_data = df.groupby('item_id').agg({
            'price': ['mean', 'min', 'max', 'count'],
            'quantity': 'sum'
        }).reset_index()
        
        logger.info(f"Loaded market data for {len(self.market_data)} items")
    
    def analyze_spec_demand(self, profession: str) -> Dict[str, Any]:
        """
        Analyze which specialization has highest profit potential.
        
        Args:
            profession: Profession name (e.g., "Blacksmithing")
        
        Returns:
            Spec recommendations with profit projections
        """
        logger.info(f"Analyzing {profession} specialization demand...")
        
        # Define spec-specific item categories (simplified)
        spec_items = self._get_spec_items(profession)
        
        recommendations = []
        
        for spec, item_ids in spec_items.items():
            # Calculate demand metrics
            demand = self._calculate_demand(item_ids)
            
            # Estimate weekly profit
            weekly_profit = self._estimate_weekly_profit(item_ids, demand)
            
            recommendations.append({
                "spec": spec,
                "demand_score": demand['score'],
                "competition": demand['competition'],
                "weekly_profit_estimate": weekly_profit,
                "top_items": demand['top_items'][:3],
                "recommendation": self._generate_recommendation(demand, weekly_profit)
            })
        
        # Sort by profit
        recommendations.sort(key=lambda x: x['weekly_profit_estimate'], reverse=True)
        
        return {
            "profession": profession,
            "timestamp": datetime.now().isoformat(),
            "recommendations": recommendations,
            "best_spec": recommendations[0]['spec'] if recommendations else None
        }
    
    def _get_spec_items(self, profession: str) -> Dict[str, List[int]]:
        """Map specs to their exclusive items."""
        # In production, load from recipe database
        # For now, return example structure
        
        if profession.lower() == "blacksmithing":
            return {
                "Armorsmithing": [12345, 12346, 12347],  # Plate armor items
                "Weaponsmithing": [23456, 23457, 23458]   # Weapon items
            }
        elif profession.lower() == "alchemy":
            return {
                "Potionmaster": [34567, 34568],
                "Transmutation": [45678, 45679],
                "Elixir Master": [56789, 56790]
            }
        
        return {"General": []}
    
    def _calculate_demand(self, item_ids: List[int]) -> Dict[str, Any]:
        """Calculate demand metrics for item set."""
        # Filter market data for these items
        relevant_items = self.market_data[self.market_data['item_id'].isin(item_ids)]
        
        if relevant_items.empty:
            return {
                "score": 0,
                "competition": "unknown",
                "top_items": []
            }
        
        # Demand score based on volume and price
        total_volume = relevant_items[('price', 'count')].sum()
        avg_price = relevant_items[('price', 'mean')].mean() / 10000  # To gold
        
        demand_score = (total_volume * avg_price) / 1000  # Normalized score
        
        # Competition (High vol = more sellers)
        competition = "high" if total_volume > 100 else "medium" if total_volume > 30 else "low"
        
        # Top items
        top = relevant_items.nlargest(3, ('price', 'mean'))
        top_items = [
            {"item_id": row['item_id'], "avg_price": row[('price', 'mean')] / 10000}
            for _, row in top.iterrows()
        ]
        
        return {
            "score": round(demand_score, 2),
            "competition": competition,
            "top_items": top_items
        }
    
    def _estimate_weekly_profit(self, item_ids: List[int], demand: Dict) -> int:
        """Estimate weekly profit from spec."""
        # Simplified calculation
        base_profit = demand['score'] * 1000  # Scale up
        
        # Adjust for competition
        if demand['competition'] == "low":
            base_profit *= 1.5
        elif demand['competition'] == "high":
            base_profit *= 0.5
        
        return int(base_profit)
    
    def _generate_recommendation(self, demand: Dict, profit: int) -> str:
        """Generate human-readable recommendation."""
        if profit > 50000:
            return f"HIGHLY RECOMMENDED - Strong demand, projected {profit/1000:.0f}k gold/week"
        elif profit > 20000:
            return f"Recommended - Moderate profit potential ({profit/1000:.0f}k gold/week)"
        else:
            return f"Consider alternatives - Low profit ({profit/1000:.0f}k gold/week)"

if __name__ == "__main__":
    optimizer = SpecOptimizer()
    optimizer.load_market_data()
    
    result = optimizer.analyze_spec_demand("Blacksmithing")
    
    print("\n" + "="*60)
    print(f"SPEC OPTIMIZER: {result['profession']}")
    print("="*60)
    print(f"\nBest Spec: {result['best_spec']}")
    
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"\n{i}. {rec['spec']}")
        print(f"   Weekly Profit: {rec['weekly_profit_estimate']/1000:.0f}k gold")
        print(f"   Competition: {rec['competition']}")
        print(f"   {rec['recommendation']}")
