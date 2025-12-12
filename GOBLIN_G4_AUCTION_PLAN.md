GOBLIN_G4_AUCTION_PLAN.md
=========================

Goblin Phase G4 — Auction Scanning & Post/Cancel Queues
(DESIGN-ONLY — NO IMPLEMENTATION UNTIL G1C SANITY PASSES)

------------------------------------------------------------
GOAL
------------------------------------------------------------

Replace TSM auctioning outcomes WITHOUT copying TSM design.

Goblin must:
- scan the Auction House in-game
- generate explicit Post / Cancel queues
- never automate destructive actions
- remain fully offline-first

Holocron may store history and analytics, but NEVER drives live decisions.

------------------------------------------------------------
HARD RULES (NON-NEGOTIABLE)
------------------------------------------------------------

1) AH scanning ONLY happens in-game
2) AH scanning ONLY happens while AH UI is open
3) No background polling
4) No blind posting or canceling
5) Every action must be explainable

If a scan is stale or missing, Goblin must refuse to act.

------------------------------------------------------------
DATA OWNERSHIP
------------------------------------------------------------

Goblin owns (authoritative):
- live AH snapshot
- your auctions snapshot
- post queue
- cancel queue

Holocron owns (optional memory):
- historical prices
- sale outcomes
- long-term trends

------------------------------------------------------------
AUCTION SNAPSHOT MODEL
------------------------------------------------------------

AHScan = {
  scanId,
  scannedAt,
  realm,
  faction,

  listings: {
    [itemId]: {
      minBuyout,
      listingsCount,
      totalQuantity,
      samplePrices[]
    }
  },

  myAuctions: {
    [auctionId]: {
      itemId,
      quantity,
      buyout,
      expiresAt
    }
  }
}

Snapshots are immutable.
New scan = new snapshot.

------------------------------------------------------------
SCAN TRIGGERS
------------------------------------------------------------

- Triggered ONLY when AH frame opens
- Manual button: "Scan AH"
- Throttled (one scan per X minutes)

If scan fails:
- store failure reason
- show banner
- do NOT crash

------------------------------------------------------------
POST QUEUE GENERATION
------------------------------------------------------------

Inputs:
- Workflow targets (G1D)
- Inventory snapshot
- Latest AH scan

Rules:
- No scan → no post queue
- Never exceed target quantity
- Never post if price unknown
- Never post below configured floor (future)

PostQueueEntry = {
  itemId,
  quantity,
  unitPrice,
  reason,        // human-readable explanation
  workflowId
}

------------------------------------------------------------
CANCEL QUEUE GENERATION
------------------------------------------------------------

Inputs:
- MyAuctions snapshot
- Latest AH scan

Rules:
- Cancel ONLY if:
  - undercut beyond threshold
  - auction expired soon
- Never cancel blindly
- Each cancel has a reason

CancelQueueEntry = {
  auctionId,
  itemId,
  reason,
  recommendedRepostPrice
}

------------------------------------------------------------
UI REQUIREMENTS (MVP)
------------------------------------------------------------

Tab: Auction

Sections:
- Scan Status (Fresh / Stale / Missing)
- Post Queue (review-only)
- Cancel Queue (review-only)

Buttons:
- Scan AH
- Execute Post Queue (manual, step-by-step)
- Execute Cancel Queue (manual, step-by-step)

No "one-click do everything".

------------------------------------------------------------
SANITY RULES
------------------------------------------------------------

- No scan → queues empty
- Stale scan → warning banner
- Queue entry count must match explanations
- All prices must be visible
- User can always say "why is this here?"

------------------------------------------------------------
WHAT G4 DOES NOT DO
------------------------------------------------------------

- No auto posting
- No auto canceling
- No pricing models (yet)
- No shopping scans (future phase)

------------------------------------------------------------
EXIT CRITERIA
------------------------------------------------------------

G4 is complete when:
- AH can be scanned safely
- Post queue is understandable
- Cancel queue is understandable
- Nothing happens without confirmation
- User trusts Goblin more than TSM

------------------------------------------------------------
AUTHORITATIVE NOTE
------------------------------------------------------------

If implementation conflicts with this document,
THIS DOCUMENT WINS.

End of G4 Auction Plan.
