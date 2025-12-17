-- utils/DecisionTrace.lua
local addonName, addonTable = ...
local Trace = {}
addonTable.DecisionTrace = Trace -- expose internally if needed, or via return

Trace.max = 80
Trace.enabled = 1 -- 0 off, 1 normal, 2 verbose

SkillWeaver_Trace = SkillWeaver_Trace or { items = {} }

local function push(item)
  local t = SkillWeaver_Trace.items
  t[#t+1] = item
  if #t > Trace.max then
    table.remove(t, 1)
  end
end

function Trace:Enable()
    self.enabled = 1
end

function Trace:Disable()
    self.enabled = 0
end

function Trace:SetLevel(n)
  self.enabled = tonumber(n) or 0
end

function Trace:GetLevel()
    return self.enabled
end

function Trace:Log(event)
  if self.enabled <= 0 then return end
  event.t = GetTime and GetTime() or 0
  push(event)
end

function Trace:LogBlocked(step, reason, context)
  if self.enabled <= 0 then return end
  if self.enabled == 1 and reason.details == "verbose" then return end -- Filter verbose blocks if level 1

  -- Extract command safely
  local cmd = step.command or "?"
  
  self:Log({
    kind = "blocked",
    section = context.__sectionName,
    block = context.__blockName,
    command = cmd,
    reason = reason.code or "UNKNOWN",
    detail = reason.detail,
  })
end

function Trace:LogChosen(step, context)
  if self.enabled <= 0 then return end
  self:Log({
    kind = "chosen",
    section = context.__sectionName,
    block = context.__blockName,
    command = step.command,
    spell = context.lastExecuted and context.lastExecuted.spell,
  })
end

function Trace:Last(n)
  local t = SkillWeaver_Trace.items
  n = math.min(n or 10, #t)
  local out = {}
  for i = #t - n + 1, #t do
    out[#out+1] = t[i]
  end
  return out
end

return Trace
