local DP = DeepPockets
if not DP then return end

local traceEnabled = false

local function SafeText(fs)
    if fs and fs.GetText then
        return fs:GetText()
    end
end

local function Print(msg)
    DEFAULT_CHAT_FRAME:AddMessage("|cff88ccffDP-TT|r "..msg)
end

local function OnShow()
    if not traceEnabled then return end

    local owner = GameTooltip:GetOwner()
    local ownerName = owner and owner:GetName() or "nil"
    local line1 = SafeText(_G.GameTooltipTextLeft1) or "nil"

    Print("SHOW owner="..ownerName.." text="..line1)
end

local function OnHide()
    if not traceEnabled then return end
    Print("HIDE")
end

GameTooltip:HookScript("OnShow", OnShow)
GameTooltip:HookScript("OnHide", OnHide)

function DP:ToggleTooltipTrace(state)
    if state == nil then
        traceEnabled = not traceEnabled
    else
        traceEnabled = state
    end

    Print("trace "..(traceEnabled and "ON" or "OFF"))
end
