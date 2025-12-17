local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local Split = {}
SkillWeaver.SectionSplit = Split

-- Very practical heuristics (edit these lists over time)
local interruptSpells = {
  ["Mind Freeze"]=true, ["Strangulate"]=true, ["Asphyxiate"]=true, ["Gnaw"]=true,
  ["Counterspell"]=true, ["Kick"]=true, ["Pummel"]=true, ["Rebuke"]=true, ["Solar Beam"]=true, 
  ["Spear Hand Strike"]=true, ["Wind Shear"]=true, ["Muzzle"]=true, ["Silence"]=true,
}

local defensiveSpells = {
  ["Icebound Fortitude"]=true, ["Anti-Magic Shell"]=true, ["Vampiric Blood"]=true,
  ["Rune Tap"]=true, ["Death Pact"]=true, ["Lichborne"]=true,
  ["Ice Block"]=true, ["Divine Shield"]=true, ["Cloak of Shadows"]=true, ["Turtle"]=true,
}

local cooldownSpells = {
  ["Dancing Rune Weapon"]=true, ["Pillar of Frost"]=true, ["Empower Rune Weapon"]=true,
  ["Dark Transformation"]=true, ["Apocalypse"]=true, ["Army of the Dead"]=true,
  ["Abomination Limb"]=true, ["Summon Gargoyle"]=true, ["Frostwyrm's Fury"]=true,
  ["Combustion"]=true, ["Icy Veins"]=true, ["Arcane Power"]=true, ["Avenging Wrath"]=true,
}

local function extractCastName(command)
  if type(command) ~= "string" then return nil end
  local body = command:gsub("^/cast%s+", "")
  body = body:gsub("^%b[]%s*", "")
  body = body:gsub("^%b[]%s*", "")
  body = body:gsub("%s*$", "")
  if body == "" then return nil end
  return body
end

local function bucketFor(step)
  local spell = extractCastName(step.command)
  if not spell then return "core" end

  if interruptSpells[spell] then return "interrupts" end
  if defensiveSpells[spell] then return "defensives" end
  if cooldownSpells[spell] then return "cooldowns" end

  -- Optional: if conditions include "should_interrupt", treat as interrupt even if spell unknown
  if type(step.conditions) == "string" and step.conditions:find("should_interrupt") then
    return "interrupts"
  end

  return "core"
end

function Split:FromBlocks(blocks)
  local sections = {
    interrupts = { st = {}, aoe = {} },
    defensives = { st = {}, aoe = {} },
    cooldowns  = { st = {}, aoe = {} },
    core       = { st = {}, aoe = {} },
    fillers    = { st = {}, aoe = {} },
  }

  for _, blockName in ipairs({ "st", "aoe" }) do
    for _, step in ipairs(blocks[blockName] or {}) do
      local b = bucketFor(step)
      table.insert(sections[b][blockName], step)
    end
  end

  return sections
end

return Split
