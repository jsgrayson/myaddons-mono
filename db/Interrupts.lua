local ADDON_NAME, SkillWeaver = ...
-- GENERATED FILE - DO NOT EDIT MANUALLY
-- Merged Data: Patch 11.2.7 Mandatory + Comprehensive TWW/M+ Coverage

SkillWeaver.Interrupts = SkillWeaver.Interrupts or {}

-- ============================================================================
-- TWW Dungeons (Native)
-- ============================================================================

SkillWeaver.Interrupts["Ara-Kara, City of Echoes"] = {
    ["Bloodstained Webmage"] = { priority = {"Revolting Volley"}, optional = {"Silken Restraints"} },
    ["Nix"] = { priority = {"Horrifying Shrill"}, optional = {} },
    ["Ixin"] = { priority = {"Web Wrap", "Horrifying Shrill"}, optional = {} },
    ["Trilling Attendant"] = { priority = {"Resonant Barrage"}, optional = {"Web Bolt"} },
    ["Blood Overseer"] = { priority = {"Venom Volley"}, optional = {} },
    ["Atik"] = { priority = {"Poison Bolt"}, optional = {} },
    ["Herald of Ansurek"] = { priority = {"Twist Thoughts"}, optional = {} },
}

SkillWeaver.Interrupts["City of Threads"] = {
    ["Sureki Silkbinder"] = { priority = {"Silk Binding"}, optional = {"Web Bolt"} },
    ["Herald of Ansurek"] = { priority = {"Grim Weaver", "Twist Thoughts"}, optional = {} },
    ["Xeph'itik"] = { priority = {"Gossamer Barrage"}, optional = {} },
    ["Covert Webmancer"] = { priority = {"Grimweave Blast", "Mending Web"}, optional = {} },
    ["Elder Shadeweaver"] = { priority = {}, optional = {"Web Bolt"} },
    ["Sureki Unnaturaler"] = { priority = {"Void Wave"}, optional = {} },
}

SkillWeaver.Interrupts["The Stonevault"] = {
    ["Turned Speaker"] = { priority = {"Censoring Gear"}, optional = {} },
    ["Void Bound Howler"] = { priority = {"Piercing Wail"}, optional = {} },
    ["Forgebound Mender"] = { priority = {"Restoring Metals"}, optional = {"Alloy Bolt"} },
    ["E.D.N.A"] = { priority = {"Seismic Smash", "Earth Spike"}, optional = {"Refracting Beam"} },
    ["Ghastly Voidsoul"] = { priority = {"Howling Fear"}, optional = {} },
    ["Cursedheart Invader"] = { priority = {"Arcing Void"}, optional = {} },
    ["Cursedforge Stoneshaper"] = { priority = {"Earth Burst Totem", "Stone Bolt"}, optional = {} },
    ["Master Machinists"] = { priority = {"Molten Metal"}, optional = {} },
}

SkillWeaver.Interrupts["The Dawnbreaker"] = {
    ["Nightfall Dark Architect"] = { priority = {"Tormenting Eruption", "Night Bolt"}, optional = {} },
    ["Nightfall Ritualist"] = { priority = {"Tormenting Beam"}, optional = {} },
    ["Sureki Militant"] = { priority = {"Silken Shell"}, optional = {} },
    ["Nightfall Darkcaster"] = { priority = {"Tormenting Beam", "Umbral Barrier"}, optional = {} },
    ["Sereki Web Mage"] = { priority = {}, optional = {"Web Bolt"} },
    ["Nightfall Commander"] = { priority = {"Abyssal Howl"}, optional = {} },
    ["Speaker Shadowcrown"] = { priority = {"Shadow Bolt"}, optional = {} },
}

SkillWeaver.Interrupts["Cinderbrew Meadery"] = {
    ["Flavor Scientist"] = { priority = {"Rejuvenating Honey"}, optional = {} },
    ["Careless Hopgoblin"] = { priority = {"Cinderbrew Toss"}, optional = {} },
    ["Goldie's Add"] = { priority = {"Vent"}, optional = {} },
    ["Taste Tester"] = { priority = {"Free Samples?"}, optional = {} },
    ["Venture Co. Pyromaniac"] = { priority = {"Boiling Flames"}, optional = {} },
    ["Bee Wrangler"] = { priority = {"Bee-stial Wrath"}, optional = {} },
    ["Royal Jelly Purveyor"] = { priority = {"Honey Volley"}, optional = {} },
}

SkillWeaver.Interrupts["Darkflame Cleft"] = {
    ["Kobold Wicklighter"] = { priority = {"Flash", "Wicklighter Bolt"}, optional = {} },
    ["Wandering Candle"] = { priority = {"Quenching Blast"}, optional = {} },
    ["Lowly Moleherd"] = { priority = {"Mole Frenzy"}, optional = {} },
    ["Kobold Flametender"] = { priority = {"Flame Bolt"}, optional = {} },
    ["Sootsnout"] = { priority = {"Flaming Tether"}, optional = {"Candleflame Bolt"} },
    ["Blazing Fiend"] = { priority = {"Explosive Flame"}, optional = {} },
    ["Shuffling Horror"] = { priority = {"Drain Light"}, optional = {} },
    ["The Candle King"] = { priority = {"Paranoid Mind"}, optional = {} },
}

SkillWeaver.Interrupts["Priory of the Sacred Flame"] = {
    ["Devout Priest"] = { priority = {"Greater Heal"}, optional = {"Holy Smite"} },
    ["Risen Mage"] = { priority = {"Fireball Volley"}, optional = {"Fireball"} },
    ["Prioress Murrpray"] = { priority = {"Repentance", "Embrace the Light"}, optional = {"Holy Smite"} },
    ["Baron Braunpyke"] = { priority = {"Burning Light"}, optional = {} },
    ["Fanatical Conjurer"] = { priority = {"Fireball Volley"}, optional = {"Fireball"} },
    ["Arathi Footman"] = { priority = {"Defend"}, optional = {} },
}

SkillWeaver.Interrupts["The Rookery"] = {
    ["Coalescing Void Diffuser"] = { priority = {"Attracting Shadows"}, optional = {} },
    ["Void Ascendant"] = { priority = {"Void Volley", "Void Bolt"}, optional = {} },
    ["Corrupted Oracle"] = { priority = {"Detect Thoughts", "Void Bolt"}, optional = {} },
    ["Cursed Thunderer"] = { priority = {"Lightning Bolt"}, optional = {} },
    ["Cursed Rooktender"] = { priority = {"Enrage Rook"}, optional = {} },
}

SkillWeaver.Interrupts["Eco-Dome Al'dani"] = {
    ["Unstable Mote"] = { priority = {"Arcane Eruption"}, optional = {} },
    ["Ether-Binder"] = { priority = {"Seal Magic"}, optional = {} },
    ["Soul-Scribe"] = { priority = {"Violent Scripture"}, optional = {} },
    ["Overgorged Mite"] = { priority = {"Gorge"}, optional = {} },
    ["Wastelander Farstalker"] = { priority = {"Arcing Zap"}, optional = {} },
    ["Wastelander Ritualist"] = { priority = {}, optional = {"Arcane Bolt"} },
    ["Wastelander Pactspeaker"] = { priority = {"Erratic Ritual"}, optional = {"Arcane Bolt"} },
}

SkillWeaver.Interrupts["Operation: Floodgate"] = {
    ["Darkfuse Bloodwarper"] = { priority = {"Warp Blood"}, optional = {"Blood Bolt"} },
    ["Mechadrone Sniper"] = { priority = {"Trickshot"}, optional = {} },
    ["Disturbed Kelp"] = { priority = {"Restorative Algae"}, optional = {} },
    ["Mechadrone"] = { priority = {"Maximum Distortion"}, optional = {} },
    ["Venture Co. Electrician"] = { priority = {}, optional = {"Lightning Bolt"} },
    ["Venture Co. Diver"] = { priority = {"Harpoon"}, optional = {} },
    ["Darkfuse Hyena"] = { priority = {"Bloodthirsty Cackle"}, optional = {} },
    ["Architect"] = { priority = {"Surveying Beam"}, optional = {"Nail Gun"} },
}

-- ============================================================================
-- Mythic+ Rotation (Season 1 & 3)
-- ============================================================================

SkillWeaver.Interrupts["Grim Batol"] = {
    ["Twilight Earthcaller"] = { priority = {"Mass Tremor"}, optional = {"Earth Bolt"} },
    ["Twilight Beguiler"] = { priority = {"Sear Mind"}, optional = {"Shadowflame Bolt"} },
    ["Twilight Warlock"] = { priority = {}, optional = {"Shadowflame Bolt"} },
    ["General Umbriss"] = { priority = {}, optional = {} },
    ["Drahga Shadowburner"] = { priority = {}, optional = {"Shadowflame Bolt"} },
}

SkillWeaver.Interrupts["Siege of Boralus"] = {
    ["Scrimshaw Enforcer"] = { priority = {"Shattering Bellow"}, optional = {} },
    ["Irontide Waveshaper"] = { priority = {"Watertight Shell"}, optional = {"Brackish Bolt"} },
    ["Bilge Rat Tempest"] = { priority = {"Choking Waters"}, optional = {"Water Bolt"} },
    ["Bilge Rat Pillager"] = { priority = {"Stinky Vomit"}, optional = {} },
    ["Ashvane Commander"] = { priority = {"Bolstering Shout"}, optional = {} },
}

SkillWeaver.Interrupts["Mists of Tirna Scithe"] = {
    ["Mistveil Shaper"] = { priority = {"Bramblethorn Coat"}, optional = {} },
    ["Mistveil Tender"] = { priority = {"Nourish the Forest"}, optional = {} },
    ["Drust Harvester"] = { priority = {"Harvest Essence"}, optional = {"Spirit Bolt"} },
    ["Ingra Maloch"] = { priority = {}, optional = {"Spirit Bolt"} },
    ["Mistcaller"] = { priority = {"Patty Cake"}, optional = {} },
    ["Spinema Staghorn"] = { priority = {"Stimulate Resistance", "Stimulate Regeneration"}, optional = {} },
}

SkillWeaver.Interrupts["Necrotic Wake"] = {
    ["Corpse Harvester"] = { priority = {"Drain Fluids"}, optional = {} },
    ["Zolramus Necromancer"] = { priority = {"Necrotic Bolt"}, optional = {} },
    ["Skeletal Marauder"] = { priority = {"Rasping Scream"}, optional = {} },
    ["Amarth"] = { priority = {}, optional = {"Necrotic Bolt"} },
    ["Reanimated Mage"] = { priority = {"Frostbolt Volley"}, optional = {} },
    ["Craftsman"] = { priority = {"Repair Flesh"}, optional = {} },
}

SkillWeaver.Interrupts["Halls of Atonement"] = {
    ["Depraved Collector"] = { priority = {"Siphon Life"}, optional = {} },
    ["Depraved Houndmaster"] = { priority = {"Loyal Beasts"}, optional = {} },
    ["Stoneborn Slasher"] = { priority = {"Disrupting Screech"}, optional = {} },
    ["High Adjudicator Aleez"] = { priority = {}, optional = {"Anima Bolt"} },
}

SkillWeaver.Interrupts["Tazavesh, the Veiled Market"] = {
    ["Support Officer"] = { priority = {"Hard Light Barrier"}, optional = {"Hyperlight Bolt"} },
    ["Overloaded Mail Elemental"] = { priority = {"Spam Filter"}, optional = {} },
    ["Oasis Security"] = { priority = {"Menacing Shout"}, optional = {} },
    ["Portalmancer Zo'honn"] = { priority = {"Empowered Glyph of Restraint"}, optional = {"Hyperlight Bolt"} },
    ["So'leah"] = { priority = {}, optional = {} },
    ["Assassin"] = { priority = {"Shuriken Blitz"}, optional = {} },
}

-- ============================================================================
-- Mythic+ Affixes
-- ============================================================================

SkillWeaver.Interrupts["Mythic+ Affixes"] = {
    ["Void Emissary"] = { priority = {"Dark Prayer"}, optional = {} }, -- Xal'atath's Bargain: Voidbound
}

-- ============================================================================
-- TWW Raids
-- ============================================================================

SkillWeaver.Interrupts["Nerub-ar Palace"] = {
    ["Princess Ky'veza"] = { priority = {"Nether Rift"}, optional = {} },
    ["Ulgrax the Devourer"] = { priority = {"Venomous Spit"}, optional = {} },
    ["Rasha'nan"] = { priority = {"Acidic Eruption"}, optional = {} },
}

SkillWeaver.Interrupts["Liberation of Undermine"] = {
    ["The One-Armed Bandit"] = { priority = {"Spin to Win", "Total Destruction"}, optional = {} },
    ["Pit Mechanic"] = { priority = {"Repair"}, optional = {} },
}

SkillWeaver.Interrupts["Manaforge Omega"] = {
    ["Nexus-King Salhadaar"] = { priority = {}, optional = {} },
    ["Plexus Sentinel"] = { priority = {"Protocol: Purge"}, optional = {} },
    ["Shadowguard Mage"] = { priority = {"Void Burst"}, optional = {} },
    ["Nexus Prince"] = { priority = {"Netherblast"}, optional = {} },
}

-- ============================================================================
-- World Bosses
-- ============================================================================

SkillWeaver.Interrupts["Khaz Algar (World)"] = {
    ["Reshanor"] = { priority = {"Veilshatter Roar"}, optional = {} },
    ["The Gobfather"] = { priority = {"Death From Above", "Giga-Rocket Slam"}, optional = {} },
    ["Kordac"] = { priority = {}, optional = {} },
    ["Aggregation of Horrors"] = { priority = {}, optional = {} },
    ["Shurrai"] = { priority = {}, optional = {} },
    ["Orta"] = { priority = {}, optional = {} },
}

-- ============================================================================
-- Future Content (Midnight 12.0)
-- ============================================================================

SkillWeaver.Interrupts["Midnight (12.0)"] = {
    -- Placeholder for next expansion content
}
