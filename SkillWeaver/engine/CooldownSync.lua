local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local CooldownSync = {}
SkillWeaver.CooldownSync = CooldownSync

-- Sync groups: define a "leader" burst button and its desired partners.
-- If leader is ready but partners aren't, we may wait up to maxWait seconds.
CooldownSync.groups = {
  -- Frost DK example
  ["Pillar of Frost"] = {
    partners = { "Empower Rune Weapon", "Frostwyrm's Fury" },
    maxWait = 6.0,
    minTTD  = 12.0,
  },

  -- Blood DK example
  ["Dancing Rune Weapon"] = {
    partners = { "Tombstone" },
    maxWait = 5.0,
    minTTD  = 10.0,
  },

  -- Unholy DK example
  ["Summon Gargoyle"] = {
    partners = { "Dark Transformation", "Unholy Assault" },
    maxWait = 7.0,
    minTTD  = 14.0,
  },
  
  -- Add other specs here or populate dynamically
  ["Combustion"] = { partners = { "Fire Blast", "Rune of Power" }, maxWait=4.0, minTTD=15.0 },
  ["Adrenaline Rush"] = { partners = { "Blade Flurry" }, maxWait=3.0, minTTD=10.0 },
}

-- If holding a cooldown would cause you to lose a cast over the fight window, don't hold it.
-- "fightRemaining" can be estimated or just use a large number if unknown.
local function wouldLoseUse(cooldown, fightRemaining, holdFor)
  if not cooldown or cooldown <= 0 then return false end
  if not fightRemaining or fightRemaining <= 0 then return false end
  -- If by holding, you push the next use beyond remaining time, you've lost a use.
  return (cooldown + holdFor) > fightRemaining
end

-- Cooldown queries (adapt these if you already have wrappers)
local function spellCooldown(spell)
  if not spell then return 999 end
  -- Assuming C_Spell or GetSpellCooldown usage. Using classic API for compatibility/simplicity here.
  local start, duration, enabled = GetSpellCooldown(spell)
  if not enabled or enabled == 0 then return 999 end
  if not start or start == 0 or not duration then return 0 end
  local cd = (start + duration) - GetTime()
  if cd < 0 then cd = 0 end
  return cd
end

local function spellCharges(spell)
  if not spell then return nil end
  local charges, maxCharges, start, duration = GetSpellCharges(spell)
  if not charges then return nil end
  return { charges = charges, max = maxCharges or charges, start = start, duration = duration }
end

local function minCdOfPartners(partners)
  local minCd = 0
  for _, p in ipairs(partners or {}) do
    local cd = spellCooldown(p)
    -- We want the MAX of the partner cooldowns? Wait...
    -- Prompt logic: "If leader is ready but partners aren't..."
    -- Generally you want to wait for the *slowest* critical partner, but
    -- standard logic is usually "wait for ALL partners", so we track the max delay needed.
    -- Wait, prompt said "minCdOfPartners" iterating > minCd. That finds the *largest* CD among partners. 
    -- Naming confusion in prompt vs logic. Let's stick to "Max CD of partners" effectively determines wait time.
    if cd > minCd then minCd = cd end
  end
  return minCd
end

-- Returns true if we should HOLD this spell right now to sync.
function CooldownSync:ShouldHold(spell, context)
  local g = self.groups[spell]
  if not g then return false end

  context = context or {}
  local ttd = context.targetTTD or 999
  if ttd < (g.minTTD or 0) then
    return false -- Don't hold if target dying (just send it if Policy allows, or Policy blocks it anyway)
  end

  local partnerWait = minCdOfPartners(g.partners)
  if partnerWait <= 0 then
    return false -- partners ready, don't hold
  end

  local maxWait = g.maxWait or 0
  if partnerWait > maxWait then
    -- too long to wait; don't hold
    return false
  end

  -- Charge-aware exception: if this spell has charges and is (near) capped, don't hold
  local ch = spellCharges(spell)
  if ch and ch.max and ch.charges and ch.charges >= ch.max then
    return false
  end

  -- Don't hold if we'd lose a use (need fightRemaining estimate; if unknown, ignore)
  if wouldLoseUse(spellCooldown(spell), context.fightRemaining, partnerWait) then
    return false
  end

  -- Optional: if user forces burst, don't hold
  if context.forceBurst then
    return false
  end

  return true -- HOLD IT, waiting for sync
end

return CooldownSync
