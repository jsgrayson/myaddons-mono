#!/usr/bin/env python3
"""
Import ALL WoW pet species from PetTracker data
Then mark which ones you own
"""

import sqlite3
import json

print("📚 Importing complete WoW pet species catalog from PetTracker...")

# Load PetTracker decoded data
with open('pettracker_decoded.json', 'r') as f:
    pettracker = json.load(f)

all_species = pettracker.get('species', {})
print(f"Found {len(all_species)} total WoW pet species in PetTracker")

conn = sqlite3.connect('petweaver.db')
cursor = conn.cursor()

# Import all species from PetTracker
count = 0
for species_id, species_info in all_species.items():
    cursor.execute('''
        INSERT OR IGNORE INTO species (species_id, name, pet_type, can_battle)
        VALUES (?, ?, ?, ?)
    ''', (
        int(species_id),
        species_info.get('name', 'Unknown'),
        species_info.get('type', 1),
        True  # PetTracker only tracks battle pets
    ))
    count += 1

conn.commit()
print(f"✅ Imported {count} pet species from PetTracker")

# Now show ownership stats
cursor.execute('''
    SELECT 
        COUNT(DISTINCT s.species_id) as total_species,
        COUNT(DISTINCT p.species_id) as owned_species,
        COUNT(p.pet_id) as total_owned_pets
    FROM species s
    LEFT JOIN pets p ON s.species_id = p.species_id
''')

stats = cursor.fetchone()
print(f"\n📊 Collection Statistics:")
print(f"  Total WoW Pet Species: {stats[0]}")  
print(f"  Unique Species Owned: {stats[1]}")
print(f"  Total Pet Instances: {stats[2]}")
print(f"  Missing Species: {stats[0] - stats[1]}")
print(f"  Collection %: {(stats[1]/stats[0]*100):.1f}%")

conn.close()
print("\n✅ Species catalog complete!")

stats = cursor.fetchone()
print(f"\n📊 Collection Statistics:")
print(f"  Total WoW Pet Species: {stats[0]}")
print(f"  Unique Species Owned: {stats[1]}")
print(f"  Total Pet Instances: {stats[2]}")
print(f"  Missing Species: {stats[0] - stats[1]}")

conn.close()
print("\n✅ Species catalog complete!")
