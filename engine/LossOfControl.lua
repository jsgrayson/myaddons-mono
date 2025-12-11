local ADDON_NAME, SkillWeaver = ...
SkillWeaver.LossOfControl = {}
local LoC = SkillWeaver.LossOfControl

-- Class Abilities that break CC
-- Format: [Class] = { { id = SpellID, types = { "FEAR", "STUN", ... } }, ... }
local CLASS_CC_BREAKS = {
    ["WARRIOR"] = {
        { id = 18499, types = { "FEAR", "CHARM", "SLEEP" } }, -- Berserker Rage
    },
    ["DEATHKNIGHT"] = {
        { id = 48792, types = { "STUN" } }, -- Icebound Fortitude
        { id = 49039, types = { "FEAR", "CHARM", "SLEEP" } }, -- Lichborne
    },
    ["MAGE"] = {
        { id = 45438, types = { "STUN", "FEAR", "ROOT", "SILENCE" } }, -- Ice Block
    },
    ["PALADIN"] = {
        { id = 642, types = { "STUN", "FEAR", "ROOT", "SILENCE" } }, -- Divine Shield
    },
    ["HUNTER"] = {
        { id = 53271, types = { "ROOT", "SNARE" } }, -- Master's Call
    },
    ["DRUID"] = {
        -- Barkskin usable while stunned/feared/sleeping? Usually yes.
        -- { id = 22812, types = { "STUN", "FEAR", "SLEEP" } }, -- Barkskin (Mitigation, not break, but usable)
        -- Tiger's Dash breaks roots?
    },
    -- Add more as needed
}

-- PvP Trinket Spell ID (Gladiator's Medallion)
local PVP_TRINKET_SPELL_ID = 336126

function LoC.ShouldBreakCC()
    -- 1. Check if we are actually CC'd
    local eventIndex = C_LossOfControl.GetActiveLossOfControlDataCount()
    if eventIndex == 0 then return false, nil, nil end

    local locData = C_LossOfControl.GetActiveLossOfControlData(1)
    local type = locData.locType -- STUN, FEAR, CHARM, SLEEP, ROOT, SILENCE, PACIFY, DISARM
    local duration = locData.duration or 0
    
    -- Only break significant CC (> 1.5s) or specific types
    -- Ignore short micro-stuns unless critical?
    if duration < 1.5 and type ~= "STUN" then return false, nil, nil end

    -- 2. Check Trinket (Priority 1)
    for slot = 13, 14 do
        local itemID = GetInventoryItemID("player", slot)
        if itemID then
            local _, spellID = C_Item.GetItemSpell(itemID)
            if spellID == PVP_TRINKET_SPELL_ID then
                local start, dur, enable = GetInventoryItemCooldown("player", slot)
                if enable == 1 and start == 0 then
                    return true, slot, "item" -- Return slot ID for item use
                end
            end
        end
    end

    -- 3. Check Racial (Priority 2)
    if SkillWeaver.Racials and SkillWeaver.Racials.GetPlayerRacial then
        local racial = SkillWeaver.Racials.GetPlayerRacial()
        if racial then
            local matches = false
            if racial.type == "CCBreak" and type == "STUN" then matches = true end
            if racial.type == "CCBreak_Fear" and (type == "FEAR" or type == "CHARM" or type == "SLEEP") then matches = true end
            if racial.type == "RootBreak" and type == "ROOT" then matches = true end
            
            if matches then
                local usable, noMana = C_Spell.IsSpellUsable(racial.id)
                local start, duration = C_Spell.GetSpellCooldown(racial.id)
                if usable and not noMana and (start == 0 or duration <= 1.5) then
                    return true, racial.id, "spell"
                end
            end
        end
    end

    -- 4. Check Class Ability (Priority 3)
    local _, classFilename = UnitClass("player")
    local abilities = CLASS_CC_BREAKS[classFilename]
    if abilities then
        for _, ability in ipairs(abilities) do
            -- Check if ability handles this CC type
            local handles = false
            for _, t in ipairs(ability.types) do
                if t == type then handles = true break end
            end
            
            if handles then
                -- Check cooldown/usability
                local usable, noMana = C_Spell.IsSpellUsable(ability.id)
                local start, duration = C_Spell.GetSpellCooldown(ability.id)
                if usable and not noMana and (start == 0 or duration <= 1.5) then
                    return true, ability.id, "spell"
                end
            end
        end
    end

    return false, nil, nil
end
