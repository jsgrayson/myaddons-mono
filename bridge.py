import time
import os
import json
import requests
import socket
import shutil
import hashlib
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# CONFIGURATION
# TODO: User needs to set the correct Account Name
WOW_SAVED_VARIABLES_PATH = "/Applications/World of Warcraft/_retail_/WTF/Account/YOUR_ACCOUNT_NAME_HERE/SavedVariables"
SERVER_URL = "http://localhost:5001/upload_data"

class MirrorClient:
    def __init__(self, server_url, wtf_path):
        self.server_url = server_url
        self.wtf_path = wtf_path
        self.hostname = socket.gethostname()
        self.device_type = "UNKNOWN"
        
    def register(self):
        """Register device with server."""
        try:
            resp = requests.post(f"{self.server_url}/api/mirror/register", json={"hostname": self.hostname})
            if resp.status_code == 200:
                data = resp.json()
                self.device_type = data.get('device_type')
                print(f"[Mirror] Registered as {self.device_type} ({self.hostname})")
                return True
            else:
                print(f"[Mirror] Registration failed with status {resp.status_code}: {resp.text}")
        except requests.exceptions.ConnectionError:
            print(f"[Mirror] Registration failed: Could not connect to server at {self.server_url}")
        except Exception as e:
            print(f"[Mirror] Registration failed: {e}")
        return False

    def backup_wtf(self):
        """Create a safety backup of WTF."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(self.wtf_path, "Backups")
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup Macros
            # TODO: Replace "YOUR_ACCOUNT" with the actual account name from WOW_SAVED_VARIABLES_PATH
            account_name = os.path.basename(os.path.dirname(WOW_SAVED_VARIABLES_PATH))
            macro_file = os.path.join(self.wtf_path, "Account", account_name, "macros-cache.txt")
            if os.path.exists(macro_file):
                shutil.copy2(macro_file, os.path.join(backup_dir, f"macros_{timestamp}.txt"))
                print(f"[Mirror] Backed up macros to {backup_dir}")
            else:
                print(f"[Mirror] Macro file not found at {macro_file}. Skipping macro backup.")
        except Exception as e:
            print(f"[Mirror] Backup failed: {e}")

    def sync_macros(self):
        """Sync macros with server."""
        try:
            # 1. Read Local Macros
            # TODO: Replace "YOUR_ACCOUNT" with actual account discovery
            account_name = os.path.basename(os.path.dirname(WOW_SAVED_VARIABLES_PATH))
            macro_file = os.path.join(self.wtf_path, "Account", account_name, "macros-cache.txt")
            
            if not os.path.exists(macro_file):
                print(f"[Mirror] Macro file not found at {macro_file}")
                return

            with open(macro_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 2. Upload Current (Backup/Sync Up)
            payload = {
                "hostname": self.hostname,
                "file_type": "MACROS",
                "content": content,
                "char_guid": "GLOBAL" 
            }
            requests.post(f"{self.server_url}/api/mirror/upload", json=payload)
            
            # 3. Check for Updates (Sync Down)
            resp = requests.get(f"{self.server_url}/api/mirror/sync", params={
                "hostname": self.hostname,
                "file_type": "MACROS",
                "char_guid": "GLOBAL"
            })
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("found"):
                    server_content = data.get("content")
                    # Simple check: if different, overwrite (Safety backup already done on init)
                    if server_content != content:
                        print("[Mirror] New macros found on server. Syncing down...")
                        with open(macro_file, 'w', encoding='utf-8') as f:
                            f.write(server_content)
                        print("[Mirror] Macros synced successfully.")
                    else:
                        print("[Mirror] Macros are in sync.")
            
        except Exception as e:
            print(f"[Mirror] Sync failed: {e}")

class SavedVariablesHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        
        filename = os.path.basename(event.src_path)
        
        # Phase 1-5: DataStore
        if filename.startswith("DataStore") and filename.endswith(".lua"):
            print(f"Detected change in {filename}. Processing...")
            self.process_lua_file(event.src_path, filename)
            
        # Phase 6: SavedInstances (Pathfinder)
        elif filename == "SavedInstances.lua":
            print(f"Detected change in {filename}. Processing...")
            self.process_lua_file(event.src_path, filename)

        # Phase 8: DataStore_Reputations (Diplomat)
        elif filename == "DataStore_Reputations.lua":
            print(f"Detected change in {filename}. Processing...")
            self.process_lua_file(event.src_path, filename)

        # Transmog
        elif filename == "CanIMogIt.lua":
            print(f"Detected change in {filename}. Processing...")
            self.process_lua_file(event.src_path, filename)

        # DeepPockets (Inventory & Recipes)
        elif filename == "DeepPockets.lua":
            print(f"Detected change in {filename}. Processing...")
            self.process_lua_file(event.src_path, filename)

    def process_lua_file(self, filepath, filename):
        """
        Reads the Lua file, attempts to parse it (naive parsing or using a library),
        and sends it to the server.
        """
        try:
            # TODO: Implement robust Lua to JSON parsing. 
            # For now, we will just read the raw content and send it wrapped.
            # In a real scenario, we'd use slpp or similar to parse Lua tables to Python dicts.
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            payload = {
                "source": filename.replace(".lua", ""),
                "data": content # Sending raw content for server to parse for now
            }

            response = requests.post(SERVER_URL, json=payload)
            if response.status_code == 200:
                print(f"Successfully uploaded {filename}")
            else:
                print(f"Failed to upload {filename}: {response.text}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    print(f"Starting Holocron Bridge...")
    print(f"Watching: {WOW_SAVED_VARIABLES_PATH}")
    
    event_handler = SavedVariablesHandler()
    observer = Observer()
    
    # Check if path exists to avoid immediate crash
    if not os.path.exists(WOW_SAVED_VARIABLES_PATH):
        print(f"WARNING: Path not found: {WOW_SAVED_VARIABLES_PATH}")
        print("Please edit bridge.py to set the correct WOW_SAVED_VARIABLES_PATH.")
    else:
        observer.schedule(event_handler, WOW_SAVED_VARIABLES_PATH, recursive=False)
        observer.start()
        
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
