"""
HardwareConfig.py - Multi-Hardware Profile System

Supports:
  - Mac M2 Pro (Retina)
  - MSI Claw 8 AI+ (Handheld 1080p/1200p)
  - Samsung 57" Odyssey Neo G9 (Dual 4K - Multiple layouts)
"""

import os
import time

# =============================================================================
# HARDWARE PROFILE DEFINITIONS
# =============================================================================

HARDWARE_PROFILES = {
    # MacBook M2 Pro with Retina display
    "MAC_M2_PRO": {
        "SCREEN_SCALE": 2,          # Retina 2x scaling
        "PIXEL_GAP": 1,
        "START_X": 0,
        "START_Y": 1116,            # Calibrated for Mac
        "SAMPLE_WIDTH": 128,
        "ANCHOR_COLOR": (255, 0, 255),
        "HID_SIGNATURE": [3, 2],    # Internal keyboard
        "DESCRIPTION": "MacBook M2 Pro Retina Display"
    },
    
    # MSI Claw 8 AI+ Handheld
    "MSI_CLAW_8_AI": {
        "SCREEN_SCALE": 1,          # Windows handles scaling
        "PIXEL_GAP": 1,
        "START_X": 5,
        "START_Y": 700,
        "SAMPLE_WIDTH": 128,
        "ANCHOR_COLOR": (255, 0, 255),
        "HID_SIGNATURE": None,      # USB HID
        "DESCRIPTION": "MSI Claw 8 AI+ Handheld"
    },
    
    # Samsung 57" - Centered Window (3840px window in middle)
    "SAMSUNG_57_CENTERED": {
        "SCREEN_SCALE": 1,
        "PIXEL_GAP": 2,
        "START_X": 1920,            # Left edge of centered 3840px window
        "START_Y": 20,
        "SAMPLE_WIDTH": 128,
        "ANCHOR_COLOR": (255, 0, 255),
        "HID_SIGNATURE": None,
        "DESCRIPTION": "Samsung 57\" - Centered Window"
    },
    
    # Samsung 57" - Right Half (Second virtual 4K)
    "SAMSUNG_57_RIGHT_HALF": {
        "SCREEN_SCALE": 1,
        "PIXEL_GAP": 2,
        "START_X": 3840,            # Start of right 4K panel
        "START_Y": 20,
        "SAMPLE_WIDTH": 128,
        "ANCHOR_COLOR": (255, 0, 255),
        "HID_SIGNATURE": None,
        "DESCRIPTION": "Samsung 57\" - Right Half (3840+)"
    },
    
    # Samsung 57" - Left Half
    "SAMSUNG_57_LEFT_HALF": {
        "SCREEN_SCALE": 1,
        "PIXEL_GAP": 2,
        "START_X": 0,
        "START_Y": 20,
        "SAMPLE_WIDTH": 128,
        "ANCHOR_COLOR": (255, 0, 255),
        "HID_SIGNATURE": None,
        "DESCRIPTION": "Samsung 57\" - Left Half"
    },
    
    # Samsung 57" - Full Screen
    "SAMSUNG_57_FULL": {
        "SCREEN_SCALE": 1,
        "PIXEL_GAP": 2,
        "START_X": 10,
        "START_Y": 10,
        "SAMPLE_WIDTH": 128,
        "ANCHOR_COLOR": (255, 0, 255),
        "HID_SIGNATURE": None,
        "DESCRIPTION": "Samsung 57\" - Full 7680px"
    },
    
    # Samsung 57" - PBP Mode (Picture-by-Picture as single 4K)
    "SAMSUNG_57_PBP": {
        "SCREEN_SCALE": 1,
        "PIXEL_GAP": 1,
        "START_X": 0,
        "START_Y": 20,
        "SAMPLE_WIDTH": 128,
        "ANCHOR_COLOR": (255, 0, 255),
        "HID_SIGNATURE": None,
        "DESCRIPTION": "Samsung 57\" - PBP Mode (Single 4K)"
    }
}

# CLI flag -> profile name mapping
PROFILE_FLAGS = {
    "--mac": "MAC_M2_PRO",
    "--msi": "MSI_CLAW_8_AI",
    "--center": "SAMSUNG_57_CENTERED",
    "--right": "SAMSUNG_57_RIGHT_HALF",
    "--left": "SAMSUNG_57_LEFT_HALF",
    "--full": "SAMSUNG_57_FULL",
    "--pbp": "SAMSUNG_57_PBP"
}

# Default profile
CURRENT_PROFILE = os.environ.get("SKILLWEAVER_PROFILE", "MAC_M2_PRO")


# =============================================================================
# PROFILE MANAGEMENT
# =============================================================================

def get_profile() -> dict:
    """Get the current hardware profile configuration."""
    return HARDWARE_PROFILES.get(CURRENT_PROFILE, HARDWARE_PROFILES["MAC_M2_PRO"])


def set_profile(profile_name: str) -> bool:
    """Set the active hardware profile."""
    global CURRENT_PROFILE
    if profile_name in HARDWARE_PROFILES:
        CURRENT_PROFILE = profile_name
        return True
    return False


def set_profile_from_flag(flag: str) -> bool:
    """Set profile from CLI flag (e.g., --right, --mac)."""
    profile = PROFILE_FLAGS.get(flag)
    if profile:
        return set_profile(profile)
    return False


# =============================================================================
# COORDINATE FUNCTIONS
# =============================================================================

def get_hardware_coords(pixel_index: int) -> tuple:
    """Get screen coordinates for a pixel index."""
    profile = get_profile()
    scale = profile["SCREEN_SCALE"]
    x = (profile["START_X"] + (pixel_index * profile["PIXEL_GAP"])) * scale
    y = profile["START_Y"] * scale
    return int(x), int(y)


def get_uplink_region() -> dict:
    """Get MSS-compatible region for uplink sampling."""
    profile = get_profile()
    scale = profile["SCREEN_SCALE"]
    return {
        "top": int(profile["START_Y"] * scale),
        "left": int(profile["START_X"] * scale),
        "width": profile["SAMPLE_WIDTH"],
        "height": 1
    }


# =============================================================================
# VISUAL ANCHOR CALIBRATION
# =============================================================================

def calibrate_to_window() -> tuple:
    """Find 'Magic Pink' anchor to locate game window."""
    profile = get_profile()
    anchor_color = profile["ANCHOR_COLOR"]
    
    try:
        import mss
        import numpy as np
        
        sct = mss.mss()
        scan_width = 7680 if "57" in CURRENT_PROFILE else 3840
        
        region = {"top": 0, "left": 0, "width": scan_width, "height": 100}
        screenshot = np.array(sct.grab(region))
        
        anchor_bgr = (anchor_color[2], anchor_color[1], anchor_color[0])
        
        for y in range(screenshot.shape[0]):
            for x in range(screenshot.shape[1]):
                if tuple(screenshot[y, x, :3]) == anchor_bgr:
                    print(f"[ANCHOR] Found at ({x}, {y})")
                    return x, y
        
        return 0, 0
    except Exception as e:
        print(f"[ANCHOR] Failed: {e}")
        return 0, 0


def print_profile_info():
    """Print current hardware profile."""
    profile = get_profile()
    print(f"╔{'═'*50}╗")
    print(f"║ Profile: {CURRENT_PROFILE:<40}║")
    print(f"║ {profile['DESCRIPTION']:<49}║")
    print(f"║ Scale: {profile['SCREEN_SCALE']}x | Origin: ({profile['START_X']}, {profile['START_Y']}){' '*15}║")
    print(f"╚{'═'*50}╝")
