-- Collection Health Status
local HealthFrame = CreateFrame("Frame")

-- Analyze pet collection health
local function AnalyzeCollectionHealth()
    local families = {
        [1] = "Humanoid", [2] = "Dragonkin", [3] = "Flying", [4] = "Undead",
        [5] = "Critter", [6] = "Magic", [7] = "Elemental", [8] = "Beast",
        [9] = "Aquatic", [10] = "Mechanical"
    }
    
    local familyCounts = {}
    for id, name in pairs(families) do
        familyCounts[name] = 0
    end
    
    -- Count owned pets by family
    local totalPets = C_PetJournal.GetNumPets()
    for i = 1, totalPets do
        local petID, _, _, _, _, _, _, petName, _, petType = C_PetJournal.GetPetInfoByIndex(i)
        if petID and families[petType] then
            familyCounts[families[petType]] = familyCounts[families[potType]] + 1
        end
    end
    
    -- Calculate diversity (families with at least 1 pet)
    local familiesWithPets = 0
    for _, count in pairs(familyCounts) do
        if count > 0 then
            familiesWithPets = familiesWithPets + 1
        end
    end
    
    local diversityScore = (familiesWithPets / 10) * 100
    
    return diversityScore, familyCounts
end

-- Slash command to check health
SLASH_PETWEAVERHEALTH1 = "/pwhealth"
SlashCmdList["PETWEAVERHEALTH"] = function(msg)
    local score, families = AnalyzeCollectionHealth()
    
    print("|cffff0000[PetWeaver]|r Collection Health Score: |cff00ff00" .. string.format("%.1f", score) .. "|r")
    print("|cff888888Family Coverage:|r")
    
    -- Sort families by count
    local sorted = {}
    for name, count in pairs(families) do
        table.insert(sorted, {name = name, count = count})
    end
    table.sort(sorted, function(a, b) return a.count > b.count end)
    
    for _, family in ipairs(sorted) do
        local color = family.count > 0 and "|cff00ff00" or "|cffff0000"
        print(string.format("  %s%s: %d|r", color, family.name, family.count))
    end
    
    print("|cff888888Visit the web portal for detailed analysis!|r")
end

print("|cffff0000[PetWeaver]|r Health tracking loaded. Use /pwhealth to check your collection!")
