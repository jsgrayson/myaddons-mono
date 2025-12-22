import sqlite3
import re
import os

# CONFIGURATION
LUA_PATH = "../PetWeaver_StaticDB.lua"
DB_PATH = "../../petweaver.db"

def parse_lua_table(content):
    encounters = []
    strategies = []
    
    # regex for encounters: 
    # addon.Data.Encounters[123] = { name="Squirt", zone="Garrison", exp="WOD" }
    enc_pattern = re.compile(r'addon\.Data\.Encounters\[(\d+)\]\s*=\s*{\s*name="(.*?)",\s*zone="(.*?)",\s*exp="(.*?)"\s*}')
    
    # regex for strategies:
    # table.insert(addon.Data.Strategies[123], { ... })
    # This is harder because of multi-line. We'll iterate lines.
    
    lines = content.split('\n')
    current_strat = {}
    in_strat = False
    
    for line in lines:
        # Encounters
        m_enc = enc_pattern.search(line)
        if m_enc:
            encounters.append((int(m_enc.group(1)), m_enc.group(2), m_enc.group(3), m_enc.group(4)))
            continue
            
        # Strategy Start
        if "addon.Data.Strategies[" in line and " = {" in line:
            # New format grouped by ID
            current_encounter_id = int(re.search(r'\[(\d+)\]', line).group(1))
            continue
            
        if "pets = {" in line:
            m_pets = re.search(r'pets = { (\d+), (\d+), (\d+) }', line)
            if m_pets:
                current_strat['pets'] = [int(m_pets.group(1)), int(m_pets.group(2)), int(m_pets.group(3))]
            
        if "names = {" in line:
            m_names = re.search(r'names = { "(.*?)", "(.*?)", "(.*?)" }', line)
            if m_names:
                current_strat['names'] = [m_names.group(1), m_names.group(2), m_names.group(3)]

        if "script = [[" in line:
             # simple single line extraction for now, assuming 1 line or simple block
             script_content = line.split("[[")[1].split("]]")[0]
             current_strat['script'] = script_content
             
        if "notes =" in line:
            current_strat['notes'] = line.split('notes = "')[1].rstrip('",').rstrip('"')
            # End of strat object usually implies flush if we track braces, but let's just push when we have enough
            if 'pets' in current_strat:
                 strategies.append((current_encounter_id, 
                                    current_strat.get('pets', [0,0,0]), 
                                    current_strat.get('names', ["","",""]),
                                    current_strat.get('script', ""), 
                                    current_strat.get('notes', "")))
                 current_strat = {} # Reset
                 
    return encounters, strategies

def recreate_db():
    print(f"📖 Reading {LUA_PATH}...")
    try:
        with open(LUA_PATH, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ Lua file not found.")
        return

    encounters, strategies = parse_lua_table(content)
    print(f"   found {len(encounters)} encounters, {len(strategies)} strategies.")

    print(f"🔧 Rebuilding {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Schema
    c.execute("DROP TABLE IF EXISTS encounters")
    c.execute("CREATE TABLE encounters (encounter_id INTEGER PRIMARY KEY, npc_name TEXT, zone TEXT, expansion TEXT)")
    
    c.execute("DROP TABLE IF EXISTS strategies")
    c.execute("""CREATE TABLE strategies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        encounter_id INTEGER,
        pet1_species INTEGER, pet2_species INTEGER, pet3_species INTEGER,
        pet1_name TEXT, pet2_name TEXT, pet3_name TEXT,
        script TEXT, notes TEXT
    )""")
    
    # Insert
    c.executemany("INSERT INTO encounters VALUES (?,?,?,?)", encounters)
    
    for s in strategies:
        # s = (enc_id, [p1,p2,p3], [n1,n2,n3], script, notes)
        c.execute("INSERT INTO strategies (encounter_id, pet1_species, pet2_species, pet3_species, pet1_name, pet2_name, pet3_name, script, notes) VALUES (?,?,?,?,?,?,?,?,?)",
                  (s[0], s[1][0], s[1][1], s[1][2], s[2][0], s[2][1], s[2][2], s[3], s[4]))
                  
    conn.commit()
    conn.close()
    print("✅ Database Restored.")

if __name__ == "__main__":
    recreate_db()
