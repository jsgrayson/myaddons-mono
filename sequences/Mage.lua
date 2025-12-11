local ADDON_NAME, SkillWeaver = ...

-- Mage Sequences
-- Covers: Arcane (62), Fire (63), Frost (64)

local MAGE_ARCANE = "MAGE_62"
local MAGE_FIRE = "MAGE_63"
local MAGE_FROST = "MAGE_64"

-----------------------------------------------------------
-- ARCANE MAGE (62)
-----------------------------------------------------------
SkillWeaver.Sequences[MAGE_ARCANE] = {
    ["Mythic+"] = {
        ["Sunfury"] = { -- Arcane / Sunfury Hero Talent
            type = "Priority",
            st = {
                -- Survival & Utility
                { command = "/cast Counterspell", conditions = "should_interrupt and range <= 40" },
                { command = "/cast Ice Block", conditions = "health < 20" },
                { command = "/cast [target=player] Alter Time", conditions = "health < 40 and talent(Alter Time)" },
                { command = "/cast [target=player] Mass Barrier", conditions = "health < 50 and in_group and talent(Mass Barrier)" },
                { command = "/cast Remove Curse", conditions = "dispellable:curse and range <= 40" },
                { command = "/cast Remove Curse", conditions = "dispellable:curse and range <= 40" },
                { command = "/cast Spellsteal", conditions = "target:has_stealable_buff and range <= 40" },
                { command = "/cast Greater Invisibility", conditions = "health < 15 or (in_group and threat > 90)" },
                { command = "/cast Invisibility", conditions = "health < 15 or (in_group and threat > 90)" },
                
                -- Pre-Combat
                { command = "/cast Arcane Intellect", conditions = "not buff:Arcane Intellect and not in_combat" },
                
                -- Cooldowns
                { command = "/cast Arcane Surge", conditions = "cooldown:Arcane Surge == 0 and mana >= 70" },
                { command = "/cast Touch of the Magi", conditions = "cooldown:Touch of the Magi == 0 and range <= 40" },
                { command = "/cast Radiant Spark", conditions = "talent(Radiant Spark) and range <= 40" },
                
                -- Arcane Charges Management
                { command = "/cast Arcane Blast", conditions = "buff:Arcane Charges < 4 and range <= 40" },
                { command = "/cast Arcane Barrage", conditions = "buff:Arcane Charges == 4 and mana < 50 and range <= 40" },
                { command = "/cast Arcane Missiles", conditions = "buff:Clearcasting and range <= 40" },
                
                -- Spenders
                { command = "/cast Arcane Barrage", conditions = "buff:Arcane Charges == 4 and buff:Arcane Surge and range <= 40" },
                
                -- Filler
                { command = "/cast Arcane Blast", conditions = "range <= 40" },
            },
            aoe = {
                { command = "/cast Counterspell", conditions = "should_interrupt and range <= 40" },
                { command = "/cast Arcane Surge", conditions = "cooldown:Arcane Surge == 0" },
                { command = "/cast Arcane Orb", conditions = "talent(Arcane Orb) and range <= 40" },
                { command = "/cast Arcane Barrage", conditions = "buff:Arcane Charges >= 3 and range <= 40" },
                { command = "/cast Arcane Explosion", conditions = "enemies_nearby >= 3 and range <= 10" },
                { command = "/cast Arcane Blast", conditions = "range <= 40" },
            },
            steps = {}
        }
    }
}

-----------------------------------------------------------
-- FIRE MAGE (63)
-----------------------------------------------------------
SkillWeaver.Sequences[MAGE_FIRE] = {
    ["Mythic+"] = {
        ["Sunfury"] = { -- Fire / Sunfury Hero Talent
            type = "Priority",
            st = {
                -- Survival & Utility
                { command = "/cast Counterspell", conditions = "should_interrupt and range <= 40" },
                { command = "/cast Ice Block", conditions = "health < 20" },
                { command = "/cast [target=player] Alter Time", conditions = "health < 40 and talent(Alter Time)" },
                { command = "/cast Blazing Barrier", conditions = "health < 60 and not buff:Blazing Barrier" },
                { command = "/cast Remove Curse", conditions = "dispellable:curse and range <= 40" },
                { command = "/cast Spellsteal", conditions = "target:has_stealable_buff and range <= 40" },
                { command = "/cast Greater Invisibility", conditions = "health < 15 or (in_group and threat > 90)" },
                { command = "/cast Invisibility", conditions = "health < 15 or (in_group and threat > 90)" },
                
                -- Pre-Combat
                { command = "/cast Arcane Intellect", conditions = "not buff:Arcane Intellect and not in_combat" },
                
                -- Cooldowns
                { command = "/cast Combustion", conditions = "cooldown:Combustion == 0" },
                { command = "/cast Phoenix Flames", conditions = "charges:Phoenix Flames > 2 and range <= 40" },
                { command = "/cast Fire Blast", conditions = "charges:Fire Blast > 2 and range <= 40" },
                
                -- Combustion Window
                { command = "/cast Pyroblast", conditions = "buff:Combustion and buff:Hot Streak and range <= 40" },
                { command = "/cast Fire Blast", conditions = "buff:Combustion and buff:Heating Up and range <= 40" },
                
                -- Hot Streak Management
                { command = "/cast Pyroblast", conditions = "buff:Hot Streak and range <= 40" },
                { command = "/cast Fire Blast", conditions = "buff:Heating Up and range <= 40" },
                { command = "/cast Phoenix Flames", conditions = "buff:Heating Up and range <= 40" },
                
                -- Generators
                { command = "/cast Scorch", conditions = "moving and range <= 40" },
                { command = "/cast Fireball", conditions = "range <= 40" },
            },
            aoe = {
                { command = "/cast Counterspell", conditions = "should_interrupt and range <= 40" },
                { command = "/cast Combustion", conditions = "cooldown:Combustion == 0" },
                { command = "/cast Flamestrike", conditions = "buff:Hot Streak and enemies_nearby >= 3 and range <= 40" },
                { command = "/cast Phoenix Flames", conditions = "range <= 40" },
                { command = "/cast Fire Blast", conditions = "range <= 40" },
                { command = "/cast Flamestrike", conditions = "enemies_nearby >= 3 and range <= 40" },
                { command = "/cast Fireball", conditions = "range <= 40" },
            },
            steps = {}
        }
    }
}

-----------------------------------------------------------
-- FROST MAGE (64)
-----------------------------------------------------------
SkillWeaver.Sequences[MAGE_FROST] = {
    ["Mythic+"] = {
        ["Frostfire"] = { -- Frost / Frostfire Hero Talent
            type = "Priority",
            st = {
                -- Survival & Utility
                { command = "/cast Counterspell", conditions = "should_interrupt and range <= 40" },
                { command = "/cast Ice Block", conditions = "health < 20" },
                { command = "/cast [target=player] Alter Time", conditions = "health < 40 and talent(Alter Time)" },
                { command = "/cast Ice Barrier", conditions = "health < 60 and not buff:Ice Barrier" },
                { command = "/cast Remove Curse", conditions = "dispellable:curse and range <= 40" },
                { command = "/cast Spellsteal", conditions = "target:has_stealable_buff and range <= 40" },
                { command = "/cast Greater Invisibility", conditions = "health < 15 or (in_group and threat > 90)" },
                { command = "/cast Invisibility", conditions = "health < 15 or (in_group and threat > 90)" },
                
                -- Pre-Combat
                { command = "/cast Arcane Intellect", conditions = "not buff:Arcane Intellect and not in_combat" },
                
                -- Cooldowns
                { command = "/cast Icy Veins", conditions = "cooldown:Icy Veins == 0" },
                { command = "/cast Frozen Orb", conditions = "cooldown:Frozen Orb == 0 and range <= 40" },
                { command = "/cast Comet Storm", conditions = "talent(Comet Storm) and range <= 40" },
                { command = "/cast Ray of Frost", conditions = "talent(Ray of Frost) and buff:Icy Veins and range <= 40" },
                
                -- Brain Freeze & Fingers of Frost
                { command = "/cast Flurry", conditions = "buff:Brain Freeze and range <= 40" },
                { command = "/cast Ice Lance", conditions = "buff:Fingers of Frost and range <= 40" },
                { command = "/cast Ice Lance", conditions = "debuff:Winter's Chill and range <= 40" },
                
                -- Generators
                { command = "/cast Ice Nova", conditions = "talent(Ice Nova) and range <= 40" },
                { command = "/cast Frostbolt", conditions = "range <= 40" },
            },
            aoe = {
                { command = "/cast Counterspell", conditions = "should_interrupt and range <= 40" },
                { command = "/cast Icy Veins", conditions = "cooldown:Icy Veins == 0" },
                { command = "/cast Frozen Orb", conditions = "range <= 40" },
                { command = "/cast Comet Storm", conditions = "talent(Comet Storm) and range <= 40" },
                { command = "/cast Blizzard", conditions = "enemies_nearby >= 3 and range <= 40" },
                { command = "/cast Ice Lance", conditions = "buff:Fingers of Frost and range <= 40" },
                { command = "/cast Flurry", conditions = "buff:Brain Freeze and range <= 40" },
                { command = "/cast Frostbolt", conditions = "range <= 40" },
            },
            steps = {}
        }
    },
    ["Midnight"] = { -- Visual Weaver Mode
        type = "Priority",
        st = {
            -- Cooldowns & Talents
            { command = "/cast Icy Veins", conditions = "can_cast:Icy Veins" },
            { command = "/cast Frozen Orb", conditions = "can_cast:Frozen Orb" },
            { command = "/cast Comet Storm", conditions = "can_cast:Comet Storm" },
            { command = "/cast Ray of Frost", conditions = "can_cast:Ray of Frost" },
            { command = "/cast Glacial Spike", conditions = "can_cast:Glacial Spike" },
            { command = "/cast Ice Nova", conditions = "can_cast:Ice Nova" },
            { command = "/cast Cone of Cold", conditions = "can_cast:Cone of Cold" },
            { command = "/cast Ebonbolt", conditions = "can_cast:Ebonbolt" },
            
            -- Core Rotation
            { command = "/cast Flurry", conditions = "can_cast:Flurry" },
            { command = "/cast Ice Lance", conditions = "can_cast:Ice Lance" },
            { command = "/cast Frostbolt", conditions = "true" },
        },
        aoe = {
            { command = "/cast Icy Veins", conditions = "can_cast:Icy Veins" },
            { command = "/cast Frozen Orb", conditions = "can_cast:Frozen Orb" },
            { command = "/cast Comet Storm", conditions = "can_cast:Comet Storm" },
            { command = "/cast Blizzard", conditions = "can_cast:Blizzard" },
            { command = "/cast Ice Nova", conditions = "can_cast:Ice Nova" },
            { command = "/cast Cone of Cold", conditions = "can_cast:Cone of Cold" },
            { command = "/cast Ice Lance", conditions = "can_cast:Ice Lance" },
            { command = "/cast Frostbolt", conditions = "true" },
        },
        steps = {}
    }
}
