# Addon UI Strategy: Backend Core + UI Plugins

**Project Scope:** DeepPockets, PetWeaver, SkillWeaver, Goblin
**Architecture:** Headless "Brain" + Interchangeable "Face"

---

## 1. DeepPockets (The Inventory Brain)
- **Status:** Backend-Only (Implemented)
- **Role:** The single source of truth for "What do I have?", "Is it an upgrade?", and "Where does it go?".
- **Components:**
    - `DeepPockets.lua`: Memory state, standard inventory scan (C_Container), data persistence.
    - `dp_ext/`: Modules for API, Indexing, and Search.
- **Integration:**
    - **BetterBags:** DeepPockets acts as a *plugin* (`DeepPocketsBB_Categories` or direct integration). BetterBags handles 100% of the rendering and clicking.
    - **Other Addons:** DeepPockets exports a global `DeepPocketsAPI` table.

## 2. PetWeaver (The Pet Brain)
- **Status:** Planned Refactor
- **Role:** Pet collection analysis, team building logic, "best against X" calculations.
- **Strategy:**
    - **Backend:** `PetWeaver_Core`. Headless. Scans `C_PetJournal` and stores collection state. Runs algorithms.
    - **Frontend:** `PetWeaver_UI` or `Rematch` plugin.
    - **Rule:** Do not write a custom Pet Journal UI unless absolutely necessary. Integrating with Rematch is the "BetterBags" equivalent move here.

## 3. SkillWeaver (The Profession Brain)
- **Status:** Planned
- **Role:** Recipe tracking, craft queues, reagent calculations.
- **Strategy:**
    - **Backend:** `SkillWeaver_Core`. Scans `C_TradeSkillUI`.
    - **Frontend:** Lightweight window for "Queue" and "Reagents". Do not attempt to replace the main Profession Frame (it is complex and protected). **Overlay** or **Side-Panel** only.

## 4. Goblin (The Economy Brain)
- **Status:** Planned
- **Role:** Auction scanning, price history, sniping logic.
- **Strategy:**
    - **Backend:** `Goblin_Core`. Heavy data processing.
    - **Frontend:** Independent frame. *Exceptions apply:* Auction House UI is heavily protected. Goblin should mostly provide a separate "Dashboard" window rather than hooking the AH frame excessively.

---

## Summary of Rules for All Projects

1. **Separation of Concerns:**
   Every addon starts as a folder named `AddonName_Core`. If it needs a UI, that is a separate folder/addon (e.g., `AddonName_UI` or `AddonName_BetterBags`).

2. **No "God Addons":**
   DeepPockets does not know about Pet battles. PetWeaver does not scan bags. They communicate via APIs if needed (e.g., "Do I have this pet cage in my bags?").

3. **External Dependencies:**
   - **Ace3:** Standard library for Events, Comm, and basic Config UI.
   - **BetterBags:** Standard inventory host.
   - **Rematch:** Standard pet host (target integration).

4. **Testing Protocol:**
   - **Stage 1 (Backend):** Does `/dp dump` show the correct data? (No UI needed).
   - **Stage 2 (Integration):** Does the UI (BetterBags) reflect the backend data?
   - **Stage 3 (Combat):** Does it crash during a boss fight?
