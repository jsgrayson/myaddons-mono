--========================================================--
-- SkillWeaver - Stock Manager
-- Monitors consumable inventory and warns when supplies are low
--========================================================--

local ADDON_NAME, SkillWeaver = ...
local StockManager = {}
SkillWeaver.StockManager = StockManager

-- Tracked Consumables (TWW/Midnight Era)
local TRACKED_ITEMS = {
    -- Healing Potions
    {
        name = "Algari Healing Potion",
        ids = {211880, 211879, 211878}, -- Rank 3, 2, 1
        category = "Potion",
        threshold = 5
    },
    -- Healthstones
    {
        name = "Healthstone",
        ids = {5512}, -- Healthstone (all ranks use same ID in TWW)
        category = "Healthstone",
        threshold = 3
    },
    -- Flasks
    {
        name = "Flask of Alchemical Chaos",
        ids = {212283, 212282, 212281},
        category = "Flask",
        threshold = 2
    },
    {
        name = "Flask of Tempered Mastery",
        ids = {212277, 212276, 212275},
        category = "Flask",
        threshold = 2
    },
    -- Food
    {
        name = "The Sushi Special",
        ids = {222720},
        category = "Food",
        threshold = 5
    },
    -- Augment Runes
    {
        name = "Algari Mana Oil",
        ids = {224107},
        category = "Rune",
        threshold = 2
    },
}

------------------------------------------------------------
-- Get count of an item in bags
------------------------------------------------------------
function StockManager:GetItemCount(itemIDs)
    local total = 0
    
    for _, id in ipairs(itemIDs) do
        total = total + (GetItemCount(id) or 0)
    end
    
    return total
end

------------------------------------------------------------
-- Check all consumable stock
-- Returns: { lowItems = {...}, warnings = {...} }
------------------------------------------------------------
function StockManager:CheckStock()
    -- Check if warnings are enabled
    if not SkillWeaver.Settings or not SkillWeaver.Settings.consumables.lowStockWarning then
        return { lowItems = {}, warnings = {} }
    end
    
    local threshold = SkillWeaver.Settings.consumables.lowStockThreshold or 5
    local lowItems = {}
    local warnings = {}
    
    for _, item in ipairs(TRACKED_ITEMS) do
        local count = self:GetItemCount(item.ids)
        
        -- Use item-specific threshold if available, otherwise use global
        local itemThreshold = item.threshold or threshold
        
        if count < itemThreshold then
            table.insert(lowItems, {
                name = item.name,
                category = item.category,
                count = count,
                threshold = itemThreshold
            })
            
            local warning = string.format("|cffFF0000LOW STOCK:|r %s (%d/%d)", 
                item.name, count, itemThreshold)
            table.insert(warnings, warning)
        end
    end
    
    return { lowItems = lowItems, warnings = warnings }
end

------------------------------------------------------------
-- Show warning UI
------------------------------------------------------------
function StockManager:ShowWarning(result)
    if #result.warnings == 0 then
        return
    end
    
    print("|cffFF0000SkillWeaver: Low Consumable Stock!|r")
    for _, warning in ipairs(result.warnings) do
        print("  " .. warning)
    end
    
    -- Play warning sound
    PlaySound(8959) -- RAID_WARNING sound
end

------------------------------------------------------------
-- Perform stock check (called on events)
------------------------------------------------------------
function StockManager:PerformCheck()
    local result = self:CheckStock()
    if #result.lowItems > 0 then
        self:ShowWarning(result)
    end
end

-- Check on login and zone change
local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_ENTERING_WORLD")
f:SetScript("OnEvent", function(self, event)
    C_Timer.After(5, function()
        StockManager:PerformCheck()
    end)
end)

return StockManager
