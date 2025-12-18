-- core/Init.lua
-- SkillWeaver bootstrap (offline-only)

-- Always bind explicitly to the global table
_G.SkillWeaver = _G.SkillWeaver or {}
SkillWeaver = _G.SkillWeaver
local SW = SkillWeaver

-- Namespace safety
SW.version = "0.9.0"
SW.loaded = false

-- Event frame
local f = CreateFrame("Frame")

f:RegisterEvent("ADDON_LOADED")
f:RegisterEvent("PLAYER_LOGIN")
f:RegisterEvent("PLAYER_LOGOUT")

f:SetScript("OnEvent", function(_, event, arg1)
  if event == "ADDON_LOADED" then
    if arg1 ~= "SkillWeaver" then return end

    -- SavedVariables init
    SkillWeaverDB = SkillWeaverDB or {}

    -- Mark addon namespace as live
    SW.loaded = true

  elseif event == "PLAYER_LOGIN" then
    -- Core systems init (order matters)
    if SW.SecureButtons and SW.SecureButtons.Init then
      SW.SecureButtons:Init()
    end

    if SW.Engine and SW.Engine.RefreshAll then
      SW.Engine:RefreshAll("login")
    end

  elseif event == "PLAYER_LOGOUT" then
    -- nothing required yet (reserved for future UI state save)
  end
end)