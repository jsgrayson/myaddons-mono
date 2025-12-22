# SKILLWEAVER LOGIC ENGINE v3.2 (SELF-HEALING)
# PROTOCOL: DARK MATTER (GAIN 0.90)

import mss
import mss.tools
import numpy as np
import time
import json
import sys
import os

# --- CONFIGURATION ---
RETINA_SCALE = 2 # 2 for Mac, 1 for Windows
# ---------------------

# --- SPEC DATABASE (Must match Lua) ---
SPEC_DB = {
    41: "Rogue - Assassination",
    42: "Rogue - Outlaw",
    43: "Rogue - Subtlety",
    93: "Warlock - Destruction",
    91: "Warlock - Affliction",
    31: "Hunter - BeastMastery",
    121: "DH - Havoc",
    112: "Druid - Feral",
    11: "Warrior - Arms"
}

class RotationManager:
    def __init__(self):
        self.current_hash = 0
        self.rotation_data = None
        self.last_load_attempt = 0

    def ensure_rotation_file(self, hash_id):
        """Creates a default rotation file if one does not exist."""
        filename = f"rotation_{hash_id}.json"
        if not os.path.exists(filename):
            print(f"[AUTO-GENESIS] Creating missing rotation file: {filename}")
            
            spec_name = SPEC_DB.get(hash_id, "Unknown")
            
            # Default Template
            default_data = {
                "meta": {
                    "version": "1.0",
                    "spec_id": hash_id,
                    "spec_name": spec_name
                },
                "rotation": [
                    {
                        "spell": "Auto Attack",
                        "key": "1",
                        "conditions": { "combat": True }
                    }
                ]
            }
            
            try:
                with open(filename, 'w') as f:
                    json.dump(default_data, f, indent=4)
                print("[SUCCESS] File created. Please edit logic.")
            except Exception as e:
                print(f"[ERROR] Could not create file: {e}")

        return filename

    def load_rotation(self, hash_id):
        if hash_id == self.current_hash:
            return
        
        # Debounce
        if time.time() - self.last_load_attempt < 2:
            return

        self.last_load_attempt = time.time()
        print(f"[SYSTEM] Detected New Spec Hash: {hash_id}")
        
        filename = self.ensure_rotation_file(hash_id)
        
        try:
            with open(filename, 'r') as f:
                self.rotation_data = json.load(f)
            self.current_hash = hash_id
            print(f"[SYSTEM] Rotation Loaded: {filename}")
        except Exception as e:
            print(f"[ERROR] JSON Load Failed: {e}")

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
        LUA: Base(0.08) + (Val/255 * 0.90)
        
        CALIBRATION FIX:
        Previous Divisor: 225.0 -> Resulted in 98% (0.98)
        New Divisor: 215.0 -> Resulted in 102% clamped to 100%
        """
        diff = int(b) - int(r)
        # Normalize with lower divisor to boost signal
        val = (diff / 215.0) * 255.0
        return max(0, min(255, val))

    def calibrate(self):
        print("------------------------------------------------")
        print("[BOOT] v3.2 LOGIC ENGINE STARTING...")
        print("[INIT] DARK MATTER PROTOCOL ENGAGED.")
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
        
        for y in range(scan_height - 1, 0, -1):
            for x in range(0, 10): 
                px = img[y, x]
                b, g, r = int(px[0]), int(px[1]), int(px[2])
                
                # Check for Dark Blue Pilot
                diff = b - r
                if diff > 60:
                    real_y = scan_area["top"] + y
                    real_x = scan_area["left"] + x
                    self.uplink_y = real_y
                    self.uplink_x = real_x
                    print(f"[LOCK] Stealth Uplink ACQUIRED at Y={real_y}, X={real_x}")
                    found = True
                    break
            if found: break
                
        if not found:
            print("[ERROR] Uplink NOT DETECTED.")
            sys.exit(1)
            
        print("[SUCCESS] Sensor Calibrated.")

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
            # Decode
            # Index 1: Spec Hash
            self.state['spec_hash'] = self.decode_differential(pixels[1][2], pixels[1][1], pixels[1][0])
            
            # Index 2: Combat
            self.state['combat'] = self.decode_differential(pixels[2][2], pixels[2][1], pixels[2][0]) > 128

            # Index 3: HP (Clamped to 100%)
            hp_raw = (self.decode_differential(pixels[3][2], pixels[3][1], pixels[3][0]) / 255.0) * 100
            self.state['player_hp'] = min(100.0, hp_raw)
            
            # Index 7: Resource (Clamped to 100%)
            res_raw = (self.decode_differential(pixels[7][2], pixels[7][1], pixels[7][0]) / 255.0) * 100
            self.state['resource'] = min(100.0, res_raw)
            
            # Index 8: Secondary
            sec_raw = self.decode_differential(pixels[8][2], pixels[8][1], pixels[8][0])
            self.state['secondary'] = int(round(sec_raw / 25.0))
            
            # Index 30: Snapshot
            self.state['snapshot'] = self.decode_differential(pixels[30][2], pixels[30][1], pixels[30][0]) > 128
        except:
            pass
        
        return self.state

def main():
    vision = VisionSystem()
    rot_mgr = RotationManager()
    vision.calibrate() 
    
    while True:
        data = vision.scan()
        
        # Process Hash
        raw_hash = data.get('spec_hash', 0)
        locked_hash = int(round(raw_hash))
        
        # Lookup Name
        spec_name = SPEC_DB.get(locked_hash, "UNKNOWN")
        
        # Load Rotation Logic if valid hash
        if locked_hash > 0:
            rot_mgr.load_rotation(locked_hash)
        
        # Clean Output Dashboard
        combat_status = "COMBAT" if data.get('combat') else "IDLE"
        
        sys.stdout.write(f"\r[{combat_status}] SPEC:{spec_name} ({locked_hash}) | HP:{int(data.get('player_hp',0))}% | Res:{int(data.get('resource',0))}%   ")
        sys.stdout.flush()
        time.sleep(0.016)

if __name__ == "__main__":
    main()
