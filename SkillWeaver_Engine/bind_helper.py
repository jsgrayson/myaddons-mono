#!/usr/bin/env python3
"""
Binding Helper: Sends each key with delay so you can switch to WoW and bind
Layout: F13, F16, F17, F18, F19, HOME, END, DELETE
"""
import serial
import time
import glob

ports = glob.glob("/dev/cu.usbmodem*")
if not ports:
    print("ERROR: No Arduino found!")
    exit(1)

port = ports[0]
print(f"Using port: {port}")
print("Connecting to Arduino...")
s = serial.Serial(port, 250000, timeout=2)
time.sleep(2)

DELAY = 3

BAR_1 = [
    (0x01, "F13"), (0x02, "F16"), (0x03, "F17"), (0x04, "F18"),
    (0x05, "F19"), (0x06, "HOME"), (0x07, "END"), (0x08, "DELETE")
]

BAR_2 = [
    (0x09, "Shift+F13"), (0x0A, "Shift+F16"), (0x0B, "Shift+F17"), (0x0C, "Shift+F18"),
    (0x0D, "Shift+F19"), (0x0E, "Shift+HOME"), (0x0F, "Shift+END"), (0x10, "Shift+DELETE")
]

BAR_3 = [
    (0x11, "Ctrl+F13"), (0x12, "Ctrl+F16"), (0x13, "Ctrl+F17"), (0x14, "Ctrl+F18"),
    (0x15, "Ctrl+F19"), (0x16, "Ctrl+HOME"), (0x17, "Ctrl+END"), (0x18, "Ctrl+DELETE")
]

BAR_4 = [
    (0x19, "Alt+F13"), (0x1A, "Alt+F16"), (0x1B, "Alt+F17"), (0x1C, "Alt+F18"),
    (0x1D, "Alt+F19"), (0x1E, "Alt+HOME"), (0x1F, "Alt+END"), (0x20, "Alt+DELETE")
]

def send_with_delay(byte, name):
    print(f"\n>>> Sending {name} in {DELAY} seconds... CLICK WOW KEYBIND SLOT NOW!")
    for i in range(DELAY, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    s.write(bytes([byte]))
    print(f"  SENT {name}!")
    time.sleep(0.5)

print("\n=== BINDING HELPER ===")
print(f"Layout: F13, F16, F17, F18, F19, HOME, END, DELETE\n")

for bar_name, bar in [("BAR 1 (Base)", BAR_1), ("BAR 2 (Shift)", BAR_2), ("BAR 3 (Ctrl)", BAR_3), ("BAR 4 (Alt)", BAR_4)]:
    print(f"=== {bar_name} ===")
    for byte, name in bar:
        input(f"Ready to bind {name}? Press ENTER, then click WoW slot...")
        send_with_delay(byte, name)
    print(f"\n=== {bar_name} Complete! ===\n")

print("=== ALL DONE! 32 keys bound! ===")
