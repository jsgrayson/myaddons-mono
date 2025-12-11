local Engine = require("skillweaver.core.HealerEngine")

local H = {}

H.specMap = {
    PALADIN_65      = "paladin_holy",
    PRIEST_256      = "priest_disc",
    PRIEST_257      = "priest_holy",
    DRUID_105       = "druid_resto",
    SHAMAN_264      = "shaman_resto",
    MONK_270        = "monk_mw",
    EVOKER_1468     = "evoker_preservation",
}

function H:Activate(specID)
    local specName = H.specMap[specID]
    if not specName then
        print("[SkillWeaver] No healer config for spec:", specID)
        return
    end

    Engine:LoadSpecConfig(specName)
    Engine:BindToInput()

    print("[SkillWeaver] Healer Engine Active →", specName)
end

return H
