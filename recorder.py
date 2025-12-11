import json
import time
import os
import re
import requests
from datetime import datetime

# Configuration
CONFIG_FILE = "recorder_config.json"
DEFAULT_CONFIG = {
    "wtf_path": "/Path/To/World of Warcraft/_retail_/WTF/Account/ACCOUNT_NAME/SavedVariables/PetWeaver.lua",
    "server_url": "http://localhost:5001/api/record_battle",
    "fallback_file": "recorded_battles.json"
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        print(f"Created default config: {CONFIG_FILE}. Please edit 'wtf_path'.")
        return DEFAULT_CONFIG
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def parse_lua_table(content):
    """
    Extremely basic Lua table parser for PetWeaver structure.
    Assumes standard SavedVariables formatting.
    """
    battles = []
    # Regex to find battles
    # This is brittle. A real Lua parser is better, but for "Basic" fallback:
    # We look for the structure.
    
    # Actually, let's just extract strings that look like log lines
    # or use a library if we can install one.
    # For now, let's assume the user copies the content or we read the whole file
    # and try to regex out the "battles" block.
    
    return battles # Placeholder for complex logic

def main():
    config = load_config()
    wtf_path = config["wtf_path"]
    
    print(f"PetWeaver Recorder Watching: {wtf_path}")
    last_mtime = 0
    
    while True:
        if os.path.exists(wtf_path):
            mtime = os.path.getmtime(wtf_path)
            if mtime > last_mtime:
                print("File changed! Parsing...")
                last_mtime = mtime
                
                try:
                    with open(wtf_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    # TODO: Implement robust Lua parsing here
                    # For now, we just acknowledge the change
                    print(f"Read {len(content)} bytes.")
                    
                    # Mock Data for testing fallback
                    data = {"timestamp": time.time(), "status": "raw_lua_read"}
                    
                    # Try Server
                    try:
                        requests.post(config["server_url"], json=data, timeout=2)
                        print("Sent to Server.")
                    except:
                        print("Server Down. Saving to Fallback.")
                        with open(config["fallback_file"], 'a') as f:
                            f.write(json.dumps(data) + "\n")
                            
                except Exception as e:
                    print(f"Error reading file: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    main()
