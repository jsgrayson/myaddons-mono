local SW = SkillWeaver
SW.TalentSuggestions = SW.TalentSuggestions or {}

-- Minimal stub; backend should override with current patch builds.
SW.TalentSuggestions["WARRIOR_71"] = { -- Arms example
  PvE = {
    Delves = { talents = "CLASS_TREE_STRING", notes = "Low APM, strong sustain." },
    MythicPlus = { talents = "CLASS_TREE_STRING", notes = "Cleave + survivability." },
  },
  PvP = {
    BGs = { pvpTalents = { "Disarm", "War Banner", "Storm of Destruction" } }
  }
}
