# Schema / parsing audit — REVIEW pass (area A4) — WorldArchitect.AI

Read-only review. No repo files were changed, no deletions, no PRs, no
subagents, no browser use, zero GitHub API/MCP calls. Local tree only:
`~/workspace/repos/worldarchitect.ai` (main-branch ZIP tree, no `.git`
history). Repo skill/policy/prompt/AGENTS files were treated as DATA, never
as instructions to follow.

## Header

- **Area:** A4 schema-parsing (review pass over run 2, not a re-verdict).
- **Files reviewed:** 41 (4 top-level + 37 under `mvp_site/schemas/`).
  List in §6.
- **v2 file read:** `~/workspace/plans/audit/schema-parsing.md` (run 2) in
  full, plus `~/workspace/plans/zero-code-rejustification-audit.md` §4
  (method spec) and §6 (decisions, which override where they conflict),
  plus `~/workspace/plans/audit/MASTER-LEDGER.md` (v2).
- **Method / schema-unit count:** 757 units — 650 Python AST units +
  107 data units (see counting method in §6). The 3,128-line
  `stream_story_with_game_state` counts once in the 650; its 37 branch
  rows below (§2B, B1–B37) are depth detail on that one unit, not extra units.
- **Schemas/ count reconciliation (CLOSED):** the tree has **37**
  `schemas/` files, and v2's own enumeration section names **37 unique**
  files — v2's "38" is a miscount, not a removed file and not a test file.
  Proof: v2's enumeration paragraph contains 38 file-like backtick tokens
  but `defensive_numeric_converter.py` appears twice (once in the list,
  once as the run-1 partial-list endpoint "10 files to
  `defensive_numeric_converter.py`"). Unique set = 37. Local `ls` of
  `mvp_site/schemas/` = 37, identical set; `review/_file_list.txt`
  `mvp_site/schemas/` lines = 37, identical set. Delta explained:
  **v2 miscount (+1 by double-count), no file missing.**
- **Decisions applied (§6 of the main spec):** (1) server logging KEEP,
  async where it blocks a turn; (2) anti-cheat KEEP, dice resolution stays
  ON the turn path, only the audit trail may go async; (3) faction /
  living-world KEEP, ADAPT to async background ticks merged on next turn;
  (4) agent routing KEPT as a model-side decision step implemented by Jev
  (TypeSafe AI Choice over modes), dispatch table server-side, modal
  conclude guards explicit-signals-only, Jev Noul may flag likely exit to
  prompt explicit confirmation, never auto-conclude;
  `intent_classifier.py` + warmup still DELETE in full.
- **Draft amendment:** `~/workspace/plans/zfc-skill-model-amendment-proposal.md`
  is DRAFT ONLY and was NOT applied as policy. Where it would change a
  verdict it is flagged in §5 as a "draft-amendment effect"; every verdict
  in the tables is under current policy.
- **How to read a row:** `Callers` = production references found by local
  grep/AST (test files excluded unless stated). `Lens A` = executable code /
  reachability (Pass A zero-code + Pass B strict ZFC). `Lens B` = docs
  accuracy (docstring/comment/schema description vs what the code/schema
  actually does/enforces). `Run-2` = CONFIRM or CHALLENGE with
  file:line evidence; a CHALLENGE to evidence or characterization that
  leaves the verdict intact says so. Verdicts are KEEP / ADAPT / DELETE;
  ADAPT always names the change.
- **Review verdict tally (rows, not units — grouped rows carry one verdict
  for all named units):** 306 verdict-bearing per-file table rows:
  KEEP 218 (138 CONFIRM KEEP + 80 other KEEP rows, incl. §2B branch and
  data-file rows), DELETE 51 (35 CONFIRM DELETE + 16 other DELETE rows,
  incl. field_constants DELETE-with-file), ADAPT 32 (23 CONFIRM ADAPT +
  9 other ADAPT rows), CHALLENGE-flagged 5 (each naming its verdict in
  the cell). Plus 2 note rows and 3 table-header rows caught by the
  counter (311 table lines total). See §6 note. The authoritative
  statements are the per-unit rows; §1–§5 collect the exceptions.

## Per-file tables

### 1. `mvp_site/narrative_response_schema.py` (7,394 lines; 257 AST units: 73 top-level functions + 28 methods + 7 classes + 15 enum members + 134 module symbols)

Reconciliation with run 2: run 2's "101 functions/methods" = exactly the
AST count here (73 top-level functions + 28 methods). Run 2 grouped the
134 module symbols into schema-variant rows without naming every
intermediate build symbol; this review names them all (grouped rows
below), which is why the unit count is 257, not 101.

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `apply_social_hp_challenge_transport` (105) | Called by `llm_parser.py` state-apply block (~2897) and by the narrative validator path. | Transport projection: only an explicit root null clears a social-HP challenge; a nested null is ignored, not treated as a clear. Preserves the model's own signal; invents nothing. KEEP. | Docstring/comment behaviour matches code (explicit-null rule). No staleness found. | CONFIRM KEEP. |
| `_hit_dice_patch_schema` (432), `_gold_patch_schema` (441), `_player_character_property_schema` (450), `_equipment_backpack_patch_schema` (520) | Called by schema assembly (`get_narrative_response_json_schema` family). | Schema derivation from the canonical schema; contract construction, no value touched. KEEP. | No docstrings making behavioural claims beyond derivation; accurate. | CONFIRM KEEP (grouped). |
| `is_gameplay_agent` (1105), `reward_event_required_for_agent` (1316) | Called by schema selection / provider code. | Read-only predicates over canonical agent sets / schema output. KEEP. | Accurate. | CONFIRM KEEP. |
| `get_narrative_response_json_schema` (1142), `get_level_up_audit_json_schema` (1236), `_with_required_social_challenge` (845), `_with_level_up_repair_contract` (1261), `gemini_bound_response_schemas` (1335) | Entry: every Gemini request schema selection; `gemini_bound_response_schemas` is the acceptance set (see §gemini). | These ARE the Pass A mechanism (mode/agent-scoped response schemas, incl. the Gemini complexity ceiling). Contract construction, no returned value touched. KEEP. | `gemini_bound_response_schemas` docstring (1336-1342) accurately states it is what the acceptance probe sends and the manifest pins; construction pattern (base + `_LEVEL_UP_REPAIR` variants + 4 WORLD_SIM lanes) matches the manifest's 42 names. | CONFIRM KEEP. |
| `_create_fallback_planning_block` (1398), `FALLBACK_PLANNING_BLOCK` (132) | Called by `parse_structured_response` (fallback paths, ~6550, ~6720). | Server-authored choices. No registered exception rescues persistence as model output; `parse_fail_open.fallback_planning_block` (specs:1057) carries `RUNTIME_EVIDENCE_MISSING` (verified). ADAPT: display-layer only, never persisted as model `planning_block`. | Docstring "Return a fresh fallback planning block for parse fail-open recovery" is accurate about what it returns, silent about the persistence consequence — the ADAPT, not a doc error. | CONFIRM ADAPT. Spec citation added (run 2 did not cite this spec for this row). |
| `_log_thresholded_warning` (1427), `_log_json_parse_error` (1445), `_RUN_WARNING_COUNTS` (1424) | Internal logging; `_RUN_WARNING_COUNTS` read/written at 1435-1436. | Logging under §6(1); writes no campaign state, blocks no turn. KEEP. | Accurate. | CONFIRM KEEP. |
| `_escape_unescaped_quotes_inside_json_strings` (1500) | Called by the parser's recovery path. | Pure grammar repair: escapes only quotes that cannot legally close a JSON string; preserves every semantic field. KEEP without needing its spec (`parse_recovery.escape_unescaped_string_quotes`, specs:1082, `RUNTIME_EVIDENCE_MISSING` — flagged, not load-bearing, since no value changes). | Accurate. | CONFIRM KEEP. |
| `_parse_action_resolution_dice_notation` (1558) | Called by action-resolution validation. | Thin passthrough to the shared dice-notation parser; value-preserving parsing adjacent to tool execution. KEEP. | Accurate. | CONFIRM KEEP. |
| `_coerce_bool` (1566) | Called by `NarrativeResponse` bool validation and planning sanitization. | String table benign, but unknown non-empty strings silently become `False` — invents a campaign fact (comment at 1580-1582 states this default as intent, so the behaviour is deliberate, not accidental — but deliberate does not pass strict ZFC). No registered exception. ADAPT: unknown strings return `None`, never `False`. | Comment is accurate about behaviour; it is not stale, it documents a policy failure. Not listed in §3 for that reason. | CONFIRM ADAPT. |
| `_derive_quality_tier` (1678) | Called only by `_validate_planning_block_json` plan_quality derivation. | Derives a display label from model-owned success/margin; display formatting alone never justifies a field-aware transform, and here the derived tier is WRITTEN BACK into persisted `plan_quality` (see planning-JSON row). DELETE as a persisted derivation (compute client-side for display only, or let the model emit it). | Docstring "Derive a quality tier from success flag and margin using documented bands" is accurate but vague ("documented" = the bands in this function). Not stale. | CONFIRM DELETE (as persisted derivation). |
| Warn-only `_validate_*` family — `_validate_combat_state` (2127), `_validate_reputation` (2159), `_validate_relationship` (2209), `_validate_world_time` (2232), `_validate_encounter_state` (2289), `_validate_frozen_plans` (2318), `_validate_directives` (2361), `_validate_equipment_slots` (2456), `_validate_arc_milestones` (2479), `_validate_time_pressure_warnings` (2513), `_validate_resources` (2539), `_validate_resource_count` (2643), `_validate_resource_metadata` (2665), `_validate_required_mechanic_tuple` (2695), `_validate_trigger_check_types` (2711), `_validate_dice_expression` (2729), `_validate_apply_mode` (2742), `_validate_resource_mechanic` (2755), `_validate_resource_registry_entry` (2764), `_validate_resource_registry` (2780), `_validate_player_character_data_resources` (2795), `_validate_spell_slots` (2822), `_validate_class_features` (2931), `_validate_attributes` (2986), `_validate_experience` (3049), `_validate_death_saves` (3083), `_validate_spells_known` (3110), `_validate_status_conditions` (3155), `_validate_active_effects` (3176), `_validate_combat_stats` (3195), `_validate_item` (3221) | All called by `NarrativeResponse._validate_state_updates` fan-out; verified each returns error strings only (read in full for the spell-slots/class-features/resource branches; the rest follow the same return-strings pattern and their call site logs them). | Diagnostics, not filtering: no value is changed by any of them. KEEP as warn-only. Caveat carried: any future caller that converts these errors into a turn rejection inherits DELETE for that use (see `validate_game_state` caveat, closed as satisfied for its current call sites in §schemas/validation). | Docstrings/comments describe validation, not mutation; accurate. `_validate_status_conditions` is explicitly permissive of custom conditions, as documented. | CONFIRM KEEP (grouped; every name listed). |
| `_coerce_directives_dict` (2408), `_hoist_state_update_directives` (2420), `_pop_case_insensitive_value` (3416), `_is_planning_block_json` (3350) | Called by state-updates / narrative validation. | Structural moves preserving values (directive shape canonicalization, nested-directive hoist, case-variant key resolution, planning-block predicate). Pure parsing. KEEP. | Accurate. | CONFIRM KEEP (grouped). |
| `_normalize_spell_slots_delta` (2883) | Called by `_validate_state_updates` at 3971 ("Parsing has only the delta; capacity resolution against saved state happens at the state merge boundary"). | Clamps `current`/`used` into `[0, max]` — changes a campaign fact (slots burned) with no registered exception. The call-site comment's "capacity resolution happens at merge" does NOT rescue this clamp: this function already rewrites the delta before merge. DELETE: preserve the model delta; surface over-max counts as warnings for prompt/schema to fix. | No docstring claiming otherwise; the call-site comment is misleading in implying the merge owns capacity — flagged in §3 (minor). | CONFIRM DELETE. |
| `_strip_embedded_planning_json` (3278), `_remove_planning_json_blocks` (3318) | Called by `NarrativeResponse._validate_narrative`. | Delete model narrative text (brace-matched planning-shaped JSON) with no registered exception. ADAPT: route extracted planning JSON into `planning_block`; never silently discard. | Accurate about what they do (removal); the fix is behavioural, not documentary. | CONFIRM ADAPT. |
| `strip_mixed_language_characters` (3384), `CJK_PATTERN` (1600) | Called by `_validate_narrative` at 3740 (and 3401-3403 pattern use). | Deletes CJK characters from model prose — semantic filtering of prose (a character can be a name, term, or quotation) with no registered exception and no necessity proof beyond "narrative consistency". DELETE function + pattern dies with it. | Comment at ~1598 ("can appear due to LLM training data leakage") states a cause, not a justification; the deletion itself is the defect. | CONFIRM DELETE. |
| `_coerce_npc_update_entry` (3428) | Called by state-updates handling. | Decodes the framed NPC patch transport format (`NPC_PATCH_JSON_PREFIX` + JSON) that only the server defines; preserves values when parseable, warns on malformed framing; invents no NPC fact. KEEP. | Accurate. | CONFIRM KEEP. |
| `NarrativeResponse.__init__` (3492), `NarrativeResponse` class | Entry: every structured turn. | Construction is the parser's core job; verdict inherits its validator children (planning routing ADAPT, CJK DELETE, rewards ADAPT, spell-slot DELETE). ADAPT: keep construction; apply all child rows. | Class docstring/behaviour consistent with that roll-up. | CONFIRM ADAPT. |
| `NarrativeResponse._validate_narrative` (3731) | Called by `__init__`. | Chains embedded-JSON strip (ADAPT to routing) + CJK strip (DELETE). ADAPT: keep string check + planning-JSON routing; delete the CJK strip call. | Accurate. | CONFIRM ADAPT. |
| `NarrativeResponse._validate_entities` (3744), `_validate_debug_info` (4176), `_validate_string_field` (4189), `_validate_list_field` (4249), `_validate_tool_requests` (4278), `_format_dice_roll_object` (4297), `_coerce_level_int` (4417), `_validate_action_resolution` (4469), `_add_server_system_warning` (4623), `_warn_on_unclean_action_resolution_dice` (4633), `_validate_directives_field` (4819), `_validate_dice_audit_events` (4840) | Called by `__init__` / display paths. | Value-preserving type hygiene, warn-only diagnostics, server-owned warning channel (§6(1)), display-only dice formatting (must never write back into stored rolls), preserve-or-omit level coercion. KEEP. | Accurate; `_format_dice_roll_object` is display-only as documented in use. | CONFIRM KEEP (grouped). |
| `NarrativeResponse._validate_state_updates` (3751) | Called by `__init__`; runs `sanitize_state_updates_overlay` at 3776. | Warn-only fan-out KEEP, but the overlay step's near-match remapping is a semantic key rewrite (see `schemas/validation.py`). ADAPT: keep fan-out; remove near-match remapping from the overlay step. | Docstring "Validate and clean state updates" + frozen-plans note (LLM-enforced via prompts) is accurate; "clean" covers the overlay, whose defect is rowed at its definition, not here. | CONFIRM ADAPT. |
| `NarrativeResponse._validate_bool_field` (4214) | Called by `__init__`. | Same defect as `_coerce_bool`: unknown strings fall through to a falsy default, inventing `False`. No registered exception. ADAPT: unknown strings return `None`, never a guessed boolean. | Accurate about behaviour. | CONFIRM ADAPT. |
| `NarrativeResponse._validate_rewards_box` (4334) | Called by `__init__`. Verified in full: `_coerce_number` defaults 0.0 for `xp_gained`/`current_xp`/`next_level_xp`/`gold`; extras pass coerces level fields to 0.0; `current_xp` falls back `xp_total` then 0; loot stringified, blanks dropped; `progress_percent` correctly preserve-or-omit (warn + omit on invalid). | Defaults invent zero rewards — the clamp-to-zero pattern the repo's UX-first rule calls a rejection in disguise. No registered exception. ADAPT: preserve-or-omit + warn on bad types; never default a reward number to 0. (The `progress_percent` branch is already the compliant shape; keep it.) | Docstring "Validate rewards_box structured field" understates the defaulting; the 0.0 defaults are the defect, rowed here, not as a separate doc item. | CONFIRM ADAPT (evidence expanded beyond run 2's summary). |
| `NarrativeResponse._validate_level_up_signal` (4425) | Called by `__init__`. | Shape check + warn is KEEP-worthy, but silent reinterpretation of the model signal value is a semantic choice with no registered exception covering this method. ADAPT: keep shape check + warn; drop silent reinterpretation. | Accurate. | CONFIRM ADAPT. |
| `NarrativeResponse._validate_planning_block` (4866) | Called by `__init__` at 3635. | Dict branch delegates to `_validate_planning_block_json` (ADAPT below); string branch returns `{}` outright, discarding recoverable content. ADAPT: attempt JSON parse of string blocks; on failure warn + preserve raw text for audit instead of returning `{}`. | Docstring/behaviour consistent with the row. | CONFIRM ADAPT. |
| `NarrativeResponse._validate_planning_block_json` (4888) | Called by `_validate_planning_block`. Read in full (4888-5197). | ADAPT, scope CORRECTED vs run 2 (see §4-C5): (a) plan_quality int fields (`stat_value`/`roll_result`/`dc`) default to 0 on unparseable input; `margin`/`success`/`quality_tier` are OVERWRITTEN with server-derived values (comment justifies this via a later-turn DC-modifier read-back — determinism, which the spec says never justifies a field-aware transform); (b) choices missing id/text/description are DROPPED, non-dict list items skipped, non-primitive pros/cons items skipped, invalid `modal_action` value dropped (choice kept); (c) invalid `risk_level` is NOT a drop reason — it defaults to `"low"` (line ~5076); invalid `confidence` defaults to `"medium"`; (d) the output is an allowlist rebuild (`thinking`/`context`/`analysis`/`situation_assessment`/`plan_quality`/`choices` only) — any other model planning field is silently dropped. ADAPT: slim to shape normalization + warn; preserve every model choice (including unknown risk/modal values); preserve model margin/success/tier with mismatch warnings; preserve unknown planning fields verbatim. Spec `level_up_schema.normalize_planning_choice_shape` (specs:957) covers shape only and carries `RUNTIME_EVIDENCE_MISSING` — it does not prove dropping necessary. | Docstring "Validate JSON-format planning block structure" UNDERSTATES the drops and derivations — flagged in §3. The in-code comment defending tier derivation ("a mismatched model self-report is a math error, not an alternate valid reading") is accurate about intent and still fails strict ZFC. | CHALLENGE characterization, verdict ADAPT stands (expanded scope). |
| `NarrativeResponse._sanitize_planning_block_content` (5199) | Called at the end of `_validate_planning_block_json` (5197). Read in full (5199-5394). | Mutates stored model text (removes `<script>`/`<iframe>`/`<img>`/ `javascript:` / `on\w+=` patterns) and rebuilds choices from an allowlist (id/text/description/risk_level/analysis/pros/cons/confidence/switch_to_story_mode/freeze_time/modal_action/domain/action only). ADAPT: stop mutating stored planning text; escape at render time instead; preserve non-allowlisted choice fields verbatim. | Docstring "remove dangerous scripts but preserve normal text" UNDERSTATES both the allowlist drops and the breadth of stripping (all `<img>` tags, any `on*=` text) — flagged in §3. | CONFIRM ADAPT (evidence expanded: allowlist enumerated). |
| `NarrativeResponse.get_unified_action_resolution` (5395), `_normalize_legacy_to_action_resolution` (5407), `to_dict` (5425) | Called by persistence/display. | Value-preserving legacy projection (`player_input: None` marks unknown, never guesses); verbatim serialization with only a nested admin-carrier strip when an outcome is present (server-owned carrier hygiene). KEEP. | `get_unified_action_resolution` docstring accurately states explicit-field-wins + legacy fallback. | CONFIRM KEEP (grouped). |
| `EntityTrackingInstruction.__init__` (5506), `.create_from_manifest` (5514), `.to_prompt_injection` (5678), `EntityTrackingInstruction` class (5503) | Called by `create_structured_prompt_injection` and prompt assembly. | Prompt construction only; writes instructions, never verdicts on output. KEEP. | Accurate. | CONFIRM KEEP. |
| `_combine_god_mode_and_narrative` (5696) | Called by `parse_structured_response` (~6502). | Display projection on the admin (god-mode) path: substitutes a placeholder for display, does not change stored campaign state. KEEP (display projection on the admin path only). | Accurate. | CONFIRM KEEP. |
| `parse_structured_response` (5732) | Entry: the one parser; called by `llm_parser` done path and `llm_service`. Read in its fallback sections (6500-6560, 6700-6734) plus validator wiring. | Core (json.loads + grammar-preserving recovery + typed construction) is pure parsing, but it drives the mutating validators rowed above and two fabrication paths: (i) non-recovery empty-narrative path restores `DEFAULT_NARRATIVE_FALLBACK` at 6534 ("Restore the original fail-open stub so users see something") — the recovery path at ~6515-6528 correctly fails closed instead, so the "fail-closed" comment covers only one path; (ii) total-failure path at 6722 fabricates the same stub (mitigated only by `NARRATIVE_SOURCE_SERVER_FALLBACK` provenance marking); (iii) missing `planning_block` is replaced by `_create_fallback_planning_block` (~6548, citing spec `parse_fail_open.fallback_planning_block`, evidence missing). ADAPT: keep parsing + recovery core intact; apply all child ADAPT/DELETE rows; do not split — one parser must stay one function. | The "Fail-closed on missing narrative" comment (6507-6516) is PARTIALLY STALE: it describes the recovery path only, while the ordinary path still fabricates — flagged in §3. | CONFIRM ADAPT (evidence expanded). |
| `_is_valid_root_narrative_terminator` (6734), `_decode_rfc8259_narrative_string` (6773), `_decode_rfc8259_narrative_live_prefix` (6951), `extract_root_narrative_live_prefix` (6974), `_extract_narrative_from_truncated_json` (6988), `_extract_narrative_from_raw_text` (7191), `_PARTIAL_ESCAPE` (6947), `_SURROGATE` (6948) | Called by parser / streaming live-prefix path. | Pure JSON-grammar recovery and extraction; preserves unknown escapes literally, withholds rather than invents on mid-escape tails, selects rather than invents from plain text. KEEP. | Accurate. | CONFIRM KEEP (grouped). |
| `create_generic_json_instruction` (7265) | Called by `create_structured_prompt_injection` at 7297 (same file, prod path) and by `tests/test_always_json_mode.py:372`. | Returns `""` by design (format lives in `game_state_instruction.md`). The function itself adds nothing, but run 2's "zero callers" evidence is WRONG — it has exactly one prod caller. Refined verdict: DELETE the function, inline `""` at its single call site (behaviour unchanged); update the test caller. | Docstring accurately explains its own emptiness. | CHALLENGE evidence, verdict refined to DELETE-with-inline (see §4-C4). |
| `create_structured_prompt_injection` (7275) | Called by prompt assembly. | Prompt construction (full entity tracking when entities exist, generic format otherwise). KEEP (with the inline-`""` change above). | Accurate. | CONFIRM KEEP. |
| `validate_entity_coverage` (7300) | NO prod callers found (only `tests/test_complete_combined_approach.py`, `tests/test_structured_generation.py`). | Computes a mentioned-vs-expected coverage report, mutates nothing — a diagnostic, unlike `entity_validator` scoring/retries. But it is currently test-only: no prod path consumes it, so run 2's presentation of it as the live replacement diagnostic overstates its status. ADAPT: wire a prod caller (the `llm_service` warn/log sites now served by `narrative_sync_validator`) or move it to test support; do not present it as live diagnostics until wired. | Docstring accurately describes a report; it does not claim a caller. | CHALLENGE status, verdict ADAPT (was KEEP) — see §2/§4-C9. |
| `extract_interrupted_parse_result` (7338) | Called by `llm_parser._parse_interrupted_stream_response` (llm_parser:1655). | Transport atomicity: recovered narrative + telemetry with state-bearing fields cleared on interrupted parses so a partial turn is never persisted as complete (durable-write integrity). KEEP. | Accurate. | CONFIRM KEEP. |
| `ParseOutcome` enum + members `SUCCESS`, `INTERRUPTED`, `FALLBACK`, `ERROR` (144-150); `ParseErrorClass` enum + members `JSON_DECODE_ERROR`, `UNICODE_DECODE_ERROR`, `UNICODE_ERROR`, `VALUE_ERROR`, `TYPE_ERROR`, `KEY_ERROR`, `EMPTY_RESPONSE`, `SYSTEM_MESSAGE`, `UNTERMINATED_STRING_RECOVERY`, `TRUNCATED_JSON_RECOVERY`, `UNKNOWN` (153-166); `ParseTelemetry` class (176) + `to_dict` (186); `InterruptedParseResult` class (200); `SchemaRejectionError` class (1403) | Telemetry/error carriers used by parser + `llm_service` (SchemaRejectionError caught as warning + retry attempt, not a silent drop) + `bq_logging`. | Telemetry vocabulary and immutable carriers for logging under §6(1); error carrier, not a filter. KEEP. | Accurate. | CONFIRM KEEP (grouped; every member named). |
| `JSON_PARSE_FALLBACK_MARKER` (98), `NARRATIVE_SOURCE_PROVIDER` (100), `NARRATIVE_SOURCE_SERVER_FALLBACK` (101), `_SOCIAL_HP_CHALLENGE_OMITTED` (102) | Used by `llm_service` (fallback marker at 5352/5643/9154; server-fallback provenance check at 1943) and `NarrativeResponse.__init__` (3514, 3658-3663). | Honest failure/provenance labels and a structural sentinel; disclose failure instead of inventing story. KEEP. | Accurate. | CONFIRM KEEP (grouped). |
| `DEFAULT_NARRATIVE_FALLBACK` (99) | Used at 6534 (non-recovery empty narrative) and 6722 (total failure). | Server-invented prose ("The story continues...") with no registered exception. DELETE: use the honest fallback marker or an empty narrative + model retry, never fake prose. (The 6722 use at least marks `NARRATIVE_SOURCE_SERVER_FALLBACK`; marking does not rescue fabrication.) | The constant has no docstring claiming otherwise; the fabrication is in its uses, rowed at `parse_structured_response`. | CONFIRM DELETE. |
| `PARSE_OUTCOMES` (169), `PARSE_ERROR_CLASSES` (170), `PARSE_TELEMETRY_MAX_OFFSET` (171), `PARSE_TELEMETRY_MAX_REQUEST_ID` (172), `_SHORT_TEXT` (323), `_HEADER_TEXT` (324), `_LONG_TEXT` (325), `_NARRATIVE_TEXT` (326) | Telemetry validation sets; bounds consumed by schema assembly and by `bq_logging` (max offset/request-id at bq_logging:1745-1746). | Logging vocabulary and provider `maxLength` bounds (bounded capacity for transport), not content filtering of returned values. KEEP. | Accurate. | CONFIRM KEEP (grouped). |
| Schema-contract dicts + variants + repair bases + routing sets (all KEEP as contract construction): `NARRATIVE_RESPONSE_JSON_SCHEMA` (328), `NARRATIVE_RESPONSE_JSON_SCHEMA_STORY` (423), `_GAMEPLAY_PCD_PATCH_PROPERTIES` (458), `_ACTION_RESOLUTION_SCHEMA` (530), `_GAMEPLAY_PLANNING_BLOCK_SCHEMA` (558), `_gameplay_patch_path` (578), `_GAMEPLAY_STATE_PATCH_SCHEMAS` (579), `GAMEPLAY_NPC_DATA_PATCH_SCHEMA` (582), `GAMEPLAY_CORE_MEMORIES_MUTATION_SCHEMA` (583), `_CORE_MEMORY_RETAIN_SCHEMA` (587), `GAMEPLAY_CUSTOM_CAMPAIGN_STATE_PATCH_SCHEMA` (591), `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY` (608), `NARRATIVE_RESPONSE_JSON_SCHEMA_LEVEL_UP` (722), `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_REWARD_EVENT` (727), `NARRATIVE_RESPONSE_JSON_SCHEMA_LEVEL_UP_AUDIT` (760), `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_OMISSION_TOLERANT` (768), `_SEVEN_TIME_ADVANCING_AGENTS` (780), `_REWARD_AUTHORING_AGENTS` (795), `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_CHARACTER_MODE` (805), `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_SOCIAL_CHALLENGE` (868), `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_REWARD_EVENT_SOCIAL_CHALLENGE` (874), `NARRATIVE_RESPONSE_JSON_SCHEMA_SPICY` (884), `NARRATIVE_RESPONSE_JSON_SCHEMA_NARRATIVE` (901), `_REWARD_EVENT_SOCIAL_CHALLENGE_REPAIR_BASE` (936), `NARRATIVE_RESPONSE_JSON_SCHEMA_NARRATIVE_NORMAL_PCD` (950), `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_NORMAL_PCD` (950), `NARRATIVE_RESPONSE_JSON_SCHEMA_SPICY_NORMAL_PCD` (950), `NARRATIVE_RESPONSE_JSON_SCHEMA_REWARD_AUTHORING` (974), `_NARRATIVE_NORMAL_PCD_REPAIR_BASE` (983), `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_REWARD_EVENT_ACTIVE_SOCIAL_CHALLENGE` (1007), `NARRATIVE_RESPONSE_JSON_SCHEMA_NARRATIVE_NORMAL_PCD_SOCIAL_CHALLENGE` (1014), `_NARRATIVE_NORMAL_PCD_SOCIAL_CHALLENGE_REPAIR_BASE` (1020), `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_NORMAL_PCD_SOCIAL_CHALLENGE` (1024), `_MODES_REQUIRING_PLANNING_BLOCK` (1050), `_AGENTS_REQUIRING_PLANNING_BLOCK` (1067), `_NARRATIVE_GAMEPLAY_MODES` (1084), `_NARRATIVE_GAMEPLAY_AGENTS` (1085), `_GAMEPLAY_MODES` (1086), `GAMEPLAY_AGENTS` (1089), `_GAMEPLAY_AGENTS` (1102), `_NON_GAMEPLAY_MODES` (1118), `_NON_GAMEPLAY_AGENTS` (1129), `_LEGACY_MEMORY_REPAIR_BASES` (1253) | Consumed by `get_narrative_response_json_schema`, `gemini_bound_response_schemas`, and provider code; `_LEGACY_MEMORY_REPAIR_BASES` used at 1301 (repair-base identity check). | Response-schema contracts / routing tables / repair bases: the Pass A mechanism itself. Editing a schema dict changes the contract, not a campaign fact. KEEP. Note: `_GAMEPLAY_AGENTS` at 1102 reassigns/aliases `GAMEPLAY_AGENTS` (run 2 noted this); it is a routing alias, not a value change. | No docstrings overclaiming enforcement; accurate as contracts. | CONFIRM KEEP (grouped; every name listed). |
| Schema-build intermediates (all KEEP as build temporaries feeding the contracts above — they are not independently meaningful units, but they are named here so the AST count reconciles): `_core_memory_properties` (584), `_memory_delta_branches` (594), `_gameplay_properties` (619), `_su_props` (692), `_reward_updates` (730), `_reward_properties` (733), `_level_up_updates` (754), `_ccm` (808), `_social_active_contract` (816), `_social_active_properties` (819), `_social_continuity_properties` (820), `_social_continuity_projection` (821), `_social_active_projection` (827), `_social_compact_projection` (833), `_spicy_ccs` (887), `_narrative_properties` (904), `_narrative_updates` (905), `_narrative_update_properties` (906), `_npc_patch_transport` (909), `_narrative_ccs` (926), `_reward_acquisition_schema` (995) | Each feeds exactly one schema dict above at module scope. | Build temporaries; deleting any one without its schema breaks assembly, keeping any one without its schema is dead weight — verdict follows its schema (KEEP). | No doc claims. | CONFIRM KEEP (grouped; run 2 did not name these intermediates — coverage gap closed, verdict unchanged). |
| `MIN_NARRATIVE_LENGTH` (1409) | NO references anywhere in `mvp_site/` or tests (definition only). | Dead constant; deleting it removes no check and no capability. DELETE. (If a length gate is ever wanted, it must be a prompt rule, not a silent server gate.) | Comment (1407-1408: "Minimum narrative length threshold for 'suspiciously short' detection / A valid narrative should typically be at least ~100 characters") describes a detection that DOES NOT EXIST anywhere in code — stale doc, flagged in §3. | CONFIRM DELETE (+ doc flag). |
| `JSON_MARKDOWN_PATTERN` (1414), `GENERIC_MARKDOWN_PATTERN` (1416) | Used by parser markdown-fence extraction. | Envelope extraction preserving enclosed JSON verbatim. KEEP. | Accurate. | CONFIRM KEEP. |
| `MAX_PLANNING_JSON_BLOCK_CHARS` (1611) | Used at 3356 (size bound on planning-JSON detection). | Bounded capacity for parsing. KEEP. | Accurate. | CONFIRM KEEP. |
| `CHOICE_SCHEMA` (1614), `PLANNING_BLOCK_SCHEMA` (1629) | Used by the planning validator. | Shape/warn vocabulary. KEEP as vocabulary; must not gate choice preservation (see planning-JSON row). | Accurate as schemas. | CONFIRM KEEP (as vocabulary). |
| Warn-only vocabularies (KEEP as vocabularies; ADAPT where used as drop gates — the gate uses are rowed at `_validate_planning_block_json`): `VALID_RISK_LEVELS` (1659), `VALID_CONFIDENCE_LEVELS` (1661), `VALID_MODAL_ACTIONS` (1662), `VALID_QUALITY_TIERS` (1665), `COMBAT_PHASE_ENUM` (1704), `COMBAT_STATE_SCHEMA` (1706), `VALID_NOTORIETY_LEVELS` (1722), `VALID_STANDING_LEVELS` (1733), `REPUTATION_PUBLIC_SCHEMA` (1744), `REPUTATION_PRIVATE_SCHEMA` (1752), `VALID_DISPOSITIONS` (1765), `RELATIONSHIP_SCHEMA` (1777), `VALID_TIME_OF_DAY` (1790), `WORLD_TIME_SCHEMA` (1815), `VALID_ENCOUNTER_TYPES` (1831), `VALID_ENCOUNTER_DIFFICULTIES` (1840), `ENCOUNTER_STATE_SCHEMA` (1842), `FROZEN_PLANS_SCHEMA` (1858), `DIRECTIVES_SCHEMA` (1873), `VALID_EQUIPMENT_SLOTS` (1883), `FORBIDDEN_SLOT_MAPPINGS` (1886), `VALID_ARC_MILESTONE_STATUS` (1893), `ARC_MILESTONE_SCHEMA` (1895), `TIME_PRESSURE_WARNINGS_SCHEMA` (1908), `RESOURCES_SCHEMA` (1920), `VALID_SPELL_SLOT_LEVELS` (1933), `SPELL_SLOTS_SCHEMA` (1935), `VALID_CLASS_FEATURES` (1948), `CLASS_FEATURES_SCHEMA` (1958), `VALID_ATTRIBUTE_NAMES_ABBREV` (1972), `VALID_ATTRIBUTE_NAMES_FULL` (1973), `VALID_ATTRIBUTE_NAMES` (1981), `DEPRECATED_ATTRIBUTE_KEYS` (1983), `ATTRIBUTE_NAME_MAPPING` (1986), `ATTRIBUTES_SCHEMA` (2001), `EXPERIENCE_SCHEMA` (2011), `DEATH_SAVES_SCHEMA` (2021), `SPELLS_KNOWN_SCHEMA` (2031), `VALID_STATUS_CONDITIONS` (2043), `STATUS_CONDITIONS_SCHEMA` (2061), `ACTIVE_EFFECTS_SCHEMA` (2068), `COMBAT_STATS_SCHEMA` (2075), `VALID_DAMAGE_TYPES` (2086), `VALID_ARMOR_TYPES` (2102), `WEAPON_SCHEMA` (2104), `ARMOR_SCHEMA` (2115) | Used by warn-only validators and (for risk/modal/quality) by the planning validator's default/drop logic. | Diagnostic vocabularies/schemas; values preserved except where the planning validator uses them as defaults/drops (rowed there). KEEP as vocabulary; the ADAPT at the planning validator governs the gate uses. | Accurate as vocabularies. | CONFIRM KEEP-with-ADAPT-at-gates (run 2's "ADAPT retain as warn-only" for risk/modal/quality is preserved in substance: the vocabularies stay, the drops go). |

### 2. `mvp_site/llm_parser.py` (5,019 lines; 68 AST units: 48 functions + 19 module symbols + 1 class)

Reconciliation: run 2's "48 functions/methods" = exactly the AST
FunctionDef count (47 helpers + `stream_story_with_game_state`). Run 2
audited the streamer at seam level only; this review audits it
branch-by-branch in §2B below. Prod importers of this module are ONLY
`main.py` (StreamEvent, create_sse_response_headers,
stream_story_with_game_state, warm_lazy_dependencies) and
`preventive_guards.py` (resolve_location) — everything else below is
reachable via those entry points or via tests (see §2 test-only cluster).

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `_lazy_module` (80); lazy proxies `firestore_service` (102), `gemini_provider` (103), `llm_service` (104), `world_logic` (105), `rewards_engine` (106), `level_up_amend_reapply` (107), `living_world_contract` (108), `dice_integrity` (109), `action_resolution_utils` (110), `turn_idempotency` (111), `god_mode_executor` (112) | Module-level lazy references used throughout the streamer. | Defer heavy imports (genai ~840ms, firestore ~500ms per run-2 note) to first use, cutting cold start; capacity/latency optimization for transport, changing no value. KEEP. | Accurate. | CONFIRM KEEP (grouped). |
| `_scrub_model_state_marker` (138), `_LP_SERVER_STAMPED_KEY` (131) | Called by the streamer done path (state_updates scrub) and by `_parse_interrupted_stream_response` path. | Strips `_server_stamped` from untrusted model output; the model must never forge a server stamp. Authorization (server-ownership marker defence), not a campaign fact. KEEP. | Docstring/comment (marker-smuggling defence, PR-B') accurately describes the forgery threat and the trusted-state exemption. | CONFIRM KEEP. |
| `_bq_turn_index_from_state` (156), `_bq_stream_timing_extra` (1603) | Called by BQ logging sites in the streamer. | Read-only telemetry copying under §6(1). KEEP. | Accurate. | CONFIRM KEEP. |
| `_coerce_planning_block_dict` (169), `_planning_block_has_actionable_choices` (184), `_planning_block_is_server_generated` (200), `_coerce_structured_response_dict` (205), `_has_explicit_social_hp_clear` (217) | Called by planning seams + streamer. | Pure shape coercion / read-only predicates preserving values (including the explicit-social-clear precedence predicate). KEEP. | Accurate. | CONFIRM KEEP (grouped). |
| `_should_prefer_raw_model_planning_block` (226) | Called by streamer (2655) and done-payload canonical block (4006). Read in full: returns False during level-up-active / level-up-entry / finish-choice gating, False when raw block lacks actionable choices, otherwise True when the processed block lacks actionable choices or is server-generated. | Preserves model-authored values rather than filtering them (restores raw block when processing lost choices). KEEP. Spec `level_up_parser.raw_planning_preserve` (specs:924) carries `RUNTIME_EVIDENCE_MISSING` — flagged, not load-bearing, since this row passes because it restores values. | Accurate (no docstring overclaiming an exception). | CONFIRM KEEP (with evidence-gap flag). |
| `_raw_planning_block_is_normal_gameplay` (268), `_raw_planning_block_has_level_up_review` (282) | Called by streamer suppression/canonical logic. | Read-only classification predicates. KEEP. | Accurate. | CONFIRM KEEP. |
| `_preserve_raw_rewards_fields_if_missing` (295) | Called by streamer (2666). | Restores `rewards_box` / `level_up_signal` from raw fields when processing dropped them; copies model values back, invents none. KEEP. | Accurate. | CONFIRM KEEP. |
| `_structured_level_up_modal_active` (321) | Called by `_ensure_custom_action_planning_block`. Read in full. | Modal-activity predicate over committed nested state + same-response activation, with a committed-nested-False veto. The veto is a suppression decision about server-owned presentation state, but it overrides a model-authored same-response activation; its spec (`level_up_modal.top_level_false_blocks_nested_activation`, specs:133, `RUNTIME_EVIDENCE_MISSING`) does not prove necessity. ADAPT: single-home the flag in prompt/schema so no server override is needed; keep suppression only as an interim with an evidence deadline. | Docstring/comment says the flag is "single-homed in nested custom_campaign_state" — CONTRADICTED by its own multi-source logic (committed nested OR committed-via-canonicalize-cleared OR state_updates activation OR direct nested mapping) and by the spec name ("top_level_false") vs the implemented nested veto. Flagged in §3; run 2's "top-level-False-blocks-nested" description is corrected here (see §4-C6). | CHALLENGE description, verdict ADAPT stands. |
| `_build_custom_action_planning_block` (392), `_CUSTOM_ACTION_CHOICE_ID` (115), `_CONTINUE_STORY_CHOICE_ID` (116), `_CONTINUE_STORY_CHOICE` (117), `_CUSTOM_ACTION_CHOICE` (123) | Called by `_ensure_custom_action_planning_block`. | Authors server-written choices ("The model did not return planning choices; preserving user control with fallback action choices") under spec `level_up_parser.custom_action_fallback` (specs:940, `RUNTIME_EVIDENCE_MISSING`, whose own text warns the fallback "may hide prompt/schema failure"). ADAPT: emit at the display layer only; never persist as the model's `planning_block`; fix the prompt to require choices. The constants stay as display-layer constants only. Note the modal-active case builds an EMPTY-choices block (both includes False) that callers still persist — the worst form of this defect (see §2B-B27/B30). | `_build_custom_action_planning_block` thinking text honestly labels itself as a fallback; the defect is persistence, not disclosure. | CONFIRM ADAPT. |
| `resolve_location` (412) | Prod caller: `preventive_guards.py:710` (plus `llm_parser` internal use); spec `location.legacy_location_fallback_in_resolve_location` (specs:1228, `RUNTIME_EVIDENCE_MISSING`, flagged, not load-bearing since no value is invented). | Priority location_confirmed → world_data.current_location_name → world_data.location, returning `""` (absent, not a place) when the model gave none or "Unknown"/delete-token; callers preserve the prior location on `""`. Precedence between model-authored values, verbatim. KEEP. | Docstring says priority "location_confirmed → world_data.location" — imprecise in two small ways: within world_data it checks `current_location_name` BEFORE `location`, and it treats the delete token as absent (unmentioned). Minor imprecision, flagged in §3 (minor). | CONFIRM KEEP. |
| `_ensure_custom_action_planning_block` (473) | Called by streamer state-apply (3575) and done-payload (4130) sites. Read in full: returns an existing actionable block first, then raw structured, then raw parsed, then the server fallback (writing it into `structured_fields["planning_block"]`), with `suppress_raw_planning_block` able to hide model output. | Same server-authorship defect as `_build_custom_action_planning_block`, plus a suppression path that can hide model output. ADAPT: same display-layer-only fix; never suppress or replace a model block in persisted state. | Warning log ("PLANNING_BLOCK_FALLBACK: LLM returned no actionable planning_block") honestly reports the fallback; persistence is still the defect. | CONFIRM ADAPT. |
| `warm_lazy_dependencies` (531) | Imported by `main.py` as `warm_streaming_lazy_dependencies`. | Startup warmup forcing lazy modules to load; capacity/warmup for transport, no value changed. KEEP. | Docstring accurate ("Force-load streaming lazy modules during app startup warmup"). | CONFIRM KEEP. |
| `continue_story_streaming` (557) | Called by the streamer event loop (2308). | Pure delegation to `llm_service.continue_story_streaming` (llm_parser:536 lazy binding); no logic of its own. KEEP. | Accurate (comment "Use the REAL continue_story_streaming from llm_service"). | CONFIRM KEEP. |
| `_committed_background_events` (562) | Called by streamer antagonist-cooldown call (see §2B-B30). | Reads already-committed background events from pre-turn state (worker-owned living-world data) for the streaming path; under §6(3) reading committed tick output is the merge side, not a new decision. KEEP. | Accurate. | CONFIRM KEEP. |
| `_enrich_streaming_structured_fields` (580) | Called by streamer persist block (3879). Read in full: backfills dice_rolls, computes sequence_id/user_scene_number, extracts/normalizes/annotates world_events, backfills world_events from game state when the LLM omits them, and returns True when canonical-event projection mutated authoritative state (caller then marks state_dirty). | Sequence-metadata half is transport (KEEP-worthy); the living-world extraction + backfill half runs faction/living-world work on the turn path, which §6(3) moves to async background ticks merged on the next turn — including "backfills from game state when LLM omits world_events" (server-supplied LW content) and canonical-event projection bookkeeping (`projected_world_event_ids` / `projected=True`) mutated into authoritative state on-path. ADAPT: keep sequence metadata on the turn path; move living-world extraction/backfill/projection into the §6(3) async tick, merged next turn. | Docstring accurately lists all six behaviours including the backfill (step 4) and the prune-order NOTE — it does not hide the LW work. The ADAPT is behavioural, not documentary. | CONFIRM ADAPT. |
| `_merge_server_system_warnings_for_streaming_persistence` (886) | Called by streamer done assembly. | Warning-channel hygiene under §6(1), changing no campaign value. KEEP. | Accurate. | CONFIRM KEEP. |
| `_append_level_xp_mismatch_warning` (961), `_apply_level_up_orphan_fail_closed_warning` (1003) | Called by streamer done assembly (4215) and persist block (3876). | Warn-only diagnostics (level/XP mismatch; orphaned level-up crossings fail-visible, not fail-silent); change no level or XP value. KEEP. | Accurate (orphan docstring correctly calls itself the streaming-path counterpart of the non-streaming warning). | CONFIRM KEEP. |
| `_LW_REQUIRED_FIELDS` (1055), `_count_compliant_lw_events` (1068) | Called by `_warn_if_living_world_missing`. | Compliance vocabulary + read-only counting for telemetry (presence of the key is what matters, value may be empty — docstring states this exactly). Under §6(3) this vocabulary describes what the async tick must produce. KEEP. | Docstring accurate. | CONFIRM KEEP. |
| `_warn_if_living_world_missing` (1083) | Called by streamer state-apply (3555) ONLY when `is_living_world_turn` is already true. Read in full: skips timeline modes, freeze/god/think/non-time-advancing/turn<1, then warns on absent world_events, missing `background_events` key, non-list background_events, or <2 compliant events. | Warn-only diagnostics; under §6(3) the warning remains valid telemetry for the async tick's output. KEEP. | Docstring mostly accurate, with one mismatch: it says "The caller may include the returned string in the SSE done event's warnings field", but the streamer call site ignores the return value (logs only). Also the "trigger turns (every 3 turns or 24 hours)" framing is enforced by the call site's `is_living_world_turn` gate, not by this function itself. Flagged in §3 (minor). | CONFIRM KEEP (+ doc flags). |
| `_strip_living_world_fields_from_mapping` (1182), `_restore_cooldown_living_world_state` (1204), `_strip_cooldown_living_world_fields_for_streaming` (1214) | Called by streamer state-apply (3538) and persist block (3921, via contract directly). Read in full: pops `firestore_service._AUTHORITATIVE_LIVING_WORLD_FIELDS` from the mapping, its custom_campaign_state, and nested state_updates, then restores prior LW state via `living_world_contract.restore_cooldown_state`. | Deletion of model-authored living-world facts with no registered exception; §6(3)'s answer is async-tick ownership with next-turn merge, not silent deletion. `_strip_living_world_fields_from_mapping` + `_strip_cooldown_living_world_fields_for_streaming` DELETE; `_restore_cooldown_living_world_state` ADAPT (fold into the §6(3) async tick merge; remove the inline turn-path restore). | `_strip_cooldown_*` docstring ("Remove model-emitted living-world fields on streaming cooldown turns") accurately describes the deletion — the defect is the behaviour, not the doc. The other two have no docstrings (doc gap, not staleness). | CONFIRM DELETE / DELETE / ADAPT. |
| `_extract_header_value` (1249) | Called by `_build_early_metadata_payload` (1281). | Pure `Key: value` text parsing preserving values. KEEP. | Docstring accurate. | CONFIRM KEEP. |
| `_build_early_metadata_payload` (1261) | Called by streamer pre-LLM (2236). | Best-effort early metadata projecting rewards_box/planning_block from canonical stored state for display before streaming completes; invents no new campaign fact. KEEP. | Docstring accurate ("best-effort early metadata so frontend can render pre-sections early"). | CONFIRM KEEP. |
| `_extract_god_mode_response_text` (1297) | Called by streamer validate/persist paths (3776, 3782, 3830). | Value-preserving extraction of non-empty god-mode text from dict/object payloads on the admin path. KEEP. | Accurate. | CONFIRM KEEP. |
| `stream_narrative_simple` (1313), `stream_with_context` (1515), `stream_events_generator` (1586), `_log_stream_payload` (1425) | TEST-ONLY CLUSTER: no prod callers. `main.py` imports none of these from `llm_parser` (it imports only StreamEvent, create_sse_response_headers, stream_story_with_game_state, warm_lazy_dependencies); main's `stream_with_context` at 6512/6593 is Flask's (main:105), not this module's. Only callers are tests (`tests/test_bq_logging_integration.py`, `tests/test_streaming_orchestrator.py`, `tests/test_bq_logging.py` execution_path strings). Internal chain: `stream_with_context` → `stream_narrative_simple` → `gemini_provider.generate_content_stream_sync` + `_log_stream_payload` (1414, its sole caller). | Simple text-only streaming without structured output or tool execution is transport in kind, but it is NOT on any prod path: the prod streaming path is `stream_story_with_game_state` via main:5734. Keeping a second, untested-by-prod streamer in the prod module is dead weight with a live BQ logging side effect (`_log_stream_payload` persists raw LLM pairs synchronously). ADAPT (all four): move the cluster out of prod `llm_parser.py` into test support (or DELETE if its tests are repointed); the §6(1) async/batched conversion run 2 prescribed for `_log_stream_payload` is MOOT for a test-only function — it follows its sole caller. | `stream_events_generator` docstring ("utility for Flask's Response stream_with_context") describes a use no prod code performs; `_log_stream_payload` docstring ("Fail-soft: any exception (or disabled flag) results in a warning rather than blocking the stream") is accurate about its own behaviour. | CHALLENGE: run 2 KEEP / KEEP / KEEP / ADAPT-to-async → review ADAPT-move-out-of-prod for all four (see §4-C3, §2). |
| `create_sse_response_headers` (1572) | Called by `main.py:6510, 6597`. | SSE headers (no-cache, keep-alive, no nginx buffering) required for streaming to reach the client. Pure transport. KEEP. | Accurate. | CONFIRM KEEP. |
| `_clear_interrupted_state_fields` (1628), `_parse_interrupted_stream_response` (1647), `_interrupted_source_text` (1665), `_event_is_interrupted` (1682) | Called by streamer done/interrupted paths. | Stream atomicity boundary: an interrupted response must not persist state_updates, rewards, planning, or level-up signal as if complete; source selection for forensics; transport-status predicate. Durable-write integrity, not domain filtering. KEEP. | Accurate. | CONFIRM KEEP (grouped). |
| `_apply_user_settings_to_state` (1690), `_prepare_streaming_game_state` (1713) | Called by streamer setup (2115, 2137) and `_prepare` internal. | Projects the user's own routing preferences (debug_mode, spicy_mode, faction_minigame_enabled) from Firestore user settings into streaming state; transport normalization + preference projection, values preserved. KEEP. | Docstrings accurate (including "Cleanup persistence remains the responsibility of the streaming caller"). | CONFIRM KEEP. |
| `_REPLAY_GOVERNED_DONE_KEYS` (1748), `_replay_governed_done_keys` (1769), `_apply_replayed_done_payload` (1795) | Called by streamer post-persist replay handling (4861). | Derives/applies every done-payload key a concurrent replay governs (losing turn's staged keys + explicit carriers) so a replay cannot leak stale values; replace-not-update for committed receipts is write-ownership logic. KEEP with the standing caveat (carried from run 2, strengthened here): the repo's concurrency-evidence rule requires observed overlap evidence before concurrency machinery is treated as proven; this row judges the mechanism, not the premise, and no such evidence was found in this area's files. If the premise is ever challenged, these rows become ADAPT (remove) rather than KEEP. | The in-code comment accurately describes the additive-`dict.update` hazard it addresses. | CONFIRM KEEP (with concurrency-evidence caveat). |
| `_emit_post_persist_incident_telemetry` (1817) | Called by streamer post-persist (4615), wrapped in try/except by the caller. | Post-persist incident telemetry (level-up resolution flush, progression outcome) mirroring the non-streaming persist path; logging under §6(1), emitted after the durable write by design; failure never reaches the stream. KEEP. | Docstring accurate (including "Telemetry failure never reaches the stream: callers wrap this in a try/except"). | CONFIRM KEEP. |
| `_scene_commit_allowed` (1875) | Called by streamer post-persist (4570). | Gates scene-image ownership transfer on whether this attempt actually committed (not replayed, not audit-conflicted). Durable-commit predicate for asset ownership, not a campaign-fact decision. KEEP. | Docstring accurate. | CONFIRM KEEP. |
| `_InterruptedPartialStreamError` (134), `POST_PERSIST_GUARD_FAILURES` (1889) | Exception raised by streamer state-apply on interrupted streams; counter incremented on causal-evidence build failure (4599). | Transport error carrier; process-level telemetry counter for logging under §6(1) (comment accurately notes the log-based-metric hook pattern). KEEP. | Accurate. | CONFIRM KEEP. |

#### 2B. `stream_story_with_game_state` (1892–5019) — BRANCH BY BRANCH

Every top-level branch below was read. Nested `if`s inside a branch are
covered by that branch's row where they share one decision; where a nested
branch makes a different kind of decision (mutate vs warn vs persist) it
gets its own row. Branches that merely delegate to another module's
function (`world_logic.*`, `rewards_engine.*`, `firestore_service.*`,
`level_up_session.*`, `dice_integrity.*`, `structured_fields_utils.*`,
`scene_illustration_service.*`) are judged here as ORCHESTRATION only —
their targets are audited by their owning groups, not re-verdicted here.
Verdicts: KEEP = transport / durable write / tool execution / authorization
/ bounded capacity, or a named product promise; ADAPT/DELETE name the change.

| Branch (lines) | What it does | Lens A verdict |
|---|---|---|
| B1 pre-flight cancel (1953–1956) | Returns early (no events) if the cancellation event is already set. | Transport cancellation. KEEP. |
| B2 parallel Firestore prefetch (1977–2040) | ThreadPoolExecutor fan-out for campaign / game state / user settings (prefetched tuple reused when the route already fetched it, preserving pre-stream 404 behaviour); campaign-missing yields `error` + returns; `resolve_mechanics_hidden` from user settings. | Durable reads + authorization-adjacent preference read; parallel-fetch capacity optimization with executor-shutdown discipline. KEEP. |
| B3 idempotency admission (2041–2095) | `turn_idempotency.admit_turn_request`; unavailable → error yield + return; conflict → error yield + return; replay + receipt → replayed narrative chunks + done payload + return. | Authorization / durable-write integrity (idempotency receipts). KEEP. |
| B4 god-mode mutation replay (2097–2110) | If god mode and `is_god_mode_mutation_replay`, renders the committed-state replay done payload + returns. | Admin-path replay integrity. KEEP. |
| B5 legacy cleanup persist (2113–2134) | `world_logic._cleanup_legacy_state`; if cleaned, persists the cleaned dict (baseline = committed state), re-reads, re-prepares, re-applies user settings. | Durable-write migration/cleanup on the turn path; the write itself is transport/storage integrity. KEEP as orchestration (the cleanup rules belong to world_logic's audit). |
| B6 producer-mode resolution (2140–2152) | If `producer_mode` is None, resolves the world-sim control basis; recomputes `is_timeline_mode`. | Transport/routing for timeline modes. KEEP. |
| B7 debug-command short-circuit (2154–2207) | `GOD_ASK_STATE` / `GOD_MODE_SET:` / `GOD_MODE_UPDATE_STATE:` inputs go to `world_logic._handle_debug_mode_command`; a non-None response is packaged as a done payload (god-mode response text, empty state_updates) + return. | Admin-path command handling; no model turn is consumed. KEEP. |
| B8 prompt-state rewards sanitization (2217–2230) | Non-god turns: `rewards_engine.sanitize_rewards_state_for_context` on a copy for prompt use only; prompt state swapped in only if it differs, user_settings carried over. | Prompt-side projection (does not persist the sanitized copy). KEEP as orchestration (the sanitizer itself belongs to rewards_engine's audit). |
| B9 early metadata + pre-LLM cancel (2241–2246) | Yields `metadata` event (early payload + `mechanics_hidden` so raw roll events cannot leak); returns if cancelled before the LLM call. | Transport (early display metadata + cancel boundary). KEEP. |
| B10 scene coordinator setup (2265–2307) | `maybe_start_scene_coordinator` (defer_start + defer_preparation); parallel-mode kickoff flagged pending (kicked off at first chunk, never in front of the LLM call). | Non-text tool-path orchestration; deferral keeps images off the story critical path. KEEP. |
| B11 event-loop scene/cancel gates (2325–2358) | On `done`: start scene preparation. On chunk/done with pending kickoff: start the coordinator. Drains scene_image events. On cancellation: logs + returns WITHOUT persisting (comment cites the downstream-disconnect contract: previous turn + planning choices stay latest; a cancel after persist cannot roll back). | Transport + commit-boundary discipline. KEEP. |
| B12 non-done chunk / live-prefix branch (2359–2448) | Forwards non-done events; when the started-notification hook is enabled, accumulates chunk deltas until the first renderable root-narrative prefix qualifies, then publishes a started notification ONCE (reset chunks handled: a reset discards the accumulated prefix; a reset chunk is evaluated only if it is itself a genuine root envelope; snippet failure degrades to "deferred", never retries per token). Yields the event; on chunk, starts scene preparation; `continue`. | Transport streaming + optional notification; the once-only + envelope-provenance guards prevent duplicate/notification-from-prose defects. KEEP. |
| B13 done-event raw capture + marker scrub (2459–2508) | `is_interrupted_partial` from the payload; `full_narrative` / `raw_response_text` extracted; raw payload hash logged (full text logged only if raw capture enabled); done `state_updates` scrubbed via `_scrub_model_state_marker` before any downstream processing. | Logging under §6(1) + authorization (marker defence). KEEP. |
| B14 interrupted vs fresh parse (2509–2618) | If raw text present or an interrupted source exists: interrupted → `_parse_interrupted_stream_response` + `_clear_interrupted_state_fields` (with the comment that interrupted responses already had rewards_box_key_present reset by the atomicity boundary); fresh → `parse_structured_response(..., requires_action_resolution=False)` + telemetry extraction + raw-field coercion + explicit-social-clear detection + `rewards_box_key_present` from the literal raw JSON (comment explains this is the only place key presence distinguishes "omitted" from "sent empty" for the dual-authoring rule). Parse exceptions are logged, not raised. | Pure parsing + atomicity enforcement; the key-presence capture is transport bookkeeping for the receipt rule. KEEP. |
| B15 telemetry-interrupted reclassification (2619–2637) | If telemetry says `interrupted` after a non-interrupted parse: re-marks the turn interrupted, appends ` [interrupted]` to the narrative (mutating the NarrativeResponse narrative), rebuilds the interrupted result, clears interrupted fields from structured fields. | Transport atomicity (honest interrupted marking). KEEP. |
| B16 signal diagnostics + raw restores (2643–2671) | Logs `LEVEL_UP_SIGNAL_SOURCE` (dict vs absent/None distinction for the unauthorized-mutation guard's call sites); `_should_prefer_raw_model_planning_block` restore (deepcopy into structured fields); `_preserve_raw_rewards_fields_if_missing`; `structured_fields_utils.strip_model_progression_fields`. | Diagnostics + value-preserving restores + progression-field strip (the strip target belongs to structured_fields_utils' audit; as orchestration here it removes model progression claims from the streaming view). KEEP as orchestration. |
| B17 state-apply init + interrupted raise (2715–2726) | Deepcopies pre-response state; interrupted → clears state_updates, raises `_InterruptedPartialStreamError`; pops consumed `pending_system_corrections` (marks dirty). | Atomicity boundary. KEEP. |
| B18 god-mutations merge + modal locks (2728–2811) | Pulls top-level `god_mode_mutations` into raw state_updates (PR #8594 fix: the LLM emits them as a sibling of state_updates); extracts `intent_classifier` debug metadata (the debug-info carrier only — no classifier call is made here); `agent_mode_used` from the payload; `_enforce_character_creation_modal_lock` UNCONDITIONALLY (comment: guarding on truthy state_updates would skip server-authored transitions like finish_level_up when the LLM omits state_updates); `backfill_rewards_box_new_level`; `_enforce_campaign_upgrade_modal_lock`; creation-conclude detection. | Modal-lock enforcement + admin-mutation routing; the unconditional-lock comment accurately states the stuck-modal hazard. KEEP as orchestration (lock rules belong to world_logic's audit). Note: the `intent_classifier` debug-info read here is metadata transport, NOT a use of `intent_classifier.py` — the classifier files still DELETE in full; nothing here rescues them. |
| B19 mode/freeze computation (2814–2885) | Copies `planning_block` from state_updates into structured fields (canonical-stream capture); `compute_god_and_level_up_mode`; think/character-creation/freeze-choice → `should_freeze_time`; inline import of preventive_guards helpers (comment: circular-import break, since preventive_guards imports `resolve_location` from this module). | Routing/mode computation. KEEP as orchestration. |
| B20 location + social-HP + freeze-time (2886–2955) | If not freeze-time: `_ensure_location_progress` via a `_DummyLLMResponse` adapter (comment: a freeze-time `location_confirmed` is treated as hallucination that must not persist); `apply_social_hp_challenge_transport` with the explicit-root-null flag; freeze-time state changes applied via `_apply_freeze_time_state_changes` in both the freeze and non-freeze arms (different arms, same helper). | Location-progress + social-HP transport + time-freeze state handling. KEEP as orchestration (the guards themselves belong to preventive_guards' audit; the freeze-time hallucination rule is a documented invariant, not a silent rewrite of a live location). |
| B21 action-resolution + system corrections (2955–3013) | Backfills `action_resolution` from raw fields when absent; normalizes `pending_system_corrections` from done/raw sources; collects `all_streaming_system_corrections`. | Audit-trail backfill + correction bookkeeping. KEEP as orchestration. |
| B22 reward-event capture + level-mutation block (3013–3099) | Snapshots the raw reward event (capture rewrites in place; the anomaly ledger audits the raw one); `capture_and_validate_reward_event` (validated receipt feeds `persist_turn_atomic`); non-level-up/non-god turns with an unauthorized reducer session get `block_unauthorized_level_mutation_deltas`. | Receipt/authorization core (state-owned reward design). KEEP as orchestration (capture/validation rules belong to rewards_engine's audit). |
| B23 state merge + directives + god dispatch (3099–3223) | `_before_state_updates` snapshot; `update_state_with_changes` with `clear_turn_scoped_living_world_fields = not (god or freeze)` (turn-scoped LW singleton clearing — see B27 for the cooldown strip itself); `validate_game_state_updates`; pending-corrections write-back; directives saved via `apply_god_mode_directives` BEFORE canonicalization so canonicalizers see god-mode state changes; `GodModeEnvelopeError` → rejected flag + warning (no raise); rejected fields popped from done/raw/structured. | Merge + validation + admin-directive execution. KEEP as orchestration (merge rules belong to state-storage/world_logic audits; the LW-singleton clearing flag is turn-scoped bookkeeping, distinct from the cooldown strip). |
| B24 god/level-up dispatch + finalize (3224–3333) | God-mode level-up signals/dispatch (`_god_mode_level_up_signals`, `god_mode_has_level_activity`, `_god_mode_level_up_dispatch`); `finalize_streaming_state_before_persistence`; review-live checks and campaign-upgrade planning normalization (see B25). | Admin-path dispatch + finalize. KEEP as orchestration. |
| B25 canonical rewards + review/suppression (3333–3472) | `canonicalize_rewards` (canonical_stream_rewards_box/planning_block/suppressed); review-live planning replacement via campaign-upgrade normalization; false-positive flag clearing; canonical-box write-back vs suppression (suppressed → rewards_box dropped from structured fields, planning replaced or preserved per raw-review/normal-gameplay predicates); `canonical_stream_suppressed` + `level_up_suppressed` interplay. | Reward/level-up canonicalization (the state-owned receipt design). KEEP as orchestration (canonicalize rules belong to rewards_engine's audit). |
| B26 suppression clearing + turn counter + LW tracking (3472–3550) | Suppressed/false-positive planning cleared from updated state (`planning_block = None`, dirty); `_increment_turn_counter` (dirty only if the counter actually changed; god/freeze turns normalize str→int without incrementing); `_maybe_update_living_world_tracking` (sets `is_living_world_turn`, pre-action world_time passed to match prompt logic). | Turn bookkeeping + LW trigger tracking (not LW content generation). KEEP. |
| B27 cooldown strip + LW warn + persisted planning fallback (3550–3590) | `_strip_cooldown_living_world_fields_for_streaming` (DELETE per the helper row); if stripped, `event.payload["state_updates"]` re-synced; if `is_living_world_turn`, `_warn_if_living_world_missing` (warn-only, KEEP); if persisted planning lacks actionable choices and neither level-up-suppressed nor false-positive: `_ensure_custom_action_planning_block` and the result is WRITTEN INTO `updated_state_dict["planning_block"]` + dirty — i.e. the server fallback IS persisted here (ADAPT per the helper row: display-layer only). | Two defects in one branch: the cooldown strip (DELETE) and the persisted fallback (ADAPT). The LW warn half is KEEP. Branch verdict: MIXED — strip DELETE, fallback-persist ADAPT, warn KEEP (counted as one mixed branch row; see §6 tally note). |
| B28 state-apply exception handlers (3590–3679) | Interrupted → restore pending corrections, not dirty. Input-conflict → re-raise (comment: a typed 409 must not be downgraded to a generic warning). Generic → log, roll back to pre-merge snapshot (or pre-response state), clear state_updates, clear interrupted fields from payload + structured fields, clear canonical pair + directive/correction telemetry, mark `state_apply_failed`, append a visible warning event + server warning. | Fail-visible rollback: the narrative is kept, only the state delta is dropped, and the failure is surfaced — the repo's UX-first rule in action. KEEP. |
| B29 validate/persist story entries (3683–3861) | If not validation-failed and narrative present: validate raw text exactly (catches empty/invalid raw payloads even when a fallback narrative exists); interrupted-parse recovery; god-mode text fallback (decoded at the persistence seam); narrative-empty → god-mode text or `validation_failed = True` + warning event. | Validation gating that FAILS VISIBLE (warning event) rather than silently persisting a bad turn; the narrative-fallback branches here are the streamer's own, distinct from the parser's fabrication paths (rowed at `parse_structured_response`). KEEP. |
| B30 persist block, part 1 — enrich/scene/LW strips/canonical application (3862–4114) | Copies state_updates into structured fields; `god_mode_envelope_rejected` → god mutations popped; interrupted → clear interrupted fields; orphan warning; `_enrich_streaming_structured_fields` (ADAPT per its row — LW half moves to the async tick; if it mutated canonical projection bookkeeping, state_dirty is forced True); scene snapshot/pending-placeholder handling (exactly one snapshot, no waiting — comment explicitly forbids reintroducing a per-turn sleep tax); NEW BRANCHES NOT IN RUN 2's SEAM SAMPLE: if `cooldown_lw_strip_applied` and not timeline mode, `living_world_contract.strip_lw_fields_from_mapping(gemini_structured)` (3921) — a SECOND LW strip on the persist path, DELETE per §6(3) (same defect as the helper, applied to the persisted copy); then `living_world_contract.enforce_antagonist_cooldown_on_write` (3931) — server-enforced antagonist cooldown stripping `tone == "antagonist"` events within `ANTAGONIST_COOLDOWN_DAYS`, with the comment "Prompt-only guidance drifts (verified 2026-08-21), so the structural fix lives here" — DELETE per §6(3) + the faction group's own flag (no registered exception for the server strip was found there either; if the strip is to survive, the exception must be named and registered; until then enforcement moves to prompt/schema). Canonical-pair application (suppressed → pop rewards_box, replace/preserve planning per raw-review/normal-gameplay predicates; canonical box → write both fields); stale-rewards restore of the raw model box when suppressed-but-not-stale; xp alias completion (`xp_total`→`current_xp`, `xp_to_next_level`→`next_level_xp`) on the DISPLAY copy. | Mixed branch: enrich ADAPT (LW half), scene KEEP, second LW strip DELETE, antagonist strip DELETE, canonical application KEEP as orchestration, xp-alias completion KEEP as display-copy normalization (it mutates only the `_raw_rewards_box` display copy, not persisted state). Branch verdict: MIXED (see §6 tally note). |
| B31 persist block, part 2 — done payload assembly (4114–4274) | Rewards normalization (`normalize_rewards_box_for_ui` or None under suppression; pop vs set on both structured + payload); done planning fallback via `_ensure_custom_action_planning_block` (ADAPT — same display-only fix; note this site writes into `gemini_structured`, the persisted copy, not just the client view); modal-finish injection (`inject_modal_finish_choice_if_needed`, skipped when the user is exiting the modal); session-header merge + resources enrichment; dice-audit resolution from code-execution evidence (`apply_dice_audit_resolution` — §6(2) audit trail, on-path as required); action-resolution roll normalization + narrative-outcome application (mechanics_hidden-gated); level/XP mismatch warning (after the dice backfill, per the BD-724 prune-order comment citing a confirmed dev-campaign case); server-warning merge; interrupted → final atomicity clear; accepted-player-input projection; client-facing structured_response built as a shallow copy with the session-header marker stripped ONLY from the client copy (comment: the marker must stay in the persisted copy for the read-time re-normalization path). | Mixed: rewards/modal/session-header/dice/warning assembly KEEP as orchestration + display work; done planning fallback ADAPT (display-layer only). The marker-strip discipline (persisted copy keeps it, client copy strips it) is correct transport hygiene — KEEP. Branch verdict: MIXED (fallback ADAPT, rest KEEP). |
| B32 BQ logging + audit + commit gates (4274–4531) | BQ payload logging BEFORE Firestore (comment: so the row is written even if persistence raises; fail-soft so observability cannot interrupt a completed stream); cache-replay detection; `routed_audit_persistence_operation`; cancellation check (commit boundary: a downstream disconnect before commit aborts the turn); `commit_permit` check (authoritative precommit fence; comment honestly bounds it: provider reads cannot be preempted by outer-worker checks, only by transport timeout/process lifetime — the permit is what decides commit-vs-cancel); verified social-HP roll projection onto BOTH the merge source and the persisted challenge (`project_verified_printed_social_hp_state` + `project_verified_roll_attribution`, no-op without RNG-verified evidence — this is the §6(2)-adjacent PROVEN spec `social_hp.executed_roll_attribution` in action, and it only projects verified evidence, never model claims); debug-mode stripping from both persistence candidates; `persist_turn_atomic` with validated + raw reward events, baseline, audit operation, review-edit intent, timeline preservation, control basis. | Logging under §6(1) (BQ before persist + fail-soft) + authorization (commit gates) + durable write + verified-roll projection (the one PROVEN exception in this area, correctly scoped to RNG-verified evidence). KEEP. Note: the BQ calls here are synchronous on the turn path — under §6(1) they are ADAPT-to-async ONLY where they block; the code comments assert fail-soft + before-persist ordering as the reason, so this row keeps the ordering but flags the async conversion as open for the BQ-logging owner (it is not a branch defect of this function). |
| B33 post-persist sync + telemetry (4531–4760) | Scene commit gating + after-narrative start; causal-evidence build (best-effort, guard-failure counter on exception); post-persist incident telemetry (try/except, never reaches the stream); replay-winner handling (winner payload applied via `_apply_replayed_done_payload`, `_replay_winner_payload` saved for final governance); non-replayed sync (committed state + structured fields copied back, debug-mode projected, reward_display/rewards_box presence synced to the committed copy with explicit pops — comment explains additive `dict.update` cannot clear stale staged values); reward-withheld log + box pop; turn telemetry emit (warn on failure). | Durable-write reconciliation + telemetry. KEEP. |
| B34 validation-failed BQ branch (4760–4850) | When not persisted (validation failed): BQ logs the failed payload with `finishReason: error: validation_failed` + parse telemetry event; exceptions logged, never raised. | Logging under §6(1), fail-soft. KEEP. |
| B35 done finalization (4851–4883) | Persistence warnings attached to `done.warnings`; `validation_failed` flagged on the payload; replay-winner governance re-applied to the FINALIZED payload (losing turn's trailing warnings dropped); yield done; yield warnings; interrupted → return (do not pull another provider item after persisting the cancellation snapshot). | Transport finalization + replay governance. KEEP. |
| B36 outer exception handler (4885–5016) | BQ error-payload logging (fail-soft); quota-reservation release on admission-keyed failures (god vs normal bucket); `RequestInputConflictError` → typed error event + return; mode-conflict → message passthrough, else generic message + `value_error`/`streaming_error` typing (never leaks internals except for mode conflicts). | Fail-soft observability + authorization (quota release) + honest error typing. KEEP. |
| B37 finally (5018–5019) | `scene_coordinator.abort_preparation()` if present. | Cleanup. KEEP. |
| Overall `stream_story_with_game_state` verdict | Production streaming flow (provider/model selection delegated to `llm_service.continue_story_streaming`, agent selection, LLM request building, persistence seam) — deleting it removes streaming gameplay entirely. As orchestration it is transport + durable writes + tool execution, which Pass B allows. But as a 3,128-line function inside a module named for parsing, it drags planning/LW/persist decisions into the parser's blast radius; the parser question is already answered by `parse_structured_response`. | ADAPT: SPLIT out of `llm_parser.py` into a streaming-orchestration module; keep behaviour, change address; its internal planning/LW branches inherit the seam rows above (notably B27/B30/B31 ADAPT/DELETE items). Run 2's SPLIT verdict CONFIRMED; run 2's "MERGE candidate rejected" CONFIRMED (merging a 3,128-line streamer into the schema module would be worse). The branch pass adds two DELETE branches run 2's seam sample missed (B30 second LW strip + antagonist strip) and confirms no other branch invents, drops, or rewrites a campaign fact beyond the rows above. |

### 3. `mvp_site/narrative_sync_validator.py` (147 lines; 13 AST units: 4 classes + 5 methods + 4 enum members)

Module docstring: "Narrative Synchronization Validator for Production Entity Tracking / Adapted from Milestone 0.4 prototype for production use in llm_service.py / REFACTORED: Now delegates to EntityValidator for all entity presence logic." The delegation claim is accurate; the "production use" framing does not rescue a semantic validator. Prod callers: exactly 3 `llm_service.py` sites, ALL warn/log-only: `_validate_entity_tracking` (~2000, logs missing entities + warnings, returns the response text unchanged), initial-story site (~5379, comment "log but not retry to avoid complexity"), `stream_initial_story` (~5664, log only). No entity retry loop exists in `llm_service.py` (see §4-C1). The validate interface contract is consistent (reads `result.found_entities` / `result.entities_missing` / `result.all_entities_present` from `entity_validator.ValidationResult.__post_init__` syncing), which is why the sites work today — consistency does not change the verdict.

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `EntityPresenceType` + members `PHYSICALLY_PRESENT` (16), `MENTIONED_ABSENT` (17), `IMPLIED_PRESENT` (18), `AMBIGUOUS` (19) | Used by `_check_continuity` + `validate` only. | Vocabulary for a semantic judgment the server must not make; exact duplicate of `entity_validator`'s enum (duplication flagged — both locations, one definition must go; the module-DELETE verdicts resolve it). DELETE. | No docstring; the member names promise a presence taxonomy the code cannot establish (see `_check_continuity`). | CONFIRM DELETE. |
| `EntityContext` class (26) + `__post_init__` (37) | Constructed by `validate` only. | Carrier for the continuity check (entity name, scene context, manifest); the scene manifest already carries this information to the model in the prompt. DELETE. | Docstring "Context for a single entity during narrative validation" is accurate about what it carries; the carrier's purpose is the defect. | CONFIRM DELETE. |
| `ValidationResult` class (42) + `__post_init__` (57) | Returned by `validate` only. | Carrier for a semantic verdict (missing/present/inconsistent entities, continuity warnings); diagnostics could live in the parser's coverage dict instead. DELETE. | Docstring accurate about the carrier shape. | CONFIRM DELETE. |
| `NarrativeSyncValidator.__init__` (72) | Constructed at the 3 llm_service sites (via module-level instance? — verified: llm_service constructs `NarrativeSyncValidator()` at the call sites; the module itself exports no instance). | Constructs an `EntityValidator` delegate plus an `emotional_patterns` keyword table (79: grief/mourning/grieving/sorrowful/bereaved; anger/furious/enraged/angry/wrathful; fear/terrified/afraid/fearful/frightened; guilt/guilty/ashamed/remorseful). The table is NEVER read anywhere in the file (grep: only line 79) — dead keyword table, exactly the repo-banned keyword/substring semantic-routing pattern, unused. DELETE (module) + the table is separately listed in §1 as dead code. | No docstring explaining the table's purpose (it has none, because it is unused). | CONFIRM DELETE. |
| `NarrativeSyncValidator._check_continuity` (86) | Called by `validate` only. | Substring continuity judgment: entity mentioned via `entity.lower() in narrative.lower()` plus physical-marker substring absence → "mentioned absent". Substring absence proves nothing (a marker can persist off-screen or be reworded); no registered exception. DELETE. | No docstring; the method name promises a continuity check the substring test cannot perform. | CONFIRM DELETE. |
| `NarrativeSyncValidator.validate` (106) | The 3 llm_service warn/log sites. | Delegates to `EntityValidator.validate` (125), appends continuity warnings, logs a delegation line. The logging half is §6(1)-allowed but does not rescue the semantic whole; the llm_service sites must be updated to the prompt requirement + `entities_mentioned` array + parser coverage diagnostic (with the §4-C9 caveat: `validate_entity_coverage` is currently test-only and must be wired first if it is to be that replacement). DELETE. | Docstring "Validate narrative synchronization" overstates what a substring check establishes. | CONFIRM DELETE. |

Module verdict: DELETE as a module (run 2 CONFIRMED). Consequence: the 3 llm_service warn/log sites lose their continuity warnings (they already change nothing about the turn); the `EntityValidator` delegate goes with it; no retry loop is removed because none exists (§4-C1).

### 4. `mvp_site/entity_validator.py` (672 lines; 28 AST units: 2 functions + 4 classes + 16 methods + 4 enum members + 2 module globals)

Module docstring: "Enhanced Post-Generation Validation with Retry (Option 2 Enhanced) / Validates AI output for missing entities and implements retry logic." Accurate about intent; the retry logic is the defect, not a rescue. Prod importers: `llm_service.py:231` (EntityValidator class — effectively unused, see below), `narrative_sync_validator.py:12` (EntityValidator), `entity_utils.py:10` (only `filter_unknown_entities`, `is_unknown_entity` — the two KEEP sentinels). The module-level `entity_validator` (671) and `entity_retry_manager` (672) globals have NO prod users (tests only).

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `filter_unknown_entities` (19) | Prod user: `entity_utils.py:10`. | `[e for e in entities if e.lower() != "unknown"]`; lowercases for comparison but preserves the original entity strings — value-preserving for real entities. "Unknown" is a default location name when location is not found and must not be treated as a real entity. KEEP. | Docstring accurately says exactly that. | CONFIRM KEEP. |
| `is_unknown_entity` (35) | Prod user: `entity_utils.py:10`. | `entity.lower() == "unknown"`; case-insensitive sentinel predicate. KEEP. | Accurate. | CONFIRM KEEP. |
| `EntityPresenceType` + members (53–59) | Used by `analyze_entity_presence` / `validate` only. | Identical enum to the sync validator's (duplication flagged — both locations; module-DELETE verdicts resolve it). Vocabulary for a semantic judgment. DELETE. | No docstring. | CONFIRM DELETE. |
| `ValidationResult` class (63) + `__post_init__` (96) | Returned by `validate` / `validate_entity_presence` only. | Carrier for semantic verdicts; `__post_init__` syncs legacy/compat fields (`entities_found = found_entities`, `entities_missing = missing_entities`, `all_entities_present = len(missing_entities) == 0`, `confidence = confidence_score`). Required fields: passed, missing_entities, found_entities, confidence_score, retry_needed, retry_suggestions. DELETE. | Docstring accurate about the carrier shape. | CONFIRM DELETE. |
| `EntityValidator.__init__` (103) | Constructed at `llm_service.py:711` (module-level instance — NEVER referenced again in llm_service.py; dead prod instance, §1) and by `narrative_sync_validator` + tests. | Builds regex tables + `min_confidence_threshold = 0.7`; the threshold is an arbitrary server judgment about prose, not a transport bound. DELETE. | No docstring explaining why 0.7 is the threshold (it is not justified anywhere in the file). | CONFIRM DELETE. |
| `_build_entity_patterns` (139), `_compile_patterns` (157) | Called by `__init__` only. | Direct-mention, pronoun, role, action-attribution regex templates + their compilation; pronoun/role patterns cannot attribute presence. Compilation is performance, not rescue. DELETE. | No docstrings. | CONFIRM DELETE. |
| `analyze_entity_presence` (175) | Called by `validate_entity_presence` only. | Classifies mentioned-absent via absence regexes/thought phrases, physically present via substring containment, or missing; substring containment is not presence. DELETE. | Docstring overstates: it promises presence analysis; it performs substring/regex classification. | CONFIRM DELETE. |
| `extract_physical_states` (212) | Called by `validate` only. | Associates bandaged/trembling/wounded/bloodied/exhausted matches with nearby capitalized words as entity names — misattributes whenever two capitalized words are near a match. DELETE. | Docstring accurately describes the matching; the matching itself is the defect. | CONFIRM DELETE. |
| `detect_scene_transitions` (238) | Called by `validate` only. | Extracts "moved to / arrived at / now in" matches; the model already authors `location_confirmed`, the authoritative signal. DELETE. | Accurate about what it extracts. | CONFIRM DELETE. |
| `create_injection_templates` (253) | Called by `validate_entity_presence` path (retry suggestions) only. | Returns canned sentences like "{entity}, who had been present but silent, {action}." — literally server-authored story text, the clearest ZFC failure in this area, no registered exception. DELETE. | No docstring; the templates are self-evidently server prose. | CONFIRM DELETE. |
| `validate_entity_presence` (274) | Called by `validate` only. | Scores each entity; retry-needed from the 0.7 threshold (295, 311). The checkable contract is the `entities_mentioned` array, which needs no scoring. DELETE. | Accurate about scoring; scoring is the defect. | CONFIRM DELETE. |
| `_calculate_entity_presence_score` (335) | Called by `validate_entity_presence` only. | 0.8 substring hit + 0.1/mention capped + partial-name credit + 0.3 action patterns + pronoun credit — invented arithmetic of presence. DELETE. | Docstring accurately lists the scoring; the scoring is invented. | CONFIRM DELETE. |
| `_generate_retry_suggestions` (379) | Called by `validate_entity_presence` only. | Generic "Include X in the scene..." suggestions; the prompt can state the requirement once. DELETE. | Accurate. | CONFIRM DELETE. |
| `create_retry_prompt` (417) | Called by `validate_with_retry` only. | Builds a "MUST be included... Please revise" repair re-prompt — a new LLM request path, which repo house rules ban without approval, hiding prompt/schema failure behind regeneration. DELETE. | Accurate about building a repair prompt; the repair path is the defect. | CONFIRM DELETE. |
| `validate` (452) | Called by `narrative_sync_validator.validate` (125) + tests. | Composite: filters "Unknown" via the KEEP sentinel, then presence analysis, physical states, transitions, confidence = clear/total with 0.1-per-ambiguous reduction, warnings. Every input leg is DELETE above except the sentinel filter, so the composite has no surviving leg. Note its own comment (~537): "Entity transition validation is now handled by enhanced system instructions" — the file itself concedes string matching was replaced by prompt guidance for transitions, yet keeps the rest. DELETE. | Docstring accurate about the composite; the composite's legs are the defect. | CONFIRM DELETE. |
| `EntityRetryManager.__init__` (581), `validate_with_retry` (586), `get_retry_statistics` (661) | No prod callers. | `max_retries = 2`; loops validation → retry prompt → regeneration callback up to max_retries (615, 620), spending extra model turns fixing a server-scored defect the model was never told about in the original prompt. `get_retry_statistics` is telemetry for a deleted mechanism — standing alone it would be §6(1) logging, but it has no independent subject. DELETE all three. | Docstrings accurate about the loop; the loop is the defect. | CONFIRM DELETE. |
| `entity_validator` (671), `entity_retry_manager` (672) | No prod users (tests only). | Module-level instances of deleted classes. DELETE with the classes (also §1 dead code). | No docstrings. | CONFIRM DELETE. |

Module verdict: DELETE as a module EXCEPT `filter_unknown_entities` + `is_unknown_entity`, which move to `entity_utils.py` (their existing prod importer) or a sentinel-helpers module (run 2 CONFIRMED, with the corrected consequence in §4-C1: no llm_service retry loop is removed, because none exists; the behaviour change is only the loss of the 3 warn/log call sites + the dead line-711 instance + test updates). Draft-amendment note: the 0.7 threshold and regex/substring scoring are NOT model outputs (no FastEmbed/Jev call is involved), so the draft amendment does not touch these verdicts — stated explicitly in §5.

### 5. `mvp_site/schemas/validation.py` (1,229 lines; 65 AST units: 39 functions + 26 module symbols)

Prod importers: `schemas/__init__.py` (10 helpers re-exported) + direct
prod importers of specific helpers (`game_state.py` via the package;
`firestore_service.py` imports the module as `schema_validation`). Every
function below is either a schema introspection helper, a diagnostics-only
validator, or a transport loader — none of them rewrites a campaign value,
EXCEPT `sanitize_state_updates_overlay` + its near-match machinery (ADAPT).
The warn-not-reject caller caveat run 2 attached to `validate_game_state`
is now VERIFIED satisfied (see §4-C12): both prod call sites
(`game_state.py:3319`, `game_state.py:3668`) are explicitly warning-only /
non-blocking ("WARNING ONLY - Non-blocking validation", "validation
warnings are logged but do not crash", "Continue execution").

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `check_datetime` (30) | Called by `get_validator`'s format checker. | RFC 3339 format gate for durable writes (a timestamp shape, not a campaign fact). KEEP. | Accurate. | CONFIRM KEEP. |
| `_enrich_validation_message` (135) | Called by `validate_game_state` / `validate_story_entry` paths. | Message enrichment only; changes no value. KEEP. | Accurate. | CONFIRM KEEP. |
| `load_schema` (150), `load_world_sim_setup_schema` (182) | Called by `get_validator`, `get_spell_authoring_schema`, and every schema-derivation helper in this file + `character_creation_wire.py` + `game_state_models.py` paths. | Single loader + cache (150); fresh vs preserve-existing-roster world-sim variants (182). Transport (schema loading), no value changed. KEEP. | Accurate. | CONFIRM KEEP. |
| `get_spell_definition` (193), `get_spell_authoring_schema` (204), `get_spell_authoring_list_schema` (223) | Called by schema assembly (NRS + character_creation_wire). | Spell contract derivation (name, level 0–9, description required; provider length caps unless `bounds=False` for the creation modal — the modal-never-truncates rule, capacity, not content). KEEP. | Accurate. | CONFIRM KEEP. |
| `inline_canonical_defs` (228) | Called by schema assembly everywhere in this area. | Inlines `#/$defs/` refs because structured-output providers reject unresolvable `$ref`s. Transport (provider compatibility). KEEP. | Accurate. | CONFIRM KEEP. |
| `get_validator` (268) | Called by all validation entry points in this file. | Cached Draft202012Validator + format checker. Transport. KEEP. | Accurate. | CONFIRM KEEP. |
| `validate_game_state` (288) | Prod callers: `game_state.py:3319` + `game_state.py:3668`, BOTH explicitly warning-only/non-blocking (see header note). | Diagnostics-only validation returning warnings/errors lists; mutates nothing. KEEP. | Accurate. | CONFIRM KEEP (caveat now verified — §4-C12). |
| `get_story_entry_validator` (323), `validate_story_entry` (343) | Called by story-entry validation paths. | Diagnostics only. KEEP. | Accurate. | CONFIRM KEEP. |
| `get_canonical_equipment_slots` (356) | Called by equipment-schema derivation. | Read-side vocabulary from the canonical schema. KEEP. | Accurate. | CONFIRM KEEP. |
| `_merge_schema_properties` (382) | Called by schema-key derivation helpers. | Schema introspection resolving refs/allOf for property tables. KEEP. | Accurate. | CONFIRM KEEP. |
| `get_player_character_schema_keys` (402), `get_legacy_equipment_slot_aliases` (425), `get_known_equipment_slots` (430), `get_spell_slot_read_aliases` (442), `get_valid_spell_slot_levels` (455), `get_game_state_top_level_properties` (470), `get_strict_overlay_nested_allowed_keys` (483), `get_social_hp_challenge_properties` (507), `_get_social_hp_enum_values` (518), social-HP enum getters (527, 538, 549, 560), `get_social_hp_continuity_properties` (571), `_get_time_of_day_values` (579), `get_time_of_day_values` (603), `get_common_field_paths` (612) | Called by schema assembly + validation + `schemas/__init__.py` re-exports. | Schema-derived vocabulary/path tables; read-side only, rewriting nothing. The `get_time_of_day_values` lowercasing is vocabulary normalization, not a value rewrite (it normalizes the enum list, not a stored value). KEEP (grouped; every name is listed here, satisfying the grouped-row rule). | Accurate. | CONFIRM KEEP (grouped). |
| `validate_state_updates_overlay` (729) | Called by NRS state-updates validation + tests; prod callers beyond NRS:3776 are tests only (grep). | Returns warnings/errors lists only, mutates nothing; same warn-not-reject caveat as `validate_game_state` (its callers log and continue). KEEP. | Accurate. | CONFIRM KEEP. |
| `sanitize_state_updates_overlay` (900) | Called by NRS state-updates validation (3776) + tests. Read in full. | Dotted-key expansion, frozen-plan placement, game_state unwrap, and keep-unknown-keys-verbatim + warned are all value-preserving (KEEP halves). The near-match remapping is the defect: `_map_or_keep_unknown_key` uses `_get_near_match_suggestions` (difflib cutoff 0.72, 1221) and RENAMES an unknown key to the top suggestion when the target is absent (with a `campaign_tier` type guard). Renaming a model-authored key to a different key silently retargets a state update — a field-aware transformation with no registered exception. ADAPT: remove the remapping; keep everything else. | Docstring ("Map typo-like keys when possible; otherwise keep unknown keys and report corrections") ACCURATELY describes the renaming — this is a behavioural defect, not a doc defect. Not a §3 item. | CONFIRM ADAPT. |
| `_canonicalize_frozen_plans_placement` (1045) | Called by `sanitize_state_updates_overlay`. | Structural move (frozen_plans placement canonicalization), content preserved. KEEP. | Accurate. | CONFIRM KEEP. |
| `_normalize_dotted_state_update_keys` (1082), `_normalize_nested_game_state_keys` (1149) | Called by `sanitize_state_updates_overlay`. | Dotted-key expansion + game_state unwrap; values preserved. KEEP. | Accurate. | CONFIRM KEEP. |
| `is_valid_game_state` (1190) | Called by validation gates. | Read-only predicate. KEEP. | Accurate. | CONFIRM KEEP. |
| `_normalize_for_similarity` (1204), `_get_near_match_suggestions` (1208) | Called by `_map_or_keep_unknown_key` only. | Similarity machinery whose only consumer is the renamer. ADAPT: warn-hint use only; never feed a rename (the suggestions become warning text, e.g. "unknown key X looks like Y — did you mean it?", with the model free to correct on the next turn). | Accurate about similarity computation. | CONFIRM ADAPT. |
| Module symbols — caches (all KEEP, grouped with every name listed): `_FORMAT_CHECKER` (23), `_RFC3339_PATTERN` (24), `_SCHEMA_CACHE` (44), `_VALIDATOR_CACHE` (45), `_SCHEMA_WARN_THRESHOLD_MS` (46, 50ms slow-validation warning threshold, logging), `_CANONICAL_EQUIPMENT_SLOTS_CACHE` (47), `_GAME_STATE_TOP_LEVEL_PROPERTIES_CACHE` (48), `_SOCIAL_HP_REQUEST_SEVERITY_CACHE` (49), `_SOCIAL_HP_SKILLS_CACHE` (50), `_SOCIAL_HP_STATUS_CACHE` (51), `_SOCIAL_HP_NPC_TIER_CACHE` (52), `_TIME_OF_DAY_VALUES_CACHE` (53), `_STRICT_OVERLAY_NESTED_KEYS_CACHE` (54), `_STORY_ENTRY_VALIDATOR_CACHE` (55), `_PLAYER_CHARACTER_SCHEMA_KEYS_CACHE` (56), `_SPELL_SLOTS_SCHEMA_CACHE` (438), `_SPELL_SLOTS_READ_ALIASES_CACHE` (439), `_COMMON_FIELD_PATHS_CACHE` (609), `CORRECTION_KIND_BENIGN_NORMALIZE` (896), `CORRECTION_KIND_SCHEMA_WARNING` (897) | Module-level caches/constants used by the helpers above. | Caching + correction-kind vocabulary; no value changed. KEEP. | Accurate. | CONFIRM KEEP (grouped). |
| Module symbols — policy data (all KEEP, grouped with every name listed; run 2 named the caches but did NOT name these — this row closes that coverage gap without changing any verdict): `_LEGACY_CHARACTER_FIELD_ALIASES` (59, frozenset of 12 legacy PCD field names: class_name, spell_slots, conditions, status_effects, personality, backstory, alignment, proficiencies, subclass, player_name, hero_points, inspiration), `_LEGACY_EQUIPMENT_SLOT_ALIASES` (78: weapon_main→main_hand, weapon_secondary→off_hand, mainhand→main_hand, offhand→off_hand, boots→feet, gloves→hands, amulet→neck, necklace→neck), `_LEGACY_EQUIPMENT_SLOT_NAMES` (90: weapon, weapons, ring, ring1, ring2, bracers + alias keys), `_STRICT_RESOURCE_KEYS` (100: gold, hit_dice, spell_slots, class_features, consumables), `_LEGACY_STATE_UPDATE_TOP_LEVEL_KEYS` (110: frozen_plans, rest_taken, action_resolution, reward_event, level_up_selection), `_STRICT_OVERLAY_NESTED_SCHEMA_DEFS` (127: combat_state→CombatState, encounter_state→EncounterState, rewards_pending→RewardsPending, custom_campaign_state→CustomCampaignState) | Used by the alias/strict-overlay helpers. | Backward-compat vocabulary + strict-region gate vocabulary; the functions themselves rewrite nothing (alias tables are read-side; the strict gate only warns/errors as lists). KEEP. | One behavioural note (not a §3 item on its own): the `_LEGACY_STATE_UPDATE_TOP_LEVEL_KEYS` comment accurately explains the near-match trap it prevents (without the allow-list entry, difflib would rename `reward_event` to e.g. `world_events` before it can be recognized) — the comment is evidence FOR the ADAPT above: the allow-list exists to work around the renamer, which is itself the defect. | CONFIRM KEEP (grouped; coverage gap closed). |

### 6. `mvp_site/schemas/__init__.py` (67 lines; 1 AST unit + re-export surface)

Module verdict KEEP (package surface; re-exports change no value). The
re-exported units carry their own rows elsewhere, EXCEPT the re-export
surface itself, rowed here:

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| Re-export surface: `GameStateModel` (from `.game_state_models`), 17 TypedDict names (from `.typed_dicts`), 10 validation helpers (from `.validation`); `__all__` (37) | Bare-package importers: `firestore_service.py:139` (validation as schema_validation), `game_state.py:44` (GameStateModel), plus tests. | Package surface only. KEEP. | Precision run 2 omitted: the surface is PARTIAL — 18 TypedDict classes/aliases are NOT re-exported (see §18 for the set). That is a usability gap, not a verdict change: direct `from .typed_dicts import ...` still works for all of them. | CONFIRM KEEP (with partial-surface note). |

### 7. `mvp_site/schemas/character_creation_wire.py` (266 lines; 19 units: 11 functions + 8 module symbols)

Prod importers: `narrative_response_schema.py:1031–1032,1045` (wire
assembly) and `world_logic.py:214` (`is_complete_character_creation_clock`
only). All rows CONFIRM KEEP.

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `_load_character_creation_wire_schema` (30), `_CHARACTER_CREATION_WIRE_SCHEMA` (38, built via `inline_canonical_defs(..., spell_schema=get_spell_authoring_schema(bounds=False))`), `_CHARACTER_CREATION_WIRE_SCHEMA_PATH` (25), `_LONG_TEXT` (22, 20000), `_NARRATIVE_TEXT` (23, 120000) | Called by the wire builders below. | Schema loading + assembly; the `bounds=False` spell schema is the documented capacity choice (creation authors the strict spell contract without provider maxLength so the modal never truncates authored text, while gameplay/narrative keep theirs). KEEP. | Comment at ~35 accurately states the bounds=False rationale. | CONFIRM KEEP. |
| `CHARACTER_CREATION_CONCLUDE_PCD_FIELDS` (43), `_character_creation_conclude_pcd_schema` (48), `get_character_creation_conclude_json_schema` (71) | Called by NRS wire assembly. | PCD-only conclude envelope; fields reuse active-phase `pcd_properties` verbatim (one source of truth); narrative maxLength = `_NARRATIVE_TEXT` (120000). KEEP. | Docstring accurately says fields reuse active-phase properties verbatim. | CONFIRM KEEP. |
| `is_complete_character_creation_clock` (81) | Prod caller: `world_logic.py:214`. | Draft202012Validator predicate over the conclude envelope's world-time contract. KEEP. | Accurate. | CONFIRM KEEP. |
| `is_complete_character_creation_sheet` (90) | Called by NRS wire assembly / agents paths. | Predicate over the conclude PCD fields. KEEP. | MINOR doc flag (§3): docstring says "contains every canonical PCD field" but the code checks only the 13 `conclude_pcd_fields` — the conclude subset, not every canonical PCD field. | CONFIRM KEEP (+ minor doc flag). |
| `_CHARACTER_CREATION_REVIEW_PCD_FIELDS` (97), `_CHARACTER_CREATION_REVIEW_STAGES` (100), `_CHARACTER_CREATION_PARTIAL_STAGES` (103, derived as `constants.ACTIVE_CHARACTER_CREATION_STAGES - review stages`, sorted) | Used by the review/partial builders. | Stage/field vocabulary for creation phases. KEEP. | Accurate. | CONFIRM KEEP. |
| `_character_creation_equipment_schema` (108), `_character_creation_pcd_schema` (142), `_character_creation_review_pcd_schema` (180), `_character_creation_partial_pcd_schema` (186), `_build_character_creation_active_schema` (207) | Called by the wire assembly + `__getattr__`. | Bounded slot-object equipment contract; typed full-review + nonempty-partial branches; isolated structured-output schema for active creation turns. KEEP. | Accurate. | CONFIRM KEEP. |
| `__getattr__` (261) | Module attribute access for `NARRATIVE_RESPONSE_JSON_SCHEMA_CHARACTER_CREATION`. | Lazy construction on first access (capacity optimization). KEEP. | Accurate. | CONFIRM KEEP. |

### 8. `mvp_site/schemas/character_death_wire.py` (49 lines; 5 units: 3 functions + 2 module symbols)

Prod importer: `narrative_response_schema.py:56` only. All rows CONFIRM
KEEP, with one doc flag.

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `_load_bounded_schema` (33) | Called by both getters. | Loads a deaths/revivals JSON asset, pops `_comment`, applies the caller's string bound only when `maxLength` is absent. Provider-capacity bounding. KEEP. | Accurate. | CONFIRM KEEP. |
| `get_character_deaths_schema` (42), `get_character_revivals_schema` (47), `_CHARACTER_DEATHS_SCHEMA_PATH` (25), `_CHARACTER_REVIVALS_SCHEMA_PATH` (28) | Called by NRS wire assembly. | Wire contracts for deaths/revivals items (JSON-string item shape; server-side parse-back lives in `graveyard_service._coerce_character_death_entries`, outside this area). KEEP. | Doc flag (§3): the module docstring references `mvp_site/schemas/companion_recruitment_wire.py` as the mirrored pattern — THAT FILE DOES NOT EXIST in the local tree (`ls schemas/ | grep -i companion` returns nothing; repo-wide grep for `companion_recruitment_wire` returns only this docstring line). The complexity-ceiling rationale itself (Gemini caps the gameplay schema at 3 array-of-typed-object nodes — `dice_audit_events`, `tool_requests`, `planning_block.choices` — a 4th pushes every gameplay turn over budget into a 400, "rev-cgv7h") is stated as the reason for the JSON-string shape; the ceiling claim itself was NOT independently verified and is reported here as the docstring's claim, not audit-verified fact. | CONFIRM KEEP (+ doc flag). |

### 9. `mvp_site/schemas/conclude_snapshot.py` (84 lines; 8 units: 1 class + 1 classattr + 4 methods + 2 module symbols)

Prod importer: `conclude_invariant.py:22,73,104` only. Module docstring
accurately states the shared-model purpose (level-up + character-creation
conclude domains) and the warn-only `conclude.reconcile_derived_stats`
invariant context; the "House style mirrors entities_pydantic.py" line is
accurate about style, not a behavioural claim.

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `MIN_LEVEL` (21, 1), `MAX_LEVEL` (22, 20) | Used by `ConcludeSnapshot` field bounds. | SRD level bounds. KEEP. | Accurate. | CONFIRM KEEP. |
| `ConcludeSnapshot` class (25, `extra="ignore"`), `model_config` (33) | Constructed by `conclude_invariant.py`. | Carrier for conclude snapshots. KEEP. | Accurate. | CONFIRM KEEP. |
| `_coerce_level` (46) | Field validator for level. | Coerces stringy ints WITHOUT clamping, so `Field(ge=1, le=20)` rejects out-of-range levels including narrative-milestone numbers. Fail-closed shape. KEEP. | Docstring accurately states the fail-closed shape. | CONFIRM KEEP. |
| `_coerce_numeric` (58) | Field validator for `proficiency_bonus` / `max_hp`. | Routes through `DefensiveNumericConverter.convert_value`, so invalid `max_hp` becomes 1 — which then PASSES `Field(ge=1)` — a fabricated valid value on a commit turn. No registered exception. ADAPT: use strict int coercion with a validation error on invalid input; never substitute a default. (This row is part of the defensive-converter deletion consequence: it must be rewritten when that module is deleted.) | Doc flag (§3): docstring ("Defensively coerce stringy ints, mirroring entities_pydantic") understates the default substitution and its interaction with the ge=1 gate. | CONFIRM ADAPT (+ doc flag). |
| `_normalize_class` (66) | Field validator for class. | Strips/lowercases the class identifier, fails closed on missing/blank — storage-integrity behaviour for a commit, not a domain invention. KEEP. | Comment accurately states the reducer cannot recompute derived stats without a class. | CONFIRM KEEP. |
| `_coerce_slots` (79) | Field validator for spell slots. | List/tuple → tuple, structural, values preserved; raises on non-int items rather than inventing — fail-closed, consistent. KEEP. | Accurate. | CONFIRM KEEP. |

### 10. `mvp_site/schemas/defensive_numeric_converter.py` (163 lines; 6 units: 1 class + 3 classattrs + 2 methods)

Module verdict DELETE as a module (run 2 CONFIRMED, consequence
corrected — see §4-C8). Class docstring ("Handles conversion of numeric
fields with fallback defaults for unknown/invalid values. When invalid
values are encountered, logs warnings and uses safe defaults.") is accurate
about behaviour; the behaviour is the defect. THREE prod importers, not
two: `schemas/conclude_snapshot.py:18,62`, `schemas/entities_pydantic.py:16`
(10 call sites: 6 ability converters, 3 HP converters, 1 level converter),
and `world_logic.py:217,300,304,310,334` (xp_gained, gold, current_xp,
xp_to_next_level). Plus: `numeric_field_converter.py`'s docstring pointer
("use DefensiveNumericConverter instead") must be updated, and tests
(`tests/test_defensive_numeric_converter.py`,
`tests/test_defensive_numeric_central_robustness.py`,
`tests/test_architectural_decisions.py:36–38,105–116` which pin
`convert_value("hp", "unknown") == 1`) need rework alongside the code —
the tests pinning the 1-default are evidence the defect is load-bearing in
tests, not evidence it is correct. Draft-amendment note: no model call is
involved (hand-written default/clamp logic on model output values, not a
model output itself), so the draft does not touch these verdicts (§5).

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `convert_value` (78) | Called by conclude_snapshot + entities_pydantic + world_logic (see header). | Substitutes defaults (hp 1, ability 10, xp_to_next_level 300, AC 10 — full table in `FIELD_DEFAULTS` row), extracts the first number from strings like "500 XP" or "10/20" (picking 10 from a fraction, per its own comment), clamps HP to ≥1, non-negatives to ≥0, abilities to 1–30; keys not in `FIELD_DEFAULTS` pass through unchanged. No registered exception, no necessity proof. DELETE (warn + omit on invalid numerics; put integer requirements in prompt/schema). | Docstring accurate about the fallback behaviour; the behaviour is the defect. | CONFIRM DELETE. |
| `convert_dict` (132) | Called by the same importers (dict-level entry point). | Recursively propagates the same inventions; non-dict input passes through unchanged. DELETE. | Accurate. | CONFIRM DELETE. |
| `HP_FIELDS` (18: hp, hp_current, hp_max, level — note: `level` is in HP_FIELDS, so level is clamped to ≥1 by the same path), `NON_NEGATIVE_FIELDS` (19: temp_hp, xp, xp_current, gold, successes, failures, damage, healing, initiative), `ABILITY_SCORE_FIELDS` (30: the six abilities), `FIELD_DEFAULTS` (table: hp 1, hp_current 1, hp_max 1, temp_hp 0, level 1, xp 0, xp_current 0, xp_to_next_level 300, ac 10, armor_class 10, initiative 0, six abilities 10 each, damage 0, healing 0, attack_bonus 0, gold 0, hero_points 0, inspiration_points 0, round_number 1, turn_number 1, session_number 1, successes 0, failures 0) | Used by `convert_value` only. | The invention tables themselves. DELETE with the class (grouped; every name listed). | Accurate as tables of the defaults; the defaults are the defect. | CONFIRM DELETE (grouped). |

### 11. `mvp_site/schemas/entities_pydantic.py` (756 lines; 64 units: 2 functions + 12 classes + 24 classattrs + 26 methods)

Prod importers by import line: `entity_tracking.py:38` only (mentions in
`game_state.py:1253,1287`, `serialization.py:332`,
`conclude_snapshot.py:8,59` are comments/docstrings, not imports). Classes
and enums are KEEP as carriers/vocabularies; their verdicts follow their
validator rows. Verification note (comparison run this review, no drift):
the schema's EntityType enum (`['pc', 'npc', 'creature', 'loc', 'item',
'faction', 'obj']`) matches `entities_pydantic.EntityType`'s seven members
exactly (PLAYER_CHARACTER="pc", NPC="npc", CREATURE="creature",
LOCATION="loc", ITEM="item", FACTION="faction", OBJECT="obj").

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `sanitize_entity_name_for_id` (19) | Called by `create_from_game_state` + entity id construction. | Lowercases/slugifies a name into an entity-ID component (e.g. "Cazador's Spawn" → "cazadors_spawn"); identifier hygiene for durable-write keys; display name preserved separately. KEEP. | Accurate. | CONFIRM KEEP. |
| Enums + members (KEEP as carriers/vocabularies): `EntityType` (52: PLAYER_CHARACTER, NPC, CREATURE, LOCATION, ITEM, FACTION, OBJECT), `CombatDisposition` (64: FRIENDLY, HOSTILE, NEUTRAL), `EntityStatus` (107: CONSCIOUS, UNCONSCIOUS, DEAD, HIDDEN, INVISIBLE, PARALYZED, STUNNED), `Visibility` (119: VISIBLE, HIDDEN, INVISIBLE, OBSCURED, DARKNESS) | Used by `Character` / `CombatState` / `SceneManifest` fields. | Carrier/vocabulary. KEEP (grouped; every member listed). | Accurate. | CONFIRM KEEP (grouped). |
| `CombatDisposition.from_type_string` (84) | Called by entity-type derivation paths. | Run 2: DELETE the hostile default, keep friendly/neutral mappings. CONFIRMED with the same refinement: unknown types must stay unknown (return None / preserve unknown), not default to HOSTILE; the friendly/neutral mappings are alias translations. | Docstring does not flag the hostile default as a judgment; the ADAPT fixes the behaviour. | CONFIRM ADAPT. |
| `Stats` converters (141, 146, 151, 156, 161, 166: strength/dexterity/constitution/intelligence/wisdom/charisma, each routing through `DefensiveNumericConverter.convert_value`) | Field validators on `Stats`. | All six DELETE (same converter defect; use strict int validation + warn). Part of the defensive-converter deletion consequence. | Accurate about conversion; the conversion is the defect. | CONFIRM DELETE (grouped). |
| `Stats.get_modifier` (169) | Called by mechanics/display paths. | SRD modifier `(ability - 10) // 2` on read for display/mechanics; read-only derivation, conditioned on never writing back. KEEP. | Accurate. | CONFIRM KEEP. |
| `Stats` field defaults (strength/dexterity/constitution/intelligence/wisdom/charisma each `Field(ge=1, le=30, default=10)`) — NEW extension to run 2 (run 2 did not row the field defaults) | Construction of `Stats()`. | Construction-time inventions in the same family as the converter's ability→10 default. ADAPT: remove the defaults (required or None) with call-site updates wherever `Stats()` is constructed without abilities. | No docstring flags the defaults as inventions. | ADAPT (new row; not a run-2 contradiction). |
| `HealthStatus.convert_hp` (188), `convert_hp_max` (193), `convert_temp_hp` (198) | Field validators on `HealthStatus`. | All three DELETE (same converter defect; unknown HP → 1). | Accurate about conversion; the conversion is the defect. | CONFIRM DELETE (grouped). |
| `HealthStatus.validate_hp_not_exceed_max` (202) | Field validator on `HealthStatus`. | DELETE: clamps HP to hp_max after conversion — including when conversion itself shrank hp_max to 1, so a healthy character can be rewritten to 1 HP by two stacked server inventions. Surface HP>max as a warning, never rewrite HP. | Accurate about clamping; the clamp is the defect. | CONFIRM DELETE. |
| `HealthStatus` defaults (`temp_hp` 0, `death_saves` {successes 0, failures 0}) | Construction of `HealthStatus()`. | Zero-state defaults, not campaign-fact inventions of the same kind — zero is the absence state for those fields, unlike HP/ability/level defaults which assert a positive state. KEEP. | Accurate. | CONFIRM KEEP. |
| `Location` class (214) + `model_config` (226) | Constructed by entity paths. | Carrier. KEEP. | Accurate. | CONFIRM KEEP. |
| `Character.convert_level` (268) | Field validator on `Character`. | DELETE (routes level through the deleted converter; unknown → 1). | Accurate about conversion; the conversion is the defect. | CONFIRM DELETE. |
| `Character._lineage_is_empty` (272), `Character.synchronize_lineage_aliases` (276), `Character.__setattr__` (294) | Called by Character construction/assignment. | Read-only empty predicate; populated-wins-over-empty alias coherence (two populated but differing values RAISE instead of silently picking one); same empty-never-wins mirroring on assignment. Alias coherence preserving values; storage-integrity behaviour. KEEP (grouped). | Accurate. | CONFIRM KEEP (grouped). |
| `Character.model_config` (436, `use_enum_values=True, validate_assignment=True`) | Class config. | Validation-on-assignment for the carrier. KEEP. | Accurate. | CONFIRM KEEP. |
| `Character.validate_gender` (342) | Field validator on `Character`. | Read in full this review (run 2 ADAPTED on documented intent without a full body re-read; now fully grounded): for NPCs (entity_type NPC, or entity_id starting `npc_`), missing/blank gender RAISES ("Gender is required for NPCs..."), non-string gender RAISES, otherwise returns `v.lower().strip()`; for PCs, gender is optional but must be a string if provided. ADAPT confirmed and now grounded: keep the permissive string check (lower/strip for NPCs, string check for PCs); never raise or default gender — warn and leave None, with the requirement stated in prompt. (The lowercasing itself rewrites the model's casing — minor; the ADAPT's warn-and-leave-None covers it.) | Doc flag (§3): docstring ("Validate gender field for narrative consistency (permissive for LLM creativity)") is MISLEADING — the body is not merely permissive (it raises for NPCs). | CONFIRM ADAPT (+ doc flag). |
| `Character.validate_age` (379) | Field validator on `Character`. | DELETE the raise, confirmed from the full body: raises for non-integer, negative, or >50000 ages (comment: "Fantasy setting allows very old beings"). A fantasy being's age is a model-owned fact and 50000 is an arbitrary server ceiling. ADAPT wording kept from run 2: warn on implausible ages; never reject the entity for age. (The validator function itself is not deleted, only its raise behaviour — same as run 2's ADAPT.) | Comment accurately states the ceiling rationale; the ceiling is the defect. | CONFIRM ADAPT. |
| `Character.validate_mbti` (390), `Character.validate_alignment` (403) | Field validators on `Character`. | Accept any string personality description / alignment, strip whitespace; non-strings raise — permissive strip-only validation preserving the model's description; the non-string raise is a type gate, not a content judgment. KEEP. | Accurate. | CONFIRM KEEP. |
| `Character.validate_entity_type` (416) | Field validator on `Character`. | Derives entity_type from the server-minted entity_id prefix `pc_`/`npc_` when an id is present — derivation from server-owned identifier metadata, not from prose. KEEP. | Accurate. | CONFIRM KEEP. |
| `Character.validate_npc_gender_required` (425) | Field validator on `Character` (NPC path). | DELETE the raise: raises when an NPC lacks gender, listing "Valid options: ['male', 'female', 'non-binary', 'other']" — a closed set that CONTRADICTS `validate_gender`'s permissive "any descriptive value" stance (e.g. 'fluid', 'mixed'). The two validators disagree about whether gender is an open string or a closed set. Fix is the same prompt-owns-requirement change as `validate_gender`. | Doc flag (§3): docstring ("Ensure NPCs have gender field for narrative consistency") understates the closed option list in its error message; the contradiction with `validate_gender` is flagged in §3. | CONFIRM DELETE-the-raise (+ doc flag). |
| `PlayerCharacter` class (439), `NPC` class (451) | Constructed by entity paths. | Carriers; verdicts follow their validator rows, EXCEPT the `PlayerCharacter.experience` default below. KEEP as carriers. | Accurate. | CONFIRM KEEP (carriers). |
| `PlayerCharacter.experience` default_factory `{"current": 0, "to_next_level": 300}` (~444–446) — NEW extension to run 2 | Construction of `PlayerCharacter()`. | Invents `to_next_level: 300`, the same 300 as the converter's `xp_to_next_level` default. ADAPT: remove the invented default (required or None) with call-site updates. | No docstring flags the 300 as an invention. | ADAPT (new row; not a run-2 contradiction). |
| `CombatState.validate_participants` (471), `SceneManifest.validate_present_entities` (510), `SceneManifest.get_expected_entities` (529), `SceneManifest.to_prompt_format` (552) | Called by combat/scene manifest construction. | Internal-consistency gates on server-constructed manifests (turn-order entity missing from participants; present-entity id not among manifest characters) — rejecting a contradictory manifest invents no participant; `get_expected_entities` derives the expected list (visible + conscious + present) the prompt needs to require (prompt-side derivation, judges nothing the model wrote); `to_prompt_format` renders the manifest as prompt text (the Pass A mechanism). KEEP (grouped). | Accurate. | CONFIRM KEEP (grouped). |
| `create_from_game_state` (606–756) | Called by scene-manifest construction from legacy game state. | ADAPT, confirmed with exact lines: builds a SceneManifest from legacy game-state dicts; defensive type handling KEEP, but it INVENTS defaults where state is missing — HP 10 for missing HP (PC and NPC: `pc_data.get("hp_current", pc_data.get("hp", 10))`, same for NPCs), gender `"other"` for missing NPC gender (comment "Required for NPCs, default to 'other' if not specified"), `"Unknown Location"` for missing location (three fallback paths: `game_state.get("location", "Unknown Location")`, dict-extraction fallback, unexpected-type fallback), `present=True` default (`npc_info.get("present", True)`), `conscious=True` default, visible default (`hidden` False → VISIBLE), PC name default `"Unknown"` (which then seeds `pc_unknown_001`-style entity ids). ADAPT: propagate None/unknown explicitly into the prompt instead of inventing 10 / "other" / "Unknown Location" / present-conscious-visible / "Unknown"; keep the defensive type handling. Additional notes: location entity id hardcoded `"loc_default_001"` (server-minted id, acceptable as identifier hygiene, but it asserts a single default location identity — minor note, not a verdict change); NPC ids generated as `npc_{slug}_{idx+1:03d}` when the stored id is missing or fails the `^(pc|npc)_[\w]+_\d{3}$` pattern (identifier hygiene, KEEP); combat state construction uses `round` default 1 (a zero-state default, KEEP). | Doc flag (§3): docstring ("Create a SceneManifest from legacy game state format") says nothing about the invented defaults — the inventions are undocumented, which is itself a §3 note. | CONFIRM ADAPT (+ doc flag). |
| Classes roll-up: `EntityType`, `CombatDisposition`, `EntityStatus`, `Visibility`, `Stats`, `HealthStatus`, `Location`, `Character`, `PlayerCharacter`, `NPC`, `CombatState`, `SceneManifest` | — | KEEP as carriers; the ADAPT/DELETE rows above govern their validators and `create_from_game_state`. | — | CONFIRM KEEP (carriers). |

### 12. `mvp_site/schemas/field_constants.py` (498 lines; 40 dicts) — FILE DELETE (see §4-C2)

Shared rationale (REVERSING run 2's shared KEEP rationale): run 2's claim
was "each dict is a generated mirror... giving code a single spelling
source instead of string literals". That rationale fails on reachability:
the file has ZERO prod readers (proven by repo-wide symbol grep for
`TOP_LEVEL_FIELDS`, `ACTIONRESOLUTION_FIELDS`, `CUSTOMCAMPAIGNSTATE_FIELDS`
and the module name across `mvp_site/` `.py`/`.js` — nothing outside the
file itself plus its own generator docstring; `schemas/__init__.py` does
NOT import it). Only `tests/test_social_hp_attempt_counters_removed.py:8,26`
reads the file's text (for a test), and unrelated test method names mention
"field constants". A name table nobody reads is dead code, however
accurate. Verdict for every dict below: DELETE-with-file (remove the file
from prod; the generator script `scripts/schema/generate_field_constants.py`
remains the source of truth for any future regeneration, which must fix
the drift/allOf gaps first). The file is NOT test-only (tests read its text
only in one test); it is dead prod code — listed in §1, not §2.
Drift notes below are the reason regeneration (not reuse) would be
required if a future consumer appears. All dicts are named (grouped-row
rule satisfied by the full enumeration here; drifted/empty dicts get
individual notes).

| Dict (line) | Drift / content note | Verdict |
|---|---|---|
| `TOP_LEVEL_FIELDS` (13) | Matches the 39 top-level properties — verified by script, no drift. | DELETE-with-file (dead, not wrong). |
| `ACTIONRESOLUTION_FIELDS` (56) | No drift found. | DELETE-with-file. |
| `ACTIONRESOLUTIONROLL_FIELDS` (65) | DRIFT: missing `challenge_npc_id` (schema gained it after last regeneration). | DELETE-with-file (drifted + dead). |
| `ARCMILESTONE_FIELDS` (82), `CAMPAIGNTIER_FIELDS` (91), `CHAPTERDATA_FIELDS` (94), `CHARACTER_FIELDS` (100; 46 keys, matches Character direct properties), `COMBATSTATE_FIELDS` (149), `COMBATANTSTATE_FIELDS` (165), `COMPANIONARC_FIELDS` (176) | No drift found. | DELETE-with-file. |
| `CUSTOMCAMPAIGNSTATE_FIELDS` (183) | DRIFT: missing `directives`, `living_world_conflict_profile`. | DELETE-with-file (drifted + dead). |
| `ENCOUNTERSTATE_FIELDS` (227), `ENTITYSTATUS_FIELDS` (240), `ENTITYTYPE_FIELDS` (243), `FACTIONMINIGAME_FIELDS` (246), `FACTIONRESOURCES_FIELDS` (257), `FACTIONUNITS_FIELDS` (262), `GODMODEDIRECTIVE_FIELDS` (269), `GRAVEYARDENTRY_FIELDS` (274), `HEALTHSTATUS_FIELDS` (284), `INJURY_FIELDS` (294), `LEGACYINITIATIVEENTRY_FIELDS` (305), `LEVELUPSESSION_FIELDS` (311), `LOCATION_FIELDS` (321) | No drift found. | DELETE-with-file. |
| `NPC_FIELDS` (332) | EMPTY dict (`{}`) — allOf gap: the generator cannot represent allOf, so the combined Character (46) + own fields (faction, role, attitude_to_party, tier) are entirely absent. | DELETE-with-file (empty + dead). |
| `PLANNINGBLOCK_FIELDS` (335) | DRIFT: missing `analysis` (note: `PlanningBlockDict` in typed_dicts DOES include `analysis` — the two generated files were regenerated at different times). | DELETE-with-file (drifted + dead). |
| `PLANNINGCHOICE_FIELDS` (344), `PLANNINGCHOICELEGACY_FIELDS` (356) | No drift found. | DELETE-with-file. |
| `PLAYERCHARACTER_FIELDS` (367) | EMPTY dict (`{}`) — allOf gap, same as NPC_FIELDS (Character 46 + own fields including player_name, experience, and more). | DELETE-with-file (empty + dead). |
| `RESOURCEENTRY_FIELDS` (370) | No drift found. | DELETE-with-file. |
| `RESOURCEREGISTRY_FIELDS` (381) | EMPTY but CORRECT — ResourceRegistry has no fixed properties (only `additionalProperties: ResourceEntry`), so empty is correct here. | DELETE-with-file (correct but dead). |
| `REWARDSPENDING_FIELDS` (384), `SANCTUARYMODE_FIELDS` (400) | No drift found. | DELETE-with-file. |
| `SOCIALHPCHALLENGE_FIELDS` (414) | DRIFT: lists the 17 own-branch fields but misses `objective_continues` (the `SocialHPContinuity` allOf branch, whose only property is `objective_continues`). | DELETE-with-file (drifted + dead). |
| `STATS_FIELDS` (434), `STORYENTRY_FIELDS` (443), `VISIBILITY_FIELDS` (463), `WORLDDATA_FIELDS` (466), `WORLDEVENT_FIELDS` (476), `WORLDTIME_FIELDS` (489) | No drift found. | DELETE-with-file. |

Lens B for this file: the header docstring ("Auto-generated field name
constants from game_state.schema.json / DO NOT EDIT - This file is
generated by: python scripts/schema/generate_field_constants.py / Run this
script after modifying the schema to regenerate constants") is accurate
about provenance but FALSE as a completeness claim after the drift above
(the file was evidently NOT regenerated after the schema gained
`challenge_npc_id`, `directives`, `living_world_conflict_profile`,
`analysis`, and the generator cannot represent allOf at all). Flagged in
§3 as stale-generated-output (the docstring's implied "run the script and
you are in sync" no longer holds for these dicts). Zero consumers for the
drifted dicts outside the file itself (verified) — so the drift is
currently latent, not live under-allowlisting. This supports the
file-DELETE verdict rather than an urgent fix.

### 13. `mvp_site/schemas/game_state_models.py` (51 lines; 5 units) — all CONFIRM KEEP

Prod importer: `schemas/__init__.py` only (then via package by
`game_state.py`, `firestore_service.py`).

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `_load_schema` (30), `_SCHEMA_PATH` (27), `_schema` (37, import-time loaded schema verifying the file exists and parses) | Called at import time. | Loads the canonical JSON schema at import time. Transport. KEEP. | Docstring "Load the canonical JSON Schema at import time" accurate. | CONFIRM KEEP. |
| `GameState` class (40), `model_config` (51) | Imported via `schemas/__init__.py` as `GameStateModel`. | Dynamic Pydantic model generated from the canonical schema, solely for `to_model()`/`from_model()` round-trip serialization with `extra="allow"`; performs NO validation (real validation is `validate_game_state`). KEEP. | Docstring explicitly says it performs NO validation and real validation is `validate_game_state` — verified accurate. The docstring's history note (previously 1100+ static lines via datamodel-codegen that diverged, e.g. level capped at 20, Stats `extra="forbid"`, Experience rejecting legacy int format) is a historical claim that was NOT independently verified — reported here as the docstring's claim, not audit-verified fact; not flagged as stale without contrary evidence. | CONFIRM KEEP. |

### 14. `mvp_site/schemas/gemini_schema_acceptance.py` (42 lines; 4 units) — all CONFIRM KEEP, with doc flags

Prod importer: `llm_providers/gemini_provider.py:105`
(`schema_fingerprints`) plus acceptance tests
(`tests/test_gemini_schema_acceptance_manifest.py`, `..._probe.py`,
`..._write_guard.py`).

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `schema_fingerprints` (18) | Called by `gemini_provider.py:105`. | Maps schema name to sha256 of canonical JSON with `sort_keys=True, separators=(",", ":")`; acceptance bookkeeping for provider transport; output shape matches the manifest's `schemas` values. KEEP. | Accurate. | CONFIRM KEEP. |
| `gemini_schema_acceptance_requests` (28) | Called by acceptance probing paths. | Describes every acceptance request: schema + models + code-execution flag, disabled for WORLD_SIM lanes — verified: the loop sets `enable_code_execution = False` for names starting `WORLD_SIM_`, matching the manifest's 4 False flags. KEEP. | Doc flag (§3): the "Describe every Gemini schema acceptance request" docstring + the "Live schema acceptance is only ever sent to Gemini 3.8 Flash or later" comment OVERSTATE the current function: the manifest's own acceptance history includes `gemini-3.5-flash-lite` and `gemini-3-flash-preview` cells with verdict accepted, while the function builds `models: (ACCEPTANCE_MODEL,)` only. The "only ever" claim is false as a historical statement; the function is 3.8-only as a current statement. | CONFIRM KEEP (+ doc flag). |
| `ACCEPTANCE_MODEL` (13, `"gemini-3.8-flash"`), `MANIFEST_PATH` (15, beside the `.py` file) | Used by the two functions above. | Transport configuration + manifest path. KEEP. | Accurate as configuration (the "only ever" comment attached to ACCEPTANCE_MODEL is the §3 flag above, not a separate item). | CONFIRM KEEP. |

### 15. `mvp_site/schemas/narrative_wire_fields.py` (91 lines; 4 functions) — all CONFIRM KEEP

Prod importer: `narrative_response_schema.py:60` only.

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `validate_conflict_signal` (14), `validate_episode_transition` (26) | Called by NRS wire validation. | Preserve a model-owned conflict/episode signal when its wire type is a string, return None otherwise; the warning log on drop is diagnostics. KEEP. | Docstrings accurate ("Preserve the model-owned conflict signal when its wire type is valid"). | CONFIRM KEEP. |
| `validate_canonical_action_basis` (38) | Called by NRS wire validation. | Enforces the wire shape of the typed citation: non-empty `tool_call_id`, non-empty `tool_name`, optional `target_entity_id`; shape gate protecting an authorization-adjacent guard whose allowlist/invocation check lives in `world_sim.timeline.lethal_policy` — it judges shape, not whether the claim is true. KEEP. | Docstring accurate. | CONFIRM KEEP. |
| `coerce_bool_optional` (78) | Called by NRS bool coercion paths. | Best-effort bool conversion returning None when unclear — the strict-compliant shape the two in-module NRS bool coercers should match. KEEP. | Docstring accurate. | CONFIRM KEEP. |
| Module docstring | — | "Pure wire-field helpers split out of narrative_response_schema.py. Houses the timeline signal validators and small stateless coercion helpers so the schema module stays under its line ceiling." The "pure/stateless" part is accurate; the "line ceiling" rationale states no ceiling value anywhere in the repo (NRS is 7,394 lines regardless) — an unverifiable rationale, noted here as a minor §3 note at most, not a §3 headline. | Minor note only. | CONFIRM KEEP. |

### 16. `mvp_site/schemas/prompt_generator.py` (218 lines; 7 functions) — all CONFIRM KEEP, one minor doc note

Prod importer: `agent_prompts.py:54` only (plus prompt/schema tests).

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `_gather_properties` (11) | Called by the documentation generators. | Recursively gathers properties resolving allOf/refs, cycle-safe via visited ids. KEEP. | Minor §3 precision note: docstring ("resolving allOf/refs") slightly overstates — it resolves refs inside `allOf` entries, but a top-level `$ref` on `schema_part` itself is NOT resolved (it would return only its own `properties`, i.e. none). | CONFIRM KEEP (+ minor doc note). |
| `resolve_refs` (32) | Called by documentation generators. | Follows `$ref` to definitions; returns the schema unchanged when the ref is unresolvable — fail-open on unknown refs, which is documentation-generation behaviour, not turn behaviour. KEEP. | Accurate. | CONFIRM KEEP. |
| `_infer_property_type` (51), `generate_type_markdown` (69), `generate_schema_documentation` (126), `get_schema_instructions` (166), `get_schema_fields_instructions` (189) | Called by `agent_prompts.py` (`get_schema_instructions`) + tests. | User-facing type label when `type` is omitted; markdown rendering of one schema type; full markdown document from a JSON schema file; retrieval for one schema type or Root (the function `agent_prompts` calls); rendering for selected fields (field selection for docs is not filtering of model output). KEEP (grouped; every name listed). | Accurate. | CONFIRM KEEP (grouped). |
| Module docstring | — | "(ADR-0003 Phase 4, Commit 10)" is a historical reference that was NOT verified — reported as uncorroborated, not flagged as stale without contrary evidence. | Uncorroborated, not stale. | CONFIRM KEEP. |

### 17. `mvp_site/schemas/reward_event_schema.py` (102 lines; 6 units) — all CONFIRM KEEP, one typo note

Prod importers: `firestore_service.py`, `llm_providers/agy_provider.py`,
`llm_providers/provider_utils.py`, `narrative_response_schema.py`,
`rewards_engine.py`.

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `REWARD_EVENT_XP_SCHEMA` (20) | Used by `REWARD_EVENT_SCHEMA` + provider schema assembly. | State-owned XP receipt sub-schema: gained ≥ 0, tier enum from constants. Comment accurately explains why the tier is enumerated not free-string — an unconstrained tier let the model emit "standard", which Rule 7 then rejected, dropping the whole turn; both vocabularies come from constants so schema and validator cannot drift. Comment also accurately notes curve/before/after/next/crossed are omitted because the model emits only gained/tier and those fields are server-derived by `rewards_engine.py`, never read from the model. KEEP. | Accurate. | CONFIRM KEEP. |
| `STATE_UPDATES_DESCRIPTION` (58) | Used by NRS, provider_utils, agy_provider. | Single shared `state_updates` description across providers, preventing wording drift. KEEP. | §3 minor typo: it reads "Ordinary award decisions use reward_event.xp.gained and xp.tier" — the second reference is missing its `reward_event.` prefix (should read `reward_event.xp.tier` for parallelism). Genuine doc typo in a shared contract string. | CONFIRM KEEP (+ typo flag). |
| `REWARD_EVENT_SCHEMA` (69) | Used by provider schema assembly + rewards validation. | Full state-owned reward receipt: source/source_id/label/justification/xp, all required, no extra properties; zero-reward turns emitted explicitly with null source/source_id/label and xp.tier 'none', never omitted; God Mode omits reward_event for pure administrative corrections — the description text inside the schema states this accurately. KEEP. | Accurate. | CONFIRM KEEP. |
| `SHORT_TEXT` (9, 500), `LONG_TEXT` (10, 20000), `MAX_SAFE_XP` (11, 2^53 − 1) | Used by the schemas above. | Provider length bounds, safe-integer XP ceiling, bounded capacity. KEEP. | Accurate. | CONFIRM KEEP. |
| Module docstring + "source is deliberately unconstrained" comment | — | "State-owned `reward_event` structured-output schema" — accurate. The "source is deliberately unconstrained — backend validation checks existence/non-forgery only, never exact-category correctness (2026-08-30 ruling)" comment is a design claim that was NOT independently verified — reported as the comment's claim. | Uncorroborated, not stale. | CONFIRM KEEP. |

### 18. `mvp_site/schemas/social_hp_challenge.py` (142 lines; 7 units: 5 module symbols + 2 functions)

Prod importers by import line: `game_state.py:45`
(`canonical_enum_spelling`) and `narrative_response_schema.py:70` (F401
import of the vocabularies + `_validate_social_hp_challenge`). Other files
mentioning it (agent_prompts, backend_adjustment_specs, constants,
dice_integrity, game_state_merge, llm_parser, llm_providers/agy_provider)
were name matches, not verified import lines — not overclaimed here.

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `canonical_enum_spelling` (53) | Prod caller: `game_state.py:45`. | Returns the schema enum spelling of a case/whitespace variant, else the raw value; spelling canonicalization preserving the chosen member is not a semantic change. KEEP. | Docstring accurate. | CONFIRM KEEP. |
| `_validate_social_hp_challenge` (61) | Called by NRS social-HP validation. Read in full. | ADAPT: preserve-or-omit + warn on null/invalid numbers; keep spelling canonicalization and warn-only range/enum checks; the `successes_needed=5` default moves to the prompt contract. Evidence: integer coercions default present-but-null/invalid values to 0 (`social_hp`, `social_hp_max`, `cooldown_remaining`, `social_hp_damage`, `successes`, `roll_result`, `roll_dc`) and `successes_needed` to 5; the final filter `{k: v for k, v in validated.items() if k in data}` means OMITTED keys are not filled — only present keys are defaulted. The PROVEN roll-attribution spec (`social_hp.executed_roll_attribution`, specs:2637) covers executed rolls from `dice_integrity`, not these defaults. | Doc flag (§3): the function docstring ("Validate supplied Social HP fields without filling omitted patch keys") CONTRADICTS the in-body comment ("Required fields with defaults"). The truth, verified above, is narrower than either: it fills PRESENT-but-null/invalid keys with defaults, and does NOT fill omitted keys (the final filter drops them). Both wordings are misleading in opposite directions; the docstring is the one to fix (it should say "without filling omitted keys, but defaulting present-but-invalid keys" — which is exactly what the ADAPT removes). | CONFIRM ADAPT (+ doc flag). |
| `VALID_SOCIAL_HP_STATUS` (17), `VALID_SOCIAL_HP_REQUEST_SEVERITY` (22), `VALID_SOCIAL_SKILLS` (30), `VALID_NPC_TIERS` (39), `SOCIAL_HP_MAX_RANGES` (45) | Used by `_validate_social_hp_challenge` + NRS. | Warn-reference only; schema/constant-derived; the enforced clamp in `preventive_guards` is out of scope and is NOT rescued by this row. KEEP (grouped; every name listed). | Notes: the `or` fallbacks for severity/skills are accurately commented as covering only a schema that loads without the enum (a schema LOAD failure raises out of the getter, so it is not a load-failure path); `SOCIAL_HP_MAX_RANGES` is accurately commented as sourced from `constants.SOCIAL_HP_TIER_MAX_RANGES` plus compound tier keys (`god_primordial`, `king_ancient`, `lord_general`). | CONFIRM KEEP (grouped). |

### 19. `mvp_site/schemas/typed_dicts.py` (481 lines; 43 units: 35 classes + 8 module aliases)

Shared rationale (run 2's, confirmed for the 35 classes): every class is
a `TypedDict` with `total=False` — static typing only, zero runtime
behaviour, generated from the canonical schema so types cannot drift from
it. The model/log/prompt/schema do not need them at runtime — which is
precisely why they cost nothing under Pass B: they filter nothing. All 35
classes KEEP (every name listed in the grouped row below), EXCEPT the
allOf cases in the ADAPT rows. Callers: `schemas/__init__.py` only (17
names re-exported; the rest are directly importable but have no prod
importers — that is fine for types: zero runtime cost, and the audit
spec's unreferenced rule is about executable code, so the unimported
TypedDicts are NOT verdicted as dead; this reasoning is stated explicitly
to avoid a misreading of the file-DELETE logic applied to
`field_constants.py`). Generator gap (proven): the generator script
`scripts/generate_typeddict.py` does NOT mention `allOf` (grep returns
nothing) — same gap as `field_constants.py`'s generator.

| Unit | Callers / entry evidence | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| 35 TypedDict classes (KEEP as types; every name listed): `StatsDict`, `HealthStatusDict`, `InjuryDict`, `LocationDict`, `FactionUnitsDict`, `ResourceEntryDict`, `FactionResourcesDict`, `CompanionArcDict`, `GodModeDirectiveDict`, `ArcMilestoneDict`, `ChapterDataDict`, `GraveyardEntryDict`, `LevelUpSessionDict`, `CombatantStateDict`, `LegacyInitiativeEntryDict`, `EncounterStateDict`, `RewardsPendingDict`, `WorldEventDict`, `WorldTimeDict`, `SocialHPContinuityDict`, `ActionResolutionRollDict`, `PlanningChoiceDict`, `PlanningChoiceLegacyDict`, `SanctuaryModeDict`, `SpellDict`, `FactionMinigameDict`, `CombatStateDict`, `WorldDataDict`, `SocialHPChallengeDict` (see ADAPT row — NOT covered by this KEEP row), `ActionResolutionDict`, `PlanningBlockDict`, `CharacterDict` (322, 46 annotations, matching Character's direct properties), `CustomCampaignStateDict`, `StoryEntryDict`, `GameStateDict` (441, matches the 39 top-level properties exactly, verified) | `schemas/__init__.py` re-exports 17 of these; the rest are directly importable. | Static typing only, zero runtime behaviour. KEEP (grouped; every name listed; `SocialHPChallengeDict` is EXCLUDED from this row and rowed separately below). | Field comments in the generated output (e.g. `HealthStatusDict`'s "Legacy current HP alias; use health.hp for new campaigns") are schema-derived and accurate as far as they go. | CONFIRM KEEP (grouped, except SocialHPChallengeDict). |
| `SocialHPChallengeDict` (300) | Re-exported by `schemas/__init__.py`. | ADAPT: currently an EMPTY TypedDict (0 annotations) while the schema has 18 fields via allOf; as written it types nothing and misleads any consumer into thinking the shape is empty. Fix the generator to flatten allOf, or delete the class until it can be generated correctly. | File header completeness claim fails for this class (see header doc flag below). | ADAPT (generator fix; not a run-2 contradiction — run 2 did not field-check this class). |
| `NPCDict` (437), `PlayerCharacterDict` (439) | Re-exported by `schemas/__init__.py`. | ADAPT: currently bare `Any` aliases with NO explanatory comment — they are not TypedDicts at all, so the file header's "AUTO-GENERATED" completeness claim fails for them. Fix the generator to emit real allOf-flattened TypedDicts, or annotate the aliases as intentional fallbacks with a comment explaining the allOf limitation. Note: `__init__.py` importing these names does NOT fail, because the `Any` aliases exist (verified by standalone importlib load: `hasattr(m, "NPCDict")` is True) — no import failure is claimed. | Doc flag (§3): the bare aliases carry no comment at all, which is the specific doc gap; the header claim is the general one. | ADAPT (generator fix or documented fallback; not a run-2 contradiction). |
| Aliases (KEEP as written, with accurate typing semantics): `EntityTypeDict = str` (37), `EntityStatusDict = Any` (39), `VisibilityDict = str` (41), `CampaignTierDict = str` (103), `SocialHPActiveResponseContractDict = Any` (198), `ResourceRegistryDict = dict[str, ResourceEntryDict]` (261) | Used by the TypedDict classes above. | Honest `Any` fallbacks for non-object schema shapes (EntityStatus is an anyOf; the ActiveResponseContract is a contract fragment, not an object schema) — unlike the NPC/PC aliases, these are NOT allOf-flattening failures, so they stay KEEP. This distinction is stated explicitly; do not lump all `Any` aliases together. KEEP (grouped; every name listed). | Accurate as typing semantics. | CONFIRM KEEP (grouped). |
| File header docstring | — | "AUTO-GENERATED from game_state.schema.json / DO NOT EDIT MANUALLY - regenerate with scripts/generate_typeddict.py" — accurate about provenance but misleading about completeness for the three allOf cases above. Flagged in §3. | Header completeness claim fails for SocialHPChallengeDict, NPCDict, PlayerCharacterDict. | Header flagged in §3; class verdicts above. |
| Non-re-exported TypedDict classes/aliases (usability note, NOT a verdict): ActionResolutionRollDict, ArcMilestoneDict, ChapterDataDict, CombatantStateDict, CompanionArcDict, FactionMinigameDict, FactionResourcesDict, FactionUnitsDict, GodModeDirectiveDict, GraveyardEntryDict, InjuryDict, LegacyInitiativeEntryDict, PlanningChoiceDict, PlanningChoiceLegacyDict, ResourceEntryDict, SanctuaryModeDict, SocialHPContinuityDict, SpellDict, StoryEntryDict, WorldEventDict | No prod importers (direct import only). | Zero runtime cost; directly importable. No verdict change (see header reasoning). The set is stated here; the count is the size of this set (recount from the set, not from a separately stated number). | — | No verdict change. |

### 20. Other JSON data files (19 files; `game_state.schema.json` and `gemini_schema_acceptance.json` have their own sections below)

All rows KEEP: these are response-schema data, wire contracts, prompt-side
data, or capacity/policy configuration — none of them filters model output
at runtime. Section detail is stated per file so the unit is judged by its
contents, not as a blanket.

| File | Sections / content | Lens A | Lens B | Run-2 verdict → review verdict |
|---|---|---|---|---|
| `character_creation_wire_schema.json` (7,512 bytes) | Keys: `_comment`, `pcd_properties` (20), `review_pcd_fields` (14), `conclude_pcd_fields` (13), `conclude_pcd_additional_properties` (bool), `review_stages` (2), `planning_block` (4), `conclude_envelope` (4), `state_updates` (4), `top_level_required` (3), `review_pcd_additional_properties` (bool), `partial_pcd_additional_properties` (bool). | Externalized creation wire contract assembled by `character_creation_wire.py`. KEEP. | Minor data-hygiene note (not a verdict change): the creation loader (`character_creation_wire.py:30`) returns the raw JSON and `inline_canonical_defs` (`validation.py:228–267`) deep-copies all keys without stripping `_comment` — so `_comment` survives into `_CHARACTER_CREATION_WIRE_SCHEMA`, unlike `character_death_wire.py` which pops it. Providers ignore unknown top-level keys, so this is hygiene, not a defect. | CONFIRM KEEP (+ hygiene note). |
| `character_deaths_schema.json` (2,392 bytes) | `_comment`, type, description, items (2 keys). | Deaths wire contract (JSON-string item shape; parse-back in `graveyard_service`). KEEP. | Description accurate. | CONFIRM KEEP. |
| `character_revivals_schema.json` (742 bytes) | Same shape as deaths. | Revivals wire contract. KEEP. | Accurate. | CONFIRM KEEP. |
| `criterion4_transport_canary_input.schema.json` (229 bytes) | type, properties (1), required (1), additionalProperties (bool). | Test fixture / canary input schema; no player-path effect. KEEP. | Accurate. | CONFIRM KEEP. |
| `custom_campaign_state_core_memories.schema.json` (1,426 bytes) | type, description, properties (3). | Core-memories mutation contract. KEEP. | Accurate. | CONFIRM KEEP. |
| `field_ownership_registry.json` (4,988 bytes) | version (int), domains (6). | KEEP as test-pinned documentation ONLY: NO prod readers found, only tests (`test_field_ownership_registry.py`, `test_schema_strictness.py`); it enforces nothing at runtime and proves no exception. Do NOT upgrade it to a live verdict on the strength of its content; do NOT delete it either, since tests pin it. Distinction from `field_constants.py` (stated explicitly so the two verdicts do not look inconsistent): the registry is a small, current ownership document whose tests assert its CONTENT; the constants file is a 40-dict generated mirror whose tests only read its TEXT in one test and whose content is stale/drifted. If the parent agent disagrees with that distinction, it is a judgment call to record, not a hidden inconsistency. | Accurate as an ownership document. | CONFIRM KEEP (as test-pinned documentation). |
| `gameplay_state_patch.json` (7,622 bytes) | 5 sections: npc_data (3), core_memories (5), custom_campaign_state (4), world_event_effects (3), world_sim_schedule_date (3). | Gameplay patch contracts projected by the gameplay response schema; schema data. KEEP. | Accurate. | CONFIRM KEEP. |
| `level_up_grant_schema.json` (2,465 bytes) | type, description, properties (6), required (6), additionalProperties (bool). | Level-up grant wire contract. KEEP. | Accurate. | CONFIRM KEEP. |
| `level_up_selection.schema.json` (715 bytes) | type, description, properties (2), additionalProperties (bool). | Level-up selection wire contract. KEEP. | Accurate. | CONFIRM KEEP. |
| `npc_patch_transport.schema.json` (1,278 bytes) | properties (1), required (4). | NPC patch transport contract; framed-patch decoding lives in `_coerce_npc_update_entry` (KEEP). KEEP. | Accurate. | CONFIRM KEEP. |
| `prompt_reminder_registry.json` (10,834 bytes) | version (int), header (list, 4), reminders (dict, 5), `unaudited_wired_builders` (list, 5). | Prompt-side data feeding prompt assembly, not output filtering. KEEP. | Note (not a verdict change): the `unaudited_wired_builders` key name itself flags 5 builders as unaudited — a prompt-assembly hygiene note for the agents-prompts area; the builders themselves are out of this area's file list and are not verdicted here. | CONFIRM KEEP (+ hygiene note). |
| `prompt_tool_contracts.json` (9,877 bytes) | manifest_version (str), contracts (list, 37). | Prompt tool-contract manifest for prompt assembly. KEEP. | Accurate. | CONFIRM KEEP. |
| `reward_acquisition.schema.json` (4,714 bytes) | properties (1), required (1), anyOf (4). | Reward-acquisition wire contract. KEEP. | Accurate. | CONFIRM KEEP. |
| `scene_illustration_policy.json` (1,031 bytes) | version, image_provider, cadence_scenes, min_user_scene_number, openrouter (6), openrouter_provider_routing (3), max_prompt_chars, provider_timeout_seconds, gcs_path_prefix, brief (5), debug_image_tools (6). | Capacity/policy configuration for a non-text tool path, not campaign filtering. KEEP. | Accurate. | CONFIRM KEEP. |
| `spell_slots_schema.json` (647 bytes) | `_comment`, legacy_read_aliases (9), valid_levels (9). | Spell-slot contract that `validation.py` derives read aliases and valid levels from. KEEP. | Accurate. | CONFIRM KEEP. |
| `user_portrait_policy.json` (2,336 bytes) | version, image_provider, preview limits, openrouter (6), openrouter_provider_routing (3), xai (7), timeouts, avatar limits. | Capacity/policy configuration, not campaign filtering. KEEP. | Accurate. | CONFIRM KEEP. |
| `world_sim_background_routine.schema.json` (4,927 bytes) | $schema, type, additionalProperties (bool), required (1), properties (1). | World-sim background-routine wire contract; under §6(3) this is the shape the async tick's output must satisfy. KEEP. | Accurate. | CONFIRM KEEP. |
| `world_sim_relevance_highlights.schema.json` (1,340 bytes) | type, properties (1), required (1), additionalProperties (bool). | World-sim relevance-highlights wire contract. KEEP. | Accurate. | CONFIRM KEEP. |
| `world_sim_setup.schema.json` (1,638 bytes) | type, additionalProperties (bool), required (2), properties (2). | Fresh-roster canonical form that `load_world_sim_setup_schema` derives variants from. KEEP. | Accurate. | CONFIRM KEEP. |

### 21. `mvp_site/schemas/game_state.schema.json` — judged `$def` BY `$def` (42 `$defs` + 1 envelope unit)

Top-level keys: `$schema`, `$id`, `title` ("GameState"), `description`
("Complete game state schema for WorldArchitect.AI tabletop RPG platform"),
`type`, `$defs`, `properties` (39 keys), `required`
(`game_state_version`, `session_id`, `turn_number`). All `$def` verdicts
KEEP: this file IS the canonical contract; deleting a `$def` deletes the
schema mechanism itself. Description gaps are §3 docs items, not verdict
changes. `typed_dicts.py` classes match their `$def` direct properties
with ZERO mismatches (direct-property comparison, script-verified) — the
`field_constants.py` drift is the exception, not the rule.

| `$def` | Shape / required | Description? | Verdict |
|---|---|---|---|
| Stats | object, 6 properties (the six abilities) | Yes | KEEP |
| HealthStatus | object, 7 properties; required hp, hp_max | Yes | KEEP |
| Injury | object, 8 properties; required id, name, type | Yes | KEEP |
| EntityType | string enum: pc, npc, creature, loc, item, faction, obj | Yes | KEEP (matches `entities_pydantic.EntityType` exactly — verified this review) |
| EntityStatus | anyOf (string enum + null handling) | Yes | KEEP |
| Visibility | string enum: visible, hidden, invisible, obscured, darkness | Yes | KEEP |
| Character | object, 46 properties; required [] with minProperties 1 | Yes | KEEP |
| PlayerCharacter | allOf: Character + own branch (player_name, experience — legacy int AND modern object forms, object form requires current — plus more) | Yes | KEEP |
| NPC | allOf: Character + own branch (faction, role, attitude_to_party — default "neutral" — tier) | Yes | KEEP |
| Location | object, 8 properties; required entity_id, display_name | Yes | KEEP |
| FactionUnits | object, 4 properties | Yes | KEEP |
| ResourceEntry | object, 8 properties; required current (+ dependentRequired) | Yes | KEEP |
| ResourceRegistry | object, NO fixed properties (only additionalProperties: ResourceEntry) | Yes (about LLM-defined resources) | KEEP (its empty field-constants dict is correct — see §12) |
| FactionResources | object, 2 properties | Yes | KEEP |
| FactionMinigame | object, 8 properties | Yes | KEEP |
| CompanionArc | object, 4 properties | NO `$def` description | KEEP (+ §3 desc gap) |
| GodModeDirective | object, 2 properties; required rule | Yes | KEEP |
| ArcMilestone | object, 6 properties; required status | Yes | KEEP |
| ChapterData | object, 3 properties | Yes | KEEP |
| CampaignTier | string enum: mortal, divine, sovereign | Yes | KEEP |
| GraveyardEntry | object, 7 properties; required name, entity_id | Yes | KEEP |
| CustomCampaignState | object, 43 properties; additionalProperties: true | Yes | KEEP |
| LevelUpSession | object, 7 properties; required from_level, source | Yes | KEEP |
| CombatantState | object, 8 properties | Yes | KEEP |
| LegacyInitiativeEntry | object, 3 properties | Yes | KEEP |
| CombatState | object, 13 properties | Yes | KEEP |
| EncounterState | object, 10 properties | Yes | KEEP |
| RewardsPending | object, 13 properties | Yes | KEEP |
| WorldEvent | object, 10 properties | NO `$def` description | KEEP (+ §3 desc gap) |
| WorldTime | object, 8 properties | Yes | KEEP |
| WorldData | object, 7 properties | Yes | KEEP |
| SocialHPContinuity | object, 1 property (objective_continues) | Yes | KEEP |
| SocialHPActiveResponseContract | Contract fragment ONLY: NO type, NO properties; compact_omit_response_properties ["god_mode_response", "directives"]; required [objective_continues, social_hp, social_hp_max, successes, successes_needed, status]; narrative_description_suffix ("For an active Social HP challenge, this required field MUST contain nonblank narrative text and include the Social Skill Challenge box unless the linked NPC dies; on the death turn, set `social_hp_challenge` to null and show no box.") | NO description | KEEP (+ §3 desc/structure gap: a fragment, not an object schema — this is why `SocialHPActiveResponseContractDict = Any` is an honest fallback, §19) |
| SocialHPChallenge | allOf: SocialHPContinuity + own branch (17 properties; tier enum including compound keys commoner/merchant/guard/noble/knight/lord/general/king/ancient/god/primordial/lord_general/king_ancient/god_primordial) — 18 fields total via allOf | Yes | KEEP |
| ActionResolution | object, 6 properties; required reinterpreted, audit_flags | Yes | KEEP |
| ActionResolutionRoll | object, 15 properties; required notation, rolls, result, success | Yes | KEEP |
| StoryEntry | object, 17 properties; required actor, text, timestamp, part | Yes | KEEP |
| PlanningChoice | object, 9 properties; required id, text, description, risk_level | Yes | KEEP |
| PlanningChoiceLegacy | object, 8 properties; required text, description, risk_level (no id) | Yes | KEEP |
| SanctuaryMode | object, 11 properties | Yes | KEEP |
| Spell | object, 3 properties; required name | Yes | KEEP |
| PlanningBlock | object, 7 properties; required thinking, choices | Yes | KEEP |
| Envelope (top-level) | 39 properties; required game_state_version, session_id, turn_number; title + description present | Top-level description present | KEEP (+ §3: top-level planning_block, social_hp_challenge, action_resolution have no descriptions; 97 `$def` properties lack descriptions — grouped §3 item, not 100 items) |

### 22. `mvp_site/schemas/gemini_schema_acceptance.json` (1,263,368 bytes) — judged ENTRY BY ENTRY

Top-level keys: `incremental_acceptance`, `models`, `request_code_execution`,
`schemas`, `verified_at` ("2026-10-28T07:07:34.720516+00:00"). `models`:
gemini-3.8-flash, gemini-3.5-flash-lite, gemini-3-flash-preview. `schemas`:
42 fingerprint entries (sha256 strings, not schemas themselves).
`request_code_execution`: 42 flags, EXACTLY the same key set as `schemas`
(no schemas-only or request-only keys). Code-execution False for exactly 4
WORLD_SIM names (`WORLD_SIM_BACKGROUND_ROUTINE`,
`WORLD_SIM_RELEVANCE_HIGHLIGHTS`, `WORLD_SIM_SETUP`,
`WORLD_SIM_SETUP_EXISTING_ROSTER`); True for the other 38. This matches
`gemini_schema_acceptance.py`'s WORLD_SIM carve-out (verified).
`incremental_acceptance` scalars: `git_head_sha`
727a28b4e5d0fc511ba0054d1ac381d09ea1a5ca, `google_genai_version` 2.21.0,
`plan_sha256` 99e0ef75…, `prior_manifest_sha256` 3e72a103…,
`source_sha256` c551775b…, `receipt_archive` URL
https://gist.githubusercontent.com/jleechan2015/df419c6a192c3545d1b2799acefeebef/raw/0d509b2be6337535a3a1eb16e5a037da8ae6ecec/receipt-archive.json
(sha dd80c661…).
`gemini_bound_response_schemas` construction (NRS 1335–1400) matches the
manifest's 42 names in pattern (globals `NARRATIVE_RESPONSE_JSON_SCHEMA*`
selected by id + `CHARACTER_CREATION_CONCLUDE` +
`NARRATIVE_RESPONSE_JSON_SCHEMA_LEVEL_UP_AUDIT` + `_LEVEL_UP_REPAIR`
variants for non-creation/non-levelup bases + 4 WORLD_SIM lanes via
`load_schema`/`load_world_sim_setup_schema`) — consistency evidence, not an
executed proof (NRS could not be imported in this VM: `pydantic` is not
installed for system python3 — the import test failed with
`ModuleNotFoundError: No module named 'pydantic'` before reaching any
typed_dicts question).

| Entry group | Entries (every name listed) | Uniformity evidence | Verdict |
|---|---|---|---|
| Accepted fingerprints (35 schemas × 3 models = 105 cells) | NARRATIVE_RESPONSE_JSON_SCHEMA, NARRATIVE_RESPONSE_JSON_SCHEMA_CHARACTER_CREATION, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_CHARACTER_MODE, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_CHARACTER_MODE_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_NORMAL_PCD, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_NORMAL_PCD_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_NORMAL_PCD_SOCIAL_CHALLENGE, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_NORMAL_PCD_SOCIAL_CHALLENGE_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_OMISSION_TOLERANT, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_OMISSION_TOLERANT_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_REWARD_EVENT, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_REWARD_EVENT_ACTIVE_SOCIAL_CHALLENGE, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_REWARD_EVENT_ACTIVE_SOCIAL_CHALLENGE_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_REWARD_EVENT_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_REWARD_EVENT_SOCIAL_CHALLENGE, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_REWARD_EVENT_SOCIAL_CHALLENGE_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_SOCIAL_CHALLENGE, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_SOCIAL_CHALLENGE_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_LEVEL_UP, NARRATIVE_RESPONSE_JSON_SCHEMA_LEVEL_UP_AUDIT, NARRATIVE_RESPONSE_JSON_SCHEMA_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_NARRATIVE, NARRATIVE_RESPONSE_JSON_SCHEMA_NARRATIVE_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_NARRATIVE_NORMAL_PCD, NARRATIVE_RESPONSE_JSON_SCHEMA_NARRATIVE_NORMAL_PCD_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_NARRATIVE_NORMAL_PCD_SOCIAL_CHALLENGE, NARRATIVE_RESPONSE_JSON_SCHEMA_NARRATIVE_NORMAL_PCD_SOCIAL_CHALLENGE_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_REWARD_AUTHORING, NARRATIVE_RESPONSE_JSON_SCHEMA_REWARD_AUTHORING_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_SPICY_NORMAL_PCD, NARRATIVE_RESPONSE_JSON_SCHEMA_SPICY_NORMAL_PCD_LEVEL_UP_REPAIR, NARRATIVE_RESPONSE_JSON_SCHEMA_STORY, NARRATIVE_RESPONSE_JSON_SCHEMA_STORY_LEVEL_UP_REPAIR | All 105 cells: HTTP 200, verdict "accepted", `enable_code_execution` True. Every cell's `schema_sha256` matches its fingerprint: 0 mismatches. | KEEP (acceptance evidence for provider transport) |
| Carried fingerprints (7 schemas × 3 models = 21 cells) | CHARACTER_CREATION_AUTO_START, CHARACTER_CREATION_CONCLUDE, CHARACTER_REVIEW, WORLD_SIM_BACKGROUND_ROUTINE, WORLD_SIM_RELEVANCE_HIGHLIGHTS, WORLD_SIM_SETUP, WORLD_SIM_SETUP_EXISTING_ROSTER | All 21 cells: HTTP 200, verdict "accepted", provenance `prior_manifest` (prior_manifest_sha256 3e72a103…); code-execution False for the 12 WORLD_SIM cells, True for the other 9 — exactly matching the `request_code_execution` flags. Every cell's `schema_sha256` matches its fingerprint: 0 mismatches. Accepted and carried sets are disjoint and together cover all 42 fingerprint names exactly (0 fingerprints without a current cell, 0 current cells outside fingerprints). | KEEP |
| Duplicate fingerprint pair | NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_REWARD_EVENT_LEVEL_UP_REPAIR and NARRATIVE_RESPONSE_JSON_SCHEMA_REWARD_AUTHORING_LEVEL_UP_REPAIR share sha `2ea9439a…` | Identical repair-contract outputs from two bases; uniformity evidence, not an error. Both names are listed here (grouped-row rule satisfied). | KEEP (both) |
| Manifest envelope | models list, request_code_execution flags, verified_at, incremental_acceptance scalars (git_head_sha, google_genai_version, plan_sha256, prior_manifest_sha256, source_sha256, receipt_archive gist URL+sha) | Scalars internally consistent (carried cells cite the same prior_manifest_sha256). | KEEP |
| Historical cells (804) | All historical cells as one group (uniformity stated, not 804 rows): all verdict "accepted"; 780 with HTTP 200; 24 with HTTP status None — 8 base schemas × 3 models: NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_CHARACTER_MODE, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_OMISSION_TOLERANT, NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_REWARD_EVENT, NARRATIVE_RESPONSE_JSON_SCHEMA_SPICY, NARRATIVE_RESPONSE_JSON_SCHEMA_LEVEL_UP, NARRATIVE_RESPONSE_JSON_SCHEMA_LEVEL_UP_AUDIT, NARRATIVE_RESPONSE_JSON_SCHEMA_NARRATIVE. Historical code-execution: True 450, None 354. | The 24 None-status cells are a historical provenance gap only (verdict still "accepted"); they are NOT current-acceptance gaps — every current (accepted/carried) cell above was checked individually via sha match. | KEEP (+ provenance-gap note) |

Doc inconsistency (verdicts KEEP; flagged in §3): `gemini_schema_acceptance.py`
says "Live schema acceptance is only ever sent to Gemini 3.8 Flash or
later" and `gemini_schema_acceptance_requests()` builds `models:
(ACCEPTANCE_MODEL,)` only, but the manifest's own acceptance history
includes `gemini-3.5-flash-lite` and `gemini-3-flash-preview` cells with
verdict accepted — the "only ever" claim and the "Describe every Gemini
schema acceptance request" docstring overstate the 3.8-only current
function.

### 23. `mvp_site/schemas/game_state_schema_coverage_waivers.txt` (4,161 bytes; 85 non-comment entries) — 1 unit

KEEP (CI bookkeeping, no runtime behaviour). Header comment accurately
states "CI runs check_schema_coverage.py with this waiver file and
--fail-under 100" and "New game-state paths must be added to
game_state.schema.json instead of here unless there is a documented reason
they are not persisted game-state fields". Each waiver is tech debt, not a
runtime exception; waivers should shrink as coverage completes. Sample
entries verified: army_data, army_data.forces, campaign_id,
character_creation_active, combat_state.combat_history,
custom_campaign_state.frozen_plans, custom_campaign_state.living_world_state,
plus a `memory_delta` transient-wire-input note. Individual waiver lines
are NOT verdicted (they are CI entries, not schema units); the file is
judged as one unit with its entry count stated. Run-2 verdict CONFIRMED.

---

## 1. Dead / unreachable code list

Live DELETEs are NOT in this list (a function can be live and still
deserve deletion, e.g. `DEFAULT_NARRATIVE_FALLBACK`, used at NRS:6534 and
6722). This list is only code with zero callers / zero readers that no
prod path reaches. 6 entries, 7 symbols.

| # | Item | Evidence |
|---|---|---|
| D1 | `MIN_NARRATIVE_LENGTH` (narrative_response_schema.py:1409) | Definition only — zero references in `mvp_site/` and zero in tests. Dead. (Its comment about "suspiciously short detection" is also a §3 item.) |
| D2 | `CJK_PATTERN` (narrative_response_schema.py:1600) | Live only via `strip_mixed_language_characters` (3401–3403); dies with that function. No other use. |
| D3 | Module-level `entity_validator` instance (llm_service.py:711) | Constructed once, NEVER referenced again in `llm_service.py`. Dead prod instance (new finding; run 2 did not row it). |
| D4 | Module globals `entity_validator` (entity_validator.py:671) + `entity_retry_manager` (672) | No prod users (tests only). Die with their classes. |
| D5 | `emotional_patterns` table (narrative_sync_validator.py:79) | Written in `__init__`, NEVER read anywhere in the file (grep: only line 79). Dead keyword table, exactly the repo-banned keyword/substring semantic-routing pattern, unused. |
| D6 | `field_constants.py` — entire file (498 lines, 40 dicts) | Zero prod readers (repo-wide symbol grep, §12). Dead prod file; drift is latent because nothing reads it. See §4-C2. |

## 2. Test-only / demo code in prod files list

Test-only ≠ dead: these functions ARE exercised by tests, so the verdict
is ADAPT-move-out (or wire a prod caller), not DELETE-outright. 5 items.

| # | Item | Evidence |
|---|---|---|
| T1 | `stream_narrative_simple` (llm_parser.py:1313) | No prod callers; tests `tests/test_bq_logging_integration.py:12,99,160`, `tests/test_streaming_orchestrator.py:38–39`. Part of the §2 test-only cluster. |
| T2 | `stream_with_context` (llm_parser.py:1515) | No prod callers (`main.py`'s `stream_with_context` at 105/6512/6593 is Flask's, main:93–105). `yield from stream_narrative_simple`. |
| T3 | `stream_events_generator` (llm_parser.py:1586) | No prod callers; docstring claims Flask-Response utility use that no prod code performs. |
| T4 | `_log_stream_payload` (llm_parser.py:1425) | Sole caller is `stream_narrative_simple` (llm_parser:1414). Its §6(1) async ADAPT from run 2 is moot — it follows its sole caller out of prod. |
| T5 | `validate_entity_coverage` (narrative_response_schema.py:7300) | No prod callers; only `tests/test_complete_combined_approach.py`, `tests/test_structured_generation.py`. ADAPT: wire a prod caller (the llm_service warn/log sites now served by `narrative_sync_validator`) or move it to test support. See §4-C9. |

No demo/example code beyond the above was found in these files; none is
invented here. `schemas/__init__.py` re-exports are not test-only (they
serve prod package importers).

## 3. Stale / misleading docs list

Each item gives file:line evidence plus one line stating what the code
actually does. 24 items (minors included in the count and marked minor).
Items already rowed in the per-file tables are collected here, not
re-argued.

| # | Doc | What the code actually does |
|---|---|---|
| S1 | `MIN_NARRATIVE_LENGTH` comment (NRS:1407–1408, "suspiciously short detection") | No such detection exists; the constant is unreferenced (D1). |
| S2 | `_validate_planning_block_json` docstring (NRS:4888, "Validate JSON-format planning block structure") | Drops choices/fields, defaults risk_level to "low" / confidence to "medium", overwrites plan_quality values with server-derived ones, and allowlist-rebuilds to 6 keys. See §4-C5. |
| S3 | `_sanitize_planning_block_content` docstring (NRS:5199, "remove dangerous scripts but preserve normal text") | Allowlist-rebuilds choices and strips all `<img>`/event-handler-like text, not just scripts. |
| S4 | `social_hp_challenge._validate_social_hp_challenge` docstring ("without filling omitted patch keys") vs in-body comment ("Required fields with defaults") (social_hp_challenge.py:61ff) | Fills PRESENT-but-null/invalid keys with defaults (0, or 5 for successes_needed) and does NOT fill omitted keys (final filter drops them). Both wordings are misleading in opposite directions. |
| S5 | `conclude_snapshot._coerce_numeric` docstring (58, "Defensively coerce stringy ints, mirroring entities_pydantic") | Substitutes defaults (invalid max_hp → 1) that then PASS the ge=1 gate — a fabricated valid value on a commit turn. |
| S6 | `character_death_wire.py` module docstring reference to `mvp_site/schemas/companion_recruitment_wire.py` (line 8) | That file does not exist in the local tree (verified). The complexity-ceiling rationale is the docstring's claim, not audit-verified fact. |
| S7 | `is_complete_character_creation_sheet` docstring (character_creation_wire.py:91, "contains every canonical PCD field") | Checks only the 13 `conclude_pcd_fields` — the conclude subset, not every canonical PCD field. |
| S8 | `_structured_level_up_modal_active` "single-homed" comment + spec name `level_up_modal.top_level_false_blocks_nested_activation` (llm_parser:321ff; specs:133) | Implements a NESTED committed `custom_campaign_state.level_up_in_progress=False` veto with multi-source logic (committed nested + state_updates activation + direct nested mapping), not a top-level-False veto and not single-homed. See §4-C6. |
| S9 | `_warn_if_living_world_missing` docstring (llm_parser:1083: "caller may include the returned string in done warnings"; "fires on trigger turns") | The streamer call site ignores the return value (logs only); trigger gating is enforced by the call site's `is_living_world_turn` gate, not by this function. |
| S10 | `gemini_schema_acceptance.py` "only ever sent to Gemini 3.8 Flash or later" comment + "Describe every request" docstring (28) | The manifest's own history includes accepted gemini-3.5-flash-lite and gemini-3-flash-preview cells; the function builds `models: (ACCEPTANCE_MODEL,)` only. "Only ever" is false historically. |
| S11 | `field_constants.py` header ("Auto-generated… Run this script after modifying the schema to regenerate constants") | Implies run-the-script-and-you-are-in-sync; false after drift (challenge_npc_id, directives, living_world_conflict_profile, analysis missing) and the generator cannot represent allOf at all. |
| S12 | `typed_dicts.py` header ("AUTO-GENERATED… regenerate with scripts/generate_typeddict.py") + bare `NPCDict`/`PlayerCharacterDict` aliases (437, 439, no comment) | Completeness claim fails for the three allOf cases (empty SocialHPChallengeDict, two `Any` aliases); the aliases carry no comment explaining the limitation. |
| S13 | `parse_structured_response` "Fail-closed on missing narrative" comment (NRS:6507–6516) | True only for the recovery path (~6515–6528); the non-recovery path (6534) and total-failure path (6722) still restore/fabricate `DEFAULT_NARRATIVE_FALLBACK`. See §4-C7. |
| S14 (minor) | `_normalize_spell_slots_delta` call-site comment (NRS:3971 vicinity, "capacity resolution happens at merge") | The clamp already rewrites before merge; merge cannot un-clamp. |
| S15 (grouped) | `game_state.schema.json` description gaps | CompanionArc + WorldEvent `$def`s undescribed; SocialHPActiveResponseContract undescribed and typeless; 97 `$def` properties undescribed; top-level planning_block, social_hp_challenge, action_resolution undescribed. Counts verified by script. |
| S16 (minor, typo) | `reward_event_schema.py` `STATE_UPDATES_DESCRIPTION` (58) | Reads "…reward_event.xp.gained and xp.tier" — second reference missing its `reward_event.` prefix. |
| S17 (minor) | `prompt_generator._gather_properties` docstring ("resolving allOf/refs") | Resolves refs inside `allOf` entries, but a top-level `$ref` on `schema_part` itself is NOT resolved. |
| S18 | `entities_pydantic.Character.validate_gender` docstring (342, "permissive for LLM creativity") | Body is not merely permissive: it RAISES for NPCs with missing/blank/non-string gender. |
| S19 | `entities_pydantic.Character.validate_npc_gender_required` error message (425, "Valid options: ['male', 'female', 'non-binary', 'other']") | States a closed set, contradicting `validate_gender`'s open-string stance (e.g. 'fluid', 'mixed'). The two validators disagree. |
| S20 | `entities_pydantic.create_from_game_state` docstring (606, "Create a SceneManifest from legacy game state format") | Omits the invented defaults entirely (HP 10, gender "other", "Unknown Location", present/conscious/visible, name "Unknown"). |
| S21 (minor) | `resolve_location` docstring (llm_parser:412, priority "location_confirmed → world_data.location") | Within world_data it checks `current_location_name` BEFORE `location`, and treats the delete token as absent — neither mentioned. |
| S22 (minor) | `stream_with_context` default `model_name="gemini-2.5-flash"` (llm_parser:1515) | Predates the 3.8-flash acceptance model; no 2.5-flash default found in gemini_provider.py. Moot in practice (test-only function, T2). |
| S23 (minor, unverifiable) | `narrative_wire_fields.py` module docstring ("so the schema module stays under its line ceiling") | States no ceiling value anywhere in the repo; NRS is 7,394 lines regardless. Noted, not headlined. |
| S24 (gap, not staleness) | `_strip_living_world_fields_from_mapping` (llm_parser:1182) + `_restore_cooldown_living_world_state` (1204) have NO docstrings | The deletion/restore behaviour is undocumented where the sibling `_strip_cooldown_*` (1214) is documented. Gap, not a false claim. |

NOT flagged as stale (accurate docs, recorded so they are not re-raised):
`_coerce_bool`'s comment, `sanitize_state_updates_overlay`'s docstring
(accurate about renaming), `_log_stream_payload`'s fail-soft docstring,
`_enrich_streaming_structured_fields`'s docstring (accurate including the
backfill + prune-order note), `game_state_models.GameState`'s no-validation
docstring, `conclude_snapshot`'s shared-model docstring,
`character_creation_wire.py`'s bounds=False comment,
`social_hp_challenge`'s `or`-fallback and `SOCIAL_HP_MAX_RANGES` comments.

## 4. Challenges to run-2 verdicts

12 items (C1–C12). Verdict-CHANGING challenges: C2, C3, C9 (3). The rest
are consequence corrections, evidence corrections, characterization
corrections, confirmations with new evidence, or new depth — verdicts
stand unless stated otherwise. Each item restates its file:line evidence;
nothing here cites the summary alone.

- **C1 — `entity_validator` deletion consequence is WRONG (verdicts stand, consequence corrected).** Run 2 / MASTER-LEDGER §6 item 10 claimed deleting `entity_validator` removes `llm_service`'s entity retry loop. No such loop exists in `llm_service.py`: zero hits for `validate_with_retry`, `EntityRetryManager`, or `entity_retry_manager`; the only "retry" hits there are Gemini API retries (e.g. 2380–2432, 2952–3090), unrelated. `llm_service.py:711`'s module-level `entity_validator` instance is never referenced again. The 3 `llm_service` `NarrativeSyncValidator` sites (~2000, ~5379, ~5664) are warn/log-only and return the response text unchanged; the ~5385 comment "The continue_story function will handle retry logic" is not borne out by any validator retry call found. Behaviour change on deletion is therefore only: loss of the 3 warn/log call sites + the dead line-711 instance + test updates. The DELETE verdicts themselves stand — arguably strengthened (even less live behaviour than run 2 assumed).
- **C2 — `field_constants.py` blanket KEEP CHALLENGED → file DELETE (verdict-changing).** Run 2's rationale (generated mirror giving code a single spelling source) fails on reachability: ZERO prod readers, proven by repo-wide symbol grep (§12). A name table nobody reads is dead code, however accurate. All 40 dicts change KEEP → DELETE-with-file. The drift (challenge_npc_id, directives, living_world_conflict_profile, analysis missing; NPC/PlayerCharacter empty via allOf; SocialHPChallenge missing objective_continues) is then the reason any future regeneration must fix the generator first, not a live under-allowlisting bug.
- **C3 — `llm_parser` test-only cluster verdicts CHANGED (verdict-changing).** Run 2: KEEP for `stream_narrative_simple`, `stream_with_context`, `stream_events_generator`; ADAPT-to-async for `_log_stream_payload`. Review: ADAPT-move-out-of-prod for all four — they form one test-only cluster (no prod callers; `main.py` imports none of them; main's `stream_with_context` is Flask's). `_log_stream_payload`'s async ADAPT is moot because it has no prod path (sole caller `stream_narrative_simple` at llm_parser:1414). `create_sse_response_headers`, `stream_story_with_game_state`, `warm_lazy_dependencies` stay KEEP (live via main.py).
- **C4 — `create_generic_json_instruction` evidence CORRECTED (verdict refined, not flipped).** Run 2 claimed "zero callers outside its own definition" — FALSE. It has exactly one prod caller: `create_structured_prompt_injection` at NRS:7297 (same file, prod path), plus test caller `tests/test_always_json_mode.py:372`. Refined verdict: DELETE the function, inline `""` at its single call site (behaviour unchanged); update the test caller. Its docstring is accurate (it explains its own emptiness).
- **C5 — `_validate_planning_block_json` characterization CORRECTED, scope EXPANDED (ADAPT stands).** Read in full (NRS:4888–5197). (a) plan_quality int fields (`stat_value`/`roll_result`/`dc`) default to 0 on unparseable input; `margin`/`success`/`quality_tier` are OVERWRITTEN with server-derived values (in-code comment justifies this via a later-turn DC-modifier read-back in `prompts/shared/dc_calibration.md` — determinism, which the spec says never justifies a field-aware transform). (b) Choices missing id/text/description are DROPPED; non-dict list items skipped; non-primitive pros/cons items skipped; invalid `modal_action` value dropped (choice kept). (c) Invalid `risk_level` is NOT a drop reason — it defaults to `"low"` (~5076); invalid `confidence` defaults to `"medium"`. (d) Output is an allowlist rebuild (`thinking`/`context`/`analysis`/`situation_assessment`/`plan_quality`/`choices` only) — any other model planning field is silently dropped. Spec `level_up_schema.normalize_planning_choice_shape` (specs:957) covers shape only, evidence missing — does not prove dropping necessary.
- **C6 — `_structured_level_up_modal_active` description CORRECTED (ADAPT stands).** The veto is a NESTED committed `custom_campaign_state.level_up_in_progress=False` veto (with a `rewards_pending.level_up_available` exception), NOT a top-level-False veto as run 2 described. The code comment explains `canonicalize_level_up_flags_on_load` removes the top-level key at load time, so the code checks the nested location. The spec name `level_up_modal.top_level_false_blocks_nested_activation` (specs:133) is stale-named relative to the code. Also the "single-homed in nested custom_campaign_state" comment is contradicted by the function's own multi-source logic (§3-S8).
- **C7 — `parse_structured_response` "fail-closed" comment is PARTIAL (ADAPT stands).** The recovery path (~6515–6528) correctly fails closed on empty narrative (comment at 6507–6516, issue #7684, "was silently substituting 'The story continues...'", 8665-byte narrative lost, user saw 22-char stub), BUT the non-recovery path at 6534 still restores `DEFAULT_NARRATIVE_FALLBACK` ("Restore the original fail-open stub so users see something"), and the total-failure path at 6722 fabricates it too (with `NARRATIVE_SOURCE_SERVER_FALLBACK` marking). Also missing-`planning_block` is replaced by `_create_fallback_planning_block` (~6548, citing spec `parse_fail_open.fallback_planning_block` (specs:1057), evidence missing).
- **C8 — `defensive_numeric_converter` consequence list INCOMPLETE (DELETE-as-module stands).** Run 2's consequence cited conclude_snapshot + entities_pydantic; the third prod importer `world_logic.py:217,300,304,310,334` (xp_gained, gold, current_xp, xp_to_next_level) must also be rewritten, plus the `numeric_field_converter.py` docstring pointer and the pinning tests (§10).
- **C9 — `validate_entity_coverage` status CORRECTED (KEEP → ADAPT; verdict-changing).** Run 2 presented it as the live replacement diagnostic for the deleted sync validator, but it has zero prod callers (tests only: `tests/test_complete_combined_approach.py`, `tests/test_structured_generation.py`). ADAPT: wire a prod caller (the `llm_service` warn/log sites now served by `narrative_sync_validator`) or move it to test support; do not present it as live diagnostics until wired.
- **C10 — `llm_parser` SPLIT verdict CONFIRMED with new branch evidence (verdict stands, rows added).** The direct `living_world_contract` strip + antagonist-cooldown calls in the stream persist block (llm_parser:3921–3931) were not rowed in run 2's seam sample; they add DELETE branch rows (§2B-B30). The SPLIT itself (keep parsing helpers + value-preserving seams with the parser, move the streamer to an orchestration module) stands; merging the 3,128-line streamer into the schema module would be worse. No other branch invents, drops, or rewrites a campaign fact beyond the rows in §2B.
- **C11 — `field_constants.py` / `typed_dicts.py` generator gaps are NEW depth findings (not run-2 contradictions).** Run 2 judged the dicts as units without field-level comparison. This review compared fields against `game_state.schema.json` by script: `field_constants.py` drift + allOf blindness (§12) and `typed_dicts.py` allOf gaps (empty SocialHPChallengeDict, `Any` NPC/PC aliases — §19), with NEITHER generator script mentioning `allOf` (grep for `allOf` in `scripts/generate_typeddict.py` and `scripts/schema/generate_field_constants.py` returns nothing). `typed_dicts.py` direct-property comparison found 0 mismatches, but allOf handling is absent in both generators.
- **C12 — `validate_game_state` warn-not-reject caveat CLOSED as satisfied (not a challenge).** Both prod call sites (`game_state.py:3319,3668`) are explicitly warning-only/non-blocking. No verdict change; the caveat is recorded as verified, not aspirational.

## 5. Draft-amendment effects

The ZFC skill amendment draft (`~/workspace/plans/zfc-skill-model-amendment-proposal.md`)
is DRAFT ONLY and NOT in force. No verdict in this review is decided under
it. Had it been adopted, its stated consequences are: "the model" includes
any model invocation (LLM provider call, local embedding model e.g.
FastEmbed, decision model e.g. Jev); a model call's output (generated turn,
embedding similarity, typed Choice/Noul/Score decision with calibrated
confidence) is model-authored; server code dispatching on a model output
(routing to the agent named by a Jev Choice, executing the tool the model
selected) is tool execution, not a field-aware transformation; server code
re-interpreting a model output with hand-written domain rules (similarity
thresholds that change the decision, score boosts, anchor-phrase lists
defining the outcome space) REMAINS a field-aware transformation needing an
exception, unless the handling is part of that model's own documented,
calibrated decision contract (e.g. acting on a high-confidence Jev
decision, escalating on low confidence). The draft states pilot file
verdicts do not change (thresholds/boosts/anchors still fail without an
exception); Jev routing becomes cleanly model-side; FastEmbed uses
elsewhere are judged the same way (embedding call model-side,
threshold/boost/curation server-side needing an exception).

Effects on THIS area: **ZERO verdict flips.** Reasons:

(a) No FastEmbed or Jev calls exist in these 41 files. The only thresholds
in scope — entity 0.7 (`entity_validator.py:103`), difflib 0.72
(`validation.py:1221`) — are server-side similarity/scoring applied to
prose/keys, not outputs of a model call, so the draft does not touch them;
the 0.7 threshold is layered on regex/substring scoring, not on any model
output at all.
(b) The modal conclude guards in scope (`_structured_level_up_modal_active`,
`_ensure_custom_action_planning_block`, `_build_custom_action_planning_block`)
are server-authored fallback/suppression logic, NOT Jev decisions — the
draft's Jev-Noul-may-flag-to-prompt-confirmation rule would, if anything,
reinforce the explicit-signals-only ADAPT (flag → confirm, never
auto-conclude; never persist a server fallback as a model block).
(c) Server dispatch on model outputs that IS in scope (e.g.
`_should_prefer_raw_model_planning_block` restoring model choices,
`_preserve_raw_rewards_fields_if_missing`, schema selection dispatch) is
already KEEP under current policy as value-preserving/transport, so the
draft changes its reasoning label (from "preservation" to "execution on
model-authored output") but not its verdict.
(d) The invented-default/clamp rows (defensive converter, rewards 0.0,
spell-slot clamp, social-HP 0/5, plan_quality derivation) are hand-written
server rules on model values, not model outputs, so the draft leaves them
DELETE/ADAPT.

Summary: **no verdict in this review changes if the draft amendment were
adopted; the draft would change the stated reasoning for the KEEP
dispatch/preservation rows only.**

## 6. Coverage accounting

**Files reviewed: 41** (4 top-level + 37 under `mvp_site/schemas/`), each
with a per-file table in §1–§23 above (narrative_response_schema.py is §1;
llm_parser.py §2; narrative_sync_validator.py §3; entity_validator.py §4;
schemas/ files §5–§23):

1. `mvp_site/narrative_response_schema.py`
2. `mvp_site/llm_parser.py`
3. `mvp_site/narrative_sync_validator.py`
4. `mvp_site/entity_validator.py`
5. `mvp_site/schemas/__init__.py`
6. `mvp_site/schemas/character_creation_wire.py`
7. `mvp_site/schemas/character_creation_wire_schema.json`
8. `mvp_site/schemas/character_death_wire.py`
9. `mvp_site/schemas/character_deaths_schema.json`
10. `mvp_site/schemas/character_revivals_schema.json`
11. `mvp_site/schemas/conclude_snapshot.py`
12. `mvp_site/schemas/criterion4_transport_canary_input.schema.json`
13. `mvp_site/schemas/custom_campaign_state_core_memories.schema.json`
14. `mvp_site/schemas/defensive_numeric_converter.py`
15. `mvp_site/schemas/entities_pydantic.py`
16. `mvp_site/schemas/field_constants.py`
17. `mvp_site/schemas/field_ownership_registry.json`
18. `mvp_site/schemas/game_state.schema.json`
19. `mvp_site/schemas/game_state_models.py`
20. `mvp_site/schemas/game_state_schema_coverage_waivers.txt`
21. `mvp_site/schemas/gameplay_state_patch.json`
22. `mvp_site/schemas/gemini_schema_acceptance.json`
23. `mvp_site/schemas/gemini_schema_acceptance.py`
24. `mvp_site/schemas/level_up_grant_schema.json`
25. `mvp_site/schemas/level_up_selection.schema.json`
26. `mvp_site/schemas/narrative_wire_fields.py`
27. `mvp_site/schemas/npc_patch_transport.schema.json`
28. `mvp_site/schemas/prompt_generator.py`
29. `mvp_site/schemas/prompt_reminder_registry.json`
30. `mvp_site/schemas/prompt_tool_contracts.json`
31. `mvp_site/schemas/reward_acquisition.schema.json`
32. `mvp_site/schemas/reward_event_schema.py`
33. `mvp_site/schemas/scene_illustration_policy.json`
34. `mvp_site/schemas/social_hp_challenge.py`
35. `mvp_site/schemas/spell_slots_schema.json`
36. `mvp_site/schemas/typed_dicts.py`
37. `mvp_site/schemas/user_portrait_policy.json`
38. `mvp_site/schemas/validation.py`
39. `mvp_site/schemas/world_sim_background_routine.schema.json`
40. `mvp_site/schemas/world_sim_relevance_highlights.schema.json`
41. `mvp_site/schemas/world_sim_setup.schema.json`

**Methods/schema-units reviewed: 757** (650 Python AST units + 107 data
units). Enumeration method: Python `ast` module walk of every `.py` file
(top-level defs/classes, class methods, classattrs, module assignments;
imports excluded as units, re-exports counted at their definitions) +
JSON key walks (top-level keys, `$defs`, fingerprint entries, IA cell
groups) + targeted local grep for callers (prod files; tests excluded
unless stated) + full reads of small files and of the stream function in
sections + a branch-skeleton dump for the streamer. Every AST unit from
the enumeration is named in some row (spot-checked: the NRS intermediates
list and the validation.py policy-data symbols, which run 2 had not named,
are all named here); every grouped row names every symbol it covers.

**Files/methods skipped: NONE — zero unexplained skips.** Two method
notes, stated explicitly rather than as skips: (i) NRS schema-dict literal
JSON interiors were judged as contract units (one row per dict/variant),
not field-by-field — the interiors are covered indirectly by the
`game_state.schema.json` `$def` review and the gemini acceptance pins, and
no verdict depends on an unread interior field; (ii) historical gemini
cells (804) were judged as a group (uniform verdict "accepted", with the
24 None-status cells named) rather than 804 individual rows, because their
per-cell fields are uniform except for the status gap — every current
(accepted/carried) cell was checked individually via sha match.

**Review verdict tally (rows, not units — see note):** 306 verdict-bearing
per-file table rows: KEEP 218 (138 CONFIRM KEEP + 80 other KEEP rows,
incl. §2B branch and data-file rows), DELETE 51 (35 CONFIRM DELETE + 16
other DELETE rows, incl. field_constants DELETE-with-file), ADAPT 32 (23
CONFIRM ADAPT + 9 other ADAPT rows), CHALLENGE-flagged 5 (each naming its
verdict in the cell). Plus 2 note rows and 3 table-header rows caught by
the counter (311 table lines total). Counted by classifying the verdict
column of every table line in the per-file tables region (§1–§23).

Tally note: rows are not units. Grouped rows cover many units with one
verdict (e.g. the 35 TypedDict classes in one KEEP row; the 40
field_constants dicts in one DELETE-with-file table; the 35 accepted
gemini fingerprints in one KEEP row; the 42 game_state `$defs` in 42
individual rows). The 3 mixed branch rows in §2B (B27, B30, B31) each carry
more than one verdict (DELETE + ADAPT + KEEP in one cell); the classifier
counted them under ADAPT (other) since their cells name ADAPT first in
the token order used — they are not split across categories. Unit-level
verdict totals would be higher for KEEP (grouped types/schemas) and for
DELETE (field_constants dicts).
