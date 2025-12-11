# Data Sources & Enemy AI System

## Overview
This document explains the various data sources in the PetWeaver project, their compatibility issues, and the current working solution for enemy AI.

## Data Files

### Working Data
- **`enhanced_enemy_npc_scripts.json`** ✅ WORKING
  - 123 encounters with AI scripts
  - Generated from analyzing 182,452 player battle scripts
  - Contains: priority abilities, HP conditionals, general rotation
  - Format: `use(AbilityName:ID) [condition]`
  
- **`npc_move_orders.json`** ✅ WORKING
  - 123 encounters with 15-round move sequences
  - Generated from enhanced AI scripts
  - Used by `simulator/npc_move_loader.py`
  - Format: `{"encounter": {"1": {"1": "Move", "2": "Move", ...}}}`

- **`abilities.json`** ✅ WORKING
  - 620 ability definitions with cooldowns
  - 953 species ability mappings
  - Used by enhanced AI script generation

### Incompatible/Broken Data
- **`encounters.json`** ❌ INCOMPATIBLE
  - 306 NPC encounters
  - **Problem:** All pets have empty `abilities: []` arrays
  - **Why:** Species IDs don't match `abilities.json` mapping
  - **Example:** Species 872, 873, 889 not found in abilities database
  - **Cannot be hydrated** without correct species mapping

- **`variations_with_scripts_final.json`** ⚠️ REFERENCE ONLY
  - 279 unique encounter URLs
  - 182,452 player strategy variations
  - **Use:** Source data for AI generation, not runtime

## System Architecture

### Current Working Solution: Enhanced AI System

```
Player Scripts (182K) 
    ↓
Analyze Patterns
    ↓
Enhanced Enemy AI Scripts (123)
    ↓
Generate Move Orders
    ↓
Battle Simulator
```

### What DOESN'T Work

```
encounters.json (empty abilities)
    ↓
Try to hydrate from abilities.json
    ↓
❌ Species ID mismatch
    ↓
❌ Cannot generate valid moves
```

## Integration Status

### ✅ Complete
1. **Enemy AI Scripts**
   - `simulator/npc_ai_loader.py` - Loads enhanced AI scripts
   - `simulator/npc_ai.py` - Uses AI for combat decisions
   - Priority abilities, HP conditionals, rotation logic

2. **Move Orders**
   - `simulator/npc_move_loader.py` - Loads JSON move orders
   - `simulator/npc_move_simulator.py` - Generates moves with cooldowns
   - Cooldown-aware, never-pass guarantee

3. **Battle Simulator**
   - Real enemy AI integrated
   - 123 encounters ready for genetic algorithm
   - No more "Black Claw spam" bug

## Known Issues & Solutions

### Issue: Black Claw Spam
**Problem:** Enemy uses cooldown abilities every turn  
**Cause:** Empty abilities array in encounters.json  
**Solution:** Use enhanced AI move orders instead  
**Status:** ✅ Fixed

### Issue: Species ID Mismatch
**Problem:** Can't hydrate encounters.json from abilities.json  
**Cause:**  
- encounters.json species IDs: 1, 872, 873, 890, 889...
- abilities.json species IDs: 2051, 2062, 2446, 2084...
- Different data sources, incompatible mappings

**Solution:** Don't use encounters.json for abilities  
**Status:** ✅ Documented, using enhanced AI instead

### Issue: Move Order Generation
**Problem:** generate_final_npc_move_orders.py produces empty moves  
**Cause:** Relies on encounters.json which has no abilities  
**Solution:** Use `regenerate_move_orders.py` with enhanced AI  
**Status:** ✅ Alternative implemented

## File Purposes

| File | Purpose | Status |
|------|---------|--------|
| `enhanced_enemy_npc_scripts.json` | AI combat logic | ✅ Use this |
| `npc_move_orders.json` | Turn-by-turn moves | ✅ Use this |
| `abilities.json` | Ability stats | ✅ Reference |
| `encounters.json` | NPC metadata | ⚠️ Stats only |
| `variations_with_scripts_final.json` | Raw scrape data | 📚 Archive |

## Scripts

### Working Scripts
- `comprehensive_enemy_analysis.py` - Analyzes battle data
- `generate_enhanced_enemy_scripts.py` - Creates AI scripts
- `regenerate_move_orders.py` - Generates move orders from AI
- `simulator/npc_ai_loader.py` - Runtime AI loader

### Reference/Debug Scripts
- `generate_final_npc_move_orders.py` - Attempts encounters.json hydration (fails)
- `fix_encounters.py` - Attempts species ID mapping (incompatible data)
- `deduce_enemy_movesets.py` - Initial analysis tool

## Recommendations

### For Battle Simulation
1. Use `npc_move_orders.json` via `npc_move_loader.py`
2. Load enhanced AI scripts via `npc_ai_loader.py`
3. Don't try to fix encounters.json - data is incompatible

### For Adding New Encounters
1. Add to `variations_with_scripts_final.json`
2. Run `comprehensive_enemy_analysis.py`
3. Run `generate_enhanced_enemy_scripts.py`
4. Run `regenerate_move_orders.py`

### For Genetic Algorithm
- ✅ Ready to use
- 123 encounters with realistic AI
- No data compatibility issues
- Proper cooldown management

## Summary

**Working Solution:** Enhanced AI system based on reverse-engineering 182K player battles  
**Data Source:** `enhanced_enemy_npc_scripts.json` + `npc_move_orders.json`  
**Integration:** Complete and tested  
**Coverage:** 123 encounters (44% of total)  

The enhanced AI approach is superior to trying to patch incompatible databases, as it's based on actual battle data rather than theoretical species mappings.
