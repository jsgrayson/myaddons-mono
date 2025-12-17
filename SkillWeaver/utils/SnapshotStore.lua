-- utils/SnapshotStore.lua
local addonName, addonTable = ...
local Store = {}
addonTable.SnapshotStore = Store

Store.max = 400

function Store:Init()
  SkillWeaver_Snapshots = SkillWeaver_Snapshots or { version=1, items={} }
end

function Store:Clear()
  self:Init()
  SkillWeaver_Snapshots.items = {}
end

function Store:Append(snapshot)
  self:Init()
  local items = SkillWeaver_Snapshots.items
  items[#items+1] = snapshot
  if #items > self.max then
    table.remove(items, 1)
  end
end

function Store:Count()
  self:Init()
  return #SkillWeaver_Snapshots.items
end

function Store:Get(i)
  self:Init()
  return SkillWeaver_Snapshots.items[i]
end

return Store
