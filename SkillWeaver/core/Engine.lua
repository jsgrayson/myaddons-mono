-- Core/Engine.lua
SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver

SW.Engine = SW.Engine or {}

function SW.Engine:RefreshAll(reason)
  if not SkillWeaverDB.enabled then return end
  if InCombatLockdown() then return end

  local key = SW.State:GetClassSpecKey()
  local mode = SW.State:GetMode()
  local profile = (SW.Profiles and SW.Profiles.GetActiveProfileName) and SW.Profiles:GetActiveProfileName(key) or "Balanced"

  local rotation
  if SW.Defaults then
    rotation = SW.Defaults:GetFallbackRotation(key, mode, profile)
  end

  -- final fallbacks
  rotation = rotation or {}

  local stMacro, aoeMacro, intMacro, utilMacro = SW.Decision:BuildButtonMacros(rotation, key)
  local healMacro = SW.Decision:BuildHealMacro(rotation)
  local selfMacro = SW.Decision:BuildSelfMacro(rotation, key)

  SW.SecureButtons:SetMacro("ST", stMacro)
  SW.SecureButtons:SetMacro("AOE", aoeMacro)
  SW.SecureButtons:SetMacro("HEAL", healMacro)
  SW.SecureButtons:SetMacro("SELF", selfMacro)
  SW.SecureButtons:SetMacro("INT", intMacro)
  SW.SecureButtons:SetMacro("UTIL", utilMacro)



  local shouldHide = SkillWeaverDB.toggles.hideEmptyButtons

  local showHeal = SkillWeaverDB.toggles.showHealButton and (healMacro and healMacro ~= "")
  local showSelf = SkillWeaverDB.toggles.showSelfButton and (selfMacro and selfMacro ~= "")

  if shouldHide then
    SW.SecureButtons:SetVisible("HEAL", showHeal)
    SW.SecureButtons:SetVisible("SELF", showSelf)
  else
    SW.SecureButtons:SetVisible("HEAL", SkillWeaverDB.toggles.showHealButton)
    SW.SecureButtons:SetVisible("SELF", SkillWeaverDB.toggles.showSelfButton)
  end

  if SW.UI and SW.UI.UpdatePanel then
    SW.UI:UpdatePanel()
  end
end

