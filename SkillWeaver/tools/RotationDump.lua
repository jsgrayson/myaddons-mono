-- tools/RotationDump.lua
local addonName, addonTable = ...
local RotationDump = {}
addonTable.RotationDump = RotationDump

local function esc(s)
  s = tostring(s or "")
  s = s:gsub("\\","\\\\"):gsub("\"","\\\""):gsub("\n","\\n")
  return s
end

local function cleanSpell(cmd)
  if type(cmd) ~= "string" then return nil end
  -- match "/cast X" and "/cast [..] X"
  local spell = cmd:match("^%s*/cast%s+(.+)$")
  if not spell then return nil end
  spell = spell:gsub("^%s*%[[^%]]*%]%s*", "") -- strip leading [condition]
  spell = spell:gsub("%s*;.*$", "")          -- strip macro ; clause
  spell = spell:gsub("%s*$", "")
  -- strip trailing parenthetical notes
  spell = spell:gsub("%s*%b()%s*$", "")
  if spell == "" then return nil end
  return spell
end

local function addSpell(set, list, spell)
  if not spell or spell == "" then return end
  if not set[spell] then
    set[spell] = true
    list[#list+1] = spell
  end
end

-- Walk any sequence shape you support and collect spells from command fields
local function walkNode(node, set, list)
  if type(node) ~= "table" then return end

  -- legacy variant shape: { steps = { {command=...}, ... } }
  if type(node.steps) == "table" then
    for _, step in ipairs(node.steps) do
      if type(step) == "table" then
        addSpell(set, list, cleanSpell(step.command))
      end
    end
  end

  -- profile shape: { st={...}, aoe={...}, steps={...} }
  if type(node.st) == "table" then
    for _, step in ipairs(node.st) do
      if type(step) == "table" then
        addSpell(set, list, cleanSpell(step.command))
      end
    end
  end
  if type(node.aoe) == "table" then
    for _, step in ipairs(node.aoe) do
      if type(step) == "table" then
        addSpell(set, list, cleanSpell(step.command))
      end
    end
  end

  -- recurse into nested tables (safe guard against infinite loops by shallow heuristic)
  for k, v in pairs(node) do
    if type(v) == "table" and k ~= "__locks" then
      -- don't dive into a step table again (already handled)
      if k ~= "steps" and k ~= "st" and k ~= "aoe" then
        walkNode(v, set, list)
      end
    end
  end
end

-- Resource token hints (used by policy_autotag; not authoritative)
local function inferTokens(specKey)
  if type(specKey) ~= "string" then return { "MANA" } end
  if specKey:find("^DEATHKNIGHT_") then return { "RUNIC_POWER" } end
  if specKey:find("^DEMONHUNTER_") then return { "FURY" } end
  if specKey:find("^DRUID_") then return { "MANA", "ENERGY", "RAGE", "COMBO_POINTS", "ASTRAL_POWER" } end
  if specKey:find("^EVOKER_") then return { "MANA", "ESSENCE" } end
  if specKey:find("^HUNTER_") then return { "FOCUS" } end
  if specKey:find("^MAGE_") then return { "MANA", "ARCANE_CHARGES" } end
  if specKey:find("^MONK_") then return { "ENERGY", "CHI", "MANA" } end
  if specKey:find("^PALADIN_") then return { "MANA", "HOLY_POWER" } end
  if specKey:find("^PRIEST_") then return { "MANA", "INSANITY" } end
  if specKey:find("^ROGUE_") then return { "ENERGY", "COMBO_POINTS" } end
  if specKey:find("^SHAMAN_") then return { "MANA", "MAELSTROM" } end
  if specKey:find("^WARLOCK_") then return { "MANA", "SOUL_SHARDS" } end
  if specKey:find("^WARRIOR_") then return { "RAGE" } end
  return { "MANA" }
end

function RotationDump:BuildRotations()
  if not SkillWeaverDB or not SkillWeaverDB.Sequences then
    return nil, "SkillWeaverDB.Sequences not loaded"
  end

  local rotations = {}
  for specKey, specTable in pairs(SkillWeaverDB.Sequences) do
    if type(specKey) == "string" and type(specTable) == "table" then
      -- Export full data for offline defaults
      rotations[#rotations+1] = {
        specKey = specKey,
        data = specTable
      }
    end
  end

  table.sort(rotations, function(a,b) return a.specKey < b.specKey end)
  return rotations
end

function RotationDump:ExportChunks(chunkLen)
  chunkLen = tonumber(chunkLen) or 220

  local rotations, err = self:BuildRotations()
  if not rotations then
    print("SkillWeaver: rotdump failed: " .. tostring(err))
    return
  end

  -- JSON encode (simple + stable)
  local parts = { "[\n" }
  for i, r in ipairs(rotations) do
    -- Full export (raw data)
    local jsonStr = "null"
    if SkillWeaver and SkillWeaver.TableToJSON then
       jsonStr = SkillWeaver:TableToJSON(r.data)
    else
       -- Fallback: assumes helper exists or user accepts partial
       jsonStr = "{}" 
    end

    parts[#parts+1] = ('  {"specKey":"%s","data":%s'):format(esc(r.specKey), jsonStr)
    parts[#parts+1] = (i < #rotations) and "},\n" or "}\n"
  end
  parts[#parts+1] = "]\n"

  local raw = table.concat(parts)
  local total = math.ceil(#raw / chunkLen)
  print(("SkillWeaver: rotdump export %d specs, %d chars, %d chunks. Copy all lines:"):format(#rotations, #raw, total))

  for i=1, total do
    local a = (i-1)*chunkLen + 1
    local z = math.min(i*chunkLen, #raw)
    print(("SWROT_CHUNK|%d/%d|%s"):format(i, total, raw:sub(a, z)))
  end
end

return RotationDump
