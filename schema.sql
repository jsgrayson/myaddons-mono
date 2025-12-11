-- PetWeaver SQL Schema
-- Using SQLite for simplicity and portability
-- This provides massive performance gains over JSON files

-- Pet Collection Table
CREATE TABLE IF NOT EXISTS pets (
    pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
    species_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    level INTEGER DEFAULT 1,
    quality INTEGER DEFAULT 1, -- 1=Poor, 2=Common, 3=Uncommon, 4=Rare, 5=Epic, 6=Legendary
    breed_id INTEGER,
    health INTEGER,
    power INTEGER,
    speed INTEGER,
    is_favorite BOOLEAN DEFAULT 0,
    custom_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pets_species ON pets(species_id);
CREATE INDEX IF NOT EXISTS idx_pets_level ON pets(level);
CREATE INDEX IF NOT EXISTS idx_pets_quality ON pets(quality);
CREATE INDEX IF NOT EXISTS idx_pets_name ON pets(name);

-- Pet Species Master Data
CREATE TABLE IF NOT EXISTS species (
    species_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    pet_type INTEGER, -- Family: 1=Humanoid, 2=Dragonkin, etc.
    can_battle BOOLEAN DEFAULT 1,
    is_tradable BOOLEAN DEFAULT 0,
    source_text TEXT,
    icon TEXT
);

CREATE INDEX IF NOT EXISTS idx_species_name ON species(name);
CREATE INDEX IF NOT EXISTS idx_species_type ON species(pet_type);

-- Strategies Table
CREATE TABLE IF NOT EXISTS strategies (
    strategy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    encounter_id INTEGER NOT NULL,
    encounter_name TEXT NOT NULL,
    expansion TEXT,
    category TEXT,
    pet1_species INTEGER,
    pet1_name TEXT,
    pet2_species INTEGER,
    pet2_name TEXT,
    pet3_species INTEGER,
    pet3_name TEXT,
    win_rate REAL DEFAULT 0.0,
    script TEXT, -- Xu-Fu script
    notes TEXT,
    is_verified BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_strategies_encounter ON strategies(encounter_id);
CREATE INDEX IF NOT EXISTS idx_strategies_expansion ON strategies(expansion);
CREATE INDEX IF NOT EXISTS idx_strategies_pet1 ON strategies(pet1_species);
CREATE INDEX IF NOT EXISTS idx_strategies_pet2 ON strategies(pet2_species);
CREATE INDEX IF NOT EXISTS idx_strategies_pet3 ON strategies(pet3_species);

-- User's Ready Strategies (Matched)
CREATE TABLE IF NOT EXISTS ready_strategies (
    ready_id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_id INTEGER NOT NULL,
    user_has_pet1 BOOLEAN DEFAULT 0,
    user_has_pet2 BOOLEAN DEFAULT 0,
    user_has_pet3 BOOLEAN DEFAULT 0,
    is_complete BOOLEAN DEFAULT 0,
    priority INTEGER DEFAULT 0,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (strategy_id) REFERENCES strategies(strategy_id)
);

CREATE INDEX IF NOT EXISTS idx_ready_complete ON ready_strategies(is_complete);
CREATE INDEX IF NOT EXISTS idx_ready_priority ON ready_strategies(priority DESC);

-- Encounters Table
CREATE TABLE IF NOT EXISTS encounters (
    encounter_id INTEGER PRIMARY KEY,
    npc_name TEXT NOT NULL,
    zone TEXT,
    expansion TEXT,
    category TEXT,
    difficulty INTEGER DEFAULT 1,
    is_daily BOOLEAN DEFAULT 0,
    is_weekly BOOLEAN DEFAULT 0,
    rewards TEXT -- JSON blob for rewards
);

CREATE INDEX IF NOT EXISTS idx_encounters_expansion ON encounters(expansion);
CREATE INDEX IF NOT EXISTS idx_encounters_zone ON encounters(zone);

-- Combat Logs Table
CREATE TABLE IF NOT EXISTS combat_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    encounter_id INTEGER,
    result TEXT NOT NULL, -- 'WIN' or 'LOSS'
    duration_seconds INTEGER,
    rounds INTEGER,
    pet1_species INTEGER,
    pet2_species INTEGER,
    pet3_species INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (encounter_id) REFERENCES encounters(encounter_id)
);

CREATE INDEX IF NOT EXISTS idx_combat_timestamp ON combat_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_combat_result ON combat_logs(result);
CREATE INDEX IF NOT EXISTS idx_combat_encounter ON combat_logs(encounter_id);

-- Market Data Table
CREATE TABLE IF NOT EXISTS market_prices (
    price_id INTEGER PRIMARY KEY AUTOINCREMENT,
    species_id INTEGER NOT NULL,
    pet_name TEXT,
    price_copper INTEGER NOT NULL,
    server TEXT DEFAULT 'Unknown',
    region TEXT DEFAULT 'US',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (species_id) REFERENCES species(species_id)
);

CREATE INDEX IF NOT EXISTS idx_market_species ON market_prices(species_id);
CREATE INDEX IF NOT EXISTS idx_market_timestamp ON market_prices(timestamp DESC);

-- Wishlist Table  
CREATE TABLE IF NOT EXISTS wishlist (
    wishlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    species_id INTEGER NOT NULL,
    pet_name TEXT,
    breed_id INTEGER,
    breed_name TEXT,
    priority INTEGER DEFAULT 1,
    notes TEXT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (species_id) REFERENCES species(species_id)
);

CREATE INDEX IF NOT EXISTS idx_wishlist_species ON wishlist(species_id);
CREATE INDEX IF NOT EXISTS idx_wishlist_priority ON wishlist(priority DESC);

-- Analytics/Stats View
CREATE VIEW IF NOT EXISTS collection_stats AS
SELECT 
    COUNT(*) as total_pets,
    COUNT(DISTINCT species_id) as unique_species,
    SUM(CASE WHEN level = 25 THEN 1 ELSE 0 END) as max_level,
    SUM(CASE WHEN quality >= 4 THEN 1 ELSE 0 END) as rare_or_better,
    AVG(level) as avg_level
FROM pets;

-- Ready Strategies Summary View
CREATE VIEW IF NOT EXISTS ready_summary AS
SELECT 
    expansion,
    category,
    COUNT(*) as total_ready,
    SUM(CASE WHEN is_complete = 1 THEN 1 ELSE 0 END) as fully_ready
FROM ready_strategies rs
JOIN strategies s ON rs.strategy_id = s.strategy_id
GROUP BY expansion, category;
