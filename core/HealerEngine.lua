local HealerUltra   = require("skillweaver.healer.HealerUltra")
local HealSnap      = require("skillweaver.healer.HealSnap")
local HealerUI      = require("skillweaver.healer.HealerUI")
local Bindings      = require("skillweaver.healer.HealerBindings")

local Engine = {}

Engine.activeSpec = nil
Engine.config = nil
Engine.context = {}

-----------------------------------------------------------
-- Load per-spec healer config
-----------------------------------------------------------
function Engine:LoadSpecConfig(specName)
    local path = "skillweaver.healer_configs." .. specName
    local ok, cfg = pcall(require, path)

    if not ok or not cfg then
        print("[SkillWeaver] ERROR loading healer config:", specName)
        return
    end

    self.config = cfg
    print("[SkillWeaver] Loaded healer config:", specName)
end

-----------------------------------------------------------
-- Build the decision context for Ultra Brain
-----------------------------------------------------------
function Engine:BuildContext()
    local C = {}
    local cfg = self.config
    if not cfg then return nil end

    local function stub(spell)
        return {
            spell = spell,
            usable = true -- real API hook later
        }
    end

    C.emergency  = stub(cfg.emergency)
    C.cleanse    = stub(cfg.cleanse)
    C.self       = stub(cfg.fast)
    C.tank       = stub(cfg.tank)
    C.aoe        = stub(cfg.aoe)
    C.cooldown   = stub(cfg.emergency)
    C.fast       = stub(cfg.fast)
    C.efficient  = stub(cfg.efficient)
    C.dps        = stub("Smite") -- replaced per class later

    self.context = C
    return C
end

-----------------------------------------------------------
-- Get spell recommendation
-----------------------------------------------------------
function Engine:GetRecommendation()
    local ctx = self:BuildContext()
    local spell, reason = HealerUltra:GetRecommendedSpell(ctx)
    return spell, reason
end

-----------------------------------------------------------
-- Behavior when the MAIN HEAL BUTTON is pressed
-----------------------------------------------------------
function Engine:OnHealPressed()
    local spell, reason = self:GetRecommendation()
    if not spell then return end

    local bestTarget = "Target"

    HealerUI:ShowRecommendation(spell, reason, bestTarget)

    HealSnap:BeginSnap(bestTarget)
    local finalTarget = HealSnap:EndSnap()

    print("[SkillWeaver] CAST:", spell, " → ", finalTarget)
end

-----------------------------------------------------------
-- Bind the engine to the main input
-----------------------------------------------------------
function Engine:BindToInput()
    Bindings:OnMainButtonPressed(function()
        self:OnHealPressed()
    end)
end

return Engine
