local addonName, addon = ...
local UI = PetWeaverUI

-- Scanner Module
UI.Scanner = UI.Scanner or {}
local Scanner = UI.Scanner

-- Events
local frame = CreateFrame("Frame")
frame:RegisterEvent("PET_BATTLE_OPENING_START")
frame:RegisterEvent("PET_BATTLE_PET_CHANGED")
frame:SetScript("OnEvent", function(self, event, ...)
    if PetWeaverDB and PetWeaverDB.wishlist then
        Scanner:ScanEnemyTeam()
    end
end)

function Scanner:ScanEnemyTeam()
    local numPets = C_PetBattles.GetNumPets(2) -- 2 = Enemy
    
    for i = 1, numPets do
        local speciesID = C_PetBattles.GetPetSpeciesID(2, i)
        local quality = C_PetBattles.GetBreedQuality(2, i)
        local level = C_PetBattles.GetLevel(2, i)
        local maxHealth = C_PetBattles.GetMaxHealth(2, i)
        local power = C_PetBattles.GetPower(2, i)
        local speed = C_PetBattles.GetSpeed(2, i)
        
        -- Attempt to determine breed (Requires PetTracker or BreedID addon usually)
        -- For now, we'll try to use PetTracker if available
        local breedID = self:GetBreedID(2, i)
        
        self:CheckWishlist(speciesID, breedID)
    end
end

function Scanner:GetBreedID(owner, index)
    -- Try PetTracker
    if PetTracker and PetTracker.Predict then
        -- PetTracker logic might be complex, let's look for a simpler hook
        -- Actually, PetTracker adds a .breedID to the pet info in some contexts
    end
    
    -- Try LibPetBreedInfo if available (often embedded)
    if LibStub then
        local LibBreed = LibStub("LibPetBreedInfo-1.0", true)
        if LibBreed then
            local breed = LibBreed:GetBreedByPetBattleSlot(owner, index)
            if breed then return breed end
        end
    end
    
    return 0 -- Unknown
end

function Scanner:CheckWishlist(speciesID, breedID)
    if not PetWeaverDB.wishlist then return end
    
    for _, item in ipairs(PetWeaverDB.wishlist) do
        if item.speciesId == speciesID then
            -- Match Species! Check Breed
            if item.breedId == breedID or item.breedId == 0 then
                self:AlertUser(item.petName, item.breedName)
            elseif breedID == 0 then
                -- Warn about species match but unknown breed
                print("|cffff0000PetWeaver:|r Found " .. item.petName .. " (Breed Unknown)")
            end
        end
    end
end

function Scanner:AlertUser(petName, breedName)
    local msg = "WISH LIST MATCH: " .. petName .. " (" .. breedName .. ")!"
    
    -- Raid Warning
    RaidNotice_AddMessage(RaidWarningFrame, msg, ChatTypeInfo["RAID_WARNING"])
    
    -- Sound
    PlaySound(8959) -- Raid Warning
    
    -- Print
    print("|cff00ff00PetWeaver:|r " .. msg)
end

-- Import/Export
function Scanner:ImportWishlist(importStr)
    -- Format: speciesId:breedId,speciesId:breedId
    PetWeaverDB.wishlist = {}
    
    for item in string.gmatch(importStr, "([^,]+)") do
        local speciesId, breedId = string.match(item, "(%d+):(%d+)")
        if speciesId and breedId then
            table.insert(PetWeaverDB.wishlist, {
                speciesId = tonumber(speciesId),
                breedId = tonumber(breedId),
                petName = "Unknown", -- We don't have name DB here easily
                breedName = "ID " .. breedId
            })
        end
    end
    print("PetWeaver: Imported " .. #PetWeaverDB.wishlist .. " wishlist items.")
end
