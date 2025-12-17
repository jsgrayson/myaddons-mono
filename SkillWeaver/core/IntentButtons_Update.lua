-- core/IntentButtons_Update.lua
local Buttons = require("core.BindableButtons") -- your 4 bindable secure buttons
local Profiles = require("policies.healing.SpecProfiles")
local HybridProfiles = require("policies.healing.HybridSupport")
local CastMacroBuilder = require("engine.CastMacroBuilder")

local function getSpecKey()
  -- Use SkillWeaver's existing method
  if SkillWeaver and SkillWeaver.GetCurrentSpecKey then
      return SkillWeaver:GetCurrentSpecKey()
  end
  return nil
end

local function setMacro(btn, macro)
  if not btn then return end
  btn:SetAttribute("type", "macro")
  btn:SetAttribute("macrotext", macro)
end

local pending = false

local function applyNow()
  pending = false
  local specKey = getSpecKey()
  if not specKey then return end
  
  local profile = Profiles[specKey]
  
  -- Fallback to Hybrid Support if enabled and not a main healer spec
  if not profile then
      if SkillWeaverDB and SkillWeaverDB.SupportHealsEnabled then
          profile = HybridProfiles[specKey]
      end
  end

  local mPrimary = CastMacroBuilder:BuildIntentMacro(profile, "PRIMARY", specKey)
  local mGroup   = CastMacroBuilder:BuildIntentMacro(profile, "GROUP", specKey)
  local mTank    = CastMacroBuilder:BuildIntentMacro(profile, "TANK", specKey)
  local mSelf    = CastMacroBuilder:BuildIntentMacro(profile, "SELF", specKey)

  setMacro(Buttons.Primary,   mPrimary)
  setMacro(Buttons.GroupHeal, mGroup)
  setMacro(Buttons.TankSave,  mTank)
  setMacro(Buttons.SelfSave,  mSelf)

  if SkillWeaver and SkillWeaver.Print then
      -- SkillWeaver:Print("Updated intent macros for " .. tostring(specKey))
  end
end

-- Public API
function SkillWeaver:ApplyIntentMacros()
    if InCombatLockdown() then 
        pending = true
        return 
    end
    applyNow()
end

function SkillWeaver:RequestIntentMacroRefresh()
    self:ApplyIntentMacros()
end

local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_ENTERING_WORLD")
f:RegisterEvent("PLAYER_SPECIALIZATION_CHANGED")
f:RegisterEvent("PLAYER_REGEN_DISABLED")
f:RegisterEvent("PLAYER_REGEN_ENABLED")
-- Listen for learned spells to update pruning
f:RegisterEvent("LEARNED_SPELL_IN_TAB") 
f:RegisterEvent("TRAIT_CONFIG_UPDATED") -- Talents changed

f:SetScript("OnEvent", function(_, event)
  if event == "PLAYER_REGEN_DISABLED" then
    pending = true
    return
  end
  SkillWeaver:RequestIntentMacroRefresh()
end)

-- Defer handling
f:HookScript("OnEvent", function(_, event)
  if event == "PLAYER_REGEN_ENABLED" and pending then
     SkillWeaver:ApplyIntentMacros()
  end
end)
