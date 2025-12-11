#!/usr/bin/env python3
"""
Import real WoW character data into the Holocron database.
Reads from WoW SavedVariables and populates the database tables.
"""

import os
import psycopg2
import re
from datetime import datetime

# Configuration
WOW_ACCOUNT = "NIGHTHWK77"
WOW_PATH = f"/Applications/World of Warcraft/_retail_/WTF/Account/{WOW_ACCOUNT}"
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://jgrayson@localhost/holocron')

# Character directories (Realm/CharacterName)
REALMS = {
    "Dalaran": ["Vaxo", "Slaythe", "Vacco", "Bronha"]
}

def get_db_connection():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def parse_blizzard_character_vars(char_path):
    """
    Parse Blizzard_ClientSavedVariables.lua to extract basic character info.
    This file contains: name, class, race, faction info
    """
    vars_file = os.path.join(char_path, "SavedVariables", "Blizzard_ClientSavedVariables.lua")
    
    if not os.path.exists(vars_file):
        return None
    
    try:
        with open(vars_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract character name from file structure
        char_name = os.path.basename(char_path)
        realm_name = os.path.basename(os.path.dirname(char_path))
        
        # Try to find class info if available
        # Blizzard_ClientSavedVariables may not have all info, 
        # but we can at least get the name and realm
        
        return {
            "name": char_name,
            "realm": realm_name,
            "guid": f"Player-{realm_name}-{char_name}",  # Simplified GUID
            "class": None,  # Will try to determine from other sources
            "race": None,
            "faction": None,
            "level": 80,  # Default to max level
        }
    except Exception as e:
        print(f"Error parsing {vars_file}: {e}")
        return None

def parse_pettracker_for_chars(account_saved_vars):
    """
    PetTracker SavedVariables might contain character data.
    """
    pettracker_file = os.path.join(account_saved_vars, "PetTracker.lua")
    
    if not os.path.exists(pettracker_file):
        return {}
    
    char_data = {}
    try:
        with open(pettracker_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for character entries (format varies)
        # This is a naive parse - adjust based on actual file structure
        # Example: ["accounts"]["AccountName"]["Realm"]["CharName"]
        
        # For now, return empty dict as we'll use character directories
        return char_data
    except Exception as e:
        print(f"Error parsing PetTracker: {e}")
        return {}

def detect_character_class_from_addons(char_path):
    """
    Try to detect class from addon SavedVariables
    """
    # Check if any addon data hints at the class
    # This is a fallback approach
    
    # Common class indicators (you'd expand this based on actual data)
    class_map = {
        "Vaxo": "Druid",
        "Slaythe": "Rogue",
        "Vacco": "Priest",
        "Bronha": "Warrior"  # Corrected from Shaman
    }
    
    char_name = os.path.basename(char_path)
    return class_map.get(char_name, "Unknown")

def clear_mock_data():
    """Remove sample/mock characters before importing real data"""
    conn = get_db_connection()
    if not conn:
        return
    
    cur = conn.cursor()
    try:
        # Delete sample characters from Area 52 realm
        cur.execute("DELETE FROM holocron.characters WHERE realm = 'Area 52'")
        deleted = cur.rowcount
        conn.commit()
        print(f"🗑️  Cleared {deleted} mock characters")
    except Exception as e:
        print(f"❌ Error clearing mock data: {e}")
    finally:
        cur.close()
        conn.close()

def import_characters():
    """Import character data from WoW SavedVariables"""
    conn = get_db_connection()
    if not conn:
        return
    
    cur = conn.cursor()
    imported = 0
    
    print("🔍 Scanning WoW directories for characters...")
    
    for realm, characters in REALMS.items():
        for char_name in characters:
            char_path = os.path.join(WOW_PATH, realm, char_name)
            
            if not os.path.exists(char_path):
                print(f"⚠️  Character path not found: {char_path}")
                continue
            
            # Parse character data
            char_info = parse_blizzard_character_vars(char_path)
            
            if not char_info:
                print(f"⚠️  Could not parse data for {char_name}")
                continue
            
            # Detect class if not found
            if not char_info["class"]:
                char_info["class"] = detect_character_class_from_addons(char_path)
            
            # Generate GUID
            guid = f"Player-{realm.replace(' ', '')}-{char_name}"
            
            try:
                # Insert or update character
                cur.execute("""
                    INSERT INTO holocron.characters 
                    (character_guid, name, realm, class, level, race, faction, spec, item_level)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (character_guid) 
                    DO UPDATE SET
                        name = EXCLUDED.name,
                        realm = EXCLUDED.realm,
                        class = EXCLUDED.class,
                        level = EXCLUDED.level,
                        last_seen = CURRENT_TIMESTAMP
                """, (
                    guid,
                    char_info["name"],
                    char_info["realm"],
                    char_info["class"],
                    char_info["level"],
                    char_info.get("race"),
                    char_info.get("faction"),
                    None,  # spec - would need more addon data
                    None   # item_level - would need gear scan
                ))
                
                imported += 1
                print(f"✅ Imported: {char_name} ({char_info['class']}) - {realm}")
                
            except Exception as e:
                print(f"❌ Error importing {char_name}: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    
    print(f"\n✅ Import complete! Imported {imported} characters.")
    return imported

def verify_import():
    """Verify the import by querying the database"""
    conn = get_db_connection()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("SELECT name, realm, class, level FROM holocron.characters ORDER BY name")
    rows = cur.fetchall()
    
    print("\n📊 Current characters in database:")
    print("-" * 60)
    for row in rows:
        print(f"  {row[0]:15} | {row[1]:15} | {row[2]:10} | Level {row[3]}")
    print("-" * 60)
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("HOLOCRON DATA IMPORT")
    print("=" * 60)
    print(f"Source: {WOW_PATH}")
    print(f"Target: {DATABASE_URL}")
    print("=" * 60)
    
    # Clear mock data first
    clear_mock_data()
    
    imported = import_characters()
    
    if imported > 0:
        print("\nVerifying import...")
        verify_import()
    else:
        print("\n⚠️  No characters were imported. Check the configuration.")
