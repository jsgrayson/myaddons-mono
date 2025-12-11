local ADDON_NAME, SkillWeaver = ...

-- Monk Sequences
-- Covers: Windwalker (269)

local MONK_WINDWALKER = "MONK_269"

SkillWeaver.Sequences[MONK_WINDWALKER] = {
    ["Raid"] = {
        ["Balanced"] = { -- Default
            type = "Priority",
            st = {
                { command = "/cast Invoke Xuen, the White Tiger", conditions = "heroism or target_health < 20" },
                { command = "/cast Touch of Death", conditions = "target_health < 15" },
                { command = "/cast Whirling Dragon Punch", conditions = "cooldown:Fists of Fury > 0 and cooldown:Rising Sun Kick > 0" },
                { command = "/cast Rising Sun Kick", conditions = "chi >= 2" },
                { command = "/cast Fists of Fury", conditions = "chi >= 3" },
                { command = "/cast Blackout Kick", conditions = "chi >= 1 and buff:Teachings of the Monastery < 3" },
                { command = "/cast Tiger Palm", conditions = "chi < 4 and energy > 50" },
            },
            aoe = {
                { command = "/cast Invoke Xuen, the White Tiger", conditions = "true" },
                { command = "/cast Whirling Dragon Punch", conditions = "true" },
                { command = "/cast Fists of Fury", conditions = "chi >= 3" },
                { command = "/cast Spinning Crane Kick", conditions = "chi >= 2" },
                { command = "/cast Rising Sun Kick", conditions = "buff:Mark of the Crane < 5" }, -- Apply debuff
                { command = "/cast Tiger Palm", conditions = "chi < 4" },
            },
            steps = {}
        },
        ["Shado-Pan"] = { -- Single Target / Flurry Focus
            type = "Priority",
            st = {
                -- Priority 1: SURVIVAL & UTILITY
                { command = "/cast Spear Hand Strike", conditions = "should_interrupt and range <= 8" },
                { command = "/cast Leg Sweep", conditions = "should_interrupt and cooldown:Spear Hand Strike > 0 and range <= 8" },
                { command = "/cast [target=player] Detox", conditions = "debuff_type == poison or debuff_type == disease" },
                { command = "/cast [target=mouseover,help,nodead][help] Vivify", conditions = "in_group and ally_health < 15 and chi >= 1 and range <= 40" },
                { command = "/cast Fortifying Brew", conditions = "health < 40" },
                { command = "/cast [target=player] Vivify", conditions = "health < 35 and chi >= 1" },
                { command = "/cast Touch of Karma", conditions = "health < 60 and range <= 20" },
                
                -- Cooldowns
                { command = "/cast Invoke Xuen, the White Tiger", conditions = "true" },
                { command = "/cast Touch of Death", conditions = "target_health < 15 and range <= 8" },
                { command = "/cast Strike of the Windlord", conditions = "range <= 8" },
                { command = "/cast Whirling Dragon Punch", conditions = "range <= 8" },
                { command = "/cast Rising Sun Kick", conditions = "chi >= 2 and range <= 8" }, -- Triggers Flurry Strikes
                { command = "/cast Fists of Fury", conditions = "chi >= 3 and range <= 8" }, -- Triggers Flurry Strikes
                { command = "/cast Blackout Kick", conditions = "chi >= 1 and range <= 8" },
                { command = "/cast Tiger Palm", conditions = "chi < 4 and range <= 8" },
            },
            aoe = {
                { command = "/cast Spear Hand Strike", conditions = "should_interrupt and range <= 8" },
                { command = "/cast Leg Sweep", conditions = "enemies_nearby >= 3 and range <= 8" },
                { command = "/cast Fortifying Brew", conditions = "health < 50 or enemies_nearby >= 4" },
                { command = "/cast Strike of the Windlord", conditions = "range <= 8" },
                { command = "/cast Fists of Fury", conditions = "chi >= 3 and range <= 8" },
                { command = "/cast Whirling Dragon Punch", conditions = "range <= 8" },
                { command = "/cast Spinning Crane Kick", conditions = "chi >= 2 and range <= 8" },
                { command = "/cast Rising Sun Kick", conditions = "range <= 8" },
            },
            steps = {}
        },
        ["Conduit of the Celestials"] = { -- Burst / Celestial Focus
            type = "Priority",
            st = {
                { command = "/cast Celestial Conduit", conditions = "true" }, -- Active Ability
                { command = "/cast Invoke Xuen, the White Tiger", conditions = "true" },
                { command = "/cast Strike of the Windlord", conditions = "true" },
                { command = "/cast Rising Sun Kick", conditions = "chi >= 2" },
                { command = "/cast Fists of Fury", conditions = "chi >= 3" },
                { command = "/cast Whirling Dragon Punch", conditions = "true" },
                { command = "/cast Tiger Palm", conditions = "chi < 4" }, -- Conduit buffs generators
            },
            aoe = {
                { command = "/cast Celestial Conduit", conditions = "true" },
                { command = "/cast Strike of the Windlord", conditions = "true" },
                { command = "/cast Fists of Fury", conditions = "chi >= 3" },
                { command = "/cast Spinning Crane Kick", conditions = "chi >= 2" },
                { command = "/cast Rising Sun Kick", conditions = "true" },
            },
            steps = {}
        }
    },
    ["Midnight"] = {
        type = "Priority",
        st = {
            -- Cooldowns & Talents
            { command = "/cast Invoke Xuen, the White Tiger", conditions = "can_cast:Invoke Xuen, the White Tiger" },
            { command = "/cast Touch of Death", conditions = "can_cast:Touch of Death" },
            { command = "/cast Storm, Earth, and Fire", conditions = "can_cast:Storm, Earth, and Fire" },
            { command = "/cast Serenity", conditions = "can_cast:Serenity" },
            { command = "/cast Celestial Conduit", conditions = "can_cast:Celestial Conduit" },
            { command = "/cast Whirling Dragon Punch", conditions = "can_cast:Whirling Dragon Punch" },
            { command = "/cast Strike of the Windlord", conditions = "can_cast:Strike of the Windlord" },
            
            -- Core Rotation
            { command = "/cast Rising Sun Kick", conditions = "can_cast:Rising Sun Kick" },
            { command = "/cast Fists of Fury", conditions = "can_cast:Fists of Fury" },
            { command = "/cast Blackout Kick", conditions = "can_cast:Blackout Kick" },
            { command = "/cast Tiger Palm", conditions = "true" },
        },
        aoe = {},
        steps = {}
    }
}
