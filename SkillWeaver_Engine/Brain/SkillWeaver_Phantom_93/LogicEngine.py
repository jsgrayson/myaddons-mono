# LogicEngine.py
# PROTOCOL v22.0 (STEALTH PHANTOM)
# Differential RGB Decoding: (Blue - Red) = Data

import time
import json
import serial
import mss
import numpy as np
from PIL import Image

# CONFIGURATION
LOGIC_DB_PATH = "93.json"
SERIAL_PORT = "COM3"
BAUD_RATE = 9600
RETINA_SCALE = 2 # Set to 2 for Mac/Retina, 1 for Standard

# GAME STATE (MIRRORS LUA)
class GameState:
    def __init__(self):
        self.combat = False
        self.player_hp = 100
        self.target_hp = 100
        self.resources = 0
        self.range_tier = 0
        self.pet_hp = 100
        self.snapshot_active = False
        self.safe_movement = True # Default Safety

    def decode_pixel(self, px):
        # Differential Decoding
        # Base Color is (0.1, 0.1, 0.1)
        # Data is added to Blue channel.
        # So Data = Blue - Red
        # We assume 0-255 inputs from mss
        
        r = int(px[0])
        b = int(px[2])
        
        # Simple subtraction with floor clamping
        val = max(0, b - r)
        return val

    def update(self, pixels):
        # Pixel mapping (Retina stride handled in main loop)
        
        self.combat = self.decode_pixel(pixels[2]) > 128
        self.player_hp = (self.decode_pixel(pixels[3]) / 255.0) * 100
        self.target_hp = (self.decode_pixel(pixels[4]) / 255.0) * 100
        self.pet_hp = (self.decode_pixel(pixels[22]) / 255.0) * 100
        self.snapshot_active = self.decode_pixel(pixels[30]) > 128
        
        # Advanced Parsing
        # Pixel 16: Debuffs (1=Root, 2=Snare, 4=Scatter)
        debuff_val = int((self.decode_pixel(pixels[16]) / 255.0) * 10)
        self.rooted = (debuff_val & 1) > 0
        self.scattered = (debuff_val & 4) > 0

# LOAD LOGIC
with open(LOGIC_DB_PATH, 'r') as f:
    ROTATION = json.load(f)

def evaluate_logic(state):
    for rule in ROTATION:
        # Check Safety Gate for Movement
        if rule.get('action_type') == 'SAFE_MOVEMENT' and not state.safe_movement:
            continue
            
        # Check Conditions
        conditions_met = True
        for cond in rule['conditions']:
            metric = cond['metric']
            val = cond['val']
            op = cond['op']
            
            current_val = getattr(state, metric, 0)
            
            if op == '==' and current_val != val: conditions_met = False
            elif op == '>' and current_val <= val: conditions_met = False
            elif op == '<' and current_val >= val: conditions_met = False
            
            if not conditions_met: break
            
        if conditions_met:
            return rule['hex']
    return 0

def main():
    print("SkillWeaver Engine v22.0 Online...")
    sct = mss.mss()
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
    except:
        print("Warning: Serial Port not found. Running in simulation mode.")
        ser = None
        
    state = GameState()
    
    # 1px height, 32px width (64 physical on retina)
    monitor = {"top": 1080 - 1, "left": 0, "width": 32 * RETINA_SCALE, "height": 1} 
    
    while True:
        img = np.array(sct.grab(monitor))
        
        # Parse Pixels (Handle Retina Stride)
        # We need RGB for differential decoding
        # mss returns BGRA, so slice properly
        # We take every RETINA_SCALE pixel from the first row
        
        raw_pixels = img[0, ::RETINA_SCALE] 
        # Convert BGRA to RGB if needed, but our index logic (0=B, 2=R) handles it?
        # MSS usually returns BGRA. 
        # Index 0 is Blue, Index 1 is Green, Index 2 is Red.
        # Our decode logic uses px[0] and px[2].
        # If Lua sets R=Base, B=Base+Diff
        # We want B - R. 
        # So we want Index 0 - Index 2.
        
        # Pass raw BGRA pixels to update
        state.update(raw_pixels)
        
        if state.combat:
            action_hex = evaluate_logic(state)
            if action_hex > 0:
                print(f"Action: {hex(action_hex)}")
                if ser:
                    ser.write(bytes([action_hex]))
                time.sleep(0.1 + (np.random.random() * 0.05)) # Human Jitter
        
        time.sleep(0.01)

if __name__ == "__main__":
    main()
