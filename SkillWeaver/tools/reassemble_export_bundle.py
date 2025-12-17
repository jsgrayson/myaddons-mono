import re, sys, json
from pathlib import Path

ROT_RE = re.compile(r"^SWROT_CHUNK\|(\d+)\/(\d+)\|(.*)$")
SPELL_RE = re.compile(r"^SWSPELL2_CHUNK\|(\d+)\/(\d+)\|(.*)$")

def reassemble(lines, rx, label):
    chunks = {}
    total = None
    for line in lines:
        m = rx.match(line.rstrip("\n"))
        if not m:
            continue
        i = int(m.group(1))
        total = int(m.group(2))
        chunks[i] = m.group(3)

    if total is None:
        return None

    missing = [i for i in range(1, total + 1) if i not in chunks]
    if missing:
        raise SystemExit(f"{label}: missing chunks: {missing[:10]}{'...' if len(missing)>10 else ''}")

    raw = "".join(chunks[i] for i in range(1, total + 1))
    return json.loads(raw)

def main(in_path, out_rot, out_spell):
    try:
        lines = Path(in_path).read_text(encoding="utf-8", errors="ignore").splitlines(True)
    except Exception as e:
        print(f"Error reading {in_path}: {e}")
        return

    rot = reassemble(lines, ROT_RE, "rotations")
    sp  = reassemble(lines, SPELL_RE, "spellbook")

    if rot is None:
        print("No SWROT_CHUNK found; rotations.json not written.")
    else:
        try:
            Path(out_rot).write_text(json.dumps(rot, indent=2), encoding="utf-8")
            print("wrote", out_rot, "specs:", len(rot))
        except Exception as e:
            print(f"Error writing {out_rot}: {e}")

    if sp is None:
        print("No SWSPELL2_CHUNK found; spellbook.json not written.")
    else:
        # v2 format is { "__meta":..., "spells":{...} }
        nspells = len(sp.get("spells", {})) if isinstance(sp, dict) else 0
        try:
            Path(out_spell).write_text(json.dumps(sp, indent=2), encoding="utf-8")
            print("wrote", out_spell, "spells:", nspells)
        except Exception as e:
            print(f"Error writing {out_spell}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python tools/reassemble_export_bundle.py <export.txt> [rotations.json] [spellbook.json]")
        sys.exit(1)

    in_path = sys.argv[1]
    out_rot = sys.argv[2] if len(sys.argv) > 2 else "rotations.json"
    out_sp  = sys.argv[3] if len(sys.argv) > 3 else "spellbook.json"
    main(in_path, out_rot, out_sp)
