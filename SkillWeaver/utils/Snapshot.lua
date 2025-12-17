-- utils/Snapshot.lua
local addonName, addonTable = ...
local Snapshot = {}
addonTable.Snapshot = Snapshot

local function hasAura(name, unit)
  if not AuraUtil or not AuraUtil.FindAuraByName then return false end
  return AuraUtil.FindAuraByName(name, unit) ~= nil
end

local function cdRemains(spell)
  if not GetSpellCooldown then return 999 end
  local start, dur, en = GetSpellCooldown(spell)
  if not en or en == 0 then return 999 end
  if not start or start == 0 or not dur then return 0 end
  local t = (start + dur) - (GetTime() or 0)
  if t < 0 then t = 0 end
  return t
end

-- Keep this SMALL. Add fields only when tests need them.
function Snapshot:Capture(context, chosenCommand)
  context = context or {}

  local snap = {
    t = GetTime and GetTime() or 0,
    -- specKey = context.specKey,                -- you set this upstream if available
    -- profile = context.profileName,
    -- variant = context.variantName,
    block = context.__blockName,
    section = context.__sectionName,

    enemies = context.activeEnemies,
    isBoss = context.isBoss or false,
    ttd = context.targetTTD,

    rp = context.runicPower or (UnitPower and UnitPower("player") or 0),

    procs = {
      KM = hasAura("Killing Machine", "player"),
      Rime = hasAura("Rime", "player"),
      SD = hasAura("Sudden Doom", "player"),
    },
    
    -- Capture simple CDs that might affect logic. 
    -- Ideally, we iterate context.cooldownRules to see what matters, but hardcoded common ones is fine for MVP.
    cds = {
      Pillar = cdRemains("Pillar of Frost"),
      DRW = cdRemains("Dancing Rune Weapon"),
      DT = cdRemains("Dark Transformation"),
      Apoc = cdRemains("Apocalypse"),
      ERW = cdRemains("Empower Rune Weapon"),
      MindFreeze = cdRemains("Mind Freeze"),
    },

    chosen = chosenCommand, -- what the engine executed (macro string)
  }

  return snap
end

return Snapshot
