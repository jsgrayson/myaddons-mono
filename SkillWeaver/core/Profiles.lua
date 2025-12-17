local SW = SkillWeaver

SW.Profiles = {}

function SW.Profiles:Init()
  SkillWeaverDB.profiles = SkillWeaverDB.profiles or {}
end

function SW.Profiles:GetActiveProfileName(classSpecKey)
  local p = SkillWeaverDB.profiles[classSpecKey]
  return p and p.name or "Balanced"
end

function SW.Profiles:SetActiveProfileName(classSpecKey, name)
  SkillWeaverDB.profiles[classSpecKey] = SkillWeaverDB.profiles[classSpecKey] or {}
  SkillWeaverDB.profiles[classSpecKey].name = name
  SW.Engine:RefreshAll("profile_changed")
end
