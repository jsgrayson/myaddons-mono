-- core/CoverageCommand.lua
local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")

local SpecRegistry = addonTable.SpecRegistry

local function countSteps(tbl)
  if type(tbl) ~= "table" then return 0 end
  if type(tbl.steps) == "table" then return #tbl.steps end
  local n = 0
  if type(tbl.st) == "table" then n = n + #tbl.st end
  if type(tbl.aoe) == "table" then n = n + #tbl.aoe end
  return n
end

local function hasLegacy(specTable, mode, variant)
  return type(specTable[mode]) == "table"
     and type(specTable[mode][variant]) == "table"
     and type(specTable[mode][variant].steps) == "table"
     and #specTable[mode][variant].steps > 0
end

local function hasProfile(specTable, name)
  local p = specTable[name]
  return countSteps(p) > 0
end

local function modesLine(specTable)
  local modes = { "MythicPlus", "Raid", "Delves", "PvP" }
  local variants = { "Balanced", "HighPerformance", "Safe" }

  local out = {}
  for _, m in ipairs(modes) do
    local vhit = {}
    for _, v in ipairs(variants) do
      if hasLegacy(specTable, m, v) then vhit[#vhit+1] = v:sub(1,1) end
    end
    if #vhit > 0 then
      out[#out+1] = (m .. "[" .. table.concat(vhit, "") .. "]")
    else
      out[#out+1] = (m .. "[-]")
    end
  end
  return table.concat(out, "  ")
end

local function profilesLine(specTable)
  local candidates = { "Midnight" } -- extend if you standardize more profile names
  local found = {}
  for _, p in ipairs(candidates) do
    if hasProfile(specTable, p) then found[#found+1] = p end
  end
  if #found == 0 then return "profiles: none" end
  return "profiles: " .. table.concat(found, ", ")
end

SLASH_SWCOVERAGE1 = "/swcoverage"
SlashCmdList["SWCOVERAGE"] = function()
  if not SkillWeaver.db or not SkillWeaver.db.profile or not SkillWeaver.db.profile.sequences then
    -- Checking global SkillWeaverDB directly if preferred, but Ace3 db is safer
    if not SkillWeaverDB or not SkillWeaverDB.Sequences then
        SkillWeaver:Print("No SkillWeaverDB.Sequences loaded.")
        return
    end
  end
  
  -- Use global for now as architecture implies SkillWeaverDB.Sequences stores sequences by key
  local seqDB = SkillWeaverDB.Sequences

  local total, missing = 0, 0

  if not SpecRegistry then SpecRegistry = addonTable.SpecRegistry end
  if not SpecRegistry then SkillWeaver:Print("Registry not found"); return end

  for className, specs in pairs(SpecRegistry) do
    if className ~= "Get" then -- Skip methods
    for specID, meta in pairs(specs) do
      total = total + 1
      local specKey = meta.key
      local specTable = seqDB[specKey]

      if type(specTable) ~= "table" then
        missing = missing + 1
        -- print(("MISSING %s (%s %d) - no sequences table"):format(specKey, className, specID))
      else
        local ok = false
        -- “covered” if any mode+variant or a profile exists with steps
        if hasLegacy(specTable, "MythicPlus", "Balanced")
          or hasLegacy(specTable, "Raid", "Balanced")
          or hasLegacy(specTable, "Delves", "Balanced")
          or hasLegacy(specTable, "PvP", "Balanced")
          or hasProfile(specTable, "Midnight")
        then
          ok = true
        end

        if not ok then
          missing = missing + 1
          print(("INCOMPLETE %s (%s %d) - no runnable defaults"):format(specKey, className, specID))
        end

        print(("%s — %s/%s (%s)  %s  |  %s"):format(
          specKey, className, meta.name, meta.role or "?",
          modesLine(specTable),
          profilesLine(specTable)
        ))
      end
    end
    end
  end

  print(("SkillWeaver coverage: %d specs total, %d missing/incomplete"):format(total, missing))
  print(("Policies Loaded: %d"):format((addonTable.PolicyPacks and #addonTable.PolicyPacks) or 0))
  if addonTable.PolicyPacks then
      local count = 0
      for k,v in pairs(addonTable.PolicyPacks) do count = count + 1 end
      print("Total Policy Packs: "..count)
  end
end
