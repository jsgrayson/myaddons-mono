#!/usr/bin/env python3
"""
Generate crafting leveling guides using recipe material data.
Creates optimal recipe paths to level professions efficiently.
"""

import os
import psycopg2
import json
from collections import defaultdict

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://jgrayson@localhost/holocron')

def get_db_connection():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def get_recipes_with_materials(profession_name):
    """Get recipes that have material data for a profession"""
    conn = get_db_connection()
    if not conn:
        return []
    
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            recipe_id,
            recipe_name,
            skill_tier_name,
            materials,
            crafted_item_id,
            crafted_quantity
        FROM goblin.recipe_reference
        WHERE profession_name = %s
        AND materials IS NOT NULL
        ORDER BY skill_tier_name, recipe_name
    """, (profession_name,))
    
    recipes = []
    for row in cur.fetchall():
        recipes.append({
            'id': row[0],
            'name': row[1],
            'tier': row[2],
            'materials': row[3] if row[3] else [],  # Already parsed by psycopg2
            'crafted_item_id': row[4],
            'crafted_quantity': row[5] or 1
        })
    
    cur.close()
    conn.close()
    return recipes

def estimate_material_cost(materials):
    """Estimate cost of materials (simplified)"""
    # Mock cost estimation - in real implementation, would use market data
    total_cost = 0
    for mat in materials:
        item_id = mat['item_id']
        quantity = mat['quantity']
        
        # Rough cost estimates based on item ID ranges
        if item_id < 10000:  # Classic materials
            cost_per_unit = 5
        elif item_id < 50000:  # BC/Wrath materials
            cost_per_unit = 10
        elif item_id < 100000:  # Cata/MoP materials
            cost_per_unit = 20
        else:  # Modern materials
            cost_per_unit = 50
        
        total_cost += cost_per_unit * quantity
    
    return total_cost

def generate_leveling_guide(profession_name):
    """Generate a crafting leveling guide for a profession"""
    recipes = get_recipes_with_materials(profession_name)
    
    if not recipes:
        return None
    
    # Group by expansion/tier
    by_tier = defaultdict(list)
    for recipe in recipes:
        tier = recipe['tier'] or 'Unknown'
        by_tier[tier].append(recipe)
    
    # Expansion tier mapping with keywords and level ranges
    expansion_tiers = [
        {'name': 'Classic', 'keywords': ['Classic'], 'levels': '1-60'},
        {'name': 'Burning Crusade', 'keywords': ['Outland'], 'levels': '60-70'},
        {'name': 'Wrath of the Lich King', 'keywords': ['Northrend'], 'levels': '70-80'},
        {'name': 'Cataclysm', 'keywords': ['Cataclysm'], 'levels': '80-85'},
        {'name': 'Mists of Pandaria', 'keywords': ['Pandaria'], 'levels': '85-90'},
        {'name': 'Warlords of Draenor', 'keywords': ['Draenor'], 'levels': '90-100'},
        {'name': 'Legion', 'keywords': ['Legion'], 'levels': '100-110'},
        {'name': 'Battle for Azeroth', 'keywords': ['Kul Tiran', 'Zandalari'], 'levels': '110-120'},
        {'name': 'Shadowlands', 'keywords': ['Shadowlands'], 'levels': '120-130'},
        {'name': 'Dragonflight', 'keywords': ['Dragon Isles'], 'levels': '130-140'},
        {'name': 'The War Within', 'keywords': ['Khaz Algar'], 'levels': '140-150'},
    ]
    
    guide = {
        'profession': profession_name,
        'total_recipes': len(recipes),
        'expansions': []
    }
    
    # Process each expansion
    for expansion in expansion_tiers:
        # Find tiers matching this expansion
        matching_tiers = []
        for tier_name in by_tier.keys():
            if any(keyword in tier_name for keyword in expansion['keywords']):
                matching_tiers.append(tier_name)
        
        if not matching_tiers:
            continue
        
        # Combine all recipes from matching tiers
        expansion_recipes = []
        for tier in matching_tiers:
            expansion_recipes.extend(by_tier[tier])
        
        # Sort by estimated cost (cheapest first)
        expansion_recipes.sort(key=lambda r: estimate_material_cost(r['materials']))
        
        # Create expansion guide
        expansion_guide = {
            'expansion': expansion['name'],
            'level_range': expansion['levels'],
            'total_recipes': len(expansion_recipes),
            'recommended_path': []
        }
        
        # Group into level brackets (early, mid, late)
        total = len(expansion_recipes)
        early_tier = expansion_recipes[:min(5, total)]
        mid_tier = expansion_recipes[min(5, total):min(10, total)] if total > 5 else []
        late_tier = expansion_recipes[min(10, total):min(15, total)] if total > 10 else []
        
        # Add early recipes
        if early_tier:
            expansion_guide['recommended_path'].append({
                'phase': 'Early (Start of expansion)',
                'recipes': [
                    {
                        'name': r['name'],
                        'materials': r['materials'],
                        'estimated_cost': estimate_material_cost(r['materials']),
                        'approx_crafts': '10-15'
                    } for r in early_tier
                ]
            })
        
        # Add mid recipes
        if mid_tier:
            expansion_guide['recommended_path'].append({
                'phase': 'Mid (Midway through expansion)',
                'recipes': [
                    {
                        'name': r['name'],
                        'materials': r['materials'],
                        'estimated_cost': estimate_material_cost(r['materials']),
                        'approx_crafts': '10-15'
                    } for r in mid_tier
                ]
            })
        
        # Add late recipes
        if late_tier:
            expansion_guide['recommended_path'].append({
                'phase': 'Late (End of expansion)',
                'recipes': [
                    {
                        'name': r['name'],
                        'materials': r['materials'],
                        'estimated_cost': estimate_material_cost(r['materials']),
                        'approx_crafts': '5-10'
                    } for r in late_tier
                ]
            })
        
        guide['expansions'].append(expansion_guide)
    
    return guide

def main():
    print("=" * 60)
    print("CRAFTING LEVELING GUIDE GENERATOR")
    print("=" * 60)
    
    professions = [
        'Alchemy', 'Blacksmithing', 'Enchanting', 'Engineering',
        'Inscription', 'Jewelcrafting', 'Leatherworking', 'Tailoring', 'Cooking'
    ]
    
    guides = {}
    
    for profession in professions:
        print(f"\n📖 Generating guide for {profession}...")
        guide = generate_leveling_guide(profession)
        
        if guide and guide['total_recipes'] > 0:
            guides[profession] = guide
            expansions = len(guide['expansions'])
            print(f"  ✅ {guide['total_recipes']} recipes across {expansions} expansions")
        else:
            print(f"  ⚠️  No recipes with materials yet")
    
    # Save guides
    if guides:
        output_file = 'crafting_leveling_guides.json'
        with open(output_file, 'w') as f:
            json.dump(guides, f, indent=2)
        
        print(f"\n✅ Saved guides to {output_file}")
        print(f"Generated {len(guides)} profession guides")
    else:
        print("\n⚠️  No guides generated (need more recipe material data)")

if __name__ == "__main__":
    main()
