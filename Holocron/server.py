# ARCHITECTURAL BOUNDARY: See ARCHITECTURE.md
# Holocron owns dashboard + DeepPockets view.
import sys
print("DEBUG: Starting server.py...", file=sys.stderr)
import os
import json
import psycopg2
from collections import defaultdict
from flask import Flask, request, jsonify, render_template
from datetime import datetime, timezone


app = Flask(__name__)

# --- GATEWAY CONFIGURATION ---
import requests
SERVICE_MAP = {
    "skillweaver": "http://localhost:3000",
    "petweaver":   "http://localhost:5003",
    "goblin":      "http://localhost:8001",
    "holocron":    "http://localhost:8003", # Optional self-ref
}


# In-Memory Sanity State
# Structure: val[character][addon] = { reported: {}, snapshot: {}, prev_snapshot: {}, derived: {}, updated_at: ... }
sanity_state = defaultdict(lambda: defaultdict(dict))


def apply_heuristics(addon, current_snap, prev_snap, reported_ts_iso):
    """
    Derive WARN status based on snapshot changes and staleness.
    Returns: (status, reasons_list_of_objects)
    """
    reasons = [] # List of {code, message}
    status = "OK"
    
    seen_codes = set()
    def add_reason(code, msg):
        if code not in seen_codes:
            seen_codes.add(code)
            reasons.append({"code": code, "message": msg})
    
    # 1. Staleness Check (Global)
    try:
        if reported_ts_iso:
            reported_dt = datetime.fromisoformat(reported_ts_iso.replace("Z", "+00:00"))
            age = datetime.now(timezone.utc) - reported_dt
            if age.total_seconds() > 86400: # 24h
                add_reason("SANITY_STALE_24H", "Report stale (>24h)")
                status = "WARN"
    except Exception:
        pass # Ignore parsing errors

    if not current_snap:
        return status, reasons

    # 2. Addon-Specific Checks
    if addon == "DeepPockets":
        inv = current_snap.get("inv_count", 0)
        money = current_snap.get("money_copper", 0)
        prev_inv = prev_snap.get("inv_count", 0) if prev_snap else 0
        
        # Zero Inventory Rule
        if inv == 0 and prev_inv > 0:
            add_reason("DP_INV_ZERO_AFTER_NONZERO", f"Inventory dropped to 0 (was {prev_inv})")
            status = "WARN"
            
        # Massive Drop Rule (>80%)
        elif prev_inv >= 50 and inv <= (prev_inv * 0.2):
            add_reason("DP_INV_DROP_80", f"Inventory dropped >80% ({prev_inv} -> {inv})")
            status = "WARN"
            
        # Zero Money Rule (Advisory)
        prev_money = prev_snap.get("money_copper", 0) if prev_snap else 0
        if money == 0 and prev_money > 0:
            add_reason("DP_MONEY_ZERO", "Money is 0")
            if status != "FAIL": status = "WARN"

    elif addon == "PetWeaver":
        pets = current_snap.get("owned_pet_count", 0)
        strats = current_snap.get("strategy_count", 0)
        if pets > 0 and strats == 0:
            add_reason("PW_PETS_NO_STRATS", "Pets present but no strategies loaded")
            status = "WARN"

    elif addon == "SkillWeaver":
        spec_active = current_snap.get("active_spec_present", False)
        modules = current_snap.get("module_count", 0)
        if spec_active and modules == 0:
            add_reason("SW_SPEC_NO_MODULES", "Spec detected but no modules active")
            status = "WARN"
            
    return status, reasons

@app.route('/api/v1/sanity/report', methods=['POST'])
def report_sanity():
    """
    Ingest a sanity report.
    Payload:
    {
        "character": "Name-Realm",
        "addon": "DeepPockets",
        "status": "OK|WARN|FAIL",
        "snapshot": { ... },   # Optional
        "timestamp": "ISO8601"
    }
    """
    try:
        data = request.json
        addon = data.get("addon")
        char_name = data.get("character", "Unknown-Realm")
        
        if not addon:
            return jsonify({"error": "Missing addon name"}), 400
            
        # Get existing state for rotation
        current_state = sanity_state[char_name].get(addon, {})
        
        # Rotate Snapshot
        new_snap = data.get("snapshot")
        if new_snap:
            # If we have a new snapshot, move current to prev
            if "snapshot" in current_state:
                current_state["prev_snapshot"] = current_state["snapshot"]
            current_state["snapshot"] = new_snap
            
        # Update Reported
        current_state["reported"] = {
            "status": data.get("status", "OK"),
            "timestamp": data.get("timestamp"),
            "details": data.get("details", {})
        }
        current_state["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        # Save back
        sanity_state[char_name][addon] = current_state
        
        print(f"Confidence Report [{char_name}][{addon}]: {data.get('status')}")
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error processing sanity report: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/sanity/status', methods=['GET'])
def get_sanity_status():
    """
    Return aggregated confidence status with derived heuristics.
    Structure:
    {
        "overall": "OK|WARN|FAIL",
        "characters": { ... }
    }
    """
    response = {
        "overall": "OK",
        "characters": {}
    }
    
    global_status_val = 0 # 0=OK, 1=WARN, 2=FAIL
    
    for char_name, addons in sanity_state.items():
        char_entry = {"overall": "OK", "addons": {}}
        char_max_val = 0
        
        for addon, state in addons.items():
            reported = state.get("reported", {})
            rep_status = reported.get("status", "OK")
            rep_ts = reported.get("timestamp")
            
            # Run Derived Heuristics
            curr_snap = state.get("snapshot")
            prev_snap = state.get("prev_snapshot")
            
            der_status, reasons = apply_heuristics(addon, curr_snap, prev_snap, rep_ts)
            
            # Final Status Calculation
            # Policy: FAIL > WARN > OK
            # GUARD: A reported FAIL status MUST NOT be downgraded.
            
            final_status = "OK"
            
            if rep_status == "FAIL":
                final_status = "FAIL"
            elif rep_status == "WARN":
                final_status = "WARN"
            
            # Only upgrade to WARN if we aren't already FAIL
            if der_status == "WARN" and final_status != "FAIL":
                 final_status = "WARN"
                 
            # Add derived reasons
            entry = {
                "status": final_status,
                "reported_status": rep_status,
                "derived_status": der_status,
                "reasons": reasons,
                "timestamp": rep_ts
            }
            
            char_entry["addons"][addon] = entry
            
            # Update Char Aggregate
            val = 2 if final_status == "FAIL" else 1 if final_status == "WARN" else 0
            if val > char_max_val: char_max_val = val
            
        char_entry["overall"] = "FAIL" if char_max_val == 2 else "WARN" if char_max_val == 1 else "OK"
        response["characters"][char_name] = char_entry
        
        if char_max_val > global_status_val: global_status_val = char_max_val

    response["overall"] = "FAIL" if global_status_val == 2 else "WARN" if global_status_val == 1 else "OK"
    return jsonify(response)

@app.route('/api/v1/deeppockets/inventory', methods=['GET'])
def get_deeppockets_inventory():
    """
    Local handler for DeepPockets inventory.
    Reads synced JSON data and returns it.
    """
    try:
        # Path to the synced file
        json_path = os.path.join(os.path.dirname(__file__), 'synced_data', 'deeppockets_inventory.json')
        
        if not os.path.exists(json_path):
            return jsonify({"error": "Inventory data not synced yet"}), 404
            
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        return jsonify(data)
    except Exception as e:
        print(f"Error serving inventory: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/<service>/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway_proxy(service, subpath):
    """
    Central API Gateway Logic.
    Routes /api/v1/<service>/<path> -> <SERVICE_URL>/api/<path>
    """
    upstream_base = SERVICE_MAP.get(service)
    if not upstream_base:
        return jsonify({"error": f"Service '{service}' not found"}), 404
    
    # Tag request for logging
    request.upstream_service = service


    # Construct upstream URL
    # Incoming: /api/v1/petweaver/pets
    # Outgoing: http://localhost:8001/api/pets
    upstream_url = f"{upstream_base}/api/{subpath}"
    
    try:
        # Forward request
        resp = requests.request(
            method=request.method,
            url=upstream_url,
            headers={k:v for k,v in request.headers if k.lower() != 'host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=30
        )
        
        # Return upstream response
        # Exclude hop-by-hop headers
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
                   
        return (resp.content, resp.status_code, headers)
        
    except requests.exceptions.RequestException as e:
        print(f"Gateway Error [{service}]: {e}")
        return jsonify({"error": "Upstream service unavailable"}), 502

import time
import uuid

# --- MIDDLEWARE & LOGGING ---
@app.before_request
def start_timer():
    request.start_time = time.time()
    # Ensure X-Request-Id exists
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        request_id = str(uuid.uuid4())
    request.request_id = request_id

@app.after_request
def log_request(response):
    # Calculate latency
    latency_ms = (time.time() - request.start_time) * 1000
    
    # Structured Log
    log_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "requestId": getattr(request, 'request_id', 'unknown'),
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "latencyMs": round(latency_ms, 2),
        "clientIp": request.remote_addr,
        "userAgent": request.user_agent.string,
    }
    
    # Add upstream info if available (set by gateway_proxy)
    if hasattr(request, 'upstream_service'):
        log_data["upstreamService"] = request.upstream_service
        
    print(json.dumps(log_data), file=sys.stdout)
    
    # Add Request-Id to response headers
    response.headers['X-Request-Id'] = getattr(request, 'request_id', 'unknown')
    return response

# --- DB CONNECTION (Legacy/Internal) ---
def get_db_connection():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        # Provide helpful error message if DATABASE_URL is not set
        raise ValueError(
            "DATABASE_URL environment variable is not set. "
            "Please set it in your environment or .env file. "
            "Example: export DATABASE_URL='postgresql://user:pass@localhost/holocron'"
        )
    conn = psycopg2.connect(db_url)
    return conn

# --- SYSTEM HEALTH & STATUS ---
@app.route('/readyz')
def readyz():
    """
    Checks health of all upstream services.
    Returns aggregated status.
    """
    results = {}
    overall_ok = True
    
    for name, base_url in SERVICE_MAP.items():
        if name == 'holocron': continue # Skip self
        
        start = time.time()
        try:
            # Determine health endpoint based on service
            health_path = "/healthz"
            if name in ["skillweaver", "petweaver"]:
                health_path = "/api/status"
            elif name == "goblin":
                health_path = "/"
            
            # Short timeout is critical for health checks
            resp = requests.get(f"{base_url}{health_path}", timeout=1.5)
            latency = (time.time() - start) * 1000
            
            is_ok = resp.status_code == 200
            results[name] = {
                "ok": is_ok,
                "latency_ms": round(latency, 2),
                "status_code": resp.status_code
            }
            if not is_ok: overall_ok = False
            
        except Exception as e:
            results[name] = {
                "ok": False,
                "error": str(e)
            }
            overall_ok = False
            
    status_code = 200 if overall_ok else 503
    return jsonify({
        "ok": overall_ok,
        "services": results
    }), status_code


# --- SERVER SYSTEM ENDPOINTS ---
@app.route('/api/v1/system/sync_status')
def system_sync_status():
    """
    Returns the last time data was synced.
    Reads from local sync_status.json written by sync_addon_data.py.
    """
    try:
        with open("sync_status.json", "r") as f:
            status = json.load(f)
            
        # Parse timestamp to determine staleness
        # (MVP: Just return raw data, frontend handles calculation, or we do it here)
        # Let's add server-side calc for consistency
        last_synced = datetime.fromisoformat(status["last_synced_at"].replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        age = (now - last_synced).total_seconds()
        
        # Default stale threshold: 6 hours
        STALE_THRESHOLD = 21600 
        status["is_stale"] = age > STALE_THRESHOLD
        status["age_seconds"] = int(age)
        status["stale_after_seconds"] = STALE_THRESHOLD
        
        response = jsonify(status)
        response.headers['Cache-Control'] = 'no-store'
        return response
        
    except FileNotFoundError:
        # Never synced
        return jsonify({
            "last_synced_at": None,
            "is_stale": True,
            "source": "none"
        })
    except Exception as e:
        print(f"Sync status error: {e}")
        return jsonify({"error": str(e)}), 500




@app.route('/api/stats')
def api_stats():
    """Returns stat weights from DB or JSON fallback."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT spec, stat_string FROM skillweaver.stat_weights")
        rows = cur.fetchall()
        data = [{"spec": r[0], "stat_string": r[1]} for r in rows]
        cur.close()
        conn.close()
        return jsonify({"source": "db", "data": data})
    except Exception as e:
        print(f"DB Error (Stats): {e}")
        # Fallback
        try:
            with open("scraped_stats.json", "r") as f:
                return jsonify({"source": "json", "data": json.load(f)})
        except FileNotFoundError:
            return jsonify({"source": "none", "data": []})

@app.route('/api/talents')
def api_talents():
    """Returns talent strings from DB or JSON fallback."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT spec, build_name, talent_string FROM skillweaver.talent_builds")
        rows = cur.fetchall()
        data = [{"spec": r[0], "build_name": r[1], "talent_string": r[2]} for r in rows]
        cur.close()
        conn.close()
        return jsonify({"source": "db", "data": data})
    except Exception as e:
        print(f"DB Error (Talents): {e}")
        # Fallback
        try:
            with open("scraped_talents.json", "r") as f:
                return jsonify({"source": "json", "data": json.load(f)})
        except FileNotFoundError:
            return jsonify({"source": "none", "data": []})

@app.route('/api/battles')
def api_battles():
    """Returns recorded battles from DB or JSON fallback."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM petweaver.battles LIMIT 50") # Placeholder schema
        rows = cur.fetchall()
        # Mock DB response for now as schema might vary
        data = [] 
        cur.close()
        conn.close()
        return jsonify({"source": "db", "data": data})
    except Exception as e:
        print(f"DB Error (Battles): {e}")
        # Fallback
        try:
            with open("recorded_battles.json", "r") as f:
                # Read line by line if it's JSONL, or load if JSON array
                # The recorder appends lines, so it's likely JSONL-ish or just appended dicts
                # Let's assume valid JSON array or fix it
                # Actually recorder.py appends `json.dumps(data) + "\n"`.
                # So we need to parse lines.
                data = []
                for line in f:
                    if line.strip():
                        data.append(json.loads(line))
                return jsonify({"source": "json", "data": data})
        except FileNotFoundError:
            return jsonify({"source": "none", "data": []})

@app.route('/search')
def search():
    query = request.args.get('q')
    results = []
    if query:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            # Join items with storage_locations and characters to get full context
            sql = """
                SELECT i.name, i.count, s.container_type, s.container_index, c.name
                FROM holocron.items i
                JOIN holocron.storage_locations s ON i.location_id = s.location_id
                JOIN holocron.characters c ON s.character_guid = c.character_guid
                WHERE i.name ILIKE %s
                LIMIT 50
            """
            cur.execute(sql, (f'%{query}%',))
            rows = cur.fetchall()
            for row in rows:
                results.append({
                    "name": row[0],
                    "count": row[1],
                    "container_type": row[2],
                    "container_index": row[3],
                    "character_name": row[4]
                })
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Search error: {e}")
            
    return render_template('index.html', query=query, results=results)

@app.route('/liquidation')
def liquidation():
    assets = []
    pets = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get Liquidatable Assets
        cur.execute("SELECT * FROM holocron.view_liquidatable_assets LIMIT 20")
        rows = cur.fetchall()
        for row in rows:
            assets.append({
                "name": row[0],
                "count": row[1],
                "market_value": row[2],
                "total_value": row[3],
                "container_type": row[4],
                "character_name": row[5]
            })

        # Get Safe to Sell Pets
        cur.execute("SELECT name, count FROM holocron.view_safe_to_sell_pets LIMIT 20")
        rows = cur.fetchall()
        for row in rows:
            pets.append({
                "name": row[0],
                "count": row[1]
            })

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Liquidation error: {e}")

    return render_template('liquidation.html', assets=assets, pets=pets)

@app.route('/api/generate_jobs', methods=['POST'])
def generate_jobs():
    """
    Generates logistics jobs based on the current 'Liquidatable Assets' view.
    For MVP: Moves everything to a hardcoded 'AuctionAlt' (placeholder GUID).
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 1. Get all liquidatable assets
        cur.execute("SELECT name, count, character_name FROM holocron.view_liquidatable_assets")
        rows = cur.fetchall()
        
        jobs_created = 0
        for row in rows:
            # name = row[0]
            count = row[1]
            # character_name = row[2]
            
            # In a real app, we'd lookup GUIDs. For now, we mock the insertion.
            # cur.execute("INSERT INTO holocron.logistics_jobs ...")
            jobs_created += 1

        # Mock insertion for demonstration
        print(f"Generated {jobs_created} jobs.")

        cur.close()
        conn.close()
        return jsonify({"status": "success", "jobs_created": jobs_created}), 200
    except Exception as e:
        print(f"Job generation error: {e}")
        return jsonify({"error": str(e)}), 500

# --- NAVIGATOR MODULE ---
from navigator_engine import NavigatorEngine

# Initialize Navigator engine once
navigator_engine = NavigatorEngine()
navigator_engine.load_mock_data()

@app.route('/api/navigator/activities')
def navigator_activities():
    """
    Get prioritized activities with scores
    Query params:
        include_owned (bool): Include already-collected items
        min_available (int): Minimum available characters
    """
    include_owned = request.args.get('include_owned', 'false').lower() == 'true'
    min_available = request.args.get('min_available', 1, type=int)
    
    activities = navigator_engine.get_prioritized_activities(
        include_owned=include_owned,
        min_available=min_available
    )
    
    stats = navigator_engine.get_statistics()
    
    return jsonify({
        "activities": activities,
        "statistics": stats,
        "urgent_count": len(navigator_engine.get_urgent_activities())
    })

@app.route('/api/navigator/urgent')
def navigator_urgent():
    """Get top priority activities (score >= 80)"""
    urgent = navigator_engine.get_urgent_activities(limit=10)
    return jsonify({"urgent_activities": urgent})

@app.route('/navigator')
def navigator():
    """Navigator UI page"""
    # Get prioritized activities
    activities_data = navigator_engine.get_prioritized_activities(min_available=1)
    stats = navigator_engine.get_statistics()
    urgent = navigator_engine.get_urgent_activities()
    
    # Format for template (keep compatible with existing HTML)
    activities = []
    for act in activities_data[:20]:  # Top 20
        activities.append({
            "instance_name": act["instance"],
            "drop_name": act["drop"],
            "drop_type": act["type"],
            "expansion": act["expansion"],
            "type": act['instance_type'],
            "available_count": act["available_chars"],
            "score": act["score"],
            "priority": act["priority"]
        })
    
    return render_template('navigator.html', 
                          activities=activities,
                          statistics=stats,
                          urgent_count=len(urgent))

# --- PATHFINDER MODULE ---
from pathfinder_engine import PathfinderEngine

# Initialize Pathfinder engine once
pathfinder_engine = PathfinderEngine(None)
pathfinder_engine.load_mock_data()

@app.route('/api/pathfinder/route')
def pathfinder_route():
    """
    Calculate shortest travel route between zones
    Query params:
        source (int): Source zone ID
        dest (int): Destination zone ID
        char_class (str): Optional character class (Mage, Engineer, Druid)
        hearthstone (bool): Whether hearthstone is available
    """
    source = request.args.get('source', type=int)
    dest = request.args.get('dest', type=int)
    char_class = request.args.get('char_class', None)
    hearthstone = request.args.get('hearthstone', 'true').lower() == 'true'
    
    if not source or not dest:
        return jsonify({"error": "Missing 'source' or 'dest' parameters"}), 400
    
    result = pathfinder_engine.find_shortest_path(
        source, dest,
        character_class=char_class,
        hearthstone_available=hearthstone
    )
    
    return jsonify(result)

@app.route('/api/pathfinder/reachable')
def pathfinder_reachable():
    """
    Get all zones reachable from a source within max_time
    Query params:
        source (int): Source zone ID
        max_time (int): Maximum travel time in seconds (default: 120)
    """
    source = request.args.get('source', type=int)
    max_time = request.args.get('max_time', 120, type=int)
    
    if not source:
        return jsonify({"error": "Missing 'source' parameter"}), 400
    
    reachable = pathfinder_engine.get_reachable_zones(source, max_time)
    return jsonify({"source": source, "max_time": max_time, "reachable": reachable})

@app.route('/pathfinder')
def pathfinder():
    # Get list of zones for dropdowns
    zones = [
        {"id": 84, "name": "Stormwind City"},
        {"id": 85, "name": "Orgrimmar"},
        {"id": 1670, "name": "Oribos"},
        {"id": 2112, "name": "Valdrakken"},
        {"id": 2339, "name": "Dornogal"},
        {"id": 1220, "name": "Legion Dalaran"},
        {"id": 125, "name": "Dalaran (Northrend)"},
    ]
    return render_template('pathfinder.html', zones=zones)

# --- KNOWLEDGE POINT TRACKER ---
from knowledge_tracker import KnowledgeTracker, Profession

# Initialize Knowledge tracker once
knowledge_tracker = KnowledgeTracker()
knowledge_tracker.load_mock_data()

@app.route('/api/knowledge/checklist')
def knowledge_checklist():
    """
    Get knowledge point checklist for a profession
    Query params:
        profession (str): Profession name (e.g., "Blacksmithing")
        character (str): Optional character GUID
    """
    profession_name = request.args.get('profession', 'Blacksmithing')
    character_guid = request.args.get('character', None)
    
    try:
        profession = Profession[profession_name.upper().replace(" ", "_")]
    except KeyError:
        return jsonify({"error": f"Invalid profession: {profession_name}"}), 400
    
    checklist = knowledge_tracker.get_checklist(profession, character_guid)
    return jsonify(checklist)

@app.route('/api/knowledge/complete', methods=['POST'])
def knowledge_complete():
    """
    Mark a knowledge source as complete/incomplete
    POST body: {source_id: int, character: str, complete: bool}
    """
    data = request.get_json()
    source_id = data.get('source_id')
    character_guid = data.get('character')
    complete = data.get('complete', True)
    
    if not source_id or not character_guid:
        return jsonify({"error": "Missing source_id or character"}), 400
    
    if complete:
        knowledge_tracker.mark_complete(source_id, character_guid)
    else:
        knowledge_tracker.mark_incomplete(source_id, character_guid)
    
    return jsonify({"success": True, "source_id": source_id, "complete": complete})

@app.route('/knowledge')
def knowledge():
    """Knowledge Point Tracker UI"""
    # Get checklist for default profession
    checklist = knowledge_tracker.get_checklist(Profession.BLACKSMITHING, "GUID-MainWarrior")
    
    return render_template('knowledge.html', 
                          profession="Blacksmithing",
                          checklist=checklist)

# --- UTILITY TRACKER ---
from utility_tracker import UtilityTracker, CollectionType

# Initialize Utility tracker once
utility_tracker = UtilityTracker()
utility_tracker.load_mock_data()

@app.route('/api/utility/summary')
def utility_summary():
    """Get collection summary (mounts, toys, spells)"""
    summary = utility_tracker.get_summary()
    return jsonify(summary)

@app.route('/api/utility/missing')
def utility_missing():
    """
    Get missing items for a collection type
    Query params:
        type (str): Collection type (mount, toy, spell)
        limit (int): Max items to return (default: 10)
    """
    collection_type_str = request.args.get('type', 'mount').upper()
    limit = request.args.get('limit', 10, type=int)
    
    try:
        collection_type = CollectionType[collection_type_str]
    except KeyError:
        return jsonify({"error": f"Invalid collection type: {collection_type_str}"}), 400
    
    missing = utility_tracker.get_missing_items(collection_type, limit)
    return jsonify({"type": collection_type.value, "missing": missing})

@app.route('/utility')
def utility():
    """Utility Tracker UI"""
    summary = utility_tracker.get_summary()
    missing_mounts = utility_tracker.get_missing_items(CollectionType.MOUNT, 5)
    
    return render_template('utility.html',
                          summary=summary,
                          missing_mounts=missing_mounts)

# --- GOBLIN BRAIN MODULE ---
from goblin_engine import GoblinEngine, ItemType, GoblinEngineExpanded

# Initialize Goblin engine once
goblin_engine = GoblinEngineExpanded()
goblin_engine.load_mock_data()

@app.route('/api/goblin/dashboard')
def goblin_dashboard():
    """Get market analysis dashboard data"""
    analysis = goblin_engine.analyze_market()
    sniper = goblin_engine.get_sniper_list()
    
    return jsonify({
        "analysis": analysis,
        "sniper": sniper
    })

@app.route('/api/goblin/crafting')
def goblin_crafting():
    """Get prioritized crafting queue"""
    analysis = goblin_engine.analyze_market()
    
    # Filter for profitable items only
    queue = [
        opp for opp in analysis['opportunities'] 
        if opp['profit'] > 0 and opp['sale_rate'] >= 0.2
    ]
    
    return jsonify({"queue": queue})

@app.route('/api/goblin/tsm_export', methods=['POST'])
def goblin_tsm_export():
    """
    Generate TSM import string for a list of items.
    POST body: { "items": [123, 456] }
    """
    data = request.get_json()
    items = data.get('items', [])
    
    if not items:
        # If no items provided, default to "Safe to Sell" list from DB/View
        # For MVP, we'll use a mock list or fetch from the liquidation view logic
        # Let's re-use the logic from /liquidation route but just get IDs
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT item_id FROM holocron.view_liquidatable_assets") # Assuming view has item_id
            rows = cur.fetchall()
            items = [r[0] for r in rows]
            cur.close()
            conn.close()
        except Exception:
            # Fallback mock
            items = [198765, 194820, 12345] 
            
    tsm_string = goblin_engine.generate_tsm_string(items)
    return jsonify({"tsm_string": tsm_string})

@app.route('/goblin')
def goblin():
    """Goblin Brain UI"""
    analysis = goblin_engine.analyze_market()
    score = goblin_engine.get_score()
    
    return render_template('goblin.html',
                          analysis=analysis,
                          score=score)

# ============================================================================
# GoblinAI v2.0 API Endpoints (For addon integration)
# ============================================================================

@app.route('/api/goblin/prices')
def goblin_prices():
    """
    Get market prices for all items (DBMarket equivalent)
    Returns: {"prices": {itemID: price, ...}}
    """
    try:
        # Get market prices from goblin_engine
        analysis = goblin_engine.analyze_market()
        
        # Build price dict
        prices = {}
        for opp in analysis.get('opportunities', []):
            item_id = opp.get('item_id')
            market_value = opp.get('market_value', 0)
            if item_id and market_value:
                prices[item_id] = market_value
        
        return jsonify({"prices": prices})
    except Exception as e:
        print(f"Error in /api/goblin/prices: {e}")
        return jsonify({"prices": {}})

@app.route('/api/goblin/opportunities')
def goblin_opportunities():
    """
    Get AI-recommended flip opportunities from ML models
    Returns: {"opportunities": [{itemID, buyPrice, sellPrice, profit, roi, confidence}, ...]}
    """
    try:
        analysis = goblin_engine.analyze_market()
        opportunities = []
        
        for opp in analysis.get('opportunities', []):
            if opp.get('profit', 0) > 0:
                opportunities.append({
                    "itemID": opp.get('item_id'),
                    "buyPrice": opp.get('avg_buyout', 0),
                    "sellPrice": opp.get('market_value', 0),
                    "profit": opp.get('profit', 0),
                    "roi": opp.get('profit_margin', 0),
                    "predictedDemand": "high" if opp.get('sale_rate', 0) > 0.5 else "medium",
                    "confidence": opp.get('sale_rate', 0.5),
                })
        
        # Sort by profit
        opportunities.sort(key=lambda x: x['profit'], reverse=True)
        
        return jsonify({"opportunities": opportunities[:50]})  # Top 50
    except Exception as e:
        print(f"Error in /api/goblin/opportunities: {e}")
        return jsonify({"opportunities": []})

@app.route('/api/goblin/scan', methods=['POST'])
def goblin_scan_upload():
    """
    Upload AH scan data from addon for ML training
    POST body: {timestamp, realm, faction, character, scan: [{item_id, price, quantity}, ...]}
    """
    try:
        data = request.get_json()
        
        if not data or 'scan' not in data:
            return jsonify({"error": "Missing scan data"}), 400
        
        # Store scan data in database
        conn = get_db_connection()
        cur = conn.cursor()
        
        realm = data.get('realm', 'Unknown')
        faction = data.get('faction', 'Unknown')
        character = data.get('character', 'Unknown')
        timestamp = data.get('timestamp', 0)
        
        # Insert scan metadata
        cur.execute("""
            INSERT INTO auctionhouse.scans (realm, faction, character, timestamp, item_count)
            VALUES (%s, %s, %s, to_timestamp(%s), %s)
            RETURNING scan_id
        """, (realm, faction, character, timestamp, len(data['scan'])))
        
        scan_id = cur.fetchone()[0]
        
        # Insert individual items
        for item in data['scan']:
            cur.execute("""
                INSERT INTO auctionhouse.scan_items (scan_id, item_id, price, quantity)
                VALUES (%s, %s, %s, %s)
            """, (scan_id, item.get('item_id'), item.get('price'), item.get('quantity', 1)))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"status": "success", "scan_id": scan_id, "items": len(data['scan'])})
    except Exception as e:
        print(f"Error in /api/goblin/scan: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/goblin/trends')
def goblin_trends():
    """
    Get ML-powered market trend predictions
    Returns: {"trends": [{itemID, trend, prediction, confidence, timeframe}, ...]}
    """
    try:
        # This would integrate with ML model for predictions
        # For now, return mock trends
        trends = [
            {
                "itemID": 210814,  # Algari Mana Potion
                "trend": "rising",
                "prediction": "spike_expected",
                "confidence": 0.78,
                "timeframe": "24h",
            },
            {
                "itemID": 211515,  # Null Stone
                "trend": "stable",
                "prediction": "hold_steady",
                "confidence": 0.65,
                "timeframe": "48h",
            }
        ]
        
        return jsonify({"trends": trends})
    except Exception as e:
        print(f"Error in /api/goblin/trends: {e}")
        return jsonify({"trends": []})

@app.route('/api/goblin/portfolio')
def goblin_portfolio():
    """
    Get portfolio value across all characters
    Returns: {"portfolio": {totalValue, todayProfit, weekProfit, activeAuctions, pendingSales}}
    """
    try:
        # Query database for character portfolio
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get total AH value
        cur.execute("""
            SELECT COALESCE(SUM(buyout), 0) as total_value,
                   COUNT(*) as active_auctions
            FROM auctionhouse.auctions
            WHERE owner = %s
        """, (request.args.get('character', 'Unknown'),))
        
        row = cur.fetchone()
        total_value = row[0] if row else 0
        active_auctions = row[1] if row else 0
        
        cur.close()
        conn.close()
        
        portfolio = {
            "totalValue": int(total_value),
            "todayProfit": 0,  # Would calculate from ledger
            "weekProfit": 0,   # Would calculate from ledger
            "activeAuctions": active_auctions,
            "pendingSales": int(total_value * 0.7),  # Estimate
        }
        
        return jsonify({"portfolio": portfolio})
    except Exception as e:
        print(f"Error in /api/goblin/portfolio: {e}")
        return jsonify({"portfolio": {
            "totalValue": 0,
            "todayProfit": 0,
            "weekProfit": 0,
            "activeAuctions": 0,
            "pendingSales": 0,
        }})

@app.route('/api/goblin/auto_groups')
def goblin_auto_groups():
    """
    Generate AI-optimized trading groups based on market analysis
    Uses ML engine to classify items and recommend operations
    """
    try:
        from goblin_ml_engine import generate_auto_groups_endpoint
        
        # Get market analysis
        analysis = goblin_engine.analyze_market()
        
        # Generate auto-groups using ML
        result = generate_auto_groups_endpoint(analysis.get('opportunities', []))
        
        return jsonify(result)
    except Exception as e:
        print(f"Error in /api/goblin/auto_groups: {e}")
        return jsonify({"groups": [], "error": str(e)})

@app.route('/api/goblin/predictions')
def goblin_predictions():
    """
    Get news-based market shift predictions
    Scans Wowhead, MMO-Champion, Blizzard news for upcoming changes
    """
    try:
        from goblin_news_engine import get_market_predictions_endpoint
        
        result = get_market_predictions_endpoint()
        
        return jsonify(result)
    except Exception as e:
        print(f"Error in /api/goblin/predictions: {e}")
        return jsonify({"predictions": [], "stockpile_now": [], "error": str(e)})

@app.route('/api/goblin/dominate')
def goblin_dominate():
    """
    Get aggressive market domination strategies
    Reset sniping, monopoly control, competitor analysis
    """
    try:
        from goblin_domination import get_domination_strategies
        
        # Get latest scan data
        analysis = goblin_engine.analyze_market()
        
        result = get_domination_strategies(analysis.get('opportunities', []))
        
        return jsonify(result)
    except Exception as e:
        print(f"Error in /api/goblin/dominate: {e}")
        return jsonify({"error": str(e)})


# --- CODEX MODULE ---
from codex_engine import CodexEngine, Role

# Initialize Codex engine once
codex_engine = CodexEngine()
# Use mock data by default to avoid scraping on startup
codex_engine.load_from_wowhead_json()
# try:
#     codex_engine.load_real_data()
# except Exception as e:
#     print(f"Error loading real data: {e}. Falling back to mock.")
#     codex_engine.load_mock_data()

@app.route('/api/codex/instance/<int:instance_id>')
def codex_instance(instance_id):
    """Get instance details"""
    instance = codex_engine.get_instance(instance_id)
    if not instance:
        return jsonify({"error": "Instance not found"}), 404
    return jsonify(instance)

@app.route('/api/codex/encounter/<int:encounter_id>')
@app.route('/api/codex/encounter/<int:encounter_id>')
def codex_encounter(encounter_id):
    """Get encounter details"""
    encounter = codex_engine.get_encounter(encounter_id)
    if not encounter:
        return jsonify({"error": "Encounter not found"}), 404
    return jsonify(encounter)

@app.route('/api/codex/quest/<int:quest_id>')
def codex_quest(quest_id):
    """Get quest details and status"""
    char_guid = request.args.get('character_guid') # Optional: Check completion for specific char
    quest = codex_engine.get_quest(quest_id, char_guid)
    if not quest:
        return jsonify({"error": "Quest not found"}), 404
    return jsonify(quest)

@app.route('/api/codex/campaign')
def codex_campaign():
    """Get campaign progress"""
    campaign_name = request.args.get('name', 'The War Within')
    char_guid = request.args.get('character_guid')
    
    if not char_guid:
        return jsonify({"error": "character_guid required"}), 400
        
    progress = codex_engine.get_campaign_progress(campaign_name, char_guid)
    return jsonify(progress)
    """Get encounter details"""
    encounter = codex_engine.get_encounter(encounter_id)
    if not encounter:
        return jsonify({"error": "Encounter not found"}), 404
    return jsonify(encounter)

@app.route('/codex')
def codex_page():
    """Render the Codex Dashboard"""
    # Fetch all characters
    characters = codex_engine.get_all_characters()
    
    # Define Campaigns to Track
    # In the future, this could be dynamic or user-configured
    campaign_names = ["The War Within", "Dragonflight"]
    campaign_columns = [{"name": c} for c in campaign_names]
    
    matrix = []
    campaign_summaries = {} # Map name -> {progress, status}
    
    for char in characters:
        char_row = {
            "character": {
                "name": char["name"], 
                "realm": char["realm"], 
                "class": char["class"]
            },
            "campaigns": []
        }
        
        for camp_name in campaign_names:
            progress = codex_engine.get_campaign_progress(camp_name, char["character_guid"])
            
            # Determine state/status
            state = "locked"
            status_text = "Not Started"
            percent = 0
            step_label = "0/?"
            
            if "error" not in progress:
                percent = progress["percent"]
                step_label = progress["progress"] # "3/5"
                
                if percent == 100:
                    state = "done"
                    status_text = "Completed"
                elif percent > 0:
                    state = "in_progress"
                    # Find next quest
                    for q in progress["quests"]:
                        if not q["completed"]:
                            status_text = f"Next: {q['title']}"
                            break
                else:
                    state = "locked" # Or just not started
                    status_text = "Not Started"
                
                # Update Summary (Max Progress)
                if camp_name not in campaign_summaries or percent > campaign_summaries[camp_name]["percent"]:
                    campaign_summaries[camp_name] = {
                        "name": camp_name,
                        "progress": percent,
                        "status": status_text
                    }
            
            char_row["campaigns"].append({
                "state": state,
                "step_label": step_label,
                "percent": percent,
                "status_text": status_text
            })
            
        matrix.append(char_row)
    
    # Convert summaries to list
    campaigns_list = list(campaign_summaries.values())
    if not campaigns_list:
        # Fallback if no data found
        campaigns_list = [{"name": c, "progress": 0, "status": "No Data"} for c in campaign_names]
    
    return render_template('codex.html', campaigns=campaigns_list, matrix=matrix, campaign_columns=campaign_columns)
# --- VAULT VISUALIZER ---
from vault_engine import VaultEngine, VaultCategory

# Initialize Vault engine once
vault_engine = VaultEngine()
vault_engine.load_mock_data()

@app.route('/api/vault/status')
def vault_status():
    """Get current vault status"""
    status = vault_engine.get_status()
    return jsonify(status)

@app.route('/api/vault/update', methods=['POST'])
def vault_update():
    """
    Update vault progress (Mock/Debug)
    POST body: {category: "Raid", slot_id: 1, progress: 3}
    """
    data = request.get_json()
    # In a real app, this would update the DB
    # For now, just return success
    return jsonify({"success": True, "message": "Vault updated (Mock)"})

@app.route('/vault')
def vault():
    """Vault Visualizer UI"""
    status = vault_engine.get_status()
    return render_template('vault.html', status=status)

# --- THE SCOUT MODULE ---
from scout_engine import ScoutEngine, EventType

# Initialize Scout engine once
scout_engine = ScoutEngine()
scout_engine.load_mock_data()

@app.route('/api/scout/alerts')
def scout_alerts():
    """Get active push alerts"""
    alerts = scout_engine.get_alerts()
    return jsonify({"alerts": alerts})

@app.route('/scout')
def scout():
    """The Scout UI - Push Alerts"""
    alerts = scout_engine.get_alerts()
    return render_template('scout.html', alerts=alerts)
    return render_template('scout.html', alerts=alerts)

    return render_template('scout.html', alerts=alerts)

# --- DEEPPOCKETS MODULE ---
from deeppockets_engine import DeepPocketsEngine

# Initialize DeepPockets engine once
deeppockets_engine = DeepPocketsEngine()
deeppockets_engine.load_real_data()

@app.route('/api/deeppockets/inventory')
def deeppockets_inventory():
    """Get account-wide inventory for an item"""
    item_id = request.args.get('item_id', type=int)
    if not item_id:
        return jsonify({"error": "Missing item_id"}), 400
        
    total = deeppockets_engine.get_total_count(item_id)
    locations = deeppockets_engine.find_item(item_id)
    
    return jsonify({
        "item_id": item_id,
        "total_count": total,
        "locations": locations
    })

# --- DeepPockets Endpoints ---

@app.route('/api/deeppockets/search')
def deeppockets_search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    results = deeppockets_engine.search_inventory(query)
    return jsonify(results)

@app.route('/api/deeppockets/incinerate', methods=['POST'])
def deeppockets_incinerate():
    data = request.get_json()
    items = data.get("items", [])
    
    # Sync prices from Goblin
    price_map = {}
    for item_id, price_obj in goblin_engine.prices.items():
        price_map[item_id] = float(price_obj.market_value)
        
    deeppockets_engine.set_prices(price_map)
    
    candidates = deeppockets_engine.calculate_value_density(items)
    return jsonify({"candidates": candidates})

@app.route('/api/deeppockets/remote')
def deeppockets_remote():
    main_char = request.args.get('main')
    if not main_char:
        return jsonify({"error": "Missing 'main' parameter"}), 400
        
    remote_items = deeppockets_engine.get_remote_stash(main_char)
            
    return jsonify({"items": remote_items[:50]}) # Limit to 50

# --- Artificer Endpoints ---
from artificer_engine import ArtificerEngine
artificer_engine = ArtificerEngine(goblin_engine, deeppockets_engine)

@app.route('/artificer')
def artificer_page():
    return render_template('artificer.html')

@app.route('/api/artificer/concentration')
def artificer_concentration():
    data = artificer_engine.calculate_concentration_value()
    return jsonify(data)

@app.route('/api/artificer/supply_chain')
def artificer_supply_chain():
    recipe_id = request.args.get('recipe_id', type=int)
    qty = request.args.get('qty', default=1, type=int)
    
    if not recipe_id:
        # Default mock for demo
        recipe_id = 370607 
        
    data = artificer_engine.solve_supply_chain(recipe_id, qty)
    return jsonify(data)

# --- Navigator Endpoints ---
# Re-initialize Pathfinder with DeepPockets
pathfinder_engine = PathfinderEngine(os.getenv('DATABASE_URL'), deeppockets_engine)
pathfinder_engine.load_mock_data() # Ensure mock data is loaded

@app.route('/navigator')
def navigator_page():
    return render_template('navigator.html')

@app.route('/api/navigator/optimize', methods=['POST'])
def navigator_optimize():
    data = request.get_json()
    current_zone = data.get('current_zone', 84) # Default Stormwind
    quests = data.get('quests', []) # List of Quest IDs
    destinations = data.get('destinations', []) # List of Zone IDs
    
    # 1. Check for Bank Stops
    bank_stops = pathfinder_engine.check_quest_items(quests)
    if bank_stops:
        destinations.extend(bank_stops)
        
    # 2. Optimize Route
    result = pathfinder_engine.optimize_route(current_zone, destinations)
    
    return jsonify({
        "route": result,
        "bank_stops_added": len(bank_stops) > 0,
        "bank_zones": bank_stops
    })

# --- Synergy Endpoints ---
from synergy_engine import SynergyEngine
synergy_engine = SynergyEngine(goblin_engine, deeppockets_engine)

@app.route('/synergy')
def synergy_page():
    return render_template('synergy.html')

@app.route('/api/synergy/economy_check')
def synergy_economy_check():
    item_id = request.args.get('item_id', type=int)
    if not item_id:
        return jsonify({"error": "Missing item_id"}), 400
    result = synergy_engine.economy_of_scale(item_id)
    return jsonify(result)

@app.route('/api/synergy/consumable_cost')
def synergy_consumable_cost():
    result = synergy_engine.cost_per_cast()
    return jsonify(result)

@app.route('/api/synergy/zookeeper', methods=['POST'])
def synergy_zookeeper():
    result = synergy_engine.the_zookeeper()
    return jsonify(result)

@app.route('/deeppockets')
def deeppockets():
    """DeepPockets UI"""
    total_items = len(deeppockets_engine.inventory)
    return render_template('deeppockets.html', total_items=total_items)

# --- SKILLWEAVER & ARBITER MODULES ---
from skillweaver_engine import SkillWeaverEngine
from arbiter_engine import ArbiterEngine

# Initialize Engines
skillweaver_engine = SkillWeaverEngine()
# skillweaver_engine.start()  # DISABLED: Causes blocking on startup, preventing Flask from serving requests

arbiter_engine = ArbiterEngine(skillweaver_engine)
# arbiter_engine.start()  # DISABLED: Same issue

@app.route('/api/arbiter/status')
def arbiter_status():
    """Get real-time performance stats"""
    return jsonify(arbiter_engine.get_status())

# --- DASHBOARD MODULE ---
from dashboard_engine import DashboardEngine

# Initialize Dashboard engine once
dashboard_engine = DashboardEngine()

@app.route('/api/dashboard/summary')
def dashboard_summary():
    """Get unified dashboard summary"""
    try:
        summary = dashboard_engine.get_dashboard_summary()
        return jsonify(summary)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """Enhanced Dashboard UI"""
    summary = dashboard_engine.get_dashboard_summary()
    return render_template('dashboard.html', summary=summary)

def fetch_campaigns():
    """
    Load campaign definitions from the database with a light fallback.
    """
    campaigns = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT campaign_id, name, ordered_quest_ids FROM codex.campaigns")
        for row in cur.fetchall():
            quest_ids = list(row[2]) if len(row) > 2 and row[2] else []
            campaigns.append({
                "campaign_id": row[0],
                "name": row[1],
                "quest_ids": quest_ids
            })
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Codex campaign fetch error: {e}")

    # Fallback sample so the UI always renders
    if not campaigns:
        campaigns = [
            {
                "campaign_id": 1,
                "name": "Breaching the Tomb",
                "quest_ids": [47137, 47139, 46247]
            }
        ]
    return campaigns


def fetch_characters_and_history():
    """
    Fetch character roster and quest completion history.
    Returns: (characters, completion_map)
    """
    characters = []
    completions = defaultdict(set)
    used_fallback = False

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT character_guid, name, realm, class, level FROM holocron.characters")
        for row in cur.fetchall():
            if len(row) >= 2:
                characters.append({
                    "guid": str(row[0]),
                    "name": row[1],
                    "realm": row[2] if len(row) > 2 else "",
                    "class": row[3] if len(row) > 3 else "",
                    "level": row[4] if len(row) > 4 else None
                })

        cur.execute("SELECT guid, quest_id FROM codex.character_quest_history")
        for row in cur.fetchall():
            if len(row) >= 2 and isinstance(row[1], int):
                completions[str(row[0])].add(int(row[1]))

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Codex character/history fetch error: {e}")

    # Fallback sample roster
    if not characters:
        used_fallback = True
        characters = [
            {"guid": "GUID-1", "name": "MainMage", "realm": "Dornogal", "class": "Mage", "level": 80},
            {"guid": "GUID-2", "name": "AltDruid", "realm": "Dornogal", "class": "Druid", "level": 80}
        ]

    if not completions and used_fallback:
        completions["GUID-1"] = {47137, 47139}
        completions["GUID-2"] = {47137}

    return characters, completions

def solve_dependency(quest_id, completed_ids, depth=0):
    """
    Recursive function to find the first missing prerequisite.
    Returns: (Missing Quest ID, Title)
    """
    if depth > 10: return None # Prevent infinite recursion
    
    # 1. Check if we have this quest
    if quest_id in completed_ids:
        return None
        
    # 2. Check dependencies
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT required_quest_id FROM codex.quest_dependencies WHERE quest_id = %s", (quest_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        for row in rows:
            parent_id = row[0]
            if parent_id not in completed_ids:
                # Recursively check the parent
                missing_prereq = solve_dependency(parent_id, completed_ids, depth+1)
                if missing_prereq:
                    return missing_prereq
                else:
                    # Parent is missing but has no missing prereqs -> Parent is the blocker
                    # Fetch title
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT title FROM codex.quest_definitions WHERE quest_id = %s", (parent_id,))
                    title_row = cur.fetchone()
                    cur.close()
                    conn.close()
                    return (parent_id, title_row[0] if title_row else "Unknown Quest")
                    
        # If no dependencies are missing, but we don't have this quest -> This quest is the next step
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT title FROM codex.quest_definitions WHERE quest_id = %s", (quest_id,))
        title_row = cur.fetchone()
        cur.close()
        conn.close()
        return (quest_id, title_row[0] if title_row else "Unknown Quest")
        
    except Exception as e:
        print(f"Codex solver error: {e}")
        return None


def evaluate_campaign_status(campaign, completed_ids):
    """
    Returns per-character campaign status and next action text.
    """
    quest_ids = campaign.get("quest_ids", [])
    total = len(quest_ids)
    done_count = sum(1 for q in quest_ids if q in completed_ids)
    percent = int((done_count / total) * 100) if total else 0
    next_step = next((q for q in quest_ids if q not in completed_ids), None)

    state = "not_started"
    status_text = "No quest data."
    next_quest_id = None
    next_quest_title = None

    if not quest_ids:
        status_text = "No quest steps recorded."
    elif next_step is None:
        state = "done"
        status_text = "Campaign complete."
    else:
        blocker = solve_dependency(next_step, completed_ids)
        if blocker and blocker[0] != next_step:
            state = "locked"
            next_quest_id, next_quest_title = blocker
            status_text = f"Missing prerequisite: {next_quest_title} (ID: {next_quest_id})"
        else:
            state = "in_progress" if done_count else "not_started"
            if blocker:
                next_quest_id, next_quest_title = blocker
                status_text = f"Next: {next_quest_title} (ID: {next_quest_id})"
            else:
                next_quest_id = next_step
                status_text = f"Next: Quest ID {next_step}"

    return {
        "campaign_id": campaign.get("campaign_id"),
        "name": campaign.get("name", "Unknown Campaign"),
        "percent": percent,
        "state": state,
        "status_text": status_text,
        "step_label": f"{done_count}/{total}" if total else "-",
        "next_quest_id": next_quest_id,
        "next_quest_title": next_quest_title
    }


def build_campaign_matrix(campaigns, characters, completions):
    """
    Builds the Universal Matrix: rows = characters, columns = campaign status.
    """
    matrix = []
    for char in characters:
        completed_ids = completions.get(char["guid"], set())
        entries = []
        for camp in campaigns:
            entries.append(evaluate_campaign_status(camp, completed_ids))
        matrix.append({
            "character": char,
            "campaigns": entries
        })
    return matrix


def summarize_campaigns(matrix, campaigns):
    """
    Aggregates campaign completion across the roster for the overview cards.
    """
    summaries = []
    for camp in campaigns:
        statuses = []
        for row in matrix:
            for status in row.get("campaigns", []):
                if status.get("campaign_id") == camp.get("campaign_id"):
                    statuses.append(status)

        if statuses:
            avg_percent = int(sum(s.get("percent", 0) for s in statuses) / len(statuses))
            non_done = next((s for s in statuses if s.get("state") != "done"), None)
            if non_done:
                status_text = non_done.get("status_text", "In progress")
            else:
                status_text = "Complete on all alts."
        else:
            avg_percent = 0
            status_text = "No character data."

        summaries.append({
            "campaign_id": camp.get("campaign_id"),
            "name": camp.get("name", "Campaign"),
            "progress": avg_percent,
            "status": status_text
        })
    return summaries
    return summaries

# --- FABRICATOR MODULE ---
from fabricator import Fabricator

# Initialize Fabricator (DB connection will be created per request or shared)
# For now, we pass the connection string from env
DB_URL = os.environ.get('DATABASE_URL')
fabricator_engine = Fabricator(DB_URL)

@app.route('/api/fabricator/plan')
def fabricator_plan():
    """
    Generate a crafting plan for an item
    Query params:
        item_id (int): Target item ID
        qty (int): Quantity needed
    """
    item_id = request.args.get('item_id', type=int)
    qty = request.args.get('qty', 1, type=int)
    
    if not item_id:
        return jsonify({"error": "Missing item_id"}), 400
        
    try:
        G = fabricator_engine.build_dependency_graph(item_id, qty)
        plan = fabricator_engine.generate_plan(G)
        return jsonify({"plan": plan})
    except Exception as e:
        print(f"Fabricator error: {e}")
        return jsonify({"error": str(e)}), 500

# --- SANDBOX MODULE ---
from sandbox import Sandbox
from loadout_lottery import LoadoutLottery

sandbox_engine = Sandbox()
lottery_engine = LoadoutLottery()

@app.route('/api/sandbox/run', methods=['POST'])
def sandbox_run():
    """
    Run a raw SimC simulation
    POST body: {simc_input: str}
    """
    data = request.get_json()
    simc_input = data.get('simc_input')
    
    if not simc_input:
        return jsonify({"error": "Missing simc_input"}), 400
        
    result = sandbox_engine.run_sim(simc_input)
    if result:
        return jsonify(result)
    return jsonify({"error": "Simulation failed"}), 500

@app.route('/api/sandbox/optimize', methods=['POST'])
def sandbox_optimize():
    """
    Run a talent optimization (Loadout Lottery)
    POST body: {base_profile: str, talent_strings: [str]}
    """
    data = request.get_json()
    base_profile = data.get('base_profile')
    talent_strings = data.get('talent_strings', [])
    
    if not base_profile or not talent_strings:
        return jsonify({"error": "Missing base_profile or talent_strings"}), 400
        
        return jsonify(winner)
    return jsonify({"error": "Optimization failed"}), 500

# =============================================================================
# PETWEAVER MODULE

@app.route('/petweaver')
def petweaver_dashboard():
    return render_template('petweaver.html')
# =============================================================================

@app.route('/api/petweaver/encounters')
def petweaver_encounters():
    """
    Get list of available pet battle encounters
    Returns: List of encounter IDs and names
    """
    try:
        # TODO: Replace with real data from database
        encounters = [
            {"id": "squirt", "name": "Squirt", "zone": "Garrison", "difficulty": "Medium"},
            {"id": "tiun", "name": "Ti'un the Wanderer", "zone": "Krasarang Wilds", "difficulty": "Hard"},
            {"id": "akali", "name": "Aki the Chosen", "zone": "Vale of Eternal Blossoms", "difficulty": "Easy"},
        ]
        return jsonify({"encounters": encounters})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/petweaver/strategy/<encounter_id>')
def petweaver_strategy(encounter_id):
    """
    Get strategy recommendation for a specific encounter
    Query params:
        encounter_id: Encounter identifier (e.g., "squirt", "tiun")
    Returns: Team recommendations, scripts, and win rates
    """
    try:
        # TODO: Integrate with genetic algorithm from app.py
        # For now, return mock data structure
        
        mock_strategies = {
            "squirt": {
                "encounter_id": "squirt",
                "encounter_name": "Squirt",
                "recommended_teams": [
                    {
                        "team_id": 1,
                        "pets": [
                            {"species_id": 1387, "name": "Ikky", "level": 25, "quality": 4},
                            {"species_id": 1266, "name": "MPD", "level": 25, "quality": 4},
                            {"species_id": 0, "name": "Leveling Pet", "level": 1, "quality": 1}
                        ],
                        "win_rate": 0.95,
                        "avg_rounds": 8,
                        "script": "Ikky\nBlack Claw\nFlock\nSwap to MPD\nDecoy\nBombardment\nBombardment"
                    }
                ]
            },
            "tiun": {
                "encounter_id": "tiun",
                "encounter_name": "Ti'un the Wanderer",
                "recommended_teams": [
                    {
                        "team_id": 1,
                        "pets": [
                            {"species_id": 1387, "name": "Ikky", "level": 25, "quality": 4},
                            {"species_id": 1266, "name": "MPD", "level": 25, "quality": 4},
                            {"species_id": 233, "name": "Cogblade Raptor", "level": 25, "quality": 4}
                        ],
                        "win_rate": 0.85,
                        "avg_rounds": 12,
                        "script": "Ikky\nBlack Claw\nFlock\nSwap to MPD\nDecoy\nBombardment\nSwap to Cogblade\nBatter\nBatter"
                    }
                ]
            }
        }
        
        strategy = mock_strategies.get(encounter_id, {
            "encounter_id": encounter_id,
            "encounter_name": encounter_id.title(),
            "recommended_teams": []
        })
        
        return jsonify(strategy)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/petweaver/validate_team', methods=['POST'])
def petweaver_validate_team():
    """
    Validate if a team can defeat an encounter
    POST body: {
        "encounter_id": "squirt",
        "pets": [species_id1, species_id2, species_id3]
    }
    Returns: Simulation results with win probability
    """
    try:
        data = request.json
        encounter_id = data.get('encounter_id')
        pets = data.get('pets', [])
        
        # TODO: Run simulation with genetic algorithm
        # For now, return mock validation
        
        return jsonify({
            "valid": True,
            "win_probability": 0.75,
            "simulation_rounds": 10,
            "notes": "Team appears viable. Consider breed optimization."
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =============================================================================
# MAIN
# =============================================================================



def fetch_completed_for_guid(guid):
    """
    Fetches completed quest IDs for a specific character GUID.
    """
    completed = set()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT quest_id FROM codex.character_quest_history WHERE guid = %s", (guid,))
        for row in cur.fetchall():
            if row and isinstance(row[0], int):
                completed.add(int(row[0]))
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Codex completion fetch error: {e}")
    return completed


def lookup_quest_id(target):
    """
    Resolves a quest identifier from ID or fuzzy title search.
    """
    if target is None:
        return None

    target_str = str(target).strip()
    if target_str.isdigit():
        return int(target_str)

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT quest_id FROM codex.quest_definitions WHERE title ILIKE %s LIMIT 1",
            (f"%{target_str}%",)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return int(row[0])
    except Exception as e:
        print(f"Quest lookup error: {e}")
    return None


def parse_completed_list(raw):
    """
    Parses a comma-separated list of quest IDs into a set of integers.
    """
    completed = set()
    if not raw:
        return completed
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            completed.add(int(part))
    return completed

@app.route('/codex')
def codex():
    try:
        campaigns = fetch_campaigns()
        characters, completions = fetch_characters_and_history()
        matrix = build_campaign_matrix(campaigns, characters, completions)
        campaign_cards = summarize_campaigns(matrix, campaigns)
    except Exception as e:
        print(f"Codex error: {e}")
        campaigns = fetch_campaigns()
        matrix = []
        campaign_cards = []

    return render_template(
        'codex.html',
        campaigns=campaign_cards,
        matrix=matrix,
        campaign_columns=campaigns
    )


@app.route('/api/codex/blocker')
def codex_blocker():
    """
    API for the Blocker Breaker. Accepts ?quest=<id or name>&completed=1,2&guid=<character_guid>
    """
    target = request.args.get('quest')
    if not target:
        return jsonify({"error": "Missing 'quest' parameter"}), 400

    completed = parse_completed_list(request.args.get('completed'))
    guid = request.args.get('guid')
    if guid:
        completed |= fetch_completed_for_guid(guid)

    quest_id = lookup_quest_id(target)
    if quest_id is None:
        return jsonify({"error": "Quest not found"}), 404

    if quest_id in completed:
        return jsonify({
            "target_quest_id": quest_id,
            "blocking_quest_id": None,
            "blocking_title": None,
            "state": "complete",
            "message": "Quest already completed."
        })

    result = solve_dependency(quest_id, completed)
    if not result:
        return jsonify({
            "target_quest_id": quest_id,
            "blocking_quest_id": None,
            "blocking_title": None,
            "state": "unknown",
            "message": "No blockers found or quest data unavailable."
        })

    blocker_id, blocker_title = result
    state = "blocked" if blocker_id != quest_id else "ready"
    message = f"Missing prerequisite: {blocker_title} (ID: {blocker_id})" if state == "blocked" else f"Next step: {blocker_title} (ID: {blocker_id})"

    return jsonify({
        "target_quest_id": quest_id,
        "blocking_quest_id": blocker_id,
        "blocking_title": blocker_title,
        "state": state,
        "message": message
    })

# --- DIPLOMAT MODULE ---
from diplomat_engine import DiplomatEngine

# Initialize Diplomat engine once
diplomat_engine = DiplomatEngine()
diplomat_engine.load_real_data()

@app.route('/api/diplomat/opportunities')
def diplomat_opportunities():
    """
    Get Paragon opportunities and recommended WQs
    Returns factions >80% to next reward with efficiency-ranked quests
    """
    recommendations = diplomat_engine.generate_recommendations()
    return jsonify(recommendations)

@app.route('/api/diplomat/quests')
def diplomat_quests():
    """
    Get recommended WQs for a specific faction
    Query param: faction_id (int)
    """
    faction_id = request.args.get('faction_id', type=int)
    if not faction_id:
        return jsonify({"error": "Missing 'faction_id' parameter"}), 400
    
    quests = diplomat_engine.get_recommended_quests(faction_id)
    return jsonify({"faction_id": faction_id, "quests": quests})

@app.route('/diplomat')
def diplomat():
    """Diplomat UI page"""
    # Get all data from engine
    recommendations = diplomat_engine.generate_recommendations()
    
    # Format for template
    """Render the Diplomat Dashboard"""
    # Get Recommendations
    recommendations = diplomat_engine.generate_recommendations()
    
    # Get Matrix
    matrix = diplomat_engine.get_reputation_matrix()
    
    # Format data for template
    factions_data = recommendations["opportunities"]
    sniper_list = []
    
    # Flatten recommended quests for the sniper view
    for opp in factions_data:
        for quest in opp.get("recommended_quests", []):
            sniper_list.append({
                "zone": quest["zone"],
                "quest": quest["title"],
                "reward": f"{quest['rep_reward']} Rep",
                "efficiency": f"{quest['efficiency']} rep/min",
                "assigned_char": "Any", # TODO: Assign to specific char
                "efficiency_score": quest["efficiency_score"]
            })
            
    # Sort sniper list by efficiency
    sniper_list.sort(key=lambda x: float(x["efficiency"].split()[0]), reverse=True)
    
    return render_template('diplomat.html', factions=factions_data, sniper=sniper_list, matrix=matrix)

@app.route('/api/diplomat/emissaries')
def diplomat_emissaries():
    """Get active emissaries"""
    return jsonify(diplomat_engine.get_active_emissaries())


def codex_encounter(encounter_id):
    """Codex Encounter UI"""
    encounter = codex_engine.get_encounter_details(encounter_id)
    if not encounter:
        return "Encounter not found", 404
    return render_template('codex_encounter.html', encounter=encounter)

@app.route('/api/codex/encounter/<int:encounter_id>')
def api_codex_encounter(encounter_id):
    """Get encounter details JSON"""
    encounter = codex_engine.get_encounter_details(encounter_id)
    if not encounter:
        return jsonify({"error": "Not found"}), 404
    return jsonify(encounter)

@app.route('/upload_data', methods=['POST'])
def upload_data():
    """
    Endpoint to receive JSON payloads from the Bridge script.
    Expected JSON format:
    {
        "source": "DataStore", 
        "data": "raw lua string"
    }
    """
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "No JSON payload received"}), 400

        source = payload.get('source')
        data = payload.get('data')

        if not source or not data:
            return jsonify({"error": "Missing 'source' or 'data' fields"}), 400

        # Parse Lua
        from lua_parser import parse_lua_table
        parsed_data = parse_lua_table(data)
        
        if not parsed_data:
             return jsonify({"error": "Failed to parse Lua data"}), 400
             
        # Save to JSON file for engines to consume
        filename = f"{source}.json"
        # os.makedirs("data", exist_ok=True)
        
        with open(filename, "w") as f:
            json.dump(parsed_data, f, indent=2)

        print(f"Received and saved data from {source}: {len(str(parsed_data))} bytes")
            
        # SQL Ingestion (Async-ish)
        try:
            import ingest_sql
            if source == "DataStore_Reputations":
                ingest_sql.ingest_reputations(parsed_data)
            elif source == "SavedInstances":
                ingest_sql.ingest_saved_instances(parsed_data)
        except Exception as e:
            print(f"SQL Ingestion Error: {e}")
            
        return jsonify({"status": "success", "source": source, "size": len(parsed_data)}), 200

    except Exception as e:
        print(f"Error processing upload: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": str(e)}), 500

# --- MIRROR MODULE ---

@app.route('/api/mirror/register', methods=['POST'])
def mirror_register():
    """
    Registers a device by hostname and returns its type.
    """
    try:
        data = request.get_json()
        hostname = data.get('hostname')
        if not hostname:
            return jsonify({"error": "Missing hostname"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if exists
        cur.execute("SELECT device_type FROM mirror.trusted_devices WHERE hostname = %s", (hostname,))
        row = cur.fetchone()
        
        if row:
            device_type = row[0]
            # Update last_seen
            cur.execute("UPDATE mirror.trusted_devices SET last_seen = CURRENT_TIMESTAMP WHERE hostname = %s", (hostname,))
        else:
            # Register new (Default to DESKTOP)
            device_type = 'DESKTOP'
            cur.execute("INSERT INTO mirror.trusted_devices (hostname, device_type) VALUES (%s, %s)", (hostname, device_type))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"hostname": hostname, "device_type": device_type})
    except Exception as e:
        print(f"Mirror register error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/mirror/upload', methods=['POST'])
def mirror_upload():
    """
    Uploads a config file (macros/bindings).
    """
    try:
        data = request.get_json()
        hostname = data.get('hostname')
        file_type = data.get('file_type') # MACROS, BINDINGS
        content = data.get('content')
        char_guid = data.get('char_guid', 'GLOBAL')
        
        if not all([hostname, file_type, content]):
            return jsonify({"error": "Missing fields"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get device type
        cur.execute("SELECT device_type FROM mirror.trusted_devices WHERE hostname = %s", (hostname,))
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Device not registered"}), 403
        device_type = row[0]
        
        # Upsert Profile
        sql = """
            INSERT INTO mirror.config_profiles (character_guid, device_type, file_type, content, updated_at)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (character_guid, device_type, file_type) 
            DO UPDATE SET content = EXCLUDED.content, updated_at = CURRENT_TIMESTAMP
        """
        cur.execute(sql, (char_guid, device_type, file_type, content))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"status": "success", "message": "Config uploaded"})
    except Exception as e:
        print(f"Mirror upload error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/mirror/sync', methods=['GET'])
def mirror_sync():
    """
    Downloads the latest config for a device.
    """
    try:
        hostname = request.args.get('hostname')
        file_type = request.args.get('file_type')
        char_guid = request.args.get('char_guid', 'GLOBAL')
        
        if not hostname or not file_type:
            return jsonify({"error": "Missing params"}), 400
            
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get device type
        cur.execute("SELECT device_type FROM mirror.trusted_devices WHERE hostname = %s", (hostname,))
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Device not registered"}), 403
        device_type = row[0]
        
        # Fetch Config
        cur.execute("""
            SELECT content, updated_at FROM mirror.config_profiles 
            WHERE character_guid = %s AND device_type = %s AND file_type = %s
        """, (char_guid, device_type, file_type))
        
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if row:
            return jsonify({
                "found": True,
                "content": row[0],
                "updated_at": row[1]
            })
        else:
            return jsonify({"found": False})
            
    except Exception as e:
        print(f"Mirror sync error: {e}")
        return jsonify({"error": str(e)}), 500

# --- UNIFIED DASHBOARD ---

# Legacy dashboard removed in favor of Resilient Dashboard


# --- TSM MODULE ---
from tsm_engine import TSMEngine
tsm_engine = TSMEngine()
tsm_engine.load_data()

# --- GOBLIN MODULE ---
from goblin_engine import GoblinEngine
goblin_engine = GoblinEngineExpanded()
goblin_engine.load_mock_data()

@app.route('/api/goblin')
def api_goblin():
    """Market Analysis API"""
    analysis = goblin_engine.analyze_market()
    return jsonify(analysis)

@app.route('/api/goblin/history')
def api_goblin_history():
    """Portfolio History API"""
    days = request.args.get('days', default=7, type=int)
    history = goblin_engine.get_history(days=days)
    return jsonify(history)

# --- WARDEN MODULE ---
from warden_engine import WardenEngine
warden_engine = WardenEngine()
warden_engine.load_mock_data()

@app.route('/api/warden')
def warden_api():
    """Warden API"""
    return jsonify(warden_engine.get_account_summary())

# --- QUARTERMASTER ENGINE (Logistics) ---
from quartermaster_engine import QuartermasterEngine
quartermaster_engine = QuartermasterEngine(warden_engine)

@app.route('/api/quartermaster/jobs')
def api_quartermaster_jobs():
    """Get pending mail jobs"""
    return jsonify(quartermaster_engine.get_logistics_report())

# --- MUSEUM ENGINE (Shadow Collection) ---
from museum_engine import MuseumEngine
museum_engine = MuseumEngine(warden_engine)

@app.route('/api/museum/shadow')
def api_museum_shadow():
    """Get shadow collection"""
    return jsonify(museum_engine.get_shadow_collection())

# --- BRIEFING MODULE ---
from briefing_engine import BriefingEngine

# --- BRIEFING ENGINE (Executive Assistant) ---
# Pass quartermaster to BriefingEngine
briefing_engine = BriefingEngine(
    diplomat=diplomat_engine,
    goblin=goblin_engine,
    vault=vault_engine,
    scout=scout_engine,
    knowledge=knowledge_tracker,
    warden=warden_engine,
    quartermaster=quartermaster_engine, # Added quartermaster
    museum=museum_engine
)

@app.route('/api/briefing')
def briefing_api():
    """Daily Briefing API"""
    return jsonify(briefing_engine.generate_briefing())

@app.route('/briefing')
def briefing():
    """Daily Briefing UI"""
    data = briefing_engine.generate_briefing()
    return render_template('briefing.html', briefing=data)

# --- COMMANDER ENGINE (Alt-Army) ---
@app.route('/api/commander/cooldowns')
def api_commander_cooldowns():
    """Returns profession cooldowns across all characters."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT character_name, realm, profession, spell_name, ready_at, charges 
            FROM holocron.profession_cooldowns 
            ORDER BY ready_at ASC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        cooldowns = []
        for r in rows:
            cooldowns.append({
                "character": r[0],
                "realm": r[1],
                "profession": r[2],
                "spell": r[3],
                "ready_at": r[4].isoformat() if r[4] else None,
                "charges": r[5]
            })
        return jsonify(cooldowns)
        
    except Exception as e:
        print(f"DB Error (Commander): {e}")
        # Mock Data for Verification
        return jsonify([
            {
                "character": "Mage", "realm": "Area52", "profession": "Alchemy", 
                "spell": "Transmute: Draconium", "ready_at": "2025-11-29T10:00:00Z", "charges": 1
            },
            {
                "character": "Priest", "realm": "Area52", "profession": "Tailoring", 
                "spell": "Azureweave Bolt", "ready_at": "2025-11-29T12:00:00Z", "charges": 0
            },
            {
                "character": "Druid", "realm": "Stormrage", "profession": "Leatherworking", 
                "spell": "Hide of the Earth", "ready_at": "2025-11-30T08:00:00Z", "charges": 1
            }
        ])

# ==========================================
# PROFESSION & CRAFTING API
# ==========================================

from intelligent_profession_engine import IntelligentProfessionEngine
from recommend_specs import generate_spec_guide

prof_engine = IntelligentProfessionEngine(goblin_engine=goblin_engine)

@app.route('/api/profession/guide/<character>/<profession>')
def api_profession_guide(character, profession):
    """Get dynamic leveling guide for character"""
    try:
        # Get current skill from DB
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT skill_level, max_skill 
            FROM goblin.professions p
            JOIN holocron.characters c ON p.character_guid = c.character_guid
            WHERE c.name = %s AND p.profession_name = %s
        """, (character, profession))
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if not row:
            return jsonify({"error": "Character/Profession not found"}), 404
            
        current_skill = row[0]
        max_skill = row[1]
        
        # Generate dynamic guide
        guide = prof_engine.generate_dynamic_leveling_guide(
            character, profession, current_skill, max_skill
        )
        
        return jsonify(guide)
    except Exception as e:
        print(f"Error generating guide: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/profession/specs/<character>/<profession>')
def api_profession_specs(character, profession):
    """Get specialization recommendations"""
    try:
        guide = generate_spec_guide(character, profession)
        return jsonify(guide)
    except Exception as e:
        print(f"Error generating spec guide: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/profession/intelligent/<character>/<profession>')
def api_intelligent_recommendations(character, profession):
    """Get intelligent crafting recommendations"""
    try:
        # Get skill level
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT skill_level 
            FROM goblin.professions p
            JOIN holocron.characters c ON p.character_guid = c.character_guid
            WHERE c.name = %s AND p.profession_name = %s
        """, (character, profession))
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        skill = row[0] if row else 1
        
        recs = prof_engine.recommend_recipes_intelligent(character, profession, skill)
        return jsonify(recs)
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Start the Flask server
    PORT = 8003
    print(f"Starting Holocron Server on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False)
