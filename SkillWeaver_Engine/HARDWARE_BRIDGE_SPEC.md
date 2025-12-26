# SkillWeaver v6.0 // Hardware Bridge Specification

## 1. System Architecture

The pipeline consists of three distinct stages designed to isolate the software automation from the game client.

1. **Input Interception (Python)**: The engine hooks the `2` key at the OS kernel level using `keyboard.on_press_key(..., suppress=True)`. When you press `2`, the OS and Game do not see it. The event is swallowed by Python.

2. **Logic Processing (Python)**: Python analyzes the screen pixels (Health/Energy/ComboPoints) and determines the optimal move (Builder vs. Spender).

3. **Physical Execution (Arduino)**: Python sends a 1-byte instruction to the Arduino. The Arduino acts as a standard USB Keyboard (Logitech G-Pro spoof) and physically presses `F13` or `F16`.

---

## 2. The Communication Protocol

| Property | Value |
|----------|-------|
| Interface | USB Serial (COM Port) |
| Baud Rate | 250,000 (Ultra-low latency) |
| Data Packet | Single Byte (Hex) |

| Hex Code | Target Key | Logic Meaning |
|----------|------------|---------------|
| `0xF0` | F13 | Builder (Generate Resource/Combo Points) |
| `0xF3` | F16 | Spender (Finishers/High Cost Spells) |
| `0xBD` | N/A | Handshake (XOR Encrypted Keep-Alive) |

---

## 3. The Firmware (Arduino C++)

**Hardware**: Arduino Pro Micro (ATmega32U4) or Leonardo  
**Role**: Receives raw bytes and converts them into HID Keyboard strokes with humanized jitter.

```cpp
/* 
  SKILLWEAVER FIRMWARE v6.0
  TARGET: Arduino Pro Micro
  PROTOCOL: SERIAL @ 250,000 BAUD
  SPOOF TARGET: Logitech G-Pro Keyboard
*/

#include <Keyboard.h>

void setup() {
  // 1. Initialize Serial at High Speed
  Serial.begin(250000); 
  
  // 2. Initialize HID Emulation
  Keyboard.begin();
}

void loop() {
  // Non-blocking check for incoming data
  if (Serial.available() > 0) {
    byte incoming = Serial.read();
    
    // --- SECURITY HANDSHAKE (XOR) ---
    // Python sends a handshake byte to ensure sync.
    // 0xFF XOR 0x42 = 0xBD (189 decimal)
    if (incoming == (0xFF ^ 0x42)) { 
      // Acknowledge presence to clear Desync errors in Python
      Serial.print('K'); 
      return;
    }

    // --- EXECUTION ---
    // We treat the incoming byte directly as the char code.
    // Python sends 0xF0, Keyboard.press presses key 0xF0 (F13).
    Keyboard.press((char)incoming);
    
    // --- HUMANIZATION ---
    // Gaussian-style micro-jitter (15ms to 30ms hold time)
    delay(random(15, 30)); 
    
    Keyboard.release((char)incoming);
  }
}

/*
DEVICE FINGERPRINT (Flash via avrdude configuration):
BN: Logitech USB Input Device
VID: 0x046D
PID: 0xC31C
SN: HIDPC
*/
```

---

## 4. The Engine (Python)

**Role**: Intercepts user input, reads the screen (Vision), and sends commands to the firmware.

```python
# SKILLWEAVER ENGINE v6.0
# DEPENDENCIES: pip install mss pyserial keyboard numpy

import mss
import numpy as np
import time
import serial
import keyboard
from threading import Thread

# --- CONFIGURATION ---
SERIAL_PORT = 'COM3'   # Check Device Manager
BAUD_RATE = 250000     # Must match Arduino
RETINA_SCALE = 2       # 2 for Mac/High-DPI, 1 for 1080p

# --- KEY DEFINITIONS (HEX) ---
CMD_BUILD = b'\xF0' # F13
CMD_SPEND = b'\xF3' # F16

class HardwareBridge:
    def __init__(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01)
            time.sleep(2) # Allow Arduino to soft-reset
            print(f"[LINK] HARDWARE CONNECTED ON {SERIAL_PORT}")
        except:
            print("[CRITICAL] HARDWARE NOT FOUND. ENGINE HALTED.")
            self.ser = None

    def send(self, byte_code):
        if self.ser:
            self.ser.write(byte_code)

# Initialize Hardware
bot = HardwareBridge()

# --- VISION SYSTEM ---
def get_game_state():
    with mss.mss() as sct:
        # Define the 32x1 pixel strip area (Bottom Left)
        monitor = sct.monitors[1]
        region = {
            "top": monitor["height"] - 1, 
            "left": 0, 
            "width": 32, 
            "height": 1
        }
        
        # Grab Screen
        img = np.array(sct.grab(region))
        
        # Decode Pixel 8 (Secondary Resource - CP/Runes/HolyPower)
        # Lua Logic: SetPixel(8, val * 25)
        # Python Logic: val / 25
        p8_raw = img[0, 8][0] # Blue Channel
        secondary_resource = int(round(p8_raw / 25.0))
        
        return secondary_resource

# --- DECISION CORE ---
def decision_loop(event):
    """
    This function runs continuously while '2' is held, 
    OR once per press depending on preference.
    """
    
    # 1. READ
    combo_points = get_game_state()
    
    # 2. THINK
    # Example: Rogue Logic
    if combo_points >= 5:
        action = CMD_SPEND # Eviscerate (F16)
        debug = "SPEND (5 CP)"
    else:
        action = CMD_BUILD # Sinister Strike (F13)
        debug = f"BUILD ({combo_points} CP)"
        
    print(f"[LOGIC] {debug}")
    
    # 3. ACT
    bot.send(action)

# --- INPUT HOOK ---
# suppress=True prevents the Game from seeing the '2' key.
print("[SYSTEM] OPTICAL UPLINK ACTIVE. HOLD '2' TO ENGAGE.")
keyboard.on_press_key("2", decision_loop, suppress=True)

# Keep script alive
keyboard.wait()
```

---

## 5. Usage Instructions

1. **Flash Arduino**: Upload the C++ code to your Pro Micro.

2. **Bind WoW Keys**:
   - Bind Sinister Strike (or main builder) to `F13`
   - Bind Eviscerate (or main spender) to `F16`
   - *Note: WoW allows binding F13-F24 via addons or config edits*

3. **Run Python**: Execute the Python script as Administrator (required to hook keyboard).

4. **Play**:
   - Target an enemy
   - Press the physical `2` key on your actual keyboard
   - **Result**: Python intercepts `2`, checks your Combo Points, and instantly fires `F13` or `F16` via hardware to perform the optimal rotation.
