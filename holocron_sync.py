"""
holocron_sync.py - Universal Sync Tool for Holocron Suite

Monitors SavedVariables for multiple addons (GoblinAI, PetWeaver, DeepPockets)
and syncs data with the Python backend.

Supported Addons:
1. GoblinAI - Market data, prices, opportunities
2. PetWeaver - Pet battle strategies, team validation
3. DeepPockets - Inventory syncing

Usage:
    python holocron_sync.py
"""

import time
import json
import os
import re
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Configuration
# Try to auto-detect WoW path or use env var
WOW_PATH = os.environ.get('WOW_PATH', '/Applications/World of Warcraft/_retail_')
WTF_PATH = Path(WOW_PATH) / "WTF"
API_BASE_URL = "http://localhost:5001"

# Addon Configurations
ADDONS = {
    "GoblinAI": {
        "saved_vars": "GoblinAI.lua",
        "db_name": "GoblinAIDB",
        "api_queue_key": "apiQueue",
        "api_response_key": "apiResponse",
    },
    "PetWeaver": {
        "saved_vars": "PetWeaver.lua",
        "db_name": "PetWeaverDB",
        "api_queue_key": "apiQueue",
        "api_response_key": "apiResponse",
    },
    "DeepPockets": {
        "saved_vars": "DeepPockets.lua",
        "db_name": "DeepPocketsDB",
        "api_queue_key": "apiQueue",
        "api_response_key": "apiResponse",
    },
    "HolocronViewer": {
        "saved_vars": "HolocronViewer.lua",
        "db_name": "HolocronViewerDB",
        "api_queue_key": "apiQueue",
        "api_response_key": "apiResponse",
    }
}

class HolocronSync:
    def __init__(self, wow_path=None):
        self.session = requests.Session()
        self.last_sync_time = {}
        
        # Use provided path or env var or default
        if wow_path:
            self.wow_path = Path(wow_path)
        else:
            self.wow_path = Path(os.environ.get('WOW_PATH', '/Applications/World of Warcraft/_retail_'))
            
        self.wtf_path = self.wow_path / "WTF"
        
        # Find account directory
        self.account_dir = self._find_account_dir()
        if not self.account_dir:
            print(f"Error: Could not find account directory in {self.wtf_path}")
            # Don't exit in init for testability, just warn
            # exit(1) 
            
        if self.account_dir:
            print(f"Monitoring account: {self.account_dir.name}")
        print(f"Backend URL: {API_BASE_URL}")
        print("-" * 50)

    def _find_account_dir(self) -> Path:
        """Find the first account directory in WTF/Account"""
        account_base = self.wtf_path / "Account"
        if not account_base.exists():
            return None
            
        # Return first directory that isn't SavedVariables
        for path in account_base.iterdir():
            if path.is_dir() and path.name != "SavedVariables":
                return path
        return None

    def _get_saved_vars_path(self, addon_name: str) -> Path:
        """Get path to SavedVariables file for an addon"""
        return self.account_dir / "SavedVariables" / ADDONS[addon_name]["saved_vars"]

    def _parse_lua_table(self, content: str, db_name: str) -> Dict:
        """
        Simple Lua table parser. 
        Extracts the main DB table.
        Note: This is a simplified parser. For complex data, use a proper Lua parser.
        """
        # Find the start of the table
        match = re.search(f"{db_name}\\s*=\\s*{{", content)
        if not match:
            return {}
            
        # Extract the table content (simplified - assumes balanced braces or simple structure)
        # For the sync tool, we mainly care about apiQueue which is usually at the top level
        
        # Strategy: Look for "apiQueue" = { ... }
        queue_match = re.search(r'\["apiQueue"\]\s*=\s*{(.*?)},', content, re.DOTALL)
        if not queue_match:
            # Try without brackets
            queue_match = re.search(r'apiQueue\s*=\s*{(.*?)},', content, re.DOTALL)
            
        queue_data = []
        if queue_match:
            queue_content = queue_match.group(1)
            # Parse individual requests
            # This is tricky with regex. In a real app, use `slpp` or `lupa`.
            # For now, we'll assume a specific format or just clear the queue
            pass

        return {"apiQueue": []} # Placeholder - we need a real parser for read/write

    def _python_to_lua(self, data: Any) -> str:
        """Convert Python object to Lua string"""
        if isinstance(data, bool):
            return "true" if data else "false"
        elif isinstance(data, (int, float)):
            return str(data)
        elif isinstance(data, str):
            # Escape quotes
            safe_str = data.replace('"', '\\"').replace('\n', '\\n')
            return f'"{safe_str}"'
        elif isinstance(data, list):
            items = [self._python_to_lua(item) for item in data]
            return "{" + ", ".join(items) + "}"
        elif isinstance(data, dict):
            items = [f'["{k}"] = {self._python_to_lua(v)}' for k, v in data.items()]
            return "{" + ", ".join(items) + "}"
        elif data is None:
            return "nil"
        return '"{}"'.format(str(data))

    def process_queue(self, addon_name: str):
        """
        Read SavedVariables, process API queue, write back responses.
        
        Since parsing Lua is hard without a library, we'll use a simpler approach:
        1. Read the file
        2. Look for the apiQueue section
        3. If found, extract requests
        4. Execute requests
        5. Rewrite the file with empty queue and new responses
        """
        file_path = self._get_saved_vars_path(addon_name)
        if not file_path.exists():
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file was modified recently
            mtime = file_path.stat().st_mtime
            if mtime == self.last_sync_time.get(addon_name, 0):
                return
            self.last_sync_time[addon_name] = mtime

            # 1. Extract Requests
            # We look for the pattern: ["request"] = { ... } inside apiQueue
            # This is a hacky parser. Ideally use `slpp`.
            
            # For this MVP, we'll assume the addon writes a specific marker line
            # or we just look for specific request patterns.
            
            # BETTER APPROACH:
            # The addon writes requests to a SEPARATE file if possible? No, WoW sandbox.
            # We have to parse the Lua.
            
            # Let's try to find JSON-encoded requests in the Lua file
            # The addon can serialize requests to JSON strings to make it easier
            
            requests_found = []
            
            # Regex to find JSON strings in apiQueue
            # Example: ["payload"] = "{\"endpoint\": \"...\"}"
            # We need to be careful about escaped quotes
            
            # This regex captures the content inside the quotes of ["payload"] = "..."
            # It handles escaped quotes inside the string
            matches = re.finditer(r'\["payload"\]\s*=\s*"(.*?)(?<!\\)"', content)
            
            for match in matches:
                try:
                    # Unescape Lua string:
                    # 1. \" becomes "
                    # 2. \\ becomes \
                    json_str = match.group(1).replace('\\"', '"').replace('\\\\', '\\')
                    
                    # Debug print
                    # print(f"DEBUG JSON: {json_str}")
                    
                    req_data = json.loads(json_str)
                    requests_found.append(req_data)
                except Exception as e:
                    print(f"Error parsing request in {addon_name}: {e}")
                    # print(f"Bad string: {match.group(1)}")

            if not requests_found:
                return

            print(f"[{addon_name}] Found {len(requests_found)} requests")
            
            # 2. Process Requests
            responses = []
            for req in requests_found:
                endpoint = req.get('endpoint')
                method = req.get('method', 'GET')
                params = req.get('params', {})
                req_id = req.get('id')
                
                print(f"  Processing: {method} {endpoint}")
                
                try:
                    url = f"{API_BASE_URL}{endpoint}"
                    if method == 'GET':
                        resp = self.session.get(url, params=params, timeout=5)
                    else:
                        resp = self.session.post(url, json=params, timeout=5)
                        
                    resp_data = resp.json()
                    responses.append({
                        "id": req_id,
                        "success": True,
                        "data": resp_data
                    })
                except Exception as e:
                    print(f"  API Error: {e}")
                    responses.append({
                        "id": req_id,
                        "success": False,
                        "error": str(e)
                    })

            # 3. Write Responses
            # We need to inject these responses back into the Lua file
            # and CLEAR the queue.
            
            # Construct Lua table for responses
            lua_responses = "{\n"
            for resp in responses:
                # Serialize data to JSON string for easy Lua parsing
                json_data = json.dumps(resp['data']).replace('"', '\\"')
                lua_responses += f'    ["{resp["id"]}"] = {{ success = {str(resp["success"]).lower()}, data = "{json_data}" }},\n'
            lua_responses += "}"
            
            # Replace apiResponse table
            # Pattern: ["apiResponse"] = { ... }
            # We replace the content inside the braces
            
            # First, clear apiQueue
            # Find: ["apiQueue"] = { ... }
            # Replace with: ["apiQueue"] = {}
            
            # This regex is dangerous if the file structure varies.
            # Safer: Append a command to a new file that the addon loads? No.
            
            # For MVP: We will append a "Sync" file or just overwrite specific sections if we can identify them reliably.
            # Or, we assume the addon formats the file in a specific way.
            
            # Let's try a safer replacement using known keys
            new_content = content
            
            # Clear Queue
            new_content = re.sub(
                r'\["apiQueue"\]\s*=\s*{[^}]*}', 
                '["apiQueue"] = {}', 
                new_content
            )
            
            # Write Responses
            # If apiResponse exists, replace it. If not, we might have trouble.
            if '["apiResponse"]' in new_content:
                new_content = re.sub(
                    r'\["apiResponse"\]\s*=\s*{[^}]*}', 
                    f'["apiResponse"] = {lua_responses}', 
                    new_content
                )
            else:
                # Insert it into the main table
                # Find end of main table
                new_content = new_content.replace(
                    f'{ADDONS[addon_name]["db_name"]} = {{',
                    f'{ADDONS[addon_name]["db_name"]} = {{\n    ["apiResponse"] = {lua_responses},'
                )

            # Write back
            # Create backup first
            backup_path = file_path.with_suffix('.lua.bak')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            print(f"[{addon_name}] Synced {len(responses)} responses")

        except Exception as e:
            print(f"Error syncing {addon_name}: {e}")

    def write_lua_response(self, addon_name: str, req_id: str, success: bool, data_str: str):
        """
        Manually write a response to the SavedVariables file.
        Useful for testing or external tools.
        """
        file_path = self._get_saved_vars_path(addon_name)
        if not file_path.exists():
            print(f"File not found: {file_path}")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Construct response entry
            # Escape quotes in data_str
            safe_data = data_str.replace('"', '\\"')
            response_entry = f'    ["{req_id}"] = {{ success = {str(success).lower()}, data = "{safe_data}" }},\n'

            # Inject into apiResponse
            if '["apiResponse"]' in content:
                # Append to existing table
                # Find the start of apiResponse
                # This is tricky with regex replacement for appending.
                # Easier to just replace the whole table if we assume we are the only writer
                # But for testing, we might want to append.
                
                # Simple approach: Replace the opening brace with opening brace + entry
                new_content = re.sub(
                    r'(\["apiResponse"\]\s*=\s*{)', 
                    f'\\1\n{response_entry}', 
                    content
                )
            else:
                # Insert new table
                new_content = content.replace(
                    f'{ADDONS[addon_name]["db_name"]} = {{',
                    f'{ADDONS[addon_name]["db_name"]} = {{\n    ["apiResponse"] = {{\n{response_entry}    }},'
                )

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            print(f"[{addon_name}] Wrote response for {req_id}")

        except Exception as e:
            print(f"Error writing response for {addon_name}: {e}")

    def run(self):
        print("Holocron Sync Tool Running...")
        print("Press Ctrl+C to stop")
        
        while True:
            for addon_name in ADDONS:
                self.process_queue(addon_name)
            time.sleep(2)  # Check every 2 seconds

if __name__ == "__main__":
    sync = HolocronSync()
    try:
        sync.run()
    except KeyboardInterrupt:
        print("\nStopping sync tool.")
