GOBLIN_G5_ACCOUNTING_PLAN.md
============================

Goblin Phase G5 — Accounting, History, and Confidence
(DESIGN-ONLY — NO IMPLEMENTATION UNTIL EXECUTION PHASES STABILIZE)

------------------------------------------------------------
GOAL
------------------------------------------------------------

Provide long-term economic visibility WITHOUT affecting live decisions.

Goblin executes.
Holocron remembers.

Accounting answers:
- What did I craft?
- What did it cost?
- What sold?
- What was destroyed?
- What was profitable over time?

------------------------------------------------------------
HARD RULES (NON-NEGOTIABLE)
------------------------------------------------------------

1) Accounting NEVER drives live decisions
2) Accounting NEVER blocks execution
3) Accounting is append-only (no rewriting history)
4) Goblin is authoritative at execution time
5) Holocron is authoritative for historical views

------------------------------------------------------------
EVENT MODEL (SOURCE OF TRUTH)
------------------------------------------------------------

Goblin emits events.
Holocron stores and aggregates them.

Event = {
  eventId,
  eventType,
  timestamp,
  character,
  realm,

  payload: {...}
}

Events are immutable.

------------------------------------------------------------
EVENT TYPES (MVP)
------------------------------------------------------------

CRAFT_EXECUTED
- recipeId
- quantity
- inputs [{itemId, qty}]
- outputs [{itemId, qty}]

DESTROY_EXECUTED
- processor
- itemId
- quantity
- outputs (if detectable)

MAIL_SENT
- destination
- itemId
- quantity

AUCTION_POSTED
- itemId
- quantity
- unitPrice

AUCTION_SOLD
- itemId
- quantity
- unitPrice
- deposit
- fees

AUCTION_CANCELLED
- itemId
- quantity
- reason

------------------------------------------------------------
DATA OWNERSHIP
------------------------------------------------------------

Goblin stores (short-term):
- recent execution events
- unsynced event buffer

Holocron stores (long-term):
- all events
- aggregates
- trends
- profitability views

------------------------------------------------------------
SYNC MODEL
------------------------------------------------------------

- Goblin batches events locally
- Sync is explicit or scheduled
- Failure to sync NEVER blocks Goblin
- Duplicate events are deduplicated by eventId

------------------------------------------------------------
ACCOUNTING VIEWS (HOLCRON)
------------------------------------------------------------

Examples (non-exhaustive):
- Profit by item
- Profit by workflow
- Craft vs buy cost comparison
- Destroy yield averages
- Auction success rates

These views NEVER exist in-game.

------------------------------------------------------------
CONFIDENCE & SANITY
------------------------------------------------------------

Accounting sanity rules:
- Every execution event has a matching queue origin
- Quantities are never negative
- Timestamps are monotonic per character
- Missing price data is allowed (marked unknown)

If accounting data is incomplete:
- show warnings
- NEVER block execution

------------------------------------------------------------
WHAT G5 DOES NOT DO
------------------------------------------------------------

- No live pricing
- No decision-making logic
- No automation
- No retroactive correction

------------------------------------------------------------
EXIT CRITERIA
------------------------------------------------------------

G5 is complete when:
- All execution actions emit events
- Events sync safely to Holocron
- Historical views are correct
- Goblin gameplay is unchanged if Holocron is offline

------------------------------------------------------------
AUTHORITATIVE NOTE
------------------------------------------------------------

If implementation conflicts with this document,
THIS DOCUMENT WINS.

End of G5 Accounting Plan.
