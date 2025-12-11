local ADDON_NAME, SkillWeaver = ...

SkillWeaver.HealingHelper = {}
local Helper = SkillWeaver.HealingHelper

-- Find the lowest health party/raid member
function Helper:GetLowestHealthAlly()
    local lowestUnit = nil
    local lowestPercent = 100
    
    -- Check raid first
    if IsInRaid() then
        for i = 1, 40 do
            local unit = "raid" .. i
            if UnitExists(unit) and not UnitIsDead(unit) and UnitIsConnected(unit) then
                local health = UnitHealth(unit)
                local maxHealth = UnitHealthMax(unit)
                if maxHealth > 0 then
                    local percent = (health / maxHealth) * 100
                    if percent < lowestPercent and percent < 100 then
                        lowestPercent = percent
                        lowestUnit = unit
                    end
                end
            end
        end
    -- Then party
    elseif IsInGroup() then
        for i = 1, 4 do
            local unit = "party" .. i
            if UnitExists(unit) and not UnitIsDead(unit) and UnitIsConnected(unit) then
                local health = UnitHealth(unit)
                local maxHealth = UnitHealthMax(unit)
                if maxHealth > 0 then
                    local percent = (health / maxHealth) * 100
                    if percent < lowestPercent and percent < 100 then
                        lowestPercent = percent
                        lowestUnit = unit
                    end
                end
            end
        end
    end
    
    -- Check player last
    local playerHealth = UnitHealth("player")
    local playerMaxHealth = UnitHealthMax("player")
    if playerMaxHealth > 0 then
        local playerPercent = (playerHealth / playerMaxHealth) * 100
        if playerPercent < lowestPercent and playerPercent < 100 then
            lowestPercent = playerPercent
            lowestUnit = "player"
        end
    end
    
    return lowestUnit, lowestPercent
end

-- Count allies below health threshold
function Helper:CountAlliesBelowHealth(threshold)
    local count = 0
    threshold = threshold or 70
    
    if IsInRaid() then
        for i = 1, 40 do
            local unit = "raid" .. i
            if UnitExists(unit) and not UnitIsDead(unit) then
                local health = UnitHealth(unit)
                local maxHealth = UnitHealthMax(unit)
                if maxHealth > 0 then
                    local percent = (health / maxHealth) * 100
                    if percent < threshold then
                        count = count + 1
                    end
                end
            end
        end
    elseif IsInGroup() then
        for i = 1, 4 do
            local unit = "party" .. i
            if UnitExists(unit) and not UnitIsDead(unit) then
                local health = UnitHealth(unit)
                local maxHealth = UnitHealthMax(unit)
                if maxHealth > 0 then
                    local percent = (health / maxHealth) * 100
                    if percent < threshold then
                        count = count + 1
                    end
                end
            end
        end
    end
    
    -- Include player
    local playerHealth = UnitHealth("player")
    local playerMaxHealth = UnitHealthMax("player")
    if playerMaxHealth > 0 then
        local playerPercent = (playerHealth / playerMaxHealth) * 100
        if playerPercent < threshold then
            count = count + 1
        end
    end
    
    return count
end

-- Auto-target for healing
function Helper:SetSmartHealTarget()
    local unit, percent = self:GetLowestHealthAlly()
    if unit and percent < 90 then
        TargetUnit(unit)
        return true
    end
    return false
end
