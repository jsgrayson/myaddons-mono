import hid
import time

# Targeted Path from your check_kb.py output
TARGET_PATH = b'DevSrvsID:4294969131'

try:
    device = hid.device()
    device.open_path(TARGET_PATH) # Open by path, not ID
    device.set_nonblocking(True)
    print(f"Connected to Keys at {TARGET_PATH}")
    print("Press your muted '2' key...")
    
    while True:
        report = device.read(64)
        if report:
            # Check the raw byte array for the '2' key code (31 / 0x1F)
            if 31 in report or 0x1F in report:
                print(">>> SUCCESS: Python saw the '2' key!")
        time.sleep(0.01)
except Exception as e:
    print(f"Error: {e}")
