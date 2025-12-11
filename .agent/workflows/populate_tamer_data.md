---
description: Process to populate Tamer Pet Data (Abilities/Stats) for a new expansion
---

# Tamer Data Population Workflow

This workflow describes how to generate a comprehensive `encounters_full.json` file containing all Tamer data, including abilities for NPC-only pets which are not available via the Blizzard API.

## Prerequisites
- `pettracker_tamers.json`: Lua export of Tamer data (Name, Team, Pet IDs).
- `pettracker_decoded.json`: Decoded PetTracker data.
- `.env`: Must contain `BLIZZARD_CLIENT_ID` and `BLIZZARD_CLIENT_SECRET`.
- `abilities.json`: Database of ability ID -> Name/Details.

## Step 1: Generate Base Data
Run the generation script to create the initial `encounters_full.json`. This merges the raw Tamer data with decoded stats and fetches ability data for **Player-Collectable Pets** from the Blizzard API.

```bash
python3 generate_full_tamer_encounters.py
```

## Step 2: Scrape NPC Abilities
Many Tamer pets are NPC-only versions (unique Species IDs) and won't be found in the Blizzard API. Use the Wowhead scraper to fetch their abilities by Species ID.

```bash
# This script loads tamers from encounters_full.json and scrapes missing data
python3 scrape_wowhead_final.py
```
*Note: This process takes 10-15 minutes for ~150 tamers.*

## Step 3: Merge Scraped Data
Integrate the scraped CSV data (`wow_tamer_abilities_final.csv`) into the main JSON file.

```bash
python3 merge_scraped_abilities.py
```

## Step 4: Verify Coverage
Generate a report to see if any pets are still missing abilities.

```bash
python3 report_missing_pets.py
```

## Step 5: Fallback (Optional)
If gaps remain (e.g., pets not on Wowhead), use the Model Matcher to infer abilities from Player Pets that share the same 3D model.

```bash
python3 map_models_to_abilities.py
```

## Final Output
The result is a fully populated `encounters_full.json` ready for use in the Genetic Algorithm.
