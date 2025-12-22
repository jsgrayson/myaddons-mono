# SkillWeaver: The Hybrid Neural Interface
**Architectural Deep Dive & Technical Vision**

## 1. The Core Philosophy
SkillWeaver is not a bot. It is a **Cybernetic Enhancement Suite**.
Unlike traditional Lua unlockers (which modify game memory) or pixel bots (which are inaccurate), SkillWeaver uses a novel **Air-Gapped Hybrid Architecture**.

-   **The Game (WoW):** Thinks you are playing manually. It sees standard hardware keyboard events.
-   **The Addon (Lua):** Is completely passive. It makes no decisions. It simply "broadcasts" the game state via a cryptographically encoded strip of pixels.
-   **The Engine (Python):** Is the "Brain". It reads the screen, decides the rotation, and sends signals.
-   **The Hardware (Arduino):** Is the "Hands". It receives signals from Python and physically presses keys on the computer.

To the game's anti-cheat (Warden), this looks exactly like a user playing on a second monitor with a custom accessibility controller.

---


---

## 2. The Stealth Doctrine (Zero-Footprint)
To maintain the "Second Monitor Controller" illusion, the addon must be invisible to the user and the client's rendering pipeline.

### The Invisible Frame
-   **Size:** `32px x 1px`. The strip is microscopic.
-   **Strata:** `BACKGROUND`. It lives behind the WorldFrame, invisible to the naked eye.
-   **Location:** `BOTTOMLEFT (0,0)`. Hidden under chat windows or UI elements.

### Passive Transmission
Traditional bots "hook" memory or inject code. SkillWeaver does neither.
-   **No Events:** We do not trigger `SPELL_CAST_SUCCESS` listeners for logic.
-   **No Chat Spam:** All `print()` statements are purged.
-   **No Chat Spam:** All `print()` statements are purged.
-   **One-Way Valve:** Data flows OUT (via pixels). No data flows IN to the Lua environment. The Lua addon has no idea the Python engine exists.

### Case Study: The Kick Sensor (Pixel 20)
Is auto-kicking safe?
-   **Red Flag (Bannable):** Lua detects a cast and runs `CastSpellByName("Kick")`. This is automation.
-   **Green Flag (Safe):** Lua detects a cast and turns Pixel 20 White.
    -   This is identical to a **WeakAura** playing a sound.
    -   The **Python Brain** sees the white pixel and decides *if* it should press the F-Key.
    -   The **Arduino** presses the physical key.
    -   Result: The game sees a "Human" hardware press in response to a visual cue.

---

## 3. The Optical Uplink (The Protocol)
Data is transmitted from the Game Client to the Python Engine via light.

### The Problem: macOS Color Management
On macOS, `0.5` Red is not `128` Red. Because of Display-P3 and sRGB gamma correction (ColorSync), colors are shifted.
-   *Old Way:* Send R:100. Receive R:112. (Data Corruption).
-   *SkillWeaver Way:* **The Grayscale Luminance Protocol.**

We do not trust colors. We only trust **Brightness (Luminance)**.
Every data pixel is rendered as a shade of Gray (R=G=B).
-   `UnitPowerType` -> 3 (Energy)
-   Hash -> `(ClassID * 10) + SpecIndex`

### The Data Strip
A 1px high strip at the bottom-left of the screen.
-   **Pixel 0 (Handshake):** Pure White (255). Used to anchor the vision system.
-   **Pixel 1 (Spec Hash):** Identifies Class & Spec (e.g., Rogue Assa = Hash 41).
-   **Pixel 2 (Combat):** Binary On/Off.
-   **Pixel 7 (Power):** Energy/Mana/Rage %.
-   **Pixel 8 (Resources):** Combo Points/Holy Power/Runes.

---

## 3. The Vision Stack (The Eyes)
How does Python see the game?

### The Hybrid Engine
We typically face two problems:
1.  **PIL (Pillow):** Accurate but slow (20fps).
2.  **MSS:** Fast (100fps) but confused by Retina scaling.

**Solution:** Combining them.
1.  **Phase 1 (The Scout):** Use PIL to take a high-res screenshot and find the exact **Physical Y-Coordinate** of the White Handshake pixel.
2.  **Phase 2 (The Driver):** Switch to MSS. Pass it the coordinate.

### The Retina Problem
MacBook screens are High-DPI. A "1080p" screen actually has 2x the pixels physically density.
-   **Lua** paints logical pixel 1.
-   **Screen** displays physical pixels 1, 2, 3, 4 (a 2x2 block).
-   **Python** reads duplicates.

**The Fix:**
-   **Coordinate Math:** `Logical_Y = Physical_Y / 2`.
-   **The Index Shift:** On Retina, we don't read indices 0, 1, 2. We read indices **0, 2, 4** (Stride = 2).
-   **Current Map:** Spec is at Index 2. Energy is at Index 14. CP is at Index 16.

---

## 4. The Neural Core (The Brain)
`LogicEngine.py`

Once data is extracted:
1.  **Spec Recognition:** Reads Hash (41). Loads `259_assassination.json`.
2.  **State Reconstruction:** Updates internal variables (`energy=100`, `cp=5`).
3.  **Rotation Logic:**
    *   Iterates through the JSON priority queue.
    *   Checks conditions: `cp >= 5` AND `energy >= 50`.
    *   Finds first matching spell: `Envenom`.
4.  **Key Translation:**
    *   Lookups up key bind: `Envenom` -> `F16`.
    *   Translates to Hex: `F16` -> `0x04`.

---

## 5. The Hardware Bridge (The Hands)
We do not use `pyautogui` or virtual keys (detectable).
We use a **Pro Micro Arduino**.

### The Hex Protocol
Python talks to Arduino over Serial (USB). It sends a single **Raw Byte**.
-   `0x01` -> F13
-   `0x0C` -> F24
-   `0x0D` -> Shift+F13
-   ...
-   `0x30` -> Alt+F24 (Slot 48)

The Arduino firmware (`Omni_Executor.ino`) receives the byte and instantly fires the corresponding USB HID Keycode. The OS sees a physical keyboard press. 

---

## Summary
SkillWeaver is a **Color-Blind, Retina-Aware, Hardware-Emulated Combat Engine**. 
It turns World of Warcraft into a video input stream and your rotation into a hardware output stream, entirely bypassing the client's software inputs.
