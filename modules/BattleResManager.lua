--========================================================--
-- SkillWeaver - Battle Resurrection Manager
-- Smartly manages combat resurrections (Rebirth, Raise Ally, etc.)
--========================================================--

local ADDON_NAME, SkillWeaver = ...
local BattleResManager = {}
SkillWeaver.BattleResManager = BattleResManager

-- BR Spells
local BR_SPELLS = {
    DRUID = 20484,   -- Rebirth
    DEATHKNIGHT = 61999, -- Raise Ally
    WARLOCK = 20707, -- Soulstone
    PALADIN = 391054, -- Intercession (Retribution Talent)
}

-- Toggle State
BattleResManager.Enabled = true

function BattleResManager:Toggle(state)
    if state == nil then
        self.Enabled = not self.Enabled
    else
        self.Enabled = state
    end
    print("SkillWeaver: Auto Battle Res is now " .. (self.Enabled and "|cff00ff00ON|r" or "|cffff0000OFF|r"))
end

-- Priority: Tank > Healer > DPS
local ROLE_PRIORITY = {
    ["TANK"] = 1,
    ["HEALER"] = 2,
    ["DAMAGER"] = 3,
    ["NONE"] = 4
}

------------------------------------------------------------
-- Check if player has a BR ability available
------------------------------------------------------------
function BattleResManager:CanRes()
    local _, class = UnitClass("player")
    local spellID = BR_SPELLS[class]
    
    if not spellID then return false end
    if not IsSpellKnown(spellID) then return false end
    
    -- Check Cooldown / Charges
    local start, duration = GetSpellCooldown(spellID)
    if start > 0 and duration > 1.5 then return false end
    
    -- Check Resource (e.g. Runic Power for DK? No, Raise Ally is usually free or low cost now, but good to verify)
    if class == "DEATHKNIGHT" then
        if UnitPower("player", Enum.PowerType.RunicPower) < 30 then return false end
    end
    
    return true, spellID
end

------------------------------------------------------------
-- Get Best Resurrection Target
------------------------------------------------------------
function BattleResManager:GetBestTarget()
    if not IsInGroup() then return nil end
    
    local bestUnit = nil
    local bestPriority = 100
    
    local prefix = IsInRaid() and "raid" or "party"
    local count = GetNumGroupMembers()
    
    -- Iterate group
    for i = 1, count do
        local unit = prefix .. i
        if unit == "party0" then unit = "player" end -- Handle player in party loop if needed, mostly for raid
        
        if UnitExists(unit) and UnitIsDeadOrGhost(unit) and not UnitIsFeignDeath(unit) then
            -- Check range (40 yds)
            if IsSpellInRange(GetSpellInfo(20484), unit) == 1 or IsSpellInRange(GetSpellInfo(61999), unit) == 1 then -- Check generic range
                 local role = UnitGroupRolesAssigned(unit)
                 local priority = ROLE_PRIORITY[role] or 4
                 
                 if priority < bestPriority then
                     bestPriority = priority
                     bestUnit = unit
                 end
            end
        end
    end
    
    return bestUnit
end

------------------------------------------------------------
-- Get Action for Rotation
------------------------------------------------------------
function BattleResManager:GetResAction()
    if not self.Enabled then return nil end

    local canRes, spellID = self:CanRes()
    if not canRes then return nil end
    
    local target = self:GetBestTarget()
    if target then
        local spellName = GetSpellInfo(spellID)
        return {
            command = "/cast [@" .. target .. "] " .. spellName,
            description = "Auto Battle Res: " .. UnitName(target)
        }
    end
    
    return nil
end

return BattleResManager
