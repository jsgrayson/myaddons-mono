-- policies/PolicySnapshot.lua
local addonName, addonTable = ...
local Snapshot = {}
addonTable.PolicySnapshot = Snapshot

function Snapshot:Init()
  if not SkillWeaver_PolicySnapshots then
      SkillWeaver_PolicySnapshots = { version=1, bySpec={} }
  end
  -- Migration check could go here
end

function Snapshot:Get(specKey)
  self:Init()
  return SkillWeaver_PolicySnapshots.bySpec[specKey]
end

function Snapshot:Set(specKey, policyTable)
  self:Init()
  -- store a deep copy to avoid mutation issues
  local function copy(x)
    if type(x) ~= "table" then return x end
    local o = {}
    for k,v in pairs(x) do o[k] = copy(v) end
    return o
  end
  SkillWeaver_PolicySnapshots.bySpec[specKey] = copy(policyTable)
end

return Snapshot
