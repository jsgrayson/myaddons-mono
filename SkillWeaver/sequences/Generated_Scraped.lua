local ADDON_NAME, SkillWeaver = ...
-- GENERATED FILE - DO NOT EDIT MANUALLY
-- Scraped from Icy Veins

SkillWeaver.Sequences = SkillWeaver.Sequences or {}
SkillWeaver.Talents = SkillWeaver.Talents or {}


SkillWeaver.Sequences["WARRIOR_71"] = SkillWeaver.Sequences["WARRIOR_71"] or {}
SkillWeaver.Talents["WARRIOR_71"] = SkillWeaver.Talents["WARRIOR_71"] or {}

SkillWeaver.Talents["WARRIOR_71"]["Raid"] = SkillWeaver.Talents["WARRIOR_71"]["Raid"] or {}
SkillWeaver.Talents["WARRIOR_71"]["Raid"]["Scraped"] = "BrewmasterMistweaverWindwalker"

SkillWeaver.Sequences["PALADIN_70"] = SkillWeaver.Sequences["PALADIN_70"] or {}
SkillWeaver.Talents["PALADIN_70"] = SkillWeaver.Talents["PALADIN_70"] or {}

SkillWeaver.Sequences["PALADIN_70"]["Raid"] = SkillWeaver.Sequences["PALADIN_70"]["Raid"] or {}
SkillWeaver.Sequences["PALADIN_70"]["Raid"]["Scraped"] = {
    type = "Priority",
    st = {
        { command = "/cast Blade of Justice", conditions = "true" },
        { command = "/cast Divine Toll", conditions = "holypower < 5" },
        { command = "/cast Judgment", conditions = "holypower < 5" },
        { command = "/cast Divine Hammer", conditions = "true" },
        { command = "/cast Execution Sentence", conditions = "true" },
        { command = "/cast Avenging Wrath", conditions = "true" },
        { command = "/cast Crusade", conditions = "true" },
        { command = "/cast Final Reckoning", conditions = "true" },
        { command = "/cast Wake of Ashes", conditions = "true" },
        { command = "/cast Final Verdict", conditions = "true" },
        { command = "/cast Final Verdict", conditions = "true" },
        { command = "/cast Hammer of Light", conditions = "true" },
    },
    aoe = {}, 
    steps = {}
}

SkillWeaver.Talents["PALADIN_70"]["Raid"] = SkillWeaver.Talents["PALADIN_70"]["Raid"] or {}
SkillWeaver.Talents["PALADIN_70"]["Raid"]["Scraped"] = "BrewmasterMistweaverWindwalker"

SkillWeaver.Sequences["PALADIN_70"]["MythicPlus"] = SkillWeaver.Sequences["PALADIN_70"]["MythicPlus"] or {}
SkillWeaver.Sequences["PALADIN_70"]["MythicPlus"]["Scraped"] = {
    type = "Priority",
    st = {
        { command = "/cast it first", conditions = "true" },
        { command = "/cast it often", conditions = "true" },
        { command = "/cast it
dangerous mob", conditions = "true" },
    },
    aoe = {}, 
    steps = {}
}
