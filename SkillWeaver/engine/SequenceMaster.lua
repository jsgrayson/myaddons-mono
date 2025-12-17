local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local Master = {}
SkillWeaver.SequenceMaster = Master

-- Required modules (attached to SkillWeaver during load)
-- engine/SequenceNormalize.lua
-- engine/SectionSplit.lua
-- engine/SequenceRunner.lua
-- engine/SectionScheduler.lua

local function chooseBlock(context, seq)
  local ae = context.activeEnemies or 0
  local th = context.aoeThreshold or 3
  
  -- Heuristic: If we are in AoE mode, check if the Core section has AoE steps.
  -- If not, fallback to ST (or if "Force AoE" isn't on).
  -- Simple check:
  if ae >= th then
     -- Check if we have AoE steps in Core?
     if seq.sections and seq.sections.core and #(seq.sections.core.aoe or {}) > 0 then
        return "aoe"
     end
     -- Checking legacy blocks for fallback
     if seq.blocks and #(seq.blocks.aoe or {}) > 0 then
        return "aoe"
     end
  end
  return "st"
end

-- The Master Tick
-- Inputs:
--   normalizedSeq: The meta+blocks/sections object. 
--   context: Runtime context (activeEnemies, etc.)
function Master:Tick(normalizedSeq, context)
  local Runner = SkillWeaver.SequenceRunner
  local Schedule = SkillWeaver.SectionScheduler
  local Split = SkillWeaver.SectionSplit
  
  if not (Runner and Schedule and Split) then return false end
  if not normalizedSeq then return false end

  -- 1. Create sections if not present (Splitting)
  if not normalizedSeq.sections then
    normalizedSeq.sections = Split:FromBlocks(normalizedSeq.blocks or { st={}, aoe={} })
  end
  
  -- 2. Determine Block (ST vs AoE)
  local blockName = chooseBlock(context or {}, normalizedSeq)
  context = context or {}
  
  -- 3. Setup Pointer Key Prefix (for Sequential memory)
  local profileName = normalizedSeq.meta.profile or "Profile"
  local key = normalizedSeq.meta.key or "UnknownSpec"
  context.__ptrKeyPrefix = key .. ":" .. profileName

  -- 4. Execute Sections
  for _, sectionName in ipairs(Schedule.order) do
    context.__sectionName = sectionName
    
    local execType = 
       (normalizedSeq.meta.sectionExec and normalizedSeq.meta.sectionExec[sectionName])
       or Schedule.defaultExec[sectionName]
       or (normalizedSeq.meta.exec or "Priority") -- fallback to global meta exec
       
    local steps = (normalizedSeq.sections[sectionName] and normalizedSeq.sections[sectionName][blockName]) or {}
    
    if #steps > 0 then
      if Schedule:RunSection(Runner, steps, execType, blockName, context) then
        -- Action found and executed (stored in SkillWeaver.nextAction by Runner)
        return true
      end
    end
  end

  return false
end

return Master
