-- policies/PolicyExplain.lua
local addonName, addonTable = ...
local Explain = {}
addonTable.PolicyExplain = Explain

local function isTable(x) return type(x) == "table" end

local function deepCopy(t)
  if not isTable(t) then return t end
  local out = {}
  for k,v in pairs(t) do out[k] = deepCopy(v) end
  return out
end

-- Adapt getAtPath to handle deep indexing
local function getAtPath(t, path)
  if not t then return nil end
  if not path or path == "" then return t end
  local cur = t
  for key in path:gmatch("[^%.]+") do
    if not isTable(cur) then return nil end
    cur = cur[key]
  end
  return cur
end

local function lockCheck(manual, path)
  local locks = manual and manual.__locks
  if not isTable(locks) then return false end

  -- section lock: "cooldownSync"
  local section = path:match("^[^%.]+")
  local rest = path:match("^[^%.]+%.(.+)$")
  
  -- If checking root, return false
  if not section then return false end

  if locks[section] == true then return true end
  if isTable(locks[section]) and rest then
    -- lock specific subkey: section["Key"]
    -- we only support one subkey level for clarity: "procs.Killing Machine"
    local sub = rest:match("^[^%.]+")
    if locks[section][sub] == true then return true end
  end
  return false
end

-- Builds a "why map" for a given path (or for the whole policy if path is nil)
function Explain:Why(specKey, path)
  -- Use addonTable storage
  local defaults = addonTable.PolicyManager.defaults
  local gen = addonTable.PolicyPacksGen[specKey] or {}
  local manual = addonTable.PolicyPacksManual[specKey] or {}

  local out = {
    specKey = specKey,
    path = path or "",
    locked = path and lockCheck(manual, path) or false,
    default = deepCopy(getAtPath(defaults, path)),
    gen = deepCopy(getAtPath(gen, path)),
    manual = deepCopy(getAtPath(manual, path)),
  }

  return out
end

-- Pretty print (small, chat-friendly)
function Explain:PrintWhy(info)
  local function fmt(v)
    if isTable(v) then return "{...}" end
    if v == nil then return "nil" end
    if type(v) == "boolean" then return v and "true" or "false" end
    return tostring(v)
  end

  print(("SWPOLICY WHY %s  path='%s'  locked=%s"):format(
    info.specKey, info.path, info.locked and "true" or "false"
  ))
  print(("  default: %s"):format(fmt(info.default)))
  print(("  gen:     %s"):format(fmt(info.gen)))
  print(("  manual:  %s"):format(fmt(info.manual)))
end

return Explain
