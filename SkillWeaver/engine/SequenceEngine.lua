--========================================================--
-- SkillWeaver - Deterministic Sequence Engine (Updated)
-- Midnight-Safe Mode + Restricted API Support
--========================================================--

local ADDON_NAME, SkillWeaver = ...
local Engine = {}
SkillWeaver.Engine.Sequence = Engine

-- Cache flags for performance
local SAFE      = function() return SkillWeaver.SafeMode end
local RESTRICT  = function() return SkillWeaver.Restricted end
local FULL      = function() return SkillWeaver.FullEngine end

-- Runtime state for sequences
Engine.runtime = {}

------------------------------------------------------------
-- Get runtime state safely
------------------------------------------------------------
local function GetState(key)
    if not Engine.runtime[key] then
        Engine.runtime[key] = {
            index     = 1,
            lastTime  = 0,
            lastCmd   = nil,
            locked    = false,
        }
    end
    return Engine.runtime[key]
end

------------------------------------------------------------
-- Execute Macro Command
------------------------------------------------------------
function Engine:Execute(cmd)
    if not cmd or type(cmd) ~= "string" then return end

    if SAFE() then
        -- Midnight: simple execution only; no multi-action commands allowed
        RunMacroText(cmd)
        return
    end

    -- Full Engine execution
    -- Full Engine execution
    if cmd == "racial" then
        if SkillWeaver.Racials and SkillWeaver.Racials.ShouldUseRacial then
            local should, spellId = SkillWeaver.Racials.ShouldUseRacial()
            if should and spellId then
                local spellName = GetSpellInfo(spellId)
                if spellName then
                    RunMacroText("/cast " .. spellName)
                    return
                end
            end
        end
        return -- Racial requested but not usable/found
    end

    if cmd == "cc_break" then
        if SkillWeaver.LossOfControl and SkillWeaver.LossOfControl.ShouldBreakCC then
            local should, id, type = SkillWeaver.LossOfControl.ShouldBreakCC()
            if should and id then
                if type == "item" then
                    RunMacroText("/use " .. id) -- Use item by slot ID
                    return
                elseif type == "spell" then
                    local spellName = GetSpellInfo(id)
                    if spellName then
                        RunMacroText("/cast " .. spellName)
                        return
                    end
                end
            end
        end
        return -- CC Break requested but not needed/usable
    end
    
    if cmd == "battle_res" then
        if SkillWeaver.BattleRes and SkillWeaver.BattleRes.GetBestResTarget then
            local unit, role, name = SkillWeaver.BattleRes:GetBestResTarget()
            if unit then
                local spellName = SkillWeaver.BattleRes:GetSpellName()
                if spellName then
                    RunMacroText("/cast [@" .. unit .. "] " .. spellName)
                    return
                end
            end
        end
        return
    end

    RunMacroText(cmd)
end

------------------------------------------------------------
-- Conditions (Safe Mode overrides)
------------------------------------------------------------
function Engine:PassesConditions(conditions)
    if not conditions or conditions == "" then
        return true
    end

    -- SAFE MODE: Never block rotation unless explicitly false-like
    if SAFE() then
        if conditions == "never" or conditions == "false" then
            return false
        end
        return true
    end

    -- Delegate to Parser
    return SkillWeaver.Engine.ConditionParser.Evaluate(conditions)
end

------------------------------------------------------------
-- Step Rotation Logic
------------------------------------------------------------
function Engine:NextStep(sequence, state)
    local total = #sequence.steps
    if total == 0 then return 1 end
    
    local nextIndex = state.index + 1
    if nextIndex > total then nextIndex = 1 end
    return nextIndex
end

------------------------------------------------------------
-- Core Execution Function
------------------------------------------------------------
function Engine:Run(classSpec, mode, variant)
    local classDB = SkillWeaver.Sequences[classSpec]
    if not classDB then
        print("SkillWeaver: No sequences for", classSpec)
        return
    end

    local modeSet = classDB[mode]
    if not modeSet then
        print("SkillWeaver: No mode:", mode)
        return
    end

    local seq = modeSet[variant] or modeSet["Balanced"]
    if not seq then
        print("SkillWeaver: No variant:", variant)
        return
    end

    local state = GetState(classSpec .. "_" .. mode .. "_" .. (variant or "Balanced"))
    
    -- Determine Execution Strategy
    -- If SAFE() is on, we FORCE Sequential behavior because Priority logic 
    -- relies on accurate condition evaluation, which SAFE() disables.
    local isPriority = (seq.type == "Priority") and not SAFE()

    if isPriority then
        -- PRIORITY MODE: Scan from top to bottom
        for i = 1, #seq.steps do
            local step = seq.steps[i]
            if self:PassesConditions(step.conditions) then
                self:Execute(step.command)
                state.lastCmd = step.command
                state.lastTime = GetTime()
                state.index = i -- Track where we fired
                return -- Exit after first successful action
            end
        end
    else
        -- SEQUENTIAL MODE (Default or Safe Mode Failover)
        local step = seq.steps[state.index]
        if not step then
            state.index = 1
            step = seq.steps[1]
        end

        -- In Safe Mode, conditions are mostly ignored (return true), 
        -- so this just cycles through steps.
        if self:PassesConditions(step.conditions) then
            self:Execute(step.command)
            state.lastCmd = step.command
            state.lastTime = GetTime()
        end

        -- Always advance in sequential mode
        state.index = self:NextStep(seq, state)
    end
end

------------------------------------------------------------
-- Evaluate Next Spell (For Visual Cue / AI Camera)
------------------------------------------------------------
function Engine:EvaluateNext(sequence)
    if not sequence then return nil end
    
    -- We only support Priority lists for Visual Cues (Standard Rotation)
    -- Sequential lists (Spam) are handled by the spammer itself, but we can still show the next step.
    
    local isPriority = (sequence.type == "Priority")
    
    if isPriority then
        for i, step in ipairs(sequence.st or sequence.steps) do
            if self:PassesConditions(step.conditions) then
                -- Return the icon/command
                return step.command
            end
        end
    else
        -- Sequential: Just show the next step
        local state = GetState("VISUAL_PREVIEW") -- Use a dummy state
        local step = sequence.steps[state.index] or sequence.steps[1]
        return step.command
    end
    
    return nil
end

------------------------------------------------------------
-- Public API Trigger
------------------------------------------------------------
function SkillWeaver:Click(classSpec, mode, variant)
    Engine:Run(classSpec, mode, variant)
end

return Engine
