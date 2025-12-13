-- DeepPockets.lua
DeepPockets = DeepPockets or {}
local addonName, ns = ...
DeepPockets.name = addonName

-- Global DB
DeepPocketsDB = DeepPocketsDB or {}

-- Slash Commands
SLASH_DEEPPOCKETS1 = "/dp"
SlashCmdList["DEEPPOCKETS"] = function(msg)
    msg = tostring(msg or "")
    local cmd, arg = msg:lower():match("^(%S+)%s*(.*)$")
    cmd = cmd or ""

    if cmd == "scan" then
        local ok, err = DeepPockets.API.ScanNow()
        if ok then
            print("|cffDAA520DeepPockets|r: Scan complete.")
        else
            print("|cffDAA520DeepPockets|r: Scan failed: " .. tostring(err))
        end

    elseif cmd == "dump" then
        local db = DeepPockets.API.GetIndex()
        local inv = DeepPocketsDB.inventory
        local count = 0
        for _ in pairs(inv) do count = count + 1 end
        
        local cats = 0
        if db.by_category then
            for _ in pairs(db.by_category) do cats = cats + 1 end
        end
        
        print(("DP DUMP: Inv=%d items, Cats=%d"):format(count, cats))

    elseif cmd == "sanity" then
        local db = DeepPocketsDB
        print("DP SANITY: Version=" .. tostring(db.version) .. " Enabled=" .. tostring(db.settings.enabled))

    elseif cmd == "enable" then
        DeepPockets.API.SetEnabled(true)
        print("|cffDAA520DeepPockets|r: Enabled.")

    elseif cmd == "disable" then
        DeepPockets.API.SetEnabled(false)
        print("|cffDAA520DeepPockets|r: Disabled.")

    else
        print("|cffDAA520DeepPockets|r: /dp scan | dump | sanity | enable | disable")
    end
end

-- Bootstrap
local f = CreateFrame("Frame")
f:RegisterEvent("ADDON_LOADED")
f:RegisterEvent("PLAYER_LOGIN")
f:SetScript("OnEvent", function(_, event, name)
    if event == "ADDON_LOADED" and name == addonName then
        DeepPockets.Migrate.Ensure()
        -- Initial scan if enabled? Maybe wait for PLAYER_LOGIN
    elseif event == "PLAYER_LOGIN" then
        if DeepPockets.API.IsEnabled() then
            -- Optional initial scan or just index rebuild
            -- DeepPockets.API.ScanNow() 
            print("|cffDAA520DeepPockets|r: Backend ready.")
        end
    end
end)
