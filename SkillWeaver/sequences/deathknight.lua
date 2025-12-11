--========================================================--
-- SkillWeaver - Death Knight Sequences (Blood, Frost, Unholy)
-- Advanced B-1 Logic (Clean + Optimized)
--========================================================--

local data = {}

------------------------------------------------------------
-- BLOOD DK (Spec ID 250)
------------------------------------------------------------
data["DEATHKNIGHT_250"] = {

    MythicPlus = {
        Balanced = {
            steps = {
                { command="/cast Death Strike",       conditions="player:health<60" },
                { command="/cast Marrowrend",         conditions="buff:Bone Shield_stacks<6" },
                { command="/cast Blood Boil" },
                { command="/cast Heart Strike" },
                { command="/cast Death and Decay",     conditions="active_enemies>=3" },
                { command="/cast Rune Tap",            conditions="player:health<40" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Dancing Rune Weapon", conditions="cooldown:Dancing Rune Weapon==0" },
                { command="/cast Tombstone",           conditions="buff:Bone Shield_stacks>=5" },
                { command="/cast Blood Boil" },
                { command="/cast Marrowrend",          conditions="buff:Bone Shield_stacks<6" },
                { command="/cast Heart Strike" },
                { command="/cast Death and Decay",     conditions="active_enemies>=3" },
                { command="/cast Death Strike",        conditions="player:health<70 or runic_power>80" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Marrowrend" },
                { command="/cast Heart Strike" },
                { command="/cast Death Strike" },
            }
        }
    },

    Raid = {
        Balanced = {
            steps = {
                { command="/cast Marrowrend",          conditions="buff:Bone Shield_stacks<6" },
                { command="/cast Heart Strike" },
                { command="/cast Blood Boil" },
                { command="/cast Death Strike",        conditions="player:health<55" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Dancing Rune Weapon" },
                { command="/cast Blood Boil" },
                { command="/cast Marrowrend",          conditions="buff:Bone Shield_stacks<6" },
                { command="/cast Heart Strike" },
                { command="/cast Death Strike",        conditions="player:health<70" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Heart Strike" },
                { command="/cast Marrowrend" },
                { command="/cast Death Strike" },
            }
        }
    },

    Delves = {
        Balanced = {
            steps = {
                { command="/cast Icebound Fortitude",  conditions="player:health<30" },
                { command="/cast Vampiric Blood",      conditions="player:health<45" },
                { command="/cast Marrowrend",          conditions="buff:Bone Shield_stacks<6" },
                { command="/cast Blood Boil" },
                { command="/cast Heart Strike" },
                { command="/cast Death Strike",        conditions="player:health<65" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Vampiric Blood" },
                { command="/cast Dancing Rune Weapon" },
                { command="/cast Heart Strike" },
                { command="/cast Blood Boil" },
                { command="/cast Death Strike",        conditions="player:health<75" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Marrowrend" },
                { command="/cast Heart Strike" },
                { command="/cast Death Strike" },
            }
        }
    },

    PvP = {
        Balanced = {
            steps = {
                { command="/cast Death Grip",          conditions="target:distance>10" },
                { command="/cast Icebound Fortitude",  conditions="player:stunned" },
                { command="/cast Chains of Ice" },
                { command="/cast Heart Strike" },
                { command="/cast Death Strike",        conditions="player:health<65" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Dark Command" },
                { command="/cast Strangulate" },
                { command="/cast Heart Strike" },
                { command="/cast Blood Boil" },
                { command="/cast Death Strike",        conditions="player:health<70" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Heart Strike" },
                { command="/cast Marrowrend" },
                { command="/cast Death Strike" },
            }
        }
    },
    Midnight = {
        type = "Priority",
        st = {
            -- Cooldowns & Talents
            { command = "/cast Abomination Limb", conditions = "can_cast:Abomination Limb" },
            { command = "/cast Bonestorm", conditions = "can_cast:Bonestorm" },
            { command = "/cast Consumption", conditions = "can_cast:Consumption" },
            { command = "/cast Blooddrinker", conditions = "can_cast:Blooddrinker" },
            { command = "/cast Dancing Rune Weapon", conditions = "can_cast:Dancing Rune Weapon" },
            { command = "/cast Tombstone", conditions = "can_cast:Tombstone" },
            
            -- Core Rotation
            { command = "/cast Marrowrend", conditions = "can_cast:Marrowrend" },
            { command = "/cast Death Strike", conditions = "can_cast:Death Strike" },
            { command = "/cast Blood Boil", conditions = "can_cast:Blood Boil" },
            { command = "/cast Heart Strike", conditions = "true" },
        },
        aoe = {},
        steps = {}
    }
}

------------------------------------------------------------
-- FROST DK (Spec ID 251)
------------------------------------------------------------
data["DEATHKNIGHT_251"] = {

    MythicPlus = {
        Balanced = {
            steps = {
                { command="/cast Pillar of Frost" },
                { command="/cast Remorseless Winter" },
                { command="/cast Howling Blast",     conditions="buff:Rime" },
                { command="/cast Obliterate" },
                { command="/cast Frost Strike",      conditions="runic_power>70" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Pillar of Frost" },
                { command="/cast Empower Rune Weapon", conditions="cooldown:Empower Rune Weapon==0" },
                { command="/cast Remorseless Winter" },
                { command="/cast Frostwyrm's Fury",    conditions="cooldown:Frostwyrm's Fury==0" },
                { command="/cast Howling Blast",       conditions="buff:Rime" },
                { command="/cast Obliterate",          conditions="buff:Killing Machine" },
                { command="/cast Obliterate" },
                { command="/cast Frost Strike",        conditions="runic_power>60" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Obliterate" },
                { command="/cast Howling Blast" },
                { command="/cast Frost Strike" },
            }
        }
    },

    Raid = {
        Balanced = {
            steps = {
                { command="/cast Pillar of Frost" },
                { command="/cast Remorseless Winter" },
                { command="/cast Obliterate" },
                { command="/cast Howling Blast",   conditions="buff:Rime" },
                { command="/cast Frost Strike",    conditions="runic_power>70" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Pillar of Frost" },
                { command="/cast Empower Rune Weapon" },
                { command="/cast Remorseless Winter" },
                { command="/cast Howling Blast",      conditions="buff:Rime" },
                { command="/cast Obliterate",         conditions="buff:Killing Machine" },
                { command="/cast Obliterate" },
                { command="/cast Frost Strike",       conditions="runic_power>65" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Obliterate" },
                { command="/cast Howling Blast" },
            }
        }
    },

    Delves = {
        Balanced = {
            steps = {
                { command="/cast Icebound Fortitude", conditions="player:health<30" },
                { command="/cast Remorseless Winter" },
                { command="/cast Howling Blast",     conditions="buff:Rime" },
                { command="/cast Obliterate" },
                { command="/cast Frost Strike",      conditions="runic_power>70" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Pillar of Frost" },
                { command="/cast Remorseless Winter" },
                { command="/cast Obliterate" },
                { command="/cast Howling Blast",     conditions="buff:Rime" },
                { command="/cast Frost Strike",      conditions="runic_power>60" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Obliterate" },
                { command="/cast Howling Blast" },
            }
        }
    },

    PvP = {
        Balanced = {
            steps = {
                { command="/cast Chains of Ice" },
                { command="/cast Strangulate" },
                { command="/cast Remorseless Winter" },
                { command="/cast Howling Blast",     conditions="buff:Rime" },
                { command="/cast Obliterate" },
                { command="/cast Frost Strike",      conditions="runic_power>70" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Pillar of Frost" },
                { command="/cast Remorseless Winter" },
                { command="/cast Obliterate" },
                { command="/cast Howling Blast",     conditions="buff:Rime" },
                { command="/cast Chains of Ice" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Obliterate" },
                { command="/cast Frost Strike" },
            }
        }
    },
    Midnight = {
        type = "Priority",
        st = {
            { command = "/cast Pillar of Frost", conditions = "can_cast:Pillar of Frost" },
            { command = "/cast Remorseless Winter", conditions = "can_cast:Remorseless Winter" },
            { command = "/cast Howling Blast", conditions = "can_cast:Howling Blast" },
            { command = "/cast Obliterate", conditions = "can_cast:Obliterate" },
            { command = "/cast Frost Strike", conditions = "can_cast:Frost Strike" },
        },
        aoe = {},
        steps = {}
    }
}

------------------------------------------------------------
-- UNHOLY DK (Spec ID 252)
------------------------------------------------------------
data["DEATHKNIGHT_252"] = {

    MythicPlus = {
        Balanced = { -- Default
            steps = {
                { command="/cast Outbreak",           conditions="not debuff:Virulent Plague" },
                { command="/cast Dark Transformation" },
                { command="/cast Apocalypse",         conditions="wounds>=4" },
                { command="/cast Death Coil",        conditions="runic_power>80" },
                { command="/cast Scourge Strike" },
                { command="/cast Festering Strike",  conditions="wounds<3" },
            }
        },

        ["San'layn"] = { -- Single Target / Vampiric Strike Focus
            type = "Priority",
            st = {
                -- Pet Management
                { command = "/cast Raise Dead", conditions = "not pet_exists and not in_combat" },
                { command = "/petattack", conditions = "pet_exists and target_attackable and not pet_attacking" },
                
                -- Priority 1: SURVIVAL & UTILITY
                { command = "/cast Mind Freeze", conditions = "should_interrupt and range <= 15" },
                { command = "/cast [pet] Gnaw", conditions = "should_interrupt and cooldown:Mind Freeze > 0 and pet_exists and range <= 30" }, -- Pet stun interrupt
                { command = "/cast Asphyxiate", conditions = "should_interrupt and cooldown:Mind Freeze > 0 and cooldown:Gnaw > 0 and range <= 30" },
                { command = "/cast Icebound Fortitude", conditions = "health < 35" },
                { command = "/cast Anti-Magic Shell", conditions = "health < 50 and magic_damage_incoming" },
                { command = "/cast Death Strike", conditions = "health < 60 and runic_power >= 45" },
                { command = "/cast Death Pact", conditions = "health < 40 and talent(Death Pact)" },
                
                -- Cooldowns
                { command = "/cast Unholy Assault", conditions = "true" },
                { command = "/cast Dark Transformation", conditions = "pet_exists and range <= 30" },
                { command = "/cast Apocalypse", conditions = "debuff:Festering Wound >= 4 and range <= 15" },
                { command = "/cast Summon Gargoyle", conditions = "talent(Summon Gargoyle) and range <= 30" },
                { command = "/cast Soul Reaper", conditions = "target_health < 35 and range <= 8" },
                
                -- San'layn: Vampiric Strike focus
                { command = "/cast Scourge Strike", conditions = "buff:Vampiric Strike and range <= 8" }, -- Becomes Vampiric Strike with buff
                { command = "/cast Festering Strike", conditions = "debuff:Festering Wound < 4 and range <= 8" },
                { command = "/cast Scourge Strike", conditions = "debuff:Festering Wound >= 1 and range <= 8" },
                { command = "/cast Death Coil", conditions = "runic_power >= 60 and range <= 30" },
                { command = "/cast Epidemic", conditions = "runic_power >= 40 and enemies >= 2 and range <= 30" },
            },
            aoe = {
                { command = "/cast Mind Freeze", conditions = "should_interrupt and range <= 15" },
                { command = "/cast [pet] Gnaw", conditions = "should_interrupt and cooldown:Mind Freeze > 0 and pet_exists" },
                { command = "/cast Icebound Fortitude", conditions = "health < 40 or enemies_nearby >= 5" },
                { command = "/cast Death and Decay", conditions = "range <= 30" },
                { command = "/cast Apocalypse", conditions = "debuff:Festering Wound >= 4 and range <= 15" },
                { command = "/cast Epidemic", conditions = "runic_power >= 40 and range <= 30" },
                { command = "/cast Festering Strike", conditions = "debuff:Festering Wound < 4 and range <= 8" },
                { command = "/cast Scourge Strike", conditions = "range <= 8" },
            },
            steps = {}
        },

        RiderOfTheApocalypse = { -- Mounted / Horsemen Focus
            steps = {
                { command="/cast Army of the Dead" },
                { command="/cast Abomination Limb",   conditions="true" },
                { command="/cast Apocalypse",         conditions="wounds>=4" }, -- Summons Horsemen
                { command="/cast Dark Transformation" },
                { command="/cast Soul Reaper",        conditions="target_health<35" },
                { command="/cast Death Charge",       conditions="moving" }, -- Mobility
                { command="/cast Death Coil",         conditions="runic_power>80" },
                { command="/cast Scourge Strike",     conditions="wounds>=1" },
                { command="/cast Festering Strike",   conditions="wounds<2" },
            }
        }
    },

    Raid = {
        Balanced = {
            steps = {
                { command="/cast Outbreak" },
                { command="/cast Dark Transformation" },
                { command="/cast Apocalypse",          conditions="wounds>=4" },
                { command="/cast Soul Reaper",         conditions="target_health<35" },
                { command="/cast Death Coil",          conditions="runic_power>80" },
                { command="/cast Scourge Strike" },
                { command="/cast Festering Strike",    conditions="wounds<2" },
            }
        },

        Sanlayn = {
            steps = {
                { command="/cast Abomination Limb",    conditions="true" },
                { command="/cast Dark Transformation" },
                { command="/cast Apocalypse",          conditions="wounds>=4" },
                { command="/cast Soul Reaper",         conditions="target_health<35" },
                { command="/cast Vampiric Strike",     conditions="wounds>=1" },
                { command="/cast Death Coil",          conditions="runic_power>70" },
                { command="/cast Festering Strike",    conditions="wounds<2" },
            }
        },

        RiderOfTheApocalypse = {
            steps = {
                { command="/cast Army of the Dead" },
                { command="/cast Abomination Limb",    conditions="true" },
                { command="/cast Apocalypse",          conditions="wounds>=4" },
                { command="/cast Dark Transformation" },
                { command="/cast Soul Reaper",         conditions="target_health<35" },
                { command="/cast Death Coil",          conditions="runic_power>80" },
                { command="/cast Scourge Strike",      conditions="wounds>=1" },
            }
        }
    },
    Midnight = {
        type = "Priority",
        st = {
            { command = "/cast Dark Transformation", conditions = "can_cast:Dark Transformation" },
            { command = "/cast Apocalypse", conditions = "can_cast:Apocalypse" },
            { command = "/cast Unholy Assault", conditions = "can_cast:Unholy Assault" },
            { command = "/cast Outbreak", conditions = "can_cast:Outbreak" },
            { command = "/cast Festering Strike", conditions = "can_cast:Festering Strike" },
            { command = "/cast Scourge Strike", conditions = "can_cast:Scourge Strike" },
            { command = "/cast Death Coil", conditions = "can_cast:Death Coil" },
        },
        aoe = {},
        steps = {}
    }
}

------------------------------------------------------------
-- Return DK Data
------------------------------------------------------------
return data
