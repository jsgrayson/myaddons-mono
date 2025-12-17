-- Core/Decision.lua
SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver

SW.Decision = SW.Decision or {}

local HEAL_CHAIN    = "[@targettarget,help,nodead][@focus,help,nodead][@player]"
local OFFHEAL_CHAIN = "[@targettarget,help,nodead][@focus,help,nodead]"

local function getRole()
  local specIndex = GetSpecialization()
  if not specIndex then return "DAMAGER" end
  return GetSpecializationRole(specIndex) or "DAMAGER"
end

local function isHealerRole()
  return getRole() == "HEALER"
end

local function wantsOffheals()
  return SkillWeaverDB and SkillWeaverDB.toggles and SkillWeaverDB.toggles.dpsEmergencyHeals == true
end

local function groundMode()
  return (SkillWeaverDB and SkillWeaverDB.toggles and SkillWeaverDB.toggles.groundTargetMode) or "cursor"
end

local function isCastLine(cmd)
  return type(cmd) == "string" and cmd:match("^/cast%s+")
end

local function extractSpell(cmd)
  return cmd:match("^/cast%s+(.+)$")
end

local function makeGroundTargetPrefix()
  return (groundMode() == "player") and "[@player]" or "[@cursor]"
end

local GROUND_SPELLS = {
  ["Healing Rain"] = true,
  ["Efflorescence"] = true,
  ["Death and Decay"] = true,
  ["Consecration"] = true,
  ["Sigil of Flame"] = true,
  ["Blizzard"] = true,
  ["Rain of Fire"] = true,
  ["Shadow Crash"] = true,
}

local OFFHEAL_SPELLS = {
  ["Word of Glory"] = true,
  ["Flash of Light"] = true,
  ["Lay on Hands"] = true,
  ["Healing Surge"] = true,
  ["Riptide"] = true,
  ["Regrowth"] = true,
  ["Rejuvenation"] = true,
  ["Vivify"] = true,
  ["Enveloping Mist"] = true,
  ["Renew"] = true,
  ["Flash Heal"] = true,
}

local function wrapGroundTarget(cmd)
  if not isCastLine(cmd) then return cmd end
  local spell = extractSpell(cmd)
  if not spell or spell == "" then return cmd end
  if spell:match("^%[") then return cmd end
  if GROUND_SPELLS[spell] then
    return ("/cast %s %s"):format(makeGroundTargetPrefix(), spell)
  end
  return cmd
end

local function wrapHealCast(cmd, chain)
  if not isCastLine(cmd) then return cmd end
  local spell = extractSpell(cmd)
  if not spell or spell == "" then return cmd end
  if spell:match("^%[") then return cmd end
  return ("/cast %s %s"):format(chain, spell)
end

local function compileSteps(steps, opts)
  local lines = {}
  if not (opts and opts.noStartAttack) then
    table.insert(lines, "/startattack")
  end

  if type(steps) ~= "table" then
    return table.concat(lines, "\n") .. "\n"
  end

  for _, step in ipairs(steps) do
    if step and type(step.command) == "string" and step.command ~= "" then
      local cmd = wrapGroundTarget(step.command)
      if opts and opts.healChain then
        cmd = wrapHealCast(cmd, opts.healChain)
      end
      table.insert(lines, cmd)
    end
  end

  return table.concat(lines, "\n") .. "\n"
end

local function blockHasOffheals(block)
  if type(block) ~= "table" or type(block.steps) ~= "table" then return false end
  for _, step in ipairs(block.steps) do
    if step and type(step.command) == "string" then
      local spell = extractSpell(step.command)
      if spell and OFFHEAL_SPELLS[spell] then return true end
    end
  end
  return false
end

local function resolveBlock(block, fallback, opts)
  if type(block) == "table" then
    if type(block.macro) == "string" and block.macro ~= "" then
      local m = block.macro
      if not m:match("\n$") then m = m .. "\n" end
      return m
    end
    if type(block.steps) == "table" then
      return compileSteps(block.steps, opts)
    end
  end
  return fallback
end

function SW.Decision:BuildButtonMacros(rotation, classSpecKey)
  rotation = rotation or {}

  local healer = isHealerRole()
  local allowOffheals = (not healer) and wantsOffheals()

  local stOffheal  = allowOffheals and blockHasOffheals(rotation.ST)
  local aoeOffheal = allowOffheals and blockHasOffheals(rotation.AOE)

  local stMacro = resolveBlock(rotation.ST, "/startattack\n", {
    healChain = (healer and HEAL_CHAIN) or (stOffheal and OFFHEAL_CHAIN) or nil
  })
  local aoeMacro = resolveBlock(rotation.AOE, stMacro, {
    healChain = (healer and HEAL_CHAIN) or (aoeOffheal and OFFHEAL_CHAIN) or nil
  })

  local intMacro =
    (rotation.INT and rotation.INT.macro)
    or (SW.Defaults and SW.Defaults:GetDefaultInterruptMacro(classSpecKey))
    or "/cast [harm] Kick\n"
  if not intMacro:match("\n$") then intMacro = intMacro .. "\n" end

  local utilMacro = (rotation.UTIL and rotation.UTIL.macro) or ""
  if utilMacro ~= "" and not utilMacro:match("\n$") then utilMacro = utilMacro .. "\n" end

  return stMacro, aoeMacro, intMacro, utilMacro
end

function SW.Decision:BuildHealMacro(rotation)
  if not isHealerRole() then return "" end
  rotation = rotation or {}
  local block = rotation.HEAL or rotation.ST
  local m = resolveBlock(block, "", { healChain = HEAL_CHAIN, noStartAttack = true })
  if m == "" then return "" end
  if not m:match("^/stopcasting") then
    m = "/stopcasting\n" .. m
  end
  return m
end
