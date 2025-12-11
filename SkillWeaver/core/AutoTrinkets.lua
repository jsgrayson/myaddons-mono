local ADDON_NAME, SkillWeaver = ...

local AutoTrinkets = {}
SkillWeaver.AutoTrinkets = AutoTrinkets

-- Configuration
AutoTrinkets.Enabled = true

-- Burst Buffs (When these are up, fire trinkets)
-- TODO: Move to a data file or class module
local BURST_BUFFS = {
    ["Metamorphosis"] = true,
    ["Avenging Wrath"] = true,
    ["Combustion"] = true,
    ["Icy Veins"] = true,
    ["Arcane Power"] = true,
    ["Void Form"] = true,
    ["Trueshot"] = true,
    ["Coordinated Assault"] = true,
    ["Bestial Wrath"] = true,
    ["Adrenaline Rush"] = true,
    ["Shadow Blades"] = true,
    ["Vendetta"] = true, -- Deathmark
    ["Deathmark"] = true,
    ["Pillar of Frost"] = true,
    ["Empower Rune Weapon"] = true,
    ["Dark Transformation"] = true,
    ["Summon Gargoyle"] = true,
    ["Avatar"] = true,
    ["Recklessness"] = true,
    ["Colossus Smash"] = true,
    ["Celestial Alignment"] = true,
    ["Incarnation"] = true,
    ["Berserk"] = true,
    ["Bloodlust"] = true,
    ["Heroism"] = true,
    ["Time Warp"] = true,
    ["Power Infusion"] = true,
}

-- Blacklist (Do not auto-use)
local BLACKLIST = {
    [167377] = true, -- Gladiator's Medallion (Example)
    -- Add more PvP trinkets here
}

function AutoTrinkets:ShouldUse()
    if not self.Enabled then return false end
    if not UnitAffectingCombat("player") then return false end
    
    -- 1. Check for Burst Buffs
    local burstActive = false
    for buffName, _ in pairs(BURST_BUFFS) do
        if UnitBuff("player", buffName) then
            burstActive = true
            break
        end
    end
    
    if not burstActive then return false end
    
    -- 2. Check Trinkets
    local t1 = self:CheckSlot(13)
    local t2 = self:CheckSlot(14)
    
    return t1 or t2
end

function AutoTrinkets:CheckSlot(slotID)
    local itemID = GetInventoryItemID("player", slotID)
    if not itemID then return false end
    
    -- Check Blacklist
    if BLACKLIST[itemID] then return false end
    
    -- Check Cooldown
    local start, duration, enable = GetInventoryItemCooldown("player", slotID)
    if enable == 0 then return false end -- Active
    if start > 0 and duration > 1.5 then return false end -- On CD (ignore GCD)
    
    -- Check Usable (Has On-Use effect)
    -- GetItemSpell(itemID) returns spellName if it has one
    local spellName = GetItemSpell(itemID)
    if not spellName then return false end
    
    return true
end

return AutoTrinkets
