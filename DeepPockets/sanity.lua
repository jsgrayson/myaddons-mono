DeepPocketsDB = DeepPocketsDB or {}
_G.DeepPockets_Sanity = function()
  local ok = true
  if type(DeepPocketsDB) ~= "table" then ok = false end
  if ok then
    print("|cff00ff00DeepPockets sanity: OK|r")
  else
    print("|cffff5555DeepPockets sanity: FAIL|r")
  end
end
