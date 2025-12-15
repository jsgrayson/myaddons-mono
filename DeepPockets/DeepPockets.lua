_G.DeepPockets = _G.DeepPockets or {}
local DP = _G.DeepPockets

DP.API = DP.API or {}
DP._MAIN_LOADED = true
DP._BOOTSTRAPPED = true

DP.VERSION = DP.VERSION
  or (C_AddOns and C_AddOns.GetAddOnMetadata and C_AddOns.GetAddOnMetadata("DeepPockets","Version"))
  or GetAddOnMetadata("DeepPockets","Version")
  or "0.1.0-backend-FALLBACK"

print("|cff00ff00DeepPockets MAIN LOADED|r", DP.VERSION)

local ADDON = "DeepPockets"

-- Hardcoded or fetch - user requested patching to ensure consistent behavior
local VERSION = DP.VERSION or "0.1.0-backend"

-- SavedVariables bootstrap (guarantee table exists before any module uses it)
DeepPocketsDB = DeepPocketsDB or {}
DeepPocketsDB.version = DeepPocketsDB.version or VERSION

----------------------------------------
-- Slash Commands (DeepPockets backend)
----------------------------------------
SLASH_DEEPPOCKETS1 = "/dp"
SLASH_DEEPPOCKETS2 = "/dpb"

SlashCmdList["DEEPPPOCKETS"] = nil -- in case of old key
SlashCmdList["DEEPPOCKETS"] = function(msg)
  msg = tostring(msg or "")
  local cmd, arg = msg:lower():match("^(%S+)%s*(.*)")
  cmd = cmd or "help"

  local function help()
    print("|cff00ff00DeepPockets|r backend "..VERSION.." commands: scan, dump, sanity, autoscan, whoami")
  end

  if cmd == "help" or cmd == "?" then
    help(); return
  elseif cmd == "whoami" then
    local okAPI = (_G.DeepPockets and _G.DeepPockets.API) and "OK" or "MISSING"
    print("DP whoami:", tostring(DP.VERSION), "boot=", tostring(DP._BOOTSTRAPPED), "api=", tostring(okAPI))
    return
  elseif cmd == "scan" then
    if type(_G.DeepPockets_Scan) == "function" then _G.DeepPockets_Scan(arg) else help() end
    return
  elseif cmd == "dump" then
    if type(_G.DeepPockets_Dump) == "function" then _G.DeepPockets_Dump(arg) else help() end
    return
  elseif cmd == "sanity" then
    if type(_G.DeepPockets_Sanity) == "function" then _G.DeepPockets_Sanity(arg) else help() end
    return
  elseif cmd == "autoscan" then
    if type(_G.DeepPockets_Autoscan) == "function" then _G.DeepPockets_Autoscan(arg) else help() end
    return
  else
    help(); return
  end
end
