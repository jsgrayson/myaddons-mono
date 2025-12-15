-- dp_ext/betterbags_categories.lua
DeepPockets = DeepPockets or {}
DeepPockets.API = DeepPockets.API or {}

local function TryRegisterWithBetterBags()
  if not LibStub then return false end

  local AceAddon = LibStub("AceAddon-3.0", true)
  if not AceAddon then return false end

  -- BetterBags addon object (not global _G.BetterBags)
  local BB = AceAddon:GetAddon("BetterBags", true)
  if not BB then return false end

  -- Categories module (name is “Categories” in BetterBags)
  local Categories = BB.GetModule and BB:GetModule("Categories", true) or nil
  if not Categories or type(Categories.RegisterCategoryFunction) ~= "function" then
    return false
  end

  -- Register once; BetterBags will cache results per-item.
  Categories:RegisterCategoryFunction("DeepPockets", function(data)
    -- data.itemInfo.itemID is the standard in BetterBags item data
    local itemID = data and data.itemInfo and data.itemInfo.itemID
    if not itemID then return nil end

    -- IMPORTANT: returning nil means “no opinion”; returning string sets category.
    -- We always return a bucket string for now.
    return DeepPockets.API.GetItemCategory(itemID, data.itemInfo.itemLink)
  end)

  -- Optional breadcrumb so we can confirm it’s actually wired (keep it short)
  if not DeepPockets._BB_CAT_HOOKED then
    DeepPockets._BB_CAT_HOOKED = true
    print("|cff00ff00DeepPockets|r: Registered categories with BetterBags.")
  end

  return true
end

-- Attempt immediately (works if BetterBags already loaded)
TryRegisterWithBetterBags()

-- Also retry when addons load (covers load order)
local f = CreateFrame("Frame")
f:RegisterEvent("ADDON_LOADED")
f:SetScript("OnEvent", function(_, _, name)
  if name == "BetterBags" then
    TryRegisterWithBetterBags()
  end
end)
