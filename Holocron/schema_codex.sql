-- Phase 7 Schema Updates: The Codex

-- CODEX SCHEMA
CREATE SCHEMA IF NOT EXISTS codex;

-- 1. STATIC DATA (The Encyclopedia)
CREATE TABLE IF NOT EXISTS codex.quest_definitions (
    quest_id INTEGER PRIMARY KEY,
    title VARCHAR(255),
    min_level INTEGER,
    race_mask BIGINT,
    class_mask BIGINT,
    rewards_json JSONB
);

CREATE TABLE IF NOT EXISTS codex.quest_dependencies (
    quest_id INTEGER REFERENCES codex.quest_definitions(quest_id),
    required_quest_id INTEGER REFERENCES codex.quest_definitions(quest_id), -- The parent quest
    PRIMARY KEY (quest_id, required_quest_id)
);

CREATE TABLE IF NOT EXISTS codex.campaigns (
    campaign_id SERIAL PRIMARY KEY,
    name VARCHAR(100), -- e.g., "The War Within Campaign"
    ordered_quest_ids INTEGER[] -- Array of Quest IDs in order
);

-- 2. DYNAMIC DATA (Your Alts)
CREATE TABLE IF NOT EXISTS codex.character_quest_history (
    guid VARCHAR(255) REFERENCES holocron.characters(character_guid),
    quest_id INTEGER,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (guid, quest_id)
);

-- Sample Data: "Breaching the Tomb" (Legion Class Mount Campaign)
-- Simplified Chain: A -> B -> C
INSERT INTO codex.quest_definitions (quest_id, title, min_level) VALUES
(47137, 'Champions of Legionfall', 45),
(47139, 'Shard Times', 45),
(46247, 'Defending Broken Isles', 45)
ON CONFLICT (quest_id) DO NOTHING;

INSERT INTO codex.quest_dependencies (quest_id, required_quest_id) VALUES
(47139, 47137), -- Shard Times requires Champions
(46247, 47139)  -- Defending requires Shard Times
ON CONFLICT DO NOTHING;

INSERT INTO codex.campaigns (campaign_id, name, ordered_quest_ids) VALUES
(1, 'Breaching the Tomb', ARRAY[47137, 47139, 46247])
ON CONFLICT (campaign_id) DO NOTHING;
