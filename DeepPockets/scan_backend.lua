-- scan_backend.lua - safe scan (no UseContainerItem, no protected calls)
DeepPocketsDB = DeepPocketsDB or {}
DeepPocketsDB.lastScan = DeepPocketsDB.lastScan or {}

local function ScanOnce()
  local out = {}
  for bag = 0, 4 do
    local slots = C_Container and C_Container.GetContainerNumSlots and C_Container.GetContainerNumSlots(bag) or 0
    for slot = 1, slots do
      local info = C_Container.GetContainerItemInfo(bag, slot)
      if info and info.itemID then
        out[#out+1] = { bag=bag, slot=slot, itemID=info.itemID, count=info.stackCount or 1 }
      end
    end
  end
  DeepPocketsDB.lastScan = out
  print(("DeepPockets: scan ok (%d items)"):format(#out))
  
  if _G.DeepPockets and _G.DeepPockets.API and _G.DeepPockets.API.RecordScan then
    _G.DeepPockets.API.RecordScan("manual")
  end
end

_G.DeepPockets_Scan = ScanOnce

_G.DeepPockets_AutoScan = function(on)
  DeepPocketsDB.autoscan = not not on
  print("DeepPockets autoscan:", DeepPocketsDB.autoscan and "ON" or "OFF")
  -- Note: Autoscan toggle doesn't strictly record a scan, 
  -- but per prompt Step 6 we should add RecordScan("auto") if it triggers a scan.
  -- The current implementation here just toggles the flag.
  -- I will strictly follow the prompt: "And wherever autoscan triggers a scan, call RecordScan('auto') instead."
  -- Since this function only toggles, I won't add RecordScan here unless it actually scans.
end
