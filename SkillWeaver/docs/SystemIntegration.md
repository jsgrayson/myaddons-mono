# System Integration Protocol (December 2025 Meta)

This document defines the communication standard between the **Python Logic Engine** (The Brain) and the **Arduino HID Controller** (The Hands).

---

## 1. The Data Packet Protocol (Serial)

To handle the high-speed requirements of the 12.0 Meta, we use **Single-Byte Command IDs**. This minimizes serial latency to <1ms.

| Hex Code | Command Type | Description |
| :--- | :--- | :--- |
| `0x01` - `0x18` | **Cast Slot** | Triggers standard rotation slots 1-24. |
| `0x19` | **Hold Start** | Begins an Empowered Cast (e.g., Fire Breath). |
| `0x1A` | **Hold Release** | Releases an Empowered Cast. |
| `0x1B` | **Bluff Bait** | Triggers the "Anxiety Engine" (Cast + Random Cancel). |
| `0x1C` | **Biometric Pulse** | Triggers a "Drift" movement tap (Humanized Strafe). |
| `0x52` ('R') | **Set Mode: Raid** | Switches Context to Raid (Instant Priority). |
| `0x56` ('V') | **Set Mode: Delve** | Switches Context to Delve (Survival Priority). |
| `0x50` ('P') | **Set Mode: PvP** | Switches Context to PvP (Anxiety Engine Active). |
| `0x00` | **Heartbeat** | Null byte for connection health checks. |

---

## 2. Pixel-Reader Calibration

The Python Vision Module must be calibrated to the specific screen region of your 24-slot "Signal Bar".

*   **Scan Frequency:** 60 FPS (16.6ms per frame).
*   **Target Region:** Improved reliability at **Bottom-Left** or **Top-Left** (avoiding 3D world render overlap).
*   **Logic:**
    1.  Capture Region `(x, y, w, h)`.
    2.  Read Pixel #1 Color.
    3.  If Color == `CHAOS_BOLT_HEX` -> Send `0x04` to Arduino.

---

## 3. Biometric Signature Implementation

Once the **Capture Script** data is processed, the generic `delay()` in the firmware will be replaced by a weighted distribution function.

```cpp
void humanDelay() {
  // This uses your actual recorded playstyle data
  int myDelays[] = { /* INSERT DATA HERE */ }; 
  int randomIndex = rand() % (sizeof(myDelays) / sizeof(myDelays[0]));
  delay(myDelays[randomIndex]);
}
```

---

## 4. Final Wiring & Assembly

1.  **Mount the Switch:** Secure the physical Kill Switch in a housing (3D-printed or chassis-mounted).
2.  **Extended Leads:** Use **Shielded Twisted Pair** wire to run from the switch to the PC's rear I/O area.
3.  **Strain Relief:** Zip-tie the USB and Switch cables to the PC case handle or cable management loops to prevent port damage.

### **The "Live" Test Protocol**

1.  **Plug in** the Arduino (flashed with Stealth Firmware).
2.  **Open Notepad** on the PC.
3.  **Run** the Logic Engine (targeting a Dummy).
4.  **Verify:** The Arduino should "type" the rotation keys into Notepad with a natural, human-like rhythm (no robotic perfect spacing).

---

**Status:** READY FOR BOOT.
**Meta:** 12.0 Compliant.
