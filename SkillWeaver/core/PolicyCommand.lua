-- core/PolicyCommand.lua
local addonName, addonTable = ...

local PolicyManager = addonTable.PolicyManager
local Explain = addonTable.PolicyExplain
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")

local function currentSpecKey()
  return SkillWeaver:GetCurrentSpecKey()
end

local function dumpTable(t, indent, maxDepth)
  indent = indent or 0
  maxDepth = maxDepth or 4
  if maxDepth <= 0 then
    print(string.rep(" ", indent) .. "{...}")
    return
  end

  for k,v in pairs(t or {}) do
    if type(v) == "table" then
      print(string.rep(" ", indent) .. tostring(k) .. " = {")
      dumpTable(v, indent + 2, maxDepth - 1)
      print(string.rep(" ", indent) .. "}")
    else
      print(string.rep(" ", indent) .. tostring(k) .. " = " .. tostring(v))
    end
  end
end

-- Usage:
-- /swpolicy            -> prints merged policy (top-level)
-- /swpolicy why procs.Killing Machine
-- /swpolicy why cooldownSync.Pillar of Frost
SLASH_SWPOLICY1 = "/swpolicy"
SlashCmdList["SWPOLICY"] = function(msg)
  msg = msg or ""
  local specKey = currentSpecKey()
  if not specKey then
    print("SkillWeaver: unable to determine specKey.")
    return
  end
  
  -- Lazy load dependencies if needed
  if not PolicyManager then PolicyManager = addonTable.PolicyManager end
  if not Explain then Explain = addonTable.PolicyExplain end

  local args = {}
  for w in msg:gmatch("%S+") do args[#args+1] = w end

  if args[1] == "why" then
    local path = table.concat(args, " ", 2) -- Support spaces if any, though dots preferred
    if args[2] then path = args[2] end -- Actually strict arg 2 is better for dot notation
    
    local info = Explain:Why(specKey, path)
    Explain:PrintWhy(info)
    return
  end

  -- Default: show merged policy summary
  local p = PolicyManager:Get(specKey)
  print(("SWPOLICY %s (merged)"):format(specKey))
  dumpTable(p, 2, 5)
end

return SLASH_SWPOLICY1
