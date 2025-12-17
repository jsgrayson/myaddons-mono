-- engine/Policies.lua
-- Handles loading and retrieving policy packs per spec.
local addonName, addonTable = ...
local Policies = {}
addonTable.Policies = Policies

-- If we load packs via TOC, they might register themselves into a global or addon table.
-- Let's assume packs register into addonTable.PolicyPacks[specKey]
addonTable.PolicyPacks = addonTable.PolicyPacks or {}

function Policies:Get(specKey)
    if not specKey then return nil end
    return addonTable.PolicyPacks[specKey]
end

-- Used by packs to register
function Policies:Register(specKey, pack)
    addonTable.PolicyPacks[specKey] = pack
end

return Policies
