#!/usr/bin/env python3
"""
Import all ability data into the database
"""

import sqlite3
import json
import os

print("📚 Importing WoW Pet Abilities...")

conn = sqlite3.connect('petweaver.db')
cursor = conn.cursor()

# Import abilities from abilities.json
if os.path.exists('abilities.json'):
    with open('abilities.json', 'r') as f:
        data = json.load(f)
    
    # abilities.json has {"abilities": {...}, "species_abilities": {...}}
    abilities = data.get('abilities', {})
    species_abilities_map = data.get('species_abilities', {})
    
    print(f"Found {len(abilities)} abilities to import")
    
    count = 0
    for ability_id, ability_data in abilities.items():
        cursor.execute('''
            INSERT OR REPLACE INTO abilities 
            (ability_id, name, cooldown, rounds, family_id, power, accuracy, speed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            int(ability_id),
            ability_data.get('name', 'Unknown'),
            ability_data.get('cooldown', 0),
            ability_data.get('rounds', 1),
            ability_data.get('family_id', 0),
            ability_data.get('power', 0),
            ability_data.get('accuracy', 100),
            ability_data.get('speed', 0)
        ))
        count += 1
    
    conn.commit()
    print(f"✅ Imported {count} abilities")
    
    # Import species-ability mappings
    print(f"Found {len(species_abilities_map)} species with ability mappings")
    mapping_count = 0
    for species_id, ability_list in species_abilities_map.items():
        for slot, ability_id in enumerate(ability_list, start=1):
            if ability_id:
                cursor.execute('''
                    INSERT OR IGNORE INTO species_abilities (species_id, ability_id, slot)
                    VALUES (?, ?, ?)
                ''', (int(species_id), int(ability_id), slot))
                mapping_count += 1
    
    conn.commit()
    print(f"✅ Created {mapping_count} species-ability mappings")
else:
    print("⚠️  abilities.json not found")

# Show summary
cursor.execute("SELECT COUNT(*) FROM abilities")
total_abilities = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT species_id) FROM species_abilities")
species_with_abilities = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM species_abilities")
total_mappings = cursor.fetchone()[0]

print(f"\n📊 Database Summary:")
print(f"  Total Abilities: {total_abilities}")
print(f"  Species with Abilities: {species_with_abilities}")
print(f"  Total Ability Mappings: {total_mappings}")

conn.close()
print("\n✅ Ability import complete!")
