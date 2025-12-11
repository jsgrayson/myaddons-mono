local ADDON_NAME, SkillWeaver = ...
SkillWeaver.UI = SkillWeaver.UI or {}
local UI = {}
SkillWeaver.UI.Overlay = UI

-- Configuration
local UPDATE_INTERVAL = 0.1

function UI:Create()
    if self.frame then return end

    local f = CreateFrame("Frame", "SkillWeaverOverlay", UIParent, "BackdropTemplate")
    self.frame = f
    f:SetSize(64, 64)
    f:SetPoint("CENTER", 0, 200)
    f:SetMovable(true)
    f:EnableMouse(true)
    f:RegisterForDrag("LeftButton")
    f:SetScript("OnDragStart", f.StartMoving)
    f:SetScript("OnDragStop", f.StopMovingOrSizing)

    -- Icon Texture
    local icon = f:CreateTexture(nil, "ARTWORK")
    icon:SetAllPoints()
    icon:SetTexture("Interface\\Icons\\INV_Misc_QuestionMark")
    self.icon = icon

    -- Cooldown Swipe
    local cd = CreateFrame("Cooldown", "SkillWeaverOverlayCD", f, "CooldownFrameTemplate")
    cd:SetAllPoints()
    self.cd = cd

    -- Border
    f:SetBackdrop({
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
        edgeSize = 16,
    })

    -- Update Loop
    self.elapsed = 0
    f:SetScript("OnUpdate", function(self, elapsed)
        UI.elapsed = UI.elapsed + elapsed
        if UI.elapsed > UPDATE_INTERVAL then
            UI:UpdateIcon()
            UI.elapsed = 0
        end
    end)
end

function UI:UpdateIcon()
    local seq = SkillWeaver.ActiveSequence
    if not seq then 
        self.icon:SetTexture("Interface\\Icons\\INV_Misc_QuestionMark")
        return 
    end

    -- Find the first step that passes conditions (Priority Logic)
    -- Note: This mimics the Engine logic but in Lua.
    -- It might slightly disagree with SecureHandler if state is complex,
    -- but for "Priority" mode it is usually accurate.
    
    local bestStep = nil
    
    -- Check ST vs AoE based on some heuristic? 
    -- For now, we just check the main list (which UpdateSecureButton sets as 'steps')
    -- Wait, UpdateSecureButton sets 'steps' to either st or aoe based on macro?
    -- Actually, UpdateSecureButton is called with the *whole* sequence table.
    -- But the SecureHandler logic iterates 'steps'.
    -- We need to know if the user is pressing the ST or AoE button.
    -- We can't easily know that.
    -- Fallback: Just show ST prediction for now, or check modifier keys?
    
    local steps = seq.st or seq.steps
    if not steps then return end

    for _, step in ipairs(steps) do
        if SkillWeaver.Engine:PassesConditions(step.conditions) then
            bestStep = step
            break
        end
    end

    if bestStep then
        -- Extract spell name from command
        -- "/cast Mortal Strike" -> "Mortal Strike"
        local cmd = bestStep.command
        local spell = cmd:match("/cast%s+(.+)")
        
        if spell then
            -- Handle [cond] blocks in macro text?
            -- Simple heuristic: take the last word or clean it up
            -- " [target=mouseover] Heal" -> "Heal"
            if spell:find("]") then
                spell = spell:match("]%s*(.+)")
            end
            
            local texture = GetSpellTexture(spell)
            if texture then
                self.icon:SetTexture(texture)
                
                -- Update Cooldown
                local start, duration, enable = GetSpellCooldown(spell)
                if start and duration then
                    self.cd:SetCooldown(start, duration)
                end
            else
                self.icon:SetTexture("Interface\\Icons\\INV_Misc_QuestionMark")
            end
        end
    else
        self.icon:SetDesaturated(true)
    end
end

function UI:Toggle()
    if not self.frame then self:Create() end
    if self.frame:IsShown() then self.frame:Hide() else self.frame:Show() end
end

SLASH_SWOVERLAY1 = "/swoverlay"
SlashCmdList["SWOVERLAY"] = function()
    UI:Toggle()
end
