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
        self.logical_width = 960  # Assuming Retina
        self.logical_height = 540

    def calibrate(self):
        """Finds the Data Strip Y-coordinate."""
        print("[VISION] Scanning for Data Strip (White Pixel at Index 0)...")
        with mss.mss() as sct:
            # Store PHYSICAL dimensions for mss.grab() 
            self.screen_width = sct.monitors[1]['width']
            self.screen_height = sct.monitors[1]['height']
            
            # Get ACTUAL logical dimensions from Quartz (the point coordinate system)
            import Quartz
            main_display = Quartz.CGMainDisplayID()
            display_bounds = Quartz.CGDisplayBounds(main_display)
            self.logical_width = display_bounds.size.width
            self.logical_height = display_bounds.size.height
            
            # Calculate actual scale factor
            self.SCALE = self.screen_width / self.logical_width
            print(f"[VISION] Screen: {self.screen_width}x{self.screen_height} physical, {self.logical_width:.0f}x{self.logical_height:.0f} logical, scale={self.SCALE:.2f}")
            
            # Scan bottom 100 pixels (physical)
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
        # Ensure screen dimensions are calibrated
        if not self.found_y:
            self.calibrate()
        
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
            
            # === SIMPLE CLUSTER DETECTION (no scipy) ===
            # Find distinct horizontal bands of red pixels (nameplates are horizontal bars)
            # Group by Y position with tolerance
            
            target_ys = target_coords[0]
            target_xs = target_coords[1]
            
            # Find unique Y bands (nameplates are ~10-20px tall)
            unique_bands = []
            sorted_ys = np.sort(np.unique(target_ys))
            
            current_band_start = sorted_ys[0] if len(sorted_ys) > 0 else 0
            for y in sorted_ys:
                if y - current_band_start > 25:  # New band if gap > 25px
                    unique_bands.append(current_band_start)
                    current_band_start = y
            unique_bands.append(current_band_start)
            
            # For each band, find the centroid and check for glow
            best_glow_score = 0
            best_center = None
            search_center_y = img.shape[0] // 2
            search_center_x = img.shape[1] // 2
            closest_dist = float('inf')
            fallback_center = None
            
            for band_y in unique_bands:
                # Get all pixels in this Y band (±15px)
                band_mask = (target_ys >= band_y - 15) & (target_ys <= band_y + 25)
                band_xs = target_xs[band_mask]
                band_ys = target_ys[band_mask]
                
                if len(band_xs) < 10:  # Skip tiny clusters
                    continue
                
                # Centroid of this nameplate
                center_x = int(np.mean(band_xs))
                center_y = int(np.mean(band_ys))
                
                # Check for glow around this nameplate
                glow_margin = 15
                glow_min_y = max(0, center_y - glow_margin - 10)
                glow_max_y = min(img.shape[0], center_y + glow_margin + 10)
                glow_min_x = max(0, center_x - 80)  # Nameplates are wide
                glow_max_x = min(img.shape[1], center_x + 80)
                
                glow_region = img[glow_min_y:glow_max_y, glow_min_x:glow_max_x]
                
                # Glow is bright (R+G+B > 650) - target indicator is white/yellow
                if glow_region.size > 0:
                    brightness = glow_region[:,:,0].astype(int) + glow_region[:,:,1].astype(int) + glow_region[:,:,2].astype(int)
                    glow_pixels = np.sum(brightness > 650)
                else:
                    glow_pixels = 0
                
                # Track best glow score
                if glow_pixels > best_glow_score:
                    best_glow_score = glow_pixels
                    best_center = (center_x, center_y)
                
                # Track closest to center as fallback
                dist = (center_y - search_center_y)**2 + (center_x - search_center_x)**2
                if dist < closest_dist:
                    closest_dist = dist
                    fallback_center = (center_x, center_y)
            
            # Use glow-detected if significant, otherwise center-nearest
            if best_glow_score > 100 and best_center:
                center_x, center_y = best_center
            elif fallback_center:
                center_x, center_y = fallback_center
            else:
                # Last resort: overall centroid
                center_x = int(np.mean(target_xs))
                center_y = int(np.mean(target_ys))
            
            # RETINA CONVERSION: Convert everything to logical coordinates
            # search_left/top are physical, so convert them too
            logical_search_left = search_left / self.SCALE
            logical_search_top = search_top / self.SCALE
            logical_center_x = center_x / self.SCALE
            logical_center_y = center_y / self.SCALE

            # Convert to absolute logical screen coordinates
            abs_x = logical_search_left + logical_center_x
            abs_y = logical_search_top + logical_center_y
            
            # === HUMANIZATION JITTER ===
            # Add a small random offset so we don't click the exact same pixel every time
            # Wider jitter for anti-detection (worth the occasional miss)
            abs_x += random.uniform(-5.0, 5.0)
            abs_y += random.uniform(-3.0, 3.0)
            
            # === DYNAMIC FEET OFFSET CALCULATION ===
            # The offset from nameplate to feet depends on camera angle and distance:
            # - Nameplate HIGH on screen (small Y, close target) = BIG offset needed
            # - Nameplate LOW on screen (large Y, far target) = SMALL offset needed
            #
            # Screen center is roughly where camera points. Targets above center are close,
            # targets below center are far.
            screen_center_y = self.logical_height / 2
            
            # How far above/below center is the nameplate?
            # Negative = above center (close), Positive = below center (far)
            relative_y = abs_y - screen_center_y
            
            # Base offset for nameplate at center
            BASE_OFFSET = 60
            
            # Scale factor: each 100px above center adds 30px offset
            # Each 100px below center subtracts 20px offset
            if relative_y < 0:  # Close target (above center)
                feet_offset = BASE_OFFSET + abs(relative_y) * 0.3
            else:  # Far target (below center)
                feet_offset = BASE_OFFSET - relative_y * 0.2
            
            # Clamp to reasonable range
            feet_offset = max(30, min(120, feet_offset))
            
            feet_y = abs_y + feet_offset  # ADD to aim DOWN
            
            print(f"[VISION] Locked Nameplate Logical: ({abs_x:.0f}, {abs_y:.0f}) | FeetOffset: {feet_offset:.0f}px | feet_y={feet_y:.0f} | center=({self.logical_width/2:.0f},{self.logical_height/2:.0f})")
            return (abs_x, feet_y)
    
    def get_flick_offset(self, target_range: int = 10):
        """
        Returns absolute (x, y) target position for ground-targeted spells.
        Uses Quartz warp now, so we just return the target position.
        
        Args:
            target_range: Distance to target in yards (from addon pixel data)
        """
        target_pos = self.get_target_position(target_range)
        if not target_pos:
            return None
        
        print(f"[VISION] Target at ({target_pos[0]:.0f}, {target_pos[1]:.0f})")
        
        return target_pos  # Return absolute position, not offset

