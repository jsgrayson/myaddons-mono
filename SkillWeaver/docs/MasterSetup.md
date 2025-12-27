# SkillWeaver Master Setup Guide (December 2025)

**Status:** ARCHIVED & READY FOR DEPLOYMENT.

This document consolidates all initialization steps for the **40x40 Master Matrix**, **Stealth Hardware**, and **Biometric Logic**.

---

## I. Hardware Assembly (The Physical Layer)

### 1. The Controller (Arduino Leonardo/Micro)
*   **Flash Firmware:** Upload `tools/arduino_hid_controller.ino`.
*   **Stealth Identification:** Edit `boards.txt` to spoof **Logitech VID/PID (`0x046D` / `0xC31C`)**. (Ref: `docs/HARDWARE_STEALTH.md`)

### 2. The Wiring (Safety & Utility)
*   **Pin 2 <-> GND:** **Kill Switch** (Toggle).
    *   *Function:* Instant Cutoff (Vanish Protocol).
*   **Pin 3 <-> GND:** **Medic Toggle** (Toggle).
    *   *Function:* Enables Slots 20-22 (Self/Group Healing).
    *   *OFF (Open):* Pure DPS Mode.
    *   *ON (Closed):* Life-Line Active.

---

## II. Software Installation (The Logic Layer)

### 1. The "Ghost" Addon
*   **Copy:** `ColorProfile_Lib` folder to `_retail_/Interface/AddOns/`.
*   **Verify:** In-game, ensure a tiny pixel strip appears in the bottom-left corner.

### 2. The Logic Engine
*   **Config:** Calibrate `logic_processor.py` to read the bottom-left pixel strip.
*   **Biometrics:** If you captured data, update the `humanDelay()` array in the Python/C++ code. If not, the **Gaussian Drift** default is active and safe.

---

## III. Operation Protocol (The "12.0 Meta" Flow)

1.  **Boot Phase:**
    *   Plug in Arduino (Switch 2 = OPEN/ACTIVE).
    *   Launch WoW (Windowed Borderless).
    *   Verify `ColorProfile_Lib` load.

2.  **Calibration:**
    *   Enter Instance.
    *   Check **Slot 25** (Environment Pixel):
        *   **Blue:** Raid
        *   **Green:** Delve
        *   **Red:** PvP

3.  **Deployment:**
    *   Run Python Script.
    *   **Toggle Pin 2 (Kill Switch):** System Live.

---

## IV. Emergency Codes (The "Oh Sh*t" List)

| Trigger | Indicator | Action |
| :--- | :--- | :--- |
| **Kill Switch (Pin 2)** | **(Physical)** | **Instant Halt** + `ESC` Pulse. |
| **CC / Stun** | **Yellow Pixel** | Arduino releases all keys. |
| **Mechanic / Gaze** | **Red Pixel** | Arduino halts casting. |

---

**"The system is perfect. The rest is up to the pilot."**
