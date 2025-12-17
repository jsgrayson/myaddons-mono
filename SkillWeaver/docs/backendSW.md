# SkillWeaver Backend Architecture

The addon is built to run fully offline (TWW pack) and, when the backend is present, consume backend-provided data as the source of truth for Midnight (and optionally for TWW too).

This matches the modular engine + DB layer + external sync layer architecture, including scraper, desktop sync client, and SavedVariables updater.

## Addon-side Contract
*What the backend must "feed"*

### Ruleset Switch
*   `ruleset="TWW"`: Offline defaults + optional backend override.
*   `ruleset="MIDNIGHT"`: Backend rotations/builds only.

### Keyed By
*   `CLASS_SPECID` (e.g., `DRUID_105`)
*   `mode`: `Delves` | `MythicPlus` | `Raid` | `PvP` | `OpenWorld` | `Midnight`
*   `profile`: `Balanced` | `HighPerformance` | `Safe` (and any extra)

### Normalized Rotation Format
*   `rotation.ST.steps` / `rotation.AOE.steps`: Each step `{command, conditions?}`.
*   `rotation.INT.macro` / `rotation.UTIL.macro`: Raw macro text.
*   *(Optional)* Allow `rotation.ST.macro` to bypass steps entirely.

Matches the "deterministic macro engine + multi-mode + Balanced/HighPerf + proc-aware/conditional evaluation" vision.

---

## Backend Feature List
*(Midnight-focused, but reusable for TWW)*

### A) Data Acquisition (Scraper Layer)
1.  **Rotation scraping/parsing**
    *   **Sources**: Wowhead, Icy Veins, Method.
    *   **Extract**: Priority lists (ST/AOE), cooldown windows, opener notes.
2.  **Talent import strings**
    *   Wowhead import strings per spec + per mode.
3.  **PvP talents per spec + mode**
    *   Arena/BG variants.
4.  **Hero talent trees**
    *   Per spec (and optionally per mode).

### B) Normalization + Compilation (The "Brains")
5.  **Normalize all sources into one schema**
    *   ST/AOE/INT/UTIL, plus metadata and versioning.
6.  **Generate 5 mode bundles per spec**
    *   `Delves`, `MythicPlus`, `Raid` (ST/Cleave), `PvP`, `OpenWorld`.
7.  **Generate 3 profiles per mode**
    *   `Balanced`, `HighPerformance`, `Safe`.
8.  **Optional "style knobs"**
    *   Cooldown toggle behavior (send cooldowns early vs hold).
    *   Defensives integration level (aggressive vs conservative).
9.  **Validation**
    *   Spell existence by class/spec.
    *   Illegal macro tokens check.
    *   Missing-talent warnings.

### C) Update + Delivery (Sync Layer)
10. **Versioning + metadata**
    *   `build_id`, `game_version`, `updated_at`, `source`, `confidence`.
11. **Weekly refresh automation**
    *   cron/scheduler, containerized scraper.
12. **Desktop sync client**
    *   Writes/updates WoW SavedVariables file(s).
13. **SavedVariables updater format**
    *   Outputs a single `SkillWeaver_Backend.lua` SavedVariables payload:
        *   `meta.connected = true/false`
        *   `meta.ruleset = "MIDNIGHT"` or `"TWW"`
        *   `rotations[spec][ruleset][mode][profile] = rotation`
        *   `builds[spec][ruleset][mode] = {talents, pvpTalents, heroTalents, notes}`

### D) Web UI Support
14. **Talent + PvP talent suggestions tab**
15. **Per-mode build viewer**
16. **Export buttons**
    *   Copy Wowhead strings, "controller preset" notes, etc.

---

## What the Addon Will Do
*   If backend says `ruleset="MIDNIGHT"` → Addon uses backend rotations/builds for Midnight.
*   If backend is missing/unavailable → Addon falls back to offline TWW pack automatically.
*   Same UI/engine everywhere; only the data source changes.
