--========================================================--
-- SkillWeaver - Trinket Manager
-- Automates usage of On-Use Trinkets (Slots 13 & 14)
--========================================================--

local ADDON_NAME, SkillWeaver = ...
local TrinketManager = {}
SkillWeaver.TrinketManager = TrinketManager

-- Configuration
TrinketManager.Config = {
    SyncWithBurst = true,    -- Only use DPS trinkets during burst windows
    UseDefensive = true,     -- Auto-use defensive trinkets (low priority, usually manual is better)
    HPThreshold = 30,        -- HP % to use defensive trinkets
}

-- Known Defensive Trinkets (Do not use for DPS)
local DEFENSIVE_TRINKETS = {
    [123456] = true, -- Example ID
    -- Add more IDs as discovered
}

------------------------------------------------------------
-- Check if a trinket is ready and usable
------------------------------------------------------------
function TrinketManager:CanUseTrinket(slotID)
    local itemID = GetInventoryItemID("player", slotID)
    if not itemID then return false end

    -- Check if it has an On-Use effect
    local spellName, spellID = GetItemSpell(itemID)
    if not spellName then return false end -- Passive trinket

    -- Check Cooldown
    local start, duration, enable = GetItemCooldown(itemID)
    if start > 0 and duration > 1.5 then return false end
    if enable == 0 then return false end

    -- Check if Defensive (and skip if we are looking for DPS)
    if DEFENSIVE_TRINKETS[itemID] then return "Defensive" end

    return "DPS"
end

------------------------------------------------------------
-- Get Trinket Action
-- @param context: "Burst" (Major CD active), "Execute", "Defensive", "General"
------------------------------------------------------------
function TrinketManager:GetTrinketAction(context)
    -- Slot 13 (Top Trinket)
    local type1 = self:CanUseTrinket(13)
    if type1 then
        if context == "Burst" and type1 == "DPS" then
            return { command = "/use 13", description = "Trinket 1 (Burst)" }
        elseif context == "Defensive" and type1 == "Defensive" then
            return { command = "/use 13", description = "Trinket 1 (Defensive)" }
        end
    end

    -- Slot 14 (Bottom Trinket)
    local type2 = self:CanUseTrinket(14)
    if type2 then
        if context == "Burst" and type2 == "DPS" then
            return { command = "/use 14", description = "Trinket 2 (Burst)" }
        elseif context == "Defensive" and type2 == "Defensive" then
            return { command = "/use 14", description = "Trinket 2 (Defensive)" }
        end
    end

    return nil
end

return TrinketManager
