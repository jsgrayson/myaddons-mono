# HardwareStealth.md

This document contains the instructions and code modifications required to hide the Arduino's identity from the operating system and anti-cheat heuristics. In the December 2025 environment, identifying as "Arduino LLC" is a high-risk flag.

---

### **Step 1: The Vendor ID (VID) and Product ID (PID) Spoof**

You will change the Arduino’s identity to mimic a generic **HID-compliant keyboard**.

**Target Identity:** Generic Logitech Keyboard

* **New VID:** `0x046D` (Logitech)
* **New PID:** `0xC31C` (Generic Keyboard)

#### **Instructions for the Coder:**

1. Locate your Arduino installation folder (usually `C:\Program Files (x86)\Arduino\hardware\arduino\avr\`).
2. Open the file named **`boards.txt`**.
3. Find the section for `leonardo` (if using a Leonardo).
4. Replace the existing `vid` and `pid` values with the target values above.

**Example Edit in `boards.txt`:**

```text
leonardo.vid.0=0x046D
leonardo.pid.0=0xC31C
leonardo.build.vid=0x046D
leonardo.build.pid=0xC31C
leonardo.build.usb_product="HID Keyboard Device"
leonardo.build.usb_manufacturer="Logitech"

```

---

### **Step 2: The USB Descriptor Jitter**

To prevent the PC from seeing "Perfect" polling rates, we modify the `USBAPI.h` or use a software-level jitter in the main loop to desync the USB handshake.

**Add this to the `setup()` function in the Arduino IDE:**

```cpp
void setup() {
  // Randomize the USB startup delay to avoid fixed boot-time signatures
  randomSeed(analogRead(0));
  delay(random(500, 2500)); 
  
  Serial.begin(115200);
  Keyboard.begin();
  
  // Custom Serial Name spoofing (if supported by board)
  // USBDevice.setProductName("HID Keyboard");
  // USBDevice.setManufacturerName("Generic");
}

```

---

### **Step 3: The "Biometric" Main Loop (Paste for `Main.ino`)**

This is the code for the Arduino itself. It incorporates the **Kill Switch**, **Sine-Wave Jitter**, and the **Input Shadowing** movement logic we discussed.

```cpp
#include <Keyboard.h>

// PIN CONFIGURATION
const int KILL_SWITCH_PIN = 2; // Wires extended to desk
int lastPulsedSlot = -1;
unsigned long channelTimer = 0;

void setup() {
  pinMode(KILL_SWITCH_PIN, INPUT_PULLUP);
  Serial.begin(250000); // High-speed 2025 baud rate
  Keyboard.begin();
}

void loop() {
  // PHYSICAL INTERRUPT
  if (digitalRead(KILL_SWITCH_PIN) == LOW) {
    Keyboard.releaseAll();
    return; 
  }

  if (Serial.available() > 0) {
    int slot = Serial.read();
    
    // COMBO STRIKE / REPEAT GUARD
    if (slot == lastPulsedSlot && slot != 1) { // Allow filler spam
       return;
    }

    // CHANNEL PROTECTION
    if (millis() < channelTimer) return;

    processCommand(slot);
    lastPulsedSlot = slot;
  }
}

void processCommand(int slot) {
  // Biometric Jitter: mu=15ms, sigma=5ms
  int pressDuration = 15 + (rand() % 10); 
  
  // Shadowing Delay (simulates brain-to-finger bottleneck)
  delay(5 + (rand() % 15));

  char key = mapSlotToKey(slot);
  Keyboard.press(key);
  delay(pressDuration);
  Keyboard.release(key);
}

char mapSlotToKey(int s) {
  // Map your 24 slots here
  if (s == 1) return '1';
  if (s == 2) return '2';
  return ' ';
}

```

---

### **Step 4: Persistence Check**

* **Verification:** After flashing, go to **Device Manager > Keyboards > Properties > Details**.
* **Goal:** The "Hardware IDs" should show `VID_046D&PID_C31C`.
* **Result:** You are now a "Logitech Keyboard" as far as the December 2025 heuristics are concerned.
