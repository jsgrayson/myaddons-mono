#!/usr/bin/env python3
"""
Import DeepPockets inventory data into the Holocron database.
Parses DeepPockets.lua SavedVariables to extract item and storage location data.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import re
import json

# Configuration
WOW_ACCOUNT = "NIGHTHWK77"
DEEPPOCKETS_FILE = f"/Applications/World of Warcraft/_retail_/WTF/Account/{WOW_ACCOUNT}/SavedVariables/DeepPockets.lua"
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://jgrayson@localhost/holocron')

def get_db_connection():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def parse_deeppockets_file():
    """Parse Deep Pockets.lua SavedVariables file using regex"""
    if not os.path.exists(DEEPPOCKETS_FILE):
        print(f"❌ DeepPockets file not found: {DEEPPOCKETS_FILE}")
        return None
    
    try:
        with open(DEEPPOCKETS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract inventory data using regex
        # Pattern: ["Character - Realm"] = { ... }
        inventory_data = {}
        
        # Find all character inventory sections
        pattern = r'\["([^"]+) - ([^"]+)"\] = \{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
        inventory_section = re.search(r'\["Inventory"\] = \{(.+?)\n\s*\},\n', content, re.DOTALL)
        
        if inventory_section:
            inv_content = inventory_section.group(1)
            
            # Find each character's inventory
            char_pattern = r'\["([^"]+) - ([^"]+)"\] = \{(.*?)\n\s*\},'
            for match in re.finditer(char_pattern, inv_content, re.DOTALL):
                char_name = match.group(1)
                realm = match.group(2)
                items_text = match.group(3)
                
                items = []
                # Parse individual items: { ["id"] = 123, ["count"] = 45, ["loc"] = "Bag", }
                item_pattern = r'\{[^}]*\["id"\]\s*=\s*(\d+)[^}]*\["count"\]\s*=\s*(\d+)[^}]*\["loc"\]\s*=\s*"([^"]+)"[^}]*\}'
                for item_match in re.finditer(item_pattern, items_text):
                    items.append({
                        'id': int(item_match.group(1)),
                        'count': int(item_match.group(2)),
                        'loc': item_match.group(3)
                    })
                
                if items:
                    inventory_data[f"{char_name} - {realm}"] = items
        
        return inventory_data
    
    except Exception as e:
        print(f"❌ Error parsing DeepPockets file: {e}")
        import traceback
        traceback.print_exc()
        return None

def import_inventory_data():
    """Import item and storage location data from DeepPockets"""
    conn = get_db_connection()
    if not conn:
        return 0
    
    inventory_data = parse_deeppockets_file()
    if not inventory_data:
        return 0
    
    cur = conn.cursor()
    items_imported = 0
    locations_created = 0
    
    print("🔍 Parsing DeepPockets inventory data...")
    
    # inventory_data is now a dict: {"Character - Realm": [items]}
    for char_key, items in inventory_data.items():
        # Parse character key (format: "Name - Realm")
        if ' - ' not in char_key:
            continue
        
        char_name, realm = char_key.split(' - ', 1)
        char_guid = f"Player-{realm.replace(' ', '')}-{char_name}"
        
        # Check if character exists
        cur.execute("SELECT character_guid FROM holocron.characters WHERE character_guid = %s", (char_guid,))
        if not cur.fetchone():
            print(f"⚠️  Character not found: {char_key}, skipping")
            continue
        
        print(f"\n📦 Processing inventory for {char_key}")
        
        # Process each item in the character's inventory
        for item_data in items:
            item_id = item_data.get('id')
            count = item_data.get('count', 1)
            location_type = item_data.get('loc', 'Bag')
            
            if not item_id:
                continue
            
            try:
                # Create or get storage location
                cur.execute("""
                    INSERT INTO holocron.storage_locations 
                    (character_guid, container_type, container_index)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                    RETURNING location_id
                """, (char_guid, location_type, 0))
                
                result = cur.fetchone()
                if result:
                    location_id = result[0]
                    locations_created += 1
                else:
                    # Location already exists, fetch it
                    cur.execute("""
                        SELECT location_id FROM holocron.storage_locations
                        WHERE character_guid = %s AND container_type = %s
                    """, (char_guid, location_type))
                    location_id = cur.fetchone()[0]
                
                # Insert item
                item_guid = f"{char_guid}-{item_id}-{location_type}"
                cur.execute("""
                    INSERT INTO holocron.items 
                    (item_guid, item_id, count, location_id, last_updated)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (item_guid) 
                    DO UPDATE SET
                        count = EXCLUDED.count,
                        last_updated = CURRENT_TIMESTAMP
                """, (item_guid, item_id, count, location_id))
                
                items_imported += 1
                print(f"  ✅ Item {item_id} x{count} in {location_type}")
                
            except Exception as e:
                print(f"  ❌ Error importing item {item_id}: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    
    print(f"\n✅ Import complete!")
    print(f"   - Items: {items_imported}")
    print(f"   - Storage locations: {locations_created}")
    
    return items_imported

def verify_import():
    """Verify the import by querying the database"""
    conn = get_db_connection()
    if not conn:
        return
    
    cur = conn.cursor()
    
    # Count items per character
    cur.execute("""
        SELECT c.name, c.realm, sl.container_type, COUNT(i.item_guid) as item_count
        FROM holocron.characters c
        LEFT JOIN holocron.storage_locations sl ON c.character_guid = sl.character_guid
        LEFT JOIN holocron.items i ON sl.location_id = i.location_id
        GROUP BY c.name, c.realm, sl.container_type
        ORDER BY c.name, sl.container_type
    """)
    
    rows = cur.fetchall()
    
    print("\n📊 Inventory Summary:")
    print("-" * 60)
    current_char = None
    for row in rows:
        char_name = row[0]
        if char_name != current_char:
            print(f"\n{char_name} ({row[1]}):")
            current_char = char_name
        if row[2]:  # container_type
            print(f"  {row[2]:15} - {row[3]} items")
    print("-" * 60)
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("DEEPPOCKETS INVENTORY IMPORT")
    print("=" * 60)
    print(f"Source: {DEEPPOCKETS_FILE}")
    print(f"Target: {DATABASE_URL}")
    print("=" * 60)
    
    imported = import_inventory_data()
    
    if imported > 0:
        verify_import()
    else:
        print("\n⚠️  No inventory data was imported.")
