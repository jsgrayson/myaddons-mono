import os
import sys
import subprocess
import time
import mss

# THE VERIFIED PATHS
REAL_PY = "/usr/local/Cellar/python@3.11/3.11.5/Frameworks/Python.framework/Versions/3.11/bin/python3.11"
ENGINE = "/Users/jgrayson/Documents/MyAddons-Mono/SkillWeaver_Engine/Brain/main.py"

def mute_2_key(active=True):
    """Mutes/Restores the 2 key on the MacBook keyboard."""
    mapping = '[{"HIDKeyboardModifierMappingSrc":0x70000001F,"HIDKeyboardModifierMappingDst":0}]' if active else "[]"
    os.system(f"sudo hidutil property --set '{{\"UserKeyMapping\":{mapping}}}'")

def verify_and_hold():
    """Circuit breaker: Stops the loop if permissions are missing."""
    print(">>> [CHECK] Testing Screen Access...")
    try:
        with mss.mss() as sct:
            # Attempt exactly ONE pixel grab
            sct.grab({"top": 0, "left": 0, "width": 1, "height": 1})
            print(">>> [SUCCESS] Permission verified.")
            return True
    except Exception:
        print("\n!!! [SECURITY BLOCK] macOS is denying screen access.")
        print("!!! I am HALTING now to prevent a window cascade.")
        print(">>> ACTION: Add the python3.11 binary to Screen Recording settings.")
        # We exit immediately. This is the only way to stop the cascade.
        sys.exit(1)

if __name__ == "__main__":
    # 1. Stop the cascade before it starts
    verify_and_hold()

    # 2. Mute the key (The call I missed before)
    mute_2_key(True)

    # 3. Launch Engine
    print(">>> [ENGINE] Key Muted. Starting in 3s... TAB TO WOW.")
    time.sleep(3)
    try:
        # Use 'sudo -E' to carry permissions into the engine
        subprocess.run(["sudo", "-E", REAL_PY, ENGINE, "--scale", "2"])
    except KeyboardInterrupt:
        print("\n>>> [STOP] Cleaning up...")
    finally:
        # 4. ALWAYS restore the key
        mute_2_key(False)