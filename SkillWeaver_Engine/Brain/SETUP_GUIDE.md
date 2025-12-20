# 🛠️ MSI CLAW: FIRST-RUN SETUP GUIDE (V1.1)

Follow these steps to ensure perfect alignment and stealth execution on your **MSI Claw 8ai+**.

---

## 1. VISION CALIBRATION (THE EYES)
The `VisionModule` is calibrated for a **1920x1080** display.
- **Raid Frames (The Grid):** Ensure your Raid Frames are positioned in the **lower-left** quadrant. Python scans the region `{"top": 600, "left": 50, "width": 400, "height": 600}`.
- **Nameplates (Plater):** Your target nameplate cast bar must be near the **center-screen**. Region: `{"top": 400, "left": 700, "width": 520, "height": 300}`.
- **Chameleon Strip:** This 16-pixel strip must be at the absolute **BOTTOM-LEFT** (`0, 0`). Do not overlap with other UI elements.

---

## 2. HARDWARE SYNC (THE FINGER)
- **Port Detection:** The `serial_link.py` will attempt to auto-detect your Pro Micro. Ensure it is connected via a high-speed USB-C cable.
- **XOR Handshake:** Upon starting `main.py`, the console should print `[SYNC] Hardware Handshake Verified (XOR)`. If it fails, check your XOR key (0x42).
- **Modifier Chords:** Test your **Shift+D** (Dispel) and **Ctrl+E** (External) binds in-game to ensure the Pro Micro is sending the modifiers correctly.

---

## 3. HEALER MODE ACTIVATION
The engine automatically pivots to Healer Mode when you log into:
- **Mistweaver (270)**
- **Resto Druid (105)**
- **Disc Priest (256)**
- **Resto Sham (264)**
- **Preservation (1468)**

In this mode, the **Grid Scanner** is active. Ensure "Dark Space" detection is enabled in Plater/RaidFrame settings for missing health.

---

## 4. STEALTH PROTOCOL
- **Capture-to-RAM:** No screenshots are saved to disk.
- **XOR Encryption:** All serial signals are obfuscated.
- **Biometric Jitter:** All delays are randomized between 12ms and 750ms.

---

## 5. FIRST RUN COMMAND
```bash
python3 SkillWeaver_Engine/Brain/main.py
```
*Look for the Cyan Pulse on the HUD confirming visual anchor detection.*
