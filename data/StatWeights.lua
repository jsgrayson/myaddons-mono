--========================================================--
-- SkillWeaver - Stat Weights Database
-- Default weights based on TWW Season 1 SimC/Wowhead trends
-- Users can override these in SkillWeaver.Settings
--========================================================--

local StatWeights = {}

-- Format: [SpecID] = { [ContentType] = { Stat = Weight, ... } }
-- Stats: "MainStat" (Str/Agi/Int), "Haste", "Crit", "Mastery", "Versatility"
-- ContentType: "Raid" (ST focus), "MythicPlus" (AoE/Dungeon focus)

StatWeights.Data = {
    --========================================================--
    -- WARRIOR
    --========================================================--
    [71] = { -- Arms
        Raid =       { MainStat=1.0, Crit=1.2, Haste=1.1, Mastery=0.9, Versatility=0.8 },
        MythicPlus = { MainStat=1.0, Crit=1.3, Haste=1.0, Mastery=1.1, Versatility=0.8 }, -- Crit/Mastery for Bladestorm
    },
    [72] = { -- Fury
        Raid =       { MainStat=1.0, Mastery=1.2, Haste=1.1, Crit=0.9, Versatility=0.8 },
        MythicPlus = { MainStat=1.0, Mastery=1.3, Haste=1.0, Crit=0.9, Versatility=0.8 },
    },
    [73] = { -- Protection
        Raid =       { MainStat=0.5, Haste=1.5, Versatility=1.2, Mastery=1.0, Crit=0.8 }, -- Haste for Shield Block
        MythicPlus = { MainStat=0.5, Haste=1.4, Versatility=1.3, Mastery=1.0, Crit=0.8 },
    },

    --========================================================--
    -- PALADIN
    --========================================================--
    [65] = { -- Holy
        Raid =       { MainStat=1.0, Crit=1.2, Mastery=1.0, Haste=0.9, Versatility=0.8 },
        MythicPlus = { MainStat=1.0, Haste=1.2, Crit=1.1, Versatility=1.0, Mastery=0.8 },
    },
    [66] = { -- Protection
        Raid =       { MainStat=0.5, Haste=1.4, Mastery=1.2, Versatility=1.1, Crit=0.8 },
        MythicPlus = { MainStat=0.5, Haste=1.5, Versatility=1.2, Mastery=1.1, Crit=0.8 },
    },
    [70] = { -- Retribution
        Raid =       { MainStat=1.0, Mastery=1.2, Crit=1.1, Haste=1.0, Versatility=0.9 },
        MythicPlus = { MainStat=1.0, Mastery=1.3, Crit=1.1, Haste=0.9, Versatility=0.9 },
    },

    --========================================================--
    -- HUNTER
    --========================================================--
    [253] = { -- Beast Mastery
        Raid =       { MainStat=1.0, Crit=1.2, Haste=1.1, Mastery=1.0, Versatility=0.8 },
        MythicPlus = { MainStat=1.0, Crit=1.2, Haste=1.0, Mastery=1.1, Versatility=0.8 },
    },
    [254] = { -- Marksmanship
        Raid =       { MainStat=1.0, Mastery=1.2, Crit=1.1, Haste=0.9, Versatility=0.8 },
        MythicPlus = { MainStat=1.0, Mastery=1.1, Crit=1.2, Haste=0.9, Versatility=0.8 },
    },
    [255] = { -- Survival
        Raid =       { MainStat=1.0, Haste=1.2, Crit=1.1, Versatility=1.0, Mastery=0.8 },
        MythicPlus = { MainStat=1.0, Haste=1.2, Crit=1.1, Versatility=1.0, Mastery=0.8 },
    },

    --========================================================--
    -- ROGUE
    --========================================================--
    [259] = { -- Assassination
        Raid =       { MainStat=1.0, Crit=1.2, Mastery=1.1, Haste=0.9, Versatility=0.8 },
        MythicPlus = { MainStat=1.0, Crit=1.2, Mastery=1.1, Haste=0.9, Versatility=0.8 },
    },
    [260] = { -- Outlaw
        Raid =       { MainStat=1.0, Versatility=1.2, Crit=1.1, Haste=1.0, Mastery=0.8 },
        MythicPlus = { MainStat=1.0, Versatility=1.2, Crit=1.1, Haste=1.0, Mastery=0.8 },
    },
    [261] = { -- Subtlety
        Raid =       { MainStat=1.0, Mastery=1.2, Versatility=1.1, Crit=1.0, Haste=0.8 },
        MythicPlus = { MainStat=1.0, Mastery=1.2, Versatility=1.1, Crit=1.0, Haste=0.8 },
    },

    --========================================================--
    -- PRIEST
    --========================================================--
    [256] = { -- Discipline
        Raid =       { MainStat=1.0, Haste=1.2, Crit=1.1, Mastery=1.0, Versatility=0.9 },
        MythicPlus = { MainStat=1.0, Haste=1.3, Crit=1.1, Versatility=1.0, Mastery=0.8 },
    },
    [257] = { -- Holy
        Raid =       { MainStat=1.0, Mastery=1.2, Crit=1.1, Versatility=1.0, Haste=0.9 },
        MythicPlus = { MainStat=1.0, Crit=1.2, Haste=1.1, Versatility=1.0, Mastery=0.8 },
    },
    [258] = { -- Shadow
        Raid =       { MainStat=1.0, Haste=1.3, Mastery=1.2, Crit=1.0, Versatility=0.9 },
        MythicPlus = { MainStat=1.0, Haste=1.3, Mastery=1.2, Crit=1.1, Versatility=0.9 }, -- Mastery scales well in AoE
    },

    --========================================================--
    -- DEATH KNIGHT
    --========================================================--
    [250] = { -- Blood
        Raid =       { MainStat=0.5, Haste=1.4, Versatility=1.2, Mastery=1.1, Crit=0.8 },
        MythicPlus = { MainStat=0.5, Haste=1.4, Versatility=1.2, Mastery=1.1, Crit=0.8 },
    },
    [251] = { -- Frost
        Raid =       { MainStat=1.0, Mastery=1.2, Crit=1.1, Haste=1.0, Versatility=0.9 }, -- Obliteration usually favors Mastery
        MythicPlus = { MainStat=1.0, Mastery=1.3, Crit=1.1, Haste=0.9, Versatility=0.9 },
    },
    [252] = { -- Unholy
        Raid =       { MainStat=1.0, Haste=1.2, Mastery=1.1, Crit=1.0, Versatility=0.9 },
        MythicPlus = { MainStat=1.0, Mastery=1.3, Haste=1.1, Crit=1.0, Versatility=0.9 }, -- Mastery for disease/AoE
    },

    --========================================================--
    -- SHAMAN
    --========================================================--
    [262] = { -- Elemental
        Raid =       { MainStat=1.0, Haste=1.2, Crit=1.1, Versatility=1.0, Mastery=0.9 },
        MythicPlus = { MainStat=1.0, Crit=1.2, Haste=1.1, Versatility=1.0, Mastery=0.9 },
    },
    [263] = { -- Enhancement
        Raid =       { MainStat=1.0, Haste=1.3, Mastery=1.2, Versatility=1.0, Crit=0.9 },
        MythicPlus = { MainStat=1.0, Haste=1.3, Mastery=1.2, Versatility=1.0, Crit=0.9 },
    },
    [264] = { -- Restoration
        Raid =       { MainStat=1.0, Crit=1.2, Versatility=1.1, Haste=1.0, Mastery=0.9 },
        MythicPlus = { MainStat=1.0, Crit=1.2, Haste=1.1, Versatility=1.0, Mastery=0.9 },
    },

    --========================================================--
    -- MAGE
    --========================================================--
    [62] = { -- Arcane
        Raid =       { MainStat=1.0, Crit=1.1, Haste=1.0, Mastery=1.0, Versatility=0.9 }, -- Often balanced
        MythicPlus = { MainStat=1.0, Crit=1.1, Haste=1.0, Mastery=1.0, Versatility=0.9 },
    },
    [63] = { -- Fire
        Raid =       { MainStat=1.0, Haste=1.3, Versatility=1.1, Mastery=1.0, Crit=0.8 }, -- Haste is king
        MythicPlus = { MainStat=1.0, Haste=1.3, Mastery=1.1, Versatility=1.0, Crit=0.8 },
    },
    [64] = { -- Frost
        Raid =       { MainStat=1.0, Mastery=1.2, Crit=1.0, Haste=1.1, Versatility=0.9 }, -- Crit to cap (33%)
        MythicPlus = { MainStat=1.0, Mastery=1.2, Crit=1.0, Haste=1.1, Versatility=0.9 },
    },

    --========================================================--
    -- WARLOCK
    --========================================================--
    [265] = { -- Affliction
        Raid =       { MainStat=1.0, Mastery=1.3, Haste=1.2, Crit=1.0, Versatility=0.9 },
        MythicPlus = { MainStat=1.0, Mastery=1.3, Haste=1.2, Crit=1.0, Versatility=0.9 },
    },
    [266] = { -- Demonology
        Raid =       { MainStat=1.0, Haste=1.2, Crit=1.1, Mastery=1.0, Versatility=0.9 },
        MythicPlus = { MainStat=1.0, Haste=1.3, Crit=1.1, Mastery=1.0, Versatility=0.9 },
    },
    [267] = { -- Destruction
        Raid =       { MainStat=1.0, Haste=1.3, Mastery=1.1, Crit=1.0, Versatility=0.9 },
        MythicPlus = { MainStat=1.0, Haste=1.3, Mastery=1.2, Crit=1.0, Versatility=0.9 },
    },

    --========================================================--
    -- MONK
    --========================================================--
    [268] = { -- Brewmaster
        Raid =       { MainStat=0.5, Crit=1.2, Versatility=1.2, Mastery=1.0, Haste=0.8 },
        MythicPlus = { MainStat=0.5, Crit=1.2, Versatility=1.2, Mastery=1.0, Haste=0.8 },
    },
    [269] = { -- Windwalker
        Raid =       { MainStat=1.0, Versatility=1.2, Crit=1.1, Mastery=1.0, Haste=0.8 },
        MythicPlus = { MainStat=1.0, Versatility=1.2, Crit=1.1, Mastery=1.0, Haste=0.8 },
    },
    [270] = { -- Mistweaver
        Raid =       { MainStat=1.0, Haste=1.2, Crit=1.1, Versatility=1.0, Mastery=0.9 },
        MythicPlus = { MainStat=1.0, Haste=1.3, Crit=1.1, Versatility=1.0, Mastery=0.8 },
    },

    --========================================================--
    -- DRUID
    --========================================================--
    [102] = { -- Balance
        Raid =       { MainStat=1.0, Mastery=1.3, Haste=1.2, Crit=1.0, Versatility=0.9 },
        MythicPlus = { MainStat=1.0, Mastery=1.3, Haste=1.2, Crit=1.0, Versatility=0.9 },
    },
    [103] = { -- Feral
        Raid =       { MainStat=1.0, Crit=1.2, Mastery=1.2, Versatility=1.0, Haste=0.8 },
        MythicPlus = { MainStat=1.0, Crit=1.2, Mastery=1.2, Versatility=1.0, Haste=0.8 },
    },
    [104] = { -- Guardian
        Raid =       { MainStat=0.5, Versatility=1.3, Haste=1.2, Mastery=1.1, Crit=0.8 },
        MythicPlus = { MainStat=0.5, Versatility=1.3, Haste=1.2, Mastery=1.1, Crit=0.8 },
    },
    [105] = { -- Restoration
        Raid =       { MainStat=1.0, Haste=1.2, Mastery=1.1, Versatility=1.0, Crit=0.9 },
        MythicPlus = { MainStat=1.0, Haste=1.3, Versatility=1.1, Crit=1.0, Mastery=0.9 }, -- Haste for DPS/HoTs
    },

    --========================================================--
    -- DEMON HUNTER
    --========================================================--
    [577] = { -- Havoc
        Raid =       { MainStat=1.0, Crit=1.2, Mastery=1.1, Haste=1.0, Versatility=0.9 },
        MythicPlus = { MainStat=1.0, Crit=1.2, Mastery=1.1, Haste=1.0, Versatility=0.9 },
    },
    [581] = { -- Vengeance
        Raid =       { MainStat=0.5, Haste=1.3, Versatility=1.2, Crit=1.0, Mastery=0.9 },
        MythicPlus = { MainStat=0.5, Haste=1.3, Versatility=1.2, Crit=1.0, Mastery=0.9 },
    },

    --========================================================--
    -- EVOKER
    --========================================================--
    [1467] = { -- Devastation
        Raid =       { MainStat=1.0, Mastery=1.3, Haste=1.1, Crit=1.0, Versatility=0.9 }, -- Mastery: Giantkiller
        MythicPlus = { MainStat=1.0, Mastery=1.3, Haste=1.1, Crit=1.0, Versatility=0.9 },
    },
    [1468] = { -- Preservation
        Raid =       { MainStat=1.0, Crit=1.2, Mastery=1.1, Versatility=1.0, Haste=0.9 },
        MythicPlus = { MainStat=1.0, Crit=1.2, Haste=1.1, Versatility=1.0, Mastery=0.9 },
    },
    [1473] = { -- Augmentation
        Raid =       { MainStat=1.0, Mastery=1.3, Haste=1.1, Crit=1.0, Versatility=0.9 }, -- Mastery buffs allies
        MythicPlus = { MainStat=1.0, Mastery=1.3, Haste=1.1, Crit=1.0, Versatility=0.9 },
    },
}

function StatWeights:GetWeights(specID, contentType)
    if not self.Data[specID] then return nil end
    
    -- Default to Raid if content type not found or specified
    local weights = self.Data[specID][contentType] or self.Data[specID]["Raid"]
    return weights
end

return StatWeights
