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
