--========================================================--
-- SkillWeaver - Racial Manager
-- Automatically manages and recommends Racial Abilities
--========================================================--

local ADDON_NAME, SkillWeaver = ...
local RacialManager = {}
SkillWeaver.RacialManager = RacialManager

-- Racial Spells Database
-- Format: [SpellID] = { name="Name", type="Burst"|"Utility"|"Defensive", cooldown=120 }
local RACIALS = {
    -- Orc
    [20572] = { name = "Blood Fury", type = "Burst", cooldown = 120 },
    -- Troll
    [26297] = { name = "Berserking", type = "Burst", cooldown = 180 },
    -- Mag'har Orc
    [274738] = { name = "Ancestral Call", type = "Burst", cooldown = 120 },
    -- Dark Iron Dwarf
    [265221] = { name = "Fireblood", type = "Burst", cooldown = 120 }, -- Also cleanses
    -- Tauren
    [20549] = { name = "War Stomp", type = "Utility", cooldown = 90 },
    -- Highmountain Tauren
    [255654] = { name = "Bull Rush", type = "Utility", cooldown = 120 },
    -- Blood Elf
    [202719] = { name = "Arcane Torrent", type = "Utility", cooldown = 120 }, -- Purge + Resource
    -- Goblin
    [69041] = { name = "Rocket Barrage", type = "Damage", cooldown = 90 },
    [69070] = { name = "Rocket Jump", type = "Utility", cooldown = 90 },
    -- Human
    [59752] = { name = "Will to Survive", type = "Defensive", cooldown = 180 }, -- Stun break
    -- Dwarf
    [20594] = { name = "Stoneform", type = "Defensive", cooldown = 120 },
    -- Night Elf
    [58984] = { name = "Shadowmeld", type = "Utility", cooldown = 120 },
    -- Gnome
    [20589] = { name = "Escape Artist", type = "Utility", cooldown = 60 },
    -- Draenei
    [59544] = { name = "Gift of the Naaru", type = "Defensive", cooldown = 180 },
    -- Worgen
    [68992] = { name = "Darkflight", type = "Utility", cooldown = 120 },
    -- Void Elf
    [256948] = { name = "Spatial Rift", type = "Utility", cooldown = 180 },
    -- Lightforged Draenei
    [255647] = { name = "Light's Judgment", type = "Damage", cooldown = 150 },
    -- Kul Tiran
    [287712] = { name = "Haymaker", type = "Utility", cooldown = 150 },
    -- Mechagnome
    [312924] = { name = "Hyper Organic Light Originator", type = "Utility", cooldown = 180 }, -- Clones
    -- Pandaren
    [107079] = { name = "Quaking Palm", type = "Utility", cooldown = 120 },
    -- Dracthyr
    [368970] = { name = "Tail Swipe", type = "Utility", cooldown = 90 },
    [357210] = { name = "Wing Buffet", type = "Utility", cooldown = 90 },
}

-- Cache player's racial
RacialManager.PlayerRacial = nil

function RacialManager:DetectRacial()
    for id, data in pairs(RACIALS) do
        if IsSpellKnown(id) then
            self.PlayerRacial = { id = id, data = data }
            print("SkillWeaver: Detected Racial - " .. data.name)
            return
        end
    end
end

-- Check if racial should be used
-- @param context: "Burst", "Defensive", "Interrupt"
function RacialManager:ShouldUseRacial(context)
    if not self.PlayerRacial then self:DetectRacial() end
    if not self.PlayerRacial then return false end

    local racial = self.PlayerRacial
    local spellName = GetSpellInfo(racial.id)
    
    -- Cooldown check
    local start, duration = GetSpellCooldown(racial.id)
    if start > 0 and duration > 1.5 then return false end -- On CD

    -- Logic based on type
    if context == "Burst" and racial.data.type == "Burst" then
        return true
    elseif context == "Defensive" and racial.data.type == "Defensive" then
        -- Add health check logic here if needed, usually handled by sequence conditions
        return true
    elseif context == "Interrupt" and racial.data.name == "Arcane Torrent" then
        -- Arcane Torrent is a purge, sometimes used as interrupt in PvE logic (though it's a purge now)
        -- Actually it's a purge. War Stomp / Quaking Palm are interrupts/stops.
        return false
    elseif context == "CC" and (racial.data.name == "War Stomp" or racial.data.name == "Quaking Palm" or racial.data.name == "Haymaker") then
        return true
    end

    return false
end

-- Get the macro command for the racial
function RacialManager:GetCastCommand()
    if not self.PlayerRacial then self:DetectRacial() end
    if self.PlayerRacial then
        return "/cast " .. self.PlayerRacial.data.name
    end
    return nil
end

-- Initialize
local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_LOGIN")
f:SetScript("OnEvent", function() RacialManager:DetectRacial() end)

return RacialManager
