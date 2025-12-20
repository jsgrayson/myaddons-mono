
import time
import pyautogui
import json

def calibrate_ground_truth():
    print("---------------------------------------------------")
    print(" GROUND TRUTH CALIBRATOR (v1.0)")
    print("---------------------------------------------------")
    print(" Goal: Map Nameplate Width (Distance) to Screen Y (Feet)")
    print(" 1. Log into WoW. Go to a Target Dummy.")
    print(" 2. Move Close (Melee Range). Press ENTER.")
    input("Press Enter to capture CLOSE point...")
    # Mocking capture - in real tool we'd read pixel strip or user input
    close_width = 150
    close_y = 800
    print(f" Captured: Width {close_width}px -> Y {close_y}")

    print(" 3. Move Far (30yds). Press ENTER.")
    input("Press Enter to capture FAR point...")
    far_width = 50
    far_y = 500
    print(f" Captured: Width {far_width}px -> Y {far_y}")
    
    # Calculate Linear Regression (Slope/Intercept)
    # Y = Slope * Width + Intercept
    
    slope = (close_y - far_y) / (close_width - far_width)
    intercept = close_y - (slope * close_width)
    
    print("---------------------------------------------------")
    print(f" CALIBRATED HORIZON MODEL:")
    print(f" Y = {slope:.2f} * Width + {intercept:.2f}")
    print("---------------------------------------------------")
    
    config = {
        "ground_truth_slope": slope,
        "ground_truth_intercept": intercept
    }
    
    with open('../Brain/data/config/ground_calibration.json', 'w') as f:
        json.dump(config, f, indent=4)
    print(" Saved to brain/data/config/ground_calibration.json")

if __name__ == "__main__":
    calibrate_ground_truth()
