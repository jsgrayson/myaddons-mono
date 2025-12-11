"""
Convert extracted team data to pet_slots format for the matcher.
Also build the full-scale scraper for all expansions.
"""

import json
from collections import defaultdict

def teams_to_slots(teams):
    """
    Convert list of full teams into pet_slots format.
    Each slot contains all pets that appeared in that position.
    """
    if not teams:
        return []
    
    slot1, slot2, slot3 = set(), set(), set()
    
    for team in teams:
        if len(team) >= 3:
            # Add each pet to its respective slot (using tuple for set compatibility)
            pet1, pet2, pet3 = team[0], team[1], team[2]
            slot1.add((pet1['name'], pet1['id']))
            slot2.add((pet2['name'], pet2['id']))
            slot3.add((pet3['name'], pet3['id']))
    
    # Convert sets back to list of pet dicts, filtering out [Unknown] with id=0
    return [
        [{'name': name, 'id': pid} for name, pid in slot1 if pid != 0 or name == '[Empty/Leveling]'],
        [{'name': name, 'id': pid} for name, pid in slot2 if pid != 0 or name == '[Empty/Leveling]'],
        [{'name': name, 'id': pid} for name, pid in slot3 if pid != 0 or name == '[Empty/Leveling]']
    ]

# Test with TWW data
with open('tww_test_fast.json', 'r') as f:
    tww_data = json.load(f)

# Convert and save
for enc in tww_data['encounters']:
    enc['pet_slots'] = teams_to_slots(enc['teams'])
    # Keep teams for reference but mark as raw data
    enc['teams_raw'] = enc['teams']
    del enc['teams']

with open('tww_test_converted.json', 'w') as f:
    json.dump(tww_data, f, indent=2)

print("Converted TWW data to pet_slots format")
print("\nSample:")
sample = tww_data['encounters'][0]
print(f"{sample['encounter_name']}: {sample['team_count']} teams")
for i, slot in enumerate(sample['pet_slots'], 1):
    print(f"  Slot {i}: {len(slot)} alternatives")
    if slot:
        print(f"    First few: {[p['name'] for p in slot[:3]]}")
