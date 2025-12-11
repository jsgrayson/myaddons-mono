#!/usr/bin/env python3
"""
Goblin Brain - Market Prediction & Crafting Optimizer
Analyzes market data to identify profitable crafting opportunities
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import random

class ItemType(Enum):
    MATERIAL = "Material"
    CONSUMABLE = "Consumable"
    GEAR = "Gear"
    ENCHANT = "Enchant"

@dataclass
class ItemPrice:
    item_id: int
    name: str
    item_type: ItemType
    market_value: int  # Gold
    min_buyout: int    # Gold
    region_avg: int    # Gold
    sale_rate: float   # 0.0 to 1.0 (velocity)
    
@dataclass
class Item:
    id: int
    name: str
    item_type: ItemType
    market_value: int
    sale_rate: float

class Profession(Enum):
    ALCHEMY = "Alchemy"
    BLACKSMITHING = "Blacksmithing"
    ENCHANTING = "Enchanting"
    ENGINEERING = "Engineering"
    INSCRIPTION = "Inscription"
    JEWELCRAFTING = "Jewelcrafting"
    LEATHERWORKING = "Leatherworking"
    TAILORING = "Tailoring"
    MINING = "Mining"
    HERBALISM = "Herbalism"
    SKINNING = "Skinning"

@dataclass
class Recipe:
    recipe_id: int
    name: str
    profession: Profession
    reagents: Dict[int, int]  # {item_id: quantity}
    result_item_id: int
    output_quantity: int = 1

class Profession(Enum):
    ALCHEMY = "Alchemy"
    BLACKSMITHING = "Blacksmithing"
    ENCHANTING = "Enchanting"
    ENGINEERING = "Engineering"
    INSCRIPTION = "Inscription"
    JEWELCRAFTING = "Jewelcrafting"
    LEATHERWORKING = "Leatherworking"
    TAILORING = "Tailoring"
    MINING = "Mining"
    HERBALISM = "Herbalism"
    SKINNING = "Skinning"

import json
import os
from datetime import datetime, timedelta

class GoblinEngine:
    """
    Economic intelligence engine for market analysis and crafting optimization
    """
    
    HISTORY_FILE = "goblin_history.json"
    
    TITLES = [
        (90, "Trade Prince"),
        (75, "Baron"),
        (50, "Merchant"),
        (25, "Peddler"),
        (0, "Peon")
    ]
    
    def __init__(self, tsm_engine=None):
        self.tsm_engine = tsm_engine
        self.prices = {}  # {item_id: ItemPrice}
        self.recipes = []
        self.items = []
        self.history = self._load_history()
        
    def _load_history(self) -> List[Dict]:
        if os.path.exists(self.HISTORY_FILE):
            try:
                with open(self.HISTORY_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def record_snapshot(self):
        """Records the current total value of the portfolio"""
        total_value = 0
        
        # Calculate value of tracked items (using mock prices for now if TSM missing)
        # In a real scenario, this would iterate over the Warden's inventory
        # For now, we'll simulate a fluctuating portfolio value based on our mock items
        
        # Base value from mock items
        base_value = 1250000 
        
        # Add some random fluctuation to simulate market changes
        fluctuation = random.randint(-50000, 50000)
        total_value = base_value + fluctuation
        
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "total_gold": total_value,
            "active_auctions": 47 + random.randint(-5, 5),
            "flips_today": 12 + random.randint(0, 5)
        }
        
        self.history.append(snapshot)
        
        # Keep only last 30 days
        if len(self.history) > 30:
            self.history = self.history[-30:]
            
        with open(self.HISTORY_FILE, 'w') as f:
            json.dump(self.history, f, indent=4)
            
        print(f"Recorded Snapshot: {total_value}g")

    def get_history(self, days=7) -> List[Dict]:
        """Returns the last N days of history"""
        # If history is empty, generate some mock history for the demo
        if not self.history:
            self._generate_mock_history()
            
        return self.history[-days:]

    def _generate_mock_history(self):
        """Generates fake history for the past 7 days for visualization"""
        base_value = 1200000
        now = datetime.now()
        
        for i in range(7, 0, -1):
            date = now - timedelta(days=i)
            # Create a nice upward trend
            daily_value = base_value + (i * 10000) + random.randint(-5000, 5000)
            
            self.history.append({
                "timestamp": date.isoformat(),
                "total_gold": daily_value,
                "active_auctions": 40 + random.randint(0, 10),
                "flips_today": 5 + random.randint(0, 10)
            })
        
        self.record_snapshot() # Add today

        
    def load_mock_data(self):
        """Load mock market and recipe data"""
        
        # 1. Define Items & Prices
        # Materials
        self.prices[1001] = ItemPrice(1001, "Draconium Ore", ItemType.MATERIAL, 45, 42, 48, 0.95)
        self.prices[1002] = ItemPrice(1002, "Khaz Algar Herb", ItemType.MATERIAL, 25, 24, 28, 0.90)
        self.prices[1003] = ItemPrice(1003, "Awakened Order", ItemType.MATERIAL, 150, 145, 160, 0.85)
        self.prices[1004] = ItemPrice(1004, "Resonant Crystal", ItemType.MATERIAL, 200, 190, 210, 0.60)
        
        # Crafted Items
        self.prices[2001] = ItemPrice(2001, "Algari Healing Potion", ItemType.CONSUMABLE, 80, 75, 85, 0.80)
        self.prices[2002] = ItemPrice(2002, "Draconium Plate Helm", ItemType.GEAR, 2500, 2400, 2600, 0.20)
        self.prices[2003] = ItemPrice(2003, "Enchant Weapon - Sophic Devotion", ItemType.ENCHANT, 1200, 1150, 1250, 0.75)
        self.prices[2004] = ItemPrice(2004, "Khaz Algar Flask", ItemType.CONSUMABLE, 400, 380, 420, 0.65)
        
        # 2. Define Recipes
        self.recipes = []
            # Potion: 2 Herbs (25g ea) -> 1 Potion (80g)
        """Load mock recipe and item data"""
        # But we don't need to define prices here if we use TSM, 
        # though for now we'll keep them as fallback or base cost.
        
        # 1. Draconium Ore (Material)
        draconium = Item(198765, "Draconium Ore", ItemType.MATERIAL, 45, 0.95)
        
        # 2. Khaz'gorite Ore (Material)
        khazgorite = Item(198766, "Khaz'gorite Ore", ItemType.MATERIAL, 120, 0.80)
        
        # 3. Resonant Crystal (Material)
        crystal = Item(200111, "Resonant Crystal", ItemType.MATERIAL, 200, 0.50)
        
        # 4. Hochenblume (Material)
        hochenblume = Item(194820, "Hochenblume", ItemType.MATERIAL, 15, 0.90)
        
        self.items = [draconium, khazgorite, crystal, hochenblume]
        
        # Recipes
        # 1. Draconium Ingot (Smelting)
        # Requires: 2 Draconium Ore
        ingot_recipe = Recipe(
            382900, "Draconium Ingot", Profession.MINING,
            {198765: 2}, 382901, 1
        )
        
        # 2. Elemental Potion of Ultimate Power (Alchemy)
        # Requires: 2 Hochenblume, 1 Crystal
        potion_recipe = Recipe(
            370607, "Elemental Potion of Ultimate Power", Profession.ALCHEMY,
            {194820: 2, 200111: 1}, 191304
        )
        
        self.recipes = [ingot_recipe, potion_recipe]
        print(f"✓ Loaded {len(self.items)} items, {len(self.recipes)} recipes")
        
    def calculate_crafting_cost(self, recipe: Recipe) -> int:
        """Calculate total material cost for a recipe"""
        total_cost = 0
        for item_id, quantity in recipe.materials.items():
            if item_id in self.prices:
                total_cost += self.prices[item_id].min_buyout * quantity
        return total_cost
    
    def analyze_market(self) -> Dict:
        """Analyze market for opportunities"""
        opportunities = []
        
        for recipe in self.recipes:
            # Calculate Crafting Cost
            crafting_cost = 0
            for mat_id, qty in recipe.reagents.items():
                # Use TSM price if available, else fallback to item.market_value
                mat_price = 0
                if self.tsm_engine:
                    mat_price = self.tsm_engine.get_market_value(mat_id)
                
                if mat_price == 0:
                    # Fallback to internal item list
                    mat_item = next((i for i in self.items if i.id == mat_id), None)
                    if mat_item:
                        mat_price = mat_item.market_value
                
                crafting_cost += mat_price * qty
            
            # Calculate Market Value of Result
            result_price = 0
            if self.tsm_engine:
                result_price = self.tsm_engine.get_market_value(recipe.result_item_id)
            
            # Fallback for result price (mock)
            if result_price == 0:
                 if recipe.name == "Draconium Ingot": result_price = 100
                 elif recipe.name == "Elemental Potion of Ultimate Power": result_price = 500
            
            profit = result_price - crafting_cost
            margin = (profit / crafting_cost) * 100 if crafting_cost > 0 else 0
            
            # Score = Profit * Sale Rate (Velocity)
            # High profit items that never sell get lower priority
            # For now, use a mock sale rate for the result item
            # In a real scenario, TSM would provide this for the result_item_id
            mock_sale_rate = 0.75 # Placeholder
            score = profit * mock_sale_rate
            
            # Find the output item for its type and name
            output_item_name = "Unknown"
            output_item_type = "Unknown"
            output_item_obj = next((i for i in self.items if i.id == recipe.result_item_id), None)
            if output_item_obj:
                output_item_name = output_item_obj.name
                output_item_type = output_item_obj.item_type.value

            opportunities.append({
                "recipe_name": recipe.name,
                "output_item": output_item_name,
                "type": output_item_type,
                "crafting_cost": int(crafting_cost),
                "market_value": int(result_price),
                "profit": int(profit),
                "profit_margin": int(margin),
                "sale_rate": mock_sale_rate,
                "score": int(score),
                "recommendation": self._get_recommendation(profit, mock_sale_rate)
            })
            
        # Sort by score (best opportunities first)
        opportunities.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "opportunities": opportunities,
            "timestamp": "Now",
            "total_potential_profit": sum(o["profit"] for o in opportunities if o["profit"] > 0)
        }
        
    def get_sniper_list(self) -> List[Dict]:
        """
        Identify underpriced items (Sniper)
        For mock data, we'll return a few fixed examples.
        """
        return [
            {
                "item": "Draconium Ore",
                "listed_price": 15,
                "market_value": 45,
                "potential_profit": 30
            },
            {
                "item": "Resonant Crystal",
                "listed_price": 150,
                "market_value": 200,
                "potential_profit": 50
            }
        ]
    
    def get_posting_instructions(self) -> List[Dict]:
        """
        Generate posting instructions for the in-game addon.
        Returns: List of {item_id, min_price, normal_price, max_price, stack_size}
        """
        instructions = []
        
        # For MVP, we'll generate instructions for our known items
        # In reality, this would filter for items currently in the player's inventory (via DeepPockets)
        
        for item in self.items:
            # Simple pricing logic for demo
            # Min = 80% of market, Normal = 100%, Max = 150%
            market = item.market_value
            
            instructions.append({
                "item_id": item.id,
                "name": item.name, # Helper for Lua debug
                "min_price": int(market * 0.8 * 10000), # Convert to copper
                "normal_price": int(market * 1.0 * 10000),
                "max_price": int(market * 1.5 * 10000),
                "stack_size": 1, # Default to singles for gear, max for mats?
                "undercut": 1 # 1 copper
            })
            
        return instructions

    def get_mail_instructions(self) -> List[Dict]:
        """
        Generate mailing instructions for the in-game addon.
        Returns: List of {item_id, target, keep_amount, reason}
        """
        instructions = []
        
        # Mock Rules (In reality, these would be user-configured)
        # 1. Herbs -> Alchemist (Alt-A)
        # 2. Ore -> Blacksmith (Main)
        # 3. Cloth -> Tailor (Alt-B)
        # 4. BoE/Transmog -> Banker (BankAlt)
        
        # We'll use our mock items to demonstrate
        
        # Draconium Ore (198765) -> Main
        instructions.append({
            "item_id": 198765,
            "target": "Main",
            "keep_amount": 0,
            "reason": "Blacksmithing"
        })
        
        # Hochenblume (194820) -> Alt-A
        instructions.append({
            "item_id": 194820,
            "target": "Alt-A",
            "keep_amount": 0,
            "reason": "Alchemy"
        })
        
        # Resonant Crystal (200111) -> BankAlt (Valuable Mat)
        instructions.append({
            "item_id": 200111,
            "target": "BankAlt",
            "keep_amount": 0,
            "reason": "Storage"
        })
        
        return instructions

    def get_best_crafting_value(self, item_id: int) -> float:
        """
        Calculate the highest potential value of an item if used in crafting.
        Returns: Value per unit of the item.
        """
        best_value = 0.0
        
        # Iterate through all recipes to see if this item is a reagent
        for recipe in self.recipes:
            if item_id in recipe.reagents:
                # Calculate value contribution:
                # (Result Price - Cost of OTHER reagents) / Quantity of THIS reagent
                
                result_price = 0
                if self.tsm_engine:
                    result_price = self.tsm_engine.get_market_value(recipe.result_item_id)
                
                # Fallback Result Price
                if result_price == 0:
                     if recipe.name == "Draconium Ingot": result_price = 100
                     elif recipe.name == "Elemental Potion of Ultimate Power": result_price = 500
                
                other_reagents_cost = 0
                this_reagent_qty = recipe.reagents[item_id]
                
                for rid, qty in recipe.reagents.items():
                    if rid != item_id:
                        # Cost of other reagents
                        r_price = 0
                        if self.tsm_engine:
                            r_price = self.tsm_engine.get_market_value(rid)
                        if r_price == 0:
                             # Fallback
                             r_item = next((i for i in self.items if i.id == rid), None)
                             if r_item: r_price = r_item.market_value
                        
                        other_reagents_cost += r_price * qty
                
                # Value attributed to this item
                # Profit from craft = Result - (Other + This)
                # We want to know if (Result - Other) / Qty > Current Value
                implied_value = (result_price - other_reagents_cost) / this_reagent_qty
                
                if implied_value > best_value:
                    best_value = implied_value
                    
        return best_value

    def get_destroy_instructions(self) -> List[Dict]:
        """
        Generate destroy instructions (Disenchant/Mill/Prospect).
        Returns: List of {item_id, action, macro_text}
        """
        instructions = []
        
        # Mock Rules
        # 1. Green Gear -> Disenchant
        # 2. Herbs -> Mill
        # 3. Ore -> Prospect
        
        # Mock Values
        # Dust = 20g, Pigment = 50g, Gem = 100g
        
        # Mock Items
        # Green Bracers (123456) -> Disenchant
        # Market Value: 15g. Destroy Value: 20g (1 Dust). Profit: +5g.
        # Crafting Value: 0 (Not used in crafting)
        instructions.append({
            "item_id": 123456,
            "action": "Disenchant",
            "macro_text": "/cast Disenchant\n/use item:123456",
            "profit": 5,
            "destroy_value": 20,
            "market_value": 15
        })
        
        # Draconium Ore (198765) -> Prospect (if > 5)
        # Market Value: 45g. 
        # Destroy Value: 60g (0.6 Gem). 
        # Crafting Value (Ingot): (100g - 0) / 2 = 50g.
        # Best Alternative: Crafting (50g) > Market (45g).
        # Destroy (60g) > Crafting (50g).
        # Profit vs Best Alt: 60 - 50 = +10g.
        
        crafting_val = self.get_best_crafting_value(198765) # Should be 50
        market_val = 45
        destroy_val = 60
        best_alt = max(market_val, crafting_val)
        
        if destroy_val > best_alt:
            instructions.append({
                "item_id": 198765,
                "action": "Prospect",
                "macro_text": "/cast Prospecting\n/use item:198765",
                "profit": destroy_val - best_alt,
                "destroy_value": destroy_val,
                "market_value": best_alt # Show the best alternative as the baseline
            })
        
        return instructions

    def generate_tsm_string(self, items: List[int]) -> str:
        """
        Generate a TSM Group Import string from a list of item IDs.
        Format: i:12345,i:67890
        """
        if not items:
            return ""
        
        # Filter out invalid IDs
        valid_ids = [str(i) for i in items if isinstance(i, int) and i > 0]
        
        # Prefix with 'i:' and join with commas
        tsm_string = ",".join([f"i:{i}" for i in valid_ids])
        
        return tsm_string
    
    def _get_recommendation(self, profit: float, sale_rate: float) -> str:
        """Generate recommendation string"""
        if profit <= 0:
            return "DO NOT CRAFT (Loss)"
        
        if sale_rate >= 0.5:
            if profit > 500:
                return "CRAFT IMMEDIATELY (High Profit/High Vol)"
            elif profit > 100:
                return "Craft (Good Profit)"
            else:
                return "Craft (Low Margin)"
        else:
            if profit > 1000:
                return "Craft 1-2 (High Profit/Low Vol)"
            else:
                return "Avoid (Low Vol/Low Profit)"

    def calculate_score(self, weekly_income: int, profit_margin: int) -> Dict:
        """Calculate score based on metrics"""
        # Score components
        income_score = min(50, (weekly_income / 20000) * 50) # Cap at 20k/week for 50pts
        margin_score = min(30, profit_margin) # Cap at 30% margin for 30pts
        activity_score = 20 # Mock activity score
        
        total_score = int(income_score + margin_score + activity_score)
        total_score = min(100, total_score)
        
        return {
            "score": total_score,
            "title": self._get_title(total_score),
            "comparison": self._get_comparison(weekly_income)
        }
        
    def _get_title(self, score: int) -> str:
        current_title = "Peon"
        for threshold, title in self.TITLES:
            if score >= threshold:
                current_title = title
        return current_title
        
    def _get_comparison(self, income: int) -> str:
        trade_prince_avg = 100000
        percent = int((income / trade_prince_avg) * 100)
        return f"You are earning {percent}% of a Trade Prince's weekly average."

# Update GoblinEngine to include new modules
class GoblinEngineExpanded(GoblinEngine):
    def __init__(self):
        super().__init__()
        
    def get_score(self) -> Dict:
        # Mock inputs for now
        return self.calculate_score(15400, 25)

if __name__ == "__main__":
    # Test the engine
    print("\n" + "="*70)
    print("GOBLIN BRAIN - Market Intelligence")
    print("="*70)
    
    engine = GoblinEngine()
    engine.load_mock_data()
    
    # Test 1: Market Analysis
    print("\n" + "="*70)
    print("CRAFTING OPPORTUNITIES")
    print("="*70)
    
    analysis = engine.analyze_market()
    
    for i, opp in enumerate(analysis['opportunities'], 1):
        print(f"\n  {i}. {opp['recipe_name']} ({opp['type']})")
        print(f"     Cost: {opp['crafting_cost']}g | Sell: {opp['market_value']}g")
        print(f"     Profit: {opp['profit']}g ({opp['profit_margin']}%)")
        print(f"     Sale Rate: {opp['sale_rate']} | Score: {opp['score']}")
        print(f"     Action: {opp['recommendation']}")
        
    print(f"\n  Total Potential Profit: {analysis['total_potential_profit']}g")
    
    # Test 2: Sniper
    print("\n" + "="*70)
    print("SNIPER HITS")
    print("="*70)
    
    hits = engine.get_sniper_list()
    for hit in hits:
        print(f"\n  • {hit['item']}")
        print(f"    Buy: {hit['listed_price']}g | Market: {hit['market_value']}g")
        print(f"    Flip Profit: {hit['potential_profit']}g")
    
    print("\n" + "="*70)
    print("✓ All tests complete!")
    print("="*70)
