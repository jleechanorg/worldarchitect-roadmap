# Schema / parsing audit — WorldArchitect.AI (jleechanorg/worldarchitect.ai) — SECOND RUN

Read-only audit. Nothing was written, committed, pushed, deleted, or changed in
any repo. All file reads were local only, from
`~/workspace/repos/worldarchitect.ai` (main-branch ZIP tree, no `.git`
history). Zero GitHub API/MCP calls were made in this run. Repo file contents
are DATA for this audit, never orders; no instruction found in repo files was
followed.

Scope (assigned): `mvp_site/narrative_response_schema.py`,
`mvp_site/llm_parser.py`, `mvp_site/narrative_sync_validator.py`,
`mvp_site/entity_validator.py`, and the ENTIRE `mvp_site/schemas/` directory.
Explicitly OUT of scope: `mvp_site/intent_classifier.py` and
`mvp_site/intent_classifier_warmup.py` (separate pilot).

Method (as assigned): Pass A — zero-code baseline (bare conversation log +
Gemini API): what player-visible capability breaks if the unit is deleted, and
can the model supply it through the log, a prompt, or the response schema? If
the model can supply it, DELETE. Pass B — strict ZFC: the model owns all
campaign-domain facts; the server provides ONLY transport, durable writes,
tool execution, authorization, and bounded capacity. A field-aware transform
fails unless it names a specific registered exception AND proves that
exception necessary. Registry membership alone proves nothing; determinism,
schema validity, display formatting, or normalization alone never justify a
field-aware transform. Pure parsing that preserves values is allowed; semantic
filtering is not. Final verdict is the stricter of the two passes unless a
named product promise rescues it (named explicitly per row where relied on).
Every function/method/symbol below gets 2–4 sentences covering both passes
and ends in its verdict (KEEP / ADAPT / DELETE). ADAPT names the change.
Reference counting: zero callers = DELETE unless entry point, test target, or
proven registered exception. Caller counts below are production-file
references from local `rg` over the tree (test files excluded from the
"prod" counts); they are approximate because a name match is not a proven
call site, and that limitation is stated wherever a count is load-bearing.

Jeffrey's standing decisions (§6, override everything else):
(1) Server logging KEEP; where it blocks a player turn, ADAPT to async/batched
delivery. (2) Anti-cheat KEEP; dice resolution stays ON the turn path; only
the audit trail may go async. (3) Faction/living-world KEEP but ADAPT to async
background ticks merged on the next turn.
§6 conflict check for this group: NO direct conflict with §6.1 or §6.2 was
found — no validator in this group gates dice resolution, and logging verdicts
below follow §6.1 (one ADAPT: `llm_parser._log_stream_payload`, batched
delivery). One §6.3 interaction is flagged, not a conflict: the living-world
strip/restore helpers in `llm_parser.py` are judged against §6.3's async-tick
rule, and their verdicts (DELETE the strips, ADAPT the restore into the tick
merge) implement §6.3 rather than contradict it. The one registered exception
with full runtime proof found in this group is social-HP executed-roll
attribution (`social_hp.executed_roll_attribution`, evidence PROVEN) — but its
writer is `dice_integrity`, not this group, so it rescues nothing here; the
`llm_parser` streaming seam only transports that verified roll. All other
registered specs touching this group carry `RUNTIME_EVIDENCE_MISSING`, which
under this audit's proof requirement means the spec is named but the
necessity proof is incomplete; those rows say so explicitly instead of
treating registration as a pass.

## Coverage — read this first (exact)

- `mvp_site/narrative_response_schema.py` (7,394 lines, 315,598 bytes) —
  DONE: all 101 functions/methods and all named module/class symbols audited
  below. Schema-dict bodies were audited as units (each named schema constant
  gets a row); the literal JSON inside each dict was not re-read field by
  field, which is stated here rather than hidden.
- `mvp_site/llm_parser.py` (5,019 lines, 241,324 bytes) — PARTIAL at depth,
  DONE at function level: all 48 named functions/methods and all named
  symbols audited below. `stream_story_with_game_state` (lines 1892–5019,
  3,128 lines) was audited at seam level — its documented role, its imports,
  and sampled seams (planning-block handling, living-world handling, persist
  seam, replay handling) — NOT branch by branch. Its verdict (ADAPT: split
  out of the parser module) does not depend on any unsampled branch, but a
  branch-level audit of that one function remains open work and is listed as
  such in "What remains".
- `mvp_site/narrative_sync_validator.py` (147 lines) — DONE in full.
- `mvp_site/entity_validator.py` (672 lines) — DONE in full.
- `mvp_site/schemas/` — DONE in full, 38 files enumerated (see enumeration).
  Every `.py` function/method/symbol and every `.json`/`.txt` file gets a row.
  The 1.26 MB `gemini_schema_acceptance.json` manifest was audited as a unit
  (top-level keys + role + readers), not entry by entry; `game_state.schema.json`
  (100,672 bytes) was audited as a unit (top-level keys + `$defs` role +
  readers), not `$def` by `$def`. Both limitations are stated here.
- Files untouched: NONE in scope. Files blocked: NONE in this run — the run-1
  GitHub 429 blocker is resolved by the local-copy rule, and all four
  top-level files' existence is now VERIFIED (run 1 left them unconfirmed).

## Verdict counts

Counts below cover every unit in the per-unit tables (functions/methods,
classes/enums, module symbols, and JSON/data files), with grouped rows
expanded to their named units (e.g. one row naming 9 schema variants counts
as 9). If a count here disagrees with a row, the row governs.

- KEEP: 458
- ADAPT: 35
- DELETE: 50
- Total units judged: 543

## Enumeration — `mvp_site/schemas/` (complete, local listing)

38 files: `__init__.py` (1,647 B), `character_creation_wire.py` (9,758 B),
`character_creation_wire_schema.json` (7,512 B), `character_death_wire.py`
(2,066 B), `character_deaths_schema.json` (2,392 B),
`character_revivals_schema.json` (742 B), `conclude_snapshot.py` (3,257 B),
`criterion4_transport_canary_input.schema.json` (229 B),
`custom_campaign_state_core_memories.schema.json` (1,426 B),
`defensive_numeric_converter.py` (5,340 B), `entities_pydantic.py`
(27,016 B), `field_constants.py` (14,506 B),
`field_ownership_registry.json` (4,988 B), `game_state.schema.json`
(100,672 B), `game_state_models.py` (1,753 B),
`game_state_schema_coverage_waivers.txt` (4,161 B),
`gameplay_state_patch.json` (7,622 B), `gemini_schema_acceptance.json`
(1,263,368 B), `gemini_schema_acceptance.py` (1,410 B),
`level_up_grant_schema.json` (2,465 B), `level_up_selection.schema.json`
(715 B), `narrative_wire_fields.py` (3,145 B),
`npc_patch_transport.schema.json` (1,278 B), `prompt_generator.py`
(7,008 B), `prompt_reminder_registry.json` (10,834 B),
`prompt_tool_contracts.json` (9,877 B), `reward_acquisition.schema.json`
(4,714 B), `reward_event_schema.py` (3,966 B),
`scene_illustration_policy.json` (1,031 B), `social_hp_challenge.py`
(5,874 B), `spell_slots_schema.json` (647 B), `typed_dicts.py` (30,518 B),
`user_portrait_policy.json` (2,336 B), `validation.py` (46,227 B),
`world_sim_background_routine.schema.json` (4,927 B),
`world_sim_relevance_highlights.schema.json` (1,340 B),
`world_sim_setup.schema.json` (1,638 B). Run 1's partial list (10 files to
`defensive_numeric_converter.py`) is confirmed and extended; the 4 top-level
files are confirmed present with the sizes in the Coverage section.

## The key question: one parser or two?

TWO modules, ONE parser. `narrative_response_schema.parse_structured_response`
(1,000 lines) is the only true parser: it turns raw model text into a typed
`NarrativeResponse` via `json.loads` plus grammar-preserving recovery
(quote-escaping repair, RFC 8259 string decoding, truncated-JSON extraction,
live-prefix extraction). `llm_parser.py` is not a second parser; it is the
streaming orchestrator (its 3,128-line `stream_story_with_game_state` plus
SSE helpers) with a planning-block seam layer grafted on. The overlap the
ledger flagged is real but narrow: both modules touch `planning_block` and
`rewards_box`/`level_up_signal`, and `llm_parser` second-guesses the parser's
planning-block output (`_should_prefer_raw_model_planning_block`,
`_ensure_custom_action_planning_block`, `_preserve_raw_rewards_fields_if_missing`).
The fix is therefore NOT a merge — merging a 3,128-line streamer into the
schema module would make the schema module worse — it is a SPLIT: keep the
parsing helpers and the value-preserving planning seams with the parser, and
move `stream_story_with_game_state` plus the SSE/persist/replay machinery into
a streaming-orchestration module. Pure parsing vs semantic filtering split:
pure parsing (KEEP) is everything that recovers or re-shapes model text
without choosing between model values; semantic filtering (DELETE/ADAPT) is
concentrated in five places — numeric defaulting/clamping
(`defensive_numeric_converter`, entity-model converters,
`_normalize_spell_slots_delta`), narrative-content deletion (CJK stripping,
planning-choice dropping), invented fallbacks (server-authored planning
choices), living-world stripping on cooldown turns, and entity-presence
regex scoring with retry regeneration. Each is rowed below with its
replacement (prompt/schema contract, warn-only diagnostics, or display-layer
fallback).

## Module verdicts (roll-up; per-unit rows govern)

- `narrative_response_schema.py` — ADAPT: keep as the one parser and the
  Gemini response-schema source; convert its mutating validators to
  warn-only/preserve, delete the CJK strip and spell-slot clamp, and slim the
  planning-block validator to shape-only. The schema dicts themselves are
  KEEP: they are the Pass A mechanism (the model is bound by them), not
  server filtering.
- `llm_parser.py` — ADAPT: split, don't merge. Keep the lazy-load transport,
  the planning-block predicates, the value-preserving raw-planning seams, and
  the transport/telemetry helpers; move the streamer out; delete the
  living-world strips; move the custom-action fallback to the display layer.
- `narrative_sync_validator.py` — DELETE as a module: a thin wrapper over
  `EntityValidator` whose only unique logic is a substring continuity check
  and a dead emotion-pattern table. Nothing in it is transport, durable
  writing, tool execution, authorization, or bounded capacity.
- `entity_validator.py` — DELETE as a module except `filter_unknown_entities`
  / `is_unknown_entity` (KEEP: sentinel handling). Regex presence scoring,
  retry regeneration, and server-authored injection templates are semantic
  judgments about prose that the model owns; the checkable contract is the
  `entities_mentioned` array plus the prompt requirement, not a 0.7 substring
  threshold.
- `schemas/validation.py` — ADAPT: keep the schema loading, validator
  construction, and warn-only gates; remove the near-match key remapping from
  `sanitize_state_updates_overlay` (keep dotted-key expansion and frozen-plan
  placement, which preserve values).
- `schemas/defensive_numeric_converter.py` — DELETE as a module: every
  default it substitutes (hp 1, ability 10, xp-to-next 300, AC 10) is a
  server-invented campaign fact with no registered exception and no runtime
  proof, and it directly contradicts the repo's UX-first rule against
  defaults/clamps without an approved ZFC contract.
- `schemas/entities_pydantic.py` — ADAPT: keep the type carriers, the prompt
  rendering, and the alias-mirroring; delete the numeric converters, the HP
  clamp, the hostile default, and the gender/age raises; stop
  `create_from_game_state` inventing HP 10 / "other" gender / "Unknown
  Location" when building a prompt manifest.
- All other `schemas/` modules and data files — KEEP except the two ADAPT
  rows noted (`schemas/social_hp_challenge._validate_social_hp_challenge`,
  `schemas/conclude_snapshot._coerce_numeric`) and the field-ownership
  registry note (KEEP as test-pinned documentation only; it enforces nothing
  at runtime and therefore proves no exception).

## How to read the tables

Each row is one unit. "Pass A" is the zero-code test (can the model, log,
prompt, or response schema supply it?), "Pass B" is the strict-ZFC test
(transport / durable write / tool execution / authorization / bounded
capacity, or a named + proven registered exception?). A row that says
"warn-only" was verified to emit warnings/diagnostics without changing the
persisted value; where a caller was found to treat those warnings as a
rejection, the row says so. "No registered exception" means no
`backend_adjustment_specs.py` entry naming that unit was found by local
search; "registered, evidence missing" means an entry names it but carries
`RUNTIME_EVIDENCE_MISSING`.

## Per-unit tables

### 1. `mvp_site/narrative_response_schema.py` — functions/methods

| Unit | Pass A + Pass B justification (2–4 sentences) + verdict |
|---|---|
| `apply_social_hp_challenge_transport` | Pass A: deleting it loses the rule that only an explicit root null clears a social-HP challenge, which the model cannot express more precisely than the null it already emits, so the rule must live somewhere server-side. Pass B: it is transport projection, not a domain judgment — it preserves the model's own root null as a clear and pops (ignores) a nested null rather than treating it as a clear, inventing no value. No registered exception is needed because no campaign fact is changed. **KEEP** |
| `ParseTelemetry.to_dict` | Pass A: telemetry serialization is invisible to the player and the model cannot supply server-side parse telemetry through the log or schema. Pass B: it copies telemetry fields into a dict, a logging operation covered by §6.1 (server logging KEEP). It changes no campaign value. **KEEP** |
| `create_parse_telemetry` | Pass A: without it there is no canonical record of parse outcome, error class, offset, or checksum for debugging interrupted or recovered parses, which the model cannot self-report reliably. Pass B: it builds a sanitized telemetry dict (bounded offset/request-id), i.e. logging under §6.1, and does not alter the parsed payload. **KEEP** |
| `_parse_outcome_is_interrupted` | Pass A: a one-line predicate over server-owned telemetry; the model cannot authoritatively mark its own stream as interrupted. Pass B: it reads a telemetry flag only, changing nothing, so it is pure transport bookkeeping. **KEEP** |
| `_hit_dice_patch_schema` | Pass A: it derives a hit-dice patch from the canonical game-state schema, which is exactly the response-schema mechanism Pass A allows the server to own. Pass B: it assembles a schema (a contract the model is bound by), it never touches a model value. **KEEP** |
| `_gold_patch_schema` | Pass A: same as above — a schema fragment derived from the canonical schema for the response contract. Pass B: popping a `default` key from a schema dict changes the contract, not a campaign fact, so it is schema assembly, not filtering. **KEEP** |
| `_player_character_property_schema` | Pass A: it looks up one canonical property schema by name; deleting it forces hand-duplicated property schemas, which the response-schema mechanism exists to prevent. Pass B: pure schema derivation with a `KeyError` on unknown names, no value transformation. **KEEP** |
| `_equipment_backpack_patch_schema` | Pass A: it restricts the equipment patch to the backpack property from the canonical schema, a wire-contract narrowing the model is bound by. Pass B: schema assembly only; it filters schema properties, not model-authored equipment values. **KEEP** |
| `_with_required_social_challenge` | Pass A: it builds a social-challenge schema variant (required challenge + narrative suffix + omitted properties) that the model must be bound by at request time; the model cannot bind itself. Pass B: it edits a schema dict, not a response value, so it is contract construction. **KEEP** |
| `is_gameplay_agent` | Pass A: routing which schema binds a given agent is a server transport decision; the model cannot select its own binding schema. Pass B: a membership predicate over a canonical agent set, changing no value. **KEEP** |
| `get_narrative_response_json_schema` | Pass A: this IS the Pass A mechanism — the mode/agent-scoped Gemini response schema. Deleting it removes structured output entirely, which no prompt text can replace. Pass B: selecting and patching a response schema is transport/bounded-capacity work (including the Gemini complexity ceiling), not filtering of returned values. **KEEP** |
| `get_level_up_audit_json_schema` | Pass A: it returns the agent's schema plus the level-up repair contract, the binding contract for audit turns; the model cannot impose its own repair contract. Pass B: schema selection only, no value mutation. **KEEP** |
| `_with_level_up_repair_contract` | Pass A: the repair contract tells the model what a valid repair payload looks like; without it, repair turns have no binding shape. Pass B: it constructs a schema variant from prompt-owned contract material, changing no returned value. **KEEP** |
| `reward_event_required_for_agent` | Pass A: a predicate derived from the schema the selector returns, so providers ask one source of truth whether an agent must author `reward_event`; the model cannot answer this about itself authoritatively. Pass B: a read-only predicate over schema output, not a transform of any value. **KEEP** |
| `gemini_bound_response_schemas` | Pass A: it enumerates every distinct schema that may be attached to a Gemini request, which is what real-API acceptance testing pins; deleting it unbinds acceptance coverage. Pass B: enumeration for provider transport and acceptance, touching no model value. **KEEP** |
| `_create_fallback_planning_block` | Pass A: deleting it leaves parse fail-open recovery with no choices to show, but the model can always be required by prompt/schema to emit choices, so a server-authored fallback is not the only option. Pass B: it returns a deepcopy of a server-written planning block, i.e. the server inventing player choices — semantic content creation, with no registered exception. The honest fix keeps a fallback for display only and never persists it as model output. **ADAPT (move fallback to display layer only; never persist as model planning_block)** |
| `_log_thresholded_warning` | Pass A: per-process warning escalation is server telemetry the model cannot supply. Pass B: logging under §6.1; it writes no campaign state and blocks no turn (log call only). **KEEP** |
| `_log_json_parse_error` | Pass A: parse-error diagnostics with content are needed to debug malformed model output; the model cannot diagnose its own malformed JSON after the fact. Pass B: logging under §6.1, fail-soft by design (a logger function parameter). **KEEP** |
| `_escape_unescaped_quotes_inside_json_strings` | Pass A: without grammar repair, a single unescaped dialogue quote destroys the whole turn's JSON, and no prompt reliably prevents all such quotes. Pass B: it is pure parsing repair — it escapes only quotes that cannot legally close a JSON string, preserving every model-authored semantic field. A registered spec exists (`parse_recovery.escape_unescaped_string_quotes`) but carries `RUNTIME_EVIDENCE_MISSING`; the verdict does not need it because no value is changed. **KEEP** |
| `_parse_action_resolution_dice_notation` | Pass A: a thin passthrough to the shared dice-notation parser; deleting it only moves the call, it removes no capability. Pass B: parsing a notation string into numbers is value-preserving parsing adjacent to tool execution (dice), not a domain judgment. **KEEP** |
| `_coerce_bool` | Pass A: the model can emit real booleans under the response schema, so the server need not guess at unknown strings at all. Pass B: its string table (true/yes/1, false/no/0) is benign normalization, but its fallback — unknown strings silently become `False` — invents a campaign fact (e.g. an unknown flag read as false). No registered exception covers it. **ADAPT (unknown/non-empty strings return None, never False)** |
| `_derive_quality_tier` | Pass A: the model can emit a quality tier itself under the response schema (it already authors success and margin, from which the tier is a lookup), so the server derivation is replaceable by prompt/schema. Pass B: it derives a new display label from model-owned mechanics, and display formatting alone never justifies a field-aware transform; no registered exception names it. **DELETE (move tier to the model/schema, or compute it client-side for display only)** |
| `_validate_combat_state` | Pass A: it returns error strings only; deleting it loses diagnostics, not player capability, since the caller only logs the errors. Pass B: warn-only validation is diagnostics, not filtering — no value is changed, so it passes as logging/telemetry. **KEEP** |
| `_validate_reputation` | Pass A: same as above — error strings consumed as warnings, so deletion costs diagnostics only. Pass B: it checks integer ranges and enum membership but returns messages without rewriting the reputation object. **KEEP** |
| `_validate_relationship` | Pass A: error-list diagnostics for trust/disposition ranges; the caller logs them and keeps the model values. Pass B: no mutation, no rejection in this caller, so it is telemetry, not a transform. **KEEP** |
| `_validate_world_time` | Pass A: diagnostics for day/hour/minute/time-of-day shape; the model values survive regardless of errors. Pass B: warn-only, values preserved, so it is allowed diagnostics. **KEEP** |
| `_validate_encounter_state` | Pass A: diagnostics for encounter type/difficulty enums, logged not enforced. Pass B: no value change, hence not a field-aware transform at all. **KEEP** |
| `_validate_frozen_plans` | Pass A: diagnostics for frozen-plan structure; the docstring itself says frozen plans are LLM-enforced via prompts, and this only surfaces shape errors. Pass B: warn-only shape checking, values untouched. **KEEP** |
| `_validate_directives` | Pass A: diagnostics for directive add/drop shapes, kept consistent with what `_coerce_directives_dict` accepts so valid inputs do not false-positive. Pass B: returns error strings only; the coercion path preserves values. **KEEP** |
| `_coerce_directives_dict` | Pass A: it normalizes dict-shaped directives into the canonical add/drop shape the rest of the server reads; the model could emit the canonical shape, but accepting its variants preserves turns that would otherwise break. Pass B: shape normalization that preserves every directive value (with metadata preserved on add) is pure structural parsing, not semantic filtering. **KEEP** |
| `_hoist_state_update_directives` | Pass A: it moves nested `state_updates.directives` to the root so one code path reads them; the model values are identical before and after. Pass B: a structural move preserving values and validation semantics, explicitly not a content decision. **KEEP** |
| `_validate_equipment_slots` | Pass A: diagnostics for forbidden/unknown slot names, logged not enforced. Pass B: returns error strings; the equipment object itself is unchanged by this function. **KEEP** |
| `_validate_arc_milestones` | Pass A: diagnostics for milestone status enums, logged not enforced. Pass B: warn-only, values preserved. **KEEP** |
| `_validate_time_pressure_warnings` | Pass A: diagnostics for boolean warning flags, logged not enforced. Pass B: warn-only, values preserved. **KEEP** |
| `_validate_resources` | Pass A: diagnostics dispatching to registry/resource validation, logged not enforced. Pass B: returns error strings only; it never rewrites a resource value. **KEEP** |
| `_validate_resource_count` | Pass A: diagnostics for non-negative integer counts (with integer-valued floats accepted), logged not enforced. Pass B: it normalizes only for the check itself and returns messages; the stored value is untouched. **KEEP** |
| `_validate_resource_metadata` | Pass A: diagnostics for reset-trigger/category metadata, logged not enforced. Pass B: warn-only, values preserved. **KEEP** |
| `_validate_required_mechanic_tuple` | Pass A: diagnostics for the all-or-none custom-mechanic field trio, logged not enforced. Pass B: returns a message, changes nothing. **KEEP** |
| `_validate_trigger_check_types` | Pass A: diagnostics for trigger-check name lists, logged not enforced. Pass B: warn-only. **KEEP** |
| `_validate_dice_expression` | Pass A: diagnostics for dice-expression shape, logged not enforced. Pass B: warn-only. **KEEP** |
| `_validate_apply_mode` | Pass A: diagnostics for apply-mode enum membership, logged not enforced. Pass B: warn-only. **KEEP** |
| `_validate_resource_mechanic` | Pass A: diagnostics aggregating the four mechanic checks above, logged not enforced. Pass B: aggregation of messages only. **KEEP** |
| `_validate_resource_registry_entry` | Pass A: diagnostics per registry entry (counts + metadata + mechanic), logged not enforced. Pass B: warn-only aggregation. **KEEP** |
| `_validate_resource_registry` | Pass A: diagnostics over the whole registry allowing partial deltas, logged not enforced. Pass B: warn-only, delta-friendly by design. **KEEP** |
| `_validate_player_character_data_resources` | Pass A: diagnostics catching malformed entries at the canonical registry location (per the prompt, not under `resources`), logged not enforced. Pass B: warn-only surfacing of model mistakes, values preserved. **KEEP** |
| `_validate_spell_slots` | Pass A: diagnostics for spell-slot level keys and counts, logged not enforced. Pass B: warn-only; it does not rewrite any slot count (contrast `_normalize_spell_slots_delta`, DELETE below). **KEEP** |
| `_normalize_spell_slots_delta` | Pass A: the model can emit in-range slot counts under the response schema, and the prompt can state the bound; the server need not silently rewrite over-max counts to max or negatives to 0. Pass B: it clamps `current`/`used` into `[0, max]` — a field-aware transform that changes a campaign fact (slots burned) — with no registered exception and no necessity proof; "the LLM occasionally overcounts" is exactly the normalization/determinism rationale the spec rejects. **DELETE (preserve the model delta; surface over-max counts as warnings for the prompt/schema to fix)** |
| `_validate_class_features` | Pass A: diagnostics for class-feature structure, logged not enforced. Pass B: warn-only, values preserved. **KEEP** |
| `_validate_attributes` | Pass A: diagnostics for base/derived attribute keys, logged not enforced. Pass B: warn-only. **KEEP** |
| `_validate_experience` | Pass A: diagnostics for experience current/needed integers, logged not enforced. Pass B: warn-only. **KEEP** |
| `_validate_death_saves` | Pass A: diagnostics for death-save counts in 0–3, logged not enforced. Pass B: warn-only. **KEEP** |
| `_validate_spells_known` | Pass A: diagnostics for spell-entry shape, logged not enforced. Pass B: warn-only. **KEEP** |
| `_validate_status_conditions` | Pass A: diagnostics for status-condition strings (unknown conditions only warned, custom conditions allowed), logged not enforced. Pass B: warn-only and explicitly permissive, so it is not a filter. **KEEP** |
| `_validate_active_effects` | Pass A: diagnostics for active-effect strings, logged not enforced. Pass B: warn-only. **KEEP** |
| `_validate_combat_stats` | Pass A: diagnostics for speed/perception integers, logged not enforced. Pass B: warn-only. **KEEP** |
| `_validate_item` | Pass A: diagnostics for item sub-shapes (only enforced for known typed shapes; open-set general items pass), logged not enforced. Pass B: warn-only and deliberately permissive for unknown types. **KEEP** |
| `_strip_embedded_planning_json` | Pass A: the model can keep planning JSON out of narrative under the response schema (planning_block is a separate field), so stripping is replaceable by schema discipline — but until then, discarding the block loses model content. Pass B: it deletes text from the model narrative, which is semantic filtering even though the content is JSON-shaped; no registered exception covers narrative deletion. The value-preserving fix routes the block into `planning_block` instead of dropping it. **ADAPT (route extracted planning JSON into planning_block; never silently discard)** |
| `_remove_planning_json_blocks` | Pass A: same as above — brace-matched removal of planning-shaped JSON from narrative text, replaceable by schema discipline. Pass B: deletion of model text with no registered exception; the block's choices are campaign-relevant content, not noise. **ADAPT (same routing fix as `_strip_embedded_planning_json`; delete the discard path)** |
| `_is_planning_block_json` | Pass A: a predicate (thinking + choices keys, size-bounded, valid JSON) that the routing fix needs to decide what is a planning block. Pass B: a pure predicate changing nothing by itself; it only classifies. **KEEP** |
| `strip_mixed_language_characters` | Pass A: the model can be instructed by prompt to write in the campaign language, and the response schema cannot prevent CJK leakage — but that inconvenience does not license deleting prose. Pass B: it deletes CJK characters from model-authored narrative, which is semantic filtering of prose (a character can be a name, a term, or quoted text), with no registered exception and no necessity proof beyond "narrative consistency". **DELETE (enforce language in prompt; never delete model prose server-side)** |
| `_pop_case_insensitive_value` | Pass A: it resolves case-variant keys to the canonical key, preserving the first non-empty value; the model could emit exact-case keys, but case variance breaks no turn if resolved. Pass B: key resolution preserving the model's value is structural parsing, not a content decision. **KEEP** |
| `_coerce_npc_update_entry` | Pass A: it decodes the framed NPC patch transport format (`NPC_PATCH_JSON_PREFIX` + JSON) that only the server defines, so the model cannot supply the decoded form directly. Pass B: decoding a transport framing preserves values when parseable and warns on malformed framing; it invents no NPC fact. **KEEP** |
| `NarrativeResponse.__init__` | Pass A: constructing the typed response is the parser's core job — without it there is no structured turn object for persistence or display. Pass B: it orchestrates the validators below, so its verdict inherits theirs: keep the construction and the warn-only validators, and apply each child's ADAPT/DELETE (planning routing, CJK deletion removal, rewards default removal, spell-slot clamp removal). **ADAPT (keep construction; apply all child ADAPT/DELETE rows in this table)** |
| `NarrativeResponse._validate_narrative` | Pass A: narrative must be a string and embedded planning JSON must not leak into displayed prose; both are achievable by schema + routing. Pass B: it chains the embedded-JSON strip (ADAPT to routing) with the CJK strip (DELETE), so the method as written is a mixed filter. **ADAPT (keep string check + planning-JSON routing; delete the CJK strip call)** |
| `NarrativeResponse._validate_entities` | Pass A: trimming entity strings and dropping blanks is whitespace hygiene the model could do itself, but it changes no entity identity. Pass B: it preserves every non-blank entity verbatim (only `str.strip()`), so it is value-preserving parsing. **KEEP** |
| `NarrativeResponse._validate_state_updates` | Pass A: the method's value is its warn-only validation fan-out plus the overlay sanitizer; the model cannot self-report schema-gate diagnostics. Pass B: the `_validate_*` fan-out is warn-only (KEEP), but it also runs `sanitize_state_updates_overlay`, whose near-match remapping is a semantic key rewrite (see `schemas/validation.py`, ADAPT). **ADAPT (keep warn-only fan-out; remove near-match remapping from the overlay step)** |
| `NarrativeResponse._validate_debug_info` | Pass A: debug-info type hygiene (non-dict becomes `{}`) protects downstream log/display code; debug info is server-side metadata, not campaign facts. Pass B: transport/metadata handling, no campaign value involved. **KEEP** |
| `NarrativeResponse._validate_string_field` | Pass A: string fields need a string type for display/persistence, and the model can emit strings under the schema; coercion here is a type contract, not a content choice. Pass B: null becomes `""` and non-strings are stringified (including a JSON dump for dict/list `resources`), preserving content in the field's declared type. **KEEP** |
| `NarrativeResponse._validate_bool_field` | Pass A: the model can emit real booleans under the schema, so guessing at unknown strings is unnecessary. Pass B: its string table is benign, but unknown non-empty strings fall through to a falsy default, inventing `False` for a model value the server did not understand — the same defect as `_coerce_bool`, with no registered exception. **ADAPT (unknown strings return None, never a guessed boolean)** |
| `NarrativeResponse._validate_list_field` | Pass A: list fields need list type for downstream code, and dice-roll dicts need a display string; the model could emit the canonical list form, but formatting preserves content. Pass B: it drops only `None` items and formats dict dice rolls into display strings, preserving every real item's content. **KEEP** |
| `NarrativeResponse._validate_tool_requests` | Pass A: tool requests must be a list of dicts to be executable; a non-dict item cannot be executed by any tool, so dropping it loses no executable instruction. Pass B: a transport type gate for tool execution (an allowed server function), not a campaign-fact filter. **KEEP** |
| `NarrativeResponse._format_dice_roll_object` | Pass A: formatting a dice-roll dict into a human-readable string is display work the client could do from the same dict. Pass B: it produces a display string and changes no stored value; display formatting alone would not justify a state transform, but this performs no state transform. **KEEP (display-only; must never write back into stored rolls)** |
| `NarrativeResponse._validate_rewards_box` | Pass A: the model can emit well-typed reward numbers under the response schema, and the state-owned `reward_event` receipt (see `schemas/reward_event_schema.py`) is the canonical award path, so server-invented reward numbers are unnecessary. Pass B: its inner number coercer defaults missing/unparseable numbers to `0.0`, inventing a zero reward — the clamp-to-zero pattern the repo's UX-first rule explicitly calls a rejection in disguise — with no registered exception. **ADAPT (preserve-or-omit + warn on bad types; never default a reward number to 0)** |
| `NarrativeResponse._coerce_level_int` | Pass A: level must be an integer for the level-up machinery, and unparseable input correctly yields `None` rather than a guessed level. Pass B: it preserves-or-omits (never invents a level), which is the strict-compliant shape. **KEEP** |
| `NarrativeResponse._validate_level_up_signal` | Pass A: the level-up signal's shape must be canonical for the modal machinery to read it, and the model authors the signal under the schema. Pass B: it deep-copies and normalizes the signal's `level_up` string form, but silent reinterpretation of a model string into a boolean-ish signal is a semantic choice without a registered exception covering this method. **ADAPT (keep shape check + warn; drop silent reinterpretation of the signal value)** |
| `NarrativeResponse._validate_action_resolution` | Pass A: action resolution is the audit trail for player actions, and its absence is a warning, not a turn rejection — the narrative is always returned, which is the repo's UX-first rule in action. Pass B: warn-only enforcement plus a `{}` fallback for absence (absence, not invention) keeps it within diagnostics; it decides no outcome. **KEEP** |
| `NarrativeResponse._add_server_system_warning` | Pass A: the trusted server-warning channel is how diagnostics reach the player; the model cannot write to it (that would defeat its purpose). Pass B: it appends to a server-owned debug channel, a logging function under §6.1. **KEEP** |
| `NarrativeResponse._warn_on_unclean_action_resolution_dice` | Pass A: dice-audit warnings (missing roll fields, unclean notation) are diagnostics the model cannot self-report after generating the roll. Pass B: warn-only by construction (185 lines of warnings, no mutation), and adjacent to §6.2 anti-cheat — but it only warns, so the "audit trail may go async" allowance is not even needed; it already blocks nothing. **KEEP** |
| `NarrativeResponse._validate_directives_field` | Pass A: callers index `directives['add']`/`['drop']`, so a canonical empty shape for invalid input prevents crashes; the model could emit the canonical shape, but the fallback shape contains no domain values. Pass B: structural default shape only, preserving any valid directives verbatim. **KEEP** |
| `NarrativeResponse._validate_dice_audit_events` | Pass A: dice audit events must be a list of dicts for the audit trail, and the docstring explicitly keeps validation permissive so gameplay is never blocked. Pass B: a permissive type gate for the §6.2 audit trail, changing no event content. **KEEP** |
| `NarrativeResponse._validate_planning_block` | Pass A: planning blocks must be JSON to be actionable, but a model string block may still contain parseable JSON choices, so returning `{}` for all strings discards recoverable content. Pass B: the dict branch delegates to the JSON validator (ADAPT below), while the string branch drops the block outright with an error log — a content deletion with no registered exception covering string blocks. **ADAPT (attempt JSON parse of string blocks; on failure warn + preserve raw text for audit instead of returning {})** |
| `NarrativeResponse._validate_planning_block_json` | Pass A: planning choices are the player's next actions; the model authors them under the schema, and the server cannot know better than the model which choices are valid. Pass B: it does shape normalization (thinking/context strings, choice id/text/description presence) but also DROPS choices with invalid risk levels, invalid modal actions, or missing fields — semantic filtering of player options. The registered spec `level_up_schema.normalize_planning_choice_shape` covers shape normalization only and carries `RUNTIME_EVIDENCE_MISSING`, so it does not prove dropping necessary. **ADAPT (slim to shape normalization + warn; preserve every model choice, including ones with unknown risk/modal values)** |
| `NarrativeResponse._sanitize_planning_block_content` | Pass A: removing script tags from planning text is display safety, and the frontend already handles display — the model text need not be mutated at parse time. Pass B: it mutates model-authored text (removing script-like patterns), which is a content transform; as output-encoding safety it belongs at render time, not in stored state, and no registered exception names it. **ADAPT (stop mutating stored planning text; escape at render time instead)** |
| `NarrativeResponse.get_unified_action_resolution` | Pass A: legacy dice fields still exist in older payloads, and normalizing them into the canonical action-resolution shape preserves audit history the model cannot retroactively rewrite. Pass B: value-preserving legacy compatibility — it returns the explicit field when present and only derives from legacy fields otherwise, inventing no roll. **KEEP** |
| `NarrativeResponse._normalize_legacy_to_action_resolution` | Pass A: same as above — a legacy-to-canonical projection for dice_rolls + audit events. Pass B: it builds a canonical shape from existing values (`player_input: None` marks unknown, it does not guess), so it preserves rather than invents. **KEEP** |
| `NarrativeResponse.to_dict` | Pass A: serialization to a dict is the transport form for persistence and display; without it the response cannot leave the parser. Pass B: it projects fields verbatim and strips only a nested admin carrier when an outcome is present — transport hygiene for a server-owned carrier, not a campaign-fact change. **KEEP** |
| `EntityTrackingInstruction.__init__` | Pass A: a prompt-construction carrier (manifest + expected entities + format); deleting it removes the structured prompt injection the model needs to track entities. Pass B: it stores prompt inputs, it filters nothing. **KEEP** |
| `EntityTrackingInstruction.create_from_manifest` | Pass A: it builds the entity-tracking prompt injection from a scene manifest, which is prompt-side work Pass A explicitly allows (the model needs the requirement in the prompt). Pass B: prompt construction, not output filtering — it writes instructions, not verdicts on output. **KEEP** |
| `EntityTrackingInstruction.to_prompt_injection` | Pass A: it renders the tracking requirement as prompt text; without it the model has no checkable entity requirement. Pass B: prompt text generation, no output mutation. **KEEP** |
| `_combine_god_mode_and_narrative` | Pass A: god-mode responses and narrative can duplicate each other, and the placeholder prevents double display; the model cannot deduplicate its own two fields after emission. Pass B: it is a display projection on the admin (god-mode) path — it substitutes a placeholder for display, it does not change stored campaign state. **KEEP (display projection on the admin path only)** |
| `parse_structured_response` | Pass A: this is the one parser — deleting it removes JSON parsing, markdown extraction, recovery, and typed construction for every structured turn, which no prompt can replace. Pass B: its core (json.loads + grammar-preserving recovery + typed construction) is pure parsing, but it also drives the mutating validators rowed above (planning-choice dropping, CJK stripping, rewards defaulting, spell-slot clamping), so the function as a whole inherits their verdict. **ADAPT (keep parsing + recovery core intact; apply all child ADAPT/DELETE rows; do not split — one parser must stay one function)** |
| `_is_valid_root_narrative_terminator` | Pass A: a grammar predicate deciding whether a quote can terminate the root narrative string, needed for recovery parsing the model cannot do for itself. Pass B: pure JSON-grammar logic, no value judgment. **KEEP** |
| `_decode_rfc8259_narrative_string` | Pass A: RFC 8259 decoding with unknown-escape preservation recovers model prose from malformed JSON that `json.loads` alone would lose. Pass B: it preserves unknown escapes literally and trims only provably-dangling escapes — value-preserving decoding, not filtering. **KEEP** |
| `_decode_rfc8259_narrative_live_prefix` | Pass A: live-prefix decoding for streaming lets the frontend show narrative as it arrives; the model cannot stream its own prefix decoding. Pass B: it withholds (returns None) rather than invents when the tail is mid-escape — fail-absent, not fail-invented. **KEEP** |
| `extract_root_narrative_live_prefix` | Pass A: the narrow streaming entry point for the live narrative prefix, with eligibility decided by the scanner so unrelated "narrative" mentions cannot suppress it. Pass B: a read-only extraction for transport streaming, changing no value. **KEEP** |
| `_extract_narrative_from_truncated_json` | Pass A: truncated/interrupted JSON still contains a salvageable narrative, and recovering it is what makes interrupted streams displayable instead of empty. Pass B: a zero-regex state machine that extracts the model's own string value — pure parsing recovery. **KEEP** |
| `_extract_narrative_from_raw_text` | Pass A: fail-open extraction from non-JSON plain text preserves a turn that would otherwise be lost entirely; the model already wrote the text. Pass B: it selects (strips markdown fences) rather than invents or deletes prose content. **KEEP** |
| `create_generic_json_instruction` | Pass A: it returns `""` by design because the format lives in `game_state_instruction.md`, so deleting it loses nothing — callers already get the format elsewhere. Pass B: a dead no-op with zero callers outside its own definition (its only value is a docstring explaining its own emptiness). **DELETE** |
| `create_structured_prompt_injection` | Pass A: it builds the structured prompt injection (full entity tracking when entities exist, generic format otherwise) that the model needs to emit valid JSON. Pass B: prompt construction, not output filtering. **KEEP** |
| `validate_entity_coverage` | Pass A: it reports mentioned-vs-expected entity coverage as a dict for diagnostics; the model cannot self-report coverage authoritatively. Pass B: it computes a report and mutates nothing — a diagnostic, unlike `entity_validator`, which scores and retries. **KEEP** |
| `extract_interrupted_parse_result` | Pass A: a single typed result for interrupted streams (recovered narrative + telemetry + atomicity) is what lets an interrupted turn display honestly instead of vanishing. Pass B: transport atomicity — it guarantees state-bearing fields are cleared on interrupted parses so a partial turn is never persisted as complete, which is durable-write integrity, not domain filtering. **KEEP** |

### 2. `mvp_site/narrative_response_schema.py` — classes, enums, and module symbols

Rows are compact (2 sentences each) but each symbol is judged individually;
"schema dict" rows mean the dict is a response-schema contract, which Pass A
owns and Pass B treats as transport, not filtering.

| Unit | Justification + verdict |
|---|---|
| `ParseOutcome` (enum) | Pass A: parse-outcome vocabulary (success/recovered/interrupted/failed) the model cannot self-report. Pass B: telemetry vocabulary for logging under §6.1, no value changed. **KEEP** |
| `ParseErrorClass` (enum) | Pass A: error-class vocabulary for parse diagnostics. Pass B: telemetry vocabulary, no value changed. **KEEP** |
| `ParseTelemetry` (frozen dataclass) | Pass A: the typed telemetry carrier for parse results. Pass B: immutable logging data under §6.1. **KEEP** |
| `InterruptedParseResult` (frozen dataclass) | Pass A: the typed carrier for interrupted-parse results (narrative + telemetry + structured response). Pass B: transport atomicity carrier for durable-write integrity. **KEEP** |
| `SchemaRejectionError` (exception) | Pass A: the typed error for schema rejection, caught in `llm_service` as a warning + retry attempt, not a silent drop. Pass B: an error carrier, not a filter — callers warn and re-attempt via the model, which is the honest failure path. **KEEP** |
| `NarrativeResponse` (class) | Pass A: the typed structured-response object every downstream consumer (persistence, display, audit) reads. Pass B: a carrier whose verdict follows its `__init__`/validator rows (ADAPT overall). **ADAPT (same child fixes as `__init__`)** |
| `EntityTrackingInstruction` (class) | Pass A: the prompt-injection carrier for entity tracking. Pass B: prompt construction only. **KEEP** |
| `JSON_PARSE_FALLBACK_MARKER` | Pass A: the honest error string ("Invalid JSON response received. Please try again.") shown when parsing fails; the model cannot display its own failure message. Pass B: an error message, not fake prose — it discloses failure instead of inventing story. **KEEP** |
| `DEFAULT_NARRATIVE_FALLBACK` | Pass A: "The story continues..." is server-invented prose used in `parse_structured_response` fail-open paths (lines ~6534, ~6722); the model could retry or the UI could show the honest marker instead. Pass B: inventing narrative text is semantic content creation with no registered exception. **DELETE (use the honest fallback marker or an empty narrative + model retry, never fake prose)** |
| `NARRATIVE_SOURCE_PROVIDER` / `NARRATIVE_SOURCE_SERVER_FALLBACK` | Pass A: provenance labels distinguishing model narrative from server fallback, needed for honest display and debugging. Pass B: telemetry labels under §6.1, no value changed. **KEEP** |
| `_SOCIAL_HP_CHALLENGE_OMITTED` | Pass A: a sentinel distinguishing "challenge omitted" from "challenge null" in transport projection. Pass B: a structural sentinel, not a campaign value. **KEEP** |
| `FALLBACK_PLANNING_BLOCK` | Pass A: the server-authored choice block used by `_create_fallback_planning_block`; a display-layer fallback can serve the same UI need without pretending to be model output. Pass B: server-invented player choices, no registered exception. **ADAPT (display-layer only; never persist as model planning_block)** |
| `PARSE_OUTCOMES` / `PARSE_ERROR_CLASSES` | Pass A: frozensets of the telemetry vocabularies, used to validate telemetry values. Pass B: logging vocabulary, no value changed. **KEEP** |
| `PARSE_TELEMETRY_MAX_OFFSET` / `PARSE_TELEMETRY_MAX_REQUEST_ID` | Pass A: bounds for telemetry fields (10,000,000 / 128) keeping logs bounded. Pass B: bounded capacity for logging under §6.1. **KEEP** |
| `_SHORT_TEXT` (500) / `_HEADER_TEXT` (8000) / `_LONG_TEXT` (20000) / `_NARRATIVE_TEXT` (120000) | Pass A: provider `maxLength` bounds for response-schema string fields; without them Gemini payloads are unbounded. Pass B: bounded capacity for provider transport, not content filtering of returned values. **KEEP** |
| `NARRATIVE_RESPONSE_JSON_SCHEMA` | Pass A: the base response schema — the Pass A mechanism itself. Pass B: contract construction, no value touched. **KEEP** |
| `NARRATIVE_RESPONSE_JSON_SCHEMA_STORY` | Pass A: the story-mode schema variant (narrative + planning_block required). Pass B: schema variant selection, no value touched. **KEEP** |
| `_GAMEPLAY_PCD_PATCH_PROPERTIES` | Pass A: the gameplay PCD patch property set derived for the response schema. Pass B: schema assembly. **KEEP** |
| `_ACTION_RESOLUTION_SCHEMA` | Pass A: the action-resolution sub-schema binding the audit trail shape. Pass B: schema assembly. **KEEP** |
| `_GAMEPLAY_PLANNING_BLOCK_SCHEMA` | Pass A: the gameplay planning-block sub-schema binding choice shape. Pass B: schema assembly. **KEEP** |
| `_gameplay_patch_path` / `_GAMEPLAY_STATE_PATCH_SCHEMAS` | Pass A: loading the externalized gameplay patch JSON so schema patches are data, not hand-duplicated literals. Pass B: schema loading, no value touched. **KEEP** |
| `GAMEPLAY_NPC_DATA_PATCH_SCHEMA` / `GAMEPLAY_CORE_MEMORIES_MUTATION_SCHEMA` / `_CORE_MEMORY_RETAIN_SCHEMA` / `GAMEPLAY_CUSTOM_CAMPAIGN_STATE_PATCH_SCHEMA` | Pass A: the named patch schemas projected from the gameplay patch file for the response contract. Pass B: schema assembly. **KEEP** |
| `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY` | Pass A: the canonical gameplay response schema, the most-used binding contract. Pass B: schema assembly. **KEEP** |
| `NARRATIVE_RESPONSE_JSON_SCHEMA_LEVEL_UP` / `NARRATIVE_RESPONSE_JSON_SCHEMA_LEVEL_UP_AUDIT` | Pass A: level-up and level-up-audit schema variants with the repair contract. Pass B: schema assembly. **KEEP** |
| `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_REWARD_EVENT` | Pass A: the gameplay schema variant requiring the state-owned reward receipt. Pass B: schema assembly. **KEEP** |
| `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_OMISSION_TOLERANT` | Pass A: the omission-tolerant gameplay variant for turns where strict requiredness would lose the turn. Pass B: schema variant selection; tolerance here means fewer rejections, not value changes. **KEEP** |
| `_SEVEN_TIME_ADVANCING_AGENTS` / `_REWARD_AUTHORING_AGENTS` | Pass A: agent sets driving schema-variant selection (time-advancing / reward-authoring). Pass B: routing tables for contract selection, no value touched. **KEEP** |
| `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_CHARACTER_MODE` / `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_SOCIAL_CHALLENGE` / `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_REWARD_EVENT_SOCIAL_CHALLENGE` / `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_SPICY` / `NARRATIVE_RESPONSE_JSON_SCHEMA_NARRATIVE` / `NARRATIVE_RESPONSE_JSON_SCHEMA_REWARD_AUTHORING` / `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_REWARD_EVENT_ACTIVE_SOCIAL_CHALLENGE` / `NARRATIVE_RESPONSE_JSON_SCHEMA_NARRATIVE_NORMAL_PCD_SOCIAL_CHALLENGE` / `NARRATIVE_RESPONSE_JSON_SCHEMA_GAMEPLAY_NORMAL_PCD_SOCIAL_CHALLENGE` | Pass A: mode/agent schema variants (character mode, social challenge, spicy, narrative, reward authoring, PCD variants) — each is a binding contract for its turn type. Pass B: schema assembly/selection only. **KEEP** |
| `_REWARD_EVENT_SOCIAL_CHALLENGE_REPAIR_BASE` / `_NARRATIVE_NORMAL_PCD_REPAIR_BASE` / `_NARRATIVE_NORMAL_PCD_SOCIAL_CHALLENGE_REPAIR_BASE` / `_LEGACY_MEMORY_REPAIR_BASES` | Pass A: repair-base schemas for audit/repair turns, giving the model a valid shape to repair into. Pass B: schema assembly. **KEEP** |
| `_MODES_REQUIRING_PLANNING_BLOCK` / `_AGENTS_REQUIRING_PLANNING_BLOCK` | Pass A: routing tables deciding which modes/agents must carry a planning block in their schema. Pass B: contract-selection tables, no value touched. **KEEP** |
| `_NARRATIVE_GAMEPLAY_MODES` / `_NARRATIVE_GAMEPLAY_AGENTS` / `_GAMEPLAY_MODES` / `GAMEPLAY_AGENTS` / `_GAMEPLAY_AGENTS` / `_NON_GAMEPLAY_MODES` / `_NON_GAMEPLAY_AGENTS` | Pass A: mode/agent routing sets for schema selection (including the line-1102 reassignment aliasing `_GAMEPLAY_AGENTS` to `GAMEPLAY_AGENTS`). Pass B: routing tables only. **KEEP** |
| `MIN_NARRATIVE_LENGTH` (100) | Pass A: a minimum-length constant with no use found in the module or its callers in this audit — deleting it removes no check and no capability. Pass B: a dead constant proves nothing and guards nothing. **DELETE (dead; if a length gate is ever wanted, it must be a prompt rule, not a silent server gate)** |
| `JSON_MARKDOWN_PATTERN` / `GENERIC_MARKDOWN_PATTERN` | Pass A: the markdown-fence extraction patterns for the parser — the only regex use in this file that is pure envelope extraction, not semantic routing. Pass B: envelope parsing preserving the enclosed JSON verbatim. **KEEP** |
| `_RUN_WARNING_COUNTS` | Pass A: per-process warning-escalation counters for `_log_thresholded_warning`. Pass B: logging state under §6.1. **KEEP** |
| `CJK_PATTERN` | Pass A: the CJK regex serves only `strip_mixed_language_characters` (DELETE above); with that function gone it has no other use. Pass B: a deletion pattern dies with its deleter. **DELETE (with `strip_mixed_language_characters`)** |
| `MAX_PLANNING_JSON_BLOCK_CHARS` (50000) | Pass A: a size bound for planning-block JSON detection, keeping the brace-matching scan bounded. Pass B: bounded capacity for parsing. **KEEP** |
| `CHOICE_SCHEMA` / `PLANNING_BLOCK_SCHEMA` | Pass A: the choice and planning-block shape schemas used by the JSON validator. Pass B: schema assembly; their use as drop gates is what the validator ADAPT removes, the schemas themselves stay as warn vocabulary. **KEEP (as shape/warn vocabulary; must not gate choice preservation)** |
| `VALID_RISK_LEVELS` / `VALID_MODAL_ACTIONS` / `VALID_QUALITY_TIERS` | Pass A: vocabularies for risk levels, modal actions, and quality tiers that the model authors under the schema. Pass B: as warn-only vocabularies they are diagnostics, but as drop gates (current planning-validator use) they are semantic filtering with no proven registered exception. **ADAPT (retain as warn-only vocabulary; never drop a choice/tier for falling outside them)** |
| `VALID_CONFIDENCE_LEVELS` | Pass A: confidence-level vocabulary for planning metadata. Pass B: diagnostic vocabulary, no gating use found that changes values. **KEEP** |
| `COMBAT_PHASE_ENUM` / `COMBAT_STATE_SCHEMA` | Pass A: combat-phase vocabulary + shape schema for warn-only validation. Pass B: diagnostic vocabulary/schema, values preserved. **KEEP** |
| `VALID_NOTORIETY_LEVELS` / `VALID_STANDING_LEVELS` / `REPUTATION_PUBLIC_SCHEMA` / `REPUTATION_PRIVATE_SCHEMA` | Pass A: reputation vocabularies + shape schemas for warn-only validation. Pass B: diagnostic vocabulary/schema. **KEEP** |
| `VALID_DISPOSITIONS` / `RELATIONSHIP_SCHEMA` | Pass A: relationship disposition vocabulary + shape schema for warn-only validation. Pass B: diagnostic vocabulary/schema. **KEEP** |
| `VALID_TIME_OF_DAY` / `WORLD_TIME_SCHEMA` | Pass A: time-of-day vocabulary + shape schema for warn-only validation. Pass B: diagnostic vocabulary/schema. **KEEP** |
| `VALID_ENCOUNTER_TYPES` / `VALID_ENCOUNTER_DIFFICULTIES` / `ENCOUNTER_STATE_SCHEMA` | Pass A: encounter vocabularies + shape schema for warn-only validation. Pass B: diagnostic vocabulary/schema. **KEEP** |
| `FROZEN_PLANS_SCHEMA` / `DIRECTIVES_SCHEMA` | Pass A: frozen-plan and directive shape schemas for warn-only validation. Pass B: diagnostic schemas. **KEEP** |
| `VALID_EQUIPMENT_SLOTS` / `FORBIDDEN_SLOT_MAPPINGS` | Pass A: slot vocabulary derived from `get_known_equipment_slots` / legacy aliases in `schemas/validation.py`, used for warn-only slot validation. Pass B: schema-derived diagnostic vocabulary. **KEEP** |
| `VALID_ARC_MILESTONE_STATUS` / `ARC_MILESTONE_SCHEMA` | Pass A: milestone vocabulary + shape schema for warn-only validation. Pass B: diagnostic vocabulary/schema. **KEEP** |
| `TIME_PRESSURE_WARNINGS_SCHEMA` / `RESOURCES_SCHEMA` | Pass A: warning-flag and resource shape schemas for warn-only validation. Pass B: diagnostic schemas. **KEEP** |
| `VALID_SPELL_SLOT_LEVELS` / `SPELL_SLOTS_SCHEMA` | Pass A: spell-slot level vocabulary derived from `spell_slots_schema.json`, used for warn-only validation (not for clamping — the clamp lives in `_normalize_spell_slots_delta`, DELETE). Pass B: diagnostic vocabulary/schema. **KEEP** |
| `VALID_CLASS_FEATURES` / `CLASS_FEATURES_SCHEMA` | Pass A: class-feature vocabulary + shape schema for warn-only validation. Pass B: diagnostic vocabulary/schema. **KEEP** |
| `VALID_ATTRIBUTE_NAMES_ABBREV` / `VALID_ATTRIBUTE_NAMES_FULL` / `VALID_ATTRIBUTE_NAMES` / `ATTRIBUTE_NAME_MAPPING` | Pass A: attribute-name vocabularies plus the abbreviation-to-full-name mapping, letting the validator accept both model spellings. Pass B: alias mapping preserving meaning (STR = strength), i.e. structural, not semantic. **KEEP** |
| `DEPRECATED_ATTRIBUTE_KEYS` | Pass A: the deprecated-key set (`secondary_attribute`) used inside warn-only `_validate_attributes`. Pass B: diagnostic vocabulary only — it must warn, never drop the key's value. **KEEP (warn-only; any caller that drops on this set inherits DELETE)** |
| `ATTRIBUTES_SCHEMA` / `EXPERIENCE_SCHEMA` / `DEATH_SAVES_SCHEMA` / `SPELLS_KNOWN_SCHEMA` | Pass A: shape schemas for attributes, experience, death saves, and spells-known for warn-only validation. Pass B: diagnostic schemas. **KEEP** |
| `VALID_STATUS_CONDITIONS` / `STATUS_CONDITIONS_SCHEMA` / `ACTIVE_EFFECTS_SCHEMA` | Pass A: status-condition vocabulary (explicitly permissive of custom conditions) + shape schemas for warn-only validation. Pass B: diagnostic vocabulary/schemas. **KEEP** |
| `COMBAT_STATS_SCHEMA` / `VALID_DAMAGE_TYPES` / `VALID_ARMOR_TYPES` / `WEAPON_SCHEMA` / `ARMOR_SCHEMA` | Pass A: combat-stat, damage-type, armor-type vocabularies + weapon/armor shape schemas for warn-only item validation. Pass B: diagnostic vocabularies/schemas. **KEEP** |
| `_PARTIAL_ESCAPE` / `_SURROGATE` | Pass A: regex helpers for the RFC 8259 live-prefix decoder (partial escapes, lone surrogates). Pass B: pure grammar parsing aids, no value judgment. **KEEP** |

### 3. `mvp_site/llm_parser.py` — functions/methods

| Unit | Justification + verdict |
|---|---|
| `_lazy_module` | Pass A: lazy module proxies defer heavy imports (genai ~840ms, firestore ~500ms) to first use, cutting cold start; the model cannot affect import timing. Pass B: capacity/latency optimization for transport, changing no value. **KEEP** |
| `_scrub_model_state_marker` | Pass A: it strips `_server_stamped` from untrusted model output; the model must never be able to forge a server stamp, so only the server can do this. Pass B: authorization — removing a forged server-ownership marker is a security operation on a server-owned key, not a campaign fact; it mirrors `firestore_service` scrubbing for test-mock reasons stated in its docstring. **KEEP** |
| `_bq_turn_index_from_state` | Pass A: it reads a turn index from several possible state keys for telemetry; the model cannot supply server telemetry. Pass B: logging under §6.1, read-only. **KEEP** |
| `_coerce_planning_block_dict` | Pass A: it accepts a planning block as dict or JSON string and returns the dict or None; the model could emit only dicts, but accepting its string form preserves turns. Pass B: pure shape coercion preserving values. **KEEP** |
| `_planning_block_has_actionable_choices` | Pass A: a predicate (choices present and non-blank, dict or list form) that the planning seams need to decide whether a block is usable. Pass B: a read-only predicate, changing nothing. **KEEP** |
| `_planning_block_is_server_generated` | Pass A: a predicate reading the `server_generated` flag, needed to distinguish server fallbacks from model blocks. Pass B: read-only flag check. **KEEP** |
| `_coerce_structured_response_dict` | Pass A: it normalizes a structured response (dict, pydantic `model_dump`, or `to_dict`) into a plain dict for the streaming seams; without it each seam would hand-roll the same conversion. Pass B: value-preserving transport normalization. **KEEP** |
| `_has_explicit_social_hp_clear` | Pass A: it detects an explicit root null / explicit-null attribute for social-HP clearing, the counterpart to `apply_social_hp_challenge_transport`. Pass B: a precedence predicate preserving the model's explicit clear; it invents nothing. **KEEP** |
| `_should_prefer_raw_model_planning_block` | Pass A: it decides when the raw model planning block (with actionable choices) should win over the processed block, e.g. when processing lost choices; the model's own choices are the ground truth here. Pass B: it preserves model-authored values rather than filtering them, so its direction is pro-model; a registered spec exists (`level_up_parser.raw_planning_preserve`) but carries `RUNTIME_EVIDENCE_MISSING`, so this row does NOT claim proven-exception status — it passes because it restores values, and the spec's evidence gap is flagged for the owning team. **KEEP (with evidence-gap flag on its registered spec)** |
| `_raw_planning_block_is_normal_gameplay` | Pass A: a predicate (actionable choices, no level-up choices) classifying a raw block as normal gameplay. Pass B: read-only classification, changing nothing. **KEEP** |
| `_raw_planning_block_has_level_up_review` | Pass A: a predicate (actionable choices + level-up review choice) classifying a raw block as a level-up review. Pass B: read-only classification. **KEEP** |
| `_preserve_raw_rewards_fields_if_missing` | Pass A: it restores `rewards_box` / `level_up_signal` from raw structured fields when processing dropped them, so a turn's rewards are not silently lost. Pass B: value-preserving repair — it copies model values back, it never invents or alters one. **KEEP** |
| `_structured_level_up_modal_active` | Pass A: it decides modal activity from committed state vs this response's activation, with a top-level-False-blocks-nested exception; the model could single-home the flag, but today it emits it in two places. Pass B: it is a suppression decision about a UI modal (server-owned presentation state), yet it overrides a model-authored nested activation — a semantic decision whose registered spec (`level_up_modal.top_level_false_blocks_nested_activation`) carries `RUNTIME_EVIDENCE_MISSING`, so necessity is unproven. **ADAPT (single-home the flag in prompt/schema so no server override is needed; keep the suppression only as an interim with an evidence deadline)** |
| `_build_custom_action_planning_block` | Pass A: it builds Continue/Custom-Action choices when the model returned none, preserving player control; the model could always be required to emit choices, but today it sometimes does not. Pass B: it authors server-written choices — semantic content creation — under a registered spec (`level_up_parser.custom_action_fallback`) that itself warns the fallback "may hide prompt/schema failure" and carries `RUNTIME_EVIDENCE_MISSING`. **ADAPT (emit the fallback at the display layer only; never persist it as the model's planning_block; fix the prompt to require choices)** |
| `resolve_location` | Pass A: it resolves the turn's location with priority location_confirmed → world_data.location, returning "" when the model gave none, and callers preserve the prior location on ""; the model authors both candidate fields. Pass B: precedence between two model-authored values, verbatim, inventing nothing ("" means absent, not a place); a registered spec exists (`location.legacy_location_fallback_in_resolve_location`) with `RUNTIME_EVIDENCE_MISSING`, flagged here but not load-bearing since no value is invented. **KEEP (with evidence-gap flag on its registered spec)** |
| `_ensure_custom_action_planning_block` | Pass A: it guarantees a planning block with actionable choices exists for the UI, falling back to the custom-action block when the model (raw or processed) has none. Pass B: same server-authorship problem as `_build_custom_action_planning_block`, under the same evidence-missing spec, plus a `suppress_raw_planning_block` path that can hide model output. **ADAPT (same display-layer-only fix; never suppress or replace a model block in persisted state)** |
| `warm_lazy_dependencies` | Pass A: startup warmup forcing lazy modules to load, so first player turns do not pay cold-start cost. Pass B: capacity/warmup for transport, changing no value. **KEEP** |
| `continue_story_streaming` | Pass A: a passthrough alias so streaming call sites (and tests) patch one name; deleting it only renames call sites. Pass B: pure delegation, no logic of its own. **KEEP** |
| `_committed_background_events` | Pass A: it reads already-committed background events from pre-turn state (worker-owned living-world data) for the streaming path. Pass B: a durable-state read; under §6.3 these events belong to async ticks, and reading committed ones here is the merge side, not a new decision. **KEEP** |
| `_enrich_streaming_structured_fields` | Pass A: it extracts living-world data and adds sequence metadata to streaming fields, mirroring `world_logic.process_action_unified`; the model cannot attach server sequence metadata itself. Pass B: the sequence-metadata half is transport (KEEP-worthy), but the living-world extraction half runs faction/living-world work on the turn path, which §6.3 explicitly moves to async background ticks merged on the next turn. **ADAPT (keep sequence metadata on the turn path; move living-world extraction into the §6.3 async tick, merged next turn)** |
| `_merge_server_system_warnings_for_streaming_persistence` | Pass A: it canonicalizes server warnings for streaming persistence/display, pruning duplicates the validator pre-check already suppresses. Pass B: warning-channel hygiene under §6.1, changing no campaign value. **KEEP** |
| `_append_level_xp_mismatch_warning` | Pass A: it appends a saved-state level/XP diagnostic to the trusted warning channel so a mismatch is visible instead of silent. Pass B: warn-only diagnostics under §6.1. **KEEP** |
| `_apply_level_up_orphan_fail_closed_warning` | Pass A: it surfaces a visible fail-closed warning for orphaned level-up crossings on the streaming path (the primary production path), matching the non-streaming counterpart. Pass B: warn-only and fail-visible, not fail-silent; it changes no level or XP value. **KEEP** |
| `_count_compliant_lw_events` | Pass A: it counts background events carrying all required living-world fields, a compliance metric for diagnostics. Pass B: read-only counting for telemetry. **KEEP** |
| `_warn_if_living_world_missing` | Pass A: it warns when living-world events are missing on trigger turns (every 3 turns / 24h), aiding debugging of the living-world instruction. Pass B: warn-only diagnostics; under §6.3 the warning remains valid telemetry for the async tick's output. **KEEP** |
| `_strip_living_world_fields_from_mapping` | Pass A: it pops authoritative living-world fields from state containers; the model could simply not emit them off-turn, but today it does, and the server deletes them. Pass B: deletion of model-authored living-world facts is semantic filtering — the server deciding living-world content — with no registered exception, and §6.3's answer is async-tick ownership with next-turn merge, not silent deletion. **DELETE (let the §6.3 async tick own living-world fields; never silently pop model LW content)** |
| `_restore_cooldown_living_world_state` | Pass A: it restores prior living-world state on cooldown turns via the living-world contract, preserving continuity the model cannot reconstruct. Pass B: restoring server-owned prior state is closer to durable-state preservation than to filtering, but as a turn-path LW operation it belongs in the §6.3 async merge, not inline. **ADAPT (fold into the §6.3 async tick merge; remove the inline turn-path restore)** |
| `_strip_cooldown_living_world_fields_for_streaming` | Pass A: it removes model-emitted living-world fields on streaming cooldown turns; the model could be prompted not to emit them, and the prompt is the correct enforcement point. Pass B: same deletion defect as `_strip_living_world_fields_from_mapping` — semantic filtering of model facts with no registered exception — now on the primary streaming path, where it is most harmful. **DELETE (cooldown enforcement belongs in prompt + async tick ownership, not in silent stripping)** |
| `_extract_header_value` | Pass A: it parses `Key: value` lines from normalized session-header text, a transport parsing helper. Pass B: pure text parsing preserving values. **KEEP** |
| `_build_early_metadata_payload` | Pass A: it builds best-effort early metadata (projected rewards_box/planning_block from canonical state) so the frontend renders pre-modal sections before streaming completes. Pass B: projection from canonical stored state for display, inventing no new campaign fact. **KEEP** |
| `_extract_god_mode_response_text` | Pass A: it extracts non-empty god-mode response text from dict or object payloads for the admin path. Pass B: value-preserving extraction on the admin path. **KEEP** |
| `stream_narrative_simple` | Pass A: simple text-only streaming without structured output or tool execution, for cases that need raw narrative only. Pass B: pure transport (provider streaming), no parsing or filtering of campaign facts. **KEEP** |
| `_log_stream_payload` | Pass A: it persists the raw LLM request/response pair for the simple streamer (forensics/debugging), which the model cannot do. Pass B: logging under §6.1, and it is already fail-soft (exceptions/disabled flag yield a warning, never block the stream) — but §6.1 still requires async/batched delivery where logging sits on a player turn path, which this row makes explicit. **ADAPT (confirm/convert delivery to async/batched per §6.1; the fail-soft behavior stays)** |
| `stream_with_context` | Pass A: it streams narrative from story context + user input for interactive continuation, the context-based counterpart to the simple streamer. Pass B: transport streaming with prompt assembly, no campaign-fact filtering. **KEEP** |
| `create_sse_response_headers` | Pass A: SSE headers (no-cache, keep-alive, no nginx buffering) are required for streaming to reach the client at all. Pass B: pure transport. **KEEP** |
| `stream_events_generator` | Pass A: it converts StreamEvent objects to SSE strings for Flask responses. Pass B: pure transport serialization. **KEEP** |
| `_bq_stream_timing_extra` | Pass A: it copies canonical pre-stream timing fields into BigQuery extra payloads for latency forensics. Pass B: logging/telemetry under §6.1, read-only copying. **KEEP** |
| `_clear_interrupted_state_fields` | Pass A: it enforces the stream atomicity boundary — an interrupted response must not persist state_updates, rewards, planning, or level-up signal as if complete. Pass B: durable-write integrity (transport boundary), not domain filtering; it clears fields precisely because they are uncommitted. **KEEP** |
| `_parse_interrupted_stream_response` | Pass A: it parses one interrupted transport response and enforces persistence atomicity via the parser's interrupted-result helper. Pass B: transport + durable-write integrity, delegating value recovery to the parser. **KEEP** |
| `_interrupted_source_text` | Pass A: it selects the server-owned complete source text when forensic raw text is capped (full_narrative over truncated raw text). Pass B: source selection for forensics/telemetry, changing no campaign value. **KEEP** |
| `_event_is_interrupted` | Pass A: it reads provider terminal outcome (falling back to legacy flags) to decide whether an event stream was interrupted. Pass B: a transport-status predicate. **KEEP** |
| `_apply_user_settings_to_state` | Pass A: it projects user routing preferences (debug_mode, spicy settings, etc.) from Firestore user settings into streaming state. Pass B: user-owned preference projection (authorization-adjacent: the user's own settings), not campaign facts. **KEEP** |
| `_prepare_streaming_game_state` | Pass A: it normalizes a streaming game-state input (GameState, dict, or snapshot) and applies routing preferences, so the streamer has one input shape. Pass B: transport normalization + preference projection, values preserved. **KEEP** |
| `_replay_governed_done_keys` | Pass A: it derives every done-payload key a concurrent replay governs (losing turn's staged keys + explicit carriers), so a replay cannot leak stale values. Pass B: durable-write conflict handling — replace-not-update for committed receipts — which is write-ownership logic, not a domain judgment about which game outcome is right. **KEEP (note: if the concurrency premise is ever challenged, the repo's concurrency-evidence rule requires observed overlap evidence; this row judges the mechanism, not the premise)** |
| `_apply_replayed_done_payload` | Pass A: it replaces replay-governed done fields with the winning committed values, because additive `dict.update` cannot clear keys the winner does not carry. Pass B: same durable-write ownership rationale as above; the winner is the committed receipt, not a server preference. **KEEP (same concurrency-evidence note)** |
| `_emit_post_persist_incident_telemetry` | Pass A: post-persist incident telemetry (level-up resolution flush, progression outcome) mirrors the non-streaming persist path's telemetry. Pass B: logging under §6.1, emitted after the durable write by design. **KEEP** |
| `_scene_commit_allowed` | Pass A: it gates scene-image ownership transfer on whether this attempt actually committed (not replayed, not audit-conflicted). Pass B: a durable-commit predicate for asset ownership, not a campaign-fact decision. **KEEP** |
| `stream_story_with_game_state` | Pass A: this is the production streaming flow (provider/model selection, agent selection, LLM request building, persistence seam) — deleting it removes streaming gameplay entirely, which no prompt can replace. Pass B: as orchestration it is transport + durable writes + tool execution, which Pass B allows — but as a 3,128-line function inside a module named for parsing, it is unmaintainable and it drags planning/LW/persist decisions into the parser's blast radius; the parser question is already answered by `parse_structured_response`, so this function must move, not merge. **ADAPT (split out of llm_parser.py into a streaming-orchestration module; keep behavior, change address; its internal planning/LW branches inherit the seam rows above)** |

### 4. `mvp_site/llm_parser.py` — classes and module symbols

| Unit | Justification + verdict |
|---|---|
| `_InterruptedPartialStreamError` (exception) | Pass A: the typed error for interrupted partial streams, letting callers distinguish interruption from other failures. Pass B: an error carrier for transport, changing no value. **KEEP** |
| `firestore_service` / `gemini_provider` / `llm_service` / `world_logic` / `rewards_engine` / `level_up_amend_reapply` / `living_world_contract` / `dice_integrity` / `action_resolution_utils` / `turn_idempotency` / `god_mode_executor` (lazy proxies) | Pass A: lazy module references keeping cold start low while preserving module-level import conventions. Pass B: capacity optimization for transport, no values involved. **KEEP** |
| `_CUSTOM_ACTION_CHOICE_ID` / `_CONTINUE_STORY_CHOICE_ID` / `_CONTINUE_STORY_CHOICE` / `_CUSTOM_ACTION_CHOICE` | Pass A: the choice constants backing the server fallback block; the UI needs choice ids to render actions. Pass B: they are server-authored choice content, so they inherit the display-layer-only ADAPT of `_build_custom_action_planning_block` — the constants stay, their persistence as model output goes. **ADAPT (display-layer constants only; never persisted as model planning_block)** |
| `_LP_SERVER_STAMPED_KEY` (`_server_stamped`) | Pass A: the server-stamp key name that `_scrub_model_state_marker` defends. Pass B: authorization marker vocabulary. **KEEP** |
| `_LW_REQUIRED_FIELDS` | Pass A: the living-world compliance field set (actor, action, location, outcome, event_type, status, discovery_condition) used by the compliance counter. Pass B: diagnostic vocabulary for telemetry; under §6.3 it describes what the async tick must produce. **KEEP** |
| `_REPLAY_GOVERNED_DONE_KEYS` | Pass A: the explicit carrier set supplementing derived replay-governed keys. Pass B: durable-write conflict vocabulary. **KEEP** |
| `POST_PERSIST_GUARD_FAILURES` (Counter) | Pass A: a process-level counter of post-persist guard failures for telemetry. Pass B: logging state under §6.1. **KEEP** |

### 5. `mvp_site/narrative_sync_validator.py` — full module (147 lines)

Module verdict: DELETE (except nothing — see rows). It is imported by
`llm_service` (production reference found), so deletion is a behavior change
that needs the caller's go-ahead, but the audit verdict is still DELETE: a
production caller does not rescue a semantic validator, and the replacement
is the prompt requirement + the `entities_mentioned` array + the parser's
`validate_entity_coverage` diagnostic.

| Unit | Justification + verdict |
|---|---|
| `EntityPresenceType` (enum) | Pass A: presence-type vocabulary (physically_present / mentioned_absent / implied_present / ambiguous) duplicating `entity_validator`'s identical enum; the model cannot use a server enum to prove presence. Pass B: vocabulary for a semantic judgment the server must not make — prose presence is a model-owned fact, and substring/regex classification cannot establish it. **DELETE (duplicate of the entity_validator enum, deleted there too)** |
| `EntityContext.__post_init__` | Pass A: it defaults `physical_markers` to `[]`, a dataclass convenience for a carrier that dies with its validator. Pass B: carrier initialization, no independent value. **DELETE (dies with `EntityContext`/`validate`)** |
| `EntityContext` (dataclass) | Pass A: the per-entity context carrier (presence type, location, last action, emotional state, physical markers) for the continuity check; the scene manifest in the prompt already carries this information to the model. Pass B: a carrier for semantic validation, not transport or storage. **DELETE** |
| `ValidationResult.__post_init__` | Pass A: it defaults the sync result's lists/dicts, a carrier convenience. Pass B: carrier initialization, no independent value. **DELETE (dies with `ValidationResult`)** |
| `ValidationResult` (dataclass) | Pass A: the sync-validation result carrier (found/missing/all-present/confidence/warnings/metadata); diagnostics could live in the parser's coverage dict instead. Pass B: a carrier for a semantic verdict the server must not produce. **DELETE** |
| `NarrativeSyncValidator.__init__` | Pass A: it constructs an `EntityValidator` delegate plus an `emotional_patterns` table that `_check_continuity` never reads (dead data — the grief/anger/fear/guilt keyword lists are written but unused). Pass B: construction of a semantic validator plus a dead regex table; the repo bans keyword/substring semantic routing, and this table is exactly that pattern, unused. **DELETE (including the dead `emotional_patterns` table)** |
| `NarrativeSyncValidator._check_continuity` | Pass A: it warns when a previously noted physical marker (e.g. "bandaged ear") is absent from new narrative mentioning the entity; the model owns continuity and the prompt can require marker persistence, while substring absence proves nothing (a marker can persist off-screen or be reworded). Pass B: substring continuity judgment over prose — semantic filtering by another name (warnings here feed retry/validation pressure) — with no registered exception. **DELETE (continuity belongs in prompt + schema-tracked marker fields, not substring checks)** |
| `NarrativeSyncValidator.validate` | Pass A: it delegates entity logic to `EntityValidator.validate` (DELETE below) and appends continuity warnings; deleting it removes no player capability, since validation pressure here can only trigger retries or warnings. Pass B: delegation to a semantic validator plus warning appends, with a logging call — the logging half is §6.1-allowed but does not rescue the semantic whole. **DELETE (callers use prompt requirement + `entities_mentioned` + parser coverage diagnostic instead)** |

### 6. `mvp_site/entity_validator.py` — full module (672 lines)

Module verdict: DELETE except the two sentinel helpers (KEEP). It is
imported by `llm_service` and `narrative_sync_validator` (production
references found) and by `entity_utils` for the sentinel helpers, so
deletion needs caller go-ahead — but the verdict stands: substring scoring
cannot establish narrative presence, retry regeneration is a repair
re-prompt the repo bans without approval, and server-authored injection
templates are the server writing story.

| Unit | Justification + verdict |
|---|---|
| `filter_unknown_entities` | Pass A: it removes the literal "Unknown" placeholder from expected-entity lists; "Unknown" is a server sentinel for "location not found", never a real entity, and the model cannot be expected to mention a sentinel. Pass B: sentinel handling, not semantic filtering — it removes a non-entity, not a model fact. **KEEP** |
| `is_unknown_entity` | Pass A: the predicate for the same sentinel (case-insensitive "Unknown"). Pass B: sentinel predicate, no value judgment. **KEEP** |
| `EntityPresenceType` (enum) | Pass A: same presence vocabulary as the sync validator's duplicate; the model cannot use it to prove presence. Pass B: vocabulary for semantic prose classification. **DELETE** |
| `ValidationResult.__post_init__` | Pass A: it syncs legacy/compat fields (entities_found/missing, all_present, confidence) for a result carrier that dies with its validators. Pass B: carrier initialization only. **DELETE (dies with `ValidationResult`)** |
| `ValidationResult` (dataclass) | Pass A: the unified validation-result carrier for both validator interfaces; its fields (scores, retry flags, suggestions) exist to drive retries. Pass B: a carrier for semantic verdicts. **DELETE** |
| `EntityValidator.__init__` (incl. `min_confidence_threshold` = 0.7, `presence_patterns`, `physical_state_patterns`, `_compiled_patterns`) | Pass A: it builds regex tables for absence/location/physical-state patterns and sets the 0.7 presence threshold; no prompt or schema needs these tables, since the model authors presence directly. Pass B: the threshold and the keyword/substring tables are exactly the banned semantic-routing pattern, and 0.7 is an arbitrary server judgment about prose. **DELETE (all four attributes die with the class; the 0.7 threshold is not a transport bound)** |
| `EntityValidator._build_entity_patterns` | Pass A: it returns direct-mention, pronoun, role, and action-attribution regex templates; pronoun/role patterns in particular cannot attribute presence (a pronoun may refer to anyone). Pass B: semantic-routing tables, banned pattern, no registered exception. **DELETE** |
| `EntityValidator._compile_patterns` | Pass A: it pre-compiles the pattern tables for performance; performance does not rescue the patterns themselves. Pass B: compilation of semantic-routing tables. **DELETE** |
| `EntityValidator.analyze_entity_presence` | Pass A: it classifies an entity as mentioned-absent (via absence regexes / thought phrases), physically present (via substring containment), or missing; substring containment is not presence (a name in dialogue about someone absent is still a substring hit unless a regex happens to catch it). Pass B: regex/substring semantic classification of prose with no registered exception. **DELETE** |
| `EntityValidator.extract_physical_states` | Pass A: it associates bandaged/trembling/wounded/bloodied/exhausted matches with nearby capitalized words as entity names — a heuristic that misattributes states whenever two capitalized words are near a match. Pass B: heuristic semantic inference from prose, no registered exception. **DELETE** |
| `EntityValidator.detect_scene_transitions` | Pass A: it extracts "moved to / arrived at / now in" matches as location transitions; the model already authors `location_confirmed`, which is the authoritative location signal. Pass B: regex inference of a model-owned fact, redundant with the schema field. **DELETE** |
| `EntityValidator.create_injection_templates` | Pass A: it returns canned sentences ("{entity}, who had been present but silent, {action}.") for missing entities — literally server-authored story text. Pass B: the server writing narrative is semantic content creation, the clearest possible ZFC failure, with no registered exception. **DELETE** |
| `EntityValidator.validate_entity_presence` | Pass A: it scores each expected entity and decides retry-needed from the 0.7 threshold; the checkable contract is the `entities_mentioned` array, which needs no scoring. Pass B: threshold-scored semantic validation driving retries, no registered exception. **DELETE** |
| `EntityValidator._calculate_entity_presence_score` | Pass A: it scores presence as 0.8 for a substring hit + 0.1/mention (capped) + partial-name credit + 0.3 for action patterns + pronoun credit — an invented arithmetic of presence that no prompt or schema can reproduce or audit. Pass B: numeric semantic scoring of prose, no registered exception. **DELETE** |
| `EntityValidator._generate_retry_suggestions` | Pass A: it generates generic suggestions ("Include X in the scene...") for missing entities; the prompt can state the entity requirement once, without per-turn server suggestions. Pass B: suggestion generation for a semantic verdict. **DELETE** |
| `EntityValidator.create_retry_prompt` | Pass A: it builds a retry prompt ("MUST be included... Please revise") — a repair re-prompt, which the repo bans as a new LLM request path without approval and which hides prompt/schema failure behind regeneration. Pass B: repair-prompt construction for a semantic verdict, no registered exception. **DELETE** |
| `EntityValidator.validate` | Pass A: it combines presence analysis, physical states, transitions, confidence, and warnings into the comprehensive result; every input is a DELETE above, so the composite has no surviving leg. Pass B: composite semantic validation, no registered exception. **DELETE** |
| `EntityRetryManager.__init__` | Pass A: it constructs a validator + retry history for up to 2 retries; the retry loop is the behavior being deleted. Pass B: construction for a repair loop. **DELETE** |
| `EntityRetryManager.validate_with_retry` | Pass A: it loops validation → retry prompt → regeneration callback up to `max_retries`, spending extra model turns to fix a server-scored defect the model was never told about in the original prompt. Pass B: an extra-LLM-request loop driven by semantic scoring, with no registered exception and against the repo's repair re-prompt ban. **DELETE** |
| `EntityRetryManager.get_retry_statistics` | Pass A: it returns configured max retries + threshold — telemetry about a deleted loop, useful to no one once the loop is gone. Pass B: telemetry for a deleted mechanism; standing alone it would be §6.1 logging, but it has no independent subject. **DELETE (dies with the retry manager)** |
| `entity_validator` (global instance) | Pass A: a module-level validator instance for callers; with the class deleted it has no use. Pass B: dies with its class. **DELETE** |
| `entity_retry_manager` (global instance) | Pass A: a module-level retry-manager instance; with the manager deleted it has no use. Pass B: dies with its class. **DELETE** |

### 7. `mvp_site/schemas/validation.py` — functions/methods (1,229 lines)

| Unit | Justification + verdict |
|---|---|
| `check_datetime` | Pass A: an RFC 3339 format checker for the jsonschema format checker; stored-state datetimes need a format gate the model cannot self-enforce after persistence. Pass B: a format gate for durable writes (transport/storage integrity), not a campaign-fact judgment. **KEEP** |
| `_enrich_validation_message` | Pass A: it adds actionable hints for common schema failures (e.g. god-mode PCD null-or-full guidance), which helps the model/user fix a payload. Pass B: message enrichment for diagnostics, changing no value. **KEEP** |
| `load_schema` | Pass A: it loads a JSON schema from the schemas directory with caching; every validator and schema assembler depends on this single loader. Pass B: schema loading for transport contracts, with a cache for capacity. **KEEP** |
| `load_world_sim_setup_schema` | Pass A: it derives both world-sim setup variants (fresh vs preserve-existing roster) from the canonical schema; the model cannot select its own setup contract. Pass B: schema-variant selection (toggling `additionalProperties` for the roster), a contract choice, not a value change. **KEEP** |
| `get_spell_definition` | Pass A: it returns the canonical stored Spell definition (name-only required, for legacy sheets) so stored-state validation does not warn on legacy entries. Pass B: schema derivation preserving backward compatibility. **KEEP** |
| `get_spell_authoring_schema` | Pass A: it returns the model-facing authoring Spell (name, level 0–9, description required, plus provider length caps unless `bounds=False` for the creation modal). Pass B: response-schema construction with provider capacity bounds. **KEEP** |
| `get_spell_authoring_list_schema` | Pass A: the array form of the authoring Spell schema. Pass B: schema assembly. **KEEP** |
| `inline_canonical_defs` | Pass A: it inlines `#/$defs/` references because structured-output providers reject or ignore unresolvable `$ref`s; without it, wire schemas carrying refs fail at the provider. Pass B: provider-transport adaptation of a schema, changing no model value. **KEEP** |
| `get_validator` | Pass A: it returns a cached Draft202012Validator with the format checker for a named schema; validation is the diagnostic mechanism for stored state. Pass B: validator construction for storage integrity, cached for capacity. **KEEP** |
| `validate_game_state` | Pass A: it validates a full game state against the canonical schema and returns error messages; the model cannot self-validate stored state after the fact. Pass B: it returns errors only — it does not rewrite state — so it is diagnostics; the standing caveat is that any caller turning these errors into a turn rejection must instead warn, except where committing would corrupt server-owned storage (the repo's UX-first rule). **KEEP (errors are diagnostics; callers must not convert them into turn rejections except for storage corruption)** |
| `get_story_entry_validator` | Pass A: it builds the StoryEntry validator from the canonical schema's `$defs` for Firestore story entries. Pass B: validator construction for storage integrity. **KEEP** |
| `validate_story_entry` | Pass A: it validates a Firestore story entry and returns error paths/messages. Pass B: diagnostics only, no mutation. **KEEP** |
| `get_canonical_equipment_slots` | Pass A: it derives canonical slot names from the game-state schema (resolving refs/allOf), giving every consumer one slot vocabulary. Pass B: schema-derived vocabulary, no value touched. **KEEP** |
| `_merge_schema_properties` | Pass A: it merges schema-fragment properties resolving refs/allOf inheritance, the helper every schema-derived vocabulary above needs. Pass B: schema introspection, no value touched. **KEEP** |
| `get_player_character_schema_keys` | Pass A: it derives allowed PCD keys from the canonical schema for the overlay and validators. Pass B: schema-derived vocabulary. **KEEP** |
| `get_legacy_equipment_slot_aliases` | Pass A: it returns the legacy→canonical slot alias map for reads and warnings. Pass B: alias vocabulary, no value rewritten by this function itself. **KEEP** |
| `get_known_equipment_slots` | Pass A: it returns canonical + (optionally) legacy slots for runtime reads, without widening the model's write contract. Pass B: read-side vocabulary. **KEEP** |
| `get_spell_slot_read_aliases` | Pass A: it reads legacy display aliases from `spell_slots_schema.json` without widening the write contract. Pass B: read-side vocabulary. **KEEP** |
| `get_valid_spell_slot_levels` | Pass A: it returns canonical valid spell-slot levels from the external contract file. Pass B: schema-derived vocabulary. **KEEP** |
| `get_game_state_top_level_properties` | Pass A: it returns canonical top-level game-state keys from the schema for overlay/validation use. Pass B: schema-derived vocabulary. **KEEP** |
| `get_strict_overlay_nested_allowed_keys` | Pass A: it returns strict nested allowlists for high-risk overlay regions from the schema. Pass B: schema-derived vocabulary for the overlay gate; the gate itself only warns/errors as lists (see `validate_state_updates_overlay`). **KEEP** |
| `get_social_hp_challenge_properties` | Pass A: it resolves SocialHPChallenge properties from the canonical schema for validators. Pass B: schema-derived vocabulary. **KEEP** |
| `_get_social_hp_enum_values` | Pass A: it extracts enum values for one SocialHPChallenge property from the schema. Pass B: schema-derived vocabulary. **KEEP** |
| `get_social_hp_request_severity_values` / `get_social_hp_skill_values` / `get_social_hp_status_values` / `get_social_hp_npc_tier_values` | Pass A: cached enum-value getters for the four SocialHPChallenge enums, used by the social-HP validator and its tests. Pass B: schema-derived vocabularies. **KEEP** |
| `get_social_hp_continuity_properties` | Pass A: it returns the model-owned SocialHPContinuity property definitions from the schema. Pass B: schema-derived vocabulary. **KEEP** |
| `_get_time_of_day_values` / `get_time_of_day_values` | Pass A: lowercase time-of-day enum values from the WorldTime definition, the canonical form for comparisons. Pass B: schema-derived vocabulary (lowercasing here is vocabulary normalization, not a value rewrite). **KEEP** |
| `get_common_field_paths` | Pass A: it returns schema-derived semantic field paths (e.g. pc.resources) so `game_state.py` avoids hardcoded string literals. Pass B: schema-derived path table, no value touched. **KEEP** |
| `validate_state_updates_overlay` | Pass A: it validates the strict overlay policy for high-risk regions and returns (warnings, errors) — stricter than canonical `additionalProperties` behavior, protecting write paths from field drift. Pass B: it returns lists only and mutates nothing, so it is a gate/diagnostic; the same caller caveat as `validate_game_state` applies (errors must warn, not reject turns, except for storage corruption). **KEEP (with the warn-not-reject caller caveat)** |
| `sanitize_state_updates_overlay` | Pass A: it canonicalizes overlays (dotted-key expansion, frozen-plan placement, nested game_state unwrap, typo handling) and reports corrections; the dotted/unwrap/placement steps preserve values and save turns the model shaped slightly wrong. Pass B: the value-preserving steps are structural parsing (KEEP-worthy), but the near-match step RENAMES unknown keys to canonical keys on a difflib 0.72 similarity score — a semantic guess that a model-invented key means a canonical key — with no registered exception. **ADAPT (remove near-match remapping; keep dotted expansion, frozen-plan placement, and game_state unwrap, and keep unknown keys verbatim + warned)** |
| `_canonicalize_frozen_plans_placement` | Pass A: it moves `custom_campaign_state.frozen_plans` to top-level `frozen_plans`, where overlay policy expects it, so historical prompt placements do not generate warning noise. Pass B: a structural move preserving payload content exactly. **KEEP** |
| `_normalize_dotted_state_update_keys` | Pass A: it expands dotted top-level keys (`player_character_data.experience.current`) into nested dicts, accepting a model shaping variant without losing any value. Pass B: structural normalization preserving every value. **KEEP** |
| `_normalize_nested_game_state_keys` | Pass A: it unwraps updates nested under `state_updates.game_state` to top level (deep-merging), accepting another model shaping variant losslessly. Pass B: structural unwrap preserving values. **KEEP** |
| `is_valid_game_state` | Pass A: a boolean shortcut for full-state schema validity, used where a pass/fail answer suffices. Pass B: a read-only predicate over stored state. **KEEP** |
| `_normalize_for_similarity` | Pass A: it lowercases and normalizes key spellings (hyphens/spaces to underscores) for near-match comparison — needed only by the remapping path. Pass B: as a warn-hint helper it is harmless text normalization; as a rename engine it is the defect in `sanitize_state_updates_overlay`. **ADAPT (warn-hint use only; never feed a rename)** |
| `_get_near_match_suggestions` | Pass A: difflib suggestions for unknown keys are genuinely useful as warning hints ("did you mean X?"), which help prompt/schema authors fix drift. Pass B: suggestions as diagnostics are allowed; suggestions as renames are not. **ADAPT (return suggestions for warnings only; never apply them as key renames)** |

`schemas/validation.py` symbols: `_FORMAT_CHECKER` / `_RFC3339_PATTERN` (format-checking machinery, **KEEP**); `_SCHEMA_CACHE` / `_VALIDATOR_CACHE` and the per-vocabulary caches (`_CANONICAL_EQUIPMENT_SLOTS_CACHE`, `_GAME_STATE_TOP_LEVEL_PROPERTIES_CACHE`, `_SOCIAL_HP_REQUEST_SEVERITY_CACHE`, `_SOCIAL_HP_SKILLS_CACHE`, `_SOCIAL_HP_STATUS_CACHE`, `_SOCIAL_HP_NPC_TIER_CACHE`, `_TIME_OF_DAY_VALUES_CACHE`, `_STRICT_OVERLAY_NESTED_KEYS_CACHE`, `_STORY_ENTRY_VALIDATOR_CACHE`, `_PLAYER_CHARACTER_SCHEMA_KEYS_CACHE`, `_SPELL_SLOTS_SCHEMA_CACHE`, `_SPELL_SLOTS_READ_ALIASES_CACHE`, `_COMMON_FIELD_PATHS_CACHE`) (in-process caches for schema-derived data, capacity optimization, **KEEP** — with the repo's standing note that per-instance caches are acceptable here because the data is static schema material, not per-user state); `_SCHEMA_WARN_THRESHOLD_MS` (50ms slow-validation warning threshold, logging, **KEEP**); `CORRECTION_KIND_BENIGN_NORMALIZE` / `CORRECTION_KIND_SCHEMA_WARNING` (correction classification labels for telemetry, **KEEP**).

### 8. `mvp_site/schemas/__init__.py`

No functions. The module re-exports `GameStateModel`, schema-validation
helpers, and TypedDict types with an explicit `__all__`. Pass A: a package
surface is needed for importers to find one schema API. Pass B: re-exports
change no value. **KEEP (module verdict; the re-exported units carry their own rows)**.

### 9. `mvp_site/schemas/character_creation_wire.py`

| Unit | Justification + verdict |
|---|---|
| `_load_character_creation_wire_schema` | Pass A: it loads the externalized creation wire-schema JSON asset, keeping the contract as data. Pass B: schema loading. **KEEP** |
| `_character_creation_conclude_pcd_schema` | Pass A: it builds the minimal required shape for the creation conclude commit from the active-phase declarations verbatim (one source of truth). Pass B: schema assembly. **KEEP** |
| `get_character_creation_conclude_json_schema` | Pass A: it returns the dedicated PCD-only conclude envelope (with the 120,000-char narrative bound). Pass B: response-schema assembly for the conclude turn. **KEEP** |
| `is_complete_character_creation_clock` | Pass A: it validates a clock against the conclude envelope's world-time contract — a commit-time shape check for the conclude turn. Pass B: a schema-validity predicate over a commit candidate, changing no value. **KEEP** |
| `is_complete_character_creation_sheet` | Pass A: it checks a conclude candidate contains every canonical PCD field (a completeness predicate, not a value rewrite). Pass B: read-only completeness check for the commit path. **KEEP** |
| `_character_creation_equipment_schema` | Pass A: it builds the bounded slot-object equipment contract from canonical slots (arrays for backpack/weapons, single items elsewhere). Pass B: schema assembly. **KEEP** |
| `_character_creation_pcd_schema` | Pass A: it builds the typed full-review + nonempty-partial PCD branches for active phases. Pass B: schema assembly. **KEEP** |
| `_character_creation_review_pcd_schema` / `_character_creation_partial_pcd_schema` | Pass A: they project the review branch and the partial branch from the combined PCD schema for their respective stages. Pass B: schema projection. **KEEP** |
| `_build_character_creation_active_schema` | Pass A: it assembles the isolated structured-output schema for active creation turns (planning-block bounds, stage enums, state-update branches, top-level required) from the gameplay base schema + wire asset. Pass B: response-schema assembly, the Pass A mechanism for creation turns. **KEEP** |
| `__getattr__` | Pass A: lazy construction of `NARRATIVE_RESPONSE_JSON_SCHEMA_CHARACTER_CREATION` on first access, avoiding import-time schema cost. Pass B: lazy capacity optimization for schema delivery. **KEEP** |
| Symbols: `_LONG_TEXT` (20000) / `_NARRATIVE_TEXT` (120000) / `_CHARACTER_CREATION_WIRE_SCHEMA_PATH` / `_CHARACTER_CREATION_WIRE_SCHEMA` / `CHARACTER_CREATION_CONCLUDE_PCD_FIELDS` / `_CHARACTER_CREATION_REVIEW_PCD_FIELDS` / `_CHARACTER_CREATION_REVIEW_STAGES` / `_CHARACTER_CREATION_PARTIAL_STAGES` | Pass A: bounds, asset path, loaded asset, and derived field/stage tuples for the creation wire contract. Pass B: schema data and capacity bounds, no value touched. **KEEP** |

### 10. `mvp_site/schemas/character_death_wire.py`

| Unit | Justification + verdict |
|---|---|
| `_load_bounded_schema` | Pass A: it loads a deaths/revivals JSON asset, strips `_comment`, and applies the caller's string bound — the bound is provider capacity, and the string-array item shape is what keeps the gameplay schema under Gemini's 3-array-of-typed-object complexity ceiling (per the module docstring). Pass B: schema loading + provider-capacity bounding. **KEEP** |
| `get_character_deaths_schema` / `get_character_revivals_schema` | Pass A: they return the bounded wire schemas for deaths (JSON-encoded-string items, parsed back server-side by `graveyard_service`) and revivals (entity-id strings). Pass B: schema assembly for transport; the deaths parsing back into dicts is transport decoding of a wire format, not a domain decision. **KEEP** |
| Symbols: `_CHARACTER_DEATHS_SCHEMA_PATH` / `_CHARACTER_REVIVALS_SCHEMA_PATH` | Pass A: asset paths for the two wire schemas. Pass B: schema location data. **KEEP** |

### 11. `mvp_site/schemas/conclude_snapshot.py`

| Unit | Justification + verdict |
|---|---|
| `ConcludeSnapshot._coerce_level` | Pass A: it coerces stringy ints WITHOUT clamping, so the Field (1–20) rejects out-of-range levels (e.g. narrative-milestone numbers) instead of silently rewriting them — the fail-closed shape a commit turn needs. Pass B: coercion preserving value + a schema range gate on a canonical commit field (SRD levels 1–20), which rejects rather than invents. **KEEP** |
| `ConcludeSnapshot._coerce_numeric` | Pass A: it defensively coerces stringy ints for proficiency_bonus/max_hp via `DefensiveNumericConverter.convert_value`; the model can emit ints under the conclude schema, so default substitution is unnecessary. Pass B: it inherits the converter's defect — invalid `max_hp` becomes 1 (an invented fact on a commit turn) — with no registered exception. **ADAPT (use strict int coercion with validation error on invalid input; never substitute a default)** |
| `ConcludeSnapshot._normalize_class` | Pass A: it strips/lowercases the class identifier and rejects missing/blank values, because the reconcile reducer cannot recompute derived stats without a class. Pass B: identifier normalization (case/whitespace) preserving identity + fail-closed on blank, which is storage-integrity behavior for a commit, not a domain invention. **KEEP** |
| `ConcludeSnapshot._coerce_slots` | Pass A: it converts list/tuple spell slots to a tuple, a structural form change for the snapshot model. Pass B: structural coercion preserving every slot value. **KEEP** |
| Symbols: `MIN_LEVEL` (1) / `MAX_LEVEL` (20) / `ConcludeSnapshot` (class) | Pass A: SRD level bounds + the conclude-turn snapshot model shared by level-up and character-creation conclude domains. Pass B: schema bounds + a carrier model; the model's `extra="ignore"` keeps unknown fields from breaking the snapshot. **KEEP** |

### 12. `mvp_site/schemas/defensive_numeric_converter.py`

Module verdict: DELETE. Every row below is the same defect from a different
angle, stated per unit as required: the converter substitutes server-chosen
defaults for model values and clamps ranges, with no registered exception
and no necessity proof, on fields (HP, XP, gold, ability scores) that are
core campaign facts.

| Unit | Justification + verdict |
|---|---|
| `DefensiveNumericConverter.convert_value` | Pass A: the model can emit integers under the response schema, and "unknown"/malformed numbers can be warned + omitted; nothing requires the server to answer "unknown HP" with 1, "unknown ability" with 10, or "unknown xp_to_next_level" with 300. Pass B: it substitutes defaults, extracts the first number from strings like "500 XP" or "10/20" (picking 10 from a fraction), and clamps HP to ≥1, non-negatives to ≥0, abilities to 1–30 — three kinds of semantic invention in one function, with no registered exception. **DELETE (warn + omit on invalid numerics; put integer requirements in prompt/schema)** |
| `DefensiveNumericConverter.convert_dict` | Pass A: recursive application of `convert_value` over dicts/lists; deleting it removes no capability the prompt/schema cannot supply. Pass B: it propagates the same default/clamp inventions through every nested numeric field. **DELETE (with `convert_value`)** |
| Symbols: `HP_FIELDS` / `NON_NEGATIVE_FIELDS` / `ABILITY_SCORE_FIELDS` / `FIELD_DEFAULTS` | Pass A: the field-category sets and default table exist only to serve the converter; with it deleted they have no reader or purpose. Pass B: they are the invention tables themselves (hp→1, ability→10, AC→10, xp_to_next→300). **DELETE (with the class)** |

### 13. `mvp_site/schemas/entities_pydantic.py`

| Unit | Justification + verdict |
|---|---|
| `sanitize_entity_name_for_id` | Pass A: it lowercases and slugifies a name into an entity-ID component (e.g. "Cazador's Spawn" → "cazadors_spawn") for storage keys; the model cannot mint server ID slugs. Pass B: identifier hygiene for durable-write keys, not a campaign fact — the display name is preserved separately. **KEEP** |
| `CombatDisposition.from_type_string` | Pass A: it maps legacy type strings (pc/enemy/companion) to dispositions, but its default for unknown types is HOSTILE — the model never said hostile, the server did. Pass B: inventing a hostile disposition for an unknown type is a semantic fact creation with no registered exception; unknown must stay unknown. **DELETE the hostile default (return None / preserve unknown; keep the friendly/neutral mappings, which are alias translations)** |
| `Stats.convert_strength` / `convert_dexterity` / `convert_constitution` / `convert_intelligence` / `convert_wisdom` / `convert_charisma` | Pass A: each routes one ability score through `DefensiveNumericConverter.convert_value` (DELETE above); the model can emit ability ints under the schema. Pass B: same default/clamp invention (unknown ability → 10, out-of-range → clamped) with no registered exception. **DELETE (all six; use strict int validation + warn)** |
| `Stats.get_modifier` | Pass A: it computes the SRD modifier `(ability - 10) // 2` on read for display/mechanics consumers; the formula is deterministic from an already-stored value. Pass B: a read-only derivation that changes no stored field — it must never write back, and this row's KEEP is conditioned on that boundary. **KEEP (read-only derivation only; any write-back use inherits DELETE)** |
| `HealthStatus.convert_hp` / `convert_hp_max` / `convert_temp_hp` | Pass A: each routes HP fields through the deleted converter; the model can emit HP ints under the schema. Pass B: same default/clamp invention (unknown HP → 1) with no registered exception. **DELETE (all three)** |
| `HealthStatus.validate_hp_not_exceed_max` | Pass A: it clamps HP to hp_max when HP exceeds it after conversion — including when conversion itself shrank hp_max to 1, so a healthy character can be rewritten to 1 HP by two stacked server inventions. Pass B: a clamp changing a campaign fact (HP) with no registered exception, and the repo's UX-first rule treats clamping as rejection-like when it destroys value. **DELETE (surface HP>max as a warning; never rewrite HP)** |
| `Character.convert_level` | Pass A: it routes level through the deleted converter (unknown level → 1). Pass B: same default invention with no registered exception. **DELETE** |
| `Character._lineage_is_empty` | Pass A: a predicate (None / "" / {} = empty) for lineage-alias handling. Pass B: a read-only predicate. **KEEP** |
| `Character.synchronize_lineage_aliases` | Pass A: it keeps parentage/parents aliases authoritative together — populated wins over empty placeholders, and two populated but differing values raise instead of silently picking one. Pass B: alias coherence preserving values (empty never overwrites populated; conflict raises rather than invents a winner), which is storage-integrity behavior. **KEEP** |
| `Character.__setattr__` | Pass A: it mirrors direct writes to either lineage alias with the same empty-never-wins rule. Pass B: alias mirroring preserving values, same rationale as above. **KEEP** |
| `Character.validate_gender` | Pass A: it validates gender for narrative consistency (permissive for creativity per its docstring); the full body was not re-read line by line in this audit, so this row judges its documented intent (permissive check, NPC-mandatory requirement) rather than every branch. Pass B: to the extent it raises or defaults gender for NPCs, it invents or gates a model-owned identity fact with no registered exception; the permissive string check itself is harmless. **ADAPT (keep the permissive string check; never raise or default gender — warn and leave None, with the requirement stated in prompt)** |
| `Character.validate_age` | Pass A: it raises for non-integer, negative, or >50000 ages; the model can emit a valid age, but a fantasy being's age is a model-owned fact and 50000 is an arbitrary server ceiling. Pass B: a hard range raise on a model fact with no registered exception; a warning would suffice. **DELETE the raise (warn on implausible ages; never reject the entity for age)** |
| `Character.validate_mbti` | Pass A: it accepts any string personality description (MBTI or creative) and strips whitespace; nothing is rejected except non-strings. Pass B: permissive strip-only validation preserving the model's description. **KEEP** |
| `Character.validate_alignment` | Pass A: it accepts any string alignment (D&D or creative) and strips whitespace. Pass B: permissive strip-only validation preserving the model's description. **KEEP** |
| `Character.validate_entity_type` | Pass A: it derives entity_type from the entity_id prefix (pc_ → player character, npc_ → NPC) when an id is present. Pass B: derivation from the server-minted identifier itself, not from prose — the id prefix is server-owned metadata, so this is structural, not semantic. **KEEP** |
| `Character.validate_npc_gender_required` | Pass A: it raises when an NPC lacks gender, for "narrative consistency"; the prompt can require NPC gender without the server rejecting an otherwise valid entity. Pass B: a hard raise gating entity construction on a model-owned identity field, with no registered exception. **DELETE the raise (same prompt-owns-requirement fix as `validate_gender`)** |
| `CombatState.validate_participants` | Pass A: it raises when a turn-order entity is missing from participants — an internal-consistency gate on a server-constructed combat manifest, not on raw model output. Pass B: a storage-integrity check on derived data (both lists come from the same manifest), which raises on contradiction rather than inventing a participant. **KEEP** |
| `SceneManifest.validate_present_entities` | Pass A: it raises when a present-entity id is not among the manifest's characters — again an internal-consistency gate on server-constructed data. Pass B: same storage-integrity rationale; it rejects a contradictory manifest, it does not rewrite presence. **KEEP** |
| `SceneManifest.get_expected_entities` | Pass A: it derives the expected-entity list (visible + conscious + present) that the prompt needs to require in narrative — prompt input, not an output verdict. Pass B: prompt-side derivation from stored state; it judges nothing the model wrote. **KEEP** |
| `SceneManifest.to_prompt_format` | Pass A: it renders the manifest (location, present characters with HP/status/visibility, combat, conditions) as prompt text for the model. Pass B: prompt rendering, the Pass A mechanism. **KEEP** |
| `create_from_game_state` | Pass A: it builds a SceneManifest from legacy game-state dicts, handling string/dict/malformed location forms; the manifest is prompt input the model needs. Pass B: its defensive extractions are mostly value-preserving, but it INVENTS defaults where state is missing — HP 10 for missing HP, gender "other" for missing NPC gender, "Unknown Location" for missing location, and `present=True` / `conscious=True` / `visible` defaults for NPC flags — asserting facts the state never contained, with no registered exception. **ADAPT (propagate None/unknown explicitly into the prompt instead of inventing 10 / "other" / "Unknown Location" / present-conscious-visible; keep the defensive type handling)** |
| Classes/enums: `EntityType` / `CombatDisposition` / `EntityStatus` / `Visibility` / `Stats` / `HealthStatus` / `Location` / `Character` / `PlayerCharacter` / `NPC` / `CombatState` / `SceneManifest` | Pass A: the typed entity carriers used by entity tracking, preloading, instructions, and game-state serialization (production readers found in `entity_tracking.py`, `entity_preloader.py`, `entity_instructions.py`, `game_state.py`, `serialization.py`, `llm_service.py`). Pass B: type definitions change no value; their verdicts follow their validator rows (converters DELETE, carriers KEEP). **KEEP (as carriers; the ADAPT/DELETE rows above govern their validators and `create_from_game_state`)** |

### 14. `mvp_site/schemas/field_constants.py` (auto-generated from `game_state.schema.json`)

Shared rationale (applies to every row, with per-dict coverage noted):
Pass A: each dict is a generated mirror of one canonical-schema definition's
field names, giving code a single spelling source instead of string literals;
the model is bound by the schema, not by these mirrors. Pass B: a name table
changes no value, and per the audit spec registry membership alone proves
nothing — these rows claim nothing beyond "name table, no runtime filtering."
All rows: **KEEP**.

| Dict | Coverage |
|---|---|
| `TOP_LEVEL_FIELDS` | Top-level game-state keys (action_resolution through world_resources). **KEEP** |
| `ACTIONRESOLUTION_FIELDS` | Action-resolution object keys (interpreted_as, mechanics, audit_flags, narrative_outcome). **KEEP** |
| `ACTIONRESOLUTIONROLL_FIELDS` | Action-resolution roll keys. **KEEP** |
| `ARCMILESTONE_FIELDS` | Arc-milestone keys. **KEEP** |
| `CAMPAIGNTIER_FIELDS` | Campaign-tier keys. **KEEP** |
| `CHAPTERDATA_FIELDS` | Chapter-data keys. **KEEP** |
| `CHARACTER_FIELDS` | Character keys. **KEEP** |
| `COMBATSTATE_FIELDS` | Combat-state keys. **KEEP** |
| `COMBATANTSTATE_FIELDS` | Combatant-state keys. **KEEP** |
| `COMPANIONARC_FIELDS` | Companion-arc keys. **KEEP** |
| `CUSTOMCAMPAIGNSTATE_FIELDS` | Custom-campaign-state keys. **KEEP** |
| `ENCOUNTERSTATE_FIELDS` | Encounter-state keys. **KEEP** |
| `ENTITYSTATUS_FIELDS` | Entity-status keys. **KEEP** |
| `ENTITYTYPE_FIELDS` | Entity-type keys. **KEEP** |
| `FACTIONMINIGAME_FIELDS` | Faction-minigame keys (faction data is model-owned content; this table only names it). **KEEP** |
| `FACTIONRESOURCES_FIELDS` | Faction-resource keys. **KEEP** |
| `FACTIONUNITS_FIELDS` | Faction-unit keys. **KEEP** |
| `GODMODEDIRECTIVE_FIELDS` | God-mode directive keys (admin path). **KEEP** |
| `GRAVEYARDENTRY_FIELDS` | Graveyard-entry keys. **KEEP** |
| `HEALTHSTATUS_FIELDS` | Health-status keys. **KEEP** |
| `INJURY_FIELDS` | Injury keys. **KEEP** |
| `LEGACYINITIATIVEENTRY_FIELDS` | Legacy initiative-entry keys. **KEEP** |
| `LEVELUPSESSION_FIELDS` | Level-up-session keys. **KEEP** |
| `LOCATION_FIELDS` | Location keys. **KEEP** |
| `NPC_FIELDS` | NPC keys. **KEEP** |
| `PLANNINGBLOCK_FIELDS` | Planning-block keys. **KEEP** |
| `PLANNINGCHOICE_FIELDS` | Planning-choice keys. **KEEP** |
| `PLANNINGCHOICELEGACY_FIELDS` | Legacy planning-choice keys. **KEEP** |
| `PLAYERCHARACTER_FIELDS` | Player-character keys. **KEEP** |
| `RESOURCEENTRY_FIELDS` | Resource-entry keys. **KEEP** |
| `RESOURCEREGISTRY_FIELDS` | Resource-registry keys. **KEEP** |
| `REWARDSPENDING_FIELDS` | Rewards-pending keys. **KEEP** |
| `SANCTUARYMODE_FIELDS` | Sanctuary-mode keys. **KEEP** |
| `SOCIALHPCHALLENGE_FIELDS` | Social-HP-challenge keys. **KEEP** |
| `STATS_FIELDS` | Stats keys. **KEEP** |
| `STORYENTRY_FIELDS` | Story-entry keys. **KEEP** |
| `VISIBILITY_FIELDS` | Visibility keys. **KEEP** |
| `WORLDDATA_FIELDS` | World-data keys. **KEEP** |
| `WORLDEVENT_FIELDS` | World-event keys (living-world content named, not decided, here). **KEEP** |
| `WORLDTIME_FIELDS` | World-time keys. **KEEP** |

### 15. `mvp_site/schemas/game_state_models.py`

| Unit | Justification + verdict |
|---|---|
| `_load_schema` | Pass A: it loads the canonical JSON schema at import time (and fails fast if the file is missing/invalid JSON). Pass B: schema loading for the runtime model. **KEEP** |
| `GameState` (class) | Pass A: the dynamic Pydantic model generated from the canonical schema, existing solely for `to_model()`/`from_model()` round-trip serialization with `extra="allow"`. Pass B: it explicitly performs NO validation (its docstring says real validation is `validate_game_state`), so it passes values through untouched — the opposite of filtering. **KEEP** |
| Symbols: `_SCHEMA_PATH` / `_schema` | Pass A: the canonical schema path and the import-time loaded schema (validating the file exists and parses). Pass B: schema location/data. **KEEP** |

### 16. `mvp_site/schemas/gemini_schema_acceptance.py`

| Unit | Justification + verdict |
|---|---|
| `schema_fingerprints` | Pass A: it maps each bound schema name to the sha256 of its canonical JSON, pinning exactly which schemas passed real-API acceptance. Pass B: acceptance bookkeeping for provider transport. **KEEP** |
| `gemini_schema_acceptance_requests` | Pass A: it describes every acceptance request (schema + model + code-execution flag, disabled for WORLD_SIM lanes) that the acceptance manifest sends to Gemini. Pass B: provider-transport contract description. **KEEP** |
| Symbols: `ACCEPTANCE_MODEL` (`gemini-3.8-flash`) / `MANIFEST_PATH` | Pass A: the acceptance model floor and the manifest path (the 1.26 MB `gemini_schema_acceptance.json` beside it). Pass B: transport/acceptance configuration. **KEEP** |

### 17. `mvp_site/schemas/narrative_wire_fields.py`

| Unit | Justification + verdict |
|---|---|
| `validate_conflict_signal` | Pass A: it preserves a model-owned conflict signal when its wire type is a string, returning None otherwise; the signal's meaning is the model's, the type gate is the wire's. Pass B: a wire-type gate that drops only unparseable (non-string) values, which carry no signal to preserve. **KEEP** |
| `validate_episode_transition` | Pass A: same shape as above for episode transitions — preserve valid strings, drop non-strings. Pass B: wire-type gate, no semantic choice. **KEEP** |
| `validate_canonical_action_basis` | Pass A: it enforces the wire shape of the typed citation (tool_call_id, tool_name, optional target_entity_id) that must ground a lethal-conflict claim, so a malformed citation never reaches the backend lethal guard as truthy-but-broken. Pass B: a shape gate protecting an authorization-adjacent guard (the allowlist/invocation check itself lives in `world_sim.timeline.lethal_policy`, out of scope); it judges shape, not whether the claim is true. **KEEP** |
| `coerce_bool_optional` | Pass A: best-effort bool conversion that returns None when unclear — the strict-compliant behavior the two in-module bool coercers (ADAPT above) should match. Pass B: it preserves-or-omits (never guesses False), so it passes Pass B outright. **KEEP** |

### 18. `mvp_site/schemas/prompt_generator.py`

All seven functions generate prompt documentation from schemas; none filters
a turn. Production readers found: `agent_prompts.py` (schema instructions
and field instructions for prompt assembly). Each row is judged individually.

| Unit | Justification + verdict |
|---|---|
| `_gather_properties` | Pass A: it recursively gathers properties from a schema fragment resolving allOf/refs (cycle-safe via visited ids) for documentation generation. Pass B: schema introspection for prompt text. **KEEP** |
| `resolve_refs` | Pass A: it follows `$ref` pointers to their definitions for documentation. Pass B: schema introspection. **KEEP** |
| `_infer_property_type` | Pass A: it infers a user-facing type label (array/object/ref/any) when `type` is omitted, for readable docs. Pass B: documentation labeling, no runtime effect on turns. **KEEP** |
| `generate_type_markdown` | Pass A: it renders one schema type as markdown documentation for prompts. Pass B: prompt documentation generation. **KEEP** |
| `generate_schema_documentation` | Pass A: it renders a full markdown document from a JSON schema file for prompt inclusion. Pass B: prompt documentation generation. **KEEP** |
| `get_schema_instructions` | Pass A: it retrieves documentation for one schema type (or Root) — the function `agent_prompts` calls to build prompts. Pass B: prompt assembly input. **KEEP** |
| `get_schema_fields_instructions` | Pass A: it renders documentation for selected fields of a schema type, letting prompts include only relevant fields. Pass B: prompt assembly input (field selection for docs is not filtering of model output). **KEEP** |

### 19. `mvp_site/schemas/reward_event_schema.py`

| Unit | Justification + verdict |
|---|---|
| `REWARD_EVENT_XP_SCHEMA` | Pass A: the state-owned XP receipt sub-schema (gained ≥ 0, tier enum from constants) — the model emits gained/tier, the server derives the rest, per the state-owned reward design. Pass B: response-schema contract; the enum constraint prevents the model inventing tiers the validator has no rule for. **KEEP** |
| `STATE_UPDATES_DESCRIPTION` | Pass A: the single shared `state_updates` description across providers (partial patch; omitted preserved; cumulative XP server-materialized from the receipt; god-mode absolute corrections keep their admin contract), preventing provider wording drift. Pass B: prompt/schema wording, no value touched. **KEEP** |
| `REWARD_EVENT_SCHEMA` | Pass A: the full state-owned reward receipt schema (source/source_id/label/justification/xp, all required, no extra properties; zero-reward turns emitted explicitly, never omitted). Pass B: response-schema contract for the receipt. **KEEP** |
| Symbols: `SHORT_TEXT` (500) / `LONG_TEXT` (20000) / `MAX_SAFE_XP` (2^53 − 1) | Pass A: provider length bounds and the safe-integer XP ceiling for the receipt schema. Pass B: bounded capacity for transport. **KEEP** |

### 20. `mvp_site/schemas/social_hp_challenge.py`

| Unit | Justification + verdict |
|---|---|
| `canonical_enum_spelling` | Pass A: it returns the schema enum spelling of a case/whitespace variant (else the raw value), so "persuasion" matches "Persuasion" without changing which enum member the model chose. Pass B: spelling canonicalization preserving the chosen member is not a semantic change; if it ever mapped to a different member it would fail, but it only matches case-insensitively. **KEEP** |
| `_validate_social_hp_challenge` | Pass A: it validates supplied social-HP fields and returns only keys present in the input (no invented keys), with warn-only range/enum checks — but its integer coercions default present-but-null/invalid values to 0 (and successes_needed to 5), inventing numbers for a challenge whose HP/damage/roll values are campaign facts. Pass B: the warn-only checks and spelling canonicalization are KEEP-worthy, but the 0/5 defaults are semantic invention with no registered exception (the PROVEN roll-attribution spec covers executed rolls from `dice_integrity`, not these defaults). **ADAPT (preserve-or-omit + warn on null/invalid numbers; keep spelling canonicalization and warn-only range/enum checks; the successes_needed=5 default moves to the prompt contract)** |
| Symbols: `VALID_SOCIAL_HP_STATUS` / `VALID_SOCIAL_HP_REQUEST_SEVERITY` / `VALID_SOCIAL_SKILLS` / `VALID_NPC_TIERS` (schema-derived, with documented fallbacks) / `SOCIAL_HP_MAX_RANGES` (tier ranges from constants) | Pass A: enum vocabularies and tier ranges the validator needs for its warn-only checks. Pass B: schema/constant-derived reference data; the ranges here only warn (the enforced clamp in `preventive_guards` is out of scope and is NOT rescued by this row). **KEEP (warn-reference only)** |

### 21. `mvp_site/schemas/typed_dicts.py` (auto-generated from `game_state.schema.json`)

Shared rationale: every class below is a `TypedDict` with `total=False` —
static typing only, zero runtime behavior, generated from the canonical
schema so types cannot drift from it. Pass A: types help readers and
checkers but the model, log, prompt, and schema do not need them at runtime
— which is precisely why they cost nothing under Pass B: they filter
nothing. All rows: **KEEP**.

| Class | Coverage |
|---|---|
| `StatsDict` | Ability-score fields. **KEEP** |
| `HealthStatusDict` | HP / temp-HP fields. **KEEP** |
| `InjuryDict` | Injury fields. **KEEP** |
| `LocationDict` | Location fields. **KEEP** |
| `FactionUnitsDict` | Faction-unit fields. **KEEP** |
| `ResourceEntryDict` | Resource-entry fields. **KEEP** |
| `FactionResourcesDict` | Faction-resource fields. **KEEP** |
| `CompanionArcDict` | Companion-arc fields. **KEEP** |
| `GodModeDirectiveDict` | God-mode directive fields. **KEEP** |
| `ArcMilestoneDict` | Arc-milestone fields. **KEEP** |
| `ChapterDataDict` | Chapter-data fields. **KEEP** |
| `GraveyardEntryDict` | Graveyard-entry fields. **KEEP** |
| `LevelUpSessionDict` | Level-up-session fields. **KEEP** |
| `CombatantStateDict` | Combatant-state fields. **KEEP** |
| `LegacyInitiativeEntryDict` | Legacy initiative-entry fields. **KEEP** |
| `EncounterStateDict` | Encounter-state fields. **KEEP** |
| `RewardsPendingDict` | Rewards-pending fields. **KEEP** |
| `WorldEventDict` | World-event fields. **KEEP** |
| `WorldTimeDict` | World-time fields. **KEEP** |
| `SocialHPContinuityDict` | Social-HP continuity fields. **KEEP** |
| `ActionResolutionRollDict` | Action-resolution roll fields. **KEEP** |
| `PlanningChoiceDict` | Planning-choice fields. **KEEP** |
| `PlanningChoiceLegacyDict` | Legacy planning-choice fields. **KEEP** |
| `SanctuaryModeDict` | Sanctuary-mode fields. **KEEP** |
| `SpellDict` | Spell fields. **KEEP** |
| `FactionMinigameDict` | Faction-minigame fields. **KEEP** |
| `CombatStateDict` | Combat-state fields. **KEEP** |
| `WorldDataDict` | World-data fields. **KEEP** |
| `SocialHPChallengeDict` | Social-HP-challenge fields. **KEEP** |
| `ActionResolutionDict` | Action-resolution fields. **KEEP** |
| `PlanningBlockDict` | Planning-block fields. **KEEP** |
| `CharacterDict` | Character fields. **KEEP** |
| `CustomCampaignStateDict` | Custom-campaign-state fields. **KEEP** |
| `StoryEntryDict` | Story-entry fields. **KEEP** |
| `GameStateDict` | Whole-game-state fields. **KEEP** |

### 22. `mvp_site/schemas/` — JSON and text data files

Each file is judged as a unit (contract/data, not code). "Readers" notes
come from local search; a file with no production readers but test readers
is kept as a test target where stated, never as a runtime exception proof.

| File | Justification + verdict |
|---|---|
| `character_creation_wire_schema.json` | Pass A: the externalized creation wire contract (pcd_properties, review/conclude fields and stages, planning block, conclude envelope, state_updates) that `character_creation_wire.py` assembles. Pass B: response-schema data, no filtering. **KEEP** |
| `character_deaths_schema.json` / `character_revivals_schema.json` | Pass A: the deaths (JSON-string items) and revivals (entity-id strings) wire contracts. Pass B: schema data for transport. **KEEP** |
| `criterion4_transport_canary_input.schema.json` | Pass A: a 229-byte canary input schema for criterion-4 transport testing. Pass B: test-transport data, no player-path effect. **KEEP (test fixture)** |
| `custom_campaign_state_core_memories.schema.json` | Pass A: the core-memories mutation contract for custom campaign state. Pass B: schema data. **KEEP** |
| `field_ownership_registry.json` | Pass A: the field-ownership registry (version + domains) pinning which domain owns rewards/level/experience and display/loot fields. Pass B: it has NO production readers found in this audit — only tests (`test_field_ownership_registry.py`, `test_schema_strictness.py`) — so it enforces nothing at runtime and, per the audit spec, proves no exception; it survives solely as a test-pinned ownership document. **KEEP (test-pinned documentation only; runtime enforcement value: none)** |
| `game_state.schema.json` | Pass A: the canonical game-state schema (100,672 bytes; `$defs` + properties + required) — the single source of truth every validator, schema assembler, TypedDict, and field-constant table derives from. Pass B: the contract itself; deleting it deletes the schema mechanism. **KEEP** |
| `game_state_schema_coverage_waivers.txt` | Pass A: the CI waiver list for schema-coverage gaps and scanner false positives, with the rule that new persisted paths belong in the schema, not here. Pass B: CI bookkeeping, no runtime behavior. **KEEP (waivers should shrink as coverage completes; each waiver is tech debt, not a runtime exception)** |
| `gameplay_state_patch.json` | Pass A: the gameplay patch contracts (npc_data, core_memories, custom_campaign_state, world_event_effects, world_sim_schedule_date) that the gameplay response schema projects. Pass B: schema data. **KEEP** |
| `gemini_schema_acceptance.json` | Pass A: the 1.26 MB acceptance manifest (incremental_acceptance, models, request_code_execution, schemas, verified_at) pinning which bound schemas passed real Gemini acceptance. Pass B: acceptance evidence for provider transport. **KEEP** |
| `level_up_grant_schema.json` | Pass A: the level-up grant wire contract. Pass B: schema data. **KEEP** |
| `level_up_selection.schema.json` | Pass A: the level-up selection wire contract. Pass B: schema data. **KEEP** |
| `npc_patch_transport.schema.json` | Pass A: the NPC patch transport contract (properties + required). Pass B: schema data; the framed-patch decoding lives in `_coerce_npc_update_entry` (KEEP). **KEEP** |
| `prompt_reminder_registry.json` | Pass A: the prompt-reminder registry (version, header, reminders, unaudited wired builders) feeding prompt assembly. Pass B: prompt-side data, not output filtering. **KEEP** |
| `prompt_tool_contracts.json` | Pass A: the prompt tool-contract manifest (manifest_version + contracts) for prompt assembly. Pass B: prompt-side data. **KEEP** |
| `reward_acquisition.schema.json` | Pass A: the reward-acquisition wire contract (properties + required + anyOf). Pass B: schema data. **KEEP** |
| `scene_illustration_policy.json` | Pass A: the scene-illustration policy (provider, cadence, timeouts, GCS prefix, brief) governing image generation cadence. Pass B: capacity/policy configuration for a non-text tool path, not campaign filtering. **KEEP** |
| `spell_slots_schema.json` | Pass A: the spell-slot contract (`legacy_read_aliases`, `valid_levels`) that `validation.py` derives read aliases and valid levels from. Pass B: schema-derived contract data. **KEEP** |
| `user_portrait_policy.json` | Pass A: the user-portrait policy (provider, preview delivery/transfer limits, suggest model) governing portrait generation. Pass B: capacity/policy configuration, not campaign filtering. **KEEP** |
| `world_sim_background_routine.schema.json` | Pass A: the world-sim background-routine wire contract. Pass B: schema data; under §6.3 this is the shape the async tick's output must satisfy. **KEEP** |
| `world_sim_relevance_highlights.schema.json` | Pass A: the world-sim relevance-highlights wire contract. Pass B: schema data. **KEEP** |
| `world_sim_setup.schema.json` | Pass A: the world-sim setup wire contract (fresh-roster canonical form that `load_world_sim_setup_schema` derives variants from). Pass B: schema data. **KEEP** |

## What remains (exact, open work — not hidden)

1. `llm_parser.stream_story_with_game_state` (lines 1892–5019): branch-level
   audit of the 3,128-line body. Function-level verdict (ADAPT: split out of
   the parser module) is recorded above and does not depend on unsampled
   branches, but any branch that invents, drops, or rewrites a campaign fact
   beyond the seams rowed above would add ADAPT/DELETE rows. A completing
   run should read it in ~500-line sections and append branch rows.
2. `game_state.schema.json` (`$def` by `$def`) and
   `gemini_schema_acceptance.json` (entry by entry): unit-level verdicts
   recorded above; field-level review is open but is schema review, not
   parser review, and should be scheduled as its own pass if wanted.
3. Registered-spec evidence gaps flagged above
   (`level_up_parser.raw_planning_preserve`,
   `level_up_parser.custom_action_fallback`,
   `level_up_modal.top_level_false_blocks_nested_activation`,
   `location.legacy_location_fallback_in_resolve_location`,
   `level_up_schema.normalize_planning_choice_shape`,
   `parse_recovery.escape_unescaped_string_quotes`): each carries
   `RUNTIME_EVIDENCE_MISSING` in `backend_adjustment_specs.py`. The owning
   team should either produce current-head real-LLM evidence or retire the
   spec; this audit's verdicts do not rely on any of them except as noted.
4. Implementation of every ADAPT/DELETE row needs the user's go-ahead per
   change (per standing boundaries: no repo writes without explicit
   approval). In particular, deleting `entity_validator` /
   `narrative_sync_validator` changes `llm_service` behavior (no more
   entity retry loop) and must be landed with its callers updated and the
   prompt entity requirement verified in the same change.
5. Run-1 handoff items are all closed by this run: full `schemas/`
   enumeration (38 files), existence of all four top-level files verified,
   and the GitHub 429 blocker bypassed by the local-copy rule. No run-1
   verdict was adopted, since run 1 recorded none.

## Reconciliation note (verdict counts)

Counts were tallied from the tables above by script after writing
(verdict tokens counted, then grouped rows expanded to named units:
validation.py symbol caches, NRS schema-variant rows, llm_parser lazy
proxies, entity classes, field-constant and TypedDict rows, and the
deaths/revivals JSON pair). Result: KEEP 458, ADAPT 35, DELETE 50,
total 543 units. If any count disagrees with a row, the row governs and
this note must be corrected, not the row.
