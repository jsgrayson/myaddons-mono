# Personalized Profession Guide System - Design

## Overview
Multi-character coordinated profession management system that optimizes crafting across your entire account for maximum profit and efficiency.

## Features

### 1. Character-Specific Leveling Guides
**Input:** Character name + current profession skill  
**Output:** Exact recipes to craft from current skill → max skill

**Example:**
```json
{
  "character": "Vaxo",
  "profession": "Alchemy",
  "current_skill": 45,
  "max_skill": 100,
  "next_steps": [
    {"skill_range": "45-55", "craft": "Lesser Healing Potion", "quantity": 20},
    {"skill_range": "55-70", "craft": "Elixir of Defense", "quantity": 15}
  ]
}
```

### 2. Profit-Optimized Specialization Guides
**For:** Dragonflight & The War Within professions  
**Input:** Character's profession + server economy data  
**Output:** Recommended knowledge point allocation for max profit

**Example:**
```json
{
  "character": "Slaythe",
  "profession": "Alchemy",
  "specialization_recommendations": [
    {"spec": "Potion Mastery", "priority": 1, "reason": "Potions sell 3x faster"},
    {"spec": "Phial Cauldrons", "priority": 2, "reason": "High profit margin (2500g avg)"}
  ]
}
```

### 3. Multi-Character Coordination 🆕
**Scenario:** You have 3 Alchemists across different characters  
**System:** Recommends which character should craft which recipes based on:
- Specializations (which char has the best spec for this recipe?)
- Materials availability (which char has the mats?)
- Profit margins (which recipe makes most gold?)
- Cooldowns (which char hasn't used their transmute CD?)

**Example:**
```json
{
  "profession": "Alchemy",
  "characters": ["Vaxo", "Slaythe", "Bronha"],
  "optimal_assignment": {
    "Potions": "Vaxo (has Potion Mastery spec)",
    "Transmutes": "Slaythe (transmute CD available)",
    "Phials": "Bronha (has Phial specialization)"
  }
}
```

## Data Requirements

### Currently Have ✅
- 9,761 recipes across all professions
- 840+ recipes with material data (growing)
- 4 character profiles

### Currently Missing ❌
- **Character profession skill levels** (need TradeSkillMaster or Skillet addon data)
- **Known recipes per character** (which recipes each char knows)
- **Profession specializations** (Dragonflight/TWW knowledge trees)
- **Material inventories** (waiting for DeepPockets scan)

## Import Plan

### Step 1: TradeSkillMaster Data
Import from `TradeSkillMaster.lua`:
```lua
TradeSkillMaster = {
  ["characters"] = {
    ["Vaxo - Dalaran"] = {
      ["Alchemy"] = {
        skill = 87,
        maxSkill = 100,
        recipes = {12345, 12346, ...}
      }
    }
  }
}
```

### Step 2: Profession Specs (Dragonflight/TWW)
Import from SavedVariables or Blizzard API:
- Knowledge points spent
- Active specializations
- Unlocked bonuses

### Step 3: Material Inventories
From DeepPockets (already have script, waiting for user to scan):
- Which character has which materials
- Quantities available

## Algorithm: Multi-Character Optimization

```python
def optimize_crafting_across_characters(profession, crafting_goal):
    """
    Given a crafting goal (e.g., "make 100 potions"),
    determine which characters should craft what
    """
    
    # Get all characters with this profession
    alchemists = get_characters_with_profession("Alchemy")
    
    # For each recipe needed
    for recipe in crafting_goal:
        # Score each character for this recipe
        scores = []
        for char in alchemists:
            score = calculate_craft_score(char, recipe)
            scores.append((char, score))
        
        # Assign to best character
        best_char = max(scores, key=lambda x: x[1])
        assign_recipe(best_char, recipe)
    
    return assignments

def calculate_craft_score(character, recipe):
    """Score = specialization bonus + material availability + cooldown status"""
    score = 0
    
    # Has the right specialization? +50 points
    if character.has_specialization_for(recipe):
        score += 50
    
    # Has materials? +30 points
    if character.has_materials_for(recipe):
        score += 30
    
    # Cooldown available? +20 points
    if not character.on_cooldown(recipe):
        score += 20
    
    return score
```

## UI Mockup

### Dashboard View
```
╔════════════════════════════════════════════════════╗
║  PROFESSION COORDINATOR                             ║
╠════════════════════════════════════════════════════╣
║                                                      ║
║  Alchemy (3 characters)                             ║
║  ├─ Vaxo        [Potion Master] Skill: 87/100      ║
║  │  └─ Next: Craft 15x Healing Potion (55-70)     ║
║  ├─ Slaythe     [Transmutation] Skill: 92/100      ║
║  │  └─ Next: Transmute: Iron to Gold (profit!)    ║
║  └─ Bronha      [Phial Expert]  Skill: 45/100      ║
║     └─ Next: Level to 55 (craft cheap phials)     ║
║                                                      ║
║  Recommended Crafts for Maximum Profit:             ║
║  • Vaxo: 50x Potion of Power (est. 5,000g profit) ║
║  • Slaythe: 10x Transmutes (est. 3,500g profit)   ║
║                                                      ║
╚════════════════════════════════════════════════════╝
```

## Next Steps

1. **Import profession data** from TradeSkillMaster or Skillet addon
2. **Populate professions table** with each character's current skills
3. **Import known recipes** per character
4. **Generate personalized guides** using the system above
5. **Add profit optimization** using market data from GoblinStack

## Files to Create

- `import_tradeskill_data.py` - Import from TSM/Skillet
- `profession_coordinator.py` - Multi-character optimization logic
- `generate_profit_guides.py` - Specialization recommendations
- `/api/profession-guide/{character}` - REST endpoint for guides
