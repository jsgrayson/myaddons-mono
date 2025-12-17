# tools/coverage_diff.py
import re, pathlib
from collections import defaultdict

SPEC_RE = re.compile(r'key\s*=\s*"([^"]+)"')
SPENDER_RE = re.compile(r'resources\s*=\s*{[\s\S]*spells\s*=\s*{[\s\S]*role\s*=\s*"spender"')
PROCS_RE = re.compile(r'\bprocs\s*=\s*{[\s\S]*\["')
CDSYNC_RE = re.compile(r'\bcooldownSync\s*=\s*{[\s\S]*\["')
CHARGES_RE = re.compile(r'\bcharges\s*=\s*{[\s\S]*\["')

def read(p: pathlib.Path) -> str:
  return p.read_text(encoding="utf-8") if p.exists() else ""

def spec_keys(repo: pathlib.Path):
  reg = read(repo / "db" / "SpecRegistry.lua")
  return sorted(set(SPEC_RE.findall(reg)))

def score_spec(repo: pathlib.Path, spec_key: str):
  pol_dir = repo / "policies" / "spec"
  gen = read(pol_dir / f"{spec_key}.gen.lua")
  man = read(pol_dir / f"{spec_key}.manual.lua")
  txt = gen + "\n" + man

  score = 0
  reasons = []

  if gen.strip() or man.strip():
    score += 1
  else:
    return 0, ["no policy"]

  if SPENDER_RE.search(txt): score += 1
  else: reasons.append("no spender tags")

  if PROCS_RE.search(txt): score += 1
  else: reasons.append("no procs")

  if CDSYNC_RE.search(txt): score += 1
  else: reasons.append("no cooldownSync")

  if CHARGES_RE.search(txt): score += 1
  else: reasons.append("no charges")

  return score, reasons

def score_map(repo: pathlib.Path):
  m = {}
  for k in spec_keys(repo):
    m[k] = score_spec(repo, k)[0]
  return m

def main():
  import argparse
  ap = argparse.ArgumentParser()
  ap.add_argument("--base", required=True, help="path to base checkout")
  ap.add_argument("--head", required=True, help="path to head checkout")
  ap.add_argument("--out", default="coverage_diff.md")
  args = ap.parse_args()

  base = pathlib.Path(args.base)
  head = pathlib.Path(args.head)

  # If base doesn't exist (e.g. first run), assume empty
  if not base.exists():
      print("Base path not found, assuming empty baseline.")
      b = {}
  else:
      b = score_map(base)
      
  # Inspect head
  h = score_map(head)

  all_keys = sorted(set(b.keys()) | set(h.keys()))
  improved = []
  regressed = []
  unchanged = 0

  for k in all_keys:
    bs = b.get(k, 0)
    hs = h.get(k, 0)
    if hs > bs: improved.append((k, bs, hs))
    elif hs < bs: regressed.append((k, bs, hs))
    else: unchanged += 1

  improved.sort(key=lambda x: (x[1]-x[2], x[0]))
  regressed.sort(key=lambda x: (x[2]-x[1], x[0]))

  lines = []
  lines.append("# SkillWeaver Policy Coverage Diff\n")
  lines.append(f"- Improved: **{len(improved)}**")
  lines.append(f"- Regressed: **{len(regressed)}**")
  lines.append(f"- Unchanged: **{unchanged}**\n")

  def fmt_list(title, items, limit=40):
    if not items:
      lines.append(f"## {title}\n\n_None._\n")
      return
    lines.append(f"## {title}\n")
    for i, (k, bs, hs) in enumerate(items[:limit], 1):
      lines.append(f"- `{k}`: {bs} → **{hs}**")
    if len(items) > limit:
      lines.append(f"\n… and {len(items)-limit} more.\n")
    else:
      lines.append("")

  fmt_list("Improved", improved)
  fmt_list("Regressed", regressed)

  pathlib.Path(args.out).write_text("\n".join(lines), encoding="utf-8")
  print("wrote", args.out)

if __name__ == "__main__":
  main()
