-- policies/healing/ClassHeals.lua
local H = {}

H.PRIEST = {
  enable = true,
  selfThreshold = 0.70,
  groupThreshold = 0.82,
  aoeCount = 3,
  emergency = { "Desperate Prayer", "Pain Suppression" },
  aoe = { "Prayer of Healing" },
  big = { "Flash Heal" },
  filler = { "Renew" },
}

H.DRUID = {
  enable = true,
  selfThreshold = 0.70,
  groupThreshold = 0.82,
  aoeCount = 3,
  emergency = { "Swiftmend" },
  aoe = { "Wild Growth" },
  big = { "Regrowth" },
  filler = { "Rejuvenation" },
}

H.PALADIN = {
  enable = true,
  selfThreshold = 0.65,
  groupThreshold = 0.80,
  aoeCount = 3,
  emergency = { "Lay on Hands", "Blessing of Protection" },
  aoe = { "Light of Dawn" },
  big = { "Holy Shock" },
  filler = { "Flash of Light" },
}

H.SHAMAN = {
  enable = true,
  selfThreshold = 0.70,
  groupThreshold = 0.82,
  aoeCount = 3,
  emergency = { "Nature's Swiftness" },
  aoe = { "Healing Rain", "Chain Heal" },
  big = { "Healing Surge" },
  filler = { "Riptide" },
}

H.MONK = {
  enable = true,
  selfThreshold = 0.70,
  groupThreshold = 0.82,
  aoeCount = 3,
  emergency = { "Life Cocoon" },
  aoe = { "Essence Font" },
  big = { "Enveloping Mist" },
  filler = { "Vivify" },
}

H.EVOKER = {
  enable = true,
  selfThreshold = 0.70,
  groupThreshold = 0.82,
  aoeCount = 3,
  emergency = { "Rewind" },
  aoe = { "Dream Breath", "Spiritbloom" },
  big = { "Verdant Embrace" },
  filler = { "Living Flame" },
}

return H
