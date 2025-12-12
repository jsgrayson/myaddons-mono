GOBLIN_PLAN.md
================

Goblin — In-Game Economy & Crafting System
(Offline-First, TSM-Outcome Compatible, TSM-Design Rejected)

------------------------------------------------------------
CORE PHILOSOPHY
------------------------------------------------------------

Goblin exists to achieve the *same outcomes* as TSM:
- restocking
- crafting
- material planning
- destroying
- auctioning
- mailing
- accounting

WITHOUT copying:
- groups + subgroup inheritance
- opaque operations
- config-heavy indirection

Goblin is **workflow + queue driven**, not group driven.

------------------------------------------------------------
OFFLINE-FIRST RULE (HARD)
------------------------------------------------------------

Goblin MUST:
- function fully in-game with no backend
- scan inventory itself
- generate all queues locally
- never depend on Holocron for live decisions

Holocron MAY:
- store snapshots
- aggregate across characters
- provide history & suggestions
- enhance Goblin when available

Goblin is authoritative in-game.
Holocron is memory, not control.

------------------------------------------------------------
DATA OWNERSHIP
------------------------------------------------------------

Goblin owns:
- live inventory totals (bags/bank/reagent)
- craft queues
- subcraft dependency graph
- material lists
- execution queues (destroy/mail/post)

Holocron owns:
- inventory history
- mail history
- auction history
- craft accounting

------------------------------------------------------------
CORE CONCEPTS (REPLACES TSM GROUPS)
------------------------------------------------------------

### Workflows
A workflow represents a GOAL, not a category.

Examples:
- Restock Raid Consumables
- Craft for Profit
- Leveling Supplies
- Liquidate Old Mats

A workflow defines:
- inputs (items / recipes)
- targets (stock levels, budgets)
- scope (character, bags/bank)
- outputs (queues)

Workflows generate queues.
Queues are what the player executes.

------------------------------------------------------------
QUEUES (THE PRIMARY UI OBJECT)
------------------------------------------------------------

Goblin produces and manages these queues:

- Craft Queue
- Material List (Need / Have / Short)
- Buy List
- Post Queue
- Cancel Queue
- Mail Queue
- Destroy Queue

All queues:
- are reviewable before execution
- are deterministic
- can be rebuilt at any time
- survive reloads

------------------------------------------------------------
CRAFTING SYSTEM (FOUNDATIONAL)
------------------------------------------------------------

Crafting includes:
- craft queue
- subcraft expansion
- dependency cycle detection
- material list computation

Subcraft expansion is automatic by default.
Manual override is always allowed.

------------------------------------------------------------
DESTROYING
------------------------------------------------------------

Destroying includes:
- disenchant
- prospect
- mill
- scrap

Destroying is:
- explicit
- queue-based
- throttled
- never automatic without confirmation

------------------------------------------------------------
AUCTIONING
------------------------------------------------------------

Auctioning is queue-driven:
- Post Queue
- Cancel Queue

Goblin:
- prepares actions
- fills auction UI
- respects throttling
- never hides what it is about to do

------------------------------------------------------------
MAILING
------------------------------------------------------------

Mailing is queue-driven:
- send items to alts
- send mats to crafters
- send sale items to banker

Always reviewable.
Never blind "send all".

------------------------------------------------------------
INVENTORY SCANNING RULE
------------------------------------------------------------

Goblin scans inventory independently of DeepPockets.

- DeepPockets scans slots for UI
- Goblin scans totals for planning

No live data sharing between addons.
Schemas may be shared for sync only.

------------------------------------------------------------
PHASED IMPLEMENTATION
------------------------------------------------------------

G1C — Craft Queue + Subcraft + Material List
G1D — Workflows + Restock Targets + Shopping List
G2  — Destroy Queue MVP
G3  — Mail Queue MVP
G4  — Auction Post/Cancel MVP
G5  — Accounting + History (Holocron-heavy)

------------------------------------------------------------
NON-GOALS
------------------------------------------------------------

Goblin will NOT:
- copy TSM group/operation design
- require backend to function
- auto-execute destructive actions
- optimize before correctness

------------------------------------------------------------
SUCCESS CRITERIA
------------------------------------------------------------

Goblin is successful when:
- it can replace TSM for the author
- queues are understandable
- decisions are explainable
- nothing breaks when offline

------------------------------------------------------------
G1C CRAFT QUEUE INVARIANTS (MUST ALWAYS HOLD)
------------------------------------------------------------

These invariants define "correct" behavior for G1C. If any fail, treat as a bug.

### Queue invariants
- Queue quantities are always integers >= 0.
- Deduplication is deterministic:
  - identical recipe nodes merge quantities (no duplicate entries for same recipe at same depth).
- Parent-child relationships never form a cycle.
- Subcraft expansion must terminate:
  - visited-set prevents recursion loops
  - depth cap prevents runaway graphs

### Recipe graph invariants
- links[recipeId] contains:
  - outputItemId (or nil if unavailable)
  - outputQty (>=1 when available)
  - reagents[] where each reagent has itemId and qty>=1
- Missing/unavailable recipe info must never crash:
  - the system skips and records a warning instead.

### Materials invariants
- Materials list is derived from the expanded queue only (never ad-hoc scanning).
- For every material itemId:
  - short = max(need - have, 0)
  - have defaults to 0 when inventory unknown
- If auto-subcraft is ON:
  - craftable reagents are represented by subcraft nodes rather than remaining as base mats (unless recipe data missing)

### Inventory invariants
- Goblin inventory snapshot is independent from DeepPockets.
- Scans are event-driven only (no OnUpdate loops).
- Bank counts are only trusted when bank is open; otherwise bank may be 0/unknown but must not crash.

### Safety invariant
- Unknown/malformed steps never crash the addon; they degrade with warnings.

------------------------------------------------------------
G1C IN-GAME TEST SCRIPT (COPY/PASTE CHECKLIST)
------------------------------------------------------------

Run this exact script during validation. Do not improvise.

1) /reload
2) Open the profession window (any profession with known recipes)
3) /gob resetdb        (optional once, first run only)
4) /gob ingest
5) /gob dump           (EXPECT: recipe count > 0)
6) /gob add <simpleRecipeId>
7) /gob
   - Queue tab: simple recipe visible
   - Materials tab: shows Need/Have/Short (non-empty)
8) /gob add <complexRecipeId with subcrafts>
   - Queue tab: indented subcraft entries appear
   - Materials tab: base mats list updates accordingly
9) /gob sanity         (EXPECT: PASS)
10) /reload
11) /gob
   - Queue preserved
   - Materials preserved (or rebuilds cleanly)
12) /gob sanity        (EXPECT: PASS)

Optional bank check:
13) Open bank
14) /gob scan
15) Verify "have" increases for bank items

Pass criteria:
- No Lua errors
- sanity always PASS
- subcraft expansion makes sense
- material short list is believable enough to actually gather/buy/craft

