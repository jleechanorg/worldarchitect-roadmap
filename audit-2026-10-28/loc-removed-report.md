# LOC removed if every DELETE verdict were applied

Source: WorldArchitect.AI zero-code / strict-ZFC audit, run 2 (local copy, main @ c2af304)
plus the run-1 intent-classifier pilot. Code tree: `~/workspace/repos/worldarchitect.ai`
(9,545 files, ZIP tree, no `.git` history). Audit files: `~/workspace/plans/audit/`.
Computation script: `~/workspace/plans/audit/loc-removed-compute.py` (v3 run).

## Headline result — mvp_site production code only

| Component | Lines |
|---|---|
| Whole-file DELETEs (19 files) | 5,758 |
| In-file DELETE symbol spans (50 files, 389 symbols) | 11,086 |
| **Grand total, headline scope** | **16,844** |

The 5,758 whole-file lines are exact `wc -l` counts. The 11,086 in-file lines are
AST-derived symbol spans (see Method). The total is exact-plus-estimate in this sense:
whole-file lines are exact; in-file lines are exact spans of the named symbols, but a
symbol span counts every line from its first decorator line through its `end_lineno`,
including interior blank lines and comments, and excluding trailing blank lines.
Nothing uncertain was added to the total — uncertain items are listed in §(c) only.

Scope rule (per Jeffrey's direction): headline = the shipped game path under `mvp_site/`
— backend Python plus the shipped `mvp_site/frontend_v1` UI — excluding test files
(`*/tests/*`, `test_*.*`, `*_test.*`, test-only helpers such as `mvp_site/mocks/`),
excluding `mvp_site/docs/`, docs/artifacts (`PROMPTS_README.md`, `coverage_report.txt`,
`monitor_doc_sizes.sh`), and excluding everything outside `mvp_site/` (`scripts/`,
`tests/`, `testing_*/`, docs, roadmap, tooling, automation, prototypes). Non-headline
numbers are in the Appendix only and are NOT part of the headline total.

## Method

1. **Whole-file DELETEs**: every file whose file-level verdict is DELETE. Line count is
   exact `wc -l` from the local tree.
2. **In-file DELETE symbols**: for every DELETE row inside a file that is NOT wholly
   deleted, the symbol's span from the local file. Python spans come from the AST
   (def/class start line — decorator-inclusive on Python 3.8+ — through `end_lineno`),
   merged per file so nested defs and methods inside a deleted class count once.
   Grouped rows naming several symbols sum each symbol's span. Bare names with several
   defs count only when the DELETE rows naming that name number at least the def count.
3. **Partial deletes**: only the deleted symbols' spans are counted, never kept helpers
   (e.g. `entity_validator` except its two "Unknown"-sentinel helpers;
   `campaign_divine` except its pure tier reader).
4. **Exclusions**: ADAPT rows, MIXED rows, KEEP rows, conditional DELETE rows, and
   test-only rework are NOT counted. Docs-configs has zero verdicts and contributes
   nothing.
5. **Proven-unused rule**: DELETE verdicts already encode the audit's proven-unused test
   (zero production callers, not an entry point, not a test target, no registered
   exception). Only DELETE verdicts were counted; no new deletion candidates were added.
6. All 396 mapped in-file symbols resolved to Python AST spans. No JS/CSS in-file span
   was required: every frontend JS/CSS DELETE was a whole file.

## (a) Headline whole-file DELETEs

| File | Lines (`wc -l`) |
|---|---|
| `mvp_site/entity_preloader.py` | 25 |
| `mvp_site/entity_tracking.py` | 68 |
| `mvp_site/entity_utils.py` | 12 |
| `mvp_site/faction/combat.py` | 309 |
| `mvp_site/faction/rankings.py` | 404 |
| `mvp_site/frontend_preview_release.py` | 165 |
| `mvp_site/frontend_v1/js/component-enhancer.js` | 617 |
| `mvp_site/frontend_v1/js/visual-validator.js` | 423 |
| `mvp_site/frontend_v1/parallel_dual_pass.css` | 75 |
| `mvp_site/frontend_v1/parallel_dual_pass.js` | 219 |
| `mvp_site/intent_classifier.py` | 1885 |
| `mvp_site/intent_classifier_warmup.py` | 182 |
| `mvp_site/llm_providers/minimax_provider.py` | 256 |
| `mvp_site/mcp_memory_real.py` | 194 |
| `mvp_site/memory_integration.py` | 341 |
| `mvp_site/memory_mcp_real.py` | 79 |
| `mvp_site/narrative_sync_validator.py` | 147 |
| `mvp_site/portrait_model_compare.py` | 194 |
| `mvp_site/schemas/defensive_numeric_converter.py` | 163 |
| **Subtotal, 19 files** | **5,758** |

Notes:

- `mvp_site/intent_classifier.py` (1,885) + `intent_classifier_warmup.py` (182) =
  2,067 lines, from the run-1 pilot (both files DELETE in full, no method kept). The
  pilot's own file states 1,886 / 183; the local tree counts 1,885 / 182 by `wc -l`
  (both files end with a trailing newline, so this is a 1-line-per-file version drift
  between the pilot's checkout and this ZIP, not a counting-method difference).
- Two headline files are tool-like but sit inside `mvp_site/` and are not test files,
  so they are counted under the stated scope rule: `frontend_preview_release.py` (165)
  and `portrait_model_compare.py` (194), 359 lines combined. Excluding them would lower
  the headline whole-file subtotal to 5,399 and the grand total to 16,485.
- Two files under `mvp_site/frontend_v1/` are in the Appendix, not the headline, because
  they are test files despite living in the shipped-UI tree: `test_planning_block_parsing.js`
  (638) and `mocks/mock_header_avatar_and_scroll_gate.html` (359), 997 lines combined.

## (b) Headline in-file DELETE symbol spans

Per-group in-file spans (all-scope vs headline; only the scripts group differs, because
all of its in-file spans are outside `mvp_site/` or in test infrastructure):

| Audit group | Symbols (all-scope) | Lines (all-scope) | Symbols (headline) | Lines (headline) |
|---|---|---|---|---|
| gateway | 42 | 1111 | 42 | 1111 |
| state | 167 | 5197 | 167 | 5197 |
| schema | 43 | 820 | 43 | 820 |
| dice | 7 | 209 | 7 | 209 |
| godmode | 24 | 1188 | 24 | 1188 |
| faction | 31 | 1003 | 31 | 1003 |
| providers | 18 | 200 | 18 | 200 |
| logging | 2 | 72 | 2 | 72 |
| scripts | 7 | 240 | 0 | 0 |
| frontend | 22 | 480 | 22 | 480 |
| agents | 33 | 806 | 33 | 806 |
| **Total** | **396** | **11,326** | **389** | **11,086** |

Headline in-file spans by file (merged spans per file; symbols = DELETE symbols mapped
in that file):

| File | Symbols | Lines |
|---|---|---|
| `mvp_site/action_resolution_utils.py` | 3 | 165 |
| `mvp_site/agent_prompts.py` | 2 | 53 |
| `mvp_site/agents.py` | 22 | 501 |
| `mvp_site/avatar_image_gen.py` | 2 | 80 |
| `mvp_site/bq_logging.py` | 2 | 72 |
| `mvp_site/campaign_divine.py` | 5 | 153 |
| `mvp_site/clock_skew_credentials.py` | 11 | 92 |
| `mvp_site/continuation_admission.py` | 1 | 19 |
| `mvp_site/criterion4_admission.py` | 1 | 2 |
| `mvp_site/dice.py` | 1 | 3 |
| `mvp_site/dice_integrity.py` | 1 | 2 |
| `mvp_site/dice_provably_fair.py` | 2 | 39 |
| `mvp_site/document_generator.py` | 9 | 212 |
| `mvp_site/entity_instructions.py` | 9 | 252 |
| `mvp_site/entity_validator.py` | 20 | 585 |
| `mvp_site/equipment_display.py` | 8 | 150 |
| `mvp_site/faction/battle_sim.py` | 6 | 217 |
| `mvp_site/faction/dual_mode.py` | 2 | 78 |
| `mvp_site/faction/intel.py` | 6 | 232 |
| `mvp_site/faction/srd_units.py` | 3 | 97 |
| `mvp_site/faction/tools.py` | 2 | 26 |
| `mvp_site/firestore_service.py` | 6 | 89 |
| `mvp_site/game_state.py` | 19 | 661 |
| `mvp_site/game_state_merge.py` | 51 | 1671 |
| `mvp_site/game_state_mixins.py` | 41 | 1604 |
| `mvp_site/god_mode_executor.py` | 1 | 18 |
| `mvp_site/graveyard_service.py` | 6 | 139 |
| `mvp_site/json_utils.py` | 1 | 17 |
| `mvp_site/living_world_contract.py` | 9 | 266 |
| `mvp_site/llm_parser.py` | 2 | 53 |
| `mvp_site/llm_providers/gemini_provider.py` | 9 | 93 |
| `mvp_site/llm_providers/provider_utils.py` | 1 | 50 |
| `mvp_site/llm_response.py` | 1 | 26 |
| `mvp_site/llm_service.py` | 9 | 583 |
| `mvp_site/location_util.py` | 3 | 141 |
| `mvp_site/main.py` | 7 | 83 |
| `mvp_site/mcp_client.py` | 1 | 21 |
| `mvp_site/memory_utils.py` | 9 | 154 |
| `mvp_site/narrative_response_schema.py` | 7 | 113 |
| `mvp_site/numeric_converters.py` | 1 | 27 |
| `mvp_site/numeric_field_converter.py` | 3 | 39 |
| `mvp_site/opening_story_merge.py` | 6 | 52 |
| `mvp_site/openrouter_auth.py` | 8 | 57 |
| `mvp_site/portrait_generator_agent.py` | 3 | 38 |
| `mvp_site/preventive_guards.py` | 6 | 202 |
| `mvp_site/rewards_engine.py` | 18 | 1017 |
| `mvp_site/schemas/entities_pydantic.py` | 14 | 69 |
| `mvp_site/session_header_utils.py` | 26 | 686 |
| `mvp_site/world_sim/timeline/validation.py` | 1 | 20 |
| `mvp_site/world_time.py` | 2 | 67 |
| **Subtotal, 50 files** | **389** | **11,086** |

Largest contributors: `game_state_merge.py` (1,671), `game_state_mixins.py` (1,604),
`rewards_engine.py` (1,017), `session_header_utils.py` (686), `game_state.py` (661),
`entity_validator.py` (585), `llm_service.py` (583), `agents.py` (501).

## (c) Uncounted / uncertain items (NOT in the total)

### C1. DELETE symbols with no countable code span — 9 symbols

Registry-key entries in `mvp_site/backend_adjustment_specs.py` (godmode group). These are
spec-path keys in a data registry, not function/class definitions, so no AST span exists
for them. Their lines are not counted; each entry is a few lines of registry data, so
resolving them would add only a small number of lines.

- `level_up_signal.format_to_ui_pair` (mvp_site/backend_adjustment_specs.py) — symbol not found in AST
- `level_up_core.enrich_missing_xp_evidence` (mvp_site/backend_adjustment_specs.py) — symbol not found in AST
- `level_up_rewards.synthesize_primary_rewards_box` (mvp_site/backend_adjustment_specs.py) — symbol not found in AST
- `rewards_box.progress_percent_xp_anchor` (mvp_site/backend_adjustment_specs.py) — symbol not found in AST
- `location.legacy_location_fallback_in_resolve_location` (mvp_site/backend_adjustment_specs.py) — symbol not found in AST
- `location.session_header_fallback_generation` (mvp_site/backend_adjustment_specs.py) — symbol not found in AST
- `world_time.partial_merge_date_protection` (mvp_site/backend_adjustment_specs.py) — symbol not found in AST
- `session_header.timestamp_canonical_repair` (mvp_site/backend_adjustment_specs.py) — symbol not found in AST
- `rewards_box.progress_percent_xp_curve_fallback` (mvp_site/backend_adjustment_specs.py) — symbol not found in AST

### C2. Conditional DELETE rows — 9 rows, 83 symbols (spans excluded)

These rows carry a DELETE verdict limited to a context (turn path only, per-turn only,
value-reconciliation only, etc.) while preserving a surviving part or an ADAPT
migration. Because the surviving part's lines cannot be separated from the deleted
part's lines without reading each body, none of their spans are counted. This is the
largest excluded bucket: the two `firestore_service.py` clusters alone name 61 symbols.

- **state / `game_state.py`** — 2 symbols: `_canonicalize_player_gold_in_place`, `_canonicalize_player_gold_state_update_in_place`
- **state / `game_state.py`** — 1 symbols: `_normalize_legacy_ability_scores_to_attributes_in_place`
- **state / `game_state.py`** — 9 symbols: `is_meaningful_parentage`, `_is_valid_parentage_value`, `_is_missing_parentage_value`, `_reconcile_parentage_aliases_in_place`, `_restore_parentage_alias_from_extras_in_place`, `_restore_parentage_from_extras_in_place`, `_canonicalize_parentage_in_place`, `_PLAYER_CHARACTER_SCHEMA_KEYS`, `_PARENTAGE_ALIASES`
- **state / `game_state.py`** — 4 symbols: `_canonicalize_resource_registry_in_place`, `reset_resource_registry_in_place`, `VALID_RESOURCE_RESET_TRIGGERS`, `VALID_RESOURCE_CATEGORIES`
- **state / `game_state.py`** — 3 symbols: `GameState.validate_and_correct_state`, `GameState.migrate_legacy_state_for_schema`, `GameState._validate_post_migration_schema_invariants`
- **state / `game_state_merge.py`** — 2 symbols: `_apply_rest_resource_reset`, `apply_long_rest_to_resources`
- **state / `game_state_mixins.py`** — 1 symbols: `CharacterStateMixin.get_character_identity_block`
- **state / `firestore_service.py`** — 20 symbols: `_world_event_ids`, `_projected_world_event_ids`, `_merge_model_mapping`, `_same_world_event_value`, `_merge_world_event_values`, `_merge_timeline_living_world_fields`, `_filter_story_world_events`, `_fence_model_projected_world_events`, `_claim_world_event_story_projection`, `_preserve_projected_event_flags`, `_projection_nodes`, `_mapping_has_world_event_projection`, `_request_has_world_event_projection`, `_strip_world_event_projection`, `_restore_live_projection_fields`, `_resolve_producer_control_basis`, `_basis_suppresses_projection`, `_read_boundary_control_record`, `_apply_producer_control_fence`, `_prepare_timeline_projection_request`
- **state / `firestore_service.py`** — 41 symbols: `_merge_concurrent_level_up_session`, `_merge_live_level_up_session`, `_merge_baseline`, `_rebase_audit_arm_in_txn`, `_apply_audit_operation_in_txn`, `_pending_identity`, `_pending_record_for`, `_merge_pending_record`, `_merge_rewards_pending`, `_merge_turn_state`, `_merge_pending_rewards_into_state`, `_resolve_audit_arm_from_live_state`, `_persist_turn_atomic_audit_transactional`, `_lookup_turn_receipt_before_write`, `_persistence_baseline_kwarg`, `_compute_pcd_delta`, `_apply_concurrent_state_delta`, `_apply_concurrent_pcd_diff`, `_merge_concurrent_pcd`, `_omit_unchanged_experience_projections`, `_authored_xp_change`, `_keep_authored_xp`, `_is_sane_reconciliation_xp_value`, `_merge_live_into_reward_candidate`, `_reconcile_reward_event_xp_transactional`, `_reproject_reward_display_after_reconciliation`, `_reward_claim_halves_on_conflict`, `_collision_claim_amendment`, `_carry_forward_winner_state`, `_restore_withheld_xp_half`, `_restore_withheld_tangible_half`, `_strip_reward_views`, `_payloads_without_reward_views`, `_reconcile_reward_collision_state`, `_refresh_reward_views`, `_build_reconciled_reward_turn_plan`, `_persist_turn_atomic_reward_transactional`, `_reproject_scene_heading`, `_is_same_concurrent_grant`, `_audit_supersedes`, `_int_or_none`

One row in this set groups a DELETE symbol with two ADAPT migration symbols
(`GameState.validate_and_correct_state` is the DELETE part;
`migrate_legacy_state_for_schema` and post-migration invariant checks are ADAPT), which
is why the row is conditional rather than plain DELETE.

### C3. Branch-level deletions named inside KEEP rows — 3 rows (no lines claimed)

- **state / `graveyard_service.py`**: | `apply_character_death_signals` | `world_logic.py`, `game_state_merge.py`, `game_state_mixins.py`, `backend_adjustment_specs.py` | Pass A: applying declared d
- **state / `game_state.py`**: | `PendingRewardsState` (class) + `to_dict`, `read_pending_xp_gained`, `pending_reward_records`, `is_open_pending_reward`, `normalize_pending_rewards`, `resolve
- **state / `game_state.py`**: | `_validate_monotonic_counters` | Internal (validation) | Pass A: checking that counters never go backwards is a storage-integrity invariant the baseline needs

These rows say certain branches delete while the enclosing function KEEPs. Branch spans
were not computed; no lines are claimed for them.

### C4. Counting-basis notes (not additional uncounted lines)

- **Schema group, stated 50 vs row-expanded 57.** The schema file's verdict-counts note
  states DELETE 50 units, but expanding its grouped rows to named symbols gives 57
  DELETE symbols (43 mapped in-file + 14 covered by the two whole-file deletions
  `narrative_sync_validator.py` and `defensive_numeric_converter.py`). The file itself
  says "if a count disagrees with a row, the row governs"; LOC counting uses per-symbol
  spans, so 57 is the correct basis here. The 7-unit difference is a grouping convention
  (grouped converter rows expanded to named methods), not missing symbols.
- **Providers group, 36 = 18 + 18.** The 36 stated DELETE symbols reconcile exactly:
  18 symbols mapped in-file plus 18 `minimax_provider.py` section rows whose lines are
  covered by that file's whole-file count (256), not double-counted.
- **`prompts/AGENTS.md` (plus 2 symlinks): NOT counted.** Its verdict is
  DELETE-from-runtime-claim but KEEP as repo documentation, so it is not a removal.
- **Frontend LEGACY_* symbols: NOT counted.** Their verdict is KEEP while legacy URLs
  are still served, then DELETE — a future conditional, excluded.
- **Test-only rework: NOT counted.** Tests referencing deleted symbols
  (e.g. `test_intent_classifier.py`, `test_portrait_generator_agent.py` importing
  `assemble_campaign_portrait_context`) need updating alongside any deletion, but test
  edits are not removed production code.

## (d) Grand total with caveats

**Headline total: 16,844 lines of mvp_site production code would be removed**
(5,758 exact whole-file lines + 11,086 AST-span in-file lines).

Caveats:

- Exact for whole files; span-derived for in-file symbols (decorator-inclusive spans,
  overlaps merged per file, interior blanks/comments included, trailing blanks excluded).
- Excludes ADAPT rewrites, MIXED rows, conditional DELETE rows (§C2, 83 symbols),
  branch-level deletions (§C3), the 9 registry entries (§C1), and all test-only rework.
  Resolving §C1–§C3 would raise the total; the conditional clusters in §C2 are the
  material unknown (61 symbols in the two `firestore_service.py` clusters alone).
- Deletions still happen only by PR with Jeffrey's go-ahead; this report counts verdicts,
  it does not execute them. Two §6 conflicts need owner eyes before PRs act on those
  rows (faction/antagonist cooldown stripping has no registered exception; provider-utils
  faction patching is synchronous where §6(3) requires async ticks).

## Appendix — all-scope numbers (NOT part of the headline)

| Component | Files | Lines |
|---|---|---|
| Whole-file DELETEs, all scopes | 118 | 32,624 |
| In-file DELETE symbol spans, all scopes | 54 files, 396 symbols | 11,326 |
| **All-scope total** | | **43,950** |
| of which headline (mvp_site prod) | | 16,844 |
| of which appendix-only | | 27,106 |

Appendix whole-file DELETEs (99 files, 26,866 lines) — scripts/ (90 files, 23,571 lines),
repo-root scripts (2 files, 326 lines), mvp_site docs/dev artifacts (5 files, 1,972
lines), and frontend_v1 test/mock files (2 files, 997 lines):

| File | Lines (`wc -l`) |
|---|---|
| `Genesis.sh` | 325 |
| `codebase_loc.sh` | 1 |
| `mvp_site/PROMPTS_README.md` | 255 |
| `mvp_site/coverage_report.txt` | 229 |
| `mvp_site/docs/zfc_audit/FULL_AUDIT.md` | 1301 |
| `mvp_site/docs/zfc_audit/SUMMARY.md` | 141 |
| `mvp_site/frontend_v1/js/test_planning_block_parsing.js` | 638 |
| `mvp_site/frontend_v1/mocks/mock_header_avatar_and_scroll_gate.html` | 359 |
| `mvp_site/monitor_doc_sizes.sh` | 46 |
| `scripts/ablate_code_execution_schema.py` | 268 |
| `scripts/aggressive_test_reducer.py` | 397 |
| `scripts/analyze_coverage_impact.py` | 132 |
| `scripts/archive_openrouter_release_receipt.py` | 46 |
| `scripts/backfill_alexiel_core_memories.py` | 683 |
| `scripts/backfill_spell_slots_shape.py` | 225 |
| `scripts/bq_migrate_add_revision_id.py` | 215 |
| `scripts/bq_migrate_ttl.py` | 115 |
| `scripts/build_srd_class_corpus.py` | 203 |
| `scripts/campaign_analyzer.py` | 376 |
| `scripts/campaign_selector_0.4.py` | 375 |
| `scripts/campaign_selector_mock.py` | 272 |
| `scripts/campaign_selector_real.py` | 276 |
| `scripts/capture_collapsed_choices_evidence.py` | 38 |
| `scripts/capture_ip_wizard_screenshot.py` | 131 |
| `scripts/capture_ip_wizard_video_evidence.py` | 340 |
| `scripts/capture_quick_hide_evidence.py` | 395 |
| `scripts/capture_scene_provider_rejection_backend.py` | 523 |
| `scripts/capture_share_video_evidence.py` | 2078 |
| `scripts/ci_cache_busting.sh` | 16 |
| `scripts/cleanup_debug_info.py` | 205 |
| `scripts/cleanup_failing_tests.py` | 207 |
| `scripts/cleanup_stale_lua_flags.py` | 219 |
| `scripts/collect_real_gemini_before_after.py` | 307 |
| `scripts/compare_productivity.py` | 325 |
| `scripts/complete_email_setup.sh` | 31 |
| `scripts/dead_code_eliminator.py` | 321 |
| `scripts/debug_rate_limit_live.py` | 101 |
| `scripts/debug_state_updates_issue.py` | 164 |
| `scripts/delete_all_my_epic_adventure.sh` | 69 |
| `scripts/dependency_analyzer.py` | 669 |
| `scripts/deploy_context_optimization.py` | 468 |
| `scripts/detect_inline_imports.py` | 560 |
| `scripts/download_personalities.py` | 114 |
| `scripts/elimination_safety_checker.py` | 172 |
| `scripts/es_campaign_duplicate_batch.py` | 191 |
| `scripts/evidence_openrouter_nonstreaming_bq_path10.py` | 190 |
| `scripts/fetch_pr_data.py` | 62 |
| `scripts/fix_debug_mocks.py` | 62 |
| `scripts/fix_dice_notation_concat.py` | 754 |
| `scripts/fix_god_mode_directives.py` | 300 |
| `scripts/fix_llm_mocks.py` | 60 |
| `scripts/fix_mvp_imports.py` | 144 |
| `scripts/fix_mvp_site_imports.py` | 189 |
| `scripts/generate_models.py` | 24 |
| `scripts/grant_gcp_service_account_permissions.sh` | 104 |
| `scripts/import_optimizer.py` | 362 |
| `scripts/llm_mock.py` | 229 |
| `scripts/mcp_repro_full_bar_harness_rerun.sh` | 125 |
| `scripts/mcp_repro_full_bar_provenance_cast.sh` | 80 |
| `scripts/mcp_repro_full_bar_record_video.sh` | 100 |
| `scripts/mcp_repro_full_bar_run_all.sh` | 12 |
| `scripts/pr6734_strict_es_evidence.py` | 792 |
| `scripts/probe_8537_cap_raise_evidence.py` | 167 |
| `scripts/probe_gemini_thinking_levels.py` | 524 |
| `scripts/probe_memory_compaction_and_scrub.py` | 166 |
| `scripts/probe_memory_delta_branches.py` | 406 |
| `scripts/probe_schema_maxlength_enforcement.py` | 326 |
| `scripts/prompt_templates.py` | 178 |
| `scripts/publish_quickhide_gist.py` | 107 |
| `scripts/pytest_cache_optimizer.py` | 206 |
| `scripts/recheck_field_inventory.py` | 256 |
| `scripts/repro_streaming_contract_preview_auth.sh` | 130 |
| `scripts/run_campaign_selector.sh` | 27 |
| `scripts/run_level_up_class_repro_suite.sh` | 4 |
| `scripts/run_pr_3491_parallel_tests.py` | 271 |
| `scripts/run_web_advice_ip_wizard.py` | 259 |
| `scripts/scene_illustration_design_examples.py` | 651 |
| `scripts/scrub_class_4_residue.py` | 97 |
| `scripts/simple_inline_detector.py` | 279 |
| `scripts/smart_mock_generator.py` | 168 |
| `scripts/test_ai_universe_api_keys.sh` | 425 |
| `scripts/test_broken_logic_demo.sh` | 51 |
| `scripts/test_coverage_analyzer.py` | 256 |
| `scripts/test_dependency_analyzer.py` | 675 |
| `scripts/test_firebase_read_write.py` | 237 |
| `scripts/test_firebase_with_data.py` | 197 |
| `scripts/test_importance_ranker.py` | 346 |
| `scripts/test_inline_detector.py` | 66 |
| `scripts/test_json_bugs_simple.py` | 121 |
| `scripts/test_monitoring_dashboard.py` | 211 |
| `scripts/test_multiple_ip_campaigns.py` | 162 |
| `scripts/test_optimization_suite.py` | 435 |
| `scripts/test_scenarios.py` | 331 |
| `scripts/test_test_dependency_analyzer.py` | 171 |
| `scripts/test_utils.py` | 22 |
| `scripts/validate_aggressive_optimization.py` | 106 |
| `scripts/validate_firebase_auth.py` | 357 |
| `scripts/validation_only_approach.py` | 339 |
| `scripts/verify_exemption.py` | 25 |
| **Subtotal, 99 files** | **26,866** |

Appendix in-file DELETE spans (4 files, 7 symbols, 240 lines):

| File | Symbols | Lines |
|---|---|---|
| `capture_mocks.py` | 2 | 55 |
| `mvp_site/mocks/mock_llm_service.py` | 2 | 37 |
| `test_mobile_campaigns.py` | 1 | 68 |
| `test_mobile_server.py` | 2 | 80 |
| **Subtotal, 4 files** | **7** | **240** |

Per-group reconciliation (DELETE rows found by the parser vs each group's stated totals):
gateway 38/38; state 91 plain + 9 conditional = 100/100; schema 47 rows / 57 symbols
vs stated 50 units (rows govern, see §C4); dice 7/7; godmode 28 rows / 33 symbols
(24 mapped + 9 registry keys, §C1); faction 46/46; providers 36/36 (18 mapped + 18
minimax section rows); logging 3 (1 symbol row + 2 whole files); scripts 80 stated
(6 symbol rows + §2/§6/§7 file rows expanding to 90 files); frontend 16 rows + 8
Phase-1 whole files; agents 13 rows + 1 globals split row = 14; intent pilot 52 symbol
rows + 2 whole files. Zero parser-missing whole files; zero unresolved file references
after group-aware resolution.
