GOBLIN_G3_MAIL_PLAN.md
======================

Goblin Phase G3 — Mail Queue
(DESIGN-ONLY — NO IMPLEMENTATION UNTIL IN-GAME VALIDATION)

------------------------------------------------------------
GOAL
------------------------------------------------------------

Provide a safe, explicit, offline-first replacement for TSM mailing.

Goblin must:
- generate deterministic mail queues
- make inventory movement explicit and reviewable
- support crafter/banker/alt workflows
- never send mail blindly or automatically

------------------------------------------------------------
CORE PRINCIPLE
------------------------------------------------------------

Mailing is a LOGISTICS ACTION, not automation.

Mail queues are:
- generated from workflows and inventory state
- reviewed by the user
- executed step-by-step

No hidden rules.
No implicit routing.
No magic.

------------------------------------------------------------
DATA OWNERSHIP
------------------------------------------------------------

Goblin owns:
- mail rules
- mail queue
- execution state

Holocron may store:
- mail history
- delivery outcomes
- cross-character summaries

Holocron never executes mail.

------------------------------------------------------------
MAIL RULE MODEL
------------------------------------------------------------

MailRule = {
  id: string,
  name: string,
  enabled: boolean,

  sourceScope: {
    character: string,
    includeBank: boolean
  },

  destination: {
    character: string,
    mailbox: "PLAYER"
  },

  selectors: {
    includeItemIds: [itemId],
    includeCategories: [category],
    excludeItemIds: [itemId]
  },

  limits: {
    maxPerItem: number | nil,
    maxPerSession: number | nil,
    keepAtLeast: { [itemId]: qty }
  },

  policies: {
    splitStacks: boolean,
    requireShiftHeld: boolean,
    stopOnError: boolean
  }
}

------------------------------------------------------------
MAIL QUEUE MODEL
------------------------------------------------------------

MailQueueEntry = {
  itemId,
  quantity,
  destinationCharacter,
  reason,          // human-readable explanation
  ruleId
}

Rules:
- Queue is deterministic and rebuildable
- Never violates keepAtLeast
- Never includes soulbound or locked items
- Never exceeds mailbox constraints

------------------------------------------------------------
QUEUE GENERATION PIPELINE
------------------------------------------------------------

1) Read active mail rules
2) Evaluate selectors against inventory snapshot
3) Apply limits + keepAtLeast
4) Generate mail queue entries
5) Present queue for review

No execution occurs here.

------------------------------------------------------------
EXECUTION MODE (SAFETY-FIRST)
------------------------------------------------------------

UI: Mail tab

Sections:
- Rules (enable/disable)
- Queue preview (read-only)
- Execution panel:
  - "Start Mail Mode"
  - Shows next item + destination
  - "Send Next" button
  - STOP button

Safety gates:
- Optional: require holding SHIFT to send
- Throttle delay between sends
- Stop cleanly on error

No "send all" button.

------------------------------------------------------------
SANITY RULES
------------------------------------------------------------

- Queue quantities >= 0
- No entry violates keepAtLeast
- Destination must be valid
- Execution never proceeds without user action
- Errors stop execution safely

------------------------------------------------------------
WHAT G3 DOES NOT DO
------------------------------------------------------------

- No auto mailing
- No routing logic based on prices
- No execution without confirmation
- No background sending

------------------------------------------------------------
EXIT CRITERIA
------------------------------------------------------------

G3 is complete when:
- Mail queue can be generated deterministically
- User understands why each item is queued
- Execution is safe and explicit
- No accidental item loss is possible

------------------------------------------------------------
AUTHORITATIVE NOTE
------------------------------------------------------------

If implementation conflicts with this document,
THIS DOCUMENT WINS.

End of G3 Mail Plan.
