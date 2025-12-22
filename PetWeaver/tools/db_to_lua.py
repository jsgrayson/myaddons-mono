import sqlite3
import json
import os

# CONFIGURATION
# Script is in /tools, DB is in root
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "petweaver.db")
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "PetWeaver_StaticDB.lua")

def escape_lua_string(s):
    if not s: return ""
    # Escape quotes and backslashes for Lua strings
    return str(s).replace("\\", "\\\\").replace("\"", "\\\"").replace("\'", "\\\'").replace("\n", "\\n")

def generate_static_db():
    print(f"🔌 Connecting to {DB_PATH}...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
    except Exception as e:
        print(f"❌ Error: Could not connect to DB. {e}")
        return

    lua_out = []
    lua_out.append("-- [[ PETWEAVER STATIC DATABASE ]]")
    lua_out.append("-- Generated from SQLite. DO NOT EDIT MANUALLY.")
    lua_out.append("local addonName, addon = ...")
    lua_out.append("addon.Data = addon.Data or {}")
    lua_out.append("addon.Data.Encounters = {}")
    lua_out.append("addon.Data.Strategies = {}")
    lua_out.append("")

    # ---------------------------------------------------------
    # 1. DUMP ENCOUNTERS (The "Phonebook")
    # ---------------------------------------------------------
    print("📦 Dumping Encounters...")
    try:
        cursor.execute("SELECT encounter_id, npc_name, zone, expansion FROM encounters")
        
        lua_out.append("-- [SECTION 1: ENCOUNTER METADATA]")
        count = 0
        for row in cursor.fetchall():
            enc_id, name, zone, exp = row
            # Lua Format: addon.Data.Encounters[123] = { name="Squirt", zone="Garrison" }
            line = f'addon.Data.Encounters[{enc_id}] = {{ name="{escape_lua_string(name)}", zone="{escape_lua_string(zone)}", exp="{escape_lua_string(exp)}" }}'
            lua_out.append(line)
            count += 1
        print(f"   -> Exported {count} encounters.")
    except sqlite3.OperationalError as e:
         print(f"   -> Warning: Could not dump encounters: {e}")

    # ---------------------------------------------------------
    # 2. DUMP STRATEGIES (The "Grimoire")
    # ---------------------------------------------------------
    print("📜 Dumping Strategies...")
    # We join strategies with encounter_id to ensure we only get valid ones
    # Check if table exists first
    try:
        cursor.execute("""
            SELECT 
                encounter_id, 
                pet1_species, pet2_species, pet3_species,
                pet1_name, pet2_name, pet3_name,
                script, notes
            FROM strategies
            WHERE script IS NOT NULL AND script != ''
        """)

        lua_out.append("\n-- [SECTION 2: BATTLE STRATEGIES]")
        
        # We will buffer strategies by encounter_id to group them locally
        strat_buffer = {} 
        
        for row in cursor.fetchall():
            enc_id, p1, p2, p3, n1, n2, n3, script, notes = row
            
            if enc_id not in strat_buffer:
                strat_buffer[enc_id] = []
                
            # Format the Strategy Object
            # Note: We use [[ ]] for scripts to handle multi-line easily, 
            # but we must be careful if the script contains "]]".
            safe_script = script.replace("]]", "] ]") 
            
            strat_str = f"""    {{
        pets = {{ {p1 or 0}, {p2 or 0}, {p3 or 0} }},
        names = {{ "{escape_lua_string(n1)}", "{escape_lua_string(n2)}", "{escape_lua_string(n3)}" }},
        script = [[{safe_script}]],
        notes = "{escape_lua_string(notes)}"
    }}"""
            strat_buffer[enc_id].append(strat_str)

        # Write buffer to Lua
        strat_count = 0
        for enc_id, strats in strat_buffer.items():
            lua_out.append(f"addon.Data.Strategies[{enc_id}] = {{")
            lua_out.append(",\n".join(strats))
            lua_out.append("}")
            strat_count += len(strats)

        print(f"   -> Exported {strat_count} strategies.")
    except sqlite3.OperationalError as e:
         print(f"   -> Warning: Could not dump strategies: {e}")
    
    # ---------------------------------------------------------
    # 3. FINISH
    # ---------------------------------------------------------
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lua_out))
    
    print(f"✅ SUCCESS! Database written to {OUTPUT_FILE}")
    conn.close()

if __name__ == "__main__":
    generate_static_db()
