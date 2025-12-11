import mss
import numpy as np
import json
import time
import os
import sys
import threading
import cv2  # OpenCV for Computer Vision
from pynput import keyboard
from pynput.keyboard import Key, Controller

# --- CONFIGURATION ---
CONFIG_FILE = "visual_config.json"
DEFAULT_CONFIG = {
    "trigger_key": "space",
    "healer_mode": False,
    "regions": {
        "dps_icon": {"top": 500, "left": 500, "width": 20, "height": 20},      # ST Cue
        "dps_icon_aoe": {"top": 500, "left": 580, "width": 20, "height": 20},  # AoE Cue (Offset by ~80px)
        "party1": {"top": 200, "left": 100, "width": 100, "height": 30},
        "party2": {"top": 240, "left": 100, "width": 100, "height": 30},
        "party3": {"top": 280, "left": 100, "width": 100, "height": 30},
        "party4": {"top": 320, "left": 100, "width": 100, "height": 30},
        "party5": {"top": 360, "left": 100, "width": 100, "height": 30},
        "nameplates": {"top": 100, "left": 0, "width": 1920, "height": 800} # Scan area for nameplates
    },
    "key_map": {
        # Blue Channel -> Key
        20: "1", 40: "2", 60: "3", 80: "4", 
        100: "5", 120: "6", 140: "7", 160: "8", 
        180: "9", 200: "0", 220: "-", 240: "="
    },
    "mod_map": {
        # Green Channel -> Modifier
        0: None,
        64: Key.shift,
        128: Key.ctrl,
        192: Key.alt
    },
    "special_keys": {
        "interrupt": "r",
        "cycle": "tab",
        "trinket": "t",
        "pet_action": "a" # Key to spam for Pet Battles
    },
    "tolerance": 15
}

class VisualWeaver:
    def __init__(self):
        self.config = DEFAULT_CONFIG
        self.paused = True
        self.healer_mode = False
        self.pet_mode = False
        self.running = False
        self.trigger_pressed = False
        self.keyboard_controller = Controller()
        self.thread = None
        self.target_count = 0
        self.aoe_mode = False
        self.load_config()

    def load_config(self):
        """Loads configuration from visual_config.json or creates a default one."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
            print(f"Configuration loaded from {CONFIG_FILE}")
        else:
            self.config = DEFAULT_CONFIG
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
            print(f"Default configuration created at {CONFIG_FILE}")

    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)
        print("Configuration saved.")

    def on_press(self, key):
        try:
            # Control Keys
            if key == Key.f8:
                self.paused = not self.paused
                print(f"[{'PAUSED' if self.paused else 'RESUMED'}]")
            elif key == Key.f9:
                self.healer_mode = not self.healer_mode
                self.pet_mode = False # Exclusive
                print(f"Healer Mode: {'ON' if self.healer_mode else 'OFF'}")
            elif key == Key.f11:
                self.pet_mode = not self.pet_mode
                self.healer_mode = False # Exclusive
                print(f"Pet Battle Mode: {'ON' if self.pet_mode else 'OFF'}")
            elif key == keyboard.KeyCode.from_char('q'):
                print("Quitting...")
                self.stop()
            
            # Trigger Key
            if str(key).replace("'", "") == self.config["trigger_key"]:
                self.trigger_pressed = True
                
        except AttributeError:
            if str(key).replace("'", "") == self.config["trigger_key"]:
                self.trigger_pressed = True

    def on_release(self, key):
        if str(key).replace("'", "") == self.config["trigger_key"]:
            self.trigger_pressed = False

    def get_action_from_color(self, r, g, b):
        """Decodes the pixel color into an action (Key + Modifier)."""
        tolerance = self.config["tolerance"]
        
        # 1. Check Interrupt (Red)
        if r > 200 and g < 50 and b < 50:
            return self.config["special_keys"]["interrupt"], None
            
        # 2. Check Trinket (Magenta: Red + Blue)
        if r > 200 and g < 50 and b > 200:
            return self.config["special_keys"].get("trinket", "t"), None

        # 3. Check Cycle (Cyan: Green + Blue)
        if r < 50 and g > 200 and b > 200:
            return self.config["special_keys"]["cycle"], None
            
        # 3. Check Rotation (Blue + Green Mod)
        # Find closest Key (Blue)
        best_key = None
        min_dist = float('inf')
        
        for val, key in self.config["key_map"].items():
            dist = abs(int(val) - b)
            if dist < min_dist:
                min_dist = dist
                best_key = key
                
        if min_dist > tolerance:
            return None, None # No key detected
            
        # Find closest Modifier (Green)
        best_mod = None
        min_mod_dist = float('inf')
        
        for val, mod in self.config["mod_map"].items():
            dist = abs(int(val) - g)
            if dist < min_mod_dist:
                min_mod_dist = dist
                best_mod = mod
                
        return best_key, best_mod

    def scan_nameplates(self, sct):
        """
        Scans the screen for enemy nameplates (Red Bars) using OpenCV.
        Returns the count of active targets.
        """
        region = self.config["regions"].get("nameplates", {"top": 100, "left": 0, "width": 1920, "height": 800})
        monitor = {
            "top": int(region["top"]), 
            "left": int(region["left"]), 
            "width": int(region["width"]), 
            "height": int(region["height"])
        }
        
        # Capture screen
        img = np.array(sct.grab(monitor))
        
        # Convert to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) # Remove Alpha
        hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
        
        # Define Red Color Range (Enemy Nameplates)
        # Red wraps around 0/180 in HSV
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])
        
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2
        
        # Find Contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        count = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # Filter small noise (health bars are usually significant size)
            if area > 100: 
                x, y, w, h = cv2.boundingRect(cnt)
                # Filter by aspect ratio (Health bars are wide rectangles)
                aspect_ratio = float(w)/h
                if aspect_ratio > 3: 
                    count += 1
                    
        return count

    def run_loop(self):
        print("Visual Weaver Loop Started 👁️")
        last_scan_time = 0
        
        with mss.mss() as sct:
            while self.running:
                current_time = time.time()
                
                # 1. Context Awareness (Nameplate Scan) - Every 0.5s
                if not self.paused and (current_time - last_scan_time > 0.5):
                    self.target_count = self.scan_nameplates(sct)
                    last_scan_time = current_time
                    
                    # Auto-Switch Logic
                    new_aoe_mode = self.target_count >= 3
                    if new_aoe_mode != self.aoe_mode:
                        self.aoe_mode = new_aoe_mode
                        mode_str = "AoE (Multi-Target)" if self.aoe_mode else "ST (Single-Target)"
                        print(f"Context Shift: {self.target_count} Targets -> {mode_str}")

                # 2. Rotation Execution
                if not self.paused and self.trigger_pressed:
                # 2. Rotation Execution
                if not self.paused and self.trigger_pressed:
                    # Determine which cue to read
                    target_region = "dps_icon" # Default ST
                    
                    if self.aoe_mode:
                        # Try AoE first
                        region = self.config["regions"].get("dps_icon_aoe", self.config["regions"]["dps_icon"])
                        monitor = {
                            "top": int(region["top"]), 
                            "left": int(region["left"]), 
                            "width": int(region["width"]), 
                            "height": int(region["height"])
                        }
                        img = np.array(sct.grab(monitor))
                        cy, cx = region["height"] // 2, region["width"] // 2
                        pixel = img[cy, cx]
                        b, g, r = int(pixel[0]), int(pixel[1]), int(pixel[2])
                        
                        key_to_press, modifier = self.get_action_from_color(r, g, b)
                        
                        if key_to_press:
                            # Found valid AoE key
                            pass 
                        else:
                            # Fallback to ST
                            # print("AoE Cue empty, falling back to ST")
                            target_region = "dps_icon"
                    
                    if target_region == "dps_icon":
                        region = self.config["regions"]["dps_icon"]
                        monitor = {
                            "top": int(region["top"]), 
                            "left": int(region["left"]), 
                            "width": int(region["width"]), 
                            "height": int(region["height"])
                        }
                        img = np.array(sct.grab(monitor))
                        cy, cx = region["height"] // 2, region["width"] // 2
                        pixel = img[cy, cx]
                        b, g, r = int(pixel[0]), int(pixel[1]), int(pixel[2])
                        
                        key_to_press, modifier = self.get_action_from_color(r, g, b)

                    if key_to_press:
                        mod_str = f"{modifier}+" if modifier else ""
                        mode_label = "AoE" if (self.aoe_mode and target_region != "dps_icon") else "ST"
                        print(f"[{mode_label}] Color ({r},{g},{b}) -> {mod_str}{key_to_press}")
                        
                        if modifier:
                            self.keyboard_controller.press(modifier)
                            time.sleep(0.01)
                            
                        self.keyboard_controller.press(key_to_press)
                        time.sleep(0.05 + np.random.uniform(0.01, 0.03))
                        self.keyboard_controller.release(key_to_press)
                        
                        if modifier:
                            self.keyboard_controller.release(modifier)
                            
                        time.sleep(0.1)
                    
                # 3. Pet Battle Mode (Auto-Script)
                if not self.paused and self.pet_mode:
                    pet_key = self.config["special_keys"].get("pet_action", "a")
                    print(f"Pet Mode: Pressing {pet_key}")
                    self.keyboard_controller.press(pet_key)
                    time.sleep(0.05)
                    self.keyboard_controller.release(pet_key)
                    time.sleep(0.5) # Spam rate
                
                time.sleep(0.01) # Loop rate
        print("Visual Weaver Loop Stopped.")

    def start(self):
        if self.running:
            return
        self.running = True
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        
        self.thread = threading.Thread(target=self.run_loop)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        if hasattr(self, 'listener'):
            self.listener.stop()

if __name__ == "__main__":
    weaver = VisualWeaver()
    weaver.start()
    print("Press F8 to Pause/Resume. Press Q to Quit.")
    try:
        while weaver.running:
            time.sleep(1)
    except KeyboardInterrupt:
        weaver.stop()
