import json, argparse, pathlib, re, sys

def read_text(p: pathlib.Path) -> str:
  return p.read_text(encoding="utf-8") if p.exists() else ""

def find_spec_keys_in_registry(registry_path: pathlib.Path):
  """
  Reads db/SpecRegistry.lua and extracts meta.key="CLASS_SPECID" values.
  """
  txt = read_text(registry_path)
  # Looks for key = "CLASS_SPECID"
  keys = re.findall(r'key\s*=\s*"([^"]+)"', txt)
  return sorted(set(keys))

def lua_has_table_key(lua_text: str, key: str) -> bool:
  # rough but effective: look for e.g. 'procs =' or 'resources ='
  return re.search(rf"\b{re.escape(key)}\s*=\s*{{", lua_text) is not None

def lua_has_spell_role(lua_text: str) -> bool:
  # looks for resources.spells entries with role="spender"
  return re.search(r'resources\s*=\s*{[^}]*spells\s*=\s*{[\s\S]*role\s*=\s*"spender"', lua_text) is not None

def load_sequences(sequences_root: pathlib.Path):
  """
  Detects whether specKey appears in any sequences file.
  """
  hits = set()
  if not sequences_root.exists():
    return hits
  for p in sequences_root.rglob("*.lua"):
    txt = read_text(p)
    # common pattern: ["MAGE_63"] = ...
    for k in re.findall(r'\[\s*"([^"]+)"\s*\]\s*=', txt):
      hits.add(k)
    # common pattern: data["MAGE_63"] = ...
    for k in re.findall(r'data\[\s*"([^"]+)"\s*\]\s*=', txt):
      hits.add(k)
  return hits

def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--repo", default=".", help="repo root")
  ap.add_argument("--fail-on-missing", action="store_true")
  ap.add_argument("--require-spender", action="store_true", help="require at least one spender tag in policy")
  ap.add_argument("--require-safe", action="store_true", help="require Safe variant in sequences (best-effort heuristic)")
  args = ap.parse_args()

  root = pathlib.Path(args.repo)

  registry = root / "db" / "SpecRegistry.lua"
  keys = find_spec_keys_in_registry(registry)
  if not keys:
    print("ERROR: could not find spec keys in db/SpecRegistry.lua")
    return 2

  pol_dir = root / "policies" / "spec"
  sequences_dir = root / "sequences"

  seq_hits = load_sequences(sequences_dir)

  missing = []
  warn = []

  for specKey in keys:
    gen = pol_dir / f"{specKey}.gen.lua"
    manual = pol_dir / f"{specKey}.manual.lua"

    gen_txt = read_text(gen)
    manual_txt = read_text(manual)

    # minimum: at least one policy file exists
    if not gen_txt and not manual_txt:
      missing.append((specKey, "no policy pack (missing .gen.lua and .manual.lua)"))
      continue

    # spender check
    if args.require_spender:
      if not (lua_has_spell_role(gen_txt) or lua_has_spell_role(manual_txt)):
        warn.append((specKey, "no resources.spells role='spender' found"))

    # sequences presence
    if specKey not in seq_hits:
      warn.append((specKey, "no sequences file reference found under /sequences"))

    # safe variant check
    if args.require_safe:
      safe_found = False
      for p in sequences_dir.rglob("*.lua"):
        txt = read_text(p)
        if specKey in txt and re.search(r'\bSafe\b', txt):
          safe_found = True
          break
      if not safe_found:
        warn.append((specKey, "Safe variant not detected (heuristic)"))

  print(f"Spec keys found: {len(keys)}")
  print(f"Missing (hard): {len(missing)}")
  print(f"Warnings: {len(warn)}")

  if missing:
    print("\nHARD MISSING:")
    for k, reason in missing:
      print(f"  {k}: {reason}")

  if warn:
    print("\nWARN:")
    for k, reason in warn:
      print(f"  {k}: {reason}")

  if args.fail_on_missing and missing:
    return 1
  return 0

if __name__ == "__main__":
  sys.exit(main())
