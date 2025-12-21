import mss
import numpy as np

def wide_scan():
    print("--- WIDE SCAN INITIATED ---")
    print("Searching entire left edge for Handshake (Red 173)...")
    
    with mss.mss() as sct:
        # Get full monitor dimensions
        monitor_info = sct.monitors[1] # Primary Monitor
        width = monitor_info['width']
        height = monitor_info['height']
        
        print(f"Screen Dimensions: {width}x{height}")
        
        # Capture the entire left column (Width: 2px)
        # We start from Top=0 to Bottom=Height
        region = {"top": 0, "left": 0, "width": 5, "height": height}
        
        img_shot = sct.grab(region)
        img = np.array(img_shot)
        
        found_count = 0
        
        # Iterate every row
        for y, row in enumerate(img):
            # Check the first pixel (x=0) and second pixel (x=1)
            # Img is [B, G, R, A]
            p0 = row[0]
            
            # Check Red Channel (Index 2)
            if abs(p0[2] - 173) < 5:
                print(f"[MATCH] Found Red~173 at Y={y} (Color: {p0})")
                found_count += 1
                
        if found_count == 0:
            print("[FAIL] No Red 173 pixels found in the entire leftmost column.")
            print("Troubleshooting:")
            print("1. Is the Addon Loaded? (/reload)")
            print("2. Is the Addon anchored to BOTTOMLEFT?")
            print("3. Is the WoW window covering the bottom-left corner?")
            print("4. Is f.lux or Night Shift altering colors?")
        else:
            print(f"--- SCAN COMPLETE: Found {found_count} matches ---")
            print("Use the 'Y' value from the [MATCH] lines above to configure your engine.")

if __name__ == "__main__":
    wide_scan()
