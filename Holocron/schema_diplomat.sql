-- Phase 8 Schema Updates: The Diplomat

-- DIPLOMAT SCHEMA
CREATE SCHEMA IF NOT EXISTS diplomat;

-- 1. STATIC FACTION DATA
CREATE TABLE IF NOT EXISTS diplomat.factions (
    faction_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    expansion VARCHAR(50),
    is_warbound BOOLEAN DEFAULT TRUE,
    paragon_threshold INTEGER DEFAULT 10000
);

-- 2. YOUR STANDING (Dynamic)
CREATE TABLE IF NOT EXISTS diplomat.reputation_status (
    guid VARCHAR(255) REFERENCES holocron.characters(character_guid),
    faction_id INTEGER REFERENCES diplomat.factions(faction_id),
    current_level INTEGER,
    current_value INTEGER,
    is_paragon_active BOOLEAN DEFAULT FALSE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (guid, faction_id)
);

-- 3. WORLD QUESTS (Live Feed - Mocked for MVP)
CREATE TABLE IF NOT EXISTS diplomat.active_world_quests (
    quest_id INTEGER PRIMARY KEY,
    title VARCHAR(255),
    zone_id INTEGER,
    faction_id INTEGER,
    rep_reward_amount INTEGER,
    gold_reward_amount INTEGER,
    item_reward_id INTEGER,
    expires_at TIMESTAMP
);

-- Sample Data: The War Within Factions
INSERT INTO diplomat.factions (faction_id, name, expansion) VALUES
(2600, 'Council of Dornogal', 'The War Within'),
(2601, 'The Assembly of the Deeps', 'The War Within'),
(2602, 'Hallowfall Arathi', 'The War Within'),
(2603, 'The Severed Threads', 'The War Within')
ON CONFLICT (faction_id) DO NOTHING;
