import mss
import mss.tools
import numpy as np
import json
import os
import sys
import time
import random
import glob
from modules.serial_link import SerialLink as ArduinoBridge
import ConditionEngine

# --- UNIVERSAL SKILLWEAVER ENGINE (v4.2 PRECISION) ---
# Supports ALL 13 Classes / 60 Specs. CALIBRATED SIGNAL (Divisor 229.5).
# Dynamic Spec Loading & Adaptive Decoder.

REACTION_MEAN = 0.08
REACTION_STD = 0.02
INPUT_JITTER = 0.01

# v4.2 CALIBRATED DIVISOR: 218.0 (Compensates for display blue-loss)
DIVISOR_UNIVERSAL = 218.0

KEY_MAP = {
    "F13": 0x01, "F14": 0x02, "F15": 0x03, "F16": 0x04, "F17": 0x05, "F18": 0x06, "F19": 0x07, "F20": 0x08,
    "F21": 0x09, "F22": 0x0A, "F23": 0x0B, "F24": 0x0C,
    "SHIFT+F13": 0x0D, "SHIFT+F14": 0x0E, "SHIFT+F15": 0x0F, "SHIFT+F16": 0x10, "SHIFT+F17": 0x11, "SHIFT+F18": 0x12,
    "SHIFT+F21": 0x13, "SHIFT+F22": 0x14, "SHIFT+F23": 0x15, "SHIFT+F24": 0x16,
    "CTRL+F13": 0x17, "CTRL+F14": 0x18, "CTRL+F15": 0x19, "CTRL+F16": 0x1A, "CTRL+F17": 0x1B, "CTRL+F18": 0x1C,
    "CTRL+F19": 0x1D, "CTRL+F20": 0x1E, "CTRL+F21": 0x1F, "CTRL+F22": 0x20
}

# --- UNIVERSAL SPEC DATABASE ---
SPEC_DB = {
    11: "Warrior - Arms", 12: "Warrior - Fury", 13: "Warrior - Protection",
    21: "Paladin - Holy", 22: "Paladin - Protection", 23: "Paladin - Retribution",
    31: "Hunter - Beast Mastery", 32: "Hunter - Marksmanship", 33: "Hunter - Survival",
    41: "Rogue - Assassination", 42: "Rogue - Outlaw", 43: "Rogue - Subtlety",
    51: "Priest - Discipline", 52: "Priest - Holy", 53: "Priest - Shadow",
    61: "Death Knight - Blood", 62: "Death Knight - Frost", 63: "Death Knight - Unholy",
    71: "Shaman - Elemental", 72: "Shaman - Enhancement", 73: "Shaman - Restoration",
    81: "Mage - Arcane", 82: "Mage - Fire", 83: "Mage - Frost",
    91: "Warlock - Affliction", 92: "Warlock - Demonology", 93: "Warlock - Destruction",
    101: "Monk - Brewmaster", 102: "Monk - Mistweaver", 103: "Monk - Windwalker",
    111: "Druid - Balance", 112: "Druid - Feral", 113: "Druid - Guardian", 114: "Druid - Restoration",
    121: "Demon Hunter - Havoc", 122: "Demon Hunter - Vengeance",
    131: "Evoker - Devastation", 132: "Evoker - Preservation", 133: "Evoker - Augmentation"
}

class SkillWeaverEngine:
    def __init__(self):
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]
        self.bridge = ArduinoBridge()
        self.bridge_connected = False
        self.active_spec = None
        self.rotation = {}
        self.priority_list = []
        self.next_action_time = 0
        self.last_load_attempt = 0
        
        # Calibration State
        self.uplink_y = 1116 
        self.uplink_x = 0
        self.scale = 2 # Retina
        
        # Paths
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.spec_dir = os.path.join(self.base_dir, "data", "specs")

    def calibrate(self):
        print("\n[SCAN] Searching for UNIVERSAL Stealth Signal (v4.1)...")
        scan_height = 200 
        scan_area = {
            "top": self.monitor["height"] - scan_height,
            "left": 0,
            "width": 128,
            "height": scan_height
        }
        
        img = np.array(self.sct.grab(scan_area))
        found = False
        for y in range(scan_height - 1, 0, -1):
            for x in range(0, 10):
                px = img[y, x]
                diff = int(px[0]) - int(px[2])
                
                # Pilot signal (0.4 Blue - 0.08 Red > 50 diff)
                if diff > 50:
                    self.uplink_y = scan_area["top"] + y
                    self.uplink_x = scan_area["left"] + x
                    print(f"[LOCK] UPLINK ESTABLISHED at Y={self.uplink_y}, X={self.uplink_x}")
                    found = True
                    break
            if found: break
        
        if not found:
            print("[CRITICAL] NO SIGNAL DETECTED. CHECK GAME ADDON.")
            sys.exit(1)
            
    def decode(self, pixel, divisor=DIVISOR_UNIVERSAL):
        diff = int(pixel[0]) - int(pixel[2])
        if diff < 5: return 0.0, diff
        val = (diff / divisor) * 255.0
        return val, diff

    def load_rotation(self, hash_id):
        h_int = int(hash_id + 0.5)
        if h_int == self.active_spec: return
        
        # Debounce loading
        if time.time() - self.last_load_attempt < 2: return
        self.last_load_attempt = time.time()

        # DYNAMIC PULL BASED ON SPEC ID (e.g., 41_*.json)
        pattern = os.path.join(self.spec_dir, f"{h_int}_*.json")
        matches = glob.glob(pattern)
        
        if not matches:
            print(f"\n[ERROR] No rotation file discovered for Spec ID: {h_int}")
            return False
            
        path = matches[0]
        filename = os.path.basename(path)
            
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                
                # AUTHORITATIVE FORMAT PARSING
                self.rotation = data.get('universal_slots', {})
                # Combined Rotation (Ramp + Normal)
                priorities = data.get('proc_priority', {}).get('rotation', [])
                ramp = data.get('proc_priority', {}).get('kingsbane_ramp', [])
                self.priority_list = ramp + priorities
                
                self.active_spec = h_int
                spec_name = data.get('spec_name', SPEC_DB.get(h_int, "Unknown"))
                print(f"\n[SYSTEM] Rotation Active: {filename} ({spec_name})")
                print(f"[SYSTEM] Linked {len(self.priority_list)} logic nodes.")
                return True
        except Exception as e:
            print(f"\n[ERROR] JSON Load Failed for {filename}: {e}")
            return False

    def evaluate(self, slot_id, state):
        if slot_id not in self.rotation: return False
        slot = self.rotation[slot_id]
        if state['power'] < slot.get('min_resource', 0): return False
        for c in slot.get('conditions', []):
            if not ConditionEngine.evaluate(c, state): return False
        return True

    def run(self):
        print(">> SkillWeaver Engine Active (v4.1 Universal Core)")
        self.calibrate()
        self.bridge_connected = self.bridge.connect()
        
        while True:
            try:
                # 1. CAPTURE
                snap = np.array(self.sct.grab({
                    "top": self.uplink_y, 
                    "left": self.uplink_x, 
                    "width": 128, 
                    "height": 1
                }))
                row = snap[0]

                # 2. DECODE
                pil_val, pil_diff = self.decode(row[0])
                h, _ = self.decode(row[1])

                # v4.2: Universal Telemetry
                sec_raw = self.decode(row[8])[0]
                sec_val = int(round(sec_raw / 25.0))

                state = {
                    "hash": h,
                    "combat": self.decode(row[2])[0] > 128,
                    "hp": min(100.0, (self.decode(row[3])[0] / 255.0) * 100),
                    "thp": min(100.0, (self.decode(row[4])[0] / 255.0) * 100),
                    "valid": self.decode(row[5])[0] > 128,
                    "power": min(100.0, (self.decode(row[7])[0] / 255.0) * 100),
                    "sec": sec_val,
                    "snap": self.decode(row[30])[0] > 128
                }



                # 3. SPEC WATCHDOG
                h_int = int(h + 0.5)
                if h_int > 0 and h_int != self.active_spec:
                    self.load_rotation(h)

                # 4. STATUS + DEBUG
                status = "COMBAT" if state['combat'] else "IDLE  "
                spec_name = SPEC_DB.get(h_int, "UNKNOWN")
                # DEBUG: Show raw Blue/Red from Spec pixel
                spec_pix = row[1]
                raw_b, raw_r = int(spec_pix[0]), int(spec_pix[2])
                output = f"\r[{status}] {spec_name} ({h_int}) | HP:{state['hp']:.0f}% | Res:{state['power']:.0f}% | B:{raw_b} R:{raw_r} Diff:{raw_b-raw_r}   "

                # 5. ROTATION EXECUTION
                if self.active_spec and state['combat']:
                    if time.time() >= self.next_action_time:
                        for slot_id in self.priority_list:
                            if self.evaluate(slot_id, state):
                                action = self.rotation[slot_id]
                                byte = KEY_MAP.get(action['key']) 
                                if not byte:
                                    byte = KEY_MAP.get(action['key'].upper())
                                
                                if byte and self.bridge_connected:
                                    self.bridge.send_pulse(byte)
                                    delay = max(0, random.normalvariate(REACTION_MEAN, REACTION_STD)) + INPUT_JITTER
                                    self.next_action_time = time.time() + delay
                                    output += f" => CAST: {action['action']}   "
                                    break
                
                sys.stdout.write(output.ljust(120))
                sys.stdout.flush()
                time.sleep(0.01)

            except KeyboardInterrupt:
                print("\n[STOP] SkillWeaver Engine halted.")
                break

if __name__ == "__main__":
    SkillWeaverEngine().run()
