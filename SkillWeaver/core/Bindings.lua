local SW = SkillWeaver
SW.Bindings = {}

_G.BINDING_HEADER_SKILLWEAVER = "SkillWeaver"
_G.BINDING_NAME_SKILLWEAVER_PRIMARY   = "Primary (ST)"
_G.BINDING_NAME_SKILLWEAVER_GROUPHEAL = "Group Heal (AOE/Heal)"
_G.BINDING_NAME_SKILLWEAVER_TANKSAVE  = "Tank Save (Utility)"
_G.BINDING_NAME_SKILLWEAVER_SELFSAVE  = "Self Save"
_G.BINDING_NAME_SKILLWEAVER_INT       = "Interrupt"
_G.BINDING_NAME_SKILLWEAVER_UTIL      = "Utility/Misc"


local function bindKey(key, buttonName)
  if not key or key == "" or not buttonName then return end
  SetBindingClick(key, buttonName, "LeftButton")
end

function SW.Bindings:Apply()
  -- clear old
  -- (optional) don’t ClearAllBindings(); just set yours explicitly.
  local st  = SW.SecureButtons:GetButtonName("ST")
  local aoe = SW.SecureButtons:GetButtonName("AOE")
  local intr= SW.SecureButtons:GetButtonName("INT")
  local util= SW.SecureButtons:GetButtonName("UTIL")
  local heal= SW.SecureButtons:GetButtonName("HEAL")
  local selfBtn = SW.SecureButtons:GetButtonName("SELF")

  bindKey(SkillWeaverDB.bindings.ST, st)
  bindKey(SkillWeaverDB.bindings.AOE, aoe)
  bindKey(SkillWeaverDB.bindings.INT, intr)
  bindKey(SkillWeaverDB.bindings.UTIL, util)
  bindKey(SkillWeaverDB.bindings.HEAL, heal)
  bindKey(SkillWeaverDB.bindings.SELF, selfBtn)

  SaveBindings(GetCurrentBindingSet())
end
