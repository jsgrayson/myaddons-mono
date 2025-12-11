-- Phase 4: Equipment AI & Talent Management

-- Stat Weights Table
-- Stores stat priorities for Equipment Manager
CREATE TABLE IF NOT EXISTS skillweaver.stat_weights (
    weight_id SERIAL PRIMARY KEY,
    spec_id INT NOT NULL, -- WoW Spec ID (e.g., 577 for Havoc)
    content_type VARCHAR(50) NOT NULL, -- 'Raid', 'MythicPlus', 'Delves', 'PvP'
    stat_name VARCHAR(50) NOT NULL, -- 'Crit', 'Haste', 'Mastery', 'Versatility', 'MainStat'
    weight_value DECIMAL(5, 2) NOT NULL, -- e.g., 1.25
    source VARCHAR(50) DEFAULT 'Manual', -- 'IcyVeins', 'SimulationCraft', 'Manual'
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(spec_id, content_type, stat_name)
);

-- Talent Loadouts Table
-- Stores import strings for auto-switching
CREATE TABLE IF NOT EXISTS skillweaver.talent_loadouts (
    loadout_id SERIAL PRIMARY KEY,
    spec_id INT NOT NULL,
    content_type VARCHAR(50) NOT NULL, -- 'Raid', 'MythicPlus', 'Delves', 'PvP'
    loadout_name VARCHAR(100), -- e.g., 'Aldrachi Reaver Raid'
    import_string TEXT NOT NULL,
    source VARCHAR(50) DEFAULT 'Manual', -- 'IcyVeins', 'Wowhead'
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(spec_id, content_type, loadout_name)
);

-- Index for fast lookups
CREATE INDEX idx_stat_weights_spec ON skillweaver.stat_weights(spec_id, content_type);
CREATE INDEX idx_talent_loadouts_spec ON skillweaver.talent_loadouts(spec_id, content_type);
