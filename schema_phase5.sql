-- Phase 5 Schema Updates

-- INSTANCE SCHEMA
CREATE TABLE IF NOT EXISTS holocron.instance_locations (
    instance_id INT PRIMARY KEY,
    name VARCHAR(255),
    expansion VARCHAR(50), -- 'WotLK', 'TBC', etc.
    type VARCHAR(20), -- 'Raid', 'Dungeon'
    coordinates VARCHAR(100) -- e.g., "Icecrown: 50, 50"
);

CREATE TABLE IF NOT EXISTS holocron.instance_drops (
    drop_id SERIAL PRIMARY KEY,
    instance_id INT REFERENCES holocron.instance_locations(instance_id),
    item_id INT, -- The mount/pet ID
    name VARCHAR(255),
    type VARCHAR(50) -- 'Mount', 'Pet', 'Transmog'
);

CREATE TABLE IF NOT EXISTS holocron.character_lockouts (
    lockout_id SERIAL PRIMARY KEY,
    character_guid VARCHAR(255) REFERENCES holocron.characters(character_guid),
    instance_id INT REFERENCES holocron.instance_locations(instance_id),
    is_locked BOOLEAN DEFAULT TRUE,
    reset_time TIMESTAMP
);

-- Sample Data for MVP
INSERT INTO holocron.instance_locations (instance_id, name, expansion, type) VALUES
(1, 'Icecrown Citadel', 'WotLK', 'Raid'),
(2, 'Firelands', 'Cata', 'Raid'),
(3, 'Dragon Soul', 'Cata', 'Raid'),
(4, 'Scarlet Monastery (Graveyard)', 'Classic', 'Holiday'),
(5, 'Shadowfang Keep (Crown Chemical Co.)', 'Classic', 'Holiday'),
(6, 'Blackrock Depths (Coren Direbrew)', 'Classic', 'Holiday')
ON CONFLICT (instance_id) DO NOTHING;

INSERT INTO holocron.instance_drops (instance_id, item_id, name, type) VALUES
(1, 50818, 'Invincible''s Reins', 'Mount'),
(2, 69224, 'Smoldering Egg of Millagazor', 'Mount'),
(3, 77069, 'Life-Binder''s Handmaiden', 'Mount'),
(4, 37012, 'The Horseman''s Reins', 'Mount'),
(5, 50250, 'X-45 Heartbreaker', 'Mount'),
(6, 37828, 'Great Brewfest Kodo', 'Mount')
ON CONFLICT DO NOTHING;
