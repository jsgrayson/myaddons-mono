# Claw & Arduino Guide: F13-F24 Key Bindings

## Overview
You use the **F13-F24** keys in WoW by mapping them to your gaming mouse buttons (like on MMO mice) or custom keyboards. They offer extra, non-conflicting keybinds.

However, you often need **AutoHotkey (AHK)** or your mouse software to make WoW recognize them, as Windows or WoW sometimes ignores them by default.

### The Standard Workflow
1.  **Configure in Software**: Bind your mouse buttons to F13-F24 in your device's utility (Synapse, G Hub, iCUE).
2.  **Verify in Windows**: Ensure the OS sees the keypress.
3.  **Bind in WoW**: Assign spells or macros to F13-F24 in the Keybindings menu.

---

## How to Use F13-F24 Keys

### 1. Identify Your Hardware
You're likely using an:
*   **MMO Mouse** (e.g., Razer Naga, Logitech G600).
*   **Programmable Keyboard** (e.g., Corsair, Razer) with extra macro keys (G1, G2, etc.).
*   **Arduino/Microcontroller** (Pro Micro) acting as a HID device.

### 2. Configure in Mouse/Keyboard Software
Open your device's utility software (e.g., Razer Synapse, Logitech G Hub, Corsair iCUE).
*   Map your mouse's extra buttons (often labeled G1, G2, etc.) to **F13, F14, F15... up to F24**.
*   *Note for Arduino Users:* Your Arduino sketch (`Omni_Executor.ino`) sends these raw HID codes directly.

### 3. AutoHotkey (AHK) Workaround
If WoW does not detect the F13-F24 press directly from your hardware driver, you may need an AutoHotkey script as a bridge.

**Example AHK Script:**
```autohotkey
; Maps Mouse Button 4 to F13
XButton1::F13
return

; Maps Mouse Button 5 to F14
XButton2::F14
return
```

### 4. Use in World of Warcraft
1.  Go to **WoW's Keybindings**.
2.  Assign spells or macros to **F13, F14, etc.**, just like you would F1-F12.
3.  SkillWeaver engines often rely on these "Hidden Keys" to trigger rotation actions without conflicts.
