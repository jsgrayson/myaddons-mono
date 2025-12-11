#!/usr/bin/env python3
"""
Import profession data from TradeSkillMaster (TSM) SavedVariables.
Parses TSM's Lua data to populate character professions, skills, and known recipes.
"""

import os
import re
import psycopg2
import json
from datetime import datetime

# Path to TSM SavedVariables
TSM_PATH = "/Applications/World of Warcraft/_retail_/WTF/Account/NIGHTHWK77/SavedVariables/TradeSkillMaster.lua"
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://jgrayson@localhost/holocron')

def get_db_connection():
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def parse_lua_table(content):
    """
    Custom parser for TSM's specific Lua format.
    TSM stores data in a complex nested structure that standard parsers often fail on.
    """
    data = {}
    
    # Extract the internalData table which contains profession info
    # Structure: ["internalData"] = { ... ["_characterProfessions"] = { ... } ... }
    
    # 1. Find character professions
    # Pattern: ["_characterProfessions"] = { ... }
    prof_match = re.search(r'\["_characterProfessions"\]\s*=\s*{(.+?)}\s*,', content, re.DOTALL)
    if not prof_match:
        print("⚠️  Could not find _characterProfessions in TSM data")
        return {}
        
    prof_content = prof_match.group(1)
    
    # Parse each character's entry
    # Format: ["Name - Realm"] = { ... }
    char_pattern = re.compile(r'\["(.+?)"\]\s*=\s*{(.+?)}\s*,', re.DOTALL)
    
    for match in char_pattern.finditer(prof_content):
        char_key = match.group(1)  # "Vaxo - Dalaran"
        char_data_str = match.group(2)
        
        # Parse name and realm
        if " - " in char_key:
            name, realm = char_key.split(" - ", 1)
        else:
            name = char_key
            realm = "Unknown"
            
        data[name] = {
            'realm': realm,
            'professions': {}
        }
        
        # Parse professions for this character
        # Format: ["Profession"] = { ... "level" = 100, "maxLevel" = 100 ... }
        prof_entry_pattern = re.compile(r'\["(.+?)"\]\s*=\s*{(.+?)}', re.DOTALL)
        
        for p_match in prof_entry_pattern.finditer(char_data_str):
            prof_name = p_match.group(1)
            prof_details = p_match.group(2)
            
            # Extract level and max level
            level_match = re.search(r'\["level"\]\s*=\s*(\d+)', prof_details)
            max_match = re.search(r'\["maxLevel"\]\s*=\s*(\d+)', prof_details)
            
            if level_match and max_match:
                data[name]['professions'][prof_name] = {
                    'level': int(level_match.group(1)),
                    'max_level': int(max_match.group(1)),
                    'recipes': [] # TSM stores recipes elsewhere, usually in a separate module
                }
                
    return data

def import_tsm_data():
    """Read TSM file and update database"""
    if not os.path.exists(TSM_PATH):
        print(f"❌ TSM file not found at: {TSM_PATH}")
        return
        
    print(f"📖 Reading TSM data from: {TSM_PATH}")
    try:
        with open(TSM_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    # Parse data
    print("🔍 Parsing Lua data...")
    parsed_data = parse_lua_table(content)
    
    if not parsed_data:
        print("⚠️  No profession data found in TSM file")
        return

    conn = get_db_connection()
    if not conn:
        return
        
    cur = conn.cursor()
    
    try:
        imported_count = 0
        
        for char_name, char_info in parsed_data.items():
            print(f"\n👤 Processing {char_name} ({char_info['realm']})...")
            
            # Get character GUID (or create placeholder if not exists)
            cur.execute("SELECT character_guid FROM holocron.characters WHERE name = %s", (char_name,))
            res = cur.fetchone()
            
            if res:
                guid = res[0]
            else:
                # Create character if missing
                guid = f"Player-{char_name}-{char_info['realm']}"
                print(f"   Creating new character entry for {char_name}")
                cur.execute("""
                    INSERT INTO holocron.characters (character_guid, name, realm, last_seen)
                    VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                """, (guid, char_name, char_info['realm']))
            
            # Update professions
            for prof_name, prof_data in char_info['professions'].items():
                print(f"   🛠️  {prof_name}: {prof_data['level']}/{prof_data['max_level']}")
                
                # Map profession name to ID (simplified mapping)
                prof_id_map = {
                    'Alchemy': 171, 'Blacksmithing': 164, 'Enchanting': 333,
                    'Engineering': 202, 'Herbalism': 182, 'Inscription': 773,
                    'Jewelcrafting': 755, 'Leatherworking': 165, 'Mining': 186,
                    'Skinning': 393, 'Tailoring': 197, 'Cooking': 185
                }
                prof_id = prof_id_map.get(prof_name, 0)
                
                cur.execute("""
                    INSERT INTO goblin.professions 
                    (character_guid, profession_id, profession_name, skill_level, max_skill, last_updated)
                    VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (character_guid, profession_id) 
                    DO UPDATE SET
                        skill_level = EXCLUDED.skill_level,
                        max_skill = EXCLUDED.max_skill,
                        last_updated = CURRENT_TIMESTAMP
                """, (guid, prof_id, prof_name, prof_data['level'], prof_data['max_level']))
                
                imported_count += 1
        
        conn.commit()
        print(f"\n✅ Successfully imported {imported_count} professions")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("TRADESKILLMASTER DATA IMPORT")
    print("=" * 60)
    import_tsm_data()
