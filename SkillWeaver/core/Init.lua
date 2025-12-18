-- core/Init.lua
_G.SkillWeaver = _G.SkillWeaver or {}
local SW = _G.SkillWeaver

SW.version = "0.9.7" 
SW.loaded = false

local f = CreateFrame("Frame")
f:RegisterEvent("ADDON_LOADED")
f:RegisterEvent("PLAYER_LOGIN")

f:SetScript("OnEvent", function(_, event, arg1)
    if event == "ADDON_LOADED" and arg1 == "SkillWeaver" then
        -- 1. Initialize Database
        if SW.Defaults and SW.Defaults.InitDB then
            SW.Defaults:InitDB()
        end
        SW.loaded = true

    elseif event == "PLAYER_LOGIN" then
        -- FAILSAFE: If ADDON_LOADED missed us (e.g. folder name mismatch), run InitDB now
        if not SW.loaded then
             if SW.Defaults and SW.Defaults.InitDB then
                 SW.Defaults:InitDB()
             end
             SW.loaded = true
        end
    
        print("|cFF00FF00SkillWeaver " .. SW.version .. " Loading...|r")

        -- 2. Init Secure Buttons
        if SW.SecureButtons then
            SW.SecureButtons:Init()
        end

        -- 3. LOAD ROTATIONS
        if SW.SpecPackLoader and SW.Rotations then
            SW.SpecPackLoader:LoadClassPack(SW.Rotations)
        end

        -- 4. Load UI
        if SW.UI then
            if SW.UI.InitPanel then SW.UI:InitPanel() end
            if SW.UI.InitMinimap then SW.UI:InitMinimap() end
        end

        -- 5. Start Engine
        if SW.Engine and SW.Engine.RefreshAll then
            SW.Engine:RefreshAll("login")
        end
        
        -- 6. FORCE UI UPDATE
        if SW.UI and SW.UI.UpdatePanel then
            SW.UI:UpdatePanel()
        end

        print("|cFF00FF00SkillWeaver Ready.|r")
    end
end)

-- Slash Commands
SLASH_SKILLWEAVER1 = "/skillweaver"
SLASH_SKILLWEAVER2 = "/sw"

SlashCmdList.SKILLWEAVER = function(msg)
    local cmd, arg = msg:match("^(%S*)%s*(.-)$")
    cmd = cmd:lower()
    
    if cmd == "save" then
        if SW.Bindings and SW.Bindings.SaveProfile then
            SW.Bindings:SaveProfile(arg)
        end
    elseif cmd == "load" then
        if SW.Bindings and SW.Bindings.LoadProfile then
            SW.Bindings:SaveProfile(arg)
        end
    elseif cmd == "ui" or cmd == "" then
        if SW.UI and SW.UI.TogglePanel then SW.UI:TogglePanel() end
    elseif cmd == "reload" then
        ReloadUI()
    elseif cmd == "debug" then
        print("SW Debug:")
        print("- Enabled:", SkillWeaverDB and SkillWeaverDB.enabled)
        print("- Mode:", SW.State and SW.State:GetMode())
        print("- ClassKey:", SW.State and SW.State:GetClassSpecKey())
        print("- Current Profile:", SW.Defaults and SW.Defaults:GetCurrentBindingProfile())
    end
end