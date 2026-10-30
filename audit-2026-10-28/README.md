# Zero-code / strict-ZFC audit analysis — 2026-10-28

Consolidated record of the rejustification audit of `mvp_site` in
`jleechanorg/worldarchitect.ai`: every file, then every method, judged first
against a zero-code baseline (bare conversation log + Gemini API) and then
against strict ZFC (the model authors campaign-domain facts; the server
provides only transport, durable writes, tool execution, authorization, and
bounded capacity). Verdicts are KEEP / ADAPT / DELETE.

## Basis

- Audited tree: `main` at `c2af304` (Oct 28, 2026 snapshot). The same
  classification is published in the game repo as draft PR #11003
  (`docs/audit-2026-10-28/`), and the first deletion is draft WIP PR #11012
  (see `pilot-deletion-status.md`).
- Owner decisions applied: server logging KEEP (async where it blocks a
  turn); anti-cheat KEEP (server dice stays on the turn path); factions KEEP
  but async; agent routing role KEPT as a Jev-powered model-side decision
  step (Jev not yet implemented).
- Nothing here is merged to the game repo. PRs are review-only.

## Contents

- `MASTER-LEDGER.md` — run 2 merged ledger: 3,163 rows
  (KEEP 2,470 / ADAPT 325 / DELETE 366 / MIXED 3), plus the audit spec,
  the zero-code "needed" list, and the owner decisions.
- `loc-removed-report.md` — mvp_site prod DELETE line count: 16,844-line
  floor (5,758 whole-file + 11,086 in-file); ADAPT/MIXED/conditional
  excluded. `loc-removed-compute.py` reproduces it.
- `review/MERGED-SUMMARY.md` + 14 per-area reports — review pass:
  585/585 non-test files, ~10,635 units, ~130 dead/unreachable entries,
  ~169 stale-docs items, 36 run-2 verdict flips.
- Per-group files (`agents-prompts.md`, `dice-mechanics.md`,
  `docs-configs.md`, `faction-worldsim-time.md`, `frontend.md`,
  `gateway-call-path.md`, `godmode-levelup-rewards.md`,
  `logging-ops-incident.md`, `providers-auth.md`, `schema-parsing.md`,
  `scripts-tests.md`, `state-storage.md`) — the run 2 group records
  behind the merged ledger.
- `intent_classifier.md` — the pilot audit (intent classifier + warmup:
  both files DELETE in full, 52 DELETE / 2 ADAPT / 0 KEEP).
- `pilot-pr-body.md` — the full body drafted for pilot deletion PR #11012.
- `zfc-skill-model-amendment-proposal.md` — DRAFT ONLY, not applied:
  FastEmbed and Jev count as models under the ZFC ownership contract.
  Needs owner approval, then a PR and full independent review.
- `manifest_mvp_site.txt` — the audited file manifest.
- `scripts-tests-enumeration.txt` — the scripts/tests enumeration.

## Excluded from this folder

- GCP runtime evidence (kept out: GCP project/service internals).
- Review helper/coverage files (`_areas.json`, `_file_list.txt`,
  `_leftovers.json`, `gen_prompts_data.py`).
- The audit follow-ups are still open, not recorded here as done:
  scripts-tests remainder, docs-configs content audit, depth caveats,
  assignment confirmations, the 8 run-2 section 6 flags, and the
  remaining deletion PRs beyond the pilot.
