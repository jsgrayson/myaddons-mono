"""
test_petweaver_integration.py - Verify PetWeaver Backend Connection

Simulates the full flow:
1. Creates a mock PetWeaver.lua with a queued request
2. Runs holocron_sync.py to process it
3. Verifies the response is written back to PetWeaver.lua
"""

import os
import time
import json
import shutil
from pathlib import Path
import threading
from holocron_sync import HolocronSync

# Setup mock environment
WOW_PATH = Path("/tmp/mock_wow/_retail_")
WTF_PATH = WOW_PATH / "WTF"
ACCOUNT_DIR = WTF_PATH / "Account" / "TEST_ACCOUNT"
SAVED_VARS = ACCOUNT_DIR / "SavedVariables"

def setup_mock_env():
    if WOW_PATH.exists():
        shutil.rmtree(WOW_PATH)
    
    # Ensure full path exists: _retail_/WTF/Account/TEST_ACCOUNT/SavedVariables
    SAVED_VARS.mkdir(parents=True)
    
    print(f"Created mock env at: {WOW_PATH}")
    print(f"SavedVars at: {SAVED_VARS}")
    
    # Create initial PetWeaver.lua
    # Note: In Lua, " inside a string must be escaped as \"
    # So the JSON string {"endpoint": "..."} becomes "{\"endpoint\": \"...\"}"
    # And in Python string literal, backslashes need escaping too.
    
    initial_lua = """
PetWeaverDB = {
    ["apiQueue"] = {
        {
            ["payload"] = "{\\"endpoint\\": \\"/api/petweaver/encounters\\", \\"method\\": \\"GET\\", \\"id\\": \\"TEST-123\\"}",
            ["timestamp"] = 1234567890
        }
    },
    ["apiResponse"] = {}
}
"""
    with open(SAVED_VARS / "PetWeaver.lua", "w") as f:
        f.write(initial_lua)
        
    # Set env var for sync tool
    os.environ["WOW_PATH"] = str(WOW_PATH.parent)

def run_sync_tool():
    # Pass the mock path explicitly (WOW_PATH is the _retail_ folder)
    sync = HolocronSync(wow_path=str(WOW_PATH))
    # Run one pass
    sync.process_queue("PetWeaver")

def verify_response():
    with open(SAVED_VARS / "PetWeaver.lua", "r") as f:
        content = f.read()
        
    print("\nVerifying response in PetWeaver.lua...")
    if '["TEST-123"]' in content and "success = true" in content:
        print("✅ SUCCESS: Response found in SavedVariables!")
        return True
    else:
        print("❌ FAILED: Response not found.")
        print("Content preview:")
        print(content[:500])
        return False

if __name__ == "__main__":
    print("Setting up mock environment...")
    setup_mock_env()
    
    print("Running sync tool...")
    try:
        run_sync_tool()
        time.sleep(1)
        verify_response()
    except Exception as e:
        print(f"Test failed with error: {e}")
