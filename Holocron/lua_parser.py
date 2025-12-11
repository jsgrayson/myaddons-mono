import re
import ast
from slpp import decode as slpp_decode

def parse_lua_table(file_path):
    """
    Parses a WoW SavedVariables Lua file into a Python dictionary.
    
    Args:
        file_path (str): Path to the .lua file.
        
    Returns:
        dict: A dictionary representing the Lua table.
    """
    if not file_path:
        return {}
        
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # WoW SavedVariables usually look like:
        # MyAddonDB = {
        #    ["profileKeys"] = {
        #       ["Char - Realm"] = "Default",
        #    },
        #    ["global"] = {
        #       ...
        #    }
        # }
        
        # 1. Extract the main table content (everything after the first " = ")
        # We assume one main variable per file for simplicity, or we split by variable.
        # Let's try to find the first assignment.
        match = re.search(r'^\s*[\w_]+\s*=\s*({.*})', content, re.DOTALL)
        if not match:
            # Fallback: maybe it starts with the brace?
            match = re.search(r'({.*})', content, re.DOTALL)
            
        if not match:
            print(f"Could not find Lua table in {file_path}")
            return {}
            
        lua_str = match.group(1)
        
        # 2. Parse using SLPP
        # SLPP handles native Lua syntax including comments, booleans, nil, and key formats.
        try:
            data = slpp_decode(lua_str)
            return data
        except Exception as e:
            print(f"SLPP parsing failed: {e}")
            return {}
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return {}

