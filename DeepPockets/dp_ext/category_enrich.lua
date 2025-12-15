-- ================================
-- FILE: dp_ext/category_enrich.lua
-- PURPOSE: Category enrichment layer (NO UI, NO BB fork)
-- LOAD ORDER: AFTER category_api.lua, BEFORE DeepPockets.lua
-- ================================

-- Preconditions (do NOT recreate globals)
if not _G.DeepPockets or not _G.DeepPockets.API then return end

local API = _G.DeepPockets.API

-- Guard: do not overwrite if already implemented
if API.GetItemCategoryEx then return end

-- Cache to avoid recomputation
local cache = {}

-- Enriched category info (non-breaking)
-- Returns a TABLE, not a string
-- Existing GetItemCategory() remains untouched
function API.GetItemCategoryEx(itemID)
  if not itemID then return nil end
  if cache[itemID] then return cache[itemID] end

  local _, _, _, _, _, classID, subClassID, _, equipLoc =
    C_Item.GetItemInfoInstant(itemID)

  local cat = API.GetItemCategory and API.GetItemCategory(itemID) or "Miscellaneous"

  local info = {
    category      = cat,
    classID       = classID,
    subClassID    = subClassID,
    equipLoc      = equipLoc,

    isEquipment   = (classID == Enum.ItemClass.Weapon or classID == Enum.ItemClass.Armor),
    isConsumable  = (classID == Enum.ItemClass.Consumable),
    isTrade       = (classID == Enum.ItemClass.Tradegoods),
    isQuest       = (classID == Enum.ItemClass.Questitem),
    isMisc        = (classID == Enum.ItemClass.Miscellaneous),

    isAccountBound = C_Item.IsBoundToAccountUntilEquip(itemID)
                     or C_Item.IsBoundToAccount(itemID)
                     or false,
  }

  cache[itemID] = info
  return info
end

-- Optional helper (safe)
function API.ClearCategoryCache()
  wipe(cache)
end

-- Signal availability
API.Has = API.Has or {}
API.Has.category_enrich = true

-- Debug (single line, safe)
-- print("|cff88ff88DeepPockets|r category_enrich loaded")
