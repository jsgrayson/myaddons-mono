#!/usr/bin/env python3
"""
Import encounters and enemy team data into SQL
Includes special encounter mechanics and leveling info
"""

import sqlite3
import json
import os

print("📚 Importing encounters and enemy team data...")

conn = sqlite3.connect('petweaver.db')
cursor = conn.cursor()

# Import encounters
if os.path.exists('encounters_complete.json'):
    with open('encounters_complete.json', 'r') as f:
        encounters = json.load(f)
    
    print(f"Found {len(encounters)} encounters to import")
    
    count = 0
    for enc_id, enc_data in encounters.items():
        # Extract enemy pets (note: npc_pets, not enemies)
        enemies = enc_data.get('npc_pets', [])
        
        # Convert string ID to integer hash for database
        enc_id_int = hash(enc_id) % (10**9)  # Keep it reasonable size
        
        cursor.execute('''
            INSERT OR REPLACE INTO encounters 
            (encounter_id, name, expansion, category, is_daily, is_weekly,
             npc1_name, npc1_species, npc1_level, npc1_quality,
             npc2_name, npc2_species, npc2_level, npc2_quality,
             npc3_name, npc3_species, npc3_level, npc3_quality,
             special_mechanics, leveling_encounter, npc_name, zone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            enc_id_int,
            enc_data.get('name', 'Unknown'),
            enc_data.get('expansion', 'Unknown'),
            'Tamer',  # Default category
            False,  # is_daily
            False,  # is_weekly
            f"{enc_data.get('name', 'Unknown')} Pet 1" if len(enemies) > 0 else None,
            enemies[0].get('species_id') if len(enemies) > 0 else None,
            enemies[0].get('level', 25) if len(enemies) > 0 else None,
            4,  # Default rare quality
            f"{enc_data.get('name', 'Unknown')} Pet 2" if len(enemies) > 1 else None,
            enemies[1].get('species_id') if len(enemies) > 1 else None,
            enemies[1].get('level', 25) if len(enemies) > 1 else None,
            4,
            f"{enc_data.get('name', 'Unknown')} Pet 3" if len(enemies) > 2 else None,
            enemies[2].get('species_id') if len(enemies) > 2 else None,
            enemies[2].get('level', 25) if len(enemies) > 2 else None,
            4,
            '{}',  # Empty special mechanics for now
            True if enemies and any(e.get('level', 25) < 25 for e in enemies) else False,  # Leveling encounter if any pet < 25
            enc_data.get('name', 'Unknown'),
            enc_data.get('location', 'Unknown')
        ))
        count += 1
    
    conn.commit()
    print(f"✅ Imported {count} encounters")
else:
    print("⚠️  encounters_complete.json not found")

# Show final stats
cursor.execute("SELECT COUNT(*) FROM encounters")
total_encounters = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM strategies")
total_strategies = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM ready_strategies")
total_ready = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT encounter_id) FROM strategies")
encounters_with_strats = cursor.fetchone()[0]

print(f"\n📊 Database Summary:")
print(f"  Total Encounters: {total_encounters}")
print(f"  Total Strategies: {total_strategies}")
print(f"  Ready Strategies: {total_ready}")
print(f"  Encounters with Strategies: {encounters_with_strats}")

# Show some examples
cursor.execute('''
    SELECT name, expansion, category, 
           npc1_name, npc2_name, npc3_name,
           special_mechanics, leveling_encounter
    FROM encounters 
    WHERE leveling_encounter = 1
    LIMIT 5
''')

print(f"\n🎓 Leveling Encounters:")
for row in cursor.fetchall():
    print(f"  - {row[0]} ({row[1]}): {row[3]}, {row[4]}, {row[5]}")
    if row[6] and row[6] != '{}':
        print(f"    Special: {row[6]}")

conn.close()
print("\n✅ Import complete!")
