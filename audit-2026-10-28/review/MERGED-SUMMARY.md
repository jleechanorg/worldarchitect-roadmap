# MERGED SUMMARY — mvp_site review pass (run 3, review of run 2)

**Scope:** `mvp_site/` NON-TEST files only, from the local tree `~/workspace/repos/worldarchitect.ai`
(main-branch ZIP tree, commit c2af304, Oct 28 2026; no `.git` history). Read-only pass:
no repo files changed, no deletions, no PRs, zero GitHub API/MCP calls.
**This is a review pass, not a re-verdict:** every run-2 verdict below was checked against
file/line evidence; confirmations and challenges are both recorded. Nothing is deleted
except by its own PR with Jeffrey's go-ahead, and only where non-use is proven first
(2026-10-29 deletion rule).

**Per-area reports (all under `~/workspace/plans/audit/review/`):**

| Area | Report | Files | Units* | Headline |
|---|---|---|---|---|
| A1 gateway-core | `gateway-core.md` | 26 | 592 def/class occurrences | 4 dead, 8 stale docs, 6 challenges |
| A2 top-level-unassigned | `top-level-unassigned.md` | 26 | 640 AST occurrences (362 rows) | 14 dead entries, 7 test-only, 25 stale docs |
| A3 state-storage | `state-storage.md` | 23 | 1,000 AST units | 6 dead, 9 test-only, 6 stale docs, 6 challenges |
| A4 schema-parsing | `schema-parsing.md` | 41 | 757 (650 Python + 107 data) | 6 dead entries (7 symbols), 24 stale docs, 12 challenges (3 verdict-changing) |
| A5 dice-mechanics | `dice-mechanics.md` | 10 | 207 rows | 8 dead, 7 stale docs (+1 incomplete note), 5 challenges |
| A6 godmode-levelup-rewards | `godmode-levelup-rewards.md` | 44 | 606 items | 7 dead, 12 stale docs, 8 challenges |
| A7 faction-worldsim-time | `faction-worldsim-time.md` | 50 | 808 (805 Python + 3 assets) | 4 dead entries (32 symbols), 3 stale-doc groups, 7 challenge groups |
| A8 providers-auth | `providers-auth.md` | 20 | 743 rows | 35 dead, 5 stale docs, 1 verdict flip + corrections |
| A9 logging-ops-incident | `logging-ops-incident.md` | 26 | 659 (419 fns + 53 classes + 184 constants + 3 non-Python) | 7 dead, 14 stale docs, 6 challenges |
| A10 agents-prompts-code | `agents-prompts-code.md` | 11 | 389 AST | 6 proven dead, 19 stale docs, 20 challenges |
| A11 prompts-data | `prompts-data.md` | 128 | 867 sections | 3 orphaned files, 4+ stale/contradicting groups, 8 challenge items |
| A12 frontend | `frontend.md` | 68 | ~2,762 (1,064 JS + 1,518 CSS + ~30 HTML + 151 Python) | 9 dead, 13 stale docs, 9 challenges |
| A13 test-infra-in-prod-tree | `test-infra.md` | 32 | 284 units (+ 10 Markdown files section-by-section) | 32 files test-only in prod tree, ~11 dead entries, 16 stale docs |
| A14 misc docs/data/services | `misc.md` | 80 | 321 (262 code + 59 non-Python) | 10 dead, 13 stale docs, 13 config mismatches (§4 below), 6 challenges |
| **TOTAL** | | **585** | **~10,635** | **~130 dead entries, ~169 stale-docs items** |

\* "Units" are not one homogeneous kind: AST defs/classes, JS symbols, CSS rule blocks,
prompt sections, JSON keys/$defs, registered specs, doc files, and script units are all
counted in their area's own unit. The ~10,635 total is therefore a coverage total, not a
claim that 10,635 "methods" of one kind were reviewed. Every area enumerates its units
by AST/script walk and names every symbol in a row (grouped rows name every symbol).

**Headline numbers:** files reviewed **585** · units reviewed **~10,635** · dead/unreachable
entries **~130** (§1, clusters/whole files counted once — symbol total is higher) ·
test-only/demo items: **the whole A13 tree (32 files) plus per-area items in §2** ·
stale/misleading docs items **~169** (§3, clusters counted once) · run-2 challenges:
**36 verdict-changing flips** plus evidence/wording/qualification corrections in every
area (§4) · files skipped: **0 unexplained** (§5).

## Coverage and manifest reconciliation (§5, required accounting)

- Partition verified by script against `_file_list.txt` and `_areas.json`:
  `_areas.json` lists 558 files, `_leftovers.json` lists the 27 top-level remainder files
  folded into A14; union = **585, zero overlaps, zero gaps** against the 585-file find.
- Manifest drift, closed: the manifest (`~/workspace/plans/audit/manifest_mvp_site.txt`,
  1,972 lines) is NOT a file count — 1,885 file entries + 79 directory entries + 8 ERROR
  lines. Tree = 2,072 regular files = 585 non-test + 1,487 test-excluded. Reconciliation:
  1,885 + 191 tree-only paths − 4 = 2,072. The 4 manifest entries "missing" from the tree
  are symlinks present in the tree (`mvp_site/CLAUDE.md`, `mvp_site/prompts/CLAUDE.md`,
  `mvp_site/prompts/GEMINI.md`, `mvp_site/tests/CLAUDE.md`), not missing files. The 191
  tree-only paths are mostly test files plus ~60 in-scope files added since the manifest
  (mostly `prompts/shared/`, `prompts/injection/`, `prompts/multiverse/` fragments, plus
  `mvp_site/static/v2/index.html` and `mvp_site/testing_framework/examples/capture_example.py`).
- Count discrepancies closed: gateway "26 files / 593 occurrences" = 25 Python files + 1 JSON
  file, and run 2's own per-file numbers sum to **592**, not 593 (A1 C1); `schemas/` is
  **37** files, not 38 — v2 counted `defensive_numeric_converter.py` twice (A4 C-37/38);
  the gateway-flagged set is **43** names, not 42 — 26 reviewed in A2 + 17 disposition-only
  (logging-ops 8, frontend 7, agents-prompts-code 1, misc 1), zero names without an owner (A2).
- Skips: **zero unexplained skips in any area.** Scope exclusions (not skips):
  `frontend_v1/tests/` and `testing_framework/tests/` + `test_*.py` (test files, out of
  scope by definition); A14's `docs/zfc_audit/FULL_AUDIT.md` + `SUMMARY.md` (assigned to A6);
  A11's symlinked `prompts/CLAUDE.md` + `GEMINI.md` (aliases of `prompts/AGENTS.md`, counted once).
  Files that turned out test-only were flagged in their rows, never silently skipped
  (notably all of A13, `arch.py`, `schema_ci_checks.py`, `trace_capture.py`).
- Per-area caveats that bound the coverage claim (full text in each report's §6):
  A1 KEEP rows rest on AST presence + run-2 reconciliation + targeted caller/doc checks for
  all DELETE/ADAPT/dead/doc candidates, NOT a verbatim re-read of every line of `main.py`
  (9,634 lines) and `llm_service.py` (12,030 lines); A2's complete unreferenced-symbol proof
  for all 451 `constants.py` module symbols was not completed by bare-name grep (short names
  collide — dead clusters proven by qualified grep); A5 caller evidence is import/call-graph
  grep + body reads for contested items, not a full dynamic call graph; A7's five large files
  got full inventories with decision-point reads, not every line, and the cutover schema was
  judged at schema level, not field-by-field; A9's `bq_logging.py`/`logging_util.py` grouped
  transport helpers were audited at signature/docstring level with bodies read for every
  public entry point and ADAPT/DELETE candidate; A11 large files (game_state 1,364 lines,
  narrative 906, living_world 667) were verified at heading + flagged-section + grep level,
  with full re-reads targeted to challenged/script-flagged/linter-failing files; A14 sampled
  the largest function bodies and did not recompute evidence proof-hashes or re-verify
  deferred doc targets outside its file list.

## (1) Dead / unreachable executable code

Proven non-use (zero production callers, not an entry point, registration, or dynamic
target) unless marked otherwise. Live-but-policy-DELETE items are NOT in this list — they
are run-2 verdicts confirmed in §4, and removing them is a migration, not a dead-code sweep.

- **A1:** `llm_response.py:365 _strip_debug_content` (live path uses `_strip_all_debug_tags`);
  `llm_response.py:384 _strip_state_updates_only`; `mcp_client.py example_usage` (demo,
  `__main__` only); `input_validation.py:79 sanitize_user_input` (duplicate of
  `sanitize_string`). Explicitly NOT dead: the clock-skew family (prod-inert, not unreferenced
  — see §4 C2).
- **A2:** `constants.py` soul/XP helpers `calculate_soul_xp:1285`, `calculate_soul_dissonance:1305`,
  `is_fiendish_portfolio:1323`, `get_capped_xp:1358`; attribute helpers `get_attributes_for_system:1388`,
  `get_attribute_codes_for_system:1396`, `uses_charisma:1404`, `uses_big_five:1409` (test-only,
  identical branches / always False); divine cluster (`get_divine_rank_from_level`,
  `get_divine_rank_bonus`, `get_divine_safe_limit`, `get_divine_immunities`, `is_epic_level`,
  `is_divine_level`) and combatant cluster (`is_friendly_combatant`, `is_neutral_combatant`,
  `is_generic_enemy_role`) — sole prod consumer is the `game_state_mixins.py` cluster already
  DELETE in run-2 state-storage (cascade DELETE, with their tables `DIVINE_RANK_*`,
  `SOUL_VALUES`/`SOUL_TIERS`/`SOUL_ACQUISITION_METHODS`, `XP_SOURCE_CAPS`,
  `FRIENDLY/NEUTRAL_COMBATANT_TYPES`, `GENERIC_ENEMY_ROLES`); `user_lifecycle_telemetry.py:16
  MAX_EVENT_BYTES` (never used); dead-in-production `UseActualTime` branch in
  `waitlist_access.py`; stale `FUNCTIONS_TO_TRACE` entries in `trace_capture.py` (silently
  skipped by a `getattr(..., None)` guard — verify each name before deleting).
- **A3:** whole `state_update_provenance.py` (4 symbols, test-only scaffold, self-admitted in
  its docstring, plus an envelope-dropping hazard if ever wired); whole `location_util.py`
  (5 symbols, test-only — run 2's callers were same-named different functions in
  `llm_parser`/`agent_prompts`); `turn_idempotency.render_replayed_sse_events:624` (wholly
  uncalled); `graveyard_service.get_visible_graveyard_prompt_keys` (wholly uncalled);
  `graveyard_service.collect_referenced_npc_tokens` + helpers (wholly uncalled);
  `session_header_utils.derive_location_in_session_header` (wholly uncalled).
- **A4:** `MIN_NARRATIVE_LENGTH`, `CJK_PATTERN`, the dead `llm_service.py:711` instance,
  the `entity_validator` globals, the never-read `emotional_patterns` table, and the entire
  `schemas/field_constants.py` file (zero prod readers — see §4 C2).
- **A5:** the 7 run-2 DELETEs all confirmed, plus new `dice_provably_fair.py:195
  verify_commitment` (run 2 claimed 2 production call sites; import-level grep finds zero —
  live code uses `compute_commitment` directly and `is_valid_injected_seed`; see §4 C1).
- **A6:** `level_up_session.TERMINAL_STATUSES`, `rewards_engine.ASI_CHOICE_IDS`,
  `rewards_engine._coerce_flag_or_none`, `adjusters/base.py list_adjusters`,
  `backend_adjustment_specs.ACTIVE_REWARDS_DELIVERY_SUPPRESSION_SPECS` (tuple only; members
  keep KEEP), empty `ACTIVE_PR_7164_ADJUSTMENT_SPECS`, shadowed first
  `ACTIVE_PR_8489_ADJUSTMENT_SPECS` definition. NOT dead (checked): `god_mode_schema.validate_total_operations`
  (Pydantic `@model_validator` dispatch).
- **A7:** whole `faction/dual_mode.py` (29 symbols — `DualModeManager` appears only at its
  definition and the `faction/__init__.py` re-export; zero prod or test importers of the
  faction package; all prod callers import `faction.tools` directly); `faction/combat.py:221
  calculate_damage_deterministic` and `faction/intel.py:178 calculate_intel_success_deterministic`
  (zero references in prod AND tests); dead alias `relevance_worker.py:1187
  run_timeline_relevance_worker` (worker itself stays KEEP).
- **A8 (35):** all 18 symbols in `llm_providers/minimax_provider.py` (live dispatch is
  Gemini/OpenRouter/Cerebras only at `llm_service.py:2995,3049,3311,3328,5537–5539`; MiniMax
  selection scaffolding terminates in the unsupported-provider error — a dead end, not
  dispatch); 9 exhaustive Gemini BigQuery field-spec/alias tables (`gemini_provider.py`
  L2441–L2901, only test callers); 8 duplicate delegation wrappers in `openrouter_auth.py`
  (L70–L1537) deferring to canonical `openrouter_identity`/`openrouter_maintenance`.
  NOT dead: `provider_utils.inject_tool_requests_if_missing` (live at `llm_service.py:3944,4046`
  — its DELETE is strict-ZFC, not non-use).
- **A9:** `bq_logging.log_dice_roll` + `DICE_TABLE` (zero production callers, only
  `tests/test_bq_logging.py:1178`); `bq_logging._dice_schema` + its boot provisioning (L1539)
  and TTL-list entry (L1189) — orphaned once the writer goes (see §4 C2);
  `serious_user_incidents.IncidentFamily` alias (zero production users; flagged, not deleted,
  pending a tests-tree grep); `bq_request_logger.setup_request_logging`'s `executor_getter`
  parameter (never read); duplicate stdlib re-export block in `logging_util.py` (L100–114
  vs L824–827); `coverage_report.txt` (stale artifact, no reader — DELETE as artifact only).
  Explicitly NOT dead: `monitor_doc_sizes.sh` (live CI consumer — see §4 C1), `incident_canary.py`,
  gap reconciliation, the dispatcher (separate Cloud Run service), `debug_hybrid_system.py`,
  `debug_image_budget.py`.
- **A10:** 6 proven prod-dead/no-op: `check_classifier_startup`, `warm_synchronously`
  (already dead independent of the audit), intent error classes, `EntityEnforcementChecker` +
  global (strengthened to zero prod references), `_is_location_owner` (always False),
  `LocationEntityEnforcer` + global with empty `location_rules = {}` (no-op). Distinguished
  as NOT dead today: the semantic family (live today, future-dead only after the Jev swap)
  and the sovereign-tier branch (conditionally unreachable behind a default-off flag).
- **A11 (orphaned/unloaded, live-path):** `prompts/multiverse/sovereign_system.md` and
  `prompts/multiverse/sovereign_ascension_ceremony.md` (gated-unreachable:
  `constants.py:861 MULTIVERSE_TIER_ENABLED = False`, PATH_MAP sovereign extras unregistered
  at `agent_prompts.py:302-307`, tier branch commented unreachable at `agent_prompts.py:4547-4562`,
  ceremony falls back to divine at `agents.py:3494-3515`); `prompts/shared/rag_output_contract.md`
  (dead: `agent_prompts.py:4400-4407 build_rag_output_contract_block()` returns `""`,
  "RAG retrieval has been removed"). `prompts/AGENTS.md` is policy-excluded from runtime by
  its own lines 1–5, not accidentally orphaned — not counted here.
- **A12:** five unreferenced files confirmed unloaded (no `index.html` tag; only dynamic
  injection in shipped JS is `app.js:2576–2583` for `settings.js`; `main.py` serves
  generically and names no asset except the tooltip kill-switch pair — files remain
  direct-URL retrievable, strengthening DELETE): `component-enhancer.js`, `visual-validator.js`,
  `test_planning_block_parsing.js`, `parallel_dual_pass.js` + `.css`, mock HTML;
  `frontend_preview_release.py` (inert without the PR-10571 receipt); portrait-ai compare pair
  (subject is DELETE); `build_legacy_scene_image_prompt` (ADAPT, moves with ablation);
  plus NEW dead branch `app.js:2595–2596` calling `window.setupBYOKEventListeners`, which
  `settings.js` never assigns (it defines snake_case `setup_byok_event_listeners`, L72) —
  guarded, so dead not broken.
- **A13:** `parse_state_updates_from_response` (zero importers anywhere); both wrapper modules
  (`mock_firestore_service_wrapper.py`, `mock_llm_service_wrapper.py`); dead `_use_full_mocks`
  flag and shadowed first `MockServiceProvider` import in `factory.py`; `capture_cli.py:13`
  import-before-path-insert bug; `migration_examples.py` classes; `pytest_integration.py`
  nested example tests; `integration_utils.py:13` importing `main`; `DISCREPANCY_SCENARIOS`
  with no reader; cross-area: `main.py:9421,9445 run_test_command` points at
  `testing_ui/run_all_browser_tests.py`, which exists nowhere in the tree.
- **A14:** `equipment_display.classify_equipment_query` (imported, never called);
  `avatar_image_gen.generate_image_xai`, `capture_openrouter_image_forensics`,
  `time_direct_openrouter_minimal` (zero prod callers); `portrait_generator_agent.assemble_campaign_portrait_context`
  wrapper; `static/v2/index.html` referenced assets absent; `tools.py` (1-line docstring stub,
  0 symbols, 0 importers); `config/paths.py` (zero prod callers — only one test, via a
  different import path); `analysis/*.py` (4 files, test/analysis-only, workstation-hardcoded
  paths); document_generator prose-mining/debug helpers (test-only).

## (2) Test-only / demo code in prod files

- **A13 — the whole area (32 files) is test infrastructure in the prod tree: RELOCATE, not
  capability-delete.** File verdicts: 28 relocate-out-of-prod-tree / 4 ADAPT / 0 KEEP; unit
  verdicts 267 DELETE / 17 ADAPT / 0 KEEP. Covers the entire `testing_framework/` package,
  mock services, wrappers, fixtures, and all 8 framework/mocks docs. **Exception (see §4/§6
  owner decision):** `llm_providers/provider_gateway.py:21–22` imports `MockLLMClient` and
  `FULL_STRUCTURED_RESPONSE`, executed on the shipped mock-services path (gated by
  `MOCK_SERVICES_MODE` / `main.py:2414` smoke token) — those two are ADAPT (extract smoke
  execution into an explicitly-gated smoke module), and whether smoke mode is a shipped
  promise is an owner decision. This REFUTES the scripts-tests claim that no player turn
  path imports the mocks, for these two files.
- **A1:** whole `arch.py` (test-suite tooling; only `tests/test_architectural_decisions.py`
  callers); `mcp_client.py example_usage` (demo); `mcp_api.py _roll_dice_tool` + registration
  (self-described test-only, behind `ENABLE_DICE_TEST_TOOL=true` — registered, so not dead,
  but test-only surface in prod); `llm_service.py` mock constructs (MOCK_SERVICES_MODE-gated).
  NOT test-only: `gunicorn.conf.py` lifecycle hooks (process logging, KEEP); criterion4 files
  (operational-canary authorization with live consumers).
- **A2 (7):** whole `schema_ci_checks.py` and `trace_capture.py` (test/CI callers only —
  ADAPT out of `mvp_site/`); `rate_limiting._drain_rate_limit_telemetry` (self-described
  test-only); `world_logic` test shim `ensure_level_up_rewards_pending` and test-version
  `get_campaigns_for_user_list`. `start_flask.py` is a dev/UI-test entry point, kept as such.
- **A3 (9, §2):** including the Firestore in-memory fake as a test seam and test-only
  `normalize_session_header` / `resolve_xp_pair` / `record_deceased_npc_in_graveyard`. No
  demo/example functions found in this area.
- **A4:** `llm_parser` test-only cluster → ADAPT-move-out-of-prod (see §4 C3);
  `stream_with_context`'s stale `gemini-2.5-flash` default is moot — the function is test-only.
- **A6:** `register_allowed_specs` (test-only); `adjusters/registry.py` and
  `backend_adjustment_registry.py` shims (test/tooling-consumed only, kept as compat surfaces,
  flagged). No demo code found.
- **A7:** the two deterministic helpers in §1 are test-family; docstring "Example:" blocks
  are prose only, not demo code; no other demo code found.
- **A8:** see A13 exception above for the mock-services path; no further test-only/demo items
  listed beyond the §1 dead groups (test callers noted per item in the area report).
- **A9:** `incident_canary.py` is dev-only (checked, kept as such); no further test-only/demo
  items beyond §1.
- **A10:** intent-classifier warmup/startup demo surface is covered by the pilot DELETE
  (files go in full); no additional demo code beyond §1 items.
- **A12:** mock HTML and `test_planning_block_parsing.js` are the demo/test surface (see §1);
  no other demo code in shipped JS.
- **A14:** `analysis/*.py` (test/analysis-only, §1); `install.sh` is AGY sandbox prep misnamed
  as an installer (see §4-config below).

## (3) Stale / misleading docs

Each item: file:line, the doc claim, and what the code actually does (one line). Full
line-level lists are in each area report's §3.

- **A1 (8):** clock-skew docstrings claiming 720s/production-safe when code returns 0 on
  Cloud Run/CI/prod; `CLOCK_SKEW_SECONDS` "safe for production" comment contradicting the
  file's own rationale; module header presenting the patch as normal usage;
  `llm_response.py get_narrative_text` docstring vs unconditional `narrative_text` return;
  `preventive_guards.py` header mandating all guards including the five run-2 DELETEs;
  `main.py _strip_equipment_from_game_state` contradictory dedupe sequencing;
  `llm_service.py _translate_completed_character_creation_finish_input` docstring omitting
  the classifier-metadata gate and injected instruction; `decorators.py` header
  "emoji-enhanced logging" with no emoji in the message. Explicitly NOT stale:
  `llm_capture.py honor_suppression` — docs accurately say it currently has no effect.
- **A2 (25):** headliners — `get_attributes_for_system`/`get_attribute_codes_for_system`
  docstrings claim per-system results but both branches always return D&D;
  `trace_capture.py` documents a `TRACE_FUNCTIONS` env var the code never reads;
  `extract_structured_fields` has a one-line docstring for a 200+-line extractor with
  synthesis/suppression/relocation; `get_proficiency_bonus` hides its 1–20 clamp;
  `get_spellcasting_ability` hides keyword-matching + highest-stat guessing fallbacks.
- **A3 (6, D1–D6):** `entity_preloader` docstring omitting the `entity_tracking` source;
  `entity_tracking` docstring overstating a re-export as the implementation;
  `_seed_starting_spells_if_missing` name (seeds nothing, only logs; docstring itself honest);
  `memory_utils` "Presence is a server-owned structural fact" assertion;
  `persist_turn_atomic` name overpromising for its non-transactional mock fallback branch;
  `turn_idempotency.render_replayed_turn_response` "Preserves server-owned keys" wording
  (keys are dropped top-level, kept only inside `structured_fields`). Explicitly cleared:
  the provenance docstring, the `GameState` no-conflict claim (AST-verified true),
  `to_validated_dict`'s warn-only docstring.
- **A4 (24, incl. minors):** headliners — `game_state.schema.json` description gaps grouped
  as one item (97 undescribed properties, 3 undescribed top-level properties, 2 undescribed
  `$def`s); `stream_story_with_game_state` doc vs its 37 audited branches (incl. the two
  DELETE strips run 2's seam sample missed); `character_creation_wire_schema.json`'s
  `_comment` survives into the built wire schema (loader returns raw JSON;
  `inline_canonical_defs` strips nothing — hygiene note, not a verdict change).
- **A5 (7 + 1 incomplete note):** `derived_stats.py:1-17` ("consumed by all finalize paths" —
  sole prod consumer is `conclude_invariant.py:21`; "arity 3" vs 4 params; "ZFC-exempt" claim
  rejected); `dice_rng.py:118-132 verify_uniform_distribution` ("Reject (i.e. raise)" —
  returns float chi², raises only for bad args; claimed `wa-daily-dice-audit` cron caller not
  found in `scripts/daily_dice_audit.py`); `dice_provably_fair.py:22-26` ("dice_rng does not
  exist on origin/main" — it exists in this tree); `dice_rng.py` module docstring framing the
  SHA sampler as live when the live mechanism is `stamp_seed`.
- **A6 (12):** modal docstrings naming FastEmbed as "the SOLE authority" post-pilot;
  `_bare_token_normalize`'s "NOT used to rewrite" claim contradicted by stage 4b;
  `extract_modal_choice_id` omitting its verbatim-fallback behavior;
  `adjusters/specs.py`'s false "forwarding all active specs" (14 of 20);
  `json_strip_prefix`'s false "(array)" stripping claim; undisclosed id-synthesis/display-refresh
  behavior in `campaign_upgrade.normalize_planning_block_choices` and
  `god_mode_executor._synchronize_replacement_xp_aliases` docstrings.
- **A7 (3 groups):** `faction/README.md` whole "Resources (`resources.py`)" section for a
  nonexistent module, Dual Mode presented as live Phase 1 while its code is dead;
  `faction/__init__.py` empty `# Resources` marker and re-exports of DELETE-verdict formulas
  as public API; `dual_mode.py` module docstring claiming `/faction`, `/adventure` commands
  and reminder injection — no such handler or caller exists. Checked NOT stale: validation.py's
  spec citation, `tools.json`, the cutover schema, `_simulate_fast`'s docstring, the cooldown
  docstring's issue-#7956 failure-mode claim (honest, but not a registered exception).
- **A8 (5):** AGY module doc "default: off" vs the gateway's implicit default-on
  (`provider_gateway.py:112-151`); AGY "intentionally minimal" vs a 1,944-line file with
  prompt composition and JSON salvage; `reasoning_policy.py` "MiniMax M2.1 ignores effort
  controls" (no MiniMax entry exists, MiniMax never dispatched); `openrouter_auth.py`
  "inert until the reviewed deployment contract is packaged" vs unconditional route
  registration at `main.py:2630` with handler-level gating; misleading name
  `_is_flow_id` (L80, only checks digest format).
- **A9 (14):** observer module docstring's "No added latency on the terminal response"
  guarantee and `record_stream_turn_observation`'s "never blocks" docstring both fail against
  the streaming call site (`main.py:6393`, generator `finally`, bounded wait + Firestore
  `complete_journey`); emitter module docstring's "zero PII leakage" overstates a pattern
  screen on 4 keys; `is_automated_test_account_email`'s "never a real user" overstates a
  prefix heuristic; `CausalEvidenceRef`'s universal downgrade claim overstates
  `validate_root_cause_route` (LLM/BACKEND only); dispatcher's "fallback to InMemory" comment
  and "Private dispatcher" docstring are stale/imprecise (no fallback in code; privacy comes
  from deployment ingress + OIDC gates, not the bind address).
- **A10 (19, S-1–S-19):** agents.py header priority list vs the actual 17-resolver table;
  `get_agent_for_input` / `_resolve_semantic_intent` "PRIMARY BRAIN" docstrings;
  `_detect_conclude_signal`'s FastEmbed branch; warmup `main.create_app()` caller claims (no
  such caller; `main.py:1550` calls `warm_in_background`); `_is_player_character`'s "based on
  game state" claim (body never consults state); the enforcer's capability claim;
  `_filter_location_schema_fields` understating its xp/location pops; all 8 PROMPTS_README
  claim groups (it lists 8 files vs 128 regular prompt files verified).
- **A11 (contradicting/stale, §3 + §2 duplicates):** linter failure run 2 missed
  (`scripts/check_prompt_agnosticism.py` FAILS — 15 errors across 6 files: divine appendix
  deities, game_state calendar table:1039, god_mode Shadowheart example:264, living_world
  Faerûn example:230, "3-Generation Power Lineage" in master:138 / narrative:845,
  "Helm of Telepathy" examples — mostly conditionally gated examples, but the linter scans
  whole files, so the files do not pass `prompts/AGENTS.md`'s ban as written);
  game-state faction block (:206+) duplicates `faction_management_instruction.md:6-9` (same
  100/500 thresholds) — the home is faction_management, not faction_minigame as run 2 said;
  divine "setting-agnostic" claim true only by gate (Appendix A:208-250 entirely Forgotten
  Realms but explicitly gated to FR campaigns at :210); stale code-side reference
  (`context_compaction.py:1056-1060` names `level_up_modal_output_contract.md`, which does
  not exist in `prompts/`); include-target count corrected to 31 distinct targets (58 refs),
  all present, none broken — not run 2's 32. Resolved non-contradictions: living-world
  visibility (mechanics invisible vs effects visible), XP boundary (model authors
  `reward_event`, server materializes cumulative), dice modal exception identical on both paths.
- **A12 (13):** README's `static/` layout; nonexistent light/dark/cyberpunk themes;
  nonexistent API methods (`makeApiCall`, `initializeAuth`, `signInWithGoogle`,
  `loadDragonKnightCampaignContent` — zero definitions in shipped JS); "app.js ~2,000 lines"
  vs actual 10,666; README entries presenting the DELETE files as live modules; ablation
  docstring claiming a `debug_mode` gate when the route gates on admin claim
  (`main.py:5107–5113`, "debug_mode is informational, not a gate"); worker's misleading default
  `timing_mode = PARALLEL` (server canonicalizes parallel → after_scene); terms-of-use §3 vs
  §20 age wording tension and §19 Report-action frontend presence unverified (server endpoint
  exists, no frontend control located); mock's broken `../styles/style.css` link.
  Verified-accurate (listed so they are not "fixed" wrongly): share-modal PR #5823 comment,
  flag docstrings, outcome-verdict header.
- **A13 (16):** headliners — `mocks/README.md` documents `USE_MOCK_SERVICES`/`MOCK_FIRESTORE`/
  `MOCK_GEMINI` env vars with no `getenv` in any `mocks/*.py` and a nonexistent
  `MockFirestoreService(response_delay, error_rate, max_campaigns)` API;
  `testing_framework/README.md` omits 9 files and tells readers to run nonexistent
  `test_integration_demo.py`/`simple_test.py`; `CAPTURE_README.md`/`IMPLEMENTATION_SUMMARY.md`
  advertise a `/testerc` command existing nowhere in `mvp_site/*.py`.
- **A14 (13):** `CODE_REVIEW_SUMMARY.md` line counts stale by an order of magnitude (main.py
  "985" vs 9,634); `UNIFIED_API_IMPLEMENTATION.md` subject files don't exist;
  `PARALLEL_DUAL_PASS_INTEGRATION.md` dead feature; `README.md` "Flask 2.x" vs actual 3.1.3;
  `world/README.md` archive section for a nonexistent directory; `README_FOR_AI.md` 2025-07-07
  issue; `FALLBACK_REVIEW.md` `frontend_v2` reference; `config/paths.py` false "single source
  of truth" claim.

**A14 §4 config/reality mismatches (13, kept separate because they are config, not prose
docs):** tracked push config can never validate — fail-closed by design, document as shape
template not live config; Dockerfile provisions fastembed for the deleted classifier and
copies `testing_mcp/`/`testing_utils/` into the prod image; `requirements.txt` mixes
prod/dev/test deps; `pytest.ini` flags need an unpinned plugin; `run_integration_tests.sh`
targets a nonexistent `test_integration/` dir; `install.sh` is AGY sandbox prep misnamed as
an installer; `static/v2` asset hashes match nothing. Push itself is NOT dead
(`push/routes.py:register_routes` called from `main.py:2632-2634`; obligation path live via
`durable_intent.py:340`, `firestore_service.py:8529-8553`, `llm_parser.py:2418`) but inert
by fail-closed configuration (`push/config.json` `enabled: false`, empty scheduler/APNs fields)
— all push files KEEP.

## (4) Challenges to run-2 verdicts, with evidence

Verdict-changing flips are marked **FLIP**. Everything else in this section is an
evidence, wording, consequence, or scope correction with the verdict standing. All other
run-2 verdicts are CONFIRMED on the evidence cited in the area reports; the confirmations
that matter most are listed after the challenge table.

**Verdict flips (36, by area):**

- **A1 (2):** C2 clock-skew family DELETE→**ADAPT** (prod-inert but not dead —
  `world_logic.py:41` calls `apply_clock_skew_patch`, `openrouter_auth.py:234-235` and
  `waitlist_access.py:57-59` use `UseActualTime` — remove from prod path, don't delete as
  unused); C3 `llm_response._strip_debug_content` ADAPT→**DELETE**. Plus C1 counting (592
  not 593, §5 above); C4 framing qualification (most run-2 DELETEs — `coerce_integral_number`,
  preventive-guard backfills, `get_spell_level`, `_strip_equipment_from_game_state`,
  llm_service strip/normalize family, `default_scoring` — are live code with real call sites;
  confirmed as policy verdicts, but removals are migrations, not dead-code sweeps); C5
  `main.py` nested `calc_modifier` DELETE confirmed plus duplication (`stats_display.calc_modifier`
  already implements it and `get_stats` already uses it); C6 additional duplicates with
  file:line (two nested `safe_get`s in `main.py`, two `run_in_fresh_loop`s in `mcp_client.py`,
  `_is_mock_services_mode` in both `main.py` and `llm_service.py`, llm_service wrappers over
  continuation entry points, triple request/response shapes, `convert_dict` alias, criterion4
  wrapper).
- **A3 (2 file-level):** C3 `location_util.py` is test-only (run 2's callers were same-named
  different functions) — `resolve_location`/`_resolve_raw` ADAPT→**DELETE**, module
  MIXED→**DELETE** in full. Plus C1 game_state "duplicates" are not dead (`graveyard` 3374/3384
  is one property getter+setter; `validate_and_correct_state` 3469/3478 are `@overload` stubs
  + 3486 implementation); C2 entity shim DELETEs stand only with mandatory rewiring
  (live on the turn path: `llm_service.py:229,709,8038` and `:230,1795`; `entity_instructions.py:11,413`);
  C4 Firestore reconciliation DELETEs require replacing the merge step in all three commit
  routes (reward txn 7442, audit txn 5870, batch fallback 5298); C5 run 2's "768 symbols"
  matches no AST count (687 top-level / 786 all defs / 870 including module consts for the
  19 files) and 41 nested helpers were unnamed; C6 `graveyard_service._turn_val` upgraded from
  tentative to proven live caller (`agent_prompts.py:4894`).
- **A4 (3):** C2 `schemas/field_constants.py` KEEP→**DELETE** in full (zero prod readers);
  C3 llm_parser test-only cluster → **ADAPT**-move-out-of-prod; C9 `validate_entity_coverage`
  KEEP→**ADAPT** (test-only, not live diagnostics). Plus 9 consequence/evidence/characterization
  corrections with verdicts standing — notably C1: run 2's claimed consequence is wrong,
  because **no entity retry loop exists in `llm_service.py`**; deleting `entity_validator`
  removes only 3 warn/log sites + a dead instance. Also confirmed: llm_parser SPLIT,
  `defensive_numeric_converter` DELETE (with a third prod importer, `world_logic.py`, added to
  the consequence), `entity_validator` DELETE except the two "Unknown" sentinels,
  `narrative_sync_validator` DELETE, and the `validate_game_state` warn-not-reject caveat
  verified satisfied at both prod call sites. Depth caveats closed: `stream_story_with_game_state`
  audited branch-by-branch (37 branch rows B1–B37, overall SPLIT, incl. two DELETE branches
  run 2's seam sample missed — the second living-world strip and the antagonist-cooldown strip
  at `llm_parser.py:3921–3931`); `game_state.schema.json` judged $def by $def (42 + envelope,
  all KEEP); `gemini_schema_acceptance.json` judged entry by entry (all 35 accepted + 7
  carried fingerprint names, every current cell sha-matched, 0 mismatches).
- **A5 (2):** C1 `dice_provably_fair.verify_commitment` KEEP→**DELETE** (see §1);
  C2 `dice_integrity._log_fabricated_dice_if_detected` KEEP→**ADAPT** delivery-only (emits via
  `logging_util.warning` on turn-path processing, `llm_service.py:5294,9000`). Plus C3
  `structured_fields_utils.py:105` only mentions `resolve_dice_audit_events` in a comment,
  does not call it; C4 `progression_outcome` sink already sends BigQuery via background
  executor — only the Cloud Logging `logger.info` is still synchronous; C5
  `_record_model_rolls_in_debug_info` is a dict write — ADAPT scopes to the persisted
  `debug_info` step. Revised totals KEEP 175 / ADAPT 24 / DELETE 8 (run 2: 177/23/7). §6(2)
  check clean.
- **A6 (8):** C1–C5 the five dead-code corrections in §1 (KEEP→DELETE, C5 tuple-only);
  C6 `modal_conclude_policy.detect_conclude_signal` KEEP→**ADAPT** (free-text path live-wired
  to pilot-DELETE `intent_classifier.*` in `agents.py`; must be rewired to Jev Noul flag +
  explicit confirmation per §6(4)); C7 widened ADAPT on `extract_modal_choice_id`
  (prefixed/JSON branches return unrecognized ids verbatim, safe today only because every
  caller membership-checks); C8 `register_allowed_specs` KEEP→**ADAPT** out of the production
  module (test callers only). Sharpenings (not verdict changes): campaign_divine rewiring must
  cover 4 caller files, not just the lock; `canonicalize_rewards` ADAPT must remove calls to
  DELETE functions and resolve a `current_level = to_level` vs `from_level` inconsistency.
  Cross-cutting: 77 active specs carry RUNTIME_EVIDENCE_MISSING, so registry membership proves
  nothing for them.
- **A7 (3):** dual_mode file KEEP/ADAPT→**DELETE** in full (see §1, largest challenge);
  `validate_highlight_semantics` DELETE→**KEEP** and `validate_bulk_highlight_response`
  ADAPT→**KEEP** (the "semantics" function is pure jsonschema validation against the canonical
  response schema, `validation.py:49-70`, rejects never repairs/judges; live via
  `coordinator.py:422,686`). Plus rankings corrections (`BEHAVIOR_DESCRIPTIONS`,
  `rankings.py:148`, omitted from all run-2 rows — DELETE with its lookup;
  `get_all_ai_factions` ADAPT confirmed but corrected — as written it regenerates the roster
  on every call, `rankings.py:200-209`, so ADAPT requires real persisted-roster work, not
  relabelling); constants filled (all 107 rowed, no verdict surprises); `merge_partial_world_time`
  is LIVE not test-only (`game_state_merge.py:2053` via `handle_world_time_merge_if_needed`),
  so ADAPT stands and the conditional DELETE does not trigger; cooldown-stripping DELETE
  confirmed (no antagonist/living-world-cooldown spec in `backend_adjustment_specs.py` or the
  registry — survival requires a named + registered exception with necessity proof);
  §6(3) gap: `execute_faction_tool` still synchronous from the turn path (`dice.py:692`,
  `game_state.py:4013`, `provider_utils.py`, `preventive_guards.py`) and
  `evaluate_living_world_trigger` at `game_state_mixins.py:996` — ADAPT scope extends to those
  call sites (dice rolls stay on-path per §6(2); bulk work goes async).
- **A8 (1):** `openrouter_credentials.py:_is_sha256_hex` (L257) KEEP→**ADAPT** (pure delegation
  to `openrouter_identity.is_sha256_hex`, used only intra-file — the same pattern run 2 DELETEs
  for `openrouter_auth._is_flow_id`). Plus 17 genuinely new nested rows run 2 had no row for
  (16 KEEP, 1 ADAPT for `_TestResponse.__init__`) and 5 run-2 addendum qualifier corrections
  at the same lines (e.g. `_transaction.operation` is actually `_rate_limit.operation`).
- **A9 (2):** C1 `monitor_doc_sizes.sh` DELETE→**ADAPT** (run 2 missed a live CI consumer —
  `.github/workflows/doc-size-check.yml` lines 171–172 run it, trigger paths lines 20/31/145 —
  relocate out of `mvp_site/` with a workflow-path update, not delete outright);
  C2 `bq_logging._dice_schema` KEEP→**DELETE** with `log_dice_roll` (only uses are boot
  provisioning and the TTL list; keeping it provisions an empty table forever). Plus C3 ADAPT
  narrowed (only the streaming `record_stream_turn_observation` call is sync; non-streaming
  path `main.py:5015–5032` already uses `submit_background_telemetry`); C4 detail correction,
  verdict stands (`coverage_report.txt` is not "every module at 0%" — 4 lines are at 100%;
  TOTAL is still 0% and the artifact is still stale); C5/C6 qualifications, verdicts stand
  (emitter's "2-worker background executor" covers only the BQ leg — Cloud Logging + sanitize
  are synchronous on the caller thread; dispatcher is not wired into `main.py` at all — separate
  service at `monitoring/serious_user_incidents/deploy.sh:764` — so "wired into the player path"
  holds for the observation/emission side, not the dispatcher process). The 3 serious files
  (no run-2 verdicts) got full reviews, all KEEP, no DELETE.
- **A10 (3):** `character_creation_semantic_completion_allowed` DELETE→**KEEP** (body is only a
  `stage == "review"` state gate, live `world_logic.py:2922` caller);
  `_is_companion_shaped` DELETE→**KEEP** (body uses only contract `detection_paths`/
  `detection_sentinels`, 2 internal call sites); `_resolve_character_creation_state`
  ADAPT→**KEEP** (pure state, unlike `_resolve_dialog_state`). Plus scope expansions run 2
  missed (`_resolve_rewards`' classifier level-up skip, `_resolve_character_creation_completion`'s
  complete-sheet gameplay escape at `agents.py:4070-4083`, `_resolve_dialog_state`'s five
  override families, `_resolve_rewards_fallback`'s classifier-metadata copying); count/evidence
  corrections (prompt_cache 5→4 functions, prompt_utils 10→9 functions, overlay/test-only
  caller corrections, spicy resolver's actual table position 16);
  `prepare_story_context_entries_for_prompt`'s ADAPT now unconditional (filtering found on full
  read: duplicate clearing + malformed-entry discard); `_resolve_campaign_tier`'s read-vs-compute
  flag closed as a pure read with a mortal default. This pass performed the sequential full read
  of `agents.py` (5,342 lines) and `agent_prompts.py` (4,938 lines) that run 2 left open, and
  closed both of run 2's flagged bodies. File verdicts: agents.py SPLIT confirmed;
  agent_prompts.py ADAPT confirmed; prompt_loader KEEP; entity_instructions SPLIT confirmed;
  context_compaction ADAPT confirmed; prompt_context_metrics KEEP; prompt_cache KEEP;
  prompt_utils ADAPT (one function); PROMPTS_README DELETE-from-shipped-path confirmed;
  intent_classifier + warmup DELETE in full confirmed (pilot, with its 2 call-site ADAPT
  rewiring items only).
- **A11 (7):** multiverse ×2 KEEP→**ADAPT** (gate-or-remove); rag_output_contract
  KEEP→**DELETE**-from-runtime; portrait_style_avatar KEEP→**ADAPT** (word-identical to
  portrait_style.txt except paragraph breaks); narrative and living_world ADAPT→**KEEP**
  (single-homing would delete a scope, not a duplicate — cross-reference only);
  character_creation ADAPT→**KEEP** (its "level-up" content is only a 9-line pointer + guard,
  lines 303-311, not mixed procedure). Game_state ADAPT confirmed but corrected (delete, don't
  move). Tally KEEP 122 / ADAPT 4 / DELETE-from-runtime 2 vs run 2's 123/4/1. All other files:
  run-2 KEEP confirmed. Draft-amendment effects: none (prompt files are model-authored data).
- **A12 (0 verdict flips):** two wording corrections with verdicts unchanged
  (interface-manager.js:91,99 *do* guardedly reference `window.componentEnhancer`, contra "no
  shipped code references the export"; the mock *does* contain `toggleDesktopChoices()` + a
  scroll listener); the new BYOK dead branch (§1); count-method reconciliation (run 2's ~702
  excluded class/object methods and property assignments — app.js 303 vs 257, auth.js 91 vs 46);
  provenance note (v2 §4 already contains full frontend_*.py rows — all re-verified, all
  CONFIRMED: cutover ADAPT, preview DELETE, release ADAPT); CSS count 18 vs 17 shipped (DELETE
  sheet included); terms KEEP confirmed with notes; equipment/document-generator backend verdicts
  confirmed with the frontend contract handed to misc (frontend renders full `equipment_list`
  with no truncation and does not depend on backpack subcategories/importance, so the backend
  keyword-branch/truncation deletions don't break it).
- **A13 (1 group):** the scripts-tests claim that no player turn path imports the mocks is
  REFUTED for two files — `llm_providers/provider_gateway.py:21–22` imports `MockLLMClient` and
  `FULL_STRUCTURED_RESPONSE`, executed on the shipped mock-services path (see §2/§6 owner
  decision). All other run-2 verdicts in this area confirmed on upgraded evidence.
- **A14 (2 refinements):** document_generator choice-matching is mixed, not purely prose
  inference (keep the `choice:`-prefix stored-key branch + `_get_choice_by_key`, delete only
  Methods 1–4; run-2's verdict upheld over run-1's blanket wording); equipment
  `_classify_backpack_item` is entirely keyword branches, so run-2's "single Backpack group"
  correction is adopted, and `classify_equipment_query` is dead as well as violating. Portrait
  compare DELETE confirmed but must also remove the live admin-gated `main.py:8619` route.
  All other run-1 portrait/document/equipment verdicts confirmed. `mvp_site/__init__.py` is
  load-bearing (10 legacy aliases, dozens of `from mvp_site import …` users): KEEP, with aliases
  for deleted targets pruned in the same PRs.

**Key confirmations with fresh evidence (not challenges):** §6 positions hold throughout —
server logging KEEP (async/batched where it blocks a turn), anti-cheat KEEP with dice
resolution on the turn path (A5 §6(2) check clean; A1's `_roll_dice_tool` test tool is not
rescued by it), faction KEEP with ticks async (A7 gap noted above, not a deletion);
classifier role KEPT as a model-side Jev decision step, `intent_classifier.py` +
`intent_classifier_warmup.py` still DELETE in full (A10 pilot confirmed; A6 C6 rewiring to
Jev Noul + explicit confirmation); provider-utils faction patching synchronously on the turn
path at `llm_service.py:3944-3948` and `:10880` is ADAPT to async per §6(3), not DELETE (A8);
the OpenRouter second identity system is live, not dead (`firestore_service.py:2206-2212,
10134-10142` plus `openrouter_identity.py`), so run-2's collapse-onto-Firebase ADAPT stands (A8);
no Jev provider module exists in the tree — Jev routing is a future implementation, not
current code (A8, A10).

## (6) Owner decisions carried forward (not decided by this pass)

1. **Smoke mode (`MOCK_SERVICES_MODE`) — is it a shipped promise?** (A13) Decides whether the
   two mock imports on the shipped path are extracted into an explicitly-gated smoke module
   (ADAPT) or removed with the mocks.
2. **`log_dice_roll` deletion despite §6(2)** (A9): zero production callers confirmed — the
   owner confirmation run 2 left pending is still pending. Note: §6(2) keeps anti-cheat
   integrity, not this writer; it provides no live trail.
3. **`monitor_doc_sizes.sh` relocation with workflow-path update** (A9): relocate out of
   `mvp_site/` and update `.github/workflows/doc-size-check.yml`, rather than deleting a
   live CI consumer.
4. **Clock-skew removal from the prod path** (A1): prod-inert family to be removed from the
   prod path (ADAPT), not deleted as unused — and the `UseActualTime` branch in
   `waitlist_access.py` is dead in production for the same reason (A2).
5. **Entity shim DELETEs requiring mandatory rewiring** (A3): `entity_preloader`/
   `entity_tracking` are live on the turn path; deletion without rewiring breaks it.
6. **Document_generator choice-matching refinement + portrait-compare route removal at
   `main.py:8619`** (A14).
7. **Faction/antagonist cooldown stripping DELETE vs §6(3)** (run-2 v2 §6 flag, confirmed by
   A7): no registered exception found; an exception must be named and registered with
   necessity proof to survive — the issue-#7956 docstring note is a start, not a substitute.
   Same standing question for the 77 RUNTIME_EVIDENCE_MISSING active specs (A6): registry
   membership proves nothing for them.
8. **ZFC skill amendment draft approval** (see below) — needs Jeffrey's approval → PR → full
   review before anything lands; it changes no verdict in this pass either way.

## Draft-amendment effects (DRAFT ONLY — not applied as policy)

The draft (`~/workspace/plans/zfc-skill-model-amendment-proposal.md`: FastEmbed and Jev count
as models; model-call outputs are model-authored; hand-written thresholds/boosts/anchor lists
layered on outputs still need an exception) was NOT applied in any area. Every area records
**zero verdict flips under the draft**: A1 (FastEmbed appears only in comments; `_translate_…`
stays DELETE because regex stripping + injected instruction remain server re-interpretation
even under the draft's own text); A2 (7 spots checked, zero changes); A3 (zero FastEmbed/Jev
references; similarity code uses `SequenceMatcher`/hand weights, which the draft itself leaves
needing an exception); A4 (no FastEmbed/Jev calls; 0.7/0.72 thresholds are server-side scoring,
not model outputs — draft would change only the reasoning label on KEEP dispatch/preservation
rows); A5 (0); A6 (draft would reword C6's rationale, ADAPT stands because the live callable is
the deleted classifier); A7 (nil — no FastEmbed/Jev usage; deleted items are hand-written server
arithmetic/transforms); A8 (no verdict changes); A9 (none — no file calls FastEmbed or Jev;
adapters decide from server-observed receipts/fingerprints/drops); A10 (zero flips — every
DELETE/ADAPT rests on hand thresholds, boosts, anchors, keyword matching, or server invention
that the draft itself leaves as server-side transformations); A11 (none — prompt files are
model-authored data); A12 (none — no FastEmbed/Jev/thresholds in frontend code); A13 (none);
A14 (none — keyword/threshold artefacts here are not model outputs).

## What this pass closed from run 2

Grouped rows: closed — every unit named in a row in all 14 areas (A2's 362 rows cover 640
occurrences; A3's giants use cluster rows plus delta rows for every nested helper run 2 left
unnamed; A7's store files and `models.py` got one row per method). Godmode sampling: closed —
`rewards_engine.py` reducers read in full, `modal_conclude_policy.py` read in full including
bodies, `agents.py`/`agent_prompts.py` read sequentially in full. Frontend big-file partials:
closed — JS enumerated script-by-script with one row per symbol (1,064), CSS one row per rule
block (1,518), Python full per-symbol reviews. Manifest drift: closed (§5 above). Assignment
confirmations: closed — 42-vs-43 gateway-flagged set reconciled (A2), 4 state-adjacent files
got full first verdicts (A3: `serialization.py` KEEP with one ADAPT — consolidate `json_serial`
into `json_default_serializer`, secret-NPC/browser-boundary redaction is an authorization KEEP
via `main.py:5944` and `project_browser_payload`; `state_update_provenance.py` DELETE in full;
`turn_replay_projection.py` KEEP, display-only projection with God Mode envelope drop;
`turn_idempotency.py` KEEP except `render_replayed_sse_events` DELETE).

## Remaining work (outside this pass, unchanged)

Scripts-tests untouched scope, docs-configs content audit, non-shipped directories, and test
files method-by-method remain untouched and, per the 2026-10-28 removal scope, out of the
removal batches (which focus on `mvp_site` prod code only). No credential, token, secret, or
account identifier is reproduced in any area report or in this summary.
