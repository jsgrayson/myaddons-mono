-- Schema for "The Alt-Army Commander" (Profession Cooldowns)

CREATE TABLE IF NOT EXISTS holocron.profession_cooldowns (
    character_name TEXT NOT NULL,
    realm TEXT NOT NULL,
    profession TEXT NOT NULL,
    spell_name TEXT NOT NULL,
    spell_id INT NOT NULL,
    ready_at TIMESTAMP WITH TIME ZONE,
    charges INT DEFAULT 0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (character_name, realm, spell_id)
);

-- Index for fast lookup of ready cooldowns
CREATE INDEX IF NOT EXISTS idx_cooldowns_ready ON holocron.profession_cooldowns (ready_at);
