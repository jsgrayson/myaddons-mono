import mss
import numpy as np

def debug_color_profile():
    print("--- DEBUG COLOR PROFILE (BOTTOM-LEFT CHECK) ---")
    # MacBook Retina Scaling (usually 2.0)
    # The addon is at the very BOTTOM-LEFT of the WoW window
    SCALE = 2.0 
    
    # Try to auto-detect height to be helpful, otherwise default to 1080
    with mss.mss() as sct:
        monitor = sct.monitors[1] # Primary monitor
        height = monitor['height']
        width = monitor['width']
        print(f"[INFO] Monitor 1 Detected: {width}x{height}")
        
        # Override if logic height differs from physical (Retina handling varies by OS reporting)
        # If mss reports physical pixels directly (e.g. 3024x1964), then SCALE logic might differ.
        # But assuming User's logic: Logical Height 1080 -> Physical Scan at Y ~ 2160?
        # Or if MSS reports logical 1080, we scan at 1080. 
        # User said: "Logical height (e.g. 1080) ... target_y = int((SCREEN_HEIGHT - 1) * SCALE)"
        # This implies MSS grabs in physical pixels but we define coords in logical.
        
        # Let's trust the User's snippet logic for the calculation but use auto-detected height if it looks logical (approx 1000-1200), 
        # or defaults if it looks physical (approx 2000+).
        
        # Using User's hardcoded default for safety as requested, but printing detected.
        LOGICAL_HEIGHT = 1080 
        
        target_y = int((LOGICAL_HEIGHT - 1) * SCALE)
        # On some Retina setups, mss might grab using physical coordinates directly, 
        # so if monitor['height'] is ~2160, target_y should be close to that.
        
        print(f"[CONFIG] Logical Height: {LOGICAL_HEIGHT} | Scale: {SCALE} | Scan Y: {target_y}")

        # Capture 1x1 at Handshake (Index 0)
        # WoW (0,0) is Bottom-Left. MSS (0,0) is Top-Left.
        # So WoW Y=0 is MSS Y=Height-1.
        region = {"top": target_y, "left": 0, "width": 1, "height": 1}
        
        try:
            img = np.array(sct.grab(region))
            color = img[0][0] # BGRA
            blue, green, red, alpha = color[0], color[1], color[2], color[3]
            
            print(f"Index 0 Handshake at Y={target_y}: BGR {color[:3]} | Red: {red}")
            
            if abs(red - 173) < 5: # Tolerance
                print(">>> SUCCESS: ColorProfile_Lib Found!")
            else:
                print(">>> ERROR: Value mismatch. (Expected Red ~173)")
                print("    Troubleshooting: Check 'LOGICAL_HEIGHT' or 'SCALE'. The Scan Y might be off-screen or in black bar.")
                
        except Exception as e:
            print(f"[ERROR] Grab failed: {e}")

if __name__ == "__main__":
    debug_color_profile()
