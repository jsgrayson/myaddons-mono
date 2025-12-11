Project Holocron: The World of Warcraft ERP Ecosystem

Version: 2.0 (God Mode)
Hardware: Dell R720 (Brain), Jetson Orin Nano (Voice/Display), Gaming PC (Client)

1. System Architecture

1.1 The Topology

The Brain (Dell R720): Hosts the Postgres Database, Python Logic Engines, Llama 3 LLM, and SimulationCraft. It runs 24/7.

The Senses (Jetson Orin Nano): Acts as the "Physical Interface."

Output: Text-to-Speech (TTS) via speakers for in-game alerts.

Display: Renders the "Boredom Mode" dashboard on a secondary monitor.

The Client (Gaming PC): Runs WoW. Uses a lightweight Python Bridge script to sync SavedVariables to the Brain.

The Comm Link (Mobile): Uses ntfy.sh for bi-directional push notifications and a PWA (Web App) for remote management.

2. Feature Specification

Module A: Logistics ("Holocron")

Unified Inventory: Searchable DB of every item across Bags, Banks, Mail, Guild Banks, and Warband Banks.

Warband Priority: Logistics logic prefers moving items via Warband Bank (Instant) over Mailbox (1 hour).

The Mailing Shortcut: Generates a Lua manifest (Holocron_Logistics.lua). In-game button auto-fills outgoing mail based on server orders.

Module B: Strategy ("Petweaver")

Collection Safety: Prevents liquidation of pets if < 3 owned or if the specific GUID is part of a saved Battle Team.

Breed Upgrader: Identifies if a new drop (e.g., S/S) is superior to a current pet (B/B) and queues a swap.

Module C: Intelligence ("The Codex" & "The Forge")

RAG Guide (Codex): AI-driven Q&A. "How do I unlock Earthen?" -> AI checks your specific quest history and gives the exact missing step.

Auto-Sim (The Forge): R720 runs SimulationCraft on the Great Vault loot table every Tuesday morning. Dashboard ranks drops by % Upgrade.

Module D: Efficiency ("Pathfinder" & "Diplomat")

Route Optimization (Pathfinder): Solves the "Traveling Salesman Problem" for daily chores using graph theory (Portals, Hearths, Flight Paths).

Renown Sniper (Diplomat): Calculates "Reputation per Minute" of active World Quests. Alerts you only when a Paragon Chest (Gold) is imminent.

Module E: The Assistant ("The Construct")

In-Game Voice: You type /holo [Query]. The Jetson speaks the answer via Coqui TTS. "Draconic Runes are 200g. Sell now."

Mobile Push: Proactive alerts sent to phone via ntfy. "Arbitrage Opportunity: Buy on Area 52, Sell on Moonguard."

3. Implementation Plan

Phase 1: The Foundation (Database & Bridge)

Goal: Data flowing from Gaming PC -> R720.

Database: Deploy PostgreSQL on R720. Run schema.sql (see below).

Bridge Script: Deploy bridge.py on Gaming PC.

Watch: DataStore_*.lua, SavedInstances.lua.

Action: Parse Lua -> JSON -> POST to R720.

Dashboard MVP: Deploy Flask/Django on R720. Create basic "Search" view.

Phase 2: The Logic Engines (Python)

Goal: Turning data into instructions.

Goblin Engine: Python script polling Blizzard Auction API. Populates market_prices.

Logistics Engine: SQL Logic to generate logistics_jobs (e.g., "Main needs Potions -> Find in Warband Bank").

The Generator: Script to write Holocron_Logistics.lua for the client to download.

Phase 3: The AI Layer (Compute)

Goal: Utilizing the R720's CPU/RAM.

The Forge: Deploy Dockerized SimulationCraft. Script to ingest player string -> Run Sim -> Store result.

The Brain: Deploy Ollama (Llama 3).

The Briefing: Create briefing_agent.py. Queries DB -> Prompts Llama 3 -> Sends ntfy push notification.

Phase 4: The "Construct" (Audio/Mobile)

Goal: Breaking the Fourth Wall.

Jetson Setup: Install Coqui TTS or Piper TTS (Fast/Local).

Audio API: Create a simple endpoint on Jetson: POST /speak {text}.

Chat Hook: Update Bridge to watch Holocron_Chat.lua. When changed, R720 processes query -> Sends text to Jetson -> Jetson speaks.

4. Database Schema (PostgreSQL)

-- 1. CORE ENTITIES
CREATE TABLE characters (
    guid VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50),
    realm VARCHAR(50),
    class VARCHAR(20),
    gold BIGINT, -- Copper
    ilvl DECIMAL(5,2),
    current_zone VARCHAR(100),
    last_seen TIMESTAMP
);

-- 2. STORAGE & WARBAND
CREATE TABLE storage_locations (
    location_id SERIAL PRIMARY KEY,
    owner_guid VARCHAR(50) REFERENCES characters(guid),
    type VARCHAR(20), -- 'BAG', 'BANK', 'WARBAND', 'GUILD'
    tab_index INTEGER,
    tab_name VARCHAR(100)
);

CREATE TABLE items (
    item_guid SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES storage_locations(location_id),
    item_id INTEGER,
    count INTEGER,
    item_link TEXT
);

-- 3. INTELLIGENCE TABLES
CREATE TABLE market_prices (
    item_id INTEGER PRIMARY KEY,
    min_buyout BIGINT,
    market_value BIGINT,
    last_updated TIMESTAMP
);

CREATE TABLE raid_lockouts (
    character_guid VARCHAR(50),
    instance_name VARCHAR(100),
    is_locked BOOLEAN,
    reset_time TIMESTAMP
);

-- 4. THE CONSTRUCT (AI Memory)
CREATE TABLE ai_context (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    query TEXT,
    response TEXT,
    context_zone VARCHAR(100) -- Used to tune "Persona"
);

-- 5. LOGISTICS QUEUE
CREATE TABLE logistics_jobs (
    job_id SERIAL PRIMARY KEY,
    priority VARCHAR(10), -- 'HIGH', 'LOW'
    status VARCHAR(20), -- 'PENDING', 'COMPLETED'
    instruction TEXT, -- "Mail [Item] to [Char]"
    source_guid VARCHAR(50),
    target_guid VARCHAR(50)
);


5. Deployment Checklist

R720 (Server)

[ ] Docker & Docker Compose installed.

[ ] Postgres Container running.

[ ] Ollama (Llama 3) installed.

[ ] SimulationCraft installed.

[ ] Python Environment (flask, pandas, psycopg2, ortools).

Gaming PC (Client)

[ ] WoW Addons: DataStore, SavedInstances.

[ ] Python Bridge Script running in background.

Jetson (Edge)

[ ] TTS Engine installed.

[ ] Speakers connected.

[ ] Web Browser (Kiosk Mode) pointing to R720 Dashboard.

Mobile

[ ] ntfy app installed.

[ ] Subscribed to topic holocron_alerts.