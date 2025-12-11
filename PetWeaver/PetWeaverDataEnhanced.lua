-- PetWeaver Enhanced Data Structure (supports multiple strategies per encounter)
-- This file demonstrates the new format with category tags and alternative strategies

PetWeaverEnhancedDB = {
    ["Robot Rumble"] = {
        expansion = "Shadowlands",
        zone = "Maldraxxus",
        category = "World Quest",
        difficulty = "Medium",
        
        -- Multiple strategy options
        strategies = {
            {
                name = "Standard Team",
                tags = {"reliable", "common-pets"},
                rating = "Safe",
                pet1 = 115146,  -- Boneshard
                pet2 = 86447,   -- Teroclaw Hatchling
                pet3 = 143564,  -- Fragment of Suffering
                script = [[use(Blistering Cold:786)
use(Chop:943) [!enemy.aura(Bleeding:491).exists]
use(BONESTORM!!:1762)
use(Chop:943)
use(Black Claw:919) [!enemy.aura(Black Claw:918).exists]
use(Flock:581)
standby
change(next)]]
            }
            -- Additional strategies would go here
        }
    },
    
    ["Major Malfunction"] = {
        expansion = "Shadowlands",
        zone = "Maldraxxus",
        category = "World Quest",
        difficulty = "Easy",
        
        strategies = {
            {
                name = "Magic Spam",
                tags = {"f2p", "quick"},
                rating = "Fast",
                pet1 = 55367,   -- Darkmoon Zeppelin
                pet2 = 64899,   -- Mechanical Pandaren Dragonling
                pet3 = 86716,   -- Tideskipper
                script = [[use(Thunderbolt:779) [round=1]
use(Explode:282)
use(Call Blizzard:206)
use(#1)
change(next)]]
            }
        }
    }
}

-- Metadata helper
PetWeaverEnhancedDB._meta = {
    version = "2.0",
    lastUpdated = "2025-11-21",
    totalEncounters = 0,
    
    -- Category definitions
    categories = {
        "World Quest",
        "Dungeon",
        "Raid",
        "Trainer",
        "Celestial Tournament",
        "PvP",
        "Wild Battle"
    },
    
    -- Expansion list
    expansions = {
        "The War Within",
        "Dragonflight",
        "Shadowlands",
        "Battle for Azeroth",
        "Legion",
        "Warlords of Draenor",
        "Mists of Pandaria",
        "Cataclysm",
        "Wrath of the Lich King",
        "The Burning Crusade",
        "Classic"
    },
    
    -- Difficulty ratings
    difficulties = {
        "Very Easy",
        "Easy",
        "Medium",
        "Hard",
        "Very Hard"
    },
    
    -- Strategy tags
    strategyTags = {
        "f2p",          -- Free to play pets only
        "budget",       -- Common/uncommon pets
        "speed",        -- Quick battles
        "safe",         -- Low risk of failure
        "reliable",     -- Consistent wins
        "common-pets",  -- Uses commonly owned pets
        "rare-pets",    -- Requires rare pets
        "leveling",     -- Good for leveling a carry pet
        "achievement"   -- Required for achievements
    }
}
