local ADDON_NAME, SkillWeaver = ...

-- Rogue Sequences
-- Covers: Subtlety (261)

local ROGUE_ASSASSINATION = "ROGUE_259"
local ROGUE_SUBTLETY = "ROGUE_261"

SkillWeaver.Sequences[ROGUE_ASSASSINATION] = {
    ["Raid"] = {
        ["Balanced"] = { -- Default
            type = "Priority",
            st = {
                { command = "/cast Slice and Dice", conditions = "buff:Slice and Dice < 5" },
                { command = "/cast Kingsbane", conditions = "true" },
                { command = "/cast Deathmark", conditions = "true" },
                { command = "/cast Garrote", conditions = "buff:Garrote < 5" },
                { command = "/cast Rupture", conditions = "combo_points >= 5 and buff:Rupture < 5" },
                { command = "/cast Envenom", conditions = "combo_points >= 4" },
                { command = "/cast Ambush", conditions = "stealthed" },
                { command = "/cast Mutilate", conditions = "true" },
            },
            aoe = {
                { command = "/cast Fan of Knives", conditions = "combo_points < 5" },
                { command = "/cast Crimson Tempest", conditions = "combo_points >= 5" },
                { command = "/cast Envenom", conditions = "combo_points >= 5" },
            },
            steps = {}
        },
        ["Fatebound"] = { -- Single Target / Execute Focus
            type = "Priority",
            st = {
                -- Priority 1: SURVIVAL & UTILITY
                { command = "/cast Kick", conditions = "should_interrupt and range <= 8" }, -- Interrupt
                { command = "/cast [target=focus] Tricks of the Trade", conditions = "in_group and focus_role == tank and pull_timer < 2" }, -- Threat redirect on pull
                { command = "/cast Feint", conditions = "in_group and threat > 75 and in_combat" }, -- Threat reduction
                { command = "/cast Cloak of Shadows", conditions = "debuff_type == magic or dangerous_debuff or health < 30" }, -- Magic immunity + cleanse
                { command = "/cast Evasion", conditions = "health < 35 or physical_damage_incoming" }, -- Physical DR
                { command = "/cast Crimson Vial", conditions = "health < 35 and energy >= 20" }, -- Emergency heal
                
                -- Cooldowns (Coordinate with Garrote/Kingsbane for max damage)
                { command = "/cast Deathmark", conditions = "dot:Rupture and dot:Garrote and energy >= 20" }, -- With bleeds up
                { command = "/cast Kingsbane", conditions = "dot:Rupture and dot:Garrote" },
                { command = "/cast Thistle Tea", conditions = "energy < 30 and combo_points >= 4" }, -- Emergency energy
                
                -- Maintain Buffs/DoTs
                { command = "/cast Slice and Dice", conditions = "buff:Slice and Dice < 6" }, -- Maintain SND
                { command = "/cast Garrote", conditions = "dot:Garrote < 5 and range <= 8" }, -- Keep Garrote rolling
                { command = "/cast Rupture", conditions = "combo_points >= 4 and dot:Rupture < 5 and range <= 8" }, -- Refresh before drop
                
                -- Fatebound Execution (<35% HP)
                { command = "/cast Envenom", conditions = "combo_points >= 5 and target_health < 35 and range <= 8" }, -- Max CP during execute
                { command = "/cast Envenom", conditions = "combo_points >= 6 and range <= 8" }, -- Avoid cap
                { command = "/cast Envenom", conditions = "combo_points >= 4 and buff:Envenom < 2 and range <= 8" }, -- Maintain Envenom buff
                
                -- Combo Point Generation
                { command = "/cast Ambush", conditions = "(stealthed or buff:Blindside) and range <= 8" }, -- Blindside proc
                { command = "/cast Mutilate", conditions = "combo_points < 5 and energy >= 50 and range <= 8" }, -- Don't starve energy
                { command = "/cast Mutilate", conditions = "target_health > 35 and range <= 8" }, -- Standard generator
                
                -- Fatebound Execute Logic
                { command = "/cast Ambush", conditions = "target_health < 35 and energy >= 50 and range <= 8" }, -- Fatebound execute scaling
                { command = "/cast Mutilate", conditions = "energy >= 60 and range <= 8" }, -- Fallback
            },
            aoe = {
                { command = "/cast Kick", conditions = "should_interrupt and range <= 8" },
                { command = "/cast Feint", conditions = "in_group and enemies_nearby >= 4" }, -- DR in AoE
                { command = "/cast Deathmark", conditions = "true" },
                { command = "/cast Garrote", conditions = "dot:Garrote < 5 and range <= 8" },
                { command = "/cast Rupture", conditions = "combo_points >= 5 and dot:Rupture < 5 and range <= 8" },
                { command = "/cast Crimson Tempest", conditions = "combo_points >= 5 and range <= 8" },
                { command = "/cast Envenom", conditions = "combo_points >= 5 and enemies < 3 and range <= 8" },
                { command = "/cast Fan of Knives", conditions = "combo_points < 5 and range <= 8" },
            },
            steps = {}
        },
        ["Deathstalker"] = { -- AoE / Bleed Spread Focus
            type = "Priority",
            st = {
                { command = "/cast Deathmark", conditions = "true" },
                { command = "/cast Indiscriminate Carnage", conditions = "true" }, -- Spread bleeds
                { command = "/cast Garrote", conditions = "buff:Garrote < 5" },
                { command = "/cast Rupture", conditions = "combo_points >= 5 and buff:Rupture < 5" },
                { command = "/cast Envenom", conditions = "combo_points >= 4" },
                { command = "/cast Mutilate", conditions = "true" },
            },
            aoe = {
                { command = "/cast Indiscriminate Carnage", conditions = "true" },
                { command = "/cast Garrote", conditions = "buff:Garrote < 5" },
                { command = "/cast Rupture", conditions = "combo_points >= 5" },
                { command = "/cast Crimson Tempest", conditions = "combo_points >= 5" },
                { command = "/cast Fan of Knives", conditions = "true" },
            },
            steps = {}
        }
    }
}

SkillWeaver.Sequences[ROGUE_SUBTLETY] = {
    ["Raid"] = {
        ["Balanced"] = { -- Default
            type = "Priority",
            st = {
                { command = "/cast Shadow Blades", conditions = "heroism or target_health < 20" },
                { command = "/cast Shadow Dance", conditions = "charges:Shadow Dance > 0 and buff:Shadow Dance == 0" },
                { command = "/cast Symbols of Death", conditions = "buff:Shadow Dance" },
                { command = "/cast Secret Technique", conditions = "combo_points >= 5" },
                { command = "/cast Eviscerate", conditions = "combo_points >= 5" },
                { command = "/cast Shadowstrike", conditions = "stealthed or buff:Shadow Dance" },
                { command = "/cast Backstab", conditions = "true" },
                { command = "/cast Slice and Dice", conditions = "buff:Slice and Dice < 5" },
            },
            aoe = {
                { command = "/cast Shuriken Storm", conditions = "enemies >= 3" },
                { command = "/cast Black Powder", conditions = "combo_points >= 5" },
                { command = "/cast Secret Technique", conditions = "combo_points >= 5" },
                { command = "/cast Shadow Dance", conditions = "true" },
            },
            steps = {}
        },
        ["Trickster"] = { -- Single Target / Unseen Blade Focus
            type = "Priority",
            st = {
                -- Priority 1: SURVIVAL & UTILITY
                { command = "/cast Kick", conditions = "should_interrupt and range <= 8" },
                { command = "/cast [target=focus] Tricks of the Trade", conditions = "in_group and focus_role == tank and pull_timer < 2" },
                { command = "/cast Feint", conditions = "in_group and threat > 75 and in_combat" },
                { command = "/cast Cloak of Shadows", conditions = "debuff_type == magic or dangerous_debuff or health < 30" },
                { command = "/cast Evasion", conditions = "health < 35 or physical_damage_incoming" },
                { command = "/cast Crimson Vial", conditions = "health < 35 and energy >= 20" },
                
                -- Cooldowns (Coordinate Shadow Dance with Symbols)
                { command = "/cast Shadow Blades", conditions = "combo_points <= 2" }, -- Don't waste on high CP
                { command = "/cast Flagellation", conditions = "combo_points >= 5" }, -- With finisher ready
                { command = "/cast Shadow Dance", conditions = "charges:Shadow Dance > 1 or buff:Shadow Blades or target_health < 20" }, -- Save 1 charge normally
                { command = "/cast Symbols of Death", conditions = "buff:Shadow Dance or cooldown:Shadow Dance < 2" }, -- Coordinate with Dance
                
                -- Finisher Priority (during Shadow Dance)
                { command = "/cast Secret Technique", conditions = "(combo_points >= 6 or combo_points >= 5 and buff:Shadow Dance) and range <= 8" }, -- Max CP or during Dance
                { command = "/cast Eviscerate", conditions = "combo_points >= 6 and range <= 8" }, -- Avoid cap
                { command = "/cast Eviscerate", conditions = "combo_points >= 5 and buff:Slice and Dice > 6 and range <= 8" }, -- With SND up
                
                -- Maintain Slice and Dice
                { command = "/cast Slice and Dice", conditions = "buff:Slice and Dice < 6 and combo_points >= 4" },
                
                -- Combo Point Generation
                { command = "/cast Thistle Tea", conditions = "energy < 40 and cooldown:Shadow Dance < 5" }, -- Prepare for Dance
                { command = "/cast Shadowstrike", conditions = "(stealthed or buff:Shadow Dance) and range <= 8" }, -- Triggers Unseen Blade
                { command = "/cast Cold Blood", conditions = "combo_points >= 4 and energy >= 40" }, -- Trickster synergy before finisher
                { command = "/cast Backstab", conditions = "energy >= 35 and range <= 8" }, -- Don't starve energy
                { command = "/cast Backstab", conditions = "combo_points < 5 and range <= 8" },
            },
            aoe = {
                { command = "/cast Kick", conditions = "should_interrupt and range <= 8" },
                { command = "/cast Feint", conditions = "in_group and enemies_nearby >= 4" },
                { command = "/cast Shadow Dance", conditions = "charges:Shadow Dance > 0" },
                { command = "/cast Symbols of Death", conditions = "buff:Shadow Dance" },
                { command = "/cast Shuriken Storm", conditions = "(buff:Shadow Dance or enemies >= 4) and range <= 8" },
                { command = "/cast Black Powder", conditions = "combo_points >= 5 and range <= 8" },
                { command = "/cast Secret Technique", conditions = "combo_points >= 5 and range <= 8" },
                { command = "/cast Thistle Tea", conditions = "energy < 50" },
            },
            steps = {}
        },
        ["Deathstalker"] = { -- Burst / Mark Focus
            type = "Priority",
            st = {
                { command = "/cast Shadow Blades", conditions = "true" },
                { command = "/cast Flagellation", conditions = "true" },
                { command = "/cast Shadowstrike", conditions = "stealthed" }, -- Applies Mark
                { command = "/cast Shadow Dance", conditions = "true" },
                { command = "/cast Symbols of Death", conditions = "true" },
                { command = "/cast Thistle Tea", conditions = "energy < 50" },
                { command = "/cast Eviscerate", conditions = "combo_points >= 5 and buff:Darkest Night" }, -- Finisher buff
                { command = "/cast Secret Technique", conditions = "combo_points >= 5" },
                { command = "/cast Eviscerate", conditions = "combo_points >= 5" },
                { command = "/cast Backstab", conditions = "true" },
            },
            aoe = {
                { command = "/cast Shuriken Storm", conditions = "true" },
                { command = "/cast Black Powder", conditions = "combo_points >= 5" },
                { command = "/cast Secret Technique", conditions = "true" },
                { command = "/cast Thistle Tea", conditions = "energy < 50" },
            },
            steps = {}
        }
    },
            { command = "/cast Shadow Dance", conditions = "can_cast:Shadow Dance" },
            { command = "/cast Symbols of Death", conditions = "can_cast:Symbols of Death" },
            { command = "/cast Secret Technique", conditions = "can_cast:Secret Technique" },
            { command = "/cast Cold Blood", conditions = "can_cast:Cold Blood" },
            { command = "/cast Flagellation", conditions = "can_cast:Flagellation" },
            { command = "/cast Goremaw's Bite", conditions = "can_cast:Goremaw's Bite" },
            { command = "/cast Shuriken Tornado", conditions = "can_cast:Shuriken Tornado" },
            
            -- Core Rotation
            { command = "/cast Eviscerate", conditions = "can_cast:Eviscerate" },
            { command = "/cast Shadowstrike", conditions = "can_cast:Shadowstrike" },
            { command = "/cast Backstab", conditions = "true" },
        },
        aoe = {},
        steps = {}
    }
}
