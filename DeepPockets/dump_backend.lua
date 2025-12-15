DeepPocketsDB = DeepPocketsDB or {}
_G.DeepPockets_Dump = function()
  local n = (DeepPocketsDB.lastScan and #DeepPocketsDB.lastScan) or 0
  print(("DeepPockets dump: lastScan=%d autoscan=%s"):format(n, tostring(DeepPocketsDB.autoscan)))
end
