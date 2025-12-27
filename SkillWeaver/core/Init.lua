-- core/Init.lua
_G.SkillWeaver = _G.SkillWeaver or {}
local SW = _G.SkillWeaver

SW.version = "0.9.7" 
print("|cFFFFFF00[SkillWeaver] Core Loading...|r")
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
    
    if cmd == "bars" or cmd == "populate" or cmd == "fixbars" or cmd == "fix" then
        if SkillWeaver.PopulateBars then 
            SkillWeaver:PopulateBars() 
        elseif SkillWeaver.RestoreBars then
            SkillWeaver:RestoreBars()
        else
            print("SkillWeaver Error: PopulateBars function not found!")
        end
    elseif cmd == "save" then
        if SW.Bindings and SW.Bindings.SaveProfile then
            SW.Bindings:SaveProfile(arg)
        end
    elseif cmd == "ui" or cmd == "" then
        if SkillWeaverFrame then
            if SkillWeaverFrame:IsShown() then
                SkillWeaverFrame:Hide()
            else
                SkillWeaverFrame:Show()
            end
        else
            print("SkillWeaver Error: SkillWeaverFrame not found!")
        end
    elseif cmd == "reload" then
        ReloadUI()
    elseif cmd == "debug" then
        print("SW Debug:")
        print("- Enabled:", SkillWeaverDB and SkillWeaverDB.enabled)
        print("- Mode:", SW.State and SW.State:GetMode())
    elseif cmd == "help" then
        print("|cFFFFFF00SkillWeaver Commands:|r")
        print("  /sw bars - Populate action bars with spells")
        print("  /sw ui - Toggle UI")
        print("  /sw debug - Show debug info")
        print("  /sw reload - Reload UI")
    end
end