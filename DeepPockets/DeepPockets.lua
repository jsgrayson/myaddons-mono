DeepPocketsDB = DeepPocketsDB or {}

local ADDON_NAME = ...
local VERSION = "0.1.0-backend"

local function printPrefix(msg)
    print("|cff4db8ffDeepPockets|r:", msg)
end

printPrefix("LOADED backend " .. VERSION)

-- Backend namespace only
DeepPockets = DeepPockets or {}
local DP = DeepPockets
DP.version = VERSION

-- REQUIRED: implement the method your slash handler is trying to call.
function DP:ToggleTooltipTrace()
  if not DP.TooltipTrace or not DP.TooltipTrace.Toggle then
    print("|cff55aaffDP|r TooltipTrace module missing. Check DeepPockets.toc includes tooltip_trace.lua before DeepPockets.lua")
    return
  end
  DP.TooltipTrace:Toggle()
end

-- Slash commands (backend-safe, no legacy bleed)
SLASH_DEEPPOCKETS1 = "/dp"
SLASH_DEEPPOCKETS2 = "/dpb"

SlashCmdList["DEEPPOCKETS"] = function(msg)
    msg = (msg or ""):lower()

    if msg == "help" or msg == "" then
        printPrefix("Backend-only addon")
        print("  /dp help      - show this help")
        print("  /dp version   - print version")
        print("  /dp dump      - dump backend DB size")
        print("  /dp tt        - toggle tooltip trace")
        return
    end

    if msg == "version" then
        printPrefix("Version " .. VERSION)
        return
    end

    if msg == "dump" then
        local count = 0
        for _ in pairs(DeepPocketsDB) do count = count + 1 end
        printPrefix("DB entries: " .. count)
        return
    end
    
    if msg == "tt" or msg == "tooltip" or msg == "tooltiptrace" then
      DP:ToggleTooltipTrace()
      return
    end

    printPrefix("Unknown command. Use /dp help")
end
