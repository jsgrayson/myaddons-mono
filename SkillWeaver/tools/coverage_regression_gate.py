# tools/coverage_regression_gate.py
import argparse, pathlib, re, sys

LINE = re.compile(r"^- `([^`]+)`: (\d+) → \*\*(\d+)\*\*")

def parse_regressions(md_path: pathlib.Path):
  txt = md_path.read_text(encoding="utf-8")
  in_regressed = False
  out = []
  for line in txt.splitlines():
    if line.strip() == "## Regressed":
      in_regressed = True
      continue
    if line.startswith("## ") and line.strip() != "## Regressed":
      in_regressed = False
    if in_regressed:
      m = LINE.match(line.strip())
      if m:
        spec = m.group(1)
        base = int(m.group(2))
        head = int(m.group(3))
        out.append((spec, base, head))
  return out

def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--diff", default="coverage_diff.md")
  ap.add_argument("--max-drop", type=int, default=1, help="fail if any spec drops by more than this")
  args = ap.parse_args()

  path = pathlib.Path(args.diff)
  if not path.exists():
      print(f"Diff file not found: {path}")
      return 0

  regressions = parse_regressions(path)
  bad = []
  for spec, base, head in regressions:
    drop = base - head
    if drop > args.max_drop:
      bad.append((spec, base, head, drop))

  if bad:
    print("Policy coverage regression gate FAILED:")
    for spec, base, head, drop in sorted(bad, key=lambda x: (-x[3], x[0])):
      print(f"  {spec}: {base} -> {head}  (drop {drop})")
    return 1

  print("Policy coverage regression gate OK.")
  return 0

if __name__ == "__main__":
  sys.exit(main())
