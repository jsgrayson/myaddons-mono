SkillWeaverDB = SkillWeaverDB or {}

local function deepCopy(src)
  local t = {}
  for k,v in pairs(src) do
    if type(v) == "table" then t[k] = deepCopy(v) else t[k] = v end
  end
  return t
end

SkillWeaverDefaults = {
  version = 1,
  enabled = true,

  -- Global “Mode” selection (can be overridden per spec)
  mode = "Delves", -- "Delves" | "MythicPlus" | "Raid" | "PvP" | "OpenWorld"

  -- Safety toggles (exposes & persists user preferences)
  toggles = {
    burst = true,
    defensives = true,
    interrupts = true,
    trinkets = false,
    emergencyGroupHeals = true,

    dpsEmergencyHeals = true,
    groundTargetMode = "cursor",
    showHealButton = true,
    showSelfButton = true,
    hideEmptyButtons = true,
  }, -- for hybrid DPS specs

  -- UI
  ui = {
    minimap = { hide = false },
    panel = { show = true },
  },

  -- Profile selection
  profiles = {
    -- keyed by "CLASS_SPECID"
    -- example: ["DEATHKNIGHT_250"] = { name="Balanced", mode="Delves" }
  },

  -- Secure button macro templates (set by engine)
  bindings = {
    ST = "X",
    AOE = "C",
    INT = "R",
    UTIL = "T",
    HEAL = "CTRL-X",
    SELF = "Z",
  },
}

if not SkillWeaverDB.version then
  SkillWeaverDB = deepCopy(SkillWeaverDefaults)
end



SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver
SW.Defaults = SW.Defaults or {}

SW.Defaults.SelfDefaults = {
  -- DK
  ["DEATHKNIGHT_250"] = { "Icebound Fortitude", "Vampiric Blood", "Rune Tap", "Anti-Magic Shell", "Death Strike" },
  ["DEATHKNIGHT_251"] = { "Anti-Magic Shell", "Icebound Fortitude" },
  ["DEATHKNIGHT_252"] = { "Anti-Magic Shell", "Icebound Fortitude", "Death Strike" },

  -- DH
  ["DEMONHUNTER_577"] = { "Blur", "Darkness" },
  ["DEMONHUNTER_581"] = { "Demon Spikes", "Metamorphosis", "Fel Devastation" },

  -- Druid
  ["DRUID_102"] = { "Barkskin", "Renewal" },
  ["DRUID_103"] = { "Survival Instincts", "Barkskin" },
  ["DRUID_104"] = { "Barkskin", "Survival Instincts", "Frenzied Regeneration", "Ironfur" },
  ["DRUID_105"] = { "Barkskin", "Renewal" },

  -- Paladin
  ["PALADIN_65"] = { "Divine Shield", "Lay on Hands" },
  ["PALADIN_66"] = { "Ardent Defender", "Guardian of Ancient Kings", "Divine Shield" },
  ["PALADIN_70"] = { "Shield of Vengeance", "Divine Protection" },

  -- Shaman
  ["SHAMAN_262"] = { "Astral Shift" },
  ["SHAMAN_263"] = { "Astral Shift" },
  ["SHAMAN_264"] = { "Astral Shift" },

  -- Warrior
  ["WARRIOR_71"] = { "Die by the Sword", "Rallying Cry" },
  ["WARRIOR_72"] = { "Enraged Regeneration", "Rallying Cry" },
  ["WARRIOR_73"] = { "Shield Wall", "Last Stand", "Ignore Pain", "Shield Block" },

  -- Warlock
  ["WARLOCK_265"] = { "Unending Resolve", "Dark Pact" },
  ["WARLOCK_266"] = { "Unending Resolve", "Dark Pact" },
  ["WARLOCK_267"] = { "Unending Resolve", "Dark Pact" },

  -- Mage
  ["MAGE_62"] = { "Ice Block", "Alter Time" },
  ["MAGE_63"] = { "Ice Block", "Blazing Barrier" },
  ["MAGE_64"] = { "Ice Block", "Ice Barrier" },

  -- Hunter
  ["HUNTER_253"] = { "Exhilaration", "Survival of the Fittest" },
  ["HUNTER_254"] = { "Exhilaration", "Survival of the Fittest" },
  ["HUNTER_255"] = { "Exhilaration", "Survival of the Fittest" },

  -- Monk
  ["MONK_268"] = { "Fortifying Brew", "Dampen Harm", "Celestial Brew" },
  ["MONK_269"] = { "Touch of Karma", "Fortifying Brew" },
  ["MONK_270"] = { "Fortifying Brew" },

  -- Priest
  ["PRIEST_256"] = { "Desperate Prayer" },
  ["PRIEST_257"] = { "Desperate Prayer" },
  ["PRIEST_258"] = { "Dispersion", "Desperate Prayer" },

  -- Evoker
  ["EVOKER_1467"] = { "Obsidian Scales", "Renewing Blaze" },
  ["EVOKER_1468"] = { "Obsidian Scales", "Renewing Blaze" },
  ["EVOKER_1473"] = { "Obsidian Scales" },
}

function SW.Defaults:GetDefaultSelfSteps(classSpecKey)
  local list = self.SelfDefaults[classSpecKey]
  if not list then return nil end
  local steps = {}
  for _, spell in ipairs(list) do
    table.insert(steps, { command = "/cast " .. spell })
  end
  return steps
end


