-- policies/healing/SpecProfiles.lua
-- Controller-friendly, bind-intent healing profiles.
-- Intents: PRIMARY (X), GROUP (Ctrl-X), TANK (Alt-X via ToT), SELF (Ctrl-Alt-X)

local P = {}

local STYLE = {
  REACTIVE = "REACTIVE",
  PROACTIVE = "PROACTIVE",
  DAMAGE_DRIVEN = "DAMAGE_DRIVEN",
}

-- Utility: quick set for ground spells per spec (engine uses this)
-- ground.mode: "CURSOR" | "PLAYER" | "RETICLE"
-- ground.spells: list of spell names treated as ground-target
-- IMPORTANT: Only include ground spells in GROUP.spells (not PRIMARY/TANK/SELF)

-- =========================
-- RESTO SHAMAN (264)
-- =========================
P["SHAMAN_264"] = {
  style = STYLE.REACTIVE,

  ground = {
    mode = "CURSOR",
    spells = {
      "Healing Rain",
      -- optional utility drops (add if you actually use them)
      -- "Capacitor Totem",
      -- "Earthbind Totem",
    }
  },

  PRIMARY = {
    spells = {
      "Earth Shield",
      "Flame Shock",
      "Lava Burst",
      "Lightning Bolt",
    },
  },

  GROUP = {
    spells = {
      "Healing Rain",          -- ground (CURSOR)
      "Chain Heal",
      "Healing Tide Totem",
      "Spirit Link Totem",
      "Ascendance",
      "Earthen Wall Totem",
    },
    rules = {
      noBlindFiller = true,
    }
  },

  TANK = {
    targetMode = "TARGETTARGET",
    spells = {
      "Nature's Swiftness",
      "Healing Wave",          -- prefer with NS (engine-gated)
      "Healing Surge",         -- danger only (engine-gated)
      "Riptide",
      "Ancestral Protection Totem",
    },
    rules = {
      noBlindFiller = true,
    }
  },

  SELF = {
    spells = {
      "Astral Shift",
      "Healing Surge",
      "Healthstone",
    },
  },
}

-- =========================
-- RESTO DRUID (105)
-- =========================
P["DRUID_105"] = {
  style = STYLE.PROACTIVE,

  ground = {
    mode = "CURSOR",
    spells = {
      "Efflorescence",
    }
  },

  PRIMARY = {
    spells = {
      "Moonfire",
      "Sunfire",
      "Wrath",
      -- Lifebloom is targeted; we keep it out of PRIMARY if you never friendly-target.
      -- If you do ToT-maintenance, you can move it to TANK.
    },
  },

  GROUP = {
    spells = {
      "Efflorescence",         -- ground (CURSOR)
      "Wild Growth",
      "Tranquility",
      "Flourish",
      "Grove Guardians",
    },
  },

  TANK = {
    targetMode = "TARGETTARGET",
    spells = {
      "Ironbark",
      "Swiftmend",
      "Lifebloom",
      "Regrowth",              -- proc-only recommended
    },
    rules = {
      noBlindFiller = true,
      procOnly = {
        ["Regrowth"] = "Clearcasting", -- Omen of Clarity
      },
    }
  },

  SELF = {
    spells = {
      "Barkskin",
      "Renewal",
      "Regrowth",
      "Healthstone",
    },
  },
}

-- =========================
-- HOLY PALADIN (65)
-- =========================
P["PALADIN_65"] = {
  style = STYLE.DAMAGE_DRIVEN,

  ground = { mode = "RETICLE", spells = {} },

  PRIMARY = {
    spells = {
      "Holy Shock",
      "Crusader Strike",
      "Judgment",
      "Consecration",
    },
  },

  GROUP = {
    spells = {
      "Light of Dawn",
      "Divine Toll",
      "Aura Mastery",
      "Avenging Wrath",
    },
  },

  TANK = {
    targetMode = "TARGETTARGET",
    spells = {
      "Blessing of Sacrifice",
      "Word of Glory",
      "Lay on Hands",
      "Blessing of Protection",
    },
  },

  SELF = {
    spells = {
      "Divine Shield",
      "Shield of Vengeance",
      "Word of Glory",
      "Healthstone",
    },
  },
}

-- =========================
-- DISC PRIEST (256)
-- =========================
P["PRIEST_256"] = {
  style = STYLE.DAMAGE_DRIVEN,

  ground = {
    mode = "CURSOR",
    spells = {
      -- include only if Barrier is ground-targeted in your client/build
      "Power Word: Barrier",
    }
  },

  PRIMARY = {
    spells = {
      "Power Word: Shield",
      "Penance",
      "Smite",
      "Shadow Word: Pain",
      "Mind Blast",
    },
  },

  GROUP = {
    spells = {
      "Power Word: Barrier",   -- ground (CURSOR) if applicable
      "Power Word: Radiance",
      "Rapture",
    },
  },

  TANK = {
    targetMode = "TARGETTARGET",
    spells = {
      "Pain Suppression",
      "Power Word: Shield",
      "Penance",
    },
  },

  SELF = {
    spells = {
      "Desperate Prayer",
      "Fade",
      "Power Word: Shield",
      "Healthstone",
    },
  },
}

-- =========================
-- HOLY PRIEST (257) (included)
-- =========================
P["PRIEST_257"] = {
  style = STYLE.REACTIVE,

  ground = {
    mode = "CURSOR",
    spells = {
      -- If Sanctify is ground-targeted in your client/build; otherwise remove.
      "Holy Word: Sanctify",
    }
  },

  PRIMARY = {
    spells = {
      "Smite",
      "Holy Word: Serenity",
    },
  },

  GROUP = {
    spells = {
      "Holy Word: Sanctify",   -- ground (CURSOR) if applicable
      "Prayer of Healing",
      "Divine Hymn",
    },
    rules = { noBlindFiller = true }
  },

  TANK = {
    targetMode = "TARGETTARGET",
    spells = {
      "Guardian Spirit",
      "Holy Word: Serenity",
      "Flash Heal",
    },
    rules = { noBlindFiller = true }
  },

  SELF = {
    spells = {
      "Desperate Prayer",
      "Flash Heal",
      "Healthstone",
    },
  },
}

-- =========================
-- MISTWEAVER MONK (270)
-- =========================
P["MONK_270"] = {
  style = STYLE.DAMAGE_DRIVEN,

  ground = { mode = "RETICLE", spells = {} },

  PRIMARY = {
    spells = {
      "Renewing Mist",
      "Rising Sun Kick",
      "Tiger Palm",
      "Blackout Kick",
    },
  },

  GROUP = {
    spells = {
      "Essence Font",
      "Revival",
      "Invoke Yu'lon, the Jade Serpent",
      "Invoke Chi-Ji, the Red Crane",
    },
  },

  TANK = {
    targetMode = "TARGETTARGET",
    spells = {
      "Life Cocoon",
      "Enveloping Mist",
      "Vivify",
    },
    rules = { noBlindFiller = true }
  },

  SELF = {
    spells = {
      "Fortifying Brew",
      "Vivify",
      "Healthstone",
    },
  },
}

-- =========================
-- PRES EVOKER (1468)
-- =========================
P["EVOKER_1468"] = {
  style = STYLE.REACTIVE,

  ground = { mode = "RETICLE", spells = {} },

  PRIMARY = {
    spells = {
      "Living Flame",
      -- You can add damage spells if you want DPS windows:
      -- "Disintegrate",
      -- "Fire Breath",
    },
  },

  GROUP = {
    spells = {
      "Dream Breath",
      "Spiritbloom",
      "Rewind",
      "Emerald Communion",
    },
  },

  TANK = {
    targetMode = "TARGETTARGET",
    spells = {
      "Time Dilation",
      "Verdant Embrace",
      "Living Flame",
    },
    rules = { noBlindFiller = true }
  },

  SELF = {
    spells = {
      "Obsidian Scales",
      "Renewing Blaze",
      "Living Flame",
      "Healthstone",
    },
  },
}

return P
