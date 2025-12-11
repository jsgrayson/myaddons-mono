"""
Check Ability Coverage

Checks if species used in pettracker_tamers.json are present in abilities.json.
"""

import json

def main():
    # Load Tamers
    try:
        with open('pettracker_tamers.json', 'r') as f:
            tamers = json.load(f)
    except FileNotFoundError:
        print("pettracker_tamers.json not found")
        return

    # Load Abilities
    try:
        with open('abilities.json', 'r') as f:
            ab_data = json.load(f)
            species_abilities = ab_data.get('species_abilities', {})
    except FileNotFoundError:
        print("abilities.json not found")
        return

    # Collect Tamer Species
    tamer_species = set()
    for tamer in tamers:
        for pet in tamer['team']:
            tamer_species.add(str(pet['species_id']))
            
    print(f"Tamers use {len(tamer_species)} unique species")
    
    # Check Coverage and Group by Model
    missing = []
    missing_models = {} # model_id -> [species_ids]
    
    # Create a lookup for species -> model from tamers
    species_to_model = {}
    for tamer in tamers:
        for pet in tamer['team']:
            species_to_model[str(pet['species_id'])] = pet['model']

    for sid in tamer_species:
        if sid not in species_abilities:
            missing.append(sid)
            mid = species_to_model.get(sid)
            if mid:
                if mid not in missing_models:
                    missing_models[mid] = []
                missing_models[mid].append(sid)
            
    print(f"Missing species in abilities.json: {len(missing)}")
    print(f"Unique Model IDs for missing species: {len(missing_models)}")
    
    # Print top models
    print("\nTop Missing Models:")
    for mid, sids in list(missing_models.items())[:20]:
        print(f"Model {mid}: {len(sids)} species (e.g. {sids[0]})")

if __name__ == "__main__":
    main()
