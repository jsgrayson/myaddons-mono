DeepPocketsAPI = DeepPocketsAPI or {}

function DeepPocketsAPI.GetDB()
  return DeepPocketsDB
end

function DeepPocketsAPI.GetIndex()
  return DeepPocketsDB and DeepPocketsDB.index
end

-- placeholder: real category logic can live in dp_ext/index.lua
function DeepPocketsAPI.GetCategoryForItem(itemID, classID, subClassID, equipLoc)
  if DeepPocketsIndex and DeepPocketsIndex.GetCategoryForItem then
    return DeepPocketsIndex.GetCategoryForItem(itemID, classID, subClassID, equipLoc)
  end
  return "Miscellaneous"
end

-- ============================================================================
-- Bridge for DeepPockets Global (used by plugins)
-- ============================================================================
-- Ensure DeepPockets global exists (it should, from core.lua)
DeepPockets = DeepPockets or {}

function DeepPockets:GetCategory(itemID, itemInfo)
  -- If itemInfo is nil, we might want to fetch it, but usually the plugin
  -- calls this with an item object if available.
  -- Minimal implementation: fetch item info if needed to get class/subclass
  
  if not itemID then return nil end

  local name, link, quality, ilvl, req, class, subclass, maxStack, equipLoc, icon, sellPrice, classID, subClassID
  if itemInfo and itemInfo.classID and itemInfo.subClassID then
      classID = itemInfo.classID
      subClassID = itemInfo.subClassID
      equipLoc = itemInfo.invType or itemInfo.equipLoc 
  else
      name, link, quality, ilvl, req, class, subclass, maxStack, equipLoc, icon, sellPrice, classID, subClassID = GetItemInfo(itemID)
  end

  return DeepPocketsAPI.GetCategoryForItem(itemID, classID, subClassID, equipLoc)
end
