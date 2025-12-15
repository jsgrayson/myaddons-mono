-- bootstrap.lua
-- Must be first file in TOC. Guarantees globals exist.

_G.DeepPockets = _G.DeepPockets or {}
local DP = _G.DeepPockets

-- Pull version from TOC if possible, otherwise fallback.
local metaVer = nil
if C_AddOns and C_AddOns.GetAddOnMetadata then
  metaVer = C_AddOns.GetAddOnMetadata("DeepPockets", "Version")
elseif GetAddOnMetadata then
  metaVer = GetAddOnMetadata("DeepPockets", "Version")
end

DP.VERSION = metaVer or DP.VERSION or "backend-UNKNOWN"
DP.API = DP.API or {}
DP._BOOTSTRAPPED = true

print(("|cff00ff00DeepPockets|r bootstrapped. Version=%s"):format(tostring(DP.VERSION)))
