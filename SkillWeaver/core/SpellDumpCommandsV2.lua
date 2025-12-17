-- core/SpellDumpCommandsV2.lua
local addonName, addonTable = ...
local DumpV2 = addonTable.SpellbookDumpV2

SLASH_SWSPELLDUMP2_1 = "/swspelldump2"
SlashCmdList["SWSPELLDUMP2_"] = function(msg)
  if not DumpV2 then DumpV2 = addonTable.SpellbookDumpV2 end
  if DumpV2 then
     msg = msg or ""
     local tooltip = (msg == "tooltip" or msg == "1")
     DumpV2:ScanSpellbook({ tooltip = tooltip })
  end
end

SLASH_SWSPELLEXPORT2_1 = "/swspellexport2"
SlashCmdList["SWSPELLEXPORT2_"] = function(msg)
  if not DumpV2 then DumpV2 = addonTable.SpellbookDumpV2 end
  if DumpV2 then
      local n = tonumber(msg) or 220
      DumpV2:ExportChunks(n)
  end
end
