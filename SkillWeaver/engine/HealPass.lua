-- engine/HealPass.lua
local UnitChain = require("engine.UnitChain")
local HealPass = {}

local function isHealerSpec(context)
  return context and context.role == "HEALER"
end

function HealPass:Run(context, canCastFn)
  local h = context.policy and (context.policy.healing or context.policy.supportHealing)
  if not h or h.enable == false then return nil end

  -- AoE first (no targeting needed, same for both modes)
  if context.groupInjuredCount and context.groupInjuredCount >= (h.aoeCount or 3) then
    for _, spell in ipairs(h.aoe or {}) do
      if canCastFn(spell, context) then
        return "/cast " .. spell
      end
    end
  end

  -- Unit Chain (Player -> Focus -> Party)
  local chain = h.unitChain or UnitChain:Default()

  -- Helper to find first available spell in a priority list
  local function findSpell(list)
    if not list then return nil end
    for _, spell in ipairs(list) do
      if canCastFn(spell, context) then return spell end
    end
    return nil
  end

  -- Select best spell (Emergency > Big > Filler)
  local spell = findSpell(h.emergency) or findSpell(h.big) or findSpell(h.filler)
  if not spell then return nil end

  -- Mode B: Hard Target (Toggle)
  -- Uses /target chain to simulate F1-F5 behavior, then restores target.
  if h.hardTarget then
      local tRules = {}
      for _, u in ipairs(chain) do
          -- /target accepts [cond] unit; [cond] unit...
          tRules[#tRules+1] = ("[@%s,help,nodead] %s"):format(u, u)
      end
      local targetBlock = table.concat(tRules, "; ")
      
      -- Note: /targetlasttarget handles restoring the previous target (enemy or friendly)
      return ("/target %s\n/cast %s\n/targetlasttarget"):format(targetBlock, spell)
  else
      -- Mode A: Secure Auto-Targeting (Default)
      -- Uses standard conditional macro, no target churn.
      local cond = UnitChain:ToMacroCond(chain)
      return ("/cast %s %s"):format(cond, spell)
  end
end

return HealPass
