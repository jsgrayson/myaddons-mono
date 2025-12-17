SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver

SW.SpecPackLoader = SW.SpecPackLoader or {}
local Loader = SW.SpecPackLoader

local MODES = { "Delves", "MythicPlus", "Raid", "PvP", "OpenWorld", "Midnight" }
local DEFAULT_PROFILES = { "Balanced", "HighPerformance", "Safe" }

local function normStepList(steps)
  if type(steps) ~= "table" then return {} end
  local out = {}
  for _, s in ipairs(steps) do
    if type(s) == "table" and type(s.command) == "string" and s.command ~= "" then
      table.insert(out, { command = s.command, conditions = s.conditions })
    end
  end
  return out
end

local function makeRotation(classSpecKey, mode, profileName)
  return {
    ST   = { steps = {} },
    AOE  = { steps = {} },
    INT  = { macro = SW.Defaults:GetDefaultInterruptMacro(classSpecKey) },
    UTIL = { macro = "" },
    meta = {
      name = profileName,
      mode = mode,
      spec = classSpecKey,
      version = 1,
    }
  }
end

-- Build from legacy profile object: { steps = {...} } optionally { aoeSteps = {...} } or { aoe = {...} }
local function buildFromLegacyProfile(classSpecKey, mode, profileName, profileObj)
  local rot = makeRotation(classSpecKey, mode, profileName)
  rot.ST.steps = normStepList(profileObj.steps)

  -- allow some legacy aliases
  local aoeCandidate =
    (type(profileObj.aoeSteps) == "table" and profileObj.aoeSteps) or
    (type(profileObj.aoe) == "table" and profileObj.aoe) or
    nil

  rot.AOE.steps = normStepList(aoeCandidate or profileObj.steps)

  -- optional overrides
  if type(profileObj.INT) == "table" and type(profileObj.INT.macro) == "string" then
    rot.INT.macro = profileObj.INT.macro
  end
  if type(profileObj.UTIL) == "table" and type(profileObj.UTIL.macro) == "string" then
    rot.UTIL.macro = profileObj.UTIL.macro
  end
  return rot
end

-- Build from priority format: { type="Priority", st={...}, aoe={...} }
local function buildFromPriority(classSpecKey, mode, profileName, block)
  local rot = makeRotation(classSpecKey, mode, profileName)
  rot.ST.steps = normStepList(block.st)
  rot.AOE.steps = normStepList((type(block.aoe) == "table" and #block.aoe > 0) and block.aoe or block.st)

  if type(block.INT) == "table" and type(block.INT.macro) == "string" then
    rot.INT.macro = block.INT.macro
  end
  if type(block.UTIL) == "table" and type(block.UTIL.macro) == "string" then
    rot.UTIL.macro = block.UTIL.macro
  end
  return rot
end

-- Build from already-normalized rotation: { ST=..., AOE=..., INT=..., UTIL=... }
local function buildFromNormalized(classSpecKey, mode, profileName, rotationObj)
  local rot = makeRotation(classSpecKey, mode, profileName)

  -- ST
  if type(rotationObj.ST) == "table" then
    rot.ST.macro = type(rotationObj.ST.macro) == "string" and rotationObj.ST.macro or nil
    rot.ST.steps = normStepList(rotationObj.ST.steps)
  end

  -- AOE
  if type(rotationObj.AOE) == "table" then
    rot.AOE.macro = type(rotationObj.AOE.macro) == "string" and rotationObj.AOE.macro or nil
    rot.AOE.steps = normStepList(rotationObj.AOE.steps)
  else
    rot.AOE.steps = rot.ST.steps
  end

  -- INT / UTIL
  if type(rotationObj.INT) == "table" and type(rotationObj.INT.macro) == "string" then
    rot.INT.macro = rotationObj.INT.macro
  end
  if type(rotationObj.UTIL) == "table" and type(rotationObj.UTIL.macro) == "string" then
    rot.UTIL.macro = rotationObj.UTIL.macro
  end

  return rot
end

local function detectAndBuild(classSpecKey, mode, profileName, obj)
  -- Case 1: already normalized rotation object
  if type(obj) == "table" and (obj.ST or obj.AOE or obj.INT or obj.UTIL) then
    return buildFromNormalized(classSpecKey, mode, profileName, obj)
  end

  -- Case 2: priority block
  if type(obj) == "table" and (obj.type == "Priority" or obj.st or obj.aoe) then
    return buildFromPriority(classSpecKey, mode, profileName, obj)
  end

  -- Case 3: legacy profile
  if type(obj) == "table" and type(obj.steps) == "table" then
    return buildFromLegacyProfile(classSpecKey, mode, profileName, obj)
  end

  return nil
end

function Loader:LoadClassPack(data)
  if type(data) ~= "table" then return end

  for classSpecKey, specTable in pairs(data) do
    if type(specTable) == "table" then

      -- If specTable itself is normalized (rare), register under Delves/Balanced
      if (specTable.ST or specTable.AOE or specTable.INT or specTable.UTIL) then
        local rot = buildFromNormalized(classSpecKey, "Delves", "Balanced", specTable)
        SW.Defaults:RegisterRotation(classSpecKey, "Delves", "Balanced", rot)
      end

      -- Modes: allow either "MythicPlus" tables, etc.
      for _, mode in ipairs(MODES) do
        local modeObj = specTable[mode]

        -- Special Midnight format: specTable.Midnight is usually a single block, not profiles
        if mode == "Midnight" and type(modeObj) == "table" then
          -- store it as Midnight/Priority unless it already contains profiles
          if modeObj.ST or modeObj.st or modeObj.type == "Priority" then
            local rot = detectAndBuild(classSpecKey, "Midnight", "Priority", modeObj)
            if rot then SW.Defaults:RegisterRotation(classSpecKey, "Midnight", "Priority", rot) end
          else
            -- if it has profiles, fall through below
          end
        end

        if type(modeObj) == "table" then
          -- If modeObj looks like a profile table (Balanced/Safe/HighPerformance)
          local anyProfileRegistered = false

          for profileName, profileObj in pairs(modeObj) do
            if type(profileObj) == "table" then
              local rot = detectAndBuild(classSpecKey, mode, profileName, profileObj)
              if rot then
                SW.Defaults:RegisterRotation(classSpecKey, mode, profileName, rot)
                anyProfileRegistered = true
              end
            end
          end

          -- If no explicit profiles exist but modeObj itself is a block, register as Balanced
          if not anyProfileRegistered then
            local rot = detectAndBuild(classSpecKey, mode, "Balanced", modeObj)
            if rot then
              SW.Defaults:RegisterRotation(classSpecKey, mode, "Balanced", rot)
            end
          end
        end
      end

      -- If a spec provides none of the known modes, default it into Delves/Balanced if possible
      -- (No extra work: above catches normalized and most common structures.)
    end
  end
end

-- Back-compat alias (older code might call this)
function Loader:LoadPackModule(data)
  return self:LoadClassPack(data)
end
