local SW = SkillWeaver
SW.State = SW.State or {}

function SW.State:Init()
  self.inCombat = InCombatLockdown()
  
  -- Ensure DB is ready
  if SkillWeaverDB and not SkillWeaverDB.mode then SkillWeaverDB.mode = "Delves" end
end

function SW.State:GetClassSpecKey()
  local _, class = UnitClass("player")
  local specIndex = GetSpecialization()
  if not specIndex then return class .. "_0" end
  local specID = select(1, GetSpecializationInfo(specIndex))
  return (class or "UNKNOWN") .. "_" .. tostring(specID or 0)
end

function SW.State:GetMode()
  return SkillWeaverDB and SkillWeaverDB.mode or "Delves"
end

function SW.State:SetMode(mode)
  if InCombatLockdown() then 
    print("|cFFFF0000Cannot switch modes in combat!|r")
    return 
  end
  
  if SkillWeaverDB then
    SkillWeaverDB.mode = mode
  end
  
  -- 1. Refresh Engine
  if SW.Engine and SW.Engine.RefreshAll then
    SW.Engine:RefreshAll("mode_changed")
  end
  
  -- 2. Update UI
  if SW.UI and SW.UI.UpdatePanel then
    SW.UI:UpdatePanel()
  end
  
  print("SkillWeaver: Mode set to " .. mode)
end
