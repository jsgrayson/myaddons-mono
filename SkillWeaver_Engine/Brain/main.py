import time
import sys
import numpy as np
# Importing actual classes but aliasing them to match User's request variables
from modules.vision import ScreenScanner as Vision
from modules.logic_engine import PriorityEngine as LogicEngine
from modules.serial_link import SerialLink as SerialBridge

# --- CONFIGURATION ---
# Preserving the verified Logitech Ghost Port/Baud
SERIAL_PORT = '/dev/cu.usbmodemHIDPC1' 
BAUD_RATE = 250000

def main():
    print("--- INITIATING SKILLWEAVER ENGINE (NO BAIT MODE) ---")
    
    try:
        bridge = SerialBridge(SERIAL_PORT, BAUD_RATE)
        vision = Vision()
        # Initialize Logic Engine with required args (placeholders)
        logic = LogicEngine(bridge=bridge, matchups="matchups_vs_all.json", gear_profile="gear_current.json")
    except Exception as e:
        print(f"[CRITICAL] Startup Failed: {e}")
        return

    if not bridge.connect():
        print("[CRITICAL] Serial Link Connection Failed.")
        return

    # 1. DELAY & CALIBRATE
    print("\n[STAGING] FOCUS WOW NOW. CALIBRATING IN 5 SECONDS...")
    time.sleep(5)
    vision.calibrate() # This gets your 173 baseline
    print(f"[ACTIVE] Baseline: {vision.target_red}. Waiting for Lethal Anchor (Pixel 16)...")

    # 2. THE LOOP
    while True:
        try:
            # Get the data strip (80px wide)
            # get_chameleon_pixels returns (1, 80, 4)
            raw_matrix = vision.get_chameleon_pixels()
            packet = raw_matrix[0] # The row
            
            # Check Spec ID (Pixel 0)
            # get_spec_id expects the raw matrix or row? 
            # In previous vision.py update, get_spec_id took (frame_row). 
            # So we pass raw_matrix[0]. 
            # vision.get_spec_id(packet)
            if vision.get_spec_id(packet) == 189000:
                
                # --- CHECK LETHAL ANCHOR ONLY (Pixel 16 / Index 32) ---
                # We check if the Red channel matches the calibration (173)
                # packet[32] is BGRA: [Blue, Green, Red, Alpha]
                # User says: "anchor_pixel_red = packet[32][0]". 
                # This implies User thinks Index 0 is Red. 
                # OR user wants us to check the channel that matches the calibration target.
                # In calibrate(), we set target_red = max(img[0,0,0], img[0,0,2]).
                # So we should check the same channel that was calibrated?
                # But here we just check packet[32][0]? 
                # If MSS returns BGRA, [0] is Blue.
                # If User's Night Shift turns screen yellow, Blue is low?
                # I will stick to the User's explicit code: packet[32][0].
                anchor_pixel_red = packet[32][0] # Red channel at index 32 (User specific)
                
                # [FIX] NOISE FILTER
                # Only trigger if the pixel is BRIGHT (meaning the Plater block is visible).
                # Backgrounds are ~50. Signals are 255.
                if int(anchor_pixel_red) > 150:
                    print(f"[PRIORITY] Lethal Anchor TRIGGERED ({anchor_pixel_red}) -> Firing Finisher")
                    bridge.send_pulse('e') # Use 'e' for Eviscerate
                
                # --- END CHECKS ---
                
            else:
                # Silent wait if not synced
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            print("\n[SHUTDOWN] User Interrupt.")
            sys.exit()
        except Exception:
            # Catch transient errors (e.g. window drag)
            continue

if __name__ == "__main__":
    main()
