-- engine/SpellValidator.lua
local SpellValidator = {}

local function getSpellId(spell)
  if type(spell) == "number" then return spell end
  if type(spell) ~= "string" then return nil end
  local _, _, _, _, _, _, id = GetSpellInfo(spell)
  if id then return id end
  return nil
end

local function isKnownSpellId(id)
  if not id then return false end
  if IsPlayerSpell and IsPlayerSpell(id) then return true end
  if IsSpellKnown and IsSpellKnown(id) then return true end
  if IsSpellKnownOrOverridesKnown and IsSpellKnownOrOverridesKnown(id) then return true end
  return false
end

local function isValidSpell(spell)
  if type(spell) == "number" or type(spell) == "string" then
    local name = GetSpellInfo(spell)
    return name ~= nil
  end
  return false
end

function SpellValidator:FilterKnown(spells)
  local out = {}
  for _, spell in ipairs(spells or {}) do
    if isValidSpell(spell) then
      local id = getSpellId(spell)
      if id == nil then
        -- can’t resolve id; keep (safer)
        out[#out+1] = spell
      else
        if isKnownSpellId(id) then
          out[#out+1] = spell
        end
      end
    end
  end
  return out
end

return SpellValidator
