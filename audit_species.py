
import json
import os

def audit_species():
    print("=== Auditing Species Data ===")
    
    if not os.path.exists('species_data.json'):
        print("ERROR: species_data.json not found!")
        return
        
    with open('species_data.json', 'r') as f:
        species_data = json.load(f)
        
    print(f"Total Species: {len(species_data)}")
    
    missing_stats = []
    missing_abilities = []
    
    # Also check PetTracker data if available
    pt_stats = {}
    if os.path.exists('pettracker_decoded.json'):
        with open('pettracker_decoded.json', 'r') as f:
            pt = json.load(f)
            pt_stats = pt.get('stats', {})
            
    for sid, data in species_data.items():
        name = data.get('name', 'Unknown')
        
        # Check Stats
        # species_data might not have stats directly?
        # app.py loads stats from my_pets.json or PetTracker.
        # But species_data.json usually has display info.
        
        # Check Abilities
        # app.py loads abilities from abilities.json (species_abilities)
        pass

    # Let's check abilities.json for species coverage
    if os.path.exists('abilities.json'):
        with open('abilities.json', 'r') as f:
            ab_data = json.load(f)
            species_abilities = ab_data.get('species_abilities', {})
            
        print(f"Species with Ability Data: {len(species_abilities)}")
        
        # Check for species in species_data but missing abilities
        for sid in species_data:
            if sid not in species_abilities:
                missing_abilities.append(f"{sid} ({species_data[sid].get('name')})")
                
    if missing_abilities:
        print(f"\n[WARNING] {len(missing_abilities)} species missing ability data:")
        for s in missing_abilities[:10]:
            print(f"  - {s}")
    else:
        print("\n[OK] All species have ability data.")
        
    # Check PetTracker coverage
    if pt_stats:
        print(f"\nPetTracker Stats Coverage: {len(pt_stats)} species")
        
        # Check overlap
        missing_pt = []
        for sid in species_data:
            if sid not in pt_stats:
                missing_pt.append(f"{sid} ({species_data[sid].get('name')})")
                
        if missing_pt:
            print(f"[INFO] {len(missing_pt)} species missing PetTracker stats (might rely on defaults):")
            # print(f"IDs: {missing_pt[:5]}...")
        else:
            print("[OK] All species have PetTracker stats.")

if __name__ == "__main__":
    audit_species()
