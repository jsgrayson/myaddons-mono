-- Phase 6 Schema Updates: Project Pathfinder

-- PATHFINDER SCHEMA
CREATE SCHEMA IF NOT EXISTS pathfinder;

-- 1. STATIC MAP DATA
CREATE TABLE IF NOT EXISTS pathfinder.zones (
    zone_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    expansion VARCHAR(50) -- 'Vanilla', 'TBC', 'WotLK', etc.
);

-- 2. CONNECTIONS (The Graph)
CREATE TABLE IF NOT EXISTS pathfinder.travel_nodes (
    node_id SERIAL PRIMARY KEY,
    source_zone_id INTEGER REFERENCES pathfinder.zones(zone_id),
    dest_zone_id INTEGER REFERENCES pathfinder.zones(zone_id),
    method VARCHAR(50), -- 'PORTAL', 'BOAT', 'ZEPPELIN', 'FLIGHT_PATH'
    travel_time_seconds INTEGER,
    requirements VARCHAR(100) -- e.g., 'Mage', 'Engineer'
);

-- 3. CHARACTER STATE (Dynamic)
CREATE TABLE IF NOT EXISTS pathfinder.char_locations (
    guid VARCHAR(255) PRIMARY KEY REFERENCES holocron.characters(character_guid),
    current_zone_id INTEGER,
    hearthstone_cd TIMESTAMP,
    dalaran_hearth_cd TIMESTAMP,
    garrison_hearth_cd TIMESTAMP,
    wormhole_cd TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample Data: Major Hubs
INSERT INTO pathfinder.zones (zone_id, name, expansion) VALUES
(84, 'Stormwind City', 'Vanilla'),
(85, 'Orgrimmar', 'Vanilla'),
(125, 'Dalaran (Northrend)', 'WotLK'),
(1670, 'Oribos', 'Shadowlands'),
(2112, 'Valdrakken', 'Dragonflight')
ON CONFLICT (zone_id) DO NOTHING;

-- Sample Data: Portals (Stormwind Hub)
INSERT INTO pathfinder.travel_nodes (source_zone_id, dest_zone_id, method, travel_time_seconds) VALUES
(84, 1670, 'PORTAL', 10), -- SW -> Oribos
(84, 125, 'PORTAL', 10), -- SW -> Dalaran
(1670, 84, 'PORTAL', 10), -- Oribos -> SW
(2112, 84, 'PORTAL', 10)  -- Valdrakken -> SW
ON CONFLICT DO NOTHING;
