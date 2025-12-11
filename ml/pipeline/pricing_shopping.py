"""
Pricing Formula Engine - TSM-compatible pricing with ML enhancements
"""
import re
from typing import Dict, Optional
from loguru import logger

class PricingEngine:
    """Evaluate pricing formulas (TSM-compatible + AI enhancements)."""
    
    def __init__(self):
        # Market data cache
        self.market_data = {}
        self.ml_predictions = {}
        
    def update_market_data(self, item_id: int, data: Dict):
        """Update market data for an item."""
        self.market_data[item_id] = data
    
    def update_ml_prediction(self, item_id: int, predicted_price: int, confidence: float):
        """Update ML prediction for an item."""
        self.ml_predictions[item_id] = {
            'price': predicted_price,
            'confidence': confidence
        }
    
    def evaluate(self, formula: str, item_id: int) -> int:
        """
        Evaluate a pricing formula.
        
        Supported variables:
        - dbmarket: Market average price
        - dbminbuyout: Minimum buyout
        - dbhistorical: Historical average
        - mlpredicted: ML predicted price
        - mlconfidence: ML confidence (0-1)
        - crafting: Crafting cost
        - vendorsell: Vendor sell price
        - vendorbuy: Vendor buy price
        
        Examples:
        - "dbmarket * 0.95" = 95% of market
        - "max(dbminbuyout, mlpredicted)" = Higher of min or ML prediction
        - "mlpredicted * mlconfidence + dbmarket * (1 - mlconfidence)" = Weighted blend
        """
        # Get data
        market = self.market_data.get(item_id, {})
        ml = self.ml_predictions.get(item_id, {})
        
        # Define variables
        variables = {
            'dbmarket': market.get('market_value', 0),
            'dbminbuyout': market.get('min_buyout', 0),
            'dbhistorical': market.get('historical_avg', 0),
            'mlpredicted': ml.get('price', 0),
            'mlconfidence': ml.get('confidence', 0.5),
            'crafting': market.get('crafting_cost', 0),
            'vendorsell': market.get('vendor_sell', 0),
            'vendorbuy': market.get('vendor_buy', 0)
        }
        
        # Replace variables in formula
        formula_eval = formula
        for var, value in variables.items():
            formula_eval = re.sub(r'\b' + var + r'\b', str(value), formula_eval)
        
        # Evaluate
        try:
            result = eval(formula_eval, {"__builtins__": {}, "max": max, "min": min, "abs": abs})
            return int(result)
        except Exception as e:
            logger.error(f"Error evaluating formula '{formula}': {e}")
            return variables.get('dbmarket', 0)
    
    def get_preset_formulas(self) -> Dict[str, str]:
        """Get common preset formulas."""
        return {
            'TSM Default': 'dbmarket',
            'Undercut Market': 'dbmarket * 0.95',
            'AI Prediction': 'mlpredicted',
            'AI Weighted': 'mlpredicted * mlconfidence + dbmarket * (1 - mlconfidence)',
            'Safe Minimum': 'max(dbminbuyout, mlpredicted * 0.8)',
            'Crafting Profit 30%': 'crafting * 1.3',
            'Above Vendor': 'max(vendorsell * 2, dbmarket)',
        }


class ShoppingSystem:
    """Advanced shopping and sniper mode."""
    
    def __init__(self):
        self.shopping_lists = {}
        self.sniper_running = False
        self.great_deals_threshold = 0.7  # 70% of market = great deal
        
    def create_shopping_list(self, name: str, item_ids: List[int], 
                             max_price_per_item: Optional[Dict[int, int]] = None):
        """Create a shopping list."""
        self.shopping_lists[name] = {
            'items': item_ids,
            'max_prices': max_price_per_item or {},
            'created_at': datetime.now()
        }
        logger.info(f"Created shopping list: {name} with {len(item_ids)} items")
    
    def scan_for_deals(self, ah_data: List[Dict], pricing_engine: PricingEngine) -> List[Dict]:
        """
        Scan AH for great deals.
        
        Returns list of deals with:
        - item_id, price, market_value, discount_pct, reason
        """
        deals = []
        
        for listing in ah_data:
            item_id = listing['item_id']
            price = listing['price_per_item']
            
            # Get market value
            market_data = pricing_engine.market_data.get(item_id, {})
            market_value = market_data.get('market_value', 0)
            
            if market_value == 0:
                continue
            
            # Calculate discount
            discount_pct = (market_value - price) / market_value
            
            if discount_pct >= (1 - self.great_deals_threshold):
                deals.append({
                    'item_id': item_id,
                    'price': price,
                    'market_value': market_value,
                    'discount_pct': discount_pct * 100,
                    'savings': market_value - price,
                    'reason': f'{discount_pct*100:.0f}% below market'
                })
        
        # Sort by best deals first
        deals.sort(key=lambda x: x['discount_pct'], reverse=True)
        
        logger.info(f"Found {len(deals)} great deals")
        return deals
    
    def sniper_mode(self, ah_data: List[Dict], pricing_engine: PricingEngine) -> List[Dict]:
        """
        Real-time sniper - find items posted way below value.
        
        More aggressive than shopping - looks for mistakes, underpricing.
        """
        snipes = []
        
        for listing in ah_data:
            item_id = listing['item_id']
            price = listing['price_per_item']
            
            # Get ML prediction
            ml = pricing_engine.ml_predictions.get(item_id, {})
            predicted = ml.get('price', 0)
            confidence = ml.get('confidence', 0)
            
            if predicted == 0 or confidence < 0.7:
                continue
            
            # Snipe if posted < 50% of predicted value (and high confidence)
            if price < predicted * 0.5:
                potential_profit = predicted - price
                roi = (potential_profit / price) * 100
                
                snipes.append({
                    'item_id': item_id,
                    'buy_price': price,
                    'predicted_sell': predicted,
                    'potential_profit': potential_profit,
                    'roi_pct': roi,
                    'confidence': confidence,
                    'reason': 'SNIPE - Posted at 50% of predicted value'
                })
        
        # Sort by ROI
        snipes.sort(key=lambda x: x['roi_pct'], reverse=True)
        
        if snipes:
            logger.warning(f"🎯 SNIPER: Found {len(snipes)} snipe opportunities!")
        
        return snipes


class GroupManager:
    """Manage item groups (like TSM groups)."""
    
    def __init__(self):
        self.groups = {}
    
    def create_group(self, name: str, item_ids: List[int], parent: Optional[str] = None):
        """Create an item group."""
        self.groups[name] = {
            'items': item_ids,
            'parent': parent,
            'operations': [],
            'created_at': datetime.now()
        }
        logger.info(f"Created group: {name} with {len(item_ids)} items")
    
    def assign_operation(self, group_name: str, operation_name: str):
        """Assign a posting operation to a group."""
        if group_name in self.groups:
            if operation_name not in self.groups[group_name]['operations']:
                self.groups[group_name]['operations'].append(operation_name)
                logger.info(f"Assigned operation '{operation_name}' to group '{group_name}'")
    
    def get_items_in_group(self, group_name: str) -> List[int]:
        """Get all items in a group."""
        return self.groups.get(group_name, {}).get('items', [])
    
    def import_ai_groups(self, ai_groups_data: Dict):
        """Import groups discovered by AI clustering."""
        for group_name, data in ai_groups_data.items():
            self.create_group(
                name=f"AI: {group_name}",
                item_ids=data.get('item_ids', [])
            )
        logger.success(f"Imported {len(ai_groups_data)} AI-discovered groups")
    
    def export_tsm_format(self) -> str:
        """Export groups in TSM import format."""
        # TSM uses a specific string format for group imports
        # This is simplified - real TSM format is more complex
        export_str = ""
        for name, data in self.groups.items():
            export_str += f"group:{name}\n"
            for item_id in data['items']:
                export_str += f"  i:{item_id}\n"
        return export_str


if __name__ == "__main__":
    from datetime import datetime
    
    # Example
    pricing = PricingEngine()
    pricing.update_market_data(12345, {'market_value': 10000, 'min_buyout': 9500})
    pricing.update_ml_prediction(12345, 11000, 0.85)
    
    formulas = pricing.get_preset_formulas()
    for name, formula in formulas.items():
        result = pricing.evaluate(formula, 12345)
        print(f"{name}: {formula} = {result} copper")
