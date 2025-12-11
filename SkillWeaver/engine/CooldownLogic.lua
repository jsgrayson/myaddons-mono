--========================================================--
-- SkillWeaver - Cooldown Logic (Midnight-Safe Version)
--========================================================--

local ADDON_NAME, SkillWeaver = ...
local CD = {}
SkillWeaver.Engine.Cooldown = CD

local SAFE      = function() return SkillWeaver.SafeMode end
local RESTRICT  = function() return SkillWeaver.Restricted end
local FULL      = function() return SkillWeaver.FullEngine end

-- WoW API shorthands
local GetSpellCooldown   = GetSpellCooldown
local GetSpellCharges    = GetSpellCharges
local GetTime            = GetTime

------------------------------------------------------------
-- SAFE MODE: Simple, Blizzard-allowed cooldown checking
------------------------------------------------------------

local function SafeRemaining(spell)
    local start, dur = GetSpellCooldown(spell)
    if not start then return 0, 0 end
    local remain = (start + dur) - GetTime()
    if remain < 0 then remain = 0 end
    return remain, dur
end

local function SafeIsReady(spell)
    local r = select(1, SafeRemaining(spell))
    return r == 0
end

------------------------------------------------------------
-- FULL ENGINE: Full cooldown handling
------------------------------------------------------------

local function FullRemaining(spell)
    local start, dur = GetSpellCooldown(spell)
    if not start then return 0, 0 end
    local remain = (start + dur) - GetTime()
    if remain < 0 then remain = 0 end
    return remain, dur
end

local function FullIsReady(spell)
    return FullRemaining(spell) == 0
end

------------------------------------------------------------
-- PUBLIC: Remaining Cooldown
------------------------------------------------------------

function CD:GetRemaining(spell)
    if SAFE() then return SafeRemaining(spell) end
    if RESTRICT() then return SafeRemaining(spell) end
    return FullRemaining(spell)
end

------------------------------------------------------------
-- PUBLIC: Is Spell Ready?
------------------------------------------------------------

function CD:IsReady(spell)
    if SAFE() then return SafeIsReady(spell) end
    if RESTRICT() then return SafeIsReady(spell) end
    return FullIsReady(spell)
end

------------------------------------------------------------
-- Charges (Blizzard still allows these APIs)
------------------------------------------------------------

local function SafeCharges(spell)
    local charges = GetSpellCharges(spell)
    if not charges then return 0, 0 end
    return charges, 0
end

local function FullCharges(spell)
    local charges, max, start, dur = GetSpellCharges(spell)
    return charges or 0, max or 0, start or 0, dur or 0
end

function CD:GetCharges(spell)
    if SAFE() then return SafeCharges(spell) end
    if RESTRICT() then return SafeCharges(spell) end
    return FullCharges(spell)
end

function CD:HasChargeAvailable(spell)
    local charges = self:GetCharges(spell)
    return (charges or 0) > 0
end

------------------------------------------------------------
-- GCD Checking
------------------------------------------------------------

local function SafeGCD()
    local start, dur = GetSpellCooldown(61304)
    if not start then return 0, 0 end
    local remain = (start + dur) - GetTime()
    if remain < 0 then remain = 0 end
    return remain, dur
end

function CD:GetGCD()
    return SafeGCD()  -- Even Full Engine uses the same logic safely
end

function CD:IsGCD()
    local remain = select(1, CD:GetGCD())
    return remain > 0
end

------------------------------------------------------------
-- Burst Phase Detection (DISABLED in Safe/Restricted Mode)
------------------------------------------------------------

function CD:IsBurstPhase()
    if SAFE() or RESTRICT() then
        return false
    end

    -- FULL ENGINE placeholder for future:
    --  - Trinket procs
    --  - Hero talent windows
    --  - Class-specific burst alignment
    return false
end

------------------------------------------------------------
-- Prediction (FULL ENGINE ONLY — disabled for Midnight)
------------------------------------------------------------

function CD:ReadyWithin(spell, window)
    if SAFE() or RESTRICT() then
        -- Midnight forbids prediction logic → only check current
        return self:IsReady(spell)
    end

    -- Future full-engine support:
    local remain = select(1, CD:GetRemaining(spell))
    return remain <= (window or 0)
end

------------------------------------------------------------
-- Bind into Engine
------------------------------------------------------------

function SkillWeaver.Engine:ResolveCooldown(spell)
    local remain = CD:GetRemaining(spell)
    return remain
end

return CD
