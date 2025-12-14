-- Backend-only core. Zero UI. Zero hooks. Safe with BetterBags.

local ADDON_NAME = ...
DeepPocketsDB = DeepPocketsDB or {}

local f = CreateFrame("Frame")
f:RegisterEvent("ADDON_LOADED")

f:SetScript("OnEvent", function(_, _, name)
    if name ~= ADDON_NAME then return end

    DeepPocketsDB.version = "0.1.0-backend"
    DeepPocketsDB.loadedAt = time()

    print("|cff00ff00DeepPockets|r: LOADED backend 0.1.0-backend")
end)

-- Minimal slash handler (backend visibility only)
SLASH_DEEPPOCKETS1 = "/dp"
SLASH_DEEPPOCKETS2 = "/dpb"

SlashCmdList["DEEPPOCKETS"] = function(msg)
    msg = (msg or ""):lower()

    if msg == "scan" then
        print("|cff00ff00DeepPockets|r: scan invoked (backend stub)")
    elseif msg == "dump" then
        print("|cff00ff00DeepPockets|r: dump invoked (backend stub)")
    elseif msg == "debug" then
        print("|cff00ff00DeepPockets|r: version", DeepPocketsDB.version)
    else
        print("|cff00ff00DeepPockets Backend|r commands:")
        print("  /dp scan")
        print("  /dp dump")
        print("  /dp debug")
    end
end
