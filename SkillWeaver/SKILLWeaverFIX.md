# SKILLWEAVER: MIDNIGHT ARCHITECTURE (V2.11 RESTORED)

> **STATUS:** RECOVERED
> **DATE:** Dec 18, 2025
> **CODENAME:** THE GOD-KILLER

## 🌌 Overview
This architecture replaces the hollow "Offline" shell with a high-performance, Hardware-in-the-Loop (HIL) combat engine known as **Midnight**. It bridges the gap between the game client (Lua), the decision engine (Python), and the input device (Arduino/Pro Micro).

---

## 🏛 The Trinity Architecture

### 1. 🧠 THE BRAIN (`SkillWeaver_Engine/Brain`)
The decision center. It processes visual data and determines the optimal next action.

*   **`LogicEngine.py` (V2.11)**: The main loop.
    *   **Input:** Reads 16-pixel RGB array from `Vision`.
    *   **Process:** Decodes Spec ID, Combat Status, and Resource Thresholds.
    *   **Output:** Sends "Chords" (e.g., `INTERRUPT`, `BURST`, `KEY_1`) to the `Bridge`.
    
*   **`modules/logic_engine.py` (Priority Hub)**:
    *   Refined `PriorityEngine` class.
    *   **Resolves Collisions:** Decides between `Late-Kick` (Priority 1), `Counter-Chord` (Priority 2), and `Rotation` (Priority 3).
    *   **Precognition:** Handles "Bait" sequences (Move-Cancel) to trick enemy interrupts.

*   **`modules/pvp_engine.py` (Combat Sim)**:
    *   Manages the **39x39 Matchup Matrix**.
    *   Executes "Wait-Your-Turn" logic for interrupts (Wait for 85% cast completion).

*   **`matrix.json` (The Registry)**:
    *   Maps **Spec IDs** (e.g., `62` Arms, `253` BM) to **Pixel Triggers**.
    *   Defines "Lethal CDs" (e.g., Bestial Wrath, Bladestorm) that trigger defensive reactions.

---

### 2. 👁️ THE EYES (`SkillWeaver_Engine/Brain/modules/vision.py`)
The sensory organ. It sees what the human eye sees, but faster.

*   **Technology:** `mss` (High-speed capture) + `numpy` (Array processing).
*   **The Chameleon Strip:** A 16x1 pixel row rendered by `Chameleon.lua` in-game.
    *   **Pixel 1:** Spec ID (0-255).
    *   **Pixel 2:** Combat/Target Status.
    *   **Pixel 6:** **Precognition Sensor** (Green = Precog Active).
*   **Grid Scanner:** (To Be Implemented) Scans party frames for "Smart-Heal" targeting.

---

### 3. 👆 THE FINGER (`SkillWeaver_Engine/Finger`)
The actuator. It mimics human physical input to bypass anti-cheat heuristics.

*   **`Omni_Executor.ino`**: C++ Firmware for Pro Micro.
    *   **Jitter Logic:** Adds 15-45ms random latency to every keypress.
    *   **Handshake:** Responds to `0xFF` with `0xAA` to verify hardware presence.
*   **`Keyboard_Map.h`**:
    *   Maps logical chords (`KEY_ST_ROTATION`) to hardware scan codes.
    *   Handles modifier chords (Shift+1, Ctrl+2).

---

## 🛠 Recovery Log (Session Dec 18)

We successfully restored the following deleted components:

1.  **Repo Cleanup:** Transitioned main addon to "Offline Mode" (removed legacy backend).
2.  **Engine Restoration:**
    *   Rebuilt `LogicEngine.py` (V2.11).
    *   Restored `matrix.json` with multi-spec data.
    *   Restored `vision.py` with `mss`/`cv2`.
    *   Restored `Omni_Executor.ino` with Jitter Logic.
    *   Refactored `logic_engine.py` for Priority Collision.

## 🔮 Next Steps
1.  **Healer Logic:** Restore `healer_scanner.py` (Grid Scanner).
2.  **WebUI:** Rebuild `GearOptimizer.tsx` (Stat Topology Lab).
3.  **Visualization:** Generate 3D Assets for Holocron OS.

> *The system is now "Armed". The Brain can see, think, and act.*
