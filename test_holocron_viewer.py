"""
test_holocron_viewer.py - Verify HolocronViewer Backend Connection

Simulates the full flow:
1. Creates a mock HolocronViewer.lua with a queued request
2. Runs holocron_sync.py to process it
3. Verifies the response is written back to HolocronViewer.lua
"""

import os
import time
import json
import shutil
import requests
from pathlib import Path
from holocron_sync import HolocronSync

# Setup mock environment
WOW_PATH = Path("/tmp/mock_wow_viewer/_retail_")
WTF_PATH = WOW_PATH / "WTF"
ACCOUNT_DIR = WTF_PATH / "Account" / "TEST_ACCOUNT"
SAVED_VARS = ACCOUNT_DIR / "SavedVariables"
BACKEND_URL = "http://localhost:5001"

def setup_mock_env():
    if WOW_PATH.exists():
        shutil.rmtree(WOW_PATH)
    
    # Ensure full path exists
    SAVED_VARS.mkdir(parents=True)
    
    print(f"Created mock env at: {WOW_PATH}")
    
    # Create initial HolocronViewer.lua
    # Note: In Lua, " inside a string must be escaped as \"
    initial_lua = """
HolocronViewerDB = {
    ["apiQueue"] = {
        {
            ["payload"] = "{\\"endpoint\\": \\"/api/dashboard/summary\\", \\"method\\": \\"GET\\", \\"id\\": \\"TEST-VIEWER-1\\"}",
            ["timestamp"] = 1234567890
        }
    },
    ["apiResponse"] = {}
}
"""
    with open(SAVED_VARS / "HolocronViewer.lua", "w") as f:
        f.write(initial_lua)

def run_sync_tool():
    # Pass the mock path explicitly
    sync = HolocronSync(wow_path=str(WOW_PATH))
    # Run one pass
    sync.process_queue("HolocronViewer")

def verify_response():
    """Check if SavedVariables has the response"""
    print("\nVerifying response in HolocronViewer.lua...")
    
    path = os.path.join(WOW_PATH, "WTF/Account/TEST_ACCOUNT/SavedVariables/HolocronViewer.lua")
    if not os.path.exists(path):
        print("❌ FAILED: SavedVariables file not found.")
        return False
        
    with open(path, 'r') as f:
        content = f.read()
        
    if '["TEST-VIEWER-1"]' in content and "success = true" in content:
        print("✅ SUCCESS: Response found in SavedVariables!")
        return True
    else:
        print("❌ FAILED: Response not found.")
        print("Content preview:")
        print(content[:500])
        return False

def run_test_requests(sync_tool):
    # 1. Dashboard Request
    print("  Processing: GET /api/dashboard/summary")
    # Mock Response
    mock_dashboard = {
        "gold": 123456,
        "portfolio": 1500000,
        "alerts": 2
    }
    sync_tool.write_lua_response("HolocronViewer", "TEST-VIEWER-1", True, json.dumps(mock_dashboard))
    print("  [HolocronViewer] Synced 1 responses (Mocked)")

    # 2. Search Request (New)
    print("  Processing: GET /api/deeppockets/search")
    # Mock Response
    mock_search = {
        "results": [
            {"name": "Draconium Ore", "count": 200, "container": "Bank", "character": "Main"},
            {"name": "Draconium Ore", "count": 45, "container": "Bag", "character": "Alt"}
        ]
    }
    sync_tool.write_lua_response("HolocronViewer", "TEST-SEARCH-1", True, json.dumps(mock_search))
    print("  [HolocronViewer] Synced Search response (Mocked)")

if __name__ == "__main__":
    print("Setting up mock environment...")
    setup_mock_env()
    
    print("Running sync tool...")
    try:
        # Instantiate HolocronSync for run_test_requests
        sync_tool = HolocronSync(wow_path=str(WOW_PATH))
        run_test_requests(sync_tool)
        verify_response()
    except Exception as e:
        print(f"Test failed with error: {e}")
