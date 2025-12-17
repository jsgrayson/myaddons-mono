import json, os, pathlib, hashlib

def lua_str(s: str) -> str:
  return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'

def dump_list(xs):
  xs = xs or []
  return "{ " + ", ".join(lua_str(x) for x in xs) + " }"

def stable_items(d):
  return sorted((d or {}).items(), key=lambda kv: str(kv[0]).lower())

def normalize_procs(procs):
  if procs is None: return {}
  if isinstance(procs, dict):
    out = {}
    for k, v in procs.items():
      out[str(k)] = {
        "prefer": list(v.get("prefer", [])) if isinstance(v, dict) else [],
        "avoid": list(v.get("avoid", [])) if isinstance(v, dict) else [],
      }
    return out
  if isinstance(procs, list):
    out = {}
    for p in procs:
      if not isinstance(p, dict): continue
      name = p.get("name")
      if not name: continue
      out[str(name)] = {
        "prefer": list(p.get("prefer", [])),
        "avoid": list(p.get("avoid", [])),
      }
    return out
  return {}

def normalize_charges(charges):
  if charges is None: return {}
  if isinstance(charges, dict): return charges
  if isinstance(charges, list):
    out = {}
    for c in charges:
      if isinstance(c, dict) and c.get("spell"):
        out[str(c["spell"])] = c
    return out
  return {}

def normalize_cooldown_sync(cd):
  if cd is None: return {}
  if isinstance(cd, dict): return cd
  if isinstance(cd, list):
    out = {}
    for g in cd:
      if isinstance(g, dict) and g.get("leader"):
        out[str(g["leader"])] = {
          "partners": list(g.get("partners", [])),
          "maxWait": g.get("maxWait", 6.0),
          "minTTD": g.get("minTTD", 12.0),
        }
    return out
  return {}

def write_if_changed(path: pathlib.Path, content: str) -> bool:
  prev = path.read_text(encoding="utf-8") if path.exists() else None
  if prev == content:
    return False
  path.write_text(content, encoding="utf-8")
  return True

def to_lua_policy(spec_key: str, payload: dict) -> str:
  out = []
  out.append(f"-- AUTO-GENERATED from scraper for {spec_key}")
  out.append("local addonName, addonTable = ...")
  out.append("local pack = {")

  # resources
  res = payload.get("resources", {}) or {}
  out.append("  resources = {")
  for k, v in stable_items(res):
    if k == "spells" and isinstance(v, dict): continue
    if isinstance(v, bool):
      out.append(f"    {k} = {'true' if v else 'false'},")
    elif isinstance(v, (int, float)):
      out.append(f"    {k} = {v},")
    else:
      out.append(f"    {k} = {lua_str(v)},")
  # resources.spells map (stable)
  spells = res.get("spells", {}) if isinstance(res, dict) else {}
  if isinstance(spells, dict) and spells:
    out.append("    spells = {")
    for spell, meta in stable_items(spells):
      role = meta.get("role") if isinstance(meta, dict) else None
      if role:
        out.append(f"      [{lua_str(spell)}] = {{ role = {lua_str(role)} }},")
    out.append("    },")
  out.append("  },")

  # procs
  procs = normalize_procs(payload.get("procs"))
  out.append("  procs = {")
  for name, rule in stable_items(procs):
    prefer = rule.get("prefer", []) if isinstance(rule, dict) else []
    avoid  = rule.get("avoid", []) if isinstance(rule, dict) else []
    out.append(f"    [{lua_str(name)}] = {{ prefer = {dump_list(prefer)}, avoid = {dump_list(avoid)} }},")
  out.append("  },")

  # cooldown sync
  cds = normalize_cooldown_sync(payload.get("cooldownSync"))
  out.append("  cooldownSync = {")
  for leader, rule in stable_items(cds):
    partners = rule.get("partners", []) if isinstance(rule, dict) else []
    max_wait = rule.get("maxWait", 6.0) if isinstance(rule, dict) else 6.0
    min_ttd  = rule.get("minTTD", 12.0) if isinstance(rule, dict) else 12.0
    out.append(
      f"    [{lua_str(leader)}] = {{ partners = {dump_list(partners)}, maxWait = {max_wait}, minTTD = {min_ttd} }},"
    )
  out.append("  },")

  # charges
  charges = normalize_charges(payload.get("charges"))
  out.append("  charges = {")
  for spell, c in stable_items(charges):
    if not isinstance(c, dict): continue
    spend = c.get("spendAtOrAbove", 1)
    aoe_bonus = c.get("aoeBonus", 0.0)
    cap_urg = c.get("capUrgency", 2.0)
    out.append(
      f"    [{lua_str(spell)}] = {{ spendAtOrAbove = {spend}, aoeBonus = {aoe_bonus}, capUrgency = {cap_urg} }},"
    )
  out.append("  },")

  # interrupts
  out.append("  interrupts = {},")

  out.append("}")
  
  # Register
  out.append(f"\nif addonTable then")
  out.append("    addonTable.PolicyPacksGen = addonTable.PolicyPacksGen or {}")
  out.append(f"    addonTable.PolicyPacksGen[{lua_str(spec_key)}] = pack")
  out.append("end")
  out.append("return pack")
  out.append("")
  return "\n".join(out)

def main(in_path: str, out_dir="policies/spec"):
  try:
    data = json.loads(pathlib.Path(in_path).read_text(encoding="utf-8"))
  except Exception as e:
    print(f"Error reading input {in_path}: {e}")
    return

  if isinstance(data, dict) and "specKey" in data:
    items = [data]
  else:
    items = list(data)

  os.makedirs(out_dir, exist_ok=True)

  changed = 0
  for item in items:
    spec_key = item.get("specKey")
    if not spec_key: continue

    content = to_lua_policy(spec_key, item)
    path = pathlib.Path(out_dir) / f"{spec_key}.gen.lua"

    if write_if_changed(path, content):
      changed += 1
      print("updated:", path.as_posix())

  print("done. updated", changed, "files.")

if __name__ == "__main__":
  import sys
  if len(sys.argv) < 2:
    print("usage: python tools/policy_compiler.py <policies.json>")
  else:
    main(sys.argv[1])
