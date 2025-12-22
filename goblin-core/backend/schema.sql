-- 1. REALM CONSTANTS
CREATE TABLE IF NOT EXISTS global_constants (
    key TEXT PRIMARY KEY, -- 'WOW_TOKEN', 'LAST_SCAN_TIME'
    value_json JSONB,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. ITEM DATABASE (The Source of Truth)
CREATE TABLE IF NOT EXISTS item_pricing (
    item_id INT PRIMARY KEY,
    name TEXT,
    icon_url TEXT,
    
    -- PRICING VECTORS
    market_value_local BIGINT,    -- From TSM
    min_buyout_remote BIGINT,     -- From Blizzard API
    region_avg_daily BIGINT,      -- From Blizzard API
    
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. WARBAND INVENTORY (The Assets)
CREATE TABLE IF NOT EXISTS inventory_state (
    guid TEXT,             -- 'Player-123-0A...' or 'Warbank-Tab-1'
    container_type TEXT,   -- 'BAG', 'BANK', 'WARBANK', 'MAIL'
    slot_id INT,
    item_id INT,
    quantity INT,
    ilvl INT,
    
    -- LOGISTICS
    is_warbound BOOLEAN DEFAULT FALSE,
    target_recipient TEXT, -- 'Alt_Warrior' (If pending transfer)
    
    PRIMARY KEY (guid, container_type, slot_id)
);

-- 4. TRADE ROUTES (Pending Orders)
CREATE TABLE IF NOT EXISTS logistics_manifest (
    id SERIAL PRIMARY KEY,
    source_char TEXT,
    target_char TEXT,
    item_id INT,
    action_type TEXT, -- 'MAIL', 'WARBANK_DEPOSIT'
    status TEXT DEFAULT 'PENDING'
);
