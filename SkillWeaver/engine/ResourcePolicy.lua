-- engine/ResourcePolicy.lua
local addonName, addonTable = ...
local ResourcePolicy = {}
addonTable.ResourcePolicy = ResourcePolicy

local ResourceProvider = addonTable.ResourceProvider

ResourcePolicy.defaults = {
  enablePooling = true,

  -- pooling for burst
  poolForBurst = true,
  burstSoonWindow = 6.0,
  targetPoolPct = 0.80,       -- pool to 80% of cap (generic)
  minTTDToPool = 10.0,

  -- dump to avoid cap
  dumpAtPct = 0.90,           -- prefer spenders at 90%+
  nearCapPct = 0.90,          -- ResourceProvider uses this too
}

-- Spell role mapping should be data-driven via policy packs:
-- context.policy.resources.spells = { ["Frost Strike"]={role="spender"}, ... }
local function spellRole(spell, context)
  local p = context and context.policyPack -- policyPack in context usually
  if not p then return nil end
  local map = p.resources and p.resources.spells
  if map and map[spell] and map[spell].role then return map[spell].role end
  return nil
end

local function burstSoon(context, rules)
  if context.burstWindow then return false end
  if context.forceBurst then return true end
  if context.burstSoonSeconds ~= nil then
    return context.burstSoonSeconds <= (rules.burstSoonWindow or 6.0)
  end
  return false
end

function ResourcePolicy:IsPooling(context)
  local rules = (context and context.resourceRules) or self.defaults
  if not rules.enablePooling then return false end

  local ttd = (context and context.targetTTD) or 999
  if ttd < (rules.minTTDToPool or 0) then return false end

  if rules.poolForBurst and burstSoon(context, rules) then
    return true
  end

  return false
end

function ResourcePolicy:ShouldHoldSpender(spell, context)
  local rules = (context and context.resourceRules) or self.defaults
  if not rules.enablePooling then return false end

  local role = spellRole(spell, context)
  if role ~= "spender" then return false end
  
  -- Use provider
  if not ResourceProvider then ResourceProvider = addonTable.ResourceProvider end
  local rs = ResourceProvider:Get(context)
  local dumpAtPct = rules.dumpAtPct or 0.90

  -- Never hold if near cap (avoid wasting regen)
  if rs.pct >= dumpAtPct then
    return false
  end

  -- If pooling, hold spenders until we hit target pool %
  if self:IsPooling(context) then
    local targetPct = rules.targetPoolPct or 0.80
    if rs.pct < targetPct then
      return true
    end
  end

  return false
end

function ResourcePolicy:ShouldPreferSpender(spell, context)
  local rules = (context and context.resourceRules) or self.defaults
  local role = spellRole(spell, context)
  if role ~= "spender" then return false end

  if not ResourceProvider then ResourceProvider = addonTable.ResourceProvider end
  local rs = ResourceProvider:Get(context)
  local dumpAtPct = rules.dumpAtPct or 0.90
  return rs.pct >= dumpAtPct
end

return ResourcePolicy
