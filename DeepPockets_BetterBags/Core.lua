-- DeepPockets_BetterBags
-- Integration Bridge
-- Connects DeepPockets (Backend) -> BetterBags (UI)

local ADDON_NAME = ...
local DP = _G.DeepPockets
local BB = _G.BetterBags

if not DP or not BB then
    print("|cffDAA520DP_BB|r: Missing Dependency (DP or BB).")
    return
end

local Frame = CreateFrame("Frame")
local NewItems = {} -- Cache of { bag:slot -> true } for fast overlay lookup

-- =============================================================
-- UTILITIES
-- =============================================================
local function UpdateNewItemCache()
    NewItems = {}
    local snap = DP:GetInventory()
    for _, item in ipairs(snap) do
        if item.isNew then
            local k = item.bag .. ":" .. item.slot
            NewItems[k] = true
        end
    end
end

-- =============================================================
-- EVENT HANDLING
-- =============================================================
-- Listen to DeepPockets backend events
DP:RegisterCallback(DP.Events.SCAN_FINISHED, function(count)
    UpdateNewItemCache()
    
    -- Trigger UI Refresh in BetterBags if needed
    -- For now, we rely on BetterBags' own update cycle or force it if we want instant badges
    -- But since bag update triggered the scan, BetterBags is likely updating too.
    -- We just need to make sure our hooks read from the fresh cache.
end)

DP:RegisterCallback(DP.Events.DELTA_UPDATED, function(delta)
    -- Optional: Chat spam for debug
    -- print("DP_BB: Delta updated.")
end)

-- =============================================================
-- HOOKS: ITEM BUTTON OVERLAY
-- =============================================================
-- BetterBags buttons usually have a container Item impl. 
-- We need to find where the item button updates.
-- BetterBags exposes 'BetterBags.ItemButton' class-like table? 
-- Or we hook the frames creation. It's safe to use hooksecurefunc on the XML template or mixin if accessible.
-- For a safe "Phase 1", let's assume we can loop visible frames or hook the specific mixin method.
-- "BetterBags.Inventory.Item" is a common path if using the Lua API.

-- Simple Approach:
-- Hook the ItemButton:SetItem method if available, or hook the underlying Update function.
-- Since we don't have the BB source code docs in front of us, we'll try a generic hook strategy 
-- or wait for the user to verify specifics. Safe guess:
-- BetterBags buttons often inherit from some mixin.

-- Let's define a badge provider function
local function UpdateButtonBadge(button)
    if not button or not button.GetBagID or not button.GetSlotID then return end
    
    local bag = button:GetBagID()
    local slot = button:GetSlotID()
    local key = bag .. ":" .. slot
    
    if NewItems[key] then
        -- SHOW BADGE
        -- Create texture if missing
        if not button.dpNewBadge then
            button.dpNewBadge = button:CreateTexture(nil, "OVERLAY")
            button.dpNewBadge:SetTexture("Interface\\AddOns\\DeepPockets_BetterBags\\assets\\new_badge") 
            -- Fallback to standard interface icon if asset missing
            if not button.dpNewBadge:GetTexture() then
               button.dpNewBadge:SetColorTexture(0, 1, 0, 0.5) -- Green glow overlay
            end
            button.dpNewBadge:SetPoint("TOPRIGHT", -2, -2)
            button.dpNewBadge:SetSize(10, 10)
        end
        button.dpNewBadge:Show()
    else
        -- HIDE BADGE
        if button.dpNewBadge then button.dpNewBadge:Hide() end
    end
end

-- Hooking Strategy:
-- We'll use a timer to hook frames lazily or try to hook a known global/library. 
-- For now, let's assume we can scan frames or hook `ContainerFrame_Update` style logic? 
-- BetterBags likely uses `CallbackRegistry` or `LibWindow`?
-- Let's TRY to hook `BetterBags` global function if exposed. 
-- OR, use a crude frame scan for now (Phase 1).

-- A safer bet for BetterBags (which uses a pool of frames):
-- hooksecurefunc(BetterBags.Themes.Simple.Item, "SetItem", ...) -- HYPOTHETICAL
-- Let's stick to the Tooltip hook first as it's 100% standard API.
-- And generic Frame hook for buttons.

-- =============================================================
-- HOOKS: TOOLTIP
-- =============================================================
TooltipDataProcessor.AddTooltipPostCall(Enum.TooltipDataType.Item, function(tooltip, data)
    if not data or not data.id then return end
    
    local itemID = data.id -- This is ItemID. We need bag/slot for context?
    -- Sometimes tooltip doesn't have bag/slot info easily.
    -- DeepPockets has history by "Key". If we have GUID-based history, we can check by GUID if available.
    
    local _, link = tooltip:GetItem()
    if not link then return end
    
    -- Try to find this item in our history by some means.
    -- Since we only have ItemID here easily, we might just show "Seen X times" totals from Index.
    
    -- But for "New" status, we tracked it by Bag:Slot or Key.
    -- If we can get owner, we can check.
    local owner = tooltip:GetOwner()
    if owner and owner.GetBagID and owner.GetSlotID then
        local bag = owner:GetBagID()
        local slot = owner:GetSlotID()
        local key = bag .. ":" .. slot
        
        if NewItems[key] then
            tooltip:AddLine("|cff00FF00DeepPockets: NEW!|r")
        end
    end
    
    -- Show Totals (from Index)
    local total = DP:GetItemTotals(itemID)
    if total > 0 then
         tooltip:AddLine("|cffDAA520DeepPockets:|r Own " .. total)
    end
end)

print("|cffDAA520DP_BB|r: Integration Loaded.")
