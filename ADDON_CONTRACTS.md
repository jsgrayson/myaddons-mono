# ADDON CONTRACTS & PARITY RULES

This document defines **non-negotiable architectural rules, addon boundaries, and parity guarantees** for the `myaddons-mono` repository.

It exists to prevent feature drift, backend coupling, and UX regression over time.

For actionable implementation tracking, see: **[PARITY_SCORECARDS.md](./PARITY_SCORECARDS.md)**

---

## NOTE
Addon-level behavioral guarantees and parity rules are defined in:
[ADDON_CONTRACTS.md](./ADDON_CONTRACTS.md)

Detailed implementation checklists and status tracking are in:
[PARITY_SCORECARDS.md](./PARITY_SCORECARDS.md)

---

## Core Principle (Hard Rule)

> **Every addon must be fully usable, configurable, and authorable in-game on its own, with NO backend or web dependency.  
> The web stack (Holocron + services) is strictly additive.**

If the backend is offline, disabled, or uninstalled:
- The addon must still operate **at least as well as the in-game addon it replaces**.
- No core functionality may require the web UI.

---

## In-Game vs Web Responsibility Split

### In-Game Addons
- Fast
- Reactive
- Tactical
- Authorable
- Offline-safe
- Minimal latency
- Blizzard-UI-compatible

### Web (Holocron)
- Analytical
- Comparative
- Cross-character
- Historical
- Confidence & verification
- Visualization & aggregation

**Web features may enhance, never replace, in-game input or control.**

---

## Addon Definitions & Contracts

### DeepPockets

**Purpose:**  
Replace the default bag UI with a modern, reliable inventory interface.

**Must work standalone (no backend):**
- Open with `B`
- Display all items reliably
- Correct gold display
- Categories (BetterBags-class parity)
- Search & filters
- New item indication
- UI scale & layout controls
- No input leakage to Blizzard bags

**Does NOT need in-game:**
- Deep analytics
- Historical trends
- Cross-character totals
- Market valuation

**Web enhancements (via Holocron):**
- Aggregated totals
- Value calculations
- History
- Cross-character views
- Links into Goblin

---

### PetWeaver

**Purpose:**  
Automate pet battles end-to-end.

**Must work standalone (no backend):**
- Encounter detection
- Team creation & selection
- Full script authoring/editing (PetBattleScript parity)
- Manual overrides
- Import/export of teams & scripts (Rematch/Wowhead-style)
- In-combat usability

**Web enhancements:**
- Strategy comparison
- Optimization
- Statistics & analysis
- Cross-character sharing

---

### SkillWeaver

**Purpose:**  
Advanced rotation and ability automation framework.

**Must work standalone (no backend):**
- Spec detection
- Rotation/sequence authoring
- Conditions & toggles
- Import/export of builds (Wowhead/guide parity)
- Persistent configuration

**Web enhancements:**
- Visualization
- Comparison
- Performance analysis
- Build sharing

---

### HolocronViewer (In-Game)

**Purpose:**  
In-game data hub and navigation layer.

**Rules:**
- Must open and function without backend
- Displays locally available data
- Never blocks other addons’ input paths
- Degrades gracefully if backend is unavailable

---

## Input Parity Requirement (Critical)

> **Every addon must provide full in-game input capabilities equivalent to the addon(s) it replaces.**

Examples:
- PetWeaver ≈ Rematch + PetBattleScript
- SkillWeaver ≈ Wowhead/guide build editors
- DeepPockets ≈ BetterBags-class bag addons

The web may mirror or enhance input, but **cannot be the only place input is possible**.

---

## Confidence & Verification

- Each addon emits `SANITY_RESULT` in-game
- Backend ingests and derives confidence
- Web UI displays confidence state
- Verification detects:
  - Broken states (FAIL)
  - Suspicious states (WARN)
  - Healthy states (OK)

Confidence is **advisory**, not blocking.

---

## Design Veto Rule

If a proposed change:
- Removes in-game input
- Forces the user to use the web
- Makes an addon unusable offline
- Couples core behavior to backend availability

➡️ **It is architecturally invalid.**

---

## Final Note

This document is a **reference, not a suggestion**.

When in doubt:
- Favor in-game autonomy
- Favor clear boundaries
- Favor additive web features
- Favor user trust over cleverness
