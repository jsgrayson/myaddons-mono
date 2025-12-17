local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local InterruptAuthority = {}
SkillWeaver.InterruptAuthority = InterruptAuthority

-- Priority order of your tools (per spec you can override)
InterruptAuthority.defaultKit = {
  { spell = "Mind Freeze",  range = 15, type = "kick" },
  { spell = "Gnaw",         range = 30, type = "pet_stun", requiresPet = true },
  { spell = "Asphyxiate",   range = 20, type = "stun" },
  { spell = "Strangulate",  range = 30, type = "silence" },
  -- Add other classes/specs common kicks here or populate dynamically
  { spell = "Kick", range = 5, type = "kick" },
  { spell = "Pummel", range = 5, type = "kick" },
  { spell = "Rebuke", range = 5, type = "kick" },
  { spell = "Counterspell", range = 40, type = "kick" },
  { spell = "Wind Shear", range = 30, type = "kick" },
  { spell = "Solar Beam", range = 40, type = "silence" },
  { spell = "Spear Hand Strike", range = 5, type = "kick" },
  { spell = "Muzzle", range = 5, type = "kick" },
  { spell = "Silence", range = 40, type = "silence" },
  { spell = "Disrupt", range = 5, type = "kick" },
  { spell = "Skull Bash", range = 13, type = "kick" },
}

-- Pull from your interrupt DB if present (Stub for now)
-- InterruptsDB[instanceID][spellID] = { priority=1..N, dangerous=true, notes="..." }
local function getInterruptInfo(context, spellID)
  local db = context and context.interruptDB
  if not db or not context.instanceID or not spellID then return nil end
  local inst = db[context.instanceID]
  return inst and inst[spellID] or nil
end

local function unitCastInfo(unit)
  if not UnitCastingInfo then return nil end
  local name, text, texture, startTimeMs, endTimeMs, isTrade, castID, notInterruptible, spellID = UnitCastingInfo(unit)
  if not name then
      -- Channeling?
    name, text, texture, startTimeMs, endTimeMs, isTrade, notInterruptible, spellID = UnitChannelInfo(unit)
  end
  if not name then return nil end
  
  -- Handle timestamps (GetTime is seconds, unit cast is ms)
  local nowMs = (GetTime() or 0) * 1000
  local remain = (endTimeMs - nowMs) / 1000
  local elapsed = (nowMs - startTimeMs) / 1000
  local duration = (endTimeMs - startTimeMs) / 1000
  local pct = duration > 0 and (elapsed / duration) or 0
  
  return {
    name = name, spellID = spellID, notInterruptible = notInterruptible,
    remaining = remain, progress = pct,
  }
end

local function inRange(spell, unit)
  if not IsSpellInRange or not spell then return true end
  local r = IsSpellInRange(spell, unit)
  if r == nil then return true end
  return r == 1
end

local function cdReady(spell)
  if not GetSpellCooldown then return true end
  local start, dur, en = GetSpellCooldown(spell)
  if not en or en == 0 then return false end
  if not start or start == 0 or not dur then return true end
  return (start + dur - (GetTime() or 0)) <= 0
end

local function canUseTool(tool, context)
  if tool.requiresPet and not (context and context.petExists) then return false end
  if not cdReady(tool.spell) then return false end
  if not inRange(tool.spell, context.interruptUnit or "target") then return false end
  return true
end

-- Core decision: should we interrupt now, and with what?
function InterruptAuthority:Decide(context)
  context = context or {}

  local unit = context.interruptUnit
  local meta = nil
  
  -- Auto-scan if requested or defaulted
  if (not unit or unit == "AUTO") and SkillWeaver.InterruptScanner then
      unit, meta = SkillWeaver.InterruptScanner:SelectUnit(context)
  end
  
  -- Fallback to target if scanning failed or disabled (and unit wasn't manual)
  if not unit and (not context.interruptUnit or context.interruptUnit == "AUTO") then
      unit = "target"
  end

  if not UnitExists(unit) then return nil end
  if not UnitCanAttack("player", unit) then return nil end -- Sanity check

  local cast = unitCastInfo(unit)
  if not cast then return nil end
  if cast.notInterruptible then return nil end

  -- Determine if this cast is worth interrupting (DB + generic rules)
  -- MVP: Treat all interruptible casts as candidates if no DB
  
  -- local info = getInterruptInfo(context, cast.spellID)
  -- local dangerous = info and info.dangerous or false
  -- local priority = info and info.priority or 999
  
  -- MVP Fallback: Everything is interruptible if we don't have a DB yet.
  local dangerous = false
  local priority = 1

  -- Generic timing: don’t kick instantly; default to “late kick” unless dangerous
  local kickAt = context.kickAt or (dangerous and 0.20 or 0.50) -- slightly aggressive default for MVP testing
  if cast.progress < kickAt then
    -- Wait... unless remaining is tiny
    if cast.remaining > (context.minKickRemaining or 0.5) then
        return nil
    end
  end

  -- Pick best available tool
  local kit = context.interruptKit or self.defaultKit
  for _, tool in ipairs(kit) do
    if canUseTool(tool, context) then
      return {
        action = tool.spell,
        unit = unit,
        cast = cast,
        priority = priority,
        dangerous = dangerous,
        toolType = tool.type,
        meta = meta, -- Carry over scanner metadata
      }
    end
  end

  return nil
end

return InterruptAuthority
