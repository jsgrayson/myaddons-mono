-- Pathfinder: Populate Major Zones and Travel Network
-- Run this to add TWW, DF, SL, and other major hubs

-- Add major expansion hubs
INSERT INTO pathfinder.zones (zone_id, name, expansion) VALUES
-- TWW (The War Within)
(2339, 'Dornogal', 'TWW'),
(2248, 'Isle of Dorn', 'TWW'),
(2215, 'Hallowfall', 'TWW'),
(2255, 'Azj-Kahet', 'TWW'),

-- Dragonflight
(2112, 'Valdrakken', 'Dragonflight'),
(2022, 'The Waking Shores', 'Dragonflight'),
(2023, 'Ohn''ahran Plains', 'Dragonflight'),
(2024, 'The Azure Span', 'Dragonflight'),
(2025, 'Thaldraszus', 'Dragonflight'),

-- Shadowlands
(1670, 'Oribos', 'Shadowlands'),
(1533, 'Bastion', 'Shadowlands'),
(1536, 'Maldraxxus', 'Shadowlands'),
(1565, 'Ardenweald', 'Shadowlands'),
(1525, 'Revendreth', 'Shadowlands'),

-- BFA
(1161, 'Boralus', 'BFA'),
(1165, 'Dazar''alor', 'BFA'),

-- Legion
(1220, 'Legion Dalaran', 'Legion'),
(1015, 'Azsuna', 'Legion'),

-- WoD
(1116, 'Draenor', 'WoD'),

-- Pandaria
(1011, 'Vale of Eternal Blossoms', 'Pandaria'),

-- Classic
(84, 'Stormwind City', 'Vanilla'),
(85, 'Orgrimmar', 'Vanilla'),
(87, 'Ironforge', 'Vanilla'),
(88, 'Thunder Bluff', 'Vanilla'),
(90, 'Undercity', 'Vanilla'),
(103, 'The Exodar', 'TBC'),
(110, 'Silvermoon City', 'TBC'),
(111, 'Shattrath City', 'TBC'),
(125, 'Dalaran (Northrend)', 'WotLK')

ON CONFLICT (zone_id) DO NOTHING;

-- Portal Network (Major Hubs)
INSERT INTO pathfinder.travel_nodes (source_zone_id, dest_zone_id, method, travel_time_seconds, requirements) VALUES

-- Stormwind Portal Room
(84, 1670, 'PORTAL', 10, NULL), -- SW → Oribos
(84, 2112, 'PORTAL', 10, NULL), -- SW → Valdrakken
(84, 2339, 'PORTAL', 10, NULL), -- SW → Dornogal
(84, 1161, 'PORTAL', 10, NULL), -- SW → Boralus
(84, 1220, 'PORTAL', 10, NULL), -- SW → Legion Dalaran
(84, 125, 'PORTAL', 10, NULL),  -- SW → Northrend Dalaran
(84, 111, 'PORTAL', 10, NULL),  -- SW → Shattrath

-- Orgrimmar Portal Room
(85, 1670, 'PORTAL', 10, NULL), -- Org → Oribos
(85, 2112, 'PORTAL', 10, NULL), -- Org → Valdrakken
(85, 2339, 'PORTAL', 10, NULL), -- Org → Dornogal
(85, 1165, 'PORTAL', 10, NULL), -- Org → Dazar'alor
(85, 1220, 'PORTAL', 10, NULL), -- Org → Legion Dalaran
(85, 125, 'PORTAL', 10, NULL),  -- Org → Northrend Dalaran
(85, 111, 'PORTAL', 10, NULL),  -- Org → Shattrath

-- Return Portals (from expansion hubs to capitals)
(1670, 84, 'PORTAL', 10, NULL), -- Oribos → SW
(1670, 85, 'PORTAL', 10, NULL), -- Oribos → Org
(2112, 84, 'PORTAL', 10, NULL), -- Valdrakken → SW
(2112, 85, 'PORTAL', 10, NULL), -- Valdrakken → Org
(2339, 84, 'PORTAL', 10, NULL), -- Dornogal → SW
(2339, 85, 'PORTAL', 10, NULL), -- Dornogal → Org

-- Mage Teleports (major cities, no cooldown)
(84, 85, 'MAGE_PORTAL', 5, 'Mage'),   -- SW → Org
(84, 87, 'MAGE_PORTAL', 5, 'Mage'),   -- SW → Ironforge
(85, 84, 'MAGE_PORTAL', 5, 'Mage'),   -- Org → SW
(85, 88, 'MAGE_PORTAL', 5, 'Mage'),   -- Org → Thunder Bluff
(85, 90, 'MAGE_PORTAL', 5, 'Mage'),   -- Org → Undercity
(84, 125, 'MAGE_PORTAL', 5, 'Mage'),  -- Any → Dalaran
(85, 125, 'MAGE_PORTAL', 5, 'Mage'),

-- Hearthstone connections (15 min CD, goes to inn location)
-- These would be character-specific but we'll add generic examples
(2339, 84, 'HEARTHSTONE', 10, NULL),  -- Assume hearth set to SW
(2112, 85, 'HEARTHSTONE', 10, NULL),  -- Assume hearth set to Org

-- Dalaran Hearthstone (20 min CD)
(84, 1220, 'DALARAN_HEARTHSTONE', 10, NULL),
(85, 1220, 'DALARAN_HEARTHSTONE', 10, NULL),
(2339, 1220, 'DALARAN_HEARTHSTONE', 10, NULL),

-- Garrison Hearthstone
(84, 1116, 'GARRISON_HEARTHSTONE', 10, NULL),
(85, 1116, 'GARRISON_HEARTHSTONE', 10, NULL)

ON CONFLICT DO NOTHING;
