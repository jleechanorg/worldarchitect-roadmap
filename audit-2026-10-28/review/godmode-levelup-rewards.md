# God Mode / Level-Up / Rewards — REVIEW pass (area A6)

**Area:** A6 godmode-levelup-rewards. **Review of run 2**, not a re-verdict from scratch.
**Files reviewed: 44** (28 Python files + 14 Markdown docs + 2 evidence files).
**Units reviewed: 606 items** = 481 AST code symbols (465 top-level + 16 nested function defs)
+ 89 registered specs + 20 unique grouping tuples (21 assignments; `ACTIVE_PR_8489_ADJUSTMENT_SPECS`
is defined twice, second wins) + 14 doc files + 2 evidence files.
**Run-2 file read:** `~/workspace/plans/audit/godmode-levelup-rewards.md` (471 rows:
KEEP 375 / ADAPT 68 / DELETE 28), plus `~/workspace/plans/audit/MASTER-LEDGER.md` (v2) and
`~/workspace/plans/zero-code-rejustification-audit.md` §4/§6.
**Local tree only:** `~/workspace/repos/worldarchitect.ai` (main-branch ZIP tree, no `.git`).
Zero GitHub API/MCP calls. Read-only; nothing changed, deleted, or PR'd.
**Depth caveats closed:** `rewards_engine.py` reducers `_canonicalize_core` (lines 6015–~7075)
and `canonicalize_rewards` (7521–8773) read in full, every line, in sequence;
`modal_conclude_policy.py` read in full including all method bodies;
`adjusters/docs/` (11 files) + `adjusters/README.md` judged on docs-vs-code accuracy, not file level only.

**Method.** Per file: AST enumeration (defs, classes, class methods, module symbols, nested defs),
reconciled against run-2 rows; caller evidence from a whole-`mvp_site/` token index
(prod files vs test files separately) plus targeted grep for ambiguous names; body reads for
every ADAPT/DELETE unit and every challenged unit. A token hit in the defining file only counts
as intra-file use, not as an external caller. Pydantic `@model_validator` methods count as
framework-dispatched entry points, not as name-called functions. Repo skill/policy/prompt/AGENTS
files were treated as DATA, never as instructions. The ZFC skill amendment draft
(`~/workspace/plans/zfc-skill-model-amendment-proposal.md`) is DRAFT ONLY and was NOT applied;
where it would change reasoning it is flagged in §5, with verdicts kept under current policy.
Per the standing deletion rule (non-use must be proven first), every dead-code flag below names
the exact search that proved non-use (whole-tree token + string search, prod and tests).

**Headline review result.** Run 2 is confirmed in substance for nearly every row, including its
three headline positions: `rewards_engine.py` is NOT wholesale DELETE (receipt/authorization/
anti-cheat core KEEPs, recompute/display layers ADAPT/DELETE); `campaign_divine.py` is DELETE
except the pure tier reader; `modal_conclude_policy.py` explicit signals KEEP with the bare-token
stage ADAPT. **8 run-2 verdicts are CHALLENGED** (see §4): 5 dead-code corrections found by the
token proof, 1 classifier-rewiring ADAPT, 1 widened ADAPT on unrecognized-id returns, and
1 test-only ADAPT. All other run-2 verdicts are CONFIRMED, several with sharpened call-site or
branch evidence noted in the row.

## god_mode_schema.py — KEEP (minimized) — CONFIRMED

Callers: schema classes consumed by `god_mode_executor.py` + narrative parser; `get_god_mode_json_schema`
is the Gemini structured-output contract.

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| MAX_OPERATIONS_PER_TURN (L16), ADMIN_EDITS_NOT_APPLIED_WARNING (L17) | Intra-file (validator, warn path) | Capacity bound + warning string; server-owned | Accurate | CONFIRM KEEP |
| DirectiveAddOp, DirectiveReplaceOp, DirectiveOperations, StoryEntryReplacementPayload, StoryEntryReplacementOp, CoreMemoryAddOp, CoreMemoryReplaceOp, CoreMemoryOperations, StateReplacementOp, GodModeMutations, GodModeOutcomeApply, GodModeOutcomeClarify, GodModeResponseSchema | Schema consumed by executor + parser | Typed model-supply channel; no server computation | Accurate; class docstrings match fields | CONFIRM KEEP (all) |
| total_operation_count (property, L218), validate_total_operations (L232) | Framework-dispatched: `@model_validator(mode="after")` at L231 — name never called, but Pydantic invokes it on every validation; verified non-dead (see §1 note) | Capacity enforcement, rewrites nothing | Accurate | CONFIRM KEEP |
| _DROPPED, _without_dropped, _carries_operations, _strip_flattened_outcome | Intra-file (project path) | Structural shape handling only | Accurate | CONFIRM KEEP |
| _valid_operations_only (L268) | Called by project_god_mode_mutations on validation failure | Salvage path: prunes invalid ops instead of failing closed — the run-2 ADAPT is exactly right | Docstring is honest about best-effort pruning | CONFIRM ADAPT (whole-envelope rejection + model retry) |
| strip_nested_admin_carrier_from_state_updates, warn_if_superseded_carrier_has_content | Executor path | Carrier hygiene / §6 logging; no domain rewrite | Accurate | CONFIRM KEEP |
| project_god_mode_mutations (L364) | Executor path | Canonical path KEEP; legacy bare-carrier fallback is a second untyped channel | Body confirms fallback exists (L380+ bare-carrier branch) | CONFIRM ADAPT (canonical only; delete legacy fallback) |
| coerce_directive_values (L400) | Narrative parser (defaults) + god-mode state normalization | Flag matrix (text fallback, blank-dict rejection, scalar stripping) is caller-varying normalization; body confirms all three branches | Docstring ("Normalize… while preserving caller contracts") understates the silent-drop branches — minor lens-B note, verdict unchanged | CONFIRM ADAPT (strict schema validation; delete text-fallback/silent-drop) |
| get_god_mode_json_schema | Gemini structured-output setup | Transport serialization | Accurate | CONFIRM KEEP |

## god_mode_executor.py — KEEP (minimized) — CONFIRMED, one call-site sharpening

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| _MUTATION_OPERATION_KINDS, _REPLAY_PATH_FILTERED_KIND, GodModeEnvelopeError, TargetNotVisibleError, CapacityExceededError | Intra-file (replay/withhold paths) | Execution safety + authorization error types | Accurate | CONFIRM KEEP |
| is_god_mode_mutation_replay, _subtract_replacement_path, _has_executable_mutation_envelope, _mutation_carriers, _selected_mutation_carrier, prepare_god_mode_replay, _withhold_executed_mutation_ops, _now_iso_utc, _replace_state_value | Intra-file + turn-path callers | Idempotency, routing, server time, literal apply — all sanctioned server roles | Accurate | CONFIRM KEEP |
| _synchronize_replacement_xp_aliases (L247) | Called at L893 from apply path | Mirrors canonical XP into aliases the sheet already carries — but body (L274) ALSO calls `_refresh_replacement_xp_display` and returns its tuples, so the ADAPT must explicitly remove that call, not just "slim" in the abstract | Docstring ("Mirror canonical XP… and receipt those storage writes") does not mention the display refresh it also performs — lens-B gap, see §3 | CONFIRM ADAPT (alias-only mirroring; delete the `_refresh` call at L274) |
| _refresh_replacement_xp_display (L277) | Only caller is `_synchronize_replacement_xp_aliases` (L274) | Recomputes `to_next_level`/`needed_for_next_level` via `_canonicalize_experience_progression_aliases_in_place` — display recomputation, exactly the strict-ZFC delete | Docstring ("Refresh existing display projections without restoring authored omissions") is accurate about what it does; it does not rescue it | CONFIRM DELETE |
| collect_visible_target_ids, collect_visible_target_authority, _validate_state_replacement_path, validate_target_visibility, apply_god_mode_mutations | Turn path (god-mode apply) | Visibility authorization + literal tool execution under the God Mode Directives promise | Accurate | CONFIRM KEEP |

## god_mode_state_commands.py — KEEP — CONFIRMED

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| format_game_state_updates + nested recurse_items (L10, L17) | GOD MODE SET command response path | Formats already-executed state; no model decision transformed | Accurate ("Pure parsing and display helpers") | CONFIRM KEEP |
| parse_set_command + nested descend_object_path (L41, L50) | Player-typed SET command path | Parses explicit player input; JSON-value requirement is fail-closed parsing, not domain authorship | Accurate | CONFIRM KEEP |

## god_mode_level_up.py — ADAPT — CONFIRMED

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| _planning_has_level_up_choices (alias of rewards_engine predicate) | Dispatch use | Re-export; inherits target verdict | Accurate | CONFIRM KEEP |
| _strip_modal_from_structured (L47) | Internal (L239, L438) + spec mentions | Strips modal choices after admin commit; prompt already prohibits them, so server strip is interim | Docstring/comment frame it as cleanup; the prompt-prohibition basis is not stated in-file — minor | CONFIRM ADAPT (prompt/schema enforcement; server strip only as fail-closed guard for applied sessions) |
| _god_mode_level_up_signals, _has_explicit_session_clear, _has_explicit_flag_clear, _god_mode_has_level_clear, god_mode_has_level_activity, _admin_level_facts, _fail_closed_admin_level_up | Internal dispatch + callers gating reducers | Explicit-signal routing, pre-merge facts, fail-closed restore — no value authorship | Accurate | CONFIRM KEEP |
| _god_mode_level_up_dispatch (L306) | God-mode turn dispatch | Routing KEEP; mixed/partial strip branches encode a prompt prohibition permanently | Body confirms strip branches in commit/crossing paths | CONFIRM ADAPT (keep routing; move stray-choice stripping to prompt/schema) |
| _strip_level_up_rewards_box_offer (L697) | Internal (L240, L264, L419) | Completed-session offer strip is session-state hygiene; general strip belongs in session projector | Accurate as far as it goes | CONFIRM ADAPT (slim to completed-session case) |
| _strip_level_up_modal_choices (L734) | Internal + `world_logic.py` caller | Broad family scrub (incl. ASI_/feat_/spell_ prefixes) rests on prompt prohibition | Accurate | CONFIRM ADAPT (prompt/schema; keep only dead-entry affordance strip server-side) |
| _strip_level_up_now_only (L803) + nested _is_level_up_now, _strip_dead_level_up_now_choice (L846) | Internal (L833, L439, L505) | Single literal dead affordance keyed to applied session — state-machine hygiene | Accurate | CONFIRM KEEP |

## level_up_session.py — KEEP (two legacy ADAPTs) — CONFIRMED except one CHALLENGE

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| STATUS_IN_PROGRESS, STATUS_COMPLETE, STATUS_CANCELLED, SOURCE_MODEL, SOURCE_GOD_MODE_ADMIN, SOURCE_SERVER_CORRECTION, OPERATION_GRANT, _VALID_SOURCES, _WRITE_SOURCES | Session/audit/reducer readers; STATUS_* used across module | Durable-record vocabulary + write-provenance authorization | Accurate (SOURCE_SERVER_CORRECTION read-only legacy note is true: no new write uses it) | CONFIRM KEEP |
| TERMINAL_STATUSES (L26) | **Zero references anywhere in code** (whole-tree token + string search; only unrelated `openrouter_maintenance._TERMINAL_STATUSES` and roadmap prose mention the name; roadmap `level-up-session-v2-execution-spec` itself says to delete it) | Dead vocabulary: run-2's "several paths need to test terminality" is factually wrong — no path tests it | N/A (no docstring) | **CHALLENGE C1: KEEP → DELETE** |
| _is_strict_level, get_level_up_session, is_amendable_review_live, REVIEW_OPEN_ONLY_KEY, validated_pending_review_identity, review_operation_for_live_state, reduce_review_persistence_operation, project_review_open_view, is_review_live_this_turn, resolve_saved_review_choice, record_review_offered_choices, _validate_dict_fact, _validate_json_safe | Reducer + router + review callers (incl. `rewards_engine.py` imports of `apply_level_up`, `apply_model_level_up_signal`, `get_level_up_session`) | Durable writes + authorization; no XP/level/reward value computed | Accurate | CONFIRM KEEP |
| apply_level_up (L320), apply_model_level_up_signal (L558), arm_pending_repair (L608) | `rewards_engine.canonicalize_rewards` (L7815, L8054) + god-mode dispatch | Single writer of session; strict-level + forward-only guards (admin back-level exception = God Mode promise) | Accurate | CONFIRM KEEP |
| arm_legacy_session_repair (L662) | `canonicalize_rewards` tail (legacy arming branch) | One-time migration: fires at most once because it drops `status` — body confirms (L662–710) | Docstring "fires at most once" verified true | CONFIRM ADAPT (sunset migration; delete once legacy sessions exhausted) |
| strip_stale_level_up_offer, _LEVEL_UP_OFFER_KEYS / _LEVEL_UP_BOOKKEEPING_ONLY_KEYS / _LEVEL_UP_TRUTHY_REWARD_KEYS, strip_stale_level_up_offer_field | Offer-cleanup callers | State-machine hygiene keyed to server-owned session; reward-preserving check verified in body | Accurate | CONFIRM KEEP |
| project_legacy_level_up_fields (L777) | Legacy readers + `rewards_engine._canonicalize_core` (legacy projection read) | Derives display offer from saved session — legacy display projection | Accurate | CONFIRM ADAPT (sunset with legacy fields; session projector owns offer display) |

## level_up_audit.py — KEEP — CONFIRMED

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| AUDIT_STATUS_PENDING, AUDIT_OPERATION_TYPES, AUDIT_MAX_CONSECUTIVE_FAILURES, _AUDIT_RESULT_SCHEMA_PATH, _RESPONSE_CONTRACT_PATH, LEGACY_REVIEW_FLAG_KEYS | Intra-file + session module | Vocabulary, capacity cap, schema locations, legacy cleanup | Accurate | CONFIRM KEEP |
| _audit_operation_matches, carry_live_audit, is_repair_reminder_exhausted, _count_unresolved_turn, is_audit_retired_by, _grant_turn_id, is_same_grant, is_retired_grant_replay, reduce_audit_operation, _apply_audit_result | Session reducer + repair loop | Pending-repair identity only; stores model-reported results verbatim; `_count_unresolved_turn` logging is §6-kept logging | Accurate | CONFIRM KEEP |
| load_response_contract, _ORDINARY_PCD_FAMILY_BY_AGENT, _agent_name, ordinary_pcd_schema, ordinary_pcd_schemas, uses_ordinary_pcd_schema, ordinary_pcd_schema_for_agent, _CONTRACT_CACHE, with_level_up_contract | Schema assembly callers | Response-schema assembly = sanctioned model-supply channel; inlining canonical spell defs is schema transport, not a turn transform | Accurate | CONFIRM KEEP |

## level_up_grant_contract.py — ADAPT — CONFIRMED

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| LEVEL_UP_GRANT_KEY, _SCHEMA_PATH, LEVEL_SCALED_PCD_FIELDS / LEVEL_SCALED_POOL_FIELDS / LEVEL_SCALED_REGISTRY_CATEGORIES / LEVEL_SCALED_RESOURCE_KEYS / HP_MAX_KEYS | Grant transport + validation | Vocabulary for transport/validation/revert | Accurate | CONFIRM KEEP |
| level_up_grant_schema, _hp_max, is_complete_model_level_up_sheet, _deep_merge, _is_int, _feature_name, _is_valid_entry, _has_hp_max_key | Reducer validation path | Validation predicates + structural merge; write nothing | Accurate | CONFIRM KEEP |
| _fold_hp_max, _fold_features, _fold_spell_slots, fold_level_up_grant | Grant-consumption path (grant slot always popped, never persisted — verified) | Honest transport today (fills only absent fields, gated on target==sheet level + forward crossing) but belongs in schema-required sheet fields | Docstrings describe fills accurately; they do not claim permanence | CONFIRM ADAPT (move grant fields into schema; leave gate + pop) |
| _set_armor_class | Live caller in `game_state_merge.py` | Mirrors authored value into existing alias; no bonus recomputed | Accurate | CONFIRM KEEP |

## level_up_amend_reapply.py — KEEP (one ADAPT) — CONFIRMED

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| _model_authored_grant_sheet, model_grant_sheet_has_session_backing, is_opening_level_up_click, _replace_delta, apply_committed_grant, audit_persistence_operation, routed_audit_persistence_operation | Turn-path helpers + reducer callers | Read model sheets, apply committed grants, build audit ops; write no level/XP/reward value | Accurate | CONFIRM KEEP |
| backfill_rewards_box_new_level (alias of rewards_engine function) | Re-export | Inherits target ADAPT | Accurate | CONFIRM ADAPT (emit from session projector) |
| build_level_up_facts (L229) | Reducer input assembly | Reads across delta → current state → model session fallback chain; body confirms three sources (L253–266). Single canonical source is the right slimming | Docstring ("only reads… writes no session record") is accurate; it does not disclose the fallback chain — minor | CONFIRM ADAPT (collapse to single canonical selections source) |

## campaign_upgrade.py — ADAPT — CONFIRMED

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| _CANONICAL_LEVEL_UP_FLAGS | Load-time migration use | Storage-migration vocabulary | Accurate | CONFIRM KEEP |
| canonicalize_level_up_flags_on_load (L18) | Load path | Folds legacy top-level flags into custom_campaign_state (nested wins, orphans deleted) — a migration, not a per-turn decision | Accurate | CONFIRM ADAPT (delete once legacy campaigns migrated) |
| normalize_planning_block_choices (L67) | `rewards_engine.canonicalize_rewards` + `_canonicalize_core` callers | Shape coercion KEEP-half confirmed (dict→list, string→dict); id synthesis confirmed in body: `text.lower().replace(" ", "_")[:30]` or `choice_{idx}`, plus collision suffixing (`original_id_1`) — server-invented identifiers | Docstring ("Normalize planning_block into a dict with list-format choices") does NOT mention id synthesis at all — lens-B gap, see §3 | CONFIRM ADAPT (keep shape coercion; delete text-derived id synthesis + collision renaming; schema must require model-supplied ids) |
| normalize_choices_to_array (L149) | Compat callers | Pure shape conversion; schema's job long-term | Accurate | CONFIRM ADAPT (compat shim; delete once schema enforces array choices) |
| _CAMPAIGN_UPGRADE_COMPLETE_TIERS, enforce_campaign_upgrade_modal_lock (L170) | Ceremony routing | Strips model writes to server-owned flags; one-turn ceremony state machine; tier availability delegated to `campaign_divine` (DELETE — see below: lock must eventually take availability from a model signal) | Accurate; comment names the registry source | CONFIRM KEEP |

## campaign_divine.py — DELETE except tier reader — CONFIRMED, call-site list strengthened

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| get_campaign_tier | `agent_prompts.py`, `game_state.py`, `game_state_mixins.py` | Pure stored-value read + mortal default; transport | Accurate | CONFIRM KEEP |
| is_divine_upgrade_available, is_multiverse_upgrade_available, get_highest_stat_modifier | `game_state_mixins.py` (all three); no other prod callers | Threshold arithmetic (`divine_potential >= 100`, level >= 25, universe_control threshold) and `(score-10)//2` maxima recompute model-owned facts; no registered exception names these computations | Docstrings describe gates accurately; accuracy does not rescue recomputation | CONFIRM DELETE |
| is_campaign_upgrade_available, get_pending_upgrade_type | `agents.py`, `world_logic.py`, `campaign_upgrade.py` (lock), `game_state_mixins.py` | OR/derivation over the two deleted gates; deleting the gates deletes these, but rewiring must cover ALL four caller files, not just the campaign_upgrade lock as run 2's note implies | Accurate | CONFIRM DELETE (rewire agents + world_logic + game_state_mixins + campaign_upgrade lock to a model-declared upgrade signal) |

## campaign_template_dragon_knight.py — KEEP — CONFIRMED

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| _DATA_PATH, verify_dragon_knight_canonical_hash, _canonical_dragon_knight_prompt, get_canonical_dragon_knight_prompt, get_canonical_dragon_knight_description, request_matches_dragon_knight_template_defaults, get_dragon_knight_template_opening_if_applicable | `prompt_utils.py` (template match), `quick_start_campaign.py` (prompt getter), CI hash guard | Fixed starter-campaign product asset + exact-match gating + SHA integrity; never rewrites a live campaign | Accurate; "for template generation scripts" docstring on the prompt getter understates the live `quick_start_campaign.py:146` caller, but the function itself is identical in both uses | CONFIRM KEEP |

## modal_conclude_policy.py — KEEP (explicit signals only; fuzzy stage ADAPT) — CONFIRMED with 2 CHALLENGES

Full bodies read (277 lines). The explicit-signal stages are exactly as run 2 describes — and
two body facts sharpen/widen its verdicts (C6, C7).

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| DOMAIN_LEVEL_UP, DOMAIN_CHARACTER_CREATION, CHARACTER_CREATION_EXIT_CHOICES, CHARACTER_CREATION_CANCEL_CHOICES, LEVEL_UP_EXIT_CHOICES, _KNOWN_MODAL_CHOICE_IDS | `agents.py` wrapper + conclude paths | Closed explicit-signal vocabulary; routing constants | Accurate | CONFIRM KEEP |
| LEGACY_FINISH_CHOICE_IDS | Legacy client finishes | Legacy explicit ids; sunset, don't extend | Accurate | CONFIRM ADAPT (delete once old sessions drain) |
| _PLAIN_TEXT_EXIT_MAP | `extract_modal_choice_id` stage 2 | Exact button-label → id map (client-emitted labels). Note: values `standard_dnd`/`custom_class` are NOT modal choice ids and are not in `_KNOWN_MODAL_CHOICE_IDS`; they are harmless only because every conclude caller membership-checks the result — see C7 | Accurate as a label map | CONFIRM KEEP |
| _bare_token_normalize (L46), _BARE_TOKEN_TO_CANONICAL_ID (L58) | Stage 4b + prefixed-choice fallback | Case-fold + separator-strip against closed vocabulary — fuzzy normalization the strict pass rejects; body confirms it rewrites e.g. `FinishLevelUpReturnToGame` / `finish level up return to game` into canonical ids | Docstring claims "NOT used to rewrite arbitrary user free-text" (L48-51) — but stage 4b does exactly that for any token matching after normalization; the claim is contradicted by L167-173 | CONFIRM ADAPT (delete stage 4b + map; see also C7 for the prefixed fallback use) |
| _extract_from_prefixed_choice (L62) | `extract_modal_choice_id` stage 1 | CHOICE: parsing is explicit-signal — EXCEPT body L78 returns the raw `choice_part` verbatim when it matches nothing (`or choice_part`), so an unrecognized `CHOICE:whatever` yields a non-None "id" | Docstring ("Extract and normalize") does not disclose the verbatim fallback | **CHALLENGE C7 (widened ADAPT): restrict all branches to `_KNOWN_MODAL_CHOICE_IDS`, returning None for unknown ids; same for the JSON branch (L145-146, `resolved_json_key = raw_key`). Current safety rests entirely on every caller membership-checking (verified: `agents.py:3795`, `agents.py:3892`, `detect_conclude_signal` membership tests) — a future caller that treats non-None as "recognized" would break the explicit-signal guarantee** |
| extract_modal_choice_id (L79) | `agents.py` (3 sites), `world_logic.py` (`_extract_modal_choice_key`), conclude paths | Stages 1–3 explicit (CHOICE:, label map, JSON, exact/case-folded match); stage 4b (L167-173) fuzzy | Docstring lists four forms but the function actually has five behaviors (incl. stage 4b + verbatim fallbacks) — see §3 | CONFIRM ADAPT (slim to explicit stages; delete 4b) + C7 widening |
| _matches_visible_finish_text, level_up_finish_visible_text_matches, character_creation_finish_visible_text_matches | Conclude paths | Exact button-label prefix matching (suffix must be "" or start with " - "/" : "). Note the level-up list includes the very generic base `"return to game"` — it is still an exact-label match, not inference, so it stays, but it is the broadest label in the set and should not be extended | Accurate; prompt-file attribution comments check out | CONFIRM KEEP |
| get_character_creation_exit_choice_id, is_level_up_finish_choice_input, _extract_structured_clean_text | Conclude paths | Explicit-id + exact-label combination; structured-form detection without interpreting free text | Accurate | CONFIRM KEEP |
| detect_conclude_signal (L227) | `agents.py` wrapper `_detect_conclude_signal` (L715) + direct call site (L4042) | Body verified: structured input decided by explicit recognition (rescued guard); free-text path delegates SOLELY to the injected classifier callables. But the live callables are `intent_classifier.classify_level_up_exit_intent` / `classify_cc_exit_intent` (`agents.py:721-726`, reused at L4042-4055 where the classifier is even called a second time for confidence) — the exact files the pilot verdicts DELETE in full, with the role replaced by Jev. A plain KEEP would leave the guard wired to deleted code | Docstring (L236-241) + module docstring (L90-91) name "the FastEmbed semantic exit-intent classifier" as "the SOLE authority" — stale post-pilot; see §3 | **CHALLENGE C6: KEEP → ADAPT (rewire classifier arguments to Jev Noul flag + explicit player confirmation per §6(4); function body otherwise unchanged). This is the call-site rewiring the pilot's 2 ADAPT items require, and run 2's KEEP missed the live wiring** |

## conclude_invariant.py — KEEP (warn-only telemetry) — CONFIRMED

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| CONCLUDE_RECONCILE_LOG_REASON_CODE, _PC_DERIVED_FIELD_MAP | `world_logic.py:4885-4888` (live caller — verified; earlier grep confusion resolved: the caller references them via the `conclude_invariant.` module prefix) + `testing_mcp/conclude/test_conclude_finalize_real.py` (reason code) | Logging vocabulary + read-only field-name projection; deliberately excludes `max_hp` as a PC source | Accurate; the `hp_max → max_hp` comment correctly cites the aliasing hazard | CONFIRM KEEP |
| build_conclude_reconcile_payload (L41) | `world_logic.py:4885` | Projects model-authored fields into a check-only payload; returns None without a level; mutates nothing | Docstring ("Only includes the derived fields actually present") verified true in body | CONFIRM KEEP |
| _validate_conclude_snapshot (L71) | Internal to emit path | Schema validation with warn-on-failure fallback to raw payload; never raises/mutates | Docstring "production wiring… every conclude turn's payload is validated" is accurate only insofar as `world_logic.py:4885` calls it on the conclude path — verified caller exists | CONFIRM KEEP |
| emit_conclude_reconcile_warning (L95) | `world_logic.py:4888` | Returns state unmutated by construction; reconcile via `derived_stats.reconcile` (pure reducer); mismatch → §6-kept logging only. Spec `conclude.reconcile_derived_stats` names this exact function (specs L992-1020) and is RUNTIME_EVIDENCE_PROVEN | Module docstring ("NEVER mutates state… warn-only NOOP") verified true in body (L119 `return state`) | CONFIRM KEEP |

## backend_adjustment_registry.py — KEEP (shim) — CONFIRMED with reachability caveat

All 24 re-exported names (18 spec groups + 6 types) verified against `__all__`:
`ACTIVE_COMBAT_END_NPC_CLEANUP_ADJUSTMENT_SPECS`, `ACTIVE_LEVEL_UP_MAIN_CLEANUP_SPECS`,
`ACTIVE_LEVEL_UP_SESSION_ROUTING_SPECS`, `ACTIVE_LEVEL_UP_THRESHOLD_OVERRIDE_SPECS`,
`ACTIVE_LLM_ADJUSTER_FRAMEWORK_SPECS`, `ACTIVE_LOCATION_ADJUSTMENT_SPECS`,
`ACTIVE_PR_6958_ADJUSTMENT_SPECS`, `ACTIVE_PR_7149_ADJUSTMENT_SPECS`,
`ACTIVE_PR_7164_ADJUSTMENT_SPECS`, `ACTIVE_PR_7236_RESOURCE_REGISTRY_SPECS`,
`ACTIVE_PR_7339_ADJUSTMENT_SPECS`, `ACTIVE_PR_8489_ADJUSTMENT_SPECS`,
`ACTIVE_PR_8777_ADJUSTMENT_SPECS`, `ACTIVE_PR_9859_ADJUSTMENT_SPECS`,
`ACTIVE_PR_9867_ADJUSTMENT_SPECS`, `ACTIVE_PR_9942_ADJUSTMENT_SPECS`,
`ACTIVE_SOCIAL_HP_ROLL_ATTRIBUTION_ADJUSTMENT_SPECS`,
`ACTIVE_SOCIAL_HP_TERMINAL_RESOLUTION_ADJUSTMENT_SPECS`,
`AdjustmentSpec`, `EvidenceStatus`, `InvalidAdjustmentSpecError`, `RootCauseStatus`,
`SpecCategory`, `SpecScope`.
Reachability caveat (not a verdict change): no production file imports this shim — consumers are
`mvp_site/tests/test_backend_adjustment_registry.py`, `test_admin_xp_correction_adjuster.py`, and
`scripts/adjustment_proof_matrix.py`. It is a backward-compat/test/tooling surface, not a live game-path
import. Each name inherits its source verdict; the shim performs no transform and justifies no spec.
Correction to run 2's registry note: this shim does NOT omit `ACTIVE_LEVEL_UP_MODAL_REWARDS_PAIRING_SPECS`
and `ACTIVE_REWARDS_DELIVERY_SUPPRESSION_SPECS` "which live in adjusters/specs.py instead" — it omits
both, and `adjusters/specs.py` forwards only the former (see C5); the latter is forwarded nowhere.
| Run-2 verdict: CONFIRM KEEP (shim), with the importer correction above. |

## backend_adjustment_types.py — KEEP (shim) — CONFIRMED

Re-exports `AdjustmentSpec`, `EvidenceStatus`, `InvalidAdjustmentSpecError`, `RootCauseStatus`,
`SpecCategory`, `SpecScope` from `adjusters/types.py`, each inheriting its source verdict.
No independent behavior. | Run-2 verdict: CONFIRM KEEP. |

## rewards_engine.py — ADAPT (split the reducer; keep the authorization core) — CONFIRMED, fully read

Both reducers read in full (see header). Branch inventory for `_canonicalize_core`
(L6015–~7075): classify + transition extraction → signal-enrichment block (rewards_box
source/source_id copy; XP enrich from box incl. derived `previous_turn_exp = current - gained`;
threshold copy; progress-provenance copy of `progress_percent`/`xp_floor`/`progress_floor`/
`level_floor`/`canonical_progression`; rewards_pending-context enrich) → `canonicalize_level_up_signal`
None-path (transitioned raw-box return; modal-projection return; orphan-strip return) →
contradiction guard + false-positive path → `_hydrate_level_up_signal_xp` (DELETE) +
`format_model_level_up_signal` (DELETE) calls → formatted-box level-projection merge → stale
reference-state guard (×2 sites) → level_up=False non-level preservation branch (with
`_anchor_rewards_box_xp` call) → formatted-present path incl. `world_logic.inject_modal_finish_choice_if_needed`
call → malformed-signal path (sealed-box deepcopy with server-written `level_up_available=True`;
modal projection; delta-match preservation; `non_level_rewards_box_synthesis_allowed` meta) →
no-signal path (stale explicit-false suppression; canonical-pending/transitioned/review-live
detection; Step A: stale-echo strip, `synthesize_rewards_box_from_state` (DELETE) call gated on
`agent_mode == MODE_REWARDS`, state-box fallback with transient-key pops, rewards_pending
`xp_gained` merge gated on delta equality, M3 transitional stale-flag suppression,
`_level_crossing_this_turn` server-setting `level_up_available=True`, state-backed suppression,
`_anchor_rewards_box_xp` + `current_level` backfill from sheet, visibility gate, atomicity returns;
Step B: raw + `ensure_rewards_box` merge (skipped when transitioned+raw), `_anchor_rewards_box_xp`,
planning unwrap, normalize, visibility-gate exemption, atomicity return).
Branch inventory for `canonicalize_rewards` (L7521–8773): raw extraction incl. `state_updates`
fallback → signal XP backfill from `state_updates` PCD (a second enrichment branch, same ADAPT
family) → transition-only (context-backed minimal transition) projection → `_canonicalize_core`
call → `normalize_planning_block_choices` on canon_pb → snapshot/writeback → authored-PCD
canonicalization → PCD progression grant reducer (`_apply_level_up`) → pcd_session_landed branch
(session-backed `level_up_available`/`current_level=from_level`/`new_level=to_level`) → atomic
persistence boundary (accepted-signal handling, secondary stale guard, same-response-crossing
`_apply_level_up` branch, generic `_apply_model_level_up_signal` branch, fail-closed rollback via
`_restore_canonical_pair`, orphan-meta clear) → saved-session announcement block → XP-delta
mismatch delivery guard → delivery recording → admitted-reward-event fallback synthesis
(`synthesize_rewards_box_from_state` (DELETE) call + level fields) → orphan fail-closed detector →
`_normalize_inconsistent_rewards_box_level_aliases` (DELETE) call → backward-offer retire →
`strip_fabricated_rewards_box_new_level` + nested `state_updates` sync → unresolved-signal repair
arming → legacy-session repair arming → review-doorway projection (`project_level_up_review_choice`,
ADAPT) → return. The ADAPT split below must remove/replace every DELETE-function call listed, not
just "branches" in the abstract.

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| _world_logic_module, is_state_flag_true / is_state_flag_false | Intra-file + lazy world_logic access (L6423 modal-finish injection) | Import transport; boolean predicates | Accurate | CONFIRM KEEP |
| _REWARDS_BOX_XP_GAIN_KEYS, REWARD_CORRECTION_PREFIX, is_reward_correction / _is_reward_correction, _REWARD_EVENT_TIER_BAND_CEILINGS, _UNRECEIPTED_XP_BAND_CEILING / _UNRECEIPTED_XP_FLOOR, _REFUSED_DUPLICATE_SOURCE_CLAIM / _REFUSED_INVALID, SANCTIONED_ZERO_DELTA_CARVE_OUTS, LEVEL_UP_CHOICE_IDS / LEGACY_STALE_LEVEL_UP_CHOICE_IDS / LEVEL_UP_ENTRY_CHOICE_IDS / LEVEL_UP_CHOICE_TYPES, _LEVEL_MUTATION_AUTHORIZED_MODES, _POOL_MAX_KEYS / _POOL_REMAINING_KEYS, TURN_CLASS_* constants, _TANGIBLE_GOLD_PATHS / _TANGIBLE_ITEM_PATHS | Intra-file (receipt/authorization vocabulary) | Capacity + receipt + explicit-signal vocabularies | Accurate, except ASI_CHOICE_IDS below | CONFIRM KEEP (grouped; every name named here) |
| ASI_CHOICE_IDS (L1934) | **Zero references anywhere** (whole-tree token + string search; `world_logic.py:3588` defines its own separate `_ASI_CHOICE_IDS`) | Dead vocabulary: run-2's grouped KEEP ("choice recognition needs the exact id vocabularies") is wrong for this one constant — ASI routing in this file uses `LEVEL_UP_CHOICE_TYPES` ("asi") and god-mode prefix strips, never this tuple | No docstring; the grouping hid it | **CHALLENGE C2: grouped KEEP → DELETE (this constant only)** |
| _record_rewards_delivery, record_rewards_delivery (alias), is_trackable_reward_source, _reward_event_source_bucket_id, _resolve_reward_event_source_provenance, reward_event_tangible_delta_is_positive, extract_and_validate_reward_event, _validate_reward_event, reject_model_authored_rewards_box, _unreceipted_xp_increase_rejected, _is_plain_number, _tangible_item_key, _tangible_holder, _restore_tangible_field, _turn_added_tangibles, _reapply_tangible_spend, restore_tangible_reward_baseline, _clamp_xp_to_allowance, clamp_reward_event_to_allowance, restore_collision_reward_views, snapshot_raw_reward_event, _admit_model_reward_event, _authored_positive_gained, _sync_admin_xp_update, capture_and_validate_reward_event, admit_reward_event_for_state_update | Receipt/validation path; `canonicalize_rewards` delivery tail; `llm_parser.py`/`world_logic.py` boundaries | Receipt validation, anti-cheat clamps (nonzero remainder preserved — consistent with the repo's clamp rule), baseline restore, admin absolute-XP sync under the God Mode promise. None sizes a reward | Accurate | CONFIRM KEEP (grouped; every name named here) |
| effective_pre_turn_level | Band sizing | `max(stored level, XP-derived level)` lets XP-derived levels override the model's level — body confirms the XP branch | Accurate | CONFIRM ADAPT (stored level only; delete XP-derived branch) |
| level_band_span, detect_reward_anomalies + nested _record, _is_pending_level_up_modal_activation, _has_level_up_modal_structure, should_clear_false_positive_level_up_flags, is_level_up_choice_identifier, is_level_up_choice, is_level_up_review_choice, is_level_up_review_doorway, _find_choice_in_block, _lookup_planning_choice_by_id, _planning_choice_items, resolves_to_level_up_entry, strip_fabricated_rewards_box_new_level, _extract_xp_robust, _coerce_nested_mapping, is_level_up_audit_active, _session_transition_is_actionable, _model_level_transition_is_actionable, _pending_level_up_transition_is_actionable, _canonical_pending_level_up_transition + nested _session_available_fallback, rewards_box_level_transition_is_actionable, _reject_malformed_normalized_lus, public_level_up_signal_contract, _pre_turn_character_creation_concluded, cc_authorized_level_write, _is_authorized_level_up_finish_release, _is_authorized_pcd_progression_grant, _is_number, _revert_pool_maximum / _revert_pool_entry / _revert_resource_pool / _revert_level_scaled_sheet_fields / nested _revert / _restore_rejected_pcd_transaction, block_unauthorized_level_mutations, block_unauthorized_level_mutation_deltas, _coerce_state_mapping, _has_unapplied_xp_threshold_crossing, authorize_level_up_entry, level_up_pending_has_reward_payload + nested _positive, is_stale_rewards_pending, is_level_up_active, is_level_up_transition_actionable, pending_level_up_target_level, contains_mapping_shape, clear_stale_level_up_complete_flags, clear_level_up_lock_flags, resolve_level_up_signal, ensure_rewards_box, ensure_planning_block, _coerce_rewards_box_xp_gained, _raw_rewards_box_level_up_is_actionable, _active_modal_rewards_box_from_signal_or_state, _is_positive_reward_value, should_show_rewards_box, _reward_values_match, _raw_rewards_box_looks_like_stale_echo, scrub_stale_rewards_from_older_entries, sanitize_rewards_state_for_context, extract_planning_choice_ids, enforce_rewards_box_planning_atomicity, planning_has_level_up_review_choice, planning_has_level_up_choices, planning_has_time_freezing_level_up_choices, planning_has_advanced_level_up_choice, LevelUpTurnClassification + active_context, classify_level_up_turn, _box_target_is_open_session_review, _MISSING, _snapshot_canonical_pair + nested _capture, _restore_canonical_pair + nested _restore, _write_canonical_field, _writeback_canonical_pair, _canonical_persistence_state_changed + nested _changed, _clear_orphan_level_up_meta, _strip_post_finish_level_up_choices + nested _is_stale, _strip_orphan_level_up_choices + nested _is_orphan_control, _detect_level_up_orphan_fail_closed, format_level_up_orphan_fail_closed_warning, format_level_xp_mismatch_warning, _resolve_authored_level_up_intent, _planning_block_has_explicit_freeze_time, project_level_up_ui, project_level_up_ui_locally (alias), detect_rewards_discrepancy, _detect_rewards_discrepancy (alias) | Turn-path + polling-path callers (`world_logic.py`, `llm_parser.py`); `_detect_level_up_orphan_fail_closed` uses `xp_needed_for_level` thresholds but only to decide whether to WARN, never to mutate — warn-only diagnostic, same class as conclude_invariant | Authorization, fail-closed reverts, explicit-signal routing, durable-write mechanics, polling projection from persisted evidence only. `_detect_level_up_orphan_fail_closed`'s threshold use is detection-only | Mostly accurate; one precision flag: `detect_rewards_discrepancy`'s docstring framing ("Report discrepancies without marking delivery") is true about delivery, but the body MUTATES its input (creates `combat_state`/`encounter_state` {} when absent and pops `rewards_synthesized_for_total_xp`) — "reports only" overstates purity; see §3. Verdict unchanged | CONFIRM KEEP (grouped; every name named here) |
| _sync_authored_xp_fields | Sheet sync path | Canonical sync KEEP; legacy-alias sync sunsets with aliases | Accurate | CONFIRM ADAPT (canonical sync only) |
| _anchor_rewards_box_xp | Called from core (×3 sites), non-level branch, Step B, same-response-crossing branch | Re-anchors box XP to accepted sheet, hiding model/box disagreement instead of flagging it; integrity-case flagging may stay | Body confirms overwrite semantics | CONFIRM ADAPT (integrity flagging only; delete routine re-anchoring) |
| _reward_display_inventory_item_name, _reward_display_inventory_counts, _reward_display_loot_delta, _reward_display_gold, project_reward_display_from_receipt | Display path only | Display derivation the client can do from the validated receipt; formatting alone never justifies a transform | Accurate | CONFIRM DELETE |
| saved_level_up_choice_id_for_text | `agents.py` entry resolution (`or saved_level_up_choice_id_for_text(...)` fallback) | Text→saved-control-id matching is fuzzy text matching under explicit-signals-only; id submission is the clean path | Accurate | CONFIRM ADAPT (explicit id submission; delete text branch) |
| backfill_rewards_box_new_level, _normalize_inconsistent_rewards_box_level_aliases | `level_up_amend_reapply` alias; `canonicalize_rewards` tail (alias-normalization call) | Post-hoc box mutation / alias normalization; session projector must own it. NOTE: the ADAPT for `canonicalize_rewards` must remove its alias-normalization call site, since the function itself is DELETE | Accurate | CONFIRM ADAPT (backfill) / DELETE (alias normalizer) |
| _total_character_level | Multiclass total path | Sums class levels — model-owned derived value, no named exception | Accurate | CONFIRM DELETE |
| _PROGRESS_PERCENT_ABS_TOLERANCE_PP / _PROGRESS_PERCENT_REL_TOLERANCE_FRAC / _PROGRESS_PERCENT_MIN_ABS_DIFF_FOR_REL, _calculate_canonical_expected_progress, _cross_check_progress_percent_against_xp, _format_model_progress_percent, resolve_canonical_progress_fields, synthesize_rewards_box_from_state | Progress/synthesis paths (incl. core Step A + admitted-event fallback in `canonicalize_rewards`) | Canonical D&D progress recompute + box synthesis from XP delta — the T1 delete target; tolerances die with the recompute they parameterize | Accurate | CONFIRM DELETE |
| _pick_first_present, _coerce_model_int, _coerce_model_optional_int, _coerce_model_optional_percent, _coerce_model_optional_floor | Signal parsing (core + canonicalize) | Boundary parsing preserving explicit values incl. explicit zero; invent nothing | Accurate | CONFIRM KEEP |
| _coerce_flag_or_none (L2558) | **Zero callers anywhere** (whole-tree token + string search) | Dead helper: run-2's grouped KEEP is wrong for this one function | Docstring claims it prevents Mock flag confusion "in is_level_up_active" — but `is_level_up_active` (L4446) never calls it; it delegates to `is_level_up_audit_active`. Stale docstring + dead code | **CHALLENGE C3: grouped KEEP → DELETE** |
| _level_up_signal_can_use_rewards_box_xp_evidence, _normalize_level_up_signal_payload, canonicalize_level_up_signal, _hydrate_level_up_signal_xp, format_model_level_up_signal, _pending_rewards_from_canonical_signal, _inject_levelup_choices_if_needed, _apply_contradiction_guard, substitute_level_up_target, normalize_rewards_box, project_level_up_review_choice | Core + canonicalize paths | XP backfill gate, alias/display normalization, hydration (copy XP from another artifact into the signal), ~300-line UI formatting, compat pending synthesis, server contradiction checks, prompt-placeholder surgery, box typing-with-synthesis, server doorway injection — all belong in prompt/schema/projector or deleted, per run 2's named moves. `canonicalize_rewards`' own signal-XP backfill from `state_updates` PCD is an additional enrichment branch in the same family | Accurate, except `format_model_level_up_signal`'s scale (~300 lines of UI payload formatting) is understated in run 2's one-liner — body confirms display recomputation throughout | CONFIRM ADAPT (each with run 2's named move); `_hydrate_level_up_signal_xp` and `format_model_level_up_signal` are DELETE as functions (their call sites in `_canonicalize_core` must be replaced, not left dangling) — run 2 already says DELETE for both; confirmed |
| _is_authorized_level_up_signal_backed_grant | Legacy compat check | Explicitly grants no authority beyond PCD-evidence checks its callers already have — redundant authorization theater | Accurate ("claims no authority") | CONFIRM DELETE |
| _canonicalize_core (L6015), canonicalize_rewards (L7521) | `world_logic.py` (L3288, L3366, L9113), `llm_parser.py` (L3342), polling path | Full branch inventories above confirm the ADAPT split exactly: session-backed projection + fail-closed authorization + receipt/delivery guards KEEP; synthesis (state boxes, signal XP enrich, transition-only projection, admitted-event fallback synthesis), suppression (stale guards are the KEEP-adjacent half only insofar as they gate on persisted evidence — the stale-guess suppression of model boxes goes), and progress recompute DELETE to prompt/schema. Two additional branch findings inside the ADAPT (not verdict changes): (a) the saved-session announcement block in `canonicalize_rewards` writes `canon_rb["current_level"] = saved_session["to_level"]` AND `new_level = to_level` — inconsistent with the pcd_session_landed branch (`current_level=from_level`); resolve the labeling inside the ADAPT. (b) core's formatted-present path calls `world_logic.inject_modal_finish_choice_if_needed` — a modal-choice injection outside this group whose registered-spec cover must be confirmed before the ADAPT lands | Docstrings ("ALL paths converge here", "STREAMING + NON-STREAMING path… Single source of truth") are accurate about convergence; they do not disclose the synthesis/suppression mix — which is precisely why the split is needed | CONFIRM ADAPT (same named split as run 2, plus (a) and (b) as ADAPT work items) |

## backend_adjustment_specs.py — ADAPT (registry of interim exceptions) — CONFIRMED

Data, not behavior: 89 `AdjustmentSpec` records (verified by `adjustment_id=` count = 89).
Evidence-status tally computed from the file itself: **79 RUNTIME_EVIDENCE_MISSING
(77 active + 2 inactive) / 10 RUNTIME_EVIDENCE_PROVEN (all active)**. Registry membership
justifies nothing — each row below is judged on its `allowed_when`, as run 2 did. The
evidence gap is a cross-cutting caveat (§4, note N1), not a per-spec verdict change, except
where run 2 already tied the verdict to it. Graduation-policy note: the file header states
active specs target graduation (`active=False`) within 90 days with renewal justification;
most active specs here predate that window by PR number (PR 6958/7149/7236/7339/8489/8777/9859/
9867/9942) and still carry MISSING evidence — a process staleness flag for the owner, not a
re-verdict of any single spec. One row per spec; "CONFIRM" means run-2 verdict + reasoning hold
against the spec's own `allowed_when` text.

| Spec | Verdict (run 2) | Evidence | Review |
|---|---|---|---|
| level_up_badge.clear_when_state_proves_stale | KEEP | MISSING | CONFIRM — clears only when persisted pre-turn level proves staleness; removes echo, invents nothing |
| level_up_ui.requires_canonical_pending_evidence | KEEP | MISSING | CONFIRM — gates UI on persisted pending evidence (authorization of display) |
| level_up_modal.pending_activation_flag_sync | ADAPT | MISSING | CONFIRM — slim to server-owned flags only |
| level_up_modal.top_level_false_blocks_nested_activation | KEEP | MISSING | CONFIRM — explicit false wins; fail-closed precedence |
| level_up_routing.exit_suppresses_stale_character_creation_lock | KEEP | MISSING | CONFIRM — explicit-exit cleanup |
| level_up_modal.server_enforces_finish_exit_state | KEEP | MISSING | CONFIRM — modal state machine on explicit finish; explicit-exit guarantee rescues it |
| level_up_modal.blocks_non_finish_state_release | KEEP | MISSING | CONFIRM — fail-closed gating on explicit finish |
| character_creation_modal.finish_choice_normalization_and_affordance | ADAPT | MISSING | CONFIRM — canonical forms to schema; keep explicit-id routing |
| level_up_choice.expand_id_to_visible_text_context | ADAPT | MISSING | CONFIRM — id→text mapping to prompt; delete server expansion |
| level_up_rewards.pending_sync_and_synthesis | ADAPT | MISSING | CONFIRM — keep sync-to-session half; delete synthesis half |
| level_up_rewards.clear_stale_pending_notification | KEEP | MISSING | CONFIRM — removes proven-stale notification |
| level_up_rewards.block_complete_no_new_xp_retrigger | KEEP | MISSING | CONFIRM — anti-replay gating on explicit evidence |
| level_up_story.scrub_stale_history_level_up_ui | KEEP | MISSING | CONFIRM — history hygiene on proven-stale UI |
| level_up_story.project_canonical_pair_for_polling | KEEP | MISSING | CONFIRM — durable read for polling |
| level_up_routing.unrelated_rewards_precede_modal_lock | KEEP | MISSING | CONFIRM — routing precedence; changes no value |
| level_up_choice.classify_backend_choice_ids | KEEP (AUDIT_ONLY) | MISSING | CONFIRM — audit-only; mutates nothing |
| level_up_signal.normalize_aliases_and_display_fields | ADAPT | MISSING | CONFIRM — draining shim to schema |
| level_up_signal.reject_malformed_payload | KEEP | MISSING | CONFIRM — fail-closed validation; invents no replacement |
| level_up_signal.format_to_ui_pair | DELETE | MISSING | CONFIRM — display formatting; client renders the signal contract |
| level_up_pending.derive_from_canonical_signal | ADAPT | MISSING | CONFIRM — fold into session reducer; delete standalone derivation |
| level_up_state.block_unauthorized_model_mutations | KEEP | MISSING | CONFIRM — authorization core (same gate as `block_unauthorized_level_mutations`) |
| level_up_active.suppress_stale_pending_flags | KEEP | MISSING | CONFIRM — proven-stale flag removal |
| level_up_ui.project_from_persisted_pending | KEEP | MISSING | CONFIRM — durable read |
| level_up_rewards.suppress_stale_raw_rewards_echo | KEEP | MISSING | CONFIRM — dedup hygiene on proven-stale echo |
| level_up_context.strip_rewards_state_from_prompt | KEEP | MISSING | CONFIRM — prompt hygiene; persisted state untouched |
| level_up_atomicity.audit_rewards_planning_pair | KEEP (AUDIT_ONLY) | MISSING | CONFIRM — audit-only |
| level_up_core.suppress_stale_target_ui | KEEP | MISSING | CONFIRM — removes UI for already-passed target |
| level_up_core.enrich_missing_xp_evidence | DELETE | MISSING | CONFIRM — invents the XP facts the signal was supposed to carry; the MISSING evidence status strengthens, not weakens, this DELETE |
| level_up_pending.normalize_legacy_xp_alias | ADAPT | MISSING | CONFIRM — draining shim; delete with legacy pendings |
| level_up_validation.flag_xp_level_mismatch | KEEP | MISSING | CONFIRM — flags, never corrects |
| level_up_rewards.synthesize_primary_rewards_box | DELETE | MISSING | CONFIRM — T1 synthesis target; model authors the box |
| level_up_rewards.suppress_unpaired_pending_box | KEEP | MISSING | CONFIRM — modal-envelope enforcement |
| level_up_rewards.defer_box_on_rejected_crossing_grant | KEEP | MISSING | CONFIRM — fail-closed on reducer rejection |
| level_up_modal.clear_stale_pending_when_inactive | KEEP | MISSING | CONFIRM — provably-inactive cleanup |
| level_up_ui.reconcile_story_pair | ADAPT | MISSING | CONFIRM — fold into single session projector |
| level_up_canonicalize.persist_canonical_pair | KEEP | MISSING | CONFIRM — durable write of accepted fields |
| level_up_false_positive.clear_modal_flags | KEEP | MISSING | CONFIRM — proven-false-positive cleanup |
| level_up_response.reconcile_unified_response | ADAPT | MISSING | CONFIRM — single schema shape; delete reconcile pass |
| level_up_polling.project_latest_ui | KEEP | MISSING | CONFIRM — durable read for polling |
| level_up_parser.raw_planning_preserve | KEEP | MISSING | CONFIRM — preservation is the opposite of transformation |
| level_up_parser.custom_action_fallback | ADAPT | MISSING | CONFIRM — prompt-gap coverage to prompt/schema |
| level_up_schema.normalize_planning_choice_shape | ADAPT | MISSING | CONFIRM — shape belongs in schema |
| level_up_context.initial_story_drops_signal | KEEP | MISSING | CONFIRM — prompt hygiene; no persisted grant touched |
| conclude.reconcile_derived_stats | KEEP | PROVEN | CONFIRM — implementation verified warn-only (`conclude_invariant.py:95-119`); the CORRECTION category overstates a logging exception, as run 2 noted |
| level_up_amend.backfill_rewards_box_new_level | ADAPT | MISSING | CONFIRM — inherits backfill ADAPT (projector emission) |
| parse_fail_open.fallback_planning_block | ADAPT | MISSING | CONFIRM — parse-gap coverage to schema/parser contract |
| parse_recovery.escape_unescaped_string_quotes | KEEP | MISSING | CONFIRM — JSON syntax recovery restoring the model's own intended string, not semantic rewrite |
| world_time.partial_merge_preserves_canonical_time | KEEP | MISSING | CONFIRM — durable-write integrity for persisted canonical time |
| session_header.timestamp_repair_from_canonical_world_time | KEEP | MISSING | CONFIRM — server-record integrity from persisted canonical clock |
| rewards_box.progress_percent_xp_anchor | DELETE | MISSING | CONFIRM — display percent recomputed from XP; schema-required signal field instead |
| location.legacy_location_fallback_in_resolve_location | DELETE | MISSING | CONFIRM — legacy compat, not a necessary exception |
| location.prior_location_preservation_when_model_omits_location | ADAPT | MISSING | CONFIRM — interim only; delete once location is schema-required |
| location.session_header_fallback_generation | DELETE | MISSING | CONFIRM — generates a domain fact from a header; server authorship |
| location.early_metadata_deriving_location_confirmed_from_header | ADAPT | MISSING | CONFIRM — narrow to server-stamped headers only |
| combat_end.defeated_enemy_cleanup | ADAPT | PROVEN | CONFIRM — PROVEN evidence does not make it permanent: move removal into combat schema, delete server pass |
| combat_end.nonlethal_combatant_removed_from_tracking | ADAPT | PROVEN | CONFIRM — inherits defeated-cleanup ADAPT |
| ADJ-WA-JSON-STRIP-PREFIX | KEEP | PROVEN | CONFIRM — structural prefix strip before JSON parsing; committed proof artifact + disk gate (see adjusters section) |
| world_time.partial_merge_date_protection | DELETE | MISSING, active=False | CONFIRM — inactive spec; deleting changes no runtime behavior |
| session_header.timestamp_canonical_repair | DELETE | MISSING, active=False | CONFIRM — inactive; live behavior covered by the active `timestamp_repair_from_canonical_world_time` spec |
| rewards_box.progress_percent_xp_curve_fallback | DELETE | PROVEN | CONFIRM — PROVEN here proves the fallback fires, not that server recomputation is the necessary fix (run 2's reasoning holds); schema-require the field instead |
| level_up_canonicalize_core.false_positive_rewards_box_suppressed | ADAPT | MISSING | CONFIRM — interim until M2 prompt fix lands, then delete (spec's own graduation note) |
| level_up_canonicalize_rewards.secondary_stale_signal_guard | KEEP | MISSING | CONFIRM — staleness authorization on persisted level vs signal target |
| level_up_canonicalize_rewards.no_session_rewards_stripped | KEEP | MISSING | CONFIRM — strips offers with no landed session (authorization by reducer result) |
| level_up_session.strip_stale_offer_after_admin_commit | ADAPT | MISSING | CONFIRM — dies at M3 when projector owns offer lifecycle (spec's own note) |
| level_up_session.phantom_offer_clear | ADAPT | MISSING | CONFIRM — same M3 sunset |
| god_mode.strip_modal_choices_on_admin_commit | ADAPT | MISSING | CONFIRM — interim until demonstrated model compliance with god-mode prompt prohibition |
| god_mode.mixed_contract_admin_commit_wins | ADAPT | MISSING | CONFIRM — same compliance sunset; admin commit is the operator's explicit act |
| god_mode.rejected_commit_level_revert | KEEP | MISSING | CONFIRM — fail-closed durability for operator action |
| level_up_session.finish_release_authorization | KEEP | MISSING | CONFIRM — authorization gate on explicit finish evidence |
| level_up_session.signal_backed_grant_authorization | KEEP | MISSING | CONFIRM — authorization gate on explicit signal evidence |
| level_up_routing.session_overrides_stale_clear | KEEP | MISSING | CONFIRM — durable-session precedence over stale clear |
| player_character_data.ac_alias_mirrors_authored_armor_class | KEEP | MISSING | CONFIRM — storage consistency, same class as `_set_armor_class` |
| level_up_modal.in_modal_rewards_box_pairing | KEEP | PROVEN | CONFIRM — modal-envelope authorization |
| level_up_turn.classify_mid_review_active_context | KEEP | MISSING | CONFIRM — routing on explicit review-context evidence |
| level_up_story.preserve_amendable_review_ui | KEEP | MISSING | CONFIRM — projection of persisted grant state, not a new offer |
| level_up_modal.session_authoritative_lock_gate | KEEP | MISSING | CONFIRM — authorization by the durable session record |
| level_up_signal.context_backed_minimal_transition | ADAPT | MISSING | CONFIRM — narrow to contexts carrying an explicit signal; delete the derivation branch (matches the transition-only projection branch in `canonicalize_rewards`) |
| level_up_review.project_doorway_when_missing | ADAPT | MISSING | CONFIRM — doorway into prompt/schema; interim server projection only |
| level_up_choice.resolve_saved_control_text | ADAPT | MISSING | CONFIRM — text→id resolution under explicit-signals-only; move to id submission |
| god_mode.resource_registry_clamp_bypass | KEEP | MISSING | CONFIRM — operator-directed bypass = God Mode promise, not server authorship |
| resource_registry.death_saves_reset_on_long_rest | ADAPT | MISSING | CONFIRM — rules recomputation; move into rest contract |
| resource_registry.preserve_triggered_current_without_rest | KEEP | PROVEN | CONFIRM — preservation, not transformation |
| level_up_modal.stale_freeze_time_choice_stripped_after_close | KEEP | PROVEN | CONFIRM — cleanup keyed to explicit close + server-owned modal state |
| admin_xp_correction.pop_zero_gained_receipt | KEEP | PROVEN | CONFIRM — operator-directed receipt handling under God Mode promise |
| rewards_delivery.tangible_award_gate | KEEP | MISSING | CONFIRM — delivery gating on receipt evidence |
| rewards_delivery.xp_delta_mismatch_guard | KEEP | MISSING | CONFIRM — anti-cheat guard on receipt mismatch |
| graveyard.apply_character_death_signals | ADAPT | MISSING | CONFIRM — move death state into death contract; delete server application |
| social_hp.executed_roll_attribution | KEEP | PROVEN | CONFIRM — attribution of a server-executed (RNG-verified) roll; §6 anti-cheat audit bookkeeping, not an outcome decision. The only fully-proven spec in this group besides the adjuster/structural ones |
| social_hp.terminal_status_resolution | ADAPT | MISSING | CONFIRM — rules computation; move into damage contract |

### Grouping tuples (20 unique; 21 assignments)

Each tuple is a pure index; members carry their own rows above. 19 tuples CONFIRM KEEP as indices.
**One CHALLENGE (C5):** `ACTIVE_REWARDS_DELIVERY_SUPPRESSION_SPECS` (specs L2465) — **KEEP → DELETE
(tuple only; its two member specs keep their KEEP verdicts)**. Proof: whole-tree token + string
search finds zero importers — it is NOT forwarded by `adjusters/specs.py` (which forwards only 14
groups) and NOT imported by `backend_adjustment_registry.py`, contrary to run 2's registry note
claiming it "lives in adjusters/specs.py instead". The only mention outside its definition is a
historical `docs/conflicts/` summary. An index nothing imports indexes nothing.
Dead-weight notes (no behavior change, listed in §1): `ACTIVE_PR_7164_ADJUSTMENT_SPECS` is an
empty tuple, and the first `ACTIVE_PR_8489_ADJUSTMENT_SPECS` definition (L1113, empty) is shadowed
by the second (L1989) — run 2 correctly noted "second definition wins".
Tuples confirmed KEEP: `ACTIVE_LOCATION_ADJUSTMENT_SPECS`, `ACTIVE_PR_6958_ADJUSTMENT_SPECS`,
`ACTIVE_PR_7149_ADJUSTMENT_SPECS`, `ACTIVE_PR_7164_ADJUSTMENT_SPECS` (empty; see dead-weight note),
`ACTIVE_PR_8489_ADJUSTMENT_SPECS`, `ACTIVE_PR_7339_ADJUSTMENT_SPECS`,
`ACTIVE_PR_9867_ADJUSTMENT_SPECS`, `ACTIVE_COMBAT_END_NPC_CLEANUP_ADJUSTMENT_SPECS`,
`ACTIVE_LLM_ADJUSTER_FRAMEWORK_SPECS`, `ACTIVE_LEVEL_UP_THRESHOLD_OVERRIDE_SPECS`,
`ACTIVE_LEVEL_UP_MAIN_CLEANUP_SPECS`, `ACTIVE_LEVEL_UP_SESSION_ROUTING_SPECS`,
`ACTIVE_LEVEL_UP_MODAL_REWARDS_PAIRING_SPECS`, `ACTIVE_PR_7236_RESOURCE_REGISTRY_SPECS`,
`ACTIVE_PR_8777_ADJUSTMENT_SPECS`, `ACTIVE_PR_9859_ADJUSTMENT_SPECS`,
`ACTIVE_PR_9942_ADJUSTMENT_SPECS`, `ACTIVE_SOCIAL_HP_ROLL_ATTRIBUTION_ADJUSTMENT_SPECS`,
`ACTIVE_SOCIAL_HP_TERMINAL_RESOLUTION_ADJUSTMENT_SPECS`.

## adjusters/ — KEEP (framework) — CONFIRMED, with 2 CHALLENGES and docs lens below

Live wire-in verified: `narrative_response_schema.py:5943` calls `engine.process` inside
`parse_structured_response`, wrapped in try/except (L5928-5955), with a session id resolved from
`session_id` → `campaign_state.campaign_id` → `campaign_state.session_id` — exactly the
session-resolution the docs describe (see docs lens). The engine is therefore live, not theoretical.

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict |
|---|---|---|---|---|
| adjusters/__init__.py (imports game for registration side effects; re-exports AdjusterEngine, engine, AdjusterRegistration, AdjusterScope, CorrectionMode, EvidenceObject) | Package import path (`narrative_response_schema.py:34`) | Registration side effect + re-exports only | Accurate | CONFIRM KEEP |
| adjusters/base.py AdjusterEngine.__init__ (max_sessions=1000) | Singleton construction | Capacity bound; server-owned | Accurate | CONFIRM KEEP |
| AdjusterEngine._ensure_registered | process() path (lazy) | Lazy load; failure logs and fails open to unmodified output | Accurate | CONFIRM KEEP |
| AdjusterEngine.register_allowed_specs | **Only callers are tests** (`tests/_adjuster_fixtures.py:9`, `tests/test_llm_adjuster.py` ×7) — no production caller | Test-fixture plumbing shipped in a production module | Docstring itself says "For test fixtures only" — accurate, and that accuracy is the flag | **CHALLENGE C8: KEEP → ADAPT (move to a test-only engine subclass/fixture; production module should not carry test-only extension points). Low priority; behavior-neutral** |
| AdjusterEngine.register | `_register_once` (json_strip_prefix) + tests | Proof gate verified in body: active registered spec + pre-committed disk sha256 recomputed + valid scope; synthetic in-code evidence rejected | Docstring matches the gate exactly | CONFIRM KEEP |
| AdjusterEngine._sorted_adjusters, _get_session_counts_locked, _should_intercept_safely | process() internals | Priority order, bounded LRU under lock, fail-closed predicate errors | Accurate | CONFIRM KEEP |
| AdjusterEngine.process | `narrative_response_schema.py:5943` (sole prod caller) | Fast path returns original dict untouched when nothing intercepts (verified); SILENT exemption from T9 cap (verified in body); snapshot rollback; result-type validation; applied-adjustment records; WARN/FLAG notices. Bounded capacity + transaction integrity, not domain authorship | Docstring is thin ("Process LLM output through registered adjusters") but the class docstring states the caps/rollback contract accurately | CONFIRM KEEP |
| AdjusterEngine.list_adjusters | **Zero callers anywhere** (whole-tree token + string search, prod and tests) | Operator observability with no consumer — dead public method on a live class | No docstring claim beyond "for observability" | **CHALLENGE C4: KEEP → DELETE (an external ops caller outside this tree would rescue it; none exists in the tree)** |
| adjusters/base.py engine (singleton) | Imported by `narrative_response_schema.py:34` (as `_adjuster_engine`) + json_strip_prefix registration | Shared instance; no logic | Accurate | CONFIRM KEEP |
| adjusters/registry.py (re-export shim) | **Only test importers** (`tests/test_backend_adjustment_registry.py`, `tests/test_conclude_invariant.py`); no prod importer | Re-exports 16 groups + 6 types; subsetting is import history, not judgment | Module docstring ("re-export shim for the backend adjustment authority list") overstates completeness — it is a subset (missing COMBAT_END, PR_7164, SOCIAL_HP_TERMINAL, REWARDS_DELIVERY_SUPPRESSION) | CONFIRM KEEP (compat/test surface; flagged in §2), docs precision note in §3 |
| adjusters/specs.py (forwarding module) | `adjusters/base.py` register() (live: ACTIVE_LLM_ADJUSTER_FRAMEWORK_SPECS) + registry shim | Forwards 14 groups verbatim; no transform; each group inherits members' verdicts | **Docstring false: "forwarding all active specs" / "Avoids dual source-of-truth drift by forwarding all active specs directly" — it forwards 14 of 20 groups** (missing PR_7149, PR_7164, COMBAT_END, SOCIAL_HP_ROLL, SOCIAL_HP_TERMINAL, REWARDS_DELIVERY_SUPPRESSION). See §3 | CONFIRM KEEP (forwarding itself is sound); docstring correction required |
| adjusters/types.py InvalidAdjustmentSpecError, SpecCategory, SpecScope, RootCauseStatus, EvidenceStatus, _PROOF_REQUIRED_CATEGORIES, _is_gist_url, _is_runtime_ref, _has_runtime_evidence, AdjustmentSpec, AdjustmentSpec.__post_init__, AdjustmentSpec.enabled (deprecated alias) | Specs module + registry shims + engine validation | Framework authorization record: proof requirements, raw_response ban, gist/runtime URL shape, PROVEN-requires-artifact rule — all verified in body. `enabled` alias: active-wins rule verified | Accurate; deprecation comments are explicit | CONFIRM KEEP (all); `enabled` CONFIRM ADAPT (delete once legacy callers migrate) |
| adjusters/schemas/__init__.py, adjusters/utils/__init__.py, adjusters/game/__init__.py | Package imports; game init imports json_strip_prefix for registration | No logic beyond import side effect | Accurate | CONFIRM KEEP |
| adjusters/schemas/models.py AdjusterScope, CorrectionMode, EvidenceObject, EvidenceObject.validate_proof_artifacts, EvidenceObject.compute_hash, EvidenceObject.load_from_disk, EvidenceObject.save_to_disk, AdjusterRegistration | Engine + json_strip_prefix + evidence flow | Serializable proof schema; redaction enforced via `redact_pii` on save; hash excludes hash/URL fields (verified in body) | Accurate; `validate_proof_artifacts` docstring honestly states it checks artifact shape, not the semantic claim | CONFIRM KEEP |
| adjusters/game/json_strip_prefix.py _EVIDENCE_DIR, _load_committed_evidence, _get_evidence, _PREFIX_RE, _RAW_RESPONSE_KEYS, _strip_mode_prefixes, _iter_raw_response_values, should_intercept_json_prefix, override_strip_json_prefix, _register_once (+ import-time try/except) | Engine registration (priority 10, first) via `adjusters/__init__` → game import | Regex matches only declared literal mode labels (`[Mode: …]`, `[STORY MODE]`, `[GOD MODE]`) with REGEXP APPROVED note; strips only when remainder parses as JSON object; fails open to unmodified output when evidence is absent. Structural parse fix, not semantic routing | Two precision flags (see §3): override docstring claims stripping "before first '{' or '[' (array)" but `_strip_mode_prefixes` returns None unless the remainder starts with "{" — arrays are never stripped (the intercept docstring correctly says arrays must NOT intercept). Module docstring's "~50% failure rate" claim is evidence-bundled, not re-verified here | CONFIRM KEEP (all) |
| adjusters/utils/redact.py _SSN_RE, _PII_PATTERNS, is_luhn_valid, redact_pii | Evidence save path (`models.py`) | PII redaction for durable artifacts; SSN consistent-separator rule + Luhn-gated card redaction verified in body; recursive over str/list/dict | Accurate | CONFIRM KEEP |
| adjusters/evidence/ADJ-WA-JSON-STRIP-PREFIX/v1/proof.json + proof.sha256 | Required by `_load_committed_evidence` → engine proof gate | Durable proof data; without them the adjuster cannot register (fail-open to unmodified output) | N/A (data files; hash verified by the gate at registration, not re-computed in this review) | CONFIRM KEEP |

### adjusters/docs/ + adjusters/README.md — docs lens (accuracy vs code) — KEEP, with corrections

Read all 12 files (README 176 lines; docs 00–10, 130–315 lines each) and checked their load-bearing
claims against the code. The framework description is substantially accurate; the corrections are:

| Doc | Verdict | Accuracy finding |
|---|---|---|
| README.md | KEEP | Accurate: entry point, authority split (specs = governance, engine = mechanism), wire-in call site (`narrative_response_schema.parse_structured_response`), fleet table correctly labels 5 of 6 adjusters "planned" and only JSON-STRIP-PREFIX "shipped". The "MUST have matching entry" convention note honestly states it is enforced by script + review, not a CI gate. One overstatement: "Quick orientation" calls `adjusters/registry.py` the "Backward-compatible re-export shim for the backend adjustment authority list" without noting it is a subset (see specs.py note above) |
| 00-zfc-origin.md | KEEP | Accurate lineage + self-contained ZFC excerpt; correctly states the engine encodes named ZFC rules. No code contradiction found |
| 01-core-invariant.md | KEEP | "LLM decides by default; overrides only with empirical proof" matches `register()`'s gate and `process()`'s fast path |
| 02-tenets.md | KEEP | Tenets table is honest where the code falls short: T8 auto-deprecation is marked "not yet wired in WorldAI" (confirmed — no such job in this group; 09-lifecycle says the same). T6 rollback + T9 caps match `process()` body |
| 03-types.md | KEEP | "The bulk of the engine lives in one `process()` method" — true in substance (`process()` is the largest method in `base.py`, ~130 of 321 lines, containing the fast path, cap, snapshot, and rollback logic). The scope/mode non-enforcement note ("the engine itself does not enforce which mode goes with which scope") matches the code (no such check in `register()`/`process()`) |
| 04-engine.md | KEEP | Registration, priority sort, SILENT cap exemption, rollback, and `_applied_adjustments` records all match `base.py`. The SILENT-exemption rationale ("runs on every JSON response and never [exhausts budget]") matches the code comment |
| 05-authoring.md | KEEP | Two-callable contract (`should_intercept`, `override_action`) matches the shipped adjuster; fleet table (§ WorldAI fleet) correctly says "currently planned or shipped" and "Only ADJ-WA-JSON-STRIP-PREFIX has a committed proof artifact today" — verified: it is the only directory under `adjusters/evidence/`. Proof-directory path cited matches the tree |
| 06-wire-in.md | KEEP | Wire-in contract matches the live call site: response text under `llm_raw_output`/`raw_response_text` keys (both passed at `narrative_response_schema.py:5945-5948`), session-id resolution (call site resolves campaign/session id before calling, and `process()` itself falls back to `campaign_state` ids), try/except wrapping (call site + engine fail-closed). The "Without [session id] the T9 cap is disabled" warning is accurate for direct `process()` callers and is handled at both layers for the shipped call site |
| 07-redaction.md | KEEP | Redaction list matches `_PII_PATTERNS` (JWT, Bearer, API keys, SSN, email, Luhn-gated card) |
| 08-testing.md | KEEP | Test references check out: `mvp_site/tests/test_llm_adjuster.py` and `mvp_site/tests/test_end2end/test_adjuster_framework_end2end.py` both exist in the tree; layer descriptions match the engine mechanics |
| 09-lifecycle.md | KEEP | `add → deprecate → remove` with no direct `add → remove` is a process rule, not code, so it cannot contradict code; its honesty notes check out ("this job is not yet wired", "this state is empty; no adjuster has been removed"). The deprecation example citing the shipped adjuster's spec entry matches the specs file |
| 10-checklist.md | KEEP | Checklist items (proof, scope, priority, cap, redaction) map 1:1 onto `register()`'s enforced gates and `AdjusterRegistration` fields |

### mvp_site/docs/zfc_audit/ — DELETE (archive, stale 2026-05-01 snapshot) — CONFIRMED

| Doc | Evidence | Review |
|---|---|---|
| SUMMARY.md (141 lines, audit date 2026-05-01, scope 118 files / ~631 methods) | Claims "~95% ZFC-compliant", 3 non-compliant methods, ~35 needing review; its "ZFC-Compliant — Keep" table lists "FastEmbed semantic routing: `intent_classifier.py` — user confirmed counts as 'LLM decides'" and its target architecture centers the FastEmbed classifier | **CONFIRM DELETE (archive).** The classifier row is directly superseded: the pilot + §6(4) verdict DELETEs `intent_classifier.py` in full and replaces the role with Jev — the snapshot's central compliant-pattern claim is now the deleted pattern. The 95% headline is also irreconcilable with this review pass's own findings in this group alone (28 run-2 DELETE rows + 68 ADAPT rows in godmode/levelup/rewards). A May snapshot must not be cited as current compliance evidence |
| FULL_AUDIT.md (1,301 lines, same 2026-05-01 snapshot, per-file per-method) | Same staleness at larger scale; its own update protocol warns rows go stale on renames; this review pass supersedes its godmode/levelup/rewards rows | **CONFIRM DELETE (archive).** Not imported or executed (deleting breaks nothing at runtime); superseded by the run-2 group file for this area and by this review. Archive, don't cite |

## (1) Dead / unreachable code list

Proven by whole-`mvp_site/` token index (prod + tests separately) + whole-repo string search.
Intra-file-only helpers (140 symbols) are NOT listed: use within their own file is use.
Framework-dispatched methods are NOT listed: `god_mode_schema.validate_total_operations` looks
name-uncalled but is invoked by Pydantic via `@model_validator(mode="after")` (schema L231) —
verified non-dead, and run-2 KEEP stands.

1. `level_up_session.py:26` TERMINAL_STATUSES — zero code references; run-2 KEEP → DELETE (C1).
2. `rewards_engine.py:1934` ASI_CHOICE_IDS — zero references; run-2 grouped KEEP → DELETE (C2).
3. `rewards_engine.py:2558` _coerce_flag_or_none — zero callers; run-2 grouped KEEP → DELETE (C3).
4. `adjusters/base.py:305` list_adjusters — zero callers in tree incl. tests; run-2 KEEP → DELETE (C4).
5. `backend_adjustment_specs.py:2465` ACTIVE_REWARDS_DELIVERY_SUPPRESSION_SPECS (tuple only) —
   zero importers; run-2 grouped KEEP → DELETE tuple only, members keep KEEP (C5).
6. `backend_adjustment_specs.py:1111` ACTIVE_PR_7164_ADJUSTMENT_SPECS — empty tuple; dead weight,
   no behavior change on removal (grouped KEEP stands as an index of nothing; recommend deletion as cleanup).
7. `backend_adjustment_specs.py:1113` ACTIVE_PR_8489_ADJUSTMENT_SPECS (first definition, empty) —
   shadowed by the second definition (L1989); dead by shadowing, no behavior change on removal.
8. No other symbol in this group is wholly unreferenced: run-2's headline claim ("no symbol was
   found wholly unreferenced") is WRONG for items 1–5 above but holds for everything else once
   intra-file use and framework dispatch are counted correctly.

## (2) Test-only / demo code in prod files list

1. `adjusters/base.py:63` register_allowed_specs — only callers are `tests/_adjuster_fixtures.py:9`
   and `tests/test_llm_adjuster.py`; docstring admits "For test fixtures only". CHALLENGE C8:
   ADAPT out of the production module into test harness (behavior-neutral, low priority).
2. `adjusters/registry.py` (whole shim) — only importers are tests
   (`tests/test_backend_adjustment_registry.py`, `tests/test_conclude_invariant.py`); no production
   importer. KEEP as compat/test surface, flagged (not a verdict change: shims exist for import
   stability, and tests pin the import path).
3. `backend_adjustment_registry.py` (whole shim) — no production importer; consumers are tests
   plus `scripts/adjustment_proof_matrix.py` (tooling). KEEP as compat/test/tooling surface, flagged.
4. No demo/example code was found in any file in this group (contrast `mcp_client.example_usage`
   in the gateway group, which is not in this area). No file in this group is test-only as a whole.

## (3) Stale / misleading docs list

Each item states what the code actually does.

1. `mvp_site/modal_conclude_policy.py:90-91` + `:236-241` — docstrings name "the FastEmbed
   semantic exit-intent classifier" as "the SOLE authority for free-text input". Code actually does:
   delegate free text to injected callables that are live-wired to `intent_classifier.*`
   (pilot-DELETE files) in `agents.py`. Post-pilot, the authority is Jev Noul flag + explicit
   confirmation, not FastEmbed. Stale; update with the C6 rewiring.
2. `mvp_site/modal_conclude_policy.py:48-51` (`_bare_token_normalize` docstring) — claims "NOT
   used to rewrite arbitrary user free-text into routing decisions". Code actually does: stage 4b
   (L167-173) rewrites any token matching after case-fold/separator-strip into a canonical id.
   The claim contradicts the stage it serves.
3. `mvp_site/modal_conclude_policy.py:79-100` (`extract_modal_choice_id` docstring) — lists four
   structured forms but omits the fifth behavior: stage 4b bare-token matching plus the verbatim
   fallbacks for unrecognized CHOICE:/JSON ids (L78, L145-146). Code actually returns unrecognized
   ids verbatim; only caller membership-checks make that safe (C7).
4. `mvp_site/rewards_engine.py:2558` (`_coerce_flag_or_none` docstring) — claims the helper
   prevents Mock flag confusion "in is_level_up_active". Code actually does: nothing calls it;
   `is_level_up_active` (L4446) delegates to `is_level_up_audit_active` without it. Stale + dead (C3).
5. `mvp_site/rewards_engine.py` (`detect_rewards_discrepancy` docstring framing) — "Report
   discrepancies without marking delivery" reads as report-only. Code actually does: mutate its
   input dict (creates `combat_state`/`encounter_state` {} when absent; pops
   `rewards_synthesized_for_total_xp`). Delivery-marking claim is true; report-only purity is not.
6. `mvp_site/campaign_upgrade.py:67` (`normalize_planning_block_choices` docstring) — "Normalize
   planning_block into a dict with list-format choices". Code actually does: also synthesize choice
   ids from lowercased text (`text.lower().replace(" ", "_")[:30]`) or `choice_{idx}`, and rename
   on collision (`original_id_1`). The id synthesis — the exact behavior the ADAPT deletes — is
   undisclosed in the docstring.
7. `mvp_site/god_mode_executor.py:247` (`_synchronize_replacement_xp_aliases` docstring) —
   "Mirror canonical XP into existing aliases and receipt those storage writes". Code actually
   does: also refresh display projections via `_refresh_replacement_xp_display` (L274) and return
   their paths. The display refresh — the exact behavior the DELETE removes — is undisclosed.
8. `mvp_site/adjusters/specs.py` module docstring — "forwarding all active specs" / "forwarding
   all active specs directly". Code actually does: forward 14 of 20 groups. False as written.
9. `mvp_site/adjusters/game/json_strip_prefix.py` (`override_strip_json_prefix` docstring) —
   "Strip all mode-prefixes before first '{' or '[' (array)". Code actually does: strip only when
   the remainder starts with "{" (`_strip_mode_prefixes` returns None otherwise); arrays are never
   stripped. The "(array)" clause is false (the intercept docstring's array exclusion is correct).
10. `mvp_site/docs/zfc_audit/SUMMARY.md` + `FULL_AUDIT.md` — 2026-05-01 snapshot; see zfc_audit
    section above. Stale in full, not just in details: the FastEmbed/intent_classifier compliance
    claim is superseded by the pilot + §6(4), and the 95% headline contradicts this group's own
    ADAPT/DELETE findings. DELETE (archive).
11. `mvp_site/backend_adjustment_specs.py` header graduation policy (90-day graduation, renewal
    with justification) vs 77 active MISSING-evidence specs from old PRs — process staleness, not
    a code-doc falsehood: the policy states a target the specs do not meet. Flagged for the owner
    in the specs section; no per-spec verdict change follows from it alone.
12. `mvp_site/level_up_amend_reapply.py:229` (`build_level_up_facts` docstring) — accurate that
    it only reads and writes no session record, but does not disclose the three-source fallback
    chain (delta → current state → model session) that the ADAPT collapses. Minor omission.

## (4) Challenges to run-2 verdicts (with evidence)

- **C1 — `level_up_session.TERMINAL_STATUSES`: KEEP → DELETE.** Whole-tree token + string search:
  zero code references. Run-2's justification ("several paths need to test terminality") has no
  referent in the tree. (Roadmap prose independently says to delete it.)
- **C2 — `rewards_engine.ASI_CHOICE_IDS`: grouped KEEP → DELETE (constant only).** Zero references
  in tree; the live ASI handling uses `LEVEL_UP_CHOICE_TYPES` and god-mode prefix strips, and
  `world_logic.py:3588` carries its own separate `_ASI_CHOICE_IDS`. The grouped row hid a dead constant.
- **C3 — `rewards_engine._coerce_flag_or_none`: grouped KEEP → DELETE.** Zero callers; docstring's
  claimed use site (`is_level_up_active`, L4446) never calls it.
- **C4 — `adjusters/base.py list_adjusters`: KEEP → DELETE.** Zero callers in tree incl. tests.
  Observability with no consumer. Caveat: an ops caller outside this tree would rescue it; none exists
  in the tree, and the deletion rule requires proof from the tree — which this is.
- **C5 — `backend_adjustment_specs.ACTIVE_REWARDS_DELIVERY_SUPPRESSION_SPECS` (tuple only):
  grouped KEEP → DELETE (tuple only).** Zero importers; not forwarded by `adjusters/specs.py`
  (14 groups only) nor imported by `backend_adjustment_registry.py`. Corrects run-2's registry note
  claiming it "lives in adjusters/specs.py instead" — it does not. Member specs
  (`rewards_delivery.tangible_award_gate`, `rewards_delivery.xp_delta_mismatch_guard`) keep KEEP.
- **C6 — `modal_conclude_policy.detect_conclude_signal`: KEEP → ADAPT.** Body verified: free-text
  path delegates to injected classifiers, and the live callables are `intent_classifier.*`
  (`agents.py:715-726`, `agents.py:4042-4055`) — the pilot-DELETE files. The guard cannot stay KEEP
  while wired to deleted code; rewire to Jev Noul flag + explicit confirmation per §6(4). Body
  otherwise unchanged (explicit-signal half stays KEEP).
- **C7 — `modal_conclude_policy.extract_modal_choice_id` / `_extract_from_prefixed_choice`:
  ADAPT widened.** Run-2 ADAPT covered stage 4b only. Bodies show two more verbatim-return paths
  (L78 prefixed fallback; L145-146 JSON fallback) that return unrecognized ids as if recognized.
  Current safety is entirely caller membership-checking (verified at `agents.py:3795`, `agents.py:3892`,
  and inside `detect_conclude_signal`). ADAPT: restrict all branches to `_KNOWN_MODAL_CHOICE_IDS`,
  returning None for unknown ids.
- **C8 — `adjusters/base.py register_allowed_specs`: KEEP → ADAPT (test-only move).** Only callers
  are tests; production module should not carry test-only extension points. Behavior-neutral, low priority.
- **Sharpenings that are NOT verdict changes:** (a) `campaign_divine` DELETE rewiring must cover
  `game_state_mixins.py` + `agents.py` + `world_logic.py` + `campaign_upgrade.py`, not just the lock;
  (b) `_synchronize_replacement_xp_aliases` ADAPT must explicitly remove the L274 `_refresh` call;
  (c) `canonicalize_rewards` ADAPT must remove its calls to DELETE functions
  (`_normalize_inconsistent_rewards_box_level_aliases`, `synthesize_rewards_box_from_state` in the
  admitted-event fallback) and resolve the saved-session `current_level = to_level` vs
  pcd_session_landed `current_level = from_level` inconsistency, and confirm registered-spec cover
  for core's `world_logic.inject_modal_finish_choice_if_needed` call; (d) run-2's "no symbol wholly
  unreferenced" claim is corrected by C1–C5 (it holds for everything else once intra-file use and
  Pydantic dispatch are counted); (e) run-2's registry subsetting note is corrected by C5.
- **Note N1 (not a challenge):** 77 active specs carry RUNTIME_EVIDENCE_MISSING. Run-2 verdicts rest
  on `allowed_when` text, which this review re-read per spec and confirms — but any future claim
  that "the registry proves" one of these transforms is necessary would be false, exactly as §4
  states (registry membership alone proves nothing).

## (5) Draft-amendment effects (DRAFT ONLY — not applied)

The draft ("FastEmbed or Jev count as models": model-call outputs are model-authored; server dispatch
on them is execution; hand-written thresholds/boosts/anchor lists layered on outputs still need an
exception) would change reasoning in exactly one place in this group and no verdicts:

1. `modal_conclude_policy.detect_conclude_signal` (C6): under the draft, delegating free-text exit
   judgment to a model call would be model-side dispatch, not server authorship — so the *reason*
   for touching this function would shift from "delegation is suspect" to "the callable is the deleted
   classifier". The ADAPT itself stands unchanged: the live callable is `intent_classifier.*`, which
   the pilot DELETEs in full, and §6(4) requires the Jev Noul + explicit-confirmation rewiring
   regardless of whether FastEmbed counts as a model. No verdict change.
2. No other verdict changes: stage 4b bare-token normalization is hand-written rewriting layered on
   input, not a model output — it still fails under the draft (draft consequence 1 says thresholds/
   boosts/anchor lists still need an exception). `saved_level_up_choice_id_for_text` text matching is
   server matching of player-submitted text to saved controls, not dispatch on a model-call output —
   unaffected. `_PREFIX_RE` prefix stripping is structural parsing of a declared literal prefix,
   not model-output interpretation — unaffected. All KEEP/ADAPT/DELETE verdicts above are therefore
   identical with or without the draft; only C6's rationale note would be reworded if the draft merges.

## (6) Coverage accounting

**Files reviewed (44, all in the assigned list, zero skipped):**
`mvp_site/god_mode_executor.py`, `god_mode_level_up.py`, `god_mode_schema.py`,
`god_mode_state_commands.py`, `level_up_amend_reapply.py`, `level_up_audit.py`,
`level_up_grant_contract.py`, `level_up_session.py`, `campaign_upgrade.py`,
`campaign_divine.py`, `campaign_template_dragon_knight.py`, `modal_conclude_policy.py`,
`conclude_invariant.py`, `backend_adjustment_registry.py`, `backend_adjustment_types.py`,
`rewards_engine.py`, `backend_adjustment_specs.py` (17 top-level);
`mvp_site/adjusters/README.md`, `adjusters/__init__.py`, `adjusters/base.py`,
`adjusters/registry.py`, `adjusters/specs.py`, `adjusters/types.py`,
`adjusters/game/__init__.py`, `adjusters/game/json_strip_prefix.py`,
`adjusters/schemas/__init__.py`, `adjusters/schemas/models.py`,
`adjusters/utils/__init__.py`, `adjusters/utils/redact.py`,
`adjusters/docs/00-zfc-origin.md`, `01-core-invariant.md`, `02-tenets.md`, `03-types.md`,
`04-engine.md`, `05-authoring.md`, `06-wire-in.md`, `07-redaction.md`, `08-testing.md`,
`09-lifecycle.md`, `10-checklist.md`,
`adjusters/evidence/ADJ-WA-JSON-STRIP-PREFIX/v1/proof.json`,
`adjusters/evidence/ADJ-WA-JSON-STRIP-PREFIX/v1/proof.sha256` (25 adjusters paths);
`mvp_site/docs/zfc_audit/FULL_AUDIT.md`, `mvp_site/docs/zfc_audit/SUMMARY.md` (2 docs).
**No file in the list was test-only** (no file skipped as test-only); the test-only *symbols* inside
prod files are listed in §2.
**Methods/specs reviewed (606 items):** 481 AST code symbols enumerated per file (465 top-level +
16 nested defs: `god_mode_executor` 1, `god_mode_level_up` 4, `god_mode_state_commands` 2,
`rewards_engine` 9) + 89 specs (each its own row above; `adjustment_id=` count verified = 89) +
20 unique grouping tuples (21 assignments; PR_8489 twice) + 14 doc files + 2 evidence files.
Enumeration method: `ast` parse of every Python file (module-level defs/classes/methods/constants/
annotated assignments + one level of nested defs), reconciled line-by-line against run-2's rows;
specs extracted by `adjustment_id=` scan and cross-checked against run-2's 89-row table (sets match);
tuples extracted by annotated-assignment scan (21 assignments, 20 unique names).
**Files/methods skipped: none.** Zero unexplained skips. Known method limits, stated not hidden:
(a) grouped rows name every symbol they cover (per the task's grouping rule); (b) `rewards_engine`
helper bodies outside the two reducers were judged on signature + docstring + targeted body reads
and caller evidence, while the two reducers themselves were read in full, every line; (c) doc files
were judged at file level with claim-by-claim checks, not per-paragraph rows, since prose docs have
no methods; (d) the `proof.json`/`proof.sha256` evidence files were judged as provenance data (the
engine's hash gate is the verifier), not parsed field-by-field; (e) caller evidence is a whole-tree
token index over `mvp_site/**/*.py` (prod vs tests) plus targeted grep — string/dynamic references
(e.g. `getattr`, importlib) were checked for the challenged symbols specifically and none was found
for C1–C5; a dynamic reference outside the tree would be the only rescue for C4, as stated there.
