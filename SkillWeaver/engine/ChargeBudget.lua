local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local ChargeBudget = {}
SkillWeaver.ChargeBudget = ChargeBudget

-- Per-spell tuning (keep small; extend via scraper later)
ChargeBudget.spells = {
  -- Blood DK
  ["Blood Boil"] = { spendAtOrAbove = 1, aoeBonus = 0.6, capUrgency = 2.0 },
  ["Death and Decay"] = { spendAtOrAbove = 1, aoeBonus = 0.8, capUrgency = 1.5 },
  
  -- Frost
  ["Howling Blast"] = { spendAtOrAbove = 1, aoeBonus = 0.5, capUrgency = 1.0 }, -- Rime proc usually handles this, but raw validation helps
  
  -- Unholy
  ["Epidemic"] = { spendAtOrAbove = 1, aoeBonus = 1.0, capUrgency = 1.0 }, -- RP spender, not charge based usually, but if charges added...
  ["Festering Strike"] = { spendAtOrAbove = 1, aoeBonus = 0.2, capUrgency = 1.2 }, -- Generally not charged, but safe to list
  
  -- Warrior
  ["Charge"] = { spendAtOrAbove = 1, capUrgency = 0.5 },
  ["Raging Blow"] = { spendAtOrAbove = 1, capUrgency = 1.5 },
  ["Overpower"] = { spendAtOrAbove = 1, capUrgency = 1.2 },
  ["Shield Block"] = { spendAtOrAbove = 1, capUrgency = 2.0 },
  
  -- Mage
  ["Fire Blast"] = { spendAtOrAbove = 1, capUrgency = 2.5 }, -- Critical for Combustion
  ["Phoenix Flames"] = { spendAtOrAbove = 1, capUrgency = 1.8 },
  
  -- Hunter
  ["Barbed Shot"] = { spendAtOrAbove = 1, capUrgency = 2.5 }, -- Maintenance
  ["Kill Command"] = { spendAtOrAbove = 1, capUrgency = 1.1 },
  
  -- DH
  ["Fel Rush"] = { spendAtOrAbove = 1, capUrgency = 0.8 },
  ["Throw Glaive"] = { spendAtOrAbove = 1, capUrgency = 0.5 },
  
  -- Paladin
  ["Crusader Strike"] = { spendAtOrAbove = 1, capUrgency = 1.2 },
  ["Judgment"] = { spendAtOrAbove = 1, capUrgency = 1.1 },
  ["Hammer of Wrath"] = { spendAtOrAbove = 1, capUrgency = 1.5 },
  
  -- Monk
  ["Keg Smash"] = { spendAtOrAbove = 1, capUrgency = 2.0 },
  ["Rising Sun Kick"] = { spendAtOrAbove = 1, capUrgency = 1.5 },
}

local function getCharges(spell)
  if not spell or not GetSpellCharges then return nil end
  local charges, maxCharges, start, duration = GetSpellCharges(spell)
  if not charges then return nil end
  return {
    charges = charges,
    max = maxCharges or charges,
    start = start or 0,
    duration = duration or 0,
  }
end

local function timeToNextCharge(ch)
  if not ch or ch.charges >= ch.max then
    return 0
  end
  if not ch.start or ch.start == 0 or not ch.duration or ch.duration == 0 then
    return 0
  end
  local t = (ch.start + ch.duration) - (GetTime and GetTime() or 0)
  if t < 0 then t = 0 end
  return t
end

-- Deterministic score: higher = more urgent to spend NOW
function ChargeBudget:Score(spell, context)
  local cfg = self.spells[spell]
  if not cfg then return nil end

  local ch = getCharges(spell)
  if not ch or not ch.max or ch.max <= 1 then
    return nil
  end

  context = context or {}
  local ae = context.activeEnemies or 1
  local aoeBonus = (cfg.aoeBonus or 0) * math.max(0, ae - 1)
  local burstBonus = (context.burstWindow and 0.4 or 0.0)

  local ttn = timeToNextCharge(ch)

  -- Cap urgency: if we're at max charges, huge score (spend ASAP)
  local capUrgency = (cfg.capUrgency or 2.0)
  local capScore = 0
  if ch.charges >= ch.max then
    capScore = 10 * capUrgency
  else
    -- if next charge is soon, spending now prevents cap soon
    capScore = (ttn <= 2.0) and (3.0 * capUrgency) or (1.0 * capUrgency)
  end

  -- Charge amount bias
  local chargeScore = (ch.charges / ch.max) * 3.0

  return capScore + chargeScore + aoeBonus + burstBonus
end

-- Hard allow/deny: if at cap, always allow; else allow based on threshold
function ChargeBudget:ShouldPrefer(spell, context)
  local cfg = self.spells[spell]
  if not cfg then return false end

  local ch = getCharges(spell)
  if not ch or not ch.max then return false end

  if ch.charges >= ch.max then
    return true
  end

  -- If we have >= spendAtOrAbove charges and next charge is soon, prefer spending
  local spendAt = cfg.spendAtOrAbove or 1
  if ch.charges >= spendAt then
    local ttn = timeToNextCharge(ch)
    if ttn <= 2.0 then
      return true
    end
  end

  return false
end

return ChargeBudget
