#!/usr/bin/env python3
"""
Validate encounters.json to ensure no fake/mock/placeholder data exists.
"""

import json
import re

def validate_encounters():
    """Check encounters.json for fake/incomplete data"""
    
    try:
        with open('encounters_converted.json', 'r') as f:
            encounters = json.load(f)
    except FileNotFoundError:
        print("❌ encounters_converted.json not found!")
        return False
    
    issues = []
    stats = {
        'total_encounters': len(encounters),
        'total_npc_pets': 0,
        'total_abilities': 0,
        'placeholder_names': 0,
        'missing_stats': 0,
        'default_stats': 0,
        'valid_encounters': 0
    }
    
    placeholder_pattern = re.compile(r'^[0-9]+$|^npc pet|^mock|^fake|^placeholder', re.IGNORECASE)
    
    for encounter_id, encounter_data in encounters.items():
        encounter_valid = True
        npc_pets = encounter_data.get('npc_pets', [])
        stats['total_npc_pets'] += len(npc_pets)
        
        for pet_idx, pet in enumerate(npc_pets):
            pet_name = pet.get('name', '')
            
            # Check for placeholder names
            if placeholder_pattern.search(pet_name):
                issues.append(f"{encounter_id}: Pet {pet_idx+1} has placeholder name '{pet_name}'")
                stats['placeholder_names'] += 1
                encounter_valid = False
            
            # Check for missing required fields
            required_fields = ['species_id', 'level', 'health', 'power', 'speed', 'abilities']
            for field in required_fields:
                if field not in pet:
                    issues.append(f"{encounter_id}: Pet '{pet_name}' missing {field}")
                    stats['missing_stats'] += 1
                    encounter_valid = False
            
            # Check for default/placeholder stats
            if pet.get('species_id', 0) < 100:  # Species IDs start around 39
                issues.append(f"{encounter_id}: Pet '{pet_name}' has suspicious species_id {pet.get('species_id')}")
                encounter_valid = False
            
            # Validate abilities
            abilities = pet.get('abilities', [])
            stats['total_abilities'] += len(abilities)
            
            for ab_idx, ability in enumerate(abilities):
                # Check for default power values that might indicate missing data
                if ability.get('power') == 20 and ability.get('accuracy') == 100:
                    stats['default_stats'] += 1
                    # This might be okay for some abilities, so just count
        
        if encounter_valid:
            stats['valid_encounters'] += 1
    
    # Report results
    print("\n" + "="*60)
    print("ENCOUNTER VALIDATION REPORT")
    print("="*60)
    print(f"\nTotal Encounters: {stats['total_encounters']}")
    print(f"Valid Encounters: {stats['valid_encounters']}")
    print(f"Total NPC Pets: {stats['total_npc_pets']}")
    print(f"Total Abilities: {stats['total_abilities']}")
    print(f"\nIssues Found:")
    print(f"  Placeholder Names: {stats['placeholder_names']}")
    print(f"  Missing Stats: {stats['missing_stats']}")
    print(f"  Default Stats (may be valid): {stats['default_stats']}")
    
    if issues:
        print(f"\n⚠️  Found {len(issues)} issues:")
        for issue in issues[:20]:  # Show first 20
            print(f"  - {issue}")
        if len(issues) > 20:
            print(f"  ... and {len(issues) - 20} more")
    
    # Check original encounters.json
    print("\n" + "-"*60)
    print("ORIGINAL encounters.json:")
    try:
        with open('encounters.json', 'r') as f:
            original = json.load(f)
        print(f"  Encounters: {len(original)}")
        print(f"  Size: {len(json.dumps(original)) / 1024:.1f} KB")
    except:
        print("  ❌ Not found or invalid")
    
    print("\nCONVERTED encounters_converted.json:")
    print(f"  Encounters: {stats['total_encounters']}")
    print(f"  Size: {len(json.dumps(encounters)) / 1024:.1f} KB")
    
    # Final verdict
    print("\n" + "="*60)
    if stats['placeholder_names'] == 0 and stats['missing_stats'] == 0:
        print("✅ NO FAKE DATA DETECTED!")
        print("Note: Some abilities use default stats, which may be legitimate.")
    else:
        print("⚠️  ISSUES DETECTED - See above for details")
        print("This is expected for the initial conversion.")
        print("NPC pet data needs to be enriched with real Wowhead/API data.")
    print("="*60 + "\n")
    
    return stats['placeholder_names'] == 0 and stats['missing_stats'] == 0

if __name__ == "__main__":
    validate_encounters()
