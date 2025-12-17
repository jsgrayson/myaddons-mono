-- SkillWeaver Proc Policy
-- "Don't break the proc!"
-- Manages preferences for consuming procs and avoidance of wasting them.

local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local ProcPolicy = {}
SkillWeaver.ProcPolicy = ProcPolicy

-- Small, explicit rules. Expand per class/spec over time or via scraper.
ProcPolicy.rules = {
  -- FROST DK
  ["Killing Machine"] = {
    prefer = { "Obliterate" },             -- consume KM with Obliterate
    avoid  = { "Frost Strike" },           -- don't waste KM on FS (unless you want to relax this)
    ttlKey = "kmTTL",                      -- usually KM is buff, ttl is duration
  },
  ["Rime"] = {
    prefer = { "Howling Blast" },
    avoid  = { "Obliterate" },             -- optional: helps ensure you spend Rime before next Oblit?
    -- Actually standard frost often casts Oblit during Rime, but we PREFER HB.
    -- If we put Obliterate in 'avoid', we might deadlock if HB is on CD? 
    -- So be careful with 'avoid'. Prefer is safe.
    -- avoid = {}, 
    ttlKey = "rimeTTL",
  },
  
  -- UNHOLY DK
  ["Sudden Doom"] = {
    prefer = { "Death Coil", "Epidemic" },
    avoid  = {},
    ttlKey = "sdTTL",
  },
  
  -- FIRE MAGE
  ["Heating Up"] = {
    prefer = { "Fire Blast" }, -- convert to Hot Streak
    avoid = {},
  },
  ["Hot Streak"] = {
    prefer = { "Pyroblast", "Flamestrike" },
    avoid = { "Fireball" }, -- Don't hard cast fireball with instant pyro available? (Usually you cast fireball then pyro, but engine is instant decision)
  },
  
  -- RET PALADIN
  ["Divine Purpose"] = {
    prefer = { "Templar's Verdict", "Divine Storm" },
    avoid = {}, -- Free spenders match regular priority usually
  },
}

local function toSet(list)
  local s = {}
  for _, v in ipairs(list or {}) do s[v] = true end
  return s
end

-- Build cached sets for speed
ProcPolicy._compiled = nil
function ProcPolicy:Compile()
  if self._compiled then return end
  self._compiled = {}
  for proc, r in pairs(self.rules) do
    self._compiled[proc] = {
      prefer = toSet(r.prefer),
      avoid  = toSet(r.avoid),
      ttlKey = r.ttlKey,
    }
  end
end

-- Context should provide: context.procs["Killing Machine"]=true, etc.
local function hasProc(context, proc)
  return context and context.procs and context.procs[proc] == true
end

-- Optional TTL: if you don’t have durations, return nil and policy still works.
local function procTTL(context, ttlKey)
  if not context or not ttlKey then return nil end
  local v = context[ttlKey]
  if type(v) == "number" then return v end
  return nil
end

-- Should we block this spell because it would waste a proc?
function ProcPolicy:ShouldAvoidSpell(spell, context)
  self:Compile()
  if not spell or not context or not context.procs then return false end

  for proc, r in pairs(self._compiled) do
    if hasProc(context, proc) and r.avoid[spell] then
      -- Exception: if proc is about to expire, don't overthink it, just cast whatever
      local ttl = procTTL(context, r.ttlKey)
      if ttl and ttl <= 1.0 then
        return false
      end
      return true
    end
  end

  return false
end

-- Should we prefer this spell because it consumes an active proc?
function ProcPolicy:ShouldPreferSpell(spell, context)
  self:Compile()
  if not spell or not context or not context.procs then return false end

  for proc, r in pairs(self._compiled) do
    if hasProc(context, proc) and r.prefer[spell] then
      return true
    end
  end

  return false
end

-- A deterministic score bonus you can add into your existing step scoring.
function ProcPolicy:ScoreBonus(spell, context)
  if self:ShouldPreferSpell(spell, context) then
    local bonus = 6.0
    -- If it’s expiring, boost more (optional)
    for proc, r in pairs(self._compiled or {}) do
      if hasProc(context, proc) and r.prefer[spell] then
        local ttl = procTTL(context, r.ttlKey)
        if ttl and ttl <= 1.5 then 
             bonus = 15.0 -- PANIC SPEND
        end
      end
    end
    return bonus
  end
  return 0.0
end

return ProcPolicy
