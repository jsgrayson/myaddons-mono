-- policies/PolicyManager.lua
local addonName, addonTable = ...
local PolicyManager = {}
addonTable.PolicyManager = PolicyManager
local Merger = addonTable.PolicyMerger

PolicyManager.cache = {}

-- Defaults applied when no spec pack exists yet
PolicyManager.defaults = {
  resources = { enablePooling=false },
  procs = {},
  cooldownSync = {},
  charges = {},
  interrupts = {}, 
}

-- Storage for packs
addonTable.PolicyPacksGen = addonTable.PolicyPacksGen or {}
addonTable.PolicyPacksManual = addonTable.PolicyPacksManual or {}

local function deepMerge(dst, src)
  if type(dst) ~= "table" then dst = {} end
  if type(src) ~= "table" then return dst end
  for k,v in pairs(src) do
    if type(v) == "table" and type(dst[k]) == "table" then
      deepMerge(dst[k], v)
    else
      dst[k] = v
    end
  end
  return dst
end

function PolicyManager:Get(specKey)
  if self.cache[specKey] then return self.cache[specKey] end
  
  -- Load from separate tables
  local gen = addonTable.PolicyPacksGen[specKey]
  local manual = addonTable.PolicyPacksManual[specKey]
  
  -- Fallback: Check old single table just in case transitional
  if not gen and not manual and addonTable.PolicyPacks and addonTable.PolicyPacks[specKey] then
      gen = addonTable.PolicyPacks[specKey]
  end

  local merged
  if Merger then
      merged = Merger:Merge(self.defaults, gen, manual)
  else
      merged = {}
      deepMerge(merged, self.defaults)
      deepMerge(merged, gen or {})
      deepMerge(merged, manual or {})
  end

  self.cache[specKey] = merged
  return merged
end

return PolicyManager

