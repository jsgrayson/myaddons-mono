-- db/SpecRegistry.lua
-- Canonical registry for all class/specs. Keep this stable.
local addonName, addonTable = ...
local Registry = {
  DEATHKNIGHT = {
    [250] = { key="DEATHKNIGHT_250", name="Blood",  role="TANK", resource="RUNIC_POWER", aoeThreshold=3 },
    [251] = { key="DEATHKNIGHT_251", name="Frost",  role="DAMAGER", resource="RUNIC_POWER", aoeThreshold=3 },
    [252] = { key="DEATHKNIGHT_252", name="Unholy", role="DAMAGER", resource="RUNIC_POWER", aoeThreshold=3 },
  },

  DEMONHUNTER = {
    [577] = { key="DEMONHUNTER_577", name="Havoc",     role="DAMAGER", resource="FURY", aoeThreshold=3 },
    [581] = { key="DEMONHUNTER_581", name="Vengeance", role="TANK", resource="FURY", aoeThreshold=3 },
  },

  DRUID = {
    [102] = { key="DRUID_102", name="Balance", role="DAMAGER", resource="MANA/ASTRAL_POWER", aoeThreshold=3 },
    [103] = { key="DRUID_103", name="Feral",   role="DAMAGER", resource="ENERGY/COMBO_POINTS", aoeThreshold=3 },
    [104] = { key="DRUID_104", name="Guardian",role="TANK", resource="RAGE", aoeThreshold=3 },
    [105] = { key="DRUID_105", name="Restoration", role="HEALER", resource="MANA", aoeThreshold=4 },
  },

  EVOKER = {
    [1467] = { key="EVOKER_1467", name="Devastation", role="DAMAGER", resource="MANA/ESSENCE", aoeThreshold=3 },
    [1468] = { key="EVOKER_1468", name="Preservation",role="HEALER", resource="MANA/ESSENCE", aoeThreshold=4 },
    [1473] = { key="EVOKER_1473", name="Augmentation",role="DAMAGER", resource="MANA/ESSENCE", aoeThreshold=3 },
  },

  HUNTER = {
    [253] = { key="HUNTER_253", name="Beast Mastery", role="DAMAGER", resource="FOCUS", aoeThreshold=3 },
    [254] = { key="HUNTER_254", name="Marksmanship",  role="DAMAGER", resource="FOCUS", aoeThreshold=3 },
    [255] = { key="HUNTER_255", name="Survival",      role="DAMAGER", resource="FOCUS", aoeThreshold=3 },
  },

  MAGE = {
    [62]  = { key="MAGE_62",  name="Arcane", role="DAMAGER", resource="MANA/ARCANE_CHARGES", aoeThreshold=3 },
    [63]  = { key="MAGE_63",  name="Fire",   role="DAMAGER", resource="MANA", aoeThreshold=3 },
    [64]  = { key="MAGE_64",  name="Frost",  role="DAMAGER", resource="MANA", aoeThreshold=3 },
  },

  MONK = {
    [268] = { key="MONK_268", name="Brewmaster", role="TANK", resource="ENERGY", aoeThreshold=3 },
    [269] = { key="MONK_269", name="Windwalker", role="DAMAGER", resource="ENERGY/CHI", aoeThreshold=3 },
    [270] = { key="MONK_270", name="Mistweaver", role="HEALER", resource="MANA", aoeThreshold=4 },
  },

  PALADIN = {
    [65]  = { key="PALADIN_65",  name="Holy",       role="HEALER", resource="MANA/HOLY_POWER", aoeThreshold=4 },
    [66]  = { key="PALADIN_66",  name="Protection", role="TANK", resource="HOLY_POWER", aoeThreshold=3 },
    [70]  = { key="PALADIN_70",  name="Retribution",role="DAMAGER", resource="HOLY_POWER", aoeThreshold=3 },
  },

  PRIEST = {
    [256] = { key="PRIEST_256", name="Discipline", role="HEALER", resource="MANA", aoeThreshold=4 },
    [257] = { key="PRIEST_257", name="Holy",       role="HEALER", resource="MANA", aoeThreshold=4 },
    [258] = { key="PRIEST_258", name="Shadow",     role="DAMAGER", resource="MANA/INSANITY", aoeThreshold=3 },
  },

  ROGUE = {
    [259] = { key="ROGUE_259", name="Assassination", role="DAMAGER", resource="ENERGY/COMBO_POINTS", aoeThreshold=3 },
    [260] = { key="ROGUE_260", name="Outlaw",        role="DAMAGER", resource="ENERGY/COMBO_POINTS", aoeThreshold=3 },
    [261] = { key="ROGUE_261", name="Subtlety",      role="DAMAGER", resource="ENERGY/COMBO_POINTS", aoeThreshold=3 },
  },

  SHAMAN = {
    [262] = { key="SHAMAN_262", name="Elemental",  role="DAMAGER", resource="MANA/MAELSTROM", aoeThreshold=3 },
    [263] = { key="SHAMAN_263", name="Enhancement",role="DAMAGER", resource="MANA/MAELSTROM", aoeThreshold=3 },
    [264] = { key="SHAMAN_264", name="Restoration",role="HEALER", resource="MANA", aoeThreshold=4 },
  },

  WARLOCK = {
    [265] = { key="WARLOCK_265", name="Affliction", role="DAMAGER", resource="MANA/SOUL_SHARDS", aoeThreshold=3 },
    [266] = { key="WARLOCK_266", name="Demonology", role="DAMAGER", resource="MANA/SOUL_SHARDS", aoeThreshold=3 },
    [267] = { key="WARLOCK_267", name="Destruction",role="DAMAGER", resource="MANA/SOUL_SHARDS", aoeThreshold=3 },
  },

  WARRIOR = {
    [71]  = { key="WARRIOR_71", name="Arms",        role="DAMAGER", resource="RAGE", aoeThreshold=3 },
    [72]  = { key="WARRIOR_72", name="Fury",        role="DAMAGER", resource="RAGE", aoeThreshold=3 },
    [73]  = { key="WARRIOR_73", name="Protection",  role="TANK", resource="RAGE", aoeThreshold=3 },
  },
}

-- Add helper to get by SpecID
function Registry:Get(specID)
    specID = tonumber(specID)
    if not specID then return nil end
    for class, specs in pairs(self) do
        if type(specs) == "table" and specs[specID] then
            return specs[specID]
        end
    end
    return nil
end

addonTable.SpecRegistry = Registry
return Registry
