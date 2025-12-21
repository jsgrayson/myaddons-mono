import sys
import time
import numpy as np
import mss
from PIL import ImageGrab

# --- CONFIGURATION ---
SCAN_RANGE = 20 # How many pixels up/down to check around the expected row

def luminance_scout():
    """
    Uses PIL (The Sniper) to find the exact physical row of the pixels.
    """
    print("Scouting with PIL (Luminance Protocol)...")
    # Grab the full retina buffer
    screen = ImageGrab.grab(all_screens=True).convert('L') 
    data = np.array(screen)
    height = data.shape[0]
    
    # Scan the bottom 50 pixels (Physical coordinates)
    for y in range(height - 1, height - 50, -1):
        # Check X=0 for the White Handshake (Luminance > 200)
        if data[y][0] > 200:
            print(f"[LOCKED] Anchor found at Physical Y:{y}")
            return y
    return None

def main():
    # 1. THE SCOUT PHASE (PIL)
    # We use PIL to find the Y-coord because we know it works for you.
    locked_y = luminance_scout()
    
    if not locked_y:
        print("[FAIL] Could not find White Pixel anchor.")
        return

    # 2. THE DRIVER PHASE (MSS)
    # Now we switch to the fast library
    with mss.mss() as sct:
        # Get the primary monitor
        monitor = sct.monitors[1] 
        
        # RETINA MATH CHECK
        # PIL sees physical (e.g., 2234), MSS might see logical (1117)
        # We need to determine the scale factor to tell MSS where to look.
        scale_factor = locked_y / monitor["height"]
        
        # If scale is ~2.0, we are on Retina.
        # MSS usually grabs the LOGICAL area but returns PHYSICAL pixels.
        # We define a tiny capture box exactly where PIL found the pixels.
        
        bbox = {
            # Default to raw Y
            "top": locked_y, 
            "left": 0, 
            "width": 10, 
            "height": 1
        }
        
        print(f"[HYBRID] Switching to MSS High-Speed Loop...")
        print(f"[DEBUG] MSS Monitor Height: {monitor['height']} | PIL Y: {locked_y}")
        
        # If PIL Y is ~2x MSS Height, we divide Y by 2 for the MSS coordinate system
        if scale_factor > 1.5:
            print("[INFO] Retina Scale Detected (2x). Adjusting MSS coordinates.")
            bbox["top"] = int(locked_y / 2)

        print(f"[LOCKED] MSS Capture Region: {bbox}")

        # 3. THE COMBAT LOOP
        print(">> ENGINE ACTIVE. LISTENING FOR COMBAT DATA.")
        try:
            while True:
                # Capture just the tiny 10x1 strip
                sct_img = sct.grab(bbox)
                img = np.array(sct_img)
                
                # MSS returns BGRA. We need indices 1, 6, 8.
                # Note: Because of Retina scaling, 1 logical pixel might = 2 physical pixels.
                # If we asked for width 10, we might get 20 pixels back on Retina.
                
                # Handshake check (White Pixel at Index 0)
                # We check the Blue channel (index 0 in BGRA) for high value
                # Assuming index 0 pixel is still index 0 in the array
                if img[0][0][0] > 180: # Lowered threshold slightly for MSS noise
                    # Index 1: Spec (Red Channel is index 2 in BGRA)
                    # We map 1 logical pixel step to likely physical index 
                    # If Retina: Logical 0 -> Physical 0, Logical 1 -> Physical 2?
                    # Let's try direct mapping first, but verify indexes.
                    
                    spec_px = img[0][1] # B, G, R, A
                    nrg_px = img[0][6]
                    cp_px = img[0][8]
                    
                    # Spec is Red (Index 2), Resources are Green (Index 1)
                    spec_val = int((spec_px[2] / 255) * 1000)
                    energy = nrg_px[1]
                    cp = cp_px[1]
                    
                    # Print data stream for verification
                    sys.stdout.write(f"\r Spec:{spec_val} | NRG:{energy} | CP:{cp}   ")
                    sys.stdout.flush()
                    
                    # --- ROTATION LOGIC START ---
                    if spec_val == 259: # Assassination
                        # Example: Mutilate at < 5 CP
                        if cp < 5:
                            # Firing logic here
                            pass
                    # --- ROTATION LOGIC END ---
                    
                time.sleep(0.01) # ~100 FPS
                
        except KeyboardInterrupt:
            print("\n[STOP] Engine halted.")

if __name__ == "__main__":
    main()
