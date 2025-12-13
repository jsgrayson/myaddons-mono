DeepPockets.API = DeepPockets.API or {}

function DeepPockets.API.Scan()
  local count = DeepPockets.Scanner.ScanBags()
  DeepPockets.Index.Rebuild()
  return count
end

function DeepPockets.API.GetDB()
  DeepPockets.Migrate.Ensure()
  return DeepPocketsDB
end

function DeepPockets.API.GetTotalsByItem(itemID)
  DeepPockets.Migrate.Ensure()
  local by_item = DeepPocketsDB.index and DeepPocketsDB.index.by_item
  return by_item and by_item[itemID] or nil
end

function DeepPockets.API.GetCategory(itemID)
  local t = DeepPockets.API.GetTotalsByItem(itemID)
  return t and t.category or nil
end

-- Placeholder: later integrate SkillWeaver weights / Pawn-like scoring
function DeepPockets.API.GetUpgradeScore(itemLink)
  return nil, { reason = "not_implemented" }
end
