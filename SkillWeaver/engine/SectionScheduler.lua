local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local SectionScheduler = {}
SkillWeaver.SectionScheduler = SectionScheduler
local Trace = addonTable.DecisionTrace -- Will be populated after files load


-- Default execution order (never changes)
SectionScheduler.order = { "interrupts", "defensives", "cooldowns", "core", "fillers" }

-- Per-section default exec type if not specified in the sequence meta
SectionScheduler.defaultExec = {
  interrupts = "Priority",
  defensives = "Priority",
  cooldowns  = "Priority",
  core       = "Sequential", -- this is the big win: deterministic core
  fillers    = "Priority",
}

-- Simple throttle to prevent same spell from firing repeatedly in one short window
SectionScheduler.throttle = {
  -- spellName -> lastTime
  lastCastAt = {},
  minInterval = 0.15, -- seconds
}

local function now()
  return GetTime and GetTime() or 0
end

local function throttled(spell)
  if not spell then return false end
  local t = now()
  local last = SectionScheduler.throttle.lastCastAt[spell]
  if last and (t - last) < SectionScheduler.throttle.minInterval then
    return true
  end
  SectionScheduler.throttle.lastCastAt[spell] = t
  return false
end

-- Optional guard: don't try to cast if you're already in GCD / casting
local function isLockedByGCD()
  -- Keep this lightweight and adapt to your existing lock logic if you already have it.
  -- Using IsCurrentSpell can be noisy; prefer your own engine state if available.
  if UnitCastingInfo and UnitCastingInfo("player") then return true end
  if UnitChannelInfo and UnitChannelInfo("player") then return true end
  return false
end

-- Extract spell name from "/cast ..."
local function extractCastName(command)
  if type(command) ~= "string" then return nil end
  local body = command:gsub("^/cast%s+", "")
  body = body:gsub("^%b[]%s*", "")
  body = body:gsub("^%b[]%s*", "")
  body = body:gsub("%s*$", "")
  if body == "" then return nil end
  return body
end

local function sortedByChargeUrgency(steps, context)
  -- Stable sort: if scores tie, preserve original order
  local indexed = {}
  for i, step in ipairs(steps) do
    local spell = extractCastName(step and step.command)
    local score = nil
    if spell and SkillWeaver.ChargeBudget then
      score = SkillWeaver.ChargeBudget:Score(spell, context)
    end
    
    -- Resource Spender Boost (if dumping)
    if spell and SkillWeaver.ResourcePolicy then
        if SkillWeaver.ResourcePolicy:ShouldPreferSpender(spell, context) then
            score = (score or 0) + 5.0 -- Significant boost to beat normal prio
        end
    end

    -- Proc Consumer Boost
    if spell and SkillWeaver.ProcPolicy then
       score = (score or 0) + SkillWeaver.ProcPolicy:ScoreBonus(spell, context)
    end
    
    indexed[#indexed+1] = { i=i, step=step, score=score or -1e9 }
  end

  table.sort(indexed, function(a, b)
    if a.score == b.score then
      return a.i < b.i
    end
    -- Higher score = higher priority
    return a.score > b.score
  end)

  local out = {}
  for _, it in ipairs(indexed) do out[#out+1] = it.step end
  return out
end

-- Wrap runner TryStep so we can apply global guardrails
function SectionScheduler:TryStepWithGuards(Runner, step, context)
  -- Temporarily disabled isLockedByGCD for MVP responsiveness, 
  -- but can re-enable if spamming is an issue.
  -- if isLockedByGCD() then return false end

  local spell = extractCastName(step and step.command)
  if throttled(spell) then return false end

  -- NEW: cooldown gating only when we're executing the cooldowns section
  -- (Requires CooldownPolicy to be loaded on SkillWeaver)
  if context.__sectionName == "cooldowns" then
      if SkillWeaver.CooldownPolicy then
        if not SkillWeaver.CooldownPolicy:AllowCooldown(spell, context, context.cooldownRules) then
          if Trace then Trace:LogBlocked(step, {code="CD_POLICY", detail="policy gate"}, context) end
          return false
        end
      end
      -- NEW: sync hold logic
      if SkillWeaver.CooldownSync and SkillWeaver.CooldownSync:ShouldHold(spell, context) then
        if Trace then Trace:LogBlocked(step, {code="CD_SYNC", detail="holding for sync"}, context) end
        return false
      end
  end

  -- NEW: Resource pooling gate (typically applies in core; you may also apply in cooldowns)
  if (context.__sectionName == "core" or context.__sectionName == "cooldowns") and SkillWeaver.ResourcePolicy then
     if SkillWeaver.ResourcePolicy:ShouldHoldSpender(spell, context) then
        if Trace then Trace:LogBlocked(step, {code="POOLING", detail="pooling resource"}, context) end
        return false
     end
  end

  -- NEW: Proc waste gate
  if context.__sectionName == "core" and SkillWeaver.ProcPolicy then
    if SkillWeaver.ProcPolicy:ShouldAvoidSpell(spell, context) then
      if Trace then Trace:LogBlocked(step, {code="PROC_AVOID", detail="saving proc"}, context) end
      return false
    end
  end

  local result = Runner:TryStep(step, context)
  if result and Trace then
      Trace:LogChosen(step, context)
  end
  return result
end

-- Runs one section (interrupts/defensives/...)
function SectionScheduler:RunSection(Runner, sectionSteps, execType, blockName, context)
  if type(sectionSteps) ~= "table" then return false end

  if context.__sectionName == "interrupts" and SkillWeaver.InterruptAuthority then
      local d = SkillWeaver.InterruptAuthority:Decide(context)
      if d then
          -- Resolve the Specific Tool using CC Authority if available (for escalation/DR logic)
          local toolDecision = d
          if SkillWeaver.CCAuthority then
             local cc = SkillWeaver.CCAuthority:Choose({
                 unit = d.unit,
                 cast = d.cast,
                 interruptKit = context.interruptKit, -- Should be passed from context if set, else defaults
                 petExists = context.petExists,
                 isPvP = context.isPvP,
                 dr = context.dr,
             })
             if cc then
                 toolDecision = cc
             else
                 -- Authority said "Interrupt!", but CCAuthority found no valid tool (maybe due to DR or wait-for-kick)?
                 -- If CCAuthority returns nil, it means "Don't cast anything right now" (e.g. wait for kick).
                 toolDecision = nil
             end
          end
          
          if toolDecision then
              -- Auto-execute the decision
              -- Use [@unit] syntax if possible, or target fallback
              -- NOTE: Protected casting limitations may apply. For standard macro secure env, /cast [@unit] often works if unit is a valid token (target/focus/nameplateN).
              local cmd = ("/cast [@%s] %s"):format(toolDecision.unit, toolDecision.action)
              SkillWeaver:ExecuteCommand(cmd)
              context.lastInterrupt = toolDecision
              return true
          end
      end
  end

  if #sectionSteps == 0 then return false end
  
  -- Runner methods expect to call TryStep; we’ll inline so we can guard.
  if execType == "Sequential" then
    -- Deterministic pointer per section+block
    local key = (context.__ptrKeyPrefix or "core") .. ":" .. (context.__sectionName or "core") .. ":" .. blockName
    Runner.state.pointers[key] = Runner.state.pointers[key] or 1

    local ptr = Runner.state.pointers[key]
    if ptr < 1 or ptr > #sectionSteps then ptr = 1 end
    local start = ptr

    repeat
      if self:TryStepWithGuards(Runner, sectionSteps[ptr], context) then
        ptr = ptr + 1
        if ptr > #sectionSteps then ptr = 1 end
        Runner.state.pointers[key] = ptr
        return true
      end
      ptr = ptr + 1
      if ptr > #sectionSteps then ptr = 1 end
    until ptr == start

    Runner.state.pointers[key] = start
    return false
  else
    -- Priority
    
    -- Optimize order based on ChargeBudget (if enabled)
    if context.__sectionName == "cooldowns" or context.__sectionName == "core" then
       sectionSteps = sortedByChargeUrgency(sectionSteps, context)
    end
    
    for i = 1, #sectionSteps do
      if self:TryStepWithGuards(Runner, sectionSteps[i], context) then
        return true
      end
    end
    return false
  end
end

return SectionScheduler
