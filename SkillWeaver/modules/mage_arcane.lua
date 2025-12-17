-- ============================================================================
-- Arcane Mage Module (Spec ID 62)
-- ============================================================================

local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local Engine = SkillWeaver.Engine

local MOD = {}
local SPEC_ID = 62 

-- ============================================================================
-- Scoring Logic
-- ============================================================================

function MOD:Score(action, state)
  local score = 0
  
  -- Mock Logic for Prototype
  
  -- 1. Arcane Blast (Builder)
  if action == "Arcane Blast" then
    score = 50
    -- If low charges, higher priority
    local charges = UnitPower("player", Enum.PowerType.ArcaneCharges) or 0
    if charges < 4 then score = 80 end
  end

  -- 2. Arcane Barrage (Spender)
  if action == "Arcane Barrage" then
    local charges = UnitPower("player", Enum.PowerType.ArcaneCharges) or 0
    if charges >= 4 then 
        score = 90 -- Dump at 4 stacks
    else
        score = 10 -- Don't dump early
    end
  end

  -- 3. Evocation (Mana)
  if action == "Evocation" then
    local manaPct = 0
    if state.player.powerMax > 0 then
        manaPct = state.player.power / state.player.powerMax
    end
    if manaPct < 0.2 then score = 100 end -- Emergency
  end

  return score
end

-- ============================================================================
-- Registration
-- ============================================================================
if Engine then
  Engine:RegisterModule(SPEC_ID, MOD)
end
