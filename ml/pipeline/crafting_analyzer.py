"""
Crafting Profitability Analyzer - Calculate true profit including all sub-crafts
"""
import os
import json
import pandas as pd
from loguru import logger
from typing import Dict, List, Any, Tuple
from ml.pipeline.recipe_database import RecipeDatabase

class CraftingAnalyzer:
    """Analyze crafting profitability with full dependency resolution."""
    
    def __init__(self):
        self.recipe_db = RecipeDatabase()
        self.auction_prices = {}
        self.ah_cut = 0.05  # 5% AH fee
        
    def load_current_prices(self):
        """Load latest auction prices."""
        raw_dir = os.path.join(os.path.dirname(__file__), "../data/raw")
        
        import glob
        all_files = sorted(glob.glob(os.path.join(raw_dir, "blizzard_*.csv")))
        
        if not all_files:
            logger.error("No auction data available")
            return
        
        latest_file = all_files[-1]
        logger.info(f"Loading prices from {latest_file}")
        
        df = pd.read_csv(latest_file)
        
        # Get cheapest price per item
        self.auction_prices = df.groupby('item_id')['price'].min().to_dict()
        logger.info(f"Loaded prices for {len(self.auction_prices)} items")
    
    def calculate_material_cost(self, item_id: int, quantity: int = 1, 
                               craft_intermediates: bool = True) -> Tuple[float, List[Dict]]:
        """
        Calculate total cost to obtain materials.
        
        Args:
            item_id: Item to price
            quantity: How many needed
            craft_intermediates: If True, craft sub-components; if False, buy all
        
        Returns:
            (total_cost, cost_breakdown)
        """
        # Check if item can be crafted
        recipe = self.recipe_db._find_recipe_for_item(item_id)
        
        if not recipe and craft_intermediates:
            # Can't craft, must buy
            price = self.auction_prices.get(item_id, 0)
            if price == 0:
                logger.warning(f"No price data for item {item_id}")
            return price * quantity, [{
                "item_id": item_id,
                "quantity": quantity,
                "method": "buy",
                "cost": price * quantity
            }]
        
        if not craft_intermediates:
            # User wants to buy instead of craft
            price = self.auction_prices.get(item_id, 0)
            return price * quantity, [{
                "item_id": item_id,
                "quantity": quantity,
                "method": "buy",
                "cost": price * quantity
            }]
        
        # Craftable - recurse through dependencies
        total_cost = 0
        breakdown = []
        
        for reagent in recipe.get('reagents', []):
            reagent_id = reagent.get('reagent', {}).get('id')
            reagent_qty = reagent.get('quantity', 1) * quantity
            
            # Recursive cost calculation
            sub_cost, sub_breakdown = self.calculate_material_cost(
                reagent_id, reagent_qty, craft_intermediates
            )
            
            total_cost += sub_cost
            breakdown.extend(sub_breakdown)
        
        return total_cost, breakdown
    
    def generate_crafting_queue(self, item_id: int, quantity: int = 1) -> List[Dict]:
        """
        Generate ordered crafting queue (dependencies first).
        
        Returns list of steps in correct order:
        [
            {"action": "buy", "item_id": X, "quantity": Y},
            {"action": "craft", "item_id": Z, "quantity": W, "requires": [...]},
            ...
        ]
        """
        queue = []
        recipe = self.recipe_db._find_recipe_for_item(item_id)
        
        if not recipe:
            # Can't craft, just buy
            return [{"action": "buy", "item_id": item_id, "quantity": quantity}]
        
        # Build dependency tree
        tree = self.recipe_db.build_recipe_tree(recipe)
        
        # Flatten tree into queue (depth-first)
        self._build_queue_recursive(tree, quantity, queue)
        
        # Add final craft
        queue.append({
            "action": "craft",
            "item_id": item_id,
            "item_name": recipe.get('name', f'Item {item_id}'),
            "quantity": quantity,
            "recipe_id": recipe.get('id')
        })
        
        return queue
    
    def _build_queue_recursive(self, tree: Dict, multiplier: int, queue: List[Dict]):
        """Recursively build crafting queue."""
        for dep in tree.get('dependencies', []):
            qty = dep['quantity'] * multiplier
            
            if dep.get('craftable') and dep.get('sub_recipe'):
                # Craft this dependency first (recurse)
                self._build_queue_recursive(dep['sub_recipe'], qty, queue)
                queue.append({
                    "action": "craft",
                    "item_id": dep['item_id'],
                    "quantity": qty
                })
            else:
                # Buy raw material
                queue.append({
                    "action": "buy",
                    "item_id": dep['item_id'],
                    "quantity": qty
                })
    
    def analyze_profitability(self, item_id: int, quantity: int = 1) -> Dict[str, Any]:
        """
        Complete profitability analysis for crafting an item.
        
        Returns:
            {
                "item_id": ...,
                "quantity": ...,
                "sell_price": ...,
                "crafting_scenarios": [
                    {
                        "name": "Craft Everything",
                        "total_cost": ...,
                        "net_profit": ...,
                        "roi": ...,
                        "queue": [...]
                    },
                    {
                        "name": "Buy Intermediates",
                        ...
                    },
                    {
                        "name": "Just Flip (Buy & Resell)",
                        ...
                    }
                ],
                "recommendation": "..."
            }
        """
        # Get sell price
        sell_price_raw = self.auction_prices.get(item_id, 0)
        sell_price_after_cut = sell_price_raw * (1 - self.ah_cut) * quantity
        
        scenarios = []
        
        # Scenario 1: Craft everything
        craft_cost, craft_breakdown = self.calculate_material_cost(item_id, quantity, craft_intermediates=True)
        craft_queue = self.generate_crafting_queue(item_id, quantity)
        
        scenarios.append({
            "name": "Craft Everything",
            "total_cost": craft_cost,
            "net_profit": sell_price_after_cut - craft_cost,
            "roi": ((sell_price_after_cut - craft_cost) / craft_cost * 100) if craft_cost > 0 else 0,
            "queue": craft_queue,
            "breakdown": craft_breakdown
        })
        
        # Scenario 2: Buy intermediates
        buy_cost, buy_breakdown = self.calculate_material_cost(item_id, quantity, craft_intermediates=False)
        
        scenarios.append({
            "name": "Buy Intermediates",
            "total_cost": buy_cost,
            "net_profit": sell_price_after_cut - buy_cost,
            "roi": ((sell_price_after_cut - buy_cost) / buy_cost * 100) if buy_cost > 0 else 0,
            "queue": [{"action": "buy", "item_id": item_id, "quantity": quantity}],
            "breakdown": buy_breakdown
        })
        
        # Find best scenario
        best = max(scenarios, key=lambda x: x['net_profit'])
        
        return {
            "item_id": item_id,
            "quantity": quantity,
            "sell_price_raw": sell_price_raw * quantity,
            "sell_price_after_ah_cut": sell_price_after_cut,
            "scenarios": scenarios,
            "recommendation": best['name'],
            "best_profit": best['net_profit'],
            "best_roi": best['roi']
        }

if __name__ == "__main__":
    analyzer = CraftingAnalyzer()
    analyzer.load_current_prices()
    
    # Example: Analyze a random item
    if analyzer.auction_prices:
        sample_item = list(analyzer.auction_prices.keys())[0]
        result = analyzer.analyze_profitability(sample_item, quantity=1)
        
        print("\n" + "="*60)
        print(f"CRAFTING ANALYSIS: Item {sample_item}")
        print("="*60)
        print(f"Sell Price (after AH cut): {result['sell_price_after_ah_cut']/10000:.2f}g")
        print(f"\nRecommendation: {result['recommendation']}")
        print(f"Best Profit: {result['best_profit']/10000:.2f}g ({result['best_roi']:.1f}% ROI)")
