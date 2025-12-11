local addonName, addon = ...
local UI = PetWeaverUI

-- Team Validator Module
UI.teamValidator = UI.teamValidator or {}
local Validator = UI.teamValidator

---
--- Validate team before loading
---
function Validator:ValidateTeam(pet1, pet2, pet3)
    local issues = {}
    local warnings = {}
    local petIDs = {pet1, pet2, pet3}
    
    for i, petID in ipairs(petIDs) do
        if petID and petID ~= 0 then
            local owned, petInfo = UI.analyzer:CheckPetOwnership(petID)
            local speciesName = C_PetJournal.GetPetInfoBySpeciesID(petID)
            
            if not owned then
                table.insert(issues, string.format("Slot %d: %s - NOT OWNED", i, speciesName or "Unknown"))
            elseif petInfo then
                -- Check level
                if petInfo.level < 25 then
                    table.insert(warnings, string.format("Slot %d: %s - Level %d (not max)", i, speciesName, petInfo.level))
                end
                
                -- Check health
                if petInfo.health == 0 then
                    table.insert(issues, string.format("Slot %d: %s - DEAD (revive needed)", i, speciesName))
                elseif petInfo.health < petInfo.maxHealth then
                    table.insert(warnings, string.format("Slot %d: %s - Injured (%d/%d HP)", 
                        i, speciesName, petInfo.health, petInfo.maxHealth))
                end
                
                -- Check quality (uncommon or better recommended)
                if petInfo.quality < 3 then
                    local qualityText = UI.analyzer:GetQualityText(petInfo.quality)
                    table.insert(warnings, string.format("Slot %d: %s - %s quality (Rare recommended)", 
i, speciesName, qualityText))
                end
            end
        else
            table.insert(issues, string.format("Slot %d: Empty slot", i))
        end
    end
    
    return {
        valid = #issues == 0,
        issues = issues,
        warnings = warnings,
        canLoad = #issues == 0
    }
end

---
--- Display validation results
---
function Validator:ShowValidation(validation, encounterName)
    if validation.valid and #validation.warnings == 0 then
        print("|cff00ff00PetWeaver:|r ✓ Team ready for " .. encounterName)
        return true
    end
    
    print("|cff00ff00PetWeaver - Team Validation:|r " .. encounterName)
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    if #validation.issues > 0 then
        print("|cffff0000BLOCKING ISSUES:|r")
        for _, issue in ipairs(validation.issues) do
            print("  ✗ " .. issue)
        end
    end
    
    if #validation.warnings > 0 then
        print("|cfffff000WARNINGS:|r")
        for _, warning in ipairs(validation.warnings) do
            print("  ⚠ " .. warning)
        end
    end
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    if validation.canLoad then
        print("|cff00ff00Can load team (with warnings)|r")
    else
        print("|cffff0000Cannot load team - fix issues first|r")
    end
    
    return validation.canLoad
end

---
--- Quick health check for all battle pets
---
function Validator:CheckAllPetsHealth()
    local injured = {}
    local dead = {}
    
    local numPets, numOwned = C_PetJournal.GetNumPets()
    for i = 1, numOwned do
        local petID, speciesID, owned, _, level, _, _, name, icon, petType = C_PetJournal.GetPetInfoByIndex(i)
        if owned and level == 25 then
            local health, maxHealth = C_PetJournal.GetPetStats(petID)
            if health == 0 then
                table.insert(dead, name)
            elseif health < maxHealth then
                table.insert(injured, string.format("%s (%d/%d)", name, health, maxHealth))
            end
        end
    end
    
    if #dead > 0 or #injured > 0 then
        print("|cff00ff00PetWeaver - Pet Health Check:|r")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        if #dead > 0 then
            print("|cffff0000Dead Pets:|r " .. table.concat(dead, ", "))
        end
        
        if #injured > 0 then
            print("|cfffff000Injured Pets:|r")
            for _, pet in ipairs(injured) do
                print("  " .. pet)
            end
        end
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("Use a |cff00ffffStable Master|r or |cff00ffffRevive Battle Pets|r spell")
    else
        print("|cff00ff00PetWeaver:|r ✓ All level 25 pets healthy!")
    end
end
