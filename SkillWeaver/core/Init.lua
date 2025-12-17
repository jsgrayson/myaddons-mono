
SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver

if SkillWeaverBackend then SkillWeaverBackend:RequestSync(SW.State:GetClassSpecKey()) end

SW._lastBackendUpdatedAt = SW._lastBackendUpdatedAt or 0
C_Timer.NewTicker(1.0, function()
  if not SkillWeaverBackend then return end
  local ts = SkillWeaverCache.meta.updatedAt or 0
  if ts > (SW._lastBackendUpdatedAt or 0) then
    SW._lastBackendUpdatedAt = ts
    if not InCombatLockdown() then
      SW.Engine:RefreshAll("backend_sync")
    end
  end
end)

SW.name = SkillWeaverL.ADDON_NAME
SW.events = CreateFrame("Frame")
SW.logPrefix = "|cff00d1ffSkillWeaver|r: "

local function printSW(msg)
  print(SW.logPrefix .. msg)
end

SW.print = printSW

SW.events:RegisterEvent("ADDON_LOADED")
SW.events:RegisterEvent("PLAYER_LOGIN")
SW.events:RegisterEvent("PLAYER_SPECIALIZATION_CHANGED")
SW.events:RegisterEvent("PLAYER_ENTERING_WORLD")
SW.events:RegisterEvent("PLAYER_REGEN_ENABLED")
SW.events:RegisterEvent("PLAYER_REGEN_DISABLED")

SW.events:SetScript("OnEvent", function(_, event, ...)
  if event == "ADDON_LOADED" then
    local addonName = ...
    if addonName ~= "SkillWeaver" then return end
    -- init done in PLAYER_LOGIN
  elseif event == "PLAYER_LOGIN" then
    SW.State:Init()
    SW.SecureButtons:Init()
    SW.Profiles:Init()
    SW.Engine:Init()

    SW.UI:Init()
    SW.Bindings:Apply()
    SW.Engine:RefreshAll("login")

    SW.print(SkillWeaverL.READY)
  elseif event == "PLAYER_SPECIALIZATION_CHANGED" then
    SW.Engine:RefreshAll("spec_changed")
  elseif event == "PLAYER_ENTERING_WORLD" then
    SW.Engine:RefreshAll("entering_world")
  elseif event == "PLAYER_REGEN_ENABLED" then
    SW.State.inCombat = false
    SW.Engine:OnCombatChanged(false)
  elseif event == "PLAYER_REGEN_DISABLED" then
    SW.State.inCombat = true
    SW.Engine:OnCombatChanged(true)
  end
end)
