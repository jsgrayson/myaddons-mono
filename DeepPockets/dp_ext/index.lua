DeepPocketsIndex = DeepPocketsIndex or {}

function DeepPocketsIndex.GetCategoryForItem(itemID, classID, subClassID, equipLoc)
  -- Keep this conservative for now; we can expand later.
  if classID == 2 or (equipLoc and equipLoc ~= "" and equipLoc ~= "INVTYPE_NON_EQUIP_IGNORE") then
    return "Equipment"
  elseif classID == 0 then
    return "Consumable"
  elseif classID == 7 then
    return "Trade Goods"
  elseif classID == 12 then
    return "Quest"
  else
    return "Miscellaneous"
  end
end

function DeepPocketsIndex.Rebuild(inv)
  DeepPocketsDB.index = DeepPocketsDB.index or { by_item = {}, by_category = {} }
  local by_item = {}
  local by_category = {}

  for _, it in ipairs(inv or {}) do
    if it.id then
      local t = by_item[it.id]
      if not t then
        t = { id = it.id, name = it.name, icon = it.icon, quality = it.quality or 0, count = 0 }
        by_item[it.id] = t
      end
      t.count = (t.count or 0) + (it.count or 1)
    end

    local cat = it.category or "Miscellaneous"
    by_category[cat] = by_category[cat] or {}
    table.insert(by_category[cat], it)
  end

  DeepPocketsDB.index.by_item = by_item
  DeepPocketsDB.index.by_category = by_category
end
