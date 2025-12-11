-- Codex Encounter Database Schema
-- Stores raid/dungeon encounter guides with role-specific tactics

CREATE TABLE IF NOT EXISTS codex.instances (
    instance_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'raid' or 'dungeon'
    expansion VARCHAR(100), -- e.g., 'The War Within'
    tier VARCHAR(50), -- e.g., 'Season 1'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS codex.encounters (
    encounter_id SERIAL PRIMARY KEY,
    instance_id INTEGER REFERENCES codex.instances(instance_id) ON DELETE CASCADE,
    boss_name VARCHAR(255) NOT NULL,
    boss_slug VARCHAR(255) NOT NULL,
    overview TEXT,
    icy_veins_url VARCHAR(500),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(instance_id, boss_slug)
);

CREATE TABLE IF NOT EXISTS codex.encounter_abilities (
    ability_id SERIAL PRIMARY KEY,
    encounter_id INTEGER REFERENCES codex.encounters(encounter_id) ON DELETE CASCADE,
    ability_text TEXT NOT NULL,
    display_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS codex.encounter_phases (
    phase_id SERIAL PRIMARY KEY,
    encounter_id INTEGER REFERENCES codex.encounters(encounter_id) ON DELETE CASCADE,
    phase_name VARCHAR(255) NOT NULL,
    description TEXT,
    phase_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS codex.encounter_role_notes (
    note_id SERIAL PRIMARY KEY,
    encounter_id INTEGER REFERENCES codex.encounters(encounter_id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- 'tank', 'healer', 'dps'
    note_text TEXT NOT NULL,
    display_order INTEGER DEFAULT 0
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_encounters_instance ON codex.encounters(instance_id);
CREATE INDEX IF NOT EXISTS idx_abilities_encounter ON codex.encounter_abilities(encounter_id);
CREATE INDEX IF NOT EXISTS idx_phases_encounter ON codex.encounter_phases(encounter_id);
CREATE INDEX IF NOT EXISTS idx_role_notes_encounter ON codex.encounter_role_notes(encounter_id);
CREATE INDEX IF NOT EXISTS idx_role_notes_role ON codex.encounter_role_notes(role);
