--========================================================--
-- SkillWeaver - Hunter Sequences (BM, MM, SV)
-- Advanced B-1 Logic (Clean + Optimized)
--========================================================--

local data = {}

------------------------------------------------------------
-- BEAST MASTERY HUNTER (Spec ID 253)
------------------------------------------------------------
data["HUNTER_253"] = {

    --------------------------------------------------------
    -- Mythic+
    --------------------------------------------------------
    MythicPlus = {
        Balanced = {
            steps = {
                -- Pet Management (CRITICAL)
                { command="/cast Call Pet 1",          conditions="not pet:exists and not in_combat" },
                { command="/cast Revive Pet",          conditions="pet:dead and not in_combat" },
                { command="/petattack",                conditions="pet:exists and target:attackable and not pet:attacking" },
               { command="/cast Mend Pet",            conditions="pet:exists and pet:health<60 and not buff:Mend Pet" },
                { command="/cast [pet] Growl",         conditions="pet:exists and not in_group and not pet:buff:Growl" }, -- Enable solo
                { command="/cast [pet] Growl",         conditions="pet:exists and in_group and pet:buff:Growl" }, -- Disable group
                
                -- Misdirection (Context-Aware)
                { command="/cast [target=focus] Misdirection", conditions="in_group and focus:role==tank and pull_timer<1" },
                { command="/cast [target=pet] Misdirection", conditions="not in_group and pet:exists and pull_timer<1" },
                { command="/cast [target=focus] Misdirection", conditions="in_group and focus:role==tank and threat>70" },
                
                -- Survival & Utility
                { command="/cast Counter Shot",        conditions="should_interrupt" },
                { command="/cast Intimidation",        conditions="should_stun and talent(Intimidation)" }, -- Pet Stun
                { command="/cast Tranquilizing Shot",  conditions="target:buff_type==magic or target:buff_type==enrage" },
                { command="/cast Tranquilizing Shot",  conditions="target:buff_type==magic or target:buff_type==enrage" },
                { command="/cast [target=player] Master's Call", conditions="rooted or snared" },
                { command="/cast [target=mouseover,help,nodead] Master's Call", conditions="in_group and ally_rooted" },
                { command="/cast Fortitude of the Bear", conditions="health<20" }, -- Tenacity Defensive
                { command="/cast Aspect of the Turtle", conditions="player:health<30" },
                { command="/cast Exhilaration",        conditions="player:health<40" },
                { command="/cast Feign Death",         conditions="in_group and threat>90" },
                { command="/cast [pet] Primal Rage",   conditions="pet:spec==Ferocity and in_group and heroism_needed" },
                { command="/cast [target=player] Spirit Mend", conditions="player:health<35 and pet:family==Spirit Beast" },
                { command="/cast [target=player] Spirit Mend", conditions="player:health<35 and pet:family==Spirit Beast" },
                { command="/cast [target=mouseover,help,nodead] Spirit Mend", conditions="in_group and ally_health<20 and pet:family==Spirit Beast" },
                
                -- Family Specific Abilities (The "Core 7")
                { command="/cast Defense",             conditions="pet:health<40" }, -- Beetle/Turtle/Crab
                { command="/cast Dodge",               conditions="pet:health<40" }, -- Cat/Monkey/Fox
                { command="/cast Magic Defense",       conditions="pet:health<40 or incoming_magic_damage" }, -- Ray/Toad
                { command="/cast Triggered Defense",   conditions="pet:health<40" }, -- Clefthoof/Scalehide (Passive-ish but good to force)
                { command="/cast Mortal Wounds",       conditions="target:health<100" }, -- Ensure applied
                { command="/cast Slow",                conditions="target:moving and not target:snared" }, -- PvP/Kiting
                { command="/cast Dispel",              conditions="target:buff_type==magic or target:buff_type==enrage" }, -- Pet Purge
                
                -- DPS Rotation
                { command="/cast Bestial Wrath",       conditions="cooldown:Bestial Wrath==0" },
                { command="/cast Call of the Wild",    conditions="cooldown:Call of the Wild==0" },
                { command="/cast Barbed Shot",         conditions="buff:Frenzy<3 or buff:Frenzy_remains<2" },
                { command="/cast Kill Command" },
                { command="/cast Multi-Shot",          conditions="active_enemies>=3" },
                { command="/cast Kill Shot",           conditions="target:health<20" },
                { command="/cast Cobra Shot",          conditions="focus>60" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Aspect of the Wild",  conditions="cooldown:Aspect of the Wild==0" },
                { command="/cast Bestial Wrath" },
                { command="/cast Bloodshed",           conditions="cooldown:Bloodshed==0" },
                { command="/cast Barbed Shot",         conditions="buff:Frenzy<3 or buff:Frenzy_remains<2" },
                { command="/cast Kill Command" },
                { command="/cast Multi-Shot",          conditions="active_enemies>=3" },
                { command="/cast Kill Shot",           conditions="target:health<20" },
                { command="/cast Cobra Shot",          conditions="focus>45" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Kill Command" },
                { command="/cast Barbed Shot" },
                { command="/cast Cobra Shot" },
            }
        }
    },

    --------------------------------------------------------
    -- Raid
    --------------------------------------------------------
    Raid = {
        Balanced = {
            steps = {
                { command="/cast Call of the Wild" },
                { command="/cast Bestial Wrath" },
                { command="/cast Barbed Shot",         conditions="buff:Frenzy<3" },
                { command="/cast Kill Command" },
                { command="/cast Kill Shot",           conditions="target:health<20" },
                { command="/cast Cobra Shot",          conditions="focus>60" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Bloodshed" },
                { command="/cast Aspect of the Wild" },
                { command="/cast Bestial Wrath" },
                { command="/cast Barbed Shot" },
                { command="/cast Kill Command" },
                { command="/cast Dire Beast",          conditions="cooldown:Dire Beast==0" },
                { command="/cast Kill Shot",           conditions="target:health<20" },
                { command="/cast Cobra Shot",          conditions="focus>50" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Kill Command" },
                { command="/cast Barbed Shot" },
                { command="/cast Cobra Shot" },
            }
        }
    },

    --------------------------------------------------------
    -- Delves
    --------------------------------------------------------
    Delves = {
        Balanced = {
            steps = {
                { command="/cast Exhilaration",        conditions="player:health<40" },
                { command="/cast Bestial Wrath" },
                { command="/cast Barbed Shot" },
                { command="/cast Kill Command" },
                { command="/cast Cobra Shot",          conditions="focus>60" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Bloodshed" },
                { command="/cast Aspect of the Wild" },
                { command="/cast Bestial Wrath" },
                { command="/cast Kill Command" },
                { command="/cast Barbed Shot" },
                { command="/cast Cobra Shot",          conditions="focus>45" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Kill Command" },
                { command="/cast Barbed Shot" },
                { command="/cast Cobra Shot" },
            }
        }
    },

    --------------------------------------------------------
    -- PvP
    --------------------------------------------------------
    PvP = {
        Balanced = {
            steps = {
                { command="/cast Roar of Sacrifice",   conditions="player:health<50" },
                { command="/cast Intimidation" },
                { command="/cast Bestial Wrath" },
                { command="/cast Kill Command" },
                { command="/cast Barbed Shot" },
                { command="/cast Kill Shot",           conditions="target:health<20" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Intimidation" },
                { command="/cast Bestial Wrath" },
                { command="/cast Bloodshed" },
                { command="/cast Kill Command" },
                { command="/cast Barbed Shot" },
                { command="/cast Kill Shot",           conditions="target:health<20" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Kill Command" },
                { command="/cast Barbed Shot" },
                { command="/cast Cobra Shot" },
            }
        }
    }
}

------------------------------------------------------------
-- MARKSMANSHIP HUNTER (Spec ID 254)
------------------------------------------------------------
data["HUNTER_254"] = {

    --------------------------------------------------------
    -- Mythic+
    --------------------------------------------------------
    MythicPlus = {
        Balanced = {
            steps = {
                -- Pet Management
                { command="/cast Call Pet 1",          conditions="not pet:exists and not in_combat" },
                { command="/petattack",                conditions="pet:exists and target:attackable" },
                { command="/cast Mend Pet",            conditions="pet:exists and pet:health<60" },
                { command="/cast [pet] Growl",         conditions="pet:exists and not in_group and not pet:buff:Growl" },
                { command="/cast [pet] Growl",         conditions="pet:exists and in_group and pet:buff:Growl" },
                
                -- Misdirection
                { command="/cast [target=focus] Misdirection", conditions="in_group and focus:role==tank and pull_timer<1" },
                { command="/cast [target=pet] Misdirection", conditions="not in_group and pet:exists and pull_timer<1" },
                
                -- Survival & Utility
                -- Survival & Utility
                { command="/cast Counter Shot",        conditions="should_interrupt" },
                { command="/cast Intimidation",        conditions="should_stun and talent(Intimidation)" }, -- Pet Stun
                { command="/cast Tranquilizing Shot",  conditions="target:buff_type==magic or target:buff_type==enrage" },
                { command="/cast [target=player] Master's Call", conditions="rooted or snared" },
                { command="/cast [target=mouseover,help,nodead] Master's Call", conditions="in_group and ally_rooted" },
                { command="/cast Fortitude of the Bear", conditions="health<20" }, -- Tenacity Defensive
                { command="/cast Aspect of the Turtle", conditions="player:health<30" },
                { command="/cast Exhilaration",        conditions="player:health<40" },
                { command="/cast [pet] Primal Rage",   conditions="pet:spec==Ferocity and in_group and heroism_needed" },
                { command="/cast [target=player] Spirit Mend", conditions="player:health<35 and pet:family==Spirit Beast" },
                { command="/cast [target=player] Spirit Mend", conditions="player:health<35 and pet:family==Spirit Beast" },
                { command="/cast [target=mouseover,help,nodead] Spirit Mend", conditions="in_group and ally_health<20 and pet:family==Spirit Beast" },
                
                -- Family Specific Abilities
                { command="/cast Defense",             conditions="pet:health<40" },
                { command="/cast Dodge",               conditions="pet:health<40" },
                { command="/cast Magic Defense",       conditions="pet:health<40 or incoming_magic_damage" },
                { command="/cast Mortal Wounds",       conditions="target:health<100" },
                { command="/cast Dispel",              conditions="target:buff_type==magic or target:buff_type==enrage" },
                
                -- DPS Rotation
                { command="/cast Trueshot" },
                { command="/cast Salvo",               conditions="cooldown:Salvo==0" },
                { command="/cast Rapid Fire" },
                { command="/cast Aimed Shot" },
                { command="/cast Multi-Shot",          conditions="active_enemies>=3" },
                { command="/cast Kill Shot",           conditions="target:health<20" },
                { command="/cast Arcane Shot" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Trueshot" },
                { command="/cast Salvo" },
                { command="/cast Wailing Arrow",       conditions="cooldown:Wailing Arrow==0" },
                { command="/cast Rapid Fire" },
                { command="/cast Aimed Shot" },
                { command="/cast Kill Shot",           conditions="target:health<20 or buff:Deathblow" },
                { command="/cast Multi-Shot",          conditions="active_enemies>=3" },
                { command="/cast Arcane Shot",         conditions="focus>60" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Rapid Fire" },
                { command="/cast Aimed Shot" },
                { command="/cast Arcane Shot" },
            }
        }
    },


    --------------------------------------------------------
    -- Raid
    --------------------------------------------------------
    Raid = {
        Balanced = {
            steps = {
                { command="/cast Trueshot" },
                { command="/cast Rapid Fire" },
                { command="/cast Aimed Shot" },
                { command="/cast Kill Shot",           conditions="target:health<20" },
                { command="/cast Arcane Shot" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Trueshot" },
                { command="/cast Salvo" },
                { command="/cast Wailing Arrow" },
                { command="/cast Aimed Shot" },
                { command="/cast Rapid Fire" },
                { command="/cast Kill Shot",           conditions="target:health<20 or buff:Deathblow" },
                { command="/cast Arcane Shot",         conditions="focus>60" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Aimed Shot" },
                { command="/cast Rapid Fire" },
                { command="/cast Arcane Shot" },
            }
        }
    },


    --------------------------------------------------------
    -- Delves
    --------------------------------------------------------
    Delves = {
        Balanced = {
            steps = {
                { command="/cast Exhilaration",        conditions="player:health<40" },
                { command="/cast Trueshot" },
                { command="/cast Rapid Fire" },
                { command="/cast Aimed Shot" },
                { command="/cast Arcane Shot" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Trueshot" },
                { command="/cast Salvo" },
                { command="/cast Wailing Arrow" },
                { command="/cast Rapid Fire" },
                { command="/cast Aimed Shot" },
                { command="/cast Kill Shot",           conditions="target:health<20" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Aimed Shot" },
                { command="/cast Rapid Fire" },
                { command="/cast Arcane Shot" },
            }
        }
    },


    --------------------------------------------------------
    -- PvP
    --------------------------------------------------------
    PvP = {
        Balanced = {
            steps = {
                { command="/cast Counter Shot",         conditions="target:casting" },
                { command="/cast Scatter Shot" },
                { command="/cast Aimed Shot" },
                { command="/cast Rapid Fire" },
                { command="/cast Kill Shot",            conditions="target:health<20" },
                { command="/cast Arcane Shot" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Trueshot" },
                { command="/cast Rapid Fire" },
                { command="/cast Aimed Shot" },
                { command="/cast Kill Shot",            conditions="target:health<20 or buff:Deathblow" },
                { command="/cast Concussive Shot" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Aimed Shot" },
                { command="/cast Rapid Fire" },
                { command="/cast Arcane Shot" },
            }
        }
    }
}

------------------------------------------------------------
-- SURVIVAL HUNTER (Spec ID 255)
------------------------------------------------------------
data["HUNTER_255"] = {

    --------------------------------------------------------
    -- Mythic+
    --------------------------------------------------------
    MythicPlus = {
        Balanced = {
            steps = {
                -- Pet Management
                { command="/cast Call Pet 1",          conditions="not pet:exists and not in_combat" },
                { command="/petattack",                conditions="pet:exists and target:attackable" },
                { command="/cast Mend Pet",            conditions="pet:exists and pet:health<60" },
                { command="/cast [pet] Growl",         conditions="pet:exists and not in_group and not pet:buff:Growl" },
                { command="/cast [pet] Growl",         conditions="pet:exists and in_group and pet:buff:Growl" },
                
                -- Misdirection
                { command="/cast [target=focus] Misdirection", conditions="in_group and focus:role==tank and pull_timer<1" },
                { command="/cast [target=pet] Misdirection", conditions="not in_group and pet:exists and pull_timer<1" },
                
                -- Survival & Utility
                -- Survival & Utility
                { command="/cast Muzzle",              conditions="should_interrupt" }, -- Melee interrupt
                { command="/cast Intimidation",        conditions="should_stun and talent(Intimidation)" }, -- Pet Stun
                { command="/cast Tranquilizing Shot",  conditions="target:buff_type==magic or target:buff_type==enrage" },
                { command="/cast Tranquilizing Shot",  conditions="target:buff_type==magic or target:buff_type==enrage" },
                { command="/cast Fortitude of the Bear", conditions="health<20" }, -- Tenacity Defensive
                { command="/cast [target=player] Master's Call", conditions="rooted or snared" },
                { command="/cast [target=mouseover,help,nodead] Master's Call", conditions="in_group and ally_rooted" },
                { command="/cast Aspect of the Turtle", conditions="player:health<30" },
                { command="/cast Exhilaration",        conditions="player:health<40" },
                { command="/cast [pet] Primal Rage",   conditions="pet:spec==Ferocity and in_group and heroism_needed" },
                
                -- Family Specific Abilities
                { command="/cast Defense",             conditions="pet:health<40" },
                { command="/cast Dodge",               conditions="pet:health<40" },
                { command="/cast Magic Defense",       conditions="pet:health<40 or incoming_magic_damage" },
                { command="/cast Mortal Wounds",       conditions="target:health<100" },
                { command="/cast Slow",                conditions="target:moving and not target:snared" },
                { command="/cast Dispel",              conditions="target:buff_type==magic or target:buff_type==enrage" },
                
                -- DPS Rotation
                { command="/cast Coordinated Assault" },
                { command="/cast Wildfire Bomb" },
                { command="/cast Kill Command" },
                { command="/cast Butchery",            conditions="active_enemies>=3" },
                { command="/cast Raptor Strike" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Spearhead" },
                { command="/cast Coordinated Assault" },
                { command="/cast Wildfire Bomb" },
                { command="/cast Kill Command" },
                { command="/cast Butchery",            conditions="active_enemies>=3" },
                { command="/cast Raptor Strike" },
                { command="/cast Kill Shot",           conditions="target:health<20" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Kill Command" },
                { command="/cast Wildfire Bomb" },
                { command="/cast Raptor Strike" },
            }
        }
    },


    --------------------------------------------------------
    -- Raid
    --------------------------------------------------------
    Raid = {
        Balanced = {
            steps = {
                { command="/cast Coordinated Assault" },
                { command="/cast Wildfire Bomb" },
                { command="/cast Kill Command" },
                { command="/cast Raptor Strike" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Spearhead" },
                { command="/cast Coordinated Assault" },
                { command="/cast Wildfire Bomb" },
                { command="/cast Kill Command" },
                { command="/cast Raptor Strike" },
                { command="/cast Kill Shot",           conditions="target:health<20" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Kill Command" },
                { command="/cast Wildfire Bomb" },
                { command="/cast Raptor Ratace" },
            }
        }
    },


    --------------------------------------------------------
    -- Delves
    --------------------------------------------------------
    Delves = {
        Balanced = {
            steps = {
                { command="/cast Exhilaration",        conditions="player:health<40" },
                { command="/cast Coordinated Assault" },
                { command="/cast Wildfire Bomb" },
                { command="/cast Kill Command" },
                { command="/cast Raptor Strike" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Spearhead" },
                { command="/cast Coordinated Assault" },
                { command="/cast Wildfire Bomb" },
                { command="/cast Kill Command" },
                { command="/cast Raptor Strike" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Kill Command" },
                { command="/cast Wildfire Bomb" },
                { command="/cast Raptor Strike" },
            }
        }
    },


    --------------------------------------------------------
    -- PvP
    --------------------------------------------------------
    PvP = {
        Balanced = {
            steps = {
                { command="/cast Mending Bandage",     conditions="player:health<50" },
                { command="/cast Harpoon" },
                { command="/cast Kill Command" },
                { command="/cast Wing Clip" },
                { command="/cast Raptor Strike" },
            }
        },

        HighPerformance = {
            steps = {
                { command="/cast Spearhead" },
                { command="/cast Coordinated Assault" },
                { command="/cast Kill Command" },
                { command="/cast Raptor Strike" },
                { command="/cast Kill Shot",           conditions="target:health<20" },
            }
        },

        Safe = {
            steps = {
                { command="/cast Kill Command" },
                { command="/cast Wildfire Bomb" },
                { command="/cast Raptor Strike" },
            }
        }
    },
            { command = "/cast Wildfire Bomb", conditions = "can_cast:Wildfire Bomb" },
            { command = "/cast Kill Command", conditions = "can_cast:Kill Command" },
            { command = "/cast Flanking Strike", conditions = "can_cast:Flanking Strike" },
            { command = "/cast Raptor Strike", conditions = "true" },
        },
        aoe = {},
        steps = {}
    }
}

------------------------------------------------------------
-- Return Hunter Data
------------------------------------------------------------
return data
