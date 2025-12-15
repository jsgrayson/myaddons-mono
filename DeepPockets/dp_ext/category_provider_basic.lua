-- dp_ext/category_provider_basic.lua
-- Safe, backend-only categorizer (Retail). No UI. No hooks. No protected calls.

local DP = _G.DeepPockets
if not DP or not DP.API or not DP.API._SetCategoryProvider then return end

local function GetInstant(itemLinkOrID)
  if not itemLinkOrID then return end
  if type(itemLinkOrID) == "number" then
    return C_Item.GetItemInfoInstant(itemLinkOrID)
  end
  if type(itemLinkOrID) == "string" then
    local id = itemLinkOrID:match("item:(%d+)")
    if id then return C_Item.GetItemInfoInstant(tonumber(id)) end
    if itemLinkOrID:match("^%d+$") then
      return C_Item.GetItemInfoInstant(tonumber(itemLinkOrID))
    end
  end
end

local function Categorize(itemID, itemLink)
  local id, _, _, _, _, classID = GetInstant(itemLink or itemID)
  if not id or not classID then return "Misc" end

  if Enum.ItemClass.Questitem and classID == Enum.ItemClass.Questitem then return "Quest" end
  if Enum.ItemClass.Consumable and classID == Enum.ItemClass.Consumable then return "Consumables" end
  if Enum.ItemClass.Tradegoods and classID == Enum.ItemClass.Tradegoods then return "Trade Goods" end
  if Enum.ItemClass.Reagent and classID == Enum.ItemClass.Reagent then return "Reagents" end
  if Enum.ItemClass.Weapon and classID == Enum.ItemClass.Weapon then return "Equipment" end
  if Enum.ItemClass.Armor and classID == Enum.ItemClass.Armor then return "Equipment" end
  if Enum.ItemClass.Gem and classID == Enum.ItemClass.Gem then return "Gems" end
  if Enum.ItemClass.Container and classID == Enum.ItemClass.Container then return "Bags" end
  if Enum.ItemClass.Recipe and classID == Enum.ItemClass.Recipe then return "Recipes" end

  if Enum.ItemClass.Miscellaneous and classID == Enum.ItemClass.Miscellaneous then
    local quality = select(3, GetItemInfo(itemLink or id))
    if quality == Enum.ItemQuality.Poor then return "Junk" end
    return "Misc"
  end

  return "Misc"
end

DP.API._SetCategoryProvider(Categorize)
