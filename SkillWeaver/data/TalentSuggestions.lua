-- data/TalentSuggestions.lua
SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver

SW.TalentSuggestions = SW.TalentSuggestions or {}

SW.TalentSuggestions["PRIEST_258"] = {
  PvE = {
    -- Delves / Open World priority
    ST = {
      notes = "Shadow (258) — Delves/OW ST (Easy Mode): forgiving, steady damage.",
      talents = "CIQAAAAAAAAAAAAAAAAAAAAAAMDmZAAAAAAAAAAAAYM2gZmZZbjZGzMzMLDmNmZmZMbMwYMMLmtpmZwCMzMAQAmtZbBMbsAYbmB",
    },
    AOE = {
      notes = "Shadow (258) — Delves/OW AOE (Easy Mode): burst AoE + simpler play.",
      talents = "CIQAAAAAAAAAAAAAAAAAAAAAAMDmZAAAAAAAAAAAAYM2YMzMLbGzMmZmZWGMbMzMzY2YgxYYWMbTNzgFYmZAgAMbz2CY2YBw2MA",
    },
  },
}

-- Mapping aliases
SW.TalentSuggestions["PRIEST_258"].PvE.Delves = SW.TalentSuggestions["PRIEST_258"].PvE.ST
SW.TalentSuggestions["PRIEST_258"].PvE.OpenWorld = SW.TalentSuggestions["PRIEST_258"].PvE.ST
