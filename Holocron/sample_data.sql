-- Insert sample characters for testing
INSERT INTO holocron.characters (character_guid, name, realm, class, level, race, faction) VALUES
('GUID-001', 'Thunderfist', 'Area 52', 'Shaman', 80, 'Orc', 'Horde'),
('GUID-002', 'Shadowmend', 'Area 52', 'Priest', 80, 'Undead', 'Horde'),
('GUID-003', 'Moonfire', 'Area 52', 'Druid', 80, 'Tauren', 'Horde'),
('GUID-004', 'Firestorm', 'Area 52', 'Mage', 80, 'Blood Elf', 'Horde')
ON CONFLICT (character_guid) DO NOTHING;

-- Add spec and item_level columns if they don't exist
ALTER TABLE holocron.characters ADD COLUMN IF NOT EXISTS spec VARCHAR(50);
ALTER TABLE holocron.characters ADD COLUMN IF NOT EXISTS item_level INT;

-- Update characters with spec and item level data
UPDATE holocron.characters SET spec = 'Enhancement', item_level = 489 WHERE character_guid = 'GUID-001';
UPDATE holocron.characters SET spec = 'Shadow', item_level = 476 WHERE character_guid = 'GUID-002';
UPDATE holocron.characters SET spec = 'Balance', item_level = 492 WHERE character_guid = 'GUID-003';
UPDATE holocron.characters SET spec = 'Fire', item_level = 485 WHERE character_guid = 'GUID-004';
