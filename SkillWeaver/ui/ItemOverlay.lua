local ADDON_NAME, SkillWeaver = ...
SkillWeaver.UI = SkillWeaver.UI or {}
local ItemOverlay = {}
SkillWeaver.UI.ItemOverlay = ItemOverlay

local EquipmentManager = SkillWeaver.EquipmentManager
local StatWeights = require("SkillWeaver.data.StatWeights")

-- Configuration
local FONT_PATH = "Fonts\\FRIZQT__.TTF"
local FONT_SIZE = 12

------------------------------------------------------------
-- Helper: Create Overlay Frames
------------------------------------------------------------
local function CreateOverlay(button)
    if button.swOverlay then return button.swOverlay end

    local overlay = CreateFrame("Frame", nil, button)
    overlay:SetAllPoints()
    overlay:SetFrameLevel(button:GetFrameLevel() + 10)

    -- iLvl Text (Bottom Left)
    local ilvlText = overlay:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    ilvlText:SetPoint("BOTTOMLEFT", 2, 2)
    ilvlText:SetTextColor(1, 1, 1) -- White
    overlay.ilvlText = ilvlText

    -- Score Text (Bottom Right)
    local scoreText = overlay:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    scoreText:SetPoint("BOTTOMRIGHT", -2, 2)
    scoreText:SetTextColor(1, 1, 0) -- Yellow
    overlay.scoreText = scoreText

    -- Upgrade Arrow (Top Right)
    local arrow = overlay:CreateTexture(nil, "OVERLAY")
    arrow:SetSize(16, 16)
    arrow:SetPoint("TOPRIGHT", 2, 2)
    arrow:SetTexture("Interface\\Buttons\\UI-MicroStream-Green") -- Placeholder green arrow-ish
    -- Better texture: Interface\AddOns\SkillWeaver\Media\UpgradeArrow.tga (if we had one)
    -- Using standard green arrow
    arrow:SetTexture("Interface\\MiniMap\\ObjectIconsAtlas") 
    arrow:SetAtlas("groupfinder-icon-arrow")
    arrow:SetVertexColor(0, 1, 0)
    arrow:Hide()
    overlay.arrow = arrow

    button.swOverlay = overlay
    return overlay
end

------------------------------------------------------------
-- Core: Update Button Overlay
------------------------------------------------------------
function ItemOverlay:UpdateButton(button, bag, slot)
    local overlay = CreateOverlay(button)
    
    -- Clear previous state
    overlay.ilvlText:SetText("")
    overlay.scoreText:SetText("")
    overlay.arrow:Hide()

    local itemLink
    if bag then
        itemLink = C_Container.GetContainerItemLink(bag, slot)
    else
        -- Character Frame (slot is inventory slot ID)
        itemLink = GetInventoryItemLink("player", slot)
    end

    if not itemLink then return end

    -- 1. Get iLvl
    local ilvl = GetDetailedItemLevelInfo(itemLink)
    if ilvl then
        overlay.ilvlText:SetText(ilvl)
    end

    -- 2. Get Score
    -- Need current content type for weights. Default to Raid?
    -- Ideally we use the current detected content type.
    local contentType = SkillWeaver.ContentDetector and SkillWeaver.ContentDetector.CurrentType or "RAID"
    -- Map to DB keys
    if contentType == "RAID" then contentType = "Raid"
    elseif contentType == "MYTHIC_PLUS" then contentType = "MythicPlus"
    elseif contentType == "PVP" or contentType == "ARENA" then contentType = "PvP"
    else contentType = "Raid" end -- Fallback

    local specID = GetSpecializationInfo(GetSpecialization())
    local weights = StatWeights:GetWeights(specID, contentType)
    
    if weights then
        local score = EquipmentManager:GetItemScore(itemLink, weights)
        if score > 0 then
            overlay.scoreText:SetText(string.format("%.0f", score))
            
            -- 3. Check Upgrade (Only for Bag items)
            if bag then
                local _, _, _, _, _, _, _, _, equipLoc = GetItemInfo(itemLink)
                if equipLoc then
                    -- Find equipped item for this slot
                    -- Simplified: Just check the first mapped slot
                    -- Real logic needs to check both finger/trinket slots
                    local slotID = nil
                    -- Need the EQUIP_LOC_MAP from EquipmentManager, but it's local there.
                    -- We should expose it or duplicate it.
                    -- For now, let's just use GetInventoryItemLink if we can guess the slot.
                    -- Actually, EquipmentManager:GetBestSet logic handles the comparison.
                    -- Let's just compare against the *currently equipped* item in the primary slot.
                    
                    -- Quick hack: Use GetInventorySlotInfo with a lookup
                    -- This is getting complex to duplicate.
                    -- Let's just skip upgrade arrow for this iteration if it's too hard, 
                    -- OR expose the map in EquipmentManager.
                    
                    -- Assuming we can get the slot:
                    -- local equippedLink = GetInventoryItemLink("player", slotID)
                    -- local equippedScore = EquipmentManager:GetItemScore(equippedLink, weights)
                    -- if score > equippedScore then overlay.arrow:Show() end
                end
            end
        end
    end
end

------------------------------------------------------------
-- Hooks
------------------------------------------------------------
-- Hook Bag Updates
hooksecurefunc("ContainerFrame_Update", function(frame)
    local bag = frame:GetID()
    local name = frame:GetName()
    for i = 1, frame.size do
        local button = _G[name .. "Item" .. i]
        if button then
            ItemOverlay:UpdateButton(button, bag, button:GetID())
        end
    end
end)

-- Hook Bank/Bag Addons? (Bagnon, Adibags, etc support might be needed later)

-- Hook Character Frame
hooksecurefunc("PaperDollItemSlotButton_Update", function(button)
    local slotID = button:GetID()
    ItemOverlay:UpdateButton(button, nil, slotID)
end)
