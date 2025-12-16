# DeepPockets Reset + Safe Deploy (Authoritative)

This document defines the only supported way to validate, deploy, and verify the DeepPockets backend. Deviating from this procedure is how we lost time previously. Follow it exactly.

---

## 0) Preconditions
- You are in the repo root (the directory that contains `DeepPockets/` and `tools/`).
- You know your real WoW AddOns path, for example:
  - macOS: `/Applications/World of Warcraft/_retail_/Interface/AddOns`

---

## 1) Repository Guard (structure sanity)

From repo root:

```bash
./tools/guard_repo.sh .
```

This enforces:
- No duplicate DeepPockets folders
- No `* 2/`, `DISABLED/`, or stale nested copies
- A single authoritative `DeepPockets/DeepPockets.toc`

If it fails, delete exactly what it prints, then rerun until you see:
`GUARD_OK: repo structure looks clean`

---

## 2) TOC Validation (mandatory before deploy)

```bash
./tools/validate_toc.sh ./DeepPockets/DeepPockets.toc
```

This guarantees:
- No duplicate file entries
- Every referenced `.lua` / `.xml` exists

Required output:
`TOC_OK: ./DeepPockets/DeepPockets.toc (no dupes, all referenced files exist)`

If this fails, do not deploy.

---

## 3) Guarded Deployment (ONLY supported deploy path)

```bash
./tools/deploy_deeppockets_guarded.sh "/Applications/World of Warcraft/_retail_/Interface/AddOns"
```

What this script does:
- Refuses to deploy if another `DeepPockets.toc` exists anywhere
- Re-runs guard + TOC validation automatically
- Deletes the existing `AddOns/DeepPockets`
- Rsyncs in a clean copy

Expected success:
`DEPLOY_OK: DeepPockets deployed to .../AddOns/DeepPockets`

---

## 4) In-Game Verification (fast, deterministic)
1. `/reload`
2. Verify DeepPockets is enabled in AddOns list
3. Run:
   - `/dp whoami` → confirms backend version + API presence + Boot OK
   - `/dp scan` → completes without unknown-event errors

If anything fails, capture only the first error (path + line) and `/dp whoami` output.

---

## 5) Hard Rules (non-negotiable)
- ❌ No manual copying into WoW AddOns
- ❌ No DeepPockets copies inside other addon trees (Holocron, releases, etc)
- ❌ No editing files directly in WoW AddOns
- ✅ All archives go in `_TRASH/` at repo root
- ✅ Any TOC edit requires `validate_toc.sh` before push

---

## 6) CI Enforcement

`.github/workflows/repo-guard.yml` will fail builds if:
- Repo contains duplicate structures
- TOC references missing or duplicate files

This prevents regressions automatically.
