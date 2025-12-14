-- dp_ext/migrate.lua
local addonName = ...
DeepPocketsDB = DeepPocketsDB or {}

-- One-time import if user previously had BetterBagsDB
if BetterBagsDB and not DeepPocketsDB.__importedFromBetterBags then
  for k,v in pairs(BetterBagsDB) do
    if DeepPocketsDB[k] == nil then DeepPocketsDB[k] = v end
  end
  DeepPocketsDB.__importedFromBetterBags = true
end

DeepPocketsDB.version = DeepPocketsDB.version or 1
