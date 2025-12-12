IN_GAME_VALIDATION.md
=====================

Purpose:
This document defines the deterministic, copy/paste validation scripts for ALL in-game addons.
Run these exactly as written. Do not improvise during testing.

============================================================
GLOBAL RULES
============================================================
- No Lua errors allowed
- /reload must never corrupt state
- Sanity commands must PASS
- If behavior differs from this doc, it is a BUG (not "expected")

============================================================
DEEPPOCKETS — VALIDATION SCRIPT (PHASE 10 / 10.5)
============================================================

1) /reload
2) Press B
   EXPECT: DeepPockets opens, Blizzard bags do NOT
3) Close DP, press B again
   EXPECT: DP opens again (no double hook)
4) Type in search box
   EXPECT: search auto-focus, items filter
5) Press ESC
   EXPECT: clears search OR closes DP cleanly
6) Disable DP via settings (if exposed) OR command
7) Press B
   EXPECT: Blizzard bags open normally
8) Re-enable DP
9) Press B
   EXPECT: DP opens again
10) Loot or spend gold
    EXPECT: gold updates live
11) Open bank
12) Switch to bank scope
    EXPECT: bank items render (no blank UI)
13) /reload
14) Press B
    EXPECT: same behavior as before reload

PASS CRITERIA:
- No Blizzard bag input leakage
- No stuck focus
- No Lua errors
- Gold always correct

============================================================
PETWEAVER — VALIDATION SCRIPT (PHASE 8)
============================================================

1) /reload
2) /pw
3) Create a new team
4) Set 3 pets + abilities
5) Add notes
6) Create a new script (multiline)
7) Export team
8) Import team
   EXPECT: identical team created
9) /reload
10) /pw
    EXPECT: teams + scripts still present
11) Enter a pet battle with no binding
12) Enter a pet battle with a binding
    EXPECT: correct team/script auto-loads

PASS CRITERIA:
- Persistence across reload
- Import/export round-trip works
- Battle hook works
- No Lua errors

============================================================
SKILLWEAVER — VALIDATION SCRIPT (PHASE 9)
============================================================

1) /reload
2) /sw
3) Create a profile (spec-based)
4) Set profile active
5) Create a sequence:
   Example lines:
     12345 | always
     67890 | target.health<0.2
6) Enable debug (if present)
7) /reload
8) /sw
   EXPECT: profile + sequence still active
9) Enter combat or trigger runtime
   EXPECT: debug prints selected actions
10) /sw sanity
    EXPECT: PASS
11) /sw rebuild
12) /sw sanity
    EXPECT: PASS

PASS CRITERIA:
- Authoring works
- Runtime reads active sequence
- Reload-safe
- Sanity always PASS

============================================================
GOBLIN — VALIDATION SCRIPT (PHASE G1C)
============================================================

1) /reload
2) Open a profession window
3) /gob ingest
4) /gob dump
   EXPECT: recipe count > 0
5) /gob add <simpleRecipeId>
6) /gob
   EXPECT:
     - Queue shows recipe
     - Materials tab populated
7) /gob add <complexRecipeId with subcrafts>
   EXPECT:
     - subcrafts auto-expand
     - quantities make sense
8) /gob sanity
   EXPECT: PASS
9) /reload
10) /gob
    EXPECT: queue + materials preserved or rebuilt cleanly
11) /gob sanity
    EXPECT: PASS
12) Optional bank test:
    - Open bank
    - /gob scan
    - Materials "have" increases appropriately

PASS CRITERIA:
- No cycles
- No negative quantities
- Materials list is believable enough to act on
- Reload-safe
- Sanity always PASS

============================================================
EXIT CONDITION
============================================================

All four sections must PASS before:
- starting new features
- starting G1D (Workflows)
- adding posting, mailing, destroying

This document is authoritative.
