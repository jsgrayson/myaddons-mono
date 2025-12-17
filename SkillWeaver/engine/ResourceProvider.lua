-- engine/ResourceProvider.lua
local addonName, addonTable = ...
local ResourceProvider = {}
addonTable.ResourceProvider = ResourceProvider

local SpecRegistry = addonTable.SpecRegistry

-- Power types by token (WoW uses Enum.PowerType; we keep it string-safe)
ResourceProvider.powerMap = {
  MANA = 0,
  RAGE = 1,
  FOCUS = 2,
  ENERGY = 3,
  COMBO_POINTS = 4,
  RUNIC_POWER = 6,
  SOUL_SHARDS = 7,
  MAELSTROM = 11,
  CHI = 12,
  INSANITY = 13,
  HOLY_POWER = 9,
  ARCANE_CHARGES = 16,
}

-- Per-spec preferred "primary spend resource"
-- (If absent, we fall back to registry.resource heuristic)
ResourceProvider.primaryBySpecKey = {
  -- DK
  DEATHKNIGHT_250 = "RUNIC_POWER",
  DEATHKNIGHT_251 = "RUNIC_POWER",
  DEATHKNIGHT_252 = "RUNIC_POWER",
}

local function getPowerType(token)
  return ResourceProvider.powerMap[token]
end

local function unitPower(unit, token)
  local pt = getPowerType(token)
  if pt == nil or not UnitPower then return nil end
  return UnitPower(unit, pt)
end

local function unitPowerMax(unit, token)
  local pt = getPowerType(token)
  if pt == nil or not UnitPowerMax then return nil end
  return UnitPowerMax(unit, pt)
end

-- Some "secondary" resources are better treated as 0..max points
local function points(unit, token)
  local cur = unitPower(unit, token)
  local cap = unitPowerMax(unit, token)
  if cur == nil or cap == nil then return nil end
  return { cur=cur, cap=cap, deficit=(cap-cur) }
end

-- Determine specKey -> primary token
local function choosePrimary(specKey, context)
  if context and context.primaryResource then return context.primaryResource end
  if specKey and ResourceProvider.primaryBySpecKey[specKey] then
    return ResourceProvider.primaryBySpecKey[specKey]
  end

  -- fallback: inspect registry resource string and map common ones
  if context and context.registryResource then
    local r = context.registryResource
    if type(r) == "string" then
      if r:find("RUNIC_POWER") then return "RUNIC_POWER" end
      if r:find("ENERGY") then return "ENERGY" end
      if r:find("RAGE") then return "RAGE" end
      if r:find("FOCUS") then return "FOCUS" end
      if r:find("MANA") then return "MANA" end
      if r:find("HOLY_POWER") then return "HOLY_POWER" end
      if r:find("INSANITY") then return "INSANITY" end
      if r:find("MAELSTROM") then return "MAELSTROM" end
      if r:find("CHI") then return "CHI" end
      if r:find("SOUL_SHARDS") then return "SOUL_SHARDS" end
      if r:find("ARCANE_CHARGES") then return "ARCANE_CHARGES" end
      if r:find("COMBO_POINTS") then return "COMBO_POINTS" end
    end
  end

  return "MANA" -- safe default
end

-- Public: returns normalized resource state
function ResourceProvider:Get(context)
  context = context or {}
  local unit = context.resourceUnit or "player"
  local specKey = context.specKey

  local primary = choosePrimary(specKey, context)
  local cur = unitPower(unit, primary) or 0
  local cap = unitPowerMax(unit, primary) or 100
  local deficit = cap - cur
  local pct = (cap > 0) and (cur / cap) or 0

  -- "nearCap" threshold can be tuned per spec via context.resourceRules.nearCapPct
  local nearPct = (context.resourceRules and context.resourceRules.nearCapPct) or 0.90
  local nearCap = pct >= nearPct

  -- Optional secondary resources (common patterns)
  local secondary = {}
  secondary.COMBO_POINTS = points(unit, "COMBO_POINTS")
  secondary.HOLY_POWER = points(unit, "HOLY_POWER")
  secondary.CHI = points(unit, "CHI")
  secondary.SOUL_SHARDS = points(unit, "SOUL_SHARDS")
  secondary.ARCANE_CHARGES = points(unit, "ARCANE_CHARGES")

  return {
    token = primary,
    cur = cur,
    cap = cap,
    deficit = deficit,
    pct = pct,
    nearCap = nearCap,
    secondary = secondary,
  }
end

return ResourceProvider
