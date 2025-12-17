-- SkillWeaver Sequence Contract
-- Defines the canonical schema for sequences.
-- This file is the single source of truth for sequence structure.

SkillWeaver.SequenceContract = {
  meta = {
    class        = "string",
    spec         = "string",
    mode         = "MYTHIC_PLUS|RAID|PVP|OPEN_WORLD|DELVE",
    variant      = "BALANCED|SCRAPED|SAFE",
    source       = "ICY_VEINS|MANUAL|COMMUNITY",
    version      = "string",
    patch        = "string",
    hash         = "string",
  },

  talents = {
    wowhead = "string",
    hero    = "string",
    pvp     = { "spellID" }
  },

  sections = {
    -- Execution keys:
    precombat  = {},
    interrupts = {},
    defensives = {},
    cooldowns  = {},
    core       = {},
    fillers    = {},
  },

  rules = {
    allowFallback   = true,
    requireTalents  = true,
    requireHeroTree = false,
    strictPvP       = true,
  }
}

-- The deterministic order in which sections are evaluated.
SkillWeaver.SectionOrder = {
  "interrupts",
  "defensives",
  "cooldowns",
  "core",
  "fillers"
}
