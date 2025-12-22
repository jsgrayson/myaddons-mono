# SKILLWEAVER VISION ENGINE v3.1 (HIGH-GAIN)
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
        Max Diff = 0.90 * 255 = 229.5
        
        CALIBRATION:
        New Divisor = 229.5
        Adjusted for 2% signal loss cushion -> 225.0
        """
        diff = int(b) - int(r)
        # Normalize
        val = (diff / 225.0) * 255.0
        return max(0, min(255, val))

    def calibrate(self):
        print("------------------------------------------------")
        print("[BOOT] v3.1 HIGH-GAIN ENGINE STARTING...")
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
        candidates = []

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
            # Index 1: Spec Hash (Double)
            self.state['spec_hash'] = self.decode_differential(pixels[1][2], pixels[1][1], pixels[1][0])
            
            # Index 2: Combat
            self.state['combat'] = self.decode_differential(pixels[2][2], pixels[2][1], pixels[2][0]) > 128

            # Index 3: HP (Clamped to 100%)
            hp_raw = (self.decode_differential(pixels[3][2], pixels[3][1], pixels[3][0]) / 255.0) * 100
            self.state['player_hp'] = min(100.0, hp_raw)
            
            # Index 7: Resource (Clamped to 100%)
            res_raw = (self.decode_differential(pixels[7][2], pixels[7][1], pixels[7][0]) / 255.0) * 100
            self.state['resource'] = min(100.0, res_raw)
            
            # Index 8: Secondary (Standardized Scale 25)
            # Use rounding for resources to snap to integer
            sec_raw = self.decode_differential(pixels[8][2], pixels[8][1], pixels[8][0])
            self.state['secondary'] = int(round(sec_raw / 25.0))
            
            # Index 30: Snapshot
            self.state['snapshot'] = self.decode_differential(pixels[30][2], pixels[30][1], pixels[30][0]) > 128
        except:
            pass
        
        return self.state

def main():
    vision = VisionSystem()
    vision.calibrate() 
    
    while True:
        data = vision.scan()
        # Clean Output Dashboard
        combat_status = "COMBAT" if data.get('combat') else "IDLE"
        spec_hash = data.get('spec_hash', 0)
        
        # Display formatted output
        sys.stdout.write(f"\r[{combat_status}] Raw:{spec_hash:.2f} | Locked:{int(round(spec_hash))} | HP:{int(data.get('player_hp',0))}% | Res:{int(data.get('resource',0))}%   ")
        sys.stdout.flush()
        time.sleep(0.016)

if __name__ == "__main__":
    main()
