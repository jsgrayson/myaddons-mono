DeepPockets.Scanner = DeepPockets.Scanner or {}
local C = C_Container

local function SafeItemLink(bag, slot)
  local ok, link = pcall(C.GetContainerItemLink, bag, slot)
  if ok then return link end
  return nil
end

local function SafeItemInfo(bag, slot)
  local ok, info = pcall(C.GetContainerItemInfo, bag, slot)
  if ok then return info end
  return nil
end

function DeepPockets.Scanner.ScanBags()
  DeepPockets.Migrate.Ensure()
  local db = DeepPocketsDB
  wipe(db.inventory)

  local total = 0
  for bag = 0, 4 do
    local numSlots = C.GetContainerNumSlots(bag) or 0
    for slot = 1, numSlots do
      local info = SafeItemInfo(bag, slot)
      if info and info.itemID then
        local link = SafeItemLink(bag, slot)
        local name, _, quality, _, _, itemType, itemSubType, _, equipLoc, icon, _, classID, subClassID =
          (link and GetItemInfo(link))

        local itemID = info.itemID
        local count = info.stackCount or 1

        db.inventory[#db.inventory + 1] = {
          bag = bag,
          slot = slot,
          id = itemID,
          count = count,
          link = link,
          name = name or tostring(itemID),
          icon = icon or info.iconFileID,
          quality = quality or info.quality,
          classID = classID,
          subClassID = subClassID,
          itemType = itemType,
          itemSubType = itemSubType,
          equipLoc = equipLoc,
        }
        total = total + 1
      end
    end
  end

  db.meta.last_scan = time()
  return total
end
