-- core/ControllerMode.lua
SkillWeaverDB = SkillWeaverDB or {}
SkillWeaverDB.ControllerMode = SkillWeaverDB.ControllerMode or false

local ControllerMode = {}

function ControllerMode:Get()
  return SkillWeaverDB.ControllerMode == true
end

function ControllerMode:Set(on)
  SkillWeaverDB.ControllerMode = (on == true)
  if SkillWeaver then 
      SkillWeaver:Print("Controller Mode: " .. (on and "ON" or "OFF")) 
      if SkillWeaver.RequestIntentMacroRefresh then
        SkillWeaver:RequestIntentMacroRefresh()
      end
  end
end

SLASH_SWCONTROLLER1 = "/swcontroller"
SlashCmdList["SWCONTROLLER"] = function(msg)
  msg = (msg or ""):lower():gsub("%s+", "")
  if msg == "" then
    local state = ControllerMode:Get() and "ON" or "OFF"
    if SkillWeaver then SkillWeaver:Print("Controller Mode: " .. state .. " (use: /swcontroller on|off)") end
    return
  end
  if msg == "on" then ControllerMode:Set(true)
  elseif msg == "off" then ControllerMode:Set(false)
  else
    if SkillWeaver then SkillWeaver:Print("Use: /swcontroller on|off") end
  end
end

return ControllerMode
