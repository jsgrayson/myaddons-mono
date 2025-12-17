-- Core/Decision.lua
SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver

SW.Decision = SW.Decision or {}

local HEAL_CHAIN = "[@targettarget,help,nodead][@focus,help,nodead][@player]"
local OFFHEAL_CHAIN = "[@targettarget,help,nodead][@focus,help,nodead]" -- no self unless fallback

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

local function getRole()
  local specIndex = GetSpecialization()
  if not specIndex then return "DAMAGER" end
  return GetSpecializationRole(specIndex) or "DAMAGER"
end

local function isHealerRole()
  return getRole() == "HEALER"
end

local function isCastLine(cmd)
  return type(cmd) == "string" and cmd:match("^/cast%s+")
end

local function extractSpell(cmd)
  return cmd:match("^/cast%s+(.+)$")
end

local function stripBracketTargets(spell)
  -- if someone already has [@cursor] etc, do not touch it
  if spell:match("^%[") then return nil end
  return spell
end

local function makeGroundTargetPrefix()
  local mode = (SkillWeaverDB and SkillWeaverDB.toggles and SkillWeaverDB.toggles.groundTargetMode) or "cursor"
  if mode == "player" then
    return "[@player]"
  end
  return "[@cursor]"
end

local function wrapHealCast(cmd, isOffheal)
  if not isCastLine(cmd) then return cmd end
  local spell = extractSpell(cmd)
  if not spell or spell == "" then return cmd end

  -- If spell already has bracket conditionals, leave it alone.
  if spell:match("^%[") then
    return cmd
  end

  local chain = isOffheal and OFFHEAL_CHAIN or HEAL_CHAIN
  return ("/cast %s %s"):format(chain, spell)
end

local function wrapGroundTarget(cmd)
  if not isCastLine(cmd) then return cmd end
  local spell = extractSpell(cmd)
  if not spell or spell == "" then return cmd end

  -- If already specified [@cursor]/[@player]/etc, respect it
  if spell:match("^%[") then return cmd end

  if GROUND_SPELLS[spell] then
    local gt = makeGroundTargetPrefix()
    return ("/cast %s %s"):format(gt, spell)
  end

  return cmd
end

local function compileSteps(steps, policy)
  local lines = { "/startattack" }
  if type(steps) ~= "table" then
    return table.concat(lines, "\n") .. "\n"
  end

  for _, step in ipairs(steps) do
    if step and type(step.command) == "string" and step.command ~= "" then
      local cmd = step.command

      -- Ground targeting rewrite first (so heals like Efflo/Healing Rain become @cursor/@player)
      cmd = wrapGroundTarget(cmd)

      -- Heal routing: healers always routed; DPS only if toggle on and marked offheal
      if policy.wrapHeals then
        cmd = wrapHealCast(cmd, false)
      elseif policy.wrapOffheals then
        cmd = wrapHealCast(cmd, true)
      end

      table.insert(lines, cmd)
    end
  end

  return table.concat(lines, "\n") .. "\n"
end

-- Detect if a rotation is "mostly healer" (actual healer role determines routing),
-- but allow DPS emergency heals only when toggle is enabled.
local function wantsOffheals()
  return SkillWeaverDB
    and SkillWeaverDB.toggles
    and SkillWeaverDB.toggles.dpsEmergencyHeals == true
end

-- Healer spells we should treat as offheals when you are NOT a healer role.
-- (This is conservative; you can expand per class later.)
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

local function blockHasOffheals(block)
  if type(block) ~= "table" or type(block.steps) ~= "table" then return false end
  for _, step in ipairs(block.steps) do
    if step and type(step.command) == "string" then
      local spell = extractSpell(step.command)
      if spell and OFFHEAL_SPELLS[spell] then
        return true
      end
    end
  end
  return false
end

function SW.Decision:BuildButtonMacros(rotation, classSpecKey)
  rotation = rotation or {}

  local roleHealer = isHealerRole()
  local allowOffheals = (not roleHealer) and wantsOffheals()

  local function resolveBlock(block, fallback, treatAsOffhealBlock)
    if type(block) == "table" then
      if type(block.macro) == "string" and block.macro ~= "" then
        local m = block.macro
        if not m:match("\n$") then m = m .. "\n" end
        return m
      end
      if type(block.steps) == "table" then
        local policy = {
          wrapHeals = roleHealer,
          wrapOffheals = allowOffheals and treatAsOffhealBlock,
        }
        return compileSteps(block.steps, policy)
      end
    end
    return fallback
  end

  -- Treat ST/AOE blocks as offheal blocks only if they contain offheal spells and you're not a healer.
  local stOffheal  = allowOffheals and blockHasOffheals(rotation.ST)
  local aoeOffheal = allowOffheals and blockHasOffheals(rotation.AOE)

  local stMacro  = resolveBlock(rotation.ST, "/startattack\n", stOffheal)
  local aoeMacro = resolveBlock(rotation.AOE, stMacro, aoeOffheal)

  local intMacro =
    (rotation.INT and rotation.INT.macro)
    or (SW.Defaults and SW.Defaults:GetDefaultInterruptMacro(classSpecKey))
    or "/cast [harm] Kick\n"
  if not intMacro:match("\n$") then intMacro = intMacro .. "\n" end

  local utilMacro = (rotation.UTIL and rotation.UTIL.macro) or ""
  if utilMacro ~= "" and not utilMacro:match("\n$") then utilMacro = utilMacro .. "\n" end

  -- Offheal fallback: if offheal chain fails (no ToT/focus friendly), you still want a self-save sometimes.
  -- We provide that via UTIL in your offline tables (e.g., Word of Glory / Exhilaration / etc).
  return stMacro, aoeMacro, intMacro, utilMacro
end

function SW.Decision:BuildHealMacro(rotation)
  -- Only meaningful for healer roles; if not healer, return empty so button can be hidden/disabled if you want.
  local specIndex = GetSpecialization()
  if not specIndex then return "" end
  if (GetSpecializationRole(specIndex) or "DAMAGER") ~= "HEALER" then
    return ""
  end

  rotation = rotation or {}
  local block = rotation.HEAL -- allow offline pack to provide HEAL block; else empty

  -- compileSteps already wraps heals for healer role and applies ground targeting
  local policy = { wrapHeals = true, wrapOffheals = false }

  if type(block) == "table" then
    if type(block.macro) == "string" and block.macro ~= "" then
      local m = block.macro
      if not m:match("\n$") then m = m .. "\n" end
      return m
    end
    if type(block.steps) == "table" then
      -- reuse internal compiler
      local lines = { "/stopcasting" } -- optional, makes heals feel snappier
      local compiled = compileSteps(block.steps, policy) -- uses /startattack; not ideal for heal
      -- strip /startattack for heal macro
      compiled = compiled:gsub("^/startattack\n", "")
      return table.concat(lines, "\n") .. "\n" .. compiled
    end
  end

  return ""
end

-- Dedicated SELF button: always casts on player only
-- Dedicated SELF button: always casts on player only
function SW.Decision:BuildSelfMacro(rotation, classSpecKey)
  rotation = rotation or {}

  local block = rotation.SELF or rotation.UTIL
  local steps = (block and block.steps)

  -- If no SELF/UTIL steps provided, fall back to per-spec defaults
  if (not steps or type(steps) ~= "table") and SW.Defaults and SW.Defaults.GetDefaultSelfSteps then
    steps = SW.Defaults:GetDefaultSelfSteps(classSpecKey)
  end

  if block and type(block.macro) == "string" and block.macro ~= "" then
    local m = block.macro
    if not m:match("\n$") then m = m .. "\n" end
    return m
  end

  if not steps or type(steps) ~= "table" then return "" end

  local lines = { "/stopcasting" }
  for _, step in ipairs(steps) do
    if step and type(step.command) == "string" then
      local spell = step.command:match("^/cast%s+(.+)$")
      if spell then
        table.insert(lines, "/cast [@player] " .. spell)
      end
    end
  end

  return table.concat(lines, "\n") .. "\n"
end
