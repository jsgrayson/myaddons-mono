import json

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

encounters = load_json('encounters.json')
abilities = load_json('abilities.json').get('abilities', {})

print("--- INSPECTING CAPTAIN KLUTZ ---")

# Find Klutz
klutz_data = None
if isinstance(encounters, list):
    for e in encounters:
        if "Klutz" in e.get('name', ''):
            klutz_data = e
            break
elif isinstance(encounters, dict):
    # Handle dict structure
    for k1, v1 in encounters.items():
        if isinstance(v1, list):
             for e in v1:
                 if "Klutz" in e.get('name', ''):
                     klutz_data = e; break
        if klutz_data: break
        if isinstance(v1, dict):
             for k2, v2 in v1.items():
                 if isinstance(v2, list):
                     for e in v2:
                         if "Klutz" in e.get('name', ''):
                             klutz_data = e; break
        if klutz_data: break

if not klutz_data:
    print("ERROR: Captain Klutz not found in encounters.json!")
    exit()

print(f"Found: {klutz_data['name']}")
pets = klutz_data.get('pets') or klutz_data.get('npc_pets') or []

for i, pet in enumerate(pets):
    print(f"\nPet {i+1}: {pet.get('name', 'Unknown')}")
    ab_list = pet.get('abilities', [])
    print(f"  Raw Abilities: {ab_list}")
    
    for ab in ab_list:
        ab_id = str(ab['id']) if isinstance(ab, dict) else str(ab)
        ab_info = abilities.get(ab_id)
        
        if ab_info:
            print(f"    - ID {ab_id}: {ab_info.get('name')} (CD: {ab_info.get('cooldown', 0)})")
        else:
            print(f"    - ID {ab_id}: [MISSING IN DB]")
