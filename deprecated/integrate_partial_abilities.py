# integrate_partial_abilities.py
"""
Integrate partial tamer ability data from CSV into encounters_full.json.
The CSV has: Tamer Name, Pet Name, Species ID, Slot 1, Slot 2, Slot 3
Each pet has 6 abilities total (2 per slot), but we only have the first ability of each slot.
"""
import json
import csv

# Load existing data
with open('encounters_full.json', 'r', encoding='utf-8') as f:
    encounters = json.load(f)

with open('abilities.json', 'r', encoding='utf-8') as f:
    abilities_data = json.load(f)
    abilities_by_name = {v['name'].lower(): v for v in abilities_data.get('abilities', {}).values()}

# Parse CSV data
csv_data = """Tamer Name,Pet Name,Species ID,Slot 1 Ability,Slot 2 Ability,Slot 3 Ability
Major Payne,Grizzle,979,Bash,Hibernate,Rampage
,Beakmaster X-225,978,Batter,Shock and Awe,Wind-Up
,Bloom,977,Lash,Soothing Mists,Entangling Roots
Burning Pandaren Spirit,Pandaren Fire Spirit,1155,Immolate,Conflagrate,Cauterize
,Glowy,1147,Swarm,Confusing Sting,Glowing Toxin
,Crimson,1137,Breath,Cyclone,Lift-Off
Flowing Pandaren Spirit,Pandaren Water Spirit,1154,Water Jet,Whirlpool,Geyser
,Marley,1148,Water Jet,Healing Wave,Tidal Wave
Lorewalker Cho,Wisdom,1285,Arcane Blast,Arcane Storm,Evanescence
,Knowledge,1286,Amplify Magic,Surge of Power,Mana Surge
,Patience,1287,Flank,Dodge,Comeback"""

# Build species -> abilities mapping from CSV
species_abilities = {}
current_tamer = None

for line in csv_data.strip().split('\n')[1:]:  # Skip header
    parts = [p.strip() for p in line.split(',')]
    if len(parts) >= 6:
        tamer_name = parts[0] if parts[0] else current_tamer
        species_id = int(parts[2])
        ability_names = [parts[3], parts[4], parts[5]]
        
        # Look up ability objects by name
        ability_objs = []
        for name in ability_names:
            name_lower = name.lower()
            if name_lower in abilities_by_name:
                ability_objs.append(abilities_by_name[name_lower])
            else:
                print(f"⚠️ Ability '{name}' not found in abilities.json")
        
        species_abilities[species_id] = ability_objs
        current_tamer = tamer_name

# Update encounters_full.json
updated_count = 0
for tamer in encounters:
    for pet in tamer['pets']:
        species_id = pet['species_id']
        if species_id in species_abilities:
            pet['abilities'] = species_abilities[species_id]
            pet['missing_abilities'] = False
            updated_count += 1

# Save updated file
with open('encounters_full.json', 'w', encoding='utf-8') as f:
    json.dump(encounters, f, indent=2, ensure_ascii=False)

print(f"✅ Updated {updated_count} pets with abilities from CSV")
print(f"📊 Coverage: {updated_count}/305 pets now have abilities")

# Show which species were updated
print(f"\nUpdated species IDs: {sorted(species_abilities.keys())}")
