#!/usr/bin/env python3
"""
Import inventory data from DeepPockets SavedVariables.
Parses DeepPockets.lua to populate character bags, bank, and item details.
"""

import os
import re
import psycopg2
import json

# Path to DeepPockets SavedVariables
DEEPPOCKETS_PATH = "/Applications/World of Warcraft/_retail_/WTF/Account/NIGHTHWK77/SavedVariables/DeepPockets.lua"
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://jgrayson@localhost/holocron')

def get_db_connection():
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def parse_lua_table(content):
    """
    Custom parser for DeepPockets Lua format.
    """
    data = {}
    
    # Extract the global Inventory table
    # Structure: ["global"] = { ... ["Inventory"] = { ... } ... }
    
    # 1. Find Inventory table content
    # Look for ["Inventory"] = { ... } inside ["global"]
    # This is tricky with regex, so let's find the start and extract the block
    
    start_marker = '["Inventory"] = {'
    start_idx = content.find(start_marker)
    
    if start_idx == -1:
        print("⚠️  Could not find Inventory table start")
        return {}
    
    # Simple brace counting to find the end of the table
    brace_count = 0
    end_idx = -1
    
    for i in range(start_idx + len(start_marker) - 1, len(content)):
        char = content[i]
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i
                break
    
    if end_idx == -1:
        print("⚠️  Could not find Inventory table end")
        return {}
        
    inv_content = content[start_idx:end_idx+1]
    
    # 2. Parse characters
    # Format: ["Name - Realm"] = { ... }
    # We'll split by character keys
    
    # Find all character keys
    char_matches = list(re.finditer(r'\["(.+?)"\]\s*=\s*{', inv_content))
    
    for i, match in enumerate(char_matches):
        char_key = match.group(1)
        start_pos = match.end()
        
        # Determine end position (either next match start or end of string)
        if i < len(char_matches) - 1:
            end_pos = char_matches[i+1].start()
        else:
            end_pos = len(inv_content)
            
        char_block = inv_content[start_pos:end_pos]
        
        if " - " in char_key:
            name, realm = char_key.split(" - ", 1)
        else:
            name = char_key
            realm = "Unknown"
            
        data[name] = {
            'realm': realm,
            'items': []
        }
        
        # Parse items in this block
        # Format: { ["id"] = 123, ["count"] = 5, ["loc"] = "Bag" },
        # OR simplified: { [1]=123, [2]=5, [3]="Bag" } depending on Lua serializer
        
        # Let's try a more robust item pattern
        # Look for blocks starting with { and containing "id"
        item_blocks = re.finditer(r'{(.+?)}', char_block, re.DOTALL)
        
        for block in item_blocks:
            inner = block.group(1)
            
            # Extract fields
            id_match = re.search(r'\["id"\]\s*=\s*(\d+)', inner)
            count_match = re.search(r'\["count"\]\s*=\s*(\d+)', inner)
            loc_match = re.search(r'\["loc"\]\s*=\s*"(.+?)"', inner)
            
            if id_match and count_match:
                data[name]['items'].append({
                    'id': int(id_match.group(1)),
                    'count': int(count_match.group(1)),
                    'location': loc_match.group(1) if loc_match else "Unknown"
                })
            
    return data

def import_inventory():
    """Read DeepPockets file and update database"""
    if not os.path.exists(DEEPPOCKETS_PATH):
        print(f"❌ DeepPockets file not found at: {DEEPPOCKETS_PATH}")
        return
        
    print(f"📖 Reading inventory from: {DEEPPOCKETS_PATH}")
    try:
        with open(DEEPPOCKETS_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    # Parse data
    print("🔍 Parsing Lua data...")
    parsed_data = parse_lua_table(content)
    
    if not parsed_data:
        print("⚠️  No inventory data found")
        return

    conn = get_db_connection()
    if not conn:
        return
        
    cur = conn.cursor()
    
    try:
        total_items = 0
        
        # Create tables if not exist (matching schema.sql)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS holocron.storage_locations (
                location_id SERIAL PRIMARY KEY,
                character_guid VARCHAR(255) REFERENCES holocron.characters(character_guid),
                container_type VARCHAR(50) NOT NULL,
                container_index INT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS holocron.items (
                item_guid VARCHAR(255) PRIMARY KEY,
                item_id INT NOT NULL,
                name VARCHAR(255),
                count INT DEFAULT 1,
                location_id INT REFERENCES holocron.storage_locations(location_id),
                slot INT,
                quality INT,
                ilvl INT,
                class_id INT,
                subclass_id INT,
                texture VARCHAR(255),
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        for char_name, char_info in parsed_data.items():
            # Filter out fake data
            if char_name in ["Jaina", "Thrall", "Inventory"]:
                continue
                
            print(f"\n👤 Processing {char_name} ({char_info['realm']})...")
            
            # Get character GUID
            cur.execute("SELECT character_guid FROM holocron.characters WHERE name = %s", (char_name,))
            res = cur.fetchone()
            
            if res:
                guid = res[0]
            else:
                guid = f"Player-{char_name}-{char_info['realm']}"
                # Auto-create character
                cur.execute("""
                    INSERT INTO holocron.characters (character_guid, name, realm, last_seen)
                    VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (character_guid) DO NOTHING
                """, (guid, char_name, char_info['realm']))
            
            # Clear old inventory for this character
            # First get location IDs to delete items
            cur.execute("SELECT location_id FROM holocron.storage_locations WHERE character_guid = %s", (guid,))
            loc_ids = [row[0] for row in cur.fetchall()]
            
            if loc_ids:
                cur.execute("DELETE FROM holocron.items WHERE location_id = ANY(%s)", (loc_ids,))
                cur.execute("DELETE FROM holocron.storage_locations WHERE character_guid = %s", (guid,))
            
            # Insert new items
            char_items = 0
            
            # Create default locations for Bag and Bank
            cur.execute("""
                INSERT INTO holocron.storage_locations (character_guid, container_type, container_index)
                VALUES (%s, 'Bag', 0) RETURNING location_id
            """, (guid,))
            bag_loc_id = cur.fetchone()[0]
            
            cur.execute("""
                INSERT INTO holocron.storage_locations (character_guid, container_type, container_index)
                VALUES (%s, 'Bank', 0) RETURNING location_id
            """, (guid,))
            bank_loc_id = cur.fetchone()[0]
            
            for item in char_info['items']:
                loc_id = bank_loc_id if item['location'] == 'Bank' else bag_loc_id
                item_guid = f"{guid}-{item['id']}-{item['location']}" # Pseudo-GUID
                
                cur.execute("""
                    INSERT INTO holocron.items 
                    (item_guid, item_id, name, count, location_id, last_updated)
                    VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (item_guid) DO UPDATE SET
                        count = EXCLUDED.count,
                        last_updated = CURRENT_TIMESTAMP
                """, (item_guid, item['id'], f"Item {item['id']}", item['count'], loc_id))
                
                char_items += 1
                total_items += 1
            
            print(f"   ✅ Imported {char_items} items")
        
        conn.commit()
        print(f"\n✅ Successfully imported {total_items} total items across {len(parsed_data)} characters")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("DEEPPOCKETS INVENTORY IMPORT")
    print("=" * 60)
    import_inventory()
