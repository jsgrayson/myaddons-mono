import json
import time
from modules.vision import ScreenScanner
from modules.serial_bridge import ArduinoBridge

class SkillWeaverEngine:
    def __init__(self):
        self.matrix = self._load_matrix()
        self.vision = ScreenScanner()
        self.bridge = ArduinoBridge()
        self.active_spec = None
        self.combat_state = "IDLE"

    def _load_matrix(self):
        with open('brain/matrix.json', 'r') as f:
            return json.load(f)

    def process_frame(self):
        # 1. Capture the Chameleon Data Strip (16-pixel steganographic row)
        pixel_data = self.vision.get_chameleon_pixels()
        
        # 2. Decode Spec ID & Combat State
        spec_id = pixel_data[0] # Pixel 1: Spec
        is_in_combat = pixel_data[1] > 128
        target_health = pixel_data[2] / 255.0
        
        if spec_id != self.active_spec:
            self.active_spec = spec_id
            print(f"SWITCHING TO SPEC_ID: {spec_id}")

        # 3. Late-Kick Algorithm (85% Cast Threshold)
        if self.vision.detect_enemy_cast():
            cast_percent = self.vision.get_cast_progress()
            if cast_percent > 0.85:
                self.bridge.execute_chord("INTERRUPT")

        # 4. Priority Execution
        priority_list = self.matrix.get(str(spec_id), [])
        for action in priority_list:
            if self.evaluate_condition(action, pixel_data):
                self.bridge.send_input(action['key'])
                break

    def execute_single_pulse(self):
        """
        Semi-Auto Trigger: Decides which Universal Slot (1-24) to fire based on momentary state.
        Expanded for Midnight V2.11 24-Slot Array.
        """
        # 1. Capture & Decode State
        pixel_data = self.vision.get_chameleon_pixels()
        spec_id = pixel_data[0]
        combat_data = {
            'health': pixel_data[2] / 2.55,
            'enemy_casting': self.vision.detect_enemy_cast(),
            'cast_percent': self.vision.get_cast_progress() if self.vision.detect_enemy_cast() else 0,
            'kill_window_detected': pixel_data[4] > 200,
            'enemy_burst_active': pixel_data[5] > 200,
            'resource': pixel_data[3]
        }

        # 2. Logic: Universal Slot Resolution (Priority Order)

        # RECOVERY (23-24): Critical Health
        if combat_data['health'] < 15:
            return self.data_injector("SLOT_23") # Healthstone/Potion

        # DEFENSE (15-18): Major Survival
        if combat_data['health'] < 40 or combat_data['enemy_burst_active']:
            return self.data_injector("SLOT_15") # Main Defensive

        # CONTROL (11-14): Interrupts
        if combat_data['enemy_casting'] and combat_data['cast_percent'] > 0.85:
            return self.data_injector("SLOT_11") # Primary Interrupt

        # UTILITY (19-22): Catch-all for specialized movement/dispel
        # (Placeholder condition)

        # OFFENSE (07-10): Burst Logic
        if combat_data['kill_window_detected']:
            return self.data_injector("SLOT_07") # Major Offensive CD

        # CORE (01-06): Standard Rotation
        # Simplified resource check example
        if combat_data['resource'] > 80:
             return self.data_injector("SLOT_02") # Spender
        
        return self.data_injector("SLOT_01") # Builder/Filler

    def data_injector(self, slot_name):
        # Maps 24 Universal Slots to F13-F18 with Modifiers
        # Base Keys: F13, F14, F15, F16, F17, F18
        # Groups: Shift (01-06), Ctrl (07-12), Alt (13-18), Shift+Ctrl (19-24)
        
        slot_map = {}
        
        # CORE (01-06) -> Shift + F13-F18
        for i in range(1, 7):
            slot_map[f"SLOT_{i:02d}"] = f"shift+f{12+i}"
            
        # OFFENSE (07-10) -> Ctrl + F13-F16
        for i in range(7, 11):
            slot_map[f"SLOT_{i:02d}"] = f"ctrl+f{12+(i-6)}"
            
        # CONTROL (11-14) -> Alt + F13-F16
        for i in range(11, 15):
            slot_map[f"SLOT_{i:02d}"] = f"alt+f{12+(i-10)}"
            
        # DEFENSE (15-18) -> Alt + F17-F18 + others (Using Shift+Ctrl for consistency)
        # Re-mapping for 6-key block consistency:
        # DEFENSE (15-18) group uses Ctrl+F17, F18... actually let's stick to the 4-block schema
        # Group 3: Alt (13-18) covers Control(11-14 partial) and Defense? 
        # Let's map explicitly for clarity:
        
        # OFFENSE (07-12) -> Ctrl
        slot_map["SLOT_07"] = "ctrl+f13"
        slot_map["SLOT_08"] = "ctrl+f14"
        slot_map["SLOT_09"] = "ctrl+f15"
        slot_map["SLOT_10"] = "ctrl+f16"
        # Control usually uses 11-14
        
        # CONTROL (11-14) -> Alt
        slot_map["SLOT_11"] = "alt+f13"
        slot_map["SLOT_12"] = "alt+f14"
        slot_map["SLOT_13"] = "alt+f15"
        slot_map["SLOT_14"] = "alt+f16"

        # DEFENSE (15-18) -> Alt (continued) or Shift+Ctrl
        slot_map["SLOT_15"] = "alt+f17"
        slot_map["SLOT_16"] = "alt+f18"
        slot_map["SLOT_17"] = "shift+ctrl+f13"
        slot_map["SLOT_18"] = "shift+ctrl+f14"

        # UTILITY (19-22) -> Shift+Ctrl
        slot_map["SLOT_19"] = "shift+ctrl+f15"
        slot_map["SLOT_20"] = "shift+ctrl+f16"
        slot_map["SLOT_21"] = "shift+ctrl+f17"
        slot_map["SLOT_22"] = "shift+ctrl+f18"

        # RECOVERY (23-24) -> Shift+Alt
        slot_map["SLOT_23"] = "shift+alt+f13"
        slot_map["SLOT_24"] = "shift+alt+f14"

        key_chord = slot_map.get(slot_name)
        if key_chord:
            print(f"INJECTING: {slot_name} -> {key_chord}")
            self.bridge.send_input(key_chord)

if __name__ == "__main__":
    engine = SkillWeaverEngine()
    while True:
        engine.process_frame()
