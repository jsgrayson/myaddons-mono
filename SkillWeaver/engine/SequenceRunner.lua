local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local SequenceRunner = {}
SkillWeaver.SequenceRunner = SequenceRunner

-- Mock ConditionParser to map to SkillWeaver:EvaluateCondition
local ConditionParser = {
  Evaluate = function(self, cond, context)
    return SkillWeaver:EvaluateCondition(cond, context)
  end
}

-- Per-player runtime pointers (keep in SkillWeaver_SV if you want persistence)
SequenceRunner.state = {
  pointers = {
    st = 1,
    aoe = 1
  }
}

-- --- Helpers ------------------------------------------------

local function getBlockName(context)
  -- context.activeEnemies should be provided by your engine/environment layer
  if (context.activeEnemies or 0) >= (context.aoeThreshold or 3) then
    return "aoe"
  end
  return "st"
end

local function defaultTrue(cond)
  return cond == nil or cond == "" or cond == "true"
end

-- Extract spell name from "/cast X" (very simple; supports "/cast [mod] X" lightly)
local function extractCastName(command)
  if type(command) ~= "string" then return nil end
  local body = command:gsub("^/cast%s+", "")
  -- strip bracket conditionals if present: "/cast [@target] Spell"
  body = body:gsub("^%b[]%s*", "")
  body = body:gsub("^%b[]%s*", "") -- twice to be safe with two bracket groups
  body = body:gsub("%s*$", "")
  if body == "" then return nil end
  return body
end

-- --- Core: execute one step ---------------------------------

function SequenceRunner:TryStep(step, context)
  if type(step) ~= "table" or type(step.command) ~= "string" then
    return false
  end

  -- Condition evaluation
  if not defaultTrue(step.conditions) then
    if not ConditionParser:Evaluate(step.conditions, context) then
      return false
    end
  end

  -- Optional: can_cast gating (if you want it centralized here)
  -- If you already implement can_cast:* inside ConditionParser, remove this block.
  if step.conditions and step.conditions:find("can_cast:") then
    -- already handled by ConditionParser
  end

  -- Execute macro command
  SkillWeaver:ExecuteCommand(step.command)

  -- Track for overlay / debugging
  local spell = extractCastName(step.command)
  if context then
      context.lastExecuted = { command = step.command, spell = spell }
  end

  return true
end

-- --- Priority block -----------------------------------------

function SequenceRunner:RunPriority(steps, context)
  for i = 1, #steps do
    if self:TryStep(steps[i], context) then
      return true
    end
  end
  return false
end

-- --- Sequential block (deterministic pointer) ----------------

function SequenceRunner:RunSequential(steps, blockName, context)
  local ptr = self.state.pointers[blockName] or 1
  if ptr < 1 then ptr = 1 end
  if ptr > #steps then ptr = 1 end

  -- Deterministic: try current pointer first; if it fails, advance until one succeeds or we wrap.
  local start = ptr

  repeat
    if self:TryStep(steps[ptr], context) then
      -- advance pointer for next call
      ptr = ptr + 1
      if ptr > #steps then ptr = 1 end
      self.state.pointers[blockName] = ptr
      return true
    end

    ptr = ptr + 1
    if ptr > #steps then ptr = 1 end
  until ptr == start

  -- none valid; keep pointer where it was (or set to 1)
  self.state.pointers[blockName] = start
  return false
end

-- --- Main entry ---------------------------------------------

-- normalizedSeq:
-- {
--   meta = { exec="Priority"|"Sequential", ... },
--   blocks = { st={...}, aoe={...} }
-- }
function SequenceRunner:Tick(normalizedSeq, context)
  if type(normalizedSeq) ~= "table" or type(normalizedSeq.meta) ~= "table" or type(normalizedSeq.blocks) ~= "table" then
    return false
  end

  context = context or {}
  local blockName = slightly_renamed_getBlockName and slightly_renamed_getBlockName(context) or getBlockName(context)
  local steps = normalizedSeq.blocks[blockName] or {}
  if #steps == 0 then
    -- fallback to ST if AOE empty
    steps = normalizedSeq.blocks.st or {}
    blockName = "st"
  end
  if #steps == 0 then return false end

  local exec = normalizedSeq.meta.exec or "Priority"

  if exec == "Sequential" then
    return self:RunSequential(steps, blockName, context)
  else
    return self:RunPriority(steps, context)
  end
end

return SequenceRunner
