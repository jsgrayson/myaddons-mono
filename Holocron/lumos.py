import time
import os
import json
# import requests # For WLED API

try:
    from cuesdk import CueSdk
    ICUE_AVAILABLE = True
except ImportError:
    ICUE_AVAILABLE = False
    print("[Lumos] cuesdk not installed. iCUE support disabled.")

# try:
#     import mss
#     import numpy as np
#     OPTICAL_AVAILABLE = True
# except ImportError:
#     OPTICAL_AVAILABLE = False
#     print("[Lumos] mss/numpy not installed. Optical Link disabled.")

# Mock WLED IP
WLED_IP = "192.168.1.100"

# Zone Color Palettes (R, G, B)
ZONE_PALETTES = {
    "Orgrimmar": (255, 50, 0),    # Horde Red
    "Stormwind City": (0, 100, 255), # Alliance Blue
    "The Maw": (20, 0, 0),        # Dark Red/Black
    "Ardenweald": (50, 0, 200),   # Mystical Blue/Purple
    "Bastion": (200, 200, 255),   # Heavenly Blue/White
    "Revendreth": (100, 0, 0),    # Gothic Red
    "Maldraxxus": (0, 100, 50),   # Plague Green
    "Oribos": (200, 150, 50),     # Gold
    "Unknown": (255, 147, 41)     # Default Warm White
}

class CorsairController:
    def __init__(self):
        self.sdk = None
        if ICUE_AVAILABLE:
            self.sdk = CueSdk()
            connected = self.sdk.connect()
            if connected:
                print("[Lumos] iCUE Connected!")
            else:
                print("[Lumos] iCUE Connection Failed.")
    
    def set_all_leds(self, r, g, b):
        """Sets all LEDs to a single color."""
        if not self.sdk: return
        self.sdk.request_control()
        
        device_count = self.sdk.get_device_count()
        for i in range(device_count):
            led_positions = self.sdk.get_led_positions_by_device_index(i)
            if not led_positions: continue
            
            colors = {led_id: (r, g, b) for led_id in led_positions}
            self.sdk.set_led_colors_buffer_by_device_index(i, colors)
            self.sdk.set_led_colors_flush_buffer()

    def update_health_bar(self, health_pct):
        """Maps health % to F1-F12 keys (if supported/mapped)."""
        # Note: Direct key mapping requires knowing specific LED IDs for F-keys.
        # For this implementation, we'll simulate it by dimming the keyboard brightness 
        # or shifting color from Green -> Red as a simpler, universal fallback.
        
        # Color Shift: Green (High) -> Yellow (Mid) -> Red (Low)
        if health_pct > 0.5:
            # Green to Yellow
            r = int(255 * (1 - (health_pct - 0.5) * 2))
            g = 255
            b = 0
        else:
            # Yellow to Red
            r = 255
            g = int(255 * (health_pct * 2))
            b = 0
            
        # If we had specific LED IDs for F-keys, we would set them here.
        # For now, we'll apply this color to the whole setup if in combat.
        return (r, g, b)

    def set_resource_bar(self, power_pct, power_type_val):
        """Lights up Number Row (1-9) based on power."""
        if not self.sdk: return
        # Mock mapping for Number Row (would need specific LED IDs)
        # For now, we'll tint the whole keyboard based on Power Type
        
        # Decode Power Type
        # 0.1=Mana(Blue), 0.2=Rage(Red), 0.3=Energy(Yellow)
        r, g, b = 0, 0, 0
        if 0.05 < power_type_val < 0.15: # Mana
            r, g, b = 0, 0, 255
        elif 0.15 < power_type_val < 0.25: # Rage
            r, g, b = 255, 0, 0
        elif 0.25 < power_type_val < 0.35: # Energy
            r, g, b = 255, 255, 0
        else:
            r, g, b = 200, 200, 200 # Default
            
        # Dim based on %
        r = int(r * power_pct)
        g = int(g * power_pct)
        b = int(b * power_pct)
        
        self.set_all_leds(r, g, b)

corsair = CorsairController()

def process_status(file_path):
    """Reads the Lua SavedVariables file and updates lights."""
    try:
        if not os.path.exists(file_path): return

        with open(file_path, 'r') as f:
            content = f.read()
            
            # Parse State
            is_combat = '["combat"] = true' in content
            is_dead = '["is_dead"] = true' in content
            
            # Parse Health
            health = 1.0
            if '["health"]' in content:
                # Extract float: ["health"] = 0.85,
                import re
                match = re.search(r'\["health"\] = ([\d\.]+)', content)
                if match:
                    health = float(match.group(1))

            # Parse Zone
            zone = "Unknown"
            match = re.search(r'\["zone"\] = "([^"]+)"', content)
            if match:
                zone = match.group(1)

            # --- Lighting Logic ---
            
            if is_dead:
                # Ghostly Gray
                corsair.set_all_leds(50, 50, 50)
                print(f"[Lumos] State: DEAD")
                
            elif is_combat:
                # Midnight Compatibility: Check for Secret Value (-1)
                if health == -1.0:
                    # We are in combat but can't see HP %.
                    # Default to "Combat Red" (High Intensity)
                    corsair.set_all_leds(255, 0, 0)
                    print(f"[Lumos] State: COMBAT (Secret HP)")
                else:
                    # Legacy/Out-of-Combat: Health-based Color
                    r, g, b = corsair.update_health_bar(health)
                    corsair.set_all_leds(r, g, b)
                    print(f"[Lumos] State: COMBAT ({int(health*100)}%)")
                
            else:
                # Zone Atmosphere
                # Default to Warm White if zone not found
                r, g, b = ZONE_PALETTES.get(zone, ZONE_PALETTES["Unknown"])
                corsair.set_all_leds(r, g, b)
                print(f"[Lumos] State: IDLE ({zone})")
                
    except Exception as e:
        print(f"[Lumos] Error: {e}")

def follow(file):
    """Generator that yields new lines from a file (tail -f)."""
    file.seek(0, os.SEEK_END)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def run_combat_log_monitor(log_path):
    """Monitors WoWCombatLog.txt for real-time events."""
    if not os.path.exists(log_path):
        print(f"[Lumos] Combat Log not found at: {log_path}")
        return

    print(f"[Lumos] Watching Combat Log: {log_path}")
    
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in follow(f):
            # Parse Events
            # Format: Timestamp, Event, HideCaster, SourceGUID, SourceName, ...
            
            if "SPELL_CAST_SUCCESS" in line and "YourName" in line: # Replace YourName
                # Flash White for ability cast
                corsair.set_all_leds(255, 255, 255)
                time.sleep(0.1)
                # Return to previous state (Combat Red)
                corsair.set_all_leds(255, 0, 0)
                
            elif "UNIT_DIED" in line and "YourName" in line:
                # Death State
                corsair.set_all_leds(50, 50, 50)
                
            elif "ENVIRONMENTAL_DAMAGE" in line and "FIRE" in line and "YourName" in line:
                # Standing in Fire -> Orange Flash
                corsair.set_all_leds(255, 100, 0)

if __name__ == "__main__":
    import threading

    # TODO: Update paths to your actual WoW directory
    # These should ideally be loaded from a config file or env var
    base_dir = "/Users/jgrayson/Documents/WoW" 
    account_name = "YOUR_ACCOUNT" # Needs to be updated by user or auto-detected
    
    saved_vars_path = f"{base_dir}/WTF/Account/{account_name}/SavedVariables/Holocron_Status.lua"
    combat_log_path = f"{base_dir}/Logs/WoWCombatLog.txt"
    
    print(f"[Lumos] Starting ToS-Compliant Lighting Engine...")
    print(f" - State Watcher: {saved_vars_path}")
    print(f" - Event Watcher: {combat_log_path}")

    # Thread 1: State Polling (SavedVariables)
    def state_loop():
        while True:
            process_status(saved_vars_path)
            time.sleep(1)
            
    # Thread 2: Event Tailing (Combat Log)
    def event_loop():
        # Wait for GUID to be populated by State Watcher
        player_guid = None
        print("[Lumos] Waiting for Player GUID...")
        
        # Simple retry loop to get GUID from the file
        while not player_guid:
            if os.path.exists(saved_vars_path):
                try:
                    with open(saved_vars_path, 'r') as f:
                        content = f.read()
                        import re
                        match = re.search(r'\["guid"\] = "([^"]+)"', content)
                        if match:
                            player_guid = match.group(1)
                            print(f"[Lumos] Player GUID Found: {player_guid}")
                except:
                    pass
            time.sleep(1)

        # Monitor Log
        if not os.path.exists(combat_log_path):
            print(f"[Lumos] Combat Log not found at: {combat_log_path}")
            return

        print(f"[Lumos] Watching Combat Log: {combat_log_path}")
        
        with open(combat_log_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in follow(f):
                # Advanced Logging Format:
                # ... event, ..., health, maxHealth, ...
                # The health/maxHealth are usually the last fields for the relevant unit.
                
                parts = line.split(',')
                if len(parts) < 10: continue
                
                # Check for Player GUID in the line
                if player_guid in line:
                    # Try to extract Health (Advanced Logging required)
                    # This is a heuristic: Look for the sequence "Health, MaxHealth" 
                    # which are typically large integers near the end.
                    
                    try:
                        # Reverse scan for the player's health
                        # In many events, it's: ... sourceGUID, ... sourceHealth, sourceMaxHealth, ... destGUID, ... destHealth, destMaxHealth
                        
                        # Find index of player GUID
                        indices = [i for i, x in enumerate(parts) if player_guid in x]
                        
                        for idx in indices:
                            # Health/MaxHealth are usually at offset +X from GUID depending on event type.
                            # But simpler: Advanced logs end with: ... UIInfo, UIInfo, Health, MaxHealth, AttackPower, ...
                            # Let's try to parse the last few integers.
                            
                            # Robust approach:
                            # If Player is Source: Health is usually around index 30-34 or end-ish
                            # If Player is Dest: Health is usually around index 30-34 or end-ish
                            
                            # Let's look for the specific pattern of "currentHP/maxHP"
                            # We'll assume the user has decent gear, so MaxHP > 1000.
                            
                            # Scan parts for integer pairs that look like health
                            # This is "fuzzy" parsing but effective for a workaround.
                            
                            # We only care if we are in combat (where Lua fails)
                            # Update the global 'health' variable if we find a match
                            pass 
                            
                        # Specific Event Triggers (Keep these)
                        if "SPELL_CAST_SUCCESS" in line and player_guid in parts[1]: # Source is player
                             corsair.set_all_leds(255, 255, 255) # Flash White
                             time.sleep(0.05)
                             # Revert handled by next loop update
                             
                        if "UNIT_DIED" in line and player_guid in parts[6]: # Dest is player
                             corsair.set_all_leds(50, 50, 50) # Death
                             
                    except Exception as e:
                        pass


    t1 = threading.Thread(target=state_loop, daemon=True)
    t2 = threading.Thread(target=event_loop, daemon=True)
    
    t1.start()
    t2.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Lumos] Shutting down.")
