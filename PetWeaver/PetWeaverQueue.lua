local addonName, addon = ...
local UI = PetWeaverUI

-- Queue Manager Module
UI.queueManager = UI.queueManager or {}
local QueueManager = UI.queueManager

-- Queue storage
QueueManager.levelingQueue = {}
QueueManager.gatheringQueue = {}
QueueManager.currentMode = "none" -- "leveling" or "gathering"

---
--- LEVELING QUEUE SYSTEM (Encounter-Based)
---

function QueueManager:GenerateLevelingQueueForEncounters(selectedEncounters)
    if not selectedEncounters or #selectedEncounters == 0 then
        print("|cffff0000PetWeaver:|r No encounters selected")
        return {}
    end
    
    -- Step 1: Identify which pets are needed and their current state
    local neededPets = {}
    
    for _, encounterName in ipairs(selectedEncounters) do
        local data = PetWeaverDB[encounterName]
        if data then
            local petIDs = {data.pet1, data.pet2, data.pet3}
            for _, petID in ipairs(petIDs) do
                if petID and petID ~= 0 then
                    local owned, petInfo = UI.analyzer:CheckPetOwnership(petID)
                    if owned and petInfo then
                        if petInfo.level < 25 then
                            -- Pet is owned but needs leveling
                            if not neededPets[petID] then
                                neededPets[petID] = {
                                    speciesID = petID,
                                    name = C_PetJournal.GetPetInfoBySpeciesID(petID),
                                    currentLevel = petInfo.level,
                                    guid = petInfo.guid,
                                    neededFor = {}
                                }
                            end
                            table.insert(neededPets[petID].neededFor, encounterName)
                        end
                    end
                end
            end
        end
    end
    
    -- Step 2: For each pet that needs leveling, find encounters where it can be leveled
    local levelingPlan = {}
    
    for speciesID, petData in pairs(neededPets) do
        local levelingEncounters = self:FindLevelingEncountersForPet(petData.guid, petData.currentLevel)
        
        table.insert(levelingPlan, {
            pet = petData,
            encounters = levelingEncounters,
            priority = #petData.neededFor  -- More encounters = higher priority
        })
    end
    
    -- Sort by priority (pets needed for most encounters first)
    table.sort(levelingPlan, function(a, b) return a.priority > b.priority end)
    
    self.levelingQueue = levelingPlan
    self.currentMode = "leveling"
    
    print(string.format("|cff00ff00PetWeaver:|r Generated leveling queue for %d pets needed for %d encounters", 
        #levelingPlan, #selectedEncounters))
    
    return levelingPlan
end

function QueueManager:FindLevelingEncountersForPet(petGUID, petLevel)
    -- Find encounters where this specific pet can safely participate for leveling
    local candidates = {}
    
    for encounterName, data in pairs(PetWeaverDB) do
        local analysis = UI.analyzer:AnalyzeTeam(data.pet1, data.pet2, data.pet3)
        
        -- Must be a ready encounter (all other pets owned)
        if analysis.ready then
            local score = self:ScoreEncounterForPetLeveling(encounterName, data, petLevel)
            if score > 0 then
                table.insert(candidates, {
                    name = encounterName,
                    score = score
                })
            end
        end
    end
    
    -- Sort by score and return top 5
    table.sort(candidates, function(a, b) return a.score > b.score end)
    
    local result = {}
    for i = 1, math.min(5, #candidates) do
        table.insert(result, candidates[i].name)
    end
    
    return result
end


function QueueManager:ScoreEncounterForPetLeveling(encounterName, data, petLevel)
    local score = 30  -- Base score
    
    -- Bonus for quick encounters
    if data.script then
        local lineCount = select(2, data.script:gsub('\n', '\n'))
        if lineCount < 10 then
            score = score + 20
        elseif lineCount < 20 then
            score = score + 10
        end
    end
    
    -- Safety check for low-level pets
    if petLevel < 15 then
        if encounterName:match("Easy") or encounterName:match("Beginner") or encounterName:match("Intro") then
            score = score + 25
        end
    end
    
    -- Penalty for travel-intensive encounters
    if encounterName:match("Dungeon") or encounterName:match("Raid") or encounterName:match("Instance") then
        score = score - 15
    end
    
    return score
end


---
--- PET GATHERING QUEUE SYSTEM (Encounter-Based)
---

function QueueManager:GenerateGatheringQueueForEncounters(selectedEncounters)
    if not selectedEncounters or #selectedEncounters == 0 then
        print("|cffff0000PetWeaver:|r No encounters selected")
        return {}
    end
    
    -- Step 1: Find all missing pets needed for selected encounters
    local missingPets = {}
    
    for _, encounterName in ipairs(selectedEncounters) do
        local data = PetWeaverDB[encounterName]
        if data then
            local analysis = UI.analyzer:AnalyzeTeam(data.pet1, data.pet2, data.pet3)
            
            for _, missingPet in ipairs(analysis.missingPets) do
                if not missingPets[missingPet.speciesID] then
                    missingPets[missingPet.speciesID] = {
                        name = missingPet.name,
                        speciesID = missingPet.speciesID,
                        neededFor = {}
                    }
                end
                table.insert(missingPets[missingPet.speciesID].neededFor, encounterName)
            end
        end
    end
    
    -- Step 2: Group missing pets by zone for efficient gathering
    local petsByZone = {}
    
    for speciesID, petData in pairs(missingPets) do
        local location = UI.mapHelper:GetPetLocation(speciesID)
        if location then
            local zone = location.zone or "Unknown"
            local continent = location.continent or "Unknown"
            
            if not petsByZone[continent] then
                petsByZone[continent] = {}
            end
            if not petsByZone[continent][zone] then
                petsByZone[continent][zone] = {
                    zoneName = zone,
                    continent = continent,
                    pets = {}
                }
            end
            
            table.insert(petsByZone[continent][zone].pets, {
                name = petData.name,
                speciesID = speciesID,
                location = location,
                neededFor = petData.neededFor,
                priority = #petData.neededFor  -- More encounters = higher priority
            })
        else
            -- No location data - add to "Check WoWHead" list
            if not petsByZone["No Location Data"] then
                petsByZone["No Location Data"] = {}
            end
            if not petsByZone["No Location Data"]["Manual Lookup"] then
                petsByZone["No Location Data"]["Manual Lookup"] = {
                    zoneName = "Manual Lookup Required",
                    continent = "N/A",
                    pets = {}
                }
            end
            
            table.insert(petsByZone["No Location Data"]["Manual Lookup"].pets, {
                name = petData.name,
                speciesID = speciesID,
                location = nil,
                neededFor = petData.neededFor,
                priority = #petData.neededFor
            })
        end
    end
    
    -- Step 3: Create optimized gathering route
    local route = {}
    
    for continent, zones in pairs(petsByZone) do
        for zoneName, zoneData in pairs(zones) do
            -- Sort pets within zone by priority, then by coordinates
            table.sort(zoneData.pets, function(a, b)
                if a.priority ~= b.priority then
                    return a.priority > b.priority
                end
                if a.location and b.location and a.location.x and b.location.x then
                    return a.location.x < b.location.x
                end
                return true
            end)
            
            table.insert(route, {
                continent = continent,
                zone = zoneName,
                pets = zoneData.pets,
                count = #zoneData.pets
            })
        end
    end
    
    -- Sort route by: 1) pet count (most first), 2) continent grouping
    table.sort(route, function(a, b)
        if a.count ~= b.count then
            return a.count > b.count
        end
        return a.continent < b.continent
    end)
    
    self.gatheringQueue = route
    self.currentMode = "gathering"
    
    local totalPets = 0
    for _, stop in ipairs(route) do
        totalPets = totalPets + stop.count
    end
    
    print(string.format("|cff00ff00PetWeaver:|r Gathering queue: %d pets across %d zones needed for %d encounters", 
        totalPets, #route, #selectedEncounters))
    
    return route
end


function QueueManager:SetWaypointsForZone(zoneData)
    if not zoneData or not zoneData.pets then return end
    
    for _, pet in ipairs(zoneData.pets) do
        UI.mapHelper:AddWaypoint(pet.speciesID, pet.name)
    end
    
    print(string.format("|cff00ff00PetWeaver:|r Set %d waypoints in %s", #zoneData.pets, zoneData.zone))
end

---
--- QUEUE NAVIGATION
---

function QueueManager:GetNextInQueue()
    if self.currentMode == "leveling" then
        if #self.levelingQueue > 0 then
            return table.remove(self.levelingQueue, 1)
        end
    elseif self.currentMode == "gathering" then
        -- For gathering, return next zone
        if #self.gatheringQueue > 0 then
            return self.gatheringQueue[1] -- Don't remove, user marks complete
        end
    end
    return nil
end

function QueueManager:MarkZoneComplete(zoneName)
    for i, zoneData in ipairs(self.gatheringQueue) do
        if zoneData.zone == zoneName then
            table.remove(self.gatheringQueue, i)
            print(string.format("|cff00ff00PetWeaver:|r Zone complete: %s", zoneName))
            return true
        end
    end
    return false
end

function QueueManager:ClearQueue()
    self.levelingQueue = {}
    self.gatheringQueue = {}
    self.currentMode = "none"
end

function QueueManager:GetQueueStatus()
    if self.currentMode == "leveling" then
        return string.format("Leveling Queue: %d encounters remaining", #self.levelingQueue)
    elseif self.currentMode == "gathering" then
        local totalPets = 0
        for _, zone in ipairs(self.gatheringQueue) do
            totalPets = totalPets + zone.count
        end
        return string.format("Gathering Queue: %d pets in %d zones", totalPets, #self.gatheringQueue)
    else
        return "No active queue"
    end
end
