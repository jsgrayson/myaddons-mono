#!/usr/bin/env python3
"""
The Artificer - Crafting Solver & Supply Chain Manager
Optimizes Concentration usage and manages cross-character reagents.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ConcentrationData:
    recipe_id: int
    concentration_cost: int
    r2_price: float
    r3_price: float
    
class ArtificerEngine:
    def __init__(self, goblin_engine, deeppockets_engine):
        self.goblin = goblin_engine
        self.deeppockets = deeppockets_engine
        self.concentration_db = self._load_mock_concentration_data()

    def _load_mock_concentration_data(self) -> Dict[int, ConcentrationData]:
        """
        Mock database of concentration costs and difficulty.
        In reality, this would come from an addon export.
        """
        return {
            370607: ConcentrationData(370607, 150, 400.0, 1200.0), # Elemental Potion
            2003: ConcentrationData(2003, 200, 150.0, 1200.0),     # Enchant Weapon
            2002: ConcentrationData(2002, 300, 2000.0, 5000.0),    # Plate Helm
        }

    def calculate_concentration_value(self) -> List[Dict]:
        """
        Calculate the Gold per Concentration point for known recipes.
        Value = (Price_Quality3 - Price_Quality2) / Concentration_Cost
        """
        results = []
        
        for recipe_id, data in self.concentration_db.items():
            # Try to get real prices from Goblin if available, else use mock defaults
            # Goblin prices are keyed by Item ID, but here we have Recipe IDs.
            # For simplicity in this mock, we'll assume the data.r2/r3_price are accurate 
            # or we would look up the result item ID from Goblin recipes.
            
            diff = data.r3_price - data.r2_price
            gpc = diff / data.concentration_cost if data.concentration_cost > 0 else 0
            
            results.append({
                "recipe_id": recipe_id,
                "name": self._get_recipe_name(recipe_id),
                "concentration_cost": data.concentration_cost,
                "profit_gain": diff,
                "gold_per_concentration": round(gpc, 2)
            })
            
        # Sort by best value
        results.sort(key=lambda x: x["gold_per_concentration"], reverse=True)
        return results

    def solve_supply_chain(self, recipe_id: int, quantity: int = 1) -> Dict:
        """
        Identify missing reagents and find them on alts.
        Returns a list of 'Mail Tasks'.
        """
        # 1. Get Recipe Reagents (Mocking lookup for now)
        reagents = self._get_mock_reagents(recipe_id)
        
        mail_tasks = []
        missing_reagents = []
        
        for item_id, required_count in reagents.items():
            total_needed = required_count * quantity
            
            # Check Main's Inventory (Mock: assume main has 0 for demo)
            # real: self.deeppockets.get_item_count(main_char, item_id)
            on_main = 0 
            
            needed = total_needed - on_main
            
            if needed > 0:
                # Search Alts using DeepPockets
                # We need a method to find *who* has the item.
                # deepockets.search_inventory returns locations.
                locations = self.deeppockets.search_inventory(str(item_id))
                
                found_on_alts = 0
                for loc in locations:
                    # Skip main (logic to be refined with real char name)
                    if loc['character'] == "Main": continue
                    
                    amount_to_take = min(loc['count'], needed - found_on_alts)
                    if amount_to_take > 0:
                        mail_tasks.append({
                            "from": loc['character'],
                            "item_id": item_id,
                            "item_name": self._get_item_name(item_id),
                            "count": amount_to_take,
                            "container": loc['container']
                        })
                        found_on_alts += amount_to_take
                        
                    if found_on_alts >= needed:
                        break
                
                if found_on_alts < needed:
                    missing_reagents.append({
                        "item_id": item_id,
                        "name": self._get_item_name(item_id),
                        "count": needed - found_on_alts
                    })

        return {
            "recipe_id": recipe_id,
            "recipe_name": self._get_recipe_name(recipe_id),
            "mail_tasks": mail_tasks,
            "shopping_list": missing_reagents
        }

    def _get_recipe_name(self, recipe_id):
        # Mock lookup
        names = {
            370607: "Elemental Potion of Ultimate Power",
            2003: "Enchant Weapon - Sophic Devotion",
            2002: "Draconium Plate Helm"
        }
        return names.get(recipe_id, f"Recipe {recipe_id}")

    def _get_item_name(self, item_id):
        # Mock lookup
        names = {
            194820: "Hochenblume",
            200111: "Resonant Crystal",
            198765: "Draconium Ore"
        }
        return names.get(item_id, f"Item {item_id}")

    def _get_mock_reagents(self, recipe_id):
        if recipe_id == 370607: # Potion
            return {194820: 2, 200111: 1} # 2 Hochenblume, 1 Crystal
        return {}
