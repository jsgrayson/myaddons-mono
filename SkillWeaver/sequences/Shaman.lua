local ADDON_NAME, SkillWeaver = ...

-- Shaman Sequences
-- Covers: Enhancement (263)

local SHAMAN_ENHANCEMENT = "SHAMAN_263"

SkillWeaver.Sequences[SHAMAN_ENHANCEMENT] = {
    ["Raid"] = {
        ["Balanced"] = { -- Default
            type = "Priority",
            st = {
                { command = "/cast Feral Spirit", conditions = "true" },
                { command = "/cast Primordial Wave", conditions = "true" },
                { command = "/cast Lightning Bolt", conditions = "buff:Maelstrom Weapon >= 8" },
                { command = "/cast Elemental Blast", conditions = "buff:Maelstrom Weapon >= 5 and charges:Elemental Blast > 0" },
                { command = "/cast Stormstrike", conditions = "true" },
                { command = "/cast Lava Lash", conditions = "true" },
                { command = "/cast Ice Strike", conditions = "true" },
                { command = "/cast Frost Shock", conditions = "buff:Hailstorm" },
            },
            aoe = {
                { command = "/cast Feral Spirit", conditions = "true" },
                { command = "/cast Primordial Wave", conditions = "true" },
                { command = "/cast Chain Lightning", conditions = "buff:Maelstrom Weapon >= 8" },
                { command = "/cast Crash Lightning", conditions = "true" },
                { command = "/cast Stormstrike", conditions = "true" },
                { command = "/cast Lava Lash", conditions = "true" },
            },
            steps = {}
        },
        ["Stormbringer"] = { -- Single Target / Tempest Focus
            type = "Priority",
            st = {
                -- Emergency Healing (Ally then Self)
                { command = "/cast [target=mouseover,help,nodead][help] Healing Surge", conditions = "in_group and ally_health < 20 and buff:Maelstrom Weapon >= 10 and range <= 40" },
                { command = "/cast [target=player] Healing Surge", conditions = "health < 40 and buff:Maelstrom Weapon >= 10" },
                { command = "/cast [target=player] Astral Shift", conditions = "health < 50" },
                
                -- Interrupt & Cleanse
                { command = "/cast Wind Shear", conditions = "should_interrupt and range <= 30" },
                { command = "/cast [target=player] Cleanse Spirit", conditions = "(debuff_type == curse or debuff_type == poison and talent(Cleanse Spirit)) or movement_impaired" },
                
                -- Cooldowns
                { command = "/cast Feral Spirit", conditions = "true" },
                { command = "/cast Ascendance", conditions = "heroism or target_health < 20" },
                { command = "/cast Doom Winds", conditions = "true" },
                { command = "/cast Primordial Wave", conditions = "range <= 40" },
                
                -- Maelstrom Spenders (with range checks)
                { command = "/cast Tempest", conditions = "buff:Maelstrom Weapon >= 10 and range <= 40" }, -- Replaces Lightning Bolt
                { command = "/cast Elemental Blast", conditions = "buff:Maelstrom Weapon >= 5 and charges:Elemental Blast > 0 and range <= 40" },
                { command = "/cast Lightning Bolt", conditions = "buff:Maelstrom Weapon >= 8 and range <= 40" },
                
                -- Melee Generators (range validation)
                { command = "/cast Stormstrike", conditions = "range <= 8" },
                { command = "/cast Lava Lash", conditions = "range <= 8" },
                { command = "/cast Ice Strike", conditions = "range <= 8" },
                { command = "/cast Frost Shock", conditions = "buff:Hailstorm and range <= 40" },
            },
            aoe = {
                { command = "/cast Wind Shear", conditions = "should_interrupt and range <= 30" },
                { command = "/cast Astral Shift", conditions = "health < 50 or enemies_nearby >= 4" },
                { command = "/cast Doom Winds", conditions = "true" },
                { command = "/cast Primordial Wave", conditions = "range <= 40" },
                { command = "/cast Tempest", conditions = "buff:Maelstrom Weapon >= 10 and range <= 40" },
                { command = "/cast Chain Lightning", conditions = "buff:Maelstrom Weapon >= 8 and range <= 40" },
                { command = "/cast Crash Lightning", conditions = "range <= 8" },
                { command = "/cast Stormstrike", conditions = "range <= 8" },
                { command = "/cast Lava Lash", conditions = "range <= 8" },
            },
            steps = {}
        },
        ["Totemic"] = { -- AoE / Surging Totem Focus
            type = "Priority",
            st = {
                { command = "/cast Surging Totem", conditions = "true" }, -- Active Ability
                { command = "/cast Feral Spirit", conditions = "true" },
                { command = "/cast Doom Winds", conditions = "true" },
                { command = "/cast Primordial Wave", conditions = "true" },
                { command = "/cast Elemental Blast", conditions = "buff:Maelstrom Weapon >= 5" },
                { command = "/cast Lightning Bolt", conditions = "buff:Maelstrom Weapon >= 8" },
                { command = "/cast Stormstrike", conditions = "true" },
                { command = "/cast Lava Lash", conditions = "true" }, -- Totemic synergy
                { command = "/cast Sundering", conditions = "true" },
            },
            aoe = {
                { command = "/cast Surging Totem", conditions = "true" },
                { command = "/cast Doom Winds", conditions = "true" },
                { command = "/cast Primordial Wave", conditions = "true" },
                { command = "/cast Crash Lightning", conditions = "true" },
                { command = "/cast Chain Lightning", conditions = "buff:Maelstrom Weapon >= 8" },
                { command = "/cast Lava Lash", conditions = "buff:Lashing Flames" },
                { command = "/cast Sundering", conditions = "true" },
            },
            steps = {}
        }
    },
            { command = "/cast Primordial Wave", conditions = "can_cast:Primordial Wave" },
            { command = "/cast Doom Winds", conditions = "can_cast:Doom Winds" },
            { command = "/cast Ascendance", conditions = "can_cast:Ascendance" },
            { command = "/cast Sundering", conditions = "can_cast:Sundering" },
            { command = "/cast Surging Totem", conditions = "can_cast:Surging Totem" },
            
            -- Core Rotation
            { command = "/cast Tempest", conditions = "can_cast:Tempest" },
            { command = "/cast Elemental Blast", conditions = "can_cast:Elemental Blast" },
            { command = "/cast Stormstrike", conditions = "can_cast:Stormstrike" },
            { command = "/cast Lava Lash", conditions = "can_cast:Lava Lash" },
            { command = "/cast Ice Strike", conditions = "can_cast:Ice Strike" },
            { command = "/cast Crash Lightning", conditions = "can_cast:Crash Lightning" },
            { command = "/cast Lightning Bolt", conditions = "true" },
        },
        aoe = {},
        steps = {}
    }
}
