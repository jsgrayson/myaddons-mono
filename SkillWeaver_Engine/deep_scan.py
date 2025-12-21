import hid
import time

# Your specific Hardware IDs
VID = 0x05AC
PID = 0x8104

print("--- INITIALIZING DEEP SCAN ---")
devices = []

# Enumerate all interfaces for your keyboard
for info in hid.enumerate(VID, PID):
    try:
        dev = hid.device()
        dev.open_path(info['path'])
        dev.set_nonblocking(True)
        devices.append((dev, info['path']))
        print(f"OPENED: {info['path']}")
    except Exception as e:
        print(f"FAILED: {info['path']} - {e}")

if not devices:
    print("\n[ERROR] Could not open any device paths. Check Accessibility/Input Monitoring.")
    exit()

print(f"\nMonitoring {len(devices)} paths. Press your muted '2' key now...")

try:
    while True:
        for dev, path in devices:
            report = dev.read(64)
            if report:
                # 0x1F (31) is the HID code for the '2' key
                if 0x1F in report or 31 in report:
                    print(f"\n[HIT] Signal detected on path: {path}")
                    print(f"Raw Report: {list(report)}")
        time.sleep(0.01) # 100Hz scan
except KeyboardInterrupt:
    print("\nClosing links...")
    for dev, path in devices:
        dev.close()
