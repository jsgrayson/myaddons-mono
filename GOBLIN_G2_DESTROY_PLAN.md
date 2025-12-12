GOBLIN_G2_DESTROY_PLAN.md
=========================

Goblin Phase G2 — Destroy Queue (Disenchant / Prospect / Mill / Scrap)
(DESIGN-ONLY — NO IMPLEMENTATION UNTIL IN-GAME VALIDATION RESUMES)

------------------------------------------------------------
GOAL
------------------------------------------------------------

Provide TSM-class "Destroy" outcomes without dangerous automation.

Goblin must:
- identify destroyable items
- generate an explicit Destroy Queue
- execute step-by-step with confirmation + throttling
- remain offline-first (no backend required)

------------------------------------------------------------
HARD RULES (NON-NEGOTIABLE)
------------------------------------------------------------

1) Destroying is ALWAYS explicit (user-initiated mode)
2) No background automation
3) No destructive action without on-screen confirmation
4) Throttle everything (avoid disconnect / protected action issues)
5) Every queued action must be explainable

------------------------------------------------------------
DATA OWNERSHIP
------------------------------------------------------------

Goblin owns:
- destroy rules
- destroy queue
- execution state (what is next)
- local event capture (yields)

Holocron may store:
- historical yields
- long-term ROI analytics
But Holocron never executes.

------------------------------------------------------------
DESTROY TYPES (MVP ORDER)
------------------------------------------------------------

Implement in this order (design supports all):
1) Disenchant
2) Prospect
3) Mill
4) Scrap (or expansion-specific salvage)

Each type is a "processor" with:
- eligibility rules
- action method
- expected outputs (optional)

------------------------------------------------------------
DESTROY RULE MODEL (NO TSM GROUPS)
------------------------------------------------------------

Rules are workflow-like, not group-like.

DestroyRule = {
  id: string,
  name: string,
  enabled: boolean,

  processor: "DISENCHANT" | "PROSPECT" | "MILL" | "SCRAP",

  selectors: {
    include: [itemId] OR includeClasses: [...]
    exclude: [itemId]
  },

  limits: {
    maxPerSession: number,
    maxPerItem: number,
    keepAtLeast: { [itemId]: qty }   // never destroy below this
  },

  policies: {
    requireShiftHeld: boolean,        // safety gate
    stopOnError: boolean
  }
}

------------------------------------------------------------
DESTROY QUEUE MODEL
------------------------------------------------------------

DestroyQueueEntry = {
  itemId,
  quantity,
  processor,
  reason,          // explain why this item is in the queue
  ruleId
}

Rules:
- Queue is deterministic and rebuildable
- Never includes items under keepAtLeast
- Never includes soulbound/locked items unless explicitly allowed (default: deny)

------------------------------------------------------------
ELIGIBILITY (HIGH-LEVEL)
------------------------------------------------------------

- Disenchant:
  - item is disenchantable (bind/quality rules)
  - player has Enchanting
- Prospect:
  - item is prospectable ore
  - player has Jewelcrafting
- Mill:
  - item is millable herb
  - player has Inscription
- Scrap:
  - item is scrappable and relevant system exists

If eligibility uncertain:
- do not queue it
- show "unknown eligibility" info row (optional), not an action

------------------------------------------------------------
EXECUTION MODE (SAFETY-FIRST)
------------------------------------------------------------

UI: Destroy tab

Sections:
- Rules (enable/disable)
- Queue preview (review-only)
- Execution panel:
  - "Start Destroy Mode"
  - shows NEXT item
  - shows remaining count
  - "Process Next" button
  - STOP button

Safety gates:
- Optional: must hold SHIFT to process next
- Throttle delay between actions
- Stop on bag changes if necessary

No "process all instantly".

------------------------------------------------------------
YIELD CAPTURE (OPTIONAL MVP)
------------------------------------------------------------

When destroying, capture:
- input itemId + qty
- outputs gained (if trackable)
- timestamp

Store locally; sync to Holocron later for analytics.

------------------------------------------------------------
SANITY RULES
------------------------------------------------------------

- Queue quantities >= 0
- No entry violates keepAtLeast
- No entry lacks a processor
- Execution never runs without explicit user input
- Stop cleanly on errors (no infinite loops)

------------------------------------------------------------
WHAT G2 DOES NOT DO
------------------------------------------------------------

- No ROI optimization
- No pricing tie-in
- No "smart best choice" between destroy vs sell
That comes later, after we have stable yields + pricing.

------------------------------------------------------------
EXIT CRITERIA
------------------------------------------------------------

G2 is complete when:
- A destroy queue can be generated deterministically
- The user can safely process items step-by-step
- No accidental destruction is possible
- The system is trustworthy

------------------------------------------------------------
AUTHORITATIVE NOTE
------------------------------------------------------------

If implementation conflicts with this document,
THIS DOCUMENT WINS.

End of G2 Destroy Plan.
