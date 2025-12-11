#!/usr/bin/env python3
"""
goblin_sync.py - GoblinAI Backend Sync Tool

Bridges WoW addon (SavedVariables) ↔ FastAPI backend (ML models)

How it works:
1. Monitors GoblinAI.lua SavedVariables file
2. Processes API request queue from addon
3. Makes HTTP calls to FastAPI server
4. Writes results back to SavedVariables
5. Addon reads updated data on next login/reload

Usage:
    python goblin_sync.py

Configuration:
    Edit SAVED_VARS_PATH and API_URL below
"""

import os
import time
import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

# ============================================================================
# Configuration
# ============================================================================

# Path to SavedVariables file
# macOS example: /Applications/World of Warcraft/_retail_/WTF/Account/ACCOUNTNAME/SavedVariables/GoblinAI.lua
SAVED_VARS_PATH = "/Applications/World of Warcraft/_retail_/WTF/Account/NIGHTHWK77/SavedVariables/GoblinAI.lua"

# FastAPI backend URL
API_URL = "http://localhost:5000"

# Poll interval (seconds)
POLL_INTERVAL = 5

# ============================================================================
# Lua Parser (Simple)
# ============================================================================

def lua_to_python(lua_str: str) -> Any:
    """
    Simple Lua to Python converter
    Handles basic tables, strings, numbers, booleans
    NOTE: For production, use slpp or lua-parser library
    """
    lua_str = lua_str.strip()
    
    # Handle nil
    if lua_str == "nil":
        return None
    
    # Handle booleans
    if lua_str == "true":
        return True
    if lua_str == "false":
        return False
    
    # Handle numbers
    try:
        if '.' in lua_str:
            return float(lua_str)
        return int(lua_str)
    except ValueError:
        pass
    
    # Handle strings
    if lua_str.startswith('"') and lua_str.endswith('"'):
        return lua_str[1:-1]
    if lua_str.startswith("'") and lua_str.endswith("'"):
        return lua_str[1:-1]
    
    # Handle tables (simplified)
    if lua_str.startswith('{') and lua_str.endswith('}'):
        # This is a very basic implementation
        # For production, use a real Lua parser
        return {}
    
    return lua_str

def python_to_lua(obj: Any, indent: int = 0) -> str:
    """
    Convert Python object to Lua table string
    """
    ind = "    " * indent
    
    if obj is None:
        return "nil"
    elif isinstance(obj, bool):
        return str(obj).lower()
    elif isinstance(obj, (int, float)):
        return str(obj)
    elif isinstance(obj, str):
        # Escape quotes
        escaped = obj.replace('"', '\\"')
        return f'"{escaped}"'
    elif isinstance(obj, list):
        if not obj:
            return "{}"
        lines = ["{"]
        for item in obj:
            lines.append(f"{ind}    {python_to_lua(item, indent + 1)},")
        lines.append(f"{ind}}}")
        return "\n".join(lines)
    elif isinstance(obj, dict):
        if not obj:
            return "{}"
        lines = ["{"]
        for key, value in obj.items():
            # Handle numeric keys
            if isinstance(key, int):
                lines.append(f"{ind}    [{key}] = {python_to_lua(value, indent + 1)},")
            else:
                lines.append(f"{ind}    {key} = {python_to_lua(value, indent + 1)},")
        lines.append(f"{ind}}}")
        return "\n".join(lines)
    else:
        return str(obj)

# ============================================================================
# SavedVariables Handler
# ============================================================================

class SavedVariablesHandler:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.data = {}
        
    def read(self) -> Dict[str, Any]:
        """Read and parse SavedVariables file"""
        if not self.file_path.exists():
            print(f"Warning: SavedVariables file not found: {self.file_path}")
            return {}
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract GoblinAIDB table
        # Very simplified regex-based extraction
        match = re.search(r'GoblinAIDB = ({.*?})\s*$', content, re.DOTALL)
        if not match:
            print("Warning: Could not find GoblinAIDB in SavedVariables")
            return {}
        
        # For now, return empty dict
        # In production, use proper Lua parser (slpp, lupa, etc.)
        print("Info: Lua parsing simplified - using mock data")
        
        # Mock structure for testing
        self.data = {
            "apiQueue": [],
            "opportunities": [],
            "marketPrices": {},
            "settings": {
                "useBackend": True
            }
        }
        
        return self.data
    
    def write(self, data: Dict[str, Any]):
        """Write Python dict back to SavedVariables as Lua"""
        self.data = data
        
        # Generate Lua code
        lua_content = f"GoblinAIDB = {python_to_lua(data)}\n"
        
        # Backup original
        if self.file_path.exists():
            backup_path = self.file_path.with_suffix('.lua.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                with open(self.file_path, 'r', encoding='utf-8') as orig:
                    f.write(orig.read())
        
        # Write new data
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(lua_content)
        
        print(f"Wrote updated data to {self.file_path}")

# ============================================================================
# API Client
# ============================================================================

class GoblinAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
    
    def process_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single API request"""
        method = request.get('method', 'GET')
        endpoint = request.get('url', '')
        data = request.get('data')
        
        url = self.base_url + endpoint
        
        try:
            if method == 'GET':
                response = self.session.get(url, timeout=10)
            elif method == 'POST':
                response = self.session.post(url, json=data, timeout=10)
            else:
                print(f"Warning: Unsupported method {method}")
                return None
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError:
            print(f"Error: Could not connect to API at {url}")
            return None
        except requests.exceptions.Timeout:
            print(f"Error: Request to {url} timed out")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"Error: HTTP error {e.response.status_code} for {url}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

# ============================================================================
# Sync Manager
# ============================================================================

class GoblinSyncManager:
    def __init__(self, saved_vars_path: str, api_url: str):
        self.sv_handler = SavedVariablesHandler(saved_vars_path)
        self.api_client = GoblinAPIClient(api_url)
        self.last_sync = 0
    
    def sync_cycle(self):
        """Perform one sync cycle"""
        # Read SavedVariables
        data = self.sv_handler.read()
        
        if not data:
            return
        
        # Process API queue
        queue = data.get('apiQueue', [])
        
        if queue:
            print(f"Processing {len(queue)} queued API requests...")
            
            for request in queue:
                print(f"  → {request.get('method')} {request.get('url')}")
                result = self.api_client.process_request(request)
                
                if result:
                    # Store result based on endpoint
                    endpoint = request.get('url', '')
                    
                    if '/prices' in endpoint:
                        data['marketPrices'] = result.get('prices', {})
                    elif '/opportunities' in endpoint:
                        data['opportunities'] = result.get('opportunities', [])
                    elif '/portfolio' in endpoint:
                        data['portfolio'] = result.get('portfolio', {})
                    elif '/trends' in endpoint:
                        data['marketTrends'] = result.get('trends', [])
            
            # Clear queue
            data['apiQueue'] = []
        
        # Auto-fetch latest data (every 5 minutes)
        now = time.time()
        if now - self.last_sync > 300:
            self.auto_sync(data)
            self.last_sync = now
        
        # Write back to SavedVariables
        self.sv_handler.write(data)
    
    def auto_sync(self, data: Dict[str, Any]):
        """Auto-fetch latest data from backend"""
        print("Auto-syncing latest data from backend...")
        
        # Fetch market prices
        prices = self.api_client.process_request({'method': 'GET', 'url': '/api/goblin/prices'})
        if prices:
            data['marketPrices'] = prices.get('prices', {})
        
        # Fetch opportunities
        opps = self.api_client.process_request({'method': 'GET', 'url': '/api/goblin/opportunities'})
        if opps:
            data['opportunities'] = opps.get('opportunities', [])

# ============================================================================
# Main Loop
# ============================================================================

def main():
    print("=" * 60)
    print("GoblinAI Backend Sync Tool")
    print("=" * 60)
    print(f"SavedVariables: {SAVED_VARS_PATH}")
    print(f"API URL: {API_URL}")
    print(f"Poll Interval: {POLL_INTERVAL}s")
    print()
    
    # Check file exists
    if not Path(SAVED_VARS_PATH).exists():
        print(f"ERROR: SavedVariables file not found!")
        print(f"Please update SAVED_VARS_PATH in this script.")
        print(f"Expected location: {SAVED_VARS_PATH}")
        return
    
    sync_manager = GoblinSyncManager(SAVED_VARS_PATH, API_URL)
    
    print("Starting sync loop... (Ctrl+C to stop)")
    print()
    
    try:
        while True:
            sync_manager.sync_cycle()
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\nSync tool stopped.")

if __name__ == "__main__":
    main()
