import argparse, json, pathlib, re
from collections import defaultdict

CAST_RE = re.compile(r'/cast\s+([^\n\r;]+)')

def clean_spell(s: str) -> str:
    s = s.strip()
    # strip macro conditionals like [@focus] or [pet]
    s = re.sub(r'^\[[^\]]*\]\s*', '', s).strip()
    # strip rank parentheses etc.
    s = re.sub(r'\s*\(.*?\)\s*$', '', s).strip()
    return s

def infer_resource_tokens(spec_key: str):
    # Heuristic mapping based on class prefix in specKey
    if spec_key.startswith("DEATHKNIGHT_"):
        return ["RUNIC_POWER"]
    if spec_key.startswith("DEMONHUNTER_"):
        return ["FURY"]
    if spec_key.startswith("DRUID_"):
        return ["MANA", "ENERGY", "RAGE", "COMBO_POINTS", "ASTRAL_POWER"]
    if spec_key.startswith("EVOKER_"):
        return ["MANA", "ESSENCE"]
    if spec_key.startswith("HUNTER_"):
        return ["FOCUS"]
    if spec_key.startswith("MAGE_"):
        return ["MANA", "ARCANE_CHARGES"]
    if spec_key.startswith("MONK_"):
        return ["ENERGY", "CHI", "MANA"]
    if spec_key.startswith("PALADIN_"):
        return ["MANA", "HOLY_POWER"]
    if spec_key.startswith("PRIEST_"):
        return ["MANA", "INSANITY"]
    if spec_key.startswith("ROGUE_"):
        return ["ENERGY", "COMBO_POINTS"]
    if spec_key.startswith("SHAMAN_"):
        return ["MANA", "MAELSTROM"]
    if spec_key.startswith("WARLOCK_"):
        return ["MANA", "SOUL_SHARDS"]
    if spec_key.startswith("WARRIOR_"):
        return ["RAGE"]
    return ["MANA"]

def extract_spec_blocks(lua_text: str):
    """
    Returns dict specKey -> list of spell names found in /cast lines
    Supports:
      data["SPEC"] = { ... }
      data["SPEC"] = ... (multi-line)
      ["SPEC"] = { ... } (inside return table)
    """
    out = defaultdict(list)

    # pattern 1: data["SPEC"] = { ... }
    spec_assign = re.finditer(r'data\[\s*"([^"]+)"\s*\]\s*=\s*{', lua_text)
    for m in spec_assign:
        spec = m.group(1)
        start = m.end()
        # take a conservative chunk until the next 'data["' or end of file
        nxt = lua_text.find('data["', start)
        chunk = lua_text[start:nxt] if nxt != -1 else lua_text[start:]
        for cm in CAST_RE.finditer(chunk):
            spell = clean_spell(cm.group(1))
            if spell and spell not in out[spec]:
                out[spec].append(spell)

    # pattern 2: ["SPEC"] = { ... } inside a return table
    spec_key_assign = re.finditer(r'\[\s*"([^"]+)"\s*\]\s*=\s*{', lua_text)
    for m in spec_key_assign:
        spec = m.group(1)
        if "_" not in spec: continue
        start = m.end()
        # find matching brace or next key roughly
        nxt = lua_text.find('["', start)
        chunk = lua_text[start:nxt] if nxt != -1 else lua_text[start:]
        for cm in CAST_RE.finditer(chunk):
            spell = clean_spell(cm.group(1))
            if spell and spell not in out[spec]:
                out[spec].append(spell)

    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sequences", default="sequences", help="directory containing lua sequences")
    ap.add_argument("--out", default="rotations.json", help="output json file")
    args = ap.parse_args()

    root = pathlib.Path(args.sequences)
    if not root.exists():
        print(f"Warning: missing sequences dir: {root}")
        return

    spells_by_spec = defaultdict(list)

    for p in root.rglob("*.lua"):
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
            found = extract_spec_blocks(txt)
            for spec, spells in found.items():
                for s in spells:
                    if s not in spells_by_spec[spec]:
                        spells_by_spec[spec].append(s)
        except Exception as e:
            print(f"Error reading {p}: {e}")

    rotations = []
    for spec, spells in sorted(spells_by_spec.items()):
        rotations.append({
            "specKey": spec,
            "rotationSpells": spells,
            "resourceTokens": infer_resource_tokens(spec),
        })

    try:
        pathlib.Path(args.out).write_text(json.dumps(rotations, indent=2), encoding="utf-8")
        print(f"wrote {args.out} with {len(rotations)} specs")
    except Exception as e:
        print(f"Error writing output: {e}")

if __name__ == "__main__":
    main()
