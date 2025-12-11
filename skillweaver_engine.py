import time
import os
import threading
import re
try:
    from cuesdk import CueSdk
    ICUE_AVAILABLE = True
except ImportError:
    ICUE_AVAILABLE = False

# --- CONFIG ---
# TODO: Load from config file
BASE_DIR = "/Users/jgrayson/Documents/WoW"
LOG_PATH = f"{BASE_DIR}/Logs/WoWCombatLog.txt"
PLAYER_NAME = "YourCharacterName" # Replace with dynamic lookup later

# --- iCUE CONTROLLER (Simplified) ---
class CorsairController:
    def __init__(self):
        self.sdk = None
        if ICUE_AVAILABLE:
            self.sdk = CueSdk()
            self.sdk.connect()
    
    def flash_key(self, key_id, r, g, b):
        """Flashes a specific key (mock implementation for now)."""
        if not self.sdk: return
        # In a real implementation, we'd map 'Q', 'E', etc. to LED IDs.
        # For this prototype, we'll flash the whole keyboard to signal the 'Type' of action.
        print(f"[SkillWeaver] Flashing {key_id} -> ({r},{g},{b})")
        # self.sdk.set_led_colors... (omitted for brevity)

corsair = CorsairController()

# --- GAME STATE ---
class GameState:
    def __init__(self):
        self.rage = 0
        self.mana = 100
        self.target_hp_pct = 1.0
        self.cooldowns = {} # spell_id -> end_time

    def update_resource(self, amount, type="Rage"):
        if type == "Rage":
            self.rage = min(100, max(0, self.rage + amount))
            print(f"[State] Rage: {self.rage}")

    def update_target_health(self, pct):
        self.target_hp_pct = pct

# --- ROTATION LOGIC (WARRIOR) ---
class WarriorRotation:
    def __init__(self, state):
        self.state = state
    
    def get_suggestion(self):
        # 1. Execute (High Priority)
        if self.state.target_hp_pct < 0.20:
            return "EXECUTE", (128, 0, 128), 5308 # Purple, SpellID
            
        # 2. Rampage (Resource Dump)
        if self.state.rage >= 80:
            return "RAMPAGE", (255, 0, 0), 184367 # Red, SpellID
            
        # 3. Bloodthirst (Builder)
        return "BLOODTHIRST", (0, 255, 0), 23881 # Green, SpellID

# --- ENGINE ---
class SkillWeaverEngine:
    def __init__(self):
        self.state = GameState()
        self.rotation = WarriorRotation(self.state)
        self.running = False
        self.thread = None
        self.current_suggestion = None
        self.mistakes = []

    def start(self):
        if self.running: return
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print(f"[SkillWeaver] Engine Running. Watching: {LOG_PATH}")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def get_recommendation(self):
        """Returns current recommendation for Arbiter"""
        if not self.current_suggestion:
            return None
        
        name, color, spell_id = self.current_suggestion
        return {
            "spell_id": spell_id,
            "spell_name": name
        }

    def report_mistake(self, actual_spell_id, expected_spell_id):
        """Feedback from Arbiter"""
        print(f"[SkillWeaver] Feedback: Mistake detected! Cast {actual_spell_id}, Expected {expected_spell_id}")
        self.mistakes.append({
            "timestamp": time.time(),
            "actual": actual_spell_id,
            "expected": expected_spell_id
        })

    def _follow(self, file):
        file.seek(0, os.SEEK_END)
        while self.running:
            line = file.readline()
            if not line:
                time.sleep(0.05)
                continue
            yield line

    def _run_loop(self):
        if not os.path.exists(LOG_PATH):
            print(f"[SkillWeaver] Log not found: {LOG_PATH}. Using Mock Mode.")
            self._mock_loop()
            return

        with open(LOG_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            for line in self._follow(f):
                self._process_line(line)

    def _mock_loop(self):
        """Simulate rotation for testing"""
        while self.running:
            time.sleep(1)
            # Simulate rage gain
            self.state.update_resource(10, "Rage")
            self._update_suggestion()

    def _process_line(self, line):
        # 1. Parse Resources (SPELL_ENERGIZE)
        if "SPELL_ENERGIZE" in line and PLAYER_NAME in line:
            parts = line.split(',')
            try:
                amount = int(parts[-2])
                self.state.update_resource(amount, "Rage")
            except:
                pass
        
        # 2. Parse Spells (SPELL_CAST_SUCCESS)
        if "SPELL_CAST_SUCCESS" in line and PLAYER_NAME in line:
            if "Rampage" in line:
                self.state.rage = max(0, self.state.rage - 80)
                print(f"[State] Rampage Cast. Rage: {self.state.rage}")

        # 3. Evaluate Rotation
        self._update_suggestion()

    def _update_suggestion(self):
        action, color, spell_id = self.rotation.get_suggestion()
        self.current_suggestion = (action, color, spell_id)
        
        # Output (Debounced in real app)
        # print(f"[Coach] Suggestion: {action}")
        # corsair.flash_key(action, *color)

if __name__ == "__main__":
    engine = SkillWeaverEngine()
    engine.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        engine.stop()
