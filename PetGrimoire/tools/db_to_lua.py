import sqlite3
import os

# CONFIGURATION
# Relative to tools/
DB_PATH = "../../petweaver.db" 
# Output to repo source first, then we deploy
OUTPUT_FILE = "../PetGrimoire_Data.lua"

def escape_lua(s):
    if not s: return ""
    return str(s).replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")

def generate():
    # Attempt to find DB in different common locations if relative fails
    db_candidates = [
        DB_PATH,
        os.path.join(os.getcwd(), "petweaver.db"),
        os.path.join(os.path.dirname(os.getcwd()), "petweaver.db"),
        os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "petweaver.db")
    ]
    
    final_db_path = None
    for path in db_candidates:
        if os.path.exists(path):
            final_db_path = path
            break
            
    if not final_db_path:
        print(f"❌ Error: Could not find petweaver.db in {db_candidates}")
        return

    print(f"🔌 Connecting to {final_db_path}...")
    
    try:
        conn = sqlite3.connect(final_db_path)
        cursor = conn.cursor()
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Start the Lua file
    lua_lines = []
    lua_lines.append("PetGrimoireDB_Static = { Encounters = {}, Strategies = {} }")

    # 1. DUMP ENCOUNTERS
    print("📦 Exporting Encounters...")
    try:
        cursor.execute("SELECT encounter_id, npc_name, zone, expansion FROM encounters")
        for row in cursor.fetchall():
            id, name, zone, exp = row
            lua_lines.append(f'PetGrimoireDB_Static.Encounters[{id}] = {{ name="{escape_lua(name)}", zone="{escape_lua(zone)}", exp="{escape_lua(exp)}" }}')
    except:
        print("Warning: Encounters table issue.")

    # 2. DUMP STRATEGIES
    print("📜 Exporting Strategies...")
    try:
        cursor.execute("SELECT encounter_id, pet1_species, pet2_species, pet3_species, script, notes FROM strategies")
        for row in cursor.fetchall():
            enc_id, p1, p2, p3, script, notes = row
            # Lua table structure
            entry = f"""table.insert(PetGrimoireDB_Static.Strategies, {{
        encounterId = {enc_id},
        pets = {{ {p1 or 0}, {p2 or 0}, {p3 or 0} }},
        script = [[{script or ""}]],
        notes = "{escape_lua(notes)}"
    }})"""
            lua_lines.append(entry)
    except:
         print("Warning: Strategies table issue.")

    # Write File
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lua_lines))
    
    print(f"✅ SUCCESS: Database compiled to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate()
