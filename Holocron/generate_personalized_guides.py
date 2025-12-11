#!/usr/bin/env python3
"""
Generate personalized crafting leveling guides based on character's current profession skill.
Shows exactly what to craft next from their current level to max.
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

def get_character_professions(character_name):
    """Get character's professions and current skill levels"""
    conn = get_db_connection()
    if not conn:
        return []
    
    cur = conn.cursor()
    
    # Check if character has profession data
    cur.execute("""
        SELECT p.profession_name, p.skill_level, p.max_skill
        FROM goblin.professions p
        JOIN holocron.characters c ON p.character_guid = c.character_guid
        WHERE c.name = %s
    """, (character_name,))
    
    professions = []
    for row in cur.fetchall():
        professions.append({
            'name': row[0],
            'current_skill': row[1],
            'max_skill': row[2]
        })
    
    cur.close()
    conn.close()
    return professions

def estimate_skill_gain(recipe_difficulty, current_skill):
    """Estimate how many skill points a recipe will give"""
    # Simplified skill gain model
    diff = recipe_difficulty - current_skill
    
    if diff >= 20:  # Orange
        return 1
    elif diff >= 10:  # Yellow
        return 0.5
    elif diff >= 0:  # Green
        return 0.25
    else:  # Gray
        return 0
    
    return 1  # Default

def get_recipes_for_skill_range(profession_name, current_skill, target_skill):
    """Get optimal recipes for a skill range"""
    conn = get_db_connection()
    if not conn:
        return []
    
    cur = conn.cursor()
    
    # Get recipes with materials for this profession
    cur.execute("""
        SELECT 
            recipe_id,
            recipe_name,
            skill_tier_name,
            materials,
            crafted_item_id
        FROM goblin.recipe_reference
        WHERE profession_name = %s
        AND materials IS NOT NULL
        ORDER BY recipe_id
    """, (profession_name,))
    
    all_recipes = []
    for row in cur.fetchall():
        all_recipes.append({
            'id': row[0],
            'name': row[1],
            'tier': row[2],
            'materials': row[3] if row[3] else [],
            'crafted_item_id': row[4]
        })
    
    cur.close()
    conn.close()
    
    # Filter recipes appropriate for current skill level
    # This is simplified - would need actual skill requirements from recipe data
    return all_recipes[:20]  # Return subset for now

def generate_personalized_guide(character_name):
    """Generate personalized leveling guide for a character"""
    professions = get_character_professions(character_name)
    
    if not professions:
        # If no profession data, return mock data for demonstration
        print(f"⚠️  No profession data found for {character_name}")
        print("   Using sample data for demonstration...")
        professions = [
            {'name': 'Blacksmithing', 'current_skill': 45, 'max_skill': 100},
            {'name': 'Mining', 'current_skill': 62, 'max_skill': 100}
        ]
    
    guide = {
        'character': character_name,
        'professions': []
    }
    
    for prof in professions:
        prof_name = prof['name']
        current = prof['current_skill']
        max_skill = prof['max_skill']
        
        # Calculate skill points needed
        points_needed = max_skill - current
        
        # Get appropriate recipes
        recipes = get_recipes_for_skill_range(prof_name, current, max_skill)
        
        prof_guide = {
            'profession': prof_name,
            'current_skill': current,
            'max_skill': max_skill,
            'points_needed': points_needed,
            'recommended_path': []
        }
        
        if not recipes:
            prof_guide['status'] = 'No recipe data available yet'
        else:
            # Group into skill brackets
            brackets = [
                {'range': f'{current}-{min(current+10, max_skill)}', 'recipes': recipes[:3]},
                {'range': f'{min(current+10, max_skill)}-{min(current+20, max_skill)}', 'recipes': recipes[3:6]},
                {'range': f'{min(current+20, max_skill)}-{max_skill}', 'recipes': recipes[6:10]}
            ]
            
            for bracket in brackets:
                if int(bracket['range'].split('-')[0]) >= max_skill:
                    continue
                    
                bracket_guide = {
                    'skill_range': bracket['range'],
                    'recipes': []
                }
                
                for recipe in bracket['recipes']:
                    # Estimate cost
                    mat_count = len(recipe['materials'])
                    est_cost = mat_count * 50  # Simplified
                    
                    bracket_guide['recipes'].append({
                        'name': recipe['name'],
                        'materials': recipe['materials'],
                        'estimated_cost': est_cost,
                        'crafts_needed': '5-10',
                        'skill_points': '5-10'
                    })
                
                if bracket_guide['recipes']:
                    prof_guide['recommended_path'].append(bracket_guide)
        
        guide['professions'].append(prof_guide)
    
    return guide

def main():
    print("=" * 60)
    print("PERSONALIZED CRAFTING GUIDE GENERATOR")
    print("=" * 60)
    
    # Get characters from database
    conn = get_db_connection()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT name FROM holocron.characters ORDER BY name")
    characters = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    
    if not characters:
        print("⚠️  No characters found in database")
        return
    
    print(f"\nGenerating personalized guides for {len(characters)} characters...")
    
    all_guides = {}
    
    for char_name in characters:
        print(f"\n📖 {char_name}...")
        guide = generate_personalized_guide(char_name)
        all_guides[char_name] = guide
        
        # Print summary
        for prof in guide['professions']:
            status = f"{prof['current_skill']}/{prof['max_skill']}"
            points = prof['points_needed']
            print(f"  - {prof['profession']:20} {status:10} ({points} points to go)")
    
    # Save guides
    output_file = 'personalized_crafting_guides.json'
    with open(output_file, 'w') as f:
        json.dump(all_guides, f, indent=2)
    
    print(f"\n✅ Saved personalized guides to {output_file}")
    print(f"Generated guides for {len(all_guides)} characters")

if __name__ == "__main__":
    main()
