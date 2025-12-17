-- engine/UnitChain.lua
local UnitChain = {}

-- Prioritize self, then focus (tank), then party list
function UnitChain:Default()
  return { "player", "focus", "party1", "party2", "party3", "party4" }
end

-- Converts a list of units into a macro conditional string
-- Example: "[@player,help,nodead][@focus,help,nodead][@party1,help,nodead]..."
function UnitChain:ToMacroCond(units)
  local parts = {}
  units = units or self:Default()
  
  for _, u in ipairs(units) do
    parts[#parts+1] = ("[@%s,help,nodead]"):format(u)
  end
  
  -- Fallback to current target if it helps
  parts[#parts+1] = "[help,nodead]"
  
  return table.concat(parts, "")
end

return UnitChain
