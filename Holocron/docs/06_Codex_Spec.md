# The Codex: Questing & Campaign Intelligence

## 1. Executive Summary
The Codex is a logic module for Holocron designed to solve the "Alt Problem": losing track of campaign progress. It provides a **Universal Matrix** to visualize progression across all characters and a **Blocker Breaker** to solve phasing issues by tracing quest dependencies.

## 2. Feature Specification

### 2.1 The "Universal Matrix" (Campaign Grid)
A massive visualization on the Web Dashboard tracking major progression points.
*   **Rows**: Characters.
*   **Columns**: Major Milestones (e.g., "Dragonflight Main Story," "Class Hall Campaign").
*   **Cells**:
    *   🟢 Done: Completed.
    *   🟡 In Progress: "Step 4/15: 'Talk to Khadgar'."
    *   🔴 Not Started: Available to pickup.
    *   🔒 Locked: Prereqs missing.

### 2.2 The "Blocker Breaker" (Dependency Solver)
*   **Input**: User types "Unlock Mechagon".
*   **Logic**: The Server traces the quest chain backwards from the end goal.
*   **Output**: "You are missing the quest 'The Warchief's Order' (ID: 543). It was abandoned in Nazjatar. Go to coords 45, 60 to re-acquire it."

### 2.3 The "Guide-RAG" (AI Walkthroughs)
*   **Context**: The AI knows exactly which quest step you are on.
*   **Query**: "How do I do the 'Ley Line' puzzle?"
*   **Response**: "Connect the Blue square to the Red triangle. Do not cross the streams." (Sourced from Wowhead comments).

## 3. Database Schema

```sql
-- STATIC DATA (The Encyclopedia)
CREATE TABLE codex.quest_definitions (
    quest_id INTEGER PRIMARY KEY,
    title VARCHAR(255),
    min_level INTEGER,
    race_mask BIGINT,
    class_mask BIGINT,
    rewards_json JSONB
);

CREATE TABLE codex.quest_dependencies (
    quest_id INTEGER,
    required_quest_id INTEGER, -- The parent quest
    PRIMARY KEY (quest_id, required_quest_id)
);

CREATE TABLE codex.campaigns (
    campaign_id SERIAL PRIMARY KEY,
    name VARCHAR(100), -- e.g., "The War Within Campaign"
    ordered_quest_ids INTEGER[] -- Array of Quest IDs in order
);

-- DYNAMIC DATA (Your Alts)
CREATE TABLE codex.character_quest_history (
    guid VARCHAR(50) REFERENCES holocron.characters(character_guid),
    quest_id INTEGER,
    completed_at TIMESTAMP,
    PRIMARY KEY (guid, quest_id)
);
```

## 4. Logic Engine (Pseudo-code)

```python
def find_next_step(character_guid, campaign_id):
    # 1. Get the full chain for the campaign
    chain = get_quest_chain(campaign_id)
    
    # 2. Get user's history
    completed_ids = get_completed_quests(character_guid)
    
    # 3. Find the first 'False' in the chain
    for quest in chain:
        if quest.id not in completed_ids:
            # 4. Check Prerequisites
            if has_prereqs(quest.id, completed_ids):
                return f"Next Step: Pick up '{quest.title}'."
            else:
                # Recursive step: Find the missing prereq
                return find_missing_prereq(quest.id, completed_ids)
    
    return "Campaign Complete."
```
