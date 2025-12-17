-- Backend/Bridge.lua
SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver

SkillWeaverBackend = SkillWeaverBackend or {}

SkillWeaverCache = SkillWeaverCache or {
  rotations = {}, -- rotations[classSpecKey][ruleset][mode][profileName] = rotation
  builds = {},    -- builds[classSpecKey][ruleset][mode] = { talents=..., pvpTalents=..., notes=... }
  meta = {
    connected = false,
    ruleset = "TWW",  -- "TWW" (offline) or "MIDNIGHT" (connected)
    updatedAt = 0,
  },
}

-- Backend sets meta.connected/meta.ruleset/meta.updatedAt when it syncs
function SkillWeaverBackend:IsConnected()
  return SkillWeaverCache.meta.connected == true
end

function SkillWeaverBackend:GetRuleset()
  return SkillWeaverCache.meta.ruleset or "TWW"
end

function SkillWeaverBackend:SupportsMidnight()
  return self:IsConnected() and (self:GetRuleset() == "MIDNIGHT")
end

function SkillWeaverBackend:RequestSync(classSpecKey)
  SkillWeaverCache.meta.lastRequested = time()
end

-- NEW: ruleset-aware getters
function SkillWeaverBackend:GetRotation(classSpecKey, ruleset, mode, profileName)
  local r = SkillWeaverCache.rotations[classSpecKey]
  if not r then return nil end
  local rr = r[ruleset]
  if not rr then return nil end
  local rm = rr[mode]
  if not rm then return nil end
  return rm[profileName]
end

function SkillWeaverBackend:GetBuild(classSpecKey, ruleset, mode)
  local b = SkillWeaverCache.builds[classSpecKey]
  if not b then return nil end
  local br = b[ruleset]
  if not br then return nil end
  return br[mode]
end
