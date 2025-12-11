#!/usr/bin/env python3
"""
Intelligent Profession Guide Engine
Integrates with GoblinStack ML, market data, and inventory systems
for truly smart crafting recommendations
"""

import os
import psycopg2
import json
import requests
from datetime import datetime, timedelta

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://jgrayson@localhost/holocron')
GOBLIN_API_URL = os.getenv('GOBLIN_API_URL', 'http://localhost:5005/api')

class IntelligentProfessionEngine:
    """AI-powered profession recommendation engine"""
    
    def __init__(self, goblin_engine=None):
        self.conn = self._get_db_connection()
        self.market_cache = {}
        self.inventory_cache = {}
        self.goblin_engine = goblin_engine
    
    def _get_db_connection(self):
        try:
            return psycopg2.connect(DATABASE_URL)
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return None
    
    def get_market_price(self, item_id):
        """Get current market price from GoblinStack"""
        if item_id in self.market_cache:
            return self.market_cache[item_id]
        
        # 1. Try direct GoblinEngine access (Fastest, no deadlock)
        if self.goblin_engine:
            # Check TSM engine inside GoblinEngine
            if self.goblin_engine.tsm_engine:
                price = self.goblin_engine.tsm_engine.get_market_value(item_id)
                if price > 0:
                    self.market_cache[item_id] = price
                    return price
            
            # Check internal prices
            if item_id in self.goblin_engine.prices:
                price = self.goblin_engine.prices[item_id].market_value
                self.market_cache[item_id] = price
                return price

        # 2. Fallback: estimate from database or use simplified model
        return self._estimate_price(item_id)
    
    def _estimate_price(self, item_id):
        """Fallback price estimation"""
        # Simplified model based on item ID ranges
        if item_id < 10000:  # Classic materials
            return 5
        elif item_id < 50000:  # BC/Wrath
            return 20
        elif item_id < 100000:  # Cata/MoP
            return 50
        else:  # Modern
            return 150
    
    def calculate_recipe_profit(self, recipe):
        """Calculate real profit for a recipe using market data"""
        # Get material costs
        material_cost = 0
        for mat in recipe.get('materials', []):
            item_id = mat['item_id']
            quantity = mat['quantity']
            price = self.get_market_price(item_id)
            material_cost += price * quantity
        
        # Get crafted item value
        crafted_item_id = recipe.get('crafted_item_id')
        if not crafted_item_id:
            return 0
        
        sell_price = self.get_market_price(crafted_item_id)
        crafted_quantity = recipe.get('crafted_quantity', 1)
        
        # Calculate profit
        revenue = sell_price * crafted_quantity
        ah_cut = revenue * 0.05  # 5% AH cut
        profit = revenue - ah_cut - material_cost
        
        return {
            'material_cost': material_cost,
            'sell_price': sell_price,
            'revenue': revenue,
            'ah_cut': ah_cut,
            'profit': profit,
            'profit_margin': (profit / revenue * 100) if revenue > 0 else 0
        }
    
    def get_character_inventory(self, character_name):
        """Get character's material inventory"""
        # TODO: Query from DeepPockets data when available
        # For now, return empty
        return {}
    
    def calculate_gold_per_hour(self, recipe, profit_data):
        """Calculate gold/hour for a recipe"""
        # Estimated craft time based on profession
        avg_craft_time = 5  # seconds per craft
        crafts_per_hour = 3600 / avg_craft_time
        
        # Account for material gathering time if needed
        # (simplified - would need inventory check)
        gold_per_hour = profit_data['profit'] * crafts_per_hour
        
        return gold_per_hour
    
    def recommend_recipes_intelligent(self, character_name, profession, skill_level):
        """
        Intelligent recipe recommendations based on:
        1. Current skill level
        2. Market profitability
        3. Material availability
        4. Time efficiency (gold/hour)
        5. ML predictions
        """
        
        print(f"DEBUG: recommend_recipes_intelligent called for {character_name}, {profession}", flush=True)
        cur = self.conn.cursor()
        
        # Get recipes for this profession with materials
        cur.execute("""
            SELECT 
                recipe_id, recipe_name, skill_tier_name,
                materials, crafted_item_id, crafted_quantity
            FROM goblin.recipe_reference
            WHERE profession_name = %s
            AND materials IS NOT NULL
            ORDER BY recipe_id
            LIMIT 100
        """, (profession,))
        
        recommendations = []
        
        rows = cur.fetchall()
        print(f"DEBUG: Found {len(rows)} recipes", flush=True)
        
        for i, row in enumerate(rows):
            if i % 10 == 0: print(f"DEBUG: Processing recipe {i}", flush=True)
            recipe = {
                'id': row[0],
                'name': row[1],
                'tier': row[2],
             'materials': row[3],
                'crafted_item_id': row[4],
                'crafted_quantity': row[5]
            }
            
            # Calculate real profit
            profit_data = self.calculate_recipe_profit(recipe)
            
            if profit_data['profit'] <= 0:
                continue  # Skip unprofitable recipes
            
            # Calculate gold/hour
            gph = self.calculate_gold_per_hour(recipe, profit_data)
            
            # Calculate recommendation score
            score = self._calculate_intelligence_score(
                recipe, profit_data, gph, skill_level
            )
            
            recommendations.append({
                'recipe_name': recipe['name'],
                'profit': profit_data['profit'],
                'profit_margin': profit_data['profit_margin'],
                'gold_per_hour': gph,
                'cost': profit_data['material_cost'],
                'value': profit_data['sell_price'],
                'score': score,
                'recommendation': self._generate_smart_reason(
                    profit_data, gph, score
                )
            })
        
        # Sort by intelligence score
        recommendations.sort(key=lambda x: x['intelligence_score'], reverse=True)
        
        cur.close()
        return recommendations[:10]  # Top 10
    
    def _calculate_intelligence_score(self, recipe, profit_data, gph, skill_level):
        """
        Multi-factor intelligence score:
        - Profit margin (40%)
        - Gold/hour (30%)
        - Material availability (20%)
        - Market trend (10%)
        """
        score = 0
        
        # Factor 1: Profit margin (0-40 points)
        margin = profit_data['profit_margin']
        score += min(margin / 2.5, 40)  # Cap at 40
        
        # Factor 2: Gold/hour (0-30 points)
        gph_normalized = min(gph / 1000, 30)  # 30k+ gold/hour = max score
        score += gph_normalized
        
        # Factor 3: Material availability (0-20 points)
        # TODO: Check inventory, for now assume mid-range
        score += 10
        
        # Factor 4: Market trend (0-10 points)
        # TODO: Query ML predictions, for now use simplified
        score += 5
        
        return score
    
    def _generate_smart_reason(self, profit_data, gph, score):
        """Generate intelligent recommendation reason"""
        reasons = []
        
        if profit_data['profit'] > 1000:
            reasons.append(f"High profit: {profit_data['profit']:.0f}g per craft")
        
        if profit_data['profit_margin'] > 50:
            reasons.append(f"Excellent margin: {profit_data['profit_margin']:.0f}%")
        
        if gph > 10000:
            reasons.append(f"Time-efficient: {gph:.0f}g/hour")
        
        if not reasons:
            reasons.append("Profitable option")
        
        return " | ".join(reasons)
    
    def generate_multi_character_strategy(self, profession):
        """
        Coordinate multiple characters with same profession
        for maximum account-wide profit
        """
        cur = self.conn.cursor()
        
        # Get all characters with this profession
        cur.execute("""
            SELECT DISTINCT c.name, p.skill_level, p.max_skill
            FROM holocron.characters c
            JOIN goblin.professions p ON c.character_guid = p.character_guid
            WHERE p.profession_name = %s
        """, (profession,))
        
        characters = []
        for row in cur.fetchall():
            characters.append({
                'name': row[0],
                'skill': row[1],
                'max_skill': row[2]
            })
        
        if not characters:
            return {"error": "No characters found with this profession"}
        
        # Get profitable recipes
        strategy = {
            'profession': profession,
            'total_characters': len(characters),
            'assignments': []
        }
        
        # Assign recipes to characters based on skill and specs
        # (Simplified - full version would check specializations)
        for char in characters:
            recipes = self.recommend_recipes_intelligent(
                char['name'], profession, char['skill']
            )
            
            if recipes:
                best_recipe = recipes[0]
                strategy['assignments'].append({
                    'character': char['name'],
                    'skill_level': char['skill'],
                    'assigned_recipe': best_recipe['recipe'],
                    'expected_profit': best_recipe['profit'],
                    'gold_per_hour': best_recipe['gold_per_hour']
                })
        
        cur.close()
        return strategy
    
    def generate_dynamic_leveling_guide(self, character_name, profession, current_skill, target_skill):
        """
        Generate DYNAMIC leveling guide that updates based on TODAY'S market prices
        Finds the cheapest path to level up right now
        """
        
        cur = self.conn.cursor()
        
        # Get all recipes with materials for this profession
        cur.execute("""
            SELECT 
                recipe_id, recipe_name, skill_tier_name,
                materials, crafted_item_id, crafted_quantity
            FROM goblin.recipe_reference
            WHERE profession_name = %s
            AND materials IS NOT NULL
        """, (profession,))
        
        all_recipes = []
        for row in cur.fetchall():
            all_recipes.append({
                'id': row[0],
                'name': row[1],
                'tier': row[2],
                'materials': row[3],
                'crafted_item_id': row[4],
                'crafted_quantity': row[5]
            })
        
        cur.close()
        
        # Calculate cost for each recipe using CURRENT market prices
        recipe_costs = []
        for recipe in all_recipes:
            material_cost = 0
            for mat in recipe['materials']:
                price = self.get_market_price(mat['item_id'])
                material_cost += price * mat['quantity']
            
            recipe_costs.append({
                'recipe': recipe['name'],
                'cost_per_craft': material_cost,
                'materials': recipe['materials'],
                'tier': recipe['tier']
            })
        
        # Sort by cost (cheapest first)
        recipe_costs.sort(key=lambda x: x['cost_per_craft'])
        
        # Build leveling path
        leveling_path = []
        skill_points_needed = target_skill - current_skill
        
        # Group by skill brackets
        brackets = [
            {'range': f'{current_skill}-{current_skill+20}', 'points': 20},
            {'range': f'{current_skill+20}-{current_skill+40}', 'points': 20},
            {'range': f'{current_skill+40}-{target_skill}', 'points': skill_points_needed - 40}
        ]
        
        for bracket in brackets:
            if bracket['points'] <= 0:
                continue
            
            # Get cheapest recipes for this bracket
            # (Simplified - would need actual skill requirements)
            cheapest = recipe_costs[:3]
            
            bracket_guide = {
                'skill_range': bracket['range'],
                'recommended_recipes': []
            }
            
            for recipe in cheapest:
                # Estimate crafts needed (assume 1 point per craft, declining)
                crafts_needed = int(bracket['points'] / 0.7)  # Account for skill-up chance
                total_cost = recipe['cost_per_craft'] * crafts_needed
                
                bracket_guide['recommended_recipes'].append({
                    'recipe': recipe['recipe'],
                    'cost_per_craft': recipe['cost_per_craft'],
                    'crafts_needed': crafts_needed,
                    'total_cost': total_cost,
                    'materials_per_craft': recipe['materials'],
                    'price_updated': datetime.now().strftime("%Y-%m-%d %H:%M")
                })
            
            leveling_path.append(bracket_guide)
        
        # Calculate total leveling cost
        total_cost = sum(
            rec['total_cost'] 
            for bracket in leveling_path 
            for rec in bracket['recommended_recipes'][:1]  # Cheapest per bracket
        )
        
        guide = {
            'character': character_name,
            'profession': profession,
            'current_skill': current_skill,
            'target_skill': target_skill,
            'points_needed': skill_points_needed,
            'leveling_path': leveling_path,
            'total_estimated_cost': total_cost,
            'price_snapshot': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'note': 'Prices update daily - re-run for cheapest path'
        }
        
        return guide

def main():
    print("=" * 60)
    print("INTELLIGENT PROFESSION ENGINE")
    print("=" * 60)
    
    engine = IntelligentProfessionEngine()
    
    # Example: Get intelligent recommendations for Alchemy
    print("\n🧪 Intelligent Alchemy Recommendations (Skill 50)")
    recipes = engine.recommend_recipes_intelligent("Vaxo", "Alchemy", 50)
    
    print(f"\nTop {len(recipes)} Most Profitable Recipes:")
    for i, rec in enumerate(recipes[:5], 1):
        print(f"\n{i}. {rec['recipe']}")
        print(f"   💰 Profit: {rec['profit']:.0f}g ({rec['profit_margin']:.1f}% margin)")
        print(f"   ⏱️  Gold/Hour: {rec['gold_per_hour']:.0f}g")
        print(f"   📊 Intelligence Score: {rec['intelligence_score']:.1f}/100")
        print(f"   ℹ️  {rec['recommendation_reason']}")
    
    # Dynamic leveling guide
    print("\n" + "=" * 60)
    print("DYNAMIC LEVELING GUIDE (Price-Optimized)")
    print("=" * 60)
    
    leveling = engine.generate_dynamic_leveling_guide("Vaxo", "Alchemy", 45, 100)
    
    print(f"\n📈 Leveling Path: {leveling['current_skill']} → {leveling['target_skill']}")
    print(f"💰 Total Est. Cost: {leveling['total_estimated_cost']:.0f}g")
    print(f"🕒 Prices as of: {leveling['price_snapshot']}")
    print(f"\n{leveling['note']}")
    
    for i, bracket in enumerate(leveling['leveling_path'], 1):
        print(f"\n📖 Step {i}: {bracket['skill_range']}")
        cheapest = bracket['recommended_recipes'][0]
        print(f"   Best Option: {cheapest['recipe']}")
        print(f"   Cost: {cheapest['cost_per_craft']:.0f}g/craft × {cheapest['crafts_needed']} = {cheapest['total_cost']:.0f}g total")
        
        # Show alternative options
        if len(bracket['recommended_recipes']) > 1:
            alt = bracket['recommended_recipes'][1]
            print(f"   Alternative: {alt['recipe']} ({alt['cost_per_craft']:.0f}g/craft)")
    
    # Multi-character strategy
    print("\n" + "=" * 60)
    print("MULTI-CHARACTER STRATEGY (Example)")
    print("=" * 60)
    
    print("\n⚠️  Waiting for profession data import to enable multi-character optimization")
    print("   Once available, will coordinate:")
    print("   • Which character crafts which recipes")
    print("   • Account-wide gold/hour optimization")
    print("   • Material sharing strategies")
    
    # Save guide to file
    output_file = 'dynamic_leveling_guide.json'
    with open(output_file, 'w') as f:
        json.dump(leveling, f, indent=2)
    print(f"\n✅ Saved dynamic guide to {output_file}")

if __name__ == "__main__":
    main()

