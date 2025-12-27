# Hardware Stealth Guide (December 2025 Meta)

To prevent the Arduino from flagging as an "Arduino Leonardo" in the OS Device Manager, we must spoof its USB Identity to mimic a generic Logitech Keyboard.

## 1. Locate `boards.txt`

You need to edit the `boards.txt` file in your Arduino IDE installation.

### **Windows**
`C:\Program Files (x86)\Arduino\hardware\arduino\avr\boards.txt`

### **macOS**
Right-click `Arduino.app` in Applications -> Show Package Contents.
`Contents/Java/hardware/arduino/avr/boards.txt`
*(Path may vary slightly by version, look for `hardware/arduino/avr`)*

## 2. Edit the Identity

Find the section starting with `leonardo.name=Arduino Leonardo`.
Replace the `vid` and `pid` lines with the following **Logitech Stealth Values**:

```text
leonardo.vid.0=0x046D
leonardo.pid.0=0xC31C

leonardo.build.vid=0x046D
leonardo.build.pid=0xC31C
leonardo.build.usb_product="Generic HID Device"
leonardo.build.usb_manufacturer="Logitech"
```

## 3. Flash the Firmware

1.  Save `boards.txt`.
2.  Restart the Arduino IDE.
3.  Select **Arduino Leonardo** (It might show up with the new name or generic name).
4.  Upload the `arduino_hid_controller.ino` sketch.

## 4. Verification

*   **Windows:** Device Manager -> Keyboards. Look for "HID Keyboard Device" or "Logitech...". Check Hardware IDs in Properties.
*   **macOS:** Apple Menu -> System Report -> USB. Look for the Vendor ID `0x046D`.

> **CRITICAL:** Do this BEFORE playing on the main account.
