local SW = SkillWeaver
SW.Profiles = SW.Profiles or {}

-- Helper to find a loadout by name in the default UI
local function FindLoadoutID(name)
    local specID = PlayerUtil.GetCurrentSpecID()
    local configID = C_ClassTalents.GetActiveConfigID()
    if not configID then return nil end
    
    local specs = C_ClassTalents.GetConfigIDsBySpecID(specID)
    for _, id in ipairs(specs) do
        local info = C_Traits.GetConfigInfo(id)
        if info and info.name == name then
            return id
        end
    end
    return nil
end

function SW.Profiles:LoadProfile(classSpecKey, mode, profileName)
    if InCombatLockdown() then 
        print("|cFFFF0000[SW] Cannot switch profiles in combat!|r")
        return 
    end
    
    -- 1. Update Internal State
    SW.State:SetMode(mode)
    
    -- 2. Smart Talent Switching
    self:ApplyTalents(classSpecKey, mode)
    
    -- 3. Refresh Engine
    SW.Engine:RefreshAll("profile_load")
end

function SW.Profiles:ApplyTalents(classSpecKey, mode)
    local suggestions = SW.TalentSuggestions and SW.TalentSuggestions[classSpecKey]
    if not suggestions then return end
    
    -- Get the string
    local tStr = (suggestions[mode] and suggestions[mode].talents) 
              or (suggestions.PvE and suggestions.PvE[mode] and suggestions.PvE[mode].talents)
    
    if not tStr then return end

    -- A. TRY AUTO-SWITCH (Look for "SW [Mode]")
    local targetLoadoutName = "SW " .. mode
    local loadoutID = FindLoadoutID(targetLoadoutName)

    if loadoutID then
        -- Attempt to load existing config
        local status = C_ClassTalents.LoadConfig(loadoutID, true)
        if status ~= 0 then -- 0 is success in some APIs, check return
            -- Trigger UI Toast: Success
            if SW.UI and SW.UI.ShowToast then
                SW.UI:ShowToast("Auto-Switched Talents", "Loaded: " .. targetLoadoutName, "SUCCESS")
            else
                print("|cFF00FF00[SW] Auto-Switched to: " .. targetLoadoutName .. "|r")
            end
        end
    else
        -- B. FALLBACK: PROMPT IMPORT
        -- We didn't find a loadout named "SW [Mode]", so show the string
        if SW.UI and SW.UI.ShowImportModal then
            SW.UI:ShowImportModal(mode, tStr)
        else
            -- Legacy Fallback
            print("|cFF00B4FF[SW] No loadout named '"..targetLoadoutName.."' found.|r")
            print("Copy this string to create it:")
            print(tStr)
        end
    end
end

function SW.Profiles:GetActiveProfileName(key) return "Balanced" end
