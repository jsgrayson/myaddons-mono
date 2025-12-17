-- core/PolicyUICommand.lua
local addonName, addonTable = ...
local Panel = addonTable.PolicyPanel

SLASH_SWPOLICYUI1 = "/swpolicyui"
SlashCmdList["SWPOLICYUI"] = function(msg)
  if not Panel then Panel = addonTable.PolicyPanel end
  if Panel then
      Panel:Create()
      local shown = Panel.frame and Panel.frame:IsShown()
      Panel:SetShown(not shown)
  else
      print("SkillWeaver: PolicyPanel not loaded.")
  end
end
