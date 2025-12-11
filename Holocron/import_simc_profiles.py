#!/usr/bin/env python3
"""
Import SimulationCraft APLs (Action Priority Lists) for SkillWeaver.
Fetches profiles from the official SimulationCraft GitHub repository.
"""

import os
import requests
import psycopg2
import re

# SimulationCraft GitHub Base URL (The War Within / Tier 31)
# Using 'thewarwithin' branch if available, or 'dragonflight' as fallback
# Actually, TWW is usually 'main' or a specific expansion branch.
# Let's try 'thewarwithin' branch first, or check 'main'.
# Common path: profiles/Tier31/
BASE_URL = "https://raw.githubusercontent.com/simulationcraft/simc/thewarwithin/profiles/Tier31/"
GITHUB_API_URL = "https://api.github.com/repos/simulationcraft/simc/contents/profiles/Tier31?ref=thewarwithin"

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://jgrayson@localhost/holocron')

# Class ID Mapping (Standard WoW IDs)
CLASS_IDS = {
    'Warrior': 1, 'Paladin': 2, 'Hunter': 3, 'Rogue': 4, 'Priest': 5,
    'DeathKnight': 6, 'Shaman': 7, 'Mage': 8, 'Warlock': 9, 'Monk': 10,
    'Druid': 11, 'DemonHunter': 12, 'Evoker': 13
}

# Spec ID Mapping (Simplified - would ideally query DB or API)
# This is a partial list for mapping filenames to IDs
SPEC_IDS = {
    # Mage
    'Mage_Arcane': 62, 'Mage_Fire': 63, 'Mage_Frost': 64,
    # Warrior
    'Warrior_Arms': 71, 'Warrior_Fury': 72, 'Warrior_Protection': 73,
    # Rogue
    'Rogue_Assassination': 259, 'Rogue_Outlaw': 260, 'Rogue_Subtlety': 261,
    # Priest
    'Priest_Discipline': 256, 'Priest_Holy': 257, 'Priest_Shadow': 258,
    # Druid
    'Druid_Balance': 102, 'Druid_Feral': 103, 'Druid_Guardian': 104, 'Druid_Restoration': 105,
    # Paladin
    'Paladin_Holy': 65, 'Paladin_Protection': 66, 'Paladin_Retribution': 70,
    # Hunter
    'Hunter_BeastMastery': 253, 'Hunter_Marksmanship': 254, 'Hunter_Survival': 255,
    # Shaman
    'Shaman_Elemental': 262, 'Shaman_Enhancement': 263, 'Shaman_Restoration': 264,
    # Warlock
    'Warlock_Affliction': 265, 'Warlock_Demonology': 266, 'Warlock_Destruction': 267,
    # Monk
    'Monk_Brewmaster': 268, 'Monk_Windwalker': 269, 'Monk_Mistweaver': 270,
    # Demon Hunter
    'DemonHunter_Havoc': 577, 'DemonHunter_Vengeance': 581,
    # Death Knight
    'DeathKnight_Blood': 250, 'DeathKnight_Frost': 251, 'DeathKnight_Unholy': 252,
    # Evoker
    'Evoker_Devastation': 1467, 'Evoker_Preservation': 1468, 'Evoker_Augmentation': 1473
}

def get_db_connection():
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def fetch_profile_list():
    """Get list of .simc files from GitHub API"""
    print(f"🔍 Fetching profile list from: {GITHUB_API_URL}")
    try:
        response = requests.get(GITHUB_API_URL)
        if response.status_code == 404:
            print("⚠️  Branch 'thewarwithin' not found, trying 'dragonflight'...")
            fallback_url = "https://api.github.com/repos/simulationcraft/simc/contents/profiles/Tier31?ref=dragonflight"
            response = requests.get(fallback_url)
            
        response.raise_for_status()
        files = response.json()
        
        simc_files = [f['name'] for f in files if f['name'].endswith('.simc')]
        print(f"✅ Found {len(simc_files)} profiles")
        return simc_files
    except Exception as e:
        print(f"❌ Error fetching profile list: {e}")
        return []

def parse_filename(filename):
    """
    Parse filename to extract Class and Spec.
    Format: T31_Mage_Frost.simc or T31_Demon_Hunter_Havoc.simc
    """
    # Remove extension and prefix
    name = filename.replace('.simc', '')
    # Remove T31_ prefix if present
    name = re.sub(r'^T\d+_', '', name)
    
    # Handle special cases like Demon Hunter
    if name.startswith('Demon_Hunter'):
        cls_name = 'DemonHunter'
        spec_part = name.replace('Demon_Hunter_', '')
    elif name.startswith('Death_Knight'):
        cls_name = 'DeathKnight'
        spec_part = name.replace('Death_Knight_', '')
    else:
        parts = name.split('_')
        cls_name = parts[0]
        spec_part = ''.join(parts[1:])
        
    # Construct lookup key
    lookup_key = f"{cls_name}_{spec_part}"
    
    # Try to find IDs
    class_id = CLASS_IDS.get(cls_name)
    spec_id = SPEC_IDS.get(lookup_key)
    
    return class_id, spec_id, lookup_key

def import_profiles():
    """Main import function"""
    files = fetch_profile_list()
    if not files:
        return

    conn = get_db_connection()
    if not conn:
        return
    cur = conn.cursor()
    
    imported_count = 0
    
    for filename in files:
        class_id, spec_id, lookup_key = parse_filename(filename)
        
        if not class_id or not spec_id:
            print(f"⚠️  Skipping {filename}: Could not map to Class/Spec ID ({lookup_key})")
            continue
            
        # Download content
        # Construct raw URL (need to know which branch worked)
        # For simplicity, let's try thewarwithin then dragonflight
        raw_url = f"https://raw.githubusercontent.com/simulationcraft/simc/thewarwithin/profiles/Tier31/{filename}"
        
        try:
            res = requests.get(raw_url)
            if res.status_code == 404:
                raw_url = f"https://raw.githubusercontent.com/simulationcraft/simc/dragonflight/profiles/Tier31/{filename}"
                res = requests.get(raw_url)
            
            if res.status_code != 200:
                print(f"❌ Failed to download {filename}")
                continue
                
            content = res.text
            
            # Insert into DB
            cur.execute("""
                INSERT INTO skillweaver.profiles 
                (class_id, spec_id, profile_name, profile_type, content, last_updated)
                VALUES (%s, %s, %s, 'SimC_Import', %s, CURRENT_TIMESTAMP)
                ON CONFLICT (spec_id, profile_name) 
                DO UPDATE SET 
                    content = EXCLUDED.content,
                    last_updated = CURRENT_TIMESTAMP
            """, (class_id, spec_id, 'Tier31_Standard', content))
            
            print(f"✅ Imported {lookup_key}")
            imported_count += 1
            
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
            
    conn.commit()
    cur.close()
    conn.close()
    print(f"\n🎉 Successfully imported {imported_count} profiles")

if __name__ == "__main__":
    print("=" * 60)
    print("SIMULATIONCRAFT PROFILE IMPORT")
    print("=" * 60)
    import_profiles()
