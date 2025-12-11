local ADDON_NAME, SkillWeaver = ...

-- Warlock Sequences
-- Covers: Destruction (267), Affliction (265), Demonology (266)

local WARLOCK_DESTRUCTION = "WARLOCK_267"
local WARLOCK_AFFLICTION = "WARLOCK_265"
local WARLOCK_DEMONOLOGY = "WARLOCK_266"

-----------------------------------------------------------
-- AFFLICTION WARLOCK (265)
-----------------------------------------------------------
SkillWeaver.Sequences[WARLOCK_AFFLICTION] = {
    ["Mythic+"] = {
        ["Soul Harvester"] = { -- Affliction / Soul Harvester Hero Talent
            type = "Priority",
            st = {
                -- Pet Management
                { command = "/cast Summon Felhunter", conditions = "not pet_exists and not in_combat" },
                { command = "/petattack", conditions = "pet_exists and target_attackable and not pet_attacking" },
                { command = "/cast Health Funnel", conditions = "pet_exists and pet_health < 40 and health > 60 and not in_combat" },
                { command = "/cast [pet] Threatening Presence", conditions = "pet_exists and not in_group and not pet:buff:Threatening Presence and pet_name == Voidwalker" },
                { command = "/cast [pet] Threatening Presence", conditions = "pet_exists and in_group and pet:buff:Threatening Presence and pet_name == Voidwalker" },
                
                -- Survival & Utility
                { command = "/cast [pet] Spell Lock", conditions = "should_interrupt and range <= 40" },
                { command = "/cast [pet] Axe Toss", conditions = "should_interrupt and cooldown:Spell Lock > 0 and pet_name == Felguard and range <= 30" },
                { command = "/cast Mortal Coil", conditions = "(should_interrupt or health < 50) and talent(Mortal Coil) and range <= 20" },
                { command = "/use Healthstone", conditions = "health < 30" },
                { command = "/cast Unending Resolve", conditions = "health < 35" },
                { command = "/cast Unending Resolve", conditions = "health < 35" },
                { command = "/cast [target=player] Command Demon", conditions = "pet_name == Imp and debuff_type == magic" }, -- Singe Magic
                { command = "/cast [target=player] Dark Pact", conditions = "health < 40 and talent(Dark Pact)" },
                { command = "/cast [target=mouseover,help,nodead][target=player] Siphon Life", conditions = "in_group and ally_health < 20 and talent(Siphon Life) and range <= 40" },
                
                -- Maintain DoTs
                { command = "/cast Agony", conditions = "debuff:Agony < 5.4 and range <= 40" },
                { command = "/cast Corruption", conditions = "debuff:Corruption < 4 and range <= 40" },
                { command = "/cast Unstable Affliction", conditions = "debuff:Unstable Affliction < 5 and range <= 40" },
                { command = "/cast Siphon Life", conditions = "debuff:Siphon Life < 5 and talent(Siphon Life) and range <= 40" },
                
                -- Cooldowns
                { command = "/cast Summon Darkglare", conditions = "cooldown:Summon Darkglare == 0" },
                { command = "/cast Soul Rot", conditions = "talent(Soul Rot) and range <= 40" },
                { command = "/cast Phantom Singularity", conditions = "talent(Phantom Singularity) and range <= 40" },
                { command = "/cast Vile Taint", conditions = "talent(Vile Taint) and soul_shards >= 1 and range <= 40" },
                
                -- Soul Harvester
                { command = "/cast Malefic Rapture", conditions = "soul_shards >= 2 and buff:Soul Harvester and range <= 40" },
                { command = "/cast Malefic Rapture", conditions = "soul_shards >= 5 and range <= 40" },
                
                -- Generators
                { command = "/cast Drain Soul", conditions = "target_health < 20 and talent(Drain Soul) and range <= 40" },
                { command = "/cast Shadow Bolt", conditions = "range <= 40" },
            },
            aoe = {
                { command = "/cast [pet] Spell Lock", conditions = "should_interrupt and range <= 40" },
                { command = "/cast Unending Resolve", conditions = "health < 40 or enemies_nearby >= 5" },
                { command = "/cast Summon Darkglare", conditions = "cooldown:Summon Darkglare == 0" },
                { command = "/cast Seed of Corruption", conditions = "enemies_nearby >= 3 and range <= 40" },
                { command = "/cast Vile Taint", conditions = "soul_shards >= 1 and range <= 40" },
                { command = "/cast Phantom Singularity", conditions = "talent(Phantom Singularity) and range <= 40" },
                { command = "/cast Malefic Rapture", conditions = "soul_shards >= 3 and range <= 40" },
                { command = "/cast Agony", conditions = "range <= 40" },
            },
            steps = {}
        }
    }
    },
    ["Midnight"] = {
        type = "Priority",
        st = {
            -- Multi-DoT: Cycle if Agony is up. 
            { command = "/cycle", conditions = "debuff:Agony" },
            
            -- Cooldowns & Talents
            { command = "/cast Summon Darkglare", conditions = "can_cast:Summon Darkglare" },
            { command = "/cast Soul Rot", conditions = "can_cast:Soul Rot" },
            { command = "/cast Phantom Singularity", conditions = "can_cast:Phantom Singularity" },
            { command = "/cast Vile Taint", conditions = "can_cast:Vile Taint" },
            
            -- Spenders
            { command = "/cast Malefic Rapture", conditions = "can_cast:Malefic Rapture" },
            
            -- DoTs & Fillers
            { command = "/cast Agony", conditions = "true" },
            { command = "/cast Corruption", conditions = "true" },
            { command = "/cast Unstable Affliction", conditions = "true" },
            { command = "/cast Siphon Life", conditions = "can_cast:Siphon Life" },
            { command = "/cast Drain Soul", conditions = "can_cast:Drain Soul" }, -- Execute/Filler
            { command = "/cast Shadow Bolt", conditions = "true" },
        },
        aoe = {},
        steps = {}
    }
}

-----------------------------------------------------------
-- DEMONOLOGY WARLOCK (266)
-----------------------------------------------------------
SkillWeaver.Sequences[WARLOCK_DEMONOLOGY] = {
    ["Mythic+"] = {
        ["Diabolist"] = { -- Demonology / Diabolist Hero Talent
            type = "Priority",
            st = {
                -- Pet Management (Felguard primary)
                { command = "/cast Summon Felguard", conditions = "not pet_exists and not in_combat" },
                { command = "/petattack", conditions = "pet_exists and target_attackable and not pet_attacking" },
                { command = "/cast Health Funnel", conditions = "pet_exists and pet_health < 40 and health > 60 and not in_combat" },
                { command = "/cast [pet] Threatening Presence", conditions = "pet_exists and not in_group and not pet:buff:Threatening Presence and pet_name == Voidwalker" },
                { command = "/cast [pet] Threatening Presence", conditions = "pet_exists and in_group and pet:buff:Threatening Presence and pet_name == Voidwalker" },
                
                -- Survival & Utility
                { command = "/cast [pet] Axe Toss", conditions = "should_interrupt and pet_name == Felguard and range <= 30" },
                { command = "/cast [pet] Spell Lock", conditions = "should_interrupt and range <= 40" },
                { command = "/cast Mortal Coil", conditions = "(should_interrupt or health < 50) and talent(Mortal Coil) and range <= 20" },
                { command = "/use Healthstone", conditions = "health < 30" },
                { command = "/cast Unending Resolve", conditions = "health < 35" },
                { command = "/cast Unending Resolve", conditions = "health < 35" },
                { command = "/cast [target=player] Command Demon", conditions = "pet_name == Imp and debuff_type == magic" }, -- Singe Magic
                { command = "/cast [target=player] Dark Pact", conditions = "health < 40 and talent(Dark Pact)" },
                
                -- Cooldowns
                { command = "/cast Summon Demonic Tyrant", conditions = "cooldown:Summon Demonic Tyrant == 0 and (buff:Demonic Core or soul_shards >= 4)" },
                { command = "/cast Nether Portal", conditions = "talent(Nether Portal) and cooldown:Nether Portal == 0" },
                { command = "/cast Grimoire: Felguard", conditions = "talent(Grimoire: Felguard) and cooldown:Grimoire: Felguard == 0 and range <= 40" },
                { command = "/cast Power Siphon", conditions = "buff:Wild Imps >= 2 and talent(Power Siphon)" },
                { command = "/cast Bilescourge Bombers", conditions = "talent(Bilescourge Bombers) and range <= 40" },
                
                -- Demon Summoning
                { command = "/cast Call Dreadstalkers", conditions = "soul_shards >= 2 and range <= 40" },
                { command = "/cast Hand of Gul'dan", conditions = "soul_shards >= 3 and range <= 40" },
                
                -- Generators (with Demonic Core management)
                { command = "/cast Demonbolt", conditions = "buff:Demonic Core and range <= 40" },
                { command = "/cast Shadow Bolt", conditions = "range <= 40" },
            },
            aoe = {
                { command = "/cast [pet] Spell Lock", conditions = "should_interrupt and range <= 40" },
                { command = "/cast Unending Resolve", conditions = "health < 40 or enemies_nearby >= 5" },
                { command = "/cast Summon Demonic Tyrant", conditions = "cooldown:Summon Demonic Tyrant == 0" },
                { command = "/cast Implosion", conditions = "buff:Wild Imps >= 4 and enemies_nearby >= 3 and range <= 40" },
                { command = "/cast Bilescourge Bombers", conditions = "talent(Bilescourge Bombers) and range <= 40" },
                { command = "/cast Hand of Gul'dan", conditions = "soul_shards >= 3 and range <= 40" },
                { command = "/cast Call Dreadstalkers", conditions = "soul_shards >= 2 and range <= 40" },
                { command = "/cast Demonbolt", conditions = "buff:Demonic Core and range <= 40" },
                { command = "/cast Shadow Bolt", conditions = "range <= 40" },
            },
            steps = {}
        }
    }
    },
    ["Midnight"] = {
        type = "Priority",
        st = {
            -- Cooldowns & Talents
            { command = "/cast Summon Demonic Tyrant", conditions = "can_cast:Summon Demonic Tyrant" },
            { command = "/cast Nether Portal", conditions = "can_cast:Nether Portal" },
            { command = "/cast Grimoire: Felguard", conditions = "can_cast:Grimoire: Felguard" },
            { command = "/cast Summon Vilefiend", conditions = "can_cast:Summon Vilefiend" },
            { command = "/cast Power Siphon", conditions = "can_cast:Power Siphon" },
            { command = "/cast Bilescourge Bombers", conditions = "can_cast:Bilescourge Bombers" },
            { command = "/cast Guillotine", conditions = "can_cast:Guillotine" },
            
            -- Core Rotation
            { command = "/cast Hand of Gul'dan", conditions = "can_cast:Hand of Gul'dan" },
            { command = "/cast Call Dreadstalkers", conditions = "can_cast:Call Dreadstalkers" },
            { command = "/cast Demonbolt", conditions = "can_cast:Demonbolt" },
            { command = "/cast Shadow Bolt", conditions = "true" },
        },
        aoe = {},
        steps = {}
    }
}

-----------------------------------------------------------
-- DESTRUCTION WARLOCK (267)
-----------------------------------------------------------
SkillWeaver.Sequences[WARLOCK_DESTRUCTION] = {
    ["Raid"] = {
        ["Balanced"] = { -- Default
            type = "Priority",
            st = {
                { command = "/cast Immolate", conditions = "buff:Immolate < 5" },
                { command = "/cast Conflagrate", conditions = "charges:Conflagrate == 2" },
                { command = "/cast Chaos Bolt", conditions = "shards >= 4" },
                { command = "/cast Incinerate", conditions = "true" },
            },
            aoe = {
                { command = "/cast Rain of Fire", conditions = "shards >= 3" },
                { command = "/cast Immolate", conditions = "true" },
                { command = "/cast Incinerate", conditions = "true" },
            },
            steps = {}
        },
        ["Diabolist"] = { -- Single Target / Ritual Focus
            type = "Priority",
            st = {
                -- Pet Management (FIRST - ensure pet exists and configured)
                { command = "/cast Summon Imp", conditions = "not pet_exists and not in_combat" },
                { command = "/petattack", conditions = "pet_exists and target_attackable and not pet_attacking" },
                { command = "/cast Health Funnel", conditions = "pet_exists and pet_health < 40 and health > 60 and not in_combat" },
                { command = "/cast [pet] Threatening Presence", conditions = "pet_exists and not in_group and not pet:buff:Threatening Presence and pet_name == Voidwalker" }, -- Enable taunt solo
                { command = "/cast [pet] Threatening Presence", conditions = "pet_exists and in_group and pet:buff:Threatening Presence and pet_name == Voidwalker" }, -- Disable taunt in groups
                
                -- Priority 1: SURVIVAL & UTILITY
                { command = "/cast [pet] Spell Lock", conditions = "should_interrupt and range <= 40" },
                { command = "/cast [pet] Axe Toss", conditions = "should_interrupt and cooldown:Spell Lock > 0 and pet_name == Felguard and range <= 30" },
                { command = "/cast Mortal Coil", conditions = "(should_interrupt or health < 50) and talent(Mortal Coil) and range <= 20" },
                { command = "/use Healthstone", conditions = "health < 30" },
                { command = "/cast Unending Resolve", conditions = "health < 35" },
                { command = "/cast Unending Resolve", conditions = "health < 35" },
                { command = "/cast [target=player] Command Demon", conditions = "pet_name == Imp and debuff_type == magic" }, -- Singe Magic
                { command = "/cast [target=player] Dark Pact", conditions = "health < 40 and talent(Dark Pact)" },
                
                -- Opener / Maintenance
                { command = "/cast Immolate", conditions = "buff:Immolate < 5 and range <= 40" },
                
                -- Cooldowns
                { command = "/cast Summon Infernal", conditions = "heroism or target_health < 20 or cooldown:Ruination < 10" },
                { command = "/cast Dimensional Rift", conditions = "(charges:Dimensional Rift > 1 or target_health < 20) and range <= 40" },
                
                -- Diabolist Ritual Cycle
                { command = "/cast Ruination", conditions = "buff:Diabolic Ritual and range <= 40" }, -- Replaces Chaos Bolt when procced
                
                -- Generators
                { command = "/cast Soul Fire", conditions = "talent(Soul Fire) and cooldown:Soul Fire == 0 and range <= 40" },
                { command = "/cast Conflagrate", conditions = "charges:Conflagrate > 0 and range <= 40" },
                
                -- Spenders
                { command = "/cast Chaos Bolt", conditions = "(shards >= 3.5 or buff:Backdraft) and range <= 40" },
                { command = "/cast Shadowburn", conditions = "(target_health < 20 or buff:Conflagration of Chaos) and range <= 40" },
                
                -- Filler
                { command = "/cast Incinerate", conditions = "range <= 40" },
            },
            aoe = {
                { command = "/cast [pet] Spell Lock", conditions = "should_interrupt and range <= 40" },
                { command = "/cast Unending Resolve", conditions = "health < 40 or enemies_nearby >= 5" },
                { command = "/cast Rain of Fire", conditions = "shards >= 3 and range <= 40" },
                { command = "/cast Cataclysm", conditions = "talent(Cataclysm) and range <= 40" },
                { command = "/cast Channel Demonfire", conditions = "talent(Channel Demonfire) and range <= 40" },
                { command = "/cast Dimensional Rift", conditions = "range <= 40" },
                { command = "/cast Immolate", conditions = "range <= 40" },
            },
            steps = {}
        },
        ["Hellcaller"] = { -- AoE / Wither Focus
            type = "Priority",
            st = {
                { command = "/cast Wither", conditions = "buff:Wither < 5" }, -- Replaces Immolate
                { command = "/cast Cataclysm", conditions = "true" },
                { command = "/cast Soul Fire", conditions = "talent(Soul Fire)" },
                { command = "/cast Conflagrate", conditions = "true" },
                { command = "/cast Chaos Bolt", conditions = "shards >= 4" },
                { command = "/cast Incinerate", conditions = "true" },
            },
            aoe = {
                { command = "/cast Wither", conditions = "true" },
                { command = "/cast Rain of Fire", conditions = "shards >= 3" },
                { command = "/cast Cataclysm", conditions = "true" },
                { command = "/cast Channel Demonfire", conditions = "true" },
                { command = "/cast Dimensional Rift", conditions = "true" },
                { command = "/cast Havoc", conditions = "true" },
            },
            steps = {}
        }
    },
    ["Midnight"] = {
        type = "Priority",
        st = {
            -- Multi-DoT: Cycle if Immolate (Wither) is up.
            { command = "/cycle", conditions = "debuff:Immolate" },
            
            -- Hero Talents (Diabolist / Hellcaller)
            { command = "/cast Ruination", conditions = "can_cast:Ruination" }, -- Diabolist Proc
            { command = "/cast Wither", conditions = "can_cast:Wither" }, -- Hellcaller Replacement
            
            -- Cooldowns & Talents
            { command = "/cast Summon Infernal", conditions = "can_cast:Summon Infernal" },
            { command = "/cast Dimensional Rift", conditions = "can_cast:Dimensional Rift" },
            { command = "/cast Cataclysm", conditions = "can_cast:Cataclysm" },
            { command = "/cast Channel Demonfire", conditions = "can_cast:Channel Demonfire" },
            { command = "/cast Soul Fire", conditions = "can_cast:Soul Fire" },
            
            -- Spenders & Finishers
            { command = "/cast Shadowburn", conditions = "can_cast:Shadowburn" },
            { command = "/cast Chaos Bolt", conditions = "can_cast:Chaos Bolt" },
            
            -- Generators
            { command = "/cast Conflagrate", conditions = "can_cast:Conflagrate" },
            { command = "/cast Immolate", conditions = "can_cast:Immolate" },
            { command = "/cast Incinerate", conditions = "true" },
        },
        aoe = {},
        steps = {}
    }
}
