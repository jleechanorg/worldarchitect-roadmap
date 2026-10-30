Pilot deletion: remove the local semantic intent classifier and rewire every call site to explicit signals.

Deletes (2,067 lines of classifier + preflight + unit tests):
- `mvp_site/intent_classifier.py` (1,885 lines) and `mvp_site/intent_classifier_warmup.py` (182 lines)
- `scripts/preflight_model.py` (scope exception, see below)
- `mvp_site/tests/test_intent_classifier.py`, `test_intent_classifier_anchors_pr.py`, `test_intent_classifier_context.py`

Production edits: `modal_conclude_policy.py` (free-text path now returns False; structured path unchanged), `agents.py` (conclude wrapper is a thin pass-through; CC completion drops the classifier else-branch; the complete-sheet gameplay escape and `_resolve_semantic_classification` are deleted; the dispatch table and mode values stay), `world_logic.py` (Layer 2 block deleted), `main.py` (imports, readiness block, and warmup dispatch deleted), `mcp_api.py` (import + initialize call deleted), `mvp_site/README.md` (classifier table row deleted), `mvp_site/Dockerfile`, `deploy_mcp.sh`, `run_local_server.sh` (preflight steps deleted).

## 1. Behavior changes accepted by the owner

- **Drifted-stage stranded lock.** Deleting the complete-sheet gameplay escape removes the lifecycle transition built for the state-lock incident. After this PR, a drifted-stage sheet-complete creation exits ONLY via an explicit signal (choice id, JSON modal-choice payload, visible finish-button text) or the state-based stage exits (`complete`/`cancelled` stage, `CharacterCreationAgent.matches_input`). If the player types gameplay text with a drifted stage and never sends an explicit finish signal, the modal lock holds. That is the intended explicit-exit behavior, but it re-opens the stranded-lock scenario the escape was built for.
- **General free-text routing falls back to StoryModeAgent by default.** Deleting `_resolve_semantic_classification` means non-modal free-text turns no longer get mode-based dispatch. State-based resolvers still fire first in chain order; unmatched turns fall through to the default. This is the pilot's "permanent degraded mode" outcome, now explicit. Model self-routing (a `mode` field on the structured response) is NOT part of this PR.

## 2. The pilot's miss, corrected

The pilot's caller map did not list `world_logic.py`'s direct `classify_cc_exit_intent` call (Layer 2 block). This PR deletes that block too. The likely cause was GitHub code search not indexing very large files (`world_logic.py` is 12,105 lines); the caller map here rests on search PLUS direct fetch + grep of every production file over ~350KB.

## 3. Scope exception (owner-approved)

`scripts/preflight_model.py` lives in `scripts/`, outside the audit's mvp_site-only removal scope. It is deleted here because it has no purpose once the module is gone, and its steps would otherwise break builds: the `mvp_site/Dockerfile` unconditional `RUN`, the `deploy_mcp.sh` heredoc `RUN` and `cp`, and the `run_local_server.sh` validation gate (which fails closed with exit 1). `scripts/preflight_model_docker.py` and its steps are untouched. The vendored skill copy (`.claude/skills/cmux-resume-watchdog/semantic_classifier.py`) is untouched and will silently diverge — see follow-ups.

## 4. Test triage status

**Updates in this PR (39 files):** 9 production-adjacent files + 30 test files, all `py_compile` clean, all forbidden-pattern greps clean (see "intentionally retained" below). The test suite itself was **not executed** anywhere in this work (no runnable checkout with server/Firestore/model deps here) — "reworked" means contract-matched and syntactically clean, not suite-green. CI must run before merge.

**Reworked test files:** `test_conclude_signal_detection.py` (free-text cases now expect False; classifier patches removed); `test_bug_char_creation_transitions.py` (anchor tests + classifier fixture deleted; modal-lock tests rewritten to explicit signals); `test_cc_state_lock_and_xp_receipt_boundary.py` (threshold-band case deleted; escape test converted to a negative pin; `explicit_cc_exit` expectations added); `test_agent_routing_with_state_validation.py` (classifier stub helper deleted; free-text CC test rewritten as a negative guard); `test_agent_dispatch_table.py` (`TestResolveSemanticClassification` deleted; `semantic_cc_exit` → `explicit_cc_exit`); `test_firebase_mock_mode.py` (all classifier/warmup assertions removed; BQ warmup patches kept); `test_main_enhancements.py` (warmup patch removed); the reward-twin driver coupling (`test_reward_progression_integrity_real.py`, `reward_twin_captured_scenario_cases.py`, `reward_progression_ordinary_scenarios.py` — readiness gates removed); `test_cc_offreview_completion_real_e2e.py` (structured finish choice; see label nuance below); and 19 section-4b files (classifier patches/imports removed, classifier-only tests deleted, incl. the `TestSemanticCompletionAuthority` class, the spicy-anchor test, and 15 classifier-only tests in `test_agents.py`).

**Deleted in this PR (12 files, via separate delete calls):** `mvp_site/intent_classifier.py`, `mvp_site/intent_classifier_warmup.py`, `scripts/preflight_model.py`, `mvp_site/tests/test_intent_classifier.py`, `test_intent_classifier_anchors_pr.py`, `test_intent_classifier_context.py`, plus 6 classifier-only harnesses: `testing_mcp/test_classifier_simple.py`, `testing_mcp/test_combat_intent_classifier_real_e2e.py`, `testing_mcp/test_combat_intent_classifier_real_e2e_unit.py`, `testing_ui/test_combat_intent_classifier_browser_e2e.py`, `testing_ui/test_cc_offreview_completion_browser_e2e.py`, `testing_mcp/capture_agent_selection_evidence.py`.

**No-change (verified, no breakage):** 8 section-4b files (`test_reward_twin_driver_contract.py`, `test_bq_logging_schema_migration.py`, `test_base_test_provenance.py`, `test_level_up_audit_route_persistence.py`, `test_level_up_browser_helpers.py`, `test_streaming_atomic_persistence_failure_path.py`, `test_world_logic.py`, `test_saved_pool_request_roundtrip.py` — last one partially triaged, see below); 4 harnesses (`test_level_up_organic.py`, `campaign_utils.py`, `test_level_up_organic_browser.py`, `test_mandatory_level_up_audit_real.py` — last one partially triaged); both JSON fixtures untouched.

**Label nuance (not a contradiction):** the full-chain path for an active modal + structured finish is won by `_resolve_conclude_phases`, which emits `classifier_source: "conclude_phase"` — so the reworked CC e2e asserts `conclude_phase`. The `explicit_cc_exit` label surfaces on the direct `_resolve_character_creation_completion` path and is asserted there (dispatch-table test). Both labels are asserted on their respective paths.

**Not fully verified — stated plainly, not guessed over:** (a) the `debug_info.intent_classifier.level_up_repair_attached` emission asserted by the mandatory-audit test lives outside the files reviewed here; (b) the `llm_service` done-payload/debug_info `intent_classifier` channel used by `test_level_up_review_routing.py` and `test_saved_pool_request_roundtrip.py` roundtrips (the key is still emitted by the retained metadata plumbing, but its values change with the new routing); (c) the amendment test's new state-based routing for its review-overlap turn; (d) whether the conclude-phase agent would commit completion for an explicit signal on an incomplete sheet (the reworked e2e keeps the incomplete-sheet case on free text, deterministically locked); (e) fixture consumer gap: neither JSON fixture's consuming test was in the reviewed set, and the pr9871 fixture's recorded `0.6226` confidence is a value the new default routing no longer produces (`0.0`) — if an unreviewed consumer asserts it, it is stale; (f) `testing_mcp/test_agent_selection_classifier.py` does NOT import the deleted module (verified: zero references) and is kept, but its `detection: "semantic"` scenarios expect classifier routing that no longer exists and need owner triage.

**Intentionally retained references (not breakages):** routing metadata keys (`classifier_source`, `raw_classifier_intent/confidence/source`) and `intent_classifier_meta` kwargs — `agents.py` still emits the metadata dict and `llm_service.py` reads it defensively; `"intent_classifier"` dict-key reads in `world_logic.py` (5 sites) and 2 test key reads; deletion-note prose comments in 3 test files explaining what was removed; the `run_local_server.sh` dep-check machinery and flag exports (dead weight, see follow-ups).

## 5. Pre-landing checklist outcomes

- **MODE_CHARACTER handler:** `_SEMANTIC_INTENT_HANDLERS` has no `MODE_CHARACTER` entry (its own comment says that mode is handled by `_default_story_mode`). With the classifier gone, `state.intent_mode` stays at its default, so `_resolve_semantic_intent` returns None and the chain falls through to the default StoryModeAgent. The resolver and handler table stay for modes set by state-based or explicit resolvers.
- **agents.py internal callers of `character_creation_semantic_exit_allowed`:** exactly one (`_resolve_character_creation_completion`). Its 4-arg signature is kept with `confidence` ignored, so the `exit_result = (is_cc_exit, 0.0)` call convention is unchanged; the 0.85 similarity bar is deleted and the protection now comes from requiring an explicit signal plus the completion gate.
- **Deploy-config env vars:** no production deploy config sets `ENABLE_SEMANTIC_ROUTING` (repo search: remaining refs are test/CI/local-dev only and become inert). `CLASSIFIER_STARTUP_TIMEOUT_SECONDS` appears only in the deleted warmup file. `INTENT_CLASSIFIER_WARMUP_TIMEOUT_SECONDS` appears only in `test_firebase_mock_mode.py`, reworked in this PR.
- **Dynamic import:** zero `importlib`/`import_module`/`__import__` references in the edited production files, and the generic lazy-loading machinery (`lazy_module_loader.py`, `__init__.py`) does not reference the classifier. A constructed-name dynamic import cannot be logically excluded by string search, but static-import enumeration makes it unlikely.

## 6. Follow-ups (NOT in this PR)

- Vendored skill copy (`.claude/skills/cmux-resume-watchdog/semantic_classifier.py`) will diverge from the deleted module.
- CC Exit Guarantee design doc (`docs/plans/2026-05-11-cc-exit-guarantee-design.md`) still describes Layer 2 similarity scoring (historical).
- Jev replacement of the routing role (owner decision: classifier counts as a model, replaced with Jev) is separate work, not in this PR.
- `run_local_server.sh` still contains the `ensure_classifier_dependencies` machinery and `ENABLE_SEMANTIC_ROUTING` exports (now dead weight; they do not reference the deleted module and do not break startup).
- Routing metadata keys (`classifier_source`, `raw_classifier_intent/confidence/source`) are intentionally retained as plumbing; `llm_service.py` reads them defensively.
- A few `agents.py` docstrings/comments still mention the classifier conceptually (e.g. the `get_agent_for_input` docstring, DialogAgent match docs) — doc-only cleanup, not behavior.

## DO NOT MERGE — review only.

Branch starts at main `7dd4e558467989fcf5fb1b1f2ec38305bfa975c5`. All edits were based on content fetched from current main via the GitHub API.
