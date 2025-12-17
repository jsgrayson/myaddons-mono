-- policies/spec/_template.lua
-- AUTO-GENERATED SCAFFOLD
local addonName, addonTable = ...
local pack = {
  resources = {
    enablePooling = false,
    -- targetPoolRP = 80,
    -- dumpAtOrAbove = 90
  },

  procs = {
    -- ["Proc Name"] = { prefer={"Spell"}, avoid={"Spell"} }
  },

  cooldownSync = {
    -- ["Leader CD"] = { partners={"Partner1","Partner2"}, maxWait=6.0, minTTD=12.0 }
  },

  charges = {
    -- ["Charge Spell"] = { spendAtOrAbove=1, aoeBonus=0.4, capUrgency=2.0 }
  },

  interrupts = {
    -- optional: override interrupt kit, kickAt, etc.
  },
}

return pack
