import json
import time
import os
from modules.vision import ScreenScanner
from modules.serial_link import SerialLink as ArduinoBridge 

# MAPPING: "JSON Key" -> "Arduino Byte"
# Adjust these characters to match what your Omni_Executor.ino expects.
# Standard assumption: '1' -> F13, '2' -> F14, '3' -> F15...
KEY_MAP = {
    "F13": '1', "F14": '2', "F15": '3', "F16": '4',
    "F17": '5', "F18": '6', "Ctrl+F13": '7', "Ctrl+F14": '8',
    "Ctrl+F15": '9', "Alt+F13": '0', "Alt+F14": '-', "Alt+F15": '='
}

class SkillWeaverEngine:
    def __init__(self):
        self.vision = ScreenScanner()
        # Corrected Baudrate
        self.bridge = ArduinoBridge(port='/dev/cu.usbmodemHIDPC1', baudrate=250000)
        self.active_spec = None
        self.current_rotation = {}
        self.priority_queue = []

    def load_spec_data(self, spec_id):
        """Loads the specific JSON file for the detected spec."""
        # Map IDs to filenames
        files = {
            259: "SkillWeaver_Engine/Brain/data/specs/259_assassination.json",
            260: "SkillWeaver_Engine/Brain/data/specs/260_outlaw.json",
            261: "SkillWeaver_Engine/Brain/data/specs/261_sub.json"
        }
        
        filepath = files.get(spec_id)
        if not filepath or not os.path.exists(filepath):
            print(f"[ERROR] No rotation file found for Spec {spec_id}")
            return False

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            self.current_rotation = data.get("universal_slots", {})
            # Flatten the priority list (combining lists if needed)
            priorities = data.get("proc_priority", {}).get("rotation", [])
            ramp = data.get("proc_priority", {}).get("kingsbane_ramp", [])
            self.priority_queue = ramp + priorities # Check Ramp first, then Rotation
            
            print(f"[SYSTEM] Loaded Rotation: {data['spec_name']}")
            return True
        except Exception as e:
            print(f"[ERROR] JSON Load Failed: {e}")
            return False

    def process_frame(self):
        # 1. Capture & Decode
        raw_matrix = self.vision.get_chameleon_pixels()
        if not raw_matrix: return
        
        pixel_data = raw_matrix[0]
        spec_id = self.vision.get_spec_id(raw_matrix[0])
        
        # Color Drift Fix for Mac (259 -> 235)
        if spec_id == 235: spec_id = 259 

        # 2. Spec Switching
        if spec_id > 0 and spec_id != self.active_spec:
            self.active_spec = spec_id
            if self.load_spec_data(spec_id):
                print(f"[SWITCH] Spec {spec_id} Active.")

        if not self.active_spec or not self.priority_queue:
            return

        # 3. Decode Pixel State (Grayscale/Color Agnostic)
        # Using simple indexing based on your Vision module
        # Note: Vision return pixels as (R,G,B). In Grayscale mode it's (L, L, L).
        # We can just pick index 0.
        
        state = {
            "energy": pixel_data[6][1], # Green Channel (or L)
            "cp": int((pixel_data[8][1] / 255.0) * 7), # Scaled to 7
            # Add other flags here from Pixels 2, 3, 4...
            "target": True # Force true for testing if pixel logic isn't ready
        }

        # 4. Priority Execution
        for slot_key in self.priority_queue:
            action_data = self.current_rotation.get(slot_key)
            if not action_data: continue

            if self.evaluate_condition(action_data, state):
                key_str = action_data['key'] # e.g., "F13"
                arduino_char = KEY_MAP.get(key_str)
                
                if arduino_char:
                    print(f"[CAST] {action_data['action']} ({key_str} -> {arduino_char})")
                    self.bridge.send_pulse(arduino_char) 
                    time.sleep(0.2) # Global Cooldown
                    break

    def evaluate_condition(self, action, state):
        # 1. Resource Check
        if state['energy'] < action.get('min_resource', 0):
            return False
            
        # 2. Add Condition Logic Here (CP checks, etc.)
        conditions = action.get('conditions', [])
        if "combo_points_4_plus" in conditions and state['cp'] < 4:
            return False
            
        return True

if __name__ == "__main__":
    engine = SkillWeaverEngine()
    # Force calibration
    engine.vision.calibrate()
    
    if engine.bridge.connect():
        print("[READY] SkillWeaver Connected.")
        while True:
            engine.process_frame()
            time.sleep(0.02)
