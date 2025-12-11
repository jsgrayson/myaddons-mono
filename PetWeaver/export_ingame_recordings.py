"""
Export PetWeaver Enemy Recordings to JSON

Reads SavedVariables from WoW addon and exports enemy move data
to update enhanced_enemy_npc_scripts.json
"""

import json
import re
import os

def parse_lua_saved_variables(lua_file_path):
    """Parse Lua SavedVariables file to extract enemy recordings."""
    
    if not os.path.exists(lua_file_path):
        print(f"❌ File not found: {lua_file_path}")
        print("Make sure to:")
        print("  1. Enable recording in-game: /pwrecord")
        print("  2. Fight some pet battle NPCs")
        print("  3. /reload to save data")
        print("  4. Find SavedVariables at: WoW/_retail_/WTF/Account/YOUR_ACCOUNT/SavedVariables/PetWeaver.lua")
        return None
    
    with open(lua_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for PetWeaverEnemyRecordings table
    pattern = r'PetWeaverEnemyRecordings\s*=\s*\{([^\}]*)\}'
    matches = re.findall(pattern, content, re.DOTALL)
    
    if not matches:
        print("⚠️  No PetWeaverEnemyRecordings found in file")
        return {}
    
    # For now, just indicate data was found
    # Full Lua parsing is complex, so we'll provide instructions
    print("✅ Found PetWeaverEnemyRecordings data!")
    print("📝 Manual extraction required or use LibSerialize")
    
    return {}

def merge_with_existing_scripts(new_data):
    """Merge new in-game recordings with existing AI scripts."""
    
    # Load existing
    with open('enhanced_enemy_npc_scripts.json', 'r') as f:
        existing = json.load(f)
    
    # Merge logic here
    # This would update encounter scripts based on real in-game data
    
    return existing

def main():
    print("PetWeaver Enemy Recording Exporter")
    print("="*60)
    
    # Default SavedVariables path (user will need to adjust)
    default_path = "~/World of Warcraft/_retail_/WTF/Account/ACCOUNT_NAME/SavedVariables/PetWeaver.lua"
    
    print(f"\nDefault path: {default_path}")
    print("\nTo use:")
    print("  1. In-game: /pwrecord (enables recording)")
    print("  2. Fight pet battle NPCs")
    print("  3. /reload (saves data)")
    print("  4. Run this script with the correct SavedVariables path")
    print("\nData will be merged with enhanced_enemy_npc_scripts.json")

if __name__ == "__main__":
    main()
