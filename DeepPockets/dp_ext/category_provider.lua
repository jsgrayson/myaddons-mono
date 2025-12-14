-- dp_ext/category_provider.lua
-- Backend-only categorization provider (Retail-safe)
-- Avoid naming locals "type" (it shadows Lua's global type() and caused your crash earlier)

local ADDON = DeepPockets
DeepPocketsDB = DeepPocketsDB or {}

-- Canonical category list (match your intended 11)
local CATEGORIES = {
  "Equipment", "Consumable", "Quest", "Trade Goods", "Gem", "Item Enhancement",
  "Battle Pets", "Container", "Account", "Junk", "Miscellaneous"
}

-- Retail item class map (classID -> category)
-- (These are "good enough" defaults; refine later with overrides)
local CLASS_MAP = {
  [0]  = "Consumable",
  [1]  = "Container",
  [2]  = "Equipment",
  [3]  = "Gem",
  [4]  = "Item Enhancement",
  [5]  = "Trade Goods",
  [6]  = "Quest",
  [7]  = "Miscellaneous",
  [8]  = "Item Enhancement",
  [9]  = "Recipe",
  [10] = "Money",
  [11] = "Quest",
  [12] = "Miscellaneous",
  [13] = "Miscellaneous",
  [14] = "Miscellaneous",
  [15] = "Miscellaneous",
  [16] = "Glyph",
  [17] = "Battle Pets",
  [18] = "Account",
  [19] = "Trade Goods",
}

-- Normalize non-canonical mappings into your 11 buckets
local NORMALIZE = {
  Recipe = "Miscellaneous",
  Money  = "Miscellaneous",
  Glyph  = "Miscellaneous",
}

-- Overrides by classID/subclassID if you want tighter control later:
-- CLASS_SUBCLASS_OVERRIDE[classID][subclassID] = "Trade Goods" etc
local CLASS_SUBCLASS_OVERRIDE = {
  -- Example placeholder:
  -- [5] = { [1] = "Trade Goods" }
}

local function Normalize(cat)
  if not cat then return "Miscellaneous" end
  return NORMALIZE[cat] or cat
end

local function SafeGetItemInfo(itemLink, itemID)
  -- Prefer C_Item for link, fallback to GetItemInfoInstant
  local classID, subclassID, equipLoc
  if itemLink and C_Item.DoesItemExistByID(itemID or 0) then
    -- no-op; existence check only
  end

  if itemLink then
    local item = Item:CreateFromItemLink(itemLink)
    if item and item:IsItemDataCached() then
      local _, _, _, _, _, _, _, _, loc = GetItemInfo(itemLink)
      equipLoc = loc
    end
  end

  if itemID then
    local _, _, _, loc, cID, scID = GetItemInfoInstant(itemID)
    classID, subclassID, equipLoc = cID, scID, equipLoc or loc
  elseif itemLink then
    local id = select(1, GetItemInfoInstant(itemLink))
    if id then
      local _, _, _, loc, cID, scID = GetItemInfoInstant(id)
      classID, subclassID, equipLoc = cID, scID, equipLoc or loc
      itemID = id
    end
  end

  return itemID, classID, subclassID, equipLoc
end

function ADDON:GetCategoryForItem(itemID, itemLink)
  itemID, classID, subclassID, equipLoc = SafeGetItemInfo(itemLink, itemID)
  if not classID then
    return "Miscellaneous"
  end

  -- Subclass override first
  local o = CLASS_SUBCLASS_OVERRIDE[classID]
  if o and subclassID and o[subclassID] then
    return Normalize(o[subclassID])
  end

  local base = CLASS_MAP[classID] or "Miscellaneous"
  base = Normalize(base)

  -- Extra heuristics
  if equipLoc and equipLoc ~= "" and equipLoc ~= "INVTYPE_NON_EQUIP_IGNORE" then
    -- Anything with an equipLoc is almost always Equipment
    return "Equipment"
  end

  return base
end

-- Optional: bulk categorize bag items into DB cache for other addons to read
function ADDON:RebuildCategoryCache()
  DeepPocketsDB.categoryCache = DeepPocketsDB.categoryCache or {}
  local cache = DeepPocketsDB.categoryCache

  for bag = 0, 4 do
    for slot = 1, C_Container.GetContainerNumSlots(bag) do
      local info = C_Container.GetContainerItemInfo(bag, slot)
      if info and info.itemID then
        local cat = self:GetCategoryForItem(info.itemID, info.hyperlink)
        cache[info.itemID] = cat
      end
    end
  end
end

-- Debug slash subcommand: /dp cat <itemID|itemLink>
-- IMPORTANT: integrate into EXISTING /dp handler (do not create a second handler).
-- Add this inside the existing DeepPockets slash command dispatch:
--   elseif cmd == "cat" then DeepPockets:CmdCategory(arg) end
function ADDON:CmdCategory(arg)
  arg = tostring(arg or ""):match("^%s*(.-)%s*$")
  local itemID = tonumber(arg)
  local link = nil
  if not itemID and arg ~= "" then link = arg end

  local cat = self:GetCategoryForItem(itemID, link)
  print(("|cffDAA520DeepPockets|r category: %s  (%s)"):format(tostring(cat), tostring(itemID or link)))
end

-- Keep cache current (lightweight)
local f = CreateFrame("Frame")
f:RegisterEvent("BAG_UPDATE_DELAYED")
f:SetScript("OnEvent", function() if ADDON.RebuildCategoryCache then ADDON:RebuildCategoryCache() end end)
