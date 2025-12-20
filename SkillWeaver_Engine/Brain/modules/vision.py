import mss
import numpy as np
import cv2

class ScreenScanner:
    def __init__(self):
        self.sct = mss.mss()
        # Monitor 1, top-left 16x1 pixel row where Chameleon.lua renders
        self.monitor = {"top": 0, "left": 0, "width": 16, "height": 1}
        
        # Ghost Calibration Defaults
        self.target_red = 173  # Default for your Mac
        self.tolerance = 15

    def calibrate(self):
        """Run this once at startup while WoW is focused."""
        with mss.mss() as sct:
            # Grab the first pixel at Y=32
            # We use 1x1 just to sample the baseline color
            img = np.array(sct.grab({"top": 32, "left": 0, "width": 1, "height": 1}))
            # Update our target based on current screen tint
            # We take the max of Ch0 and Ch2 to handle BGRA/RGB ambiguity and Night Shift
            self.target_red = max(img[0,0,0], img[0,0,2])
            print(f"[CALIBRATED] New Spec ID Baseline: {self.target_red}")

    def get_spec_id(self, frame_row):
        # frame_row is the full pixel array [Physical Width]
        pixel = frame_row[0]
        current_red = max(pixel[0], pixel[2])
        # Compare current pixel to our calibrated baseline
        if abs(int(current_red) - self.target_red) <= self.tolerance:
            return 189000
        return 0

    def get_chameleon_pixels(self):
        with mss.mss() as sct:
            # Fixed at Y=32 based on your success scan
            # Width 80 to cover 40 logical pixels on Retina
            monitor = {"top": 32, "left": 0, "width": 80, "height": 1}
            img = np.array(sct.grab(monitor))
            # This returns the raw array for the logic engine
            return img

    def detect_enemy_cast(self):
        # Scan sub-region for enemy cast bar (defined in VISUAL_ANCHORS.md)
        cast_region = {"top": 400, "left": 800, "width": 200, "height": 20}
        img = np.array(self.sct.grab(cast_region))
        # Logic to detect "Yellow/Gold" cast bar fill
        return np.mean(img[:, :, 1]) > 180 

    def get_feet_coordinates(self, nameplate_rect, screen_height):
        """
        Calculates the 'Ground-Plane Projection' for aiming.
        Solves 'Nameplate Stacking' overshoot by ignoring Nameplate Y.
        """
        if not nameplate_rect:
            return None
            
        x, y, w, h = nameplate_rect
        center_x = x + (w // 2)

        # GROUND TRUTH ALGORITHM
        # 1. Use Nameplate Width (w) as proxy for Distance (Scale).
        #    Wide = Close, Narrow = Far.
        # 2. Map 'Distance' to a fixed Screen Y coordinate based on Calibration.
        
        # Example Calibration Map (To be populated by GroundCalibrator.py):
        # Width 150px (Close) -> Y = 800
        # Width 100px (Mid)   -> Y = 650
        # Width 50px (Far)    -> Y = 500
        
        # Simple Linear Interpolation for now:
        # Assuming Y_Ground = Base_Horizon + (Width * Slope)
        
        # Default Params (Standard 1080p UI scale):
        horizon_y = screen_height * 0.45 # Horizon line approx
        slope = 2.5 # How much "down" the screen the feet move as target gets closer (wider)
        
        ground_truth_y = int(horizon_y + (w * slope))
        
        # Clamp to screen bottom safety
        ground_truth_y = min(ground_truth_y, screen_height - 50)
        
        return (center_x, ground_truth_y)
