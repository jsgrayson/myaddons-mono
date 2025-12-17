-- core/PolicyDiffCommand.lua
local addonName, addonTable = ...

local PolicyManager = addonTable.PolicyManager
local PolicySnapshot = addonTable.PolicySnapshot
local PolicyDiff = addonTable.PolicyDiff
local SpecRegistry = addonTable.SpecRegistry
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")

local function currentSpecKey()
  return SkillWeaver:GetCurrentSpecKey()
end

local function printLines(lines)
  for _, l in ipairs(lines) do print(l) end
end

local function specKeysAll()
  local keys = {}
  for _, specs in pairs(SpecRegistry) do
    if type(specs) == "table" then
      for _, meta in pairs(specs) do
        keys[#keys+1] = meta.key
      end
    end
  end
  table.sort(keys)
  return keys
end

SLASH_SWPOLICYDIFF1 = "/swpolicydiff"
SlashCmdList["SWPOLICYDIFF"] = function(msg)
  -- Lazy load
  if not PolicyManager then PolicyManager = addonTable.PolicyManager end
  if not PolicySnapshot then PolicySnapshot = addonTable.PolicySnapshot end
  if not PolicyDiff then PolicyDiff = addonTable.PolicyDiff end
  if not SpecRegistry then SpecRegistry = addonTable.SpecRegistry end
  
  msg = msg or ""
  local args = {}
  for w in msg:gmatch("%S+") do args[#args+1] = w end

  if args[1] == "save" then
    local specKey = currentSpecKey()
    if not specKey then print("SkillWeaver: no specKey."); return end
    local cur = PolicyManager:Get(specKey)
    PolicySnapshot:Set(specKey, cur)
    print("SkillWeaver: saved policy snapshot for " .. specKey)
    return
  end

  if args[1] == "all" then
    local changed = {}
    for _, specKey in ipairs(specKeysAll()) do
      local prev = PolicySnapshot:Get(specKey)
      local cur = PolicyManager:Get(specKey)
      if prev then
        local d = PolicyDiff:Compute(prev, cur)
        if (#d.added + #d.removed + #d.changed) > 0 then
          changed[#changed+1] = { specKey=specKey, n=(#d.added + #d.removed + #d.changed) }
        end
      end
    end

    if #changed == 0 then
      print("SkillWeaver: no policy diffs (or no snapshots saved). Use /swpolicydiff save on specs you care about.")
      return
    end

    table.sort(changed, function(a,b) return a.n > b.n end)
    print("SkillWeaver: policy diffs by spec:")
    for i=1, math.min(#changed, 30) do
      print(("  %s  (%d changes)"):format(changed[i].specKey, changed[i].n))
    end
    if #changed > 30 then print(("  ...and %d more"):format(#changed-30)) end
    return
  end

  -- default: diff current spec
  local specKey = currentSpecKey()
  if not specKey then print("SkillWeaver: no specKey."); return end

  local prev = PolicySnapshot:Get(specKey)
  if not prev then
    print("SkillWeaver: no snapshot for " .. specKey .. ". Use /swpolicydiff save first.")
    return
  end

  local cur = PolicyManager:Get(specKey)
  local d = PolicyDiff:Compute(prev, cur)
  print(("SkillWeaver: policy diff for %s"):format(specKey))
  printLines(PolicyDiff:Format(d, 40))
end
