DeepPockets.Index = DeepPockets.Index or {}

local function ResolveCategory(item)
  local itemType = item.itemType
  local equipLoc = item.equipLoc

  if equipLoc and equipLoc ~= "" and equipLoc ~= "INVTYPE_NON_EQUIP_IGNORE" then
    return "Equipment"
  end
  if itemType == "Consumable" then return "Consumable" end
  if itemType == "Trade Goods" then return "Trade Goods" end
  if itemType == "Quest" then return "Quest" end
  if itemType == "Gem" then return "Gem" end
  return "Miscellaneous"
end

function DeepPockets.Index.Rebuild()
  DeepPockets.Migrate.Ensure()
  local db = DeepPocketsDB

  db.index.by_item = {}
  db.index.by_category = {}

  for _, it in ipairs(db.inventory) do
    local id = it.id
    if id then
      local entry = db.index.by_item[id]
      if not entry then
        entry = {
          id = id,
          name = it.name,
          icon = it.icon,
          quality = it.quality,
          total = 0,
          per_bag = {},
          category = ResolveCategory(it),
        }
        db.index.by_item[id] = entry
      end

      entry.total = (entry.total or 0) + (it.count or 1)
      entry.per_bag[it.bag] = (entry.per_bag[it.bag] or 0) + (it.count or 1)

      local cat = entry.category or "Miscellaneous"
      db.index.by_category[cat] = db.index.by_category[cat] or {}
      if not entry._cat_added then
        table.insert(db.index.by_category[cat], id)
        entry._cat_added = true
      end
    end
  end

  for _, entry in pairs(db.index.by_item) do
    entry._cat_added = nil
  end
end
