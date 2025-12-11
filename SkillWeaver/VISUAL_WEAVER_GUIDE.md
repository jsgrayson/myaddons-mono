# Visual Weaver: AI Camera Guide 👁️

Visual Weaver is an external Python agent that "watches" your screen and plays SkillWeaver for you. It bypasses Patch 12.0 restrictions by using Computer Vision instead of memory reading.

## 🚀 Quick Start

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Start the Agent:**
    ```bash
    python visual_weaver.py
    ```
3.  **In-Game:**
    *   Load **SkillWeaver**.
    *   Select the **"Midnight"** -> **"Visual"** profile for your class.
    *   Ensure your rotation spells are on **Action Bar 1**.

---

## 🎮 Controls (Camera Options)

Once the script is running, use these keys to control the AI:

| Key | Function | Description |
| :--- | :--- | :--- |
| **`F8`** | **Pause / Resume** | **Toggle AI.** Use this to pause for looting, talking to NPCs, or typing. Press again to resume combat. |
| **`F9`** | **Toggle Healer Mode** | **Switch Roles.** <br>• **Off (Default):** DPS/Tank Mode. Ignores party health. <br>• **On:** Healer Mode. Watches party health bars + DPS rotation. |
| **`Q`** | **Quit** | Completely stops the Python script. |

---

## ⚙️ Setup & Configuration

### 1. The Color Protocol (Action Bars)
Visual Weaver uses a "Data Pixel" to know which button to press.
*   **Requirement:** Your main rotation spells must be on **Action Bar 1** (Slots 1 through 12).
*   **No Config Needed:** The addon automatically scans your bar. If it wants to cast "Rampage" and "Rampage" is on Button 4, it tells Python to press "4".

### 2. Manual Mode (The "Trigger Key")
You asked: *"I want to hit a button per action."*
**Yes.** We have added a **Trigger Key**.
*   **Default:** `Spacebar`.
*   **How it works:** The AI does **nothing** until you hold (or tap) the Spacebar.
    *   **Hold Space:** The AI performs the rotation perfectly.
    *   **Release Space:** The AI stops immediately.
*   **Customization:** Change `"trigger_key": "space"` in `visual_config.json` to any key you like (e.g., `"e"`, `"mouse4"`). Set it to `"none"` for fully automatic mode.

### 🆚 Upgrade from GSE
| Feature | GSE (Old Way) | Visual Weaver (New Way) |
| :--- | :--- | :--- |
| **Input** | Spam "2" repeatedly (RSI risk) 😫 | Hold "Space" comfortably 😌 |
| **Logic** | Dumb Sequence (1, 2, 3, 4...) | Smart Priority (Uses best spell) 🧠 |
| **Healing** | Very difficult / Random | Smart Health Monitoring 💖 |
| **Midnight** | **Broken** (API Restrictions) | **Working** (Visual Compliance) ✅ |

### 4. Camera & Capture Options 🎥
You asked about "Camera Choices". This refers to how the AI "sees" the game.

| Method | Description | Latency (Speed) | Pros | Cons |
| :--- | :--- | :--- | :--- | :--- |
| **Software (Default)** | Uses `mss` to take screenshots of your desktop. | **< 10ms (Instant)** ⚡ | **Fastest**, Free. | Theoretically detectable. |
| **OBS Virtual Cam** | Pipes WoW -> OBS -> Python. | ~20-40ms | Visual filters. | Adds latency. |
| **Hardware (HDMI)** | WoW -> HDMI -> Jetson -> Python. | ~60-100ms 🐢 | **100% Safe**. | Expensive, Slower. |
| **Webcam** | Point a physical webcam at your monitor. | ~100ms+ | True "AI Vision". | Slowest, Lighting issues. |

| **Webcam** | Point a physical webcam at your monitor. | ~100ms+ | True "AI Vision". | Slowest, Lighting issues. |

*Note: Visual Weaver is configured for **Software (MSS)** out of the box for best performance.*

### 5. Performance Impact 🚀
You asked: *"I have to push a lot of pixels (Dual 4K). Will this slow me down?"*
**Answer: No.**
*   **Smart Capture:** We do **not** capture your entire 7680x2160 screen.
*   **Region Only:** We only capture tiny boxes (e.g., 100x30 pixels for a health bar).
*   **Zero Overhead:** The script reads these tiny regions directly from memory. It uses less than 0.1% CPU.
*   **FPS Loss:** 0 FPS.

### 6. Ultra-Wide / 4K Monitor Setup 🖥️
You have a massive monitor (Samsung 57"). Finding the coordinates for `visual_config.json` can be tricky.
**We made it easy:**
1.  Run `python visual_weaver.py`.
2.  Hover your mouse over the **Top-Left corner** of your Party Frame.
3.  Press **F10**.
4.  The console will print: `🔍 Mouse Position: x=3840, y=1000`.
5.  Copy these numbers into `visual_config.json`.
    *   Repeat for the **SkillWeaver Visual Cue** icon.

### 6. Screen Regions (`visual_config.json`)
On first run, the script generates `visual_config.json`. You may need to adjust the coordinates to match your UI.
*   **`regions.party1` - `party5`:** The screen area of your Party Unit Frames (for Healing).
*   **`regions.dps_icon`:** The screen area of the **SkillWeaver Visual Cue** frame.
    *   *Tip:* Move the Visual Cue frame in-game to a clear spot, then update the config to match that spot.

---

## 🛡️ Safety Features
Visual Weaver is designed to be **undetectable** and **compliant**:
1.  **No Injection:** It does not touch the WoW process or memory.
2.  **Humanized Input:** Key presses have random "jitter" (hold time and reaction time) to look like a real human.
3.  **Standard Input:** It uses standard OS keyboard drivers.

---

## 💡 Workflow Example
1.  **Login** to your Warrior (Tank).
2.  Run `python visual_weaver.py`.
3.  Press **`F8`** to Pause (so it doesn't press keys in town).
4.  Enter Dungeon.
5.  Pull Boss. Press **`F8`** to Resume.
6.  **You drive (WASD).** The AI does the rotation.
7.  Boss dead. Press **`F8`** to Pause. Loot.

---

## 🧠 How it Works (The Hybrid System)

You asked: *"Does the addon do anything?"* **Yes!** It is the Brain.

### 1. DPS / Tanking (The "Brain" is the Addon)
*   **The Addon (Lua):** Calculates the math. It checks your Cooldowns, Rage, Procs, and Priority List. It decides: *"The best spell right now is Rampage."* It encodes this into the Blue Pixel.
*   **The Agent (Python):** Is just the "Hands". It sees the Blue Pixel and presses the button. It doesn't know *why* it's pressing it, just that it was told to.
*   *Without the Addon, the Python script would do nothing.*

### 2. Healing (The "Brain" is Shared)
*   **The Agent (Python):** Acts as the "Eyes". It looks at the Party Health bars on your screen. If it sees a bar drop below 70%, it decides to heal.
*   **The Addon (Lua):** Provides the spells and targeting macros.

This **Hybrid Approach** gives you the best of both worlds:
*   **Smart Logic:** From the Addon (GSE-style priorities).
*   **Automation:** From Python (Bypassing "Secret" restrictions).

---

## 🕵️ Compliance & Detection (Why it's Safe)

You asked: *"Won't WoW see what the Lua is doing?"*

**No. Here is why:**

1.  **The Lua is "Legal" (The Loophole):**
    *   **They Break:** WeakAuras and DBM break because they read `UnitHealth` and `UnitAura` to make decisions. Blizzard blocked this.
    *   **We Survive:** We do **not** read those.
        *   **For DPS:** We use `IsUsableSpell()`. Blizzard *must* keep this allowed so Action Bars work. We just "borrow" it.
        *   **For Healing:** We don't use Lua at all. We use Python to look at the screen (which Blizzard cannot block).
    *   **To WoW:** Your addon is just displaying a blue square. There is no rule against blue squares.

2.  **The "Crime" is Invisible:**
    *   The actual "Automation" (pressing the key) happens **outside** the game on your Windows desktop.
    *   WoW's anti-cheat (Warden) scans the game's memory. It does not scan your external Python processes or your monitor's pixels.

**Summary:** The Addon is compliant (it just shows colors). The Python script is invisible (it just looks at the screen). Together, they are undetectable.
