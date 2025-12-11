-- Phase 3 Schema Updates

-- GOBLIN SCHEMA (Pricing)
CREATE TABLE IF NOT EXISTS goblin.market_prices (
    item_id INT PRIMARY KEY,
    market_value INT, -- In copper
    region_avg_daily_sold FLOAT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PETWEAVER SCHEMA (Strategy)
CREATE TABLE IF NOT EXISTS petweaver.teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100),
    slot_1_pet_guid VARCHAR(255),
    slot_2_pet_guid VARCHAR(255),
    slot_3_pet_guid VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS petweaver.species (
    species_id INT PRIMARY KEY,
    name VARCHAR(255),
    can_battle BOOLEAN DEFAULT TRUE
);

-- VIEWS

-- View: Protected Pets
-- Returns a list of Pet GUIDs that are currently used in a Petweaver team.
CREATE OR REPLACE VIEW petweaver.view_protected_pets AS
SELECT slot_1_pet_guid AS pet_guid FROM petweaver.teams WHERE slot_1_pet_guid IS NOT NULL
UNION
SELECT slot_2_pet_guid AS pet_guid FROM petweaver.teams WHERE slot_2_pet_guid IS NOT NULL
UNION
SELECT slot_3_pet_guid AS pet_guid FROM petweaver.teams WHERE slot_3_pet_guid IS NOT NULL;

-- View: Safe to Sell Pets
-- Logic:
-- 1. Count how many of each species we have.
-- 2. If count > 3, identify the extras.
-- 3. Exclude any pet GUID that is in view_protected_pets.
-- Note: This is a simplified logic. Real logic would check breeds (S/S vs B/B).
CREATE OR REPLACE VIEW holocron.view_safe_to_sell_pets AS
WITH SpeciesCounts AS (
    SELECT 
        i.item_id, -- Using item_id as proxy for species_id for this MVP
        COUNT(*) as total_count
    FROM holocron.items i
    WHERE i.class_id = 15 -- Battle Pets
    GROUP BY i.item_id
),
PotentialSells AS (
    SELECT 
        i.item_guid,
        i.item_id,
        i.name,
        i.count,
        i.location_id
    FROM holocron.items i
    JOIN SpeciesCounts sc ON i.item_id = sc.item_id
    WHERE sc.total_count > 3
)
SELECT ps.*
FROM PotentialSells ps
LEFT JOIN petweaver.view_protected_pets pp ON ps.item_guid = pp.pet_guid
WHERE pp.pet_guid IS NULL;

-- View: Liquidatable Assets
-- Logic: Items that have a market value > threshold (e.g., 1000g) and are not bound.
CREATE OR REPLACE VIEW holocron.view_liquidatable_assets AS
SELECT 
    i.name,
    i.count,
    g.market_value,
    (i.count * g.market_value) as total_value,
    s.container_type,
    c.name as character_name
FROM holocron.items i
JOIN goblin.market_prices g ON i.item_id = g.item_id
JOIN holocron.storage_locations s ON i.location_id = s.location_id
JOIN holocron.characters c ON s.character_guid = c.character_guid
WHERE g.market_value > 100000 -- 10g (in copper)
ORDER BY total_value DESC;
