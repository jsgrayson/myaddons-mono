import pyautogui
from modules.serial_link import SerialLink

def calibrate_dpi():
    """Surgical DPI Normalization using PyAutoGUI measurement."""
    serial = SerialLink()
    if not serial.connect():
        print("[ERROR] Serial Link not found for DPI Sync.")
        return

    print("\n🌌 SKILLWEAVER DPI NORMALIZATION 🌌")
    print("---------------------------------")
    print("DPI Calibration Starting... Do not move your mouse.")
    
    # 1. Get initial position
    start_x, start_y = pyautogui.position()
    
    # 2. Tell Pro Micro to move exactly 100 'units'
    # Using SIG_MOUSE_DELTA (0xF9) with dx=100, dy=0
    serial.write_mouse_delta(100, 0)
    time.sleep(0.12) # Wait for hardware execution
    
    # 3. Measure physical pixel movement
    end_x, end_y = pyautogui.position()
    actual_movement = end_x - start_x
    
    # 4. Calculate Ratio
    if actual_movement == 0:
        print("[CRITICAL] No movement detected. Check hardware connection.")
        return 1.0

    dpi_ratio = actual_movement / 100
    print(f"Calibration Complete. Your Pixel/HID Ratio is: {dpi_ratio}")
    
    # 5. Verify Y-axis (Human Jitter check)
    serial.write_mouse_delta(0, 100)
    time.sleep(0.12)
    v_end_x, v_end_y = pyautogui.position()
    y_delta = v_end_y - end_y
    y_ratio = y_delta / 100
    
    print(f"Y-Axis Ratio: {y_ratio}")
    print("---------------------------------")
    print("✓ DPI Sync Finalized.")
    serial.close()
    return dpi_ratio

def sync_dpi():
    """Calibrates the ratio between HID units and Screen Pixels."""
    serial = SerialLink()
    if not serial.connect():
        print("[ERROR] Serial Link not found for DPI Sync.")
        return

    print("\n--- DPI / SENSITIVITY CALIBRATION ---")
    print("1. Set your WoW cursor to the exact CENTER of the screen.")
    print("2. This test will move the cursor in a 400px square.")
    input("Press Enter to begin test...")

    # Square Move (400px)
    # Relative Max is 127 per packet
    for dx, dy in [(100, 0), (100, 0), (100, 0), (100, 0), # Right 400
                   (0, 100), (0, 100), (0, 100), (0, 100), # Down 400
                   (-100, 0), (-100, 0), (-100, 0), (-100, 0), # Left 400
                   (0, -100), (0, -100), (0, -100), (0, -100)]: # Up 400
        serial.write_mouse_delta(dx, dy)
        time.sleep(0.02) # Jitter control

    print("\n✓ Calibration Test Complete.")
    print("If the cursor landed back in the center, your DPI is 1:1.")
    print("If not, adjust your Windows Sensitivity until the square matches 400 pixels.")
    serial.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--sync":
        sync_dpi()
    else:
        calibrate()
