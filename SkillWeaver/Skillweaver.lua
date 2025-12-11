local addonName, addonTable = ...
SkillweaverDB = SkillweaverDB or {}
SkillweaverDB.sequences = SkillweaverDB.sequences or {}

-- Dummy Data for testing
if #SkillweaverDB.sequences == 0 then
    tinsert(SkillweaverDB.sequences, {
        name = "Advanced Macro",
        pre = "/cast [combat] Blood Fury\n/cast [mod:shift] Kick",
        body = "/cast Sinister Strike\n/cast Eviscerate",
        post = "/use Healthstone",
        icon = "Interface\\Icons\\inv_sword_27"
    })
end

local selectedIndex = nil
local activeSecureButton = nil

-- ============================================================================
-- SECURE LOGIC SYSTEM
-- ============================================================================

local function CreateSecureButton()
    local btn = CreateFrame("Button", "SkillweaverButton1", UIParent, "SecureActionButtonTemplate, SecureHandlerBaseTemplate")
    btn:SetSize(50, 50)
    btn:SetPoint("CENTER", 0, 0)
    
    btn.icon = btn:CreateTexture(nil, "BACKGROUND")
    btn.icon:SetAllPoints()
    btn.icon:SetTexture("Interface\\Icons\\inv_misc_questionmark")
    
    btn:SetMovable(true)
    btn:EnableMouse(true)
    btn:RegisterForDrag("LeftButton")
    btn:SetScript("OnDragStart", function(self) if not InCombatLockdown() then self:StartMoving() end end)
    btn:SetScript("OnDragStop", function(self) if not InCombatLockdown() then self:StopMovingOrSizing() end end)
    
    btn.cooldown = CreateFrame("Cooldown", nil, btn, "CooldownFrameTemplate")
    btn.cooldown:SetAllPoints()

    -- ========================================================================
    -- THE ADVANCED SNIPPET (Pre + Step + Post)
    -- ========================================================================
    btn:SetAttribute("_onclick", [[
        local limit = self:GetAttribute("step_limit") or 1
        local step = self:GetAttribute("step_index") or 1
        step = (step % limit) + 1
        self:SetAttribute("step_index", step)
        
        -- 1. Get Pre-Macro
        local pre = self:GetAttribute("macro_pre") or ""
        
        -- 2. Get Current Step Line
        local line = self:GetAttribute("macro_line_" .. step) or ""
        
        -- 3. Get Post-Macro
        local post = self:GetAttribute("macro_post") or ""
        
        -- 4. Combine them into one executable block
        local full_macro = pre .. "\n" .. line .. "\n" .. post
        
        self:SetAttribute("macrotext", full_macro)
    ]])
    
    btn:SetAttribute("type", "macro")
    print("|cff00FF00Skillweaver:|r Secure Button Created.")
    return btn
end

local function UpdateSecureButton(seq)
    if InCombatLockdown() then print("Combat Lockdown! Cannot update.") return end
    if not activeSecureButton then activeSecureButton = CreateSecureButton() end
    
    activeSecureButton.icon:SetTexture(seq.icon)
    
    -- LOAD PRE & POST ATTRIBUTES
    activeSecureButton:SetAttribute("macro_pre", seq.pre)
    activeSecureButton:SetAttribute("macro_post", seq.post)
    
    -- LOAD STEPS
    local lines = {}
    for s in seq.body:gmatch("[^\r\n]+") do table.insert(lines, s) end
    
    activeSecureButton:SetAttribute("step_index", 0)
    activeSecureButton:SetAttribute("step_limit", #lines)
    
    for i, line in ipairs(lines) do
        activeSecureButton:SetAttribute("macro_line_" .. i, line)
    end
    
    activeSecureButton:Show()
    print("Updated: " .. seq.name)
end

-- ============================================================================
-- UI Logic (Saving/Loading 3 Boxes)
-- ============================================================================

local function SaveSequence()
    if not selectedIndex then return end
    
    -- Get text from all 3 boxes
    local preBox = SkillweaverFrame.RightInset.PreFrame.Scroll.Edit
    local seqBox = SkillweaverFrame.RightInset.SeqFrame.Scroll.Edit
    local postBox = SkillweaverFrame.RightInset.PostFrame.Scroll.Edit
    
    local item = SkillweaverDB.sequences[selectedIndex]
    item.pre = preBox:GetText()
    item.body = seqBox:GetText()
    item.post = postBox:GetText()
    
    SkillweaverList_Update()
    print("Saved.")
end

function Skillweaver_OnListClick(self, button)
    if not self.dataID then return end
    selectedIndex = self.dataID
    local seq = SkillweaverDB.sequences[selectedIndex]
    
    SkillweaverFrame.RightInset.PreFrame.Scroll.Edit:SetText(seq.pre or "")
    SkillweaverFrame.RightInset.SeqFrame.Scroll.Edit:SetText(seq.body or "")
    SkillweaverFrame.RightInset.PostFrame.Scroll.Edit:SetText(seq.post or "")
    
    SkillweaverList_Update()
end

function SkillweaverList_Update()
    local scrollFrame = SkillweaverFrame.LeftInset.ListScrollFrame
    local buttons = scrollFrame.buttons 
    local offset = HybridScrollFrame_GetOffset(scrollFrame) 
    local numItems = #SkillweaverDB.sequences

    for i = 1, #buttons do
        local button = buttons[i]
        local index = offset + i 
        if index <= numItems then
            local item = SkillweaverDB.sequences[index]
            button:Show()
            button.name:SetText(item.name)
            
            local lines = 0
            for _ in string.gmatch(item.body or "", "\n") do lines = lines + 1 end
            button.details:SetText("Steps: " .. (lines+1))
            button.icon:SetTexture(item.icon)
            button.dataID = index
            if index == selectedIndex then button:LockHighlight() else button:UnlockHighlight() end
        else
            button:Hide()
        end
    end
    HybridScrollFrame_Update(scrollFrame, numItems * 46, scrollFrame:GetHeight())
end

-- ============================================================================
-- Init
-- ============================================================================

local function OnEvent(self, event, ...)
    if event == "PLAYER_LOGIN" then
        local scrollFrame = SkillweaverFrame.LeftInset.ListScrollFrame
        HybridScrollFrame_CreateButtons(scrollFrame, "SkillweaverListButtonTemplate")
        scrollFrame.update = SkillweaverList_Update
        
        SkillweaverFrame.SaveButton:SetScript("OnClick", SaveSequence)
        SkillweaverFrame.SpawnButton:SetScript("OnClick", function()
            if selectedIndex then UpdateSecureButton(SkillweaverDB.sequences[selectedIndex]) end
        end)
        
        SkillweaverList_Update()
    end
end

local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:SetScript("OnEvent", OnEvent)

SLASH_SKILLWEAVER1 = "/skillweaver"
SlashCmdList["SKILLWEAVER"] = function(msg)
    if SkillweaverFrame:IsShown() then SkillweaverFrame:Hide() else SkillweaverFrame:Show() end
end
