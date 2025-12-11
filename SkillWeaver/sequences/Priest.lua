local ADDON_NAME, SkillWeaver = ...

-- Priest Sequences
-- Covers: Discipline (256), Holy (257), Shadow (258)

local PRIEST_DISC = "PRIEST_256"
local PRIEST_HOLY = "PRIEST_257"
local PRIEST_SHADOW = "PRIEST_258"

SkillWeaver.Sequences[PRIEST_DISC] = {
    ["Raid"] = {
        ["Enhanced"] = {
            type = "Priority",
            -- ULTRA-AUTOMATED: Just spam, addon does everything
            st = {
                -- CRITICAL: Player is dying
                { command = "/cast [target=player] Desperate Prayer", conditions = "health < 20" },
                { command = "/cast [target=player] Power Word: Shield", conditions = "health < 30" },
                { command = "/cast [target=player] Penance", conditions = "health < 40" },
                
                -- AUTO-TARGET: Find and heal lowest ally
                { command = "/run SkillWeaver.HealingHelper:SetSmartHealTarget()", conditions = "lowest_ally_health < 70" },
                
                -- EMERGENCY: Someone very low
                { command = "/cast [help] Power Word: Shield", conditions = "target_health < 40" },
                { command = "/cast [help] Penance", conditions = "target_health < 50" },
                
                -- AOE HEALING: 3+ people need heals
                { command = "/cast Power Word: Radiance", conditions = "allies_below_health:80 >= 3" },
                { command = "/cast [target=player] Power Word: Radiance", conditions = "allies_below_health:70 >= 5" },
                
                -- DISPEL
                { command = "/cast [help] Purify", conditions = "needs_dispel" },
                
                -- SMART SINGLE TARGET
                { command = "/cast [help] Power Word: Shield", conditions = "target_health < 90" },
                { command = "/cast [help] Shadow Mend", conditions = "target_health < 80" },
                { command = "/cast [help] Flash Heal", conditions = "target_health < 70" },
                
                -- DPS FILLER: Only if everyone healthy
                { command = "/cast [harm] Shadow Word: Pain", conditions = "lowest_ally_health > 90" },
                { command = "/cast [harm] Smite", conditions = "lowest_ally_health > 90" },
                
                -- FALLBACK: Just shield someone
                { command = "/cast [help][target=player] Power Word: Shield", conditions = "true" },
            },
            aoe = {},
            steps = {}
        },
        ["Standard"] = {
            type = "Priority",
            -- STANDARD MODE: Mouseover + Target healing (100% ToS safe, like VuhDo)
            st = {
                -- CRITICAL: Player is dying
                { command = "/cast [target=player] Desperate Prayer", conditions = "health < 20" },
                { command = "/cast [target=player] Power Word: Shield", conditions = "health < 30" },
                { command = "/cast [target=player] Penance", conditions = "health < 40" },
                
                -- EMERGENCY: Someone very low (mouseover OR target)
                { command = "/cast [target=mouseover,help,nodead][help] Power Word: Shield", conditions = "target_health < 40 or lowest_ally_health < 40" },
                { command = "/cast [target=mouseover,help,nodead][help] Penance", conditions = "target_health < 50 or lowest_ally_health < 50" },
                
                -- AOE HEALING: 3+ people need heals
                { command = "/cast Power Word: Radiance", conditions = "allies_below_health:80 >= 3" },
                { command = "/cast [target=player] Power Word: Radiance", conditions = "allies_below_health:70 >= 5" },
                
                -- DISPEL
                { command = "/cast [target=mouseover,help,nodead][help] Purify", conditions = "needs_dispel" },
                
                -- SMART SINGLE TARGET (mouseover first, then target, then self)
                { command = "/cast [target=mouseover,help,nodead][help][target=player] Power Word: Shield", conditions = "true" },
                { command = "/cast [target=mouseover,help,nodead][help][target=player] Shadow Mend", conditions = "true" },
                { command = "/cast [target=mouseover,help,nodead][help][target=player] Flash Heal", conditions = "true" },
                
                -- DPS FILLER: Only if everyone healthy
                { command = "/cast [harm] Shadow Word: Pain", conditions = "lowest_ally_health > 90" },
                { command = "/cast [harm] Smite", conditions = "lowest_ally_health > 90" },
            },
            aoe = {},
        }
    },
    ["Midnight"] = {
        type = "Priority",
        st = {
            { command = "/cast Power Word: Shield", conditions = "can_cast:Power Word: Shield" },
            { command = "/cast Penance", conditions = "can_cast:Penance" },
            { command = "/cast Shadow Mend", conditions = "can_cast:Shadow Mend" },
            { command = "/cast Purge the Wicked", conditions = "can_cast:Purge the Wicked" },
            { command = "/cast Smite", conditions = "true" },
        },
        aoe = {
            { command = "/cast Power Word: Radiance", conditions = "can_cast:Power Word: Radiance" },
            { command = "/cast Purge the Wicked", conditions = "can_cast:Purge the Wicked" },
            { command = "/cast Shadow Covenant", conditions = "can_cast:Shadow Covenant" },
            { command = "/cast Halo", conditions = "can_cast:Halo" },
            { command = "/cast Divine Star", conditions = "can_cast:Divine Star" },
            { command = "/cast Holy Nova", conditions = "true" },
        },
        steps = {}
    }
}

SkillWeaver.Sequences[PRIEST_HOLY] = {
    ["Raid"] = {
        ["Enhanced"] = {
            type = "Priority",
            st = {
                -- CRITICAL: Player dying
                { command = "/cast [target=player] Guardian Spirit", conditions = "health < 20" },
                { command = "/cast [target=player] Flash Heal", conditions = "health < 30" },
                { command = "/cast [target=player] Divine Hymn", conditions = "health < 25 and allies_below_health:50 >= 4" },
                
                -- AUTO-TARGET lowest
                { command = "/run SkillWeaver.HealingHelper:SetSmartHealTarget()", conditions = "lowest_ally_health < 70" },
                
                -- EMERGENCY healing
                { command = "/cast [help] Holy Word: Serenity", conditions = "target_health < 50" },
                { command = "/cast [help] Flash Heal", conditions = "target_health < 60" },
                
                -- AOE: Multiple people low
                { command = "/cast [@player] Holy Word: Sanctify", conditions = "allies_below_health:75 >= 3" },
                { command = "/cast Circle of Healing", conditions = "allies_below_health:80 >= 4" },
                { command = "/cast Prayer of Healing", conditions = "allies_below_health:70 >= 3" },
                
                -- DISPEL
                { command = "/cast [help] Purify Disease", conditions = "needs_dispel" },
                
                -- SMART ST
                { command = "/cast [help] Renew", conditions = "target_health < 95" },
                { command = "/cast [help] Heal", conditions = "target_health < 85" },
                { command = "/cast [help] Prayer of Mending", conditions = "target_health < 90" },
                
                -- DPS: Everyone healthy
                { command = "/cast [harm] Holy Fire", conditions = "lowest_ally_health > 90" },
                { command = "/cast [harm] Smite", conditions = "lowest_ally_health > 90" },
                
                -- FALLBACK
                { command = "/cast [help][target=player] Heal", conditions = "true" },
            },
            aoe = {},
            steps = {}
        },
        ["Standard"] = {
            type = "Priority",
            -- STANDARD MODE: Mouseover + Target healing (100% ToS safe, like VuhDo)
            st = {
                -- CRITICAL: Player dying
                { command = "/cast [target=player] Guardian Spirit", conditions = "health < 20" },
                { command = "/cast [target=player] Flash Heal", conditions = "health < 30" },
                { command = "/cast [target=player] Divine Hymn", conditions = "health < 25 and allies_below_health:50 >= 4" },
                
                -- EMERGENCY healing (mouseover OR target)
                { command = "/cast [target=mouseover,help,nodead][help] Holy Word: Serenity", conditions = "target_health < 50 or lowest_ally_health < 50" },
                { command = "/cast [target=mouseover,help,nodead][help] Flash Heal", conditions = "target_health < 60 or lowest_ally_health < 60" },
                
                -- AOE: Multiple people low
                { command = "/cast Holy Word: Sanctify", conditions = "allies_below_health:75 >= 3" },
                { command = "/cast Circle of Healing", conditions = "allies_below_health:80 >= 4" },
                { command = "/cast Prayer of Healing", conditions = "allies_below_health:70 >= 3" },
                
                -- DISPEL
                { command = "/cast [target=mouseover,help,nodead][help] Purify Disease", conditions = "needs_dispel" },
                
                -- SMART ST (mouseover first, then target, then self)
                { command = "/cast [target=mouseover,help,nodead][help][target=player] Renew", conditions = "true" },
                { command = "/cast [target=mouseover,help,nodead][help][target=player] Heal", conditions = "true" },
                { command = "/cast [target=mouseover,help,nodead][help][target=player] Prayer of Mending", conditions = "true" },
                
                -- DPS: Everyone healthy
                { command = "/cast [harm] Holy Fire", conditions = "lowest_ally_health > 90" },
                { command = "/cast [harm] Smite", conditions = "lowest_ally_health > 90" },
            },
            aoe = {},
            steps = {}
        }
    },
    ["Midnight"] = {
        type = "Priority",
        st = {
            { command = "/cast Holy Word: Serenity", conditions = "can_cast:Holy Word: Serenity" },
            { command = "/cast Holy Word: Sanctify", conditions = "can_cast:Holy Word: Sanctify" },
            { command = "/cast Circle of Healing", conditions = "can_cast:Circle of Healing" },
            { command = "/cast Flash Heal", conditions = "can_cast:Flash Heal" },
            { command = "/cast Heal", conditions = "true" },
            { command = "/cast Holy Fire", conditions = "can_cast:Holy Fire" },
            { command = "/cast Smite", conditions = "true" },
        },
        aoe = {
            { command = "/cast Holy Word: Sanctify", conditions = "can_cast:Holy Word: Sanctify" },
            { command = "/cast Circle of Healing", conditions = "can_cast:Circle of Healing" },
            { command = "/cast Prayer of Healing", conditions = "can_cast:Prayer of Healing" },
            { command = "/cast Holy Nova", conditions = "true" },
        },
        steps = {}
    }
}

SkillWeaver.Sequences[PRIEST_SHADOW] = {
    ["Raid"] = {
        ["Balanced"] = { -- Default
            type = "Priority",
            st = {
                { command = "/cast [harm] Silence", conditions = "should_interrupt" },
                { command = "/cast [target=player] Dispersion", conditions = "health < 30" },
                { command = "/cast [target=player] Vampiric Embrace", conditions = "health < 50" },
                { command = "/cast [harm] Void Eruption", conditions = "true" },
                { command = "/cast [harm] Devouring Plague", conditions = "insanity >= 50" },
                { command = "/cast [harm] Mind Blast", conditions = "true" },
                { command = "/cast [harm] Shadow Word: Death", conditions = "target_health < 20" },
                { command = "/cast [harm] Vampiric Touch", conditions = "buff:Vampiric Touch < 5" },
                { command = "/cast [harm] Shadow Word: Pain", conditions = "buff:Shadow Word: Pain < 5" },
                { command = "/cast [harm] Mind Flay", conditions = "true" },
            },
            aoe = {
                { command = "/cast [harm] Shadow Crash", conditions = "true" },
                { command = "/cast [harm] Mind Sear", conditions = "true" },
                { command = "/cast [harm] Vampiric Touch", conditions = "true" },
            },
            steps = {}
        },
        ["Archon"] = { -- Single Target / Halo/Dark Ascension Focus
            type = "Priority",
            st = {
                -- Priority 1: SURVIVAL & UTILITY
                { command = "/cast Silence", conditions = "should_interrupt and range <= 30" }, -- Interrupt
                { command = "/cast Psychic Horror", conditions = "should_interrupt and cooldown:Silence > 0 and talent(Psychic Horror) and range <= 30" }, -- Backup interrupt
                { command = "/cast [target=player] Dispel Magic", conditions = "debuff_type == magic and dispellable" }, -- Self-dispel
                { command = "/cast Fade", conditions = "in_group and threat > 85 and in_combat" }, -- Threat drop
                { command = "/cast [target=mouseover,help,nodead][help] Flash Heal", conditions = "in_group and ally_health < 15 and range <= 40" }, -- Emergency ally heal
                { command = "/cast Dispersion", conditions = "health < 30" }, -- Major defensive
                { command = "/cast [target=player] Vampiric Embrace", conditions = "health < 50" }, -- Self-heal (50% leech)
                { command = "/cast [target=player] Power Word: Shield", conditions = "health < 40 and not buff:Power Word: Shield" }, -- Absorb
                { command = "/cast [target=player] Flash Heal", conditions = "health < 35" }, -- Emergency self-heal
                
                -- Cooldowns
                { command = "/cast Dark Ascension", conditions = "cooldown:Mind Blast < 2 or buff:Mind Devourer" }, -- With Mind Blast ready
                { command = "/cast Void Eruption", conditions = "insanity >= 90 and not buff:Voidform" }, -- Enter Voidform
                { command = "/cast Mindbender", conditions = "talent(Mindbender)" },
                { command = "/cast Shadowfiend", conditions = "not talent(Mindbender)" },
                
                -- Insanity Management (Dump at >= 85 to avoid cap)
                { command = "/cast Devouring Plague", conditions = "buff:Voidform and dot:Devouring Plague < 2 and range <= 40" }, -- Maintain during Voidform
                { command = "/cast Devouring Plague", conditions = "insanity >= 85 and range <= 40" }, -- Dump before cap (deficit <= 35)
                { command = "/cast Devouring Plague", conditions = "buff:Mind Devourer and range <= 40" }, -- With proc
                { command = "/cast Devouring Plague", conditions = "buff:Entropic Rift and range <= 40" }, -- With Archon buff
                { command = "/cast Devouring Plague", conditions = "buff:Power Surge and range <= 40" }, -- With Surge buff
                { command = "/cast Devouring Plague", conditions = "dot:Devouring Plague < 2 and insanity >= 50 and range <= 40" }, -- Refresh expiring
                
                -- Void Blast Priority (Archon ability)
                { command = "/cast Void Blast", conditions = "dot:Devouring Plague > 2 and insanity < 104 and range <= 40" }, -- DP has time, won't cap
                
                -- DoT Maintenance
                { command = "/cast Shadow Crash", conditions = "dot:Vampiric Touch < 5 and talent(Shadow Crash) and range <= 40" }, -- Refresh VT via crash
                { command = "/cast Vampiric Touch", conditions = "dot:Vampiric Touch < 5 and target_ttd > 12 and range <= 40" }, -- Refresh on long-lived targets
                { command = "/cast Shadow Word: Pain", conditions = "dot:Shadow Word: Pain < 5 and range <= 40" },
                
                -- Mind Blast Priority (Skip if Mind Devourer active to save for free DP)
                { command = "/cast Mind Blast", conditions = "not buff:Mind Devourer and range <= 40" },
                
                -- Fillers
                { command = "/cast Mind Flay: Insanity", conditions = "buff:Mind Flay: Insanity and range <= 40" }, -- Channeling proc
                { command = "/cast Mind Spike", conditions = "talent(Mind Spike) and range <= 40" },
                { command = "/cast Mind Flay", conditions = "range <= 40" },
            },
            aoe = {
                { command = "/cast Silence", conditions = "should_interrupt and range <= 30" },
                { command = "/cast Fade", conditions = "in_group and enemies_nearby >= 4" }, -- DR in AoE
                { command = "/cast Vampiric Embrace", conditions = "health < 60 and enemies_nearby >= 3" },
                { command = "/cast Mind Sear", conditions = "enemies >= 3 and range <= 40" },
                { command = "/cast Shadow Crash", conditions = "enemies >= 2 and range <= 40" },
                { command = "/cast Devouring Plague", conditions = "insanity >= 85 and range <= 40" },
                { command = "/cast Void Bolt", conditions = "buff:Voidform and range <= 40" },
                { command = "/cast Shadow Word: Pain", conditions = "dot:Shadow Word: Pain < 5 and enemies < 5 and range <= 40" },
            },
            steps = {}
        },
        ["Voidweaver"] = { -- Burst / Void Torrent Focus
            type = "Priority",
            st = {
                { command = "/cast [harm] Void Torrent", conditions = "true" },
                { command = "/cast [harm] Devouring Plague", conditions = "insanity >= 50" },
                { command = "/cast [harm] Entropic Rift", conditions = "talent(Entropic Rift)" }, -- Voidweaver proc/ability
                { command = "/cast [harm] Void Blast", conditions = "cooldown:Mind Blast == 0" },
                { command = "/cast [harm] Mind Blast", conditions = "true" },
                { command = "/cast [harm] Shadow Crash", conditions = "true" },
                { command = "/cast [harm] Shadow Word: Death", conditions = "target_health < 20" },
                { command = "/cast [harm] Vampiric Touch", conditions = "buff:Vampiric Touch < 5" },
                { command = "/cast [harm] Shadow Word: Pain", conditions = "buff:Shadow Word: Pain < 5" },
            },
            aoe = {
                { command = "/cast [harm] Shadow Crash", conditions = "true" },
                { command = "/cast [harm] Void Torrent", conditions = "true" },
                { command = "/cast [harm] Devouring Plague", conditions = "insanity >= 50" },
                { command = "/cast [harm] Entropic Rift", conditions = "true" },
                { command = "/cast [harm] Psychic Link", conditions = "true" },
            },
            steps = {}
        }
    },
    ["Midnight"] = {
        type = "Priority",
        st = {
            -- Multi-DoT: Cycle if Vampiric Touch is up
            { command = "/cycle", conditions = "debuff:Vampiric Touch" },
            
            -- Hero Talents & Cooldowns
            { command = "/cast Void Eruption", conditions = "can_cast:Void Eruption" },
            { command = "/cast Dark Ascension", conditions = "can_cast:Dark Ascension" },
            { command = "/cast Void Torrent", conditions = "can_cast:Void Torrent" },
            { command = "/cast Shadow Crash", conditions = "can_cast:Shadow Crash" },
            { command = "/cast Mindgames", conditions = "can_cast:Mindgames" },
            { command = "/cast Halo", conditions = "can_cast:Halo" },
            { command = "/cast Divine Star", conditions = "can_cast:Divine Star" },
            
            -- Spenders & Generators
            { command = "/cast Devouring Plague", conditions = "can_cast:Devouring Plague" },
            { command = "/cast Mind Blast", conditions = "can_cast:Mind Blast" },
            { command = "/cast Shadow Word: Death", conditions = "can_cast:Shadow Word: Death" },
            { command = "/cast Vampiric Touch", conditions = "can_cast:Vampiric Touch" },
            { command = "/cast Shadow Word: Pain", conditions = "can_cast:Shadow Word: Pain" },
            { command = "/cast Mind Flay: Insanity", conditions = "can_cast:Mind Flay: Insanity" }, -- Proc
            { command = "/cast Mind Flay", conditions = "true" },
            { command = "/cast Mind Spike", conditions = "can_cast:Mind Spike" }, -- Alt filler
        },
        aoe = {},
        steps = {}
    }
}
