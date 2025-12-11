local ADDON_NAME, SkillWeaver = ...

-- Druid Sequences
-- Covers: Balance (102)

local DRUID_BALANCE = "DRUID_102"

SkillWeaver.Sequences[DRUID_BALANCE] = {
    ["Raid"] = {
        ["Balanced"] = { -- Default
            type = "Priority",
            st = {
                { command = "/cast Moonkin Form", conditions = "form ~= 4" },
                { command = "/cast Starsurge", conditions = "astral_power >= 40" },
                { command = "/cast Starfire", conditions = "buff:Eclipse (Solar)" },
                { command = "/cast Wrath", conditions = "buff:Eclipse (Lunar)" },
                { command = "/cast Moonfire", conditions = "buff:Moonfire < 5" },
                { command = "/cast Sunfire", conditions = "buff:Sunfire < 5" },
            },
            aoe = {
                { command = "/cast Starfall", conditions = "astral_power >= 50" },
                { command = "/cast Starfire", conditions = "true" },
                { command = "/cast Sunfire", conditions = "true" },
                { command = "/cast Moonfire", conditions = "enemies < 5" },
            },
            steps = {}
        },
        ["Elune's Chosen"] = { -- Single Target / Arcane Focus
            type = "Priority",
            st = {
                { command = "/cast Moonkin Form", conditions = "form ~= 4" },
                
                -- Priority 1: SURVIVAL & UTILITY
                { command = "/cast Skull Bash", conditions = "should_interrupt and range <= 8" },
                { command = "/cast Mighty Bash", conditions = "should_interrupt and cooldown:Skull Bash > 0 and talent(Mighty Bash) and range <= 8" },
                { command = "/cast [target=player] Remove Corruption", conditions = "debuff_type == curse or debuff_type == poison" },
                { command = "/cast [target=mouseover,help,nodead][help] Regrowth", conditions = "in_group and ally_health < 15 and range <= 40" },
                { command = "/cast Barkskin", conditions = "health < 40" },
                { command = "/cast [target=player] Regrowth", conditions = "health < 35" },
                { command = "/cast [target=player] Renewal", conditions = "health < 50 and talent(Renewal)" },
                
                -- Cooldowns (Coordinate with Celestial Alignment)
                { command = "/cast Celestial Alignment", conditions = "astral_power >= 50" }, -- Pool before CA
                { command = "/cast Convoke the Spirits", conditions = "buff:Celestial Alignment or target_health < 20" }, -- During CA or execute
                { command = "/cast Warrior of Elune", conditions = "buff:Celestial Alignment or cooldown:Celestial Alignment < 5" }, -- Prepare for/during CA
                { command = "/cast Fury of Elune", conditions = "buff:Celestial Alignment or astral_power < 50" }, -- During CA or when low AP
                
                -- Astral Power Management
                { command = "/cast Starsurge", conditions = "astral_power >= 90 and range <= 40" }, -- Dump before cap
                { command = "/cast Starsurge", conditions = "astral_power >= 50 and buff:Celestial Alignment and range <= 40" }, -- Spam during CA
                { command = "/cast Starsurge", conditions = "(buff:Starweavers Warp or buff:Starweavers Weft) and range <= 40" }, -- Buff proc usage
                
                -- Moon Cycle (High priority during CA)
                { command = "/cast Full Moon", conditions = "charges:Full Moon > 0 and buff:Celestial Alignment and range <= 40" },
                { command = "/cast New Moon", conditions = "charges:New Moon > 0 and astral_power < 90 and range <= 40" }, -- Don't cap AP
                
                -- Generators (Eclipse aware)
                { command = "/cast Starfire", conditions = "(buff:Eclipse (Solar) or buff:Warrior of Elune) and range <= 40" }, -- Elune's Chosen buffs Starfire
                { command = "/cast Wrath", conditions = "buff:Eclipse (Lunar) and range <= 40" },
                { command = "/cast Starfire", conditions = "eclipse == 0 and range <= 40" }, -- No eclipse, default to Starfire
                
                -- DoT Maintenance
                { command = "/cast Sunfire", conditions = "dot:Sunfire < 5 and range <= 40" },
                { command = "/cast Moonfire", conditions = "dot:Moonfire < 5 and range <= 40" },
            },
            aoe = {
                { command = "/cast Skull Bash", conditions = "should_interrupt and range <= 8" },
                { command = "/cast Barkskin", conditions = "health < 50 or enemies_nearby >= 4" },
                { command = "/cast Celestial Alignment", conditions = "astral_power >= 40" },
                { command = "/cast Convoke the Spirits", conditions = "buff:Celestial Alignment" },
                { command = "/cast Fury of Elune", conditions = "true" },
                { command = "/cast Starfall", conditions = "(astral_power >= 90 or buff:Celestial Alignment) and range <= 40" }, -- Dump or during CA
                { command = "/cast Full Moon", conditions = "charges:Full Moon > 0 and range <= 40" },
                { command = "/cast New Moon", conditions = "charges:New Moon > 0 and range <= 40" },
                { command = "/cast Starfire", conditions = "range <= 40" },
                { command = "/cast Sunfire", conditions = "dot:Sunfire < 5 and range <= 40" },
                { command = "/cast Moonfire", conditions = "enemies < 5 and range <= 40" },
            },
            steps = {}
        },
        ["Keeper of the Grove"] = { -- AoE / Treant Focus
            type = "Priority",
            st = {
                { command = "/cast Moonkin Form", conditions = "form ~= 4" },
                { command = "/cast Celestial Alignment", conditions = "heroism or target_health < 20" },
                { command = "/cast Force of Nature", conditions = "true" },
                { command = "/cast Warrior of Elune", conditions = "true" }, -- Trigger buff
                { command = "/cast Starsurge", conditions = "astral_power >= 40" },
                { command = "/cast Wrath", conditions = "true" },
                { command = "/cast Starfire", conditions = "buff:Warrior of Elune" },
                { command = "/cast Moonfire", conditions = "buff:Moonfire < 5" },
                { command = "/cast Sunfire", conditions = "buff:Sunfire < 5" },
            },
            aoe = {
                { command = "/cast Force of Nature", conditions = "true" },
                { command = "/cast Warrior of Elune", conditions = "true" },
                { command = "/cast Starfall", conditions = "astral_power >= 50" },
                { command = "/cast Starfire", conditions = "true" },
                { command = "/cast Sunfire", conditions = "true" },
                { command = "/cast Mushroom", conditions = "true" },
            },
            steps = {}
        }
    },
    ["Midnight"] = {
        type = "Priority",
        st = {
            -- Multi-DoT: Cycle if both Moonfire and Sunfire are up
            { command = "/cycle", conditions = "debuff:Moonfire and debuff:Sunfire" },
            
            -- Cooldowns & Talents
            { command = "/cast Celestial Alignment", conditions = "can_cast:Celestial Alignment" },
            { command = "/cast Incarnation: Chosen of Elune", conditions = "can_cast:Incarnation: Chosen of Elune" }, -- Alt CA
            { command = "/cast Convoke the Spirits", conditions = "can_cast:Convoke the Spirits" },
            { command = "/cast Fury of Elune", conditions = "can_cast:Fury of Elune" },
            { command = "/cast Force of Nature", conditions = "can_cast:Force of Nature" },
            { command = "/cast Warrior of Elune", conditions = "can_cast:Warrior of Elune" },
            { command = "/cast New Moon", conditions = "can_cast:New Moon" },
            { command = "/cast Half Moon", conditions = "can_cast:Half Moon" },
            { command = "/cast Full Moon", conditions = "can_cast:Full Moon" },
            
            -- Spenders
            { command = "/cast Starsurge", conditions = "can_cast:Starsurge" },
            { command = "/cast Starfall", conditions = "can_cast:Starfall" },
            
            -- Generators
            { command = "/cast Starfire", conditions = "can_cast:Starfire" },
            { command = "/cast Wrath", conditions = "true" },
            { command = "/cast Moonfire", conditions = "true" },
            { command = "/cast Sunfire", conditions = "true" },
        },
        aoe = {},
        steps = {}
    }
}
