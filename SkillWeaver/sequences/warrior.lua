local ADDON_NAME, SkillWeaver = ...

-- Warrior Sequences
-- Covers: Arms (71), Fury (72), Protection (73)

local WARRIOR_ARMS = "WARRIOR_71"
local WARRIOR_FURY = "WARRIOR_72"

SkillWeaver.Sequences[WARRIOR_ARMS] = {
    ["Raid"] = {
        ["Balanced"] = { -- Default/Fallback
            type = "Priority",
            st = {
                { command = "/cast Execute", conditions = "target_health < 20 or buff:Sudden Death" },
                { command = "/cast Mortal Strike", conditions = "true" },
                { command = "/cast Overpower", conditions = "true" },
                { command = "/cast Slam", conditions = "rage > 40" },
            },
            aoe = {
                { command = "/cast Sweeping Strikes", conditions = "true" },
                { command = "/cast Bladestorm", conditions = "true" },
                { command = "/cast Cleave", conditions = "true" },
                { command = "/cast Whirlwind", conditions = "true" },
            },
            steps = {}
        },
        ["Slayer"] = { -- Single Target / Execute Focus
            type = "Priority",
            st = {
                -- Priority 1: SURVIVAL & UTILITY
                { command = "/cast Pummel", conditions = "should_interrupt and range <= 8" }, -- Interrupt
                { command = "/cast Storm Bolt", conditions = "should_interrupt and cooldown:Pummel > 0 and talent(Storm Bolt) and range <= 20" }, -- Backup interrupt
                { command = "/cast Rallying Cry", conditions = "in_group and (health < 40 or raid_health < 50)" }, -- Group defensive
                { command = "/cast Shield Wall", conditions = "health < 35 and buff:Last Stand == 0" }, -- Anti-stack
                { command = "/cast Last Stand", conditions = "health < 30 and buff:Shield Wall == 0" }, -- Anti-stack
                { command = "/cast Impending Victory", conditions = "health < 40 and talent(Impending Victory)" }, -- Emergency heal
                { command = "/cast Victory Rush", conditions = "health < 50 and buff:Victorious" }, -- Free heal
                { command = "/cast Ignore Pain", conditions = "health < 60 and rage >= 40" }, -- Absorb
                
                -- Cooldowns (SimC Priority - CS debuff coordination)
                { command = "/cast Thunderous Roar", conditions = "buff:Enrage and range <= 12" },
                { command = "/cast Avatar", conditions = "cooldown:Colossus Smash < 5 or debuff:Colossus Smash" },
                { command = "/cast Champions Spear", conditions = "(debuff:Colossus Smash or buff:Avatar) and range <= 25" },
                { command = "/cast Ravager", conditions = "cooldown:Colossus Smash < 2 and range <= 8" },
                { command = "/cast Colossus Smash", conditions = "range <= 8" },
                { command = "/cast Warbreaker", conditions = "talent(Warbreaker) and range <= 8" },
                
                -- Execute Windows (Juggernaut/Sudden Death priority)
                { command = "/cast Execute", conditions = "buff:Juggernaut < 2 and talent(Juggernaut) and range <= 8" }, -- Expiring Juggernaut
                { command = "/cast Execute", conditions = "buff:Sudden Death and charges:Sudden Death > 1 and range <= 8" }, -- Dump stacks
                { command = "/cast Execute", conditions = "(target_health < 20 or target_health < 35 and talent(Massacre)) and range <= 8" },
                
                -- Core Rotation
                { command = "/cast Bladestorm", conditions = "(debuff:Colossus Smash > 4 or cooldown:Colossus Smash > 15) and range <= 8" }, -- During CS or if CS far away
                { command = "/cast Overpower", conditions = "buff:Opportunist and range <= 8" }, -- Prio with proc
                { command = "/cast Mortal Strike", conditions = "range <= 8" },
                { command = "/cast Skullsplitter", conditions = "rage < 40 and range <= 8" }, -- Rage generation when low
                { command = "/cast Overpower", conditions = "range <= 8" },
                { command = "/cast Rend", conditions = "talent(Rend) and debuff:Rend < 4 and range <= 8" },
                { command = "/cast Execute", conditions = "buff:Sudden Death and range <= 8" }, -- Cleanup SD
                { command = "/cast Slam", conditions = "rage > 40 and range <= 8" },
            },
            aoe = {
                { command = "/cast Pummel", conditions = "should_interrupt and range <= 8" },
                { command = "/cast Shield Wall", conditions = "health < 40 or enemies_nearby >= 5" },
                { command = "/cast Thunderous Roar", conditions = "range <= 12" },
                { command = "/cast Sweeping Strikes", conditions = "range <= 8" },
                { command = "/cast Avatar", conditions = "true" },
                { command = "/cast Champions Spear", conditions = "range <= 25" },
                { command = "/cast Colossus Smash", conditions = "range <= 8" },
                { command = "/cast Warbreaker", conditions = "range <= 8" },
                { command = "/cast Bladestorm", conditions = "(debuff:Colossus Smash or cooldown:Colossus Smash > 10) and range <= 8" },
                { command = "/cast Cleave", conditions = "range <= 8" },
                { command = "/cast Whirlwind", conditions = "range <= 8" },
                { command = "/cast Execute", conditions = "buff:Sudden Death and range <= 8" },
            },
            steps = {}
        },
        ["Colossus"] = { -- AoE / Demolish Focus
            type = "Priority",
            st = {
                -- Cooldowns
                { command = "/cast Thunderous Roar", conditions = "true" },
                { command = "/cast Ravager", conditions = "true" },
                { command = "/cast Champions Spear", conditions = "true" },
                { command = "/cast Avatar", conditions = "true" },
                { command = "/cast Colossus Smash", conditions = "true" }, -- CS before Demolish for debuff
                { command = "/cast Warbreaker", conditions = "true" },
                
                -- Colossus Logic
                { command = "/cast Mortal Strike", conditions = "true" },
                { command = "/cast Demolish", conditions = "debuff:Colossus Smash" }, -- Only Demolish if CS is up
                { command = "/cast Execute", conditions = "target_health < 20" },
                { command = "/cast Skullsplitter", conditions = "true" },
                { command = "/cast Overpower", conditions = "true" },
                { command = "/cast Rend", conditions = "talent(Rend) and debuff:Rend < 4" },
            },
            aoe = {
                { command = "/cast Thunderous Roar", conditions = "true" },
                { command = "/cast Sweeping Strikes", conditions = "true" },
                { command = "/cast Avatar", conditions = "true" },
                { command = "/cast Colossus Smash", conditions = "true" },
                { command = "/cast Warbreaker", conditions = "true" },
                { command = "/cast Demolish", conditions = "debuff:Colossus Smash" },
                { command = "/cast Cleave", conditions = "true" },
                { command = "/cast Whirlwind", conditions = "true" },
            },
            steps = {}
        }
    }
}

SkillWeaver.Sequences[WARRIOR_FURY] = {
    ["Raid"] = {
        ["Balanced"] = {
            type = "Priority",
            st = {
                { command = "/cast Rampage", conditions = "rage > 80" },
                { command = "/cast Execute", conditions = "true" },
                { command = "/cast Bloodthirst", conditions = "true" },
                { command = "/cast Raging Blow", conditions = "true" },
            },
            aoe = {
                { command = "/cast Whirlwind", conditions = "buff:Whirlwind == 0" },
                { command = "/cast Rampage", conditions = "true" },
            },
            steps = {}
        },
        ["Slayer"] = { -- Execute / Enrage Focus
            type = "Priority",
            st = {
                -- Cooldowns
                { command = "/cast Recklessness", conditions = "heroism or target_health < 35 or cooldown:Avatar > 20" },
                { command = "/cast Avatar", conditions = "talent(Avatar)" },
                { command = "/cast Champions Spear", conditions = "buff:Enrage and cooldown:Bladestorm > 2" },
                { command = "/cast Ravager", conditions = "buff:Enrage" },
                { command = "/cast Thunderous Roar", conditions = "buff:Enrage" },
                { command = "/cast Odyns Fury", conditions = "buff:Enrage or talent(Titanic Rage)" },
                
                -- Execute Windows (High Priority)
                { command = "/cast Execute", conditions = "buff:Sudden Death and charges:Sudden Death > 1" }, -- Dump stacks
                { command = "/cast Execute", conditions = "buff:Sudden Death and buff:Sudden Death < 2" }, -- Expiring soon
                { command = "/cast Execute", conditions = "buff:Ashen Juggernaut and buff:Ashen Juggernaut < 2" }, -- Expiring
                
                -- Enrage Maintenance
                { command = "/cast Rampage", conditions = "buff:Enrage == 0" }, -- Maintain Enrage
                { command = "/cast Rampage", conditions = "rage >= 115 and talent(Reckless Abandon) and buff:Recklessness" }, -- Pool during Reck
                
                -- Core Rotation
                { command = "/cast Bladestorm", conditions = "talent(Slayer's Dominance) and buff:Enrage" },
                { command = "/cast Execute", conditions = "target_health < 35 or debuff:Marked for Execution" },
                { command = "/cast Onslaught", conditions = "talent(Onslaught)" },
                { command = "/cast Bloodthirst", conditions = "buff:Bloodcraze >= 2 or target_health < 35 and talent(Vicious Contempt)" }, -- Prioritize with stacks
                { command = "/cast Raging Blow", conditions = "charges:Raging Blow > 1" }, -- Dump charges
                { command = "/cast Rampage", conditions = "rage >= 100" }, -- Dump rage
                { command = "/cast Bloodthirst", conditions = "true" }, 
                { command = "/cast Raging Blow", conditions = "true" },
                { command = "/cast Whirlwind", conditions = "talent(Improved Whirlwind)" },
            },
            aoe = {
                { command = "/cast Recklessness", conditions = "true" },
                { command = "/cast Avatar", conditions = "true" },
                { command = "/cast Thunderous Roar", conditions = "true" },
                { command = "/cast Odyns Fury", conditions = "true" },
                { command = "/cast Bladestorm", conditions = "talent(Slayer's Dominance) and buff:Enrage" },
                { command = "/cast Whirlwind", conditions = "buff:Whirlwind == 0" },
                { command = "/cast Rampage", conditions = "buff:Enrage == 0 or rage > 100" },
                { command = "/cast Bloodthirst", conditions = "true" },
                { command = "/cast Raging Blow", conditions = "true" },
            },
            steps = {}
        },
                -- Cooldowns
                { command = "/cast Avatar", conditions = "true" },
                { command = "/cast Recklessness", conditions = "true" },
                { command = "/cast Ravager", conditions = "true" },
                { command = "/cast Thunderous Roar", conditions = "buff:Enrage" },
                { command = "/cast Champions Spear", conditions = "buff:Enrage" },
                { command = "/cast Odyns Fury", conditions = "buff:Enrage or talent(Titanic Rage)" },
                
                -- Thane Logic (Thunder Blast priority)
                { command = "/cast Thunder Blast", conditions = "buff:Thunder Blast" }, -- Replaces Thunder Clap
                { command = "/cast Thunder Clap", conditions = "true" }, -- Generates stacks
                { command = "/cast Rampage", conditions = "buff:Enrage == 0" }, -- Maintain Enrage
                { command = "/cast Execute", conditions = "buff:Ashen Juggernaut and buff:Ashen Juggernaut < 2" },
                { command = "/cast Rampage", conditions = "rage >= 115 and talent(Reckless Abandon) and buff:Recklessness" },
                { command = "/cast Bladestorm", conditions = "buff:Enrage and talent(Unhinged)" },
                { command = "/cast Bloodthirst", conditions = "buff:Bloodcraze >= 2" },
                { command = "/cast Rampage", conditions = "rage >= 100" },
                { command = "/cast Onslaught", conditions = "talent(Onslaught)" },
                { command = "/cast Bloodthirst", conditions = "true" },
                { command = "/cast Raging Blow", conditions = "true" },
            },
            aoe = {
                { command = "/cast Avatar", conditions = "true" },
                { command = "/cast Thunderous Roar", conditions = "buff:Enrage" },
                { command = "/cast Odyns Fury", conditions = "true" },
                { command = "/cast Thunder Blast", conditions = "buff:Thunder Blast" },
                { command = "/cast Thunder Clap", conditions = "buff:Whirlwind == 0 or talent(Meat Cleaver)" },
                { command = "/cast Whirlwind", conditions = "buff:Whirlwind == 0" },
                { command = "/cast Rampage", conditions = "buff:Enrage == 0 or rage > 100" },
                { command = "/cast Bloodthirst", conditions = "true" },
                { command = "/cast Raging Blow", conditions = "true" },
            },
            steps = {}
        }
    }
}

local WARRIOR_PROT = "WARRIOR_73"

SkillWeaver.Sequences[WARRIOR_PROT] = {
    ["Raid"] = {
        ["Balanced"] = {
            type = "Priority",
            st = {
                -- Active Mitigation (maintain 100% uptime)
                { command = "/cast Shield Block", conditions = "buff:Shield Block == 0 or buff:Shield Block < 2" },
                { command = "/cast Ignore Pain", conditions = "rage >= 40 and (buff:Ignore Pain == 0 or buff:Ignore Pain < 3)" },
                
                -- Defensives (Health based, with anti-stacking)
                -- Don't use if another major defensive is already active
                { command = "/cast Last Stand", conditions = "health < 30 and cooldown:Shield Wall > 0 and buff:Shield Wall == 0" },
                { command = "/cast Shield Wall", conditions = "health < 40 and cooldown:Last Stand > 0 and buff:Last Stand == 0" },
                
                -- Interrupt
                { command = "/cast Pummel", conditions = "should_interrupt" },
                
                -- Talent-dependent: Avatar (if talented)
                -- { command = "/cast Avatar", conditions = "cooldown:Avatar == 0" },
                
                -- Rage Generators (priority for active mitigation)
                { command = "/cast Shield Slam", conditions = "true" },
                { command = "/cast Thunder Clap", conditions = "true" },
                { command = "/cast Revenge", conditions = "true" },
                
                -- Execute/Devastate (filler)
                { command = "/cast Execute", conditions = "true" },
                { command = "/cast Devastate", conditions = "true" },
            },
            aoe = {
                -- Active Mitigation first
                { command = "/cast Shield Block", conditions = "buff:Shield Block == 0" },
                { command = "/cast Ignore Pain", conditions = "rage >= 60" },
                
                -- Defensives
                { command = "/cast Shield Wall", conditions = "health < 40" },
                
                -- AoE Rotation
                { command = "/cast Thunder Clap", conditions = "true" },
                { command = "/cast Revenge", conditions = "true" },
                { command = "/cast Shield Slam", conditions = "true" },
                { command = "/cast Devastate", conditions = "true" },
            },
            steps = {}
        }
    }
            { command = "/cast Shield Wall", conditions = "can_cast:Shield Wall" },
            { command = "/cast Last Stand", conditions = "can_cast:Last Stand" },
            { command = "/cast Demoralizing Shout", conditions = "can_cast:Demoralizing Shout" },
            { command = "/cast Ravager", conditions = "can_cast:Ravager" },
            { command = "/cast Champions Spear", conditions = "can_cast:Champions Spear" },
            { command = "/cast Shockwave", conditions = "can_cast:Shockwave" },
            
            -- Core Rotation
            { command = "/cast Shield Slam", conditions = "can_cast:Shield Slam" },
            { command = "/cast Thunder Clap", conditions = "can_cast:Thunder Clap" },
            { command = "/cast Revenge", conditions = "can_cast:Revenge" },
            { command = "/cast Execute", conditions = "can_cast:Execute" },
            { command = "/cast Devastate", conditions = "true" },
        },
        aoe = {
            { command = "/cast Ravager", conditions = "can_cast:Ravager" },
            { command = "/cast Shockwave", conditions = "can_cast:Shockwave" },
            { command = "/cast Thunder Clap", conditions = "can_cast:Thunder Clap" },
            { command = "/cast Revenge", conditions = "can_cast:Revenge" },
            { command = "/cast Shield Slam", conditions = "can_cast:Shield Slam" },
            { command = "/cast Devastate", conditions = "true" },
        },
        steps = {}
    }
}
