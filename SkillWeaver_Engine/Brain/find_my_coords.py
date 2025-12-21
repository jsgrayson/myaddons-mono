import mss
import numpy as np

def find_handshake_row():
    print("--- SCANNING FOR HANDSHAKE (RED 173) ---")
    
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        width = monitor['width']
        height = monitor['height']
        print(f"Screen Dims (Physical): {width}x{height}")
        
        found = False
        
        # We scan the bottom 200 rows of the physical screen
        scan_y_start = height - 200
        
        # Grab the bottom strip at x=0
        # Region: Left=0, Top=height-200, Width=1, Height=200
        # This gives us a vertical column of pixels at x=0 from the bottom area
        region = {"top": scan_y_start, "left": 0, "width": 1, "height": 200}
        img = np.array(sct.grab(region))
        
        # Iterate through the column
        for i in range(200):
            pixel = img[i][0] # [B, G, R, A]
            red = pixel[2]
            
            # Check for 173 with tolerance
            if abs(red - 173) < 5:
                # Found it!
                actual_y = scan_y_start + i
                print(f">>> FOUND HANDSHAKE at Y={actual_y}")
                print(f"    Color: {pixel}")
                print(f"    Config for vision.py -> BOTTOM_Y = {actual_y}")
                found = True
                break
        
        if not found:
             print("[FAIL] Could not find Red 173 in the bottom 200 rows at x=0.")
             print("       Ensure WoW is focused, full screen, and the addon is loaded.")

if __name__ == "__main__":
    find_handshake_row()
