-- policies/spec/DEATHKNIGHT_251.lua (Frost)
local addonName, addonTable = ...
local pack = {
  procs = {
    ["Killing Machine"] = { prefer={"Obliterate"}, avoid={"Frost Strike"} },
    ["Rime"]            = { prefer={"Howling Blast"} },
  },
  cooldownSync = {
    ["Pillar of Frost"] = { partners={"Empower Rune Weapon","Frostwyrm's Fury"}, maxWait=6, minTTD=12 },
  },
  resources = { targetPoolRP=80, dumpAtOrAbove=90 },
  -- charges = { ["Blood Boil"] = { spendAtOrAbove=1 } }, -- Optional, not critical for Frost
}

addonTable.PolicyPacks = addonTable.PolicyPacks or {}
addonTable.PolicyPacks["DEATHKNIGHT_251"] = pack

return pack
