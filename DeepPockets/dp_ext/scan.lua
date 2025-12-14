local function Now()
  return time()
end

local function SafeItemInfo(itemLinkOrID)
  local name, link, quality, ilvl, req, class, subclass, maxStack, equipLoc, icon, sellPrice, classID, subClassID =
    GetItemInfo(itemLinkOrID)
  return name, link, quality, equipLoc, icon, classID, subClassID
end

local function ScanBags()
  local inv = {}
  for bag = 0, 4 do
    local slots = C_Container.GetContainerNumSlots(bag) or 0
    for slot = 1, slots do
      local info = C_Container.GetContainerItemInfo(bag, slot)
      if info then
        local itemID = C_Container.GetContainerItemID(bag, slot)
        local link = C_Container.GetContainerItemLink(bag, slot)
        local name, _, quality, equipLoc, icon, classID, subClassID = SafeItemInfo(link or itemID or 0)
        local count = info.stackCount or 1
        local cat = DeepPocketsAPI.GetCategoryForItem(itemID, classID, subClassID, equipLoc)

        inv[#inv+1] = {
          bag = bag,
          slot = slot,
          id = itemID,
          link = link,
          name = name or ("item:" .. tostring(itemID)),
          quality = quality or 0,
          icon = icon,
          count = count,
          classID = classID,
          subClassID = subClassID,
          equipLoc = equipLoc,
          category = cat,
        }
      end
    end
  end
  return inv
end

function DeepPocketsAPI.Scan(silent)
  if not DeepPocketsDB then return 0 end
  local inv = ScanBags()
  DeepPocketsDB.inventory = inv
  DeepPocketsDB.meta.last_scan = Now()

  if DeepPocketsIndex and DeepPocketsIndex.Rebuild then
    DeepPocketsIndex.Rebuild(inv)
  end

  if not silent then
    print("|cffDAA520DeepPockets|r: Scanned " .. tostring(#inv) .. " slots.")
  end
  return #inv
end
