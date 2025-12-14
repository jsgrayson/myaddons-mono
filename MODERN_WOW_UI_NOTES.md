# Modern WoW Addon UI Notes (Midnight-era) — “Don’t brick the UI again” Playbook

This is a **practical** set of notes to build UIs that don’t explode across patches, templates, and secure code rules.

---

## 0) The Lesson From DeepPockets

Most “it should be easy” addon UI failures come from **three traps**:

1) **Boot order / file layout / TOC drift**
- Wrong files load, wrong lib paths, wrong xml vs lua references, duplicate folders copied, stale deploy source.

2) **Protected actions & item interaction**
- “Use item”, “move item”, “bag toggle” are loaded with secure restrictions.
- If you try to call the wrong API in the wrong time/context, you get `ADDON_ACTION_FORBIDDEN`.

3) **Template mismatch**
- Blizzard templates evolve; a template expecting regions (IconBorder, Count, etc.) will error if your button/frame doesn’t have them.

**Takeaway:** Split responsibilities. Make UI “thin” and “safe”. Put logic/data elsewhere.

---

## 1) Architecture Pattern That Actually Works

### A) Backend Addon (yours)
**Goal:** Collect data, compute indices, expose APIs. **No** bag hooks. **No** bindings. **No** secure actions.

- SavedVariables: DB, cache, history, indexing.
- Provides:
  - `DP:ScanBags()`
  - `DP:GetIndex()`
  - `DP:OnUpdate(callback)` event bus (AceEvent or manual)
  - `DP:GetItemMeta(itemID)` (category, weight, etc.)

### B) UI Addon (either yours OR a fork you fully own)
**Goal:** Render UI + handle user interactions using safe calls and Blizzard-supported mixins/templates.

- Avoid direct “use item” APIs.
- Use Blizzard container/bag systems or item buttons that already know how to behave.

### C) Integration Addon(s)
**Goal:** Optional glue with BetterBags/Pawn/ConsolePort/etc.
- Detect addon presence.
- Register callbacks, categories, upgrade info, etc.
- Can be turned off independently.

**This “3 addon” approach prevents one failure from nuking everything.**

---

## 2) Boot Rules (TOC + Deploy) — Never Break These Again

### The only safe rules
- **One addon = one root TOC** in the deployed AddOns folder.
- Your deploy script must:
  - Block nested addon folders with their own TOC (except `Libs/` or known embedded libs).
  - Remove `* 2/`, `*_TRASH/`, `*DISABLED*`, `node_modules`, `examples`, `cache`, `release`, etc.
- Log what is deployed (print source path + git hash if possible).

### “Stale source” guard
- Your addon prints a loud banner on `ADDON_LOADED`, like:
  - `DeepPockets Backend LOADED v0.1.0 <hash>`
- If you don’t see it, you are not running what you think you’re running.

---

## 3) Modern Item Interaction: What You Can & Can’t Do

### Don’t do these (common footguns)
- Calling container APIs to “use” items from arbitrary code paths:
  - `UseContainerItem` is either deprecated, renamed, or protected depending on build.
- Trying to simulate clicks outside secure context.

### Do these instead
- Let Blizzard handle interaction by using correct button types:
  - Use item buttons that already implement click behavior through secure templates/mixins.
- For right-click context actions:
  - Use menus that are known-good (Blizzard dropdown / UIDropDownMenu) and load correct libs.
  - If you can’t ship the lib, **stub the feature** rather than leaving partial code that crashes.

**Rule:** If interaction needs “secure”, route it through a Blizzard-provided widget that already does it.

---

## 4) Templates & Regions: Why “IconBorder nil” Happens

If you call something like:
- `SetItemButtonQuality(button, quality)`
it expects your `button` to have fields/regions like:
- `button.IconBorder`, etc.

If your XML/template doesn’t create them, you get:
- `attempt to index field 'IconBorder' (a nil value)`

**Fix options:**
1) Use the exact template that defines these regions
2) Or don’t call those helpers; set only what you have
3) Or create the regions yourself

**Rule:** “If you didn’t create the region, don’t call helpers that assume it exists.”

---

## 5) Bags: Don’t Fight Blizzard, Don’t Fight BetterBags

### If BetterBags is working:
The best plan is **not** recreating the entire bag UI.

Instead:
- Keep BetterBags as the UI owner.
- Your addon becomes:
  - category provider
  - scoring/upgrade provider
  - indexing/search provider

### Recommended integration path
- Provide a “DP category classifier” API.
- Register DP categories into BetterBags if it supports category plugins.
- Provide “upgrade score” via Pawn-like interface OR a custom provider BetterBags can query.

**Rule:** Let BetterBags win the bag battle. You win the “intelligence layer”.

---

## 6) Bindings.xml: Why “Binding loaded twice / Unrecognized XML” Happened

Bindings are picky:
- Correct format varies by era/build.
- Duplicate headers or double-loading the same bindings file triggers warnings.

**Best approach:**
- If backend-only addon: **no Bindings.xml at all**.
- If you need bindings: keep them **in the UI addon**, not backend.
- If BetterBags already handles bindings: don’t duplicate.

---

## 7) Tooltips: “Owner nil” / disappearing tooltips

Even without ConsolePort, tooltip weirdness usually comes from:
- Tooltip owner not set (`GameTooltip:SetOwner(nil, ...)`)
- Tooltip hidden by competing UI layers
- Re-entrant show/hide calls during bag rebuild
- Frame recycling where OnEnter/OnLeave gets detached

**Hard rules for tooltip code**
- Always: `GameTooltip:SetOwner(self, "ANCHOR_RIGHT")` (or a consistent anchor)
- Always verify item is valid before setting tooltip content
- Never assume `self.itemData` exists in pooled buttons
- OnLeave must `GameTooltip:Hide()`
- If using pooling: OnAcquire/OnRelease must restore scripts

**Debug approach**
- Add a `/dp tt` command in UI addon only:
  - prints if tooltip is shown
  - prints current owner
  - prints last hovered item key

---

## 8) How We Build Future UIs (PetWeaver, SkillWeaver, Holocron, etc.)

### “Stable UI stack” checklist
- Use **mixins** / Blizzard widgets when possible
- Avoid custom XML if you can build frames in Lua (less schema break risk)
- Use one UI framework per addon (AceGUI OR custom frames), don’t half-mix

### Incremental rollout approach
1) Load-only phase (no UI created)
2) UI skeleton (frame opens, closes, no data)
3) Read-only rendering (lists display)
4) Interaction enabled (click, drag, context)
5) Integrations (Pawn, BB, etc.) last

**Rule:** Each phase must run with zero errors before next phase.

---

## 9) Action Plan We Should Follow Going Forward

### For DeepPockets (current state)
- Keep as backend companion.
- Keep BetterBags as UI owner.
- Add DP integration gradually:
  1) Category provider
  2) “upgrade score” provider (SkillWeaver weights -> Pawn-like)
  3) search/index enhancements
  4) optional UI panels later (not bag replacement)

### For “other addon UIs”
- Start with **one** framework and one load order.
- Write a “smoke test” command:
  - `/addon sanity`
  - prints loaded version, tables exist, no nil-critical fields

---

## 10) Non-negotiable Repo Cleanup Rules

- No `foo 2/` directories committed.
- No `*_TRASH/` in deploy path.
- One “deployable” addon folder per addon.
- Everything else goes under:
  - `tools/`, `dev/`, `docs/`, `scratch/` (and deploy excludes them)

---

## Appendix: What to log in every addon at startup

Print once:
- addon name + version + git hash
- build (retail/classic) if relevant
- whether integrations are detected (BetterBags, Pawn, ConsolePort, etc.)
- whether backend DB schema is valid

This single banner saves hours every time.
