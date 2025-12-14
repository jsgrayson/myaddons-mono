local addonName = ...
local f = CreateFrame("Frame")

local function Print(msg)
    print("|cffDAA520DP|r |cff00AAFF(BetterBags)|r: " .. msg)
end

local function GetDeepPockets()
    if DeepPockets then return DeepPockets end
    -- Fallback to AceAddon if global is somehow missing but addon is loaded
    if LibStub then
        return LibStub("AceAddon-3.0"):GetAddon("DeepPockets", true)
    end
    return nil
end

local function Init()
    -- 1. Check for BetterBags
    if not C_AddOns.IsAddOnLoaded("BetterBags") then return end
    if not LibStub then return end
    
    local BB = LibStub("AceAddon-3.0"):GetAddon("BetterBags", true)
    if not BB then return end

    local Categories = BB:GetModule('Categories', true)
    if not Categories then return end

    -- 2. Check for DeepPockets Backend
    local DP = GetDeepPockets()
    if not DP then 
        Print("DeepPockets backend not found. Integration disabled.")
        return 
    end

    if type(DP.GetCategoryForItem) ~= "function" then
        Print("DeepPockets API mismatch. GetCategoryForItem missing.")
        return
    end

    -- 3. Register Provider
    -- API: categories:RegisterCategoryFunction(id, func)
    if Categories.RegisterCategoryFunction then
        Categories:RegisterCategoryFunction("DeepPockets", function(data)
             -- data is ItemData info from BetterBags
             local itemID = data.itemInfo.itemID
             if not itemID then return nil end
             
             return DP:GetCategoryForItem(itemID)
        end)
        Print("Category Provider Registered.")
    else
        Print("BetterBags Categories module missing RegisterCategoryFunction API.")
    end
end

f:RegisterEvent("ADDON_LOADED")
f:SetScript("OnEvent", function(_, _, name)
    if name == "DeepPocketsBB_Categories" then
         -- Try init. BetterBags might be loaded before or after.
         -- Use Timer to wait for mostly everything.
         C_Timer.After(1, Init)
    end
end)
