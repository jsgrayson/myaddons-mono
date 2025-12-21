import os
import mss
import mss.tools
import cv2
import numpy as np

TARGET_DIR = "/Users/jgrayson/Documents/MyAddons-Mono"
TXT_FILE = os.path.join(TARGET_DIR, "debug_test.txt")
PNG_FILE = os.path.join(TARGET_DIR, "debug_mss.png")
CV2_FILE = os.path.join(TARGET_DIR, "debug_cv2.png")

print(f"--- DIAGNOSTIC START ---")
print(f"Target Directory: {TARGET_DIR}")

# 1. Test Text Write
try:
    with open(TXT_FILE, "w") as f:
        f.write("Hello from SkillWeaver Diagnostic.")
    print(f"[PASS] Text write successful: {TXT_FILE}")
except Exception as e:
    print(f"[FAIL] Text write failed: {e}")

# 2. Test MSS Capture & Save
try:
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 100, "height": 100}
        screenshot = sct.grab(monitor)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=PNG_FILE)
    print(f"[PASS] MSS Image write successful: {PNG_FILE}")
except Exception as e:
    print(f"[FAIL] MSS Image write failed: {e}")

# 3. Test CV2 Save (Fallback)
try:
    # Create a dummy image (100x100 Red)
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img[:] = (0, 0, 255) # BGR Red
    cv2.imwrite(CV2_FILE, img)
    print(f"[PASS] CV2 Image write successful: {CV2_FILE}")
except Exception as e:
    print(f"[FAIL] CV2 Image write failed: {e}")

print(f"--- DIAGNOSTIC END ---")
