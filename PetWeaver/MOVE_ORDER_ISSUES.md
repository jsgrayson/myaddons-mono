# Final Analysis: Move Order Data Sources

## All Attempts to Fix encounters.json FAILED

### Attempt 1: Hydration from abilities.json
**Result:** ❌ Species ID mismatch (0 pets hydrated)

### Attempt 2: Rebuild from wow_tamer_abilities.csv  
**Result:** ❌ CSV has placeholder data
- All 57 encounters generated
- **ALL pets have identical abilities:** Crush, Stoneskin, Haymaker
- CSV is template data, not real NPC abilities

### Attempt 3: Generate from strategies (encounters.json + abilities.json)
**Result:** ❌ encounters.json has empty abilities arrays (0 moves generated)

## Root Cause
**No valid source data exists for NPC abilities** except the enhanced AI system.

## Only Working Solution
**`npc_move_orders_enhanced.json`** (123 encounters)
- Generated from analyzing 182,452 player battles
- Real, diverse abilities per encounter
- Known issue: Cooldown tracking bug causes some spam

## Data Quality Check Results

### wow_tamer_abilities.csv
```
Julia Stevens,872,Crush,Stoneskin,Haymaker,Body Slam,Takedown,Bandage
Julia Stevens,873,Crush,Stoneskin,Haymaker,Body Slam,Takedown,Bandage
Zunta,874,Crush,Stoneskin,Haymaker,Body Slam,Takedown,Bandage
```
**Every pet:** Same 6 abilities → **Template/placeholder data**

### encounters.json (original)
```json
{"species_id": 872, "abilities": []}
{"species_id": 873, "abilities": []}
```
**All pets:** Empty abilities array → **Incomplete export**

### enhanced_enemy_npc_scripts.json ✓
```
"Captain" Klutz: use(Black Claw:919) [round=1]
Ashlei: use(Immolate:178) [round=1]
```
**123 encounters:** Real abilities from battle analysis → **VALID**

## Recommendation
1. Accept enhanced AI data with cooldown bugs
2. OR fix `regenerate_move_orders.py` to properly track cooldowns
3. Don't attempt to use CSV or encounters.json - data is fundamentally flawed

## Validation Checklist for Future
- [ ] Check for duplicate ability sets across NPCs
- [ ] Verify unique abilities per encounter
- [ ] Sample multiple encounters before claiming success
- [ ] Cross-reference with known battles
