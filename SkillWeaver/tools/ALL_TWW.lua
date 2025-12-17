-- Data/Classes/ALL.lua
-- Full offline rotation fallbacks for EVERY class/spec + ALL content types.
-- Normalized schema (ST/AOE/INT/UTIL) with Balanced / HighPerformance / Safe profiles.
-- NOTE: These are intentionally "priority-style" baselines meant to be replaced/overwritten by your backend when connected.

SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver

local function S(cmd) return { command = cmd } end

local function mkRotation(stSteps, aoeSteps, intMacro, utilMacro, healSteps)
  return {
    ST   = { steps = stSteps or {} },
    AOE  = { steps = (aoeSteps and #aoeSteps > 0) and aoeSteps or (stSteps or {}) },
    INT  = { macro = intMacro or "" },  -- empty => engine falls back to class default interrupt
    UTIL = { macro = utilMacro or "" },
    HEAL = healSteps and { steps = healSteps } or nil,
  }
end

local function mkProfiles(bal, hp, safe)
  return {
    Balanced = bal,
    HighPerformance = hp or bal,
    Safe = safe or bal,
  }
end

local function mkAllModes(profiles, pvpProfiles)
  return {
    Delves     = profiles,
    MythicPlus = profiles,
    Raid       = profiles,
    OpenWorld  = profiles,
    PvP        = pvpProfiles or profiles,
  }
end

local data = {}

-- =========================================================
-- DEATH KNIGHT
-- =========================================================
do -- Blood (250)
  local st = {
    S("/cast Dancing Rune Weapon"),
    S("/cast Vampiric Blood"),
    S("/cast Marrowrend"),
    S("/cast Death Strike"),
    S("/cast Blood Boil"),
    S("/cast Heart Strike"),
    S("/cast Tombstone"),
    S("/cast Rune Tap"),
    S("/cast Anti-Magic Shell"),
  }
  local aoe = {
    S("/cast Death and Decay"),
    S("/cast Dancing Rune Weapon"),
    S("/cast Blood Boil"),
    S("/cast Marrowrend"),
    S("/cast Heart Strike"),
    S("/cast Death Strike"),
    S("/cast Bonestorm"),
    S("/cast Rune Tap"),
  }
  local hp = {
    S("/cast Abomination Limb"),
    S("/cast Dancing Rune Weapon"),
    S("/cast Vampiric Blood"),
    S("/cast Death and Decay"),
    S("/cast Tombstone"),
    S("/cast Marrowrend"),
    S("/cast Blood Boil"),
    S("/cast Heart Strike"),
    S("/cast Death Strike"),
  }
  local safe = {
    S("/cast Icebound Fortitude"),
    S("/cast Rune Tap"),
    S("/cast Anti-Magic Shell"),
    S("/cast Death Strike"),
    S("/cast Marrowrend"),
    S("/cast Blood Boil"),
    S("/cast Heart Strike"),
  }
  data["DEATHKNIGHT_250"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Icebound Fortitude\n"),
    mkRotation(hp, aoe, "", "/cast Vampiric Blood\n"),
    mkRotation(safe, aoe, "", "/cast Rune Tap\n")
  ))
end

do -- Frost (251)
  local st = {
    S("/cast Pillar of Frost"),
    S("/cast Remorseless Winter"),
    S("/cast Howling Blast"),
    S("/cast Obliterate"),
    S("/cast Frost Strike"),
    S("/cast Empower Rune Weapon"),
    S("/cast Glacial Advance"),
    S("/cast Frostwyrm's Fury"),
  }
  local aoe = {
    S("/cast Remorseless Winter"),
    S("/cast Howling Blast"),
    S("/cast Glacial Advance"),
    S("/cast Frost Strike"),
    S("/cast Obliterate"),
    S("/cast Frostscythe"),
    S("/cast Frostwyrm's Fury"),
  }
  local hp = {
    S("/cast Pillar of Frost"),
    S("/cast Empower Rune Weapon"),
    S("/cast Remorseless Winter"),
    S("/cast Frostwyrm's Fury"),
    S("/cast Obliterate"),
    S("/cast Howling Blast"),
    S("/cast Frost Strike"),
    S("/cast Glacial Advance"),
  }
  local safe = {
    S("/cast Anti-Magic Shell"),
    S("/cast Icebound Fortitude"),
    S("/cast Remorseless Winter"),
    S("/cast Obliterate"),
    S("/cast Howling Blast"),
    S("/cast Frost Strike"),
  }
  data["DEATHKNIGHT_251"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", ""),
    mkRotation(hp, aoe, "", ""),
    mkRotation(safe, aoe, "", "/cast Anti-Magic Shell\n")
  ))
end

do -- Unholy (252)
  local st = {
    S("/cast Army of the Dead"),
    S("/cast Unholy Assault"),
    S("/cast Dark Transformation"),
    S("/cast Apocalypse"),
    S("/cast Outbreak"),
    S("/cast Festering Strike"),
    S("/cast Scourge Strike"),
    S("/cast Death Coil"),
    S("/cast Soul Reaper"),
  }
  local aoe = {
    S("/cast Army of the Dead"),
    S("/cast Dark Transformation"),
    S("/cast Outbreak"),
    S("/cast Death and Decay"),
    S("/cast Epidemic"),
    S("/cast Scourge Strike"),
    S("/cast Festering Strike"),
    S("/cast Apocalypse"),
  }
  local hp = {
    S("/cast Summon Gargoyle"),
    S("/cast Army of the Dead"),
    S("/cast Unholy Assault"),
    S("/cast Dark Transformation"),
    S("/cast Apocalypse"),
    S("/cast Death and Decay"),
    S("/cast Scourge Strike"),
    S("/cast Death Coil"),
  }
  local safe = {
    S("/cast Anti-Magic Shell"),
    S("/cast Icebound Fortitude"),
    S("/cast Death Strike"),
    S("/cast Outbreak"),
    S("/cast Scourge Strike"),
    S("/cast Death Coil"),
  }
  data["DEATHKNIGHT_252"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", ""),
    mkRotation(hp, aoe, "", ""),
    mkRotation(safe, aoe, "", "/cast Anti-Magic Shell\n")
  ))
end

-- =========================================================
-- DEMON HUNTER
-- =========================================================
do -- Havoc (577)
  local st = {
    S("/cast Metamorphosis"),
    S("/cast Eye Beam"),
    S("/cast Essence Break"),
    S("/cast Blade Dance"),
    S("/cast Chaos Strike"),
    S("/cast Immolation Aura"),
    S("/cast Throw Glaive"),
    S("/cast Demon's Bite"),
  }
  local aoe = {
    S("/cast Metamorphosis"),
    S("/cast Eye Beam"),
    S("/cast Blade Dance"),
    S("/cast Immolation Aura"),
    S("/cast Fel Rush"),
    S("/cast Chaos Strike"),
    S("/cast Throw Glaive"),
  }
  local safe = {
    S("/cast Darkness"),
    S("/cast Blur"),
    S("/cast Eye Beam"),
    S("/cast Blade Dance"),
    S("/cast Chaos Strike"),
  }
  data["DEMONHUNTER_577"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Blur\n"),
    mkRotation(st, aoe, "", "/cast Darkness\n"),
    mkRotation(safe, aoe, "", "/cast Blur\n")
  ))
end

do -- Vengeance (581)
  local st = {
    S("/cast Metamorphosis"),
    S("/cast Fel Devastation"),
    S("/cast Immolation Aura"),
    S("/cast Sigil of Flame"),
    S("/cast Spirit Bomb"),
    S("/cast Soul Cleave"),
    S("/cast Fracture"),
    S("/cast Demon Spikes"),
  }
  local aoe = {
    S("/cast Metamorphosis"),
    S("/cast Fel Devastation"),
    S("/cast Immolation Aura"),
    S("/cast Sigil of Flame"),
    S("/cast Spirit Bomb"),
    S("/cast Soul Cleave"),
    S("/cast Infernal Strike"),
    S("/cast Demon Spikes"),
  }
  local safe = {
    S("/cast Demon Spikes"),
    S("/cast Metamorphosis"),
    S("/cast Soul Cleave"),
    S("/cast Immolation Aura"),
    S("/cast Sigil of Flame"),
  }
  data["DEMONHUNTER_581"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Demon Spikes\n"),
    mkRotation(st, aoe, "", "/cast Metamorphosis\n"),
    mkRotation(safe, aoe, "", "/cast Demon Spikes\n")
  ))
end

-- =========================================================
-- DRUID
-- =========================================================
do -- Balance (102)
  local st = {
    S("/cast Incarnation: Chosen of Elune"),
    S("/cast Celestial Alignment"),
    S("/cast Sunfire"),
    S("/cast Moonfire"),
    S("/cast Starsurge"),
    S("/cast Wrath"),
    S("/cast Starfire"),
    S("/cast Fury of Elune"),
    S("/cast Starfall"),
  }
  local aoe = {
    S("/cast Celestial Alignment"),
    S("/cast Sunfire"),
    S("/cast Starfall"),
    S("/cast Starfire"),
    S("/cast Moonfire"),
    S("/cast Starsurge"),
    S("/cast Fury of Elune"),
  }
  local safe = {
    S("/cast Barkskin"),
    S("/cast Renewal"),
    S("/cast Sunfire"),
    S("/cast Moonfire"),
    S("/cast Wrath"),
    S("/cast Starsurge"),
  }
  data["DRUID_102"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Barkskin\n"),
    mkRotation(st, aoe, "", "/cast Celestial Alignment\n"),
    mkRotation(safe, aoe, "", "/cast Barkskin\n")
  ))
end

do -- Feral (103)
  local st = {
    S("/cast Berserk"),
    S("/cast Tiger's Fury"),
    S("/cast Rake"),
    S("/cast Rip"),
    S("/cast Ferocious Bite"),
    S("/cast Shred"),
    S("/cast Primal Wrath"),
    S("/cast Brutal Slash"),
    S("/cast Thrash"),
  }
  local aoe = {
    S("/cast Berserk"),
    S("/cast Tiger's Fury"),
    S("/cast Primal Wrath"),
    S("/cast Thrash"),
    S("/cast Swipe"),
    S("/cast Rake"),
    S("/cast Rip"),
  }
  local safe = {
    S("/cast Survival Instincts"),
    S("/cast Barkskin"),
    S("/cast Rake"),
    S("/cast Rip"),
    S("/cast Shred"),
    S("/cast Ferocious Bite"),
  }
  data["DRUID_103"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Survival Instincts\n"),
    mkRotation(st, aoe, "", "/cast Berserk\n"),
    mkRotation(safe, aoe, "", "/cast Barkskin\n")
  ), mkProfiles(
    mkRotation(st, aoe, "", "/cast Mighty Bash\n"),
    mkRotation(st, aoe, "", "/cast Berserk\n"),
    mkRotation(safe, aoe, "", "/cast Survival Instincts\n")
  ))
end

do -- Guardian (104)
  local st = {
    S("/cast Incarnation: Guardian of Ursoc"),
    S("/cast Berserk"),
    S("/cast Thrash"),
    S("/cast Mangle"),
    S("/cast Ironfur"),
    S("/cast Maul"),
    S("/cast Frenzied Regeneration"),
    S("/cast Swipe"),
    S("/cast Barkskin"),
  }
  local aoe = {
    S("/cast Berserk"),
    S("/cast Thrash"),
    S("/cast Swipe"),
    S("/cast Ironfur"),
    S("/cast Mangle"),
    S("/cast Maul"),
    S("/cast Frenzied Regeneration"),
  }
  local safe = {
    S("/cast Barkskin"),
    S("/cast Survival Instincts"),
    S("/cast Ironfur"),
    S("/cast Frenzied Regeneration"),
    S("/cast Thrash"),
    S("/cast Mangle"),
  }
  data["DRUID_104"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Ironfur\n"),
    mkRotation(st, aoe, "", "/cast Berserk\n"),
    mkRotation(safe, aoe, "", "/cast Barkskin\n")
  ))
end

do -- Restoration (105)
  local st = {
    S("/cast Lifebloom"),
    S("/cast Rejuvenation"),
    S("/cast Regrowth"),
    S("/cast Swiftmend"),
    S("/cast Cenarion Ward"),
    S("/cast Nature's Swiftness"),
    S("/cast Wild Growth"),
    S("/cast Flourish"),
    S("/cast Tranquility"),
  }
  local aoe = {
    S("/cast Wild Growth"),
    S("/cast Swiftmend"),
    S("/cast Flourish"),
    S("/cast Rejuvenation"),
    S("/cast Regrowth"),
    S("/cast Tranquility"),
    S("/cast [@cursor] Efflorescence"),
  }
  local safe = {
    S("/cast Barkskin"),
    S("/cast Ironbark"),
    S("/cast Nature's Swiftness"),
    S("/cast Regrowth"),
    S("/cast Rejuvenation"),
    S("/cast Wild Growth"),
  }
  data["DRUID_105"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast [@cursor] Efflorescence\n", {
    S("/cast Lifebloom"),
    S("/cast Rejuvenation"),
    S("/cast Regrowth"),
    S("/cast Swiftmend"),
    S("/cast Wild Growth"),
    S("/cast Nature's Swiftness"),
    S("/cast Ironbark"),
    S("/cast Flourish"),
    S("/cast Tranquility"),
  }),
    mkRotation(st, aoe, "", "/cast Tranquility\n", {
    S("/cast Lifebloom"),
    S("/cast Rejuvenation"),
    S("/cast Regrowth"),
    S("/cast Swiftmend"),
    S("/cast Wild Growth"),
    S("/cast Nature's Swiftness"),
    S("/cast Ironbark"),
    S("/cast Flourish"),
    S("/cast Tranquility"),
  }),
    mkRotation(safe, aoe, "", "/cast Ironbark\n", {
    S("/cast Lifebloom"),
    S("/cast Rejuvenation"),
    S("/cast Regrowth"),
    S("/cast Swiftmend"),
    S("/cast Wild Growth"),
    S("/cast Nature's Swiftness"),
    S("/cast Ironbark"),
    S("/cast Flourish"),
    S("/cast Tranquility"),
  })
  ))
end

-- =========================================================
-- EVOKER
-- =========================================================
do -- Devastation (1467)
  local st = {
    S("/cast Dragonrage"),
    S("/cast Fire Breath"),
    S("/cast Eternity Surge"),
    S("/cast Disintegrate"),
    S("/cast Living Flame"),
    S("/cast Shattering Star"),
    S("/cast Deep Breath"),
    S("/cast Azure Strike"),
  }
  local aoe = {
    S("/cast Dragonrage"),
    S("/cast Fire Breath"),
    S("/cast Eternity Surge"),
    S("/cast Deep Breath"),
    S("/cast Pyre"),
    S("/cast Disintegrate"),
    S("/cast Living Flame"),
  }
  local safe = {
    S("/cast Obsidian Scales"),
    S("/cast Renewing Blaze"),
    S("/cast Fire Breath"),
    S("/cast Disintegrate"),
    S("/cast Living Flame"),
  }
  data["EVOKER_1467"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", ""),
    mkRotation(st, aoe, "", "/cast Dragonrage\n"),
    mkRotation(safe, aoe, "", "/cast Obsidian Scales\n")
  ))
end

do -- Preservation (1468)
  local st = {
    S("/cast Reversion"),
    S("/cast Echo"),
    S("/cast Living Flame"),
    S("/cast Verdant Embrace"),
    S("/cast Spiritbloom"),
    S("/cast Dream Breath"),
    S("/cast Time Dilation"),
    S("/cast Rewind"),
    S("/cast Zephyr"),
  }
  local aoe = {
    S("/cast Dream Breath"),
    S("/cast Spiritbloom"),
    S("/cast Reversion"),
    S("/cast Echo"),
    S("/cast [@cursor] Emerald Blossom"),
    S("/cast Rewind"),
    S("/cast Zephyr"),
  }
  local safe = {
    S("/cast Obsidian Scales"),
    S("/cast Time Dilation"),
    S("/cast Reversion"),
    S("/cast Living Flame"),
    S("/cast Dream Breath"),
  }
  data["EVOKER_1468"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast [@cursor] Emerald Blossom\n", {
    S("/cast Reversion"),
    S("/cast Echo"),
    S("/cast Living Flame"),
    S("/cast Dream Breath"),
    S("/cast Spiritbloom"),
    S("/cast Verdant Embrace"),
    S("/cast Time Dilation"),
    S("/cast Rewind"),
    S("/cast Zephyr"),
  }),
    mkRotation(st, aoe, "", "/cast Rewind\n", {
    S("/cast Reversion"),
    S("/cast Echo"),
    S("/cast Living Flame"),
    S("/cast Dream Breath"),
    S("/cast Spiritbloom"),
    S("/cast Verdant Embrace"),
    S("/cast Time Dilation"),
    S("/cast Rewind"),
    S("/cast Zephyr"),
  }),
    mkRotation(safe, aoe, "", "/cast Zephyr\n", {
    S("/cast Reversion"),
    S("/cast Echo"),
    S("/cast Living Flame"),
    S("/cast Dream Breath"),
    S("/cast Spiritbloom"),
    S("/cast Verdant Embrace"),
    S("/cast Time Dilation"),
    S("/cast Rewind"),
    S("/cast Zephyr"),
  })
  ))
end

do -- Augmentation (1473)
  local st = {
    S("/cast Breath of Eons"),
    S("/cast Ebon Might"),
    S("/cast Prescience"),
    S("/cast Upheaval"),
    S("/cast Blistering Scales"),
    S("/cast Living Flame"),
    S("/cast Disintegrate"),
    S("/cast Fire Breath"),
  }
  local aoe = {
    S("/cast Breath of Eons"),
    S("/cast Ebon Might"),
    S("/cast Prescience"),
    S("/cast Upheaval"),
    S("/cast Fire Breath"),
    S("/cast Living Flame"),
  }
  local safe = {
    S("/cast Obsidian Scales"),
    S("/cast Ebon Might"),
    S("/cast Prescience"),
    S("/cast Living Flame"),
  }
  data["EVOKER_1473"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", ""),
    mkRotation(st, aoe, "", "/cast Breath of Eons\n"),
    mkRotation(safe, aoe, "", "/cast Obsidian Scales\n")
  ))
end

-- =========================================================
-- HUNTER
-- =========================================================
do -- Beast Mastery (253)
  local st = {
    S("/cast Bestial Wrath"),
    S("/cast Call of the Wild"),
    S("/cast Kill Command"),
    S("/cast Barbed Shot"),
    S("/cast Dire Beast"),
    S("/cast Cobra Shot"),
    S("/cast Bloodshed"),
    S("/cast Death Chakram"),
  }
  local aoe = {
    S("/cast Bestial Wrath"),
    S("/cast Call of the Wild"),
    S("/cast Multi-Shot"),
    S("/cast Kill Command"),
    S("/cast Barbed Shot"),
    S("/cast Beast Cleave"),
    S("/cast Cobra Shot"),
    S("/cast Death Chakram"),
  }
  local safe = {
    S("/cast Exhilaration"),
    S("/cast Kill Command"),
    S("/cast Barbed Shot"),
    S("/cast Cobra Shot"),
    S("/cast Multi-Shot"),
  }
  data["HUNTER_253"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Exhilaration\n"),
    mkRotation(st, aoe, "", "/cast Bestial Wrath\n"),
    mkRotation(safe, aoe, "", "/cast Survival of the Fittest\n")
  ))
end

do -- Marksmanship (254)
  local st = {
    S("/cast Trueshot"),
    S("/cast Aimed Shot"),
    S("/cast Rapid Fire"),
    S("/cast Kill Shot"),
    S("/cast Arcane Shot"),
    S("/cast Steady Shot"),
    S("/cast Explosive Shot"),
    S("/cast Volley"),
  }
  local aoe = {
    S("/cast Trueshot"),
    S("/cast Volley"),
    S("/cast Rapid Fire"),
    S("/cast Multi-Shot"),
    S("/cast Aimed Shot"),
    S("/cast Explosive Shot"),
    S("/cast Arcane Shot"),
  }
  local safe = {
    S("/cast Exhilaration"),
    S("/cast Rapid Fire"),
    S("/cast Aimed Shot"),
    S("/cast Arcane Shot"),
  }
  data["HUNTER_254"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Exhilaration\n"),
    mkRotation(st, aoe, "", "/cast Trueshot\n"),
    mkRotation(safe, aoe, "", "/cast Survival of the Fittest\n")
  ))
end

do -- Survival (255)
  local st = {
    S("/cast Coordinated Assault"),
    S("/cast Wildfire Bomb"),
    S("/cast Kill Command"),
    S("/cast Raptor Strike"),
    S("/cast Mongoose Bite"),
    S("/cast Serpent Sting"),
    S("/cast Flanking Strike"),
    S("/cast Harpoon"),
  }
  local aoe = {
    S("/cast Coordinated Assault"),
    S("/cast Wildfire Bomb"),
    S("/cast Carve"),
    S("/cast Butchery"),
    S("/cast Kill Command"),
    S("/cast Raptor Strike"),
    S("/cast Serpent Sting"),
  }
  local safe = {
    S("/cast Exhilaration"),
    S("/cast Wildfire Bomb"),
    S("/cast Kill Command"),
    S("/cast Raptor Strike"),
  }
  data["HUNTER_255"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Exhilaration\n"),
    mkRotation(st, aoe, "", "/cast Coordinated Assault\n"),
    mkRotation(safe, aoe, "", "/cast Survival of the Fittest\n")
  ))
end

-- =========================================================
-- MAGE
-- =========================================================
do -- Arcane (62)
  local st = {
    S("/cast Arcane Surge"),
    S("/cast Touch of the Magi"),
    S("/cast Arcane Power"),
    S("/cast Arcane Blast"),
    S("/cast Arcane Missiles"),
    S("/cast Arcane Barrage"),
    S("/cast Nether Tempest"),
    S("/cast Evocation"),
  }
  local aoe = {
    S("/cast Arcane Surge"),
    S("/cast Touch of the Magi"),
    S("/cast Arcane Explosion"),
    S("/cast Arcane Barrage"),
    S("/cast Arcane Missiles"),
    S("/cast Nether Tempest"),
    S("/cast Arcane Blast"),
  }
  local safe = {
    S("/cast Ice Block"),
    S("/cast Alter Time"),
    S("/cast Arcane Blast"),
    S("/cast Arcane Missiles"),
    S("/cast Arcane Barrage"),
  }
  data["MAGE_62"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Alter Time\n"),
    mkRotation(st, aoe, "", "/cast Arcane Power\n"),
    mkRotation(safe, aoe, "", "/cast Ice Block\n")
  ))
end

do -- Fire (63)
  local st = {
    S("/cast Combustion"),
    S("/cast Fire Blast"),
    S("/cast Phoenix Flames"),
    S("/cast Pyroblast"),
    S("/cast Fireball"),
    S("/cast Scorch"),
    S("/cast Flamestrike"),
    S("/cast Meteor"),
  }
  local aoe = {
    S("/cast Combustion"),
    S("/cast Flamestrike"),
    S("/cast Phoenix Flames"),
    S("/cast Fire Blast"),
    S("/cast Fireball"),
    S("/cast Dragon's Breath"),
    S("/cast Meteor"),
  }
  local safe = {
    S("/cast Ice Block"),
    S("/cast Blazing Barrier"),
    S("/cast Fireball"),
    S("/cast Pyroblast"),
    S("/cast Flamestrike"),
  }
  data["MAGE_63"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Blazing Barrier\n"),
    mkRotation(st, aoe, "", "/cast Combustion\n"),
    mkRotation(safe, aoe, "", "/cast Ice Block\n")
  ))
end

do -- Frost (64)
  local st = {
    S("/cast Icy Veins"),
    S("/cast Frozen Orb"),
    S("/cast Blizzard"),
    S("/cast Flurry"),
    S("/cast Ice Lance"),
    S("/cast Frostbolt"),
    S("/cast Comet Storm"),
    S("/cast Ray of Frost"),
  }
  local aoe = {
    S("/cast Frozen Orb"),
    S("/cast Blizzard"),
    S("/cast Cone of Cold"),
    S("/cast Ice Lance"),
    S("/cast Flurry"),
    S("/cast Frostbolt"),
    S("/cast Comet Storm"),
  }
  local safe = {
    S("/cast Ice Block"),
    S("/cast Ice Barrier"),
    S("/cast Frozen Orb"),
    S("/cast Ice Lance"),
    S("/cast Frostbolt"),
  }
  data["MAGE_64"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Ice Barrier\n"),
    mkRotation(st, aoe, "", "/cast Icy Veins\n"),
    mkRotation(safe, aoe, "", "/cast Ice Block\n")
  ))
end

-- =========================================================
-- MONK
-- =========================================================
do -- Brewmaster (268)
  local st = {
    S("/cast Invoke Niuzao, the Black Ox"),
    S("/cast Keg Smash"),
    S("/cast Breath of Fire"),
    S("/cast Blackout Kick"),
    S("/cast Rising Sun Kick"),
    S("/cast Purifying Brew"),
    S("/cast Celestial Brew"),
    S("/cast Tiger Palm"),
  }
  local aoe = {
    S("/cast Invoke Niuzao, the Black Ox"),
    S("/cast Keg Smash"),
    S("/cast Breath of Fire"),
    S("/cast Spinning Crane Kick"),
    S("/cast Blackout Kick"),
    S("/cast Purifying Brew"),
    S("/cast Celestial Brew"),
  }
  local safe = {
    S("/cast Fortifying Brew"),
    S("/cast Dampen Harm"),
    S("/cast Celestial Brew"),
    S("/cast Purifying Brew"),
    S("/cast Keg Smash"),
    S("/cast Breath of Fire"),
  }
  data["MONK_268"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Purifying Brew\n"),
    mkRotation(st, aoe, "", "/cast Invoke Niuzao, the Black Ox\n"),
    mkRotation(safe, aoe, "", "/cast Fortifying Brew\n")
  ))
end

do -- Windwalker (269)
  local st = {
    S("/cast Invoke Xuen, the White Tiger"),
    S("/cast Storm, Earth, and Fire"),
    S("/cast Rising Sun Kick"),
    S("/cast Fists of Fury"),
    S("/cast Whirling Dragon Punch"),
    S("/cast Blackout Kick"),
    S("/cast Tiger Palm"),
    S("/cast Touch of Death"),
  }
  local aoe = {
    S("/cast Storm, Earth, and Fire"),
    S("/cast Fists of Fury"),
    S("/cast Spinning Crane Kick"),
    S("/cast Rising Sun Kick"),
    S("/cast Whirling Dragon Punch"),
    S("/cast Blackout Kick"),
    S("/cast Touch of Death"),
  }
  local safe = {
    S("/cast Touch of Karma"),
    S("/cast Fortifying Brew"),
    S("/cast Rising Sun Kick"),
    S("/cast Blackout Kick"),
    S("/cast Tiger Palm"),
  }
  data["MONK_269"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Touch of Karma\n"),
    mkRotation(st, aoe, "", "/cast Storm, Earth, and Fire\n"),
    mkRotation(safe, aoe, "", "/cast Fortifying Brew\n")
  ), mkProfiles(
    mkRotation(st, aoe, "", "/cast Leg Sweep\n"),
    mkRotation(st, aoe, "", "/cast Touch of Death\n"),
    mkRotation(safe, aoe, "", "/cast Touch of Karma\n")
  ))
end

do -- Mistweaver (270)
  local st = {
    S("/cast Renewing Mist"),
    S("/cast Enveloping Mist"),
    S("/cast Vivify"),
    S("/cast Essence Font"),
    S("/cast Life Cocoon"),
    S("/cast Revival"),
    S("/cast Thunder Focus Tea"),
    S("/cast Rising Sun Kick"),
    S("/cast Tiger Palm"),
  }
  local aoe = {
    S("/cast Essence Font"),
    S("/cast Renewing Mist"),
    S("/cast Vivify"),
    S("/cast Revival"),
    S("/cast Chi-Ji, the Red Crane"),
    S("/cast Life Cocoon"),
  }
  local safe = {
    S("/cast Fortifying Brew"),
    S("/cast Life Cocoon"),
    S("/cast Renewing Mist"),
    S("/cast Vivify"),
    S("/cast Enveloping Mist"),
  }
  data["MONK_270"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Life Cocoon\n", {
    S("/cast Renewing Mist"),
    S("/cast Vivify"),
    S("/cast Enveloping Mist"),
    S("/cast Essence Font"),
    S("/cast Thunder Focus Tea"),
    S("/cast Life Cocoon"),
    S("/cast Revival"),
    S("/cast Chi-Ji, the Red Crane"),
  }),
    mkRotation(st, aoe, "", "/cast Revival\n", {
    S("/cast Renewing Mist"),
    S("/cast Vivify"),
    S("/cast Enveloping Mist"),
    S("/cast Essence Font"),
    S("/cast Thunder Focus Tea"),
    S("/cast Life Cocoon"),
    S("/cast Revival"),
    S("/cast Chi-Ji, the Red Crane"),
  }),
    mkRotation(safe, aoe, "", "/cast Fortifying Brew\n", {
    S("/cast Renewing Mist"),
    S("/cast Vivify"),
    S("/cast Enveloping Mist"),
    S("/cast Essence Font"),
    S("/cast Thunder Focus Tea"),
    S("/cast Life Cocoon"),
    S("/cast Revival"),
    S("/cast Chi-Ji, the Red Crane"),
  })
  ))
end

-- =========================================================
-- PALADIN
-- =========================================================
do -- Holy (65)
  local st = {
    S("/cast Holy Shock"),
    S("/cast Word of Glory"),
    S("/cast Flash of Light"),
    S("/cast Light of Dawn"),
    S("/cast Holy Prism"),
    S("/cast Bestow Faith"),
    S("/cast Aura Mastery"),
    S("/cast Avenging Wrath"),
    S("/cast Lay on Hands"),
  }
  local aoe = {
    S("/cast Aura Mastery"),
    S("/cast Light of Dawn"),
    S("/cast Holy Shock"),
    S("/cast Holy Prism"),
    S("/cast Word of Glory"),
    S("/cast Flash of Light"),
  }
  local safe = {
    S("/cast Divine Shield"),
    S("/cast Blessing of Protection"),
    S("/cast Lay on Hands"),
    S("/cast Holy Shock"),
    S("/cast Word of Glory"),
    S("/cast Flash of Light"),
  }
  data["PALADIN_65"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Blessing of Sacrifice\n", {
    S("/cast Holy Shock"),
    S("/cast Word of Glory"),
    S("/cast Flash of Light"),
    S("/cast Light of Dawn"),
    S("/cast Holy Prism"),
    S("/cast Aura Mastery"),
    S("/cast Avenging Wrath"),
    S("/cast Blessing of Sacrifice"),
    S("/cast Lay on Hands"),
  }),
    mkRotation(st, aoe, "", "/cast Avenging Wrath\n", {
    S("/cast Holy Shock"),
    S("/cast Word of Glory"),
    S("/cast Flash of Light"),
    S("/cast Light of Dawn"),
    S("/cast Holy Prism"),
    S("/cast Aura Mastery"),
    S("/cast Avenging Wrath"),
    S("/cast Blessing of Sacrifice"),
    S("/cast Lay on Hands"),
  }),
    mkRotation(safe, aoe, "", "/cast Divine Shield\n", {
    S("/cast Holy Shock"),
    S("/cast Word of Glory"),
    S("/cast Flash of Light"),
    S("/cast Light of Dawn"),
    S("/cast Holy Prism"),
    S("/cast Aura Mastery"),
    S("/cast Avenging Wrath"),
    S("/cast Blessing of Sacrifice"),
    S("/cast Lay on Hands"),
  })
  ))
end

do -- Protection (66)
  local st = {
    S("/cast Avenging Wrath"),
    S("/cast Avenger's Shield"),
    S("/cast Judgment"),
    S("/cast Shield of the Righteous"),
    S("/cast Consecration"),
    S("/cast Hammer of the Righteous"),
    S("/cast Ardent Defender"),
    S("/cast Word of Glory"),
  }
  local aoe = {
    S("/cast Avenger's Shield"),
    S("/cast Consecration"),
    S("/cast Hammer of the Righteous"),
    S("/cast Judgment"),
    S("/cast Shield of the Righteous"),
    S("/cast Ardent Defender"),
  }
  local safe = {
    S("/cast Ardent Defender"),
    S("/cast Guardian of Ancient Kings"),
    S("/cast Word of Glory"),
    S("/cast Shield of the Righteous"),
    S("/cast Avenger's Shield"),
    S("/cast Consecration"),
  }
  data["PALADIN_66"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Shield of the Righteous\n"),
    mkRotation(st, aoe, "", "/cast Avenging Wrath\n"),
    mkRotation(safe, aoe, "", "/cast Ardent Defender\n")
  ))
end

do -- Retribution (70)
  local st = {
    S("/cast Avenging Wrath"),
    S("/cast Final Reckoning"),
    S("/cast Wake of Ashes"),
    S("/cast Blade of Justice"),
    S("/cast Judgment"),
    S("/cast Templar's Verdict"),
    S("/cast Divine Storm"),
    S("/cast Crusader Strike"),
  }
  local aoe = {
    S("/cast Avenging Wrath"),
    S("/cast Wake of Ashes"),
    S("/cast Divine Storm"),
    S("/cast Blade of Justice"),
    S("/cast Judgment"),
    S("/cast Crusader Strike"),
    S("/cast Templar's Verdict"),
  }
  local safe = {
    S("/cast Shield of Vengeance"),
    S("/cast Divine Protection"),
    S("/cast Word of Glory"),
    S("/cast Blade of Justice"),
    S("/cast Judgment"),
    S("/cast Templar's Verdict"),
  }
  data["PALADIN_70"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Word of Glory\n"),
    mkRotation(st, aoe, "", "/cast Avenging Wrath\n"),
    mkRotation(safe, aoe, "", "/cast Shield of Vengeance\n")
  ), mkProfiles(
    mkRotation(st, aoe, "", "/cast Hammer of Justice\n"),
    mkRotation(st, aoe, "", "/cast Avenging Wrath\n"),
    mkRotation(safe, aoe, "", "/cast Blessing of Protection\n")
  ))
end

-- =========================================================
-- PRIEST
-- =========================================================
do -- Discipline (256)
  local st = {
    S("/cast Power Word: Shield"),
    S("/cast Penance"),
    S("/cast Purge the Wicked"),
    S("/cast Schism"),
    S("/cast Smite"),
    S("/cast Power Word: Radiance"),
    S("/cast Pain Suppression"),
    S("/cast Rapture"),
  }
  local aoe = {
    S("/cast Power Word: Radiance"),
    S("/cast Power Word: Barrier"),
    S("/cast Penance"),
    S("/cast Purge the Wicked"),
    S("/cast Smite"),
    S("/cast Rapture"),
  }
  local safe = {
    S("/cast Desperate Prayer"),
    S("/cast Pain Suppression"),
    S("/cast Power Word: Shield"),
    S("/cast Flash Heal"),
    S("/cast Penance"),
  }
  data["PRIEST_256"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Pain Suppression\n", {
    S("/cast Power Word: Shield"),
    S("/cast Penance"),
    S("/cast Power Word: Radiance"),
    S("/cast Flash Heal"),
    S("/cast Purge the Wicked"),
    S("/cast Smite"),
    S("/cast Pain Suppression"),
    S("/cast Power Word: Barrier"),
    S("/cast Rapture"),
  }),
    mkRotation(st, aoe, "", "/cast Power Word: Barrier\n", {
    S("/cast Power Word: Shield"),
    S("/cast Penance"),
    S("/cast Power Word: Radiance"),
    S("/cast Flash Heal"),
    S("/cast Purge the Wicked"),
    S("/cast Smite"),
    S("/cast Pain Suppression"),
    S("/cast Power Word: Barrier"),
    S("/cast Rapture"),
  }),
    mkRotation(safe, aoe, "", "/cast Desperate Prayer\n", {
    S("/cast Power Word: Shield"),
    S("/cast Penance"),
    S("/cast Power Word: Radiance"),
    S("/cast Flash Heal"),
    S("/cast Purge the Wicked"),
    S("/cast Smite"),
    S("/cast Pain Suppression"),
    S("/cast Power Word: Barrier"),
    S("/cast Rapture"),
  })
  ))
end

do -- Holy (257)
  local st = {
    S("/cast Holy Word: Serenity"),
    S("/cast Heal"),
    S("/cast Flash Heal"),
    S("/cast Prayer of Mending"),
    S("/cast Renew"),
    S("/cast Holy Word: Sanctify"),
    S("/cast Divine Hymn"),
    S("/cast Guardian Spirit"),
  }
  local aoe = {
    S("/cast Holy Word: Sanctify"),
    S("/cast Prayer of Healing"),
    S("/cast Prayer of Mending"),
    S("/cast Renew"),
    S("/cast Divine Hymn"),
    S("/cast Guardian Spirit"),
  }
  local safe = {
    S("/cast Desperate Prayer"),
    S("/cast Guardian Spirit"),
    S("/cast Holy Word: Serenity"),
    S("/cast Flash Heal"),
    S("/cast Renew"),
  }
  data["PRIEST_257"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Guardian Spirit\n", {
    S("/cast Holy Word: Serenity"),
    S("/cast Prayer of Mending"),
    S("/cast Flash Heal"),
    S("/cast Heal"),
    S("/cast Holy Word: Sanctify"),
    S("/cast Prayer of Healing"),
    S("/cast Guardian Spirit"),
    S("/cast Divine Hymn"),
    S("/cast Renew"),
  }),
    mkRotation(st, aoe, "", "/cast Divine Hymn\n", {
    S("/cast Holy Word: Serenity"),
    S("/cast Prayer of Mending"),
    S("/cast Flash Heal"),
    S("/cast Heal"),
    S("/cast Holy Word: Sanctify"),
    S("/cast Prayer of Healing"),
    S("/cast Guardian Spirit"),
    S("/cast Divine Hymn"),
    S("/cast Renew"),
  }),
    mkRotation(safe, aoe, "", "/cast Desperate Prayer\n", {
    S("/cast Holy Word: Serenity"),
    S("/cast Prayer of Mending"),
    S("/cast Flash Heal"),
    S("/cast Heal"),
    S("/cast Holy Word: Sanctify"),
    S("/cast Prayer of Healing"),
    S("/cast Guardian Spirit"),
    S("/cast Divine Hymn"),
    S("/cast Renew"),
  })
  ))
end

do -- Shadow (258)
  local st = {
    S("/cast Power Infusion"),
    S("/cast Vampiric Touch"),
    S("/cast Shadow Word: Pain"),
    S("/cast Devouring Plague"),
    S("/cast Mind Blast"),
    S("/cast Void Eruption"),
    S("/cast Mind Flay"),
    S("/cast Shadow Crash"),
    S("/cast Dark Ascension"),
  }
  local aoe = {
    S("/cast Shadow Crash"),
    S("/cast Vampiric Touch"),
    S("/cast Shadow Word: Pain"),
    S("/cast Devouring Plague"),
    S("/cast Mind Sear"),
    S("/cast Mind Blast"),
    S("/cast Void Eruption"),
  }
  local safe = {
    S("/cast Dispersion"),
    S("/cast Desperate Prayer"),
    S("/cast Vampiric Touch"),
    S("/cast Devouring Plague"),
    S("/cast Mind Blast"),
    S("/cast Mind Flay"),
  }
  data["PRIEST_258"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Dispersion\n"),
    mkRotation(st, aoe, "", "/cast Power Infusion\n"),
    mkRotation(safe, aoe, "", "/cast Dispersion\n")
  ), mkProfiles(
    mkRotation(st, aoe, "", "/cast Psychic Scream\n"),
    mkRotation(st, aoe, "", "/cast Silence\n"),
    mkRotation(safe, aoe, "", "/cast Dispersion\n")
  ))
end

-- =========================================================
-- ROGUE
-- =========================================================
do -- Assassination (259)
  local st = {
    S("/cast Deathmark"),
    S("/cast Kingsbane"),
    S("/cast Garrote"),
    S("/cast Rupture"),
    S("/cast Mutilate"),
    S("/cast Envenom"),
    S("/cast Shiv"),
    S("/cast Crimson Tempest"),
    S("/cast Toxic Blade"),
  }
  local aoe = {
    S("/cast Deathmark"),
    S("/cast Crimson Tempest"),
    S("/cast Fan of Knives"),
    S("/cast Rupture"),
    S("/cast Garrote"),
    S("/cast Envenom"),
    S("/cast Shiv"),
  }
  local safe = {
    S("/cast Evasion"),
    S("/cast Cloak of Shadows"),
    S("/cast Garrote"),
    S("/cast Rupture"),
    S("/cast Mutilate"),
    S("/cast Envenom"),
  }
  data["ROGUE_259"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Evasion\n"),
    mkRotation(st, aoe, "", "/cast Deathmark\n"),
    mkRotation(safe, aoe, "", "/cast Cloak of Shadows\n")
  ), mkProfiles(
    mkRotation(st, aoe, "", "/cast Kidney Shot\n"),
    mkRotation(st, aoe, "", "/cast Blind\n"),
    mkRotation(safe, aoe, "", "/cast Evasion\n")
  ))
end

do -- Outlaw (260)
  local st = {
    S("/cast Adrenaline Rush"),
    S("/cast Roll the Bones"),
    S("/cast Between the Eyes"),
    S("/cast Dispatch"),
    S("/cast Sinister Strike"),
    S("/cast Pistol Shot"),
    S("/cast Blade Flurry"),
    S("/cast Killing Spree"),
  }
  local aoe = {
    S("/cast Blade Flurry"),
    S("/cast Adrenaline Rush"),
    S("/cast Roll the Bones"),
    S("/cast Between the Eyes"),
    S("/cast Dispatch"),
    S("/cast Sinister Strike"),
    S("/cast Pistol Shot"),
  }
  local safe = {
    S("/cast Evasion"),
    S("/cast Cloak of Shadows"),
    S("/cast Blade Flurry"),
    S("/cast Sinister Strike"),
    S("/cast Dispatch"),
  }
  data["ROGUE_260"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Evasion\n"),
    mkRotation(st, aoe, "", "/cast Adrenaline Rush\n"),
    mkRotation(safe, aoe, "", "/cast Cloak of Shadows\n")
  ))
end

do -- Subtlety (261)
  local st = {
    S("/cast Shadow Dance"),
    S("/cast Symbols of Death"),
    S("/cast Secret Technique"),
    S("/cast Shadowstrike"),
    S("/cast Eviscerate"),
    S("/cast Backstab"),
    S("/cast Black Powder"),
    S("/cast Shadow Blades"),
  }
  local aoe = {
    S("/cast Shadow Dance"),
    S("/cast Black Powder"),
    S("/cast Shuriken Storm"),
    S("/cast Secret Technique"),
    S("/cast Shadowstrike"),
    S("/cast Eviscerate"),
  }
  local safe = {
    S("/cast Evasion"),
    S("/cast Cloak of Shadows"),
    S("/cast Shadowstrike"),
    S("/cast Eviscerate"),
    S("/cast Backstab"),
  }
  data["ROGUE_261"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Evasion\n"),
    mkRotation(st, aoe, "", "/cast Shadow Blades\n"),
    mkRotation(safe, aoe, "", "/cast Cloak of Shadows\n")
  ), mkProfiles(
    mkRotation(st, aoe, "", "/cast Kidney Shot\n"),
    mkRotation(st, aoe, "", "/cast Smoke Bomb\n"),
    mkRotation(safe, aoe, "", "/cast Evasion\n")
  ))
end

-- =========================================================
-- SHAMAN
-- =========================================================
do -- Elemental (262)
  local st = {
    S("/cast Stormkeeper"),
    S("/cast Fire Elemental"),
    S("/cast Flame Shock"),
    S("/cast Lava Burst"),
    S("/cast Earth Shock"),
    S("/cast Lightning Bolt"),
    S("/cast Icefury"),
    S("/cast Primordial Wave"),
    S("/cast Elemental Blast"),
  }
  local aoe = {
    S("/cast Stormkeeper"),
    S("/cast Fire Elemental"),
    S("/cast Flame Shock"),
    S("/cast Earthquake"),
    S("/cast Chain Lightning"),
    S("/cast Lava Burst"),
    S("/cast Primordial Wave"),
  }
  local safe = {
    S("/cast Astral Shift"),
    S("/cast Earth Shield"),
    S("/cast Flame Shock"),
    S("/cast Lava Burst"),
    S("/cast Lightning Bolt"),
  }
  data["SHAMAN_262"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Astral Shift\n"),
    mkRotation(st, aoe, "", "/cast Stormkeeper\n"),
    mkRotation(safe, aoe, "", "/cast Astral Shift\n")
  ))
end

do -- Enhancement (263)
  local st = {
    S("/cast Feral Spirit"),
    S("/cast Doom Winds"),
    S("/cast Stormstrike"),
    S("/cast Lava Lash"),
    S("/cast Lightning Bolt"),
    S("/cast Crash Lightning"),
    S("/cast Flame Shock"),
    S("/cast Primordial Wave"),
    S("/cast Ascendance"),
  }
  local aoe = {
    S("/cast Feral Spirit"),
    S("/cast Crash Lightning"),
    S("/cast Chain Lightning"),
    S("/cast Stormstrike"),
    S("/cast Lava Lash"),
    S("/cast Primordial Wave"),
    S("/cast Flame Shock"),
  }
  local safe = {
    S("/cast Astral Shift"),
    S("/cast Stone Bulwark Totem"),
    S("/cast Stormstrike"),
    S("/cast Lava Lash"),
    S("/cast Crash Lightning"),
  }
  data["SHAMAN_263"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Astral Shift\n"),
    mkRotation(st, aoe, "", "/cast Doom Winds\n"),
    mkRotation(safe, aoe, "", "/cast Astral Shift\n")
  ), mkProfiles(
    mkRotation(st, aoe, "", "/cast Capacitor Totem\n"),
    mkRotation(st, aoe, "", "/cast Hex\n"),
    mkRotation(safe, aoe, "", "/cast Astral Shift\n")
  ))
end

do -- Restoration (264)
  local st = {
    S("/cast Riptide"),
    S("/cast Healing Surge"),
    S("/cast Healing Wave"),
    S("/cast Earth Shield"),
    S("/cast Healing Stream Totem"),
    S("/cast Spirit Link Totem"),
    S("/cast Ascendance"),
    S("/cast Nature's Swiftness"),
    S("/cast Chain Heal"),
  }
  local aoe = {
    S("/cast Healing Rain"),
    S("/cast Chain Heal"),
    S("/cast Healing Stream Totem"),
    S("/cast Riptide"),
    S("/cast Spirit Link Totem"),
    S("/cast Ascendance"),
    S("/cast Healing Surge"),
  }
  local safe = {
    S("/cast Astral Shift"),
    S("/cast Nature's Swiftness"),
    S("/cast Riptide"),
    S("/cast Healing Surge"),
    S("/cast Chain Heal"),
    S("/cast Spirit Link Totem"),
  }
  data["SHAMAN_264"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Spirit Link Totem\n", {
    S("/cast Riptide"),
    S("/cast Healing Surge"),
    S("/cast Healing Wave"),
    S("/cast Chain Heal"),
    S("/cast Healing Rain"),
    S("/cast Healing Stream Totem"),
    S("/cast Nature's Swiftness"),
    S("/cast Spirit Link Totem"),
    S("/cast Ascendance"),
  }),
    mkRotation(st, aoe, "", "/cast Ascendance\n", {
    S("/cast Riptide"),
    S("/cast Healing Surge"),
    S("/cast Healing Wave"),
    S("/cast Chain Heal"),
    S("/cast Healing Rain"),
    S("/cast Healing Stream Totem"),
    S("/cast Nature's Swiftness"),
    S("/cast Spirit Link Totem"),
    S("/cast Ascendance"),
  }),
    mkRotation(safe, aoe, "", "/cast Astral Shift\n", {
    S("/cast Riptide"),
    S("/cast Healing Surge"),
    S("/cast Healing Wave"),
    S("/cast Chain Heal"),
    S("/cast Healing Rain"),
    S("/cast Healing Stream Totem"),
    S("/cast Nature's Swiftness"),
    S("/cast Spirit Link Totem"),
    S("/cast Ascendance"),
  })
  ))
end

-- =========================================================
-- WARLOCK
-- =========================================================
do -- Affliction (265)
  local st = {
    S("/cast Summon Darkglare"),
    S("/cast Haunt"),
    S("/cast Agony"),
    S("/cast Corruption"),
    S("/cast Unstable Affliction"),
    S("/cast Siphon Life"),
    S("/cast Malefic Rapture"),
    S("/cast Drain Soul"),
    S("/cast Soul Rot"),
  }
  local aoe = {
    S("/cast Vile Taint"),
    S("/cast Agony"),
    S("/cast Corruption"),
    S("/cast Seed of Corruption"),
    S("/cast Malefic Rapture"),
    S("/cast Soul Rot"),
    S("/cast Summon Darkglare"),
  }
  local safe = {
    S("/cast Unending Resolve"),
    S("/cast Dark Pact"),
    S("/cast Agony"),
    S("/cast Corruption"),
    S("/cast Malefic Rapture"),
    S("/cast Drain Soul"),
  }
  data["WARLOCK_265"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Dark Pact\n"),
    mkRotation(st, aoe, "", "/cast Summon Darkglare\n"),
    mkRotation(safe, aoe, "", "/cast Unending Resolve\n")
  ), mkProfiles(
    mkRotation(st, aoe, "", "/cast Fear\n"),
    mkRotation(st, aoe, "", "/cast Mortal Coil\n"),
    mkRotation(safe, aoe, "", "/cast Dark Pact\n")
  ))
end

do -- Demonology (266)
  local st = {
    S("/cast Summon Demonic Tyrant"),
    S("/cast Call Dreadstalkers"),
    S("/cast Hand of Gul'dan"),
    S("/cast Demonbolt"),
    S("/cast Shadow Bolt"),
    S("/cast Power Siphon"),
    S("/cast Grimoire: Felguard"),
    S("/cast Implosion"),
    S("/cast Doom"),
  }
  local aoe = {
    S("/cast Summon Demonic Tyrant"),
    S("/cast Call Dreadstalkers"),
    S("/cast Hand of Gul'dan"),
    S("/cast Implosion"),
    S("/cast Demonbolt"),
    S("/cast Shadow Bolt"),
    S("/cast Guillotine"),
  }
  local safe = {
    S("/cast Unending Resolve"),
    S("/cast Dark Pact"),
    S("/cast Call Dreadstalkers"),
    S("/cast Hand of Gul'dan"),
    S("/cast Shadow Bolt"),
    S("/cast Demonbolt"),
  }
  data["WARLOCK_266"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Dark Pact\n"),
    mkRotation(st, aoe, "", "/cast Summon Demonic Tyrant\n"),
    mkRotation(safe, aoe, "", "/cast Unending Resolve\n")
  ))
end

do -- Destruction (267)
  local st = {
    S("/cast Summon Infernal"),
    S("/cast Immolate"),
    S("/cast Conflagrate"),
    S("/cast Chaos Bolt"),
    S("/cast Incinerate"),
    S("/cast Havoc"),
    S("/cast Shadowburn"),
    S("/cast Cataclysm"),
    S("/cast Dimensional Rift"),
  }
  local aoe = {
    S("/cast Summon Infernal"),
    S("/cast Cataclysm"),
    S("/cast Rain of Fire"),
    S("/cast Havoc"),
    S("/cast Immolate"),
    S("/cast Conflagrate"),
    S("/cast Incinerate"),
  }
  local safe = {
    S("/cast Unending Resolve"),
    S("/cast Dark Pact"),
    S("/cast Immolate"),
    S("/cast Conflagrate"),
    S("/cast Incinerate"),
    S("/cast Chaos Bolt"),
  }
  data["WARLOCK_267"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Dark Pact\n"),
    mkRotation(st, aoe, "", "/cast Summon Infernal\n"),
    mkRotation(safe, aoe, "", "/cast Unending Resolve\n")
  ))
end

-- =========================================================
-- WARRIOR
-- =========================================================
do -- Arms (71)
  local st = {
    S("/cast Avatar"),
    S("/cast Colossus Smash"),
    S("/cast Warbreaker"),
    S("/cast Mortal Strike"),
    S("/cast Overpower"),
    S("/cast Execute"),
    S("/cast Slam"),
    S("/cast Rend"),
    S("/cast Bladestorm"),
  }
  local aoe = {
    S("/cast Avatar"),
    S("/cast Warbreaker"),
    S("/cast Bladestorm"),
    S("/cast Cleave"),
    S("/cast Whirlwind"),
    S("/cast Mortal Strike"),
    S("/cast Execute"),
  }
  local safe = {
    S("/cast Die by the Sword"),
    S("/cast Rallying Cry"),
    S("/cast Mortal Strike"),
    S("/cast Overpower"),
    S("/cast Execute"),
    S("/cast Slam"),
  }
  data["WARRIOR_71"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Rallying Cry\n"),
    mkRotation(st, aoe, "", "/cast Avatar\n"),
    mkRotation(safe, aoe, "", "/cast Die by the Sword\n")
  ), mkProfiles(
    mkRotation(st, aoe, "", "/cast Intimidating Shout\n"),
    mkRotation(st, aoe, "", "/cast Storm Bolt\n"),
    mkRotation(safe, aoe, "", "/cast Die by the Sword\n")
  ))
end

do -- Fury (72)
  local st = {
    S("/cast Recklessness"),
    S("/cast Odyn's Fury"),
    S("/cast Rampage"),
    S("/cast Raging Blow"),
    S("/cast Bloodthirst"),
    S("/cast Execute"),
    S("/cast Whirlwind"),
    S("/cast Dragon Roar"),
    S("/cast Enraged Regeneration"),
  }
  local aoe = {
    S("/cast Recklessness"),
    S("/cast Odyn's Fury"),
    S("/cast Whirlwind"),
    S("/cast Rampage"),
    S("/cast Raging Blow"),
    S("/cast Bloodthirst"),
    S("/cast Dragon Roar"),
  }
  local safe = {
    S("/cast Enraged Regeneration"),
    S("/cast Rallying Cry"),
    S("/cast Rampage"),
    S("/cast Bloodthirst"),
    S("/cast Raging Blow"),
    S("/cast Whirlwind"),
  }
  data["WARRIOR_72"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Enraged Regeneration\n"),
    mkRotation(st, aoe, "", "/cast Recklessness\n"),
    mkRotation(safe, aoe, "", "/cast Rallying Cry\n")
  ))
end

do -- Protection (73)
  local st = {
    S("/cast Avatar"),
    S("/cast Shield Wall"),
    S("/cast Shield Slam"),
    S("/cast Thunder Clap"),
    S("/cast Revenge"),
    S("/cast Ignore Pain"),
    S("/cast Shield Block"),
    S("/cast Last Stand"),
    S("/cast Demoralizing Shout"),
  }
  local aoe = {
    S("/cast Avatar"),
    S("/cast Thunder Clap"),
    S("/cast Shield Slam"),
    S("/cast Revenge"),
    S("/cast Ignore Pain"),
    S("/cast Shield Block"),
    S("/cast Shockwave"),
  }
  local safe = {
    S("/cast Shield Wall"),
    S("/cast Last Stand"),
    S("/cast Ignore Pain"),
    S("/cast Shield Block"),
    S("/cast Shield Slam"),
    S("/cast Thunder Clap"),
    S("/cast Revenge"),
  }
  data["WARRIOR_73"] = mkAllModes(mkProfiles(
    mkRotation(st, aoe, "", "/cast Ignore Pain\n"),
    mkRotation(st, aoe, "", "/cast Avatar\n"),
    mkRotation(safe, aoe, "", "/cast Shield Wall\n")
  ))
end

-- =========================================================
-- PRIEST already, remaining classes:
-- (This file includes all base classes/specs for modern retail.)
-- =========================================================

-- =========================================================
-- RANGER NOTE:
-- If you want me to also add the missing retail classes (if any new class/spec is added by a patch),
-- just tell me and I’ll extend this file.
-- =========================================================

SW:RegisterClassPack("ALL_SPECS", data)
