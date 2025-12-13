DeepPockets = DeepPockets or {}
local addonName = ...
DeepPockets.name = addonName

DeepPocketsDB = DeepPocketsDB or {}

SLASH_DEEPPOCKETS1 = "/dp"
SlashCmdList["DEEPPOCKETS"] = function(msg)
  msg = tostring(msg or "")
  local cmd, arg = msg:lower():match("^(%S+)%s*(.*)$")
  cmd = cmd or ""

  if cmd == "scan" then
    local count = DeepPockets.API.Scan()
    print(("|cffDAA520DeepPockets|r: Scanned %d items."):format(count or 0))

  elseif cmd == "dump" then
    local db = DeepPockets.API.GetDB()
    local inv = (db.inventory and #db.inventory) or 0
    local cats = 0
    if db.index and db.index.by_category then
      for _ in pairs(db.index.by_category) do cats = cats + 1 end
    end
    print(("DP DUMP: Inv=%d, Cats=%d, LastScan=%s"):format(inv, cats, tostring(db.meta and db.meta.last_scan)))

  elseif cmd == "rebuild" then
    DeepPockets.Index.Rebuild()
    print("|cffDAA520DeepPockets|r: Index rebuilt.")

  else
    print("|cffDAA520DeepPockets|r commands: /dp scan | /dp dump | /dp rebuild")
  end
end

local f = CreateFrame("Frame")
f:RegisterEvent("ADDON_LOADED")
f:SetScript("OnEvent", function(_, _, name)
  if name == addonName then
    DeepPockets.Migrate.Ensure()
    print("|cffDAA520DeepPockets|r: Backend loaded.")
  end
end)
