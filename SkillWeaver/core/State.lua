local SW = SkillWeaver

SW.State = {
  inCombat = false,
}

function SW.State:Init()
  self.inCombat = InCombatLockdown() and true or false
end

function SW.State:GetClassSpecKey()
  local _, class = UnitClass("player")
  local specIndex = GetSpecialization()
  if not specIndex then return class .. "_0" end
  local specID = select(1, GetSpecializationInfo(specIndex))
  return (class or "UNKNOWN") .. "_" .. tostring(specID or 0)
end

function SW.State:GetMode()
  return SkillWeaverDB.mode or "Delves"
end

function SW.State:SetMode(mode)
  SkillWeaverDB.mode = mode
  SW.Engine:RefreshAll("mode_changed")
end
