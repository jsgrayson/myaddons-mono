local ADDON_NAME, SkillWeaver = ...

--[[
    CombatTracker.lua
    
    Tracks combat state for intelligent decision making:
    - Combat duration
    - Damage rate (DPS/HPS)
    - Time-to-die estimates
    - Burst window tracking
]]

SkillWeaver.CombatTracker = {}
local CombatTracker = SkillWeaver.CombatTracker

-- State tracking
CombatTracker.combatStart = 0
CombatTracker.lastUpdate = 0
CombatTracker.damageHistory = {}
CombatTracker.targetHealth = {}

--[[
    Get how long we've been in combat (seconds)
]]
function CombatTracker:GetCombatTime()
    if not UnitAffectingCombat("player") then
        return 0
    end
    
    if self.combatStart == 0 then
        return 0
    end
    
    return GetTime() - self.combatStart
end

--[[
    Estimate time until target dies (seconds)
    Returns 999 if can't estimate
]]
function CombatTracker:GetTimeToDie()
    if not UnitExists("target") or UnitIsDead("target") then
        return 0
    end
    
    local currentHP = UnitHealth("target")
    local maxHP = UnitHealthMax("target")
    local targetGUID = UnitGUID("target")
    
    if not targetGUID then
        return 999
    end
    
    -- Track health changes
    if not self.targetHealth[targetGUID] then
        self.targetHealth[targetGUID] = {
            lastHP = currentHP,
            lastTime = GetTime()
        }
        return 999  -- Need data
    end
    
    local data = self.targetHealth[targetGUID]
    local timeDelta = GetTime() - data.lastTime
    
    if timeDelta < 1 then
        return 999  -- Too soon
    end
    
    local hpDelta = data.lastHP - currentHP
    
    if hpDelta <= 0 then
        -- Target gaining health or not damaged
        data.lastHP = currentHP
        data.lastTime = GetTime()
        return 999
    end
    
    -- Calculate DPS rate
    local dps = hpDelta / timeDelta
    
    if dps > 0 then
        local ttd = currentHP / dps
        
        -- Update tracking
        data.lastHP = currentHP
        data.lastTime = GetTime()
        
        return ttd
    end
    
    return 999
end

--[[
    Estimate time until execute range (20% health)
]]
function CombatTracker:GetTimeToExecute()
    if not UnitExists("target") then
        return 999
    end
    
    local currentHP = UnitHealth("target")
    local maxHP = UnitHealthMax("target")
    local executeHP = maxHP * 0.20
    
    if currentHP <= executeHP then
        return 0  -- Already in execute
    end
    
    local ttd = self:GetTimeToDie()
    if ttd == 999 then
        return 999
    end
    
    local currentPct = (currentHP / maxHP) * 100
    local pctToExecute = currentPct - 20
    
    -- Rough estimate
    return (ttd * pctToExecute) / currentPct
end

-- Event handling
local frame = CreateFrame("Frame")
frame:RegisterEvent("PLAYER_REGEN_DISABLED")  -- Combat start
frame:RegisterEvent("PLAYER_REGEN_ENABLED")   -- Combat end
frame:RegisterEvent("PLAYER_TARGET_CHANGED")

frame:SetScript("OnEvent", function(self, event)
    if event == "PLAYER_REGEN_DISABLED" then
        CombatTracker.combatStart = GetTime()
    elseif event == "PLAYER_REGEN_ENABLED" then
        CombatTracker.combatStart = 0
        -- Clear target health tracking
        CombatTracker.targetHealth = {}
    elseif event == "PLAYER_TARGET_CHANGED" then
        -- Target changed, start fresh tracking
        local targetGUID = UnitGUID("target")
        if targetGUID and not CombatTracker.targetHealth[targetGUID] then
            CombatTracker.targetHealth[targetGUID] = {
                lastHP = UnitHealth("target"),
                lastTime = GetTime()
            }
        end
    end
end)

-- Update tracker every 0.5 seconds
C_Timer.NewTicker(0.5, function()
    if UnitAffectingCombat("player") and UnitExists("target") then
        -- Update time-to-die estimate
        CombatTracker:GetTimeToDie()
    end
end)
