-- engine/CastMacroBuilder.lua
-- Builds macrotext for bindable intent buttons, respecting spec profiles.

local CastMacroBuilder = {}
local GroundMode = require("core.GroundMode")
local SpellValidator = require("engine.SpellValidator")

local function toSet(list)
  local s = {}
  if type(list) == "table" then
    for _, v in ipairs(list) do s[v] = true end
  end
  return s
end

local function resolveGroundMode(profile, specKey)
  local g = profile and profile.ground
  local mode = GroundMode:GetResolved(specKey) -- AUTO -> per spec
  local spells = {}
  if g and type(g.spells) == "table" then spells = g.spells end
  
  -- Filter ground spells to known only
  spells = SpellValidator:FilterKnown(spells)
  return mode, toSet(spells)
end

local function buildCastLine(spell, unitTag, groundMode)
  -- unitTag: e.g. "targettarget", "player", nil
  -- groundMode: "CURSOR"|"PLAYER"|"RETICLE"
  if groundMode == "CURSOR" then
    return string.format('/cast [@cursor] %s', spell)
  elseif groundMode == "PLAYER" then
    return string.format('/cast [@player] %s', spell)
  else
    if unitTag and unitTag ~= "" then
      return string.format('/cast [@%s,help,nodead] %s', unitTag, spell)
    end
    return string.format('/cast %s', spell)
  end
end

local function buildUnitTag(intent, profile)
  if intent == "TANK" then
    local mode = (SkillWeaverDB and SkillWeaverDB.TankTargetMode) or "TARGETTARGET"
    mode = tostring(mode):upper()
    
    -- "FOCUS" or "TARGETTARGET" (Profile override logic removed as User wants Global toggle here)
    -- Actually, user logic: "local mode = (profile and profile.TANK and profile.TANK.targetMode) or 'TARGETTARGET'"
    -- User's new hook: "local mode = (SkillWeaverDB and SkillWeaverDB.TankTargetMode) or 'TARGETTARGET'"
    -- So Global Toggle wins.
    
    if mode == "FOCUS" then return "focus" end
    return "targettarget"
  end
  if intent == "SELF" then
    return "player"
  end
  -- PRIMARY + GROUP should not force friendly unit targeting
  return nil
end

-- Build a macro that attempts spells in priority order.
-- It uses /castsequence reset=0 for "first available" is unreliable; we do simple ordered /cast lines:
-- The secure system will try them in order; only one should succeed each press.
local function buildPriorityMacro(spells, intent, profile, specKey)
  local groundMode, groundSet = resolveGroundMode(profile, specKey)
  local unitTag = buildUnitTag(intent, profile)

  local lines = { "#showtooltip" }

  for _, spell in ipairs(spells or {}) do
    local isGround = (intent == "GROUP") and groundSet[spell] == true
    local mode = isGround and groundMode or "RETICLE"

    -- For TANK/SELF, we do unitTag casts (not ground)
    if intent == "TANK" or intent == "SELF" then
      lines[#lines+1] = buildCastLine(spell, unitTag, "RETICLE")
    else
      -- PRIMARY/GROUP: only ground spells use @cursor/@player; otherwise plain /cast Spell
      lines[#lines+1] = buildCastLine(spell, nil, mode)
    end
  end

  -- Append Dispatch to Internal Logic
  lines[#lines+1] = "/click SkillWeaver_Internal " .. intent

  return table.concat(lines, "\n")
end

function CastMacroBuilder:BuildIntentMacro(profile, intent, specKey)
  local bucket = profile and profile[intent]
  local spells = (bucket and bucket.spells) or {}
  
  -- Prune unknown/untalented spells
  spells = SpellValidator:FilterKnown(spells)
  
  return buildPriorityMacro(spells, intent, profile, specKey)
end

return CastMacroBuilder
