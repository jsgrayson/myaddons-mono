import mss
import numpy as np
import time
import random

class ScreenScanner:
    def __init__(self):
        self.sct = mss.mss()
        self.SCALE = 2.0  # Retina Display (Use 1.0 for standard 1080p)
        self.BASE_Y = 0   # Will be found by calibrate()
        self.found_y = None
        
        # CHANGED: Now looks for PURE WHITE (255,255,255) at Index 0
        self.handshake_color = 255 
        self.tolerance = 10
        
        # Target nameplate detection (red/orange hostile bar)
        self.target_bar_min = (200, 50, 50)   # Min RGB for hostile bar
        self.target_bar_max = (255, 120, 80)  # Max RGB for hostile bar
        
        # Screen dimensions (will be set on first capture)
        self.screen_width = 1920
        self.screen_height = 1080

    def calibrate(self):
        """Finds the Data Strip Y-coordinate."""
        print("[VISION] Scanning for Data Strip (White Pixel at Index 0)...")
        with mss.mss() as sct:
            # Update screen dimensions
            self.screen_width = sct.monitors[1]['width']
            self.screen_height = sct.monitors[1]['height']
            
            # Scan bottom 100 pixels
            scan_h = 100
            scan_top = self.screen_height - scan_h
            
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

    def get_target_position(self, target_range: int = 10):
        """
        Detects target nameplate (hostile red health bar) and returns screen coordinates.
        Returns: (x, y) tuple of target feet position, or None if not found.
        
        Args:
            target_range: Distance to target in yards. Used to calculate feet offset.
                         Closer = larger offset, Farther = smaller offset
        """
        with mss.mss() as sct:
            # Search area: center of screen, upper half (where nameplates show)
            # Typical WoW nameplate is in top 40% of screen, center 60% width
            search_left = int(self.screen_width * 0.2)
            search_width = int(self.screen_width * 0.6)
            search_top = int(self.screen_height * 0.1)
            search_height = int(self.screen_height * 0.35)
            
            monitor = {
                "top": search_top,
                "left": search_left,
                "width": search_width,
                "height": search_height
            }
            
            img = np.array(sct.grab(monitor))
            
            # Extract BGR channels (img is BGRA format)
            r_channel = img[:, :, 2]
            g_channel = img[:, :, 1]
            b_channel = img[:, :, 0]
            
            # Mask 1: Hostile Red (High red, low green, low blue)
            red_mask = (r_channel > 180) & (g_channel < 100) & (b_channel < 100)
            
            # Mask 2: Neutral/Grey Dummy (R, G, B channels are close to each other and mid-bright)
            # Dummies often have grey bars ~ (120, 120, 120) or similar
            grey_diff_rg = np.abs(r_channel.astype(int) - g_channel.astype(int))
            grey_diff_rb = np.abs(r_channel.astype(int) - b_channel.astype(int))
            grey_mask = (r_channel > 80) & (grey_diff_rg < 15) & (grey_diff_rb < 15)
            
            # Combine masks
            target_mask = red_mask | grey_mask
            
            # Find coordinates of target pixels
            target_coords = np.where(target_mask)
            
            if len(target_coords[0]) == 0:
                return None
            
            # Find the red pixel closest to the screen center (the absolute center of the capture area)
            # Search area center in local coords
            search_center_y = img.shape[0] // 2
            search_center_x = img.shape[1] // 2
            
            # Calculate distances to center for all target pixels
            dists = (target_coords[0] - search_center_y)**2 + (target_coords[1] - search_center_x)**2
            best_idx = np.argmin(dists)
            
            # Seed point for the best cluster
            seed_y = target_coords[0][best_idx]
            seed_x = target_coords[1][best_idx]
            
            # Find all target pixels within a small radius (e.g. 80px width of a nameplate)
            # This isolates the specific nameplate we're targeting
            cluster_mask = (abs(target_coords[0] - seed_y) < 20) & (abs(target_coords[1] - seed_x) < 60)
            
            cluster_y = target_coords[0][cluster_mask]
            cluster_x = target_coords[1][cluster_mask]
            
            # Centroid of the specific nameplate (Physical Pixels)
            center_y = int(np.mean(cluster_y))
            center_x = int(np.mean(cluster_x))
            
            # RETINA CONVERSION: Convert physical centroid to logical offset
            # img.shape is physical (e.g. 2160x3840), monitor is logical (e.g. 1080x1920)
            logical_center_x = center_x / self.SCALE
            logical_center_y = center_y / self.SCALE

            # Convert to absolute logical screen coordinates
            abs_x = search_left + logical_center_x
            abs_y = search_top + logical_center_y
            
            # === HUMANIZATION JITTER ===
            # Add a small random offset so we don't click the exact same pixel every time
            abs_x += random.uniform(-15.0, 15.0)
            abs_y += random.uniform(-10.0, 10.0)
            
            # === RANGE-BASED FEET OFFSET ===
            # Feet offset should also be logical points
            clamped_range = max(5, min(40, target_range))
            feet_offset = int(350 - (clamped_range * 7.5)) / self.SCALE # Scale this too
            feet_offset = max(25, min(175, feet_offset))  # Adjusted logical clamp
            
            feet_y = abs_y + feet_offset
            
            print(f"[VISION] Locked Nameplate Logical: ({abs_x:.0f}, {feet_y:.0f}) | Physical: ({center_x}, {center_y}) | range={target_range}yd")
            return (abs_x, feet_y)
    
    def get_flick_offset(self, target_range: int = 10):
        """
        Returns (dx, dy) offset from screen center to target position.
        Uses target_range to calculate dynamic feet offset.
        
        Args:
            target_range: Distance to target in yards (from addon pixel data)
        """
        target_pos = self.get_target_position(target_range)
        if not target_pos:
            return None
        
        # Use Logical screen dimensions for center
        center_x = self.screen_width / 2
        center_y = self.screen_height / 2
        
        dx = target_pos[0] - center_x
        dy = target_pos[1] - center_y
        
        return (dx, dy)

