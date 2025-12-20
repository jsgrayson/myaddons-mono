import json
import time
import os
import sys

# Try imports, handle missing dependencies gracefully
try:
    from pynput import mouse, keyboard
except ImportError:
    print("Error: 'pynput' is required. Install with: pip install pynput")
    sys.exit(1)

class HorizonScanner:
    def __init__(self):
        self.clicks = []
        self.confirmed = False
        self.config_path = "brain/data/config/ground_truth.json"

    def on_click(self, x, y, button, pressed):
        if not pressed: return
        if button == mouse.Button.right: return # Ignore right clicks
        
        self.clicks.append((x, y))
        print(f" [Captured Point: {x}, {y}]")
        
        if len(self.clicks) == 1:
            print(" -> Point 1 (FEET) set. Now click on the ground at MAX LEAP RANGE (40 yds).")
        elif len(self.clicks) == 2:
            print(" -> Point 2 (MAX RANGE) set.")
            return False # Stop listener

    def save_calibration(self):
        if len(self.clicks) < 2:
            print("Calibration failed: Not enough points.")
            return

        feet_x, feet_y = self.clicks[0]
        max_x, max_y = self.clicks[1]
        
        # Calculate Slope (Pixels per Yard)
        # Assuming Max Range = 40 yards
        pixel_distance = feet_y - max_y # Y decreases as we go up
        if pixel_distance <= 0:
            print("Error: Max range cannot be 'below' feet on screen (Y must decrease).")
            return

        pixels_per_yard = pixel_distance / 40.0
        horizon_y = max_y - (20 * pixels_per_yard) # Approximate "Infinite" horizon 20y further? 
        # Actually, linear projection: Y = m*d + c. 
        # Feet (d=0) = feet_y. 
        # Max (d=40) = max_y.
        # feet_y = c
        # max_y = 40*m + c -> m = (max_y - feet_y) / 40
        slope = (max_y - feet_y) / 40.0 # This will be negative
        
        data = {
            "feet_y": feet_y,
            "max_range_y": max_y,
            "slope": slope, 
            "pixels_per_yard": abs(slope),
            "horizon_y": int(feet_y + (slope * 100)) # 100 yards away
        }
        
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=4)
            
        print("\n [CALIBRATION SAVED]")
        print(f" Slope: {slope:.4f} pixels/yard")
        print(f" Ground Truth Configuration written to: {self.config_path}")

    def run(self):
        print("=== HORIZON SCANNER PRO ===")
        print("This tool maps your screen's perspective for 'Perfect' ground targeting.")
        print("\nINSTRUCTIONS:")
        print("1. Log into WoW. Go to a flat surface.")
        print("2. Stand still.")
        print("3. CLICK 1: At your character's FEET.")
        print("4. CLICK 2: At the furthest point you can Heroic Leap (40 yards).")
        print("\nWaiting for clicks... (Press ESC to cancel)")
        
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
            
        self.save_calibration()

if __name__ == "__main__":
    scanner = HorizonScanner()
    scanner.run()
