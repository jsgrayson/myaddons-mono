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
    with open(dp_file, 'r') as f:
        content = f.read()
    
    # Count inventory entries (excluding test data)
    inv_pattern = r'\["((?!Jaina).+?) - (.+?)"\] = \{[^}]*\["id"\] = (\d+)'
    items = re.findall(inv_pattern, content)
    
    if items:
        print(f"\n📦 Found {len(items)} inventory items")
    else:
        print("\n⚠️  No inventory data yet - open bags on each character!")

if __name__ == "__main__":
    print("=" * 60)
    print("HOLOCRON SYNC")
    print("=" * 60)
    
    sync_characters()
    sync_inventory()
    
    print("\n" + "=" * 60)
    print("✅ Sync complete!")
    print("=" * 60)
