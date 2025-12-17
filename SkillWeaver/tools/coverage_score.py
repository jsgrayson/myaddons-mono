import pathlib, re
from collections import defaultdict

SPEC_RE = re.compile(r'key\s*=\s*"([^"]+)"')
SPENDER_RE = re.compile(r'resources\s*=\s*{[\s\S]*spells\s*=\s*{[\s\S]*role\s*=\s*"spender"')
PROCS_RE = re.compile(r'\bprocs\s*=\s*{[\s\S]*\["')
CDSYNC_RE = re.compile(r'\bcooldownSync\s*=\s*{[\s\S]*\["')
CHARGES_RE = re.compile(r'\bcharges\s*=\s*{[\s\S]*\["')

def read(p): return p.read_text(encoding="utf-8") if p.exists() else ""

def main():
  root = pathlib.Path(".")
  reg = read(root / "db" / "SpecRegistry.lua")
  spec_keys = sorted(set(SPEC_RE.findall(reg)))

  pol_dir = root / "policies" / "spec"

  rows = []
  for k in spec_keys:
    gen = read(pol_dir / f"{k}.gen.lua")
    man = read(pol_dir / f"{k}.manual.lua")
    txt = gen + "\n" + man

    score = 0
    reasons = []

    # 1) policy exists
    if gen.strip() or man.strip():
      score += 1
    else:
      reasons.append("no policy")
      rows.append((k, score, reasons))
      continue

    # 2) spender tagging
    if SPENDER_RE.search(txt):
      score += 1
    else:
      reasons.append("no spender")

    # 3) procs
    if PROCS_RE.search(txt):
      score += 1
    else:
      reasons.append("no procs")

    # 4) cooldown sync
    if CDSYNC_RE.search(txt):
      score += 1
    else:
      reasons.append("no cdSync")

    # 5) charges
    if CHARGES_RE.search(txt):
      score += 1
    else:
      reasons.append("no charges")

    rows.append((k, score, reasons))

  rows.sort(key=lambda x: (x[1], x[0]))

  # Print summary
  total = len(rows)
  by_score = defaultdict(int)
  for _, s, _ in rows: by_score[s] += 1

  print("Coverage score (0-5):")
  for s in range(0, 6):
    print(f"  {s}: {by_score[s]} specs")

  print("\nLowest scoring specs:")
  for k, s, reasons in rows[:25]:
    if s < 5:
        print(f"  {k}: {s}/5  ({', '.join(reasons)})")

if __name__ == "__main__":
  main()
