#!/usr/bin/env python3
"""
Test: sends F13 (byte 0x01) with debug output
"""
import serial
import time
import glob

# Find Arduino
ports = glob.glob("/dev/cu.usbmodem*")
if not ports:
    print("ERROR: No Arduino found!")
    exit(1)

port = ports[0]
print(f"Using port: {port}")

print("Connecting to Arduino...")
s = serial.Serial(port, 250000, timeout=2)
time.sleep(2)

print("Sending handshake (0xBD)...")
s.write(bytes([0xBD]))
time.sleep(0.2)
resp = s.read(10)
print(f"Handshake response: {resp}")

if resp != b'K':
    print("WARNING: Handshake failed or different response!")

print("\n>>> SWITCH TO WOW NOW! Sending F13 (0x01) in 3 seconds...")
for i in range(3, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

print("SENDING F13 (byte 0x01)...")
s.write(bytes([0x01]))  # Now using 0x01 for F13
print("Sent! Check WoW for F13 keypress.")

time.sleep(0.5)
extra = s.read(100)
if extra:
    print(f"Arduino sent back: {extra}")
