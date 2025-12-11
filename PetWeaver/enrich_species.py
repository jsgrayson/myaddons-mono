#!/usr/bin/env python3
"""
Enrich all species data from all available sources
"""

import sqlite3
import json
import os

print("📚 Enriching species data from all sources...")

conn = sqlite3.connect('petweaver.db')
cursor = conn.cursor()

# First, add more columns to species table if needed
print("Adding additional species columns...")
try:
    cursor.execute("ALTER TABLE species ADD COLUMN description TEXT")
except:
    pass
try:
    cursor.execute("ALTER TABLE species ADD COLUMN is_capturable BOOLEAN DEFAULT 0")
except:
    pass
try:
    cursor.execute("ALTER TABLE species ADD COLUMN is_unique BOOLEAN DEFAULT 0")
except:
    pass

conn.commit()

# Load species_data.json (843 species with detailed info)
species_enriched = 0
if os.path.exists('species_data.json'):
    with open('species_data.json', 'r') as f:
        species_data = json.load(f)
    
    print(f"Enriching from species_data.json ({len(species_data)} species)...")
    
    for species_id, data in species_data.items():
        cursor.execute('''
            UPDATE species 
            SET pet_type = ?,
                can_battle = ?,
                is_tradable = ?,
                source_text = ?,
                icon = ?,
                description = ?
            WHERE species_id = ?
        ''', (
            data.get('petType', data.get('type')),
            data.get('canBattle', 1),
            data.get('isTradable', 0),
            data.get('source', ''),
            data.get('icon', ''),
            data.get('description', ''),
            int(species_id)
        ))
        species_enriched += 1
    
    conn.commit()
    print(f"✅ Enriched {species_enriched} species from species_data.json")

# Load PetTracker decoded for additional species info
pettracker_enriched = 0
if os.path.exists('pettracker_decoded.json'):
    with open('pettracker_decoded.json', 'r') as f:
        pettracker = json.load(f)
    
    pt_species = pettracker.get('species', {})
    print(f"Enriching from PetTracker ({len(pt_species)} species)...")
    
    for species_id, data in pt_species.items():
        # Only update if we don't already have data
        cursor.execute('SELECT pet_type FROM species WHERE species_id = ?', (int(species_id),))
        result = cursor.fetchone()
        
        if result and result[0] is None:
            cursor.execute('''
                UPDATE species 
                SET pet_type = ?,
                    name = COALESCE(NULLIF(name, ''), ?)
                WHERE species_id = ?
            ''', (
                data.get('type'),
                data.get('name', 'Unknown'),
                int(species_id)
            ))
            pettracker_enriched += 1
    
    conn.commit()
    print(f"✅ Enriched {pettracker_enriched} additional species from PetTracker")

# Show final stats
cursor.execute('''
    SELECT 
        COUNT(*) as total,
        COUNT(pet_type) as have_type,
        COUNT(source_text) as have_source,
        COUNT(icon) as have_icon
    FROM species
''')

stats = cursor.fetchone()
print(f"\n📊 Species Database Summary:")
print(f"  Total Species: {stats[0]}")
print(f"  With Pet Type/Family: {stats[1]} ({stats[1]/stats[0]*100:.1f}%)")
print(f"  With Source Info: {stats[2]} ({stats[2]/stats[0]*100:.1f}%)")
print(f"  With Icon: {stats[3]} ({stats[3]/stats[0]*100:.1f}%)")

# Show sample enriched species
cursor.execute('''
    SELECT species_id, name, pet_type, source_text
    FROM species 
    WHERE pet_type IS NOT NULL AND source_text IS NOT NULL
    LIMIT 5
''')

print(f"\n🔍 Sample Enriched Species:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} (Type {row[2]}) - {row[3][:50]}...")

conn.close()
print("\n✅ Species enrichment complete!")
