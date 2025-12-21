import mss
import numpy as np
from modules.vision import ScreenScanner

def debug_eyes():
    print("--- DEBUGGING EYES (PIXEL CHECK) ---")
    vision = ScreenScanner()
    
    # Coordinates from vision.py (Y=32 is the calibrated strip row)
    # We check X=32 (Lethal Anchor) and X=0 (Spec ID)
    targets = [
        (0, 32, "Spec ID"),
        (32, 32, "Lethal Anchor"),
        (6, 32, "Energy"),
        (8, 32, "Combo Points")
    ]
    
    with mss.mss() as sct:
        for x, y, label in targets:
            # Capture a tiny 1x1 pixel area
            monitor = {"top": y, "left": x, "width": 1, "height": 1}
            img = np.array(sct.grab(monitor))
            
            # Get the BGRA color values
            # mss returns [Blue, Green, Red, Alpha]
            pixel = img[0][0]
            blue, green, red, alpha = pixel[0], pixel[1], pixel[2], pixel[3]
            
            print(f"[{label}] at ({x}, {y}) -> BGRA: {pixel} | Red: {red}")

if __name__ == "__main__":
    debug_eyes()
