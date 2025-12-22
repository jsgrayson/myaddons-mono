# SKILLWEAVER VISION ENGINE v24.0 (DARK MATTER)
# PROTOCOL: LOW-OBSERVABLE STEALTH

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
        LUA: Base(0.08) + (Val/255 * 0.3)
        Max Diff = 0.3 * 255 = 76.5
        This is a HIGH GAIN decoder for dark signals.
        """
        diff = int(b) - int(r)
        # Normalize: (Diff / 76.5) * 255
        val = (diff / 76.5) * 255.0
        return max(0, min(255, val))

    def calibrate(self):
        print("------------------------------------------------")
        print("[INIT] DARK MATTER PROTOCOL ENGAGED.")
        print("[SCAN] Searching for Low-Observable Pilot Signal...")
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
                # Base is ~20. Pilot Blue is ~102.
                # Diff should be ~82.
                # Threshold: > 60
                
                diff = b - r
                
                if diff > 60:
                    real_y = scan_area["top"] + y
                    real_x = scan_area["left"] + x
                    
                    self.uplink_y = real_y
                    self.uplink_x = real_x
                    print(f"[LOCK] Stealth Uplink ACQUIRED at Y={real_y}, X={real_x}")
                    print(f"[LOCK] Signal (Dark Blue): RGB({r},{g},{b}) Diff:{diff}")
                    found = True
                    break
            if found: break
                
        if not found:
            print("[ERROR] Uplink NOT DETECTED.")
            print("[HINT] Ensure Chat Window is NOT covering bottom-left corner.")
            print("[HINT] Run WoW in Windowed Fullscreen.")
            
            output = "debug_failure.png"
            mss.tools.to_png(img.tobytes(), img.shape[:2][::-1], output=output)
            print(f"[DIAGNOSTIC] Saved {output}")
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
            self.state['player_hp'] = (self.decode_differential(pixels[3][2], pixels[3][1], pixels[3][0]) / 255.0) * 100
            self.state['resource'] = (self.decode_differential(pixels[7][2], pixels[7][1], pixels[7][0]) / 255.0) * 100
            
            sec_raw = self.decode_differential(pixels[8][2], pixels[8][1], pixels[8][0])
            self.state['secondary'] = sec_raw // 25
            
            self.state['snapshot'] = self.decode_differential(pixels[30][2], pixels[30][1], pixels[30][0]) > 128
        except:
            pass
        
        return self.state

def main():
    vision = VisionSystem()
    vision.calibrate() 
    
    while True:
        data = vision.scan()
        sys.stdout.write(f"\rHP: {data.get('player_hp',0):.1f}% | Res: {data.get('resource',0):.1f}% | Sec: {int(data.get('secondary',0))} | Snap: {data.get('snapshot',False)}")
        sys.stdout.flush()
        time.sleep(0.016)

if __name__ == "__main__":
    main()
