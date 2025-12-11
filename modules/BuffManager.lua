--========================================================--
-- SkillWeaver - Buff Manager
-- Automates Group Buffs (Intellect, Fortitude, MotW, etc.)
--========================================================--

local ADDON_NAME, SkillWeaver = ...
local BuffManager = {}
SkillWeaver.BuffManager = BuffManager

-- Buff Database
local BUFFS = {
    MAGE = { id = 1459, name = "Arcane Intellect", group = true },
    PRIEST = { id = 21562, name = "Power Word: Fortitude", group = true },
    DRUID = { id = 1126, name = "Mark of the Wild", group = true },
    WARRIOR = { id = 6673, name = "Battle Shout", group = true },
    EVOKER = { id = 364342, name = "Blessing of the Bronze", group = true },
    -- Paladin Auras are passive/toggled, handled differently usually
    -- Demon Hunter (Chaos Brand) / Monk (Mystic Touch) are passive debuffs
}

------------------------------------------------------------
-- Check if we need to buff
------------------------------------------------------------
function BuffManager:GetBuffAction()
    if InCombatLockdown() then return nil end -- Don't buff in combat usually
    
    local _, class = UnitClass("player")
    local buffInfo = BUFFS[class]
    if not buffInfo then return nil end
    
    if not IsSpellKnown(buffInfo.id) then return nil end
    
    -- Check Self
    local selfBuff = UnitBuff("player", buffInfo.name)
    if not selfBuff then
        return { command = "/cast [@player] " .. buffInfo.name, description = "Auto Buff (Self)" }
    end
    
    -- Check Group (if in group)
    if IsInGroup() then
        local prefix = IsInRaid() and "raid" or "party"
        local count = GetNumGroupMembers()
        local missingCount = 0
        
        for i = 1, count do
            local unit = prefix .. i
            if unit == "party0" then unit = "player" end
            
            if UnitExists(unit) and not UnitIsDeadOrGhost(unit) and UnitIsConnected(unit) and IsSpellInRange(buffInfo.name, unit) == 1 then
                if not UnitBuff(unit, buffInfo.name) then
                    missingCount = missingCount + 1
                end
            end
        end
        
        -- If anyone is missing it, cast it (Group buffs cover everyone usually)
        if missingCount > 0 then
             return { command = "/cast " .. buffInfo.name, description = "Auto Buff (Group: " .. missingCount .. " missing)" }
        end
    end
    
    return nil
end

return BuffManager
