-- core/RotationDumpCommands.lua
local addonName, addonTable = ...
local Rot = addonTable.RotationDump

SLASH_SWROTDUMP1 = "/swrotdump"
SlashCmdList["SWROTDUMP"] = function(msg)
  if not Rot then Rot = addonTable.RotationDump end
  if Rot then
      Rot:ExportChunks(tonumber(msg) or 220)
  end
end
