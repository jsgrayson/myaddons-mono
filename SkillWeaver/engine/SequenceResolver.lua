-- engine/SequenceResolver.lua
local addonName, addonTable = ...
local Resolver = {}
addonTable.SequenceResolver = Resolver

-- Standard content modes you care about (you can add "OpenWorld" etc.)
Resolver.modes = { "MythicPlus", "Raid", "Delves", "PvP" }

-- Fallback order for variants inside a mode
Resolver.variantFallback = function(requested)
  if requested == "HighPerformance" then
    return { "HighPerformance", "Balanced", "Safe" }
  elseif requested == "Balanced" then
    return { "Balanced", "Safe" }
  elseif requested == "Safe" then
    return { "Safe", "Balanced" }
  end
  return { requested, "Balanced", "Safe" }
end

-- Fallback order for "profile blocks" (like Midnight, San'layn)
Resolver.profileFallback = function(requestedProfile)
  if not requestedProfile then return {} end
  return { requestedProfile, "Midnight" }
end

local function hasLegacyVariant(specTable, modeName, variant)
  return type(specTable[modeName]) == "table"
     and type(specTable[modeName][variant]) == "table"
     and type(specTable[modeName][variant].steps) == "table"
     and #specTable[modeName][variant].steps > 0
end

local function hasProfile(specTable, profileName)
  local p = specTable[profileName]
  if type(p) ~= "table" then return false end
  if type(p.steps) == "table" and #p.steps > 0 then return true end
  if type(p.st) == "table" and #p.st > 0 then return true end
  if type(p.aoe) == "table" and #p.aoe > 0 then return true end
  return false
end

-- Returns:
--   profileName, variantName, rawProfileTableOrVariantTable, kind
-- kind = "profile" | "legacy"
function Resolver:Resolve(specTable, requestedMode, requestedVariant, requestedProfile)
  if type(specTable) ~= "table" then return nil end

  -- 1) If a named profile is requested (Midnight/San'layn/etc.), try it first.
  for _, prof in ipairs(self.profileFallback(requestedProfile)) do
    if hasProfile(specTable, prof) then
      return prof, nil, specTable[prof], "profile"
    end
  end

  -- 2) Try mode+variant (legacy)
  if requestedMode and type(specTable[requestedMode]) == "table" then
    for _, v in ipairs(self.variantFallback(requestedVariant or "Balanced")) do
      if hasLegacyVariant(specTable, requestedMode, v) then
        return requestedMode, v, specTable[requestedMode][v], "legacy"
      end
    end
  end

  -- 3) Try any known modes in priority order (Balanced then Safe)
  for _, m in ipairs(self.modes) do
    if type(specTable[m]) == "table" then
      for _, v in ipairs({ "Balanced", "HighPerformance", "Safe" }) do
        if hasLegacyVariant(specTable, m, v) then
          return m, v, specTable[m][v], "legacy"
        end
      end
    end
  end

  -- 4) Try Midnight as global profile fallback if it exists
  if hasProfile(specTable, "Midnight") then
    return "Midnight", nil, specTable["Midnight"], "profile"
  end

  -- 5) Last resort: first profile-ish table that looks runnable
  for k, v in pairs(specTable) do
    if hasProfile(specTable, k) then
      return k, nil, v, "profile"
    end
  end

  return nil
end

return Resolver
