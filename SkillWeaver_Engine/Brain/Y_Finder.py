import mss
import numpy as np

# --- Y-FINDER (v25.4) ---
# Scans the bottom 100 pixels to find the SW_Frame Pilot signal.

def find_y():
    with mss.mss() as sct:
        # Physical screen height is ~1117 (Retina 16" MBP)
        # We scan from 1000 to the bottom
        print(">> SCANNING FOR OPTICAL BAR...")
        found = False
        for y_check in range(1000, 1117):
            snap = np.array(sct.grab({"top": y_check, "left": 0, "width": 1, "height": 1}))
            pixel = snap[0][0]
            
            # Blue - Red differential check for Pilot (0.4 Blue - 0.08 Red ~ 78-82 diff)
            diff = int(pixel[0]) - int(pixel[2])
            
            if diff > 50:
                print(f"✅ FOUND PIXELS AT Y_ROW: {y_check} (Diff: {diff})")
                found = True
        
        if not found:
            print("❌ NO SIGNAL DETECTED. Check if SW_Frame is alive in-game.")

if __name__ == "__main__":
    find_y()
