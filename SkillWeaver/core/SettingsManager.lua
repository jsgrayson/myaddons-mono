--========================================================--
-- SkillWeaver - Settings Manager
-- Handles SavedVariables persistence and per-character config
--========================================================--

local ADDON_NAME, SkillWeaver = ...
local SettingsManager = {}
SkillWeaver.SettingsManager = SettingsManager

-- Default Settings
local DEFAULTS = {
    global = {
        minimap = { hide = false, minimapPos = 220 },
        usageStats = { totalCasts = 0, timeInCombat = 0 },
    },
    char = {
        consumables = {
            enabled = false,
            usePotions = true,
            useFlasks = true,
            useFood = true,
            useAugmentRunes = true,
            potionHealthThreshold = 35,
            healthstoneThreshold = 30,
            lowStockWarning = true,
            lowStockThreshold = 5,
        },
        utilities = {
            autoInterrupt = true,
            emergencyAllyHealing = true,
            petAutoManagement = true,
            autoBattleRes = true,
            autoTrinkets = true,
            autoRacials = true,
            autoLossControl = true,
            autoBuffs = true,
        },
        equipment = {
            autoEquip = false, -- Default off for safety
        }
    }
}

------------------------------------------------------------
-- Initialize Settings
------------------------------------------------------------
function SettingsManager:Initialize()
    -- SkillWeaverDB is the SavedVariable defined in TOC
    SkillWeaverDB = SkillWeaverDB or {}
    
    -- Global Settings
    self.Global = SkillWeaverDB
    for k, v in pairs(DEFAULTS.global) do
        if self.Global[k] == nil then self.Global[k] = v end
    end
    
    -- Per-Character Settings
    -- Key format: "PlayerName-RealmName"
    local charKey = UnitName("player") .. "-" .. GetRealmName()
    SkillWeaverDB.Profiles = SkillWeaverDB.Profiles or {}
    SkillWeaverDB.Profiles[charKey] = SkillWeaverDB.Profiles[charKey] or {}
    
    self.Char = SkillWeaverDB.Profiles[charKey]
    
    -- Deep copy defaults if missing
    self:MergeDefaults(self.Char, DEFAULTS.char)
    
    -- Link to main SkillWeaver.Settings for backward compatibility/ease of use
    SkillWeaver.Settings = self.Char
    SkillWeaver.GlobalSettings = self.Global
    
    print("|cff00FF00SkillWeaver:|r Settings loaded for " .. charKey)
end

------------------------------------------------------------
-- Helper: Merge Defaults
------------------------------------------------------------
function SettingsManager:MergeDefaults(dest, src)
    for k, v in pairs(src) do
        if type(v) == "table" then
            dest[k] = dest[k] or {}
            self:MergeDefaults(dest[k], v)
        else
            if dest[k] == nil then dest[k] = v end
        end
    end
end

------------------------------------------------------------
-- Event Handler for Loading
------------------------------------------------------------
local f = CreateFrame("Frame")
f:RegisterEvent("ADDON_LOADED")
f:SetScript("OnEvent", function(self, event, arg1)
    if event == "ADDON_LOADED" and arg1 == ADDON_NAME then
        SettingsManager:Initialize()
        self:UnregisterEvent("ADDON_LOADED")
    end
end)

return SettingsManager
