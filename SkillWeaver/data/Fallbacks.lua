local SW = SkillWeaver
SW.Defaults = SW.Defaults or {}

SW.Defaults.registry = SW.Defaults.registry or {} -- registry[classSpecKey][mode][profile] = rotation

-- Reasonable interrupt defaults (you can expand this)
local defaultInterruptByClass = {
  WARRIOR = "/cast [harm] Pummel",
  ROGUE = "/cast [harm] Kick",
  DEATHKNIGHT = "/cast [harm] Mind Freeze",
  SHAMAN = "/cast [harm] Wind Shear",
  MAGE = "/cast [harm] Counterspell",
  WARLOCK = "/cast [harm] Spell Lock",
  HUNTER = "/cast [harm] Counter Shot",
  PALADIN = "/cast [harm] Rebuke",
  DRUID = "/cast [harm] Skull Bash",
  MONK = "/cast [harm] Spear Hand Strike",
  DEMONHUNTER = "/cast [harm] Disrupt",
  PRIEST = "/cast [harm] Silence",
  EVOKER = "/cast [harm] Quell",
}

local function getClassTokenFromKey(classSpecKey)
  -- key format: "CLASS_SPECID"
  return classSpecKey and classSpecKey:match("^([^_]+)_") or "UNKNOWN"
end

function SW.Defaults:GetDefaultInterruptMacro(classSpecKey)
  local class = getClassTokenFromKey(classSpecKey)
  return (defaultInterruptByClass[class] or "/stopcasting\n/cast [harm] Kick") .. "\n"
end

function SW.Defaults:RegisterRotation(classSpecKey, mode, profileName, rotation)
  if not classSpecKey or not mode or not profileName or not rotation then return end
  self.registry[classSpecKey] = self.registry[classSpecKey] or {}
  self.registry[classSpecKey][mode] = self.registry[classSpecKey][mode] or {}
  self.registry[classSpecKey][mode][profileName] = rotation
end

function SW.Defaults:GetFallbackRotation(classSpecKey, mode, profileName)
  local classBucket = self.registry[classSpecKey]
  if not classBucket then return nil end
  local modeBucket = classBucket[mode] or classBucket["Delves"] or classBucket["OpenWorld"]
  if not modeBucket then return nil end
  return modeBucket[profileName] or modeBucket["Balanced"] or nil
end
