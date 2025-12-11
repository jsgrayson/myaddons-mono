-- SQL Schema for GoblinAI Historical Training Data
-- Run this to create tables for storing news events and correlations

-- News events table
CREATE TABLE IF NOT EXISTS auctionhouse.news_events (
    event_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    source TEXT NOT NULL,  -- wowhead, mmochampion, blizzard
    title TEXT NOT NULL,
    content TEXT,
    event_type TEXT,  -- class_change, raid, patch, holiday, profession
    affected_classes TEXT[],
    affected_items INT[],
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_news_events_timestamp ON auctionhouse.news_events(timestamp);
CREATE INDEX idx_news_events_type ON auctionhouse.news_events(event_type);

-- Scans table (if not exists)
CREATE TABLE IF NOT EXISTS auctionhouse.scans (
    scan_id SERIAL PRIMARY KEY,
    realm TEXT NOT NULL,
    faction TEXT NOT NULL,
    character TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    item_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_scans_timestamp ON auctionhouse.scans(timestamp);

-- Scan items table (if not exists)
CREATE TABLE IF NOT EXISTS auctionhouse.scan_items (
    scan_item_id SERIAL PRIMARY KEY,
    scan_id INT REFERENCES auctionhouse.scans(scan_id),
    item_id INT NOT NULL,
    price BIGINT NOT NULL,  -- Copper
    quantity INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_scan_items_item_id ON auctionhouse.scan_items(item_id);
CREATE INDEX idx_scan_items_scan_id ON auctionhouse.scan_items(scan_id);

-- Event-price correlations (training results)
CREATE TABLE IF NOT EXISTS auctionhouse.event_correlations (
    correlation_id SERIAL PRIMARY KEY,
    event_id INT REFERENCES auctionhouse.news_events(event_id),
    item_id INT NOT NULL,
    baseline_price BIGINT,
    peak_price BIGINT,
    price_change_pct DECIMAL(10, 2),
    peak_time_hours DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_event_correlations_event ON auctionhouse.event_correlations(event_id);
CREATE INDEX idx_event_correlations_item ON auctionhouse.event_correlations(item_id);

-- Example: Insert a historical news event
-- INSERT INTO auctionhouse.news_events 
--   (timestamp, source, title, event_type, affected_items)
-- VALUES 
--   ('2024-08-15 10:00:00', 'wowhead', 'Fire Mage Buffed in Patch 11.0.2', 
--    'class_change', ARRAY[210814, 211515]);

COMMENT ON TABLE auctionhouse.news_events IS 'Historical WoW news events for ML training';
COMMENT ON TABLE auctionhouse.event_correlations IS 'Trained correlations between events and price movements';
