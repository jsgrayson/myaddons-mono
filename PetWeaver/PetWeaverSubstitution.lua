local addonName, addon = ...
local UI = PetWeaverUI

-- Pet Substitution Helper
UI.petSubstitution = UI.petSubstitution or {}
local Substitution = UI.petSubstitution

-- Pet family/role mappings for smart substitution
Substitution.petRoles = {
    -- Common battle pet roles
    ["Mechanical Pandaren Dragonling"] = {role = "AoE Magic", family = "Mechanical", alternatives = {64899, 68819}},
    ["Ikky"] = {role = "Flying DPS", family = "Flying", alternatives = {68659, 85256, 106426}},
    ["Terrible Turnip"] = {role = "Humanoid Trap", family = "Humanoid", alternatives = {86713, 68560}},
    ["Anubisath Idol"] = {role = "Tank/Deflection", family = "Humanoid", alternatives = {68659, 116155}},
    ["Iron Starlette"] = {role = "Mechanical DPS", family = "Mechanical", alternatives = {77221, 64899}},
    ["Chrominius"] = {role = "Dragonkin Howl", family = "Dragonkin", alternatives = {68662, 97207}},
}

-- Ability-based substitution (common abilities)
Substitution.abilityEquivalents = {
    [119] = "Magic damage dealers",     -- Arcane Blast
    [581] = "Flying multi-hit",          -- Flock
    [919] = "Damage amplification",      -- Black Claw
    [206] = "Weather (blizzard)",        -- Call Blizzard
    [256] = "Weather (darkness)",        -- Call Darkness
    [362] = "Damage boost (Howl)",       -- Howl
    [321] = "Sacrifice/DoT",             -- Unholy Ascension
}

---
--- Find alternative pets for a specific species
---
function Substitution:FindAlternatives(speciesID)
    local speciesName = C_PetJournal.GetPetInfoBySpeciesID(speciesID)
    if not speciesName then return {} end
    
    -- Check if we have predefined alternatives
    if self.petRoles[speciesName] then
        local alts = {}
        for _, altID in ipairs(self.petRoles[speciesName].alternatives) do
            local owned = UI.analyzer and UI.analyzer:CheckPetOwnership(altID)
            if owned then
                local altName = C_PetJournal.GetPetInfoBySpeciesID(altID)
                table.insert(alts, {
                    speciesID = altID,
                    name = altName,
                    reason = "Same role: " .. self.petRoles[speciesName].role,
                    owned = true
                })
            end
        end
        return alts
    end
    
    -- Fallback: find pets of same family
    return self:FindByFamily(speciesID)
end

---
--- Find pets of the same family
---
function Substitution:FindByFamily(speciesID)
    local _, _, petType = C_PetJournal.GetPetInfoBySpeciesID(speciesID)
    if not petType then return {} end
    
    local alternatives = {}
    local numPets, numOwned = C_PetJournal.GetNumPets()
    
    for i = 1, numOwned do
        local petID, _, owned, _, level, _, _, speciesName, icon, petTypeCheck = C_PetJournal.GetPetInfoByIndex(i)
        if owned and petTypeCheck == petType and level == 25 then
            local altSpeciesID = C_PetJournal.GetPetInfoByPetID(petID)
            if altSpeciesID ~= speciesID then
                table.insert(alternatives, {
                    speciesID = altSpeciesID,
                    name = speciesName,
                    reason = "Same family (" .. _G["BATTLE_PET_NAME_"..petType] .. ")",
                    owned = true
                })
                
                -- Limit to top 5
                if #alternatives >= 5 then break end
            end
        end
    end
    
    return alternatives
end

---
--- Suggest team with substitutions for missing pets
---
function Substitution:SuggestTeam(pet1, pet2, pet3)
    local suggestions = {}
    
    for i, petID in ipairs({pet1, pet2, pet3}) do
        if petID and petID ~= 0 then
            local owned = UI.analyzer and UI.analyzer:CheckPetOwnership(petID)
            if not owned then
                -- Find alternatives
                local alts = self:FindAlternatives(petID)
                suggestions[i] = {
                    original = petID,
                    alternatives = alts,
                    hasSubs = #alts > 0
                }
            end
        end
    end
    
    return suggestions
end

---
--- Display substitution suggestions
---
function Substitution:ShowSuggestions(encounterName, suggestions)
    if not suggestions or next(suggestions) == nil then
        print("|cff00ff00PetWeaver:|r No substitutions needed - you have all pets!")
        return
    end
    
    print("|cff00ff00PetWeaver - Pet Substitutions for " .. encounterName .. ":|r")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    for slot, data in pairs(suggestions) do
        local originalName = C_PetJournal.GetPetInfoBySpeciesID(data.original)
        print(string.format("\nSlot %d: %s (MISSING)", slot, originalName))
        
        if data.hasSubs then
            print("  Alternatives you own:")
            for i, alt in ipairs(data.alternatives) do
                print(string.format("  %d. %s - %s", i, alt.name, alt.reason))
            end
        else
            print("  No good alternatives found - must obtain this pet")
        end
    end
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
end
