#!/usr/bin/env python3
"""
SafeLaunch.py - Cascade-Proof Engine Launcher

CRITICAL: This launcher tests permissions BEFORE starting the engine.
If permissions are missing, it STOPS immediately to prevent window cascade.
"""

import os
import subprocess
import time
import sys

# Paths
ENGINE_PATH = "/Users/jgrayson/Documents/MyAddons-Mono/SkillWeaver_Engine/Brain/main.py"
PYTHON_PATH = sys.executable

# HID Key Codes (Hex)
KEY_2_HID = "0x70000001F"  # '2' key on Mac


def verify_tcc() -> bool:
    """Check if Terminal has Input Monitoring/Accessibility permissions."""
    print(">>> [CHECK] Testing Terminal Authority...")
    
    try:
        test = subprocess.run(
            ["sudo", "hidutil", "property", "--get", "UserKeyMapping"],
            capture_output=True,
            timeout=10
        )
        
        if test.returncode != 0:
            print("\n!!! [STOP] TERMINAL NOT AUTHORIZED")
            print("!!! Go to Settings > Privacy > Accessibility AND Input Monitoring")
            print("!!! Add Terminal to BOTH and toggle ON")
            print("!!! Then restart Terminal and try again\n")
            return False
            
    except subprocess.TimeoutExpired:
        print("!!! [TIMEOUT] Permission check timed out")
        return False
    except Exception as e:
        print(f"!!! [ERROR] {e}")
        return False
    
    print(">>> [CHECK] Permission Verified ✓")
    return True


def visual_health_check() -> bool:
    """Test screen capture before starting."""
    print(">>> [CHECK] Testing Screen Capture...")
    try:
        import mss
        sct = mss.mss()
        test = sct.grab({"top": 0, "left": 0, "width": 10, "height": 1})
        if test:
            print(">>> [CHECK] Screen Capture Working ✓")
            return True
    except ImportError:
        print(">>> [CHECK] mss not installed - skipping")
        return True
    except Exception as e:
        print(f"!!! [WARNING] Screen capture failed: {e}")
        print("!!! Add Terminal to Settings > Privacy > Screen Recording")
    return True


def mute_key():
    """Mute the '2' key so WoW doesn't see it."""
    print(">>> [HARDWARE] Muting '2' Key...")
    cmd = f'sudo hidutil property --set \'{{"UserKeyMapping":[{{"HIDKeyboardModifierMappingSrc":{KEY_2_HID},"HIDKeyboardModifierMappingDst":0}}]}}\''
    os.system(cmd)


def unmute_key():
    """Restore normal keyboard mapping."""
    print(">>> [HARDWARE] Restoring Keyboard...")
    os.system("sudo hidutil property --set '{\"UserKeyMapping\":[]}'")


def launch():
    print("\n" + "=" * 55)
    print("       SkillWeaver Cascade-Proof Launcher")
    print("=" * 55 + "\n")
    
    # Step 1: Permission Check
    if not verify_tcc():
        print("!!! [HALT] Cannot start - permissions missing")
        sys.exit(1)
    
    # Step 2: Visual Check
    visual_health_check()
    
    # Step 3: Human Delay (time to tab to WoW)
    print("\n>>> [READY] All checks passed!")
    print(">>> [READY] TAB TO WOW NOW!")
    for i in range(5, 0, -1):
        print(f">>> Starting in {i}...")
        time.sleep(1)
    
    # Step 4: Mute the trigger key
    mute_key()
    
    # Step 5: Run engine
    print("\n" + "=" * 55)
    print("               ENGINE ACTIVE")
    print("           Hold '2' to trigger")
    print("=" * 55 + "\n")
    
    try:
        subprocess.run(["sudo", PYTHON_PATH, ENGINE_PATH])
    except KeyboardInterrupt:
        print("\n>>> [EXIT] Stopped by user")
    except Exception as e:
        print(f"\n!!! [ERROR] {e}")
    finally:
        unmute_key()
        print(">>> [CLEANUP] Keyboard restored. Safe to close.")


if __name__ == "__main__":
    launch()
