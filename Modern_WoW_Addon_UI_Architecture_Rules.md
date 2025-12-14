# Modern WoW Addon UI – Architecture & Rules

Living document derived from the DeepPockets / BetterBags integration incident.
Purpose: prevent future UI catastrophes and establish stable patterns for all addons going forward.

⸻

## TL;DR (Non-Negotiable Rules)

1. **UI frameworks are immutable**
   * Do not partially fork, disable, or mock core UI modules.
   * If you adopt a UI addon (BetterBags, Rematch), you adopt it whole.
2. **Backend logic must live in backend addons**
   * No frames
   * No bindings
   * No secure actions
3. **Plugins > Forks**
   * Extend via APIs, callbacks, data providers.
   * Never rewrite UI unless Blizzard forces it.
4. **If an addon works today, do not touch its UI**
   * Build around it, not inside it.

⸻

## The Modern Reality of WoW Addons (Retail 10.x / 11.x)

### Addons Are Systems, Not Scripts

**Old mental model:**
> "An addon creates frames, binds keys, hooks events."

**Modern reality:**
* Blizzard UI is modularized
* Core systems are protected & template-driven
* Secure execution rules apply even to Lua

**Anything involving:**
* Bags
* Items
* Tooltips
* Context menus

...is no longer freely controllable.

⸻

## UI vs Backend: Hard Separation

### UI Addons (Danger Zone)

**Characteristics:**
* Frames, XML, templates
* Protected actions
* Secure handlers
* Patch-fragile

**Examples:**
* BetterBags
* Rematch
* Blizzard UI

**Rules:**
* Treat as black boxes
* Assume internal module dependencies
* Never disable submodules unless documented

⸻

### Backend Addons (Safe Zone)

**Characteristics:**
* Data collection
* Analysis
* Categorization
* Metadata

**Allowed:**
* SavedVariables
* Slash commands (non-secure)
* Events
* Hooks that do not execute actions

**Forbidden:**
* Frames
* Bindings.xml
* Secure calls

**DeepPockets (final form) belongs here.**

⸻

## Why the BetterBags Fork Failed

BetterBags is not "bags UI". It is:
* A framework
* A module graph
* A dependency web

**Key facts:**
* `GetModule()` is assumed everywhere
* ContextMenu, Anchor, Bag, Search are cross-linked
* Removing one breaks dozens of files

### Critical Lesson

**You cannot partially adopt a modern UI framework.**

Disabling modules is equivalent to deleting random engine parts.

⸻

## Bindings.xml Is a Loaded Gun

### Why Bindings Broke Everything
* Parsed before Lua
* Version-specific schema
* Zero tolerance for errors
* Global namespace collisions

**Observed failures:**
* "Unrecognized XML"
* Duplicate headers
* Silent misbehavior

### Rule

**Backend addons must never ship Bindings.xml**

If bindings are needed:
* Let the UI addon provide them
* Or register via secure Blizzard APIs only

⸻

## Protected Actions & Why You Cannot Fake Them

**Protected examples:**
* ToggleAllBags
* Item button clicks
* Tooltip ownership

**Why BetterBags works:**
* Uses Blizzard templates
* Lets Blizzard handle secure execution
* Decorates, not replaces

**Why custom UI broke:**
* Crossed protected boundaries manually

⸻

## The Correct Architecture (Validated)

### Final Pattern (This Is Canon)

**BetterBags**
* Rendering
* Interaction
* Security
* Compatibility (ConsolePort, Pawn, Masque)

**DeepPockets**
* Inventory scans
* Category logic
* Upgrade metadata
* Data export

**Relationship:**
* Plugin / provider
* Not fork

This matches:
* Pawn
* Rematch
* Blizzard-first addons

⸻

## ConsolePort & Tooltip Notes

**Observed issue:**
* Tooltips disappearing only with ConsolePort

**Likely cause:**
* Tooltip owner mismatch
* Secure frame interaction

**Important:**
* This is fixable via hooks
* Not via UI rewrites

**Action:**
* Investigate ConsolePort tooltip ownership handling

⸻

## Upgrade Scoring Strategy

**Facts:**
* BetterBags already integrates Pawn
* SkillWeaver already computes weights

**Correct approach:**
* Expose SkillWeaver weights as Pawn provider
* Let BetterBags consume Pawn normally

**Do not:**
* Re-implement upgrade UI
* Override item buttons

⸻

## What We Will Never Do Again
* Mock UI libraries
* Disable framework modules
* Rewrite secure UI paths
* Fork large UI addons without necessity
* Debug UI breakage blind

⸻

## What We Will Do Going Forward
* Backend-only logic addons
* Plugin-first mindset
* Minimal TOCs
* No XML unless mandatory
* Assume Blizzard security first

⸻

## Emotional Reality (Important)

The fear you felt was correct.

This was not a failure of skill.
It was a collision with undocumented complexity.

Now it’s mapped.

⸻

## Status
* **BetterBags**: stable
* **DeepPockets**: backend-only
* **Architecture**: sound
* **Future addons**: safer

This document should be referenced before any UI work.
