# tools/policy_autotag.py
import json
import sys
from collections import defaultdict

# How "strong" a proc hint is, per proc name.
PROC_CONF = {
    "Hot Streak": 0.90,
    "Brain Freeze": 0.85,
    "Clearcasting": 0.70,
    "Killing Machine": 0.90,
    "Rime": 0.85,
    "Sudden Doom": 0.85, 
    "Predatory Swiftness": 0.85,
    "Shooting Stars": 0.75,
}

def load_spellbook_v2(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        print(f"Error loading spellbook: {e}")
        return {}

    # v2 format: { "__meta": {...}, "spells": { "Pyroblast": {id,cooldown,charges,procHints...}, ... } }
    if isinstance(raw, dict) and "spells" in raw and isinstance(raw["spells"], dict):
        spells = raw["spells"]
        book = {}
        for name, meta in spells.items():
            book[name] = {
                "id": meta.get("id"),
                "cooldown": meta.get("cooldown") or 0,
                "charges": meta.get("charges") or 0,
                "known": meta.get("known"),
                "talent": meta.get("talent"),
                "procHints": meta.get("procHints") or [],
                "tags": meta.get("tags", {}),
                "category": meta.get("category"),
                "cost": meta.get("cost", {}),
                "gain": meta.get("gain", {}),
            }
        return book

    # legacy fallback
    if isinstance(raw, dict):
        return raw
    return {}

def is_burst_leader(spell_meta):
    cd = spell_meta.get("cooldown", 0)
    cat = spell_meta.get("category", "")
    if cd >= 45 and cat in ("offensive_cd", "burst", "major_cd"):
        return True
    
    # Just checking damage amp tag isn't enough without category if we rely on heuristic
    # But if V2 dump doesn't have categories (it doesn't yet), we rely on CD + known
    # If CD > 90s, it's likely a major
    if cd >= 90: return True
    return False

def is_partner_cd(spell_meta):
    cd = spell_meta.get("cooldown", 0)
    return 20 <= cd <= 60

def guess_spender(spell_meta, resource_tokens):
    # If we have costs
    costs = spell_meta.get("cost", {})
    for r in resource_tokens:
        if costs.get(r, 0) > 0: return True
    return False

def guess_builder(spell_meta, resource_tokens):
    gains = spell_meta.get("gain", {})
    for r in resource_tokens:
        if gains.get(r, 0) > 0: return True
    return False

def auto_charges(spell_meta):
    if spell_meta.get("charges", 0) and spell_meta["charges"] > 1:
        return { "spendAtOrAbove": 1, "aoeBonus": 0.3, "capUrgency": 2.0 }
    return None

def auto_cooldown_sync(leaders, partners):
    out = {}
    for L, Lm in leaders.items():
        Lcd = Lm.get("cooldown", 0)
        cand = []
        for P, Pm in partners.items():
            if P == L: continue
            Pcd = Pm.get("cooldown", 0)
            score = 0
            if Pcd > 0 and Lcd > 0:
                score += 10 - min(10, abs(Lcd - Pcd) / 10.0)
                if Lcd % Pcd == 0 or Pcd % Lcd == 0:
                    score += 3
            cand.append((score, P))
        cand.sort(reverse=True)
        partners_sel = [p for _, p in cand[:2]]
        out[L] = { "partners": partners_sel, "maxWait": 6.0, "minTTD": 12.0 }
    return out

def proc_confidence(proc_name: str) -> float:
    return PROC_CONF.get(proc_name, 0.55)

def add_proc_prefer(procs_out: dict, proc: str, spell: str, conf: float):
    entry = procs_out.setdefault(proc, {"prefer": [], "avoid": [], "_conf": {}})
    if spell not in entry["prefer"]:
        entry["prefer"].append(spell)
    entry["_conf"][spell] = max(entry["_conf"].get(spell, 0.0), conf)

def finalize_procs(procs_out: dict, min_conf: float = 0.80, max_spells_per_proc: int = 3) -> dict:
    final = {}
    for proc, entry in procs_out.items():
        confmap = entry.get("_conf", {})
        ranked = sorted(
            [(s, confmap.get(s, 0.0)) for s in entry.get("prefer", [])],
            key=lambda x: x[1],
            reverse=True
        )
        keep = [s for s,c in ranked if c >= min_conf][:max_spells_per_proc]
        avoid = entry.get("avoid", [])

        if keep or avoid:
            final[proc] = {"prefer": keep, "avoid": avoid}
    return final

def build_policy(spec_key, rotation_spells, spellbook, resource_tokens):
    resources = { "enablePooling": True, "targetPoolPct": 0.8, "dumpAtPct": 0.9, "spells": {} }
    charges = {}
    leaders = {}
    partners = {}
    procs_raw = {}

    for s in rotation_spells:
        meta = spellbook.get(s, {})
        
        # Resource roles (requires cost/gain data in V2 dump or manual enrichment)
        if guess_spender(meta, resource_tokens):
            resources["spells"][s] = { "role": "spender" }
        elif guess_builder(meta, resource_tokens):
            resources["spells"][s] = { "role": "builder" }

        # Charges
        ch = auto_charges(meta)
        if ch: charges[s] = ch

        # CDs
        if is_burst_leader(meta):
            leaders[s] = meta
        elif is_partner_cd(meta):
            partners[s] = meta

        # Procs
        for proc in meta.get("procHints", []):
            conf = proc_confidence(proc)
            add_proc_prefer(procs_raw, proc, s, conf)

    cooldown_sync = auto_cooldown_sync(leaders, partners) if leaders else {}
    procs = finalize_procs(procs_raw)

    return {
        "specKey": spec_key,
        "resources": resources,
        "charges": charges,
        "cooldownSync": cooldown_sync,
        "procs": procs, 
    }

def main():
    if len(sys.argv) < 3:
        print("Usage: python policy_autotag.py <rotations.json> <spellbook.json>")
        return

    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            rotations = json.load(f)
        spellbook = load_spellbook_v2(sys.argv[2])
    except Exception as e:
        print(f"Error reading input files: {e}")
        return

    out = []
    for r in rotations:
        spec_key = r.get("specKey")
        if not spec_key: continue
        pol = build_policy(spec_key, r.get("rotationSpells", []), spellbook, r.get("resourceTokens", []))
        out.append(pol)

    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
