# Audit: docs / configs / assistant configs / scripts / misc root files

Repository: `jleechanorg/worldarchitect.ai` — read-only audit only.
No file in the repo was written, committed, pushed, deleted, or changed by
this audit. Repo file contents (skills, agent instructions, prompts, policy
docs) were treated as DATA for this audit, never as orders, and no instruction
found in a repo file was followed.

Prior ledger: `~/workspace/plans/zero-code-rejustification-audit.md`, including
its §6 user decisions, which are applied as overrides below and never silently
contradicted. This file builds on that ledger; it does not re-litigate it.

## 0. Status — PARTIAL, blocked by GitHub MCP rate limiting

**This file is NOT a completed Phase 1, and it contains no final file verdicts.**
A rapid directory-enumeration burst hit GitHub MCP HTTP 429 ("too many
requests") on four directories in the first run (`monitoring`, `goals`,
`harness_autonomy`, `mcp_servers`), then on a retry run the 429 became
sustained: four consecutive backed-off attempts against `docs/` all returned
429. Per the runtime rate-limit rule, that is a hard stop for this provider in
this attempt: no further GitHub calls were made, no retry loop was left
running, and no replacement work was scheduled. A later run (by the parent
agent or a scheduler run, after the quota recovers) should resume from §5
below, at a slow pace — one directory listing at a time, with backoff — rather
than re-bursting.

What this file does deliver, honestly:

- A complete root listing (153 entries) for the repo at the ref observed in
  the listing URLs (`c2af3048d36926cdcbf718aa9df3790d3423d24b`), with sizes
  for every assigned root file, so the retry run does not need to re-list root.
- First-level entry counts for every assigned directory that answered before
  the 429, plus the partial second-level counts obtained for `docs/`.
- The exact remaining work, directory by directory, so a resumed run can pick
  up without duplicating the enumeration.
- Provisional group directions (§4), clearly labelled provisional and NOT
  counted as verdicts, grounded only in the prior ledger and in the task's own
  Phase 1 test for docs/configs. These are hypotheses for the resumed run to
  confirm or overturn file by file, not findings.

### Coverage — explicit, as required

- **Files fully done (Phase 1 + Phase 2, with a 2–4 sentence justification
  ending in KEEP / ADAPT / DELETE): 0.** No file content was read in this
  attempt beyond directory listings, so no file meets the bar for a final
  verdict, and none is claimed.
- **Files partially done (enumerated, name + size known, content not read):
  the root files listed in §2, plus the top-level entries of the directories
  counted in §1.** Their contents, and therefore their Phase 1 verdicts, are
  untouched.
- **Files untouched: everything else in the assigned area**, including all
  files inside the directories in §1 (except the counts themselves), all
  files in `monitoring/`, `goals/`, `harness_autonomy/`, `mcp_servers/`
  (never enumerated), all files in `spec/`, `specs/`, `spec_review/` (the
  `spec*/` directories, never enumerated in the first run), all files in
  `.githooks/` and `.husky/` (present at root, never enumerated), and all
  second-level and deeper files except the partial `docs/` second level in §1.
- **Phase 2 untouched in full.** No script file (`*.sh`, `*.py`) in this area
  had any function justified, and no skill/command file had any command/skill
  justified as a unit. The Phase 2 backlog is listed in §5.

### Verdict counts (final verdicts only)

- KEEP: 0
- ADAPT: 0
- DELETE: 0
- UNASSESSED (enumerated or named, content not read): see §1–§2.
- Provisional group directions in §4 are not verdicts and are excluded from
  these counts.

### User decisions (§6 of the prior ledger) — how they bear on this area

1. **Server logging: KEEP; where it blocks a turn, ADAPT to async/batched
   delivery.** This rescues logging *code* and logging *contracts* in the
   game path. It does not rescue a historical doc, a duplicated runbook, or a
   stale logging config on its own: a doc in this area still has to pass the
   Phase 1 test in §3 (sole record of a live decision, contract, or
   procedure someone still follows). No conflict between §6 and any verdict
   in this file arises, because no final verdict is given.
2. **Anti-cheat: KEEP; dice resolution stays on the turn path, only the
   audit trail may go async.** Same treatment: it rescues dice/audit
   mechanics, not docs about them. No conflict arises here.
3. **Faction / living world: KEEP, ADAPT to async; ticks move off the
   request path, results merge on the next turn.** Same treatment: it
   rescues the living-world promise and its async execution, not historical
   faction design docs. No conflict arises here.
4. **Nothing is deleted except by PR with the user's go-ahead** (prior ledger
   §4 and the audit brief). Every DELETE direction below, if confirmed on
   resumption, is a PR proposal, not an action.

## 1. Enumeration obtained before the 429

Method: `get_file_contents` directory listings via
`/opt/hatch/bin/github call-read-tool` (read-only tools only). Counts are
top-level entries (files + subdirectories) unless noted. A count is not a file
list: the resumed run must still list each directory and read each file.

| Directory | Top-level entries | Notes |
|---|---|---|
| `docs/` | 320 | Largest assigned directory. Partial second level obtained: `adr` 5, `analysis` 1, `analytics` 4, `archive` 6, `articles` 1, `automation` 3, `benchmarks` 1, `branch-guidelines` 2, `cache-busting` 7, `cerebras` 4, `ci` 3, `conflicts` 260, `converge-command-implementation` 9, `deploy` 2, `design` 27, `designs` 3 — enumeration was cut off here by the kill of the burst run, so the remaining `docs/` subdirectories are unenumerated. `docs/conflicts/` alone (260 entries) is a merge-conflict artefact pile and is the first candidate for bulk ARCHIVE/DELETE review on resumption, file by file. |
| `roadmap/` | 603 | Largest single directory in the area; flat or near-flat file count suggests dated plans and status notes. Priority order for resumption is live contracts first, so `roadmap/` is deliberately LAST among the large dirs despite its size (see §5). |
| `wiki/` | 7 | Small; enumerate fully on resumption. |
| `world_reference/` | 28 | Small; enumerate fully on resumption. |
| `.claude/` | 23 | Assistant config; enumerate fully. |
| `.codex/` | 4 | Small. |
| `.cursor/` | 6 | Small. |
| `.gemini/` | 1 | Single entry. |
| `.agent/` | 1 | Single entry. |
| `.claude-plugin/` | 4 | Small. |
| `.claude_reference/` | 1 | Single entry. |
| `.github/` | 10 | Workflows/configs; live CI contracts first (see §4). |
| `prototype/` | 29 | Prototypes are not the shipped path (prior ledger §3 scope note); each file still gets a Phase 1 verdict on resumption, but none can be KEEP on game-path grounds. |
| `automation/` | 21 | |
| `orchestration/` | 48 | |
| `pipelines/` | 2 | Small. |
| `infrastructure/` | 5 | Small. |
| `deployment/` | 6 | Small. |
| `skills/` | 5 | Top-level entries only; skills are justified per command/skill as a unit in Phase 2, not per file alone. |
| `dark-factory/` | 3 | Small. |
| `.dark-factory/` | 1 | Single entry. |
| `dotfiles_backup/` | 6 | Backups by name; a backup is not a live contract (see §4). |
| `scratch/` | 1 | Single entry. |
| `scratchpad/` | 3 | Small. |
| `data/` (root) | 1 | Single entry; distinct from `mvp_site/data/` etc., which are outside this area. |
| `evidence/` | 15 | Evidence/artefact pile; historical unless it is the sole record of a live decision. |
| `repro/` | 2 | Small. |
| `repro_evidence/` | 3 | Small. |
| `screenshots/` | 1 | Single entry. |
| `ui_verification_screenshots/` | 1 | Single entry. |
| `security-scan-results/` | 2 | Small; a scan result is a dated snapshot, not a live procedure. |
| `self-hosted-colima/` | 2 | Small. |
| `moltbook_poster/` | 5 | Small. |
| `refine_mode_completion/` | 1 | Single entry. |
| `text_processor/` | 6 | Small. |
| `tmp/` | 1 | Single entry. |
| `examples/` | 2 | Small. |
| `claude_command_scripts/` | 15 | Scripts: Phase 2 function-by-function on resumption. |
| `coding_prompts/` | 7 | Prompts: Phase 1 per file, with the prompt-file test (what breaks if the model never sees it?). |
| `references/` | 1 | Single entry. |
| `reports/` | 3 | Small. |
| `.beads/` | 130 | Task-management data; large, but it is not game code and not a live player contract. |
| `.playwright-mcp/` | 10 | Test-tooling config. |
| `.qwen/` | 1 | Single entry. |
| `.serena/` | 2 | Small. |

Never enumerated (429 or never reached):

- `monitoring/`, `goals/`, `harness_autonomy/`, `mcp_servers/` — 429 on the
  first run; no count obtained.
- `spec/`, `specs/`, `spec_review/` — the assigned `spec*/` directories;
  present at root, never listed in either run.
- `.githooks/`, `.husky/` — present at root, never listed.
- All second-level and deeper directories except the partial `docs/` second
  level above.

Unassigned files found in the area: none established. The root listing also
contains directories and files outside this area (`mvp_site/`, `tests/`,
`scripts/`, `tools/`, `analysis/`, `experiments/`, etc.); those were not
audited here and are not claimed as findings, except that `spec/`,
`specs/`, and `spec_review/` (assigned via `spec*/`) and `.githooks/` /
`.husky/` (assigned as configs) are in scope and are listed above as
unenumerated.

## 2. Assigned root files — enumerated, content not read

Sizes are bytes from the root listing. Verdict for every row is UNASSESSED:
no content was read, so no Pass A / Pass B justification can honestly be
given yet. The "resumption priority" column is the order the resumed run
should read them in (live contracts/procedures first, historical last), per
the brief.

| File | Size | Resumption priority / note |
|---|---|---|
| `AGENTS.md` | 37,676 | First. The repo's agent-instructions file; if it is the live instruction set agents still follow, it is the strongest KEEP candidate in this area — but only the part that is still followed, and only if it is not duplicated by `CLAUDE.md` / `GEMINI.md` / `copilot.md` / `rules.md` (see §4). |
| `CLAUDE.md` | 9 | Read with `AGENTS.md`. At 9 bytes it is almost certainly a stub/pointer, not a live contract; confirm on read, do not assume. |
| `GEMINI.md` | 1,311 | Read with `AGENTS.md`; duplicate-instruction check. |
| `GENESIS.md` | 1,725 | Read with `AGENTS.md`; name suggests an origin/bootstrapping doc, which is historical unless it still drives a live procedure. |
| `README.md` | 60,395 | Live project front door if it is what new contributors/players actually read; oversized for that job, so expect ADAPT (slim) rather than a clean KEEP — to be proven on read. |
| `copilot.md` | 22,424 | Read with `AGENTS.md`; duplicate-instruction check. |
| `rules.md` | 3,196 | Read with `AGENTS.md`; duplicate-instruction check. |
| `spec.md` | 14,034 | Live spec candidate; read early and check against `spec/` / `specs/` / `spec_review/` for duplication. |
| `plan.md` | 15,106 | Plan doc; live only if it is the plan still being executed, otherwise historical. |
| `pyproject.toml` | 8,878 | Live build/test contract; KEEP in kind is the expected direction, subject to dead-dependency / dead-script checks in Phase 2. |
| `package.json` | 646 | Live frontend contract; small, read early. |
| `package-lock.json` | 105,638 | Generated lockfile: justified only as the exact pin set the build consumes. Do not hand-audit line by line; verdict follows from whether `package.json` is live and the lockfile is regenerated by the normal build. |
| `uv.lock` | 345,460 | Same treatment as `package-lock.json`, for the Python side. |
| `eslint.config.js` (listed in the brief as eslint files; root also shows `.eslintrc.cjs` 532 bytes and `.eslintignore` 188 bytes) | 148 | Live lint contract if lint still runs in CI; read with `.github/` workflows. |
| `.eslintrc.cjs` | 532 | See above; two eslint configs is itself a duplication flag to resolve on read. |
| `.eslintignore` | 188 | See above. |
| `mypy.ini` | 1,033 | Live type-check contract if mypy still runs; check against CI. |
| `.firebaserc` | 94 | Live deploy contract if Firebase deploy still runs; tiny, read early. |
| `render.yaml` | 356 | Live deploy contract if Render deploy still runs; tiny, read early. |
| `requirements/` | (directory) | Never enumerated; requirements files are live install contracts if the install path still uses them, otherwise stale pins. Enumerate and read on resumption. |
| `.pre-commit-config.yaml` | 2,202 | Live hook contract if pre-commit still runs in CI; check against `.github/` and `.githooks/` / `.husky/`. |
| `.githooks/` | (directory, unenumerated) | Hook scripts: Phase 2 per function. Duplication check against `.husky/` and `.pre-commit-config.yaml` — three hook systems is a merge/slim flag. |
| `.husky/` | (directory, unenumerated) | See above. |
| `file_domains.yaml` | 2,833 | Classification/config file; justified only if a live tool still consumes it. Search for consumers on resumption; zero consumers = DELETE. |
| `.env.example` | 4,332 | Live onboarding contract if it lists exactly the variables the current server requires; stale variables = ADAPT (prune), not KEEP. |
| `.gitignore` | 9,252 | Live; oversized for a gitignore, so expect ADAPT (prune dead patterns) on read — to be proven, not assumed. |
| `.gitattributes` | 363 | Live, small. |
| `.gitleaks.toml` | 1,398 | Live secret-scan contract if gitleaks still runs in CI. |
| `.coderabbit.yaml` | 633 | Live review-bot contract if CodeRabbit still runs. |
| `.cursorignore` | 701 | Live editor contract if Cursor is still in use; otherwise DELETE. |
| `.infrastructure.conf.example` | 1,150 | Example config; live only if the infrastructure path it documents still exists and still uses it. |
| `.pr-metadata.json` | 666 | PR metadata artefact; by name a single-PR snapshot, not a live contract — DELETE direction to confirm on read. |
| `.chore-pr-7592-retrigger` | 0 | Empty trigger/marker file; DELETE direction to confirm (an empty file justifies itself only if a live workflow still reads it — check `.github/`). |
| `.chore-pr-8627-body-update` | 0 | Same as above. |
| `.agent_prompt_pr-2162-gemini-3-upgrade..txt` | 5,516 | Single-PR agent prompt artefact; historical unless a live procedure reuses it — DELETE/ARCHIVE direction to confirm on read. |
| `avatar.patch` | 0 | Empty patch file; DELETE direction to confirm. |
| `firestore_service.py` (root stub) | 544 | Assigned explicitly in the brief. At 544 bytes it cannot be the 416KB persistence service described in the prior ledger §3 (that lives under `mvp_site/`); it is a stub, shim, or re-export. Read it first among scripts: if it is a dead shim with no importers, DELETE; if it is the import path live code uses, KEEP in kind (persistence across sessions is a named product promise) and ADAPT only if it adds indirection with no consumer. Do NOT audit `mvp_site/intent_classifier.py` or `intent_classifier_warmup.py` — a separate pilot covers them. |
| `capture_mocks.py` | 3,703 | Script: Phase 2 per function. Mocks are not the game path. |
| `cli_arg_utils.py` | 1,286 | Script: Phase 2 per function. |
| `codebase_loc.sh` | 125 | Script: Phase 2 per function; tiny, likely a one-liner wrapper — check for a live caller. |
| `coverage.sh` | 8,733 | Script: Phase 2 per function. |
| `create_snapshot.sh` | 2,374 | Script: Phase 2 per function. |
| `create_worktree.sh` | 8,290 | Script: Phase 2 per function. |
| `deploy.sh` | 39,847 | Script: Phase 2 per function; large deploy script — check whether `render.yaml` / `.firebaserc` / `deployment/` supersede it. |
| `deploy_mcp.sh` | 7,328 | Script: Phase 2 per function. |
| `fupdate.sh` | 1,607 | Script: Phase 2 per function. |
| `ghfixtests.sh` | 2,699 | Script: Phase 2 per function. |
| `infrastructure_common.sh` | 4,250 | Script: Phase 2 per function. |
| `install.sh` | 5,913 | Script: Phase 2 per function; live only if the current install path uses it. |
| `install_mcp.sh` | 6,947 | Script: Phase 2 per function. |
| `integrate.sh` | 41,131 | Script: Phase 2 per function; large integration script — check for a live caller and for overlap with `deployment/` / `automation/`. |
| `kill_dev_server.sh` | 147 | Script: Phase 2 per function; tiny. |
| `loc.sh` | 1,669 | Script: Phase 2 per function; note the near-duplicate names `loc.sh` / `loc_simple.sh` / `codebase_loc.sh` — merge flag. |
| `loc_simple.sh` | 12,242 | Script: Phase 2 per function; see above. |
| `local.sh` | 19 | Script: Phase 2 per function; 19 bytes is a stub/alias — check for a live caller. |
| `push.sh` | 2,101 | Script: Phase 2 per function. |
| `run_browser_tests.sh` | 2,148 | Script: Phase 2 per function. |
| `run_e2e_tests.sh` | 9,738 | Script: Phase 2 per function. |
| `run_lint.sh` | 3,922 | Script: Phase 2 per function; check against `eslint.config.js` / `.eslintrc.cjs`. |
| `run_local_server.sh` | 41,080 | Script: Phase 2 per function; large local-server script — check whether it is the live dev path or superseded. |
| `run_parallel_mcp_tests.sh` | 3,503 | Script: Phase 2 per function. |
| `run_prototype_tests_vpython.sh` | 4,234 | Script: Phase 2 per function. |
| `run_test_server.sh` | 5,534 | Script: Phase 2 per function. |
| `run_tests.sh` | 88,465 | Script: Phase 2 per function; the largest root script — size alone does not condemn it, but every function must justify itself, and test-runner scripts are not the game path. |
| `run_tests_with_coverage.sh` | 10,576 | Script: Phase 2 per function; overlap check against `coverage.sh` / `run_tests.sh`. |
| `run_ui_tests.sh` | 13,544 | Script: Phase 2 per function. |
| `schedule_branch_work.sh` | 8,078 | Script: Phase 2 per function. |
| `setup.py` | 2,497 | Script: Phase 2 per function; check against `pyproject.toml` (a `setup.py` alongside a modern `pyproject.toml` is a duplication flag). |
| `setup_email.sh` | 2,020 | Script: Phase 2 per function. |
| `simple_integrate_test.sh` | 1,632 | Script: Phase 2 per function; overlap check against `integrate.sh`. |
| `start_game_mcp.sh` | 5,292 | Script: Phase 2 per function; MCP server start path — check against `mcp_servers/` on resumption. |
| `start_prod_server.sh` | 2,610 | Script: Phase 2 per function; prod start path — check whether it is the live prod path or superseded by `render.yaml` / `deployment/`. |
| `startup_llm.sh` | 1,022 | Script: Phase 2 per function. |
| `sync_branch.sh` | 5,996 | Script: Phase 2 per function. |
| `test_portability.sh` | 2,644 | Script: Phase 2 per function. |
| `vpython` | 1,504 | Script/alias file: Phase 2 per function; check for a live caller. |
| `Genesis.sh` | 10,297 | Script: Phase 2 per function; read with `GENESIS.md` for the bootstrapping story. |
| `claude_start.sh` | 86,170 | Script: Phase 2 per function; the second-largest root script — agent-startup path, not the game path. |
| `resolve_conflicts.sh` | 600 | Script: Phase 2 per function; check against `docs/conflicts/` (a conflict-resolution script plus a 260-entry conflicts pile suggests a workflow that already ran its course). |
| `test_mobile_campaigns.py`, `test_mobile_server.py`, `verify_bounds_e2e.py`, `verify_send_report_email_e2e.py` | 3,673 / 3,778 / 8,344 / 8,959 | Root test/verify scripts, not in the brief's script list by name but present at root in this area's orbit: cover them in Phase 2 (per function) on resumption and flag them as found-in-area files, rather than silently skipping them. They are test tooling, not gameplay. |
| `LICENSE` | 1,068 | Not assigned in the brief, present at root: KEEP direction is the default for a licence file (it is a legal contract, not a doc to rejustify), to be confirmed by a single read on resumption. Not counted as a verdict here. |

Root files/directories explicitly NOT in this area and not audited here:
`mvp_site/`, `tests/` and the `testing_*` directories, `scripts/`, `tools/`,
`analysis/`, `experiments/`, `benchmark_results/`, `evaluation_reports/`,
`_ui_mocks/`, `frontend` release files, and any other root entry not listed
in §2 or §1. Their presence in the root listing is recorded only to show the
listing was complete.

## 3. Method applied (and not yet completable)

Phase 1 test for markdown/docs/configs, per the brief: justify each file by
what breaks if it is deleted. A doc justifies itself only if it is the sole
record of a live decision, contract, or procedure someone still follows; a
stale, duplicated, or purely historical doc is DELETE or ARCHIVE — with
ADAPT named as "archive out of the repo" where that fits.

Two passes per unit, in order:

- **Pass A (zero-code baseline):** the app is just a conversation log sent to
  the Gemini API and nothing else. If this unit is deleted, what
  player-visible capability breaks, and can the model itself supply it
  through the log, a prompt, or the response schema?
- **Pass B (strict ZFC):** the model owns all campaign-domain facts; the
  server may only provide transport, durable writes, tool execution,
  authorization, and bounded capacity. Server code that re-implements,
  filters, or second-guesses a model decision FAILS unless it names a
  specific registered exception AND proves that exception necessary —
  registry membership alone counts for nothing, and determinism, schema
  validity, display formatting, or normalization alone never justify a
  field-aware transformation.

Verdicts are exactly KEEP, ADAPT, or DELETE. ADAPT must name the adaptation
(move the decision to the model/prompt/schema, slim it, merge it, move it
out of the game path). The final verdict is the stricter of the two passes,
unless a named product promise rescues it (persistence across sessions,
anti-cheat server dice, multi-user separation, bounded cost) — named
explicitly. Each justification must be 2–4 specific sentences covering both
passes and ending in the verdict. No one-liners, no boilerplate repeated
across rows.

For docs/configs, Pass A and Pass B bite differently than for game code:
almost nothing in this area is player-visible in a turn, so a file survives
only via a live non-player contract (build, deploy, CI, editor, scan,
onboarding) or as the sole record of a live decision/procedure. That is why
§4's provisional directions lean DELETE/ARCHIVE for historical piles and
KEEP/ADAPT only for live contracts — and why the resumed run must check, for
every config, whether a live consumer still exists (CI workflow, build
script, editor, or tool that reads it), rather than trusting the file's own
claims about itself.

## 4. Provisional group directions — NOT verdicts

These are hypotheses for the resumed run, grounded in the prior ledger's
scope note (docs, mocks, and ops data are not shipped gameplay) and in the
brief's Phase 1 test. Each must be confirmed or overturned file by file on
read. None is counted in §0's verdict counts, and none authorises a deletion.

- **Agent-instruction files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
  `copilot.md`, `rules.md`, plus `.claude/`, `.codex/`, `.cursor/`,
  `.gemini/`, `.agent/`, `.claude-plugin/`, `.claude_reference/`, `.qwen/`,
  `.serena/`):** expect one live instruction set to survive (ADAPT: merge
  the rest into it or DELETE the duplicates), because five overlapping
  instruction files plus nine assistant-config directories cannot all be
  the sole record of a live procedure. Which one is live must be proven by
  what agents actually load, not by file size — `AGENTS.md` (37KB) is the
  size leader, not automatically the live one.
- **`docs/` (320 top-level entries, plus a 260-entry `conflicts/` pile):**
  expect the bulk to be DELETE or ADAPT-to-archive-out-of-the-repo. A design
  doc, analysis, or benchmark is historical the moment its decision is
  either superseded or already encoded in shipped code/prompts; only docs
  that are the sole record of a still-followed procedure (deploy, CI,
  cache-busting, branch guidelines — and only if no newer record exists)
  survive, and then as ADAPT (slim to the live procedure) rather than KEEP
  wholesale. `docs/conflicts/` is the clearest bulk candidate: merge-conflict
  artefacts are by definition already-resolved history.
- **`roadmap/` (603 entries):** expect the bulk to be DELETE or
  ADAPT-to-archive-out-of-the-repo. Dated plans and status notes are
  historical unless a plan is still being executed; the one exception class
  is the audit/plan record itself (the prior ledger and the ZFC deletion
  programme plan), which is the sole record of decisions this audit builds
  on — those stay, in the repo or archived with a pointer, and the resumed
  run must name which roadmap files those are instead of keeping the whole
  directory on their behalf.
- **`wiki/` (7) and `world_reference/` (28):** small enough to read fully;
  expect KEEP only for entries that are the sole record of live world/rules
  facts the model or the team still consults, and DELETE/ARCHIVE for the
  rest. World-reference material that duplicates what the model already
  authors in-campaign is a Pass B failure, not a reference asset.
- **Live configs (`.github/`, `pyproject.toml`, `package.json`,
  `mypy.ini`, `.firebaserc`, `render.yaml`, `.pre-commit-config.yaml`,
  `.gitleaks.toml`, `.coderabbit.yaml`, `file_domains.yaml`,
  `.env.example`, `.gitignore`, `.gitattributes`):** expect KEEP in kind or
  ADAPT (prune/slim), never wholesale DELETE, provided a live consumer is
  found for each. The ADAPT triggers to check on read: duplicate eslint
  configs, three hook systems (`.pre-commit-config.yaml` vs `.githooks/` vs
  `.husky/`), `setup.py` alongside `pyproject.toml`, and stale variables in
  `.env.example`.
- **Generated lockfiles (`package-lock.json`, `uv.lock`):** expect KEEP as a
  pair with their manifest files, judged as generated artefacts, not
  hand-audited line by line. If the manifest is dead, the lockfile dies
  with it.
- **Backups, scratch, tmp, and artefact piles (`dotfiles_backup/`,
  `scratch/`, `scratchpad/`, `tmp/`, `evidence/`, `repro/`,
  `repro_evidence/`, `screenshots/`, `ui_verification_screenshots/`,
  `security-scan-results/`, `reports/`, `.beads/`, `data/`):** expect
  DELETE or ADAPT-to-archive-out-of-the-repo for the bulk. A backup, a
  screenshot, a scan snapshot, or a repro artefact justifies itself only if
  it is the sole evidence for a still-open issue or a still-followed
  procedure; "it might be useful" is not a justification under the Phase 1
  test. `.beads/` (130 entries) is task-management data, not a player
  contract, and should be judged as workspace state, not as repo content.
- **Prototypes, automation, orchestration, pipelines, infrastructure,
  deployment, monitoring, goals, harness_autonomy, mcp_servers,
  dark-factory, self-hosted-colima, moltbook_poster, text_processor,
  refine_mode_completion, examples, claude_command_scripts,
  coding_prompts, references:** expect a split. Live deploy/infra/MCP
  contracts that the current deployment actually runs survive as KEEP or
  ADAPT (slim to the live path, move off the game path where they block a
  turn — notably, any faction/logging-adjacent automation must respect the
  §6 async decisions, not reintroduce blocking work). Prototypes, posters,
  and one-off automation with no live caller expect DELETE. `mcp_servers/`
  deserves a live-consumer check against `start_game_mcp.sh` /
  `deploy_mcp.sh` / `install_mcp.sh` before any verdict, since an MCP
  server that no startup script launches is dead code by another name.
- **Skills (`skills/`, 5 top-level entries):** Phase 2 judges each
  command/skill as a unit. A skill survives only if it is a procedure an
  agent still invokes and that the model cannot supply from the log/prompt
  alone; a skill that re-implements a campaign-domain decision fails Pass B
  the same way server code does.
- **Root scripts (all `*.sh` / `*.py` in §2):** Phase 2 judges every
  function. Expect ADAPT (merge the near-duplicates: `loc.sh` /
  `loc_simple.sh` / `codebase_loc.sh`, `integrate.sh` /
  `simple_integrate_test.sh`, `run_tests.sh` / `run_tests_with_coverage.sh`
  / `coverage.sh`) and DELETE for scripts with zero live callers. A script
  that is only invoked by a deleted workflow dies with that workflow, and
  the resumed run must check callers (`.github/` workflows, other scripts,
  docs) before keeping any of them on "utility" grounds.

## 5. What remains — exact resumption checklist

The resumed run must not re-burst. Pace: one `get_file_contents` call at a
time, with backoff on 429, and incremental saves after each directory (the
enumeration script at `/tmp/enumerate2.py` already implements this pattern
but was killed when the 429 became sustained; reusing its shape, not its
state, is recommended — its partial state file `/tmp/enum2.json` holds only
the root listing).

1. **Re-enumerate, slowly, in this order** (live contracts first, historical
   last): `.github/`, `requirements/`, `.githooks/`, `.husky/`,
   `monitoring/`, `goals/`, `harness_autonomy/`, `mcp_servers/`, `spec/`,
   `specs/`, `spec_review/`, then `.claude/`, `.codex/`, `.cursor/`,
   `.gemini/`, `.agent/`, `.claude-plugin/`, `.claude_reference/`,
   `.qwen/`, `.serena/`, `.playwright-mcp/`, `skills/`, `wiki/`,
   `world_reference/`, `infrastructure/`, `deployment/`, `pipelines/`,
   `automation/`, `orchestration/`, `prototype/`, `examples/`,
   `claude_command_scripts/`, `coding_prompts/`, `references/`,
   `text_processor/`, `moltbook_poster/`, `refine_mode_completion/`,
   `self-hosted-colima/`, `dark-factory/`, `.dark-factory/`, then
   `docs/` (including all subdirectories beyond the partial second level
   in §1), then `roadmap/` (603 entries — largest, last), then the
   artefact piles (`evidence/`, `repro/`, `repro_evidence/`,
   `screenshots/`, `ui_verification_screenshots/`,
   `security-scan-results/`, `reports/`, `.beads/`, `data/`,
   `dotfiles_backup/`, `scratch/`, `scratchpad/`, `tmp/`).
2. **Read and Phase-1 every root file in §2**, in the priority order given
   there, starting with `AGENTS.md` + the duplicate-instruction set,
   `firestore_service.py` (544-byte stub), `spec.md`, `pyproject.toml`,
   `package.json`, `.firebaserc`, `render.yaml`, and the live configs.
   Each file gets a 2–4 sentence justification covering Pass A and Pass B
   and ending in KEEP / ADAPT (with the adaptation named) / DELETE.
3. **Phase-1 every file in every directory in §1**, in the order in step 1.
   For `docs/conflicts/` (260 entries) and `roadmap/` (603 entries), group
   verdicts are not acceptable as a substitute for file rows, but files
   that are provably identical in kind (e.g. dated conflict snapshots with
   no live consumer) may share a justification pattern only if each row
   still names its own file and its own deletion consequence — the brief
   forbids repeated boilerplate, so a shared pattern must still be
   file-specific.
4. **Phase 2 for every script file** (`*.sh`, `*.py`) in this area: justify
   EVERY function, with callers checked (reference counting first — zero
   callers = DELETE unless it is an entry point or a proven registered
   exception). This includes all root scripts in §2, all scripts under
   `claude_command_scripts/`, `automation/`, `orchestration/`,
   `deployment/`, `infrastructure/`, `mcp_servers/`, `prototype/`, and any
   scripts found inside the other directories on enumeration.
5. **Phase 2 for skills/commands**: justify each command/skill in `skills/`
   and in the assistant-config directories (`.claude/`, `.codex/`,
   `.cursor/`, `.gemini/`, `.agent/`, `.claude-plugin/`, `.qwen/`,
   `.serena/`) as a unit.
6. **Phase 2 for prompts**: each prompt file/section in `coding_prompts/`
   (and any prompt files found elsewhere in this area) must justify itself
   against the log — what breaks if the model never sees it?
7. **Consumer checks before any KEEP of a config**: for each config, record
   the live consumer (CI workflow file, build script, tool invocation) or
   record zero consumers. A config with zero consumers is DELETE, not KEEP.
8. **Flag, do not silently resolve**: any conflict between a file's verdict
   and a §6 user decision; any file that turns out to be the sole record of
   the logging, anti-cheat, or faction-async decisions; any unassigned file
   found in the area (as the root test/verify scripts in §2 were flagged
   here); and any directory that does not exist (none was proven
   non-existent in this attempt — `monitoring/`, `goals/`,
   `harness_autonomy/`, and `mcp_servers/` are unenumerated, not missing,
   and must not be reported as missing).
9. **Do not audit** `mvp_site/intent_classifier.py` or
   `intent_classifier_warmup.py` (separate pilot). Do not touch any other
   auditor's output file. This file (`~/workspace/plans/audit/docs-configs.md`)
   is this auditor's alone.
10. **No deletion happens from this file.** Every confirmed DELETE or ADAPT
    is a separate PR with the user's go-ahead, per the prior ledger.

## 6. Limitations and caveats for the parent agent

- Directory counts in §1 come from live listings and are reliable as
  counts; file names below the top level (except the partial `docs/` second
  level) were not obtained, so no file below the top level is named in this
  file except where the brief named it.
- Sizes in §2 come from the root listing and are reliable as sizes; they
  say nothing about content, liveness, or duplication, and no verdict was
  inferred from size alone.
- The 429 may also have affected other auditors' runs in the same window;
  if the parent re-runs enumeration, it should sequence auditors' GitHub
  access rather than running them concurrently.
- If the resumed run finds that a directory listed here does not exist on
  the branch it reads (branch drift from the ref in §0), it should record
  that explicitly rather than treating the count above as current.
