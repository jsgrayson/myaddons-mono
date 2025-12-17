-- tools/SpellbookDumpV2.lua
local addonName, addonTable = ...
local DumpV2 = {}
addonTable.SpellbookDumpV2 = DumpV2

SkillWeaver_SpellbookDump = SkillWeaver_SpellbookDump or { version=2, spells={}, meta={} }

local function now() return (GetTime and GetTime()) or 0 end

local function safeSpellName(id)
  local name = GetSpellInfo and GetSpellInfo(id)
  return name
end

local function isPassiveSpellSafe(id)
  if IsPassiveSpell then return IsPassiveSpell(id) == true end
  return false
end

-- Prefer modern APIs when present (Dragonflight+)
local function getCooldownBaseSeconds(spellID)
  -- If you can access base cooldown directly, use it.
  if C_Spell and C_Spell.GetSpellCooldown then
    local cd = C_Spell.GetSpellCooldown(spellID)
    if cd and cd.duration then
      -- duration is current duration; base may be 0 if not on CD; still useful for "recently used" sampling
      return cd.duration
    end
  end

  if GetSpellCooldown then
    local start, dur, enabled = GetSpellCooldown(spellID)
    if not enabled or enabled == 0 then return nil end
    return dur or 0
  end

  return nil
end

local function getChargesMax(spellID)
  if C_Spell and C_Spell.GetSpellCharges then
    local ch = C_Spell.GetSpellCharges(spellID)
    if ch and ch.maxCharges then return ch.maxCharges end
  end
  if GetSpellCharges then
    local cur, maxCharges = GetSpellCharges(spellID)
    return maxCharges
  end
  return nil
end

local function getPowerCosts(spellID)
  -- best effort across clients
  if C_Spell and C_Spell.GetSpellPowerCost then
    local costs = C_Spell.GetSpellPowerCost(spellID)
    if type(costs) ~= "table" then return nil end
    local out = {}
    for _, c in ipairs(costs) do
      out[#out+1] = { type=c.type, cost=c.cost, name=c.name }
    end
    return out
  end

  if GetSpellPowerCost then
    local costs = GetSpellPowerCost(spellID)
    if type(costs) ~= "table" then return nil end
    local out = {}
    for _, c in ipairs(costs) do
      out[#out+1] = { type=c.type, cost=c.cost, name=c.name }
    end
    return out
  end

  return nil
end

local function isKnown(spellID)
  if C_Spell and C_Spell.IsSpellUsable then
    -- usable is not "known", but it’s a useful signal; keep it separate
    local usable, nomana = C_Spell.IsSpellUsable(spellID)
    return usable ~= nil
  end
  if IsPlayerSpell then return IsPlayerSpell(spellID) == true end
  if IsSpellKnown then return IsSpellKnown(spellID) == true end
  return nil
end

local function isTalentSpell(spellID)
  if IsTalentSpell then return IsTalentSpell(spellID) == true end
  return nil
end

-- ---- Tooltip scanning (optional) ----
-- This is lightweight: only for spells you exported, and only once per dump.
local scanner = CreateFrame("GameTooltip", "SkillWeaverSpellScanTooltip", UIParent, "GameTooltipTemplate")
scanner:SetOwner(UIParent, "ANCHOR_NONE")

local function tooltipLinesForSpellID(spellID)
  scanner:ClearLines()
  if scanner.SetSpellByID then
    scanner:SetSpellByID(spellID)
  elseif scanner.SetHyperlink then
    scanner:SetHyperlink(("spell:%d"):format(spellID))
  else
    return nil
  end

  local lines = {}
  for i=1, 32 do
    local left = _G["SkillWeaverSpellScanTooltipTextLeft"..i]
    if left then
      local txt = left:GetText()
      if txt and txt ~= "" then lines[#lines+1] = txt end
    end
  end
  return lines
end

local PROC_HINTS = {
  -- Add patterns as you discover them; keep generic.
  -- These do NOT need to be perfect; they’re hints for the offline autotagger.
  { proc = "Hot Streak", pattern = "Hot Streak" },
  { proc = "Brain Freeze", pattern = "Brain Freeze" },
  { proc = "Clearcasting", pattern = "Clearcasting" },
  { proc = "Killing Machine", pattern = "Killing Machine" },
  { proc = "Rime", pattern = "Rime" },
  { proc = "Sudden Doom", pattern = "Sudden Doom" },
}

local function inferProcLinksFromTooltip(lines)
  if not lines then return nil end
  local consumes = {}
  for _, l in ipairs(lines) do
    for _, hint in ipairs(PROC_HINTS) do
      if l:find(hint.pattern, 1, true) then
        consumes[#consumes+1] = hint.proc
      end
    end
  end
  if #consumes == 0 then return nil end
  return consumes
end

local function addSpell(spellID, doTooltip)
  local name = safeSpellName(spellID)
  if not name or name == "" then return false end
  if isPassiveSpellSafe(spellID) then return false end

  local entry = SkillWeaver_SpellbookDump.spells[name] or {}
  entry.id = spellID
  entry.name = name
  entry.t = now()

  entry.cooldown = getCooldownBaseSeconds(spellID)
  entry.charges = getChargesMax(spellID)
  entry.powerCost = getPowerCosts(spellID)

  entry.known = isKnown(spellID)
  entry.talent = isTalentSpell(spellID)

  if doTooltip then
    local lines = tooltipLinesForSpellID(spellID)
    entry.tooltipProcHints = inferProcLinksFromTooltip(lines) -- list of proc names (hints)
  end

  SkillWeaver_SpellbookDump.spells[name] = entry
  return true
end

function DumpV2:ScanSpellbook(opts)
  opts = opts or {}
  local doTooltip = opts.tooltip == true

  SkillWeaver_SpellbookDump = SkillWeaver_SpellbookDump or { version=2, spells={}, meta={} }
  SkillWeaver_SpellbookDump.version = 2
  SkillWeaver_SpellbookDump.meta = {
    t = now(),
    tooltip = doTooltip,
    client = (GetBuildInfo and select(1, GetBuildInfo())) or "unknown",
  }

  local total = 0
  if not GetNumSpellTabs or not GetSpellTabInfo or not GetSpellBookItemInfo then
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
        if addSpell(spellID, doTooltip) then
          total = total + 1
        end
      end
    end
  end

  print(("SkillWeaver: dumped %d spells (tooltipHints=%s). Use /swspellexport2."):format(
    total, doTooltip and "on" or "off"
  ))
end

function DumpV2:ExportChunks(chunkLen)
  chunkLen = chunkLen or 220
  SkillWeaver_SpellbookDump = SkillWeaver_SpellbookDump or { version=2, spells={}, meta={} }

  local function esc(x)
    x = tostring(x or "")
    x = x:gsub("\\","\\\\"):gsub("\"","\\\""):gsub("\n","\\n")
    return x
  end

  local parts = { "{\n" }
  parts[#parts+1] = ('  "__meta": {"version":%d,"t":%s,"tooltip":%s},\n'):format(
    tonumber(SkillWeaver_SpellbookDump.version or 2),
    tostring((SkillWeaver_SpellbookDump.meta and SkillWeaver_SpellbookDump.meta.t) or 0),
    ((SkillWeaver_SpellbookDump.meta and SkillWeaver_SpellbookDump.meta.tooltip) and "true" or "false")
  )

  local first = true
  parts[#parts+1] = '  "spells": {\n'
  
  -- Sort keys
  local keys = {}
  for k in pairs(SkillWeaver_SpellbookDump.spells) do keys[#keys+1] = k end
  table.sort(keys)
  
  for _, name in ipairs(keys) do
    local s = SkillWeaver_SpellbookDump.spells[name]
    if not first then parts[#parts+1] = ",\n" end
    first = false

    local hints = "null"
    if type(s.tooltipProcHints) == "table" and #s.tooltipProcHints > 0 then
      local hs = {}
      for i=1,#s.tooltipProcHints do hs[#hs+1] = '"'..esc(s.tooltipProcHints[i])..'"' end
      hints = "[" .. table.concat(hs, ",") .. "]"
    end

    parts[#parts+1] = ('    "%s": {"id":%d,"cooldown":%s,"charges":%s,"known":%s,"talent":%s,"procHints":%s}'):format(
      esc(name),
      tonumber(s.id or 0),
      (s.cooldown ~= nil) and tostring(s.cooldown) or "null",
      (s.charges ~= nil) and tostring(s.charges) or "null",
      (s.known ~= nil) and (s.known and "true" or "false") or "null",
      (s.talent ~= nil) and (s.talent and "true" or "false") or "null",
      hints
    )
  end
  parts[#parts+1] = "\n  }\n}\n"

  local raw = table.concat(parts)
  local total = math.ceil(#raw / chunkLen)
  print(("SkillWeaver: spelldump2 export %d chars in %d chunks. Copy all lines:"):format(#raw, total))
  for i=1, total do
    local a = (i-1)*chunkLen + 1
    local z = math.min(i*chunkLen, #raw)
    print(("SWSPELL2_CHUNK|%d/%d|%s"):format(i, total, raw:sub(a, z)))
  end
end

return DumpV2
