-- dp_ext/index.lua
local ADDON_NAME, ns = ...
local DP = _G.DeepPockets
DP.Index = {}

function DP.Index.Rebuild()
    DP.Migrate.Ensure()
    local db = DeepPocketsDB
    
    wipe(db.index.by_category)
    wipe(db.index.by_itemID)
    
    for key, record in pairs(db.inventory) do
        local cat = record.category or "Miscellaneous"
        local itemID = record.itemID
        
        -- By Category
        if not db.index.by_category[cat] then
            db.index.by_category[cat] = {}
        end
        table.insert(db.index.by_category[cat], key)
        
        -- By ItemID
        if itemID then
            if not db.index.by_itemID[itemID] then
                db.index.by_itemID[itemID] = {}
            end
            table.insert(db.index.by_itemID[itemID], key)
        end
    end
    
    -- Notify listeners
    if DP.API and DP.API.NotifyListeners then
        DP.API.NotifyListeners("INDEX_UPDATED")
    end
end
