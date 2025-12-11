-- MIRROR SCHEMA (Configuration Sync)
CREATE SCHEMA IF NOT EXISTS mirror;

-- Trusted Devices (Hardware Identity)
CREATE TABLE IF NOT EXISTS mirror.trusted_devices (
    device_id SERIAL PRIMARY KEY,
    hostname VARCHAR(100) UNIQUE NOT NULL, -- e.g., "DESKTOP-MAIN", "STEAMDECK"
    device_type VARCHAR(20) DEFAULT 'DESKTOP', -- 'DESKTOP', 'HANDHELD'
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Config Profiles (The "Vault")
CREATE TABLE IF NOT EXISTS mirror.config_profiles (
    profile_id SERIAL PRIMARY KEY,
    character_guid VARCHAR(50), -- 'GLOBAL' or specific GUID
    device_type VARCHAR(20), -- 'DESKTOP' or 'HANDHELD'
    file_type VARCHAR(50), -- 'MACROS', 'BINDINGS'
    content TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(character_guid, device_type, file_type)
);

-- Initial Seed for Testing
INSERT INTO mirror.trusted_devices (hostname, device_type) 
VALUES ('DESKTOP-TEST', 'DESKTOP')
ON CONFLICT (hostname) DO NOTHING;
