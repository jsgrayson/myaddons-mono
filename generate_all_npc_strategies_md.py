# generate_all_npc_strategies_md.py
"""
Generate a markdown file that lists **every** trainer (NPC) from the Xufu‑scraped
strategies (`my_ready_strategies.json`) together with **all** of its strategy
scripts.

The JSON structure is:
{
  "Expansion Name": {
    "World Quests": [
      {
        "encounter_name": "<NPC name>",
        "url": "...",
        "strategies": [
          {
            "name": "Default Strategy",
            "pet_slots": [...],
            "script": "...\r\n...",
            "status": "READY"
          },
          ... (possible additional strategies)
        ]
      },
      ...
    ]
  },
  ...
}

The script walks the JSON, writes a markdown file `npc_all_strategies.md` with:

## <NPC name>
**URL:** <url>
### Strategy: <strategy name>
```text
<script>
```

If an NPC has multiple strategies they are listed sequentially.
"""
import json
from pathlib import Path

INPUT_JSON = Path(__file__).resolve().parent / "strategies_enhanced.json"
OUTPUT_MD = Path(__file__).resolve().parent / "npc_all_strategies.md"

def load_strategies():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_markdown(data):
    lines = ["# All NPC Strategies (Xufu Scrape)\n\n"]
    for expansion, expansion_content in data.items():
        lines.append(f"## {expansion}\n\n")
        if isinstance(expansion_content, dict):
            for category, encounters in expansion_content.items():
                lines.append(f"### {category}\n\n")
                if isinstance(encounters, list):
                    for encounter in encounters:
                        name = encounter.get("encounter_name", "Unknown")
                        url = encounter.get("url", "")
                        lines.append(f"#### {name}\n")
                        if url:
                            lines.append(f"**URL:** [{url}]({url})\n\n")
                        strategies = encounter.get("strategies", [])
                        for strat in strategies:
                            strat_name = strat.get("name", "Strategy")
                            script = strat.get("script", "")
                            # Normalise line endings
                            script = script.replace("\\r\\n", "\n").replace("\\r", "\n")
                            lines.append(f"##### Strategy: {strat_name}\n")
                            lines.append("```text\n")
                            lines.append(f"{script}\n")
                            lines.append("```\n\n")
    return "".join(lines)

def main():
    data = load_strategies()
    md = generate_markdown(data)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ Generated {OUTPUT_MD} with strategies for all NPCs.")

if __name__ == "__main__":
    main()
