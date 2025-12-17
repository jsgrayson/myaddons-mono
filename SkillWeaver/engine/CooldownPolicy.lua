local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local CooldownPolicy = {}
SkillWeaver.CooldownPolicy = CooldownPolicy

-- Tune these globally
CooldownPolicy.defaults = {
  bossOnlyMajor = true,
  minCombatTime = 2.0,          -- seconds since entering combat
  minTTD        = 8.0,          -- don't pop majors if target dies too soon
  allowOnTrash  = false,        -- if false, major CDs only on bosses
  requireBurstWindow = false,
}

-- Spell buckets (keep tiny; expand over time or generate from scraper)
CooldownPolicy.major = {
  ["Pillar of Frost"] = true,
  ["Dancing Rune Weapon"] = true,
  ["Army of the Dead"] = true,
  ["Summon Gargoyle"] = true,
  ["Frostwyrm's Fury"] = true,
  ["Combustion"] = true,
  ["Icy Veins"] = true,
  ["Arcane Power"] = true,
  ["Avenging Wrath"] = true,
  ["Metamorphosis"] = true,
  ["Ascendance"] = true,
  ["Trueshot"] = true,
  ["Coordinated Assault"] = true,
  ["Adrenaline Rush"] = true,
  ["Shadow Blades"] = true,
  ["Vendetta"] = true, -- Or Deathmark
  ["Deathmark"] = true,
  ["Void Eruption"] = true,
  ["Dark Ascension"] = true,
  ["Power Infusion"] = true,
  ["Celestial Alignment"] = true,
  ["Incarnation: Chosen of Elune"] = true,
  ["Incarnation: King of the Jungle"] = true,
  ["Berserk"] = true,
  ["Bloodlust"] = true,
  ["Heroism"] = true,
  ["Time Warp"] = true,
}

CooldownPolicy.minor = {
  ["Dark Transformation"] = true,
  ["Empower Rune Weapon"] = true,
  ["Abomination Limb"] = true,
  ["Apocalypse"] = true,
  ["Raise Dead"] = true,
  ["Rune of Power"] = true,
  ["Mirror Image"] = true,
  ["Shifting Power"] = true,
  ["Divine Toll"] = true,
  ["Bastion of Spear"] = true, -- Bastion of Spear / Spear of Bastion?
  ["Spear of Bastion"] = true,
  ["Thunderous Roar"] = true,
  ["Ravager"] = true,
  ["Blade Flurry"] = true,
  ["Symbol of Hope"] = true,
}

function CooldownPolicy:IsMajor(spell) return self.major[spell] == true end
function CooldownPolicy:IsMinor(spell) return self.minor[spell] == true end

-- Central gate: return true if we should ALLOW attempting this cooldown
function CooldownPolicy:AllowCooldown(spell, context, rules)
  rules = rules or self.defaults
  context = context or {}

  if not spell then return true end
  
  -- If not tracked as major, we allow it (minors pass through unless restricted)
  local major = self:IsMajor(spell)

  -- Don’t blow CDs out of combat / immediately on pull unless you want to
  if (context.combatTime or 0) < (rules.minCombatTime or 0) then
    -- Allow minors early, block majors early (unless Precombat section overrides this, but Policy is checked in Cooldowns section)
    if major then return false end
  end

  -- Boss / trash logic
  if major then
    if rules.bossOnlyMajor and not context.isBoss then
      return false
    end
    -- Redundant check for clarity? "allowOnTrash" overrides "bossOnlyMajor"?
    -- Logic: active if (bossOnlyMajor is false OR isBoss) AND active if (allowOnTrash is true OR isBoss)
    -- Simplified: If major, and bossOnly, block if not boss.
    -- If major, and !allowOnTrash, block if not boss.
    if rules.allowOnTrash == false and (context.isBoss == false) then
        return false
    end
  end

  -- Time-to-die gate (prevents wasting big CDs)
  if major and (context.targetTTD or 999) < (rules.minTTD or 0) then
    return false
  end

  -- Burst window coordination (optional)
  -- If you have a burst window active, allow majors; if not, you can require it.
  if major and rules.requireBurstWindow and not context.burstWindow then
    return false
  end

  return true
end

return CooldownPolicy
