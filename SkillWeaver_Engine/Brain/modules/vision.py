import mss
import numpy as np
import time

class ScreenScanner:
    def __init__(self):
        self.sct = mss.mss()
        self.SCALE = 2.0  # Retina Display (Use 1.0 for standard 1080p)
        self.BASE_Y = 0   # Will be found by calibrate()
        self.found_y = None
        
        # CHANGED: Now looks for PURE WHITE (255,255,255) at Index 0
        self.handshake_color = 255 
        self.tolerance = 10

    def calibrate(self):
        """Finds the Data Strip Y-coordinate."""
        print("[VISION] Scanning for Data Strip (White Pixel at Index 0)...")
        with mss.mss() as sct:
            # Scan bottom 100 pixels
            scan_h = 100
            scan_top = sct.monitors[1]['height'] - scan_h
            
            monitor = {"top": scan_top, "left": 0, "width": 5, "height": scan_h}
            img = np.array(sct.grab(monitor))
            
            # Scan vertical column 0
            for y_offset, row in enumerate(img):
                # img is BGRA. White is (255, 255, 255)
                # Check Blue, Green, Red
                b, g, r, a = row[0]
                
                # Check if all channels are bright white (>245)
                if b > 245 and g > 245 and r > 245:
                    self.found_y = scan_top + y_offset
                    self.BASE_Y = self.found_y
                    print(f"[SUCCESS] Locked on Data Strip at Y={self.BASE_Y}")
                    return True
        print("[FAIL] Could not find Data Strip. Check ColorProfile_Lib is running.")
        return False

    def get_chameleon_pixels(self):
        """Returns the full row of data pixels."""
        if not self.found_y:
            if not self.calibrate():
                return None

        # Capture width: We need enough for 32 slots. 
        # On Retina (Scale 2.0), capturing 32*2 = 64 pixels.
        width = int(32 * self.SCALE)
        monitor = {"top": self.BASE_Y, "left": 0, "width": width, "height": 1}
        
        with mss.mss() as sct:
            img = np.array(sct.grab(monitor))
            row_raw = img[0] # The single row
            
            # RETINA FIX: Steps by 2 to account for macOS double-pixel rendering.
            # Normal screens use stride=1. Retina uses stride=2.
            pixel_stride = 2 if self.SCALE > 1.5 else 1
            
            pixels = []
            
            # We loop up to 32 times (or row length)
            # This logic matches the user's request: i * stride
            for i in range(32):
                target_index = i * pixel_stride
                
                if target_index < len(row_raw):
                    # Convert BGRA -> RGB
                    b, g, r, a = row_raw[target_index]
                    pixels.append((r, g, b))
                else:
                    pixels.append((0,0,0))
            
            return [pixels] # Return as a matrix (list of lists)

    def get_spec_id(self, pixel_row):
        """Decodes Pixel 1 (Red Channel) into Spec ID."""
        # Lua sends s/1000. 
        # Value 0-255 represents 0.0-1.0.
        # Example: 259 (Assa) -> 0.259 -> Red ~66
        r = pixel_row[1][0] # Index 1, Red
        
        # Reverse math: (Red / 255) * 1000
        spec = int((r / 255.0) * 1000)
        
        # Jitter correction (Assassination 259 might read 258 or 260)
        if 250 <= spec <= 270: return 259 # Snap to Assa for now
        
        return spec
