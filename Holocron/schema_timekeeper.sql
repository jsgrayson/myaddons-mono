-- TIMEKEEPER SCHEMA (Analytics)
CREATE SCHEMA IF NOT EXISTS timekeeper;

CREATE TABLE IF NOT EXISTS timekeeper.session_history (
    session_id SERIAL PRIMARY KEY,
    character_guid VARCHAR(50),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    start_gold BIGINT,
    end_gold BIGINT,
    items_looted_json TEXT, -- JSON array of item IDs
    net_worth_delta BIGINT
);
