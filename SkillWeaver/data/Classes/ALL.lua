-- Data/Classes/ALL.lua
SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver

-- Helpers
local function S(cmd) return { command = cmd } end

local function mkRotation(stSteps, aoeSteps, intMacro, utilMacro, healSteps)
  return {
    ST   = { steps = stSteps },
    AOE  = { steps = aoeSteps and #aoeSteps > 0 and aoeSteps or stSteps },
    INT  = { macro = intMacro or "" },  -- loader/engine will fallback to class default if empty
    UTIL = { macro = utilMacro or "" },
    HEAL = { steps = healSteps or nil },
  }
end

-- Profiles:
-- Balanced: full list
-- HighPerformance: front-load cooldowns / throughput first
-- Safe: short list with sustain/defensive bias
local function mkProfiles(baseRot, hpRot, safeRot)
  return {
    Balanced = baseRot,
    HighPerformance = hpRot or baseRot,
    Safe = safeRot or baseRot,
  }
end

-- Modes: for now map the same profiles into each content type.
-- You can later specialize PvP or Raid by swapping only that mode table.
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

-- =======================
-- DEATH KNIGHT
-- =======================
do
  -- Blood (250)
  local st = { S("/cast Marrowrend"), S("/cast Death Strike"), S("/cast Heart Strike"), S("/cast Blood Boil") }
  local aoe = { S("/cast Death and Decay"), S("/cast Blood Boil"), S("/cast Heart Strike"), S("/cast Death Strike") }
  local base = mkRotation(st, aoe, "/cast [harm] Mind Freeze\n", "/cast Rune Tap\n")
  local hp   = mkRotation({ S("/cast Dancing Rune Weapon"), S("/cast Death and Decay"), S("/cast Marrowrend"), S("/cast Blood Boil"), S("/cast Heart Strike"), S("/cast Death Strike") }, aoe, nil, "/cast Vampiric Blood\n")
  local safe = mkRotation({ S("/cast Death Strike"), S("/cast Marrowrend"), S("/cast Heart Strike") }, { S("/cast Death Strike"), S("/cast Blood Boil"), S("/cast Heart Strike") }, nil, "/cast Icebound Fortitude\n")
  data["DEATHKNIGHT_250"] = mkAllModes(mkProfiles(base, hp, safe))
end

do
  -- Frost (251)
  local st = { S("/cast Pillar of Frost"), S("/cast Obliterate"), S("/cast Howling Blast"), S("/cast Frost Strike"), S("/cast Remorseless Winter") }
  local aoe = { S("/cast Remorseless Winter"), S("/cast Howling Blast"), S("/cast Frost Strike"), S("/cast Obliterate") }
  local base = mkRotation(st, aoe, "/cast [harm] Mind Freeze\n", "")
  local hp = mkRotation({ S("/cast Pillar of Frost"), S("/cast Empower Rune Weapon"), S("/cast Remorseless Winter"), S("/cast Obliterate"), S("/cast Howling Blast"), S("/cast Frost Strike") }, aoe, nil, "")
  local safe = mkRotation({ S("/cast Remorseless Winter"), S("/cast Obliterate"), S("/cast Frost Strike") }, { S("/cast Remorseless Winter"), S("/cast Howling Blast"), S("/cast Frost Strike") }, nil, "/cast Anti-Magic Shell\n")
  data["DEATHKNIGHT_251"] = mkAllModes(mkProfiles(base, hp, safe))
end

do
  -- Unholy (252)
  local st = { S("/cast Outbreak"), S("/cast Dark Transformation"), S("/cast Apocalypse"), S("/cast Festering Strike"), S("/cast Scourge Strike"), S("/cast Death Coil") }
  local aoe = { S("/cast Outbreak"), S("/cast Death and Decay"), S("/cast Dark Transformation"), S("/cast Epidemic"), S("/cast Scourge Strike"), S("/cast Festering Strike") }
  local base = mkRotation(st, aoe, "/cast [harm] Mind Freeze\n", "")
  local hp = mkRotation({ S("/cast Army of the Dead"), S("/cast Unholy Assault"), S("/cast Dark Transformation"), S("/cast Apocalypse"), S("/cast Scourge Strike"), S("/cast Death Coil") }, aoe, nil, "")
  local safe = mkRotation({ S("/cast Death Strike"), S("/cast Outbreak"), S("/cast Scourge Strike"), S("/cast Death Coil") }, { S("/cast Death Strike"), S("/cast Epidemic"), S("/cast Scourge Strike") }, nil, "/cast Anti-Magic Shell\n")
  data["DEATHKNIGHT_252"] = mkAllModes(mkProfiles(base, hp, safe))
end

-- =======================
-- DEMON HUNTER
-- =======================
do
  -- Havoc (577)
  local st = { S("/cast Eye Beam"), S("/cast Blade Dance"), S("/cast Chaos Strike"), S("/cast Demon's Bite") }
  local aoe = { S("/cast Eye Beam"), S("/cast Blade Dance"), S("/cast Immolation Aura"), S("/cast Chaos Strike") }
  local base = mkRotation(st, aoe, "/cast [harm] Disrupt\n", "/cast Blur\n")
  local hp = mkRotation({ S("/cast Metamorphosis"), S("/cast Eye Beam"), S("/cast Essence Break"), S("/cast Blade Dance"), S("/cast Chaos Strike") }, aoe, nil, "/cast Darkness\n")
  local safe = mkRotation({ S("/cast Blur"), S("/cast Chaos Strike"), S("/cast Blade Dance") }, { S("/cast Blur"), S("/cast Immolation Aura"), S("/cast Blade Dance") }, nil, "/cast Darkness\n")
  data["DEMONHUNTER_577"] = mkAllModes(mkProfiles(base, hp, safe))
end

do
  -- Vengeance (581)
  local st = { S("/cast Immolation Aura"), S("/cast Soul Cleave"), S("/cast Fracture"), S("/cast Shear") }
  local aoe = { S("/cast Immolation Aura"), S("/cast Sigil of Flame"), S("/cast Soul Cleave"), S("/cast Spirit Bomb") }
  local base = mkRotation(st, aoe, "/cast [harm] Disrupt\n", "/cast Demon Spikes\n")
  local hp = mkRotation({ S("/cast Fel Devastation"), S("/cast Immolation Aura"), S("/cast Sigil of Flame"), S("/cast Spirit Bomb"), S("/cast Soul Cleave") }, aoe, nil, "/cast Metamorphosis\n")
  local safe = mkRotation({ S("/cast Demon Spikes"), S("/cast Soul Cleave"), S("/cast Immolation Aura") }, { S("/cast Demon Spikes"), S("/cast Spirit Bomb"), S("/cast Immolation Aura") }, nil, "/cast Metamorphosis\n")
  data["DEMONHUNTER_581"] = mkAllModes(mkProfiles(base, hp, safe))
end

-- =======================
-- DRUID
-- =======================
do
  -- Balance (102)
  local st = { S("/cast Sunfire"), S("/cast Moonfire"), S("/cast Starsurge"), S("/cast Wrath"), S("/cast Starfire") }
  local aoe = { S("/cast Sunfire"), S("/cast Starfall"), S("/cast Starfire"), S("/cast Moonfire") }
  local base = mkRotation(st, aoe, "/cast [harm] Skull Bash\n", "/cast Barkskin\n")
  local hp = mkRotation({ S("/cast Incarnation: Chosen of Elune"), S("/cast Starfall"), S("/cast Starsurge"), S("/cast Starfire"), S("/cast Wrath") }, aoe, nil, "/cast Barkskin\n")
  local safe = mkRotation({ S("/cast Barkskin"), S("/cast Moonfire"), S("/cast Sunfire"), S("/cast Wrath") }, { S("/cast Barkskin"), S("/cast Sunfire"), S("/cast Starfall"), S("/cast Starfire") }, nil, "/cast Renewal\n")
  data["DRUID_102"] = mkAllModes(mkProfiles(base, hp, safe))
end

do
  -- Feral (103)
  local st = { S("/cast Rake"), S("/cast Rip"), S("/cast Ferocious Bite"), S("/cast Shred") }
  local aoe = { S("/cast Thrash"), S("/cast Swipe"), S("/cast Rake"), S("/cast Rip") }
  local base = mkRotation(st, aoe, "/cast [harm] Skull Bash\n", "/cast Survival Instincts\n")
  local hp = mkRotation({ S("/cast Berserk"), S("/cast Tiger's Fury"), S("/cast Rake"), S("/cast Rip"), S("/cast Ferocious Bite") }, aoe, nil, "/cast Survival Instincts\n")
  local safe = mkRotation({ S("/cast Survival Instincts"), S("/cast Rake"), S("/cast Rip"), S("/cast Shred") }, { S("/cast Survival Instincts"), S("/cast Thrash"), S("/cast Swipe") }, nil, "/cast Barkskin\n")
  data["DRUID_103"] = mkAllModes(mkProfiles(base, hp, safe))
end

do
  -- Guardian (104)
  local st = { S("/cast Thrash"), S("/cast Mangle"), S("/cast Ironfur"), S("/cast Maul") }
  local aoe = { S("/cast Thrash"), S("/cast Swipe"), S("/cast Ironfur"), S("/cast Mangle") }
  local base = mkRotation(st, aoe, "/cast [harm] Skull Bash\n", "/cast Barkskin\n")
  local hp = mkRotation({ S("/cast Incarnation: Guardian of Ursoc"), S("/cast Thrash"), S("/cast Ironfur"), S("/cast Mangle"), S("/cast Maul") }, aoe, nil, "/cast Survival Instincts\n")
  local safe = mkRotation({ S("/cast Ironfur"), S("/cast Frenzied Regeneration"), S("/cast Thrash"), S("/cast Mangle") }, { S("/cast Ironfur"), S("/cast Frenzied Regeneration"), S("/cast Thrash"), S("/cast Swipe") }, nil, "/cast Survival Instincts\n")
  data["DRUID_104"] = mkAllModes(mkProfiles(base, hp, safe))
end

do
  -- Restoration (105)
  local st = { S("/cast Sunfire"), S("/cast Moonfire"), S("/cast Wrath"), S("/cast Starfire") }
  local aoe = { S("/cast Sunfire"), S("/cast Starfire"), S("/cast Swipe") }
  local heal = { S("/cast Rejuvenation"), S("/cast Regrowth"), S("/cast Swiftmend"), S("/cast Lifebloom"), S("/cast Wild Growth") }
  
  local base = mkRotation(st, aoe, "/cast [harm] Skull Bash\n", "/cast [@cursor] Efflorescence\n", heal)
  local hp = mkRotation(st, aoe, nil, "/cast Tranquility\n", heal)
  local safe = mkRotation(st, aoe, nil, "/cast Ironbark\n", heal)
  data["DRUID_105"] = mkAllModes(mkProfiles(base, hp, safe))
end

-- =======================
-- EVOKER
-- =======================
do
  -- Devastation (1467)
  local st = { S("/cast Fire Breath"), S("/cast Disintegrate"), S("/cast Living Flame"), S("/cast Eternity Surge") }
  local aoe = { S("/cast Fire Breath"), S("/cast Eternity Surge"), S("/cast Pyre"), S("/cast Disintegrate") }
  local base = mkRotation(st, aoe, "/cast [harm] Quell\n", "")
  local hp = mkRotation({ S("/cast Dragonrage"), S("/cast Fire Breath"), S("/cast Eternity Surge"), S("/cast Disintegrate") }, aoe, nil, "")
  local safe = mkRotation({ S("/cast Obsidian Scales"), S("/cast Living Flame"), S("/cast Disintegrate") }, { S("/cast Obsidian Scales"), S("/cast Pyre"), S("/cast Disintegrate") }, nil, "")
  data["EVOKER_1467"] = mkAllModes(mkProfiles(base, hp, safe))
end

do
  -- Preservation (1468)
  local st = { S("/cast Living Flame"), S("/cast Azure Strike"), S("/cast Disintegrate") }
  local aoe = { S("/cast Deep Breath"), S("/cast Azure Strike"), S("/cast Living Flame") }
  local heal = { S("/cast Echo"), S("/cast Reversion"), S("/cast Verdant Embrace"), S("/cast Spiritbloom"), S("/cast Dream Breath") }
  
  local base = mkRotation(st, aoe, "/cast [harm] Quell\n", "/cast [@cursor] Emerald Blossom\n", heal)
  local hp = mkRotation(st, aoe, nil, "/cast Zephyr\n", heal)
  local safe = mkRotation(st, aoe, nil, "/cast Zephyr\n", heal)
  data["EVOKER_1468"] = mkAllModes(mkProfiles(base, hp, safe))
end

do
  -- Augmentation (1473)
  local st = { S("/cast Ebon Might"), S("/cast Prescience"), S("/cast Upheaval"), S("/cast Living Flame") }
  local aoe = { S("/cast Ebon Might"), S("/cast Prescience"), S("/cast Breath of Eons"), S("/cast Upheaval") }
  local base = mkRotation(st, aoe, "/cast [harm] Quell\n", "")
  local hp = mkRotation({ S("/cast Breath of Eons"), S("/cast Ebon Might"), S("/cast Prescience"), S("/cast Upheaval") }, aoe, nil, "")
  local safe = mkRotation({ S("/cast Obsidian Scales"), S("/cast Ebon Might"), S("/cast Living Flame") }, aoe, nil, "")
  data["EVOKER_1473"] = mkAllModes(mkProfiles(base, hp, safe))
end

-- =======================
-- HUNTER (Generated)
-- =======================
do -- BM (253)
   local st = { S("/cast Bestial Wrath"), S("/cast Kill Command"), S("/cast Barbed Shot"), S("/cast Cobra Shot") }
   local aoe = { S("/cast Bestial Wrath"), S("/cast Multi-Shot"), S("/cast Barbed Shot"), S("/cast Kill Command") }
   data["HUNTER_253"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Counter Shot\n", "/cast Exhilaration\n")))
end
do -- MM (254)
   local st = { S("/cast Trueshot"), S("/cast Aimed Shot"), S("/cast Rapid Fire"), S("/cast Arcane Shot"), S("/cast Steady Shot") }
   local aoe = { S("/cast Trueshot"), S("/cast Multi-Shot"), S("/cast Rapid Fire"), S("/cast Aimed Shot") }
   data["HUNTER_254"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Counter Shot\n", "/cast Exhilaration\n")))
end
do -- Surv (255)
   local st = { S("/cast Coordinated Assault"), S("/cast Wildfire Bomb"), S("/cast Mongoose Bite"), S("/cast Kill Command"), S("/cast Serpent Sting") }
   local aoe = { S("/cast Wildfire Bomb"), S("/cast Butchery"), S("/cast Kill Command"), S("/cast Mongoose Bite") }
   data["HUNTER_255"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Muzzle\n", "/cast Exhilaration\n")))
end

-- =======================
-- MAGE (Generated)
-- =======================
do -- Arcane (62)
   local st = { S("/cast Arcane Surge"), S("/cast Arcane Blast"), S("/cast Arcane Missiles"), S("/cast Arcane Barrage") }
   local aoe = { S("/cast Arcane Surge"), S("/cast Arcane Barrage"), S("/cast Arcane Orb"), S("/cast Arcane Explosion") }
   data["MAGE_62"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Counterspell\n", "/cast Ice Block\n")))
end
do -- Fire (63)
   local st = { S("/cast Combustion"), S("/cast Fire Blast"), S("/cast Pyroblast"), S("/cast Phoenix Flames"), S("/cast Fireball") }
   local aoe = { S("/cast Combustion"), S("/cast Flamestrike"), S("/cast Fire Blast"), S("/cast Phoenix Flames"), S("/cast Scorch") }
   data["MAGE_63"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Counterspell\n", "/cast Ice Block\n")))
end
do -- Frost (64)
   local st = { S("/cast Icy Veins"), S("/cast Flurry"), S("/cast Ice Lance"), S("/cast Glacial Spike"), S("/cast Frostbolt") }
   local aoe = { S("/cast Frozen Orb"), S("/cast Blizzard"), S("/cast Ice Lance"), S("/cast Cone of Cold") }
   data["MAGE_64"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Counterspell\n", "/cast Ice Block\n")))
end

-- =======================
-- MONK (Generated)
-- =======================
do -- Brew (268)
   local st = { S("/cast Keg Smash"), S("/cast Blackout Kick"), S("/cast Breath of Fire"), S("/cast Tiger Palm") }
   local aoe = { S("/cast Keg Smash"), S("/cast Breath of Fire"), S("/cast Spinning Crane Kick"), S("/cast Blackout Kick") }
   data["MONK_268"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Spear Hand Strike\n", "/cast Fortifying Brew\n")))
end
do -- Mist (270)
   local st = { S("/cast Rising Sun Kick"), S("/cast Blackout Kick"), S("/cast Tiger Palm") }
   local aoe = { S("/cast Spinning Crane Kick"), S("/cast Rising Sun Kick"), S("/cast Blackout Kick") }
   local heal = { S("/cast Renewing Mist"), S("/cast Vivify"), S("/cast Enveloping Mist"), S("/cast Essence Font") }
   data["MONK_270"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Spear Hand Strike\n", "/cast Revival\n", heal)))
end
do -- WW (269)
   local st = { S("/cast Rising Sun Kick"), S("/cast Fists of Fury"), S("/cast Blackout Kick"), S("/cast Tiger Palm") }
   local aoe = { S("/cast Fists of Fury"), S("/cast Spinning Crane Kick"), S("/cast Rising Sun Kick"), S("/cast Blackout Kick") }
   data["MONK_269"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Spear Hand Strike\n", "/cast Touch of Karma\n")))
end

-- =======================
-- PALADIN (Generated)
-- =======================
do -- Holy (65)
   local st = { S("/cast Holy Shock"), S("/cast Crusader Strike"), S("/cast Judgment"), S("/cast Hammer of Wrath") }
   local aoe = { S("/cast Holy Shock"), S("/cast Consecration"), S("/cast Judgment") }
   local heal = { S("/cast Holy Shock"), S("/cast Word of Glory"), S("/cast Light of Dawn"), S("/cast Flash of Light") }
   data["PALADIN_65"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Rebuke\n", "/cast Divine Protection\n", heal)))
end
do -- Prot (66)
   local st = { S("/cast Judgment"), S("/cast Hammer of Wrath"), S("/cast Avenger's Shield"), S("/cast Shield of the Righteous"), S("/cast Consecration") }
   local aoe = { S("/cast Avenger's Shield"), S("/cast Consecration"), S("/cast Judgment"), S("/cast Shield of the Righteous") }
   data["PALADIN_66"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Rebuke\n", "/cast Ardent Defender\n")))
end
do -- Ret (70)
   local st = { S("/cast Wake of Ashes"), S("/cast Templar's Verdict"), S("/cast Blade of Justice"), S("/cast Judgment"), S("/cast Crusader Strike") }
   local aoe = { S("/cast Wake of Ashes"), S("/cast Divine Storm"), S("/cast Judgment"), S("/cast Blade of Justice") }
   data["PALADIN_70"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Rebuke\n", "/cast Shield of Vengeance\n")))
end

-- =======================
-- PRIEST (Generated)
-- =======================
do -- Disc (256)
   local st = { S("/cast Mind Blast"), S("/cast Penance"), S("/cast Smite") }
   local aoe = { S("/cast Shadow Word: Pain"), S("/cast Penance"), S("/cast Smite") }
   local heal = { S("/cast Power Word: Shield"), S("/cast Flash Heal"), S("/cast Penance"), S("/cast Power Word: Radiance") }
   data["PRIEST_256"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Silence\n", "/cast Pain Suppression\n", heal)))
end
do -- Holy (257)
   local st = { S("/cast Holy Fire"), S("/cast Smite"), S("/cast Holy Word: Chastise"), S("/cast Shadow Word: Pain") }
   local aoe = { S("/cast Holy Nova"), S("/cast Holy Fire"), S("/cast Smite") }
   local heal = { S("/cast Holy Word: Serenity"), S("/cast Flash Heal"), S("/cast Heal"), S("/cast Circle of Healing") }
   data["PRIEST_257"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Silence\n", "/cast Guardian Spirit\n", heal)))
end
do -- Shadow (258)
   local st = { S("/cast Void Eruption"), S("/cast Void Bolt"), S("/cast Mind Blast"), S("/cast Devouring Plague"), S("/cast Mind Flay") }
   local aoe = { S("/cast Shadow Crash"), S("/cast Void Eruption"), S("/cast Devouring Plague"), S("/cast Mind Sear") }
   data["PRIEST_258"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Silence\n", "/cast Dispersion\n")))
end

-- =======================
-- ROGUE (Generated)
-- =======================
do -- Assa (259)
   local st = { S("/cast Deathmark"), S("/cast Envenom"), S("/cast Garrote"), S("/cast Rupture"), S("/cast Mutilate") }
   local aoe = { S("/cast Fan of Knives"), S("/cast Crimson Tempest"), S("/cast Garrote"), S("/cast Rupture") }
   data["ROGUE_259"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Kick\n", "/cast Cloak of Shadows\n")))
end
do -- Outlaw (260)
   local st = { S("/cast Adrenaline Rush"), S("/cast Between the Eyes"), S("/cast Dispatch"), S("/cast Pistol Shot"), S("/cast Sinister Strike") }
   local aoe = { S("/cast Blade Flurry"), S("/cast Dispatch"), S("/cast Pistol Shot"), S("/cast Sinister Strike") }
   data["ROGUE_260"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Kick\n", "/cast Evasion\n")))
end
do -- Sub (261)
   local st = { S("/cast Shadow Blades"), S("/cast Eviscerate"), S("/cast Shadowstrike"), S("/cast Backstab") }
   local aoe = { S("/cast Shuriken Storm"), S("/cast Black Powder"), S("/cast Shadowstrike") }
   data["ROGUE_261"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Kick\n", "/cast Cloak of Shadows\n")))
end

-- =======================
-- SHAMAN (Generated)
-- =======================
do -- Ele (262)
   local st = { S("/cast Stormkeeper"), S("/cast Lava Burst"), S("/cast Earth Shock"), S("/cast Lightning Bolt"), S("/cast Flame Shock") }
   local aoe = { S("/cast Chain Lightning"), S("/cast Earthquake"), S("/cast Lava Burst"), S("/cast Flame Shock") }
   data["SHAMAN_262"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Wind Shear\n", "/cast Astral Shift\n")))
end
do -- Enh (263)
   local st = { S("/cast Feral Spirit"), S("/cast Stormstrike"), S("/cast Lava Lash"), S("/cast Elemental Blast"), S("/cast Lightning Bolt") }
   local aoe = { S("/cast Chain Lightning"), S("/cast Crash Lightning"), S("/cast Sundering"), S("/cast Stormstrike") }
   data["SHAMAN_263"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Wind Shear\n", "/cast Astral Shift\n")))
end
do -- Resto (264)
   local st = { S("/cast Lava Burst"), S("/cast Lightning Bolt"), S("/cast Flame Shock") }
   local aoe = { S("/cast Chain Lightning"), S("/cast Acid Rain"), S("/cast Lava Burst") }
   local heal = { S("/cast Riptide"), S("/cast Healing Surge"), S("/cast Chain Heal"), S("/cast Healing Rain") }
   data["SHAMAN_264"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Wind Shear\n", "/cast Spirit Link Totem\n", heal)))
end

-- =======================
-- WARLOCK (Generated)
-- =======================
do -- Aff (265)
   local st = { S("/cast Malefic Rapture"), S("/cast Unstable Affliction"), S("/cast Agony"), S("/cast Corruption"), S("/cast Shadow Bolt") }
   local aoe = { S("/cast Seed of Corruption"), S("/cast Agony"), S("/cast Malefic Rapture"), S("/cast Drain Soul") }
   data["WARLOCK_265"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Spell Lock\n", "/cast Unending Resolve\n")))
end
do -- Demo (266)
   local st = { S("/cast Call Dreadstalkers"), S("/cast Hand of Gul'dan"), S("/cast Demonbolt"), S("/cast Shadow Bolt") }
   local aoe = { S("/cast Hand of Gul'dan"), S("/cast Implosion"), S("/cast Demonbolt"), S("/cast Shadow Bolt") }
   data["WARLOCK_266"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Spell Lock\n", "/cast Unending Resolve\n")))
end
do -- Destro (267)
   local st = { S("/cast Chaos Bolt"), S("/cast Incinerate"), S("/cast Conflagrate"), S("/cast Immolate") }
   local aoe = { S("/cast Rain of Fire"), S("/cast Channel Demonfire"), S("/cast Incinerate"), S("/cast Immolate") }
   data["WARLOCK_267"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Spell Lock\n", "/cast Unending Resolve\n")))
end

-- =======================
-- WARRIOR (Generated/Adapted)
-- =======================
do -- Arms (71)
   local st = { S("/cast Colossus Smash"), S("/cast Mortal Strike"), S("/cast Overpower"), S("/cast Execute"), S("/cast Slam") }
   local aoe = { S("/cast Warbreaker"), S("/cast Bladestorm"), S("/cast Cleave"), S("/cast Whirlwind"), S("/cast Overpower") }
   data["WARRIOR_71"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Pummel\n", "/cast Die by the Sword\n")))
end
do -- Fury (72)
   local st = { S("/cast Recklessness"), S("/cast Rampage"), S("/cast Execute"), S("/cast Raging Blow"), S("/cast Bloodthirst") }
   local aoe = { S("/cast Recklessness"), S("/cast Whirlwind"), S("/cast Rampage"), S("/cast Raging Blow"), S("/cast Bloodthirst") }
   data["WARRIOR_72"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Pummel\n", "/cast Enraged Regeneration\n")))
end
do -- Prot (73)
   local st = { S("/cast Avatar"), S("/cast Shield Slam"), S("/cast Thunder Clap"), S("/cast Revenge"), S("/cast Execute") }
   local aoe = { S("/cast Avatar"), S("/cast Thunder Clap"), S("/cast Revenge"), S("/cast Shield Slam") }
   data["WARRIOR_73"] = mkAllModes(mkProfiles(mkRotation(st, aoe, "/cast [harm] Pummel\n", "/cast Shield Wall\n")))
end

-- Register as one pack
SW:RegisterClassPack("ALL_SPECS", data)
