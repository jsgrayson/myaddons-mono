-- Core/Engine.lua
SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver

SW.Engine = SW.Engine or {}

function SW.Engine:RefreshAll(reason)
  if not SkillWeaverDB.enabled then return end
  if InCombatLockdown() then return end

  local key = SW.State:GetClassSpecKey()
  local ruleset = SW.State:GetRuleset()
  local mode = SW.State:GetEffectiveMode()
  local profile = SW.Profiles:GetActiveProfileName(key)

  local rotation

  -- If Midnight is available and selected, pull from backend ruleset
  if ruleset == "MIDNIGHT" and mode == "Midnight" and SkillWeaverBackend then
    rotation = SkillWeaverBackend:GetRotation(key, "MIDNIGHT", "Midnight", profile)
  end

  -- Otherwise, use backend TWW if connected (optional), else fall back offline
  if not rotation and SkillWeaverBackend and SkillWeaverBackend:IsConnected() then
    rotation = SkillWeaverBackend:GetRotation(key, "TWW", mode, profile)
  end

  if not rotation and SW.Defaults then
    rotation = SW.Defaults:GetFallbackRotation(key, mode, profile)
  end

  -- final fallbacks
  rotation = rotation or {}

  local stMacro, aoeMacro, intMacro, utilMacro = SW.Decision:BuildButtonMacros(rotation, key)
  local healMacro = SW.Decision:BuildHealMacro(rotation)
  local selfMacro = SW.Decision:BuildSelfMacro(rotation)

  SW.SecureButtons:SetMacro("ST", stMacro)
  SW.SecureButtons:SetMacro("AOE", aoeMacro)
  SW.SecureButtons:SetMacro("HEAL", healMacro)
  SW.SecureButtons:SetMacro("SELF", selfMacro)
  SW.SecureButtons:SetMacro("INT", intMacro)
  SW.SecureButtons:SetMacro("UTIL", utilMacro)

  if SW.UI and SW.UI.UpdatePanel then
    SW.UI:UpdatePanel()
  end
end

