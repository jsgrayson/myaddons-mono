-- DeepPockets
-- Backend-only Item Database & Search
-- Author: DeepPockets Team
-- Version: 0.2.0 (Backend Refactor)

local ADDON_NAME, namespace = ...
local DP = {}
_G.DeepPockets = DP

-- =============================================================
-- CONFIG & CONSTANTS
-- =============================================================
local DB_VERSION = 2
local MAX_CONTAINER_INDEX = 5 -- 0-4 (Backpack + 4 Bags)
-- We can expand to Bank/ReagentBank later if requested

-- =============================================================
-- UTILITIES
-- =============================================================
local function dprint(...)
    if DeepPocketsDB and DeepPocketsDB.debug then
        print("|cffDAA520DP|r:", ...)
    end
end

local function Print(msg)
    print("|cffDAA520DeepPockets|r: " .. tostring(msg))
end

-- =============================================================
-- DATABASE INITIALIZATION
-- =============================================================
local function InitDB()
    if not DeepPocketsDB then
        DeepPocketsDB = {}
    end
    
    -- Version Check / Migration (Wipe for now on major change)
    if not DeepPocketsDB.version or DeepPocketsDB.version < DB_VERSION then
        DeepPocketsDB = {
            version = DB_VERSION,
            debug = false,
            settings = {
                autoScan = true,
            },
            snapshot = {},  -- Raw scan data
            index = {},     -- Derived index
        }
        Print("Database upgraded/reset to v" .. DB_VERSION)
    end
    
    -- Ensure structure integrity
    DeepPocketsDB.snapshot = DeepPocketsDB.snapshot or {}
    DeepPocketsDB.index = DeepPocketsDB.index or {}
    DeepPocketsDB.settings = DeepPocketsDB.settings or { autoScan = true }
end

-- =============================================================
-- CORE: SCANNING
-- =============================================================
local C_Cont = C_Container

local function GetContainerInfo(bagID, slotID)
    local info = C_Cont.GetContainerItemInfo(bagID, slotID)
    if not info then return nil end
    
    -- Normalize data for snapshot
    -- We store minimal data necessary for search/categorization
    return {
        bag = bagID,
        slot = slotID,
        itemID = info.itemID,
        hyperlink = info.hyperlink,
        stackCount = info.stackCount or 1,
        quality = info.quality,
        isBound = info.isBound,
        iconFileID = info.iconFileID,
    }
end

function DP:ScanBags()
    InitDB()
    local snapshot = {}
    local count = 0
    
    for bag = 0, MAX_CONTAINER_INDEX do
        local numSlots = C_Cont.GetContainerNumSlots(bag)
        for slot = 1, numSlots do
            local itemData = GetContainerInfo(bag, slot)
            if itemData then
                count = count + 1
                table.insert(snapshot, itemData)
            end
        end
    end
    
    DeepPocketsDB.snapshot = snapshot
    DeepPocketsDB.lastScan = time()
    dprint("Scan complete. Items found:", count)
    
    -- Auto-rebuild index after scan
    DP:RebuildIndex()
    
    return count
end

-- =============================================================
-- CORE: INDEXING
-- =============================================================
-- Tokenize string for search
local function Tokenize(str)
    local tokens = {}
    for word in string.gmatch(str:lower(), "%S+") do
        if #word > 2 then -- Ignore tiny words
            table.insert(tokens, word)
        end
    end
    return tokens
end

function DP:RebuildIndex()
    if not DeepPocketsDB or not DeepPocketsDB.snapshot then return end
    
    local idx = {
        by_item = {},    -- itemID -> { total=N, locs={} }
        search = {},     -- token -> { itemID -> true }
        by_cat = {},     -- cat -> subcat -> { itemIDs... }
    }
    
    for _, item in ipairs(DeepPocketsDB.snapshot) do
        local iid = item.itemID
        local count = item.stackCount or 1
        
        -- 1. By Item Count
        if not idx.by_item[iid] then
            idx.by_item[iid] = { total = 0, locs = {} }
        end
        idx.by_item[iid].total = idx.by_item[iid].total + count
        table.insert(idx.by_item[iid].locs, { bag=item.bag, slot=item.slot, count=count })
        
        -- 2. Search Index (Name)
        local name = C_Item.GetItemNameByID(iid)
        if name then
            local tokens = Tokenize(name)
            for _, token in ipairs(tokens) do
                if not idx.search[token] then idx.search[token] = {} end
                idx.search[token][iid] = true
            end
        end
        
        -- 3. Category (Basic Class/Subclass)
        -- This requires item data to be cached by client. 
        -- If missing, we skip for now (async issues are complex for backend-only simple scan)
        local _, _, _, _, _, class, subclass = C_Item.GetItemInfo(item.hyperlink)
        if class and subclass then
            idx.by_cat[class] = idx.by_cat[class] or {}
            idx.by_cat[class][subclass] = idx.by_cat[class][subclass] or {}
            idx.by_cat[class][subclass][iid] = true
        end
    end
    
    DeepPocketsDB.index = idx
    DeepPocketsDB.lastIndex = time()
    dprint("Index rebuilt.")
end

-- =============================================================
-- API
-- =============================================================
function DP:GetDB()
    return DeepPocketsDB
end

function DP:GetIndex()
    if not DeepPocketsDB then return nil end
    return DeepPocketsDB.index
end

-- Returns list of ItemIDs matching query
function DP:Search(query)
    if not query or #query < 3 then return {} end
    if not DeepPocketsDB or not DeepPocketsDB.index or not DeepPocketsDB.index.search then return {} end
    
    local tokens = Tokenize(query)
    local results = {} 
    
    -- AND logic: item must match ALL tokens
    -- For simplicity, just grab first token's matches and filter
    -- (A full inverted index intersection is better but this is simple Lua)
    
    -- Collect candidate itemIDs from first token
    local firstToken = tokens[1]
    local searchIdx = DeepPocketsDB.index.search
    
    if not searchIdx[firstToken] then return {} end
    
    -- Start with candidates from first token
    local candidates = {}
    for iid, _ in pairs(searchIdx[firstToken]) do
        candidates[iid] = true
    end
    
    -- Filter by remaining tokens
    for i = 2, #tokens do
        local note = tokens[i]
        local nextSet = searchIdx[note]
        if not nextSet then return {} end -- Token matches nothing, so AND fails
        
        for iid, _ in pairs(candidates) do
            if not nextSet[iid] then
                candidates[iid] = nil -- Prune
            end
        end
    end
    
    -- Convert map to list
    local list = {}
    for iid, _ in pairs(candidates) do
        table.insert(list, iid)
    end
    return list
end

function DP:GetItemTotals(itemID)
    if not DeepPocketsDB or not DeepPocketsDB.index or not DeepPocketsDB.index.by_item then return 0 end
    local entry = DeepPocketsDB.index.by_item[itemID]
    if entry then return entry.total end
    return 0
end

-- =============================================================
-- SLASH COMMANDS
-- =============================================================
SLASH_DEEPPOCKETS1 = "/dp"
SlashCmdList["DEEPPOCKETS"] = function(msg)
    local cmd, arg = msg:lower():match("^(%S+)%s*(.*)")
    cmd = cmd or ""
    
    if cmd == "scan" then
        local count = DP:ScanBags()
        Print("Scanned " .. count .. " items.")
        
    elseif cmd == "rebuild" then
        DP:RebuildIndex()
        Print("Index force-rebuilt.")
        
    elseif cmd == "dump" then
        if not DeepPocketsDB then Print("DB not init.") return end
        local snap = #DeepPocketsDB.snapshot
        local idxItems = 0
        if DeepPocketsDB.index and DeepPocketsDB.index.by_item then
            for _ in pairs(DeepPocketsDB.index.by_item) do idxItems = idxItems + 1 end
        end
        Print("Stats:")
        Print("- Snapshot Size: " .. snap)
        Print("- Unique Items: " .. idxItems)
        Print("- Last Scan: " .. (DeepPocketsDB.lastScan or "Never"))
        
    elseif cmd == "sanity" then
        -- Simple check
        if not DeepPocketsDB then Print("FAIL: No DB") return end
        if not DeepPocketsDB.snapshot then Print("FAIL: No Snapshot") return end
        Print("Sanity Check OK. DB Version: " .. (DeepPocketsDB.version or "Unknown"))
        
    elseif cmd == "search" then
        if #arg < 3 then Print("Search too short.") return end
        local res = DP:Search(arg)
        Print("Search results for '"..arg.."': " .. #res)
        for _, iid in ipairs(res) do
            local name = C_Item.GetItemNameByID(iid) or ("Item " .. iid)
            print(" - " .. name)
        end
        
    else
        Print("Commands: /dp scan, /dp rebuild, /dp dump, /dp sanity, /dp search <query>")
    end
end

-- =============================================================
-- EVENTS
-- =============================================================
local f = CreateFrame("Frame")
f:RegisterEvent("ADDON_LOADED")
f:RegisterEvent("PLAYER_LOGIN")
f:RegisterEvent("BAG_UPDATE_DELAYED")

f:SetScript("OnEvent", function(self, event, arg1)
    if event == "ADDON_LOADED" and arg1 == ADDON_NAME then
        InitDB()
    elseif event == "PLAYER_LOGIN" then
        dprint("Player Login. Ready.")
    elseif event == "BAG_UPDATE_DELAYED" then
        if DeepPocketsDB and DeepPocketsDB.settings.autoScan then
            DP:ScanBags()
        end
    end
end)
