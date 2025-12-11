local addonName, addon = ...
local UI = PetWeaverUI

-- Map Integration Module
UI.mapHelper = UI.mapHelper or {}
local MapHelper = UI.mapHelper

-- Pet location database
MapHelper.petLocations = {
    -- Commonly Used Battle Pets
    
    -- Mechanical Pandaren Dragonling (Vendor/Engineering)
    [64899] = {
        type = "crafted",
        zone = "Engineering",
        profession = "Engineering",
        notes = "Crafted by Engineers (requires skill 300)",
        continent = "Crafted"
    },
    
    -- Terrible Turnip (Wild - Pandaria)
    [86713] = {
        type = "wild",
        mapID = 376,
        x = 53.0,
        y = 51.6,
        zone = "Valley of the Four Winds",
        continent = "Pandaria",
        notes = "Common spawn near Halfhill Market"
    },
    
    -- Ikky (Wild - Pandaria)
    [68659] = {
        type = "wild",
        mapID = 422,
        x = 67.4,
        y = 52.0,
        zone = "Isle of Giants",
        continent = "Pandaria",
        notes = "Spawns throughout the Isle of Giants"
    },
    
    -- Zandalari Anklerender (Wild - Pandaria)
    [68661] = {
        type = "wild",
        mapID = 422,
        x = 67.4,
        y = 52.0,
        zone = "Isle of Giants",
        continent = "Pandaria",
        notes = "Spawns throughout the Isle of Giants"
    },
    
    -- Zandalari Kneebiter (Wild - Pandaria)
    [68660] = {
        type = "wild",
        mapID = 422,
        x = 67.4,
        y = 52.0,
        zone = "Isle of Giants",
        continent = "Pandaria",
        notes = "Spawns throughout the Isle of Giants"
    },
    
    -- Anubisath Idol (Drop - AQ40)
    [68659] = {
        type = "drop",
        zone = "Temple of Ahn'Qiraj",
        boss = "Emperor Vek'lor",
        dropRate = "~5%",
        continent = "Kalimdor",
        notes = "Drops from Emperor Vek'lor in AQ40 raid"
    },
    
    -- Chrominius (Drop - Blackwing Lair)
    [68662] = {
        type = "drop",
        zone = "Blackwing Lair",
        boss = "Chromaggus",
        dropRate = "~5%",
        continent = "Eastern Kingdoms",
        notes = "Drops from Chromaggus in BWL raid"
    },
    
    -- Iron Starlette (Promotion)
    [77221] = {
        type = "achievement",
        zone = "Blizzard Store",
        notes = "WoW 10th Anniversary pet (no longer available)",
        continent = "N/A"
    },
    
    -- Xu-Fu, Cub of Xuen (Quest)
    [90173] = {
        type = "achievement",
        zone = "Pandaria",
        achievement = "Celestial Family",
        notes = "Complete all Celestial Tournament achievements",
        continent = "Pandaria"
    },
    
    -- Unborn Val'kyr (Wild - Northrend - Rare Spawn)
    [71163] = {
        type = "wild",
        mapID = 114,
        x = 42.0,
        y = 46.0,
        zone = "Borean Tundra",
        continent = "Northrend",
        notes = "Rare spawn across Northrend zones (multiple spawn points)"
    },
    
    -- Darkmoon Zeppelin (Vendor)
    [55367] = {
        type = "vendor",
        zone = "Darkmoon Island",
        vendorName = "Lhara",
        cost = {tickets = 90},
        continent = "Darkmoon Island",
        notes = "Cost: 90 Darkmoon Prize Tickets from Lhara"
    },
    
    -- Molten Corgi (Event)
    [90175] = {
        type = "event",
        zone = "WoW 10th Anniversary",
        event = "WoW Anniversary",
        availability = "Annual",
        continent = "N/A",
        notes = "WoW Anniversary event reward"
    },
    
    -- Boneshard (Wild - Shadowlands)
    [115146] = {
        type = "wild",
        mapID = 1536,
        x = 50.0,
        y = 50.0,
        zone = "Maldraxxus",
        continent = "Shadowlands",
        notes = "Common spawn throughout Maldraxxus"
    },
    
    -- Drafthound (Wild - Shadowlands)
    [115149] = {
        type = "wild",
        mapID = 1533,
        x = 52.0,
        y = 47.0,
        zone = "Bastion",
        continent = "Shadowlands",
        notes = "Common spawn in Bastion"
    },
    
    -- Bloodfeaster Spiderling (Wild - Maldraxxus)
    [115154] = {
        type = "wild",
        mapID = 1536,
        x = 45.0,
        y = 55.0,
        zone = "Maldraxxus",
        continent = "Shadowlands",
        notes = "Common spawn in Maldraxxus"
    },
    
    -- Crimson Skipper (Wild - Ardenweald)
    [115157] = {
        type = "wild",
        mapID = 1565,
        x = 54.0,
        y = 38.0,
        zone = "Ardenweald",
        continent = "Shadowlands",
        notes = "Common spawn in Ardenweald"
    },
    
    -- Young Garnetgullet (Wild - Korthia)
    [120276] = {
        type = "wild",
        mapID = 1961,
        x = 55.0,
        y = 50.0,
        zone = "Korthia",
        continent = "Shadowlands",
        notes = "Spawns in central Korthia"
    },
    
    -- Torghast Lurker (Wild - Torghast)
    [120279] = {
        type = "wild",
        mapID = 1543,
        x = 50.0,
        y = 50.0,
        zone = "Torghast",
        continent = "Shadowlands",
        notes = "Rare spawn in Torghast wings"
    },
    
    -- Widget the Departed (Quest)
    [115167] = {
        type = "quest",
        zone = "Maldraxxus",
        notes = "Reward from Maldraxxus storyline quests",
        continent = "Shadowlands"
    },
    
    -- Baa'l (Secret/Achievement)
    [131160] = {
        type = "achievement",
        zone = "Multiple Zones",
        achievement = "Baa'l",
        notes = "Complete the secret Baa'l puzzle (search WoWHead for guide)",
        continent = "Various"
    },
    
    -- Core Hound Pup (Promotion)
    [38381] = {
        type = "achievement",
        zone = "Blizzard Promotion",
        notes = "WoW 4th Anniversary reward (no longer available)",
        continent ="N/A"
    },
    
    -- Lil' Ragnaros (Blizzard Store)
    [50419] = {
        type = "vendor",
        zone = "Blizzard Store",
        cost = {cash = "$10"},
        notes = "Available from Blizzard Pet Store",
        continent = "Store"
    },
    
    -- Fiendish Imp (Drop)
    [27346] = {
        type = "drop",
        zone = "Dire Maul",
        boss = "Various bosses",
        dropRate = "Rare",
        continent = "Kalimdor",
        notes = "Rare drop from various Dire Maul bosses"
    },
    
    -- Nexus Whelpling (Drop)
    [68845] = {
        type = "drop",
        zone = "Coldarra",
        boss = "Blue Dragonflight mobs",
        dropRate = "~1%",
        continent = "Northrend",
        notes = "Rare drop from Blue Dragonflight mobs in Coldarra"
    },
    
    -- Shimmering Wyrmling (Wild - Shadowlands)
    [68850] = {
        type = "wild",
        mapID = 1536,
        x = 48.0,
        y = 42.0,
        zone = "Maldraxxus",
        continent = "Shadowlands",
        notes = "Spawns near Theater of Pain"
    },
    
    -- Stinker (Quest)
    [10676] = {
        type = "quest",
        zone = "Dalaran",
        notes = "Reward from 'Stinky's Escape' quest in Dalaran Sewers",
        continent = "Northrend"
    },
    
    -- Mr. Bigglesworth (Drop)
    [68657] = {
        type = "drop",
        zone = "Naxxramas",
        boss = "Kel'Thuzad",
        dropRate = "100%",
        continent = "Northrend",
        notes = "Guaranteed drop from Kel'Thuzad (once per character)"
    }
}

function MapHelper:AddWaypoint(speciesID, speciesName)
    local loc = self.petLocations[speciesID]
    if not loc then
        print("|cffff0000PetWeaver:|r No location data for " .. (speciesName or "this pet"))
        print("Visit wow-petguide.com for details")
        return false
    end
    
    -- Try TomTom first
    if TomTom then
        TomTom:AddWaypoint(loc.mapID, loc.x / 100, loc.y / 100, {
            title = speciesName or "Pet Location",
            persistent = false,
            minimap = true,
            world = true
        })
        print("|cff00ff00PetWeaver:|r Waypoint added for " .. (speciesName or "pet"))
        return true
    end
    
    -- Fallback to manual map pin or chat message
    if loc.x and loc.y then
        print("|cff00ff00PetWeaver:|r " .. (speciesName or "Pet") .. " location:")
        print(string.format("Zone: %s (%0.1f, %0.1f)", loc.zone, loc.x, loc.y))
        
        -- Try to open world map to zone
        if WorldMapFrame and WorldMapFrame.SetMapID then
            WorldMapFrame:SetMapID(loc.mapID)
        end
        
        return true
    end
    
    return false
end

function MapHelper:ExportMissingPetsList(missingPets)
    if not missingPets or #missingPets == 0 then
        print("|cff00ff00PetWeaver:|r No missing pets!")
        return
    end
    
    print("|cff00ff00PetWeaver - Missing Pets:|r")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    for i, pet in ipairs(missingPets) do
        local loc = self.petLocations[pet.speciesID]
        if loc then
            print(string.format("%d. %s - %s (%s)", i, pet.name, loc.zone, loc.type))
        else
            print(string.format("%d. %s - Check WoWHead", i, pet.name))
        end
    end
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Use /pw show to open UI for waypoints")
end

function MapHelper:GetPetLocation(speciesID)
    return self.petLocations[speciesID]
end

-- Add "Find on Map" button functionality
function MapHelper:CreateMapButton(parent, speciesID, speciesName)
    local btn = CreateFrame("Button", nil, parent, "GameMenuButtonTemplate")
    btn:SetSize(100, 22)
    btn:SetText("Find on Map")
    btn:SetNormalFontObject("GameFontNormalSmall")
    btn:SetScript("OnClick", function()
        MapHelper:AddWaypoint(speciesID, speciesName)
    end)
    
    -- Only show if we have location data
    local loc = self.petLocations[speciesID]
    if not loc then
        btn:Hide()
    end
    
    return btn
end
