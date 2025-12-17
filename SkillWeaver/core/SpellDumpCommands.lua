-- core/SpellDumpCommands.lua
local addonName, addonTable = ...
local Dump = addonTable.SpellbookDump

SLASH_SWSPELLDUMP1 = "/swspelldump"
SlashCmdList["SWSPELLDUMP"] = function()
  if not Dump then Dump = addonTable.SpellbookDump end
  if Dump then Dump:ScanSpellbook() end
end

SLASH_SWSPELLEXPORT1 = "/swspellexport"
SlashCmdList["SWSPELLEXPORT"] = function(msg)
  if not Dump then Dump = addonTable.SpellbookDump end
  local n = tonumber(msg) or 220
  if Dump then Dump:ExportChunks(n) end
end
