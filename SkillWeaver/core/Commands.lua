-- core/Commands.lua
local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local Trace = addonTable.DecisionTrace
local OverlayTrace = SkillWeaver.OverlayTrace

SLASH_SKILLWEAVERDEBUG1 = "/swdebug"
SlashCmdList["SKILLWEAVERDEBUG"] = function(msg)
  local n = tonumber(msg) or 0
  if not Trace then Trace = addonTable.DecisionTrace end
  if Trace then
      Trace:SetLevel(n)
      SkillWeaver:Print(("Debug level set to %d"):format(n))
  end
end

SLASH_SKILLWEAVERTRACE1 = "/swtrace"
SlashCmdList["SKILLWEAVERTRACE"] = function(msg)
  local n = tonumber(msg) or 12
  if not Trace then Trace = addonTable.DecisionTrace end
  if Trace then
      local items = Trace:Last(n)
      SkillWeaver:Print(("--- Trace (last %d) ---"):format(#items))
      for _, it in ipairs(items) do
        if it.kind == "chosen" then
          print(("[%0.2f] CHOSEN %s: %s"):format(it.t, it.section, it.command))
        else
          print(("[%0.2f] BLOCK  %s: %s  (%s)"):format(it.t, it.section, it.command, it.reason))
        end
      end
  end
end

SLASH_SWOVERLAY1 = "/swoverlay"
SlashCmdList["SWOVERLAY"] = function(msg)
    if not OverlayTrace then OverlayTrace = SkillWeaver.OverlayTrace end
    if OverlayTrace then
        OverlayTrace:Toggle()
    end
end

-- Snapshot / Replay Commands
SLASH_SWREC1="/swrec"
SlashCmdList["SWREC"]=function(msg)
  SkillWeaver_Record = SkillWeaver_Record or {}
  if msg == "1" then SkillWeaver_Record.enabled = true; SkillWeaver:Print("Recording ON")
  elseif msg == "0" then SkillWeaver_Record.enabled = false; SkillWeaver:Print("Recording OFF")
  else SkillWeaver:Print("Usage: /swrec 1|0") end
end

SLASH_SWCLEAR1="/swclear"
SlashCmdList["SWCLEAR"]=function()
  local Store = addonTable.SnapshotStore
  if Store then
      Store:Clear()
      SkillWeaver:Print("Snapshots cleared")
  end
end

SLASH_SWREPLAY1="/swreplay"
SlashCmdList["SWREPLAY"]=function(msg)
  local Replay = addonTable.ReplayContext
  if not Replay then return end
  if msg=="1" then Replay:Start("snapshots"); SkillWeaver:Print("Replay ON")
  elseif msg=="0" then Replay:Stop(); SkillWeaver:Print("Replay OFF")
  else SkillWeaver:Print("Usage: /swreplay 1|0") end
end

SLASH_SWCOUNT1="/swcount"
SlashCmdList["SWCOUNT"]=function()
  local Store = addonTable.SnapshotStore
  if Store then
      SkillWeaver:Print(("%d snapshots"):format(Store:Count()))
  end
end

-- Export / Import Commands
SLASH_SWEXPORT1="/swexport"
SlashCmdList["SWEXPORT"]=function(msg)
  local Export = addonTable.ReplayExport
  if not Export then return end
  local chunks, count = Export:MakeChunks(tonumber(msg) or 120, 220)
  print(("SkillWeaver: export %d snapshots in %d chunks. Copy lines below:"):format(count, #chunks))
  for _, line in ipairs(chunks) do
    print(line)
  end
end

SLASH_SWIMPORT1="/swimport"
SlashCmdList["SWIMPORT"]=function(msg)
  local Export = addonTable.ReplayExport
  if not Export then return end
  if Export:ImportLine(msg) then
    print("SkillWeaver: chunk accepted")
  else
    print("SkillWeaver: invalid chunk line")
  end
end

SLASH_SWIMPORTDONE1="/swimportdone"
SlashCmdList["SWIMPORTDONE"]=function()
  local Export = addonTable.ReplayExport
  if not Export then return end
  local raw, err = Export:FinalizeImport()
  if raw then
    print("SkillWeaver: import complete. Use /swreplay 1 to replay imported packet.")
    SkillWeaver_Replay = SkillWeaver_Replay or {}
    SkillWeaver_Replay.source = "packet"
  else
    print("SkillWeaver: import failed: "..tostring(err))
  end
end

        SkillWeaver:Print("Frost DK (251): |cff00ff00OK|r")
    else
        SkillWeaver:Print("Frost DK (251): |cffff0000MISSING|r")
    end
    
    -- Expand this to loop all Registry specs and check Sequences + Policies
    SkillWeaver:Print("--- End Coverage ---")
end

