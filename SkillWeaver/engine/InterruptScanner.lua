local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local InterruptScanner = {}
SkillWeaver.InterruptScanner = InterruptScanner

-- How many nameplates to scan (tune for performance)
InterruptScanner.maxPlates = 20

-- Iterate nameplates deterministically: nameplate1..N
local function iterNameplates(maxN)
  local i = 1
  return function()
    while i <= maxN do
      local unit = "nameplate" .. i
      i = i + 1
      if UnitExists(unit) and UnitCanAttack("player", unit) then
        return unit
      end
    end
    return nil
  end
end

local function unitCastInfo(unit)
    if not UnitCastingInfo then return nil end
    local name, text, texture, startTimeMs, endTimeMs, isTrade, castID, notInterruptible, spellID = UnitCastingInfo(unit)
    if not name then
      -- Channeling?
      name, text, texture, startTimeMs, endTimeMs, isTrade, notInterruptible, spellID = UnitChannelInfo(unit)
    end
    if not name then return nil end
    
    local nowMs = (GetTime() or 0) * 1000
    local remaining = (endTimeMs - nowMs) / 1000
    local elapsed = (nowMs - startTimeMs) / 1000
    local duration = (endTimeMs - startTimeMs) / 1000
    local progress = duration > 0 and (elapsed / duration) or 0
    return { name=name, spellID=spellID, notInterruptible=notInterruptible, remaining=remaining, progress=progress }
end

local function getInterruptInfo(context, spellID)
  local db = context and context.interruptDB
  if not db or not context.instanceID or not spellID then return nil end
  local inst = db[context.instanceID]
  return inst and inst[spellID] or nil
end

-- Deterministic score: higher = better interrupt target
local function scoreUnitCast(context, unit, cast)
  local info = getInterruptInfo(context, cast.spellID)
  local dangerous = info and info.dangerous or false
  local prio = info and info.priority or 999  -- lower number = higher priority in DB

  -- Convert priority to score (so prio 1 >> prio 5 >> prio 999)
  local prioScore = (prio == 999) and 0 or (100 - math.min(99, prio * 10))

  -- Prefer dangerous casts strongly
  local dangerScore = dangerous and 80 or 0

  -- Prefer later-in-cast (late-kick style), but don’t wait forever
  local progressScore = math.floor((cast.progress or 0) * 30) -- 0..30

  -- Prefer casts that still have time (avoid “already finished” edge)
  local remainingScore = (cast.remaining and cast.remaining > 0.15) and 10 or 0

  -- Slightly prefer your current target if tie
  local targetBias = (UnitIsUnit("target", unit) and 3 or 0)

  return dangerScore + prioScore + progressScore + remainingScore + targetBias, dangerous, prio
end

-- Choose the best unit to interrupt right now
function InterruptScanner:SelectUnit(context)
  context = context or {}

  local best = nil
  local bestScore = -1e9
  local bestMeta = nil

  for unit in iterNameplates(self.maxPlates) do
    local cast = unitCastInfo(unit)
    if cast and not cast.notInterruptible then
      -- Timing gate: only consider if past kickAt threshold
      -- If DB info exists, use dangerous logic, else use context default
      local info = getInterruptInfo(context, cast.spellID)
      local isDangerous = info and info.dangerous
      local kickAt = context.kickAt or (isDangerous and 0.20 or 0.60)
      
      if (cast.progress or 0) >= kickAt then
        local s, dangerous, prio = scoreUnitCast(context, unit, cast)
        if s > bestScore then
          bestScore = s
          best = unit
          bestMeta = { cast=cast, score=s, dangerous=dangerous, priority=prio }
        end
      end
    end
  end

  return best, bestMeta
end

return InterruptScanner
