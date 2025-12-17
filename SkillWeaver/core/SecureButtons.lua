local SW = SkillWeaver

SW.SecureButtons = {
  buttons = {},
}

local function createSecureButton(id)
  local name = "SkillWeaver_" .. id
  local b = CreateFrame("Button", name, UIParent, "SecureActionButtonTemplate")
  b:SetAttribute("type", "macro")
  b:SetAttribute("macrotext", "/startattack\n")
  b:Hide()
  return b
end

local function createAliasButton(aliasId, targetId)
  local name = "SkillWeaver_" .. aliasId
  local b = CreateFrame("Button", name, UIParent, "SecureActionButtonTemplate")
  b:SetAttribute("type", "click")
  b:SetAttribute("clickbutton", "SkillWeaver_" .. targetId)
  b:Hide()
  return b
end

function SW.SecureButtons:Init()
  -- Core buttons
  self.buttons.ST   = createSecureButton("ST")
  self.buttons.AOE  = createSecureButton("AOE")
  self.buttons.HEAL = createSecureButton("HEAL")
  self.buttons.SELF = createSecureButton("SELF")
  self.buttons.INT  = createSecureButton("INT")
  self.buttons.UTIL = createSecureButton("UTIL")

  -- Backward-compatible aliases
  self.buttons.Primary   = createAliasButton("Primary", "ST")
  self.buttons.GroupHeal = createAliasButton("GroupHeal", "HEAL")
  -- TankSave = UTIL (big external / utility)
  self.buttons.TankSave  = createAliasButton("TankSave", "UTIL")
  -- SelfSave = SELF (pure self-save only)
  self.buttons.SelfSave  = createAliasButton("SelfSave", "SELF")
end

function SW.SecureButtons:SetMacro(id, macroText)
  if InCombatLockdown() then return false end
  local b = self.buttons[id]
  if not b then return false end
  b:SetAttribute("macrotext", macroText or "")
  return true
end

function SW.SecureButtons:GetButtonName(id)
  local b = self.buttons[id]
  return b and b:GetName() or nil
end
