# SKILLWEAVER LOGIC ENGINE v4.1 (VISION CORE)
# PROTOCOL: DARK MATTER (GAIN 0.90)

import mss
import mss.tools
import numpy as np
import time
import sys
import os
import serial # Requires pyserial

# --- CONFIGURATION ---
RETINA_SCALE = 2 # 2 for Mac, 1 for Windows
SERIAL_PORT = 'COM3' 
SERIAL_BAUD = 9600
# ---------------------

# --- FULL SPEC DATABASE ---
SPEC_DB = {
    11: "Warrior - Arms",
    12: "Warrior - Fury",
    13: "Warrior - Protection",
    21: "Paladin - Holy",
    22: "Paladin - Protection",
    23: "Paladin - Retribution",
    31: "Hunter - Beast Mastery",
    32: "Hunter - Marksmanship",
    33: "Hunter - Survival",
    41: "Rogue - Assassination",
    42: "Rogue - Outlaw",
    43: "Rogue - Subtlety",
    51: "Priest - Discipline",
    52: "Priest - Holy",
    53: "Priest - Shadow",
    61: "Death Knight - Blood",
    62: "Death Knight - Frost",
    63: "Death Knight - Unholy",
    71: "Shaman - Elemental",
    72: "Shaman - Enhancement",
    73: "Shaman - Restoration",
    81: "Mage - Arcane",
    82: "Mage - Fire",
    83: "Mage - Frost",
    91: "Warlock - Affliction",
    92: "Warlock - Demonology",
    93: "Warlock - Destruction",
    101: "Monk - Brewmaster",
    102: "Monk - Mistweaver",
    103: "Monk - Windwalker",
    111: "Druid - Balance",
    112: "Druid - Feral",
    113: "Druid - Guardian",
    114: "Druid - Restoration",
    121: "Demon Hunter - Havoc",
    122: "Demon Hunter - Vengeance",
    123: "Demon Hunter - Devourer",
    131: "Evoker - Devastation",
    132: "Evoker - Preservation",
    133: "Evoker - Augmentation",
}

class HardwareBridge:
    def __init__(self):
        self.serial = None
        try:
            self.serial = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=0.05)
            print(f"[HARDWARE] Connected to Neural Hand at {SERIAL_PORT}")
        except:
            print("[HARDWARE] Emulation Mode")

    def press(self, key_code):
        if self.serial:
            self.serial.write(bytes.fromhex(key_code))

class VisionSystem:
    def __init__(self):
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]
        self.uplink_y = 0
        self.uplink_x = 0
        self.scale = RETINA_SCALE
        self.state = {}
        
    def decode_differential(self, r, g, b):
        """
        Recovers value from Blue-Red differential.
        LUA: Base(0.08) + (Val/255 * 0.90)
        """
        diff = int(b) - int(r)
        # 0.90 * 255 = 229.5 max diff. 
        # Using 215.0 as divisor provides safety margin for color compression/gamma
        val = (diff / 215.0) * 255.0
        return max(0, min(255, val))

    def calibrate(self):
        print("------------------------------------------------")
        print("[BOOT] VISION SYSTEM v4.1 INITIALIZING...")
        print("------------------------------------------------")

        scan_height = self.monitor["height"] // 2
        scan_area = {
            "top": self.monitor["height"] - scan_height,
            "left": 0,
            "width": 64, 
            "height": scan_height
        }
        
        img = np.array(self.sct.grab(scan_area))
        
        found = False
        # Scan specifically for the pure white/blue differential pilot
        for y in range(scan_height - 1, 0, -1):
            for x in range(0, 10): 
                px = img[y, x]
                b, g, r = int(px[0]), int(px[1]), int(px[2])
                
                # Check for Pilot Signal (Index 0)
                # Lua sends Base(0.08) + Blue(0.4) -> Significant Blue tint
                if (b - r) > 50:
                    real_y = scan_area["top"] + y
                    real_x = scan_area["left"] + x
                    self.uplink_y = real_y
                    self.uplink_x = real_x
                    print(f"[LOCK] UPLINK ESTABLISHED: Y={real_y}, X={real_x}")
                    found = True
                    break
            if found: break
                
        if not found:
            print("[CRITICAL] NO SIGNAL DETECTED. CHECK GAME ADDON.")
            sys.exit(1)

    def scan(self):
        capture_area = {
            "top": self.uplink_y,
            "left": self.uplink_x,
            "width": 32 * self.scale,
            "height": 1
        }
        
        img = np.array(self.sct.grab(capture_area))
        pixels = img[0, ::self.scale]
        
        try:
            # [1] SPEC HASH (ClassID * 10 + SpecID)
            self.state['spec_hash'] = self.decode_differential(pixels[1][2], pixels[1][1], pixels[1][0])
            
            # [2] COMBAT STATUS (0 or 255)
            self.state['combat'] = self.decode_differential(pixels[2][2], pixels[2][1], pixels[2][0]) > 128

            # [3] PLAYER HEALTH % (0-100)
            self.state['player_hp'] = (self.decode_differential(pixels[3][2], pixels[3][1], pixels[3][0]) / 255.0) * 100
            
            # [4] TARGET HEALTH % (0-100)
            self.state['target_hp'] = (self.decode_differential(pixels[4][2], pixels[4][1], pixels[4][0]) / 255.0) * 100

            # [5] TARGET VALID (0 or 255)
            self.state['target_valid'] = self.decode_differential(pixels[5][2], pixels[5][1], pixels[5][0]) > 128

            # [7] PRIMARY RESOURCE % (0-100)
            self.state['resource'] = (self.decode_differential(pixels[7][2], pixels[7][1], pixels[7][0]) / 255.0) * 100
            
            # [8] SECONDARY RESOURCE (Combo Points, Holy Power, etc)
            # Lua multiplies by 25 before sending. We divide by 25 to recover integer.
            sec_val = self.decode_differential(pixels[8][2], pixels[8][1], pixels[8][0])
            self.state['secondary'] = int(round(sec_val / 25.0))
            
            # [16] DEBUFF MASK (Bitmask integer)
            # Lua sends raw value * 10. We divide by 10.
            mask_val = self.decode_differential(pixels[16][2], pixels[16][1], pixels[16][0])
            self.state['debuff_mask'] = int(round(mask_val / 10.0))

            # [22] PET HEALTH % (0-100)
            self.state['pet_hp'] = (self.decode_differential(pixels[22][2], pixels[22][1], pixels[22][0]) / 255.0) * 100

            # [30] SNAPSHOT / BUFFS (Binary)
            self.state['snapshot'] = self.decode_differential(pixels[30][2], pixels[30][1], pixels[30][0]) > 128
            
        except IndexError:
            pass # Screen tearing or resize
        
        return self.state

def main():
    vision = VisionSystem()
    vision.calibrate() 
    
    print("[SYSTEM] OPTICAL STREAM ACTIVE")
    
    while True:
        data = vision.scan()
        
        # Display Diagnostics
        hash_val = int(round(data.get('spec_hash', 0)))
        spec = SPEC_DB.get(hash_val, "Waiting...")
        
        combat = "COMBAT" if data.get('combat') else "IDLE"
        php = int(data.get('player_hp', 0))
        thp = int(data.get('target_hp', 0))
        res = int(data.get('resource', 0))
        sec = data.get('secondary', 0)
        
        sys.stdout.write(f"\r[{combat}] {spec} | HP: {php}% | T_HP: {thp}% | Res: {res}% | Sec: {sec}   ")
        sys.stdout.flush()
        
        time.sleep(0.01)

if __name__ == "__main__":
    main()
