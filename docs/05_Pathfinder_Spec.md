# Project Pathfinder: Tactical Navigation & Routing Engine

## 1. Executive Summary
Pathfinder is a logic module for the Holocron ERP system that optimizes **Player Time-on-Target**. 
Instead of manually deciding "Which alt should I play?" or "What is the fastest way to get to Icecrown?", Pathfinder uses **graph theory** and **constraint programming** (via `networkx` in Python) to calculate the mathematically perfect route for your daily/weekly chores.

**Compliance**: This system relies 100% on `SavedVariables` text files. It uses no camera, no screen reading, and no memory injection.

## 2. Feature Specification

### 2.1 The "Travel Matrix" (Cooldown Tracking)
Most players forget which alt has their Dalaran Hearthstone off cooldown or which Engineer has the Wormhole Generator: Northrend ready.

*   **Function**: Tracks the exact timestamp of every teleport spell, hearthstone, and item cooldown across all characters.
*   **Dashboard View**: A "Fast Travel" status board.
    *   *Mage*: ✅ Teleport: Oribos
    *   *Druid*: ❌ Hearthstone (12m remaining)
    *   *Warrior*: ✅ Wormhole: Argus

### 2.2 The "Boredom Navigator" (The Hitlist)
Integrates **Lockout Data** with **Collection Data** to generate a dynamic "To-Do" list.

*   **Logic**: It filters content based on three criteria:
    1.  **Reward**: Do I need the Mount/Transmog/Pet? (Checked against Petweaver/Holocron DB).
    2.  **Availability**: Is the raid unlocked? (Checked against `SavedInstances`).
    3.  **Proximity**: Is the character currently parked near the entrance?
*   **Output**: A sorted card view.
    *   *1. Onyxia's Lair (Priority: High)*
        *   Target: [Mount]
        *   Character: Alt-4 (Parked in Dustwallow Marsh).
        *   Status: Unlocked.

### 2.3 The "Chore Solver" (Route Optimization)
The core feature. When you have 12 alts doing "The Feast" or "World Bosses."

*   **Input**: User selects "Weekly World Bosses" on the Dashboard.
*   **Computation**: The Server builds a "Graph" of Azeroth (Nodes = Zones, Edges = Portals/Flight Paths).
*   **Output**: An optimized itinerary:
    *   *Log Alt-A (Mage)*: Port to Dalaran -> Fly to Azsuna -> Kill Boss.
    *   *Log Alt-B (Druid)*: Dreamwalk to Legion -> Kill Boss.
    *   *Log Alt-C (Warrior)*: Hearthstone on CD -> SKIP (or use Guild Cloak).

## 3. Technical Architecture

### A. Data Ingest (The "Senses")
We need to collect location and cooldown data. We will use the standard addon **SavedInstances** and parse its database.
*   **Source File**: `SavedVariables/SavedInstances.lua`
*   **Data Extracted**:
    *   `player_zone`: Current Zone ID.
    *   `cooldowns`: Table of spell IDs and reset timestamps.
    *   `lockouts`: Raid IDs and kill counts.

### B. The Graph Database (The "Map")
We need to teach the server what Azeroth looks like. We will build a static SQL table defining connections.
*   **Nodes**: Zones (Stormwind, Oribos, Valdrakken).
*   **Edges (Connections)**:
    *   *Static*: SW -> Oribos (Portal). Cost: 10 seconds.
    *   *Dynamic*: Location A -> Location B (Hearthstone). Cost: 10 seconds (Only if `hearth_cooldown < now`).

### C. The Solver (The "Brain")
We use `networkx` (Python) to solve the routing.
*   **Algorithm**: Shortest Path (Dijkstra/A*).
*   **Cost Function**: Minimize Time.

## 4. Database Schema

```sql
-- 1. STATIC MAP DATA
CREATE TABLE pathfinder.zones (
    zone_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    expansion VARCHAR(50)
);

-- 2. CONNECTIONS (The Graph)
CREATE TABLE pathfinder.travel_nodes (
    source_zone_id INTEGER,
    dest_zone_id INTEGER,
    method VARCHAR(50), -- 'PORTAL', 'BOAT', 'FLIGHT_PATH'
    travel_time_seconds INTEGER
);

-- 3. CHARACTER STATE (Dynamic)
CREATE TABLE pathfinder.char_locations (
    guid VARCHAR(50) PRIMARY KEY,
    current_zone_id INTEGER,
    hearthstone_cd TIMESTAMP,
    dalaran_hearth_cd TIMESTAMP,
    garrison_hearth_cd TIMESTAMP,
    wormhole_cd TIMESTAMP
);
```

## 5. Integration Ideas
*   **Mage Logic**: Mages have zero-cooldown teleports. The graph weights for Mage characters should be significantly lower for major hubs.
*   **"Bus Route" Logic**: If multiple chores are in the same zone (e.g., World Boss + Raid), the solver should group them into a single "trip" to minimize porting.
