This document outlines the **"Silent Analog Bridge"** architecture for your repository. It defines how to use a **Razer Tartarus Pro** or **Azeron** as a dedicated hardware trigger for an **Arduino** while ensuring **World of Warcraft** remains completely unaware of the input.

---

## Project Overview: The Silent Analog Bridge

This system intercepts **Raw HID** data from an analog keypad. By "muting" the button in the device's native software and reading the hardware state directly via Python, we create a signal path that bypasses the Windows keyboard/controller stream entirely.

### 1. The Logic Flow

* **Movement/Analog:** Device  Driver  WoW (Normal behavior).
* **The Trigger:** Device  **Python (Raw HID)**  **Arduino**  Hardware.
* **The Hide:** Device Software (Synapse/Azeron) set to **"Unassigned"** for that button  Windows/WoW see **nothing**.

---

## 2. Hardware Diagnostic (Identify your Button)

To "grab" the button, you must find its specific index in the device's data packet. Run this script to identify your device's **VID/PID** and the **Data Byte**.

```python
import hid

# Identify all connected HID devices
for device in hid.enumerate():
    print(f"Device: {device['product_string']}, VID: {hex(device['vendor_id'])}, PID: {hex(device['product_id'])}")

# Manual Configuration: Replace with your IDs from the list above
# Common: Razer (0x1532), Azeron (0x16c0)
VENDOR_ID = 0x16C0 
PRODUCT_ID = 0x05DF 

device = hid.device()
device.open(VENDOR_ID, PRODUCT_ID)

print("Diagnostic Mode: Press the button you want to hide/grab...")
try:
    while True:
        report = device.read(64)
        if report:
            # This prints the raw array. Watch which number changes when you press.
            print(f"Raw HID Report: {list(report)}")
except KeyboardInterrupt:
    device.close()

```

---

## 3. The Python Bridge (`bridge.py`)

This script stays open in the background. It snatches the raw byte and pings the Arduino.

```python
import hid
import serial

# CONFIGURATION
VID = 0x16C0
PID = 0x05DF
ARDUINO_COM = 'COM3' 
BYTE_INDEX = 5    # The position in the report array (found in Step 2)
TRIGGER_VAL = 128 # The value sent when pressed

ser = serial.Serial(ARDUINO_COM, 115200)
dev = hid.device()
dev.open(VID, PID)

print("Bridge Active. Monitoring Analog Pad...")

while True:
    report = dev.read(64)
    if report and report[BYTE_INDEX] == TRIGGER_VAL:
        ser.write(b'1')

```

---

## 4. The Arduino Implementation (`trigger.ino`)

The Arduino side is built for **zero-latency** reception of the high-speed spam.

```cpp
void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    if (Serial.read() == '1') {
      // TRIGGER ACTION
      digitalWrite(LED_BUILTIN, HIGH);
    }
  }
  
  // Non-blocking reset (30ms pulse)
  static unsigned long lastOff = 0;
  if (millis() - lastOff > 30) {
    digitalWrite(LED_BUILTIN, LOW);
    lastOff = millis();
  }
}

```

---

## Summary of the "Hide" Mechanism

* **Driver Layer:** You must set the button to **"Disabled"** or **"Unassigned"** in Razer Synapse or the Azeron software.
* **Result:** Windows stops generating **KeyboardEvents** or **XInput** events for that button. WoW's engine sees a completely idle input stream.
* **The Exploit:** Python reads the **HID Report** directly from the hardware buffer. The physical state of the button is still sent to the USB port, even if the software chooses to ignore it.

---

**Would you like me to generate a `requirements.txt` and a `README.md` file for this repo to explain the setup to others?**
