# ColorProfile_Lib: Technical Documentation
**Codename:** Stealth-Pack "Ghost Protocol"
**Version:** 1.0.4

## Overview
`ColorProfile_Lib` is an obfuscated World of Warcraft addon designed to export "Calibration Data" (Game State) to the Python Logic Engine via visual pixel encoding. It masquerades as a UI color-correction utility.

## Pixel Grid Mapping
**Anchor:** Bottom-Left Screen (0,0) or User Configured.
**Cell Size:** 2x2 pixels.
**Spacing:** 0 pixels (Continuous Strip).

| Slot | Function | Logic Source | Use Case |
| :--- | :--- | :--- | :--- |
| **01-16** | **Core Rotation** | Legacy SkillWeaver | Standard Resources/Buffs |
| **17** | **Movement Vector** | Delve Logic | "Follow Brann" / "Dodge Hazard" |
| **21-23** | **Hero Talents** | 12.0 Meta | Proc Tracking |
| **24** | **Kill Signal** | Raid Mechanic | "Stop Casting" / "Freeze" |
| **25** | **Environment/Mode** | **Context Logic** | **The "Three Worlds" Switch** |

---

## Detailed Protocols

### Slot 25: The Environment & Safety Monitor
This single pixel dictates the **Strategy Mode** of the Arduino Controller.

| Color (RGB) | State | Arduino Behavior | Logic Triggers |
| :--- | :--- | :--- | :--- |
| **Yellow** `(1.0, 1.0, 0.0)` | **LOST CONTROL** | **RELEASE ALL** | CC, Stun, Fear, Hex. Hardware Lockout. |
| **Red** `(0.8, 0.1, 0.1)` | **PvP Mode** | **Anxiety Engine** | Bluff Casting, High-Jitter, Aggressive Interrupts. |
| **Green** `(0.1, 0.8, 0.1)` | **Delve Mode** | **Survival** | Prioritize Health Potions, Companion Sync. |
| **Blue** `(0.1, 0.1, 0.8)` | **Raid Mode** | **Throughput** | High-Uptime, Mechanic-Forced Instants. |
| **White** `(0.5, 0.5, 0.5)` | **World/Idle** | **Standard** | Generic 40/40 Rotation. |

### Slot 24: The Mechanic Kill-Switch
*   **Trigger:** DBM/BigWigs "Stop Casting" Event or "Eye Beam" Mechanic.
*   **Signal:** `(1.0, 0.0, 0.0)` (Pure Red).
*   **Action:** Arduino sends `ESC` immediately to halt casting.

---

## Deployment Instructions

1.  **Install:** Place the `ColorProfile_Lib` folder in `_retail_/Interface/AddOns/`.
2.  **Display:** Ensure WoW is in **Windowed Borderless** mode.
3.  **Calibration:** Verify that the Pixel Strip is visible in the bottom-left corner. It should look like a small, faint line of blocks.
4.  **Verification:**
    *   Enter an **Arena Skirmish** -> Slot 25 should turn **Red**.
    *   Enter a **Follower Dungeon** -> Slot 25 should turn **Green**.
    *   Get **Stunned** -> Slot 25 should flash **Yellow**.

## Security Notes
*   **Folder Name:** `ColorProfile_Lib` (Boring util name).
*   **LUA Structure:** Functions are named `UpdateCell` or `CalibrationLoop` to mask intent.
*   **Visual Footprint:** 2px high. Nearly invisible.

**Status:** GHOST PROTOCOL ACTIVE.
