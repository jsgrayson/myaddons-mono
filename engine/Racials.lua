local ADDON_NAME, SkillWeaver = ...
SkillWeaver.Racials = {}
local Racials = SkillWeaver.Racials

-- Racial Spell IDs
local RACIAL_SPELLS = {
    -- Orc
    ["Orc"] = { id = 20572, type = "DPS" }, -- Blood Fury
    ["MagharOrc"] = { id = 274738, type = "DPS" }, -- Ancestral Call
    
    -- Troll
    ["Troll"] = { id = 26297, type = "DPS" }, -- Berserking
    ["ZandalariTroll"] = { id = 291944, type = "DPS" }, -- Regeneratin' (Channel Heal - maybe Utility?) or Pterrordax Swoop? Zandalari is tricky due to Loa choice. Sticking to Regeneratin' for now as the active.
    
    -- Dwarf
    ["Dwarf"] = { id = 20594, type = "Cleanse" }, -- Stoneform
    ["DarkIronDwarf"] = { id = 265221, type = "CleanseDPS" }, -- Fireblood
    
    -- Human
    ["Human"] = { id = 59752, type = "CCBreak" }, -- Will to Survive
    
    -- Gnome
    ["Gnome"] = { id = 20589, type = "RootBreak" }, -- Escape Artist
    
    -- Undead
    ["Scourge"] = { id = 7744, type = "CCBreak_Fear" }, -- Will of the Forsaken
    
    -- Tauren
    ["Tauren"] = { id = 20549, type = "AoEStun" }, -- War Stomp
    ["HighmountainTauren"] = { id = 255654, type = "AoEStun" }, -- Bull Rush
    
    -- Blood Elf
    ["BloodElf"] = { id = 202719, type = "Dispel" }, -- Arcane Torrent
    
    -- Goblin
    ["Goblin"] = { id = 69041, type = "DPS" }, -- Rocket Barrage (Jump is 69070)
    
    -- Draenei
    ["Draenei"] = { id = 59547, type = "Heal" }, -- Gift of the Naaru
    ["LightforgedDraenei"] = { id = 255647, type = "AoEDPS" }, -- Light's Judgment
    
    -- Night Elf
    ["NightElf"] = { id = 58984, type = "Utility" }, -- Shadowmeld
    
    -- Worgen
    ["Worgen"] = { id = 68992, type = "Sprint" }, -- Darkflight
    
    -- Pandaren
    ["Pandaren"] = { id = 107079, type = "CC" }, -- Quaking Palm
    
    -- Dracthyr
    ["Dracthyr"] = { id = 368970, type = "CC" }, -- Tail Swipe (Choice node with Wing Buffet, usually Tail Swipe is default)
    
    -- Earthen
    ["Earthen"] = { id = 436344, type = "Empower" }, -- Azerite Surge
}

function Racials.GetPlayerRacial()
    local _, raceFile = UnitRace("player")
    return RACIAL_SPELLS[raceFile]
end

function Racials.ShouldUseRacial()
    local racial = Racials.GetPlayerRacial()
    if not racial then return false, nil end
    
    local spellId = racial.id
    local usable, noMana = C_Spell.IsSpellUsable(spellId)
    if not usable or noMana then return false, nil end
    
    local start, duration = C_Spell.GetSpellCooldown(spellId)
    if start > 0 and duration > 1.5 then return false, nil end -- On CD
    
    local type = racial.type
    
    -- DPS Logic
    if type == "DPS" or type == "AoEDPS" or type == "CleanseDPS" then
        -- Use on cooldown if in combat and target exists
        if UnitAffectingCombat("player") and UnitExists("target") and UnitCanAttack("player", "target") then
            return true, spellId
        end
    end
    
    -- Cleanse Logic (Stoneform/Fireblood)
    if type == "Cleanse" or type == "CleanseDPS" then
        -- Check for Bleed, Poison, Disease, Curse, Magic
        -- Simple check: Do we have any detrimental aura that is dispellable?
        -- Stoneform: Poison, Disease, Curse, Magic, Bleed
        -- Fireblood: Poison, Disease, Curse, Magic, Bleed
        -- For now, just check if we have *any* harmful aura that matches these types.
        -- This is a simplification; a more robust check would iterate auras.
        for i = 1, 40 do
            local _, _, _, debuffType = UnitDebuff("player", i)
            if debuffType and (debuffType == "Poison" or debuffType == "Disease" or debuffType == "Curse" or debuffType == "Magic") then
                return true, spellId
            end
        end
    end
    
    -- CC Break Logic
    if type == "CCBreak" or type == "CCBreak_Fear" then
        -- Check if player is stunned/feared
        -- This requires checking specific aura mechanics or loss of control events.
        -- Simplified: Check for "Stun" or "Fear" debuff types not strictly available via UnitDebuff type return (which is school).
        -- We'd need to parse C_LossOfControl.
        local locType = C_LossOfControl.GetActiveLossOfControlData(1).locType
        if locType == "STUN" and type == "CCBreak" then return true, spellId end
        if (locType == "FEAR" or locType == "CHARM" or locType == "SLEEP") and type == "CCBreak_Fear" then return true, spellId end
    end
    
    -- Root Break Logic
    if type == "RootBreak" then
        local locType = C_LossOfControl.GetActiveLossOfControlData(1).locType
        if locType == "ROOT" then return true, spellId end
    end
    
    -- AoE Stun Logic
    if type == "AoEStun" then
        -- Use if 2+ enemies in melee range? Hard to detect without nameplates.
        -- Fallback: Use if in combat and target is casting interruptible?
        if UnitAffectingCombat("player") and UnitExists("target") then
            local _, _, _, _, _, _, _, _, interruptible = UnitCastingInfo("target")
            if interruptible then return true, spellId end
        end
    end
    
    -- Dispel Logic (Arcane Torrent)
    if type == "Dispel" then
        -- Check if target has purgeable buff
        -- (Requires scanning target buffs)
        -- Also restores resource, so maybe use if resource low?
        -- For now, treat as DPS/Utility mix: Use if target casting (silence/interrupt logic removed in BFA, now just dispel).
        -- Actually Arcane Torrent is just a purge now.
        for i = 1, 40 do
            local _, _, _, _, _, _, _, _, _, _, _, isPurgeable = UnitBuff("target", i)
            if isPurgeable then return true, spellId end
        end
    end

    return false, nil
end
