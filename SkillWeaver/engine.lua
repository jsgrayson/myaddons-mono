-- ============================================================================
-- SkillWeaver Engine
-- Handles State Snapshots and Module Registry
-- ============================================================================

local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")

SkillWeaver.Engine = {}
local Engine = SkillWeaver.Engine

-- Registry
Engine.modules = {}

function Engine:RegisterModule(specId, module)
  self.modules[specId] = module
  if SkillWeaver.db and SkillWeaver.db.profile.settings.debug then
    SkillWeaver:Print("Engine: Registered module for spec " .. tostring(specId))
  end
end

function Engine:GetModuleForSpec(specId)
  return self.modules[specId]
end

-- ============================================================================
-- State Snapshot
-- ============================================================================

function Engine:GetState()
  local s = {}
  
  -- Time
  s.time = GetTime()
  s.gcdStart, s.gcdDuration = GetSpellCooldown(61304) -- Global Cooldown (using "GCD" spell id or generic)
  
  -- Player
  s.player = {
    health = UnitHealth("player"),
    healthMax = UnitHealthMax("player"),
    power = UnitPower("player"),
    powerMax = UnitPowerMax("player"),
    casting = UnitCastingInfo("player"),
    channeling = UnitChannelInfo("player"),
  }
  
  -- Target
  s.target = {
    exists = UnitExists("target"),
    canAttack = UnitCanAttack("player", "target"),
    health = UnitHealth("target"),
    healthMax = UnitHealthMax("target"),
    healthPct = 0,
  }
  
  if s.target.exists and s.target.healthMax > 0 then
    s.target.healthPct = s.target.health / s.target.healthMax
  end

  return s
end

-- ============================================================================
-- Scoring Interface (Default Fallback)
-- ============================================================================

function Engine:ScoreAction(action, state, specId)
  -- 1. Look up module
  local module = self:GetModuleForSpec(specId)
  if module and module.Score then
    return module:Score(action, state)
  end

  -- 2. Fallback: Static Analysis (Availability)
  -- Return 100 if usable, 0 if not.
  -- This essentially mimics the "Sequential MVP" but in score form.
  return 50 -- basic generic score
end
