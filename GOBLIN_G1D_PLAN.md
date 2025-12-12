GOBLIN_G1D_PLAN.md
==================

Goblin Phase G1D — Workflows & Restock Targets
(Design-Only Phase — No Code Until G1C Validated In-Game)

------------------------------------------------------------
PURPOSE
------------------------------------------------------------

Phase G1D introduces **INTENT** into Goblin.

G1C answers:
- "What do I need to craft this?"

G1D answers:
- "What do I want to maintain, and why?"

This phase replaces TSM Groups + Operations with a **Workflow → Queue** model.

------------------------------------------------------------
CORE PRINCIPLE
------------------------------------------------------------

Workflows DO NOT execute actions.
Workflows ONLY GENERATE QUEUES.

Execution (crafting, buying, mailing, auctioning) is always:
- explicit
- reviewable
- downstream

------------------------------------------------------------
WORKFLOW DEFINITION
------------------------------------------------------------

A Workflow represents a GOAL.

Examples:
- "Keep Raid Consumables Stocked"
- "Craft Weekly Cooldowns"
- "Personal Enchants"
- "Craft for Sale (Low Risk)"

Workflows are independent and composable.

------------------------------------------------------------
WORKFLOW DATA MODEL (AUTHORITATIVE)
------------------------------------------------------------

Workflow = {
  id: string,
  name: string,
  enabled: boolean,

  scope: {
    character: string | "ALL",
    includeBank: boolean,
    includeReagentBank: boolean
  },

  targets: {
    [itemId]: desiredQuantity
  },

  sources: {
    allowCraft: boolean,
    allowSubcraft: boolean,
    allowBuy: boolean,        // future
    allowInventoryUse: boolean
  },

  policies: {
    allowOvercraft: boolean,
    maxQueueSize: number | nil
  },

  meta: {
    createdAt,
    updatedAt,
    notes
  }
}

------------------------------------------------------------
WORKFLOW → QUEUE PIPELINE
------------------------------------------------------------

1) Read workflow.targets
2) Compare against current inventory snapshot
3) Compute delta:
   delta = max(target - have, 0)
4) Convert delta into:
   - craft queue entries
5) Feed into G1C:
   - subcraft expansion
   - material computation

IMPORTANT:
- G1C never decides intent
- G1D never mutates inventory or executes actions

------------------------------------------------------------
DETERMINISM RULE (CRITICAL)
------------------------------------------------------------

Given:
- same workflow
- same inventory snapshot
- same recipe data

The generated queues MUST be identical.

No hidden state.
No incremental mutation.
Always rebuildable.

------------------------------------------------------------
UI REQUIREMENTS (MVP)
------------------------------------------------------------

Tab: Workflows

- List workflows
- Enable/Disable toggle
- Create/Edit workflow
- Assign targets (item search + qty)
- Button: "Generate Queue"

Tab: Preview

- Shows resulting craft queue
- Shows material short list
- Read-only

NO execution buttons in G1D.

------------------------------------------------------------
WHAT G1D DOES NOT DO
------------------------------------------------------------

- No posting
- No cancel scanning
- No destroying
- No mailing
- No pricing logic
- No automation

Those are separate phases consuming workflow output.

------------------------------------------------------------
RELATIONSHIP TO OTHER ADDONS
------------------------------------------------------------

DeepPockets:
- UI + slot-level inventory only
- No planning logic

Goblin:
- Planning, queues, decisions
- Owns craft/material logic

Holocron:
- Historical memory
- Cross-character aggregation
- Optional enhancement only

------------------------------------------------------------
G1D EXIT CRITERIA
------------------------------------------------------------

G1D is complete when:

1) A workflow can be defined
2) It deterministically generates a craft queue
3) That queue flows cleanly into G1C
4) /reload does not break workflows
5) User can say:
   "This replaces why I used TSM groups"

------------------------------------------------------------
NEXT PHASES (LOCKED ORDER)
------------------------------------------------------------

G2  — Destroy Queue
G3  — Mail Queue
G4  — Auction Post/Cancel
G5  — Accounting & History (Holocron-heavy)

Do NOT skip ahead.

------------------------------------------------------------
AUTHORITATIVE NOTE
------------------------------------------------------------

If an implementation decision conflicts with this document,
THIS DOCUMENT WINS.

End of G1D Plan.
