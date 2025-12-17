# tools/coverage_min_gate.py
import argparse, pathlib, re, sys

SPEC_RE = re.compile(r'key\s*=\s*"([^"]+)"')
SPENDER_RE = re.compile(r'resources\s*=\s*{[\s\S]*spells\s*=\s*{[\s\S]*role\s*=\s*"spender"')
PROCS_RE = re.compile(r'\bprocs\s*=\s*{[\s\S]*\["')
CDSYNC_RE = re.compile(r'\bcooldownSync\s*=\s*{[\s\S]*\["')
CHARGES_RE = re.compile(r'\bcharges\s*=\s*{[\s\S]*\["')

def read(p): return p.read_text(encoding="utf-8") if p.exists() else ""

def score(txt: str) -> int:
  if not txt.strip(): return 0
  s = 1
  if SPENDER_RE.search(txt): s += 1
  if PROCS_RE.search(txt): s += 1
  if CDSYNC_RE.search(txt): s += 1
  if CHARGES_RE.search(txt): s += 1
  return s

def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--min-score", type=int, default=2)
  ap.add_argument("--limit", type=int, default=30, help="max failing specs to print")
  args = ap.parse_args()

  root = pathlib.Path(".")
  reg_path = root / "db" / "SpecRegistry.lua"
  
  if not reg_path.exists():
      print(f"SpecRegistry not found at {reg_path}")
      return 0 # Or fail? For now, 0.

  reg = read(reg_path)
  keys = sorted(set(SPEC_RE.findall(reg)))

  pol_dir = root / "policies" / "spec"
  failing = []

  for k in keys:
    gen = read(pol_dir / f"{k}.gen.lua")
    man = read(pol_dir / f"{k}.manual.lua")
    s = score((gen + "\n" + man).strip())
    if s < args.min_score:
      failing.append((k, s))

  if failing:
    failing.sort(key=lambda x: (x[1], x[0]))
    print(f"FAIL: {len(failing)} specs below min score {args.min_score}/5")
    for k, s in failing[:args.limit]:
      print(f"  {k}: {s}/5")
    if len(failing) > args.limit:
      print(f"  …and {len(failing)-args.limit} more")
    return 1

  print(f"OK: all specs >= {args.min_score}/5")
  return 0

if __name__ == "__main__":
  sys.exit(main())
