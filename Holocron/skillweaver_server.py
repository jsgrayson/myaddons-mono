from flask import Flask, render_template, jsonify
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '../static')

print(f"DEBUG: SkillWeaver Base Dir: {BASE_DIR}")
print(f"DEBUG: SkillWeaver Template Dir: {TEMPLATE_DIR}")
print(f"DEBUG: SkillWeaver Static Dir: {STATIC_DIR}")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

import psycopg2
from psycopg2.extras import RealDictCursor

# Mock Data (Fallback)
CHARACTERS_DATA = [
    {"name": "Thunderfist", "class": "Shaman", "spec": "Enhancement", "ilvl": 489, "dps": 4250, "color": "primary"},
    {"name": "Shadowmend", "class": "Priest", "spec": "Shadow", "ilvl": 476, "dps": 3890, "color": "secondary"},
    {"name": "Moonfire", "class": "Druid", "spec": "Balance", "ilvl": 492, "dps": 4380, "color": "success"},
    {"name": "Firestorm", "class": "Mage", "spec": "Fire", "ilvl": 485, "dps": 4120, "color": "warning"}
]

def get_db_connection():
    db_url = os.environ.get('DATABASE_URL')
    print(f"DEBUG: Connecting to DB: {db_url}")
    if not db_url:
        return None
    try:
        conn = psycopg2.connect(db_url)
        print("DEBUG: DB Connected")
        return conn
    except Exception as e:
        print(f"DB Connection Error: {e}")
        return None



def get_characters_from_db():
    conn = get_db_connection()
    if not conn:
        return CHARACTERS_DATA
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # Assuming schema based on standard WoW data
        cur.execute("SELECT name, class, spec, item_level as ilvl FROM holocron.characters LIMIT 4")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        if not rows:
            return CHARACTERS_DATA
            
        # Map DB rows to UI format
        chars = []
        colors = ["primary", "secondary", "success", "warning", "info", "danger"]
        for i, row in enumerate(rows):
            chars.append({
                "name": row['name'],
                "class": row['class'],
                "spec": row['spec'] or "Unknown",
                "ilvl": row['ilvl'] or 0,
                "dps": 0, # Placeholder as DB might not have sim dps
                "color": colors[i % len(colors)]
            })
        return chars
    except Exception as e:
        print(f"DB Query Error: {e}")
        return CHARACTERS_DATA

@app.route('/')
def dashboard():
    chars = get_characters_from_db()
    return render_template('skillweaver_dashboard.html', characters=chars)

@app.route('/test_simc')
def test_simc():
    return render_template('test_simc.html')

@app.route('/talents')
def talents():
    return render_template('skillweaver_talents.html')

@app.route('/gear')
def gear():
    return render_template('skillweaver_gear.html')

@app.route('/rotations')
def rotations():
    return render_template('skillweaver_rotations.html')

@app.route('/characters')
def characters():
    chars = get_characters_from_db()
    return render_template('skillweaver_characters.html', characters=chars)

@app.route('/settings')
def settings():
    return render_template('skillweaver_settings.html')

# API Endpoints
@app.route('/api/characters')
def get_characters():
    chars = get_characters_from_db()
    return jsonify({
        "characters": chars
    })

@app.route('/api/talents/<character>')
def get_talents(character):
    return jsonify({
        "character": character,
        "current_build": "Raid - ST",
        "dps": 4250,
        "optimal": 92,
        "suggestions": [
            {"row": 6, "current": "Hailstorm", "suggested": "Elemental Spirits", "gain": 85},
            {"row": 9, "current": "Fire Nova", "suggested": "Crash Lightning", "gain": 52}
        ]
    })

@app.route('/api/gear/<character>')
def get_gear(character):
    return jsonify({
        "character": character,
        "upgrades": [
            {"slot": "Main Hand", "current": "Stormshaper's Blade (493)", "upgrade": "Fyr'alath (496)", "gain": 210, "priority": "high"},
            {"slot": "Trinket 2", "current": "Iridescence (486)", "upgrade": "Smold's Compass (489)", "gain": 95, "priority": "medium"},
            {"slot": "Ring 1", "current": "Crit II", "upgrade": "Haste III", "gain": 42, "priority": "low"}
        ]
    })

import subprocess
import tempfile
import json
import re

@app.route('/api/simc/run/<profile_name>')
def run_simc_profile(profile_name):
    """
    Run a simulation for a specific profile (e.g., T31_Mage_Frost).
    Fetches profile from DB, runs local simc, returns JSON results.
    """
    try:
        # 1. Fetch Profile Content
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
            
        cur = conn.cursor()
        # Try to find by profile name (e.g. T31_Mage_Frost)
        # We stored them as 'Tier31_Standard' with a unique constraint on spec_id/name
        # But import script used 'Tier31_Standard' as profile_name for ALL imports?
        # Let's check the import script logic again. 
        # Ah, import script used: VALUES (..., 'Tier31_Standard', ...)
        # But the lookup_key (e.g. Mage_Frost) was not stored in profile_name?
        # Wait, the unique constraint is (spec_id, profile_name).
        # We need to look up by Class/Spec.
        
        # Let's parse the profile_name input (e.g. Mage_Frost) to find class/spec IDs
        # This is tricky without the ID mapping here.
        # Alternative: Just query the 'content' where it matches the profile signature?
        # Or better: The user will select from a dropdown of available profiles.
        
        # Let's just fetch the profile that matches the input name if we stored it?
        # The import script stored 'Tier31_Standard' as the name.
        # So we need to find the profile for the given spec.
        
        # For now, let's assume the frontend passes the Spec ID or we search by content match?
        # Let's try to find the profile by parsing the name again or just grabbing ANY profile for testing.
        
        # IMPROVEMENT: Let's fetch the profile content based on the 'lookup_key' logic if possible,
        # or just grab the first profile that looks like it.
        
        # Actually, let's just query for the specific profile content if we can identify it.
        # Since I don't have the mapping here, I'll do a text search on the content for the "armory=" or "spec=" line?
        # Or better, let's just list all profiles and let the user pick one by ID.
        
        # But for this specific endpoint, let's assume we pass the ID.
        pass
    except Exception as e:
        pass

    # RE-IMPLEMENTATION with simpler logic:
    # 1. Get profile content from DB using the ID (passed as profile_name for now, or we change route to /api/simc/run/<int:profile_id>)
    # Let's change the route to accept an ID for precision.
    return jsonify({"error": "Use /api/simc/run/<id>"})

@app.route('/api/simc/run_id/<int:profile_id>')
def run_simc_by_id(profile_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT content FROM skillweaver.profiles WHERE profile_id = %s", (profile_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if not row:
            return jsonify({"error": "Profile not found"}), 404
            
        content = row[0]
        
        # 2. Write to Temp File
        with tempfile.NamedTemporaryFile(mode='w', suffix='.simc', delete=False) as tmp:
            tmp.write(content)
            # Add JSON output option
            tmp.write(f"\njson={tmp.name}.json")
            tmp_path = tmp.name
            
        json_path = f"{tmp_path}.json"
        
        # 3. Run SimC (Dockerized)
        # Mount the temp directory to /data in the container
        # Note: On macOS Docker, /var/folders is usually shared by default.
        # We need the directory of the temp file.
        tmp_dir = os.path.dirname(tmp_path)
        tmp_filename = os.path.basename(tmp_path)
        
        # Docker command:
        # docker run --rm -v /host/path:/data simulationcraftorg/simc /data/input.simc json=/data/output.json
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{tmp_dir}:/data",
            "simulationcraftorg/simc",
            f"/data/{tmp_filename}",
            f"json=/data/{tmp_filename}.json"
        ]
        
        print(f"Running Docker SimC: {' '.join(cmd)}")
        try:
            # Add timeout (SimC can be slow, give it 60s)
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                print(f"SimC Docker Failed (Code {result.returncode}): {result.stderr}")
                return jsonify({"error": "SimC failed", "details": result.stderr}), 500
        except subprocess.TimeoutExpired:
            print("SimC timed out after 60s")
            # Check if JSON was created anyway
            if not os.path.exists(json_path):
                return jsonify({"error": "Simulation timed out"}), 504
            # If JSON exists, we might be okay to proceed (SimC sometimes hangs on exit)
            pass
            
        # 4. Parse JSON Output
        with open(json_path, 'r') as f:
            sim_data = json.load(f)
            
        # Cleanup
        os.remove(tmp_path)
        os.remove(json_path)
        
        # Extract key metrics
        dps = sim_data['sim']['statistics']['raid_dps']['mean']
        
        return jsonify({
            "dps": dps,
            "sim_length": sim_data['sim']['options']['max_time'],
            "iterations": sim_data['sim']['options']['iterations'],
            "timestamp": sim_data.get('timestamp', 0)
        })
        
    except Exception as e:
        print(f"SimC Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/profiles')
def list_profiles():
    """List available SimC profiles for the dropdown"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # Join with class/spec tables if they existed, but we only have IDs.
        # We'll just return the IDs and let the frontend guess or use a mapping.
        # Actually, we can return the ID and a generated name.
        cur.execute("SELECT profile_id, class_id, spec_id, profile_name FROM skillweaver.profiles ORDER BY profile_id DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting SkillWeaver on http://127.0.0.1:5003")
    app.run(host='0.0.0.0', port=5003, debug=False)
