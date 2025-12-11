# PetWeaver - Breed Optimization & Strategy Scraping

## Quick Start

### Testing the Genetic Algorithm
```bash
cd /Users/jgrayson/Documents/petweaver
python3 run_test_genetic.py
```

**Expected Output:**
```
Loading Data...
Target: Major Payne (3 Epic Pets)
Initializing Population (Smart Draft + Seeds)...
    [AI] Building optimized counter pools...
    [AI] Seeding population with 1 known strategies...

Starting UNLIMITED Evolution (Press Ctrl+C to stop)...

Gen 1: 2208 (LLL) | Team: ['Silver Tabby Cat', 'Hoplet', 'Wharf Rat']
Gen 10: 2445 (LLL) | Team: ['Sanctum Cub', 'Ironbound Proto-Whelp', 'Weebomination']
...
```

### Features Implemented

✅ **Breed Optimization** - GA evolves both species AND breeds (B/B, P/P, S/S, etc.)
✅ **Monte Carlo Validator** - 1000+ battle simulations for team stability testing  
✅ **Strategy Scraper** - Extract winning teams from Xu-Fu for GA seeding
✅ **Breed-Based Stats** - Accurate stat calculations with breed modifiers

### Testing Individual Components

**Test Breed System:**
```bash
python3 -c "from genetic.genome import PetGene; print(PetGene.get_available_breeds(1155, None))"
# Output: [3, 4, 5, 6]  (B/B, P/P, S/S, H/H)
```

**Test Monte Carlo Validator:**
```python
from genetic.validator import MonteCarloValidator
from genetic.fitness import FitnessEvaluator

# After running GA:
validator = MonteCarloValidator(evaluator)
report = validator.validate_team(best_genome, num_simulations=1000)
print(report.summary())
```

**Scrape Xu-Fu Strategies:**
```bash
python3 run_full_scrape.py  # Takes 30-60 min
```

### Files Modified

- `genetic/genome.py` - Breed mutations
- `genetic/fitness.py` - Breed stat calculations  
- `genetic/evolution.py` - Strategy file loading
- `genetic/validator.py` (NEW) - Monte Carlo validation
- `breed_stats.json` (NEW) - Breed definitions
- `scrape_xufu_enhanced.py` - Seed extraction
- `simulator/simulator.py` - Disabled DEBUG logging

### Known Issues

None! System is fully operational.

### Next Steps

1. Add web UI for real-time progress
2. Implement speed tier optimization  
3. Create team comparison dashboard
4. Build batch encounter solver
