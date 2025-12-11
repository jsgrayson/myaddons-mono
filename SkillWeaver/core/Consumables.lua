-- SkillWeaver Consumables System
-- Handles all consumable logic with toggle support

local AddonName, SkillWeaver = ...

SkillWeaver.Consumables = {}
local Consumables = SkillWeaver.Consumables

-----------------------------------------------------------
-- Consumable Item IDs (The War Within)
-----------------------------------------------------------

-- Healing Potions
Consumables.HealingPotions = {
    211880, -- Tempered Potion (TWW)
    207021, -- Dreamwalker's Healing Potion (DF S3/S4)
    207039, -- Potion of Withering Dreams (DF alternative)
}

-- Healthstones
Consumables.Healthstones = {
    5512,  -- Healthstone (all versions use same ID)
}

-- Flasks (TWW)
Consumables.Flasks = {
    212283, -- Flask of Alchemical Chaos (primary)
    212284, -- Flask of Tempered Mastery
    212285, -- Flask of Tempered Versatility
    212286, -- Flask of Tempered Swiftness
    212287, -- Flask of Saving Graces
}

-- Food (TWW - primary stat food)
Consumables.Food = {
    222731, -- Feast of the Divine Day (AGI)
    222730, -- Feast of the Midnight Masquerade (INT)
    222729, -- Everything Stew (STR)
    -- Individual foods
    222438, -- Chippy Tea (AGI)
    222437, -- Marinated Tenderloins (STR)
    222436, -- Sweet and Sour Meatballs (INT)
}

-- Augment Runes (TWW)
Consumables.AugmentRunes = {
    224108, -- Crystallized Augment Rune
    224107, -- Algari Augment Rune (cheaper version)
}

-----------------------------------------------------------
-- Check Functions
-----------------------------------------------------------

function Consumables:IsEnabled()
    return SkillWeaver.Settings.consumables.enabled
end

function Consumables:ShouldUseHealthstone()
    -- ALWAYS check healthstones - they're FREE from Warlocks!
    if not SkillWeaver.Settings.alwaysUseHealthstones then return false end
    
    local healthPercent = (UnitHealth("player") / UnitHealthMax("player")) * 100
    return healthPercent <= SkillWeaver.Settings.consumables.healthstoneThreshold
end

function Consumables:ShouldUseHealingPotion()
    if not self:IsEnabled() then return false end
    if not SkillWeaver.Settings.consumables.usePotions then return false end
    
    local healthPercent = (UnitHealth("player") / UnitHealthMax("player")) * 100
    return healthPercent <= SkillWeaver.Settings.consumables.potionHealthThreshold
end

function Consumables:ShouldUseFlask()
    if not self:IsEnabled() then return false end
    if not SkillWeaver.Settings.consumables.useFlasks then return false end
    if UnitAffectingCombat("player") then return false end -- Only pre-combat
    
    -- Check if we have any flask buff
    return not self:HasFlaskBuff()
end

function Consumables:ShouldUseFood()
    if not self:IsEnabled() then return false end
    if not SkillWeaver.Settings.consumables.useFood then return false end
    if UnitAffectingCombat("player") then return false end -- Only pre-combat
    
    -- Check if we have any food buff
    return not self:HasFoodBuff()
end

function Consumables:ShouldUseAugmentRune()
    if not self:IsEnabled() then return false end
    if not SkillWeaver.Settings.consumables.useAugmentRunes then return false end
    if UnitAffectingCombat("player") then return false end -- Only pre-combat
    
    -- Check if we have augment rune buff
    return not self:HasAugmentRuneBuff()
end

-----------------------------------------------------------
-- Buff Detection
-----------------------------------------------------------

function Consumables:HasFlaskBuff()
    for i = 1, 40 do
        local name, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        
        -- Check against known flask spell IDs (approx)
        if spellId and (
            spellId == 370652 or -- Flask of Alchemical Chaos
            spellId == 370653 or -- Flask of Tempered Mastery
            spellId == 370654 or -- Flask of Tempered Versatility
            spellId == 370655 or -- Flask of Tempered Swiftness
            spellId == 370656    -- Flask of Saving Graces
        ) then
            return true
        end
    end
    return false
end

function Consumables:HasFoodBuff()
    for i = 1, 40 do
        local name, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        
        -- Check for "Well Fed" buff (generic food buff)
        if name and string.find(name, "Well Fed") then
            return true
        end
    end
    return false
end

function Consumables:HasAugmentRuneBuff()
    for i = 1, 40 do
        local name, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        
        -- Check for augment rune buff
        if spellId and (spellId == 454500 or spellId == 454499) then -- Crystallized/Algari Augment
            return true
        end
    end
    return false
end

-----------------------------------------------------------
-- Use Functions
-----------------------------------------------------------

function Consumables:UseHealthstone()
    if not self:ShouldUseHealthstone() then return false end
    
    -- Find healthstone in bags
    for bag = 0, 4 do
        for slot = 1, C_Container.GetContainerNumSlots(bag) do
            local itemID = C_Container.GetContainerItemID(bag, slot)
            if itemID == 5512 then -- Healthstone
                C_Container.UseContainerItem(bag, slot)
                return true
            end
        end
    end
    return false
end

function Consumables:UseHealingPotion()
    if not self:ShouldUseHealingPotion() then return false end
    
    -- Try to use any healing potion
    for _, potionID in ipairs(self.HealingPotions) do
        for bag = 0, 4 do
            for slot = 1, C_Container.GetContainerNumSlots(bag) do
                local itemID = C_Container.GetContainerItemID(bag, slot)
                if itemID == potionID then
                    C_Container.UseContainerItem(bag, slot)
                    return true
                end
            end
        end
    end
    return false
end

function Consumables:UseFlask()
    if not self:ShouldUseFlask() then return false end
    
    -- Try to use any flask
    for _, flaskID in ipairs(self.Flasks) do
        for bag = 0, 4 do
            for slot = 1, C_Container.GetContainerNumSlots(bag) do
                local itemID = C_Container.GetContainerItemID(bag, slot)
                if itemID == flaskID then
                    C_Container.UseContainerItem(bag, slot)
                    return true
                end
            end
        end
    end
    return false
end

function Consumables:UseFood()
    if not self:ShouldUseFood() then return false end
    
    -- Try to use any food
    for _, foodID in ipairs(self.Food) do
        for bag = 0, 4 do
            for slot = 1, C_Container.GetContainerNumSlots(bag) do
                local itemID = C_Container.GetContainerItemID(bag, slot)
                if itemID == foodID then
                    C_Container.UseContainerItem(bag, slot)
                    return true
                end
            end
        end
    end
    return false
end

function Consumables:UseAugmentRune()
    if not self:ShouldUseAugmentRune() then return false end
    
    -- Try to use any augment rune
    for _, runeID in ipairs(self.AugmentRunes) do
        for bag = 0, 4 do
            for slot = 1, C_Container.GetContainerNumSlots(bag) do
                local itemID = C_Container.GetContainerItemID(bag, slot)
                if itemID == runeID then
                    C_Container.UseContainerItem(bag, slot)
                    return true
                end
            end
        end
    end
    return false
end

-----------------------------------------------------------
-- Auto-Use Pre-Combat Buffs
-----------------------------------------------------------

function Consumables:ApplyPreCombatBuffs()
    if not self:IsEnabled() then return end
    if UnitAffectingCombat("player") then return end
    
    -- Priority order: Flask > Food > Augment Rune
    if self:ShouldUseFlask() then
        self:UseFlask()
        C_Timer.After(1.5, function() self:ApplyPreCombatBuffs() end) -- Chain next buff
        return
    end
    
    if self:ShouldUseFood() then
        self:UseFood()
        C_Timer.After(1.5, function() self:ApplyPreCombatBuffs() end)
        return
    end
    
    if self:ShouldUseAugmentRune() then
        self:UseAugmentRune()
    end
end

-----------------------------------------------------------
-- Condition Tokens for SkillWeaver Engine
-----------------------------------------------------------

-- These functions are called by the condition parser
function Consumables:EvaluateCondition(token)
    if token == "consumables_enabled" then
        return self:IsEnabled()
    elseif token == "should_use_healthstone" then
        return self:ShouldUseHealthstone()
    elseif token == "should_use_potion" then
        return self:ShouldUseHealingPotion()
    elseif token == "should_use_flask" then
        return self:ShouldUseFlask()
    elseif token == "should_use_food" then
        return self:ShouldUseFood()
    elseif token == "should_use_augment" then
        return self:ShouldUseAugmentRune()
    end
    return false
end
