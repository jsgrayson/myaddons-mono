local addonName, addon = ...
local UI = PetWeaverUI

-- Capture Team System
UI.captureTeam = UI.captureTeam or {}
local CaptureTeam = UI.captureTeam

-- Best pets for capturing (by species ID)
CaptureTeam.recommendedPets = {
    slot1 = {
        {id = 64899, name = "Mechanical Pandaren Dragonling", reason = "High speed + Decoy (damage reduction)"},
        {id = 68659, name = "Darkmoon Zeppelin", reason = "Missile + Decoy combo"},
    },
    slot2 = {
        {id = 86713, name = "Terrible Turnip", reason = "Weakening Blow (never kills)"},
        {id = 68663, name = "Stunted Direhorn", reason = "Trihorn Shield + weakening moves"},
    }
}

function CaptureTeam:FindBestCaptureTeam()
    local team = {nil, nil, nil}
    
    -- Slot 1: High-speed mechanical
    for _, pet in ipairs(self.recommendedPets.slot1) do
        local owned, petInfo = UI.analyzer:CheckPetOwnership(pet.id)
        if owned then
            team[1] = petInfo.guid
            break
        end
    end
    
    -- Slot 2: Weakening pet (Terrible Turnip preferred)
    for _, pet in ipairs(self.recommendedPets.slot2) do
        local owned, petInfo = UI.analyzer:CheckPetOwnership(pet.id)
        if owned then
            team[2] = petInfo.guid
            break
        end
    end
    
    -- Slot 3: Lowest level pet for leveling
    team[3] = self:FindLowestLevelPet()
    
    return team
end

function CaptureTeam:FindLowestLevelPet()
    local numPets = C_PetJournal.GetNumPets()
    local lowestPet = nil
    local lowestLevel = 26
    
    for i = 1, numPets do
        local petID, _, owned, _, level, _, _, _, _, _, _, _, _, _, canBattle = C_PetJournal.GetPetInfoByIndex(i)
        
        if owned and canBattle and level < lowestLevel and level < 25 then
            lowestLevel = level
            lowestPet = petID
        end
    end
    
    return lowestPet
end

function CaptureTeam:LoadCaptureTeam()
    local team = self:FindBestCaptureTeam()
    
    if not team[1] or not team[2] then
        print("|cffff0000PetWeaver:|r Missing recommended capture pets!")
        print("Recommended: Mechanical Pandaren Dragonling, Terrible Turnip")
        return false
    end
    
    -- Clear slots
    C_PetJournal.SetPetLoadOutInfo(1, "0x0000000000000000")
    C_PetJournal.SetPetLoadOutInfo(2, "0x0000000000000000")
    C_PetJournal.SetPetLoadOutInfo(3, "0x0000000000000000")
    
    -- Load team
    if team[1] then C_PetJournal.SetPetLoadOutInfo(1, team[1]) end
    if team[2] then C_PetJournal.SetPetLoadOutInfo(2, team[2]) end
    if team[3] then C_PetJournal.SetPetLoadOutInfo(3, team[3]) end
    
    print("|cff00ff00PetWeaver:|r Loaded capture team!")
    print("Slot 1: Tank/DPS | Slot 2: Weakening | Slot 3: Leveling")
    
    return true
end

-- Capture Strategy Script
CaptureTeam.captureScript = [[
-- PetWeaver Capture Strategy
-- Weaken target to ~35% HP, then swap to capture

-- Use high-damage moves to quickly reduce HP
if enemy.hp% > 50 then
    use(slot1:1)  -- High damage ability
else
    use(slot2:1)  -- Weakening blow (won't kill)
end

-- When target is low, pass turn or use safe moves
if enemy.hp% < 40 then
    standby
end
]]
