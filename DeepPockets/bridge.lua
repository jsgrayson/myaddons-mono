-- dp_bb_bridge.lua
-- DeepPockets → BetterBags backend bridge
-- Safe: no UI, no frames, no hooks into item buttons

local ADDON, DP = ...
local BB = _G.BetterBags

if not BB then
    print("|cffff8800DeepPockets|r BetterBags not detected, bridge idle")
    return
end

-- Register a passive provider
local Provider = BB:NewModule("DeepPockets_Backend")

-- Called by BetterBags during refresh
function Provider:GetCategories()
    -- Return empty table for now (we layer later)
    return {}
end

-- Optional: expose backend data to BB plugins
function Provider:GetItemData(itemLink)
    if not itemLink then return nil end

    -- Example backend hooks (already working in DP)
    local data = {}

    if DP and DP.GetItemUpgradeInfo then
        data.upgrade = DP:GetItemUpgradeInfo(itemLink)
    end

    if DP and DP.GetItemFlags then
        data.flags = DP:GetItemFlags(itemLink)
    end

    return data
end

-- Register provider
BB:RegisterProvider("DeepPockets", Provider)

print("|cff00ff00DeepPockets|r BetterBags bridge active")
