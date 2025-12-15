-- dp_ext/betterbags_provider.lua
-- Optional integration: if BetterBags is loaded, register DeepPockets as a category provider.
-- Must be safe: NO hard dependency on BetterBags internals. If BB changes, this should just no-op.

local function SafeGetAddon(name)
  if LibStub then
    local AceAddon = LibStub("AceAddon-3.0", true)
    if AceAddon and AceAddon.GetAddon then
      return AceAddon:GetAddon(name, true)
    end
  end
  return _G[name]
end

local function EnsureDP()
  _G.DeepPockets = _G.DeepPockets or {}
  local DP = _G.DeepPockets
  DP.API = DP.API or {}
  return DP
end

local function ItemToCategory(itemID)
  local DP = EnsureDP()
  if DP.API and type(DP.API.GetItemCategory) == "function" then
    return DP.API.GetItemCategory(itemID)
  end
  return nil
end

local function TryRegister()
  local BB = SafeGetAddon("BetterBags")
  if not BB then return end

  -- Prefer a Categories module if it exists (AceAddon style).
  local Categories = (type(BB.GetModule) == "function") and BB:GetModule("Categories", true) or nil

  -- Provider function signature varies by version; we accept either itemID or an itemData table.
  local function Provider(arg1, arg2)
    -- Common patterns:
    -- 1) Provider(itemID)
    -- 2) Provider(itemData) where itemData.itemID exists
    -- 3) Provider(bagID, slotID) -> we can’t safely resolve here, so ignore
    local itemID = nil
    if type(arg1) == "number" then
      itemID = arg1
    elseif type(arg1) == "table" then
      itemID = arg1.itemID or arg1.id
    end

    if not itemID then return nil end
    return ItemToCategory(itemID) -- string category name (e.g. "Miscellaneous")
  end

  -- Try a few likely registration APIs (no-ops if missing).
  if Categories then
    if type(Categories.RegisterCategoryProvider) == "function" then
      -- Example: Categories:RegisterCategoryProvider("DeepPockets", providerFn)
      pcall(Categories.RegisterCategoryProvider, Categories, "DeepPockets", Provider)
      return
    end
    if type(Categories.RegisterExternalCategoryProvider) == "function" then
      pcall(Categories.RegisterExternalCategoryProvider, Categories, "DeepPockets", Provider)
      return
    end
    if type(Categories.AddCategoryProvider) == "function" then
      pcall(Categories.AddCategoryProvider, Categories, "DeepPockets", Provider)
      return
    end
  end

  -- Some builds may expose it on BB directly.
  if type(BB.RegisterCategoryProvider) == "function" then
    pcall(BB.RegisterCategoryProvider, BB, "DeepPockets", Provider)
    return
  end
end

-- Register after PLAYER_LOGIN so BB has finished booting in most cases.
local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_LOGIN")
f:SetScript("OnEvent", function()
  -- only attempt once
  TryRegister()
end)
