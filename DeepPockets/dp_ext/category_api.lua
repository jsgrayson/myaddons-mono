-- dp_ext/category_api.lua
-- DeepPockets -> BetterBags category key mapper
-- IMPORTANT: return values MUST match BetterBags category keys (your "BBKey ..." printout)

DeepPockets = DeepPockets or {}
DeepPockets.API = DeepPockets.API or {}

local SLOT_KEY_BY_EQUIPLOC = {
  INVTYPE_HEAD              = "Head",
  INVTYPE_NECK              = "Equipment",
  INVTYPE_SHOULDER          = "Equipment",
  INVTYPE_CLOAK             = "Equipment",
  INVTYPE_CHEST             = "Chest",
  INVTYPE_ROBE              = "Chest",
  INVTYPE_BODY              = "Equipment",
  INVTYPE_TABARD            = "Equipment",
  INVTYPE_WRIST             = "Equipment",
  INVTYPE_HAND              = "Hands",
  INVTYPE_WAIST             = "Waist",
  INVTYPE_LEGS              = "Legs",
  INVTYPE_FEET              = "Feet",
  INVTYPE_FINGER            = "Finger",
  INVTYPE_TRINKET           = "Equipment",

  INVTYPE_WEAPON            = "Equipment",
  INVTYPE_2HWEAPON          = "Equipment",
  INVTYPE_WEAPONMAINHAND    = "Equipment",
  INVTYPE_WEAPONOFFHAND     = "Off Hand",
  INVTYPE_SHIELD            = "Off Hand",
  INVTYPE_HOLDABLE          = "Held In Off-hand",

  INVTYPE_RANGED            = "Ranged",
  INVTYPE_RANGEDRIGHT       = "Ranged",
  INVTYPE_THROWN            = "Ranged",
  INVTYPE_RELIC             = "Ranged",

  INVTYPE_BAG               = "Bag",
  INVTYPE_QUIVER            = "Bag",
}

-- ItemClass IDs (Retail) are stable enough for this purpose.
-- If you want to be extra-safe, you can swap these to Enum.ItemClass.* when available.
local CLASS_KEY = {
  [0]  = "Consumables",   -- Consumable
  [1]  = "Bag",           -- Container
  [2]  = "Equipment",     -- Weapon
  [3]  = "Equipment",     -- Gem
  [4]  = "Equipment",     -- Armor
  [5]  = "Consumables",   -- Reagent (often behaves like consumables/tradeskill mats depending on expac)
  [6]  = "Equipment",     -- Projectile (legacy)
  [7]  = "Trade Goods",   -- Trade Goods
  [8]  = "Consumables",   -- Item Enhancement (often consumable-ish)
  [9]  = "Recipes",       -- Recipe
  [10] = "Tradeskill",    -- Currency / Profession? (varies; "Tradeskill" exists in your keys)
  [11] = "Equipment",     -- Quiver (legacy)
  [12] = "Equipment",     -- Quest (BetterBags often has Quest, but your printout didn't show it)
  [13] = "Equipment",     -- Key (legacy)
  [14] = "Equipment",     -- Permanent (legacy)
  [15] = "Junk",          -- Miscellaneous
  [16] = "Trade Goods",   -- Glyph (often treated as trade good-ish)
  [17] = "Equipment",     -- Battle Pets / Tokens (varies by client; you said battlepets-under-mounts is already handled elsewhere)
  [18] = "Equipment",
  [19] = "Trade Goods",
}

-- Optional: treat poor-quality items as Junk if we can detect it
local function IsJunk(itemID)
  if C_Item and C_Item.GetItemQualityByID then
    local q = C_Item.GetItemQualityByID(itemID)
    return q == 0
  end
  return false
end

function DeepPockets.API.GetItemCategory(itemID)
  if not itemID then return nil end

  -- If junk, prefer Junk bucket
  if IsJunk(itemID) then
    return "Junk"
  end

  local _, _, _, _, _, classID, subClassID, _, equipLoc =
    (C_Item and C_Item.GetItemInfoInstant) and C_Item.GetItemInfoInstant(itemID)

  if equipLoc and equipLoc ~= "" then
    local slotKey = SLOT_KEY_BY_EQUIPLOC[equipLoc]
    if slotKey then
      return slotKey
    end
  end

  if classID ~= nil then
    local k = CLASS_KEY[classID]
    if k then return k end
  end

  return "Equipment"
end
