-- PetWeaverWildAlert.lua
-- Alerts when a wanted wild pet is found (mouseover or nameplate)

local addonName, addon = ...
PetWeaverWildAlert = {}
local alert = PetWeaverWildAlert

-- Configuration
local ALERT_SOUND = "Sound\\Interface\\RaidWarning.ogg"
local HIGH_VALUE_SOUND = "Sound\\Interface\\PVPFlagTakenMono.ogg"
local COOLDOWN = 5 -- Seconds between alerts for same pet

local lastAlertTime = 0
local lastAlertGUID = nil

function alert:Initialize()
    print("|cFF00FF00PetWeaver Wild Alert loaded!|r")
    self:RegisterEvents()
end

function alert:RegisterEvents()
    local frame = CreateFrame("Frame")
    frame:RegisterEvent("UPDATE_MOUSEOVER_UNIT")
    frame:RegisterEvent("NAME_PLATE_UNIT_ADDED")
    
    frame:SetScript("OnEvent", function(_, event, unit)
        if event == "UPDATE_MOUSEOVER_UNIT" then
            self:CheckUnit("mouseover")
        elseif event == "NAME_PLATE_UNIT_ADDED" then
            self:CheckUnit(unit)
        end
    end)
end

function alert:CheckUnit(unit)
    if not UnitExists(unit) then return end
    if not UnitIsWildBattlePet(unit) then return end
    
    local guid = UnitGUID(unit)
    if not guid then return end
    
    -- Anti-spam
    local now = GetTime()
    if guid == lastAlertGUID and (now - lastAlertTime) < COOLDOWN then
        return
    end
    
    -- Get Species ID from GUID
    -- Wild Pet GUID format: BattlePet-0-MapID-InstanceID-ZoneUID-ID-0000000000
    -- The 6th field is the Species ID in hex? No, it's usually CreatureID.
    -- Reliable way is to scan tooltip or use C_PetJournal if we can target it.
    
    local speciesID = self:GetSpeciesIDFromTooltip(unit)
    
    if speciesID and PetWeaverWanted and PetWeaverWanted[speciesID] then
        local info = PetWeaverWanted[speciesID]
        self:TriggerAlert(info, guid)
    end
end

function alert:GetSpeciesIDFromTooltip(unit)
    local tooltip = C_TooltipInfo.GetUnit(unit)
    if not tooltip then return nil end
    
    -- Tooltip data usually contains the species ID in the args or we have to parse text
    -- But simpler: Use the name! We indexed PetWeaverWanted by name too.
    local name = UnitName(unit)
    if name and PetWeaverWanted[name] then
        return PetWeaverWanted[name].id
    end
    
    return nil
end

function alert:TriggerAlert(info, guid)
    local now = GetTime()
    lastAlertTime = now
    lastAlertGUID = guid
    
    local message = "|cFF00FF00[PetWeaver] FOUND WANTED PET:|r " .. info.name
    
    if info.count > 0 then
        message = message .. " (Needed for " .. info.count .. " strategies)"
        PlaySoundFile(ALERT_SOUND)
    end
    
    if info.value and info.value > 500 then
        message = message .. " |cFFFFD700(Value: " .. GetCoinTextureString(info.value * 10000) .. ")|r"
        PlaySoundFile(HIGH_VALUE_SOUND)
    end
    
    print(message)
    RaidNotice_AddMessage(RaidWarningFrame, "WANTED PET: " .. info.name, ChatTypeInfo["RAID_WARNING"])
end

alert:Initialize()
