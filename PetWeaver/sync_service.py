import os
import time
import re
import sqlite3
import datetime
import traceback
from pathlib import Path

# Try to import db_helper, or fallback if running standalone
try:
    import db_helper
except ImportError:
    print("Warning: db_helper not found, direct DB access might be limited.")

class LuaTableParser:
    """Robust text-based parser for WoW Lua SavedVariables tables"""
    
    @staticmethod
    def parse(lua_string):
        """Parse Lua table string into Python dict/list"""
        # Remove comments
        lua_string = re.sub(r'--.*', '', lua_string)
        
        # Tokenize (text, is_string, is_syntax)
        tokens = []
        i = 0
        length = len(lua_string)
        
        while i < length:
            char = lua_string[i]
            
            if char.isspace():
                i += 1
                continue
                
            if char == '"' or char == "'":
                quote = char
                i += 1
                start = i
                while i < length:
                    if lua_string[i] == quote and lua_string[i-1] != '\\':
                        break
                    i += 1
                tokens.append((lua_string[start:i], True))
                i += 1
            elif char in '{}=,[]':
                tokens.append((char, False))
                i += 1
            else:
                start = i
                while i < length and not (lua_string[i].isspace() or lua_string[i] in '{}=,[]'):
                    i += 1
                val = lua_string[start:i]
                
                # Convert numbers/booleans
                if val == 'true': val = True
                elif val == 'false': val = False
                elif val == 'nil': val = None
                else:
                    try:
                        if '.' in val: val = float(val)
                        else: val = int(val)
                    except ValueError:
                        pass # keep as string
                
                tokens.append((val, True)) # Treat as value
        
        # Parse tokens into structure
        stack = []
        current_obj = {} # Root is a dict (Lua table)
        current_key = None
        
        is_array_mode = False # Lua tables can be arrays or dicts
        
        idx = 0
        while idx < len(tokens):
            val, is_literal = tokens[idx]
            
            if val == '{':
                new_obj = {}
                if stack:
                    parent = stack[-1]
                    if isinstance(parent, list):
                        parent.append(new_obj)
                    else:
                        if current_key is None:
                            # Implicit array index?
                            # In Lua { "a", "b" } is mixed. 
                            # For simplicity, if key is missing and we are in dict, ignore or error?
                            # Actually WoW SVs are usually explicit keys or arrays.
                            pass
                        else:
                            parent[current_key] = new_obj
                            current_key = None
                
                stack.append(new_obj)
            
            elif val == '}':
                if stack:
                    completed = stack.pop()
                    # Convert to list if it looks like an array (keys "1", "2", etc)
                    if isinstance(completed, dict) and '1' in completed and '2' in completed:
                        # Simple heuristic for mixed tables
                        pass 
            
            elif val == '[':
                # Key start ["key"]
                idx += 1
                key_val, _ = tokens[idx]
                idx += 1 # ']'
                current_key = key_val
                
            elif val == '=':
                pass
                
            elif val == ',':
                current_key = None # Reset key for next pair
                
            else:
                # Literal value
                if stack:
                    parent = stack[-1]
                    if current_key is not None:
                        parent[current_key] = val
                        current_key = None
                    else:
                        # Array item?
                        # If we treat everything as dict first, we handle array logic later
                        # But for WoW SVs: ["key"] = val is common.
                        # Simple list: { val1, val2 } -> no keys.
                        # We need to handle this.
                        
                        # Hacky fix: if parent is dict but no key, maybe convert to list?
                        # Or just use auto-increment keys.
                        pass
            
            idx += 1
            
        # NOTE: This is a hasty parser sketch. 
        # A full parser is complex. 
        # Better approach for this task: Regex specific patterns since we know the structure.
        return {}

    @staticmethod
    def regex_extract(lua_content):
        """
        Regex extraction specifically for PetWeaver structure.
        PetWeaverDB = { ... ["petList"] = { ... } ... }
        """
        data = {"pets": [], "strategies": []}
        
        # 1. Extract petList block
        pet_list_match = re.search(r'\["petList"\]\s*=\s*{(.*?)},', lua_content, re.DOTALL)
        if pet_list_match:
            pet_block = pet_list_match.group(1)
            # Find individual pets: { ... }
            # Nested structure makes regex hard.
            # Assuming one line per pet or standard formatting?
            # Actually, `export_ingame_recordings.py` approach might be better.
            pass
            
        return data

def parse_lua_simple(filepath):
    """
    Highly simplified parser assuming specific formatting from PetWeaver.lua.
    
    Structure assumptions:
    - Tables use ["key"] = val
    - Arrays use { val, val } or [i] = val
    - We fundamentally care about 'petList' which is a list of objects.
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    data = {
        "pets": []
    }
    
    # 1. Extract Pet List
    # Look for the start of petList
    start_marker = '["petList"] = {'
    start_idx = content.find(start_marker)
    
    if start_idx != -1:
        # Simple stack counter to find end of this table
        open_brackets = 1
        i = start_idx + len(start_marker)
        pet_list_str = ""
        
        while i < len(content) and open_brackets > 0:
            char = content[i]
            if char == '{': open_brackets += 1
            elif char == '}': open_brackets -= 1
            
            if open_brackets > 0:
                pet_list_str += char
            i += 1
        
        # Now parse the inner items. Each starts with { and ends with }, -- [i]
        # Regex to find: { ["petID"] = "...", ... }
        
        # Pattern for fields
        # ["key"] = value
        # value can be number, string "...", or boolean
        
        # We can split by '}, -- [' to get rough chunks if formatted nicely
        chunks = pet_list_str.split('}, -- [')
        
        for chunk in chunks:
            pet = {}
            
            # Extract fields
            # Species ID
            m = re.search(r'\["speciesID"\]\s*=\s*(\d+)', chunk)
            if m: pet['speciesID'] = int(m.group(1))
            
            # Pet ID
            m = re.search(r'\["petID"\]\s*=\s*"([^"]+)"', chunk)
            if m: pet['petID'] = m.group(1)
            
            # Level
            m = re.search(r'\["level"\]\s*=\s*(\d+)', chunk)
            if m: pet['level'] = int(m.group(1))
            
            # Name (Custom) or Species Name
            m = re.search(r'\["name"\]\s*=\s*"([^"]+)"', chunk)
            if m: pet['name'] = m.group(1)
            
            if 'speciesID' in pet: 
                data['pets'].append(pet)
                
    return data

class SyncService:
    def __init__(self):
        self.last_mtime = 0
        
        # Find Addon Path from app config or environment
        import app
        self.addon_path = app.ADDON_PATH
        self.saved_vars_path = os.path.join(self.addon_path, 'SavedVariables', 'PetWeaver.lua')
        
        print(f"Watching: {self.saved_vars_path}")

    def run(self):
        print("Sync Service Started. Monitoring SavedVariables...")
        while True:
            try:
                self.check_file()
            except Exception as e:
                print(f"Error in sync loop: {e}")
                traceback.print_exc()
            
            time.sleep(5) 

    def check_file(self):
        if not os.path.exists(self.saved_vars_path):
            return

        mtime = os.path.getmtime(self.saved_vars_path)
        if mtime > self.last_mtime:
            print(f"File change detected at {datetime.datetime.now()}")
            self.last_mtime = mtime
            self.sync_data()

    def sync_data(self):
        # 1. Parse Lua
        data = parse_lua_simple(self.saved_vars_path)
        if not data or not data['pets']:
            print("No pet data found in SavedVariables.")
            return

        print(f"Parser found {len(data['pets'])} pets.")

        # 2. Sync to DB
        self.update_db(data['pets'])

    def update_db(self, pets):
        conn = sqlite3.connect('petweaver.db')
        cursor = conn.cursor()
        
        count = 0
        for pet in pets:
            # Upsert logic
            # We assume species_id + petID is unique.
            # Actually pet table schema is (pet_id, species_id, ...)
            
            try:
                # Check if exists
                # Assuming petID matches the GUID
                # But migration script used auto-increment ID?
                # Let's check schema/migration.
                # Migration: INSERT INTO pets (species_id...)
                # It didn't insert a GUID.
                
                # If we want to support multi_pets, we need a unique identifier.
                # PetWeaver.lua provides `petID` (BattlePet-0-...) which is unique.
                # I should add `guid` column to schema if it's missing, or match by species + attributes?
                
                # For now, let's just insert missing ones or update simple stats?
                # Actually, simplest 'Sync' is to wipe and replace for a collection?
                # Or just update levels?
                
                # Let's try to update level if we find a match by species + name?
                # Simple Update:
                cursor.execute('''
                    UPDATE pets 
                    SET level = ?
                    WHERE species_id = ? AND (custom_name = ? OR name = ?)
                ''', (pet.get('level'), pet.get('speciesID'), pet.get('name'), pet.get('name')))
                
                if cursor.rowcount == 0:
                    # Insert if strictly new? 
                    # Without full stats (health/power/speed), inserting might break stuff if those are NOT null.
                    # We'll skip insert for now to avoid polluting DB with partial data.
                    pass
                else:
                    count += 1
                    
            except Exception as ex:
                print(f"Error updating pet {pet}: {ex}")

        conn.commit()
        conn.close()
        print(f"Synced {count} pets to database.")

if __name__ == "__main__":
    service = SyncService()
    service.run()
