# Parity Scorecards

This document operationalizes `ADDON_CONTRACTS.md` into trackable checklists.

**Hard rule:** each addon must be fully usable, configurable, and authorable **in-game** with **no backend/web**.  
Web features are strictly additive.

Legend: ✅ Done | 🟡 Partial | ❌ Missing

---

## DeepPockets (Bag replacement parity)

### Must-have parity (offline / in-game)
- ❌ B key opens DeepPockets reliably (no Blizzard bags)  
- ❌ No input leakage (clicking bag area never triggers Blizzard bag UI)  
- ❌ Shows all items reliably (no “empty UI” states)  
- ❌ Correct gold display (updates live)  
- ❌ Categories comparable to BetterBags (sane defaults, collapsible sections)  
- ❌ Search works and is focused on open  
- ❌ New item indication (glow/mark) with clear/expiry behavior  
- ❌ Options panel: enable/disable bag replacement, UI scale, layout density  
- ❌ Persistence: settings survive /reload; no destructive migrations  

### Nice-to-have parity (offline / in-game)
- ❌ Custom category rules / item pinning  
- ❌ Quick vendor/junk view  
- ❌ Keybinds beyond B (toggle, search focus, category collapse)  
- ❌ Per-character inventory snapshots (local)  

### Web-only enhancements (Holocron)
- ❌ Total value calculations  
- ❌ Cross-character totals + history  
- ❌ Links into Goblin pricing/filters  

---

## PetWeaver (Rematch + PetBattleScript parity)

### Must-have parity (offline / in-game)
- ❌ Team management UI (create/edit/delete)  
- ❌ Encounter detection + team selection  
- ❌ Script authoring/editing UI (PBS parity)  
- ❌ Import/export of teams/scripts (copy/paste)  
- ❌ Manual overrides during battles  
- ❌ Battle logging (local) + basic stats  
- ❌ Safe persistence + non-destructive migrations  

### Nice-to-have parity (offline / in-game)
- ❌ Strategy library tagging/search  
- ❌ Per-NPC winrate stats  
- ❌ More robust import formats (Wowhead-like text)  

### Web-only enhancements (Holocron)
- ❌ Strategy comparison/optimization  
- ❌ Aggregated stats across characters  
- ❌ Confidence warnings based on heuristics  

---

## SkillWeaver (Build editor parity)

### Must-have parity (offline / in-game)
- ❌ Rotation/sequence authoring in-game  
- ❌ Condition/toggle editing UI (or slash-driven editor)  
- ❌ Import/export of builds (Wowhead/guide parity)  
- ❌ Spec detection + correct module activation  
- ❌ Persistent configuration + safe migrations  
- ❌ Debug view of active rules/modules  

### Nice-to-have parity (offline / in-game)
- ❌ Profile management (per spec/content)  
- ❌ In-game testing sandbox mode  

### Web-only enhancements (Holocron)
- ❌ Visualization + comparisons  
- ❌ Build sharing + analysis  

---

## HolocronViewer (In-game hub)

### Must-have parity (offline / in-game)
- ❌ Opens and functions without backend  
- ❌ Displays locally available addon states (DP/PW/SW)  
- ❌ Does not block other addons’ input  
- ❌ Graceful degraded mode when backend absent  
- ❌ Minimal navigation + module toggles persist  

### Nice-to-have parity (offline / in-game)
- ❌ Unified “addon status” panel (local only)  
- ❌ Quick jump into addon config panels  

### Web-only enhancements
- ❌ None required (HolocronViewer is not the web UI)

---

## Issue Seeding

For every ❌ item above:
- create a GitHub Issue titled: “[Parity] <Addon>: <Item>”
- include acceptance criteria:
  - steps to verify in-game without backend
  - expected behavior
- label: parity
