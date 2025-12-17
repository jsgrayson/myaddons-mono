-- tools/SpellbookDump.lua
local addonName, addonTable = ...
local SpellbookDump = {}
addonTable.SpellbookDump = SpellbookDump

local function now() return (GetTime and GetTime()) or 0 end

local function getCDSeconds(spellID)
  if not GetSpellCooldown then return nil end
  local start, dur, enabled = GetSpellCooldown(spellID)
  if not enabled or enabled == 0 then return nil end
  if not start or start == 0 or not dur then return 0 end
  -- API gives current duration if on CD. If unavailable, returns 0.
  -- This is runtime data, best-effort.
  return dur or 0
end

local function getCharges(spellID)
  if not GetSpellCharges then return nil end
  local cur, maxCharges, start, dur = GetSpellCharges(spellID)
  if not maxCharges then return nil end
  return maxCharges
end

local function getPowerCosts(spellID)
  if not GetSpellPowerCost then return nil end
  local costs = GetSpellPowerCost(spellID)
  if type(costs) ~= "table" then return nil end
  local out = {}
  for _, c in ipairs(costs) do
    out[#out+1] = {
      type = c.type,
      cost = c.cost,
      name = c.name,
    }
  end
  return out
end

local function isPassive(spellID)
  if not IsPassiveSpell then return false end
  return IsPassiveSpell(spellID) == true
end

local function addSpell(spellID)
  local name = GetSpellInfo(spellID)
  if not name or name == "" then return end
  if isPassive(spellID) then return end
  
  if not SkillWeaver_SpellbookDump then SkillWeaver_SpellbookDump = { version=1, spells={} } end

  local entry = SkillWeaver_SpellbookDump.spells[name] or {}
  entry.id = spellID
  entry.name = name
  entry.t = now()

  -- Best-effort: cooldown/charges/power costs
  entry.charges = getCharges(spellID)
  entry.cooldown = getCDSeconds(spellID)
  entry.powerCost = getPowerCosts(spellID)

  SkillWeaver_SpellbookDump.spells[name] = entry
end

-- Scan the player's spellbook tabs
function SpellbookDump:ScanSpellbook()
  SkillWeaver_SpellbookDump = SkillWeaver_SpellbookDump or { version=1, spells={} }
  local total = 0

  if not GetNumSpellTabs or not GetSpellTabInfo then
    print("SkillWeaver: spellbook scan APIs unavailable.")
    return
  end

  local tabs = GetNumSpellTabs()
  for t=1, tabs do
    local _, _, offset, numSpells = GetSpellTabInfo(t)
    for i=1, numSpells do
      local index = offset + i
      local spellType, spellID = GetSpellBookItemInfo(index, "spell")
      if spellType == "SPELL" and spellID then
        addSpell(spellID)
        total = total + 1
      end
    end
  end

  print(("SkillWeaver: dumped %d spellbook entries. Use /swspellexport to print export chunks."):format(total))
end

-- Print as JSON-ish chunks (copy/paste)
function SpellbookDump:ExportChunks(chunkLen)
  chunkLen = chunkLen or 220
  SkillWeaver_SpellbookDump = SkillWeaver_SpellbookDump or { version=1, spells={} }

  -- Build a compact JSON string
  local parts = { "{\n" }
  local first = true
  
  -- Sort keys for deterministic output
  local keys = {}
  for k in pairs(SkillWeaver_SpellbookDump.spells) do keys[#keys+1] = k end
  table.sort(keys)

  for _, name in ipairs(keys) do
    local s = SkillWeaver_SpellbookDump.spells[name]
    if not first then parts[#parts+1] = ",\n" end
    first = false

    local function esc(x)
      x = tostring(x or "")
      x = x:gsub("\\","\\\\"):gsub("\"","\\\""):gsub("\n","\\n")
      return x
    end

    parts[#parts+1] = ('  "%s": {"id":%d,"cooldown":%s,"charges":%s}'):format(
      esc(name),
      tonumber(s.id or 0),
      (s.cooldown ~= nil) and tostring(s.cooldown) or "null",
      (s.charges ~= nil) and tostring(s.charges) or "null"
    )
  end
  parts[#parts+1] = "\n}\n"
  local raw = table.concat(parts)

  -- Chunk it for chat copy safety
  local total = math.ceil(#raw / chunkLen)
  print(("SkillWeaver: spell export %d chars in %d chunks. Copy all lines:"):format(#raw, total))

  for i=1, total do
    local a = (i-1)*chunkLen + 1
    local z = math.min(i*chunkLen, #raw)
    local piece = raw:sub(a, z)
    print(("SWSPELL_CHUNK|%d/%d|%s"):format(i, total, piece))
  end
end

return SpellbookDump
