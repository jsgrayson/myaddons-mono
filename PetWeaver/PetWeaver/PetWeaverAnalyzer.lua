local addonName, addon = ...
local UI = PetWeaverUI

-- Smart Pet Analysis Module
UI.analyzer = UI.analyzer or {}
local Analyzer = UI.analyzer

function Analyzer:CheckPetOwnership(speciesID)
    if not speciesID or speciesID == 0 then
        return false, nil
    end
    
    local numPets = C_PetJournal.GetNumPets()
    local bestPet = nil
    local bestScore = -1
    
    for i = 1, numPets do
        local petID, species, owned, _, level, _, _, _, _, _, _, _, _, _, canBattle = C_PetJournal.GetPetInfoByIndex(i)
        
        if species == speciesID and owned and canBattle then
            local _, _, petQuality = C_PetJournal.GetPetStats(petID)
            local score = (level or 1) * 100 + (petQuality or 1) * 10
            
            if score > bestScore then
                bestScore = score
                bestPet = {
                    guid = petID,
                    level = level,
                    quality = petQuality,
                    species = species
                }
            end
        end
    end
    
    return bestPet ~= nil, bestPet
end

function Analyzer:GetQualityText(quality)
    local qualities = {
        [1] = {text = "Poor", color = "|cff9d9d9d"},
        [2] = {text = "Common", color = "|cffffffff"},
        [3] = {text = "Uncommon", color = "|cff1eff00"},
        [4] = {text = "Rare", color = "|cff0070dd"}
    }
    
    local q = qualities[quality] or qualities[1]
    return q.color .. q.text .. "|r"
end

function Analyzer:GetBreedText(petID)
    -- Breed detection would require additional library
    -- For now, return placeholder
    return "P/P"  -- TODO: Integrate breed detection
end

function Analyzer:AnalyzeTeam(pet1, pet2, pet3)
    local analysis = {
        ready = true,
        totalLevel = 0,
        avgLevel = 0,
        missingPets = {},
        warnings = {}
    }
    
    local petIDs = {pet1, pet2, pet3}
    local petCount = 0
    
    for i, speciesID in ipairs(petIDs) do
        if speciesID and speciesID ~= 0 then
            local owned, petInfo = self:CheckPetOwnership(speciesID)
            
            if owned and petInfo then
                analysis.totalLevel = analysis.totalLevel + (petInfo.level or 0)
                petCount = petCount + 1
                
                if petInfo.level < 25 then
                    table.insert(analysis.warnings, {
                        slot = i,
                        message = "Pet is below level 25"
                    })
                end
            else
                analysis.ready = false
                local speciesName = C_PetJournal.GetPetInfoBySpeciesID(speciesID)
                table.insert(analysis.missingPets, {
                    slot = i,
                    speciesID = speciesID,
                    name = speciesName or "Unknown Pet"
                })
            end
        end
    end
    
    if petCount > 0 then
        analysis.avgLevel = math.floor(analysis.totalLevel / petCount)
    end
    
    return analysis
end

function Analyzer:GetPetSource(speciesID)
    -- This would ideally query a database of pet sources
    -- For now, return placeholder data
    local sources = {
        -- Wild pets (example)
        [115146] = {  -- Boneshard
            type = "wild",
            zone = "Shadowlands",
            coords = "Maldraxxus (50.0, 50.0)",
            notes = "Spawns throughout Maldraxxus"
        },
        -- Add more as needed from external database
    }
    
    local source = sources[speciesID]
    if source then
        return source
    end
    
    -- Default fallback
    return {
        type = "unknown",
        zone = "Unknown",
        coords = "Check WoWHead",
        notes = "Visit wow-petguide.com for details"
    }
end

function Analyzer:GetStatusIcon(analysis)
    if analysis.ready and analysis.avgLevel >= 24 then
        return "|cff00ff00✓|r", "[READY ✓]"
    elseif #analysis.missingPets > 0 then
        return "|cffff0000✗|r", "[MISSING PETS]"
    elseif #analysis.warnings > 0 then
        return "|cfffff000⚠|r", "[NEEDS LEVELING]"
    else
        return "|cff00ff00✓|r", "[READY ✓]"
    end
end
