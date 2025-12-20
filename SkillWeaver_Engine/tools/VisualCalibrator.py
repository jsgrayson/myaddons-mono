import json
import os
import sys

try:
    from pynput import mouse, keyboard
except ImportError:
    print("Error: 'pynput' is required. Install with: pip install pynput")
    sys.exit(1)

class VisualCalibrator:
    def __init__(self):
        self.anchors = {}
        self.current_step = 0
        self.steps = [
            ("player_health_start", "Click the LEFT edge of your Health Bar."),
            ("player_health_end", "Click the RIGHT edge of your Health Bar."),
            ("player_resource_center", "Click the CENTER of your Primary Resource Bar (Rage/Energy/Mana)."),
            ("target_health_start", "Click the LEFT edge of the Target Health Bar."),
            ("target_health_end", "Click the RIGHT edge of the Target Health Bar."),
            ("target_cast_bar", "Click the CENTER of the Target Cast Bar."),
            ("focus_cast_bar", "Click the CENTER of the Focus Cast Bar."),
            ("chameleon_start", "Click the FIRST pixel (Green) of the Chameleon Strip."),
            ("chameleon_end", "Click the LAST pixel (Red) of the Chameleon Strip.")
        ]
        self.config_path = "brain/data/config/visual_anchors.json"

    def on_click(self, x, y, button, pressed):
        if not pressed: return
        if button == mouse.Button.right: return 
        
        key, prompt = self.steps[self.current_step]
        print(f" [CAPTURED] {key}: ({x}, {y})")
        self.anchors[key] = {"x": x, "y": y}
        
        self.current_step += 1
        if self.current_step >= len(self.steps):
            return False # Stop listener
        
        # Print next prompt
        next_key, next_prompt = self.steps[self.current_step]
        print(f"\nSTEP {self.current_step + 1}/{len(self.steps)}: {next_prompt}")

    def save_calibration(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.anchors, f, indent=4)
            
        print("\n [CALIBRATION SAVED]")
        print(f" Visual Anchors written to: {self.config_path}")

    def run(self):
        print("=== VISUAL AURA CALIBRATOR ===")
        print("This tool maps your UI elements for the Vision Engine.")
        print("\nINSTRUCTIONS:")
        print("1. Log into WoW.")
        print("2. Ensure your UI is in position.")
        print(f"\nSTEP 1/{len(self.steps)}: {self.steps[0][1]}")
        
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
            
        self.save_calibration()

if __name__ == "__main__":
    calibrator = VisualCalibrator()
    calibrator.run()
