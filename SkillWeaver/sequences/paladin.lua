local ADDON_NAME, SkillWeaver = ...

-- Paladin Sequences
-- Covers: Holy (65), Protection (66), Retribution (70)

local PALADIN_HOLY = "PALADIN_65"
local PALADIN_PROT = "PALADIN_66"
local PALADIN_RET  = "PALADIN_70"

-- PROTECTION (Tank)
SkillWeaver.Sequences[PALADIN_PROT] = {
    ["Raid"] = {
        ["Balanced"] = {
            type = "Priority",
            st = {
                -- Defensives (Health based, anti-stacking)
                { command = "/cast Ardent Defender", conditions = "health < 30 and buff:Guardian of Ancient Kings == 0" },
                { command = "/cast Guardian of Ancient Kings", conditions = "health < 35 and buff:Ardent Defender == 0" },
                { command = "/cast Word of Glory", conditions = "health < 50 and holypower >= 3" },
                
                -- Core Rotation
                { command = "/cast Shield of the Righteous", conditions = "holypower >= 3" },
                { command = "/cast Judgment", conditions = "true" },
                { command = "/cast Hammer of Wrath", conditions = "true" },
                { command = "/cast Avenger's Shield", conditions = "true" },
                { command = "/cast Blessed Hammer", conditions = "true" },
                { command = "/cast [@player] Consecration", conditions = "moving == 0" },
            },
            aoe = {
                { command = "/cast Ardent Defender", conditions = "health < 30" },
                { command = "/cast Word of Glory", conditions = "health < 50 and holypower >= 3" },
                { command = "/cast Avenger's Shield", conditions = "true" },
                { command = "/cast Shield of the Righteous", conditions = "holypower >= 3" },
                { command = "/cast [@player] Consecration", conditions = "true" },
                { command = "/cast Blessed Hammer", conditions = "true" },
                { command = "/cast Judgment", conditions = "true" },
            },
            steps = {}
        }
    }
    },
    ["Midnight"] = {
        type = "Priority",
        st = {
            -- Cooldowns & Talents
            { command = "/cast Sentinel", conditions = "can_cast:Sentinel" },
            { command = "/cast Eye of Tyr", conditions = "can_cast:Eye of Tyr" },
            { command = "/cast Divine Toll", conditions = "can_cast:Divine Toll" },
            { command = "/cast Bastion of Light", conditions = "can_cast:Bastion of Light" },
            { command = "/cast Ardent Defender", conditions = "can_cast:Ardent Defender" },
            { command = "/cast Guardian of Ancient Kings", conditions = "can_cast:Guardian of Ancient Kings" },
            
            -- Core Rotation
            { command = "/cast Shield of the Righteous", conditions = "can_cast:Shield of the Righteous" },
            { command = "/cast Judgment", conditions = "can_cast:Judgment" },
            { command = "/cast Avenger's Shield", conditions = "can_cast:Avenger's Shield" },
            { command = "/cast Hammer of Wrath", conditions = "can_cast:Hammer of Wrath" },
            { command = "/cast Blessed Hammer", conditions = "true" },
            { command = "/cast Consecration", conditions = "true" },
        },
        aoe = {
            { command = "/cast Eye of Tyr", conditions = "can_cast:Eye of Tyr" },
            { command = "/cast Divine Toll", conditions = "can_cast:Divine Toll" },
            { command = "/cast Avenger's Shield", conditions = "can_cast:Avenger's Shield" },
            { command = "/cast Shield of the Righteous", conditions = "can_cast:Shield of the Righteous" },
            { command = "/cast Consecration", conditions = "can_cast:Consecration" },
            { command = "/cast Blessed Hammer", conditions = "can_cast:Blessed Hammer" },
            { command = "/cast Judgment", conditions = "true" },
        },
        steps = {}
    }
}

-- RETRIBUTION (DPS)
SkillWeaver.Sequences[PALADIN_RET] = {
    ["Raid"] = {
        ["Balanced"] = { -- Default
            type = "Priority",
            st = {
                { command = "/cast Rebuke", conditions = "should_interrupt" },
                { command = "/cast Shield of Vengeance", conditions = "health < 60" },
                { command = "/cast Final Verdict", conditions = "holypower >= 3" },
                { command = "/cast Wake of Ashes", conditions = "holypower <= 2" },
                { command = "/cast Judgment", conditions = "true" },
                { command = "/cast Hammer of Wrath", conditions = "true" },
                { command = "/cast Blade of Justice", conditions = "true" },
                { command = "/cast Crusader Strike", conditions = "true" },
            },
            aoe = {
                { command = "/cast Divine Storm", conditions = "holypower >= 3" },
                { command = "/cast Wake of Ashes", conditions = "holypower <= 2" },
                { command = "/cast Judgment", conditions = "true" },
                { command = "/cast Blade of Justice", conditions = "true" },
            },
            steps = {}
        },
        ["Templar"] = { -- Single Target / Hammer of Light Focus
            type = "Priority",
            st = {
                -- Emergency Healing (Ally then Self)
                { command = "/cast [target=mouseover,help,nodead][help] Lay on Hands", conditions = "in_group and ally_health < 15 and range <= 40" },
                { command = "/cast [target=player] Lay on Hands", conditions = "health < 20" },
                { command = "/cast [target=mouseover,help,nodead][help] Word of Glory", conditions = "in_group and ally_health < 30 and holy_power >= 3 and range <= 40" },
                { command = "/cast [target=player] Word of Glory", conditions = "health < 50 and holy_power >= 3" },
                { command = "/cast [target=mouseover,help,nodead][help] Flash of Light", conditions = "in_group and ally_health < 25 and buff:Selfless Healer and range <= 40" },
                
                -- Interrupt & Cleanse
                { command = "/cast Rebuke", conditions = "should_interrupt and range <= 10" },
                { command = "/cast Hammer of Justice", conditions = "should_interrupt and cooldown:Rebuke > 0 and range <= 10" },
                { command = "/cast [target=player] Cleanse", conditions = "debuff_type == poison or debuff_type == disease or movement_impaired" },
                { command = "/cast Shield of Vengeance", conditions = "health < 50" },
                
                -- Cooldowns
                { command = "/cast Crusade", conditions = "heroism or holy_power >= 3" },
                { command = "/cast Hammer of Light", conditions = "true" }, -- Replaces Wake of Ashes when procced
                { command = "/cast Wake of Ashes", conditions = "holy_power <= 2 and range <= 12" },
                { command = "/cast Divine Toll", conditions = "holy_power <= 2" },
                
                -- Finishers
                { command = "/cast Final Verdict", conditions = "holy_power >= 3 and range <= 10" },
                
                -- Generators
                { command = "/cast Hammer of Wrath", conditions = "range <= 30" },
                { command = "/cast Blade of Justice", conditions = "range <= 12" },
                { command = "/cast Templar Slash", conditions = "range <= 8" }, -- Replaces Crusader Strike
                { command = "/cast Judgment", conditions = "range <= 30" },
            },
            aoe = {
                { command = "/cast Rebuke", conditions = "should_interrupt and range <= 10" },
                { command = "/cast Shield of Vengeance", conditions = "health < 50 or enemies_nearby >= 4" },
                { command = "/cast Hammer of Light", conditions = "true" },
                { command = "/cast Divine Storm", conditions = "holy_power >= 3 and range <= 8" },
                { command = "/cast Wake of Ashes", conditions = "holy_power <= 2 and range <= 12" },
                { command = "/cast Divine Toll", conditions = "holy_power <= 2" },
                { command = "/cast Templar Slash", conditions = "range <= 8" },
                { command = "/cast Judgment", conditions = "range <= 30" },
            },
            steps = {}
        },
        ["Herald of the Sun"] = { -- AoE / Dawnlight Focus
            type = "Priority",
            st = {
                { command = "/cast Crusade", conditions = "heroism or holypower >= 3" },
                { command = "/cast Wake of Ashes", conditions = "true" }, -- Applies Dawnlight
                { command = "/cast Divine Toll", conditions = "holypower <= 2" },
                { command = "/cast Final Verdict", conditions = "holypower >= 3" },
                { command = "/cast Hammer of Wrath", conditions = "true" },
                { command = "/cast Judgment", conditions = "true" },
                { command = "/cast Blade of Justice", conditions = "true" },
                { command = "/cast Crusader Strike", conditions = "true" },
            },
            aoe = {
                { command = "/cast Wake of Ashes", conditions = "true" },
                { command = "/cast Divine Toll", conditions = "holypower <= 2" },
                { command = "/cast Divine Storm", conditions = "holypower >= 3" }, -- Spreads Dawnlight
                { command = "/cast Judgment", conditions = "true" },
                { command = "/cast Blade of Justice", conditions = "true" },
                { command = "/cast Crusader Strike", conditions = "true" },
            },
            steps = {}
        }
    }
    },
    ["Midnight"] = {
        type = "Priority",
        st = {
            -- Cooldowns & Talents
            { command = "/cast Crusade", conditions = "can_cast:Crusade" },
            { command = "/cast Avenging Wrath", conditions = "can_cast:Avenging Wrath" },
            { command = "/cast Execution Sentence", conditions = "can_cast:Execution Sentence" },
            { command = "/cast Final Reckoning", conditions = "can_cast:Final Reckoning" },
            { command = "/cast Divine Toll", conditions = "can_cast:Divine Toll" },
            { command = "/cast Wake of Ashes", conditions = "can_cast:Wake of Ashes" },
            { command = "/cast Hammer of Light", conditions = "can_cast:Hammer of Light" },
            
            -- Core Rotation
            { command = "/cast Final Verdict", conditions = "can_cast:Final Verdict" },
            { command = "/cast Templar's Verdict", conditions = "can_cast:Templar's Verdict" },
            { command = "/cast Judgment", conditions = "can_cast:Judgment" },
            { command = "/cast Blade of Justice", conditions = "can_cast:Blade of Justice" },
            { command = "/cast Hammer of Wrath", conditions = "can_cast:Hammer of Wrath" },
            { command = "/cast Crusader Strike", conditions = "true" },
        },
        aoe = {
            { command = "/cast Crusade", conditions = "can_cast:Crusade" },
            { command = "/cast Avenging Wrath", conditions = "can_cast:Avenging Wrath" },
            { command = "/cast Wake of Ashes", conditions = "can_cast:Wake of Ashes" },
            { command = "/cast Divine Toll", conditions = "can_cast:Divine Toll" },
            { command = "/cast Hammer of Light", conditions = "can_cast:Hammer of Light" },
            { command = "/cast Divine Storm", conditions = "can_cast:Divine Storm" },
            { command = "/cast Judgment", conditions = "can_cast:Judgment" },
            { command = "/cast Blade of Justice", conditions = "can_cast:Blade of Justice" },
            { command = "/cast Crusader Strike", conditions = "true" },
        },
        steps = {}
    }
}

-- HOLY (Healer)
-- Controller Friendly: Falls back to [target=target] or [target=player] if no mouseover
SkillWeaver.Sequences[PALADIN_HOLY] = {
    ["Raid"] = {
        ["Balanced"] = {
            type = "Priority",
            st = {
                -- Emergency
                { command = "/cast [target=mouseover,help,nodead][help][target=player] Lay on Hands", conditions = "health < 15" },
                
                -- Spenders
                { command = "/cast [target=mouseover,help,nodead][help][target=player] Word of Glory", conditions = "holypower >= 3" },
                
                -- Generators / Core
                { command = "/cast [target=mouseover,help,nodead][help][target=player] Holy Shock", conditions = "true" },
                { command = "/cast Judgment", conditions = "true" },
                { command = "/cast Hammer of Wrath", conditions = "true" },
                { command = "/cast Crusader Strike", conditions = "true" },
                { command = "/cast [@player] Consecration", conditions = "moving == 0" },
            },
            aoe = {
                { command = "/cast [target=mouseover,help,nodead][help][target=player] Light of Dawn", conditions = "holypower >= 3" },
                { command = "/cast Holy Prism", conditions = "true" },
                { command = "/cast [target=mouseover,help,nodead][help][target=player] Holy Shock", conditions = "true" },
                { command = "/cast Judgment", conditions = "true" },
            },
            steps = {}
        }
    },
    ["Midnight"] = {
        type = "Priority",
        st = {
            -- Cooldowns & Talents
            { command = "/cast Avenging Wrath", conditions = "can_cast:Avenging Wrath" },
            { command = "/cast Divine Toll", conditions = "can_cast:Divine Toll" },
            { command = "/cast Tyr's Deliverance", conditions = "can_cast:Tyr's Deliverance" },
            { command = "/cast Light's Hammer", conditions = "can_cast:Light's Hammer" },
            { command = "/cast Holy Prism", conditions = "can_cast:Holy Prism" },
            { command = "/cast Barrier of Faith", conditions = "can_cast:Barrier of Faith" },
            
            -- Core Rotation
            { command = "/cast Holy Shock", conditions = "can_cast:Holy Shock" },
            { command = "/cast Word of Glory", conditions = "can_cast:Word of Glory" },
            { command = "/cast Light of Dawn", conditions = "can_cast:Light of Dawn" },
            { command = "/cast Judgment", conditions = "can_cast:Judgment" },
            { command = "/cast Hammer of Wrath", conditions = "can_cast:Hammer of Wrath" },
            { command = "/cast Crusader Strike", conditions = "true" },
        },
        aoe = {
            { command = "/cast Divine Toll", conditions = "can_cast:Divine Toll" },
            { command = "/cast Holy Prism", conditions = "can_cast:Holy Prism" },
            { command = "/cast Light's Hammer", conditions = "can_cast:Light's Hammer" },
            { command = "/cast Light of Dawn", conditions = "can_cast:Light of Dawn" },
            { command = "/cast Holy Shock", conditions = "can_cast:Holy Shock" },
            { command = "/cast Judgment", conditions = "can_cast:Judgment" },
            { command = "/cast Crusader Strike", conditions = "true" },
        },
        steps = {}
    }
}
