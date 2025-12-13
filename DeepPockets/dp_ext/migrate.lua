-- dp_ext/migrate.lua
local ADDON_NAME, ns = ...
local DP = _G.DeepPockets
DP.Migrate = {}

-- DB Contract:
-- inventory = { ["bag:slot"] = itemRecord }
-- index = { by_category = { ["Cat"]={keys...} }, by_itemID = { [id]={keys...} } }

local DB_VERSION = 1 -- Spec says 1. We reset if mismatch.

local DEFAULT_DB = {
    version = DB_VERSION,
    settings = { enabled = true, debug = false },
    meta = { lastScan = 0, lastFullScan = 0 },
    inventory = {},
    index = {
        by_category = {},
        by_itemID = {},
    }
}

function DP.Migrate.Ensure()
    if not DeepPocketsDB or not DeepPocketsDB.version or DeepPocketsDB.version ~= DB_VERSION then
        -- Hard reset for strict alignment
        DeepPocketsDB = CopyTable(DEFAULT_DB)
        -- Could preserve settings here if needed, but clean slate is safer for this refactor
    end
    
    -- Ensure tables exist
    DeepPocketsDB.settings = DeepPocketsDB.settings or { enabled = true, debug = false }
    DeepPocketsDB.meta = DeepPocketsDB.meta or {}
    DeepPocketsDB.inventory = DeepPocketsDB.inventory or {}
    DeepPocketsDB.index = DeepPocketsDB.index or {}
    DeepPocketsDB.index.by_category = DeepPocketsDB.index.by_category or {}
    DeepPocketsDB.index.by_itemID = DeepPocketsDB.index.by_itemID or {}
end
