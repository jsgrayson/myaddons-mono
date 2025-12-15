-- dp_ext/category_api.lua
DeepPockets = DeepPockets or {}
DeepPockets.API = DeepPockets.API or {}

-- Minimal category resolver (safe + deterministic).
-- Replace internals later with your real mapping, but keep the function name stable.
function DeepPockets.API.GetItemCategory(itemID, itemLink)
  itemID = tonumber(itemID)
  if not itemID then return "Miscellaneous" end

  -- Prefer item info instant when available
  local _, _, _, _, _, classID, subclassID = C_Item.GetItemInfoInstant(itemID)
  -- Fallback: if API returns nils, still return something stable
  if classID == nil then return "Miscellaneous" end

  -- VERY simple baseline buckets (tune later)
  if classID == Enum.ItemClass.Consumable then return "Consumables" end
  if classID == Enum.ItemClass.Container then return "Bags" end
  if classID == Enum.ItemClass.Weapon or classID == Enum.ItemClass.Armor then return "Equipment" end
  if classID == Enum.ItemClass.Tradegoods then return "Trade Goods" end
  if classID == Enum.ItemClass.Reagent then return "Reagents" end
  if classID == Enum.ItemClass.Questitem then return "Quest" end
  if classID == Enum.ItemClass.Miscellaneous then return "Miscellaneous" end
  if classID == Enum.ItemClass.Glyph then return "Glyphs" end
  if classID == Enum.ItemClass.Battlepet then return "Battle Pets" end
  if classID == Enum.ItemClass.Recipe then return "Recipes" end

  return "Miscellaneous"
end
