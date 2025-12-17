-- core/ExportUICommand.lua
local addonName, addonTable = ...
local ExportPanel = addonTable.ExportPanel

SLASH_SWEXPORTUI1 = "/swexportui"
SlashCmdList["SWEXPORTUI"] = function()
  if not ExportPanel then ExportPanel = addonTable.ExportPanel end
  if ExportPanel then
      ExportPanel:Toggle()
  end
end
