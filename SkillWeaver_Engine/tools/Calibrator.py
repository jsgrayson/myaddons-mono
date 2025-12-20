import pyautogui
import json

def calibrate_anchors():
    print("Move mouse to Top-Left of Chameleon Strip and press ENTER")
    input()
    tl = pyautogui.position()
    
    print("Move mouse to Bottom-Right of Chameleon Strip and press ENTER")
    input()
    br = pyautogui.position()
    
    config = {
        "anchor_tl": [tl.x, tl.y],
        "anchor_br": [br.x, br.y],
        "pixel_size": (br.x - tl.x) / 16,
        "resolution": list(pyautogui.size())
    }
    
    with open('brain/config/anchors.json', 'w') as f:
        json.dump(config, f)
    print("CALIBRATION COMPLETE: Anchors saved to brain/config/anchors.json")

if __name__ == "__main__":
    calibrate_anchors()
