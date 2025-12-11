"""
Convert Tamers to Encounters

Combines:
1. pettracker_tamers.json (Tamer Teams)
2. pettracker_decoded.json (Species Abilities & Base Stats)
3. species_data.json (Family info - optional)

Generates:
encounters.json (Format for Genetic Algorithm)
"""

import json
import math

def calculate_stats(base_stats, level, quality, breed_id=3):
    """
    Calculate battle pet stats.
    Formula approximation:
    Health = (Base + BreedMult) * Level * QualityMult + 100
    Power = (Base + BreedMult) * Level * QualityMult
    Speed = (Base + BreedMult) * Level * QualityMult
    
    Quality Multipliers:
    Poor: 1.0? Common: 1.1? Uncommon: 1.2? Rare: 1.3?
    Actually, standard multipliers are:
    Poor: 1.0, Common: 1.1, Uncommon: 1.2, Rare: 1.3, Epic: 1.4, Legendary: 1.5
    
    PetTracker Quality in Tamer data seems to be 1-based?
    Julia Stevens (L2) has Quality 2 (Uncommon).
    Major Payne (L25) has Quality 4 (Rare).
    """
    if not base_stats:
        return {'health': 1000, 'power': 200, 'speed': 200}
        
    # Quality Multiplier
    # 0: Poor (1.0), 1: Common (1.1), 2: Uncommon (1.2), 3: Rare (1.3), 4: Epic (1.4)?
    # Wait, in Tamer data: 2=Uncommon, 4=Rare.
    # So 1=Common? 0=Poor?
    # Let's map it:
    q_mults = {0: 1.0, 1: 1.1, 2: 1.2, 3: 1.3, 4: 1.4, 5: 1.5}
    q_mult = q_mults.get(quality, 1.0)
    
    # Breed Multiplier
    # Tamers usually use a specific breed, often B/B (Balance) which adds 0.5 to all.
    # Or they have custom stats.
    # For now, assume B/B (Breed 3) -> +0.5 to all base stats?
    # Actually, base stats in PetTracker are usually the "Base" values (e.g. 8).
    # Real stat = (Base + BreedVal) * Level * Quality * 5?
    # No, the formula is complex.
    # Let's use a simplified linear approximation that fits L25 Rare values (~1400/280/280).
    # L25 Rare (Q=1.3)
    # 280 = (8 + X) * 25 * 1.3 ...
    
    # Let's use the standard formula from WarcraftPets/Wowpedia if possible.
    # HP = (Base + Breed) * Level * Quality * 5 + 100
    # Power = (Base + Breed) * Level * Quality
    # Speed = (Base + Breed) * Level * Quality
    
    # But PetTracker Base Stats are like 8, 8, 8.
    # If Base=8, Breed=0.5 (B/B), Level=25, Quality=1.3 (Rare)
    # Power = (8 + 0.5) * 25 * 1.3 = 8.5 * 32.5 = 276.25 -> 276. Close to 280.
    # HP = (8 + 0.5) * 25 * 1.3 * 5 + 100 = 276.25 * 5 + 100 = 1381 + 100 = 1481. Close to 1400-1500.
    
    # This seems close enough for simulation purposes.
    
    # Breed adjustment:
    # Most wild pets are random breeds. Tamers are fixed.
    # Without breed data for tamers, assume B/B (+0.5 to all).
    breed_add = 0.5
    
    # Level adjustment
    # Tamer pets can be any level.
    
    hp = (base_stats['health'] + breed_add) * level * q_mult * 5 + 100
    power = (base_stats['power'] + breed_add) * level * q_mult
    speed = (base_stats['speed'] + breed_add) * level * q_mult
    
    return {
        'health': int(hp),
        'power': int(power),
        'speed': int(speed)
    }

def main():
    # Load Data
    try:
        with open('pettracker_tamers.json', 'r') as f:
            tamers = json.load(f)
        with open('pettracker_decoded.json', 'r') as f:
            pt_data = json.load(f)
            raw_species = pt_data.get('species', {})
            print(f"DEBUG: raw_species count (maps): {len(raw_species)}")
            
            # Flatten species_abilities: MapID -> SpeciesID -> Abilities  ==>  SpeciesID -> Abilities
            species_abilities = {}
            for map_id, species_list in raw_species.items():
                for sid, abilities in species_list.items():
                    species_abilities[str(sid)] = abilities
            
            base_stats = pt_data.get('stats', {})
        
        # Load ability details for names (optional, but good for debugging)
        ability_names = {}
        try:
            with open('abilities.json', 'r') as f:
                ab_data = json.load(f)
                for aid, data in ab_data.get('abilities', {}).items():
                    ability_names[int(aid)] = data.get('name', f"Ability {aid}")
        except:
            pass
            
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return

    encounters = {}
    
    for tamer in tamers:
        tamer_name = tamer['name']
        tamer_id = str(tamer['id'])
        
        npc_pets = []
        
        for pet in tamer['team']:
            sid = str(pet['species_id'])
            # print(f"Processing SID: {sid}") # Commented out to avoid spam, but maybe I should enable it for a few
            if sid == "872":
                 print(f"DEBUG: Found 872! In dict: {sid in species_abilities}")
                 if not sid in species_abilities:
                     print(f"DEBUG: Keys containing 872: {[k for k in species_abilities.keys() if '872' in k]}")
            # Use PetTracker decoded abilities
            abilities = []
            if sid in species_abilities:
                slots = species_abilities[sid]
                # Actually, species have 6 abilities (3 slots, 2 options each).
                # Slots 1, 2, 3 are the first choice. Slots 4, 5, 6 are the second choice.
                # Let's default to slots 1, 2, 3 (IDs at index 0, 1, 2 if we flattened it, or keys "1", "2", "3")
                
                # Flatten slots
                # species_abilities[sid] can be:
                # Dict: {"1": [id], "2": [id]...} (keys might be strings or ints)
                # List: [[id], [id]...] (if it was parsed as a list)
                
                if sid == "872":
                    print(f"DEBUG: Species 872 slots: {slots} (Type: {type(slots)})")
                
                active_ids = []
                
                if isinstance(slots, dict):
                    # Try keys "1", "2", "3" (standard slots)
                    # Also try 1, 2, 3 (int keys)
                    # Also try "0", "1", "2" (0-indexed)
                    for i in range(1, 4):
                        # Try various key formats
                        candidates = [str(i), i, str(i-1), i-1]
                        found = False
                        for key in candidates:
                            if key in slots and slots[key]:
                                # slots[key] should be a list of IDs
                                val = slots[key]
                                if isinstance(val, list) and len(val) > 0:
                                    active_ids.append(val[0])
                                    found = True
                                    break
                        if not found:
                            active_ids.append(0)
                            
                elif isinstance(slots, list):
                    # List of slots
                    # Usually 0-indexed: [slot1_ids, slot2_ids, slot3_ids...]
                    for i in range(3):
                        if i < len(slots) and slots[i]:
                            val = slots[i]
                            if isinstance(val, list) and len(val) > 0:
                                active_ids.append(val[0])
                            elif isinstance(val, int):
                                # Maybe it's just a list of IDs directly? [id1, id2, id3]
                                active_ids.append(val)
                            else:
                                active_ids.append(0)
                        else:
                            active_ids.append(0)
                
                for aid in active_ids:
                    if aid > 0:
                        abilities.append({
                            "id": aid,
                            "name": ability_names.get(aid, f"Ability {aid}"),
                            "power": 20, # Default, will be overridden by real data in app
                            "accuracy": 100,
                            "speed": 0,
                            "cooldown": 0
                        })
            
            # Get Stats
            stats = {'health': 1000, 'power': 200, 'speed': 200}
            if sid in base_stats:
                stats = calculate_stats(base_stats[sid], pet['level'], pet['quality'])
            
            # Quality Name
            q_names = {1: "common", 2: "uncommon", 3: "rare", 4: "epic", 5: "legendary"}
            quality_name = q_names.get(pet['quality'], "rare")
            
            npc_pets.append({
                "species_id": pet['species_id'],
                "name": pet['name'],
                "family": "Beast", # Placeholder, need family data
                "quality": quality_name,
                "health": stats['health'],
                "power": stats['power'],
                "speed": stats['speed'],
                "abilities": abilities
            })
            
        # Create Encounter Entry
        # Key by name (slugified) or ID? App uses name (e.g. 'squirt')
        slug = tamer_name.lower().replace(" ", "-").replace("'", "")
        
        encounters[slug] = {
            "id": tamer['id'],
            "name": tamer_name,
            "npc_pets": npc_pets,
            "strategy": "default"
        }
        
    # Save encounters.json
    with open('encounters.json', 'w') as f:
        json.dump(encounters, f, indent=2)
        
    print(f"Generated {len(encounters)} encounters in encounters.json")

if __name__ == "__main__":
    main()
