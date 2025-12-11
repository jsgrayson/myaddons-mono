from flask import Flask, render_template, jsonify, request, Response
import sys
import re
import threading
import time
import json
import os
import mss
import numpy as np
import cv2
import io
from visual_weaver import VisualWeaver

app = Flask(__name__)
weaver = VisualWeaver()

# Start weaver in a separate thread (it handles its own loop thread)
# But we need to call start() which starts the listener and the loop thread.
# However, we might want to start it in a "stopped" state initially?
# The class initializes with running=False.
# Let's start the listener but keep the loop paused/stopped?
# weaver.start() starts everything.
# Let's just initialize it.

@app.route('/')
def index():
    return render_template('visual_dashboard.html')

@app.route('/upgrades')
def upgrades_page():
    return render_template('upgrades.html')

@app.route('/droptimizer')
def droptimizer_page():
    return render_template('droptimizer.html')

@app.route('/shopping_list')
def shopping_list_page():
    return render_template('shopping_list.html')

@app.route('/junk')
def junk_page():
    return render_template('junk_manager.html')

@app.route('/encounter')
def encounter_page():
    return render_template('encounter.html')

@app.route('/api/status')
def get_status():
    return jsonify({
        "running": weaver.running,
        "paused": weaver.paused,
        "healer_mode": weaver.healer_mode,
        "pet_mode": weaver.pet_mode
    })

@app.route('/api/control', methods=['POST'])
def control():
    action = request.json.get('action')
    if action == 'start':
        if not weaver.running:
            weaver.start()
        weaver.paused = False
    elif action == 'stop':
        weaver.stop()
    elif action == 'pause':
        weaver.paused = True
    elif action == 'resume':
        weaver.paused = False
    return jsonify({"success": True})

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        new_config = request.json
        weaver.config = new_config
        weaver.save_config()
        return jsonify({"success": True})
    return jsonify(weaver.config)
    return jsonify(weaver.config)

@app.route('/api/upgrades', methods=['POST'])
def get_upgrades():
    data = request.json
    class_name = data.get('class')
    spec_name = data.get('spec')
    weights = data.get('weights', {})
    sources = data.get('sources', []) # List of allowed sources, e.g. ["Raid", "Dungeon"]

    # Special Handling for Fishing
    if spec_name == "Fishing":
        return jsonify({
            "Main Hand": [
                {"name": "Underlight Angler", "id": 133755, "source": "Legion Artifact", "score": 1000},
                {"name": "Ephemeral Fishing Pole", "id": 118381, "source": "WoD Garrison", "score": 500},
                {"name": "Mastercraft Kalu'ak Fishing Pole", "id": 44050, "source": "WotLK Rep", "score": 100}
            ],
            "Head": [
                {"name": "Nat's Drinking Hat", "id": 117405, "source": "WoD Rep", "score": 10},
                {"name": "Nat's Hat", "id": 88710, "source": "MoP Rep", "score": 10},
                {"name": "High Test Goggles", "id": 19972, "source": "Engineering", "score": 5}
            ]
        })

    # Special Handling for Speed
    if spec_name == "Speed":
        # Return generic advice or specific items
        return jsonify({
            "Feet": [
                {"name": "Sentinel's Eternal Refuge", "id": 146669, "source": "Legion Crafting", "score": 100},
                {"name": "Boots with +Speed", "id": 0, "source": "World Drop", "score": 50}
            ],
            "Head": [
                {"name": "Flashpowder Hood", "id": 159297, "source": "Azerite (Tol Dagor)", "score": 100}
            ],
            "Shoulders": [
                {"name": "Gold-Tasseled Epaulets", "id": 159303, "source": "Azerite (Freehold)", "score": 100}
            ],
            "Chest": [
                {"name": "Venture Co. Plenipotentiary Vest", "id": 159299, "source": "Azerite (Motherlode)", "score": 100}
            ]
        })

    # Normal Class/Spec Scrape
    try:
        # Import here to avoid circular deps if any
        sys.path.append('/Users/jgrayson/Documents/holocron/scrapers')
        from icy_veins import IcyVeinsScraper
        
        scraper = IcyVeinsScraper(class_name, spec_name)
        gear_data = scraper.fetch_gear()
        
        filtered_gear = {}
        
        for slot, items in gear_data.items():
            filtered_items = []
            for item in items:
                # Filter by Source
                # Source string examples: "Raid: Queen Ansurek", "Dungeon: The Stonevault"
                # If sources list is empty, allow all.
                allowed = True
                if sources:
                    allowed = False
                    for src in sources:
                        if src.lower() in item['source'].lower():
                            allowed = True
                            break
                
                if allowed:
                    # Calculate Score (Placeholder: We need stats!)
                    # For now, assign a dummy score based on list order (assuming Icy Veins lists best first)
                    # Or if we had stats, we'd use weights.
                    # item['score'] = calculate_score(item, weights)
                    item['score'] = 0 # Placeholder
                    filtered_items.append(item)
            
            # Assign dummy scores in reverse order (top of list = highest score)
            count = len(filtered_items)
            for i, item in enumerate(filtered_items):
                item['score'] = (count - i) * 10
                
            filtered_gear[slot] = filtered_items
            
        return jsonify(filtered_gear)

    except Exception as e:
        print(f"Error in upgrades API: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/droptimizer', methods=['POST'])
def get_droptimizer():
    data = request.json
    class_name = data.get('class')
    spec_name = data.get('spec')
    
    try:
        # Import here to avoid circular deps if any
        sys.path.append('/Users/jgrayson/Documents/holocron/scrapers')
        from icy_veins import IcyVeinsScraper
        
        scraper = IcyVeinsScraper(class_name, spec_name)
        gear_data = scraper.fetch_gear()
        
        instances = {}
        
        for slot, items in gear_data.items():
            for item in items:
                source_text = item['source']
                
                # Parse Instance Name
                # Formats: "Raid: Nerub-ar Palace", "Dungeon: The Stonevault", "Delve: ...", "World Boss: ..."
                # We want to group by the main instance name.
                
                instance_name = "Unknown"
                if ":" in source_text:
                    parts = source_text.split(":")
                    # The part after the colon is usually the instance
                    # e.g. "Raid: Nerub-ar Palace" -> "Nerub-ar Palace"
                    # But sometimes it's "Boss Name (Instance)"
                    candidate = parts[1].strip()
                    
                    # Heuristic: If it has parens, the instance might be inside or outside
                    # "Queen Ansurek (Nerub-ar Palace)" -> "Nerub-ar Palace"
                    if "(" in candidate and ")" in candidate:
                        match = re.search(r'\((.*?)\)', candidate)
                        if match:
                            instance_name = match.group(1)
                        else:
                            instance_name = candidate
                    else:
                        instance_name = candidate
                else:
                    # Fallback for simple strings
                    instance_name = source_text

                # Clean up
                instance_name = instance_name.replace("Mythic+", "").strip()
                
                if instance_name not in instances:
                    instances[instance_name] = {
                        "name": instance_name,
                        "score": 0,
                        "items": []
                    }
                
                # Calculate Item Score (Placeholder)
                # In a real app, we'd compare vs current gear.
                # Here, we assume every BiS item is an upgrade worth 100 points.
                item_score = 100 
                
                # Add to instance
                instances[instance_name]["score"] += item_score
                instances[instance_name]["items"].append({
                    "name": item['name'],
                    "id": item['id'],
                    "slot": slot,
                    "source": source_text
                })
        
        # Convert to list and sort
        sorted_instances = sorted(instances.values(), key=lambda x: x['score'], reverse=True)
        
        return jsonify(sorted_instances)

    except Exception as e:
        print(f"Error in droptimizer API: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/shopping_list', methods=['POST'])
def get_shopping_list():
    data = request.json
    class_name = data.get('class')
    spec_name = data.get('spec')
    
    try:
        # Import here to avoid circular deps if any
        sys.path.append('/Users/jgrayson/Documents/holocron/scrapers')
        from icy_veins import IcyVeinsScraper
        
        scraper = IcyVeinsScraper(class_name, spec_name)
        consumables = scraper.fetch_consumables()
        
        return jsonify(consumables)

    except Exception as e:
        print(f"Error in shopping list API: {e}")
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        print(f"Error in shopping list API: {e}")
        return jsonify({"error": str(e)}), 500

class LuaParser:
    """Simple parser for WoW SavedVariables (Lua tables)."""
    @staticmethod
    def parse_file(filepath):
        if not os.path.exists(filepath):
            print(f"LuaParser: File not found: {filepath}")
            return {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Very basic parsing for SkillWeaverDB structure
            # We look for SkillWeaverDB = { ... }
            # Since writing a full parser is complex, we'll use a regex strategy for known keys
            # or try to convert Lua table syntax to JSON syntax if it's simple enough.
            
            # Strategy: Extract the "Bags" table content
            # SkillWeaverDB.Bags = { ... } or inside the main table
            
            data = {}
            
            # Regex to find SkillWeaverDB.Bags = { ... }
            # Note: The addon writes: SkillWeaverDB.Bags = { ... }
            # But SavedVariables usually save as:
            # SkillWeaverDB = {
            #    ["Bags"] = {
            #       [1] = { ... },
            #    }
            # }
            
            # Let's try to find the "Bags" section
            # We will use a robust regex to find the list of items
            
            # Pattern for an item entry:
            # { ["name"] = "...", ["link"] = "...", ... }
            # This is fragile.
            
            # Better Strategy: Use `slpp` if available, or a simple state machine.
            # Given constraints, let's try a regex that matches the specific fields we export.
            
            items = []
            # Look for lines that look like item entries
            # We exported: name, link, id, quality, ilvl, sellPrice, slot, bag
            
            # Regex to capture fields. 
            # Example Lua: ["name"] = "Hearthstone", ["id"] = 6948, ...
            
            # We can iterate line by line? SavedVariables are usually pretty-printed.
            
            current_item = {}
            in_bags = False
            
            for line in content.splitlines():
                line = line.strip()
                
                if '["Bags"] = {' in line:
                    in_bags = True
                    continue
                
                if in_bags and line == '},': # End of Bags table (maybe)
                    # This is risky, it might be end of an item
                    pass
                
                if in_bags:
                    # Check for field assignments
                    # ["name"] = "Foo",
                    # ["id"] = 123,
                    
                    # Simple regex for key-value pairs
                    matches = re.findall(r'\["(.*?)"\]\s*=\s*(.*?),', line)
                    for key, val in matches:
                        # Clean value
                        val = val.strip('"')
                        if val.isdigit():
                            val = int(val)
                        current_item[key] = val
                    
                    # If line ends with "}," it might be the end of an item
                    if line.endswith('},'):
                        if current_item:
                            items.append(current_item)
                            current_item = {}

            # If regex failed (e.g. single line file), fallback to mock?
            # No, let's assume standard formatting.
            
            return {"Bags": items}

        except Exception as e:
            print(f"LuaParser Error: {e}")
            return {}

@app.route('/api/junk', methods=['POST'])
def get_junk():
    data = request.json
    class_name = data.get('class')
    spec_name = data.get('spec')
    
    # 1. Get WoW Path from Config
    wow_path = weaver.config.get("integrations", {}).get("wow_path", "")
    
    bag_items = []
    
    if wow_path:
        sv_file = os.path.join(wow_path, "SkillWeaver.lua")
        print(f"Reading SavedVariables from: {sv_file}")
        parsed = LuaParser.parse_file(sv_file)
        bag_items = parsed.get("Bags", [])
    
    # Fallback to Mock if no data found (for demo purposes if user hasn't set path)
    if not bag_items:
        print("No real bag data found. Using Mock.")
        bag_items = [
            {"name": "Rusty Sword (Mock)", "id": 12345, "ilvl": 480, "slot": "Main Hand", "quality": 1, "score": 10},
            {"name": "Shiny Pebble (Mock)", "id": 54321, "ilvl": 1, "slot": "Trinket", "quality": 0, "score": 0},
            {"name": "Fish (Mock)", "id": 11111, "ilvl": 0, "slot": "None", "quality": 1, "score": 0, "is_junk": True}
        ]
    
    equipped_score_threshold = 400 # Mock threshold (e.g. current avg ilvl/score)
    
    junk_list = []
    
    for item in bag_items:
        is_junk = False
        reason = ""
        
        # Quality Map: 0=Poor, 1=Common, 2=Uncommon, 3=Rare, 4=Epic, 5=Legendary
        quality = item.get('quality', 1)
        if isinstance(quality, str):
            # Handle string quality if parsed that way
            if quality == "Poor": quality = 0
            elif quality == "Common": quality = 1
            # ...
        
        # Logic 1: Grey Items
        if quality == 0:
            is_junk = True
            reason = "Poor Quality (Grey)"
            
        # Logic 2: Low Item Level / Score (Simplified)
        # We need real score logic here, but for now use ilvl
        elif item.get('ilvl', 0) < 500 and item.get('classID') == 2: # Weapon < 500
             is_junk = True
             reason = f"Low iLvl ({item.get('ilvl')})"
            
        # Logic 3: Explicit Junk
        elif item.get('is_junk'):
            is_junk = True
            reason = "Trash Item"
            
        if is_junk:
            item['reason'] = reason
            # Format sell price
            price = item.get('sellPrice', 0)
            if price > 0:
                g = price // 10000
                s = (price % 10000) // 100
                c = price % 100
                item['sell_value'] = f"{g}g {s}s {c}c"
            else:
                item['sell_value'] = "0g"
                
            junk_list.append(item)
            
    return jsonify(junk_list)

@app.route('/api/encounter', methods=['POST'])
def get_encounter():
    data = request.json
    instance = data.get('instance', '')
    boss = data.get('boss', '')
    
    try:
        sys.path.append('/Users/jgrayson/Documents/holocron/scrapers')
        from icy_veins import IcyVeinsScraper
        
        # Create scraper (class/spec don't matter for encounter scraping)
        scraper = IcyVeinsScraper("warrior", "arms")
        encounter_data = scraper.fetch_encounter(instance, boss)
        
        return jsonify(encounter_data)
    
    except Exception as e:
        print(f"Error in encounter API: {e}")
        return jsonify({"error": str(e)}), 500

def gen_preview():
    """Generates a MJPEG stream of the screen with overlays."""
    with mss.mss() as sct:
        while True:
            # Capture full screen or a relevant portion?
            # Full screen might be too big. Let's capture the area around the DPS icon for now?
            # Or maybe a scaled down version of the full screen.
            monitor = sct.monitors[1] # Primary monitor
            img = np.array(sct.grab(monitor))
            
            # Draw overlays
            if weaver.config:
                for name, region in weaver.config.get("regions", {}).items():
                    top, left = int(region["top"]), int(region["left"])
                    w, h = int(region["width"]), int(region["height"])
                    # Draw rectangle (BGR color)
                    cv2.rectangle(img, (left, top), (left + w, top + h), (0, 255, 0), 2)
                    cv2.putText(img, name, (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            # Resize for performance
            frame = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
            
            # Encode
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.5) # 2 FPS for preview

@app.route('/api/preview')
def preview():
    return Response(gen_preview(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)
