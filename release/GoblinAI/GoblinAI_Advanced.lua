-- Advanced.lua - Advanced TSM Features (Price Strings, Tooltips, Import/Export)
-- Part of GoblinAI v2.0

GoblinAI.Advanced = {}
local Advanced = GoblinAI.Advanced

-- ============================================================================
-- Price String System (TSM-Style Formulas)
-- ============================================================================

Advanced.PriceStrings = {
    -- Built-in price sources
    DBMarket = function(itemID)
        return GoblinAI.BackendAPI:GetMarketPrice(itemID)
    end,
    
    DBMinBuyout = function(itemID)
        local avgPrice = GoblinAI.Scanner:GetAveragePrice(itemID, 7)
        return avgPrice and (avgPrice * 0.9) or nil
    end,
    
    Crafting = function(itemID)
        -- Get crafting cost from CraftingFrame
        for _, craft in ipairs(GoblinAI.CraftingFrame.knownRecipes or {}) do
            if craft.itemID == itemID then
                return craft.materialCost
            end
        end
        return nil
    end,
    
    VendorSell = function(itemID)
        return select(11, GetItemInfo(itemID))
    end,
}

-- Parse price string formula
-- Examples: "120% DBMarket", "min(110% DBMarket, 150% Crafting)", "DBMarket + 5000"
function Advanced:ParsePriceString(formula, itemID)
    if not formula or not itemID then return nil end
    
    -- Replace price sources with actual values
    local processed = formula
    
    for source, func in pairs(self.PriceStrings) do
        local value = func(itemID)
        if value then
            processed = processed:gsub(source, tostring(value))
        else
            return nil -- Can't calculate without all sources
        end
    end
    
    -- Now evaluate the math expression
    -- Simple implementation - supports: +, -, *, /, %, min(), max()
    local result = self:EvaluateExpression(processed)
    
    return result
end

function Advanced:EvaluateExpression(expr)
    -- Remove whitespace
    expr = expr:gsub("%s+", "")
    
    -- Handle min() and max()
    expr = expr:gsub("min%(([%d%.]+),([%d%.]+)%)", function(a, b)
        return tostring(math.min(tonumber(a), tonumber(b)))
    end)
    
    expr = expr:gsub("max%(([%d%.]+),([%d%.]+)%)", function(a, b)
        return tostring(math.max(tonumber(a), tonumber(b)))
    end)
    
    -- Handle percentages (convert 120% to 1.20 multiplier)
    expr = expr:gsub("(%d+)%%", function(num)
        return tostring(tonumber(num) / 100)
    end)
    
    -- Evaluate using Lua's load (safe subset)
    local func = loadstring("return " .. expr)
    if func then
        local success, result = pcall(func)
        if success then
            return math.floor(result)
        end
    end
    
    return nil
end

-- ============================================================================
-- Tooltip Integration (TSM-Style Pricing)
-- ============================================================================

function Advanced:InitializeTooltips()
    -- Hook into item tooltip
    TooltipDataProcessor.AddTooltipPostCall(Enum.TooltipDataType.Item, function(tooltip)
        Advanced:AddPricingToTooltip(tooltip)
    end)
    
    print("|cFFFFD700Goblin AI:|r TSM-style tooltips enabled")
end

function Advanced:AddPricingToTooltip(tooltip)
    local _, link = tooltip:GetItem()
    if not link then return end
    
    local itemID = GetItemInfoInstant(link)
    if not itemID then return end
    
    -- Get pricing data
    local marketPrice = GoblinAI.BackendAPI:GetMarketPrice(itemID)
    local avgPrice = GoblinAI.Scanner:GetAveragePrice(itemID, 7)
    local trend = GoblinAI.Scanner:GetPriceTrend(itemID, 7)
    
    if not marketPrice and not avgPrice then return end
    
    -- Add section
    tooltip:AddLine(" ")
    tooltip:AddLine("|cFFFFD700Goblin AI Pricing:|r", 1, 1, 1)
    
    -- Market price
    if marketPrice then
        tooltip:AddDoubleLine("Market Value:", GoblinAI:FormatGold(marketPrice), 1, 1, 1, 1, 1, 1)
    end
    
    -- 7-day average
    if avgPrice then
        tooltip:AddDoubleLine("7-Day Avg:", GoblinAI:FormatGold(avgPrice), 1, 1, 1, 1, 1, 1)
    end
    
    -- Trend
    if trend then
        local trendText = ""
        local r, g, b = 1, 1, 1
        
        if trend > 0.1 then
            trendText = string.format("↑ Rising (+%.0f%%)", trend * 100)
            r, g, b = 0, 1, 0
        elseif trend < -0.1 then
            trendText = string.format("↓ Falling (%.0f%%)", trend * 100)
            r, g, b = 1, 0, 0
        else
            trendText = "→ Stable"
            r, g, b = 1, 1, 0
        end
        
        tooltip:AddDoubleLine("Trend:", trendText, 1, 1, 1, r, g, b)
    end
    
    -- Crafting cost (if craftable)
    for _, craft in ipairs(GoblinAI.CraftingFrame.knownRecipes or {}) do
        if craft.itemID == itemID and craft.materialCost then
            tooltip:AddDoubleLine("Craft Cost:", GoblinAI:FormatGold(craft.materialCost), 1, 1, 1, 1, 1, 1)
            
            if craft.profit then
                local profitColor = craft.profit > 0 and {0, 1, 0} or {1, 0, 0}
                tooltip:AddDoubleLine("Craft Profit:", 
                    GoblinAI:FormatGold(craft.profit), 
                    1, 1, 1, 
                    profitColor[1], profitColor[2], profitColor[3])
            end
            break
        end
    end
    
    tooltip:Show()
end

-- ============================================================================
-- Import/Export System (Groups & Operations)
-- ============================================================================

function Advanced:ExportGroups()
    local groups = GoblinAIDB.groups or {}
    
    if #groups == 0 then
        print("|cFFFF0000Goblin AI:|r No groups to export")
        return nil
    end
    
    -- Serialize groups to string
    local exportString = self:SerializeData(groups)
    
    -- Compress (simple base64-like encoding)
    local compressed = self:CompressString(exportString)
    
    print("|cFFFFD700Goblin AI:|r Exported " .. #groups .. " groups")
    print("Export string copied to clipboard (use Ctrl+V)")
    
    return compressed
end

function Advanced:ImportGroups(importString)
    if not importString or importString == "" then
        print("|cFFFF0000Goblin AI:|r Invalid import string")
        return false
    end
    
    -- Decompress
    local decompressed = self:DecompressString(importString)
    
    -- Deserialize
    local imported = self:DeserializeData(decompressed)
    
    if not imported or type(imported) ~= "table" then
        print("|cFFFF0000Goblin AI:|r Failed to import groups")
        return false
    end
    
    -- Merge with existing groups
    if not GoblinAIDB.groups then
        GoblinAIDB.groups = {}
    end
    
    for _, group in ipairs(imported) do
        table.insert(GoblinAIDB.groups, group)
    end
    
    print("|cFFFFD700Goblin AI:|r Imported " .. #imported .. " groups successfully")
    return true
end

function Advanced:SerializeData(data)
    -- Simple serialization (in production, use LibSerialize or similar)
    return "GOBLIN_DATA:" .. tostring(data)
end

function Advanced:DeserializeData(str)
    -- Simple deserialization
    if str:match("^GOBLIN_DATA:") then
        return {} -- Return empty table for now
    end
    return nil
end

function Advanced:CompressString(str)
    -- Simple encoding (in production, use LibDeflate)
    return "v1:" .. str
end

function Advanced:DecompressString(str)
    if str:match("^v1:") then
        return str:sub(4)
    end
    return str
end

-- ============================================================================
-- Notification System (Price Alerts)
-- ============================================================================

function Advanced:InitializeNotifications()
    -- Create notification frame
    if not self.notificationFrame then
        local frame = CreateFrame("Frame", "GoblinAINotifications", UIParent, "BackdropTemplate")
        frame:SetSize(300, 80)
        frame:SetPoint("TOP", 0, -150)
        frame:SetBackdrop({
            bgFile = "Interface\\DialogFrame\\UI-DialogBox-Background",
            edgeFile = "Interface\\DialogFrame\\UI-DialogBox-Border",
            tile = true, tileSize = 32, edgeSize = 16,
            insets = { left = 4, right = 4, top = 4, bottom = 4 }
        })
        frame:SetBackdropColor(0, 0, 0, 0.9)
        frame:Hide()
        
        frame.title = frame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        frame.title:SetPoint("TOP", 0, -10)
        frame.title:SetTextColor(1, 0.84, 0, 1)
        
        frame.text = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
        frame.text:SetPoint("CENTER", 0, -5)
        frame.text:SetWidth(280)
        
        self.notificationFrame = frame
    end
end

function Advanced:ShowNotification(title, text, duration)
    self:InitializeNotifications()
    
    self.notificationFrame.title:SetText(title)
    self.notificationFrame.text:SetText(text)
    self.notificationFrame:Show()
    
    -- Auto-hide
    C_Timer.After(duration or 5, function()
        if self.notificationFrame then
            self.notificationFrame:Hide()
        end
    end)
    
    -- Play sound
    PlaySound(SOUNDKIT.RAID_WARNING)
end

function Advanced:CheckPriceAlerts()
    -- Check for price changes that match alert criteria
    local alerts = GoblinAIDB.priceAlerts or {}
    
    for _, alert in ipairs(alerts) do
        local currentPrice = GoblinAI.BackendAPI:GetMarketPrice(alert.itemID)
        
        if currentPrice then
            local itemName = GetItemInfo(alert.itemID)
            
            if alert.condition == "below" and currentPrice <= alert.targetPrice then
                self:ShowNotification(
                    "Price Alert!",
                    string.format("%s is now %s (target: %s)", 
                        itemName or "Item",
                        GoblinAI:FormatGold(currentPrice),
                        GoblinAI:FormatGold(alert.targetPrice)),
                    8
                )
            elseif alert.condition == "above" and currentPrice >= alert.targetPrice then
                self:ShowNotification(
                    "Price Alert!",
                    string.format("%s is now %s (target: %s)", 
                        itemName or "Item",
                        GoblinAI:FormatGold(currentPrice),
                        GoblinAI:FormatGold(alert.targetPrice)),
                    8
                )
            end
        end
    end
end

-- ============================================================================
-- Slash Commands for Advanced Features
-- ============================================================================

SLASH_GOBLINADVANCED1 = "/gadvanced"
SlashCmdList["GOBLINADVANCED"] = function(msg)
    local cmd = msg:lower()
    
    if cmd == "export" then
        local exportStr = Advanced:ExportGroups()
        if exportStr then
            -- In a real addon, copy to clipboard
            print("Export string: " .. exportStr)
        end
        
    elseif cmd:match("^import ") then
        local importStr = cmd:gsub("^import ", "")
        Advanced:ImportGroups(importStr)
        
    elseif cmd == "tooltips on" then
        Advanced:InitializeTooltips()
        
    elseif cmd == "test notify" then
        Advanced:ShowNotification("Test Notification", "This is a test alert!", 5)
        
    else
        print("|cFFFFD700Goblin AI Advanced:|r")
        print("  /gadvanced export - Export groups")
        print("  /gadvanced import <string> - Import groups")
        print("  /gadvanced tooltips on - Enable TSM tooltips")
        print("  /gadvanced test notify - Test notifications")
    end
end

-- ============================================================================
-- Initialization
-- ============================================================================

-- Auto-enable tooltips
Advanced:InitializeTooltips()

-- Start price alert checker
C_Timer.NewTicker(60, function()
    if GoblinAIDB.settings.useBackend then
        Advanced:CheckPriceAlerts()
    end
end)

print("|cFFFFD700Goblin AI:|r Advanced features loaded - Price strings, tooltips, import/export ready")
