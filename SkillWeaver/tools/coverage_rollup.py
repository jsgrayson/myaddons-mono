# tools/coverage_rollup.py
import pathlib, re
from collections import defaultdict

SPEC_RE = re.compile(r'key\s*=\s*"([^"]+)"')
SPENDER_RE = re.compile(r'resources\s*=\s*{[\s\S]*spells\s*=\s*{[\s\S]*role\s*=\s*"spender"')
PROCS_RE = re.compile(r'\bprocs\s*=\s*{[\s\S]*\["')
CDSYNC_RE = re.compile(r'\bcooldownSync\s*=\s*{[\s\S]*\["')
CHARGES_RE = re.compile(r'\bcharges\s*=\s*{[\s\S]*\["')

def read(p): return p.read_text(encoding="utf-8") if p.exists() else ""

def score_policy_text(txt: str) -> int:
  score = 0
  if txt.strip(): score += 1  # policy exists (gen or manual)
  if SPENDER_RE.search(txt): score += 1
  if PROCS_RE.search(txt): score += 1
  if CDSYNC_RE.search(txt): score += 1
  if CHARGES_RE.search(txt): score += 1
  return score

def main():
  root = pathlib.Path(".")
  reg = read(root / "db" / "SpecRegistry.lua")
  keys = sorted(set(SPEC_RE.findall(reg)))

  pol_dir = root / "policies" / "spec"
  by_class = defaultdict(list)
  by_spec = {}

  for k in keys:
    cls = k.split("_", 1)[0] if "_" in k else "UNKNOWN"
    gen = read(pol_dir / f"{k}.gen.lua")
    man = read(pol_dir / f"{k}.manual.lua")
    txt = (gen + "\n" + man).strip()
    s = score_policy_text(txt)
    by_class[cls].append(s)
    by_spec[k] = s

  all_scores = list(by_spec.values())
  if not all_scores:
      print("No specs found.")
      return

  avg = sum(all_scores) / len(all_scores)
  print(f"Global avg: {avg:.2f} / 5 over {len(all_scores)} specs\n")

  print("Per-class avg:")
  for cls in sorted(by_class.keys()):
    scores = by_class[cls]
    print(f"  {cls:12}  avg {sum(scores)/len(scores):.2f}  min {min(scores)}  max {max(scores)}  n={len(scores)}")

  print("\nBottom specs:")
  bottom = sorted(by_spec.items(), key=lambda kv: (kv[1], kv[0]))[:20]
  for k, s in bottom:
    if s < 5:
        print(f"  {k}: {s}/5")

if __name__ == "__main__":
  main()
