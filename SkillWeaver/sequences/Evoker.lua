local ADDON_NAME, SkillWeaver = ...

-- Evoker Sequences
-- Covers: Devastation (1467), Augmentation (1473)

local EVOKER_DEVASTATION = "EVOKER_1467"
local EVOKER_AUGMENTATION = "EVOKER_1473"

-----------------------------------------------------------
-- DEVASTATION EVOKER (1467)
-----------------------------------------------------------
SkillWeaver.Sequences[EVOKER_DEVASTATION] = {
    ["Mythic+"] = {
        ["Flameshaper"] = { -- Devastation / Flameshaper Hero Talent
            type = "Priority",
            st = {
                -- Survival & Utility
                { command = "/cast Quell", conditions = "should_interrupt and range <= 25" },
                { command = "/cast Obsidian Scales", conditions = "health < 40" },
                { command = "/cast [target=player] Verdant Embrace", conditions = "health < 50 and range <= 25" },
                { command = "/cast Renewing Blaze", conditions = "health < 35 and talent(Renewing Blaze)" },
                { command = "/cast [target=mouseover,help,nodead][target=player] Dream Breath", conditions = "in_group and ally_health < 20 and talent(Dream Breath) and range <= 25" },
                { command = "/cast [target=player] Emerald Blossom", conditions = "health < 60 and talent(Emerald Blossom)" },
                { command = "/cast [target=player] Cauterizing Flame", conditions = "debuff_type == bleed or debuff_type == poison or debuff_type == curse or debuff_type == disease" },
                { command = "/cast [target=player] Expunge", conditions = "debuff_type == poison or debuff_type == disease" },
                
                -- Pre-Combat
                { command = "/cast Blessing of the Bronze", conditions = "not buff:Blessing of the Bronze and not in_combat" },
                
                -- Empowered Spells (Priority)
                { command = "/cast [empower:3] Fire Breath", conditions = "essence >= 3 and range <= 25" },
                { command = "/cast [empower:3] Eternity Surge", conditions = "essence >= 3 and talent(Eternity Surge) and range <= 25" },
                
                -- Cooldowns
                { command = "/cast Dragonrage", conditions = "cooldown:Dragonrage == 0 and essence >= 3" },
                { command = "/cast Tip the Scales", conditions = "talent(Tip the Scales) and (cooldown:Fire Breath < 1 or cooldown:Eternity Surge < 1)" },
                
                -- Essence Generators
                { command = "/cast Shattering Star", conditions = "talent(Shattering Star) and range <= 40" },
                { command = "/cast Azure Strike", conditions = "essence < 3 and range <= 25" },
                
                -- Essence Spenders
                { command = "/cast Disintegrate", conditions = "essence >= 3 and (buff:Dragonrage or debuff:Shattering Star) and range <= 25" },
                { command = "/cast Pyre", conditions = "essence >= 2 and buff:Essence Burst and range <= 25" },
                
                -- Filler
                { command = "/cast Living Flame", conditions = "range <= 25" },
            },
            aoe = {
                { command = "/cast Quell", conditions = "should_interrupt and range <= 25" },
                { command = "/cast Dragonrage", conditions = "cooldown:Dragonrage == 0" },
                { command = "/cast [empower:3] Fire Breath", conditions = "essence >= 3 and range <= 25" },
                { command = "/cast Deep Breath", conditions = "talent(Deep Breath) and enemies_nearby >= 3 and range <= 50" },
                { command = "/cast Pyre", conditions = "essence >= 2 and range <= 25" },
                { command = "/cast Disintegrate", conditions = "essence >= 3 and enemies_nearby < 3 and range <= 25" },
                { command = "/cast Living Flame", conditions = "range <= 25" },
            },
            steps = {}
        }
    },
            { command = "/cast Tip the Scales", conditions = "can_cast:Tip the Scales" },
            { command = "/cast Deep Breath", conditions = "can_cast:Deep Breath" },
            { command = "/cast Shattering Star", conditions = "can_cast:Shattering Star" },
            
            -- Core Rotation
            { command = "/cast Fire Breath", conditions = "can_cast:Fire Breath" },
            { command = "/cast Eternity Surge", conditions = "can_cast:Eternity Surge" },
            { command = "/cast Disintegrate", conditions = "can_cast:Disintegrate" },
            { command = "/cast Living Flame", conditions = "true" },
        },
        aoe = {},
        steps = {}
    }
}

-----------------------------------------------------------
-- AUGMENTATION EVOKER (1473)
-----------------------------------------------------------
SkillWeaver.Sequences[EVOKER_AUGMENTATION] = {
    ["Mythic+"] = {
        ["Scalecommander"] = { -- Augmentation / Scalecommander Hero Talent
            type = "Priority",
            st = {
                -- Survival & Utility
                { command = "/cast Quell", conditions = "should_interrupt and range <= 25" },
                { command = "/cast Obsidian Scales", conditions = "health < 40" },
                { command = "/cast [target=player] Verdant Embrace", conditions = "health < 50 and range <= 25" },
                { command = "/cast Renewing Blaze", conditions = "health < 35 and talent(Renewing Blaze)" },
                { command = "/cast Renewing Blaze", conditions = "health < 35 and talent(Renewing Blaze)" },
                { command = "/cast [target=player] Cauterizing Flame", conditions = "debuff_type == bleed or debuff_type == poison or debuff_type == curse or debuff_type == disease" },
                { command = "/cast [target=player] Expunge", conditions = "debuff_type == poison or debuff_type == disease" },
                { command = "/cast [target=mouseover,help,nodead] Dream Breath", conditions = "in_group and ally_health < 20 and talent(Dream Breath) and range <= 25" },
                
                -- Pre-Combat Buffs
                { command = "/cast Blessing of the Bronze", conditions = "not buff:Blessing of the Bronze and not in_combat" },
                { command = "/cast [target=focus] Ebon Might", conditions = "in_group and focus_role == dps and not in_combat and range <= 40" },
                
                -- Empowered Spells
                { command = "/cast [empower:3] Fire Breath", conditions = "essence >= 3 and range <= 25" },
                { command = "/cast [empower:3] Upheaval", conditions = "essence >= 3 and talent(Upheaval) and range <= 25" },
                
                -- Support Buffs (Primary Role)
                { command = "/cast [target=focus] Ebon Might", conditions = "in_group and cooldown:Ebon Might == 0 and range <= 40" },
                { command = "/cast [target=focus] Prescience", conditions = "in_group and talent(Prescience) and range <= 40" },
                { command = "/cast Breath of Eons", conditions = "talent(Breath of Eons) and in_group and range <= 25" },
                
                -- Essence Generators
                { command = "/cast Azure Strike", conditions = "essence < 3 and range <= 25" },
                
                -- Essence Spenders
                { command = "/cast Eruption", conditions = "essence >= 3 and range <= 25" },
                
                -- Filler
                { command = "/cast Living Flame", conditions = "range <= 25" },
            },
            aoe = {
                { command = "/cast Quell", conditions = "should_interrupt and range <= 25" },
                { command = "/cast [target=focus] Ebon Might", conditions = "in_group and cooldown:Ebon Might == 0 and range <= 40" },
                { command = "/cast [empower:3] Fire Breath", conditions = "essence >= 3 and range <= 25" },
                { command = "/cast [empower:3] Upheaval", conditions = "essence >= 3 and talent(Upheaval) and range <= 25" },
                { command = "/cast Eruption", conditions = "essence >= 3 and range <= 25" },
                { command = "/cast Azure Strike", conditions = "range <= 25" },
            },
            steps = {}
        }
    },
            { command = "/cast Prescience", conditions = "can_cast:Prescience" },
            { command = "/cast Breath of Eons", conditions = "can_cast:Breath of Eons" },
            { command = "/cast Fire Breath", conditions = "can_cast:Fire Breath" },
            { command = "/cast Upheaval", conditions = "can_cast:Upheaval" },
            { command = "/cast Eruption", conditions = "can_cast:Eruption" },
            { command = "/cast Living Flame", conditions = "true" },
        },
        aoe = {},
        steps = {}
    }
}
