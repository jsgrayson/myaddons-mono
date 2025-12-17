-- core/GroundMode.lua
SkillWeaverDB = SkillWeaverDB or {}
SkillWeaverDB.GroundMode = SkillWeaverDB.GroundMode or "AUTO" -- AUTO|CURSOR|PLAYER|RETICLE

local ControllerMode = require("core.ControllerMode")

local GroundMode = {}

-- Per-spec “best defaults”
-- (controller ON => prefer CURSOR for specs with ground heals)
local function recommendForSpec(specKey)
  local controller = ControllerMode:Get()

  -- Shaman/Druid: cursor feels best on controller
  if controller and (specKey == "SHAMAN_264" or specKey == "DRUID_105") then
    return "CURSOR"
  end

  -- Disc/Holy priest: only if you actually use ground spells; default reticle otherwise
  -- If you prefer CURSOR for Barrier/Sanctify on controller, you can add them here:
  if controller and (specKey == "PRIEST_256" or specKey == "PRIEST_257") then 
      -- Optional preference for Barrier/Sanctify on Controller
      -- return "CURSOR" 
  end

  return "RETICLE" -- Default fallback
end

function GroundMode:GetResolved(specKey)
  local mode = (SkillWeaverDB.GroundMode or "AUTO"):upper()
  if mode == "AUTO" then
    return recommendForSpec(specKey)
  end
  return mode
end

function GroundMode:GetRaw()
  return (SkillWeaverDB.GroundMode or "AUTO"):upper()
end

function GroundMode:Set(mode)
  mode = tostring(mode or ""):upper()
  if mode ~= "AUTO" and mode ~= "CURSOR" and mode ~= "PLAYER" and mode ~= "RETICLE" then
    print("SkillWeaver: ground mode must be auto|cursor|player|reticle")
    return
  end
  SkillWeaverDB.GroundMode = mode
  if SkillWeaver then SkillWeaver:Print("Ground Mode set to: " .. mode) end
  
  if SkillWeaver and SkillWeaver.RequestIntentMacroRefresh then
    SkillWeaver:RequestIntentMacroRefresh()
  end
end

SLASH_SWGROUND1 = "/swground"
SlashCmdList["SWGROUND"] = function(msg)
  msg = (msg or ""):lower():gsub("%s+", "")
  if msg == "" then
    if SkillWeaver then SkillWeaver:Print("Ground Mode: " .. GroundMode:GetRaw() .. " (use: /swground auto|cursor|player|reticle)") end
    return
  end
  GroundMode:Set(msg)
end

return GroundMode
