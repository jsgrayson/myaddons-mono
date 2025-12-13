#!/usr/bin/env python3
"""
Sync WoW addon data to Holocron SQLite database
"""

import sqlite3
import os
import re
from datetime import datetime

# Paths
WOW_SAVED = "/Applications/World of Warcraft/_retail_/WTF/Account/NIGHTHWK77/SavedVariables"
DB_PATH = "/Users/jgrayson/Documents/holocron/holocron.db"

def parse_lua_table(content):
    """Simple Lua table parser for SavedVariables"""
    # This is a basic parser - for complex tables use slpp.py
    data = {}
    
    # Extract character data
    char_pattern = r'\["(.+?) - (.+?)"\] = \{[^}]+\["class"\] = "(\w+)"[^}]+\["level"\] = (\d+)'
    for match in re.finditer(char_pattern, content):
        char_name, realm, char_class, level = match.groups()
        data[f"{char_name}-{realm}"] = {
            'name': char_name,
            'realm': realm,
            'class': char_class,
            'level': int(level)
        }
    
    return data

def sync_characters():
    """Sync character data from DeepPockets"""
    dp_file = os.path.join(WOW_SAVED, "DeepPockets.lua")
    
    if not os.path.exists(dp_file):
        print("❌ DeepPockets.lua not found")
        return
    
    with open(dp_file, 'r') as f:
        content = f.read()
    
    chars = parse_lua_table(content)
    
    # Filter out test data
    chars = {k: v for k, v in chars.items() if 'Jaina' not in k}
    
    if not chars:
        print("⚠️  No character data found (excluding test data)")
        return
    
    # Connect to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            character_guid TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            realm TEXT NOT NULL,
            class TEXT,
            level INTEGER,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert/update characters
    synced = 0
    for char_id, char_data in chars.items():
        cursor.execute("""
            INSERT OR REPLACE INTO characters (character_guid, name, realm, class, level, last_seen)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            char_id,
            char_data['name'],
            char_data['realm'],
            char_data['class'],
            char_data['level'],
            datetime.now()
        ))
        synced += 1
        print(f"✅ Synced: {char_data['name']} ({char_data['class']} {char_data['level']})")
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Total characters synced: {synced}")

def sync_inventory():
    """Sync inventory data from DeepPockets"""
    dp_file = os.path.join(WOW_SAVED, "DeepPockets.lua")
    
    if not os.path.exists(dp_file):
        return
    
    # TODO: Parse inventory data when bags are scanned
    # For now, just report what we have
    # Parse inventory data
    inventory_data = []
    with open(dp_file, 'r') as f:
        content = f.read()

    # Regex for item blocks (handling variable key order and optional fields)
    # We'll look for the start of a table element in a list `\n  {` or ` {` and capture the block content
    # This is rough but works for standard SavedVariables formatting.
    # Alternatively, we can just find *all* `id` fields and look around them, but that's risky.
    
    # Better: Scan the content for `{ ... }` blocks that look like items.
    # A typical item block:
    # {
    #  ["id"] = 123,
    #  ["name"] = "Foo",
    #  ...
    # },
    
    item_blocks = re.findall(r'\{([^}]+)\},', content)
    
    for block in item_blocks:
        # Extract fields from the block
        # Helper to extract value by key
        def get_val(key, text, type_func=str):
            m = re.search(r'\[' + key + r'\]\s*=\s*([^,\n]+)', text)
            if m:
                val = m.group(1).strip('"') # remove quotes if string
                return type_func(val)
            return None

        item_id = get_val('"id"', block, int)
        if not item_id: continue # Skip if no ID
        
        name = get_val('"name"', block) or f"Item {item_id}"
        count = get_val('"count"', block, int) or 1
        quality = get_val('"quality"', block, int)
        category = get_val('"category"', block)
        location = get_val('"loc"', block) or get_val('"location"', block) or "BAG"
        
        # Normalize Location
        location = location.upper()
        if "BAG" in location: location = "BAG"
        elif "BANK" in location: location = "BANK"
        
        inventory_data.append({
            "item_id": item_id,
            "name": name,
            "count": count,
            "quality": quality,
            "category": category,
            "location": location,
            "unit_value": 0 # Placeholder for now
        })

    if inventory_data:
        print(f"\n📦 Found {len(inventory_data)} inventory items")
        
        # Save to JSON
        import json
        out_path = "synced_data/deeppockets_inventory.json"
        
        # Ensure dir exists
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        
        with open(out_path, "w") as f:
            json.dump({"items": inventory_data}, f, indent=2)
            
        print(f"✅ Saved namespaced inventory to {out_path}")
    else:
        print("\n⚠️  No inventory data found (or regex mismatch)")


def extract_snapshot(addon, content):
    """
    Extract snapshot metrics from Lua content using regex.
    Returns: dict
    """
    snapshot = {}
    
    if addon == "DeepPockets":
        # Count "id" fields in item blocks to estimate inventory size
        # This matches the regex used in sync_inventory
        items = re.findall(r'\["id"\]\s*=\s*\d+', content)
        snapshot["inv_count"] = len(items)
        
        # Try to find money (rough regex)
        # DeepPocketsDB = { ... ["money"] = 12345 ... }
        # or profile based? 
        # Assuming DeepPocketsDB structure has money
        m = re.search(r'\["money"\]\s*=\s*(\d+)', content)
        if m: snapshot["money_copper"] = int(m.group(1))
        
    elif addon == "PetWeaver":
        # Count pets
        # PetWeaverDB.teams? .pets?
        # Assuming we scan for team definitions or pet IDs
        # "speciesId" is common
        pets = re.findall(r'\["speciesId"\]\s*=\s*\d+', content)
        snapshot["owned_pet_count"] = len(pets)
        
        # Count strategies/teams
        # teams = { ... }
        # Look for named teams?
        teams = re.findall(r'\["name"\]\s*=\s*"[^"]+"', content)
        snapshot["strategy_count"] = len(teams)
        
    elif addon == "SkillWeaver":
        # module_count
        # sequences = { ... }
        # Look for sequence names
        seqs = re.findall(r'\["name"\]\s*=\s*"[^"]+"', content)
        snapshot["module_count"] = len(seqs)
        
        # active_spec_present
        # ["spec"] = 269 (Windwalker)
        m = re.search(r'\["spec"\]\s*=\s*(\d+)', content)
        snapshot["active_spec_present"] = bool(m)
        
    elif addon == "Holocron": # HolocronViewer
        # character_count
        # ["MyChar - Realm"] = { ... }
        # Matches typical SavedVariables keys
        chars = re.findall(r'\["(.+? - .+?)"\]\s*=\s*\{', content)
        snapshot["character_count"] = len(set(chars))
        
    return snapshot

def sync_sanity():
    """
    Generates sanity reports based on SavedVariables content.
    If 'SANITY_RESULT' string is found (chat logs), uses that.
    Propagates metrics via 'snapshot'.
    """
    import requests
    import json
    
    print("\n🔍 Generating Confidence Reports...")
    
    addons = [
        ("DeepPockets.lua", "DeepPockets"),
        ("PetWeaver.lua", "PetWeaver"),
        ("HolocronViewer.lua", "Holocron"),
        ("Skillweaver.lua", "SkillWeaver")
    ]
    
    API_URL = "http://localhost:8003/api/v1/sanity/report"
    
    for filename, addon_name in addons:
        path = os.path.join(WOW_SAVED, filename)
        
        # 1. Check File Existence
        if not os.path.exists(path):
            print(f"⚠️  {addon_name}: File not found (FAIL)")
            # Synthesize FAIL report
            payload = {
                "addon": addon_name,
                "status": "FAIL",
                "character": "System",
                "timestamp": datetime.now().isoformat(),
                "details": {"reason": "SavedVariables file missing"}
            }
            try: requests.post(API_URL, json=payload, timeout=1) 
            except: pass
            continue
            
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 2. Extract Snapshot Metrics
            snapshot = extract_snapshot(addon_name, content)
            
            # 3. Determine Status
            # Priority A: Explict SANITY_RESULT (if present in file/logs)
            matches = re.findall(r'SANITY_RESULT\s+(\{.*?\})', content)
            
            if matches:
                # Use the addon's self-reported status
                last_json = matches[-1]
                payload = json.loads(last_json)
                
                # Ensure fields
                if "snapshot" not in payload: payload["snapshot"] = snapshot
                if "timestamp" not in payload: payload["timestamp"] = datetime.now().isoformat()
                if "character" not in payload: payload["character"] = "MyChar" # TODO: scrape correct char
                
            else:
                # Priority B: Synthesize from DB Presence
                # If we could read the file and extract snapshot, it's broadly "OK"
                # The server Heuristics will downgrade to WARN if snapshot is bad.
                payload = {
                    "addon": addon_name,
                    "status": "OK", # Assumed OK if file exists
                    "character": "MyChar", # Generic owner
                    "timestamp": datetime.now().isoformat(),
                    "snapshot": snapshot,
                    "details": {"source": "synthesized_from_sv"}
                }
                
                # Check for emptiness
                if len(snapshot) == 0:
                     payload["status"] = "WARN"
                     payload["details"]["reason"] = "DB empty or parse failed"
            
            # 4. Post Report
            try:
                resp = requests.post(API_URL, json=payload, timeout=2)
                print(f"✅ Report {addon_name}: {payload['status']} (Snap: {len(snapshot)} keys)")
            except requests.exceptions.RequestException:
                print(f"⚠️  Report Skipped: {addon_name} (API Down)")
                
        except Exception as e:
            print(f"❌ Error processing {addon_name}: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("HOLOCRON SYNC")
    print("=" * 60)
    
    sync_characters()
    sync_inventory()
    sync_sanity()
    
    print("\n" + "=" * 60)
    print("✅ Sync complete!")
    print("=" * 60)

    # Write sync status
    import json
    status = {
        "last_synced_at": datetime.utcnow().isoformat() + "Z", # UTC ISO format
        "source": "script"
    }
    with open("sync_status.json", "w") as f:
        json.dump(status, f)
    print(f"🕒 Timestamp updated: {status['last_synced_at']}")
