--========================================================--
-- SkillWeaver - Talent Recommendation System
-- Database of optimal talent builds for TWW Season 1
--========================================================--

local TalentRecommendations = {}
SkillWeaver.TalentRecommendations = TalentRecommendations

-- Format: [SpecID] = { [ContentType] = { name="Build Name", string="ImportString", hero="HeroTree" } }

TalentRecommendations.Data = {
    --========================================================--
    -- WARRIOR
    --========================================================--
    [71] = { -- Arms
        Raid = { 
            name = "Slayer Raid (Single Target)", 
            hero = "Slayer",
            string = "CcEAAAAAAAAAAAAAAAAAAAAAAAgtZMjxMzMzmlllZGAAAAMYaYGsZMDMjxMzgZGGGDzwAAAAAAAgHYMLzMzAIwYZbgFwAmhJkhBb" 
        },
        MythicPlus = { 
            name = "Slayer M+ (Bladestorm)", 
            hero = "Slayer",
            string = "CcEAAAAAAAAAAAAAAAAAAAAAAAYYmZmZMjZmFLLLjZAAAAYw0wMDLDzAjlxMzgZGGz4BYGGAAAAAAAMjZZMGgtAjltBWADYGmQGgN" 
        },
        PVP = {
            name = "Slayer PvP (Thunderous Roar)",
            hero = "Slayer",
            string = "CcEAAAAAAAAAAAAAAAAAAAAAAAgtZMjxMzMzmlllZGAAAAMYaYGsZMDMjxMzgZGGGDzwAAAAAAAgHYMLzMzAIwYZbgFwAmhJkhBb",
            pvpTalents = { "Sharpen Blade", "Disarm", "Duel" }
        },
        Delve = { name = "Slayer Delve", hero = "Slayer", string = "CcEAAAAAAAAAAAAAAAAAAAAAAAgtZMjxMzMzmlllZGAAAAMYaYGsZMDMjxMzgZGGGDzwAAAAAAAgHYMLzMzAIwYZbgFwAmhJkhBb" }
    },
    [72] = { -- Fury
        Raid = { 
            name = "Slayer Raid (Execute Focus)", 
            hero = "Slayer",
            string = "CgEAAAAAAAAAAAAAAAAAAAAAAMAAAAAAAAAgRDMDYMMDjBmFYYGjZmHYYmZbbMmZmFMzDMzMjZMbDzMMGAAAIMjltBWATwMMBGbDbA" 
        },
        MythicPlus = { 
            name = "Slayer M+ (AoE)", 
            hero = "Slayer",
            string = "CgEAAAAAAAAAAAAAAAAAAAAAAMAAAAAAAAAAagZGghZYMMzsBDzMjhZYGbbzMmZmNmZMzMjZYz2MMzYAAAgwM22GYBMBzwEYshN" 
        },
        Delve = { name = "Slayer Delve", hero = "Slayer", string = "CgEAAAAAAAAAAAAAAAAAAAAAAMAAAAAAAAAAagZGghZYMMzsBDzMjhZYGbbzMmZmNmZMzMjZYz2MMzYAAAgwM22GYBMBzwEYshN" },
        PVP = { name = "Slayer PvP", hero = "Slayer", string = "CgEAAAAAAAAAAAAAAAAAAAAAAMAAAAAAAAAAagZGghZYMMzsBDzMjhZYGbbzMmZmNmZMzMjZYz2MMzYAAAgwM22GYBMBzwEYshN", pvpTalents = { "Slaughterhouse", "Enduring Rage", "Battle Trance" } }
    },
    [73] = { -- Protection
        Raid = { 
            name = "Mountain Thane Raid (Defensive)", 
            hero = "Mountain Thane",
            string = "CkEAAAAAAAAAAAAAAAAAAAAAAYEDAAAAzMzYmZGMbzsMzMz2mZGMYYAAAAAAAjBAmZbBwAbwyiRjZAMbxMbMjB" 
        },
        MythicPlus = { 
            name = "Mountain Thane M+ (Thunder Clap)", 
            hero = "Mountain Thane",
            string = "CkEAAAAAAAAAAAAAAAAAAAAAAYEDAAAAzMzMmZGmZbmlZmZWYGDTjBjZAsMwwGzMDDz8AjZAAAAAAAzMAALbbAGGYDWWMaMDgZL2Y2A" 
        },
        Delve = { name = "Mountain Thane Delve", hero = "Mountain Thane", string = "CkEAAAAAAAAAAAAAAAAAAAAAAYEDAAAAzMzMmZGmZbmlZmZWYGDTjBjZAsMwwGzMDDz8AjZAAAAAAAzMAALbbAGGYDWWMaMDgZL2Y2A" },
        PVP = { name = "Mountain Thane PvP", hero = "Mountain Thane", string = "CkEAAAAAAAAAAAAAAAAAAAAAAYEDAAAAzMzMmZGmZbmlZmZWYGDTjBjZAsMwwGzMDDz8AjZAAAAAAAzMAALbbAGGYDWWMaMDgZL2Y2A", pvpTalents = { "Shield Bash", "Bodyguard", "Sword and Board" } }
    },

    --========================================================--
    -- HUNTER
    --========================================================--
    [253] = { -- Beast Mastery
        Raid = { 
            name = "Pack Leader Raid (Single Target)", 
            hero = "Pack Leader",
            string = "C0PAAAAAAAAAAAAAAAAAAAAAAYsNDMgFwMsEyYBAAAAAADAAAAAAgZGDjZmZYmhZYYGzMGzMzkZYMDzMjZGzwYMzMMLzwYGsB"
        },
        MythicPlus = { 
            name = "Pack Leader M+ (AoE)", 
            hero = "Pack Leader",
            string = "C0PAAAAAAAAAAAAAAAAAAAAAAYsNDMgFwMsFyYBAAAAAADAAAAAAgZsNjhZMMzMmhxMjZGjZmZyMMmZMzMmZYYMmxwsMDzyMYD" 
        },
        Delve = { name = "Pack Leader Delve", hero = "Pack Leader", string = "C0PAAAAAAAAAAAAAAAAAAAAAAYsNDMgFwMsFyYBAAAAAADAAAAAAgZsNjhZMMzMmhxMjZGjZmZyMMmZMzMmZYYMmxwsMDzyMYD" },
        PVP = { name = "Pack Leader PvP", hero = "Pack Leader", string = "C0PAAAAAAAAAAAAAAAAAAAAAAYsNDMgFwMsFyYBAAAAAADAAAAAAgZsNjhZMMzMmhxMjZGjZmZyMMmZMzMmZYYMmxwsMDzyMYD", pvpTalents = { "Dire Beast: Hawk", "Interlope", "Roar of Sacrifice" } }
    },
    [254] = { -- Marksmanship
        Raid = { 
            name = "Sentinel Raid (Single Target)", 
            hero = "Sentinel",
            string = "C4PAAAAAAAAAAAAAAAAAAAAAAwADsNGN2GQmNsBAAAAAAmxMzMDzMzwMzMMzMjxMjZAAAAAAAAmhxMzMzMmRzMGDzMwMmxMjB" 
        },
        MythicPlus = { 
            name = "Sentinel M+ (AoE)", 
            hero = "Sentinel",
            string = "C4PAAAAAAAAAAAAAAAAAAAAAAwADsNGNWGQmFsBAAAAAAMzMjZMjxMMzMzMzMMzYYMbAAAAAAAYGGzYmZmZmJzYMMzwYYmlZwG" 
        },
        Delve = { name = "Sentinel Delve", hero = "Sentinel", string = "C4PAAAAAAAAAAAAAAAAAAAAAAwADsNGNWGQmFsBAAAAAAMzMjZMjxMMzMzMzMMzYYMbAAAAAAAYGGzYmZmZmJzYMMzwYYmlZwG" },
        PVP = { name = "Sentinel PvP", hero = "Sentinel", string = "C4PAAAAAAAAAAAAAAAAAAAAAAwADsNGNWGQmFsBAAAAAAMzMjZMjxMMzMzMzMMzYYMbAAAAAAAYGGzYmZmZmJzYMMzwYYmlZwG", pvpTalents = { "Sniper Shot", "Chimaeral Sting", "Survival Tactics" } }
    },
    [255] = { -- Survival
        Raid = { 
            name = "Pack Leader Raid (Single Target)", 
            hero = "Pack Leader",
            string = "C8PAFBU0uAhOaNI6RqWjIx917NGYgtxox2AysFsNzMbzYmZYmxMDzMMzMmZMAAAAAAAAAAAAAAoZYMjZmZmZGzwYYmhxwMmBb" 
        },
        MythicPlus = { 
            name = "Pack Leader M+ (Wildfire Bomb)", 
            hero = "Pack Leader",
            string = "C8PAFBU0uAhOaNI6RqWjIx917NGYglxoxyAysFsNzYbGzMzMmZmZMzMYMzMzAAAAAAAAAAAAAAANDjZMzMjZGzwYYmhxwMLzgN" 
        },
        Delve = { name = "Pack Leader Delve", hero = "Pack Leader", string = "C8PAFBU0uAhOaNI6RqWjIx917NGYglxoxyAysFsNzYbGzMzMmZmZMzMYMzMzAAAAAAAAAAAAAAANDjZMzMjZGzwYYmhxwMLzgN" },
        PVP = { name = "Pack Leader PvP", hero = "Pack Leader", string = "C8PAFBU0uAhOaNI6RqWjIx917NGYglxoxyAysFsNzYbGzMzMmZmZMzMYMzMzAAAAAAAAAAAAAAANDjZMzMjZGzwYYmhxwMLzgN", pvpTalents = { "Diamond Ice", "Survival Tactics", "Mending Bandage" } }
    }
    --========================================================--
    -- MAGE
    --========================================================--
    [62] = { -- Arcane
        Raid = { name = "Sunfury Raid", hero = "Sunfury", string = "C4DAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Sunfury M+", hero = "Sunfury", string = "C4DAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Sunfury Delve", hero = "Sunfury", string = "C4DAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Sunfury PvP", hero = "Sunfury", string = "C4DAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Arcane Empowerment", "Master Shepherd", "Ring of Fire" } }
    },
    [63] = { -- Fire
        Raid = { name = "Sunfury Raid", hero = "Sunfury", string = "C8DAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Sunfury M+", hero = "Sunfury", string = "C8DAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Sunfury Delve", hero = "Sunfury", string = "C8DAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Sunfury PvP", hero = "Sunfury", string = "C8DAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" }
    },
    [64] = { -- Frost
        Raid = { name = "Spellslinger Raid", hero = "Spellslinger", string = "C8DAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Spellslinger M+", hero = "Spellslinger", string = "C8DAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Spellslinger Delve", hero = "Spellslinger", string = "C8DAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Spellslinger PvP", hero = "Spellslinger", string = "C8DAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" }
    },

    --========================================================--
    -- ROGUE
    --========================================================--
    [259] = { -- Assassination
        Raid = { name = "Deathstalker Raid", hero = "Deathstalker", string = "CMQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Deathstalker M+", hero = "Deathstalker", string = "CMQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Deathstalker Delve", hero = "Deathstalker", string = "CMQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Deathstalker PvP", hero = "Deathstalker", string = "CMQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Hemotoxin", "System Shock", "Smoke Bomb" } }
    },
    [260] = { -- Outlaw
        Raid = { name = "Fatebound Raid", hero = "Fatebound", string = "CMQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Fatebound M+", hero = "Fatebound", string = "CMQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Fatebound Delve", hero = "Fatebound", string = "CMQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Fatebound PvP", hero = "Fatebound", string = "CMQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Float Like a Butterfly", "Enduring Brawler", "Dismantle" } }
    },
    [261] = { -- Subtlety
        Raid = { name = "Trickster Raid", hero = "Trickster", string = "CMQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Trickster M+", hero = "Trickster", string = "CMQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Trickster Delve", hero = "Trickster", string = "CMQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Trickster PvP", hero = "Trickster", string = "CMQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Thief's Bargain", "Shadow Duel", "Cold Blood" } }
    },

    --========================================================--
    -- WARLOCK
    --========================================================--
    [265] = { -- Affliction
        Raid = { name = "Soul Harvester Raid", hero = "Soul Harvester", string = "CkQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Soul Harvester M+", hero = "Soul Harvester", string = "CkQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Soul Harvester Delve", hero = "Soul Harvester", string = "CkQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Soul Harvester PvP", hero = "Soul Harvester", string = "CkQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Jinx", "Rapid Contagion", "Rampant Afflictions" } }
    },
    [266] = { -- Demonology
        Raid = { name = "Diabolist Raid", hero = "Diabolist", string = "CkQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Diabolist M+", hero = "Diabolist", string = "CkQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Diabolist Delve", hero = "Diabolist", string = "CkQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Diabolist PvP", hero = "Diabolist", string = "CkQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Call Fel Lord", "Master Summoner", "Call Observer" } }
    },
    [267] = { -- Destruction
        Raid = { name = "Hellcaller Raid", hero = "Hellcaller", string = "CkQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Hellcaller M+", hero = "Hellcaller", string = "CkQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Hellcaller Delve", hero = "Hellcaller", string = "CkQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Hellcaller PvP", hero = "Hellcaller", string = "CkQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Bane of Havoc", "Bonds of Fel", "Casting Circle" } }
    },

    --========================================================--
    -- PRIEST
    --========================================================--
    [256] = { -- Discipline
        Raid = { name = "Voidweaver Raid", hero = "Voidweaver", string = "CAQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Voidweaver M+", hero = "Voidweaver", string = "CAQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Voidweaver Delve", hero = "Voidweaver", string = "CAQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Voidweaver PvP", hero = "Voidweaver", string = "CAQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Inner Light and Shadow", "Catharsis", "Ultimate Penitence" } }
    },
    [257] = { -- Holy
        Raid = { name = "Archon Raid", hero = "Archon", string = "CAQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Archon M+", hero = "Archon", string = "CAQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Archon Delve", hero = "Archon", string = "CAQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Archon PvP", hero = "Archon", string = "CAQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Spirit of the Redeemer", "Ray of Hope", "Cardinal Mending" } }
    },
    [258] = { -- Shadow
        Raid = { name = "Archon Raid", hero = "Archon", string = "CAQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Voidweaver M+", hero = "Voidweaver", string = "CAQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Voidweaver Delve", hero = "Voidweaver", string = "CAQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Voidweaver PvP", hero = "Voidweaver", string = "CAQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Psyfiend", "Void Origins", "Catharsis" } }
    },

    --========================================================--
    -- PALADIN
    --========================================================--
    [65] = { -- Holy
        Raid = { name = "Herald Raid", hero = "Herald of the Sun", string = "CEEAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Herald M+", hero = "Herald of the Sun", string = "CEEAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Herald Delve", hero = "Herald of the Sun", string = "CEEAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Herald PvP", hero = "Herald of the Sun", string = "CEEAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Divine Favor", "Blessed Hands", "Avenging Light" } }
    },
    [66] = { -- Protection
        Raid = { name = "Templar Raid", hero = "Templar", string = "CEEAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Templar M+", hero = "Templar", string = "CEEAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Templar Delve", hero = "Templar", string = "CEEAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Templar PvP", hero = "Templar", string = "CEEAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Steed of Glory", "Guardian of the Forgotten Queen", "Shield of Virtue" } }
    },
    [70] = { -- Retribution
        Raid = { name = "Templar Raid", hero = "Templar", string = "CEEAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Herald M+", hero = "Herald of the Sun", string = "CEEAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Herald Delve", hero = "Herald of the Sun", string = "CEEAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Herald PvP", hero = "Herald of the Sun", string = "CEEAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Luminary", "Law and Order", "Blessing of Sanctuary" } }
    },

    --========================================================--
    -- DRUID
    --========================================================--
    [102] = { -- Balance
        Raid = { name = "Elune's Chosen Raid", hero = "Elune's Chosen", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Keeper M+", hero = "Keeper of the Grove", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Keeper Delve", hero = "Keeper of the Grove", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Keeper PvP", hero = "Keeper of the Grove", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Owlkin Adept", "Star Burst", "High Winds" } }
    },
    [103] = { -- Feral
        Raid = { name = "Wildstalker Raid", hero = "Wildstalker", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Wildstalker M+", hero = "Wildstalker", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Wildstalker Delve", hero = "Wildstalker", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Wildstalker PvP", hero = "Wildstalker", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Ferocious Wound", "Leader of the Pack", "Wild Attunement" } }
    },
    [104] = { -- Guardian
        Raid = { name = "Elune's Chosen Raid", hero = "Elune's Chosen", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Elune's Chosen M+", hero = "Elune's Chosen", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Elune's Chosen Delve", hero = "Elune's Chosen", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Elune's Chosen PvP", hero = "Elune's Chosen", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Den Mother", "Rage of the Sleeper", "Demoralizing Roar" } }
    },
    [105] = { -- Restoration
        Raid = { name = "Wildstalker Raid", hero = "Wildstalker", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Keeper M+", hero = "Keeper of the Grove", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Keeper Delve", hero = "Keeper of the Grove", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Keeper PvP", hero = "Keeper of the Grove", string = "CYGAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Keeper of the Grove", "Reactive Resin", "Thorns" } }
    },

    --========================================================--
    -- SHAMAN
    --========================================================--
    [262] = { -- Elemental
        Raid = { name = "Stormbringer Raid", hero = "Stormbringer", string = "CgQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Stormbringer M+", hero = "Stormbringer", string = "CgQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Stormbringer Delve", hero = "Stormbringer", string = "CgQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Stormbringer PvP", hero = "Stormbringer", string = "CgQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Control of Lava", "Grounding Totem", "Static Field Totem" } }
    },
    [263] = { -- Enhancement
        Raid = { name = "Stormbringer Raid", hero = "Stormbringer", string = "CgQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Totemic M+", hero = "Totemic", string = "CgQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Totemic Delve", hero = "Totemic", string = "CgQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Totemic PvP", hero = "Totemic", string = "CgQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Shamanism", "Ride the Lightning", "Grounding Totem" } }
    },
    [264] = { -- Restoration
        Raid = { name = "Farseer Raid", hero = "Farseer", string = "CgQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Totemic M+", hero = "Totemic", string = "CgQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Totemic Delve", hero = "Totemic", string = "CgQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Totemic PvP", hero = "Totemic", string = "CgQAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Living Tide", "Grounding Totem", "Unleash Shield" } }
    },

    --========================================================--
    -- MONK
    --========================================================--
    [268] = { -- Brewmaster
        Raid = { name = "Master of Harmony Raid", hero = "Master of Harmony", string = "C0QAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Shado-Pan M+", hero = "Shado-Pan", string = "C0QAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Shado-Pan Delve", hero = "Shado-Pan", string = "C0QAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Shado-Pan PvP", hero = "Shado-Pan", string = "C0QAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Hot Trub", "Guided Meditation", "Microbrew" } }
    },
    [269] = { -- Windwalker
        Raid = { name = "Shado-Pan Raid", hero = "Shado-Pan", string = "C0QAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Conduit M+", hero = "Conduit of the Celestials", string = "C0QAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Conduit Delve", hero = "Conduit of the Celestials", string = "C0QAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Conduit PvP", hero = "Conduit of the Celestials", string = "C0QAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Turbo Fists", "Reverse Harm", "Grapple Weapon" } }
    },
    [270] = { -- Mistweaver
        Raid = { name = "Conduit Raid", hero = "Conduit of the Celestials", string = "C0QAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Master of Harmony M+", hero = "Master of Harmony", string = "C0QAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Master of Harmony Delve", hero = "Master of Harmony", string = "C0QAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Master of Harmony PvP", hero = "Master of Harmony", string = "C0QAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Peaceweaver", "Zen Focus Tea", "Grapple Weapon" } }
    },

    --========================================================--
    -- DEMON HUNTER
    --========================================================--
    [577] = { -- Havoc
        Raid = { name = "Fel-Scarred Raid", hero = "Fel-Scarred", string = "CEkAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Aldrachi Reaver M+", hero = "Aldrachi Reaver", string = "CEkAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Aldrachi Reaver Delve", hero = "Aldrachi Reaver", string = "CEkAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Aldrachi Reaver PvP", hero = "Aldrachi Reaver", string = "CEkAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Reverse Magic", "Detainment", "Rain from Above" } }
    },
    [581] = { -- Vengeance
        Raid = { name = "Fel-Scarred Raid", hero = "Fel-Scarred", string = "CEkAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Aldrachi Reaver M+", hero = "Aldrachi Reaver", string = "CEkAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Aldrachi Reaver Delve", hero = "Aldrachi Reaver", string = "CEkAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Aldrachi Reaver PvP", hero = "Aldrachi Reaver", string = "CEkAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Illidan's Grasp", "Trample", "Reverse Magic" } }
    },

    --========================================================--
    -- DEATH KNIGHT
    --========================================================--
    [250] = { -- Blood
        Raid = { name = "San'layn Raid", hero = "San'layn", string = "CwPAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Deathbringer M+", hero = "Deathbringer", string = "CwPAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Deathbringer Delve", hero = "Deathbringer", string = "CwPAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Deathbringer PvP", hero = "Deathbringer", string = "CwPAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Strangulate", "Blood for Blood", "Decomposing Aura" } }
    },
    [251] = { -- Frost
        Raid = { name = "Deathbringer Raid", hero = "Deathbringer", string = "CwPAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Rider M+", hero = "Rider of the Apocalypse", string = "CwPAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Rider Delve", hero = "Rider of the Apocalypse", string = "CwPAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Rider PvP", hero = "Rider of the Apocalypse", string = "CwPAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Strangulate", "Delirium", "Shroud of Winter" } }
    },
    [252] = { -- Unholy
        Raid = { name = "San'layn Raid", hero = "San'layn", string = "CwPAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Rider M+", hero = "Rider of the Apocalypse", string = "CwPAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Rider Delve", hero = "Rider of the Apocalypse", string = "CwPAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Rider PvP", hero = "Rider of the Apocalypse", string = "CwPAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Strangulate", "Necrotic Wounds", "Doomburst" } }
    },

    --========================================================--
    -- EVOKER
    --========================================================--
    [1467] = { -- Devastation
        Raid = { name = "Scalecommander Raid", hero = "Scalecommander", string = "CsbAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Flameshaper M+", hero = "Flameshaper", string = "CsbAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Flameshaper Delve", hero = "Flameshaper", string = "CsbAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Flameshaper PvP", hero = "Flameshaper", string = "CsbAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Divide and Conquer", "Nullifying Shroud", "Obsidian Mettle" } }
    },
    [1468] = { -- Preservation
        Raid = { name = "Chronowarden Raid", hero = "Chronowarden", string = "CsbAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Flameshaper M+", hero = "Flameshaper", string = "CsbAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Flameshaper Delve", hero = "Flameshaper", string = "CsbAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Flameshaper PvP", hero = "Flameshaper", string = "CsbAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Dream Projection", "Nullifying Shroud", "Obsidian Mettle" } }
    },
    [1473] = { -- Augmentation
        Raid = { name = "Chronowarden Raid", hero = "Chronowarden", string = "CsbAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        MythicPlus = { name = "Scalecommander M+", hero = "Scalecommander", string = "CsbAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        Delve = { name = "Scalecommander Delve", hero = "Scalecommander", string = "CsbAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM" },
        PVP = { name = "Scalecommander PvP", hero = "Scalecommander", string = "CsbAAAAAAAAAAAAAAAAAAAAAAMzMzMzMmZmxMzMzMjZmxAAAAAAYmZmhZmxMmZmZGzMzMzMzMzMzMzMzMzMzMzMzMzM", pvpTalents = { "Born in Flame", "Nullifying Shroud", "Obsidian Mettle" } }
    }
}

------------------------------------------------------------
-- Get Best Talent Build
------------------------------------------------------------
function TalentRecommendations:GetRecommendation(specID, contentType)
    if not self.Data[specID] then return nil end
    
    -- Map generic content types to specific keys
    local key = "Raid"
    if contentType == "MYTHIC_PLUS" or contentType == "DUNGEON" then
        key = "MythicPlus"
    elseif contentType == "PVP" or contentType == "ARENA" then
        key = "PVP"
    elseif contentType == "DELVE" then
        key = "Delve"
    elseif contentType == "OPEN_WORLD" then
        key = "Delve" -- Default to Delve (Solo/Survival) for Open World
    end
    
    -- Fallback logic: Delve -> MythicPlus -> Raid
    local build = self.Data[specID][key]
    if not build then
        if key == "Delve" then build = self.Data[specID]["MythicPlus"] end
        if not build then build = self.Data[specID]["Raid"] end
    end
    
    return build
end

------------------------------------------------------------
-- Generate Import String (Returns the stored string)
------------------------------------------------------------
function TalentRecommendations:GetImportString(specID, contentType)
    local build = self:GetRecommendation(specID, contentType)
    if build then
        return build.string
    end
    return nil
end

------------------------------------------------------------
-- Get PvP Talents (Returns table of strings)
------------------------------------------------------------
function TalentRecommendations:GetPvPTalents(specID)
    local build = self.Data[specID] and self.Data[specID]["PVP"]
    if build and build.pvpTalents then
        return build.pvpTalents
    end
    return { "Gladiator's Medallion", "Safeguard", "Relentless" } -- Generic fallback
end

return TalentRecommendations
