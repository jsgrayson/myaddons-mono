-- Data/LoadAll.lua
SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver

for packName, data in pairs(SW.ClassPacks or {}) do
  SW.SpecPackLoader:LoadClassPack(data)
end
