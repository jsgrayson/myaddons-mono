-- SkillWeaver Sequence Normalizer
-- Converts various sequence formats (Legacy, Priority-Profile) into the canonical runtime shape.

local Normalize = {}

local function isTable(t) return type(t) == "table" end

-- profileName examples: "MythicPlus", "Raid", "Delves", "PvP", "Midnight", "San'layn"
-- variant examples: "Balanced", "HighPerformance", "Safe" (legacy only)
function Normalize:One(specKey, specTable, profileName, variantName)
  local profile = specTable[profileName]
  if not isTable(profile) then return nil, "missing_profile" end

  -- Legacy: profile[variant].steps
  if variantName and isTable(profile[variantName]) and isTable(profile[variantName].steps) then
    return {
      meta = { key = specKey, profile = profileName, variant = variantName, exec = "Sequential" },
      blocks = { st = profile[variantName].steps, aoe = {} },
    }
  end

  -- Profile-style: { type="Priority", st=..., aoe=... } OR similar
  if isTable(profile) and (profile.type or profile.st or profile.aoe) then
    return {
      meta = { key = specKey, profile = profileName, variant = nil, exec = profile.type or "Priority" },
      blocks = { st = profile.st or {}, aoe = profile.aoe or {} },
    }
  end

  return nil, "unsupported_shape"
end

return Normalize
