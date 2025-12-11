# The Diplomat: Renown & Paragon Optimization

## 1. Executive Summary
The Diplomat is a module designed to optimize **Paragon/Renown Efficiency**. In modern WoW, Reputation is account-wide ("Warband"). This module identifies the fastest way to fill the "Paragon Bar" and trigger reward caches using all available characters.

## 2. Feature Specification

### 2.1 The "Paragon Meter" (Dashboard Widget)
A visual tracker for Warband Renown factions at Max Level.
*   **Visual**: Progress bars for each Major Faction.
*   **Status**: "7,800 / 10,000 (Paragon)".
*   **Insight**: "2,200 Rep needed for Reward Cache."

### 2.2 The "Reputation Sniper" (Activity Generator)
Calculates Rep-per-Minute to recommend the most efficient World Quests.
*   **Input**: Active World Quests (Blizzard API).
*   **Logic**:
    *   Quest A: 250 Rep / 30s = 500 Rep/min.
    *   Quest B: 300 Rep / 5m = 60 Rep/min.
*   **Output**: "The Diplomat recommends: Log Hunter (Alt 4). Do WQ 'Kill Rare' in Isle of Dorn."

### 2.3 The "Emissary/Calling" Tracker
Tracks weekly/daily quests with large Rep bonuses.
*   **Alert**: "2 days left to complete 'Aiding the Accord'."
*   **Analysis**: Prioritizes Gold rewards.

## 3. Database Schema

```sql
-- 1. STATIC FACTION DATA
CREATE TABLE diplomat.factions (
    faction_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    expansion VARCHAR(50),
    is_warbound BOOLEAN DEFAULT TRUE,
    paragon_threshold INTEGER DEFAULT 10000
);

-- 2. YOUR STANDING (Dynamic)
CREATE TABLE diplomat.reputation_status (
    guid VARCHAR(50) REFERENCES holocron.characters(character_guid),
    faction_id INTEGER REFERENCES diplomat.factions(faction_id),
    current_level INTEGER,
    current_value INTEGER,
    is_paragon_active BOOLEAN DEFAULT FALSE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (guid, faction_id)
);

-- 3. WORLD QUESTS (Live Feed)
CREATE TABLE diplomat.active_world_quests (
    quest_id INTEGER PRIMARY KEY,
    title VARCHAR(255),
    zone_id INTEGER,
    faction_id INTEGER,
    rep_reward_amount INTEGER,
    gold_reward_amount INTEGER,
    item_reward_id INTEGER,
    expires_at TIMESTAMP
);
```

## 4. Logic Engine (Pseudo-code)

```python
def generate_diplomat_jobs():
    # 1. Fetch Active WQs
    wqs = fetch_blizzard_wqs()
    
    # 2. Check Rep Status
    for faction in factions:
        if faction.current_value > 8000: # Close to paragon
            # 3. Find WQs for this faction
            relevant_wqs = [wq for wq in wqs if wq.faction_id == faction.id]
            
            # 4. Optimize
            for wq in relevant_wqs:
                # Check if an alt is nearby (using Pathfinder)
                best_alt = find_nearest_alt(wq.zone_id)
                create_job(best_alt, wq)
```
