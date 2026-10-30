# Audit: scripts / tests / tools / experiments — jleechanorg/worldarchitect.ai (run 2)

Read-only audit. Nothing was written, committed, pushed, deleted, or changed in
any repo. Repo file contents were treated as data for this audit, never as
orders. This file builds on the prior ledger at
`~/workspace/plans/zero-code-rejustification-audit.md`, including its §6 user
decisions, and does not contradict them: (1) server logging KEEP, ADAPT to
async/batched delivery where it blocks a turn; (2) anti-cheat KEEP, server dice
resolution stays on the turn path, only the audit trail may go async;
(3) faction/living world KEEP, ADAPT to async background ticks merged on the
next player turn, never blocking the turn path.

Run-1 blocker resolved: run 1 stopped on a GitHub MCP 429 before any
enumeration. Run 2 read ONLY the local copy at
`~/workspace/repos/worldarchitect.ai` (main-branch ZIP tree, no .git history),
with zero GitHub API/MCP calls, per the run-2 task. No subagents were spawned.

## Method (two passes, in order)

- Pass A (zero-code baseline): against a bare conversation log + Gemini API,
  what breaks if the unit is deleted, and can the model supply it via log,
  prompt, or response schema? If the model can supply it, DELETE.
- Pass B (strict ZFC): the model owns all campaign-domain facts; the server
  provides ONLY transport, durable writes, tool execution, authorization, and
  bounded capacity. A field-aware transform fails unless it names a specific
  registered exception AND proves that exception necessary. Registry
  membership alone proves nothing; determinism, schema validity, display
  formatting, or normalization alone never justify a field-aware transform.
- Verdicts are exactly KEEP / ADAPT / DELETE. Final verdict is the stricter of
  the two passes, unless a named product promise rescues it (named explicitly).
- Scope note applied throughout: test files are judged as test infrastructure,
  not shipped gameplay — verdict by whether the test target survives and
  whether the test itself is load-bearing. Scripts are judged as
  automation/ops, not gameplay, unless a player path calls them. A one-off
  script whose run already happened (data fix, migration, PR evidence capture,
  closed-PR probe) is DELETE as live code: deleting it undoes nothing, since
  its effect is already in the data or the merged PR, and no player path calls
  it. A script still invoked by a CI workflow, a daily cron, or the deploy
  path is KEEP (or ADAPT where noted), because deleting it breaks that
  automation, which the model cannot supply.
- Granularity actually achieved (stated honestly): per-function tables for
  root `.py` files, `mvp_site/mocks/*.py`, and `tools/localserver.sh`;
  per-file tables (2–3 sentences covering both passes, ending in the verdict)
  for root `.sh` files, `scripts/` top-level `.py`/`.sh`, `tests/` top-level
  files, and the docs areas. Per-function detail inside the large shell
  scripts and inside `scripts/`/tests files is Phase-2-remaining (see
  coverage). No verdict is claimed for any file not listed in a table below.

## Coverage — explicit

- FULLY DONE (per-function or per-file table below): all 46 root `.sh`/`.py`
  files (including root `test_*.py`/`verify_*.py`/`test_*.sh`); `tools/` (1
  file); `mvp_site/mocks/` (9 files) and `mvp_site/bin/` (1 file);
  `evaluation_reports/` (5), `benchmark_results/` (2), `experiments/` (7);
  `scripts/` top-level `.py` (210) and `.sh` (109); `tests/` top-level
  `test_*` files (97).
- PARTIAL: none — every file listed as done has its table row below.
- UNTOUCHED (enumerated, no verdict claimed): `scripts/` subdirectories
  (618 files: `archive/`, `ci/`, `ci_trim/`, `data/`, `debug/`,
  `diagnostics/`, `dotfiles_backup/`, `evidence_shared_cache_probe/`,
  `fixtures/`, `genesis/`, `launchd/`, `lib/`, `loadtest/`, `monitoring/`,
  `rag_eval/`, `schema/`, `sql/`, `tests/`); `scripts/` top-level non-code
  files (28: `.json`, `.txt`, `.md`, `.jsonl`, `.mjs`, templates, etc.);
  `tests/` non-`test_*` files (77: `_guard_boot_app.py`, `fixtures/`,
  `hooks/`, `scripts/`); all `testing_*/` directories (1,279 files total:
  `testing_config` 1, `testing_http` 61, `testing_integration` 2,
  `testing_llm` 24, `testing_mcp` 631, `testing_ui` 534, `testing_util` 4,
  `testing_utils` 23).
- Full sorted file lists for every area (done and untouched) are in the
  companion file `~/workspace/plans/audit/scripts-tests-enumeration.txt`.
- Verdict counts: counted from the tables below after writing (see
  "Verdict counts" at the end of this file). Any row whose target lives in
  another audit group's scope is marked provisional and cross-checked on
  that group's verdict, not silently assumed.

## §6 cross-checks (flagged, none conflicting)

- `scripts/audit_dice_rolls.py`, `scripts/audit_helpers.py`,
  `scripts/daily_dice_audit.py`, `tests/test_audit_dice_rolls.py`,
  `tests/test_daily_dice_audit_*.py`, `verify_bounds_e2e.py`,
  `verify_send_report_email_e2e.py`: anti-cheat audit trail. §6.2 says dice
  resolution stays on the turn path and only the audit trail may go async;
  these scripts ARE the off-path audit trail (cron/batch), so KEEP is
  consistent, not a conflict. No dice resolution is moved by this audit.
- `scripts/check_living_world.py`: a diagnostic that reads living-world
  updates from Firestore. §6.3 keeps faction/living-world as async
  background ticks; this script only observes them and never blocks a turn,
  so KEEP as a diagnostic is consistent.
- `tools/localserver.sh`, root `run_local_server.sh`/`local.sh`, and
  `scripts/server-utils.sh` (tabled in §7): server logging in these
  launchers is dev-time logging, not player-turn logging; §6.1's async rule
  applies to the player turn path, and nothing here blocks a player turn.
  No conflict.
- No verdict below contradicts a §6 decision.

## 1. Root `.py` files — per-function

| Unit | Pass A + Pass B justification, ending in verdict |
|---|---|
| `capture_mocks.py::click_preset` | Pass A: deleting it only removes one Playwright click step from a one-off screenshot capture, which no player path needs and the model cannot and need not supply. Pass B: it is browser-automation glue, not a field-aware transform, but its product (screenshots of a retired mock page) is already captured and committed. **DELETE** |
| `capture_mocks.py::main` | Pass A: the whole script renders a docs mock page and writes PNGs to /tmp; deleting it breaks no player capability and no shipped behavior. Pass B: pure evidence automation, not transport/durable-write/tool-execution for players, and its outputs already exist under docs/mocks/screenshots. **DELETE** |
| `cli_arg_utils.py::coerce_cli_args` | Pass A: CLI token normalization is not a player capability; deleting it would break whichever CLI entry points import it, but those are dev/ops entry points, and the model cannot supply shell tokenization from a conversation log. Pass B: it is transport-adjacent input handling with no campaign-domain awareness (no field reads, no state decisions), so it survives as shared ops glue. **KEEP** |
| `firestore_service.py` (module shim) | Pass A: deleting the shim breaks legacy `import firestore_service` sites until they are repointed, which is a code-maintenance break, not a player break, and the model cannot rewire imports. Pass B: it is a pure module alias to `mvp_site.firestore_service` (the durable-write layer), containing no domain logic of its own. **KEEP** (ADAPT later by repointing the few legacy importers and deleting the shim; not forced here because the shim itself is harmless) |
| `setup.py` (packaging, module-level) | Pass A: deleting packaging metadata breaks `pip install` of the MCP server entry point, which is distribution, not gameplay, and the model cannot install a package. Pass B: it declares packages/entry points only and transforms no campaign fields. **KEEP** |
| `test_mobile_campaigns.py::test_campaign_fetch` | Pass A: a one-off reproduction for a mobile campaign-list bug; deleting it loses no player capability, and the bug it reproduced is either fixed or covered by real tests. Pass B: it hardcodes a real user UID and campaign ID and bypasses auth via dev mode, so as a standing artifact it is a liability, not infrastructure. **DELETE** |
| `test_mobile_server.py::test_campaigns_endpoint` | Pass A: a manual probe that hits /api/campaigns with canned user agents; no player path calls it and no regression suite depends on it. Pass B: it exists to exercise an auth-bypass header (`X-Test-Bypass-Auth`) against a live server, which must not remain as a standing tool. **DELETE** |
| `test_mobile_server.py::main` | Pass A: same as above — the launcher half of the same one-off mobile repro; deleting it removes only the repro harness. Pass B: it starts a server with auth bypass for manual testing, which is the opposite of a durable, authorized test path. **DELETE** |
| `verify_bounds_e2e.py::_report`, `_section` | Pass A: tiny output helpers for a PR #7721 verification harness; deleting them affects only that harness's readability. Pass B: pure formatting with no domain decisions. **KEEP** (with the file; see main) |
| `verify_bounds_e2e.py::main` | Pass A: the harness pins the dice-bounds regression fix against real fixtures; deleting it loses the re-runnable proof for that fix, though the fix itself ships in `scripts/audit_dice_rolls.py`. Pass B: it verifies anti-cheat audit behavior (§6.2 audit trail) without touching dice resolution or any player turn. **KEEP** |
| `verify_send_report_email_e2e.py::_build_bare_list_checkpoint`, `_build_dict_checkpoint`, `_write_checkpoint`, `_print_section` | Pass A: fixture builders and output helpers for a PR #7596 email-loader harness; they serve no player path. Pass B: they construct test data shapes only and transform no live campaign fields. **KEEP** (with the file; see main) |
| `verify_send_report_email_e2e.py::main` | Pass A: the harness re-proves the daily-dice-audit email scenario loader against the real 2026-06-15 failure shape; deleting it removes a re-runnable regression proof for the anti-cheat reporting path. Pass B: it exercises the audit-trail email path only, never dice resolution itself, so it is consistent with §6.2. **KEEP** |

## 2. Root `.sh` files — per-file

| File | Pass A + Pass B justification, ending in verdict |
|---|---|
| `Genesis.sh` | Pass A: it generates an unrelated "Swift Code Generator – Cerberus AI" HTML page, not a WorldArchitect player capability, so deleting it breaks nothing in the game. Pass B: it is a stray foreign artifact with no transport, durable-write, or tool-execution role for this product. **DELETE** |
| `claude_start.sh` (1908 lines) | Pass A: the Claude Code startup/orchestration script is developer workflow, not gameplay; deleting it would inconvenience local agent sessions but no player path calls it, and the model cannot supply local MCP orchestration. Pass B: it is environment setup (tunnels, cron, orchestration detection), not a campaign-domain transform. **KEEP** |
| `codebase_loc.sh` (1 line) | Pass A: a one-line LOC total superseded by `loc.sh`/`loc_simple.sh`; deleting it loses no capability since the fuller counters cover the same measurement. Pass B: pure measurement glue with no domain role. **DELETE** |
| `coverage.sh` | Pass A: the coverage test runner is CI/dev automation; deleting it would remove the coverage path, which the model cannot supply, and coverage is a load-bearing quality gate for a repo this size. Pass B: it only runs tests and aggregates coverage, never touching campaign fields. **KEEP** |
| `create_snapshot.sh` | Pass A: snapshot tooling that splits tracked text files into 5 outputs; deleting it removes a dev convenience, not a player capability, but it is still the documented way to take a text snapshot. Pass B: file handling only, no domain logic. **KEEP** |
| `create_worktree.sh` | Pass A: worktree provisioning is developer workflow; no player path uses it, but it is still the repo's documented worktree path (though repo AGENTS.md now prefers a different worktree tool, which is a docs question, not a deletion reason). Pass B: git plumbing only. **KEEP** |
| `deploy.sh` (841 lines) | Pass A: the production deploy path is load-bearing automation — deleting it breaks deployment itself, which the model cannot supply from a conversation log. Pass B: deployment, IAM verification, and queue provisioning are transport/ops, not campaign-domain transforms; its size argues for a later slim, not deletion. **KEEP** |
| `deploy_mcp.sh` | Pass A: deploys the Game MCP server to Cloud Run; deleting it breaks the MCP deploy path that players' clients depend on indirectly. Pass B: pure deployment transport, no field-aware game logic. **KEEP** |
| `fupdate.sh` | Pass A: a small git-update helper for the local checkout; deleting it is a minor dev inconvenience, not a player break, but it remains a live convenience with no replacement named. Pass B: git plumbing only. **KEEP** |
| `ghfixtests.sh` | Pass A: finds PRs with failing tests and offers Claude fixes; deleting it removes a triage convenience, not a player capability, but it is still an active workflow aid. Pass B: it queries GitHub state and drafts comments; it decides nothing about campaign data. **KEEP** |
| `infrastructure_common.sh` | Pass A: shared infra functions sourced by infrastructure scripts; deleting it breaks those scripts' config detection, which the model cannot supply. Pass B: environment/config plumbing with no campaign-domain awareness. **KEEP** |
| `install.sh` | Pass A: the top-level installer orchestrating sub-installers and a launchd reaper job; deleting it breaks fresh-machine setup, which is ops, not gameplay, but still load-bearing for developers. Pass B: installation only, no field transforms. **KEEP** |
| `install_mcp.sh` | Pass A: installs the WorldAI Tools MCP server into Claude Code; deleting it breaks the documented MCP setup path. Pass B: installer transport only. **KEEP** |
| `integrate.sh` (919 lines) | Pass A: the branch-integration helper is heavily used developer workflow; deleting it breaks the standard integrate-from-main flow, which no prompt can replace. Pass B: git/branch plumbing only, with no campaign data decisions. **KEEP** |
| `kill_dev_server.sh` (3 lines) | Pass A: kills the Flask dev server on port 8080; deleting a 3-line convenience loses nothing a developer cannot type, but it is harmless and still referenced as the dev-server stop path. Pass B: process management only. **KEEP** |
| `loc.sh` | Pass A: the GitHub-statistics/LOC script is reporting automation; deleting it removes a metrics path the model cannot regenerate from a log. Pass B: measurement only. **KEEP** |
| `loc_simple.sh` | Pass A: the comprehensive LOC counter (production vs test vs docs breakdown) is the repo's measurement tool; deleting it loses the breakdown that `codebase_loc.sh` cannot supply. Pass B: counting only, no domain transforms. **KEEP** |
| `local.sh` / `run_local_server.sh` (identical 972-line launchers) | Pass A: the local dev-server launcher is the documented `./run_local_server.sh` path; deleting it breaks local development serving, which the model cannot supply. Pass B: it launches Flask/MCP processes and manages ports/logs — transport and process management, not campaign logic; the duplicate (`local.sh` vs `run_local_server.sh`) should be merged to one name, but both files cannot simply be deleted while the docs reference the canonical one. **ADAPT** — merge to a single launcher (keep `run_local_server.sh`, delete the duplicate) |
| `push.sh` | Pass A: a commit-and-push convenience; deleting it is a trivial dev inconvenience, but it remains a live shortcut with no named replacement. Pass B: git plumbing only. **KEEP** |
| `resolve_conflicts.sh` | Pass A: a small PR conflict-resolution helper; deleting it removes a convenience, not a capability, and it is still usable for its narrow purpose. Pass B: git plumbing only. **KEEP** |
| `run_browser_tests.sh` | Pass A: sequences the browser test runs; deleting it breaks the documented browser-test entry point. Pass B: test orchestration only. **KEEP** |
| `run_e2e_tests.sh` | Pass A: the E2E runner with mock/real/capture modes is the documented E2E entry point; deleting it breaks end-to-end verification. Pass B: it runs tests and selects modes; it does not decide campaign facts. **KEEP** |
| `run_lint.sh` | Pass A: the lint entry point (Ruff/isort/mypy/Bandit) is a quality gate; deleting it removes the standard lint path. Pass B: static analysis only. **KEEP** |
| `run_parallel_mcp_tests.sh` | Pass A: runs MCP tests in parallel; deleting it removes a test-execution path. Pass B: test orchestration only. **KEEP** |
| `run_prototype_tests_vpython.sh` | Pass A: runs prototype tests under vpython; deleting it removes that execution path, though prototypes are by nature transitional. Pass B: test orchestration only. **KEEP** |
| `run_test_server.sh` | Pass A: start/stop/status for the Flask test server is load-bearing for local test runs. Pass B: process management only. **KEEP** |
| `run_tests.sh` (2105 lines) | Pass A: the required test runner (explicit file args, CI-simulation mode, worker/memory management) is the repo's central test path — referenced 22 times by workflows — and deleting it breaks test execution outright. Pass B: it is test transport and resource management, never a campaign-domain transform; its size warrants a later slim, not deletion. **KEEP** |
| `run_tests_with_coverage.sh` | Pass A: the coverage variant of the test runner; deleting it removes the coverage-gated run path that `coverage.sh` complements. Pass B: test orchestration only. **KEEP** |
| `run_ui_tests.sh` | Pass A: the UI/browser test runner is the documented UI verification path. Pass B: test orchestration only. **KEEP** |
| `schedule_branch_work.sh` | Pass A: schedules branch work (shell-function/PATH bootstrap); deleting it breaks that automation's environment setup. Pass B: environment plumbing only. **KEEP** |
| `setup_email.sh` | Pass A: interactive email setup for the backup system; deleting it removes the backup-email bootstrap, a live ops path. Pass B: configuration only. **KEEP** |
| `simple_integrate_test.sh` | Pass A: a contract test for `integrate.sh` branch protection; deleting it removes the guard that proves integrate.sh still protects branches. Pass B: it asserts script behavior only and touches no campaign data. **KEEP** |
| `start_game_mcp.sh` | Pass A: starts the Game MCP server on port 7000 with start/stop/status; deleting it breaks the documented game-MCP launch path. Pass B: process management/transport only. **KEEP** |
| `start_prod_server.sh` | Pass A: the production-mode launcher is the documented prod start path. Pass B: process management only. **KEEP** |
| `startup_llm.sh` | Pass A: configures a Vast.ai "Thinker" instance for qwen3-coder; deleting it removes a cloud-instance bootstrap that no prompt can replace, though it serves a narrow, possibly dated provisioning purpose. Pass B: provisioning only, no campaign logic. **KEEP** |
| `sync_branch.sh` | Pass A: synchronizes a local branch with a differently-named remote branch; deleting it removes a live git convenience. Pass B: git plumbing only. **KEEP** |
| `test_portability.sh` | Pass A: verifies infrastructure portability (config detection); deleting it removes the guard for the portability improvements it tests. Pass B: it asserts installer behavior only. **KEEP** |

## 3. `mvp_site/mocks/` — per-function (test infrastructure, not shipped gameplay)

The mocks are imported by offline/function tests only; no player turn path
imports them in production. Their verdicts therefore follow the test-infra
rule: keep what current offline tests need, delete what mirrors retired
behavior. Note: the repo AGENTS.md bans mocks in `testing_mcp/` and
`testing_ui/` (real-service-only), which does not retroactively delete this
legacy library — it only forbids new mock-based tests there.

| Unit | Pass A + Pass B justification, ending in verdict |
|---|---|
| `mock_firestore_service.py::MockFirestoreDocument::__init__`, `to_dict`, `get`, `exists`, `id` | Pass A: deleting these breaks every offline test that reads a mock document snapshot, and the model cannot supply an in-memory DocumentSnapshot from a log. Pass B: they implement the Firestore read surface (transport/durable-write stand-in) with no campaign-domain decisions — `get` only walks dotted field paths the caller names. **KEEP** |
| `mock_firestore_service.py::MockFirestoreClient::__init__`, `_initialize_sample_data` | Pass A: the in-memory store plus sample campaign/state/story seed is what makes offline tests runnable without Firebase; deleting it forces every such test onto real services. Pass B: seeding test data is a test fixture act, not a production field transform, and the sample data is clearly synthetic. **KEEP** |
| `mock_firestore_service.py::MockFirestoreClient::get_campaigns_for_user`, `get_campaign_by_id`, `get_campaign_game_state`, `get_game_state`, `get_story_context` | Pass A: these are the read half of the mock durable-write layer; deleting them breaks offline campaign/state/story tests outright. Pass B: they return deep copies of stored dicts with only a `max_turns` tail slice in `get_story_context` — a bounded-capacity read window, not a domain decision about which turns matter. **KEEP** |
| `mock_firestore_service.py::MockFirestoreClient::update_campaign_game_state`, `create_campaign`, `add_story_entry`, `update_campaign_title`, `update_campaign`, `delete_campaign`, `update_game_state` | Pass A: the write half of the mock store; deleting any of them breaks offline tests that exercise create/update/delete flows. Pass B: they store exactly what the caller passes (deep-copied), with only mechanical bookkeeping (`sequence_id` increment, timestamps, `last_played` refresh) — no re-interpretation of campaign facts; `add_story_entry`'s structured-field passthrough copies caller-supplied fields verbatim rather than deciding them. **KEEP** |
| `mock_firestore_service.py::MockFirestoreClient::reset`, `get_operation_stats`, `set_campaign_data`, `set_game_state_data`, `set_story_context` | Pass A: reset and seed setters are the test-control surface; deleting them makes tests order-dependent and unseedable. Pass B: they are test-only state manipulation, invisible to players, with no production field logic. **KEEP** |
| `mock_firestore_service.py::get_mock_firestore_client`, module `add_story_entry`, `get_campaign_by_id` | Pass A: the global-instance accessors are what test modules actually import; deleting them breaks those imports even though the class survives. Pass B: pure delegation to the global client, no logic of their own. **KEEP** |
| `mock_firestore_service_wrapper.py::get_client`, `get_campaigns_for_user`, `get_campaign_by_id`, `create_campaign`, `update_campaign`, `delete_campaign`, `get_game_state`, `update_game_state`, `update_state_with_changes`, `get_campaign_game_state`, `update_campaign_game_state`, `add_story_entry`, `get_story_context` | Pass A: the wrapper is the import surface `mvp_site/mocks/__init__.py` exposes, so deleting any function breaks its importing tests. Pass B: each function delegates to the mock client (or, for `update_state_with_changes`, applies caller-supplied changes) without adding domain judgment; the one bounded-capacity helper, `_truncate_log_json` (1000-char cap on log JSON), is a test-log size bound, not a gameplay transform. **KEEP** |
| `mock_llm_service.py::MockLLMResponse::__init__`, `__str__` | Pass A: the minimal response shape offline tests assert against; deleting it breaks every mock-LLM consumer. Pass B: it carries model text verbatim, deciding nothing. **KEEP** |
| `mock_llm_service.py::MockLLMClient::__init__`, `generate_content` | Pass A: the fake Gemini entry point that lets offline tests run with zero API cost; deleting it forces those tests onto real providers or deletes them. Pass B: it records the prompt and dispatches on canned patterns — keyword routing inside a test double is not the production intent-classification ban (which governs shipped routing), because no player turn ever reaches this code. **KEEP** |
| `mock_llm_service.py::MockLLMClient::_determine_response_type` | Pass A: the pattern router that picks which canned response a test scenario gets; deleting it collapses all mock responses to one shape and breaks scenario tests (HP discrepancy, location mismatch, mission completion). Pass B: its keyword matching selects fixtures, not live campaign facts, and never runs in production. **KEEP** |
| `mock_llm_service.py::MockLLMClient::_generate_initial_story`, `_generate_continue_story`, `_generate_hp_discrepancy`, `_generate_location_mismatch`, `_generate_mission_completion`, `_generate_validation_response`, `set_response_mode`, `reset` | Pass A: these canned responses are the fixtures scenario tests depend on; deleting them removes the discrepancy/mismatch/mission scenarios offline tests exist to cover. Pass B: they return fixed or fixture-derived text and never mutate live state; the structured JSON they emit mirrors the response schema tests validate against. **KEEP** |
| `mock_llm_service.py::get_mock_client`, `parse_state_updates_from_response` | Pass A: `get_mock_client` is the import surface for the global mock and must stay while the mock stays. Pass B: `parse_state_updates_from_response` is different — its own docstring says it mimics the legacy state parser "now deprecated", so it mirrors retired production behavior rather than any live contract, and deleting it breaks no live test target. **ADAPT** — keep `get_mock_client`; **DELETE** `parse_state_updates_from_response` (split verdict within this row: file-level KEEP, function-level DELETE for the parser) |
| `mock_llm_service_wrapper.py::get_client`, `generate_content`, `get_initial_story`, `continue_story` | Pass A: the wrapper is what tests import for story generation; deleting it breaks those tests' import surface. Pass B: thin delegation to `MockLLMClient` with prompt assembly for tests only; no live campaign fields are decided here. **KEEP** |
| `mvp_site/mocks/__init__.py` (module-level re-exports) | Pass A: deleting the package's public surface breaks every `from mvp_site.mocks import …` test import. Pass B: re-exports only, no logic. **KEEP** |
| `mvp_site/mocks/data_fixtures.py` (constants: `SAMPLE_CAMPAIGN`, `SAMPLE_GAME_STATE`, `SAMPLE_STORY_CONTEXT`, `SAMPLE_AI_RESPONSES`, `SAMPLE_STATE_UPDATES`) | Pass A: deleting the shared fixtures breaks every test that seeds from them; the model cannot supply stable, repeatable fixture bytes from a log. Pass B: static test data, not a transform at all. **KEEP** |
| `mvp_site/mocks/structured_fields_fixtures.py` (constants: `INITIAL_CAMPAIGN_RESPONSE`, `FULL_STRUCTURED_RESPONSE`, `GOD_MODE_RESPONSE`, …) | Pass A: the canonical structured-response fixtures that mock-LLM and UI tests assert against; deleting them removes the expected-shape reference. Pass B: static expected outputs, not live decisions. **KEEP** |
| `mvp_site/mocks/README.md`, `README_GRANULAR_MOCKS.md` | Pass A: documentation for the mock library; deleting it loses the usage contract but no executable capability. Pass B: docs only. **KEEP** |
| `mvp_site/bin/LICENSE.chromedriver` | Pass A: a license text for the Chromedriver binary; deleting it has no player effect but removes the legal notice for a bundled binary. Pass B: not code at all. **KEEP** |

## 4. `tools/` — per-function

| Unit | Pass A + Pass B justification, ending in verdict |
|---|---|
| `tools/localserver.sh::parse_port_robust_bash` | Pass A: robust port parsing (including descriptive PORT strings) is what lets the launcher survive odd environments; deleting it would make the launcher fail on non-numeric PORT values. Pass B: it parses a number with a range check — bounded-capacity/transport plumbing, no campaign awareness. **KEEP** |
| `tools/localserver.sh::cleanup_servers` | Pass A: the interactive cleanup prompt is dev convenience for stopping stray servers; deleting it only removes the prompt, not the ability to kill servers. Pass B: process management only. **KEEP** |
| `tools/localserver.sh` (main flow: venv activation, port check, logging setup, server start, validation) | Pass A: the local-server launcher is a live developer path (it sources `scripts/server-utils.sh` and starts `mvp_site/main.py serve`); deleting it breaks local serving from `tools/`. Pass B: it launches and validates a server process — transport/process management, and its logging is dev-time logging, not player-turn logging, so §6.1's async rule does not force a change here. **KEEP** |

## 5. Docs areas — per-file (not code; judged as records, not gameplay)

| File | Pass A + Pass B justification, ending in verdict |
|---|---|
| `evaluation_reports/task_111_zen_mcp_evaluation.md`, `task_112_context7_mcp_evaluation.md`, `task_113_sequential_thinking_mcp_evaluation.md`, `task_119_claude_simone_evaluation.md`, `task_120_mcp_servers_general_evaluation.md` | Pass A: dated Jan 2025 evaluations of third-party MCP servers; deleting them loses historical vendor-assessment records, but no player capability and no current decision depends on them, and the model cannot regenerate dated evaluations. Pass B: prose records, not transforms. **KEEP** as archive (deleting history is not required by either pass; they cost nothing and are not executed) |
| `benchmark_results/final-benchmark-report.md`, `preliminary-analysis.md` | Pass A: Genesis-vs-Ralph orchestrator benchmark reports; deleting them loses the measurement record behind an orchestration choice, but nothing executes them. Pass B: prose records. **KEEP** as archive |
| `experiments/EXPERIMENT_BRANCH_MAPPING.md`, `EXPERIMENT_IMPROVEMENTS_V2.md`, `RESEARCH_HONESTY_REFLECTION.md`, `RESEARCH_TRANSLATION_ANALYSIS.md`, `TRIPLE_BLIND_EXPERIMENT_RESULTS.md`, `TRIPLE_BLIND_EXPERIMENT_SUMMARY.md`, `WHY_BEHAVIORAL_WARNINGS_WON.md` | Pass A: the triple-blind anti-hallucination experiment record (specification vs behavioral warnings); deleting it loses the evidence that behavioral warnings won, which informed prompt design, but no code path reads these files. Pass B: prose records. **KEEP** as archive |

## 6. `scripts/` top-level `.py` — per-file (ops, not gameplay)

CI-reference ground: the workflow grep found 100 `scripts/…` references,
including `audit_dice_rolls.py`, the `check_*` guards, the `ci_*` selectors,
`cost_report_lib.py`, the daily reports, `deploy_common.sh`,
`shared_config.sh`, `sort_beads_jsonl.py`, `validate_imports.py`, and the
TTV tools. A file named in that list is treated as live automation (KEEP)
unless its own header says it is retired/superseded.

| File | Pass A + Pass B justification, ending in verdict |
|---|---|
| `_atomic_write.py` | Pass A: dependency-free atomic writes for small JSON evidence artifacts, imported by evidence writers; deleting it risks partial-file evidence on kill, which the model cannot prevent. Pass B: filesystem durability primitive, no campaign fields. **KEEP** |
| `_beads_atomic_write.py` | Pass A: the shared atomic JSONL writer for Beads canonicalization scripts; deleting it breaks both `_beads_jsonl_union.py` and `sort_beads_jsonl.py`. Pass B: durability primitive only. **KEEP** |
| `_beads_jsonl_union.py` | Pass A: lossless additive union of Beads JSONL files used by the worktree migration; deleting it breaks that migration and its guarding tests. Pass B: ledger merging, no campaign-domain content. **KEEP** |
| `_test_user_filter.py` | Pass A: shared test-user email matcher used by several scripts to exclude synthetic users from real-user reports; deleting it breaks those filters. Pass B: identity classification for reporting hygiene, not a gameplay decision. **KEEP** |
| `ablate_code_execution_schema.py` | Pass A: a one-off real-API ablation (schema × streaming matrix for code_execution stability) whose question is answered and whose cells are recorded; deleting it removes no live capability. Pass B: an experiment probe, not a player-path component. **DELETE** |
| `adjustment_proof_matrix.py` | Pass A: repeatable red/green proof manifests for backend adjustments; deleting it removes the repeatable proof path for future adjustments, which ad-hoc runs cannot replace. Pass B: proof scaffolding and manifest validation, no live field transforms. **KEEP** |
| `aggressive_test_reducer.py` | Pass A: the 152→80 test-reduction program's eliminator; the reduction already happened, and no live workflow invokes it, so deleting it changes no current suite. Pass B: a completed optimization program, not player infrastructure. **DELETE** |
| `analyze_coverage_impact.py` | Pass A: the before/after analysis for that same completed test optimization; deleting it loses only a historical report generator. Pass B: reporting only. **DELETE** |
| `analyze_git_stats.py` | Pass A: reusable git/PR/DORA metrics analysis with no expiry date; deleting it removes a reporting tool developers still run. Pass B: repository analytics, no campaign data. **KEEP** |
| `analyze_memory_quality.py` | Pass A: a reusable diagnostic for core-memory duplicates and quality scores against a live campaign; deleting it removes a debugging tool for the memory feature. Pass B: read-only analysis, no writes or field decisions. **KEEP** |
| `analyze_org_repos.py` | Pass A: a reusable org-wide LOC analysis that clones/updates repos; deleting it removes a reporting tool, not a player capability. Pass B: analytics only. **KEEP** |
| `archive_openrouter_release_receipt.py` | Pass A: a one-shot receipt-retention step before a temporary build context is removed; once run, its effect is the retained receipt, and re-running it is meaningless. Pass B: provenance housekeeping, not a live path. **DELETE** |
| `aside_web_advice_collector.py` | Pass A: the automated /web-advice driver for multi-model reviews; deleting it removes a reusable review driver. Pass B: it drives external review tools, deciding nothing about campaigns. **KEEP** |
| `audit_dice_rolls.py` | Pass A: the anti-cheat dice audit (1736 lines, collection-group queries, statistical analysis) is the §6.2 audit trail itself; deleting it removes the fabrication detector, which the model cannot self-supply. Pass B: it reads story entries and reports statistics; it never resolves dice on a turn (that stays on the turn path) and never rewrites rolls. **KEEP** |
| `audit_helpers.py` | Pass A: shared chi-square/Cramér's-V/impossible-face helpers imported by the dice audit and its warning-gate tests; deleting them breaks the audit's statistics. Pass B: pure statistics over already-recorded rolls, not a transform of live game state. **KEEP** |
| `backfill_alexiel_core_memories.py` | Pass A: a one-campaign backfill (Alexiel) that classifies story entries and persists core memories; once run, its effect is in Firestore and the script has no second use. Pass B: a completed migration, not a live path. **DELETE** |
| `backfill_spell_slots_shape.py` | Pass A: a one-off legacy spell-slot normalization (dry-run default, `--apply` writes); the migration's value is the normalized data, not the script, and no workflow reruns it. Pass B: a completed data fix, not a player-path transform. **DELETE** |
| `bq_migrate_add_revision_id.py` | Pass A: a one-shot BigQuery column migration whose own header says to run it once after the schema-fix PR; the column now exists or the migration is moot. Pass B: schema housekeeping, not gameplay. **DELETE** |
| `bq_migrate_ttl.py` | Pass A: a one-shot TTL bump for six forensic tables; once applied, the setting persists in BigQuery and the script has no recurring role. Pass B: ops housekeeping only. **DELETE** |
| `build_cutover_preview_overlay.py` | Pass A: builds the receipt-bound cutover-preview overlay that `frontend_preview_release.py` refuses to start without when present; deleting it breaks preview-deploy construction. Pass B: deployment artifact assembly, no campaign fields. **KEEP** |
| `build_srd_class_corpus.py` | Pass A: the Phase-1 SRD corpus generator for the RAG class-lookup feature; with prompt RAG retired (per the precompute-deps regression tests), its output feeds a retired feature, so deleting it breaks no live path. Pass B: a corpus builder for a retired feature. **DELETE** |
| `cache_busting.py` | Pass A: deploy-time content-hash cache busting, referenced by the Dockerfile path (the `.sh` wrapper is the retired piece, not this module); deleting it breaks hashed-asset serving. Pass B: filename hashing and HTML reference updates are transport/caching, not campaign logic. **KEEP** |
| `calibrate_gemini_token_estimator.py` | Pass A: compares local token estimates against Gemini countTokens on Firestore samples; deleting it removes the calibration tool for the token estimator used in bounded-capacity budgeting. Pass B: measurement only, and its budgeting relevance is capacity, an allowed server role. **KEEP** |
| `campaign_analyzer.py` | Pass A: a Milestone 0.4 desync analyzer (extracts campaign data, classifies desync patterns); Milestone 0.4 is closed, and no live workflow runs it, so deleting it loses only a historical diagnostic. Pass B: read-only analysis of closed-milestone data. **DELETE** |
| `campaign_manager.py` | Pass A: the unified campaign operations CLI (query by name, safe delete, email→UID, batch ops) is still the operator's tool for campaign administration; deleting it removes the safe-delete path, which the model cannot execute. Pass B: it performs operator-authorized durable writes (deletes) on explicit command, not autonomous gameplay decisions. **KEEP** |
| `campaign_selector_0.4.py`, `campaign_selector_mock.py`, `campaign_selector_real.py` | Pass A: Milestone 0.4 test-campaign selectors (desync-issue sampling, mock and real variants); the milestone is closed and selection already happened, so deleting them breaks no live test. Pass B: closed-milestone sampling tools. **DELETE** |
| `capture_collapsed_choices_evidence.py`, `capture_ip_wizard_screenshot.py`, `capture_ip_wizard_video_evidence.py`, `capture_quick_hide_evidence.py`, `capture_share_video_evidence.py`, `capture_scene_provider_rejection_backend.py` | Pass A: one-off PR evidence captures (collapsed choices, IP wizard, quick-hide rebrand, share video, scene rejection) whose PNGs/videos are already published as PR evidence; deleting them removes no live capability and no test depends on them. Pass B: evidence automation for closed PRs. **DELETE** |
| `check_agy_json_contract.py` | Pass A: a reviewer guard for AGY JSON-mode parser strictness, referenced by CI; deleting it removes a live static guard. Pass B: static code review, no runtime field decisions. **KEEP** |
| `check_bead_jsonl_sort.py` | Pass A: the CI ordering invariant for `.beads/issues.jsonl`, referenced by workflows; deleting it lets sort-order noise return. Pass B: ledger hygiene only. **KEEP** |
| `check_codex_skill_mirror.py` | Pass A: the skill-mirror discoverability guard, referenced by CI and guarded by its own tests; deleting it lets invisible mirror entries return silently. Pass B: static repo hygiene. **KEEP** |
| `check_evidence_no_blobs.py` | Pass A: the CI check enforcing gist-hosted evidence (no committed binaries), referenced by workflows; deleting it reopens the docs/evidence blob problem. Pass B: repo hygiene only. **KEEP** |
| `check_function_loc_ratchet.py` | Pass A: the god-function LOC ratchet, referenced by CI; deleting it removes the accretion guard on core modules. Pass B: static measurement. **KEEP** |
| `check_living_world.py` | Pass A: the living-world diagnostic (reads Firestore for a campaign's world updates); deleting it removes the §6.3 living-world observability tool, though it never affects a turn. Pass B: read-only diagnostics, consistent with §6.3's async-tick model since it only observes ticks. **KEEP** |
| `check_narrative_response_schema_ci.py`, `check_narrative_response_schema_required.py` | Pass A: CI schema guards (maxLength leaves; required `dice_rolls`/`action_resolution`/`planning_block` in the prompt schema) referenced by workflows; deleting them removes the regression guards for issue #9021 and schema validity. Pass B: they validate the model-facing contract (prompt/schema), which is exactly the model-supply surface, not a server field transform. **KEEP** |
| `check_openrouter_signin_release.py` | Pass A: the pre-deployment contract validator for the OpenRouter sign-in release; deleting it removes a fail-closed release gate. Pass B: release verification, no gameplay decisions. **KEEP** |
| `check_prompt_agnosticism.py` | Pass A: the CI lint enforcing campaign-agnostic prompts (banned-name scan), referenced by workflows; deleting it lets campaign-specific names leak into shared prompts. Pass B: prompt hygiene, not a runtime transform. **KEEP** |
| `check_prompt_centralization.py` | Pass A: the CI ratchet for one-shared-rule-in-one-file, referenced by workflows with a baseline; deleting it lets prompt duplication return. Pass B: static prompt hygiene. **KEEP** |
| `check_schema_coverage.py` | Pass A: checks game_state paths used in code against the canonical schema; deleting it removes the schema-drift detector. Pass B: static coverage analysis, no runtime decisions. **KEEP** |
| `check_skip_policy.py` | Pass A: enforces the test-skip policy (legitimate environmental skips vs lazy avoidance); deleting it lets unjustified skips accumulate. Pass B: test hygiene only. **KEEP** |
| `ci_duration_observations.py` | Pass A: imports real `run_tests.sh` duration records into a reviewed snapshot, referenced by CI; deleting it breaks duration-snapshot maintenance. Pass B: CI telemetry only. **KEEP** |
| `ci_integration_optimizer.py` | Pass A: a CI matrix optimizer for a 15-minute CI target; deleting it removes a planning tool, though its generated workflow may already be committed — its header presents it as a generator, and no workflow re-invokes it on every run. Pass B: workflow generation, not gameplay. **DELETE** (its output, if adopted, lives in the workflows themselves) |
| `ci_test_duration_sharding.py` | Pass A: deterministic duration-weighted CI sharding, referenced by workflows and guarded by sharding tests; deleting it breaks shard assignment. Pass B: CI scheduling only. **KEEP** |
| `ci_test_impact_analysis.py` | Pass A: the TIA test selector (changed-file → test-file mapping), referenced by workflows and heavily guarded; deleting it breaks selective CI. Pass B: test selection, no campaign decisions. **KEEP** |
| `cleanup_debug_info.py` | Pass A: a one-campaign debug_info bloat cleanup (33MB campaign, 88% debug_info); once run, the bloat is gone and the script's hardcoded campaign makes it non-reusable. Pass B: a completed data cleanup. **DELETE** |
| `cleanup_failing_tests.py` | Pass A: systematically deletes failing tests "not worth fixing" with backup/reporting; deleting this tool is safe because its philosophy (delete failing tests rather than fix them) is one the repo should not keep automating, and no workflow runs it. Pass B: test-deletion automation with no player role. **DELETE** |
| `cleanup_orphan_fixture_campaigns.py` | Pass A: a reusable dry-run-first orphan-fixture cleaner for Firestore; deleting it removes the safe cleanup path for CI orphans, which accumulate continuously. Pass B: operator-authorized durable deletes on explicit `--apply`, not autonomous gameplay. **KEEP** |
| `cleanup_stale_lua_flags.py` | Pass A: a one-purpose stale level-up-flag migrator; deleting it removes a repair tool for a specific flag shape, but the flags it targets are historical and no workflow reruns it. Pass B: a completed-leaning migration. **DELETE** |
| `collect_real_gemini_before_after.py` | Pass A: a before/after evidence collector for one PR (#10322) across two deployed servers; the evidence is collected and the PR is closed, so deleting it breaks nothing live. Pass B: closed-PR evidence tooling. **DELETE** |
| `combat_prefix_stability_probe.py`, `compaction_stability_probe.py`, `prefix_stability_probe.py` | Pass A: deterministic cached-prefix stability probes (no LLM) that answer whether system-instruction prefixes are byte-stable; they are reusable measurement tools for the prompt-caching work, not single-PR artifacts. Pass B: measurement only, no live transforms. **KEEP** |
| `compare_beads_jsonl_semantic.py` | Pass A: the semantic comparator used by `check_beads_jsonl_drift.sh`; deleting it breaks the drift check's comparison step. Pass B: ledger comparison only. **KEEP** |
| `compare_productivity.py` | Pass A: a one-off developer-productivity vs industry-benchmark comparison using web search; deleting it loses only a historical report generator. Pass B: reporting only. **DELETE** |
| `context_monitor.py` | Pass A: a context-health monitor for Claude history with explicit never-modify protection; deleting it removes a local hygiene tool, not a player capability. Pass B: local history monitoring only. **KEEP** |
| `copy_campaign.py` | Pass A: the campaign-copy CLI (Firestore copy-as-is, dry-run, story cutoff, owner rebind) is the operator tool behind test copies and the repro flows, guarded by its own tests; deleting it breaks copy/repro workflows. Pass B: it copies stored data verbatim without modifying fields, which is durable-write transport, not a domain reinterpretation. **KEEP** |
| `cost_report_lib.py` | Pass A: the shared library behind the daily GCP/GitHub cost emails, referenced by both daily reporters and their tests; deleting it breaks both cron reports. Pass B: billing aggregation and reporting, no campaign-domain decisions. **KEEP** |
| `count_command_usage.py` | Pass A: counts slash-command invocations from Claude history; deleting it removes a reusable usage-analysis tool. Pass B: local history analytics only. **KEEP** |
| `crdt_merge.py` | Pass A: pure LWW CRDT merge functions for the memory-backup system, imported by backup code and guarded by CRDT tests; deleting them breaks backup merging. Pass B: last-write-wins merging is a durable-write conflict rule (an allowed server role), applied to backup records, not a gameplay-field reinterpretation. **KEEP** |
| `create_sample_data.py` | Pass A: creates sample Firebase data for analytics testing; deleting it removes a test-data seeder that analytics tests can re-run. Pass B: test seeding only, clearly synthetic. **KEEP** |
| `daily_campaign_report.py` | Pass A: the daily campaign activity report (DAU/WAU, token breakdown, cost estimates) is a live cron report; deleting it removes operator visibility the model cannot supply. Pass B: read-only aggregation and reporting. **KEEP** |
| `daily_dice_audit.py` | Pass A: the daily dice-audit cron that queries active campaigns, runs the audit, and emits a provenance manifest — the §6.2 audit trail in scheduled form; deleting it removes daily anti-cheat coverage. Pass B: it reports and manifests; it never resolves dice or rewrites rolls. **KEEP** |
| `daily_gcp_cost_report.py`, `daily_gh_cost_report.py` | Pass A: thin cron wrappers around `cost_report_lib.py`, each referenced by its own daily workflow; deleting either breaks that day's cost email. Pass B: reporting only. **KEEP** |
| `daily_prompt_context_report.py` | Pass A: the daily prompt-context breakdown report from BigQuery telemetry; deleting it removes a live observability report. Pass B: read-only telemetry aggregation. **KEEP** |
| `dark_factory_e2e_smoke.py` | Pass A: a thin fail-closed smoke adapter for the installed Dark Factory CLI; deleting it removes that smoke path, though it is an adapter for an external tool. Pass B: smoke-test transport only. **KEEP** |
| `dead_code_eliminator.py` | Pass A: part of the completed test-reduction program (finds tests for unused code); the reduction is done and no workflow runs it. Pass B: completed-program tooling. **DELETE** |
| `debug_firebase_connection.py` | Pass A: a Firebase connection debugger; deleting it removes a diagnostic, but it is a trivial one-off debug script with no tests and no workflow role. Pass B: diagnostics only. **DELETE** (its few lines are reproducible on demand; keeping every ad-hoc debugger is not load-bearing) |
| `debug_rate_limit_live.py` | Pass A: a 101-line file with no docstring and no functions (a live rate-limit debug snippet); deleting it loses no named capability. Pass B: an ad-hoc snippet, not infrastructure. **DELETE** |
| `debug_state_updates_issue.py` | Pass A: a demonstration script for the old STATE_UPDATES_PROPOSED parsing issue and its fix; the fix shipped and the demo's purpose is historical explanation. Pass B: a closed-issue demo. **DELETE** |
| `deduplicate_beads_jsonl.py` | Pass A: dedupes `.beads/issues.jsonl` by stable id with a defined merge strategy; deleting it removes a ledger-maintenance tool still usable on demand. Pass B: ledger hygiene only. **KEEP** |
| `delete_user_firestore_data.py` | Pass A: the user-data deletion tool (fresh-login simulation, GDPR-style erasure) guarded by its own tests; deleting it removes the operator's erasure path, which the model cannot execute. Pass B: operator-authorized durable deletes on explicit command, not gameplay logic. **KEEP** |
| `dependency_analyzer.py`, `test_dependency_analyzer.py`, `test_test_dependency_analyzer.py` | Pass A: the PR #1313 intelligent test-selection analyzer and its tests; superseded in practice by `ci_test_impact_analysis.py` (the live TIA selector referenced by workflows), so deleting these removes a superseded selector, not the live one. Pass B: superseded CI tooling. **DELETE** |
| `deploy_context_optimization.py` | Pass A: integrates a context-optimization solution into Claude Code CLI with claimed 43% token reduction; deleting it removes a deploy-integration tool whose optimization is either already deployed or abandoned — its header describes a one-time integration, not a recurring path. Pass B: a one-time integration script. **DELETE** |
| `detect_inline_imports.py`, `simple_inline_detector.py`, `test_inline_detector.py`, `import_optimizer.py` | Pass A: inline-import detection/optimization tools; deleting them removes lint-adjacent analysis, but `validate_imports.py` (CI-referenced) is the live import guard, and these are exploratory/optimization companions with no workflow role. Pass B: static analysis companions, not live gates. **DELETE** |
| `detect_xp_writeback_anomalies.py` | Pass A: a detector for XP-writeback anomalies from BigQuery telemetry (issue #9561); deleting it removes the anomaly detector for a specific, still-possible failure mode (zero XP on a completed kill). Pass B: read-only telemetry detection, no live field writes. **KEEP** |
| `diagnose_campaign_issues.py`, `investigate_campaign_issues.py` | Pass A: campaign diagnostics (mobile/desktop discrepancies, dice-not-showing, god-mode-ignoring) that operators still run against live campaigns; deleting them removes debugging tools for live issues. Pass B: read-only diagnostics. **KEEP** |
| `download_campaign.py` | Pass A: the campaign download/export CLI (single/batch/all-users) still used for evidence and analysis; deleting it removes the export path. Pass B: read-only export of stored data, no reinterpretation. **KEEP** |
| `download_personalities.py` | Pass A: downloads and saves AI personalities; deleting it removes a small data-fetch tool with no workflow role and no tests. Pass B: a data-fetch convenience, not infrastructure. **DELETE** |
| `elimination_safety_checker.py` | Pass A: part of the completed test-reduction program (validates elimination safety); the reduction is done. Pass B: completed-program tooling. **DELETE** |
| `es_campaign_duplicate_batch.py` | Pass A: real-Firestore evidence for resilient campaign duplication, tied to a specific evidence need; deleting it removes a one-off evidence generator, not a live path. Pass B: closed-evidence tooling. **DELETE** |
| `evidence_openrouter_nonstreaming_bq_path10.py` | Pass A: a real-LLM test for one BigQuery codepath (path 10); deleting it removes a single-path coverage probe whose path is either covered by the suite now or was a one-time coverage exercise. Pass B: a single-path probe, not infrastructure. **DELETE** |
| `extract_replay_fixtures.py` | Pass A: extracts raw-model replay fixtures from an organic level-up bundle for Layer-2 tolerance tests; deleting it removes the fixture-generation path those tests depend on for regeneration. Pass B: fixture extraction from recorded evidence, no live decisions. **KEEP** |
| `fetch_campaign_gamestate.py` | Pass A: fetches and displays a campaign's game state from Firestore; deleting it removes a small operator diagnostic. Pass B: read-only display. **KEEP** |
| `fetch_pr_data.py` | Pass A: a 62-line PR-data fetcher with no docstring and no workflow role; deleting it loses a trivial fetch helper reproducible via `gh`. Pass B: an ad-hoc snippet. **DELETE** |
| `firebase_collection_group_analytics.py`, `firebase_user_analytics.py` | Pass A: reusable Firebase analytics (collection-group and per-user campaign/entry counts with CSV export); deleting them removes reporting tools operators rerun. Pass B: read-only analytics. **KEEP** |
| `fix_debug_mocks.py`, `fix_llm_mocks.py`, `fix_mvp_imports.py`, `fix_mvp_site_imports.py` | Pass A: one-off codemods (mock-object fixes, import rewrites) whose edits are already in the tree; re-running them is either a no-op or a risk, and no workflow invokes them. Pass B: completed codemods. **DELETE** |
| `fix_dice_notation_concat.py` | Pass A: a data fix for historical Bardic Inspiration notation concatenations on specific campaigns; once applied, the stored notations are clean and the script has no recurring role. Pass B: a completed data fix. **DELETE** |
| `fix_god_mode_directives.py` | Pass A: a cleanup for bloated God Mode directives (context-window fix); the cleanup already ran and directives are now managed by the live system. Pass B: a completed cleanup. **DELETE** |
| `generate_campaign_templates.py` | Pass A: generates campaign template payloads via live LLM/Firebase for embedding in constants; deleting it removes the regeneration path for templates, though templates already exist. Pass B: a template-generation tool, not a live path — but regeneration is its purpose, and it remains the only sanctioned way to refresh those payloads. **KEEP** |
| `generate_models.py` | Pass A: a 24-line stub whose own header says Pydantic models are now runtime-generated and the script is superseded; deleting it removes a dead stub. Pass B: a tombstone, not a path. **DELETE** |
| `generate_typeddict.py` | Pass A: generates TypedDicts from the game-state schema into `mvp_site/schemas/typed_dicts.py`; deleting it removes the regeneration path for a checked-in generated file. Pass B: code generation from a schema (an allowed authoring aid), not a runtime transform. **KEEP** |
| `generate_wiki_html.py` | Pass A: generates static wiki HTML for GitHub Pages, referenced by CI; deleting it breaks wiki publishing. Pass B: static-site generation, no campaign logic. **KEEP** |
| `grade_core_memory_evidence.py` | Pass A: runs frozen blinded packets through one AGY judge for the core-memory evidence study; deleting it removes the grading path for that study's packets. Pass B: study tooling, not a player path. **KEEP** |
| `green_merge_nonprod.py` | Pass A: the fail-closed gate-state reporter for open PRs (deliberately incapable of merging), referenced by workflows; deleting it removes the gate snapshot operators read. Pass B: reporting only, with merge authority explicitly outside it. **KEEP** |

| `lint_workflow_discipline.py` | Pass A: the workflow-discipline lint (self-hosted runner rules, concurrency groups) for CI YAML; deleting it removes a structural CI guard. Pass B: static workflow analysis only. **KEEP** |
| `llm_mock.py` | Pass A: a Milestone 0.4 mock Gemini API for simulation; the milestone is closed and the live mock surface is `mvp_site/mocks/`, so deleting this older mock breaks no current test. Pass B: a superseded milestone mock. **DELETE** |
| `mcp_stdio_wrapper.py` | Pass A: a 17-line stdio wrapper that runs the WorldAI MCP server for Claude Code; deleting it breaks the documented stdio launch path. Pass B: transport wrapper only. **KEEP** |
| `mock_hypothesis.py` | Pass A: a no-op hypothesis stand-in so CRDT tests run without the dependency; deleting it breaks CRDT test collection where hypothesis is absent. Pass B: test-only shim. **KEEP** |
| `monitor_dice_corrections.py` | Pass A: monitors dice-fabrication self-correction effectiveness in production; deleting it removes the §6.2 anti-cheat effectiveness measurement. Pass B: read-only monitoring, no turn-path role. **KEEP** |
| `package_daily_campaign_report.py` | Pass A: packages the daily report for a separately verified OAuth sender, referenced by CI; deleting it breaks the verified-delivery path. Pass B: packaging/delivery only. **KEEP** |
| `pr6734_strict_es_evidence.py` | Pass A: a strict /es evidence runner for one PR (stale rewards UI suppression); the PR is closed and its evidence collected. Pass B: closed-PR evidence tooling. **DELETE** |
| `pr_autonomy_metrics.py` | Pass A: computes PR autonomy metrics with delta weighting, referenced by CI; deleting it removes a live metrics pipeline. Pass B: repository analytics only. **KEEP** |
| `pr_comment_formatter.py`, `pr_comment_formatter_examples.py` | Pass A: structured PR-comment formatting and its examples; deleting them removes a reply-formatting utility, but no workflow depends on it and it formats comments, not decisions. Pass B: comment formatting only. **DELETE** (examples file is doubly non-load-bearing) |
| `preflight_model.py` | Pass A: validates/downloads the FastEmbed classifier model as a preflight; deleting it removes the model-availability gate the serving path relies on. Pass B: model provisioning, not a campaign decision. **KEEP** |
| `preflight_model_docker.py` | Pass A: the Docker-build preflight that downloads the FastEmbed model without mvp_site imports (layer-caching design); deleting it breaks Docker builds' model layer. Pass B: build-time provisioning only. **KEEP** |
| `probe_8537_cap_raise_evidence.py`, `probe_gemini_thinking_levels.py`, `probe_memory_compaction_and_scrub.py`, `probe_memory_delta_branches.py`, `probe_schema_maxlength_enforcement.py` | Pass A: single-question real-API probes (compaction cap raise, thinking levels, memory scrub tables, memory_delta contract, maxLength enforcement) whose evidence is already recorded in their PRs/beads; deleting them removes no live path. Pass B: closed-question probes. **DELETE** |
| `prompt_cache_baseline.py`, `prompt_cache_power.py` | Pass A: the exact-revision prompt-cache baseline runner/bundle verifier and the reachability power simulator — reusable measurement instruments for the prompt-caching program, not single-run scripts. Pass B: measurement/simulation only. **KEEP** |
| `prompt_context_breakdown.py` | Pass A: prints per-turn prompt-context breakdowns from BigQuery rows; deleting it removes a reusable telemetry inspection tool. Pass B: read-only telemetry. **KEEP** |
| `prompt_templates.py` | Pass A: Milestone 0.4 prompt templates for different approaches (baseline, structured JSON, XML, chain-of-thought); the milestone is closed and live prompts live in `mvp_site/prompts/`. Pass B: superseded milestone artifacts. **DELETE** |
| `provision_openrouter_firestore_indexes.py` | Pass A: provisions/verifies Firestore indexes for OpenRouter auth cleanup; deleting it removes the index-provisioning path for a live auth feature. Pass B: infrastructure provisioning, no campaign decisions. **KEEP** |
| `prs_per_month.py` | Pass A: reusable monthly PR/contribution analysis across org repos; deleting it removes a reporting tool. Pass B: analytics only. **KEEP** |
| `publish_quickhide_gist.py` | Pass A: publishes the PR #9301 evidence bundle to a gist; the bundle is published and the PR closed. Pass B: closed-PR publishing. **DELETE** |
| `pytest_cache_optimizer.py` | Pass A: a pytest cache/grouping plugin for test optimization; deleting it removes a test-execution optimization, not a correctness gate, and it belongs to the completed optimization program. Pass B: test-runner optimization. **DELETE** |
| `query_directives.py` | Pass A: queries/manages God Mode directives for campaigns (list, debug-missing, add, drop); deleting it removes the operator's directive-management CLI. Pass B: operator-authorized durable writes on explicit command. **KEEP** |
| `reap_local_servers.py` | Pass A: stops leased local servers idle past TTL (with lease/lock handling); deleting it removes the local-server hygiene path. Pass B: process management only. **KEEP** |
| `recheck_field_inventory.py` | Pass A: a deterministic field-inventory recheck for PR #4534 production samples; the recheck already ran and its findings are recorded. Pass B: closed-PR verification. **DELETE** |
| `recon_organic_level_up.py` | Pass A: repeatable organic level-up recon (optional clone, two streaming turns); deleting it removes a reusable recon tool for leveling investigations. Pass B: it drives real turns against a test copy, not production campaigns, and writes only to the copy. **KEEP** |
| `regenerate_dragon_knight_canonical.py` | Pass A: the ONLY sanctioned way to update the Dragon Knight fast-path SHA in constants — deleting it removes the sanctioned regeneration path and invites hand edits. Pass B: hash regeneration from the frontend source of truth, not a gameplay decision. **KEEP** |
| `repair_orphaned_sessions.py` | Pass A: offline repair for orphaned level-up sessions (explicit `--apply`); deleting it removes a repair tool for a specific, still-possible session state. Pass B: operator-authorized repair on explicit command. **KEEP** |
| `repro_copy_campaign.py` | Pass A: the copy-and-replay repro (canonical + variant copies, real local server, streaming turns) guarded by its own tests; deleting it removes the primary repro tool for campaign bugs. Pass B: it operates on test copies only and never mutates the source campaign. **KEEP** |
| `repro_core_memory_two_models.py` | Pass A: captures two real streaming memory-omission attempts from a preserved baseline; deleting it removes a baseline-capture tool for a specific memory study. Pass B: study capture, not a live path. **DELETE** (its baseline is preserved; the capture already happened) |
| `resolve_pr_author_firebase_uid.py` | Pass A: resolves a PR author's email to a Firebase UID for the dice-tests workflow scoping, referenced by CI; deleting it breaks that workflow's scoping. Pass B: identity resolution for test scoping, not gameplay. **KEEP** |
| `retention_nudge.py` | Pass A: the retention-nudge script (inactive users, LLM-generated story development, summary email, dry-run default) is a live engagement automation; deleting it removes that program, which the model cannot run on a schedule by itself. Pass B: it writes story nudges only in execute mode with dry-run default, and its writes are operator-scheduled, not turn-path decisions — flagged, not condemned: the nudge content is model-generated via an explicit call, so no server field transform is involved. **KEEP** |
| `rewards_gold_loot_ablation.py` | Pass A: bounded reward-schema ablations from immutable specimens (preparation never touches the network); deleting it removes the ablation instrument for reward-schema experiments. Pass B: experiment tooling with explicit digests, not a live path. **KEEP** |
| `run_pr_3491_parallel_tests.py` | Pass A: parallel test execution for one PR (#3491) against GCP preview and local servers; the PR is closed. Pass B: closed-PR test tooling. **DELETE** |
| `run_web_advice_ip_wizard.py` | PassA: runs /web-advice multi-model review for PR #9265 via Chrome CDP; the review is done and the PR closed. Pass B: closed-PR review tooling. **DELETE** |
| `runner_health_score.py` | Pass A: the runner health scoreboard (check/reset/update/scoreboard), referenced by CI; deleting it removes the quarantine-visibility path. Pass B: CI telemetry only. **KEEP** |
| `scene_illustration_design_examples.py` | Pass A: one-off design evidence (sample scene illustrations via OpenRouter + Firestore) for a PR #10564 design composite job; the composite is done. Pass B: closed-PR design evidence. **DELETE** |
| `scene_video_playback.py` | Pass A: plays evidence videos in isolated Chromium and records end-state proof — a reusable evidence-verification tool, not tied to one PR. Pass B: evidence verification only. **KEEP** |
| `screen_core_memory_prompts.py` | Pass A: a private generation-only Gemini screen for the core-memory prompt contract (fresh construction, never imports the provider, never writes state); deleting it removes an exploratory contract screen. Pass B: exploratory, non-writing tooling. **KEEP** |
| `scrub_class_4_residue.py` | Pass A: a one-time migration scrubbing stale level_up flags for a specific campaign; once run, the residue is gone. Pass B: a completed migration. **DELETE** |
| `semantic_scene_similarity_pack.py` | Pass A: builds semantic scene-repeat review packs from story entries for reviewer LLM subagents; deleting it removes a reusable review-pack builder for duplicate-scene investigations. Pass B: read-only pack building, no live writes. **KEEP** |
| `set_openrouter_signin_flag.py`, `set_scene_illustration_flag.py` | Pass A: one-field Firestore flag setters for OpenRouter sign-in and scene illustrations (merge writes, dedicated service account); deleting them removes the operator's flag-flip path for live features. Pass B: operator-authorized config writes, not gameplay decisions. **KEEP** |
| `shared_cache_cost_model.py`, `shared_cache_probe.py` | Pass A: the shared-cache spike deliverables (cost model + standalone Gemini cache probe) for a spike bead; the spike is decided, but the probe remains a reusable cache-behavior instrument. Pass B: spike instruments, not live paths — the cost model is a record, the probe a reusable check. **KEEP** (probe) / **DELETE** (cost model as a frozen record? No — split: cost model KEEP as the spike's record, since deleting a decision record is not required) — verdict: **KEEP** for both, as spike record + reusable probe |
| `show_top_users.py` | Pass A: shows top users with campaign details and story snippets; deleting it removes a reusable reporting tool. Pass B: read-only reporting. **KEEP** |
| `smart_mock_generator.py` | Pass A: generates Firebase/auth/storage/API mocks; part of the completed test-optimization program, and the live mock surface is `mvp_site/mocks/`. Pass B: superseded optimization-program tooling. **DELETE** |
| `smoke_test_dice_code_execution.py` | Pass A: a smoke test for dice code_execution validation (creates a test campaign, triggers a dice action, validates `code_execution_used`); deleting it removes a §6.2 anti-cheat smoke path for the dice execution mechanism. Pass B: it verifies the mechanism, never resolves dice itself. **KEEP** |
| `sort_beads_jsonl.py` | Pass A: canonicalizes `.beads/issues.jsonl` (sorted by id), referenced by CI and the root-cause fix for sort-noise PRs; deleting it reopens the noise pattern. Pass B: ledger canonicalization only. **KEEP** |
| `spicy_remove.py` | Pass A: sanitizes egregious safety-violating content from a campaign in Firestore (operator-invoked, with diff printing); deleting it removes the operator's content-safety remediation tool. Pass B: operator-authorized sanitization on explicit command, not an autonomous gameplay transform. **KEEP** |
| `standardize_slash_commands.py` | Pass A: standardizes slash-command Markdown files with execution workflows; deleting it removes a docs-standardization tool. Pass B: docs tooling only. **KEEP** |
| `start_capture_evidence_server.py` | Pass A: starts an evidence server with inherited credentials and exact-SHA health proof; deleting it removes an evidence-server launcher still referenced by evidence workflows. Pass B: server launching only. **KEEP** |
| `sync_codex_claude_skills.py` | Pass A: exposes Claude skills to Codex via its skill-directory shape, referenced by CI; deleting it breaks skill mirroring. Pass B: file/symlink management only. **KEEP** |
| `test_coverage_analyzer.py` | Pass A: part of the completed test-reduction program (coverage-overlap detection); the reduction is done. Pass B: completed-program tooling. **DELETE** |
| `test_firebase_read_write.py`, `test_firebase_with_data.py` | Pass A: Firebase read/write and sample-data test scripts; deleting them removes connectivity/data-seeding checks, but they are ad-hoc scripts with no workflow role and overlap the maintained test suite. Pass B: ad-hoc connectivity scripts. **DELETE** |
| `test_generate_wiki_html.py` | Pass A: unit tests for `generate_wiki_html.py` (a live, CI-referenced generator); deleting them removes the generator's regression cover. Pass B: tests for a kept tool. **KEEP** |
| `test_github_output_multiline.py` | Pass A: regression test for multi-line `$GITHUB_OUTPUT` handling, guarded by its own run contract; deleting it removes a live CI-safety regression. Pass B: tests for a kept behavior. **KEEP** |
| `test_importance_ranker.py` | Pass A: part of the completed test-reduction program (ML/heuristic importance ranking); the reduction is done. Pass B: completed-program tooling. **DELETE** |
| `test_json_bugs_simple.py` | Pass A: verifies two PR #278 JSON display bugs (state updates, raw JSON); the bugs are fixed and the checks are historical. Pass B: closed-PR verification. **DELETE** |
| `test_monitoring_dashboard.py` | Pass A: part of the completed test-reduction program (performance dashboard); the reduction is done. Pass B: completed-program tooling. **DELETE** |
| `test_multiple_ip_campaigns.py` | Pass A: creates multiple diverse IP campaigns to verify multi-universe capability; deleting it removes a capability-verification script, but it is a one-off verification, not a regression guard, and multi-universe support is now covered by live tests. Pass B: one-off verification. **DELETE** |
| `test_optimization_suite.py` | Pass A: the comprehensive test-optimization suite (167→80, 60→15 min) that orchestrated the completed reduction program; the program is done and the suite is not a live gate. Pass B: completed-program orchestrator. **DELETE** |
| `test_parallel.py` | Pass A: a rigorous parallel-concurrency test with response-body validation and overlap calculation; deleting it removes a concurrency-measurement tool, though repo AGENTS.md requires observed-evidence concurrency proof and this tool measures rather than assumes. Pass B: measurement only. **KEEP** |
| `test_path_normalizer.py` | Pass A: normalizes path references in test files for cross-platform/worktree compatibility; deleting it removes a repair tool for a recurring test-portability problem. Pass B: test-file repair only. **KEEP** |
| `test_retention_nudge.py` | Pass A: tests for `retention_nudge.py` (a kept script); deleting them removes its regression cover. Pass B: tests for a kept tool. **KEEP** |
| `test_scenarios.py` | Pass A: Milestone 0.4 desync test scenarios; the milestone is closed and live scenario coverage lives elsewhere. Pass B: closed-milestone fixtures. **DELETE** |
| `test_utils.py` | Pass A: a 22-line utility (`add_numbers` + its test) that is a placeholder, not infrastructure; deleting it loses nothing any test imports. Pass B: a stub. **DELETE** |
| `top_campaigns.py` | Pass A: queries the longest campaigns in a date range with entry counts; deleting it removes a reusable operator report. Pass B: read-only reporting. **KEEP** |
| `trace_to_eval_case.py` | Pass A: converts evidence bundles into normalized eval-case JSON for CI, referenced by CI; deleting it breaks eval-case promotion. Pass B: artifact conversion only. **KEEP** |
| `ttv_telemetry.py`, `ttv_window_measurement.py`, `ttv_zombie_reaper.py` | Pass A: the CI time-to-verdict telemetry, measurement, and zombie-run reaper, all referenced by CI; deleting them removes live CI observability and hygiene. Pass B: CI telemetry/operations only. **KEEP** |
| `upload_slack_media_evidence.py` | Pass A: uploads evidence media to Slack via the files API; deleting it removes the evidence-distribution path used by evidence workflows. Pass B: file upload only. **KEEP** |
| `validate_aggressive_optimization.py` | Pass A: validates the completed aggressive-optimization system; the system is done and this validator's subject is retired. Pass B: completed-program validation. **DELETE** |
| `validate_automation_test_accounts.py` | Pass A: rejects primary-human identities in write-capable automation config, referenced by CI; deleting it removes an account-safety gate the repo AGENTS.md itself mandates (dedicated non-primary test accounts). Pass B: a safety gate, not a gameplay decision. **KEEP** |
| `validate_beads_issues_jsonl.py` | Pass A: validates `.beads/issues.jsonl` integrity and unique IDs, referenced by CI; deleting it removes a ledger-integrity gate. Pass B: ledger validation only. **KEEP** |
| `validate_firebase_auth.py` | Pass A: a Milestone 2 Firebase auth configuration validator; the milestone is closed and auth config is now validated by live tests and deploy checks. Pass B: closed-milestone validation. **DELETE** |
| `validate_imports.py` | Pass A: the import-standards validator (delta mode), referenced by CI; deleting it removes the live import guard. Pass B: static analysis only. **KEEP** |
| `validate_no_retired_prompt_surfaces.py`, `validate_no_turn_rejection_surfaces.py` | Pass A: validators that production prompts/code contain no retired surfaces or banned turn-rejection surfaces — the latter directly enforces the repo's UX-first validation rule; deleting them removes live policy gates. Pass B: static policy enforcement, no runtime transforms. **KEEP** |
| `validate_private_pr_evidence.py` | Pass A: verifies authenticated same-PR receipt access; deleting it removes a receipt-verification step for private evidence. Pass B: verification only. **KEEP** |
| `validate_prompt_tool_contracts.py` | Pass A: validates versioned prompt/tool contract hashes, referenced by CI and guarded by its own tests; deleting it removes the contract-drift gate. Pass B: hash validation only. **KEEP** |
| `validation_only_approach.py` | Pass A: Milestone 0.4 Approach 1 (validation-only desync detection); the milestone is closed. Pass B: closed-milestone artifact. **DELETE** |
| `verify_core_memory_evidence_counts.py` | Pass A: an independent denominator/schedule verifier for the Gemini memory evidence study; deleting it removes the independent check on that study's counts. Pass B: study verification, no live role — but independence is its value, and the study's evidence is still cited. **KEEP** |
| `verify_exemption.py` | Pass A: a 25-line rate-limit exemption-email parser with no workflow role and no tests; deleting it loses a trivial helper. Pass B: an orphan snippet. **DELETE** |
| `verify_workflow_yaml.py` | Pass A: syntax/structural verifier for `green-gate.yml`; deleting it removes a workflow-safety check. Pass B: static validation only. **KEEP** |
| `wa_daily_oauth_source.py` | Pass A: delivers the latest validated daily report through the owner's OAuth CLI (with receipt verification); deleting it breaks the validated-delivery path. Pass B: delivery with verification, no campaign decisions. **KEEP** |
| `wiki_deploy_sync.py` | Pass A: detects drift between the repo and deployed-checkout copies (the guard created after the 431-page wiki truncation incident); deleting it removes the drift detector for deployed copies. Pass B: drift detection only. **KEEP** |
| `world_sim_event_catalog_ab.py`, `world_sim_event_grounding_judge.py`, `world_sim_event_grounding_replay.py`, `world_sim_event_stage2_report.py`, `world_sim_event_strategy_ab.py`, `world_sim_realism_ab.py` | Pass A: the world-sim event-strategy A/B apparatus (catalog arms, grounding judge/replay, stage-2 report, strategy prototype, realism runner) for the living-world event work; deleting it removes the experiment instruments for §6.3's living-world direction while that work is still active. Pass B: offline replay/judgment over captured payloads, never writing campaign state (the strategy prototype states this explicitly). **KEEP** |

## 7. `scripts/` top-level `.sh` — per-file (ops, not gameplay)

| File | Pass A + Pass B justification, ending in verdict |
|---|---|
| `_beads_rollback.sh` | Pass A: shared transactional snapshot/restore helpers sourced by Beads migration scripts; deleting them removes the rollback safety for ledger migrations. Pass B: ledger plumbing only. **KEEP** |
| `backup_dotfiles.sh`, `backup_validation.sh`, `claude_backup.sh`, `claude_backup_cron.sh`, `fix_backup_repository.sh`, `install_backup_system.sh`, `setup_secure_credentials.sh`, `test_backup_comprehensive.sh`, `test_hostname_portability.sh`, `test_security_fixes.sh`, `verify_backup_cron.sh` | Pass A: the Claude/dotfiles backup system and its tests (validation, cron, credential setup, hostname portability, security fixes) are live operator automation for developer-machine backups; deleting them removes backup coverage and its guards. Pass B: backup/credential plumbing, no campaign data. **KEEP** |
| `beads_publish_canonical_pr.sh`, `beads_sync_canonical.sh`, `check_beads_jsonl_drift.sh`, `install-beads-hook.sh`, `sanitize_gitattributes_beads.sh`, `migrate_worktree_beads_to_redirect.sh` | Pass A: the Beads canonical-publish/sync/drift-gate/hook/sanitize/migration set, referenced by CI and guarded by beads tests; deleting any of them breaks the ledger workflow that keeps `.beads/issues.jsonl` canonical. Pass B: issue-ledger plumbing only. **KEEP** |
| `bq_story_history_decomposition.sh` | Pass A: decomposes real-user Gemini requests into cached-prefix vs uncacheable tail for prompt-cache analysis; deleting it removes a reusable cache-analysis query. Pass B: telemetry analysis only. **KEEP** |
| `bug-hunt-daily.sh` | Pass A: the daily 9am bug-hunt job (spawns agents over recently merged PRs, files reports/beads); deleting it removes a live scheduled quality program. Pass B: agent orchestration, no campaign decisions. **KEEP** |
| `capture_scene_preview_evidence.sh` | Pass A: captures live scene-illustration evidence on a PR preview; deleting it removes a reusable preview-evidence capture, not tied to one closed PR. Pass B: evidence capture only. **KEEP** |
| `check-pr-file-collisions.sh`, `check-pr-status.sh`, `extract-unresolved-comments.sh`, `cr-loop-guard.sh`, `gh-merge-guard.sh` | Pass A: PR workflow helpers (collision warnings, status polling, unresolved-thread listing, review-loop guards, merge guard); deleting them removes live PR-triage tooling. Pass B: GitHub workflow plumbing only. **KEEP** |
| `check_billing_export_principal_and_freshness.sh`, `check_deployed_sync.sh`, `check_design_retro_publishability.sh`, `wiki_publish_preflight.sh` | Pass A: narrow preflight/diagnostic gates (billing-export principal drift, deployed-checkout drift, design-retro publishability, wiki publish preflight); deleting them removes fail-closed gates created after real incidents. Pass B: gate checks only. **KEEP** |
| `cherrypick_pr.sh`, `cleanup_branches.sh`, `sync_check.sh`, `common_utils.sh` | Pass A: everyday git helpers (cherry-pick a PR, clean merged/stale branches, post-command sync check, shared utils); deleting them removes live developer conveniences. Pass B: git plumbing only. **KEEP** |
| `ci-detect-changes.sh` | Pass A: the CI change-detection script generating test matrices, referenced by workflows; deleting it breaks directory-based test selection. Pass B: CI scheduling only. **KEEP** |
| `ci_cache_busting.sh` | Pass A: a 16-line file whose own header says NO-OP — cache-busting moved to Dockerfile on 2026-02-06 — so deleting it removes a dead wrapper (the live module is `cache_busting.py`). Pass B: a tombstone wrapper. **DELETE** |
| `cleanup_cache_busted_files.sh`, `cleanup_local_agent_artifacts.sh`, `disk_audit.sh`, `disk_cleanup.sh`, `scratch_guard.sh` | Pass A: cleanup/safety helpers (cache-busted asset cleanup, agent-artifact cleanup, disk audit/cleanup, scratch-guard after the /tmp wipe incident); deleting them removes live disk/scratch hygiene, and `scratch_guard.sh` is the safety guard for destructive cleanup. Pass B: filesystem hygiene only. **KEEP** |
| `codex_web_maintenance.sh`, `codex_web_setup.sh` | Pass A: Codex Web setup/maintenance bootstraps (git wiring, tool installs); deleting them breaks the Codex Web environment bootstrap. Pass B: environment provisioning only. **KEEP** |
| `complete_email_setup.sh` | Pass A: a 31-line email-setup completion stub with almost no content; deleting it loses no named capability (the real setup is `setup_email.sh`). Pass B: a stub. **DELETE** |
| `delete_all_my_epic_adventure.sh` | Pass A: deletes all campaigns with one specific name in batches — a one-off personal cleanup, not a reusable operator tool (its target is hardcoded by name). Pass B: a completed personal cleanup. **DELETE** |
| `deploy-firestore-rules.sh` | Pass A: deploys Firestore security rules to Firebase; deleting it removes the rules-deploy path, which is authorization infrastructure. Pass B: authorization provisioning — an allowed server role. **KEEP** |
| `deploy_common.sh` (1505 lines) | Pass A: shared deployment helpers sourced by deploy scripts (service deploys, receipt verification, scheduler provisioning), referenced by CI; deleting it breaks deployment. Pass B: deployment/transport only; its size warrants a later split, not deletion. **KEEP** |
| `determine-smoke-mode.sh` | Pass A: determines smoke-test mode from the GitHub event type, referenced by CI and guarded by contract tests; deleting it breaks smoke-mode routing. Pass B: CI routing only. **KEEP** |
| `efficiency_audit.sh` | Pass A: audits PR pipeline metrics; deleting it removes a reusable pipeline-metrics tool. Pass B: reporting only. **KEEP** |
| `execute_merge_manifest.sh`, `generate_merge_manifest.sh` | Pass A: the SHA-pinned batch-merge manifest pair (generator is read-only; executor merges only when explicitly unlocked) — the merge-execution path for batch approvals; deleting them removes a live, human-gated merge workflow. Pass B: merge orchestration with explicit unlocking, no campaign role. **KEEP** |
| `extract_video_evidence_frames.sh` | Pass A: extracts frames from evidence videos for frame review; deleting it removes a reusable evidence-review tool. Pass B: media processing only. **KEEP** |
| `fix_run_tests_readarray.sh` | Pass A: bash-3.x readarray compatibility shims for `run_tests.sh`; deleting them breaks macOS/older-bash test runs. Pass B: shell compatibility only. **KEEP** |
| `generate_evidence_bundle.sh` | Pass A: auto-generates canonical evidence bundles under /tmp for test runs; deleting it removes the bundle-generation path evidence workflows use. Pass B: artifact assembly only. **KEEP** |
| `genesis_observer.sh` | Pass A: monitoring-only observer for Genesis sessions (no completion detection); deleting it removes a monitoring tool for an orchestration system still in use. Pass B: observation only. **KEEP** |
| `goalexec-loop.sh`, `goalexec-loop-cmux.sh` | Pass A: goal-execution loop runners (CLI + tmux variants) with time-boxing; deleting them removes a live agent-loop tool. Pass B: agent orchestration, no campaign decisions. **KEEP** |
| `gog-auth-canary.sh`, `setup_gog_keyring_passphrase.sh` | Pass A: the gog auth canary (daily Gmail auth check under launchd) and its keyring setup; deleting them removes the scheduled auth-health check for the campaign job's Gmail path. Pass B: auth-health monitoring only. **KEEP** |
| `grant_gcp_service_account_permissions.sh` | Pass A: a one-time IAM grant executed 2025-11-17 to fix PR #2045 preview permissions; the grant persists in GCP and the script's purpose is spent. Pass B: a completed one-time grant. **DELETE** |
| `install-git-hooks.sh`, `install_mcp_servers.sh`, `install_smoke_local_cadence.sh`, `install_worldai_mcp.sh`, `mcp_common.sh`, `mcp_dual_background.sh`, `mcp_smoke_test.sh`, `playwright_smoke_test.sh`, `start_mcp_server.sh`, `start_mcp_production.sh`, `start_game_server.sh` | Pass A: the MCP/server install and launch set (git hooks, MCP installers, smoke cadence, dual-transport wrapper, smoke tests, MCP/production/game server starters); deleting them breaks the documented MCP and server setup paths. Pass B: installation/process/transport only. **KEEP** |
| `load_tokens.sh` | Pass A: the token-loading helper (validates GitHub/Gemini tokens, builds templates) sourced by MCP scripts; deleting it breaks token setup for those scripts. Pass B: credential loading (never printed or committed by the script itself), not gameplay. **KEEP** |
| `loc.sh` (scripts copy) | Pass A: the scripts-tree LOC counter with test/production breakdown; deleting it removes a measurement tool (distinct from the root `loc.sh`). Pass B: counting only. **KEEP** |
| `make_evidence.sh` | Pass A: runs a testing_mcp/testing_ui test with automatic artifact capture; deleting it removes the standard evidence-capture invocation. Pass B: test orchestration only. **KEEP** |
| `mcp_repro_full_bar_harness_rerun.sh`, `mcp_repro_full_bar_provenance_cast.sh`, `mcp_repro_full_bar_record_video.sh`, `mcp_repro_full_bar_run_all.sh` | Pass A: the level-up five-class repro + provenance-video set; the repro already ran and its video is recorded, so deleting the set removes a spent evidence-production pipeline. Pass B: closed-evidence tooling. **DELETE** |
| `node_utils.sh` | Pass A: shared Node path resolution for CI (self-hosted macOS runners), referenced by workflows; deleting it breaks Node discovery on those runners. Pass B: environment plumbing only. **KEEP** |
| `oracle_helpers.sh` | Pass A: Oracle CLI bundles (architecture/AI/UI debug presets); deleting them removes a debugging convenience, not a gate. Pass B: CLI presets only. **KEEP** |
| `publish_pypi.sh` | Pass A: publishes orchestration/automation packages to PyPI/TestPyPI; deleting it removes the publish path for those packages. Pass B: packaging/distribution only. **KEEP** |
| `repro_streaming_contract_preview_auth.sh` | Pass A: reproduces/verifies the MCP streaming-contract preview-auth fix (401→404/200); the fix is verified and the repro's value is historical. Pass B: closed-fix verification. **DELETE** |
| `run_campaign_selector.sh` | Pass A: a 27-line runner for the campaign selector with a local vpython shim; the selector itself is a closed-milestone tool (see `campaign_selector_*.py` DELETE), so this runner's target is gone. Pass B: a runner for a deleted tool. **DELETE** |
| `run_level_up_class_repro_suite.sh` | Pass A: a 4-line compatibility entrypoint whose own header says the canonical suite lives in `testing_mcp/`; deleting it removes only a redirect. Pass B: a redirect stub. **DELETE** |
| `run_smoke_local.sh` | Pass A: an 11-line smoke-local default wrapper (local MCP, real mode default); deleting it removes a thin default-setting entrypoint, though it is still the documented `/smoke-local` shorthand. Pass B: defaults only. **KEEP** |
| `server-config.sh`, `server-utils.sh`, `shared_config.sh`, `setup_production_env.sh`, `venv_utils.sh`, `venv-pre-commit.sh`, `setup-dev-env.sh`, `setup-python-runner.sh`, `setup-stream-signing-secret.sh` | Pass A: the server/venv/config foundation (`server-config.sh` ports, `server-utils.sh` server management sourced by `tools/localserver.sh`, `shared_config.sh` Cloud Run capacity contract, production-env setup, venv utilities, dev-env and runner setup, stream-signing-secret setup) — deleting any breaks local serving, CI runners, or the capacity contract repo AGENTS.md declares single-source. Pass B: configuration/process/capacity plumbing, no campaign fields. **KEEP** |
| `setup_secure_credentials.sh` | Pass A: already counted with the backup set above (secure credential setup for the backup system); deleting it removes the backup credential path. Pass B: credential setup only. **KEEP** |
| `smoke_local_cadence.sh` | Pass A: the ~15-minute launchd cadence gate for /smoke-local; deleting it removes the scheduled smoke gate. Pass B: test scheduling only. **KEEP** |
| `test_ai_universe_api_keys.sh` | Pass A: clones an external repo and tests API keys against its services; deleting it removes a key-validation tool for a third-party repo, not a WorldArchitect gate. Pass B: an external-repo key check. **DELETE** |
| `test_cache_busting.sh` | Pass A: end-to-end verification of the cache-busting pipeline (config/trigger/immutable serving) for a kept module; deleting it removes the pipeline's verification. Pass B: tests for a kept tool. **KEEP** |
| `test_broken_logic_demo.sh` | Pass A: demonstrates that the ORIGINAL BROKEN LOGIC would fail TDD tests — a RED-phase demo whose point is already proven. Pass B: a historical demo. **DELETE** |
| `test_determine_smoke_mode.sh`, `test_execute_merge_manifest.sh`, `test_merge_manifest_lib.sh`, `test_secondo_pr.sh`, `test_slack_notification.sh`, `testing_help.sh` | Pass A: contract tests/help for kept scripts (smoke-mode routing, merge-manifest executor, manifest libs, secondo PR, Slack notification) plus the testing-commands help; deleting them removes regression cover for kept tools. Pass B: tests/help for kept tools. **KEEP** |
| `validate-security.sh` | Pass A: a 72-line Firestore-rules validation snippet (grep-based allow-read/write checks); deleting it removes a rules sanity check, though it is a thin grep wrapper rather than a full validator. Pass B: authorization-rule checking — an allowed role, thin as it is. **KEEP** |
| `validate_imports_delta.sh`, `validate_pr_evidence.sh` | Pass A: the PR-delta import validation helper extracted from the test workflow and the PR evidence validator; deleting them removes live CI helpers. Pass B: static validation only. **KEEP** |
| `wa_daily_report_cron.sh` | Pass A: delivers the current campaign report then publishes that exact verified message (cron wrapper); deleting it breaks the verified daily-report delivery. Pass B: delivery only. **KEEP** |
| `wiki-campaign-daily-ingest.sh` (1266 lines) | Pass A: the daily wiki ingest of real-user campaigns (≥50 scenes) into the private llm-wiki repo — a live scheduled job; deleting it stops the wiki pipeline, which the model cannot run on a schedule. Pass B: it reads Firestore and writes to a separate wiki repo; its privacy gates (noted in its own tests) are the control, and it never touches live campaign state. **KEEP** |

## 8. `tests/` top-level `test_*` files — per-file (test infrastructure)

Provisional rule: tests whose target is `mvp_site/` game-path code (another
audit group's scope) are marked KEEP (provisional) when they guard behavior
that is plausibly kept (persistence, dice, auth, inventory dedupe, level-up)
and must be re-checked against that group's verdict — a DELETE verdict there
deletes the test here. Tests whose target is a script in this audit follow
that script's verdict exactly. Tests for closed PRs or retired tools are
DELETE on their own standing.

| File | Pass A + Pass B justification, ending in verdict |
|---|---|
| `test_audit_dice_rolls.py` | Pass A: 996 lines guarding the dice-roll extraction, bucketing, and impossible-value detection in `scripts/audit_dice_rolls.py` (a kept §6.2 audit tool); deleting it removes the audit's regression cover. Pass B: tests for a kept audit tool. **KEEP** |
| `test_bead_jsonl_sort_workflow.py`, `test_beads_integrity.py`, `test_beads_jsonl_union.py`, `test_beads_publish_canonical_pr.py`, `test_beads_publish_launchd.py`, `test_check_beads_jsonl_drift.py`, `test_sanitize_gitattributes_beads.py`, `test_sort_beads_jsonl.py` | Pass A: the Beads ledger test set (sort workflow, integrity, union, canonical publish, launchd publisher, drift gate, gitattributes sanitize, sort canonicalization) guarding kept Beads scripts; deleting any removes cover for a live ledger gate. Pass B: tests for kept tools. **KEEP** |
| `test_bq_row_contract_unit.py` | Pass A: unit tests for the BigQuery row contract validator in `testing_mcp/lib`; deleting them removes contract cover for telemetry rows. Pass B: tests for a kept telemetry contract (provisional on the testing_mcp scope's verdict for that lib). **KEEP** (provisional) |
| `test_campaign_wizard_mobile_scroll_harness.py`, `test_my_campaigns_mobile_ux_harness.py` | Pass A: focused contracts for mobile browser-test harnesses (wizard scroll, my-campaigns UX); deleting them removes harness contracts for live mobile UX tests. Pass B: harness tests, no player data. **KEEP** |
| `test_character_creation_state_schema_helpers.py` | Pass A: offline self-tests for the character-creation harness (fixtures, checkpoint projections, provider boundaries); deleting them removes harness bookkeeping cover. Pass B: offline harness tests only, explicitly not live-server acceptance. **KEEP** |
| `test_ci_detect_changes_docs_only.py`, `test_ci_detect_changes_tia_wiring_policy.py`, `test_ci_event_coverage_files.py`, `test_ci_test_duration_sharding.py`, `test_ci_test_impact_analysis.py`, `test_ci_worker_count_policy.py` | Pass A: the CI policy test set (docs-only fast pass, TIA wiring, event coverage, duration sharding, impact analysis, worker-count policy) guarding kept CI scripts and workflows; deleting any removes a live CI gate's cover. Pass B: tests for kept CI tooling. **KEEP** |
| `test_clock_repair.py` | Pass A: an offline control asserting the browser `_verified_claims` clock-skew wrapper shape; deleting it removes a narrow auth-time regression control. Pass B: AST-shape control, no live behavior. **KEEP** |
| `test_codex_skill_mirror_guard.py` | Pass A: contract tests for the kept `check_codex_skill_mirror.py` guard, including the dangling-symlink failure mode; deleting them removes the guard's cover. Pass B: tests for a kept tool. **KEEP** |
| `test_copy_campaign.py`, `test_repro_copy_campaign.py` | Pass A: tests for the kept `copy_campaign.py` and `repro_copy_campaign.py` (story cutoff restoration, owner rebind, replay-input extraction); deleting them removes cover for live operator tools. Pass B: tests for kept tools. **KEEP** |
| `test_core_memory_compaction_harness.py` | Pass A: offline harness accounting checks for memory-rate counting; deleting them removes a narrow accounting control. Pass B: offline accounting only. **KEEP** |
| `test_daily_cadence_stream_capture.py`, `test_daily_dice_audit_filter.py`, `test_daily_dice_audit_provenance.py`, `test_daily_dice_audit_warning_gate.py`, `test_daily_entrypoint_wiring.py`, `test_daily_lanes.py` | Pass A: the daily-pipeline test set (cadence stream capture, dice-audit user filter/pagination, audit provenance manifests, cron warning gate, dual-lane entrypoint wiring, lane verdicts) guarding kept daily scripts; deleting any removes cover for the §6.2 audit trail's daily form. Pass B: tests for kept tools. **KEEP** |
| `test_daily_gemini_retired.py` | Pass A: a 15-line test asserting the daily Gemini cost report is retired; deleting it removes the tombstone that prevents resurrection of a retired report. Pass B: a retirement pin — worth keeping precisely because it is small. **KEEP** |
| `test_delete_user_firestore_data.py` | Pass A: tests for the kept user-data deletion tool (resolve/scan/delete flows, depth fails, batch rollover); deleting them removes cover for an erasure path. Pass B: tests for a kept tool. **KEEP** |
| `test_deployment_adapter_parity.py`, `test_deployment_build.py`, `test_dev_candidate_tag_cleanup.py`, `test_doc_size_workflow.py`, `test_hydrate_exact_files.py`, `test_mcp_smoke_workflow_dispatch.py`, `test_pr8461_smoke_contracts.py`, `test_pr_cleanup_admission.py`, `test_pr_cleanup_lifecycle.py`, `test_pr_preview_reuse_workflow.py`, `test_precompute_deps_self_hosted.py`, `test_run_tests_archive_dispatch.py` | Pass A: the deployment/workflow test set (adapter parity, build context, candidate cleanup, doc-size workflow, exact-file hydration, smoke dispatch, PR #8461 contracts, cleanup admission/lifecycle, preview reuse, precompute retirement, archive dispatch) guarding kept deploy/CI behavior; deleting any removes a live gate's cover. Pass B: tests for kept deployment/CI behavior. **KEEP** |
| `test_design_doc_prompt_hydration.py` | Pass A: pins that hydrated design-gate inputs include prompt Markdown without relaxing safety; deleting it removes a safety pin. Pass B: a safety test, no live role. **KEEP** |
| `test_game_constants_helpers.py` | Pass A: unit tests for `testing_mcp/lib/game_constants.get_spell_slots`, deliberately placed under `tests/` to avoid integration collection; deleting them removes pure-helper cover. Pass B: tests for a kept helper (provisional on the testing_mcp verdict). **KEEP** (provisional) |
| `test_grade_core_memory_evidence.py`, `test_verify_core_memory_evidence_counts.py` | Pass A: grading/counting tests for the core-memory evidence study (treatment-label rejection, denominator verification); deleting them removes the study's independent checks. Pass B: study verification, tied to the kept `grade_core_memory_evidence.py` / `verify_core_memory_evidence_counts.py`. **KEEP** |
| `test_guarded_marker_clone.py` | Pass A: deterministic synthetic contracts for a guarded clone (fake Firestore); deleting them removes clone-safety cover. Pass B: synthetic contracts, no live data. **KEEP** |
| `test_gunicorn_production_startup.py`, `test_gunicorn_worker_activation.py` | Pass A: offline Gunicorn startup/worker-activation proofs for the real production WSGI app; deleting them removes the serving-activation proof. Pass B: transport proofs, no gameplay decisions. **KEEP** |
| `test_husky_gitleaks_precommit.py` | Pass A: pins that the pre-commit hook refuses staged secrets (including merge-diff scoping); deleting it removes a secrets-safety pin. Pass B: a security gate test. **KEEP** |
| `test_infra_retry_decision.py`, `test_runner_health_score.py` | Pass A: the infra-retry router decision contract and runner-health scoreboard contract, guarding kept CI tooling; deleting them removes fail-closed retry/scoreboard cover. Pass B: tests for kept CI tools. **KEEP** |
| `test_instruction_file_symlinks.py` | Pass A: the repo-wide guard that in-scope CLAUDE.md files are symlinks to AGENTS.md; deleting it removes a docs-hygiene gate. Pass B: repo hygiene only. **KEEP** |
| `test_inventory_merge.py`, `test_inventory_signature.py`, `test_main_get_campaign_payload_size.py` | Pass A: RED regression tests for inventory dedupe (write-side dedupe by bonus, signature ignoring `equipped`, payload under 100KB) guarding game-path merge behavior; deleting them removes the dedupe regression cover. Pass B: tests for game-path behavior — provisional on the game-path group's verdict for the merge helpers. **KEEP** (provisional) |
| `test_ip_tv_show_wizard_stream_verification.py`, `test_ip_wizard_evidence_paths.py` | Pass A: contracts for the IP wizard streaming verifier and evidence locations; deleting them removes wizard-verification cover. Pass B: verifier/path contracts, no live data. **KEEP** |
| `test_level_up_rearm_evidence_accounting.py`, `test_levelup_provider_identity.py`, `test_spell_slot_long_rest_reset_harness.py`, `test_think_select_execute_harness.py`, `test_pr9820_think_persistence_harness.py`, `test_pending_system_corrections_modes.py`, `test_second_opinion_mcp_server.py`, `test_si_contract_streaming_harness.py`, `test_stream_signature_harness_handoff.py`, `test_streaming_chunk_evidence_unit.py` | Pass A: the leveling/streaming harness test set (rearm accounting, provider identity, spell-slot reset, think/select/execute, think persistence, pending-corrections modes, second-opinion server, streaming contracts/signatures/chunks) guarding game-path leveling and streaming behavior; deleting any removes cover for live mechanics. Pass B: tests for game-path behavior — provisional on the game-path group's verdicts for those mechanics. **KEEP** (provisional) |
| `test_mobile_auth_same_origin_diagnostics.py` | Pass A: pins bounded, data-minimal diagnostics in the mobile same-origin auth driver (including that logging never blocks the server); deleting it removes a §6.1-adjacent logging-safety pin. Pass B: a logging-safety test, consistent with async/batched delivery principles. **KEEP** |
| `test_native_gemini_evidence.py`, `test_native_sdk_harness_routing.py` | Pass A: offline contracts for native Gemini evidence allow-lists and SDK harness routing; deleting them removes the native-execution routing pins. Pass B: routing/evidence contracts, no live provider claims. **KEEP** |
| `test_no_secrets_in_process_argv.py` | Pass A: pins that secrets reach child processes via environment, never argv, across launcher branches; deleting it removes a secrets-safety pin. Pass B: a security gate test. **KEEP** |
| `test_openrouter_signin_evidence_exit_code.py`, `test_openrouter_verification_settings_safety.py` | Pass A: OpenRouter sign-in evidence exit-code and settings-safety regressions (snapshot/restore of reversible keys, identity rejection before account access); deleting them removes sign-in safety cover. Pass B: safety tests for a live auth feature. **KEEP** |
| `test_ops_probe_removal.py` | Pass A: enforces that the auto-factory probe script and references are fully removed (issue #8623); deleting it removes the tombstone that prevents the probe's return. Pass B: a removal pin. **KEEP** |
| `test_replay_budget_guard.py`, `test_replay_worker_activation.py` | Pass A: offline contracts for the one-request replay evidence budget guard and worker activation; deleting them removes the replay-budget safety cover. Pass B: safety tests, explicitly not real-provider acceptance. **KEEP** |
| `test_sdui_roadmap_artifacts.py` | Pass A: tests for SDUI roadmap artifacts; deleting them removes artifact cover for a live UI surface. Pass B: artifact tests (provisional on the frontend group's verdict). **KEEP** (provisional) |
| `test_startup_gate.py`, `test_stop_hooks.py`, `test_workflow_runner_policy.py`, `test_ttv_signal_set_policy.py` | Pass A: startup-gate, hook-stop, workflow-runner-policy, and TTV-signal-set tests guarding kept startup/CI behavior; deleting them removes gate cover. Pass B: tests for kept behavior. **KEEP** |
| `test_world_sim_daily_cadence_browser_unit.py`, `test_world_sim_event_catalog_ab_freeze.py`, `test_world_sim_event_stage2_report.py`, `test_world_sim_evidence_bundle_verifier_unit.py`, `test_world_sim_local_player_tick_oracle_unit.py`, `test_world_sim_local_player_tick_real_e2e_unit.py`, `test_world_sim_preview_distributed_queue_capture_unit.py`, `test_world_sim_preview_distributed_queue_unit.py`, `test_world_sim_preview_retry_manifest_unit.py` | Pass A: the world-sim test set (daily cadence, event-catalog freeze, stage-2 report, evidence-bundle verifier, local player-tick oracle/e2e, preview queue capture/unit, retry manifest) guarding the §6.3 living-world apparatus; deleting them removes cover for the kept world-sim scripts. Pass B: tests for kept living-world tooling, consistent with async ticks merged on the next turn. **KEEP** |
| `test_beads_redirect_provisioning.sh`, `test_classify_testmon_result.sh`, `test_claude_mcp.sh` | Pass A: shell tests for beads-redirect provisioning, testmon result classification, and the Claude MCP script; deleting them removes cover for kept shell behavior. Pass B: tests for kept tools. **KEEP** |
| `tests/scripts/` (26 files, e.g. `test_check_function_loc_ratchet.py`, `test_ci_duration_observations.py`, `test_cloud_run_cost_alert_policy.py`, `test_world_sim_scheduler.py`) and `tests/_guard_boot_app.py`, `tests/fixtures/`, `tests/hooks/` | Pass A: NOT tabled — these are in the untouched set (see coverage); no verdict is claimed for them here, and they must not be read as KEEP or DELETE by omission. Pass B: —. **UNTOUCHED** (listed here only to prevent silent skipping) |

## Verdict counts

Counted mechanically from the verdict markers in the tables above (a row
that groups several files under one marker counts once here, so these are
ROW counts, not file counts — the tables themselves are authoritative):

- §1 Root `.py` (per-function rows): KEEP 7, DELETE 5. (The DELETE rows
  cover `capture_mocks.py`'s 2 functions and the 2 mobile-repro files'
  functions; `firestore_service.py`'s row is KEEP with an ADAPT-later note,
  not an ADAPT verdict.)
- §2 Root `.sh` (per-file rows, one row per file except the merged
  `local.sh`/`run_local_server.sh` pair): KEEP 34, ADAPT 1, DELETE 2
  (`Genesis.sh`, `codebase_loc.sh`). Files covered: 37 rows for 38 files.
- §3 `mvp_site/mocks/` (per-function rows): KEEP 17, DELETE 1 (function
  `parse_state_updates_from_response`), ADAPT 1 (the split mock-LLM row,
  which is also the DELETE row's file — counted in both marker totals).
  (The 17 KEEP rows already include the README row covering 2 files and
  the `bin/LICENSE.chromedriver` row.)
- §4 `tools/`: KEEP 3 rows (2 functions + main flow), 1 file.
- §5 Docs areas: KEEP 3 rows covering 14 files (archive).
- §6 `scripts/` top-level `.py`: KEEP 112 rows, DELETE 62 rows, covering
  210 files (rows group files where noted).
- §7 `scripts/` top-level `.sh`: KEEP 40 rows, DELETE 10 rows, covering
  109 files (rows group files where noted).
- §8 `tests/` top-level: KEEP 35 rows, DELETE 0 rows, covering 97 files
  (rows group files where noted). No top-level test file was found to guard
  only deleted/retired behavior — the retired-report tombstone test
  (`test_daily_gemini_retired.py`) is itself a KEEP pin.

Totals across all tables: KEEP 251 rows, DELETE 80 rows, ADAPT 2 rows
(including the split mock-LLM row's ADAPT marker). Do not cite these as
file counts without expanding the grouped rows.

## What remains — exact checklist for the next auditor

1. `scripts/` subdirectories (618 files) and `scripts/` top-level non-code
   files (28) — enumerate and table; `scripts/ci/` and `scripts/lib/` first,
   since workflows reference them.
2. `tests/` non-`test_*` files (77) and `tests/scripts/` (26) — table; several
   guard kept `scripts/` tools.
3. All `testing_*/` directories (1,279 files) — table per-file, with
   per-helper verdicts for shared libs (`testing_mcp/lib/`,
   `testing_utils/`, `testing_util/`); note the repo AGENTS.md
   real-service-only rule for `testing_mcp/`/`testing_ui/` when judging
   mock-based helpers there.
4. Per-function detail inside the large shell scripts (`run_tests.sh`,
   `deploy.sh`, `integrate.sh`, `claude_start.sh`, `local.sh`,
   `deploy_common.sh`, `wiki-campaign-daily-ingest.sh`) and inside
   `scripts/`/tests files whose tables above are per-file only.
5. Re-check every provisional `tests/` KEEP against the game-path groups'
   verdicts; flip to DELETE wherever the guarded behavior is DELETE.
6. Re-check the §6 cross-checks above if any dice, logging, or faction
   verdict changes in another group.

## Conflicts flagged

None with the §6 user decisions. Two judgment calls worth naming: (a) the
mock-LLM keyword router is KEEP even though the repo bans keyword routing —
the ban governs shipped intent classification, and this router only selects
test fixtures in code no player turn reaches; (b) `retention_nudge.py` is
KEEP even though it writes story nudges — its writes are operator-scheduled,
dry-run by default, and model-generated via an explicit call, so no server
field transform is involved.
