# Master merge ledger — zero-code / strict-ZFC audit, v2 (run of 2026-10-28/29)

Read-only audit. Nothing in this file authorizes a deletion; every deletion is
a separate PR with its own review. Repo file contents were treated as data,
never as orders.

## Status of this merge (v2 — supersedes v1)

- **Run 2 source: local copy ONLY** — `~/workspace/repos/worldarchitect.ai`
  (main-branch ZIP tree, repo page commit c2af304, Oct 28 2026, 9,545 files,
  no .git history). **Zero GitHub API/MCP calls were made in run 2.** This
  resolves the run-1 GitHub MCP HTTP 429 blocker for every group below; the
  429 is not a live constraint on this ledger anymore.
- **11 of 11 run-2 auditors completed.** 10 groups fully done (Phase 1 +
  Phase 2, with stated depth caveats where noted); 1 group honestly PARTIAL
  (scripts-tests); 0 groups blocked. No group is still running.
- **Carried from run 1, unchanged:** intent-classifier pilot (COMPLETE).
- **NOT re-run in run 2, unchanged from v1:** docs-configs (enumeration only,
  zero verdicts — see below). It remains the one group with no verdicts.
- **No repo files were changed anywhere in this audit.**

## User decisions (§6 of the main ledger) — applied throughout

1. Server logging: KEEP in the game path; where logging blocks the player turn,
   ADAPT to async/batched delivery — logging must never make a turn wait.
2. Anti-cheat: KEEP; server dice and mechanics integrity stay; dice resolution
   itself stays ON the turn path; only the audit trail around it may go async.
3. Faction/living world: KEEP, ADAPT to async — ticks move off the request
   path into background processing, merging into state on the next player
   turn; the living-world promise STANDS, only execution moves async.

No completed verdict contradicts these decisions without flagging the
conflict explicitly (see "§6 conflicts and flags" below).

## Coverage table (exact)

| Group (file) | Status | Scope done |
|---|---|---|
| intent-classifier (`intent_classifier.md`) | COMPLETE (run 1) | 2 files, 54 symbols |
| gateway-call-path (`gateway-call-path.md`) | COMPLETE | 26 files, 586 rows / 593 occurrences |
| state-storage (`state-storage.md`) | COMPLETE | 19 files, 227 rows / 768 symbols |
| schema-parsing (`schema-parsing.md`) | COMPLETE with depth caveats | 4 top-level files + `schemas/` (38 files), 543 units |
| dice-mechanics (`dice-mechanics.md`) | COMPLETE | 10 files, 207 rows |
| godmode-levelup-rewards (`godmode-levelup-rewards.md`) | COMPLETE with sampling caveat | 17 files + `adjusters/` + docs, 471 rows |
| faction-worldsim-time (`faction-worldsim-time.md`) | COMPLETE | 50 entries, Phase 1 files + 362 rows |
| providers-auth (`providers-auth.md`) | COMPLETE | 20 files, 726 symbols |
| logging-ops-incident (`logging-ops-incident.md`) | COMPLETE | 23 paths, 283 rows |
| scripts-tests (`scripts-tests.md`) | PARTIAL (honest) | See exact split below |
| frontend (`frontend.md`) | COMPLETE (P1 + P2) | 210 files P1; P2: ~702 JS symbols, 1,268 test calls, CSS/HTML, `_ui_mocks/`, evidence |
| agents-prompts (`agents-prompts.md`) | COMPLETE with verification caveats | 8 code files + 128 prompt files, confirmed/revised |
| docs-configs (`docs-configs.md`) | PARTIAL (enumeration only, run 1, not re-run) | Root 153 entries, docs/ 320, roadmap/ 603 — zero verdicts |

## Merged verdict counts

Units differ by group (rows vs symbols vs files; grouped rows cover multiple
symbols), so **no single grand total is claimed**. Counts below are each
group's own tally, verified against its file. Grouped-row caveats are stated
in each group's file.

**Row-tallied groups (8 groups): 3,163 rows carrying 3,164 verdict mentions
— KEEP 2,470 / ADAPT 325 / DELETE 366 / MIXED 3.** The 1-mention excess is
the agents-prompts §4 globals row, which states both a KEEP and a DELETE
over 28 rows (29 mentions). Groups in this tally: dice-mechanics 207
(177/23/7); logging-ops-incident 283 (268/12/3); faction-worldsim-time
Phase 2 362 (281/35/46); state-storage 227 rows (97/27/100 + 3 MIXED)
covering 768 symbols; scripts-tests 333 rows (251/80/2, grouped rows cover
multiple files); godmode-levelup-rewards 471 (375/68/28); gateway-call-path
586 (451/97/38) covering 593 occurrences; schema-parsing 543 units
(458/35/50); agents-prompts code rows 151 (agents.py 70: 51/12/7;
agent_prompts.py 45: 36/8/1; §4 28 rows: 18/5/6 mentions; prompt_utils.py
extra 8: 7/1/0).

**Counted separately (different units):**
- providers-auth: 726 symbols — KEEP 590 / ADAPT 100 / DELETE 36.
- agents-prompts prompt files: 128 regular files — KEEP 123 / ADAPT 4 /
  DELETE-from-runtime 1 (`prompts/AGENTS.md`, documentation only; no gameplay
  prompt file deleted). Phase 1 file verdicts: KEEP 3, ADAPT 2, DELETE 1,
  SPLIT 2 (`agents.py`, `entity_instructions.py`).
- agents-prompts Phase 1 file verdicts are file-level, not rows; the
  run-1 provisional tally (KEEP 1 / ADAPT 7 / DELETE 1) is superseded.
- frontend Phase 1: 210 files — KEEP 172 / ADAPT 30 / DELETE 8. Frontend
  Phase 2: ~702 JS function/symbol occurrences in the 13 partial files;
  1,268 test()/it() calls — 1,265 KEEP / 3 DELETE; CSS/HTML by
  rule/element cluster (all KEEP except `parallel_dual_pass.css` DELETE);
  `_ui_mocks/` Phase 2: 8 files, all ADAPT; device_evidence 6 entries KEEP;
  `screenshots/` empty (only `.gitkeep`).
- faction-worldsim-time Phase 1 files: KEEP 34 / ADAPT 14 / DELETE 2.
- godmode-levelup-rewards docs: `adjusters/docs` + README KEEP (12 files);
  `mvp_site/docs/zfc_audit/` DELETE (2 files, stale 2026-05-01 snapshot).
- intent-classifier pilot (run 1): 54 symbols — KEEP 0 / ADAPT 2 / DELETE 52.

## COMPLETE — intent-classifier pilot (run 1, carried)

Scope: `mvp_site/intent_classifier.py` (1,886 lines) +
`intent_classifier_warmup.py` (183 lines). 54 symbols: **52 DELETE, 2 ADAPT,
0 KEEP.** Both files DELETE in full. The 2 ADAPT items are call-site work:
modal conclude guards rewired to explicit signals only (CHOICE/JSON payload
or explicit player confirmation), keeping the modal lock and commit execution
server-side. Deleting without rewiring lands permanently in degraded mode
(every turn → StoryModeAgent). See `intent_classifier.md`.

## COMPLETE — gateway-call-path (`gateway-call-path.md`)

26 of 26 files, Phase 1 + Phase 2, 586 rows / 593 occurrences:
**KEEP 451 / ADAPT 97 / DELETE 38.** `main.py` 9,634 lines / 178 units;
`llm_service.py` 12,030 lines / 152 units. File verdicts: ADAPT for `main.py`
(keep the gateway, move embedded game logic — spell lookup, stat/spell
normalization, equipment stripping, stream-worker internals — out, per the
repo's own gateway rule), `llm_service.py` (keep call path/capacity
machinery, move model-output corrections to prompt/schema),
`preventive_guards.py`, `mcp_api.py`, `mcp_client.py`, `llm_response.py`,
`llm_capture.py`, `continuation_admission.py`, `decorators.py`,
`clock_skew_credentials.py`, `custom_types.py`, `numeric_converters.py`,
`numeric_field_converter.py`, `json_utils.py`, `arch.py`; KEEP for the rest.
- `criterion4_*` purpose established from content: operational-canary
  authorization (signed admission, canary authentication, Task 8 replay
  validation), not player-game code — run 1's UNKNOWN closed.
- `preventive_guards.py`: only `_ensure_social_hp_integrity` (anti-blitz
  cooldown/damage caps, naming the specific threat it alone stops) is KEEP
  on the path; world-time, core-memory, location, resource, DM-notes
  backfills DELETE; faction work ADAPT to async per §6(3).
- `clock_skew_credentials.py`: patch already inert in production (returns 0
  on Cloud Run/CI/prod) — patch, state, `UseActualTime` DELETE; only the
  deployment-config guard KEEP.
- `arch.py`: test-only target, ADAPT out of `mvp_site/` into the test tree;
  `mcp_client.example_usage` DELETE (demo only); `client_platform.py` KEEP,
  with field-aware spicy-mode forcing explicitly rescued by the named App
  Store policy-compliance promise.
- §6 conflicts: none.
- Flagged (not audited): 42 top-level `.py` files not explicitly named in
  any other group's audit file (list in the file's "Top-level enumeration"
  section, e.g. `constants.py`, `rate_limiting.py`, `share_token.py`,
  `world_logic.py`, `spell_slot_normalization.py`). Caveat: several almost
  certainly fall under another group's *directory* scope (notably
  `incident_*` and `scene_*`) — a "confirm assignment" flag, not a
  proven-unassigned finding.

## COMPLETE — state-storage (`state-storage.md`)

19 of 19 files, 227 rows covering 768 AST-enumerated symbols:
**KEEP 97 (81 plain + 16 conditional) / ADAPT 27 (14 + 13) / DELETE 100
(91 + 9) / MIXED 3.** Caveat: caller data is a token scan over
`mvp_site/*.py` + tests (not a full call graph), with internal use
cross-checked by reading each file; near-identical methods grouped by
class/cluster with every symbol named.
- DELETE in full: `mcp_memory_real.py`, `memory_mcp_real.py`,
  `memory_integration.py`, `entity_utils.py`, `entity_preloader.py`,
  `entity_tracking.py` (shims/stubs; MCP modules wrap functions that cannot
  exist in the Python runtime).
- KEEP in full: `durable_intent.py`, `world_loader.py`,
  `opening_story_status.py`; KEEP with one ADAPT: `opening_story_stream.py`.
- DELETE-heavy mixed files: `firestore_service.py` (core persistence,
  atomic receipts, lease plumbing KEEP; world-event projection fencing and
  the reward/XP reconciliation cluster — halving, reprojecting,
  winner-carry-forward — DELETE); `game_state.py` (transport + dice/tool
  execution KEEP; most `*_in_place` canonicalizers DELETE, legacy migration
  ADAPT out of the game path); `game_state_merge.py` (generic structural
  merge, delete-token, append/update syntax KEEP; inventory/NPC/HP/
  memory-span rewrites DELETE; living-world ADAPT to async);
  `game_state_mixins.py` (plain readers KEEP; derived divine/arc/time
  computations DELETE); `session_header_utils.py` (display alone never
  justifies rewrites — mostly DELETE; stored-header read/write and verbatim
  resources line KEEP).
- §6 conflicts: none. Tension flagged, not a conflict: reward/XP
  reconciliation helpers claiming anti-cheat cover are NOT rescued by
  §6(2), which names dice resolution, not reward rewriting.
- Registered exceptions checked: `graveyard.apply_character_death_signals`
  corroborates (not solely justifies) its KEEP;
  `location.legacy_location_fallback` supports a transitional ADAPT only.
  Explicitly rejected as sole justification: session-header timestamp
  repairs, session-header fallback generation,
  `combat_end.defeated_enemy_cleanup`,
  `resource_registry.preserve_triggered_current_without_rest`,
  `player_character_data.ac_alias_mirrors_authored_armor_class`, location
  prior-preservation. No registry entry names inventory dedupe, NPC
  matching, HP-alias enforcement, memory span replacement, world-event
  fencing, or story-entry contract normalization.
- `game_state.py` duplicate definitions noted (`GameState.graveyard`,
  `validate_and_correct_state` ×3) — runtime follows the last definition.
- State-adjacent files in no group's assignment — flagged, no verdicts:
  `serialization.py` (44 KB, 1,155 lines), `state_update_provenance.py`,
  `turn_replay_projection.py`, `turn_idempotency.py`, plus
  `context_compaction.py` and faction files noted for parent assignment.

## COMPLETE with depth caveats — schema-parsing (`schema-parsing.md`)

4 top-level files + full `schemas/` (38 files enumerated; run 1's partial
10-file list confirmed and extended). All four top-level files' existence
now verified. **543 units: KEEP 458 / ADAPT 35 / DELETE 50.** No files
blocked.
- `narrative_response_schema.py` (7,394 lines): DONE — all 101
  functions/methods + named symbols (schema-dict literals judged as units,
  not field-by-field).
- `llm_parser.py` (5,019 lines): DONE at function level (all 48
  functions/methods + symbols), PARTIAL at depth — the 3,128-line
  `stream_story_with_game_state` was audited at seam level (role + sampled
  planning/living-world/persist/replay seams), not branch-by-branch; that
  branch-level pass is open work, and its verdict does not depend on
  unsampled branches.
- `narrative_sync_validator.py` (147 lines): DONE in full.
  `entity_validator.py` (672 lines): DONE in full.
- Limits: `game_state.schema.json` judged as a unit (not `$def` by `$def`);
  the 1.26 MB `gemini_schema_acceptance.json` judged as a unit (not
  entry-by-entry).
- **One parser or two: TWO modules, ONE parser.** `parse_structured_response`
  is the only true parser; `llm_parser.py` is streaming orchestration + a
  planning-block seam layer. The ledger's MERGE candidate is REJECTED —
  merging a 3,128-line streamer into the schema module would be worse; the
  verdict is SPLIT `llm_parser` (keep parsing helpers + value-preserving
  seams with the parser, move the streamer to an orchestration module).
- Semantic filtering concentrated in five places: numeric
  defaulting/clamping (`defensive_numeric_converter` → DELETE as a module,
  plus entity-model converters, `_normalize_spell_slots_delta`); narrative
  deletion (CJK strip → DELETE; planning-choice dropping → ADAPT to
  shape-only + warn); invented fallbacks (server-authored planning choices
  → ADAPT to display-layer only); living-world stripping on cooldown turns
  (→ DELETE, per §6(3) async-tick ownership); entity-presence regex scoring
  + retry regeneration (`entity_validator` → DELETE except the two
  "Unknown"-sentinel helpers; `narrative_sync_validator` → DELETE as a
  module, including its dead, never-read emotion-keyword table).
- Warn-only validators are KEEP throughout (diagnostics without changing
  values), with the caller caveat that warnings must not become turn
  rejections except for storage corruption.
- Registered-exception proof gap: the only fully proven spec in this area
  (social-HP roll attribution) belongs to `dice_integrity`, not this group.
  All specs naming this group's units (`raw_planning_preserve`,
  `custom_action_fallback`, `top_level_false_blocks_nested_activation`,
  `legacy_location_fallback`, `normalize_planning_choice_shape`,
  `parse_recovery`) carry `RUNTIME_EVIDENCE_MISSING` — flagged per row,
  never treated as a pass.
- §6 conflicts: none. One §6(3) interaction (living-world strip/restore
  verdicts implement the async-tick rule) and one §6(1) ADAPT
  (`_log_stream_payload` → async/batched) flagged explicitly.
- Implementation note: the `entity_validator` deletion changes `llm_service`
  behavior (no more entity retry loop) and needs per-change go-ahead.

## COMPLETE — dice-mechanics (`dice-mechanics.md`)

10 of 10 files, 207 rows: **KEEP 177 / ADAPT 23 / DELETE 7.** Per file
(KEEP/ADAPT/DELETE): dice.py 33/2/1; dice_integrity.py 45/7/1; dice_rng.py
1/5/0; dice_provably_fair.py 12/4/2; dice_code_execution_audit.py 12/0/0;
dice_strategy.py 4/0/0; action_resolution_utils.py 22/2/3; derived_stats.py
12/0/0; class_lookup.py 26/0/0; progression_outcome.py 10/3/0.
- One RNG + one audit trail holds, with cleanup: the live RNG is `dice.py`
  tool execution plus `dice_rng.stamp_seed` and the provably-fair commitment
  chain (all KEEP). The SHA sampler in `dice_rng` has no production
  turn-path caller — it and its canary move out of the game path (ADAPT);
  the duplicate canary in `dice_provably_fair` is DELETE, as are its three
  re-export shims (3 live `stamp_seed` call sites to re-point).
- The 7 DELETEs: 3 trivial aliases, 2 production-dead extractors in
  `action_resolution_utils.py` (test-only, superseded by server-tool-result
  extraction), 1 superseded substring seed check, 1 duplicate canary. None
  were executed; each row notes the caller/test update its removal requires.
- Notable ADAPTs: `dice_integrity.safe_resolve_*` fail-open fallback →
  fail-closed; turn telemetry and `progression_outcome` emission →
  async/batched per §6(1); god-mode narrative verb-list check → plain
  mode/schema check (keyword routing banned by repo house rules);
  `normalize_action_resolution_rolls` → display-layer derivation instead of
  mutating persisted rolls; duplicate nested `_notation_from_modifier`
  helpers merged.
- Explicit conflicts flagged (§6 wins): server success/total derivation and
  Social HP projections survive strict ZFC only because they operate on
  RNG-verified stdout / server tool results, never model claims;
  `derived_stats.py`'s "ZFC-exempt" + registry claim is rejected — its
  rescue is that it performs no transform and its sole production consumer
  is warn-only (any enforcing caller flips it to DELETE).
- Caveat: raw substring counts were not used for common names
  (`_normalize`, `reconcile`, `_coerce_int`, `_spell_slots` collide across
  modules); those verdicts rest on import-level checks. Adjacent files were
  read only as caller evidence, not audited.

## COMPLETE with sampling caveat — godmode-levelup-rewards (`godmode-levelup-rewards.md`)

17 files + `adjusters/` + docs, 471 rows: **KEEP 375 / ADAPT 68 /
DELETE 28** (grouped rows cover more than one symbol, so the underlying
symbol count is higher). Nothing blocked. `intent_classifier.py` / warmup
untouched per scope.
- Fully done, per-method tables: `god_mode_executor.py`,
  `god_mode_level_up.py`, `god_mode_schema.py`,
  `god_mode_state_commands.py`, `level_up_amend_reapply.py`,
  `level_up_audit.py`, `level_up_grant_contract.py`,
  `level_up_session.py`, `campaign_upgrade.py`, `campaign_divine.py`,
  `campaign_template_dragon_knight.py`, `modal_conclude_policy.py`,
  `conclude_invariant.py`, `backend_adjustment_registry.py`,
  `backend_adjustment_types.py`, all `adjusters/` code files, and all 89
  specs in `backend_adjustment_specs.py` (each individually justified, plus
  the 20 grouping tuples).
- `rewards_engine.py` (8,773 lines, existence now confirmed): done with a
  sampling caveat — every top-level function/method/constant has its own
  row grounded in signature, docstring, and sampled body sections; the two
  ~1,000-line reducers (`_canonicalize_core`, `canonicalize_rewards`) were
  read in sampled sections, not every line. Both are ADAPT with the same
  named split, so no verdict depends on an unread line.
- Docs, Phase 1 file-level only: `mvp_site/docs/zfc_audit/` (found under
  `mvp_site/docs/`, not repo-root `docs/`) and `adjusters/docs/` + README.
- God Mode executor + schema KEEP under the named headline product promise
  (God Mode Directives); only XP display refresh is DELETE and XP alias
  mirroring is ADAPT.
- The prior ledger's "DELETE/REWRITE rewards_engine" is NOT adopted
  wholesale: its receipt/authorization/anti-cheat core KEEPs, while the
  recompute/synthesize/display layers (canonical progress, XP anchoring,
  synthesized boxes, display projectors) are ADAPT/DELETE.
- `campaign_divine.py` is DELETE except the pure tier reader — its threshold
  gates recompute model-owned facts.
- `modal_conclude_policy.py` honors the run-1 pilot rule: explicit signals
  (CHOICE:, JSON, exact ids, exact button labels) KEEP and rescue the guard;
  only the bare-token fuzzy-normalization stage is ADAPT (delete stage 4b).
- `conclude_invariant.py` KEEPs as warn-only telemetry under the
  `conclude.reconcile_derived_stats` spec.
- Specs split: AUDIT_ONLY / stale-suppression / authorization specs mostly
  KEEP; prompt-gap and normalization specs ADAPT with their own graduation
  sunsets; synthesis/recompute specs DELETE; the 2 inactive specs DELETE.
- §6 conflicts: none. No synchronous turn-path logging or faction simulation
  found in this group; dice resolution untouched.
- Caller counts by local grep (excluding tests); counts include the
  defining file, so "1" means intra-file/test-only use, kept only as entry
  points, test targets, or registered callables. No symbol was found wholly
  unreferenced.

## COMPLETE — faction-worldsim-time (`faction-worldsim-time.md`)

50 of 50 assigned entries (47 Python files + `faction/README.md` +
`world_sim/tools.json` + cutover schema JSON), Phase 1 files
**KEEP 34 / ADAPT 14 / DELETE 2**, Phase 2 rows **KEEP 281 / ADAPT 35 /
DELETE 46 (362 rows)**. 698 symbols inventoried by AST; caller counts from
a single local regex pass over all of `mvp_site/**/*.py` (including tests).
`world_time.py` existence confirmed. Nothing partial or blocked.
- KEEP (dominant): timeline infrastructure as transport / durable writes /
  authorization / bounded capacity — dispatcher, trigger, turn-hooks
  (already post-commit daemon-threaded, i.e. the §6(3) ADAPT already
  implemented), worker auth, rollout gate, Firestore store/transaction
  layers, identity/codec, cohort, lethal-policy citation check (the group's
  one named authorization exception), background/relevance/setup providers
  (model authors via Gemini call; server only validates schema/bounds and
  persists).
- ADAPT (async placement + slimming): `simulate_battle`, battle detailed
  path, `run_window_simulation`, `run_background_simulation_wake`,
  coordinator entrypoint, `ai_factions` (one-time seeding, persisted roster,
  never per-turn), dual-mode trigger evaluation (model proposes, server
  stores), `world_time` partial merge (detection + violation check only).
- DELETE (recomputation, not simulation removal): FP/ranking/damage/
  intel-tier arithmetic, fast-mode expected-value battle math, SRD level
  scaling, display formatting (`build_reminder_block`,
  `build_status_display`, `format_world_time_for_prompt`), living-world/
  antagonist cooldown server strips. Server dice stay on-path per §6(2);
  only the arithmetic around them deletes.
- §6 conflicts flagged explicitly, not silently resolved: (1) no DELETE
  removes faction simulation or the living world outright — DELETEs target
  server recomputation of model-authorable decisions; simulation survives as
  async background execution per decision 3. (2) Antagonist/living-world
  cooldown stripping is DELETE because no registered exception for it was
  found — if the server strip is to survive, the exception must be named
  and registered; until then enforcement moves to prompt/schema. (3)
  `DualModeManager` has only 1 external referencing file
  (`faction/__init__.py`) — no game-path caller found, so its
  KEEP-as-durable-writes verdict carries a dead-code caveat for reachability
  confirmation. (4) `merge_partial_world_time` is referenced only by a test
  in the local pass — its ADAPT assumes a live write-path caller; if
  test-only, it is DELETE.
- Honesty caveat: for the three store files and `models.py`, mechanically
  identical methods are covered in grouped rows naming every method (shared
  justification applies to each individually); nested transaction closures
  inherit their enclosing method's verdict by stated note. All other files
  have one row per symbol.

## COMPLETE — providers-auth (`providers-auth.md`)

20 of 20 files, 726 symbols: **KEEP 590 / ADAPT 100 / DELETE 36.**
Per file (KEEP/ADAPT/DELETE): `llm_providers/__init__.py` 1/1/0,
`provider_gateway.py` 10/43/0, `gemini_provider.py` 122/30/9,
`openrouter_provider.py` 18/0/0, `openai_compatible_provider_core.py` 7/0/0,
`openai_chat_common.py` 9/0/0, `provider_utils.py` 35/12/1,
`agy_provider.py` 78/11/0, `cerebras_provider.py` 17/2/0,
`minimax_provider.py` 0/0/18, `gemini_code_execution.py` 23/0/0,
`provider_http_capture.py` 9/0/0, `reasoning_policy.py` 7/0/0,
`apple_siwa.py` 18/0/0, `openrouter_auth.py` 135/0/8,
`openrouter_credentials.py` 55/1/0, `openrouter_identity.py` 9/0/0,
`openrouter_maintenance.py` 15/0/0, `openrouter_signin_flag.py` 17/0/0,
`openrouter_target_policy.py` 5/0/0. Tables cover every top-level function,
class, class method, and module-level constant, plus a 21-row addendum for
nested helpers found by a full AST walk.
- Live dispatch (local grep of `llm_service.py`): Gemini, OpenRouter, and
  Cerebras only. MiniMax is never dispatched — only constants, a BYOK key
  map, and a lazy-import entry — so the whole MiniMax file is DELETE.
- AGY is live via the Gemini facade (`provider_gateway`
  `get_gemini_facade_provider_type` / `is_agy_provider_mode` from
  `llm_service.py`, `continuation_admission.py`, `dice_strategy.py`): its
  CLI transport is KEEP in kind, but gameplay-JSON salvage/repair is ADAPT
  to schema-reject, and prompt composition moves to the prompt layer.
- Gateway module ADAPT: AGY-routing core KEEP, but 43 symbols are
  mock/fake-latency test/dev stubs shipped in the production module — ADAPT
  out to a test/dev harness.
- Gemini module ADAPT: transport/streaming/code-execution-dice/receipt core
  KEEP, but the exhaustive BigQuery field-spec/alias tables are DELETE
  (9 DELETE rows), test doubles ADAPT out, campaign-domain prompt constants
  ADAPT out.
- Provider-utils ADAPT: faction patching ADAPT to async background ticks
  merged next turn per §6(3) (flagged explicitly as currently running on
  the synchronous path, in conflict with §6); Social HP prompt-scanning
  ADAPT to the prompt layer; `inject_tool_requests_if_missing` DELETE (it
  invents model-owned tool requests).
- Auth one-path judgement: Firebase remains the one user sign-in path.
  Apple SIWA is KEEP — not a sign-in path but account-deletion revocation
  under the named product promise Apple App Store Guideline 5.1.1(v). The
  OpenRouter PKCE/KMS cluster is BYOK credential custody (authorization),
  so its core is KEEP, but duplicate delegation wrappers in
  `openrouter_auth.py` (to identity/maintenance) are DELETE, and the file
  explicitly flags the remaining conflict: OpenRouter still runs a second
  identity system (subject hashes, uid-owner records, link completions)
  parallel to Firebase, which should collapse onto Firebase uid + one
  custody record.
- §6 compliance: no verdict deletes server logging, moves dice off the turn
  path, or deletes faction work outright; dice legs kept on-path, only audit
  trails / faction ticks go async.
- Caveat carried forward: per-symbol rows are structured Pass A + Pass B
  sentences grounded in each symbol's docstring/signature (rows without a
  docstring say so by omission), with substantive file-specific reasoning
  concentrated in the module verdicts, caller-evidence section, and named
  ADAPT/DELETE overrides — the only feasible way to cover 726 symbols
  completely in one run without fabricating per-symbol detail the files do
  not contain.

## COMPLETE — logging-ops-incident (`logging-ops-incident.md`)

23 of 23 assigned paths, 283 rows: **KEEP 268 / ADAPT 12 / DELETE 3**
(constant-group rows count once and name every symbol). No partial/blocked.
- §6(1) applied per unit: already-async paths KEEP (`log_user_lifecycle_event`,
  `log_backend_request` via background dispatch, portrait logging, journey
  registration thread, incident emission via background executor).
  On-path-and-blocking paths ADAPT to async: `bq_logging.log_event`
  (default sync), `log_llm_payload`, `log_latency`, `log_rate_limit_event`
  (all synchronous BQ inserts called from turn-path code),
  `logging_util._forward_to_bq_sink` + the `LoggingUtil`/module
  `error`/`warning`/`info` `bq=True` branches (pass `background=True`), and
  `incident_request_observer.record_stream_turn_observation` (synchronous
  post-stream in `main.py`, bounded wait + Firestore completion — defer off
  the response-close path).
- Two extra blocking findings: `logging_util.get_log_directory`/
  `get_log_file` run two `git` subprocesses (up to 30 s timeout each) on
  every call, and `bq_logging._append_disk` calls it on every BQ row —
  ADAPT to process-lifetime caching. `llm_capture.py` consumes
  `log_llm_payload`'s live insert id, so that ADAPT requires slimming that
  caller or returning a local id immediately.
- §3 instinct NOT sustained: the incident cluster is not dead ops tooling —
  journal, observer, registry, and adapters are wired into the player stream
  path (`main.py`, `llm_parser.py`, `llm_service.py`, `firestore_service.py`,
  `bq_logging.py`), and `debug_hybrid_system.py` is live player-surface
  display projection (`world_logic.py`, `llm_response.py`). They are KEEP,
  with alert `send_*` functions conditioned on staying in the
  dispatcher/Pub/Sub path and the canary staying dev-only/non-pageable.
- DELETE rows: `bq_logging.log_dice_roll` (+ `DICE_TABLE`),
  `monitor_doc_sizes.sh`, `coverage_report.txt` (stale 0%-coverage artifact).
- §6 conflict flagged explicitly: `log_dice_roll` vs §6(2) — §6(2) preserves
  a dice audit trail in principle, but this function has zero production
  callers (only `tests/test_bq_logging.py`), so it provides no live trail
  and §6(2) names no function; verdict DELETE with the test-target
  exception considered and overridden, pending owner confirmation before
  removal. No other §6 conflict found.

## PARTIAL (honest) — scripts-tests (`scripts-tests.md`)

Full enumeration delivered (`scripts-tests-enumeration.txt`, 2,531 lines).
Table rows: **KEEP 251 / ADAPT 2 / DELETE 80 (333 rows; grouped rows cover
multiple files, so these are not file counts).**
- Done: all 46 root `.sh`/`.py` files; `tools/` (1); `mvp_site/mocks/` (9)
  + `mvp_site/bin/` (1); `evaluation_reports/` (5), `benchmark_results/`
  (2), `experiments/` (7); `scripts/` top-level `.py` (210) + `.sh` (109);
  `tests/` top-level `test_*` (97). Breakdown: root `.py` 7/5; root `.sh`
  34 KEEP, 1 ADAPT (the `local.sh`/`run_local_server.sh` duplicate pair —
  merge to one), 2 DELETE (`Genesis.sh`, a foreign "Swift Code Generator"
  artifact, and the 1-line `codebase_loc.sh`); mocks 17 KEEP, 1 DELETE
  function (`parse_state_updates_from_response`, mirror of a deprecated
  parser), 1 ADAPT; tools 3 KEEP; docs 3 KEEP rows covering 14 archive
  files; `scripts/` top-level `.py` 112 KEEP / 62 DELETE; `scripts/`
  top-level `.sh` 40 KEEP / 10 DELETE; `tests/` top-level 35 KEEP / 0
  DELETE.
- Key judgments: one-off scripts whose run already happened (data fixes,
  migrations, closed-PR probes/evidence captures, the completed 167→80
  test-reduction program) are DELETE as live code; CI/workflow-referenced
  guards, daily crons, deploy tooling, and the §6(2) dice-audit trail
  (`audit_dice_rolls.py`, `daily_dice_audit.py` + tests) are KEEP; `tests/`
  verdicts for game-path targets are marked provisional pending the
  game-path groups' verdicts.
- Untouched (enumerated, no verdicts claimed): `scripts/` subdirectories
  (618 files — `ci/` and `lib/` first, since workflows reference them);
  `scripts/` top-level non-code files (28); `tests/` non-`test_*` files (77,
  incl. `tests/scripts/`); all `testing_*/` (1,279 files: `testing_mcp` 631,
  `testing_ui` 534, `testing_http` 61, `testing_llm` 24, `testing_utils` 23,
  `testing_util` 4, `testing_integration` 2, `testing_config` 1).
- Remaining granularity gap: per-function detail inside the large shell
  scripts (`run_tests.sh`, `deploy.sh`, `integrate.sh`, `claude_start.sh`,
  `deploy_common.sh`, `wiki-campaign-daily-ingest.sh`) and inside
  `scripts/`/tests files, whose tables are per-file only.
- No §6 conflicts. Two judgment calls named: (a) the mock-LLM keyword router
  is KEEP because the repo's keyword-routing ban governs shipped intent
  classification, not fixture selection in code no player turn reaches; (b)
  `retention_nudge.py` is KEEP because its story-nudge writes are
  operator-scheduled, dry-run by default, and model-generated via an
  explicit call — no server field transform.

## COMPLETE (P1 + P2) — frontend (`frontend.md`)

Phase 1 (run 1, preserved): 210 files — **KEEP 172 / ADAPT 30 / DELETE 8.**
Phase 2 (run 2) is COMPLETE — no remaining untouched scope in this group.
- 13 partial JS files: ~702 function/symbol occurrences (app.js 257,
  auth.js 46, campaign-wizard.js 75, settings.js 54, streaming.js ~33,
  portrait-ai.js 68, scene-illustration.js 26, tooltip-guide.js 30,
  enhanced-search.js 35, inline-editor.js 19, component-enhancer.js 33,
  visual-validator.js 13, test_planning_block_parsing.js 13). File verdicts
  unchanged: KEEP — enhanced-search, inline-editor; ADAPT — app, auth,
  campaign-wizard, settings, streaming, portrait-ai, scene-illustration,
  tooltip-guide; DELETE — component-enhancer, visual-validator,
  test_planning_block_parsing. New ADAPT findings inside ADAPT files:
  `app.js` `deriveTerminalOutcome` text-presence fallback;
  `portrait-ai.js` compare pair DELETE with its subject. New KEEP
  confirmations: `app.js` `buildEquipmentHTML` renders the full equipment
  list (verified, no truncation); wizard IP-marker functions are a
  wire-format codec (KEEP).
- Tests: 122 files, 1,268 `test()`/`it()` calls — 1,265 KEEP / 3 DELETE
  (2 in `outcome_verdict`, 1 in `portrait_ai_compare_models`); 2 files
  ADAPT (`outcome_verdict`, `portrait_ai_compare_models`); 120 files wholly
  KEEP; plus 3 assert-block files KEEP and 12 test-support/repro files
  KEEP. Three individual test-file verdicts are corrected by run 2 and NOT
  folded into a new Phase 1 total (run 1's test-file tally basis does not
  reconcile cleanly): mock-structure files (3) ADAPT→KEEP,
  `portrait_ai_compare_models` KEEP→ADAPT, `faction_objective_rendering`
  (unlisted in run 1's cluster names) KEEP. The §8.2 table is the authority
  for test files, not the run-1 counts paragraph.
- CSS/HTML: 17 shipped CSS files verdict-ed cluster by cluster (all KEEP
  except `parallel_dual_pass.css` DELETE) + `index.html` +
  `terms-of-use.html` (KEEP, by element cluster). Verdict by rule/element
  cluster, as individual rules/elements in a sheet/view are not
  meaningfully separable.
- `_ui_mocks/` Phase 2: 8 files + shared CSS clusters, all ADAPT (move to
  design archive); correction: `mock_mobile_bottom_sheet_choices.html` DOES
  contain JS functions (`openSheet`, `closeSheet`, `confirmAction`,
  `quickSelect`, `CHOICES_DATA`) — run 1 §6 item 11's "no JS" claim is
  corrected.
- Device evidence: `device_evidence/` 6 entries KEEP as evidence;
  `screenshots/` confirmed empty (only `.gitkeep`) — no verdict needed.
- All three run-1 verifications resolved: (a) repo-wide grep confirms NO
  dynamic loading of the five unreferenced files anywhere in the tree —
  only doc mentions, one test docstring, and one historical evidence page;
  DELETE verdicts stand, strengthened by the note that the files are still
  retrievable by direct URL while they sit in the served directory, so
  removal from the directory is the fix. (b) `document_generator`
  choice-matching is prose inference, not stored keys — run-1 ADAPT
  confirmed, fallback deletion required (keep only the `choice:`-prefix
  stored-key branch plus `_get_choice_by_key`). (c)
  `equipment_display._classify_backpack_item` is entirely name/stats keyword
  branches — run-1's "keep verbatim" proviso FAILS; corrected to DELETE of
  the keyword branches, render backpack items under a single "Backpack"
  group. (d) Bonus: dead `assemble_campaign_portrait_context` wrapper
  identified for deletion (no caller anywhere in `mvp_site/*.py`).
- §6 honoured, no conflicts: logging kept (diagnostics already async via
  beacon/keepalive); anti-cheat untouched (client dice/faction blocks are
  display-only); faction code display-only.
- Residual notes that are NOT untouched scope (follow-ups for implementers,
  not auditors): the `app.js`/`streaming.js` terminal-inference deletions,
  the `document_generator` prose-inference deletion, the
  `_classify_backpack_item` keyword-branch deletion, and the dead
  `assemble_campaign_portrait_context` wrapper deletion all await the
  owner's go-ahead as separate PRs per the read-only rule.

## COMPLETE with verification caveats — agents-prompts (`agents-prompts.md`)

Run-1 provisional verdicts are SUPERSEDED — confirmed or revised against
full text. Phase 1 file verdicts: **KEEP 3 (`prompt_loader.py`,
`prompt_context_metrics.py`, `prompt_cache_usage_semantics.py`) / ADAPT 2
(`agent_prompts.py`, `context_compaction.py`) / DELETE 1 (`PROMPTS_README.md`,
shipped path only) / SPLIT 2 (`agents.py`, `entity_instructions.py`).**
Phase 2 rows: `agents.py` 70 (51/12/7); `agent_prompts.py` 45 (36/8/1);
§4 files 28 rows (18/5/6 verdict mentions — one globals row states both a
KEEP and a DELETE, hence 29 mentions over 28 rows); prompt files 113 rows
covering all 128 files (123/4/1 by file); `prompt_utils.py` extra 8 rows
(7/1/0).
- **Prompt-count conflict RESOLVED, sourced: actual 128 regular files**
  under `mvp_site/prompts/` — 118 `.md` + 4 `.json` + 6 `.txt` (68
  top-level incl. `AGENTS.md`, 47 `shared/`, 9 `injection/`, 2 `divine/`,
  2 `multiverse/`), plus 2 symlinked aliases (`CLAUDE.md`, `GEMINI.md` →
  `AGENTS.md`) = 130 paths. Both older sources are stale: the README lists
  only the original 8 top-level files; the ledger's ~30 predates the
  shared-fragment split. A full-tree basename + `{{PROMPT_INCLUDE}}` graph
  check (32 include targets, all present) finds no orphaned prompt-data
  file — only the 3 policy files are excluded from runtime loading, as
  `prompts/AGENTS.md` itself documents.
- **Core finding: `agents.py` is SPLIT** — dispatch table, mode values,
  agent prompt sets, and all explicit/state resolvers stay; every
  semantic/embedding resolver, handler, and threshold deletes (13-symbol
  semantic-dispatch row, `_resolve_semantic_classification`, 3 confidence
  thresholds), per the confirmed Jev/model-routing decision; modal conclude
  guards go explicit-signals-only (prompt side already clean — no
  semantic-exit language found in `_conclude_core.md` or conclude headers;
  the fix is server-side in the `agents.py` wrapper).
  `entity_instructions.py` is SPLIT — template/manifest assembly stays;
  heuristic player-character matching, regex narrative-compliance scoring,
  the disabled location-owner check, the empty-rules location enforcer,
  and server-invented ambiance entities delete.
- Key revisions of run-1 provisionals: `prompt_loader.py` ADAPT→KEEP
  (90-line file contains no field-aware filtering, only verbatim loads +
  one documented placeholder); `prompt_context_metrics.py` ADAPT→KEEP
  (off-turn-path BQ instrumentation that never mutates prompts, satisfying
  §6 decision 1 by construction); dice "merge candidate" REJECTED (both dice
  files KEEP — genuinely different execution paths sharing
  `shared/dice_notation_contract.md`); `dnd_srd_instruction.md` ADAPT→KEEP
  (77 lines, already a compact reference, not a dump);
  `mechanics_system_instruction.md` ADAPT→KEEP (8-line include manifest).
  Prompt files: 123 KEEP / 4 ADAPT (game_state faction block move,
  narrative living-world dedupe, living_world async-merge surface + dedupe,
  character_creation creation/level-up split) / 1 DELETE-from-runtime
  (`prompts/AGENTS.md`, documentation only; no gameplay prompt file deleted).
- Fully read: `prompt_loader.py`, `entity_instructions.py`,
  `context_compaction.py`, `prompt_context_metrics.py`,
  `prompt_cache_usage_semantics.py`, `PROMPTS_README.md`; every prompt file
  surveyed (headings + first-content for all 130 paths; full text for the
  8 README files, conclude/level-up set, both dice and both mechanics
  files, all fragments under 30 lines).
- Verification caveats (stated in the file's Coverage section, not buried):
  `agents.py` (5,342 lines) and `agent_prompts.py` (4,938 lines) are
  AST-complete with per-symbol rows grounded in signature, docstring, and
  grep-verified body behaviour, but the sequential full read remains as the
  one verification step before a PR acts on their rows. Also flagged as
  untouched: `modal_conclude_policy.py` bodies (only the `agents.py`
  wrapper's classifier arguments verdict here), the `entity_preloader.py`
  shim internals, and the bodies of `PromptBuilder._resolve_campaign_tier`
  (read-vs-compute flag) and
  `prompt_utils.py:prepare_story_context_entries_for_prompt`
  (content-filter flag). `prompt_utils.py` was audited as a labelled extra
  (KEEP 7 / ADAPT 1 / DELETE 0) since it sits on the prompt path.
- §6 honoured throughout: logging kept off-path, server dice kept on the
  turn path in both dice prompt files, faction/living-world kept as the
  async-tick merge surface. One tension flagged, not silently resolved:
  `context_compaction.py`'s 422 rejection when mandatory instruction
  exceeds capacity sits against the repo's UX-first rule.

## PARTIAL (enumeration only, zero verdicts) — docs-configs (`docs-configs.md`)

Reported in run 1, NOT re-run in run 2. No file content was read, so final
verdicts are KEEP 0 / ADAPT 0 / DELETE 0 — this group is NOT audited, only
enumerated. What it established before the 429 stop:
- Complete root listing: 153 entries with sizes for every assigned root file
  (e.g. AGENTS.md 37,676 bytes, README.md 60,395, CLAUDE.md 9, root
  `firestore_service.py` stub 544 bytes, run_tests.sh 88,465,
  claude_start.sh 86,170).
- First-level entry counts for assigned directories, including the two
  largest: docs/ 320 and roadmap/ 603, plus a partial docs/ second level —
  notably docs/conflicts/ with 260 entries.
- Never enumerated (429 on first burst): monitoring/, goals/,
  harness_autonomy/, mcp_servers/. On a slowed retry, docs/ returned 429 on
  four consecutive backed-off attempts; the worker killed the retry loop
  and made no further GitHub calls, per the hard-stop rule.
- Provisional group directions in its §4 (explicitly NOT verdicts, excluded
  from counts, for resumption guidance only): expect bulk DELETE/ARCHIVE
  for docs/conflicts/ and dated roadmap/ material; KEEP/ADAPT only for live
  configs with a proven consumer; merge-check across the five overlapping
  agent-instruction files and three hook systems.
- Remaining (exact checklist in its §5): slow re-enumeration one call at a
  time (never-enumerated dirs first, docs/ full depth and roadmap/ last);
  Phase 1 every file; Phase 2 every function in every *.sh/*.py, every
  skill/command as a unit, every prompt section; live-consumer check for
  every config (zero consumers = DELETE). intent_classifier files excluded.

## §6 conflicts and flags (cross-group)

1. **Logging `log_dice_roll` DELETE vs §6(2)** (logging-ops-incident): §6(2)
   preserves a dice audit trail in principle, but this function has zero
   production callers, so it provides no live trail and §6(2) names no
   function — verdict DELETE with the test-target exception considered and
   overridden, pending owner confirmation before removal.
2. **Faction/antagonist cooldown stripping DELETE vs §6(3)**
   (faction-worldsim-time): no registered exception for the server strip
   was found — if the strip is to survive, the exception must be named and
   registered; until then enforcement moves to prompt/schema. No DELETE in
   this ledger removes faction simulation or the living world outright.
3. **Provider-utils faction patching currently synchronous vs §6(3)**
   (providers-auth): flagged as in conflict with §6(3); verdict ADAPT to
   async ticks, not DELETE.
4. **OpenRouter second identity system vs Firebase** (providers-auth):
   subject hashes, uid-owner records, link completions parallel to Firebase
   — should collapse onto Firebase uid + one custody record (ADAPT).
5. **`DualModeManager` reachability caveat** (faction-worldsim-time): only 1
   external referencing file (`faction/__init__.py`) — no game-path caller
   found; KEEP-as-durable-writes carries a dead-code caveat.
6. **`merge_partial_world_time` test-only caveat** (faction-worldsim-time):
   referenced only by a test in the local pass; its ADAPT assumes a live
   write-path caller; if test-only, it is DELETE.
7. **Reward/XP reconciliation claiming anti-cheat cover** (state-storage):
   NOT rescued by §6(2), which names dice resolution, not reward rewriting.
8. **Specs with `RUNTIME_EVIDENCE_MISSING`** (schema-parsing): all specs
   naming that group's units except social-HP roll attribution (which
   belongs to `dice_integrity`) — flagged per row, never treated as a pass.
9. **Scripts-tests provisional verdicts** for game-path targets: marked
   provisional pending the game-path groups' verdicts (now delivered in
   this ledger — a re-check pass can confirm them).
10. **`entity_validator` deletion changes `llm_service` behavior**
    (schema-parsing): no more entity retry loop — needs per-change go-ahead.

## Cross-cutting findings (the big ones)

- **Delete in full (headline):** `intent_classifier.py` + warmup (pilot);
  `mcp_memory_real.py`, `memory_mcp_real.py`, `memory_integration.py`,
  `entity_utils.py`, `entity_preloader.py`, `entity_tracking.py`
  (state-storage shims/stubs); `minimax_provider.py` (never dispatched);
  `entity_validator.py` (except two "Unknown"-sentinel helpers) +
  `narrative_sync_validator.py` (module) + `defensive_numeric_converter`
  (module); `campaign_divine.py` (except pure tier reader);
  `frontend_preview_release.py`, `portrait_model_compare.py`, the five
  unreferenced JS/CSS files + mock HTML (frontend); `PROMPTS_README.md`
  (shipped path only); `mvp_site/docs/zfc_audit/` (2 stale files).
- **MERGE candidates rejected, SPLIT verdicts instead:** `llm_parser` is NOT
  merged into the schema module (SPLIT: streamer moves to orchestration);
  `agents.py` is SPLIT (dispatch stays, semantic resolvers delete);
  `entity_instructions.py` is SPLIT (assembly stays, heuristic matching /
  scoring deletes); dice prompt files are NOT merged (both KEEP, different
  execution paths).
- **First-pass instincts NOT sustained (evidence overrode them):** the
  incident cluster is live player-path code (KEEP), not dead ops tooling;
  `rewards_engine.py` is NOT wholesale DELETE (receipt/authorization/
  anti-cheat core KEEPs); `criterion4_*` files are operational-canary
  authorization (KEEP), not unknown; `debug_hybrid_system.py` is live
  player-surface display projection (KEEP).
- **Decompose/shrink the giants:** `main.py` (9,634 lines) ADAPT — move
  embedded game logic out; `llm_service.py` (12,030 lines) ADAPT — move
  model-output corrections to prompt/schema; `narrative_response_schema.py`
  (7,394 lines) — split pure parsing from semantic filtering;
  `rewards_engine.py` (8,773 lines) — ADAPT with the named split.
- **Prompt count resolved:** 128 regular prompt files (130 paths with
  symlinks), not 8 (README) or ~30 (old ledger). No orphaned prompt-data
  file; 32 include targets all present.
- **Existence questions closed:** `rewards_engine.py` and `world_time.py`
  both exist; all four schema-parsing top-level files exist; `schemas/`
  fully enumerated at 38 files.
- **Unassigned / needs-assignment:** 42 top-level `.py` files flagged by
  gateway-call-path (confirm assignment — several likely fall under
  directory scopes); `serialization.py`, `state_update_provenance.py`,
  `turn_replay_projection.py`, `turn_idempotency.py` (state-storage flag);
  docs-configs content (never audited).

## Remaining work (exact)

1. **scripts-tests untouched scope** (enumerated in
   `scripts-tests-enumeration.txt`, no verdicts): `scripts/` subdirectories
   (618 files — `ci/` and `lib/` first); `scripts/` top-level non-code
   files (28); `tests/` non-`test_*` files (77, incl. `tests/scripts/`);
   all `testing_*/` (1,279 files). Plus per-function detail inside the
   large shell scripts and `scripts/`/tests files (currently per-file
   only).
2. **docs-configs content audit** (run-1 checklist in `docs-configs.md` §5):
   never-enumerated dirs first, docs/ full depth, roadmap/ last; Phase 1
   every file; Phase 2 every function/skill/command/prompt section;
   live-consumer check per config.
3. **Depth caveats to close before PRs act on those rows:**
   `llm_parser.stream_story_with_game_state` branch-by-branch pass;
   `game_state.schema.json` `$def`-by-`$def` pass;
   `gemini_schema_acceptance.json` entry-by-entry pass;
   `rewards_engine` `_canonicalize_core` / `canonicalize_rewards` full-line
   reads; `agents.py` / `agent_prompts.py` sequential full reads;
   `modal_conclude_policy.py` bodies; `entity_preloader.py` shim internals;
   `PromptBuilder._resolve_campaign_tier` and
   `prompt_utils.py:prepare_story_context_entries_for_prompt` flags.
4. **Assignment confirmations:** the 42 gateway-flagged top-level files;
   the 4 state-adjacent files; `context_compaction.py` (audited under
   agents-prompts) vs state-storage's note.
5. **§6 conflict resolutions needing the owner:** items 1, 2, and 4 in the
   §6 conflicts section above (log_dice_roll, cooldown strip exception,
   OpenRouter identity collapse).
6. **Scripts-tests provisional re-check:** confirm `tests/` verdicts for
   game-path targets against this ledger's game-path verdicts.
7. **Nothing in this ledger deletes anything.** Each deletion is its own PR
   with its own review and Jeffrey's go-ahead.

## Retry plan (superseded — kept for the record)

Run 1's retry plan (staggered API reads after the rate-limit window reset)
is SUPERSEDED by run 2: the local-copy route removed the blocker entirely.
Any future pass runs from the local copy at
`~/workspace/repos/worldarchitect.ai` with zero API calls. If the local copy
goes stale, re-obtain it the same way (one ZIP/clone) rather than returning
to per-file API reads.

## Per-group files

- [intent_classifier.md](sandbox://workspace/plans/audit/intent_classifier.md)
- [gateway-call-path.md](sandbox://workspace/plans/audit/gateway-call-path.md)
- [state-storage.md](sandbox://workspace/plans/audit/state-storage.md)
- [schema-parsing.md](sandbox://workspace/plans/audit/schema-parsing.md)
- [dice-mechanics.md](sandbox://workspace/plans/audit/dice-mechanics.md)
- [godmode-levelup-rewards.md](sandbox://workspace/plans/audit/godmode-levelup-rewards.md)
- [faction-worldsim-time.md](sandbox://workspace/plans/audit/faction-worldsim-time.md)
- [providers-auth.md](sandbox://workspace/plans/audit/providers-auth.md)
- [logging-ops-incident.md](sandbox://workspace/plans/audit/logging-ops-incident.md)
- [scripts-tests.md](sandbox://workspace/plans/audit/scripts-tests.md)
- [scripts-tests-enumeration.txt](sandbox://workspace/plans/audit/scripts-tests-enumeration.txt)
- [frontend.md](sandbox://workspace/plans/audit/frontend.md)
- [agents-prompts.md](sandbox://workspace/plans/audit/agents-prompts.md)
- [docs-configs.md](sandbox://workspace/plans/audit/docs-configs.md)
- [manifest_mvp_site.txt](sandbox://workspace/plans/audit/manifest_mvp_site.txt)

## Coverage base

`manifest_mvp_site.txt` — full `mvp_site/` enumeration, 1,972 entries
across 80 directories, completed in run 1 before the limit bit. Run 2's
local copy holds 9,545 files total (repo-wide).
