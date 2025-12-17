import argparse, json, pathlib, re
from collections import defaultdict

SPEC_RE = re.compile(r'key\s*=\s*"([^"]+)"')
SPENDER_RE = re.compile(r'resources\s*=\s*{[\s\S]*spells\s*=\s*{[\s\S]*role\s*=\s*"spender"')
PROCS_RE = re.compile(r'\bprocs\s*=\s*{[\s\S]*\["')
CDSYNC_RE = re.compile(r'\bcooldownSync\s*=\s*{[\s\S]*\["')
CHARGES_RE = re.compile(r'\bcharges\s*=\s*{[\s\S]*\["')

def read(p: pathlib.Path) -> str:
  return p.read_text(encoding="utf-8") if p.exists() else ""

def score_policy_text(txt: str) -> int:
  if not txt.strip(): return 0
  s = 1
  if SPENDER_RE.search(txt): s += 1
  if PROCS_RE.search(txt): s += 1
  if CDSYNC_RE.search(txt): s += 1
  if CHARGES_RE.search(txt): s += 1
  return s

def load_rotations(path: pathlib.Path):
  if not path.exists(): return {}
  data = json.loads(path.read_text(encoding="utf-8"))
  out = {}
  for r in data:
    out[r["specKey"]] = {
      "spells": r.get("rotationSpells", []),
      "tokens": r.get("resourceTokens", []),
    }
  return out

def load_spellbook_v2(path: pathlib.Path):
  if not path.exists(): return {}
  raw = json.loads(path.read_text(encoding="utf-8"))
  if isinstance(raw, dict) and "spells" in raw:
    return raw["spells"]
  # fallback: plain dict
  return raw if isinstance(raw, dict) else {}

def candidate_spenders(spells, spellbook):
  # heuristic: prefer spells with powerCost present OR "finisher-ish" names
  finisher_words = ("Strike", "Shot", "Blast", "Bolt", "Execute", "Eviscerate", "Envenom",
                    "Chaos Strike", "Templar", "Judgment", "Starsurge", "Lava Burst",
                    "Death Coil", "Frost Strike", "Pyroblast")
  cand = []
  for s in spells:
    meta = spellbook.get(s, {})
    pc = meta.get("powerCost")
    charges = meta.get("charges")
    cd = meta.get("cooldown") or 0
    score = 0
    if isinstance(pc, list) and pc: score += 3
    if any(w.lower() in s.lower() for w in finisher_words): score += 2
    if cd and cd <= 15: score += 1
    if charges and charges > 1: score -= 1  # often builders/utility
    cand.append((score, s))
  cand.sort(reverse=True)
  return [s for sc, s in cand if sc > 0][:6]

def candidate_charge_spells(spells, spellbook):
  cand = []
  for s in spells:
    meta = spellbook.get(s, {})
    ch = meta.get("charges") or 0
    if ch and ch > 1:
      cd = meta.get("cooldown") or 0
      cand.append((ch, cd, s))
  cand.sort(key=lambda x: (-x[0], -x[1], x[2]))
  return [s for _,_,s in cand][:6]

def candidate_burst_leaders(spells, spellbook):
  # heuristic: long cooldowns used in rotation
  cand = []
  for s in spells:
    meta = spellbook.get(s, {})
    cd = meta.get("cooldown") or 0
    if cd >= 45:
      cand.append((cd, s))
  cand.sort(reverse=True)
  return [s for _, s in cand][:4]

def candidate_partners(spells, spellbook, leader):
  # partners: other CDs 20s+ excluding leader
  cand = []
  for s in spells:
    if s == leader: continue
    cd = (spellbook.get(s, {}) or {}).get("cooldown") or 0
    if cd >= 20:
      cand.append((cd, s))
  cand.sort(reverse=True)
  return [s for _, s in cand][:4]

def candidate_procs(spells, spellbook):
  # v2 exporter: procHints on spells
  proc_to_spells = defaultdict(set)
  for s in spells:
    meta = spellbook.get(s, {})
    for p in meta.get("procHints", []) or []:
      proc_to_spells[p].add(s)
  # pick top procs with 1-3 consumers
  out = []
  for proc, consumers in proc_to_spells.items():
    c = sorted(consumers)
    if 1 <= len(c) <= 4:
      out.append((len(c), proc, c))
  out.sort(key=lambda x: (x[0], x[1]))
  return out[:6]

def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--rotations", default="rotations.json")
  ap.add_argument("--spellbook", default="spellbook.json")
  ap.add_argument("--min-score", type=int, default=3)
  ap.add_argument("--limit", type=int, default=50)
  args = ap.parse_args()

  root = pathlib.Path(".")
  pol_dir = root / "policies" / "spec"

  reg = read(root / "db" / "SpecRegistry.lua")
  spec_keys = sorted(set(SPEC_RE.findall(reg)))

  rotations = load_rotations(pathlib.Path(args.rotations))
  spellbook = load_spellbook_v2(pathlib.Path(args.spellbook))

  failures = []

  for specKey in spec_keys:
    gen = read(pol_dir / f"{specKey}.gen.lua")
    man = read(pol_dir / f"{specKey}.manual.lua")
    txt = (gen + "\n" + man).strip()
    s = score_policy_text(txt)

    if s < args.min_score:
      failures.append((specKey, s))

  failures.sort(key=lambda x: (x[1], x[0]))
  failures = failures[:args.limit]

  print(f"Spec checklist (min-score {args.min_score}/5). Showing {len(failures)} specs.\n")

  for specKey, s in failures:
    r = rotations.get(specKey, {})
    spells = r.get("spells", [])
    txt = (read(pol_dir / f"{specKey}.gen.lua") + "\n" + read(pol_dir / f"{specKey}.manual.lua"))

    print(f"## {specKey}  ({s}/5)")

    if not (pol_dir / f"{specKey}.gen.lua").exists() and not (pol_dir / f"{specKey}.manual.lua").exists():
      print("- [ ] Create policy pack (gen or manual)\n")

    if not SPENDER_RE.search(txt):
      spenders = candidate_spenders(spells, spellbook)
      print("- [ ] Add at least 1 spender tag under `resources.spells`")
      if spenders:
        print(f"  - Suggested spenders: {', '.join(spenders)}")
      else:
        print("  - Suggested spenders: (need spelldump)")

    if not CHARGES_RE.search(txt):
      charges = candidate_charge_spells(spells, spellbook)
      print("- [ ] Add `charges` entries (if applicable)")
      if charges:
        print(f"  - Charge candidates: {', '.join(charges)}")
      else:
        print("  - Charge candidates: none detected")

    if not CDSYNC_RE.search(txt):
      leaders = candidate_burst_leaders(spells, spellbook)
      print("- [ ] Add `cooldownSync` leader + partners")
      if leaders:
        leader = leaders[0]
        partners = candidate_partners(spells, spellbook, leader)
        print(f"  - Suggested leader: {leader}")
        if partners:
          print(f"  - Suggested partners: {', '.join(partners)}")
      else:
        print("  - Suggested leader: none detected")

    if not PROCS_RE.search(txt):
      procs = candidate_procs(spells, spellbook)
      print("- [ ] Add `procs` rules (prefer/avoid)")
      if procs:
        for _, proc, consumers in procs:
          print(f"  - Proc `{proc}` → prefer: {', '.join(consumers)}")
      else:
        print("  - Proc hints: none detected")

    print("")  # spacer

if __name__ == "__main__":
  main()
