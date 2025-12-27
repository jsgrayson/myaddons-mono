SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver

SW.ClassPacks = SW.ClassPacks or {}

-- Register a pack table keyed by "CLASS_SPECID"
function SW:RegisterClassPack(packName, data)
  if type(data) ~= "table" then return end
  SW.ClassPacks[packName or ("PACK_" .. tostring(#SW.ClassPacks + 1))] = data
end
