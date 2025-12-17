local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local CCAuthority = {}
SkillWeaver.CCAuthority = CCAuthority

-- Tool ladder: order matters (cheap -> expensive)
-- type is used for DR groups (PvP) and for "don't waste" rules
CCAuthority.defaultKit = {
  { spell="Mind Freeze",  range=15, type="kick",        dr="none" },
  { spell="Strangulate",  range=30, type="silence",     dr="silence" },
  { spell="Asphyxiate",   range=20, type="stun",        dr="stun" },
  { spell="Gnaw",         range=30, type="pet_stun",    dr="stun", requiresPet=true },
  -- Add others for fallback
  { spell="Kick",         range=5,  type="kick",        dr="none" },
  { spell="Pummel",       range=5,  type="kick",        dr="none" },
  { spell="Rebuke",       range=5,  type="kick",        dr="none" },
  { spell="Wind Shear",   range=30, type="kick",        dr="none" },
  { spell="Counterspell", range=40, type="kick",        dr="none" },
  { spell="Hammer of Justice", range=10, type="stun",   dr="stun" },
  { spell="Kidney Shot",  range=5,  type="stun",        dr="stun" },
  { spell="Cheap Shot",   range=5,  type="stun",        dr="stun" },
  { spell="Blind",        range=15, type="disorient",   dr="disorient" },
}

-- thresholds (tune globally)
CCAuthority.defaults = {
  -- If kick will be ready within this time, WAIT instead of spending a stun
  waitForKickIfReadyIn = 0.6,

  -- If cast is about to finish, allow spending a stun even if kick soon
  emergencyRemaining = 0.3,

  -- PvP: don't use stun/silence into heavy DR unless emergency
  avoidDRAtOrAbove = 0.5, -- 0.0 = none, 0.5 = medium/high, 1.0 = full immune
}

local function cdRemaining(spell)
  if not GetSpellCooldown then return 0 end
  local start, dur, en = GetSpellCooldown(spell)
  if not en or en == 0 then return 999 end
  if not start or start == 0 or not dur then return 0 end
  local t = (start + dur) - (GetTime() or 0)
  if t < 0 then t = 0 end
  return t
end

local function inRange(spell, unit)
  if not IsSpellInRange then return true end
  local r = IsSpellInRange(spell, unit)
  if r == nil then return true end
  return r == 1
end

local function usable(tool, context, unit)
  if tool.requiresPet and not (context and context.petExists) then return false end
  if cdRemaining(tool.spell) > 0.1 then return false end -- Allow slight tolerance 0.1s? No, strict check better for deterministic.
  if not inRange(tool.spell, unit) then return false end
  return true
end

-- PvP DR lookup stub: context.dr[unit][drCategory] = 0..1
local function drValue(context, unit, drCat)
  if not context or not context.dr or not unit or not drCat or drCat == "none" then return 0 end
  local u = context.dr[unit]
  if not u then return 0 end
  return u[drCat] or 0
end

-- Main: choose the best control tool for this cast given cast timing + kick cooldown + DR
-- Inputs:
--  context.cast = { remaining=..., progress=..., spellID=..., ... }  (from your InterruptAuthority)
--  context.unit = "nameplateX" | "target"
function CCAuthority:Choose(context, rules)
  rules = rules or self.defaults
  context = context or {}

  local unit = context.unit or "target"
  local cast = context.cast
  if not cast then return nil end

  local kit = context.interruptKit or self.defaultKit

  -- Identify kick tool (first kick in kit)
  local kickSpell = nil
  for _, tool in ipairs(kit) do
    if tool.type == "kick" then kickSpell = tool.spell break end
  end

  local kickCD = kickSpell and cdRemaining(kickSpell) or 999
  local remaining = cast.remaining or 999

  -- If kick is coming up very soon, don't waste CC unless emergency
  local shouldWaitForKick =
    kickCD <= (rules.waitForKickIfReadyIn or 0) and remaining > (rules.emergencyRemaining or 0) and kickCD > 0

  -- Determine best tool in order
  for _, tool in ipairs(kit) do
    if usable(tool, context, unit) then
      -- If we should wait for kick, skip non-kick tools
      if shouldWaitForKick and tool.type ~= "kick" then
        -- Skip expensive tools if cheap kick is imminent
      else
          -- PvP DR avoidance (only for stun/silence families)
          local blockedByDR = false
          if context.isPvP and tool.dr and tool.dr ~= "none" then
            local dr = drValue(context, unit, tool.dr)
            if dr >= (rules.avoidDRAtOrAbove or 1) then
              -- allow if emergency (cast almost done)
              if remaining > (rules.emergencyRemaining or 0) then
                blockedByDR = true
              end
            end
          end

          if not blockedByDR then
              return {
                action = tool.spell,
                unit = unit,
                toolType = tool.type,
                dr = tool.dr,
                kickCD = kickCD,
                castRemaining = remaining,
              }
          end
      end
    end
  end

  return nil
end

return CCAuthority
