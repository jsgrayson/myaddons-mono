-- core/Init.lua
-- Main Loader

_G.SkillWeaver = _G.SkillWeaver or {}
local SW = _G.SkillWeaver

SW.version = "0.9.0"
SW.loaded = false

local f = CreateFrame("Frame")
f:RegisterEvent("ADDON_LOADED")
f:RegisterEvent("PLAYER_LOGIN")

f:SetScript("OnEvent", function(_, event, arg1)
    if event == "ADDON_LOADED" and arg1 == "SkillWeaver" then
        SkillWeaverDB = SkillWeaverDB or {}
        SW.loaded = true

    elseif event == "PLAYER_LOGIN" then
        -- 1. Create the Secure Buttons FIRST
        if SW.SecureButtons then
            SW.SecureButtons:Init()
        end

        -- 2. Load UI
        if SW.UI then
            if SW.UI.InitPanel then SW.UI:InitPanel() end
            if SW.UI.InitMinimap then SW.UI:InitMinimap() end
        end

        -- 3. Start Engine (This pushes macros to the buttons)
        if SW.Engine and SW.Engine.RefreshAll then
            SW.Engine:RefreshAll("login")
        end
    end
end)

-- Slash Commands
SLASH_SKILLWEAVER1 = "/skillweaver"
SLASH_SKILLWEAVER2 = "/skw"

SlashCmdList.SKILLWEAVER = function(msg)
    msg = (msg or ""):lower():gsub("^%s+", ""):gsub("%s+$", "")
    
    if msg == "" or msg == "ui" then
        if SW.UI and SW.UI.TogglePanel then SW.UI:TogglePanel() end
        return
    end
    
    -- Debug / Mode switching
    if SW.State then
        local key = SW.State:GetClassSpecKey()
        if msg == "st" then SW.State:SetMode("ST")
        elseif msg == "aoe" then SW.State:SetMode("AOE")
        elseif msg == "refresh" then 
            SW.Engine:RefreshAll("manual")
            print("SkillWeaver: Engine Refreshed")
        end
    end
end