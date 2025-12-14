-- dp_ext/api.lua
-- Stable, versioned API contract + lightweight event bus (no Ace).

DeepPocketsDB = DeepPocketsDB or {}
DeepPockets = DeepPockets or {}

local DP = DeepPockets

DP.VERSION = DP.VERSION or "0.1.0-backend"

DP.API = DP.API or {}
local API = DP.API

-- Capability map: other addons can feature-detect safely.
API.capabilities = API.capabilities or {
  backend = true,
  scan = true,
  dump = true,
  provenance = true, -- if dp_ext/provenance.lua is present
  upgrade = true,    -- if your upgrade module exists
}

-- Event bus (pure Lua)
API._listeners = API._listeners or {}  -- event -> { fn1, fn2, ... }

-- Subscribe: returns an unsubscribe function
function API.On(event, fn)
  if type(event) ~= "string" or type(fn) ~= "function" then return function() end end
  API._listeners[event] = API._listeners[event] or {}
  table.insert(API._listeners[event], fn)

  local removed = false
  return function()
    if removed then return end
    removed = true
    local t = API._listeners[event]
    if not t then return end
    for i = #t, 1, -1 do
      if t[i] == fn then table.remove(t, i) break end
    end
  end
end

function API.Emit(event, payload)
  local t = API._listeners[event]
  if not t then return end
  -- pcall each listener so one bad addon doesn’t kill DP
  for i = 1, #t do
    local ok, err = pcall(t[i], payload)
    if not ok and DP.DebugPrint then
      DP:DebugPrint("API.Emit error for "..event..": "..tostring(err))
    end
  end
end

-- Safe getters (other addons should use these, not DeepPocketsDB raw)
function API.GetVersion() return DP.VERSION end
function API.Has(cap) return API.capabilities[cap] == true end

-- Core data accessors (these should be backed by your existing backend tables)
function API.GetDB()
  return DeepPocketsDB
end

-- Optional: Provenance passthrough (only if implemented)
function API.GetItemProvenance(itemID)
  if DP.GetItemProvenance then
    return DP:GetItemProvenance(itemID)
  end
  return "unknown"
end

-- Upgrade info passthrough pattern (plug in your existing upgrade logic)
-- Expected return: table or nil (don’t throw)
function API.GetUpgradeInfo(itemLinkOrID)
  if DP.GetUpgradeInfo then
    local ok, data = pcall(DP.GetUpgradeInfo, DP, itemLinkOrID)
    if ok then return data end
  end
  return nil
end

-- Notify helpers (call these from your existing scan/update code)
function API.NotifyScanComplete(summary)
  API.Emit("DP_SCAN_COMPLETE", summary or {})
end

function API.NotifyItemUpdated(info)
  API.Emit("DP_ITEM_UPDATED", info or {})
end

-- Minimal self-test
function DP:API_Sanity()
  print(("DeepPockets API OK v%s caps=%d"):format(API.GetVersion(), (function()
    local n=0; for _ in pairs(API.capabilities) do n=n+1 end; return n
  end)()))
end
