local addonName, addon = ...
PetWeaverDBMixin = {}
_G.PetWeaverDBManager = PetWeaverDBMixin

-- [INITIALIZATION]
function PetWeaverDBMixin:Init()
    if not PetWeaverDB then PetWeaverDB = {} end
    if not PetWeaverDB.Strategies then PetWeaverDB.Strategies = {} end
    if not PetWeaverDB.Wishlist then PetWeaverDB.Wishlist = {} end
    if not PetWeaverDB.LevelingQueue then PetWeaverDB.LevelingQueue = {} end
    print("|cff0070ddPetWeaver:|r Database Loaded.")
end

-- [STRATEGY MANAGER]
function PetWeaverDBMixin:SaveStrategy(targetName, teamData, scriptText)
    if not targetName or targetName == "" then targetName = "Generic" end
    PetWeaverDB.Strategies[targetName] = {
        pets = teamData, -- Table of 3 pet GUIDs
        script = scriptText,
        updated = time()
    }
    print("|cff00ff00PetWeaver:|r Saved strategy for: " .. targetName)
end

function PetWeaverDBMixin:GetStrategy(targetName)
    return PetWeaverDB.Strategies[targetName]
end

-- [LEVELING QUEUE]
function PetWeaverDBMixin:EnqueuePet(petGUID)
    for _, guid in ipairs(PetWeaverDB.LevelingQueue) do
        if guid == petGUID then return end -- Prevent dupes
    end
    table.insert(PetWeaverDB.LevelingQueue, petGUID)
    print("Pet added to Leveling Queue.")
end

function PetWeaverDBMixin:GetTopLevelingPet()
    for i, petGUID in ipairs(PetWeaverDB.LevelingQueue) do
        local _, _, _, _, level = C_PetJournal.GetPetInfoByPetID(petGUID)
        local health = C_PetJournal.GetPetStats(petGUID)
        -- Validate: Exists, Not Max Level, Alive
        if level and level < 25 and health > 0 then
            return petGUID
        end
    end
    return nil
end

-- [WISHLIST HUNTER]
function PetWeaverDBMixin:ToggleWishlist(speciesID)
    if PetWeaverDB.Wishlist[speciesID] then
        PetWeaverDB.Wishlist[speciesID] = nil
        print("Removed from Wishlist.")
    else
        PetWeaverDB.Wishlist[speciesID] = { added = time() }
        print("Added to Wishlist! Scanning enabled.")
    end
end

function PetWeaverDBMixin:IsOnWishlist(speciesID)
    return PetWeaverDB.Wishlist[speciesID] ~= nil
end
