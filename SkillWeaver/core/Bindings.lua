local SW = SkillWeaver
SW.Bindings = SW.Bindings or {}

-- The only commands we allow this system to touch
local MANAGED_COMMANDS = {
    ["CLICK SkillWeaver_Button_ST:LeftButton"] = true,
    ["CLICK SkillWeaver_Button_AOE:LeftButton"] = true,
    ["CLICK SkillWeaver_Button_INT:LeftButton"] = true,
    ["CLICK SkillWeaver_Button_UTIL:LeftButton"] = true,
    ["CLICK SkillWeaver_Button_HEAL:LeftButton"] = true,
    ["CLICK SkillWeaver_Button_SELF:LeftButton"] = true,
}

function SW.Bindings:SaveProfile(profileName)
    if not profileName or profileName == "" then return end
    
    local data = {}
    
    -- Only save bindings that match our Managed Commands
    for cmd, _ in pairs(MANAGED_COMMANDS) do
        local key1, key2 = GetBindingKey(cmd)
        if key1 or key2 then
            data[cmd] = { key1, key2 }
        end
    end
    
    SkillWeaverDB.bindingProfiles[profileName] = data
    print("|cFF00FF00SkillWeaver: Saved Profile '" .. profileName .. "'|r")
end

function SW.Bindings:LoadProfile(profileName)
    if InCombatLockdown() then print("|cFFFF0000SkillWeaver: Cannot change bindings in combat!|r"); return end
    
    local data = SkillWeaverDB.bindingProfiles[profileName]
    if not data then print("|cFFFF0000SkillWeaver: Profile '"..profileName.."' not found.|r"); return end
    
    -- 1. Clear ONLY SkillWeaver bindings (Don't wipe WASD/etc)
    for cmd, _ in pairs(MANAGED_COMMANDS) do
        local k1, k2 = GetBindingKey(cmd)
        if k1 then SetBinding(k1, nil) end
        if k2 then SetBinding(k2, nil) end
    end
    
    -- 2. Load New Bindings
    for cmd, keys in pairs(data) do
        -- Check if it's one of our commands
        if MANAGED_COMMANDS[cmd] then
            -- Handle Table format (Saved) vs String format (Defaults)
            if type(keys) == "table" then
                if keys[1] then SetBinding(keys[1], cmd) end
                if keys[2] then SetBinding(keys[2], cmd) end
            elseif type(keys) == "string" then
                SetBinding(keys, cmd)
            end
        end
    end
    
    -- 3. Save to Client
    -- FIX: Removed AttemptToSaveBindings check. Just save.
    SaveBindings(GetCurrentBindingSet())
    
    SW.Defaults:SetBindingProfile(profileName)
    print("|cFF00FF00SkillWeaver: Loaded Profile '" .. profileName .. "'|r")
end
