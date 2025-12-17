-- policies/InterruptKits.lua
local addonName, addonTable = ...
local Kits = {}
addonTable.InterruptKits = Kits

-- Each kit entry: { spell="...", type="kick|stun|silence|incap|disorient|pet_stun", dr="stun|silence|incap|disorient|none", range=.., requiresPet=bool }
Kits.byClass = {
  DEATHKNIGHT = {
    { spell="Mind Freeze", type="kick", dr="none", range=15 },
    { spell="Asphyxiate",  type="stun", dr="stun", range=20 },
    { spell="Strangulate", type="silence", dr="silence", range=30 },
  },

  DEMONHUNTER = {
    { spell="Disrupt", type="kick", dr="none", range=10 },
    { spell="Chaos Nova", type="stun", dr="stun", range=8 },
    { spell="Imprison", type="incap", dr="incap", range=20 },
  },

  DRUID = {
    { spell="Skull Bash", type="kick", dr="none", range=13 },
    { spell="Mighty Bash", type="stun", dr="stun", range=10 },
    { spell="Incapacitating Roar", type="incap", dr="incap", range=10 },
  },

  EVOKER = {
    { spell="Quell", type="kick", dr="none", range=25 },
    { spell="Tail Swipe", type="stun", dr="stun", range=10 },
    { spell="Wing Buffet", type="stun", dr="stun", range=10 },
  },

  HUNTER = {
    { spell="Counter Shot", type="kick", dr="none", range=40 },
    { spell="Muzzle", type="kick", dr="none", range=5 },
    { spell="Intimidation", type="stun", dr="stun", range=10 },
  },

  MAGE = {
    { spell="Counterspell", type="kick", dr="none", range=40 },
    { spell="Dragon's Breath", type="disorient", dr="disorient", range=12 },
    { spell="Ring of Frost", type="incap", dr="incap", range=30 },
  },

  MONK = {
    { spell="Spear Hand Strike", type="kick", dr="none", range=5 },
    { spell="Leg Sweep", type="stun", dr="stun", range=8 },
    { spell="Paralysis", type="incap", dr="incap", range=20 },
  },

  PALADIN = {
    { spell="Rebuke", type="kick", dr="none", range=5 },
    { spell="Hammer of Justice", type="stun", dr="stun", range=10 },
    { spell="Blinding Light", type="disorient", dr="disorient", range=10 },
  },

  PRIEST = {
    { spell="Silence", type="silence", dr="silence", range=30 },
    { spell="Psychic Scream", type="disorient", dr="disorient", range=8 },
    { spell="Holy Word: Chastise", type="stun", dr="stun", range=30 },
  },

  ROGUE = {
    { spell="Kick", type="kick", dr="none", range=5 },
    { spell="Cheap Shot", type="stun", dr="stun", range=5 },
    { spell="Kidney Shot", type="stun", dr="stun", range=5 },
    { spell="Blind", type="incap", dr="incap", range=15 },
  },

  SHAMAN = {
    { spell="Wind Shear", type="kick", dr="none", range=30 },
    { spell="Capacitor Totem", type="stun", dr="stun", range=8 },
    { spell="Hex", type="incap", dr="incap", range=30 },
  },

  WARLOCK = {
    { spell="Spell Lock", type="kick", dr="none", range=40, requiresPet=true },
    { spell="Shadowfury", type="stun", dr="stun", range=30 },
    { spell="Fear", type="disorient", dr="disorient", range=20 },
  },

  WARRIOR = {
    { spell="Pummel", type="kick", dr="none", range=5 },
    { spell="Storm Bolt", type="stun", dr="stun", range=20 },
    { spell="Intimidating Shout", type="disorient", dr="disorient", range=8 },
  },
}

return Kits
