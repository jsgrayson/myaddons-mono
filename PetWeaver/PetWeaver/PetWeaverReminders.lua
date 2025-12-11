-- Safari Hat Reminder and Squirt Alerts
local SafariHatFrame = CreateFrame("Frame")
local lastWarningTime = 0

-- Check for Safari Hat buff
local function HasSafariHat()
    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if name and (string.find(name, "Safari") or string.find(name, "Battle Pet Training")) then
            return true
        end
    end
    return false
end

-- Show Safari Hat warning
local function WarnSafariHat()
    local now = time()
    if now - lastWarningTime < 300 then return end -- Don't spam (5 min cooldown)
    
    if not HasSafariHat() then
        print("|cffff0000[PetWeaver]|r ⚠️ |cffFFFF00WARNING: Equip your Safari Hat for +10% XP!|r")
        lastWarningTime = now
    end
end

-- Squirt day detection
local function CheckSquirtDay()
    -- Base date: Jan 1, 2024 (adjust if needed)
    local baseDate = 1704067200 -- Unix timestamp for Jan 1, 2024
    local currentTime = time()
    local daysSinceBase = math.floor((currentTime - baseDate) / 86400)
    
    -- Squirt appears every 15 days
    local isSquirtDay = (daysSinceBase % 15) == 0
    local daysUntilSquirt = 15 - (daysSinceBase % 15)
    
    if isSquirtDay then
        print("|cffff0000[PetWeaver]|r 🎉 |cffFF00FFSQUIRT DAY!|r Visit your WoD Garrison!")
        print("|cffff0000[PetWeaver]|r 💜 Check if Pet Battle Week is active for |cffFF00FFSUPER SQUIRT|r!")
    elseif daysUntilSquirt <= 1 then
        print("|cffff0000[PetWeaver]|r ⏰ Squirt tomorrow! Prepare your Safari Hat!")
    end
end

-- Pet battle detection
SafariHatFrame:RegisterEvent("PET_BATTLE_OPENING_START")
SafariHatFrame:SetScript("OnEvent", function(self, event)
    if event == "PET_BATTLE_OPENING_START" then
        WarnSafariHat()
    end
end)

-- Login check for Squirt
SafariHatFrame:RegisterEvent("PLAYER_LOGIN")
SafariHatFrame:SetScript("OnEvent", function(self, event)
    if event == "PLAYER_LOGIN" then
        C_Timer.After(3, CheckSquirtDay) -- Check 3 seconds after login
    end
end)

-- Co-Pilot: Audio Feedback
local CoPilotFrame = CreateFrame("Frame")
CoPilotFrame:RegisterEvent("PET_BATTLE_OVER")
CoPilotFrame:RegisterEvent("PET_BATTLE_TURN_STARTED")

CoPilotFrame:SetScript("OnEvent", function(self, event, winner)
    if event == "PET_BATTLE_OVER" then
        if winner == 1 then -- Player Won
            PlaySoundFile("Sound\\Interface\\RaidWarning.ogg") -- Victory Sound
            print("|cff00ff00[PetWeaver]|r 🏆 Battle Won!")
        end
    elseif event == "PET_BATTLE_TURN_STARTED" then
        -- Check if swap is recommended (Placeholder logic)
        -- In a real implementation, this would check the strategy engine
        local activePetIndex = C_PetBattles.GetActivePet(1)
        local health = C_PetBattles.GetHealth(1, activePetIndex)
        local maxHealth = C_PetBattles.GetMaxHealth(1, activePetIndex)
        
        if health and maxHealth and (health / maxHealth) < 0.1 and health > 0 then
            -- Low health warning (Swap might be needed)
            PlaySoundFile("Sound\\Interface\\ReadyCheck.ogg") -- Alert Sound
            print("|cffff0000[PetWeaver]|r ⚠️ Low Health! Consider Swapping.")
        end
    end
end)
