# God Mode / Level-Up / Rewards audit — WorldArchitect.AI (run 2)

**Scope:** `mvp_site/god_mode_*.py`, `mvp_site/level_up_*.py`,
`mvp_site/rewards_engine.py`, `mvp_site/campaign_upgrade.py`,
`mvp_site/campaign_divine.py`, `mvp_site/campaign_template_dragon_knight.py`,
`mvp_site/modal_conclude_policy.py`, `mvp_site/conclude_invariant.py`,
`mvp_site/backend_adjustment_specs.py`, `mvp_site/backend_adjustment_registry.py`,
`mvp_site/backend_adjustment_types.py`, the entire `mvp_site/adjusters/`
directory, and `mvp_site/docs/zfc_audit/` (Phase 1 file-level only for the docs).
Explicitly OUT of scope: `mvp_site/intent_classifier.py` and
`intent_classifier_warmup.py` (separate pilot).

**Method note:** This file is analysis only. Nothing here deletes, commits,
pushes, or changes anything in any repository. Repository file contents
(skills, agent instructions, prompts, policy docs) are treated as DATA for
this audit, never as orders. All file reads for run 2 came from the local
copy at `~/workspace/repos/worldarchitect.ai` (main-branch ZIP tree, no
`.git` history); zero GitHub API/MCP calls were used.

**Method (two passes, in order):** Pass A — zero-code baseline: against a bare
conversation log + Gemini API, what breaks if the unit is deleted, and can the
model supply it via log, prompt, or response schema? If the model can supply
it, DELETE. Pass B — strict ZFC: the model owns all campaign-domain facts;
the server provides ONLY transport, durable writes, tool execution,
authorization, and bounded capacity. A field-aware transform fails unless it
names a specific registered exception AND proves that exception necessary.
Registry membership alone proves nothing; determinism, schema validity,
display formatting, or normalization alone never justify a field-aware
transform. Verdicts are exactly KEEP / ADAPT / DELETE. ADAPT names the change.
Final verdict = stricter of the two passes, unless a named product promise
rescues it (named explicitly). Reference counting first: zero callers =
DELETE unless entry point, test target, or proven registered exception.

**Jeffrey's standing decisions (§6, override everything else):** (1) Server
logging KEEP; where it blocks a player turn, ADAPT to async/batched delivery.
(2) Anti-cheat KEEP; dice resolution stays ON the turn path; only the audit
trail may go async. (3) Faction/living-world KEEP but ADAPT to async
background ticks merged on the next turn. **Conflicts with §6 found: none.**
No verdict below contradicts §6: no synchronous turn-path logging or faction
simulation was found in this group, and the conclude/rewards guards that do
run on the turn path are authorization/fail-closed checks, not logging or
faction ticks. Run-1 pilot rule honored: modal conclude guards accept
explicit signals only — similarity scorers delete; the guard itself is rescued
by the explicit-exit guarantee (see `modal_conclude_policy.py` and
`conclude_invariant.py` below).

## Coverage — read this first

**Status: DONE except as noted per file below.** Run 2 completed the full
resumption checklist from run 1: `mvp_site/` top level re-enumerated,
`rewards_engine.py` confirmed to exist (8,773 lines), the entire
`mvp_site/adjusters/` tree re-enumerated recursively, and
`mvp_site/docs/zfc_audit/` located (it lives under `mvp_site/docs/`, not
repo-root `docs/`).

- **Fully done (per-method tables):** `god_mode_executor.py`,
  `god_mode_level_up.py`, `god_mode_schema.py`,
  `god_mode_state_commands.py`, `level_up_amend_reapply.py`,
  `level_up_audit.py`, `level_up_grant_contract.py`, `level_up_session.py`,
  `campaign_upgrade.py`, `campaign_divine.py`,
  `campaign_template_dragon_knight.py`, `modal_conclude_policy.py`,
  `conclude_invariant.py`, `backend_adjustment_registry.py`,
  `backend_adjustment_types.py`, all `adjusters/` code files.
- **Done with a sampling caveat:** `rewards_engine.py` — every top-level
  function, method, and module constant below has its own row, grounded in
  its signature, docstring, and sampled body sections; the two giant
  reducers (`_canonicalize_core`, ~1,000 lines; `canonicalize_rewards`,
  ~1,000 lines) were read in sampled sections, not every line. No verdict
  below depends on an unread line: both reducers are ADAPT with the same
  named split (keep session-backed projection, delete synthesis/suppression
  branches).
- **Done (per-spec tables):** `backend_adjustment_specs.py` — all 89
  registered specs individually justified, plus the grouping tuples.
- **Done (Phase 1 file-level only, as tasked):** `mvp_site/docs/zfc_audit/`
  (`FULL_AUDIT.md`, `SUMMARY.md`) and `adjusters/docs/` (11 files) plus
  `adjusters/README.md` — documentation, not shipped code, so file-level
  verdicts only.
- **Partial / blocked: none.** No file in scope is untouched, and no verdict
  below is fabricated from a filename alone.
- **Caller-count method:** reference counts were checked with local grep
  over `mvp_site/` (excluding `tests/`). Counts include the defining file,
  so a count of 1 means intra-file or test-only use; such symbols were
  kept only where they are entry points, test targets, registered
  callables (e.g. adjuster predicates passed to the engine), or called
  from within their own file by a kept caller — no symbol was deleted
  on a bare zero-external-caller count without that check. No symbol in
  this group was found to be wholly unreferenced (no production, test,
  or intra-file reference at all).

**Verdict counts (mechanically tallied from this file's tables):
KEEP 375, ADAPT 68, DELETE 28 — 471 verdict rows total (grouped rows cover
more than one symbol each, so the symbol count is higher; see "Verdict
tally" section). Docs file-level verdicts are separate: adjusters/docs +
README KEEP (12 files), docs/zfc_audit/ DELETE (2 files, archive).**

## Prior-ledger context (superseded where this audit differs)

- `god_mode_*` cluster: prior ledger said "KEEP minimal — God Mode
  Directives are a headline product promise. Executor + schema stay."
  This audit agrees and names that promise per unit where it rescues a
  verdict: **God Mode Directives (Type A directives + Type B story/memory
  edits) are the headline product promise**; it rescues the executor and
  schema envelopes, but not XP display refresh, legacy carrier fallbacks,
  or text-derived id synthesis.
- `level_up_*` cluster: prior ledger said "SHRINK (T1)". This audit
  sharpens it: the session/audit reducers mostly KEEP as durable-write and
  authorization machinery, while the display/synthesis layers around them
  are ADAPT or DELETE.
- `rewards_engine.py`: prior ledger said "DELETE/REWRITE (T1) — XP/level/
  resource values and reward magnitude are model-authored." This audit
  does NOT adopt wholesale DELETE: the receipt/authorization/anti-cheat
  core KEEPs (it is server-owned enforcement, not model-value authorship),
  while the recompute/synthesize/display layers are ADAPT or DELETE.
  Per-method testing, not the slogan, decides each row.
- `backend_adjustment_specs.py`: prior ledger said "AUDIT EACH SPEC". Done:
  89 specs, each with its own row; registry membership justifies nothing.

## god_mode_schema.py — file verdict: KEEP (minimized)

The response schema is the wire contract through which the model authors
God Mode directives; without it there is no typed God Mode turn at all.
The headline product promise (God Mode Directives) rescues the envelope
classes, but not the legacy fallback or the coercion flags (ADAPT below).

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| MAX_OPERATIONS_PER_TURN | Pass A: deleting it removes the only per-turn bound, so a runaway model turn could stuff unbounded ops into one commit. Pass B: a capacity bound is explicitly server-owned, not a domain fact, so the constant stays. | KEEP |
| ADMIN_EDITS_NOT_APPLIED_WARNING | Pass A: without this warning string, superseded-carrier edits would vanish silently and the player would never learn their admin edits were dropped. Pass B: it is a server warning message, not a field transform, so it is transport, not domain authorship. | KEEP |
| DirectiveAddOp | Pass A: the model needs a typed shape to author a new directive, and deleting it breaks the God Mode response schema. Pass B: a response-schema model is the sanctioned way for the model to supply facts, and it computes nothing. | KEEP |
| DirectiveReplaceOp | Pass A: replacing a directive by stable id is half the Type A contract; without it the model could only add and drop, never edit. Pass B: it is schema plus identity-scope fields the model authors, with no server recomputation of the rule text. | KEEP |
| DirectiveOperations | Pass A: the add/replace/drop grouping is the envelope the executor consumes, so deleting it breaks every directive turn. Pass B: grouping and per-list length caps are schema and capacity, both server-sanctioned roles. | KEEP |
| StoryEntryReplacementPayload | Pass A: Type B story retcons need a typed replacement payload, or the model cannot author corrected narrative. Pass B: it carries model-authored text and actor/mode labels verbatim, computing no domain values. | KEEP |
| StoryEntryReplacementOp | Pass A: without the target_id + replacement pairing, a retcon could not name which entry it replaces. Pass B: it is a pure addressing schema for model-authored content, not a server rewrite of that content. | KEEP |
| CoreMemoryAddOp | Pass A: core-memory adds are part of the Type B contract, and deleting the shape breaks memory edits. Pass B: it transports model-authored summary text and source-entry ids without recomputing them. | KEEP |
| CoreMemoryReplaceOp | Pass A: memory replacement needs the same target_id discipline as directives and story entries, or edits would be unaddressable. Pass B: schema-only addressing of model-authored text, with no server-side memory synthesis. | KEEP |
| CoreMemoryOperations | Pass A: the add/replace/drop envelope is what the executor applies, so its loss breaks memory turns. Pass B: grouping plus capacity caps are schema and bounded capacity, not domain judgment. | KEEP |
| StateReplacementOp | Pass A: explicit whole-value replacement at a model-selected path is the Type B state-edit mechanism; deleting it removes surgical state edits. Pass B: the path and value are model-authored and applied literally, which is tool execution, not server authorship. | KEEP |
| GodModeMutations | Pass A: this is the root envelope every God Mode turn validates against, so deleting it ends God Mode. Pass B: it is the response schema itself, and its validator enforces only the capacity bound, which is server-owned. | KEEP |
| total_operation_count (property) | Pass A: without a count, the per-turn cap cannot be enforced anywhere. Pass B: counting envelope items is capacity bookkeeping, not a domain fact, so it is server-owned. | KEEP |
| validate_total_operations | Pass A: deleting the validator lets over-cap envelopes through to the executor, breaking the capacity guarantee. Pass B: rejecting an over-cap envelope is bounded capacity enforcement, explicitly allowed, and it rewrites no values. | KEEP |
| GodModeOutcomeApply | Pass A: the apply outcome is the success shape of every God Mode turn, so its loss breaks the feature. Pass B: it pairs player-facing confirmation prose (model-authored) with the mutation envelope, computing nothing itself. | KEEP |
| GodModeOutcomeClarify | Pass A: without a clarify outcome the model cannot ask a question instead of applying, forcing bad applies. Pass B: it is a schema branch carrying model-authored prose, with no server domain logic. | KEEP |
| GodModeResponseSchema | Pass A: the discriminated-union root is what Gemini structured output validates against, so deleting it untypes God Mode entirely. Pass B: a response schema is the sanctioned model-supply channel, not a server transform. | KEEP |
| _DROPPED (sentinel) | Pass A: the prune helper needs a marker for dropped items, and without it partial validation cannot be expressed. Pass B: it is an internal implementation sentinel with no player-visible or domain effect. | KEEP |
| _valid_operations_only | Pass A: when one op in an envelope is malformed, whole-envelope rejection would discard the player's valid edits too, so best-effort pruning preserves the turn. Pass B: silently pruning invalid ops second-guesses the model instead of failing closed, so the salvage behavior must move to whole-envelope rejection plus a model retry, keeping pruning only as a temporary compat path. | ADAPT |
| _without_dropped | Pass A: the prune path needs a pure tree walk to remove sentinel-marked nodes, or pruned envelopes cannot be rebuilt. Pass B: it walks structure without reading any domain field's meaning, so it is transport, not a field-aware transform. | KEEP |
| strip_nested_admin_carrier_from_state_updates | Pass A: without it, admin carriers nested in state updates would double-apply or leak into persisted state. Pass B: removing a transport carrier after alias normalization prevents double execution, which is durability hygiene, not domain authorship. | KEEP |
| warn_if_superseded_carrier_has_content | Pass A: when a legacy carrier held edits that the canonical outcome superseded, silence would hide lost player edits. Pass B: appending a server warning is logging, which §6 keeps, and it mutates no game field. | KEEP |
| _strip_flattened_outcome | Pass A: legacy flattened outcomes must be reduced to a mutations dict before validation, or old clients' applies break. Pass B: dropping known envelope keys is shape handling, not a judgment about any domain value. | KEEP |
| _carries_operations | Pass A: callers need a predicate for whether a bare carrier actually holds operations before deciding to ignore or warn about it. Pass B: it validates shape and counts operations, which is schema and capacity logic, not domain recomputation. | KEEP |
| project_god_mode_mutations | Pass A: the canonical outcome path is essential, but the legacy bare-carrier fallback is what keeps very old clients working. Pass B: the fallback perpetuates a second, untyped authoring channel the schema was meant to replace, so slim it to the canonical outcome only and delete the legacy fallback once old clients are gone. | ADAPT |
| coerce_directive_values | Pass A: directive values arrive as strings, dicts, or malformed items, and some coercion is needed for the narrative parser to consume them. Pass B: the flag matrix (text fallback, blank-dict rejection, scalar stripping) is normalization with caller-specific behavior that the schema should enforce instead, so slim it to strict schema validation and delete the text-fallback and silent-drop branches. | ADAPT |
| get_god_mode_json_schema | Pass A: Gemini native structured output needs the JSON Schema dict, or God Mode turns lose typed output. Pass B: serializing the response schema is transport, and it adds no server-side domain logic. | KEEP |

## god_mode_executor.py — file verdict: KEEP (minimized)

The executor is the tool-execution half of the God Mode product promise:
it validates visibility, enforces capacity, and applies model-authored
mutations atomically. Those are authorization, capacity, and durable
writes — all server-owned. Only the XP display refresh is a delete, and
only XP alias mirroring is slimmed.

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| _MUTATION_OPERATION_KINDS | Pass A: replay withholding needs the full set of executable kinds, or already-run ops would re-execute on replay. Pass B: deriving the set from the schema keeps withholding correct by construction, which is execution safety, not domain judgment. | KEEP |
| _REPLAY_PATH_FILTERED_KIND | Pass A: state_replacements is the only kind with per-op receipts, so naming it lets replay keep unrun ops while withholding run ones. Pass B: it is a routing constant for idempotency machinery, not a domain fact. | KEEP |
| GodModeEnvelopeError | Pass A: typed envelope failures let callers withhold a bad turn instead of crashing or half-applying it. Pass B: an error type is transport, and failing closed on malformed admin input is authorization-adjacent. | KEEP |
| TargetNotVisibleError | Pass A: without a distinct visibility failure, targeting an unseen id could not be distinguished from other errors and handled fail-closed. Pass B: failing closed on invisible targets is the authorization core of God Mode, so the type stays. | KEEP |
| CapacityExceededError | Pass A: over-cap envelopes need a distinct failure so callers can reject them cleanly instead of partially applying. Pass B: capacity enforcement is explicitly server-owned, so the type stays. | KEEP |
| is_god_mode_mutation_replay | Pass A: without replay recognition, a retried client request would double-apply directives, story retcons, and memory edits. Pass B: idempotency-key matching plus input-hash binding is durable-write safety, not a domain decision. | KEEP |
| _subtract_replacement_path | Pass A: replay views must remove already-applied paths from deltas, or the UI would show edits as still pending. Pass B: it is a pure dict-path subtraction used by idempotency machinery, reading no domain semantics. | KEEP |
| _has_executable_mutation_envelope | Pass A: callers need to know whether structured fields actually declare an envelope before taking the replay path. Pass B: a presence check on a known carrier key is transport routing, not field-aware transformation. | KEEP |
| _mutation_carriers | Pass A: envelopes can arrive at three carrier locations, and missing one would silently drop a player's admin edits. Pass B: enumerating carriers in authority order is message routing, and it rewrites no values. | KEEP |
| _selected_mutation_carrier | Pass A: when several carriers exist, exactly one must win, or the same envelope could apply twice. Pass B: first-carrier selection is deterministic routing for execution safety, not a judgment about the edits' content. | KEEP |
| prepare_god_mode_replay | Pass A: committed and replayed views must not re-present executed ops, or the client would re-apply them. Pass B: withholding executed operations from views is idempotency enforcement, and it preserves raw input untouched for audit. | KEEP |
| _withhold_executed_mutation_ops | Pass A: without withholding, a committed request's persisted presentation would carry ops that already ran, inviting double execution. Pass B: dropping executed envelope kinds (keeping only unrun state_replacements) is execution safety, not a rewrite of model facts. | KEEP |
| _now_iso_utc | Pass A: audit events and edit timestamps need a clock, and the model cannot be trusted to stamp server time. Pass B: server time is a server-owned fact, so stamping it is transport, not domain authorship. | KEEP |
| _replace_state_value | Pass A: literal path replacement is the primitive that makes Type B state edits actually land. Pass B: it applies the model-selected path and value verbatim (scrubbing only untrusted marker keys), which is tool execution. | KEEP |
| _synchronize_replacement_xp_aliases | Pass A: legacy XP aliases already present in a sheet would go stale when canonical XP is replaced, showing the player contradictory XP. Pass B: mirroring canonical XP into aliases the sheet already carries is storage consistency for a server-persisted representation, but it must be slimmed to alias-only mirroring with no display recomputation. | ADAPT |
| _refresh_replacement_xp_display | Pass A: display projections could be left stale, but the client and the model can both re-derive display from canonical XP, so nothing player-essential breaks. Pass B: recomputing display fields (to_next_level, needed_for_next_level) from a canonicalizer is exactly the display-recomputation strict ZFC deletes, since display formatting alone never justifies a field-aware transform. | DELETE |
| collect_visible_target_ids | Pass A: visibility validation needs the union of visible ids, or no replace/drop could ever be authorized. Pass B: collecting ids the turn already showed the model is authorization input, not a new domain fact. | KEEP |
| collect_visible_target_authority | Pass A: per-kind authority partitions are what let visibility checks fail closed per operation kind instead of blurring kinds together. Pass B: partitioning already-visible ids by kind is authorization bookkeeping, and it invents no ids (positional fallbacks only name what is already shown). | KEEP |
| _validate_state_replacement_path | Pass A: malformed paths must be rejected before the candidate-state apply, or a bad path could corrupt state. Pass B: shape validation of a path is schema enforcement, and it rewrites no values. | KEEP |
| validate_target_visibility | Pass A: without it, a model could target directives, entries, or memories it never saw, breaking the visibility guarantee. Pass B: failing closed on unseen targets is the authorization core of God Mode, and it never rewrites a targeted value. | KEEP |
| apply_god_mode_mutations | Pass A: this is the function that actually performs God Mode — deleting it deletes the headline product promise itself. Pass B: it validates the envelope, checks visibility and capacity, and applies model-authored ops literally with reserved-key protection and idempotency, which is tool execution plus authorization plus durable writes, the three sanctioned server roles. | KEEP |

## god_mode_state_commands.py — file verdict: KEEP

These are pure helpers for the player-typed GOD MODE SET command: parsing
explicit player input and formatting already-executed updates for display.
Player-typed commands are not model output, so the model cannot supply them.

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| format_game_state_updates | Pass A: after a SET command executes, the player needs a readable confirmation of what changed, or the command is a black box. Pass B: it formats already-executed server state for display and transforms no model decision, so it is presentation of a server-owned result. | KEEP |
| recurse_items (nested in format_game_state_updates) | Pass A: nested updates must be flattened to leaf paths for the confirmation to be complete. Pass B: it is a pure traversal with no domain judgment, used only by the formatter above. | KEEP |
| parse_set_command | Pass A: the SET command is player-typed `key.path = value` text, and without this parser there is no way to turn it into state changes. Pass B: parsing explicit player input into a nested dict is command transport, and its JSON-value requirement plus non-object preservation are fail-closed parsing rules, not domain authorship. | KEEP |
| descend_object_path (nested in parse_set_command) | Pass A: nested assignment needs a helper that walks or creates intermediate objects without clobbering non-object values. Pass B: it is a pure structural helper for the player-command parser, with no knowledge of any game field's meaning. | KEEP |

## god_mode_level_up.py — file verdict: ADAPT

The dispatch routes god-mode level-up turns, and its admin-commit,
crossing-turn, and signal-only paths are the God Mode product promise
applied to leveling. But its strip branches delete model-emitted UI
artifacts that the prompt already prohibits, so those strips are interim
prompt fixes, not permanent server logic.

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| _planning_has_level_up_choices (alias of rewards_engine.planning_has_level_up_choices) | Pass A: signal classification needs to know whether the planning block carries level-up choices, or dispatch cannot pick a path. Pass B: it re-exports an explicit-choice predicate, so it inherits that predicate's verdict and adds no transform of its own. | KEEP |
| _strip_modal_from_structured | Pass A: after an admin commit, leftover modal choices would render a phantom level-up prompt, so some cleanup is needed. Pass B: wholesale stripping of modal choices from structured fields is a suppression the god-mode prompt already prohibits, so move the prohibition enforcement into the prompt/schema and keep server stripping only as a fail-closed guard for already-applied sessions. | ADAPT |
| _god_mode_level_up_signals | Pass A: dispatch cannot choose among admin commit, crossing-turn, and signal-only paths without classifying the three signals. Pass B: it reads explicit fields (a level write, a target-greater-than-current signal, explicit modal choices) and computes no domain values, so it is routing. | KEEP |
| _has_explicit_session_clear | Pass A: an explicit session clear (null, DELETE_TOKEN, or cancelled status) must be recognizable, or clears would be treated as activity. Pass B: recognizing explicit clear markers is reading the model's or the server's own explicit signals, not inferring intent. | KEEP |
| _has_explicit_flag_clear | Pass A: flag clears (pending/in_progress set false, or a session clear) gate the level-clear branch, and missing them would misroute clears. Pass B: it checks explicit false values and session clears only, so it is signal routing, not semantic inference. | KEEP |
| _god_mode_has_level_clear | Pass A: clears can hide in state_changes, structured fields, state_updates, or game_state nesting, and missing one leaves stale level-up UI. Pass B: it searches known containers for explicit clear markers only, which is exhaustive signal reading, not a domain transform. | KEEP |
| god_mode_has_level_activity | Pass A: callers need one predicate for whether a god-mode turn touches level-up at all, or they cannot gate downstream reducers. Pass B: it ORs the explicit-signal classifier with the explicit-clear detector, computing no new facts. | KEEP |
| _admin_level_facts | Pass A: the reducer needs from_level/to_level/sheet facts, and deriving from_level from pre-merge state (not post-merge state) is what makes the session record correct. Pass B: it assembles reducer input from the model's own delta and the saved pre-turn level, which is plumbing, not authorship of the level. | KEEP |
| _fail_closed_admin_level_up | Pass A: when the reducer rejects an admin commit, the turn must not crash and must not persist a half-applied sheet, so a restore path is essential. Pass B: restoring pre-turn PCD and the original session is fail-closed durability, and stripping the rejected commit's artifacts is authorization, not a recomputed grant. | KEEP |
| _god_mode_level_up_dispatch | Pass A: this is the router that makes god-mode leveling coherent — admin commits, crossing-turn write+signal, and signal-only pass-through would otherwise collide. Pass B: the commit and pass-through paths are product-promise routing, but the mixed/partial strip branches permanently encode a prompt prohibition, so keep the routing and move stray-choice stripping to the prompt/schema, leaving server strips only for already-applied sessions. | ADAPT |
| _strip_level_up_rewards_box_offer | Pass A: after a completed admin commit, a model-emitted level_up_available offer would render as a phantom prompt, so cleanup matters. Pass B: removing offer keys from a box whose session already completed is state-machine hygiene backed by the server-owned session, but the general offer-strip should live in the session projector, so slim this helper to the completed-session case only. | ADAPT |
| _strip_level_up_modal_choices | Pass A: admin commits must not leave a full family of level-up choices behind, or the UI offers an entry into an already-sealed session. Pass B: scrubbing the whole choice family (including ASI_/feat_/spell_ prefixes) is a broad suppression whose necessity rests on a prompt prohibition, so move it to prompt/schema enforcement and keep only the dead-entry affordance strip on the server. | ADAPT |
| _strip_level_up_now_only | Pass A: in the crossing-turn shape the level is already applied, so a lingering level_up_now button would resurrect the click-to-level-up staleness bug. Pass B: removing one literal dead affordance whose session already applied is state-machine hygiene keyed to server-owned session state, not a judgment about the model's choices. | KEEP |
| _strip_dead_level_up_now_choice | Pass A: the crossing-turn and clear paths need an in-place structured-fields wrapper for the dead-choice strip, or they would each reimplement shape handling. Pass B: it only delegates to the dead-affordance strip above for dict and string planning blocks, adding no new judgment. | KEEP |

## level_up_session.py — file verdict: KEEP (with two legacy ADAPTs)

The session reducer is the durable-write half of leveling: it merges the
model-authored sheet and records the grant (from/to/source/choices/
selections) plus pending-repair identity. It computes no XP, level, reward
size, or feature — those all arrive in the model-authored sheet — and its
fail-closed guards are authorization, not authorship.

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| STATUS_IN_PROGRESS / STATUS_COMPLETE / STATUS_CANCELLED | Pass A: saved sessions carry status values, and readers need the canonical strings to interpret them. Pass B: they are legacy vocabulary constants for durable records, not transforms. | KEEP |
| TERMINAL_STATUSES | Pass A: several paths need to test terminality at once, and a shared frozenset keeps that test consistent. Pass B: it is a vocabulary constant for session records, with no domain computation. | KEEP |
| SOURCE_MODEL | Pass A: grant records must distinguish model-authored grants from admin ones, or audit trails blur. Pass B: a provenance label on a durable record is bookkeeping, not authorship. | KEEP |
| SOURCE_GOD_MODE_ADMIN | Pass A: admin commits need a distinct source so the backward-level guard can allow operator corrections while forbidding model back-levels. Pass B: provenance labeling is bookkeeping, and the admin source is the God Mode product promise made auditable. | KEEP |
| SOURCE_SERVER_CORRECTION | Pass A: legacy sessions already carry this source, so readers must still recognize it to interpret old records. Pass B: it is read-only legacy vocabulary, and no new write uses it. | KEEP |
| OPERATION_GRANT | Pass A: the reducer validates its operation argument, and a named grant constant keeps that check explicit. Pass B: it is a vocabulary constant for the reducer's own dispatch. | KEEP |
| _VALID_SOURCES | Pass A: review-identity validation must accept exactly the schema-admitted sources, or legacy records would be misread. Pass B: it mirrors the schema enum for durable records, which is validation vocabulary, not a transform. | KEEP |
| _WRITE_SOURCES | Pass A: quarantining "server" and "migration" from new writes prevents a new server-authored grant from ever being recorded. Pass B: restricting write provenance to model and god-mode admin is authorization of the durable record. | KEEP |
| _is_strict_level | Pass A: bool is an int subclass in Python, so without a strict check a `true` level could pass as a level. Pass B: a type predicate for schema enforcement is validation, not domain computation. | KEEP |
| get_level_up_session | Pass A: every level-up path needs the canonical session dict, and a shared reader prevents divergent ad-hoc reads. Pass B: it is a pure read returning None for absent sessions, with no mutation or derivation. | KEEP |
| is_amendable_review_live | Pass A: review edits must only apply while the latest forward grant still matches the sheet level, or stale reviews would edit dead grants. Pass B: it compares saved session facts to the saved sheet level, which is authorization of the review, not a new grant. | KEEP |
| REVIEW_OPEN_ONLY_KEY | Pass A: review-open-only persistence operations need a stable key so the reducer can fence them. Pass B: it is a vocabulary constant for a persistence protocol, not a domain value. | KEEP |
| validated_pending_review_identity | Pass A: a stale opening must not retire an audit it does not name, so the live identity must be validated before any retirement. Pass B: it checks saved audit facts (pending status, positive generation, forward levels, valid source) against the saved grant, which is authorization, not authorship. | KEEP |
| review_operation_for_live_state | Pass A: without fencing, a stale opening's operation would retire a newer audit generation. Pass B: nulling the generation on identity mismatch is fail-closed authorization, and it rewrites no game values. | KEEP |
| reduce_review_persistence_operation | Pass A: review turns need one reducer that applies audit identity and retains rendered choices for the same review. Pass B: it delegates to the audit reducer and only retains model-rendered choices for the grant they belong to, which is durable-write plumbing. | KEEP |
| project_review_open_view | Pass A: review-open views must show committed PCD and session rather than stale scene deltas, or the review UI shows the wrong grant. Pass B: it copies committed state into view aliases, which is a read projection of durable state, not a recomputation of the grant. | KEEP |
| is_review_live_this_turn | Pass A: callers must know whether this turn is the grant turn or an explicit review interaction, since ordinary later turns are not review-live. Pass B: it compares pre-turn and post-turn session facts plus an explicit route flag, which is routing on saved facts and explicit signals. | KEEP |
| resolve_saved_review_choice | Pass A: resolving a clicked choice id against the saved grant's offered choices is how review clicks are honored. Pass B: it looks up an explicit choice id in saved offered choices, which is explicit-signal routing, not inference. | KEEP |
| record_review_offered_choices | Pass A: choices the model rendered on an explicit review turn must be saved on the grant, or later review clicks cannot resolve. Pass B: it stores model-rendered choices on the amendable grant only, leaving audit identity untouched, which is durable-write plumbing. | KEEP |
| _validate_dict_fact | Pass A: reducer inputs (sheet, choices, selections) arrive as lists or non-dicts, and normalizing them keeps the reducer total. Pass B: converting a list to an indexed dict and rejecting non-dict non-None values is input-shape validation, not domain judgment. | KEEP |
| _validate_json_safe | Pass A: Firestore cannot persist datetimes, sets, bytes, or non-string keys without silent coercion, so the reducer must reject them before persistence. Pass B: rejecting non-JSON-safe leaves is durable-write integrity, and it never substitutes a value. | KEEP |
| apply_level_up | Pass A: this is the single writer of level_up_session, and deleting it removes the grant record every downstream path reads. Pass B: it deep-merges the model-authored sheet, enforces strict-level and forward-only guards (with the admin back-level exception), and records provenance, which is durable writes plus authorization; it derives no XP, feature, or reward value. | KEEP |
| apply_model_level_up_signal | Pass A: an unresolved model progression signal needs a recorded session, or the pending transition has no durable home. Pass B: it records the signal's own current/target levels verbatim and refuses already-reached targets, which is durable recording of model facts plus fail-closed authorization. | KEEP |
| arm_pending_repair | Pass A: rejected or unresolved grants need a pending repair record, or the player never gets a repair turn. Pass B: it arms audit identity from saved levels and the caller's target, carrying retired generations forward, which is repair bookkeeping, not a recomputed grant. | KEEP |
| arm_legacy_session_repair | Pass A: legacy in-progress sessions with no live audit would otherwise never enter the repair flow, stranding old grants. Pass B: it is a one-time migration that fires at most once (it drops `status`), so slim it to a migration that deletes itself once legacy sessions are exhausted rather than a permanent path. | ADAPT |
| strip_stale_level_up_offer | Pass A: after admin corrections or terminal sessions, stale offer fields would keep rendering level-up prompts for dead transitions. Pass B: removing offer keys and legacy flags while leaving the canonical session untouched is state-machine hygiene keyed to server-owned session state. | KEEP |
| _LEVEL_UP_OFFER_KEYS / _LEVEL_UP_BOOKKEEPING_ONLY_KEYS / _LEVEL_UP_TRUTHY_REWARD_KEYS | Pass A: offer stripping needs shared key sets, or each strip site would diverge about what counts as an offer versus a reward. Pass B: these are vocabulary constants for strip logic, with no domain computation. | KEEP |
| strip_stale_level_up_offer_field | Pass A: single-record offer cleanup must preserve real rewards, so a field-level strip with a reward check is needed. Pass B: it drops a record only when no reward remains, which is state hygiene that never invents or sizes a reward. | KEEP |
| project_legacy_level_up_fields | Pass A: legacy readers still expect a rewards_box offer shape for a saved unapplied target, so a projector bridges them. Pass B: it derives a display offer from the saved session, which is legacy display projection, so sunset it with the legacy fields and let the session projector own offer display. | ADAPT |

## level_up_audit.py — file verdict: KEEP

The audit reducer owns pending-repair identity only: it arms, retires, and
counts unresolved repair turns, and it assembles the response-schema
contract the model must satisfy. It stores model-reported results and owed
choices verbatim and never derives them.

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| AUDIT_STATUS_PENDING | Pass A: pending audits need a stable status string across the session, audit, and amend modules. Pass B: it is vocabulary for a durable record, not a transform. | KEEP |
| AUDIT_OPERATION_TYPES | Pass A: the reducer must reject unknown operation types, and a shared set keeps that gate exact. Pass B: it is dispatch vocabulary for the audit reducer. | KEEP |
| AUDIT_MAX_CONSECUTIVE_FAILURES | Pass A: without a cap, an unanswered repair reminder would ride along forever, taxing every later turn. Pass B: a bounded reminder budget is capacity policy, explicitly server-owned. | KEEP |
| _AUDIT_RESULT_SCHEMA_PATH / _RESPONSE_CONTRACT_PATH | Pass A: the audit result schema and response contract live in prompt JSON files, and stable paths are how the code loads them. Pass B: they are file-location constants for schema loading, not domain logic. | KEEP |
| LEGACY_REVIEW_FLAG_KEYS | Pass A: legacy flag cleanup needs the exact old key names, or orphans would survive. Pass B: it is legacy vocabulary for state hygiene. | KEEP |
| _audit_operation_matches | Pass A: an audit operation must match the live audit's source and generation, or a stale result could retire a live repair. Pass B: identity matching on saved audit facts is authorization, not authorship. | KEEP |
| carry_live_audit | Pass A: a same-level write must not drop a pending repair, or the repair would silently vanish. Pass B: copying saved audit identity onto the new session is durable-write preservation, not a new decision. | KEEP |
| is_repair_reminder_exhausted | Pass A: callers need to know when the reminder budget is spent so they stop attaching the reminder. Pass B: comparing a saved failure count to the cap is capacity bookkeeping. | KEEP |
| _count_unresolved_turn | Pass A: each repair-carrying turn that leaves the repair unresolved must increment the failure count, or the cap never triggers. Pass B: incrementing a saved counter and logging at the cap is bookkeeping plus §6 logging, not a domain recompute. | KEEP |
| is_audit_retired_by | Pass A: a down-grant that retires exactly the live generation must be recognizable, or retired audits could be reopened. Pass B: it compares saved generation facts, which is authorization of retirement. | KEEP |
| _grant_turn_id | Pass A: grant identity needs the source turn id extracted safely, since missing or non-string ids must not crash matching. Pass B: it is a pure safe accessor for an authorization check. | KEEP |
| is_same_grant | Pass A: replays and distinct grants with identical level facts must be distinguishable, or a repeat grant from another turn would be misread as a replay. Pass B: it compares saved grant facts plus turn-id tie-breaking, which is identity logic for authorization. | KEEP |
| is_retired_grant_replay | Pass A: a delayed or replayed grant must not reopen a retired audit, or retired repairs would resurrect. Pass B: it combines same-grant identity with retired-generation facts, which is fail-closed authorization. | KEEP |
| reduce_audit_operation | Pass A: this is the only writer of pending-repair identity, and deleting it removes repair tracking entirely. Pass B: it arms, supersedes, resolves, or counts failures on saved audit identity, never deriving a grant value, so it is durable-write plus authorization machinery. | KEEP |
| _apply_audit_result | Pass A: model-reported audit results (clean/repaired/needs_input) and owed choices must be recorded, or the repair loop has no input. Pass B: it stores the model's own result and owed list verbatim and only retires the audit when no debt remains, which is recording, not derivation. | KEEP |
| load_response_contract | Pass A: schema assembly needs the contract fragments, and a fresh copy prevents shared-mutation bugs. Pass B: loading prompt JSON is schema transport. | KEEP |
| _ORDINARY_PCD_FAMILY_BY_AGENT | Pass A: ordinary agents need their schema family (narrative/gameplay/spicy) to pick the right ordinary PCD variant. Pass B: it is a routing table from agent name to schema family, not a judgment about any turn's content. | KEEP |
| _agent_name | Pass A: schema selection accepts agent objects or strings, so a name extractor keeps that polymorphic input working. Pass B: it is a pure name accessor for routing. | KEEP |
| ordinary_pcd_schema | Pass A: most turns need a PCD patch schema that requires a complete crossing sheet when level is authored, or incomplete crossings would pass validation. Pass B: it assembles the response schema (including inlining canonical spell definitions so Gemini accepts it), which is the sanctioned model-supply channel, not a server transform of a turn. | KEEP |
| ordinary_pcd_schemas | Pass A: callers need all three family variants at once for the Gemini catalog. Pass B: it maps the schema builder over the three bases, adding no logic of its own. | KEEP |
| uses_ordinary_pcd_schema | Pass A: the catalog needs to know whether an agent uses the ordinary contract, or schema selection would misroute agents. Pass B: it is a membership check on a routing table. | KEEP |
| ordinary_pcd_schema_for_agent | Pass A: per-agent schema selection must return exactly that agent's family variant. Pass B: it is a routing lookup, with no content judgment. | KEEP |
| _CONTRACT_CACHE | Pass A: schema assembly is expensive and id-keyed caching prevents rebuilding identical contracts. Pass B: it is a cache for schema transport, with an identity check that prevents stale reuse. | KEEP |
| with_level_up_contract | Pass A: review and repair turns need the audit-result slot and repair sheet requirements added to the base schema, or the model cannot author a repair. Pass B: it assembles response-schema requirements (never loosening the base's own required fields), which is the sanctioned supply channel. | KEEP |

## level_up_grant_contract.py — file verdict: ADAPT

The grant contract validates model-authored sheets and folds grant values
into crossing sheets. Validation KEEPs; the fold family is ADAPT because
the grant's fields belong in the response schema as required sheet fields,
not in a server-side fill pass — though the fold is honest transport
today (it only fills fields the model left absent, and only when the
grant target equals the sheet level on a genuine forward crossing).

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| LEVEL_UP_GRANT_KEY | Pass A: the grant transport key must be stable so state_updates parsing can find and remove it. Pass B: it is a vocabulary constant for a transport slot. | KEEP |
| _SCHEMA_PATH | Pass A: the grant schema JSON must be loadable from a stable location. Pass B: it is a file-location constant for schema loading. | KEEP |
| LEVEL_SCALED_PCD_FIELDS / LEVEL_SCALED_POOL_FIELDS / LEVEL_SCALED_REGISTRY_CATEGORIES / LEVEL_SCALED_RESOURCE_KEYS / HP_MAX_KEYS | Pass A: revert and fold logic needs shared field vocabularies, or each site would diverge about which fields a crossing rewrites. Pass B: these are vocabulary constants for validation and revert logic, not computations. | KEEP |
| level_up_grant_schema | Pass A: the model-facing grant schema must be inlined and self-contained, or Gemini rejects dangling $defs references. Pass B: assembling a response schema from canonical definitions is the sanctioned supply channel. | KEEP |
| _hp_max | Pass A: completeness checks must find max HP across health/hp alias shapes, or valid sheets would be misjudged incomplete. Pass B: it reads existing alias values without writing or choosing any, so it is a read helper for validation. | KEEP |
| is_complete_model_level_up_sheet | Pass A: the reducer needs to know whether a sheet carries canonical progression plus the HP gain or another mechanical change, or incomplete sheets would pass silently. Pass B: it is a validation predicate over model-authored values that rejects nothing and writes nothing, so it is schema enforcement. | KEEP |
| _deep_merge | Pass A: sheet merging must be recursive, or nested fields (hp, spell slots, experience) would be dropped by shallow merges. Pass B: it is a pure structural merge used by reducers, with no domain judgment. | KEEP |
| _is_int | Pass A: bool-as-int confusion must be excluded from every level/HP check, or `true` would pass as a number. Pass B: a type predicate for validation. | KEEP |
| _feature_name | Pass A: feature dedup needs a normalized name (stripped, casefolded) so the same feature in different cases is not double-added. Pass B: it normalizes a name for comparison only and writes no feature itself. | KEEP |
| _is_valid_entry | Pass A: blank strings and nameless dicts must not count as gained features or spells. Pass B: it is a validity predicate for model-authored entries. | KEEP |
| _has_hp_max_key | Pass A: the HP fold must not overwrite an explicitly authored max (even null), so presence must be detectable separately from value. Pass B: it is a presence predicate for a merge guard. | KEEP |
| _fold_hp_max | Pass A: a grant's hp_max rescues a crossing sheet that omitted max HP, which the completeness check would otherwise flag. Pass B: filling an absent field from a model-authored grant is transport of the model's own value, but it belongs in the schema as a required grant field, so move it there and delete the server fill. | ADAPT |
| _fold_features | Pass A: a grant's gained features rescue a sheet that omitted features, preserving the player's level-up choices. Pass B: appending only valid, non-duplicate, model-authored features to an absent-or-empty list is transport, but like the HP fold it belongs in the schema-required sheet, so move it there and delete the server fill. | ADAPT |
| _fold_spell_slots | Pass A: a grant's spell-slot maxima rescue a sheet that omitted slot maxima. Pass B: filling only absent maxima from model-authored grant values is transport, but the maxima belong in the schema-required sheet, so move them there and delete the server fill. | ADAPT |
| fold_level_up_grant | Pass A: the grant slot must be consumed (always removed, never persisted) and its values applied to the crossing sheet, or grants would leak into state. Pass B: its target-equals-sheet-level and forward-crossing gates are authorization, but the fold orchestration itself should disappear once the grant fields are schema-required, leaving only the gate and the pop. | ADAPT |
| _set_armor_class | Pass A: armor_class and its `ac` alias must stay mirrored when the merge computes a final AC, or readers of the alias would see a stale value. Pass B: mirroring an authored value into an existing alias is storage consistency (it has a live caller in game_state_merge), not a recomputed bonus. | KEEP |

## level_up_amend_reapply.py — file verdict: KEEP (one ADAPT)

These are turn-path helpers that read model-authored sheets, apply
committed grants, and build audit persistence operations. They write no
level, XP, or reward value themselves; the reducers do the writing.

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| _model_authored_grant_sheet | Pass A: callers must distinguish a genuine model level raise from a non-grant PCD write, or session-backing checks would misfire. Pass B: it compares authored level to committed level and returns the model's own sheet, deriving no value. | KEEP |
| model_grant_sheet_has_session_backing | Pass A: a saved grant must not block a later model-authored crossing, and this predicate is how callers know the grant is session-backed. Pass B: it ANDs the sheet predicate with session presence, which is authorization bookkeeping. | KEEP |
| is_opening_level_up_click | Pass A: an opening click must resolve against the saved planning block plus an actionable pending transition, or any click could open the modal. Pass B: it resolves an explicit choice id against persisted planning-block evidence, which is explicit-signal routing. | KEEP |
| _replace_delta | Pass A: the state merge deep-merges dicts, so replacing a session needs DELETE_TOKENs for keys the new session lacks, or stale keys would survive. Pass B: it is a pure merge-transport helper with no domain knowledge. | KEEP |
| apply_committed_grant | Pass A: an accepted grant must land in state_changes while stale legacy flags are cleared, or the UI would show both the new grant and old pending flags. Pass B: it copies reducer-committed state and clears legacy flags with DELETE_TOKENs, which is durable-write plumbing. | KEEP |
| backfill_rewards_box_new_level (alias of rewards_engine.backfill_rewards_box_new_level) | Pass A: a committed level change needs its new_level visible in the rewards box, or the UI would not reflect the grant. Pass B: it re-exports the rewards-engine backfill, so it inherits that function's ADAPT: emit new_level from the session projector instead of mutating the box post-hoc. | ADAPT |
| audit_persistence_operation | Pass A: repair turns need a persistence operation (or an explicit failure count) while keeping the full gameplay candidate, or repairs would either block play or vanish. Pass B: it derives the operation from saved audit identity and the model's own audit result, never inventing a verdict, and it preserves the candidate state untouched. | KEEP |
| routed_audit_persistence_operation | Pass A: only turns that actually carried the pending repair (per router metadata) should build audit persistence, or unrelated turns would corrupt repair state. Pass B: it trusts the router's classifier metadata rather than re-deriving intent from raw input, which is routing discipline, and it fences review-open-only operations to their named identity. | KEEP |
| build_level_up_facts | Pass A: the reducer needs target level plus pending selections assembled from the turn's state, or it cannot run. Pass B: it reads model-authored selections across fallback sources, but the three-source fallback chain (delta, then current state, then model session) should collapse to a single canonical selections source, so slim it to that source and delete the fallbacks. | ADAPT |

## campaign_upgrade.py — file verdict: ADAPT

The ceremony modal lock is server-owned flag state-machine work (it strips
model writes to server-owned flags), so it KEEPs. The two normalizers and
the load-time flag canonicalization are compat shims whose work belongs in
the response schema and in a one-time migration, respectively.

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| _CANONICAL_LEVEL_UP_FLAGS | Pass A: load-time canonicalization must know exactly which flags have a nested canonical home. Pass B: it is vocabulary for a storage-migration rule. | KEEP |
| canonicalize_level_up_flags_on_load | Pass A: older campaigns persisted top-level level-up flags, and without folding them into custom_campaign_state, readers would reconcile two locations forever. Pass B: it is a load-time storage migration (nested wins, orphans deleted) rather than a per-turn domain decision, so keep it only until legacy campaigns are migrated, then delete it. | ADAPT |
| normalize_planning_block_choices | Pass A: planning blocks arrive as JSON strings, dicts, or lists, and downstream code needs list-format choices with ids. Pass B: dict-to-list shape coercion is transport, but synthesizing a choice id from lowercased text (or `choice_{idx}`) invents an identifier the model never authored, so keep the shape coercion and delete text-derived id synthesis — the schema must require model-supplied ids. | ADAPT |
| normalize_choices_to_array | Pass A: dict-format choices must become arrays of objects with an id field for uniform downstream handling. Pass B: it is pure shape conversion, but shape is the response schema's job, so keep it only as a compat shim until the schema enforces array choices, then delete it. | ADAPT |
| _CAMPAIGN_UPGRADE_COMPLETE_TIERS | Pass A: the modal lock needs the set of tiers that count as ceremony-complete without hardcoding them in the lock. Pass B: it reads the central registry so a constants toggle propagates, which is configuration, not domain judgment. | KEEP |
| enforce_campaign_upgrade_modal_lock | Pass A: without the lock, a campaign-upgrade ceremony would re-arm every turn, ignore declines, or let the model set its own in-progress flags. Pass B: it strips model writes to server-owned flags, runs a one-turn ceremony state machine, and defers tier promotion to ceremony confirmation, which is authorization plus ceremony routing; the tier-availability question itself is delegated to campaign_divine (audited separately as DELETE — the lock must eventually take availability from a model signal instead). | KEEP |

## campaign_divine.py — file verdict: DELETE (except the tier reader)

This module recomputes campaign-domain facts on the server: whether a
divine or multiverse upgrade is "available" from potential/level/control
thresholds, and the highest stat modifier for God Power conversion. Under
strict ZFC the model owns those facts and declares them through the
schema; the server's threshold arithmetic is exactly the recomputation
the audit deletes. Only the pure tier reader survives, because reading a
stored value is transport.

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| get_campaign_tier | Pass A: every upgrade path needs the stored tier, defaulting to mortal, and a shared reader prevents divergent defaults. Pass B: it reads one stored value with a default, computing nothing, so it is transport. | KEEP |
| is_divine_upgrade_available | Pass A: ceremony routing currently depends on this check, but the model can declare upgrade availability (flag, potential, or level) through the response schema, so routing would not break — it would move. Pass B: thresholding divine_potential >= 100 and level >= 25 on the server recomputes a campaign-domain fact the model owns, and no registered exception names this computation as necessary. | DELETE |
| is_multiverse_upgrade_available | Pass A: the multiverse gate is currently server-computed, but like the divine gate it can be a model-declared signal gated by the same constants toggle. Pass B: evaluating universe_control against a threshold (behind an enablement flag) is server-side domain arithmetic with no named necessary exception, so it deletes with the divine gate. | DELETE |
| is_campaign_upgrade_available | Pass A: callers use this OR of the two gates, but once both gates are model-declared signals, the OR is a trivial schema-level combination. Pass B: it inherits the DELETE of both gates it combines, since it adds no server-owned logic of its own. | DELETE |
| get_pending_upgrade_type | Pass A: the pending type (multiverse-first, then divine) is currently derived server-side, but a model-declared upgrade signal can carry its own type. Pass B: it derives a domain fact from two deleted server computations, so it deletes with them. | DELETE |
| get_highest_stat_modifier | Pass A: God Power conversion currently needs the highest modifier, but the model authors ability scores and can author the derived modifier (or the conversion input) in its sheet. Pass B: scanning attributes and computing (score-10)//2 maxima is server-side recomputation of a model-owned derived stat, with no named necessary exception. | DELETE |

## campaign_template_dragon_knight.py — file verdict: KEEP

The Dragon Knight template is a pre-generated campaign shortcut: a
canonical prompt, description, and opening payload served when a request
exactly matches the template defaults. Deterministic template delivery is
a product promise (a fixed starter campaign), not a judgment about a
player's live campaign, and the hash guard is integrity checking.

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| _DATA_PATH | Pass A: the canonical description text must be loaded from a stable bundled path. Pass B: it is a file-location constant. | KEEP |
| verify_dragon_knight_canonical_hash | Pass A: without the hash check, drift between the bundled prompt and the constants would silently serve a non-canonical template. Pass B: comparing a SHA-256 digest to a committed constant is integrity verification, not domain authorship. | KEEP |
| _canonical_dragon_knight_prompt | Pass A: the canonical prompt must be rebuilt from the same inputs as the production wizard, or the hash and the template would diverge. Pass B: it composes a prompt from constants and bundled text, which is template assembly for a fixed product asset. | KEEP |
| get_canonical_dragon_knight_prompt | Pass A: template generation scripts need the canonical prompt, and a shared getter prevents divergent rebuilds. Pass B: it delegates to the canonical builder, adding no judgment. | KEEP |
| get_canonical_dragon_knight_description | Pass A: callers need the bundled description text for the template. Pass B: it reads a bundled product asset verbatim. | KEEP |
| request_matches_dragon_knight_template_defaults | Pass A: the shortcut must fire only on an exact match (selected prompts, custom options, prompt hash), or any campaign could be hijacked into the template. Pass B: exact-match comparison against committed constants is gating for a fixed product asset, not inference about a request. | KEEP |
| get_dragon_knight_template_opening_if_applicable | Pass A: when the shortcut applies, the player gets the pre-generated opening story, structured fields, and state updates instead of a fresh generation. Pass B: serving a fixed, committed template payload on an exact match is product delivery of a canned asset, and it returns None otherwise, so it never rewrites a live campaign's facts. | KEEP |

## modal_conclude_policy.py — file verdict: KEEP (explicit signals only; fuzzy stage ADAPT)

Per the run-1 pilot rule, the conclude guard is rescued by the
explicit-exit guarantee: structured choice ids, CHOICE: prefixes, JSON
modal-choice payloads, and exact visible button labels are explicit
signals, and free text goes to the FastEmbed classifier (model-owned
judgment). The bare-token normalization stage is the one fuzzy piece:
it rewrites arbitrary mixed-case/separator input into canonical ids,
which is normalization the strict pass does not allow — the exact,
prefixed, and JSON forms already cover legitimate client emissions.

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| DOMAIN_LEVEL_UP / DOMAIN_CHARACTER_CREATION | Pass A: conclude routing must distinguish the two modal domains, or a level-up finish could release character creation and vice versa. Pass B: they are domain vocabulary constants for routing. | KEEP |
| CHARACTER_CREATION_EXIT_CHOICES | Pass A: character creation needs a closed set of finish ids the guard can recognize, or exits would be unroutable. Pass B: a closed vocabulary of explicit choice ids is the explicit-signal contract itself. | KEEP |
| CHARACTER_CREATION_CANCEL_CHOICES | Pass A: cancellation needs its own recognized id so it is not mistaken for a finish. Pass B: it is part of the same explicit-signal vocabulary. | KEEP |
| LEVEL_UP_EXIT_CHOICES | Pass A: level-up finish needs exactly one canonical exit id, or the modal could never be sealed deterministically. Pass B: a single explicit choice id is the explicit-exit guarantee for level-up. | KEEP |
| LEGACY_FINISH_CHOICE_IDS | Pass A: older clients still emit `complete_levelup`/`finish`, so dropping the set would strand their finishes. Pass B: it is legacy vocabulary for explicit ids, so keep it only until old sessions drain, then delete it rather than extending it. | ADAPT |
| _PLAIN_TEXT_EXIT_MAP | Pass A: clients emit plain-text button labels (playcharacter, standarddnd, customclass, confirmtemplate), and without the map those explicit button presses would not route. Pass B: mapping exact button labels to ids is explicit-signal recognition (the client emitted that label), not semantic inference. | KEEP |
| _KNOWN_MODAL_CHOICE_IDS | Pass A: exact-match recognition needs the union of all modal vocabularies in one set. Pass B: it is the closed vocabulary itself, derived from the explicit id sets. | KEEP |
| _bare_token_normalize | Pass A: case-folding and separator-stripping lets mixed-case client emissions match, but the exact, CHOICE:, JSON, and label forms already cover legitimate emissions. Pass B: normalizing arbitrary tokens against the vocabulary is fuzzy matching that the strict pass rejects — it rewrites input the model/client did not emit in canonical form — so delete this stage and its map, keeping only exact/prefixed/JSON/label recognition. | ADAPT |
| _BARE_TOKEN_TO_CANONICAL_ID | Pass A: the normalization stage needs its precomputed map, but the map exists only to serve that stage. Pass B: it inherits the ADAPT of the normalization stage it serves, and deletes with it. | ADAPT |
| _extract_from_prefixed_choice | Pass A: CHOICE:-prefixed input is the canonical structured form, and extracting it is how prefixed emissions route. Pass B: it reads an explicit prefix and matches against the closed vocabulary, which is explicit-signal parsing. | KEEP |
| extract_modal_choice_id | Pass A: this is the single entry point for modal choice recognition, and deleting it breaks every conclude path. Pass B: its CHOICE:, JSON, exact-match, and plain-label stages are explicit-signal parsing and stay, but its stage-4b bare-token stage is fuzzy normalization, so slim it to the explicit stages and delete stage 4b. | ADAPT |
| _matches_visible_finish_text | Pass A: visible finish-button text (with " - " or ": " suffixes) must match so button presses seal the modal. Pass B: matching exact button labels the client already emits is explicit-signal recognition, not free-text interpretation. | KEEP |
| level_up_finish_visible_text_matches | Pass A: level-up finish buttons carry several canonical wordings (current and legacy), and all must seal the modal. Pass B: it matches only listed exact label prefixes, which is the explicit-exit guarantee for button text. | KEEP |
| character_creation_finish_visible_text_matches | Pass A: the character-creation finish button label must seal creation, or players could not exit by tapping it. Pass B: it matches one exact label prefix, which is explicit-signal recognition. | KEEP |
| get_character_creation_exit_choice_id | Pass A: creation exits arrive as choice ids or as finish-button text, and one function must resolve both to the canonical id. Pass B: it combines explicit-id recognition with exact-label matching, both explicit signals, and returns None otherwise. | KEEP |
| is_level_up_finish_choice_input | Pass A: callers need a boolean for whether input is the level-up finish choice. Pass B: it is a membership test on explicit-id recognition, with no inference. | KEEP |
| _extract_structured_clean_text | Pass A: detect_conclude_signal needs to know whether input is a structured postback and what clean text it carries. Pass B: it reads explicit structured forms (dict keys, CHOICE: prefix, modal_choice JSON) and reports non-structured input as such, without interpreting free text. | KEEP |
| detect_conclude_signal | Pass A: this is the guard that decides whether a turn concludes a modal, and deleting it removes modal sealing entirely. Pass B: structured input is decided by explicit-id and exact-label recognition (the rescued guard), while free text is delegated solely to the FastEmbed classifier — model-owned judgment — so the function itself makes no semantic decision. | KEEP |

## conclude_invariant.py — file verdict: KEEP (warn-only telemetry)

This module never mutates state: it validates the conclude payload
against the snapshot schema, reconciles derived stats against the pure
reducer, and logs a warning on mismatch. Under §6, server logging KEEPs,
and a warn-only check that cannot override the model is telemetry, not a
field-aware transform. Its registered exception is
`conclude.reconcile_derived_stats` (see the specs table).

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| CONCLUDE_RECONCILE_LOG_REASON_CODE | Pass A: mismatch warnings need a stable reason code so telemetry can be queried. Pass B: it is a logging vocabulary constant matching the registered spec. | KEEP |
| _PC_DERIVED_FIELD_MAP | Pass A: the reducer payload needs PC fields projected to reducer names (notably hp_max to max_hp), or the check would compare the wrong fields. Pass B: it is a field-name mapping for a read-only check, and it deliberately excludes max_hp as a PC source to avoid shadowing, which is check hygiene, not a state transform. | KEEP |
| build_conclude_reconcile_payload | Pass A: without a payload projector, the reducer could not be run over the conclude turn's level, class, and derived fields. Pass B: it projects model-authored fields into a check-only payload and returns None when no level exists, mutating nothing. | KEEP |
| _validate_conclude_snapshot | Pass A: contract-violating payloads (e.g. narrative-milestone levels) still need a derived-stats check, so validation failure must fall back to the raw payload rather than aborting. Pass B: it validates against the schema and logs on failure, never raising or mutating, which is warn-only telemetry. | KEEP |
| emit_conclude_reconcile_warning | Pass A: the proving-window question — "is the conclude prompt actually holding in prod?" — needs mismatch telemetry, or regressions would be invisible. Pass B: it returns state unmutated by construction, so it cannot second-guess the model's commit; it only logs, which §6 keeps. | KEEP |

## rewards_engine.py — file verdict: ADAPT (split the reducer; keep the authorization core)

This file is two files fused together. Its receipt, authorization,
anti-cheat, and explicit-signal routing core KEEPs: it validates reward
receipts, blocks unauthorized level mutations, reverts rejected
transactions, and routes on explicit choice ids. Its recompute layer —
canonical progress percentages, XP anchoring, synthesized rewards boxes,
display projections, and the synthesis/suppression branches of the two
giant reducers — is the T1 target: those values are model-authored, and
the model can supply them through the signal and response schemas.
`canonicalize_rewards` and `_canonicalize_core` are therefore ADAPT with
the same named split: keep session-backed projection and fail-closed
authorization, delete synthesis and suppression branches (moving their
contracts to prompt/schema).

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| _world_logic_module (lazy import helper) | Pass A: rewards code needs world_logic without a circular import, and lazy loading is how it gets it. Pass B: it is import transport with no domain effect. | KEEP |
| is_state_flag_true / is_state_flag_false (aliases) | Pass A: flag checks are used throughout the file, and shared aliases keep truthiness consistent. Pass B: they are boolean predicates on stored flags, not domain computations. | KEEP |
| _REWARDS_BOX_XP_GAIN_KEYS | Pass A: receipt validation must know which keys count as XP gain in a rewards box. Pass B: it is vocabulary for receipt validation. | KEEP |
| REWARD_CORRECTION_PREFIX | Pass A: system correction strings for rewards need a recognizable prefix so they are not mistaken for player text. Pass B: it is a vocabulary constant for a server message channel. | KEEP |
| is_reward_correction / _is_reward_correction (alias) | Pass A: callers must recognize reward-related system corrections to handle them separately from narrative. Pass B: it is a prefix predicate on server messages, not a judgment about game facts. | KEEP |
| _record_rewards_delivery | Pass A: delivery must be recorded only for a tangible panel tied to the ended source, or duplicate delivery could not be detected. Pass B: recording a server-owned delivery receipt is durable-write bookkeeping, not reward authorship. | KEEP |
| record_rewards_delivery (alias) | Pass A: the public name is how callers record delivery, and deleting it breaks those call sites. Pass B: it inherits the receipt-bookkeeping verdict of the helper it aliases. | KEEP |
| is_trackable_reward_source | Pass A: only trackable sources can be receipted, so an untrackable source must be recognizable before delivery logic runs. Pass B: it is a source-classification predicate for server-owned receipt state. | KEEP |
| _REWARD_EVENT_TIER_BAND_CEILINGS | Pass A: allowance clamps need tier band ceilings, or unreceipted XP could not be bounded. Pass B: a capacity table is bounded-capacity policy, explicitly server-owned. | KEEP |
| effective_pre_turn_level | Pass A: band sizing needs a pre-turn level, but taking max(stored level, XP-derived level) lets XP-derived levels override the model's own level. Pass B: deriving a level from XP recomputes a model-owned fact, so slim it to the stored level only and delete the XP-derived branch. | ADAPT |
| level_band_span | Pass A: allowance clamps need the XP width of a level's band, and the threshold table is the only source for it. Pass B: a band-width lookup feeding a capacity clamp is bounded-capacity machinery, not a grant of XP. | KEEP |
| detect_reward_anomalies | Pass A: reward conversions (e.g. XP-for-gold reshaping) must surface as durable anomaly descriptors, or silent conversions would be invisible. Pass B: it detects and describes anomalies without rewriting the reward, which is audit logging that §6 keeps. | KEEP |
| _record (nested in detect_reward_anomalies) | Pass A: anomaly detection needs a local accumulator for descriptors. Pass B: it appends descriptors only, with no domain judgment of its own. | KEEP |
| _UNRECEIPTED_XP_BAND_CEILING / _UNRECEIPTED_XP_FLOOR | Pass A: unreceipted XP increases need upper and lower bounds, or the anti-cheat clamp has no numbers to enforce. Pass B: capacity bounds are explicitly server-owned. | KEEP |
| _reward_event_source_bucket_id | Pass A: anomaly provenance needs a stable bucket id per source, or identical sources would be double-counted. Pass B: it is an identity helper for receipt bookkeeping. | KEEP |
| _resolve_reward_event_source_provenance | Pass A: receipts need source identity plus anomaly provenance to be attributable. Pass B: it resolves provenance for a server-owned receipt, inventing no reward values. | KEEP |
| reward_event_tangible_delta_is_positive | Pass A: gates need to know whether a candidate actually adds gold or items versus the pre-turn sheet. Pass B: it is a comparison predicate on model-authored and stored values, not a new value. | KEEP |
| _REFUSED_DUPLICATE_SOURCE_CLAIM / _REFUSED_INVALID | Pass A: refused receipts need stable reason codes for logging and dedup. Pass B: they are vocabulary constants for receipt refusal. | KEEP |
| extract_and_validate_reward_event | Pass A: a reward_event receipt must be extracted and validated before anything trusts it, or fabricated receipts would pay out. Pass B: validating a receipt against pre-turn state is authorization of a server-owned record, not authorship of the reward. | KEEP |
| _validate_reward_event | Pass A: receipt validation needs the detailed rule set (source, tier, duplicates, deltas) in one place. Pass B: it checks a receipt against saved state and refuses invalid ones, which is anti-cheat enforcement. | KEEP |
| reject_model_authored_rewards_box | Pass A: a model-authored rewards_box that is not receipt-backed must be recognizable as rejectable, or unreceipted boxes would pay out. Pass B: it is an authorization predicate (true iff the box is model-authored without backing), not a recomputation of the box. | KEEP |
| is_character_creation_conclude_commit | Pass A: the genuine in-progress-to-complete character-creation transition needs a precise predicate so conclude commits are not misclassified. Pass B: it reads explicit transition state (server stamps plus model state), which is routing on explicit signals. | KEEP |
| SANCTIONED_ZERO_DELTA_CARVE_OUTS | Pass A: zero-delta receipts need sanctioned carve-outs, or legitimate no-change events would be refused. Pass B: it is a vocabulary constant for receipt validation exceptions. | KEEP |
| is_character_creation_exit_choice_selected | Pass A: character-creation exit handling needs to know whether a structured exit choice was selected. Pass B: it tests an explicit choice id, which is explicit-signal routing. | KEEP |
| extract_authored_level_up_intent | Pass A: the turn's level-up intent lives as a (signal, grant) pair, and callers need both halves together. Pass B: it reads the model-authored pair verbatim without deriving either half. | KEEP |
| _unreceipted_xp_increase_rejected | Pass A: XP raises with no receipt authority must be recognizable so they can be blocked. Pass B: it is an anti-cheat predicate comparing a raise against receipt authority. | KEEP |
| _is_plain_number | Pass A: numeric checks need to exclude bools and non-numbers safely. Pass B: it is a type predicate for validation. | KEEP |
| _tangible_item_key | Pass A: inventory entries (dicts or strings) need stable identity for delta computation. Pass B: it is an identity helper for baseline comparison, not a valuation. | KEEP |
| _tangible_holder | Pass A: restoring a tangible field needs the dict directly holding the leaf key. Pass B: it is a structural accessor for baseline restore logic. | KEEP |
| _restore_tangible_field | Pass A: a rejected transaction's tangible fields must be restored (or removed when the baseline never had them) for the revert to be exact. Pass B: restoring a saved baseline is fail-closed durability, not a new reward decision. | KEEP |
| _turn_added_tangibles | Pass A: collision handling must know whether the turn actually added tangibles or only shrank them. Pass B: it is a comparison predicate against the baseline. | KEEP |
| _reapply_tangible_spend | Pass A: after a baseline restore, the losing turn's own subtractions must be re-applied, or spends would be silently refunded. Pass B: re-applying the turn's own recorded subtractions preserves the player's own actions during a revert, which is transaction integrity. | KEEP |
| restore_tangible_reward_baseline | Pass A: rejected or collided reward transactions need their reward-bearing fields reset to baseline, or rejected rewards would persist. Pass B: resetting to a saved baseline is anti-cheat transaction integrity, not a recomputed reward. | KEEP |
| _sync_authored_xp_fields | Pass A: supplied and stored XP representations can drift, and syncing them keeps the sheet consistent. Pass B: it mirrors XP across representations the sheet already carries, but legacy-alias mirroring should sunset with the aliases, so keep canonical sync and delete alias sync. | ADAPT |
| _clamp_xp_to_allowance | Pass A: requested XP beyond pre_xp plus tier allowance must be bounded, or unreceipted XP could inflate without limit. Pass B: clamping to a server capacity allowance is bounded capacity, and it preserves a nonzero remainder rather than zeroing (a zero clamp would be a rejection in disguise). | KEEP |
| clamp_reward_event_to_allowance | Pass A: invalid or unreceipted reward events need clamping to allowance instead of being discarded outright, preserving the turn. Pass B: it is the public allowance-clamp entry point, inheriting the capacity verdict above. | KEEP |
| restore_collision_reward_views | Pass A: after withholding a source replay, the accepted transaction's views must be projected, or the UI would show the replayed award. Pass B: projecting accepted (already-validated) transaction state is a read of server-owned records, not a new award. | KEEP |
| snapshot_raw_reward_event | Pass A: validation must work on a deep copy of the raw receipt so validation itself cannot mutate the model's output. Pass B: copying is transport hygiene for the validation boundary. | KEEP |
| _admit_model_reward_event | Pass A: admitted receipts must be recorded for both the streaming and non-streaming paths, or one path would lose receipts. Pass B: admitting a validated receipt into server state is durable-write bookkeeping. | KEEP |
| _authored_positive_gained | Pass A: gates need to know whether raw_gained parses as strictly positive before treating it as a gain. Pass B: it is a parsing predicate, not a valuation. | KEEP |
| _sync_admin_xp_update | Pass A: an explicit administrative absolute XP update must reach every XP alias, or the admin correction would be partial. Pass B: syncing an operator-directed absolute value is the God Mode product promise applied to XP, with the operator (not the server) authoring the value. | KEEP |
| capture_and_validate_reward_event | Pass A: the state-update boundary needs one function that captures, validates, and server-stamps a reward_event in place. Pass B: stamping a validated receipt is durable-write plus authorization, and it never sizes the reward itself. | KEEP |
| _reward_display_inventory_item_name / _reward_display_inventory_counts / _reward_display_loot_delta / _reward_display_gold | Pass A: reward display panels need item names, counts, loot deltas, and canonical gold, but all four are derivable by the model or the client from the validated receipt. Pass B: display derivation alone never justifies a field-aware transform, so these display helpers delete with the display projector below. | DELETE |
| project_reward_display_from_receipt | Pass A: the backend-only RewardDisplay view-model is convenient, but the client can render the same panel from the validated receipt, so nothing player-essential breaks. Pass B: projecting a display view-model from a receipt is display formatting, which strict ZFC does not allow as a server transform. | DELETE |
| admit_reward_event_for_state_update | Pass A: the state-update boundary needs admission plus validation plus adjustment in one call, or receipts would bypass checks on one path. Pass B: it is the authorization boundary for receipts, inheriting the receipt-validation verdict. | KEEP |
| _is_pending_level_up_modal_activation | Pass A: modal entry must distinguish a legitimate pending activation from a stale flag, or stale flags would open the modal. Pass B: it tests server-owned modal fields against pending evidence, which is routing on explicit state. | KEEP |
| _has_level_up_modal_structure | Pass A: callers need proof from server-owned modal fields that a modal actually exists before treating a turn as in-modal. Pass B: it is a structural predicate on server-owned fields. | KEEP |
| should_clear_false_positive_level_up_flags | Pass A: stale false-positive flags must be clearable only when the pre-response state was not already inside the modal, or real modals would be cleared. Pass B: it is a routing predicate on saved state, not a domain recompute. | KEEP |
| LEVEL_UP_CHOICE_IDS / LEGACY_STALE_LEVEL_UP_CHOICE_IDS / LEVEL_UP_ENTRY_CHOICE_IDS / ASI_CHOICE_IDS / LEVEL_UP_CHOICE_TYPES | Pass A: choice recognition needs the exact id vocabularies (current, legacy-stale, entry, ASI, types) to route clicks correctly. Pass B: closed vocabularies of explicit choice ids are the explicit-signal contract, not inference. | KEEP |
| is_level_up_choice_identifier | Pass A: recognizing exact compatibility handles without interpreting opaque ids keeps routing precise. Pass B: it is an exact-vocabulary membership test, the strictest form of explicit-signal routing. | KEEP |
| is_level_up_choice | Pass A: callers need to read explicit choice semantics, including exact legacy handles, for modal routing. Pass B: it reads explicit ids and types, granting no permission by itself. | KEEP |
| is_level_up_review_choice | Pass A: the review pair must be readable as a pair without granting entry permission. Pass B: it reads the exact model-authored review pair and explicitly grants nothing, which is routing discipline. | KEEP |
| is_level_up_review_doorway | Pass A: doorway detection must work regardless of what else a choice carries. Pass B: it tests one explicit choice property, not the choice's meaning. | KEEP |
| _find_choice_in_block | Pass A: choice lookup needs a single-block search by id. Pass B: it is a structural search on explicit ids. | KEEP |
| _lookup_planning_choice_by_id | Pass A: resolving a click needs the choice dict from the persisted planning block, not from the current turn's possibly-stale block. Pass B: looking up an explicit id in persisted state is authorization input for click routing. | KEEP |
| _planning_choice_items | Pass A: several predicates need (id, choice) pairs from a planning block in one place. Pass B: it is a structural iterator over explicit ids. | KEEP |
| saved_level_up_choice_id_for_text | Pass A: submitted rendered text currently resolves to a saved control id, but clients can submit the id directly, so the text path is not load-bearing. Pass B: matching free text to a saved control's rendered text is fuzzy text matching, which the pilot's explicit-signals-only rule rejects — slim it to explicit id submission and delete the text-matching branch. | ADAPT |
| resolves_to_level_up_entry | Pass A: a clicked choice id must resolve against the persisted planning block to authorize modal entry. Pass B: it is explicit-id resolution against persisted evidence, which is authorization routing. | KEEP |
| backfill_rewards_box_new_level | Pass A: a genuine committed level change should be visible as new_level in the box, but the session projector can emit it from the committed grant. Pass B: mutating the box post-hoc to backfill a display field is a display transform, so move it to the session projector and delete the backfill. | ADAPT |
| _normalize_inconsistent_rewards_box_level_aliases | Pass A: inconsistent level aliases in a box are confusing, but the box should carry one canonical level from the session, not server-normalized aliases. Pass B: normalization alone never justifies a field-aware transform, so delete it and let the projector emit a single canonical level. | DELETE |
| strip_fabricated_rewards_box_new_level | Pass A: completion aliases unsupported by a saved level change must be removable, or fabricated completions would render as real. Pass B: removing aliases that no saved grant supports is anti-fabrication authorization, not a recomputation. | KEEP |
| _total_character_level | Pass A: multiclass totals are currently computed server-side, but the model authors class levels and can author the total in its sheet. Pass B: summing class levels recomputes a model-owned derived value with no named necessary exception, so it deletes. | DELETE |
| _extract_xp_robust | Pass A: XP extraction must tolerate alias shapes, and delegating to the canonical game_state helper keeps one extraction rule. Pass B: it delegates to a read helper, adding no computation of its own. | KEEP |
| _coerce_nested_mapping | Pass A: dict-like inputs must coerce to dicts safely for downstream code. Pass B: it is a shape coercion for transport, reading no domain meaning. | KEEP |
| _anchor_rewards_box_xp | Pass A: a box's current_xp and xp_total currently get anchored to the accepted sheet, which hides model/box disagreement instead of surfacing it. Pass B: re-anchoring model box values to the sheet is a field-aware overwrite, so keep only the integrity case (box XP contradicting the persisted sheet gets flagged, not silently rewritten) and delete routine re-anchoring. | ADAPT |
| _PROGRESS_PERCENT_ABS_TOLERANCE_PP / _PROGRESS_PERCENT_REL_TOLERANCE_FRAC / _PROGRESS_PERCENT_MIN_ABS_DIFF_FOR_REL | Pass A: progress cross-checks need tolerances, but the cross-check itself deletes (below), so its tolerances have no remaining use. Pass B: they inherit the DELETE of the recompute they parameterize. | DELETE |
| _calculate_canonical_expected_progress | Pass A: expected progress percent under canonical D&D 5e progression is currently server-computed, but the model can author progress_percent in its signal under the schema. Pass B: computing expected progress from XP recomputes a model-owned derived value, which is the T1 delete target. | DELETE |
| _cross_check_progress_percent_against_xp | Pass A: the cross-check re-derives progress_percent from anchored XP when the model echo disagrees, but disagreement should be flagged to the model, not silently corrected. Pass B: re-deriving a model value and overwriting the echo is exactly the second-guessing strict ZFC deletes. | DELETE |
| _pick_first_present / _coerce_model_int / _coerce_model_optional_int / _coerce_model_optional_percent / _coerce_model_optional_floor / _coerce_flag_or_none | Pass A: model payloads need safe first-present and typed coercion helpers, or malformed payloads would crash signal handling. Pass B: these are boundary parsing helpers that preserve explicit values (including explicit zero) and never invent a domain value. | KEEP |
| is_level_up_audit_active | Pass A: callers need to know whether a pending repair accompanies the next action. Pass B: it is a predicate on saved audit state. | KEEP |
| _session_transition_is_actionable | Pass A: session transitions must be actionable only on explicit evidence, or stale sessions would drive routing. Pass B: it tests explicit session evidence, not derived XP facts. | KEEP |
| _format_model_progress_percent | Pass A: progress percent within the current level span is currently server-formatted, but the model can author it in its signal. Pass B: computing a percentage from level-span arithmetic is display recomputation, which deletes. | DELETE |
| _model_level_transition_is_actionable | Pass A: routing needs to know when explicit model/state fields name a future target level. Pass B: it tests explicit fields only, deriving no transition from XP. | KEEP |
| _pending_level_up_transition_is_actionable | Pass A: pending transitions need a routing wrapper so callers share one actionability test. Pass B: it delegates to explicit-evidence checks, adding no derivation. | KEEP |
| _canonical_pending_level_up_transition | Pass A: callers need persisted canonical pending evidence as a (current, target) pair. Pass B: it reads persisted evidence (with a session fallback) without deriving a transition from XP. | KEEP |
| _session_available_fallback (nested in _canonical_pending_level_up_transition) | Pass A: when canonical evidence is absent, the session fallback supplies the pair from saved session facts. Pass B: it reads saved session facts, not XP-derived facts. | KEEP |
| rewards_box_level_transition_is_actionable | Pass A: a current model rewards box that opens a future level transition must be recognizable for routing. Pass B: it tests the box's explicit transition fields, not XP thresholds. | KEEP |
| _level_up_signal_can_use_rewards_box_xp_evidence | Pass A: same-turn rewards currently fill missing signal XP evidence, but a signal missing XP should be rejected or completed by the model, not backfilled. Pass B: filling signal XP from another artifact synthesizes signal evidence, so require the signal to carry its own XP and delete the backfill branch. | ADAPT |
| _normalize_level_up_signal_payload | Pass A: legacy and canonical signal field names must map to one contract for downstream code. Pass B: alias mapping is normalization, so move the canonical names into the response schema and keep this only as a compat shim until legacy signals drain, then delete it. | ADAPT |
| _reject_malformed_normalized_lus | Pass A: malformed normalized signals need a short rejection reason for fail-closed handling. Pass B: returning a reason (not a corrected signal) is validation, not authorship. | KEEP |
| canonicalize_level_up_signal | Pass A: model-emitted signals need canonical fields for the user-facing contract, but the canonical contract is the response schema's job. Pass B: canonicalizing field names and display fields is normalization, so move it into the schema and keep only a validation wrapper, deleting the rewrite branches. | ADAPT |
| public_level_up_signal_contract | Pass A: persistence and polling need the minimal public signal contract (current/target plus evidence) in one place. Pass B: projecting the minimal contract from an accepted signal is a read projection of model facts, not a recomputation. | KEEP |
| _hydrate_level_up_signal_xp | Pass A: the formatter currently reads XP hydrated from elsewhere into the signal, but the signal must carry its own XP or be rejected. Pass B: copying XP from another artifact into the signal synthesizes signal evidence, so delete the hydration and require signal-carried XP. | DELETE |
| format_model_level_up_signal | Pass A: the signal is currently formatted into UI payloads server-side, but the client can render the accepted signal directly. Pass B: formatting a model signal into UI payloads (including computed fields over ~300 lines) is display recomputation, so delete it and let the UI render the signal contract. | DELETE |
| _pending_rewards_from_canonical_signal | Pass A: compatibility pending state is currently built from accepted signal fields, but pending state should be the session record itself. Pass B: building a compat pending object from accepted fields is legacy synthesis, so sunset it with the legacy pending shape. | ADAPT |
| _LEVEL_MUTATION_AUTHORIZED_MODES | Pass A: level-mutation authorization needs the set of modes that can authorize, or every mode would be suspect. Pass B: it is a vocabulary constant for authorization. | KEEP |
| _pre_turn_character_creation_concluded | Pass A: authorization must know whether the pre-turn state already carries the server's CC exit stamp, or concluded creations could be re-entered. Pass B: it tests a server stamp, which is server-owned evidence. | KEEP |
| cc_authorized_level_write | Pass A: character-creation level writes need scoped authority (concluded pre-turn state plus an explicit write), or any turn could rewrite creation levels. Pass B: it is authorization scoped to explicit evidence, not a level computation. | KEEP |
| _is_authorized_level_up_finish_release | Pass A: finish releases must be recognized only for a server-recognized active modal finish, or stray finishes could release sessions. Pass B: it tests explicit modal-finish evidence, which is authorization routing. | KEEP |
| _is_authorized_level_up_signal_backed_grant | Pass A: this legacy compatibility check claims no authority beyond valid PCD evidence, so it adds no gate its callers do not already have. Pass B: a check that explicitly grants no authority is redundant authorization theater, so delete it and rely on the PCD-evidence checks directly. | DELETE |
| _is_authorized_pcd_progression_grant | Pass A: PCD progression grants need a check that canonical PCD explicitly advances level while retaining or raising XP. Pass B: it tests explicit PCD facts (level advance plus XP non-regression), which is authorization, not a level computation. | KEEP |
| _POOL_MAX_KEYS / _POOL_REMAINING_KEYS | Pass A: pool revert logic needs the max and remaining key vocabularies. Pass B: they are vocabulary constants for revert logic. | KEEP |
| _is_number | Pass A: pool revert needs a numeric predicate that excludes bools. Pass B: it is a type predicate for validation. | KEEP |
| _revert_pool_maximum / _revert_pool_entry / _revert_resource_pool / _revert_level_scaled_sheet_fields / _revert (nested) / _restore_rejected_pcd_transaction | Pass A: a rejected crossing must have its pool maxima, pool entries, and level-scaled sheet fields undone while keeping its spends, or reverts would be partial. Pass B: undoing a rejected transaction to the saved baseline is anti-cheat transaction integrity, and keeping spends preserves the player's own actions. | KEEP |
| block_unauthorized_level_mutations | Pass A: unauthorized level and session mutations must be hard-blocked before merge, or model overreach would persist. Pass B: blocking mutations that lack authorization is the anti-cheat core, explicitly kept by §6, and it never authors a level itself. | KEEP |
| block_unauthorized_level_mutation_deltas | Pass A: partial deltas need the same block before merge, or a mutation could sneak in as a fragment. Pass B: it is the delta-level form of the same authorization block. | KEEP |
| _coerce_state_mapping | Pass A: GameState-like inputs must normalize to plain mappings for the authorization checks. Pass B: it is shape coercion for transport, reading no domain meaning. | KEEP |
| _has_unapplied_xp_threshold_crossing | Pass A: migration callers still use this alias for explicit unapplied transition evidence. Pass B: it aliases an explicit-evidence check, so it inherits that check's verdict and adds no XP-threshold derivation despite its name. | KEEP |
| authorize_level_up_entry | Pass A: modal entry must be authorized from explicit model/session transition evidence, or any turn could enter the modal. Pass B: it is authorization on explicit evidence, with no XP-derived entry. | KEEP |
| level_up_pending_has_reward_payload | Pass A: pending records with gold or items still to award must be distinguishable from empty pendings. Pass B: it is a payload-presence predicate on saved records. | KEEP |
| _positive (nested in level_up_pending_has_reward_payload) | Pass A: reward presence needs a positivity test for values. Pass B: it is a local predicate with no domain effect of its own. | KEEP |
| is_stale_rewards_pending | Pass A: stale rewards_pending records must be recognizable so they can be cleared instead of paid. Pass B: it compares saved pending facts against current state, which is staleness authorization. | KEEP |
| is_level_up_active | Pass A: routing needs to know when a pending grant audit actually needs input. Pass B: it is a predicate on saved audit state. | KEEP |
| is_level_up_transition_actionable | Pass A: callers need a public actionability test for pending transitions. Pass B: it tests explicit pending evidence, not derived thresholds. | KEEP |
| pending_level_up_target_level | Pass A: callers need the target level of a currently-pending, not-yet-granted transition. Pass B: it reads the pending target from saved evidence without computing it. | KEEP |
| contains_mapping_shape | Pass A: candidates must be checkable for preserving every nested mapping key in a required shape. Pass B: it is a structural predicate for validation. | KEEP |
| substitute_level_up_target | Pass A: level_up_now prompt text carries a {target_level} placeholder that must be filled for display. Pass B: placeholder substitution is prompt templating, so move the placeholder into the prompt template itself and delete this server-side string surgery. | ADAPT |
| clear_stale_level_up_complete_flags | Pass A: stale complete flags must clear when new XP is earned or the expected-level condition is met, or completed UI would linger. Pass B: clearing stale flags on explicit new evidence is state-machine hygiene keyed to saved state. | KEEP |
| clear_level_up_lock_flags | Pass A: obsolete lock flags must be removable from a full state dict, or locks would persist past their transitions. Pass B: removing obsolete flags is state hygiene, not a grant decision. | KEEP |
| resolve_level_up_signal | Pass A: callers need an explicit model/session transition without any XP-derived fallback. Pass B: it returns explicit evidence only, which is the strict-ZFC-correct form of signal resolution. | KEEP |
| ensure_rewards_box | Pass A: polling and display paths need a rewards box built from persisted model-owned evidence when no fresh model output exists. Pass B: projecting an already-accepted evidence record is a read projection of durable state (the same basis as project_level_up_ui), not a newly authored reward. | KEEP |
| ensure_planning_block | Pass A: legacy display needs a planning-block shell when none exists, without authoring choices. Pass B: it builds an empty shell and authors no choices, so it is display scaffolding, not choice injection. | KEEP |
| normalize_rewards_box | Pass A: rewards boxes need clean booleans and coerced ints in one place, or downstream code would diverge on types. Pass B: bool/int coercion is boundary typing, but any value synthesis inside it must go, so keep the typing and delete synthesis branches. | ADAPT |
| _coerce_rewards_box_xp_gained | Pass A: xp_gained needs safe coercion at the box boundary. Pass B: it is a typed parsing helper that never invents a gain. | KEEP |
| synthesize_rewards_box_from_state | Pass A: a non-level rewards box is currently constructed from authoritative state XP delta, but the model can author that box in its turn output. Pass B: constructing a rewards box from an XP delta invents reward presentation from a derived delta, which is the model-values synthesis strict ZFC deletes. | DELETE |
| resolve_canonical_progress_fields | Pass A: synthesized boxes currently need canonical D&D progress fields, but those fields belong in the model-authored signal. Pass B: computing canonical progress fields server-side recomputes model-owned derived values, so it deletes with the synthesis it serves. | DELETE |
| _raw_rewards_box_level_up_is_actionable | Pass A: raw boxes need an actionability test before they drive routing. Pass B: it tests explicit box fields, not derived thresholds. | KEEP |
| _active_modal_rewards_box_from_signal_or_state | Pass A: in-modal display needs the active box from signal or persisted state. Pass B: it selects between two explicit evidence sources without computing a new box. | KEEP |
| _is_positive_reward_value | Pass A: reward visibility needs a positivity test for values. Pass B: it is a value predicate, not a valuation. | KEEP |
| should_show_rewards_box | Pass A: one visibility decision must replace scattered checks in world_logic and app.js, or visibility would diverge. Pass B: it gates display on explicit box and state facts, which is UI routing on saved evidence, not reward authorship. | KEEP |
| _reward_values_match | Pass A: dedup needs to know whether two raw reward values are the same persisted award. Pass B: it is an equality predicate for dedup, not a valuation. | KEEP |
| _raw_rewards_box_looks_like_stale_echo | Pass A: stale echoes of older reward state must be detectable without a current state delta, or they would re-render as new rewards. Pass B: it detects staleness by comparing against saved state, which is authorization-adjacent hygiene. | KEEP |
| scrub_stale_rewards_from_older_entries | Pass A: history entries carrying duplicate stale rewards_box echoes must be cleaned, or history would show the same reward repeatedly. Pass B: removing duplicate stale echoes from display entries is history hygiene keyed to persisted state, not a new award decision. | KEEP |
| sanitize_rewards_state_for_context | Pass A: transient rewards must be removed from client/LLM-facing state copies, or the next prompt would see stale reward state. Pass B: stripping transient fields from a context copy is prompt hygiene and transport, and it never touches persisted state. | KEEP |
| extract_planning_choice_ids | Pass A: callers need the set of choice ids from a planning block for routing and dedup. Pass B: it is a structural extraction over explicit ids. | KEEP |
| enforce_rewards_box_planning_atomicity | Pass A: the rewards_box/planning_block pair must be audited as an atomic modal envelope, or half-pairs would render broken modals. Pass B: auditing a pair's consistency and enforcing the modal envelope is authorization of the UI contract, not authorship of either half. | KEEP |
| planning_has_level_up_review_choice | Pass A: opt-in review doorways must be readable without inferring authorization or clock ownership. Pass B: it reads explicit doorway choices only, which is routing discipline. | KEEP |
| project_level_up_review_choice | Pass A: the review doorway is currently added server-side on the grant turn, but the grant turn's prompt/schema can carry the doorway itself. Pass B: server-side choice injection is the banned pattern unless a registered spec rescues it, and the rescuing spec (level_up_review.project_doorway_when_missing, MISSING_INSTRUCTION) is itself a prompt gap, so move the doorway into the prompt/schema and keep server injection only as an interim. | ADAPT |
| planning_has_level_up_choices | Pass A: modal routing needs to know whether a block contains a valid level-up control surface. Pass B: it tests explicit choice ids and types, not semantics. | KEEP |
| planning_has_time_freezing_level_up_choices | Pass A: time-freezing controls own the turn's clock, so routing must recognize them distinctly. Pass B: it tests explicit control types, which is routing. | KEEP |
| planning_has_advanced_level_up_choice | Pass A: routing must distinguish an active modal beyond stale entry buttons. Pass B: it tests explicit choice evidence beyond stale handles. | KEEP |
| _inject_levelup_choices_if_needed | Pass A: authored choices and the unresolved legacy banner shape must be preserved when injecting, or legacy UI would lose its banner. Pass B: preserving authored choices is correct, but the legacy-banner preservation is compat work, so slim it to authored-choice preservation and delete the legacy banner branch. | ADAPT |
| _apply_contradiction_guard | Pass A: deterministic integrity checks on a model-owned signal catch contradictions before they persist, but contradictions should be schema violations the model fixes. Pass B: server-side contradiction checks second-guess the model signal, so move the checks into schema validation and delete the guard's rewrite branches. | ADAPT |
| TURN_CLASS_SEALED_GRANT / TURN_CLASS_AMEND_RESEAL / TURN_CLASS_MID_REVIEW / TURN_CLASS_STALE_FINISH / TURN_CLASS_NOT_LEVEL_UP | Pass A: turn classification needs stable class labels across the classifier and its callers. Pass B: they are vocabulary constants for routing. | KEEP |
| LevelUpTurnClassification (NamedTuple) / active_context (method) | Pass A: classification results need a typed record plus a predicate for whether a turn is one correction guards must not treat as stale. Pass B: the record carries classifier output and the predicate reads its own fields, neither computing a domain value. | KEEP |
| classify_level_up_turn | Pass A: level-up turns need a single authoritative classification, or guards and routers would diverge. Pass B: it classifies on explicit session, signal, and choice evidence (not XP inference), which is routing. | KEEP |
| _box_target_is_open_session_review | Pass A: a box whose target is exactly the open session's review transition must be recognizable for review routing. Pass B: it compares explicit box and session targets. | KEEP |
| _canonicalize_core | Pass A: this is the convergence point where every rewards path lands, so deleting it outright would break all rewards UI. Pass B: its session-backed projection and fail-closed authorization stay, but its synthesis branches (building boxes from deltas), suppression branches (dropping model boxes on stale guesses), and progress recomputation must be deleted and their contracts moved to prompt/schema — hence ADAPT with that exact split, not a blanket keep. | ADAPT |
| _MISSING (sentinel) | Pass A: canonical-pair snapshots need a missing marker distinct from None. Pass B: it is an internal sentinel with no domain effect. | KEEP |
| _snapshot_canonical_pair / _capture (nested) / _restore_canonical_pair / _restore (nested) / _write_canonical_field / _writeback_canonical_pair / _canonical_persistence_state_changed / _changed (nested) | Pass A: canonical persistence needs snapshot, rollback, single-field write, writeback to both state and session, and change detection, or partial persistence would corrupt the pair. Pass B: these are durable-write mechanics operating on already-accepted canonical fields, with no value synthesis. | KEEP |
| _clear_orphan_level_up_meta | Pass A: accepted level-up meta with no landed session must be dropped fail-closed, or orphan meta would drive phantom UI. Pass B: dropping unlanded meta is fail-closed cleanup keyed to the reducer's own landing result. | KEEP |
| _strip_post_finish_level_up_choices | Pass A: once a response seals the review, stale in-modal choices must be stripped, or the sealed review could be re-entered. Pass B: stripping choices after a sealed finish is state-machine hygiene keyed to server-owned session state. | KEEP |
| _is_stale (nested in _strip_post_finish_level_up_choices) | Pass A: post-finish stripping needs a staleness test per choice. Pass B: it tests explicit choice state against the sealed finish, not semantics. | KEEP |
| _strip_orphan_level_up_choices | Pass A: level-up controls with no backing session must be stripped while model-owned story choices are kept. Pass B: stripping unbacked controls is authorization hygiene (controls require a session), and keeping story choices shows it does not over-strip. | KEEP |
| _is_orphan_control (nested in _strip_orphan_level_up_choices) | Pass A: orphan stripping needs a per-control test for session backing. Pass B: it tests explicit backing evidence. | KEEP |
| _detect_level_up_orphan_fail_closed | Pass A: orphaned crossings need a correction-only detector so they fail closed visibly instead of persisting. Pass B: detection without mutation is audit, and its fail-closed use is authorization. | KEEP |
| format_level_up_orphan_fail_closed_warning | Pass A: an orphaned crossing needs player-visible fail-closed text, or the player would see a silent failure. Pass B: rendering a server warning message is server communication, not a domain transform. | KEEP |
| format_level_xp_mismatch_warning | Pass A: explicit level/XP inconsistencies need player-visible warning text. Pass B: rendering a warning about explicit inconsistency is server communication, and it rewrites no values. | KEEP |
| _resolve_authored_level_up_intent | Pass A: the canonicalize path needs the turn's (signal, grant, unresolved-signal) triple in one place. Pass B: it reads model-authored intent verbatim, deriving no third value. | KEEP |
| canonicalize_rewards | Pass A: this is the public streaming and non-streaming entry point every rewards path calls, so outright deletion breaks all rewards UI. Pass B: like _canonicalize_core, it keeps session-backed projection and fail-closed authorization but must lose its synthesis, suppression, and progress-recompute branches to prompt/schema — ADAPT with the same named split. | ADAPT |
| _planning_block_has_explicit_freeze_time | Pass A: modal freezing must be recognized only when the model explicitly marks the block or choices as modal-frozen. Pass B: it tests an explicit freeze marker, which is the strict-correct form of freeze detection. | KEEP |
| project_level_up_ui / project_level_up_ui_locally (alias) | Pass A: the polling path has no current LLM output, so something must project the level-up UI from persisted canonical evidence. Pass B: projecting only persisted canonical evidence (no fresh model values, no synthesis) is a read of durable state, which is the sanctioned server role for polling. | KEEP |
| detect_rewards_discrepancy | Pass A: discrepancies must be reportable without marking delivery, or reporting would itself change delivery state. Pass B: it reports only, which is audit logging that §6 keeps. | KEEP |
| _detect_rewards_discrepancy (module alias) | Pass A: the alias is how some callers reference the discrepancy reporter. Pass B: it inherits the report-only verdict of the function it aliases. | KEEP |

## backend_adjustment_specs.py — file verdict: ADAPT (registry of interim exceptions, not a justification)

The file is data, not behavior: 89 `AdjustmentSpec` records plus grouping
tuples. Registry membership justifies nothing — each spec below is judged
on its own `allowed_when`. The pattern that emerges: AUDIT_ONLY specs and
stale-suppression/authorization specs mostly KEEP (they remove or gate,
never invent); normalization, display, and prompt-gap specs are ADAPT
(they are interim until prompt/schema carries the contract); synthesis
and recompute specs are DELETE (they invent model-owned values); the two
inactive specs are DELETE (they do nothing at runtime). Where a spec's
own graduation note says it dies at M2/M3 or when the model complies,
the verdict is ADAPT with that sunset, not a permanent KEEP.

| Spec (category / scope) | Pass A + Pass B justification | Verdict |
|---|---|---|
| level_up_badge.clear_when_state_proves_stale (SUPPRESSION / LEVEL_UP) | Pass A: a badge the persisted state proves stale would otherwise keep rendering a false level-up offer. Pass B: clearing only when state proves staleness removes a stale echo without inventing any value, which is hygiene keyed to durable state. | KEEP |
| level_up_ui.requires_canonical_pending_evidence (SUPPRESSION / LEVEL_UP) | Pass A: level-up UI without canonical pending evidence would be a phantom offer with no backing grant. Pass B: gating UI on persisted pending evidence is authorization of display by the durable record, not authorship. | KEEP |
| level_up_modal.pending_activation_flag_sync (CORRECTION / LEVEL_UP) | Pass A: modal activation flags can desync between top-level and nested homes, leaving the modal half-armed. Pass B: syncing flags is server-state bookkeeping, but mirroring a model flag into a server flag should narrow to server-owned flags only, so slim it to that case. | ADAPT |
| level_up_modal.top_level_false_blocks_nested_activation (SUPPRESSION / LEVEL_UP) | Pass A: a nested activation must not fire when the top-level flag is false, or the modal would open against an explicit off signal. Pass B: letting an explicit false win is fail-closed precedence for modal state, not a value judgment. | KEEP |
| level_up_routing.exit_suppresses_stale_character_creation_lock (SUPPRESSION / LEVEL_UP) | Pass A: exiting must release a stale character-creation lock, or the player would be trapped in creation after leaving it. Pass B: suppressing a stale lock on an explicit exit is state-machine cleanup keyed to an explicit signal. | KEEP |
| level_up_modal.server_enforces_finish_exit_state (CORRECTION / LEVEL_UP) | Pass A: the modal must reach a consistent finish-exit state when the finish signal arrives, or it would hang half-sealed. Pass B: enforcing exit state on an explicit finish signal is the modal state machine, rescued by the explicit-exit guarantee. | KEEP |
| level_up_modal.blocks_non_finish_state_release (SUPPRESSION / LEVEL_UP) | Pass A: non-finish releases must be blocked, or the modal could be released by an unrelated state change. Pass B: blocking release without an explicit finish is fail-closed gating on the explicit signal. | KEEP |
| character_creation_modal.finish_choice_normalization_and_affordance (CORRECTION / GENERAL) | Pass A: creation finish choices arrive in variant forms and need one canonical affordance to route. Pass B: normalizing choice forms and affordances is schema/display work, so move the canonical forms into the response schema and keep only the explicit-id routing on the server. | ADAPT |
| level_up_choice.expand_id_to_visible_text_context (CORRECTION / LEVEL_UP) | Pass A: backend choice ids need visible text in context for the model to reason about them, but the prompt can carry id-to-text mappings itself. Pass B: expanding ids into context text is context assembly, so move the mapping into the prompt and delete the server expansion. | ADAPT |
| level_up_rewards.pending_sync_and_synthesis (CORRECTION / LEVEL_UP) | Pass A: pending rewards must sync with the session, but the synthesis half builds pending values the model never authored. Pass B: keep the sync-to-session half (durable projection) and delete the synthesis half, letting the model author pending values via the signal. | ADAPT |
| level_up_rewards.clear_stale_pending_notification (SUPPRESSION / LEVEL_UP) | Pass A: a stale pending notification would keep nagging the player about a dead transition. Pass B: clearing a notification the persisted state proves stale removes an echo without inventing a value. | KEEP |
| level_up_rewards.block_complete_no_new_xp_retrigger (SUPPRESSION / LEVEL_UP) | Pass A: a completed grant must not retrigger when no new XP arrived, or the player would be re-offered a finished level-up. Pass B: blocking retrigger absent new evidence is anti-replay gating on explicit evidence. | KEEP |
| level_up_story.scrub_stale_history_level_up_ui (SUPPRESSION / LEVEL_UP) | Pass A: story history carrying stale level-up UI would re-render dead offers in the narrative stream. Pass B: scrubbing UI echoes the persisted state proves stale is history hygiene, not a narrative rewrite. | KEEP |
| level_up_story.project_canonical_pair_for_polling (CORRECTION / LEVEL_UP) | Pass A: polling has no fresh model output, so the canonical pair must be projected from persisted evidence. Pass B: projecting persisted evidence for polling is a durable read, the same sanctioned basis as project_level_up_ui. | KEEP |
| level_up_routing.unrelated_rewards_precede_modal_lock (CORRECTION / LEVEL_UP) | Pass A: unrelated rewards must be delivered before the modal lock engages, or they would be trapped behind the modal. Pass B: ordering delivery ahead of the lock is routing precedence, and it changes no reward's value. | KEEP |
| level_up_choice.classify_backend_choice_ids (AUDIT_ONLY / LEVEL_UP) | Pass A: backend choice ids need classification for audit trails, or audits could not tell backend ids from player clicks. Pass B: audit-only classification mutates nothing, so it is logging. | KEEP |
| level_up_signal.normalize_aliases_and_display_fields (CORRECTION / LEVEL_UP) | Pass A: legacy signal aliases must map to canonical names for downstream code, but the canonical names belong in the schema. Pass B: alias and display normalization is the normalization strict ZFC rejects as a permanent transform, so move it to the schema and keep this only as a draining shim. | ADAPT |
| level_up_signal.reject_malformed_payload (SUPPRESSION / LEVEL_UP) | Pass A: malformed signal payloads must be rejected rather than half-applied, or corrupt signals would drive grants. Pass B: rejecting malformed input is fail-closed validation, and it invents no replacement signal. | KEEP |
| level_up_signal.format_to_ui_pair (DEFAULT / LEVEL_UP) | Pass A: the UI pair is convenient, but the client can render the accepted signal contract directly. Pass B: formatting a model signal into a UI pair is display formatting, which alone never justifies a field-aware transform. | DELETE |
| level_up_pending.derive_from_canonical_signal (DEFAULT / LEVEL_UP) | Pass A: pending state currently derives from the canonical signal, but the session reducer already records pending transitions from signals. Pass B: a standalone derivation duplicates the reducer's job, so fold any remaining derivation into the session reducer and delete the standalone path. | ADAPT |
| level_up_state.block_unauthorized_model_mutations (CORRECTION / LEVEL_UP) | Pass A: unauthorized model mutations to level state must be blocked before merge, or model overreach would persist. Pass B: this is the authorization core (the same gate as block_unauthorized_level_mutations), explicitly server-owned. | KEEP |
| level_up_active.suppress_stale_pending_flags (SUPPRESSION / LEVEL_UP) | Pass A: stale pending flags would keep level-up UI live for dead transitions. Pass B: suppressing flags the persisted state proves stale removes echoes without inventing values. | KEEP |
| level_up_ui.project_from_persisted_pending (DEFAULT / LEVEL_UP) | Pass A: level-up UI must be projectable from persisted pending state for polling and refresh. Pass B: projecting persisted evidence is a durable read, not a new UI decision. | KEEP |
| level_up_rewards.suppress_stale_raw_rewards_echo (SUPPRESSION / LEVEL_UP) | Pass A: raw rewards echoes of older awards would re-render as new rewards if not suppressed. Pass B: suppressing an echo the persisted state proves stale is dedup hygiene, not a reward decision. | KEEP |
| level_up_context.strip_rewards_state_from_prompt (SUPPRESSION / LEVEL_UP) | Pass A: transient rewards state in the next prompt would make the model reason about stale rewards. Pass B: stripping transient fields from a context copy is prompt hygiene, and it never touches persisted state. | KEEP |
| level_up_atomicity.audit_rewards_planning_pair (AUDIT_ONLY / LEVEL_UP) | Pass A: the rewards/planning pair needs an audit record, or atomicity violations would be invisible. Pass B: audit-only recording mutates nothing, so it is logging. | KEEP |
| level_up_core.suppress_stale_target_ui (SUPPRESSION / LEVEL_UP) | Pass A: UI for a stale target level would offer a transition the character already passed. Pass B: suppressing UI the persisted level proves stale removes an echo without inventing a target. | KEEP |
| level_up_core.enrich_missing_xp_evidence (DEFAULT / LEVEL_UP) | Pass A: missing XP evidence currently gets enriched server-side, but a signal missing XP should be completed by the model or rejected. Pass B: enriching evidence invents the very XP facts the signal was supposed to carry, so it deletes. | DELETE |
| level_up_pending.normalize_legacy_xp_alias (CORRECTION / LEVEL_UP) | Pass A: legacy XP aliases in pending state must map to the canonical alias for readers. Pass B: alias normalization is legacy compat, so keep it only until legacy pendings drain, then delete it with the aliases. | ADAPT |
| level_up_validation.flag_xp_level_mismatch (CORRECTION / LEVEL_UP) | Pass A: XP/level mismatches must be flagged, or inconsistent grants would pass silently. Pass B: flagging (not correcting) a mismatch is audit, since it rewrites neither XP nor level. | KEEP |
| level_up_rewards.synthesize_primary_rewards_box (DEFAULT / LEVEL_UP) | Pass A: the primary rewards box is currently synthesized server-side, but the model can author it in its turn output under the schema. Pass B: synthesizing a rewards box invents model-owned reward presentation, which is the T1 delete target. | DELETE |
| level_up_rewards.suppress_unpaired_pending_box (SUPPRESSION / LEVEL_UP) | Pass A: a pending box with no paired planning block would render a half-modal. Pass B: suppressing an unpaired box is modal-envelope enforcement, not a value decision. | KEEP |
| level_up_rewards.defer_box_on_rejected_crossing_grant (SUPPRESSION / LEVEL_UP) | Pass A: a box for a rejected crossing grant must be deferred, or a rejected grant would still render as an offer. Pass B: deferring on a reducer rejection is fail-closed handling keyed to the reducer's own verdict. | KEEP |
| level_up_modal.clear_stale_pending_when_inactive (SUPPRESSION / LEVEL_UP) | Pass A: inactive modals must not leave pending flags behind, or the next turn would inherit a dead pending. Pass B: clearing pending flags when the modal is provably inactive removes stale state without inventing any. | KEEP |
| level_up_ui.reconcile_story_pair (CORRECTION / LEVEL_UP) | Pass A: story and UI pairs can diverge across representations, but one projector should own the pair instead of a reconcile pass. Pass B: reconciling two representations is normalization across views, so fold it into the single session projector and delete the standalone reconcile. | ADAPT |
| level_up_canonicalize.persist_canonical_pair (CORRECTION / LEVEL_UP) | Pass A: the canonical rewards/planning pair must be persisted, or polling and refresh would have nothing to read. Pass B: persisting already-accepted canonical fields is a durable write, not a new decision. | KEEP |
| level_up_false_positive.clear_modal_flags (SUPPRESSION / LEVEL_UP) | Pass A: false-positive modal flags must be clearable, or a contradicted detection would trap the player in a modal. Pass B: clearing flags on a proven false positive removes stale state keyed to detection evidence. | KEEP |
| level_up_response.reconcile_unified_response (CORRECTION / LEVEL_UP) | Pass A: unified responses currently need reconciliation across streaming and non-streaming shapes, but one canonical shape should be enforced at the schema. Pass B: reconciling representations is normalization, so enforce a single shape in the schema and delete the reconcile pass. | ADAPT |
| level_up_polling.project_latest_ui (CORRECTION / LEVEL_UP) | Pass A: polling needs the latest UI projected from persisted state, since no fresh model output exists on a poll. Pass B: projecting persisted evidence is a durable read, the sanctioned polling basis. | KEEP |
| level_up_parser.raw_planning_preserve (CORRECTION / LEVEL_UP) | Pass A: the raw planning block must be preserved through parsing, or parser normalization could destroy model-authored choices. Pass B: preservation is the opposite of transformation — it keeps the model's own output intact — so it stays. | KEEP |
| level_up_parser.custom_action_fallback (DEFAULT / LEVEL_UP) | Pass A: custom actions currently fall back server-side when unrecognized, but the prompt/schema should define custom-action handling. Pass B: a fallback that supplies behavior the model did not author is interim prompt-gap coverage, so move it to prompt/schema and delete the server fallback. | ADAPT |
| level_up_schema.normalize_planning_choice_shape (CORRECTION / LEVEL_UP) | Pass A: planning choice shapes vary, but the response schema can enforce one shape at the source. Pass B: shape normalization belongs in the schema, so move it there and delete the server normalizer. | ADAPT |
| level_up_context.initial_story_drops_signal (SUPPRESSION / LEVEL_UP) | Pass A: the initial story must not carry a level-up signal, or a fresh campaign would start with a phantom transition. Pass B: dropping a signal from a context where it cannot belong is prompt hygiene, and it touches no persisted grant. | KEEP |
| conclude.reconcile_derived_stats (CORRECTION / GENERAL) | Pass A: conclude turns need derived-stats telemetry to prove the conclude prompt holds in prod. Pass B: the implementation (conclude_invariant) is warn-only and never mutates, so this spec names a logging exception, not a transform — the one spec here whose correction category overstates its runtime effect. | KEEP |
| level_up_amend.backfill_rewards_box_new_level (CORRECTION / LEVEL_UP) | Pass A: amended grants need new_level visible in the box, but the session projector can emit it from the committed grant. Pass B: it inherits the ADAPT of backfill_rewards_box_new_level: move emission to the projector and delete the backfill. | ADAPT |
| parse_fail_open.fallback_planning_block (DEFAULT / GENERAL) | Pass A: a parse failure currently falls back to a planning block so the turn survives, but the fallback shape should be schema-defined. Pass B: supplying a fallback block is interim parse-gap coverage, so define the fallback in the schema/parser contract and delete the ad-hoc server fallback. | ADAPT |
| parse_recovery.escape_unescaped_string_quotes (CORRECTION / GENERAL) | Pass A: unescaped quotes in model JSON would otherwise fail parsing and lose the whole turn. Pass B: escaping quotes is JSON syntax recovery, not semantic rewriting — it restores the model's own intended string, so it is structural parse transport. | KEEP |
| world_time.partial_merge_preserves_canonical_time (CORRECTION / GENERAL) | Pass A: a partial world_time update lacking date fields must not clobber the persisted year/month/day, or time would regress. Pass B: preserving persisted canonical time across a partial merge is durable-write integrity for a server-persisted record. | KEEP |
| session_header.timestamp_repair_from_canonical_world_time (CORRECTION / GENERAL) | Pass A: a session header timestamp inconsistent with canonical world time must be repairable, or headers would lie about when events happened. Pass B: repairing a server-owned header from the persisted canonical clock record is server-record integrity, not narrative authorship. | KEEP |
| rewards_box.progress_percent_xp_anchor (CORRECTION / REWARDS) | Pass A: progress percent currently anchors to XP server-side, but the model can author progress_percent in its signal under a required schema field. Pass B: anchoring a display percent to XP recomputes a model-owned derived value, so it deletes. | DELETE |
| location.legacy_location_fallback_in_resolve_location (CORRECTION / GENERAL) | Pass A: legacy location resolution falls back to old fields, but legacy campaigns are the only users and the model can supply location directly. Pass B: a legacy fallback is compat, not a necessary exception, so delete it with the legacy location shapes. | DELETE |
| location.prior_location_preservation_when_model_omits_location (CORRECTION / GENERAL) | Pass A: when the model omits location, preserving the prior location keeps the player from teleporting, but the schema should require location instead. Pass B: omission handling belongs in the schema as a required field, so keep preservation only as an interim and delete it once location is schema-required. | ADAPT |
| location.session_header_fallback_generation (DEFAULT / GENERAL) | Pass A: a location is currently generated from the session header when the model omits one, but generation invents a location the model never authored. Pass B: generating a domain fact from a header is server authorship with no named necessary exception, so it deletes. | DELETE |
| location.early_metadata_deriving_location_confirmed_from_header (CORRECTION / GENERAL) | Pass A: early metadata currently derives location_confirmed from the header, which is useful only when that header is server-stamped. Pass B: deriving from a server-stamped header is server-record reading, but deriving from a model-echoed header would be authorship, so narrow it to stamped headers only and delete the rest. | ADAPT |
| combat_end.defeated_enemy_cleanup (CORRECTION / GENERAL) | Pass A: defeated enemies must leave combat tracking, but the model's combat updates should already remove them under the combat contract. Pass B: server cleanup of a model-ignored instruction is interim prompt-gap coverage, so require the removal in the combat schema and delete the server cleanup. | ADAPT |
| combat_end.nonlethal_combatant_removed_from_tracking (CORRECTION / GENERAL) | Pass A: nonlethally resolved combatants must leave tracking just like defeated ones, but again the combat contract should require it. Pass B: it inherits the ADAPT of the defeated-enemy cleanup: move the removal into the combat schema and delete the server pass. | ADAPT |
| ADJ-WA-JSON-STRIP-PREFIX (CORRECTION / GENERAL) | Pass A: Gemini's [Mode: ...] prefixes break JSON parsing outright, and without stripping, half of prefixed turns would fail to parse. Pass B: stripping a declared structured prefix before JSON parsing is transport (the same class as CHOICE: parsing), backed by a committed proof artifact and a disk-provenance gate, so this is a proven structural exception. | KEEP |
| world_time.partial_merge_date_protection (CORRECTION / GENERAL) | Pass A: this spec is inactive, so deleting it changes no runtime behavior at all. Pass B: an inactive spec justifies nothing and protects nothing, so it deletes. | DELETE |
| session_header.timestamp_canonical_repair (CORRECTION / GENERAL) | Pass A: this spec is inactive, so deleting it changes no runtime behavior at all. Pass B: an inactive spec justifies nothing, so it deletes (the active timestamp_repair_from_canonical_world_time spec above covers the live behavior). | DELETE |
| rewards_box.progress_percent_xp_curve_fallback (CORRECTION / REWARDS) | Pass A: progress percent currently falls back to an XP-curve computation when omitted, but the schema can require progress_percent instead. Pass B: computing a percent from an XP curve recomputes a model-owned derived value, and runtime evidence that the fallback fires proves the failure, not that server recomputation is the necessary fix. | DELETE |
| level_up_canonicalize_core.false_positive_rewards_box_suppressed (SUPPRESSION / LEVEL_UP) | Pass A: a contradicted level-up box inside an already-active modal must be suppressed, or the modal would show a stale offer. Pass B: the spec's own graduation note says the M2 prompt fix (current_turn_exp in the signal) removes the upstream cause, so keep it only as an interim until that fix lands, then delete it. | ADAPT |
| level_up_canonicalize_rewards.secondary_stale_signal_guard (SUPPRESSION / LEVEL_UP) | Pass A: a stale signal (target already reached) that escaped the core guard must still be caught before it drives UI. Pass B: guarding on persisted level versus signal target is staleness authorization, and it invents no target. | KEEP |
| level_up_canonicalize_rewards.no_session_rewards_stripped (SUPPRESSION / LEVEL_UP) | Pass A: a box claiming level_up_available when the reducer landed no session would render an unbacked offer. Pass B: stripping unbacked offer fields is authorization by the reducer's own landing result. | KEEP |
| level_up_session.strip_stale_offer_after_admin_commit (SUPPRESSION / LEVEL_UP) | Pass A: stale offers after an admin commit must be stripped, or completed sessions would keep rendering prompts. Pass B: the spec's own graduation note says it dies at M3 when the session projector owns offer lifecycle, so keep it only until the projector takes over, then delete it. | ADAPT |
| level_up_session.phantom_offer_clear (SUPPRESSION / LEVEL_UP) | Pass A: phantom offers for already-applied levels (the diamond-state bug) must be cleared, or players would be offered finished levels. Pass B: the spec's own graduation note says it dies at M3 when the projector owns offer lifecycle, so keep it only until then, then delete it. | ADAPT |
| god_mode.strip_modal_choices_on_admin_commit (SUPPRESSION / LEVEL_UP) | Pass A: modal choices alongside a direct admin level write must be stripped, or the committed session would coexist with a phantom prompt. Pass B: the spec's own graduation note says it deletes if the model complies with the god-mode prompt prohibition, so keep it only as an interim and delete it on demonstrated compliance. | ADAPT |
| god_mode.mixed_contract_admin_commit_wins (SUPPRESSION / LEVEL_UP) | Pass A: a god-mode turn emitting both a level write and a modal handoff needs a deterministic winner, and the admin commit is the operator's explicit act. Pass B: the spec's own graduation note says it deletes on model compliance with the prompt prohibition, so keep it only as an interim and delete it on demonstrated compliance. | ADAPT |
| god_mode.rejected_commit_level_revert (CORRECTION / LEVEL_UP) | Pass A: a rejected admin commit must revert the level, or a rejected sheet would partially persist. Pass B: reverting to the pre-turn level is fail-closed durability for an operator action, not a recomputed level. | KEEP |
| level_up_session.finish_release_authorization (CORRECTION / LEVEL_UP) | Pass A: finish releases must be authorized against the active modal session, or stray finishes could seal grants. Pass B: it is an authorization gate on explicit finish evidence, the same class as _is_authorized_level_up_finish_release. | KEEP |
| level_up_session.signal_backed_grant_authorization (CORRECTION / LEVEL_UP) | Pass A: signal-backed grants need authorization against the backing signal, or unbacked grants would land. Pass B: it is an authorization gate on explicit signal evidence. | KEEP |
| level_up_routing.session_overrides_stale_clear (DEFAULT / LEVEL_UP) | Pass A: a live session must override a stale clear, or a delayed clear could kill an active grant. Pass B: letting the durable session win over a stale clear is authorization precedence for the session record. | KEEP |
| player_character_data.ac_alias_mirrors_authored_armor_class (CORRECTION / LEVEL_UP) | Pass A: the `ac` alias must mirror an authored armor_class, or alias readers would see a stale bonus. Pass B: mirroring an authored value into an existing alias is storage consistency (the same class as _set_armor_class), not a recomputed bonus. | KEEP |
| level_up_modal.in_modal_rewards_box_pairing (CORRECTION / LEVEL_UP) | Pass A: in-modal rewards boxes must pair with the modal's planning block, or the modal would render half a pair. Pass B: pairing enforcement is modal-envelope authorization, the same class as enforce_rewards_box_planning_atomicity. | KEEP |
| level_up_turn.classify_mid_review_active_context (CORRECTION / LEVEL_UP) | Pass A: mid-review turns need classification as active context so correction guards do not treat them as stale. Pass B: classifying on explicit review-context evidence is routing, not a grant decision. | KEEP |
| level_up_story.preserve_amendable_review_ui (SUPPRESSION / LEVEL_UP) | Pass A: amendable review UI must survive story processing, or the player would lose the review they are mid-editing. Pass B: preserving UI for a live amendable grant is projection of persisted grant state, not a new offer. | KEEP |
| level_up_modal.session_authoritative_lock_gate (SUPPRESSION / LEVEL_UP) | Pass A: the modal lock must be gated on the authoritative session, or stale flags could lock or unlock the modal wrongly. Pass B: gating on the session record is authorization by the durable record. | KEEP |
| level_up_signal.context_backed_minimal_transition (CORRECTION / LEVEL_UP) | Pass A: minimal transitions currently derive from context when no explicit signal exists, but a transition without a signal should be an explicit signal or nothing. Pass B: deriving a transition from context invents signal evidence, so narrow it to contexts carrying an explicit signal and delete the derivation branch. | ADAPT |
| level_up_review.project_doorway_when_missing (CORRECTION / LEVEL_UP) | Pass A: a missing review doorway currently gets projected server-side, but the grant turn's prompt/schema can carry the doorway. Pass B: it inherits the ADAPT of project_level_up_review_choice: move the doorway into prompt/schema and keep server projection only as an interim. | ADAPT |
| level_up_choice.resolve_saved_control_text (CORRECTION / LEVEL_UP) | Pass A: saved control text currently resolves to a choice id, but clients can submit the id directly. Pass B: text-to-id resolution is fuzzy matching under the explicit-signals-only rule, so move to id submission and delete the text branch. | ADAPT |
| god_mode.resource_registry_clamp_bypass (SUPPRESSION / GENERAL) | Pass A: god-mode admin edits must bypass resource clamps, or operator corrections would be clamped back. Pass B: an operator-directed bypass is the God Mode product promise (the operator authors the value), not server authorship. | KEEP |
| resource_registry.death_saves_reset_on_long_rest (CORRECTION / GENERAL) | Pass A: death saves currently reset server-side on long rest, but the rest turn's schema can require the reset. Pass B: resetting a rules value on a narrative event is rules recomputation, so move it into the rest contract and delete the server reset. | ADAPT |
| resource_registry.preserve_triggered_current_without_rest (SUPPRESSION / GENERAL) | Pass A: triggered resource currents must survive turns without a rest, or spends would silently reset. Pass B: preservation is the opposite of transformation — it keeps the player's own recorded current intact. | KEEP |
| level_up_modal.stale_freeze_time_choice_stripped_after_close (SUPPRESSION / LEVEL_UP) | Pass A: freeze-time choices must be stripped after the modal closes, or a closed modal's clock control would linger. Pass B: stripping after an explicit close is state-machine cleanup keyed to server-owned modal state. | KEEP |
| admin_xp_correction.pop_zero_gained_receipt (SUPPRESSION / REWARDS) | Pass A: an admin XP correction currently pops a zero-gained receipt, or the correction would leave a spurious receipt behind. Pass B: popping a receipt as part of an operator-directed correction is the God Mode product promise applied to receipts. | KEEP |
| rewards_delivery.tangible_award_gate (SUPPRESSION / REWARDS) | Pass A: tangible awards must pass a delivery gate, or unreceipted items and gold would pay out. Pass B: gating delivery on receipt evidence is authorization, the same class as the receipt validators. | KEEP |
| rewards_delivery.xp_delta_mismatch_guard (SUPPRESSION / REWARDS) | Pass A: XP deltas that mismatch their receipts must be guarded, or mismatched XP would persist. Pass B: guarding on receipt mismatch is anti-cheat enforcement. | KEEP |
| graveyard.apply_character_death_signals (CORRECTION / GENERAL) | Pass A: character death signals currently apply server-side, but the death turn's schema can require the death state. Pass B: applying death state from signals is rules computation, so move it into the death contract and delete the server application. | ADAPT |
| social_hp.executed_roll_attribution (CORRECTION / GENERAL) | Pass A: executed rolls need attribution to their roller, or roll audit trails would be unattributable. Pass B: attributing a server-executed roll is audit bookkeeping for the §6 anti-cheat dice path, not a roll outcome decision. | KEEP |
| social_hp.terminal_status_resolution (CORRECTION / GENERAL) | Pass A: terminal HP status currently resolves server-side, but the damage turn's schema can require the terminal state. Pass B: resolving terminal status from HP is rules computation, so move it into the damage contract and delete the server resolution. | ADAPT |

### backend_adjustment_specs.py grouping tuples

Each tuple is a pure index: it groups specs for import convenience and
justifies nothing on its own. Every member carries its own row above;
the tuple's verdict is KEEP as an index only, and deleting a tuple
without deleting its members would change nothing about runtime behavior
except import paths.

| Tuple | Justification | Verdict |
|---|---|---|
| ACTIVE_LOCATION_ADJUSTMENT_SPECS, ACTIVE_PR_6958_ADJUSTMENT_SPECS, ACTIVE_PR_7149_ADJUSTMENT_SPECS, ACTIVE_PR_7164_ADJUSTMENT_SPECS (empty), ACTIVE_PR_7339_ADJUSTMENT_SPECS, ACTIVE_PR_8489_ADJUSTMENT_SPECS (second definition wins), ACTIVE_PR_9867_ADJUSTMENT_SPECS, ACTIVE_COMBAT_END_NPC_CLEANUP_ADJUSTMENT_SPECS, ACTIVE_LLM_ADJUSTER_FRAMEWORK_SPECS, ACTIVE_LEVEL_UP_THRESHOLD_OVERRIDE_SPECS, ACTIVE_LEVEL_UP_MAIN_CLEANUP_SPECS, ACTIVE_LEVEL_UP_SESSION_ROUTING_SPECS, ACTIVE_LEVEL_UP_MODAL_REWARDS_PAIRING_SPECS, ACTIVE_PR_7236_RESOURCE_REGISTRY_SPECS, ACTIVE_PR_8777_ADJUSTMENT_SPECS, ACTIVE_PR_9859_ADJUSTMENT_SPECS, ACTIVE_REWARDS_DELIVERY_SUPPRESSION_SPECS, ACTIVE_PR_9942_ADJUSTMENT_SPECS, ACTIVE_SOCIAL_HP_ROLL_ATTRIBUTION_ADJUSTMENT_SPECS, ACTIVE_SOCIAL_HP_TERMINAL_RESOLUTION_ADJUSTMENT_SPECS | Pass A: callers import spec groups by name, so the tuples are needed as import targets. Pass B: a tuple of spec records performs no transform and proves no necessity; each member's own row above is the only justification that counts. | KEEP |

## backend_adjustment_registry.py — file verdict: KEEP (shim)

This file is a backward-compatible re-export shim: it imports spec groups
from `backend_adjustment_specs` and types from `backend_adjustment_types`
and re-exports them under `__all__`. Pass A: deleting it breaks every
caller that imports the registry path. Pass B: re-exporting performs no
transform and justifies no spec; each re-exported name inherits its
source verdict (spec groups from the specs table above, types from the
types table below). All 24 re-exported names share this verdict and
justification, since a shim has no independent behavior to judge per
name. Note: the registry re-exports a subset of the specs-file groups
(it omits, e.g., ACTIVE_LEVEL_UP_MODAL_REWARDS_PAIRING_SPECS and
ACTIVE_REWARDS_DELIVERY_SUPPRESSION_SPECS, which live in
`adjusters/specs.py` instead) — that subsetting is itself just import
history, not a judgment about the omitted groups.

## backend_adjustment_types.py — file verdict: KEEP (shim)

This file is a backward-compatible re-export shim for the types that now
live in `adjusters/types.py`. Pass A: deleting it breaks callers on the
old import path. Pass B: re-exporting performs no transform; each name
(AdjustmentSpec, EvidenceStatus, InvalidAdjustmentSpecError,
RootCauseStatus, SpecCategory, SpecScope) inherits its verdict from the
`adjusters/types.py` table below. All six names share this verdict and
justification, since a shim has no independent behavior.

## adjusters/ — file verdicts: KEEP (framework), docs Phase 1 only

The adjuster framework is the proof-gated execution layer for
post-LLM middleware: registration requires a pre-committed,
disk-loaded, hash-matching evidence artifact, and processing is
bounded by per-session caps with rollback on failure. The framework
itself is transport and authorization; the one shipped game adjuster
(json_strip_prefix) is a structural parse fix, not a semantic override.

| Symbol | Pass A + Pass B justification | Verdict |
|---|---|---|
| adjusters/__init__.py (package init: imports adjusters.game for registration side effects; re-exports AdjusterEngine, engine, AdjusterRegistration, AdjusterScope, CorrectionMode, EvidenceObject) | Pass A: importing the package must trigger built-in adjuster registration, or the engine would run empty. Pass B: the init performs registration side effects and re-exports only, adding no transform; each re-exported name inherits its source verdict. | KEEP |
| adjusters/base.py AdjusterEngine.__init__ | Pass A: the engine needs bounded session storage, or intervention counts would grow unboundedly. Pass B: a capacity bound (max_sessions, default 1000) is explicitly server-owned. | KEEP |
| adjusters/base.py AdjusterEngine._ensure_registered | Pass A: default adjusters must load lazily on first use, or import-time disk I/O would break environments without evidence artifacts. Pass B: lazy loading with failure logging is transport robustness, and a failed load fails open to unmodified output rather than inventing a fix. | KEEP |
| adjusters/base.py AdjusterEngine.register_allowed_specs | Pass A: tests need a way to extend the allow-list with fixture specs, or framework tests could not register anything. Pass B: it is explicitly test-fixture-only plumbing, and it changes no production registration rule. | KEEP |
| adjusters/base.py AdjusterEngine.register | Pass A: without the proof gate, any adjuster could register on prose claims alone, defeating the framework's whole purpose. Pass B: requiring an active registered spec, a pre-committed disk-loaded sha256 that recomputes correctly, and a valid scope is authorization of the override layer itself — the strongest server-owned gate in this group. | KEEP |
| adjusters/base.py AdjusterEngine._sorted_adjusters | Pass A: adjusters must run in priority order, or a late structural fix could run after a semantic one that needed valid JSON. Pass B: sorting by a declared priority is deterministic execution order, not a domain decision. | KEEP |
| adjusters/base.py AdjusterEngine._get_session_counts_locked | Pass A: per-session intervention counts need LRU eviction, or the counts map would grow forever. Pass B: bounded LRU bookkeeping under a lock is capacity and concurrency hygiene. | KEEP |
| adjusters/base.py AdjusterEngine._should_intercept_safely | Pass A: a crashing predicate must not take down the whole pipeline, so fail-closed skipping is needed. Pass B: failing closed on predicate errors is safety discipline, and a skipped adjuster changes nothing. | KEEP |
| adjusters/base.py AdjusterEngine.process | Pass A: this is the pipeline that actually runs adjusters over LLM output, with a fast path that returns the original dict untouched when nothing intercepts. Pass B: it enforces session caps (exempting only SILENT structural fixes), snapshots for rollback, validates result types, and records applied adjustments — bounded capacity plus transaction integrity, not domain authorship. | KEEP |
| adjusters/base.py AdjusterEngine.list_adjusters | Pass A: operators need observability over which adjusters are registered and active. Pass B: listing registrations is logging/observability, which §6 keeps. | KEEP |
| adjusters/base.py engine (singleton) | Pass A: callers need one shared engine instance, or registrations would fragment across instances. Pass B: a singleton holder is transport, with no logic of its own. | KEEP |
| adjusters/registry.py (re-export shim) | Pass A: deleting it breaks callers on the adjusters.registry import path. Pass B: it re-exports spec groups from adjusters/specs.py and backend_adjustment_specs plus types from adjusters/types.py, performing no transform; each name inherits its source verdict (same shim reasoning as backend_adjustment_registry.py). | KEEP |
| adjusters/specs.py (forwarding module) | Pass A: deleting it breaks callers importing spec groups from the adjusters path. Pass B: it forwards 14 spec groups verbatim from backend_adjustment_specs to avoid dual-source drift, performing no transform; each group inherits its members' verdicts. | KEEP |
| adjusters/types.py InvalidAdjustmentSpecError | Pass A: incomplete or unsafe spec metadata needs a distinct failure so registration can reject it cleanly. Pass B: an error type for the framework's authorization gate is transport. | KEEP |
| adjusters/types.py SpecCategory / SpecScope / RootCauseStatus / EvidenceStatus | Pass A: specs need shared vocabularies for category, scope, root cause, and evidence status, or every spec would invent its own strings. Pass B: they are enum vocabularies for framework metadata, not domain computations. | KEEP |
| adjusters/types.py _PROOF_REQUIRED_CATEGORIES | Pass A: correction, default, and suppression specs need proof requirements, while audit-only specs do not. Pass B: it is a framework policy constant encoding which categories require evidence. | KEEP |
| adjusters/types.py _is_gist_url / _is_runtime_ref / _has_runtime_evidence | Pass A: evidence validation needs to recognize gist URLs and runtime: refs, or proven-evidence claims could not be checked. Pass B: they are format predicates for the proof gate, with no domain effect. | KEEP |
| adjusters/types.py AdjustmentSpec | Pass A: the framework needs one immutable spec record type, or registration could not be validated uniformly. Pass B: its __post_init__ enforces proof requirements (root cause, evidence refs, allowed_when, reason code), rejects raw_response storage, validates evidence URL shape, and requires a runtime artifact for proven claims — the framework's authorization record itself. | KEEP |
| adjusters/types.py AdjustmentSpec.__post_init__ | Pass A: without post-init validation, malformed specs would register and fail later at runtime. Pass B: it is the validation half of the record above, including the deprecated `enabled` alias mirroring rule (active wins). | KEEP |
| adjusters/types.py AdjustmentSpec.enabled (deprecated alias) | Pass A: legacy callers still pass `enabled`, so the alias must keep working until they migrate. Pass B: it is a deprecated compatibility alias with an explicit active-wins rule, so keep it until legacy callers migrate, then delete it. | ADAPT |
| adjusters/schemas/__init__.py, adjusters/utils/__init__.py, adjusters/game/__init__.py (package inits; game init imports json_strip_prefix for registration) | Pass A: package imports must work and the game package must trigger adjuster registration on import. Pass B: these inits contain no logic beyond an import side effect, so they inherit the verdicts of what they import. | KEEP |
| adjusters/schemas/models.py AdjusterScope / CorrectionMode | Pass A: registrations need scope and correction-mode vocabularies (including SILENT vs WARN vs FLAG surfacing). Pass B: they are enum vocabularies for framework metadata. | KEEP |
| adjusters/schemas/models.py EvidenceObject | Pass A: the framework needs a serializable evidence record with redacted responses and comparator artifacts, or proof could not be inspected. Pass B: it is a schema for durable proof artifacts, and its fields (raw_request, state_before/after, disabled comparator) are what make an adjuster auditable. | KEEP |
| adjusters/schemas/models.py EvidenceObject.validate_proof_artifacts | Pass A: registration must reject evidence that is only prose, or the proof gate would be theater. Pass B: requiring non-empty agent, provenance, reproducer, raw/comparator maps is framework authorization, checking artifact shape rather than the semantic claim. | KEEP |
| adjusters/schemas/models.py EvidenceObject.compute_hash | Pass A: the committed sha256 must be recomputable from the redacted payload, or the gate could not verify it. Pass B: hashing redacted JSON is integrity verification, and it deliberately excludes the hash and URL fields. | KEEP |
| adjusters/schemas/models.py EvidenceObject.load_from_disk | Pass A: evidence must load from committed proof.json + proof.sha256 artifacts, or the disk-provenance gate could not be satisfied. Pass B: loading committed artifacts and setting _from_disk is the provenance mechanism itself, and missing artifacts raise (a deploy problem, surfaced loudly). | KEEP |
| adjusters/schemas/models.py EvidenceObject.save_to_disk | Pass A: new evidence bundles need a way to be written (redacted) with a computed hash, or no new adjuster could ever be authored. Pass B: writing redacted payloads plus a hash file is durable proof creation with PII redaction enforced (T10). | KEEP |
| adjusters/schemas/models.py AdjusterRegistration | Pass A: registrations need a serializable metadata record (no callables) so they can be listed and inspected. Pass B: it is a schema for framework metadata, with priority and per-session caps as capacity policy. | KEEP |
| adjusters/game/json_strip_prefix.py _EVIDENCE_DIR | Pass A: the adjuster must locate its committed evidence artifact reliably. Pass B: it is a file-location constant for the proof artifact. | KEEP |
| adjusters/game/json_strip_prefix.py _load_committed_evidence / _get_evidence | Pass A: evidence must load from disk (not be constructed inline) to satisfy the engine's provenance gate, and lazily so import never raises. Pass B: disk-loaded provenance plus lazy caching is the framework's integrity mechanism, and a missing artifact fails open to unmodified output. | KEEP |
| adjusters/game/json_strip_prefix.py _PREFIX_RE | Pass A: Gemini's [Mode: ...] / [STORY MODE] / [GOD MODE] prefixes must be matched to strip them, or prefixed JSON would fail to parse. Pass B: the regex matches only declared literal mode labels (with a REGEXP APPROVED note in the file) and never routes on semantic intent, so it is structural prefix parsing, not keyword routing. | KEEP |
| adjusters/game/json_strip_prefix.py _RAW_RESPONSE_KEYS | Pass A: raw responses live under several known keys, and the stripper must check them in precedence order. Pass B: it is a key vocabulary for transport fields. | KEEP |
| adjusters/game/json_strip_prefix.py _strip_mode_prefixes | Pass A: prefixed raw text must be cleaned only when a real prefix exists and the remainder parses as JSON, or valid output could be corrupted. Pass B: it strips declared prefixes and validates the remainder with json.loads, returning None otherwise — fail-closed structural repair. | KEEP |
| adjusters/game/json_strip_prefix.py _iter_raw_response_values | Pass A: interception and override both need the present raw keys in precedence order. Pass B: it is a structural iterator over transport keys. | KEEP |
| adjusters/game/json_strip_prefix.py should_intercept_json_prefix | Pass A: the engine must know when prefix pollution is present, and must not intercept valid JSON arrays. Pass B: it tests for strippable prefixes in raw strings only, which is structural detection, not semantic classification. | KEEP |
| adjusters/game/json_strip_prefix.py override_strip_json_prefix | Pass A: polluted raw output must be cleaned before JSON parsing, or the turn fails on a formatting artifact. Pass B: it replaces only raw-string values whose cleaned form parses, leaving everything else untouched — a silent structural fix with no semantic impact, matching its SILENT correction mode. | KEEP |
| adjusters/game/json_strip_prefix.py _register_once (+ import-time try/except) | Pass A: the adjuster must register with priority 10 (first, so other adjusters see valid JSON), and a missing artifact must not break import. Pass B: registration through the engine's proof gate is framework authorization, and the try/except fails open to unmodified output when evidence is absent. | KEEP |
| adjusters/utils/redact.py _SSN_RE / _PII_PATTERNS | Pass A: evidence bundles must not commit SSNs, tokens, API keys, emails, or card numbers, so patterns must be declared in one place. Pass B: redaction patterns are privacy protection for durable artifacts, and the SSN pattern's consistent-separator requirement avoids false positives on game IDs and gold amounts. | KEEP |
| adjusters/utils/redact.py is_luhn_valid | Pass A: card-like numbers must pass Luhn before redaction, or game numbers would be wrongly redacted. Pass B: it is a checksum predicate for the redaction gate. | KEEP |
| adjusters/utils/redact.py redact_pii | Pass A: evidence data (strings, lists, dicts) must be redacted recursively before commit, or PII would leak into proof bundles. Pass B: it applies patterns plus Luhn-gated card redaction across structures, which is privacy enforcement for durable artifacts, not a game transform. | KEEP |
| adjusters/evidence/ADJ-WA-JSON-STRIP-PREFIX/v1/proof.json + proof.sha256 | Pass A: the json_strip_prefix adjuster cannot register without its committed proof artifacts. Pass B: these are durable proof data files, not code; their verdict is KEEP as the provenance backing the registered exception above. | KEEP |

### adjusters/docs/ + adjusters/README.md — Phase 1 file-level only

These are documentation for the adjuster framework (a 10-chapter
series: origin, core invariant, tenets, types, engine, authoring,
wire-in, redaction, testing, lifecycle, checklist, plus a README entry
point). Pass A: deleting them breaks no runtime behavior — they are
not imported or executed. Pass B: they document the proof-gated
invariant the framework enforces, so they are accurate supporting
material, not code to transform. File-level verdict: **KEEP** (all 12
files: README.md + docs/00–10). No per-method table applies to prose
docs; the one correction worth recording is that the docs' claim that
"the bulk of the engine lives in one process() method" remains true
in the code read for this audit.

## mvp_site/docs/zfc_audit/ — Phase 1 file-level only (as tasked)

- `SUMMARY.md` (141 lines, audit date 2026-05-01, scope 118 Python files
  / ~631 methods): a snapshot summary claiming ~95% ZFC compliance, 3
  non-compliant methods, ~35 needing human review. Pass A: deleting it
  breaks nothing at runtime — it is not imported. Pass B: it is a stale
  snapshot (it predates this audit by months, covers files and symbols
  that have since moved, and its own FULL_AUDIT companion warns that
  rows go stale when symbols are renamed). File-level verdict: **DELETE**
  (archive it as a historical snapshot; it must not be cited as current
  compliance evidence).
- `FULL_AUDIT.md` (1,301 lines, same 2026-05-01 snapshot, per-file
  per-method classification): Pass A: deleting it breaks nothing at
  runtime. Pass B: same staleness problem at larger scale — a
  per-method table that is not updated on renames is a merge-target
  hazard by its own update protocol, and this run-2 audit supersedes
  its godmode/levelup/rewards rows. File-level verdict: **DELETE**
  (archive; superseded by this file for this group).

## Conflicts with §6 user decisions

None. Server logging verdicts in this group are KEEP (warn-only
conclude telemetry, audit records, adjuster logs); no verdict moves
logging onto or off the turn path in a way §6 forbids, and no verdict
touches dice resolution. No faction/living-world simulation code lives
in this group, so the faction-async rule has nothing to attach to here.
The one §6-adjacent note: `god_mode_executor._refresh_replacement_xp_display`
is DELETE, which does not conflict with §6 because it is display
recomputation, not logging, anti-cheat, or faction work.

## Verdict tally

Counts below were tallied mechanically from the verdict cells in this
file's tables (`grep -c '| KEEP |$'` etc.): shim/grouped rows count once
per row as written, not once per re-exported name; docs file-level
verdicts are listed separately and are NOT included in the code tally.
Grouped rows (e.g. status-constant families, the specs grouping-tuples
row, shim paragraphs) each cover multiple symbols, so the underlying
symbol count exceeds 471.

- **KEEP: 375 rows** — dominated by the session/audit reducers, the
  receipt/authorization/anti-cheat core of rewards_engine, the God Mode
  executor + schema, the explicit-signal conclude guard, and the
  adjuster framework's proof gates.
- **ADAPT: 68 rows** — dominated by normalizations, legacy compat shims,
  prompt-gap strips and suppressions with graduation notes, the two
  giant rewards reducers' synthesis/suppression branches, and the
  grant-fold family (all with a named move: to prompt, to schema, to
  the session projector, or to a sunset).
- **DELETE: 28 rows** — the XP/progress recompute layer
  (effective_pre_turn_level's XP branch, canonical progress, cross-check,
  anchors, synthesizers, display projectors), the campaign_divine
  threshold gates (5), the inactive specs (2), the legacy location
  fallback and header-generation specs, the display-format signal
  spec, the XP-evidence enrichment and synthesis specs, and the
  redundant no-authority grant check.
- **Total code rows: 471 (375 + 68 + 28).**
- **Docs (separate):** adjusters/docs + README: KEEP, 12 files;
  mvp_site/docs/zfc_audit/: DELETE, 2 files (archive as stale snapshot).
