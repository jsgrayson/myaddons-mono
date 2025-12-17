-- policies/healing/HybridSupport.lua
-- Defines "Support" healing intents for DPS/Tank specs.
-- Enable via Minimap Menu -> "Enable Support Heals"

local S = {}

-- Paladin: Retribution (70), Protection (66)
S["PALADIN_70"] = {
    GROUP = { spells = { "Word of Glory", "Blessing of Sacrifice", "Lay on Hands" } },
    TANK  = { spells = { "Blessing of Sacrifice", "Word of Glory", "Lay on Hands" } }, -- ToT/Focus
    SELF  = { spells = { "Word of Glory", "Divine Shield" } },
}
S["PALADIN_66"] = {
    GROUP = { spells = { "Word of Glory", "Blessing of Sacrifice", "Lay on Hands" } },
    TANK  = { spells = { "Blessing of Sacrifice", "Word of Glory" } },
    SELF  = { spells = { "Word of Glory", "Ardent Defender" } },
}

-- Shaman: Enhancement (263), Elemental (262)
S["SHAMAN_263"] = {
    GROUP = { spells = { "Ancestral Guidance", "Healing Surge" } }, 
    TANK  = { spells = { "Healing Surge", "Earth Shield" } },
    SELF  = { spells = { "Healing Surge", "Astral Shift" } },
}
S["SHAMAN_262"] = {
    GROUP = { spells = { "Ancestral Guidance", "Healing Surge" } },
    TANK  = { spells = { "Healing Surge", "Earth Shield" } },
    SELF  = { spells = { "Healing Surge", "Astral Shift" } },
}

-- Priest: Shadow (258)
S["PRIEST_258"] = {
    GROUP = { spells = { "Vampiric Embrace", "Power Word: Life", "Power Word: Shield" } },
    TANK  = { spells = { "Power Word: Life", "Power Word: Shield" } }, 
    SELF  = { spells = { "Targeted Spells", "Dispersion", "Desperate Prayer" } }, -- Targeted Spells logic placeholder
}

-- Druid: Balance (102), Feral (103), Guardian (104)
S["DRUID_102"] = {
    GROUP = { spells = { "Nature's Vigil", "Regrowth" } },
    TANK  = { spells = { "Regrowth", "Rejuvenation" } }, 
    SELF  = { spells = { "Regrowth", "Barkskin" } },
}
S["DRUID_103"] = {
    GROUP = { spells = { "Nature's Vigil", "Regrowth" } }, -- Predatory Swiftness makes Regrowth instant
    TANK  = { spells = { "Regrowth" } },
    SELF  = { spells = { "Regrowth", "Survival Instincts" } },
}
S["DRUID_104"] = {
    GROUP = { spells = { "After the Wildfire", "Regrowth" } }, -- mostly passive, but Regrowth explicitly works
    TANK  = { spells = { "Regrowth" } },
    SELF  = { spells = { "Frenzied Regeneration", "Barkskin" } },
}

-- Evoker: Augmentation (1473), Devastation (1467)
S["EVOKER_1473"] = {
    -- Augmentation is heavily support
    GROUP = { spells = { "Rescue", "Emerald Blossom", "Verdant Embrace" } },
    TANK  = { spells = { "Blistering Scales", "Verdant Embrace", "Emerald Blossom" } },
    SELF  = { spells = { "Obsidian Scales", "Emerald Blossom" } },
}
S["EVOKER_1467"] = {
    GROUP = { spells = { "Rescue", "Emerald Blossom", "Verdant Embrace" } },
    TANK  = { spells = { "Verdant Embrace", "Emerald Blossom" } },
    SELF  = { spells = { "Obsidian Scales", "Verdant Embrace" } },
}

-- Monk: Windwalker (269), Brewmaster (268)
S["MONK_269"] = {
    GROUP = { spells = { "Vivify" } }, -- Instant with Vivacious Vivification
    TANK  = { spells = { "Vivify" } },
    SELF  = { spells = { "Vivify", "Touch of Karma" } },
}

return S
