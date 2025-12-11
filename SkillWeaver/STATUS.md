# SkillWeaver – Current Status & Planned Roadmap

## 📌 Current Status (as of 2025‑11‑20)

### ✅ Phase 1 – Core Utilities (Complete)
- **All 24 DPS specs** implemented with full rotations, utilities, and hero‑talent logic.
- **Pet Management** for Hunter, Warlock, Death Knight (including summons, taunts, health‑funnel, gnaw, etc.).
- **Consumables System** – healthstones always on, paid consumables toggle via minimap.
- **UI & Controls** – minimap button with dropdown, controller‑friendly keybinds, slash commands, macro support.
- **Documentation** – 9 comprehensive guides covering utilities, pet management, consumables, controller setup, macros.
- **Cross‑Spec Validation** – all rotations cross‑referenced against SimC APLs.

### ✅ Phase 2 – Foundations (In‑Progress)
- **Content Detection** – framework ready, awaiting final content‑type hooks.
- **Stat‑Weight Database** – static tables loaded, server‑side update optional.
- **Equipment Manager** – best‑in‑bags analysis, scoring algorithm, auto‑swap skeleton.
- **Brann Perk Helper** – perk database and UI integration added.
- **Feature‑Toggle System** – all modules can be enabled/disabled via Settings UI.

### ✅ Server‑Side (Optional) Components
- Crowd‑sourced intelligence, real‑time weight updates, ML optimization, Great Vault predictions, M+ route data, boss‑mechanic scripts.
- All optional – addon works fully offline.

---

## 📅 Planned Roadmap

| Timeframe | Phase | Goals | Key Features |
|-----------|-------|-------|--------------|
| **Immediate** | **Phase 1 – Core Utilities for 7 remaining specs** | Finish any missing utilities (cleanse, dispel, threat) for the last specs. | - Add `cleanse`/`dispel` logic.<br>- Threat generation & mitigation tweaks. |
| **This Week** | **Phase 2 – Cleanse, Dispel, Threat** | Polish core utilities across all specs, ensure threat tables are accurate. | - Implement `cleanse` spells for each class.<br>- Add `dispel` detection tokens.<br>- Refine threat generation in rotations. |
| **Next Week** | **Phase 3 – Racials, Pets, Battle Rez** | Add racial abilities, advanced pet controls, battle resurrection support. | - Racial ability wrappers (e.g., `Arcane Torrent`, `Blood Fury`).<br>- Advanced pet abilities (Soulstone, pet switching).
- Battle rez (e.g., `Rebirth`, `Revival`). |
| **Final** | **Phase 4 – QoL, Polish, Testing** | Final polish, extensive testing, UI/UX refinements, documentation updates. | - Settings persistence & per‑character profiles.
- Low‑stock consumable warnings.
- Full‑screen UI panel redesign.
- Automated test suite for rotations.
- Release candidate & user feedback loop. |

---

## ⚙️ Feature‑Toggle Overview (Light‑Weight Mode)

| Feature | Setting Key | Default | Server‑Side? |
|---------|-------------|---------|--------------|
| Content Detection | `enableContentDetection` | ✅ | No |
| Stat Optimizer | `enableStatOptimizer` | ✅ | No |
| Equipment Manager | `enableEquipmentManager` | ✅ | No |
| Talent System | `enableTalentSystem` | ✅ | No |
| Performance Tracker | `enablePerformanceTracker` | ✅ | No |
| Brann Perk Helper | `enableBrannHelper` | ✅ (only for M+/Raid) | No |
| Great Vault Optimizer | `enableGreatVault` | ❌ | ✅ |
| Boss Mechanic Helper | `enableBossHelper` | ❌ | ✅ |
| Voice Alerts | `enableVoiceAlerts` | ❌ | ✅ |
| Warband Transfer UI | `enableWarbandTransfer` | ✅ | No |
| WeakAuras Replacement | `enableWeakAuras` | ❌ | ✅ |
| M+ Route Planner | `enableMPlusPlanner` | ❌ | ✅ |
| Practice Mode | `enablePracticeMode` | ❌ | ✅ |

---

## 📂 Repository Structure (relevant files)
```
skillweaver/
├─ ADVANCED_OPTIMIZATIONS.md   # current dev notes
├─ STATUS.md                    # <‑‑ **this file**
├─ modules/
│   ├─ BrannHelper.lua
│   ├─ ContentDetector.lua
│   ├─ EquipmentManager.lua
│   └─ Settings.lua
├─ sequences/ (spec rotation files)
└─ docs/ (guides & manuals)
```

---

## 🚀 Next Steps
1. **Complete Phase 1 utilities** for the remaining 7 specs (cleanse/dispel/threat).  
2. **Mark Phase 2 tasks** as in‑progress in `task.md`.  
3. **Enable/disable features** via the Settings UI as needed for a lightweight experience.  
4. Begin **Phase 3** work on racials, pets, and battle rez once Phase 2 is solid.

*Feel free to adjust the timeline or add/remove items – the roadmap is flexible to match your development cadence.*
