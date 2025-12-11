local addonName, addon = ...

-- Configuration
addon.autoLoadEnabled = true  -- Can be toggled by user

-- Slash command handler
SLASH_PETWEAVER1 = "/pw"
SLASH_PETWEAVER2 = "/petweaver"
SLASH_PETWEAVER1 = "/pw"
SLASH_PETWEAVER2 = "/petweaver"
SlashCmdList["PETWEAVER"] = function(msg)
    local encounterName = msg:trim()
    
    if encounterName == "show" or encounterName == "ui" then
        if PetWeaverUI and PetWeaverUI.Toggle then
            PetWeaverUI:Toggle()
        else
            print("|cffff0000Error:|r UI not loaded yet")
        end
        return
    end
    
    if encounterName == "capture" then
        if PetWeaverUI and PetWeaverUI.captureTeam then
            PetWeaverUI.captureTeam:LoadCaptureTeam()
        else
            print("|cffff0000Error:|r Capture system not loaded yet")
        end
        return
    end
    
    if encounterName == "toggle" then
        addon.autoLoadEnabled = not addon.autoLoadEnabled
        local status = addon.autoLoadEnabled and "|cff00ff00ENABLED|r" or "|cffff0000DISABLED|r"
        print("|cff00ff00PetWeaver:|r Auto-load is now " .. status)
        return
    end
    
    if encounterName == "" or encounterName == "list" then
        print("|cff00ff00PetWeaver:|r Usage: /pw [Encounter Name]")
        print("Commands:")
        print("  /pw show - Open UI")
        print("  /pw capture - Load capture team")
        print("  /pw toggle - Toggle auto-load on/off")
        print("Available encounters:")
        for name, _ in pairs(PetWeaverDB) do
            print("- " .. name)
        end
        return
    end
    
    addon:LoadTeam(encounterName)
end

function addon:LoadTeam(encounterName)
    local team = PetWeaverDB[encounterName]
    if not team then
        print("|cffff0000Error:|r Encounter '" .. encounterName .. "' not found in PetWeaverDB.")
        return
    end
    
    print("|cff00ff00PetWeaver:|r Loading team for " .. encounterName)
    
    -- Clear current team
    C_PetJournal.SetPetLoadOutInfo(1, "0x0000000000000000")
    C_PetJournal.SetPetLoadOutInfo(2, "0x0000000000000000")
    C_PetJournal.SetPetLoadOutInfo(3, "0x0000000000000000")
    
    -- Load pets
    addon:SlotPet(1, team.pet1)
    addon:SlotPet(2, team.pet2)
    addon:SlotPet(3, team.pet3)
    
    -- Print script
    if team.script and team.script ~= "" then
        print("|cff00ffffScript:|r")
        print(team.script)
    end
end

function addon:SlotPet(slot, speciesID)
    if speciesID == 0 then return end -- Empty slot
    
    local guid = addon:FindPetGUID(speciesID)
    if guid then
        C_PetJournal.SetPetLoadOutInfo(slot, guid)
        print("Slot " .. slot .. ": Loaded " .. C_PetJournal.GetPetInfoBySpeciesID(speciesID))
    else
        print("|cffff0000Error:|r Could not find pet with Species ID " .. speciesID)
    end
end

function addon:FindPetGUID(speciesID)
    -- Scan pet journal for the best version of this pet
    local bestGUID = nil
    local bestScore = -1
    
    local numPets, _ = C_PetJournal.GetNumPets()
    for i = 1, numPets do
        local petID, species, _, _, level, _, _, _, _, _, _, _, _, _, _, _, _, _ = C_PetJournal.GetPetInfoByIndex(i)
        if species == speciesID and petID then
            if level > bestScore then
                bestScore = level
                bestGUID = petID
            end
        end
    end
    
    return bestGUID
end

function string:trim()
   return self:match("^%s*(.-)%s*$")
end

-- Event Frame for auto-loading
local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("PLAYER_TARGET_CHANGED")
eventFrame:RegisterEvent("ADDON_LOADED")

eventFrame:SetScript("OnEvent", function(self, event, ...)
    if event == "ADDON_LOADED" and ... == addonName then
        print("|cff00ff00PetWeaver:|r Loaded! Type /pw list to see available encounters.")
        print("|cff00ff00PetWeaver:|r Auto-load is ENABLED. Target a pet battle NPC to load the team.")
    elseif event == "PLAYER_TARGET_CHANGED" and addon.autoLoadEnabled then
        addon:OnTargetChanged()
    end
end)

function addon:OnTargetChanged()
    if not UnitExists("target") then return end
    
    local targetName = UnitName("target")
    if not targetName then return end
    
    -- Check if we have a team for this target
    local team = PetWeaverDB[targetName]
    if team then
        print("|cff00ff00PetWeaver:|r Detected '" .. targetName .. "'! Auto-loading team...")
        addon:LoadTeam(targetName)
    end
end

