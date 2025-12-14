-- dp_ext/provenance.lua
-- Tracks item source (loot, quest, craft, vendor, mail, trade)

local ADDON = DeepPockets
DeepPocketsDB = DeepPocketsDB or {}
DeepPocketsDB.provenance = DeepPocketsDB.provenance or {}

local PROVENANCE = {
  LOOT   = "loot",
  QUEST  = "quest",
  CRAFT  = "craft",
  VENDOR = "vendor",
  MAIL   = "mail",
  TRADE  = "trade",
  OTHER  = "other",
}

-- temp session markers
local lastLoot = false
local lastQuest = false
local lastCraft = false
local lastVendor = false
local lastMail = false
local lastTrade = false

local function MarkItem(itemID)
  if not itemID then return end

  local src =
    lastLoot   and PROVENANCE.LOOT   or
    lastQuest  and PROVENANCE.QUEST  or
    lastCraft  and PROVENANCE.CRAFT  or
    lastVendor and PROVENANCE.VENDOR or
    lastMail   and PROVENANCE.MAIL   or
    lastTrade  and PROVENANCE.TRADE  or
    PROVENANCE.OTHER

  DeepPocketsDB.provenance[itemID] = src
end

-- Event frame (lightweight, no bag hooks)
local f = CreateFrame("Frame")

f:RegisterEvent("CHAT_MSG_LOOT")
f:RegisterEvent("QUEST_TURNED_IN")
f:RegisterEvent("TRADE_ACCEPT_UPDATE")
f:RegisterEvent("MAIL_INBOX_UPDATE")
f:RegisterEvent("MERCHANT_SHOW")
f:RegisterEvent("TRADE_SKILL_SHOW")
f:RegisterEvent("BAG_UPDATE_DELAYED")

f:SetScript("OnEvent", function(_, event, ...)
  if event == "CHAT_MSG_LOOT" then
    lastLoot = true
  elseif event == "QUEST_TURNED_IN" then
    lastQuest = true
  elseif event == "TRADE_SKILL_SHOW" then
    lastCraft = true
  elseif event == "MERCHANT_SHOW" then
    lastVendor = true
  elseif event == "MAIL_INBOX_UPDATE" then
    lastMail = true
  elseif event == "TRADE_ACCEPT_UPDATE" then
    lastTrade = true
  elseif event == "BAG_UPDATE_DELAYED" then
    -- scan just-added items
    for bag = 0, 4 do
      for slot = 1, C_Container.GetContainerNumSlots(bag) do
        local info = C_Container.GetContainerItemInfo(bag, slot)
        if info and info.isNewItem and info.itemID then
          MarkItem(info.itemID)
        end
      end
    end

    -- clear markers after processing
    lastLoot, lastQuest, lastCraft, lastVendor, lastMail, lastTrade =
      false, false, false, false, false, false
  end
end)

-- Public API
function ADDON:GetItemProvenance(itemID)
  return DeepPocketsDB.provenance[itemID] or "unknown"
end

-- Optional debug command
-- integrate into EXISTING /dp handler only
function ADDON:CmdProv(arg)
  local id = tonumber(arg)
  if not id then
    print("Usage: /dp prov <itemID>")
    return
  end
  print(("DeepPockets provenance: %s"):format(self:GetItemProvenance(id)))
end
