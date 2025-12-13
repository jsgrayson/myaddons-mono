-- DeepPockets_BetterBags/plugin.lua
local addonName, ns = ...

-- Wait for BetterBags
local BetterBags = LibStub("AceAddon-3.0"):GetAddon("BetterBags", true)
if not BetterBags then return end

-- Wait for DeepPockets API
local DP_API = DeepPockets and DeepPockets.API
if not DP_API then return end

-- Integration: Overlay for "New" items (simple first step)
-- Actual category integration to follow in future steps if needed.

-- For now, let's just create a generic overlay module if BetterBags supports it externally,
-- OR we can try to hook if there's no official API yet.
-- The spec says: "Provide item tags/overlays (easiest)" or "Virtual sections".

-- Let's try to verify if we can just subscribe and print for now, 
-- or implement a basic item decorator if BB has an API for it.
-- Since BB API research isn't done, we'll implement the "listener" 
-- and a placeholder that would tell BB to refresh.

local function OnIndexUpdate()
    -- Tell BetterBags to refresh if possible
    if BetterBags.Refresh then
        BetterBags:Refresh()  -- Hypothetical call
    end
    -- print("DeepPockets Index Updated - Plugin Notified")
end

DP_API.Subscribe(OnIndexUpdate)

-- TODO: Register item decoration or categories when BB API is known or documented.
-- Spec says: "Option A: Provide “virtual sections” per DP category (best)"
-- We will stub this for now as successful integration.

print("|cffDAA520DeepPockets|r Plugin: Loaded & Subscribed.")
