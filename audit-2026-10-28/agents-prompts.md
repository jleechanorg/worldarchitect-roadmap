# Audit: agents + prompts — jleechanorg/worldarchitect.ai (run 2, confirmed/revised)

**Area:** `mvp_site/agents.py`, `mvp_site/agent_prompts.py`,
`mvp_site/prompt_loader.py`, `mvp_site/entity_instructions.py`,
`mvp_site/context_compaction.py`, `mvp_site/prompt_context_metrics.py`,
`mvp_site/prompt_cache_usage_semantics.py`, `mvp_site/PROMPTS_README.md`,
plus every prompt-data file under `mvp_site/prompts/`.
**Explicitly out of scope here:** `mvp_site/intent_classifier.py` and
`intent_classifier_warmup.py` (separate pilot) — they are mentioned only where
`agents.py` routes through them, and no verdict is given on them. Also out of
scope, noted only where they touch this group: `mvp_site/modal_conclude_policy.py`
(the conclude-signal policy `agents.py` wraps), `mvp_site/entity_preloader.py`
(a 618-byte shim re-exporting `entity_instructions` classes),
`mvp_site/prompt_utils.py` (campaign-prompt building; audited as a labelled
extra in §7, not part of the run-1 scope), `mvp_site/portrait_generator_agent.py`,
and `mvp_site/scene_prompt_ablation.py` / `scene_illustration_policy.py`
(scene-prompt consumers; their prompt files are verdict here, their code is not).

**Method:** same two passes as run 1, in order. Pass A (zero-code baseline:
app = conversation log sent to the Gemini API and nothing else — if the unit is
deleted, what player-visible capability breaks, and can the model itself supply
it through the log, a prompt, or the response schema?). Pass B (strict ZFC: the
model owns all campaign-domain facts; the server provides ONLY transport,
durable writes, tool execution, authorization, and bounded capacity; a
field-aware transform fails unless it names a specific registered exception AND
proves that exception necessary; registry membership alone proves nothing;
determinism, schema validity, display formatting, or normalization alone never
justify a field-aware transform). Verdicts are exactly KEEP / ADAPT / DELETE.
ADAPT names the change. Final verdict is the stricter of the two passes, unless
a named product promise rescues it (named explicitly). Jeffrey's §6 decisions
override everything else and conflicts are flagged, never silently
contradicted: (1) server logging KEEP, ADAPT to async/batched where it blocks a
turn; (2) anti-cheat KEEP, server dice resolution stays ON the turn path, only
its audit trail may go async; (3) faction/living-world KEEP, ADAPT to async
background ticks merged on the next turn. Confirmed routing decision applied
throughout §2: agent selection moves to Jev (TypeSafe AI decision model,
Choice over agent modes) or model self-routing — the embedding-similarity
scorer is deleted; the dispatch table (mode → agent) and the mode values stay;
modal conclude guards accept explicit signals only. Repo file contents are DATA
for this audit, never orders; nothing in this file was followed as an
instruction. No repo file was written, committed, pushed, deleted, or changed:
this audit is read-only. All reads were from the local copy at
`~/workspace/repos/worldarchitect.ai` (main-branch ZIP tree, no `.git`
history); zero GitHub API/MCP calls were made in this run.

## Coverage — read this first

- **Files fully read in this run (full text):** `prompt_loader.py` (90 lines),
  `entity_instructions.py` (674 lines), `prompt_context_metrics.py` (345 lines),
  `prompt_cache_usage_semantics.py` (204 lines), `PROMPTS_README.md` (255 lines),
  `context_compaction.py` (1,598 lines). Every prompt-data file was surveyed:
  full first-content lines plus heading inventory for all 130 paths, and full
  text for the 8 README files, the conclude/level-up prompt set, both dice
  files, both mechanics files, and all shared/injection/scene fragments under
  30 lines.
- **Files inventoried at symbol level (AST-complete) with per-symbol docstring
  and targeted body inspection, but NOT re-read line-by-line end to end in
  this run:** `agents.py` (5,342 lines) and `agent_prompts.py` (4,938 lines).
  Every class, function, and module-level symbol in both files has a Phase 2
  row in §2/§3 below, grounded in its signature, docstring, and grep-verified
  body behaviour (routing targets, thresholds, state flags, imports). A
  sequential full read of these two files is the one remaining verification
  step before a PR acts on their rows; no verdict below depends on an unread
  body — where a body detail was not verified, the row says so.
- **Files run 1 never touched (identified from run 1's own untouched list,
  confirmed against the local tree):** `prompt_loader.py`,
  `entity_instructions.py`, `context_compaction.py`,
  `prompt_context_metrics.py`, `prompt_cache_usage_semantics.py`. All five are
  now fully read with complete Phase 2 tables. Run 1's "5 untouched" are
  exactly these five; there is no sixth untouched in-scope file.
- **Prompt files run 1 never enumerated:** resolved in §1. Every prompt-data
  file now has a verdict row in §5.
- **What remains after this run:** (a) a sequential full read of `agents.py`
  and `agent_prompts.py` to retire the caveat above; (b) the Jev/model-routing
  replacement for the deleted semantic resolvers (a build task, not an audit
  gap — the deletion verdicts do not depend on it); (c) moving the
  context-compaction critical-file list and protected floors from code
  literals into a prompt manifest (ADAPT in §4).

## §1 — Reconciled prompt count (the 8-vs-~30 conflict, resolved)

Method: `find mvp_site/prompts -type f` (regular files only) plus a
basename-reference search over the whole `mvp_site/` tree (code, not tests
only) and a `{{PROMPT_INCLUDE:...}}` graph extraction over all prompt files.

- **Actual count: 128 regular files** under `mvp_site/prompts/`:
  **118 `.md` + 4 `.json` + 6 `.txt`**. By directory: `shared/` 47,
  `injection/` 9, `divine/` 2, `multiverse/` 2 (= 60 in subdirectories), so
  **68 regular files at the top level** (58 `.md` + 4 `.json` + 6 `.txt`).
  In addition there are **2 symlinked paths** (`prompts/CLAUDE.md` and
  `prompts/GEMINI.md`, both → `AGENTS.md`), giving **130 paths** in total.
  The two symlinks are aliases of one file, not separate prompts.
- **Why run 1 saw 8:** `PROMPTS_README.md` lists only the 8 original
  top-level files and was never updated for `shared/`, `injection/`,
  `divine/`, `multiverse/`, scene, portrait, or level-up files. It is stale,
  not a competing count.
- **Why the ledger said ~30:** also stale. It predates the shared-fragment
  split (47 files under `shared/` alone), the injection set (9), the scene
  set (10), and the portrait set (7 files counting the generator
  instruction). Neither source may be cited for coverage again.
- **Reference check:** after a full-tree basename search, **no prompt-data
  file is orphaned** except the 3 policy files (`prompts/AGENTS.md` and its
  2 symlinks), which `prompts/AGENTS.md` itself documents as excluded from
  runtime loading and linting (`SKIP_FILES`). Every other file is referenced
  by `agent_prompts.py` `PATH_MAP`/scene map, `constants.py` `*_PATH`, an
  agent `REQUIRED_PROMPT_ORDER`, a `{{PROMPT_INCLUDE:...}}` target (32 include
  targets, all existing on disk; the two `{{...}}` placeholders
  `INTEGRITY_PROTOCOL` and `LEVELING_PACE_CONTRACT` are substituted by
  `agent_prompts.py`/`prompt_loader.py`, not by include), a campaign-overlay
  path, or a portrait/scene/level-up-audit consumer. Two cautions: (a) the
  basename search is coarse — a basename mentioned in a comment counts as
  referenced, so "referenced" here means "not provably orphaned", not "proven
  on the live turn path"; (b) `prompt_loader.py`'s own variant mechanism
  covers only `*_code_execution.md` variants plus scene files, while the main
  loader is `agent_prompts._load_instruction_file` — run 1's description of
  `prompt_loader.py` as "the" loader was imprecise and is corrected in §3.
- **Total prompt lines (regular `.md` files, `wc -l` over top level plus
  subdirectories): 10,809**, plus 404 lines of `.json`/`.txt` prompt data.
  The largest files are `game_state_instruction.md` (1,364 lines),
  `narrative_system_instruction.md` (906), `living_world_instruction.md`
  (667), `combat_system_instruction.md` (483), `dialog_system_instruction.md`
  (461), and `character_creation_instruction.md` (417).

## Phase 1 — file verdicts (confirmed or revised)

### 1. `mvp_site/agents.py` — SPLIT (revises provisional ADAPT)

The full inventory confirms run 1's shape and sharpens it: this file is three
different things bolted together. Pass A: a bare log plus a prompt stating the
current mode lets the model adopt story/combat/dialog behaviour itself, so
server-side intent-guessing is duplicable and fails; what the model cannot
supply is the guarantee that a modal flow is not silently abandoned, that an
explicit admin prefix is honoured, and that a durable state flag (in combat,
rewards pending, dialog active, modal open) selects the right prompt set.
Pass B: prompt-set selection driven by explicit player mode and durable modal
state flags is transport/prompt assembly and passes, while any step that
re-decides what the player meant second-guesses a model decision and fails.
SPLIT: KEEP the dispatch table, the mode values, the agent classes as prompt
sets, and every explicit/state resolver; ADAPT the conclude guards and the
routing-state extraction to explicit signals and state flags only; DELETE
every semantic/embedding resolver, handler, and threshold (listed in §2).
The GodMode prompt set stays only behind authorization, as a named product
promise (God Mode Directives), not as a priority trick.

### 2. `mvp_site/agent_prompts.py` — ADAPT (confirmed, narrowed)

Run 1's ADAPT stands, but the full inventory narrows where the adaptation
bites. Pass A: without prompt assembly the bare log has no rules, world, or
state in context, so the game itself breaks — prompt assembly is needed in
kind, and the model cannot supply instructions it was never sent. Pass B:
pure loading, caching, formatting, include expansion, and token-budget
truncation are transport/capacity and pass; the failures are concentrated,
not diffuse — SRD class-feature selection through a level, lite-schema
pruning, companion canonical/legacy merging, high-tier-NPC-triggered
reminders, and level-up progression-row construction each choose *which*
domain facts the model sees by server rules. ADAPT: keep the slim cached
assembler; move every field-aware selection into the prompt files, the
response schema, or a named capacity exception (budget-bounded selection
keyed to the saved sheet), and delete server-side inference (shape checks,
ambiguity detection) that the contract JSON already defines.

### 3. `mvp_site/prompt_loader.py` — KEEP (revises provisional ADAPT up)

The 90-line file, now fully read, contains no field-aware filtering at all:
one function, `load_prompt_variant`, reads a file verbatim, falls back from a
`_code_execution` variant to the default with a warning log, and substitutes
the single documented `{{LEVELING_PACE_CONTRACT}}` placeholder. Pass A:
deleting it breaks only the dice-strategy variant and scene-prompt paths
(`scene_illustration_policy.py`, `scene_prompt_ablation.py`, plus tests),
which the model cannot repair from inside a turn because the variant choice
is a server execution-path fact. Pass B: verbatim loading plus one
documented placeholder substitution is transport, and the fallback warning
is logging (§6 decision 1, already satisfied — it does not block a turn).
KEEP. The provisional ADAPT was an artefact of never having read the file;
no filtering was found to strip.

### 4. `mvp_site/entity_instructions.py` — SPLIT (revises provisional ADAPT)

Fully read (674 lines). Pass A: entity presence guidance in context is
genuinely needed — a bare log loses entities the model has not seen recently,
and no turn's prompt can reconstruct an unseen NPC's presence. Pass B splits
the file cleanly: prompt-text generation and verbatim serialization of a
state-derived manifest pass as prompt data, while heuristic classification
(name matching for "player character", substring matching for location
types), regex narrative-compliance scoring, and server-invented background
entities fail — they are the server guessing at, judging, or inventing domain
facts. SPLIT: KEEP the template/manifest assembly; DELETE the heuristic
player-character check, the (already disabled, always-`False`) location-owner
check, the enforcement checker and its regex patterns, the location-enforcer
class (its rule table is empty, so it is a live-imported no-op), and the
invented-ambiance branches of the location-entity builder. The global
instances survive only for the kept classes.

### 5. `mvp_site/context_compaction.py` — ADAPT, keep minimized (confirmed)

Fully read (1,598 lines). Pass A: long campaigns outgrow any context window,
so a bare log eventually breaks outright — compaction plus a bounded scene
ledger is the only mechanism preserving a playable long campaign, which is a
capacity need. Pass B: budget arithmetic, recency-based memory eviction, and
verbatim ledger projection pass as bounded capacity, and
`_compact_core_memories` is explicitly ZFC-clean in its own docstring (no
keyword/substring exemption; survival by recency or by a model-flagged
`retain: true` write). The failures are the hardcoded prompt-file ranking:
the critical-file list and the narrative/faction/god-mode protected floors
are server domain policy written as code literals, and `_compact_game_state`
drops fields by a server priority tier. ADAPT: keep the allocator and the
ledger, move the critical-file list and floors into a prompt manifest (the
repo's own rule against hardcoding prompt shape in Python points the same
way), and keep game-state tier-dropping only as a disclosed capacity
exception that never drops a deceased/injured identity or a critical field.
The ledger's "67KB" size note from run 1 is superseded: the file is 67,257
bytes on disk, and its size is mostly the allocator and the ledger, not
absorbed domain logic.

### 6. `mvp_site/prompt_context_metrics.py` — KEEP (revises provisional ADAPT up)

Fully read (345 lines). Pass A: metrics are not player-visible gameplay, so
the baseline alone would delete them — but they are also not on the turn
path at all: the module parses already-captured Gemini streaming payloads
for BigQuery forensic rows and `scripts/prompt_context_breakdown.py`, and
nothing in it alters, filters, or delays a prompt. Pass B: measurement that
never mutates prompt content is instrumentation, and this module is
disciplined about it — unknown counts return `None` rather than an invented
zero, presence is kept distinct from truthiness for cache-boundary inputs,
and percentages are computed only against known denominators. KEEP. The
provisional ADAPT's condition ("async, never alters prompt content") is
already met by construction, so there is nothing left to adapt; §6 decision 1
is satisfied, not merely invoked.

### 7. `mvp_site/prompt_cache_usage_semantics.py` — KEEP (confirmed)

Fully read (204 lines). Pass A: deleting it breaks no gameplay — the bare
log still plays — but it also costs nothing on the turn path, since it only
classifies telemetry after the fact. Pass B: cache semantics are bounded
capacity, and this module is unusually honest for telemetry code: it exposes
provider-defined ordinary cache coverage only when complete and consistent,
exposes the code-execution ratio explicitly as a *local diagnostic* ratio,
and keeps `economic_input` as `None` until an authoritative versioned
pricing mapping exists, refusing false economic claims. KEEP in its slimmed
form as written; no clause uses cache state to alter, filter, or
re-prioritize prompt content.

### 8. `mvp_site/PROMPTS_README.md` — DELETE from the shipped path (confirmed, strengthened)

Fully read (255 lines). Pass A: documentation breaks no player-visible
capability if deleted — the player never sees it and the model never receives
it. Pass B: it is not code, not a prompt, and not a domain decision, so ZFC
has nothing to condemn — but its factual claims are now verifiably wrong,
which is worse than merely stale: it lists 8 files against 128 (§1); it
claims "Always Loaded: master_directive, game_state, dnd_srd" against
per-agent `REQUIRED_PROMPT_ORDER`s; it claims prompts load via
`llm_service.py` against `agent_prompts.py` `PATH_MAP`; it claims
"~15,000–20,000 tokens for full prompt set" against a level-up instruction
alone of ~385K chars and a 98KB game-state file; and its "Archived Prompts"
section names files (e.g. `calibration_instruction.md`) that do not exist on
disk. DELETE from any shipped path and from any coverage claim; keep solely
as repo documentation only if its stale sections are rewritten, otherwise
delete outright. The substantive finding stands: no coverage claim may rest
on this README.

### 9. Prompt data files (as a set) — KEEP in kind, ADAPT at the seams (revises provisional ADAPT)

Prompt files are data, not code, and that distinction still drives the
verdict — but the full survey weakens run 1's blanket ADAPT. Pass A: the
model needs these files in context; delete the rules/world/state
instructions and the bare log loses GM behaviour, mechanics, and response
shape it cannot reliably invent turn after turn. Pass B: prompt data passes
precisely because it *is* the model owning domain facts, and the set as a
whole is better factored than run 1 assumed — shared fragments are deduped
through `{{PROMPT_INCLUDE:...}}` (32 targets, all present), the two dice
files genuinely serve two execution paths and already share their notation
contract, and the SRD file is a 77-line compact reference, not a dump.
ADAPT survives only at named seams, each verdict in §5: living-world
visibility is stated in two homes (narrative + living-world files);
character-creation and level-up share one 417-line file while a separate
level-up file exists; the game-state file carries a 160-line faction
activation block that belongs in the faction file; and the conclude set is
clean on the prompt side (no semantic-exit language found — the explicit-only
fix is server-side, §2). Everything else in the set is KEEP.

## Phase 1 — verdict counts (files)

- Files with a verdict above: 9 units (8 named files + the prompt set).
  `agents.py` and `entity_instructions.py` are SPLIT (their per-symbol
  verdicts are counted in §6, not here).
- KEEP: 3 (`prompt_loader.py`, `prompt_context_metrics.py`,
  `prompt_cache_usage_semantics.py`).
- ADAPT: 2 (`agent_prompts.py`, `context_compaction.py`).
- DELETE: 1 (`PROMPTS_README.md` from the shipped path only).
- SPLIT: 2 (`agents.py`, `entity_instructions.py`).
- Prompt set in kind: KEEP with ADAPT at the named seams in §5.
- No verdict here contradicts §6: logging stays (metrics are off-path
  instrumentation, §6 decision 1 satisfied); anti-cheat stays (both dice
  prompt files are KEEP as server-dice delegation, decision 2, dice still
  resolving on the turn path); faction/living-world stays (faction agent
  and living-world prompt are KEEP/ADAPT to async ticks merged on the next
  turn, decision 3 — the tick machinery itself is outside this area and is
  not verdict here beyond the merge surface).

## Conflicts flagged (none silently contradicted)

- Run 1 provisional `agents.py` ADAPT → run 2 SPLIT: the semantic deletion
  is stricter, driven by the confirmed routing decision (Jev/model routing,
  embedding scorer deleted). No conflict with §6; the dispatch table and
  mode values stay.
- Run 1 provisional `prompt_loader.py` ADAPT → run 2 KEEP: no field-aware
  filtering exists in the file. No conflict.
- Run 1 provisional `prompt_context_metrics.py` ADAPT → run 2 KEEP: the
  async/non-mutating condition is already met. No conflict with §6 decision 1.
- Run 1 provisional dice "merge candidate" → REJECTED: the two dice files
  serve two genuinely different execution paths (tool_requests vs
  code_execution) and already share `shared/dice_notation_contract.md` via
  include; merging would reintroduce strategy branching into one file. Both
  are KEEP. No conflict with §6 decision 2 — both instruct delegation to
  server dice on the turn path.
- Run 1 provisional `dnd_srd_instruction.md` ADAPT (slim a full dump) →
  run 2 KEEP: the file is 77 lines, already a compact reference. The
  capacity concern was unfounded on the current text.
- Run 1 provisional `mechanics_system_instruction.md` ADAPT → run 2 KEEP:
  the file is an 8-line include manifest whose content lives in shared
  fragments that are themselves KEEP; the adaptation, if any, lives in the
  shared fragments, not the wrapper.
- Run 1 provisional `game_state_instruction.md` ADAPT → confirmed, narrowed
  to moving the faction activation block to the faction file and slimming
  via includes; the shape/protocol core is KEEP.
- `context_compaction.py` raising `MandatoryContextCapacityError` (HTTP 422)
  when mandatory instruction exceeds capacity sits in tension with the
  repo's UX-first rule ("never reject a player's turn over formatting/
  metadata errors"); this audit does not change the verdict (capacity
  rejection is a product decision, and the alternative — silently truncating
  mandatory instructions — is worse), but the tension is flagged here for
  the parent rather than resolved silently.
- The README's 8-file list vs. the ledger's ~30 vs. the actual 128: resolved
  in §1; both older sources are stale.
- `agents.py`'s module docstring still describes the semantic classifier as
  "PRIMARY BRAIN" and lists FastEmbed routing; that docstring is now false
  under the confirmed routing decision and must be rewritten when the
  semantic resolvers are deleted. Flagged, not silently corrected.

## §2 — Phase 2: `agents.py` (per symbol; caller counts from a full-tree search)

Caller counts below are references outside `agents.py` itself (production +
tests combined; a test-only count is still a count, and is labelled as such).
`get_agent_for_input` has 377 outside references (chiefly `llm_service.py`
and routing tests); `mode_advances_time` has 67; `validate_prompt_order`
15 (tests); `validate_all_agent_prompt_orders` 4 (tests);
`select_conclude_phase` 3 (conclude end-to-end tests);
`get_campaign_overlay_prompts` 13 (including `agent_prompts.py`).

### §2.1 Module helpers and constants

| Symbol | Justification (Pass A + Pass B) + verdict |
|---|---|
| `_to_state_dict` | Pass A: without a dict view of state, routing cannot read durable flags from either a `GameState` object or a plain dict, and the model cannot supply that translation from inside the log. Pass B: it is a pure shape adapter with no domain judgement — it copies no values, ranks nothing, and invents nothing. **KEEP** |
| `_level_up_instruction_cache_key`, `_level_up_finalize_fingerprint_blocks`, `_get_cached_level_up_instruction`, `_store_cached_level_up_instruction`, `_LEVEL_UP_INSTRUCTION_CACHE_MAX`, `_level_up_instruction_cache`, `_level_up_instruction_cache_lock` | Pass A: without memoization every level-up turn reallocates a ~1.5 MiB string (the file's own comment names this as the daily-job OOM driver), so deletion degrades capacity, not gameplay. Pass B: bounded LRU memoization of byte-identical output is squarely bounded capacity — it computes no availability, routes on no intent, and alters no model-owned signal (target_level > current_level is untouched). **KEEP** (all seven symbols; the lock is required because the cache is mutated across threads) |
| `_get_custom_campaign_state`, `_get_player_character_data`, `_get_rewards_pending`, `_resolve_gate` | Pass A: routing needs durable-state reads (custom state, PC data, rewards pending, dotted gate paths) that a bare log cannot provide as structured flags. Pass B: these are verbatim state extractions with truthy/dotted-path reading only; they decide nothing about what the values mean. **KEEP** |
| `get_campaign_overlay_prompts`, `_load_instruction_file_for_overlay` | Pass A: campaign overlays are how per-campaign content reaches the model at all; deleting them removes the only dynamic campaign-content path, which the model cannot invent. Pass B: overlay bodies are loaded through the shared prompt-body pipeline verbatim and are gated by enabled flags in state — prompt data assembly, not server domain authorship (campaign-agnosticism policy expressly allows this dynamic path). **KEEP** |
| `MANDATORY_FIRST_PROMPT`, `GAME_STATE_PLANNING_PAIR` | Pass A: without the head-order invariants (master directive first; game_state immediately followed by planning_protocol), prompt authority ordering becomes accidental and the model can be talked out of the hierarchy. Pass B: ordering prompt files is assembly, not a domain verdict — it says nothing about any campaign fact. **KEEP** |
| `EXPLICIT_SEMANTIC_INTENT_THRESHOLD` (0.8), `FACTION_SEMANTIC_INTENT_THRESHOLD` (0.7), `COMBAT_PRIORITY_CONFIDENCE` (0.6) | Pass A: these thresholds exist only to gate embedding-classifier outputs; once the scorer is deleted, no turn needs them and the model supplies nothing here. Pass B: confidence thresholds on a similarity scorer are the field-aware guess itself, not a registered exception, and they cannot survive the confirmed routing decision. **DELETE** (all three, with the semantic resolvers below) |
| `FACTION_FORCE_THRESHOLD` (20) | Pass A: faction mode needs a state gate, and army strength ≥ 20 is a durable state fact, not an intent guess — deleting it would route every small party into faction prompts. Pass B: a threshold on a persisted numeric state field, applied identically regardless of content, is a state gate, not a domain re-decision; it is verified here as state-gating (lines 3351/3412), not classifier-gating. **KEEP** |
| `LEVEL_UP_AUTHORING_EXEMPT_AGENTS`, `NON_TURN_ROUTING_AGENT_NAMES` | Pass A: these tables mark which agents may author level-up content and which are not turn routers; deleting them would let any agent author level-up state or let portrait routing leak into turns. Pass B: membership tables are routing metadata, but registry membership alone proves nothing — the exemption must be re-justified per agent when the tables are next touched, and any entry justified only by classifier behaviour deletes with the classifier. **ADAPT** (keep as explicit membership, prune classifier-justified entries on the same PR as the semantic deletion) |
| `validate_prompt_order` | Pass A: without head-invariant validation, a malformed agent prompt order ships silently and the model receives an authority-inverted prompt set. Pass B: validation of prompt-file order is assembly hygiene, not a domain decision, and it raises rather than rewriting anything. **KEEP** |
| `_is_spicy_mode_enabled` | Pass A: the spicy toggle is a persisted user setting; without reading it, the router cannot honour an explicit user preference. Pass B: reading a user setting is authorization/preference, not a domain guess — the setting, not the server, decides. **KEEP** |
| `PHASE_IN_PROGRESS`, `PHASE_AUDIT`, `LEVEL_UP_REPAIR_ATTACHED_KEY`, `LEVEL_UP_SAVED_CHOICE_ID_KEY`, `PHASE_CONCLUDE` | Pass A: level-up phases and repair/choice keys are the durable modal bookkeeping that keeps a multi-turn review coherent; a bare log cannot carry them as structured flags. Pass B: these are state keys, not values — naming a slot the model may fill is schema/transport, not authorship. **KEEP** |
| `character_creation_semantic_completion_allowed` | Pass A: free-text completion of character creation is exactly the modal-exit path the confirmed decision closes — the model can already say it is done in prose, which is why a server-side semantic "completion allowed" check is duplicative. Pass B: a semantic completion allowance is an embedding judgement about intent, and conclude guards must accept explicit signals only. **DELETE** (the explicit completion path in `_resolve_character_creation_completion` survives) |
| `character_creation_semantic_exit_allowed`, `_detect_conclude_signal` (agents.py wrapper) | Pass A: the modal-exit question is answered by an explicit finish-choice id; a semantic exit allowance adds no player capability the explicit path lacks. Pass B: the wrapper currently accepts a domain finish-choice id OR a FastEmbed exit-intent (it passes `classify_level_up_exit_intent` / `classify_cc_exit_intent` into `modal_conclude_policy.detect_conclude_signal`); the choice-id branch is transport, the FastEmbed branch is a deleted guess. **ADAPT** (keep the explicit-choice branch only; delete the classifier arguments and any semantic fallback — the prompt side is already clean, §5) |
| `_build_conclude_prompt_order`, `select_conclude_phase` | Pass A: on a conclude turn the in-progress domain prompt must be swapped for its conclude variant, or the model receives contradictory instructions (continue vs. finalize) in one turn. Pass B: swapping prompt files on a durable modal-phase flag is prompt assembly driven by state, not a re-decision about content. **KEEP** (after the `_detect_conclude_signal` adaptation above; `select_conclude_phase` itself takes flow-state, not raw intent) |

### §2.2 `BaseAgent` and `FixedPromptAgent`

| Symbol | Justification + verdict |
|---|---|
| `BaseAgent.__init__`, `BaseAgent.prompt_builder` | Pass A: every agent needs a bound state and a builder; without them no prompt set can be assembled for any turn. Pass B: construction and accessor plumbing carry no domain judgement. **KEEP** |
| `BaseAgent.level_up_repair_block` | Pass A: a pending level-up repair must ride the routed turn or the repair is silently dropped mid-review. Pass B: it returns a prompt contract block (plus a class row) for the model to apply — assembly, not server rewriting of the sheet. **KEEP** |
| `BaseAgent.advances_time` (default True) | Pass A: the turn path needs a default time-advancement answer for modes that do not override it, or living-world merging has no gate. Pass B: the default is dispatch metadata consumed by the async-tick merge gate (§6 decision 3), not a filter on model output; per-mode overrides below carry the actual semantics. **KEEP** (as merge-gate metadata; the narrative time rule itself lives in prompts) |
| `BaseAgent.build_system_instructions` | Pass A: this is the prompt-assembly entry point — deleting it deletes the game. Pass B: it delegates to the builder with the agent's ordered prompt set; assembly passes, and any field-aware choice inside is verdict in `agent_prompts.py`, not here. **KEEP** |
| `BaseAgent.matches_input` (default False), `BaseAgent.matches_game_state` (default False), `BaseAgent.preprocess_input` (identity) | Pass A: safe defaults matter — an agent that matched everything by default would hijack turns, and identity preprocessing preserves the player's exact words. Pass B: defaults that refuse to guess are the ZFC-correct shape; the guessing lives in the overrides verdict below, not here. **KEEP** |
| `BaseAgent.get_all_prompts`, `BaseAgent.prompt_order`, `BaseAgent.builder_flags` (default `include_debug: False`), `BaseAgent.requires_action_resolution` (default True), `BaseAgent.__repr__` | Pass A: prompt-set union, ordered prompt types, builder flags, the action-resolution requirement, and a debuggable repr are all assembly/observability plumbing without which the turn path cannot be operated. Pass B: none of these reads, ranks, or rewrites a campaign fact; `requires_action_resolution` declares a response-shape requirement (the audit trail), not a domain verdict. **KEEP** |
| `BaseAgent.validate_prompt_order`, `BaseAgent._ensure_prompt_order_valid` | Pass A: per-agent order validation catches authority-inversion before a turn ships. Pass B: raising on invariant violation is assembly hygiene, not domain authorship. **KEEP** |
| `FixedPromptAgent.build_system_instructions` | Pass A: fixed-prompt agents (god, think, info, rewards) need exactly one assembly path or their prompt sets drift per turn. Pass B: it builds from `REQUIRED_PROMPT_ORDER` and builder flags via the shared builder — assembly, with campaign overlays appended after required/optional prompts so generic contracts apply first. **KEEP** |
| `NarrativeFamilyAgent` (class, no methods) | Pass A: the narrative family groups story/dialog/spicy agents so shared narrative behaviour has one home; deleting the class forces duplication into each subclass. Pass B: a grouping base class with no behaviour of its own makes no domain decision. **KEEP** |

### §2.3 Concrete agent classes (prompt set + mode behaviour)

| Symbol | Justification + verdict |
|---|---|
| `StoryModeAgent.build_system_instructions`, `StoryModeAgent.build_system_instruction_parts`, `StoryModeAgent.builder_flags`, `StoryModeAgent.matches_input` | Pass A: story mode is the default turn — without it there is no game for ordinary input, and its parts-builder is how the narrative prompt set is assembled. Pass B: matching "any non-god-mode input" as a *default fallback* (not a classification) is transport; the class adds no intent guess, and its debug flag is observability. **KEEP** |
| `GodModeAgent.build_system_instructions`, `GodModeAgent.advances_time` (False), `GodModeAgent.prompt_order`, `GodModeAgent.matches_input`, `GodModeAgent.preprocess_input`, `GodModeAgent.requires_action_resolution` (False) | Pass A: god mode is the administrative pause menu — without it there is no admin path, and freezing time during admin turns is the product promise itself. Pass B: matching is by explicit `"GOD MODE:"` prefix or explicit `mode="god"` (authorization, not guessing); the warning inserted after the prefix preserves prefix matching while labelling the turn administrative, and not requiring action resolution for an admin turn is a shape decision, not a domain verdict. **KEEP** (prompt set kept only behind authorization, per §6-adjacent product promise) |
| `CharacterCreationAgent.__init__`, `.advances_time` (False), `.prompt_order`, `.validate_prompt_order`, `.build_system_instructions`, `.matches_game_state`, `.matches_input`, `.requires_action_resolution` (False) | Pass A: character creation is a pause/menu flow that must not advance time and must not be escapable by ordinary story input; its focused prompt stack and explicit-exit input matching are what keep the modal coherent. Pass B: state-driven matching (creation active flag) plus deterministic modal-exit choice matching are explicit/state routing, not intent guessing — provided the semantic completion branch (§2.1) is deleted, which this class's verdict assumes. **KEEP** (conditional on the §2.1 semantic deletion) |
| `CharacterCreationAgent.reducer_replace_list_paths` | Pass A: the CC backpack snapshot needs a declared replacement path or a turn cannot replace the snapshot it just built. Pass B: this is a durable-write allowlist for an explicit CC action, not a rewrite of model-authored values — it authorizes a write shape the model already chose. **KEEP** |
| `LevelUpAgent.__init__`, `.advances_time` (pause for review; gameplay turns advance), `.prompt_order`, `.validate_prompt_order`, `.build_system_instructions`, `.matches_input` (state-driven; input does not force it), `.requires_action_resolution` (False) | Pass A: level-up review is a pause flow whose focused prompt stack (including the ~385K-char instruction, hence the §2.1 cache) cannot be replaced by a bare log, and input must not force it or a story sentence would hijack a review. Pass B: state-driven selection plus explicit review choices are the approved routing shapes; the build path is assembly with a capacity cache. **KEEP** |
| `PlanningAgent.advances_time` (False), `.matches_input` (THINK: prefix or explicit mode), `.preprocess_input`, `.requires_action_resolution` (False) | Pass A: think mode is a mental pause that must not advance time, and its trigger is an explicit prefix/mode the player or UI sets. Pass B: explicit-override routing is the paradigm case of allowed routing — the server honours a stated mode rather than inferring one. **KEEP** |
| `INFO_QUERY_PATTERNS`, `STORY_ACTION_VERBS` | Pass A: these pattern tables exist to support `InfoAgent.matches_input`'s "conservative detection" of info-only queries. Pass B: pattern-based intent detection is keyword/substring routing — the very shape the confirmed routing decision replaces with Jev/model routing — and no registered exception covers it. **DELETE** (with `InfoAgent.matches_input` below) |
| `InfoAgent.advances_time` (False), `.requires_action_resolution` (False) | Pass A: info queries are pure retrieval that must not advance time or demand an action-resolution trail. Pass B: both are dispatch metadata about the mode, not domain judgements. **KEEP** (the class survives as the `mode="info"` dispatch target; only its input matcher deletes) |
| `InfoAgent.matches_input` | Pass A: the model, given an explicit info mode or self-routing, can answer equipment/inventory queries without the server pre-classifying the question — no player capability depends on this matcher. Pass B: "conservative detection" of info-only queries is server intent-guessing by pattern, failing strict ZFC and the confirmed routing decision. **DELETE** |
| `CombatAgent.build_system_instructions`, `.builder_flags`, `.matches_game_state`, `.matches_input` (never by input, only by state) | Pass A: active combat must force combat prompts or combat turns would be narrated as ordinary story; the state flag `in_combat` is durable and unambiguous. Pass B: state-flag routing plus prompt assembly passes, and the class's explicit refusal to match on input is the ZFC-correct shape. **KEEP** |
| `RewardsAgent.advances_time` (False), `.requires_action_resolution` (False), `.builder_flags`, `.matches_game_state`, `.matches_input` (never by input, only by state) | Pass A: pending rewards must resolve before story continues, and rewards processing is administrative (no time advance); the `rewards_pending` durable flag is the trigger. Pass B: state-flag routing is allowed routing, and the debug flag is observability. **KEEP** |
| `DeferredRewardsAgent.build_system_instructions`, `.should_run_deferred_check` | Pass A: deferred rewards are a parallel check that must not hijack ordinary turns; the scene-count gate is what keeps it parallel. Pass B: a turn-count scheduling gate is capacity/scheduling metadata, not a domain verdict about any reward — it decides *when* to check, never *what* is owed. **KEEP** (as a scheduling gate; the reward decision itself stays model-owned) |
| `DialogAgent.builder_flags`, `.matches_input` (always False), `.matches_game_state` | Pass A: dialog must continue an active session without being triggerable by a typed phrase, or any story sentence mentioning conversation would hijack the turn. Pass B: refusing input matching outright and routing only on an active-session state flag is the approved shape. **KEEP** |
| `HeavyDialogAgent.builder_flags` | Pass A: escalated dialog needs the same debug-off, focused prompt behaviour as dialog, or high-stakes scenes would leak debug instructions into the prompt. Pass B: a flag override carries no domain judgement. **KEEP** |
| `_normalize_spicy_toggle_input`, `_is_spicy_toggle_phrase`, `SPICY_TOGGLE_ENABLE_PHRASES`, `SPICY_TOGGLE_EXIT_PHRASES`, `SPICY_TOGGLE_UI_PREFIXES` | Pass A: the spicy toggle is an explicit user command ("enable/disable spicy mode" phrases and UI prefixes); without normalizing and recognizing exactly those phrases, the toggle cannot be honoured. Pass B: exact-phrase recognition of an explicit user command is honoring a stated preference, not inferring intent from prose — the phrases are a command vocabulary, not a semantic guess. **KEEP** |
| `SpicyModeAgent.build_system_instructions`, `.matches_game_state` | Pass A: spicy mode needs its literary prompt set, selected by the persisted `user_settings.spicy_mode` toggle, or intimate scenes fall back to default narration. Pass B: toggle-state routing is user-preference authorization, and the build preserves default-world lore when enabled rather than rewriting it. **KEEP** |
| `FactionManagementAgent.__init__`, `._detect_minigame_enabled`, `.minigame_enabled`, `.get_tools`, `.build_system_instructions`, `.matches_game_state` | Pass A: faction/army management (forces ≥ 20, minigame enabled) needs its prompt set and its faction tools, or army turns have no mechanics surface; the class already does "no forced routing" (it logs minigame state). Pass B: state-gated tool provision is tool execution (allowed), and per §6 decision 3 the *tick execution* moves async with results merged on the next turn — this class is the merge surface, not the tick engine. **KEEP** (as the merge surface; ADAPT the tick machinery outside this group to async — flagged, not verdict here) |
| `CampaignUpgradeAgent.requires_action_resolution` (False), `.__init__`, `.build_ceremony_instructions`, `.build_system_instructions`, `.matches_game_state`, `.matches_input` (never by input, only by state) | Pass A: ascension ceremonies (divine/sovereign) are state-gated setup events whose dynamic ceremony block must be built for the request tail, or the ceremony has no prompt surface. Pass B: state-flag routing plus dynamic prompt assembly passes; refusing input matching keeps ceremonies from being talked into existence. **KEEP** |
| `PortraitGeneratorAgent.advances_time` (False), `.matches_input` (False), `.matches_game_state` (False), `.build_suggest_system_instruction` | Pass A: portrait suggestion is not turn routing at all (the class docstring says so), and its suggest instruction is a bounded subset of three prompt files for an image-description task. Pass B: hard truncation to a policy `max_chars` (default 1200) is capacity handling, but mid-string truncation with an ellipsis can cut a contract mid-sentence — the subset selection is sound, the cut is crude. **ADAPT** (keep the three-file subset and the not-a-router flags; replace blind truncation with a budget-aware subset/contract-preserving cut) |
| `ALL_AGENT_CLASSES`, `__all__` | Pass A: validation (`validate_all_agent_prompt_orders`) and imports need a canonical class registry, or an agent can silently drop out of validation. Pass B: a registry of classes is metadata; per the spec, membership alone justifies nothing — but these tables justify nothing by themselves either, they only enumerate. **KEEP** (as enumeration only) |

### §2.4 Routing resolvers and dispatch (the core of the run-2 revision)

Order below follows `_ROUTING_RESOLVERS` order. "Explicit" = player prefix,
explicit mode param, explicit choice/click id, or API mode. "State" = a
durable flag in game state. "Semantic" = embedding-classifier output.

| Symbol | Justification + verdict |
|---|---|
| `_RoutingState` (class, no methods) | Pass A: threading one computed routing context through 17 resolvers avoids recomputing state flags per resolver and keeps resolver order auditable. Pass B: a context carrier makes no decision itself; its classifier-derived fields delete with the classifier (see `_extract_routing_state`). **ADAPT** (keep the carrier; drop classifier-derived fields) |
| `_should_skip_classifier_context` | Pass A: its entire purpose is dropping classifier context on first turns / CC–level-up bleed — a workaround for classifier behaviour. Pass B: with the scorer deleted there is no classifier context to skip, and the function cannot be repurposed without reintroducing a guess. **DELETE** |
| `_custom_campaign_flag_or_top` | Pass A: resolvers need one helper to read a flag from custom state or its top-level alias, or flag checks diverge per resolver. Pass B: verbatim flag reading with an alias fallback is state access, not interpretation. **KEEP** |
| `_extract_routing_state` | Pass A: computing all state-derived routing flags once up front is what makes the 17-resolver dispatch deterministic and auditable; a bare log cannot provide these as structured flags. Pass B: the state-flag extraction passes, but the function also threads classifier context into `_RoutingState` for `_resolve_semantic_classification` / `_resolve_semantic_intent` — that half is a deleted guess's plumbing. **ADAPT** (keep state-flag computation; delete classifier-context fields and the `_should_skip_classifier_context` call) |
| `_resolve_god_mode` | Pass A: god mode must outrank everything (except an active CC modal lock, which this resolver respects) or an admin command would be narrated as story. Pass B: explicit-prefix/explicit-mode routing plus a modal-lock guard is authorization plus state — the approved shapes. **KEEP** |
| `_resolve_planning_explicit` | Pass A: THINK: prefix / explicit think mode must outrank semantic routing or planning turns would be classified as story. Pass B: explicit override, paradigm-approved. **KEEP** |
| `_resolve_level_up_review_reopen` | Pass A: an explicit level-up review choice must reopen the review modal or the player's click does nothing. Pass B: explicit choice-id routing. **KEEP** |
| `_resolve_level_up_entry` | Pass A: a level-up entry click must bypass campaign-upgrade routing or the click lands in the wrong modal. Pass B: explicit click routing. **KEEP** |
| `_resolve_conclude_phases` | Pass A: a finish signal on an active modal must be owned by the conclude phase or the modal never finalizes. Pass B: the phase selection itself is state-driven, but it currently consumes `_detect_conclude_signal`, whose semantic branch must go (§2.1) — after that adaptation this resolver is pure explicit/state routing. **ADAPT** (keep; consume only the explicit-choice branch of the conclude signal) |
| `_resolve_character_creation_completion` | Pass A: explicit completion must exit character creation to story mode or the player is trapped in the modal after finishing. Pass B: explicit completion is approved; the resolver also currently consults `character_creation_semantic_completion_allowed` — that consultation deletes with §2.1. **ADAPT** (keep explicit completion; delete the semantic-completion consultation) |
| `_resolve_modal_char_creation_lock` | Pass A: the CC modal lock is the guarantee a bare log cannot supply — that a modal flow is not silently abandoned mid-flow by an ordinary story turn. Pass B: a durable modal-state lock with explicit-only exit is transport/state-machine, not a domain decision. **KEEP** (with explicit-only exit per the confirmed decision) |
| `_resolve_campaign_upgrade`, `_resolve_combat_state` | Pass A: upgrade availability and active combat are durable state facts that must select their agents before any intent question arises, or ceremonies/combat would be narrated away. Pass B: pure state-flag routing. **KEEP** |
| `_resolve_spicy_mode_override` | Pass A: a persisted user toggle must authoritatively select the spicy agent for narrative turns or the toggle is decorative. Pass B: user-setting routing is preference authorization. **KEEP** |
| `_resolve_semantic_classification` | Pass A: this resolver runs the embedding classifier early and caches its intent onto state — under Jev/model routing the model itself (or Jev's Choice) supplies the mode, so no player capability depends on this step. Pass B: it is the embedding-similarity guess itself, with a "security safeguard" that merely excludes god/think from classifier output — a safeguard on a guess does not convert it into an exception. **DELETE** |
| `_resolve_rewards` | Pass A: pending rewards must resolve before character creation, and the resolver's combat-priority deferral (in-combat, or classifier MODE_COMBAT ≥ 0.6) is what keeps rewards from clobbering combat. Pass B: the state half (rewards pending + in-combat flags) passes; the classifier-confidence half deletes with the thresholds (§2.1). **ADAPT** (keep the state-based rewards-before-creation rule and the in-combat deferral; delete the classifier-confidence deferral) |
| `_resolve_character_creation_state`, `_resolve_dialog_state` | Pass A: creation-active and dialog-active state flags must select their agents after rewards, or modal/session continuity breaks. Pass B: state-flag routing passes; `_resolve_dialog_state` also shares the 0.7 faction threshold gate with the semantic path — that gate deletes, and the active-session branch stays. **ADAPT** (keep state branches; delete the classifier/faction-threshold gate in the dialog resolver) |
| `_resolve_semantic_intent`, `_SEMANTIC_INTENT_HANDLERS`, `_semantic_info`, `_semantic_combat`, `_semantic_rewards`, `_semantic_deferred_rewards`, `_semantic_level_up`, `_semantic_character_creation`, `_semantic_faction`, `_semantic_campaign_upgrade`, `_semantic_dialog`, `_semantic_dialog_heavy`, `_semantic_spicy` | Pass A: these 11 handlers plus their dispatcher are the "PRIMARY BRAIN" — the embedding scorer's second dispatch pass, routing to info/combat/rewards/deferred/level-up/creation/faction/upgrade/dialog/heavy-dialog/spicy on classifier output. Under the confirmed routing decision (Jev Choice over agent modes, or model self-routing), the mode comes from Jev/the model, so deleting this pass removes no player capability that the replacement does not supply. Pass B: every handler is a field-aware re-decision of what the player meant, with routing-priority labels (`7_semantic_*`) that dress a guess as a priority — no registered exception covers any of them, and several carry their own hazards (semantic level-up entry freezing time on a misfire, semantic spicy routing regardless of toggle state, semantic dialog as the only dialog-initiation path). **DELETE** (all 13 symbols; dialog initiation moves to explicit mode / Jev Choice / active-session state, and `_resolve_dialog_state`'s state branch covers continuation) |
| `_resolve_explicit_mode` | Pass A: API explicit mode (god, think, deferred_rewards and other user-facing modes) is how the UI forces a mode without typing a prefix; deleting it removes the UI's mode control. Pass B: explicit mode params are stated intent, and the resolver's "USER-FACING MODES ONLY" restriction correctly refuses internal modes. **KEEP** |
| `_resolve_rewards_fallback` | Pass A: a late state fallback catches rewards pending that earlier resolvers missed, so a missed reward does not silently vanish when semantic routing falls through. Pass B: as a state fallback it passes; its current justification ("when semantic routing fell through") is obsolete and its trigger must be re-expressed as a pure pending-rewards state check. **ADAPT** (keep as a state fallback; reword its trigger off the deleted semantic pass) |
| `_default_story_mode` | Pass A: a default is required or an unmatched turn has no agent at all; story mode as the default is the game's baseline. Pass B: a default fallback is not a classification — it claims nothing about intent, it only guarantees a prompt set. **KEEP** |
| `is_explicit_review_route` | Pass A: distinguishing an explicit review route from optional model selection metadata is what keeps review routing from being talked into by model output. Pass B: it defers to the router's decision rather than to model metadata — an authorization-shaped check. **KEEP** |
| `attach_pending_level_up_repair` | Pass A: a pending repair must ride the routed turn regardless of which agent won, or the repair is lost when routing changes mid-review. Pass B: attaching a prompt block is assembly; the function explicitly never changes the winner, which is the correct restraint — but it must not become a vehicle for server-side sheet rewriting (none is present in this file). **KEEP** (as a ride-along prompt attachment only) |
| `_level_up_modal_in_progress_flag` | Pass A: the level-up modal flag has one canonical nested home; without a single accessor, resolvers read divergent flags and the modal leaks. Pass B: a canonical flag accessor is state plumbing. **KEEP** |
| `_ROUTING_RESOLVERS`, `_RoutingResolver` | Pass A: the ordered dispatch table is what makes routing auditable — order is load-bearing and documented as exactly the original if-chain sequence. Pass B: a table of resolvers is dispatch metadata; its verdict is the verdict of its members (keep explicit/state members, delete semantic members). **ADAPT** (keep the table shape and order; remove `_resolve_semantic_classification`, `_resolve_semantic_intent`, and `_should_skip_classifier_context` from it, and keep mode values unchanged for Jev) |
| `get_agent_for_input` | Pass A: this factory is the single entry point the turn path uses to select an agent; deleting it deletes routing entirely. Pass B: its shape (build state once, first non-None resolver wins, else story default, attach repair ride-along) passes once its semantic members are deleted — the docstring's "PRIMARY BRAIN" description and priority list must be rewritten on the same PR. **ADAPT** (keep the factory and its order; delete semantic members; rewrite the docstring) |
| `mode_advances_time`, `_MODE_ADVANCES_TIME_CACHE` | Pass A: living-world merging, time gating, and modal pauses all need a mode→time answer the model cannot supply as a structured flag. Pass B: the table is dispatch metadata consumed by the async-tick merge gate; it must not be used to filter or rewrite model-authored time values (no such use is present in this file). **KEEP** (as merge-gate metadata) |
| `validate_all_agent_prompt_orders` | Pass A: validating every agent's prompt order at once catches authority-inversion across the whole set, not just one agent. Pass B: validation that raises/returns errors without rewriting anything is assembly hygiene. **KEEP** |

## §3 — Phase 2: `agent_prompts.py` (per symbol)

Caller counts (outside `agent_prompts.py`): `PromptBuilder` 359 references
(chiefly `agents.py`, `llm_service.py`, tests); `get_static_prompt_parts` 47;
`get_current_turn_prompt` 19; `load_dice_instructions` 24;
`load_detailed_sections` 21; temporal builders 13. `PATH_MAP` is referenced
throughout the builder and loader paths. Module-level caches
(`_SCHEMA_DOC_CACHE`, `_FULL_CANONICAL_GAME_STATE_SCHEMA_JSON`,
`_LITE_CANONICAL_GAME_STATE_SCHEMA_JSON`, `_STATE_EXAMPLE_CACHE`,
`_loaded_instructions_cache`, `_current_request_loaded_files`) are capacity
plumbing and are **KEEP** as a group: they memoize file/schema reads and
per-request tracking, alter no content, and are cleared/tracked per request
(`clear_loaded_files_tracking`, `get_loaded_instruction_files` — **KEEP**).

### §3.1 Loading, schema docs, and prompt surgery

| Symbol | Justification + verdict |
|---|---|
| `AgentProtocol.prompt_order`, `AgentProtocol.builder_flags` | Pass A: the builder needs a protocol for "what order, what flags" or every agent build becomes ad hoc. Pass B: an interface declares shape, not content. **KEEP** |
| `_is_comment_stripping_enabled`, `_strip_prompt_comments`, `_STRIP_BLOCK_PATTERNS` | Pass A: HTML comment-only content in prompt files is dead weight in context; stripping it saves tokens without changing any instruction the model sees. Pass B: removing comments is formatting/capacity, not a domain decision — provided stripping never removes visible instruction text (the patterns are comment-scoped). **KEEP** |
| `_format_directive_scope` | Pass A: god-mode directives must reach the model verbatim for the directive's audience fields, or admin intent is paraphrased away. Pass B: verbatim rendering of model-owned directive fields is faithful transport. **KEEP** |
| `PATH_MAP`, `_PROMPT_PATH_MAP_SOVEREIGN_EXTRAS`, `_NARRATIVE_FILE_HEADERS`, `SECTION_TO_PROMPT_TYPE`, `DETAILED_INSTRUCTION_SECTIONS` | Pass A: without a prompt-type → file map, no prompt can be loaded at all; the sovereign extras and section maps extend it to ascension and detailed-section routing. Pass B: a registry is load metadata — but per the spec, membership alone justifies nothing, so each entry's *use* is verdict where it is used (§3.3, §5); the map itself makes no domain choice. **KEEP** (as a map only; field-aware uses built on it are verdict separately) |
| `init_schema_doc_cache`, `_ensure_schema_cache_warmed`, `_ensure_warmed_attempted`, `_ensure_warmed_lock`, `get_cached_schema_doc`, `_schema_to_json_string` | Pass A: schema docs must be available at build time without re-reading and re-serializing files per turn. Pass B: warming/caching/serialization are capacity/transport; the lock exists because warming races across threads. **KEEP** |
| `generate_state_example`, `_generate_example_from_def` | Pass A: the game-state file embeds `{{STATE_EXAMPLE:...}}` placeholders that must resolve to valid examples, or the model receives an unresolvable placeholder instead of a shape example. Pass B: generating examples *from the registered schema itself* is schema-faithful formatting, not invented content — the examples cannot contradict the schema they derive from. **KEEP** |
| `_inject_schema_placeholders`, `_inject_dynamic_schema_docs` | Pass A: without schema docs in context, the model cannot know the response shape the parser expects, and parsing breaks. Pass B: injecting the canonical schema is transport — but the *choice* of which defs are documented vs. stubbed (below) is where field-awareness enters, so the injectors themselves pass only as carriers. **KEEP** (as carriers; the selection logic is verdict in the next rows) |
| `_strip_descriptions_from_schema` | Pass A: schema descriptions bloat context without changing the shape the model must emit. Pass B: deleting description text is capacity trimming of metadata, not of fields — no field is hidden, only its prose gloss. **KEEP** |
| `_filter_location_schema_fields` | Pass A: server-owned and mirrored location properties must not be presented as model-authorable fields, or the model will author values the server then has to discard or overwrite. Pass B: this is a field-aware filter, and it passes only under a named exception — *server-owned storage fields must not be presented as model-authorable* (durable-write integrity, not a domain preference). It fails if it ever filters a model-owned field; the current filter is scoped to server-owned/mirrored properties. **ADAPT** (keep the server-owned exclusion only, with that exception named in a comment; delete any model-owned field filtering if added) |
| `_load_lite_defs_documented_by_schema_placeholders`, `_LITE_DEFS_DOCUMENTED_BY_SCHEMA_PLACEHOLDERS`, `_LITE_DEFS_DOCUMENTED_BY_SCHEMA_PLACEHOLDERS_PATH`, `_make_lite_placeholder_stub`, `_composed_def_properties`, `_get_standard_lite_schema` | Pass A: the lite schema exists so dialog/light turns do not pay full-schema context costs — a capacity need, not a gameplay need. Pass B: pruning a schema to a "lite" subset *is* field-aware hiding, and it passes only as a disclosed capacity exception tied to a registered contract: the lite subset must be exactly the defs whose docs the prompt already carries (the placeholders JSON), with stubs that preserve every documented property's contract. A lite subset chosen by server preference about what matters would fail. **ADAPT** (keep only the contract-tied lite subset; move the subset definition into the schema contract, not code preference) |
| `_field_doc_dedupe_pointer`, `_FIELD_DOC_LINE`, `_DROPPED_FIELDS_POINTER`, `_dedupe_repeated_field_docs` | Pass A: repeating every field definition in every prompt section wastes context and invites contradiction between copies. Pass B: stating each definition once and pointing at the dropped copies is formatting/dedupe — it hides nothing, since the pointer names the omission and its count. **KEEP** |
| `extract_dc_calibration_ledger`, `_DC_CALIBRATION_LEDGER_BEGIN`, `_DC_CALIBRATION_LEDGER_END` | Pass A: the DC ledger must be extractable as one exact block for reuse, or DC calibration text is duplicated inconsistently across prompts. Pass B: verbatim block extraction is prompt surgery without rewriting values — it passes as a move, but fails the moment it edits a ledger value, so the "exact block" discipline is load-bearing. **ADAPT** (keep as verbatim block move only; any value editing deletes) |
| `_resolve_prompt_includes` | Pass A: `{{PROMPT_INCLUDE:...}}` is how 32 shared fragments reach the model; without recursive resolution, mechanics/dice prompts arrive as unresolved placeholders. Pass B: verbatim include expansion with traversal blocking and cycle detection is transport plus authorization (path confinement) — it adds no content of its own. **KEEP** |
| `_srd_feature_rules_block` | Pass A: class features through the character's level must reach the model or level-up/mechanics turns are decided without the rules that govern them. Pass B: selecting *which* SRD sections the model sees by (game_system, class, level, subclass) is field-aware selection — it passes only as a capacity exception keyed to the saved sheet (sending the whole SRD every turn is the capacity problem §5's SRD verdict already prices), and the selection rule belongs in the prompt/schema contract, not as silent code preference. **ADAPT** (keep as capacity-bounded selection keyed to the saved sheet; document the exception; delete any selection keyed to model-inferred rather than saved values) |
| `_load_instruction_file`, `_load_typed_field_instruction`, `_load_prompt_body_from_path` | Pass A: these are the main prompt-loading path — deleting them deletes prompt assembly. Pass B: file-cache reads plus the canonical transformation pipeline (include expansion, integrity/leveling placeholder injection, schema placeholders, comment stripping, non-empty validation, `# File:` header) are transport and formatting; failing hard on unreadable files prevents sending incomplete instructions, which is safer than silent degradation. **KEEP** |
| `get_story_continuation_priority_instruction`, `get_streaming_story_continuation_priority_instruction`, `get_require_reward_event_instruction` | Pass A: continuation-priority and reward-event requirements are single-source prompt fragments that multiple paths must share verbatim, or they fork. Pass B: loading a registered prompt verbatim (with header validation for typed fields) is transport; the streaming variant is a pure alias. **KEEP** |
| `load_dice_instructions`, `_dice_instructions_already_loaded`, `_append_dice_instructions` | Pass A: dice instructions must be present exactly once per turn or the anti-cheat delegation breaks (absent) or doubles (duplicated). Pass B: strategy-keyed loading (tool_requests vs. code_execution) is execution-path selection, and the already-loaded guard prevents duplication — both are transport, and the delegation content itself is verdict in §5. **KEEP** (dice resolution stays on the turn path per §6 decision 2; this loader is on that path by design) |
| `_append_game_state_mechanics_appendix` | Pass A: mechanics-capable agents need the detailed game-state mechanics appendix or their mechanics turns lack the detailed rules. Pass B: appending a registered prompt file to a prompt set is assembly; the appendix's own content is verdict in §5. **KEEP** |
| `_get_custom_campaign_state_for_prompts` | Pass A: prompt builders need custom state reads to decide campaign-specific assembly (setting, tier, overlays). Pass B: verbatim state extraction, no interpretation. **KEEP** |
| `load_detailed_sections`, `extract_llm_instruction_hints`, `SOCIAL_HP_EARLY_REMINDER`, `SOCIAL_HP_ENFORCEMENT_REMINDER` | Pass A: detailed sections let the model request (via hints in its own previous response's debug metadata) the instruction detail it needs, instead of receiving all of it every turn. Pass B: model-requested selection is model-driven, so it passes — the server is not choosing what matters, the model's own hint is; the social-HP reminders are prompt fragments, verdict with their content in §5. **KEEP** (for the hint-driven path; any server-added section not hinted by the model would be ADAPT/DELETE — none is present in this path) |
| `_add_world_lore_to_system`, `_add_banned_names_to_system` | Pass A: world lore and the global naming-restriction section must reach the system prompt or lore/naming rules silently vanish for turns that do not otherwise load them. Pass B: appending registered prompt data is assembly; banned-names content is a global policy prompt, not a server filter on output. **KEEP** |
| `_load_companion_field_contract`, `_COMPANION_FIELD_CONTRACT_PATH` | Pass A: companion projection needs an ordered field/bounds contract or every builder invents its own truncation. Pass B: loading a contract JSON file is data loading; the contract's authority is verdict with its consumers below. **KEEP** |

### §3.2 Companion machinery (rendering vs. selection — the split matters)

Rendering/bounding helpers are capacity/formatting and pass; selection/merge
helpers that decide *which* records count as companions, or *what* a record
means, are field-aware and need the adaptation stated.

| Symbol | Justification + verdict |
|---|---|
| `_render_companion_field_value`, `_companion_equipment_item_name`, `_render_companion_equipment_summary`, `_truncate_injury_text`, `_INJURY_TRUNCATION_MARKER`, `_injury_identity`, `_format_single_injury_dict`, `_partition_injuries`, `_overflow_marker`, `_description_allowances`, `_render_permanent_parts`, `_select_identity_prefix`, `_count_only_rendering`, `_render_companion_injuries_summary`, `_render_permanent_summary`, `_render_temporaries_only`, `_render_single_injury`, `_non_empty_str` | Pass A: companion/injury blocks must fit a char budget with explicit markers, or long companion histories crowd out story context. Pass B: bounded rendering with explicit truncation/overflow markers and accurate omission counts is capacity formatting that hides nothing silently — the marker *is* the disclosure. **KEEP** (all 18 symbols as a rendering family) |
| `_traverse_path`, `_extract_entity_id` | Pass A: companion code needs path-walking and canonical-id extraction to read structured records at all. Pass B: pure structural access, no judgement about identity. **KEEP** |
| `_has_former_companion_membership`, `_has_inactive_status`, `_is_companion_status_dead`, `_is_companion_deceased` (PromptBuilder) | Pass A: departed/hostile/deactivated/dead status must be readable or the model would resurrect or re-recruit the departed. Pass B: these read persisted lifecycle status fields verbatim — durable-state predicates, not inferences. **KEEP** |
| `_is_companion_via_contract`, `_resolve_companion_relationship` | Pass A: companion detection and relationship descriptors must come from somewhere stable, or every builder guesses differently. Pass B: detection driven by the contract JSON's `detection_paths` and a descriptor resolver keyed to stored info is contract-driven assembly — it passes only while the contract, not code preference, defines the paths. **KEEP** (contract-driven; if a path is added in code rather than in the contract JSON, that addition is DELETE) |
| `_is_companion_shaped`, `_has_ambiguous_entity_identity` | Pass A: shape checks and ambiguity detection exist to avoid merging the wrong legacy mirror into a canonical record — a real merge hazard. Pass B: both are server *inferences* about identity (shape guessing, ambiguity guessing) that second-guess stored records; the contract already defines detection, so inference adds a second, unregistered decision-maker. **DELETE** (merge only on contract detection + canonical key match; on ambiguity, surface both records to the model instead of server-choosing) |
| `_project_companions_with_npc_data`, `_sync_companions_with_npc_data`, `_match_canonical_npc_record` | Pass A: legacy companion mirrors and canonical `npc_data` must be reconciled or the model receives two contradictory companion records for one person. Pass B: projection of canonical fields over legacy mirrors is field-aware merging, and it passes only under a named exception — *canonical npc_data is the server-persisted identity record, and projection is limited to identity fields the contract names* (durable-write integrity). Any projection of non-identity fields (status, injuries, relationships) by server preference fails. **ADAPT** (keep identity-field projection only, contract-named; delete non-identity projection and any inferred match) |
| `select_identity_directives_by_budget`, `select_directives_by_budget` (module-level and `PromptBuilder` methods) | Pass A: directives (god-mode directives, identity directives) must fit a token budget or they crowd out the turn. Pass B: newest-first selection within a budget is recency ordering under a capacity cap — a neutral ordering, not a domain ranking — and the budget itself is capacity. **KEEP** |

### §3.3 `PromptBuilder` (59 methods) and module entry points

| Symbol | Justification + verdict |
|---|---|
| `PromptBuilder.__init__`, `._load_for_build`, `.last_identity_block`, `.last_directives_block`, `.record_evidence_blocks` | Pass A: the builder needs state, a load path, and evidence capture for debugging what the model was actually sent. Pass B: construction, loading, and evidence recording are transport/observability; evidence blocks are copies of what was sent, not new decisions. **KEEP** |
| `PromptBuilder._append_game_state_with_planning`, `._append_campaign_setting_if_present`, `.build_from_order`, `.build_for_agent`, `.build_core_system_instructions`, `.add_character_instructions`, `.add_selected_prompt_instructions`, `.add_system_reference_instructions` | Pass A: these are the assembly spine — game_state immediately followed by planning_protocol (the §2.1 pair invariant), campaign setting when present, ordered prompt types, per-agent builds, core instructions, and conditional character/system-reference additions. Pass B: ordered assembly of registered prompt files plus state serialization is transport; the game_state→planning pair is an ordering contract, not a content verdict. **KEEP** |
| `PromptBuilder._has_high_tier_npc`, `._maybe_add_social_hp_early_reminder`, `.build_social_hp_early_reminder` | Pass A: social-HP reminders matter most when a god/king/lord-tier or level ≥ 15 NPC is present, which is why the server pre-detects that condition. Pass B: pre-detecting NPC tier on the server and injecting a reminder on that basis is field-aware triggering — the prompt itself can state the trigger ("when a high-tier NPC is present…") and let the model apply it, which is exactly where the decision belongs. **ADAPT** (move the tier trigger into the social-HP prompt text; delete the server-side tier check as a reminder gate) |
| `PromptBuilder.build_character_creation_instructions`, `.build_character_creation_handoff_block`, `.build_detailed_sections_block`, `.build_campaign_setting_block`, `.build_campaign_tier_prompts_block`, `._resolve_campaign_tier`, `._append_campaign_tier_prompts` | Pass A: creation instructions, handoff reminders, detailed sections, campaign setting, and tier prompts are the conditional blocks that make modal/tier turns coherent. Pass B: assembling registered blocks keyed to durable state (creation active, tier value) is transport; tier *resolution* passes only as a read of the stored tier, not a computation of it — if `_resolve_campaign_tier` computes a tier from other fields rather than reading it, that computation deletes. **KEEP** (as stored-tier reads; flagged: verify `_resolve_campaign_tier` reads rather than computes — its body was not fully read in this run) |
| `PromptBuilder._extract_companions_from_state`, `.has_active_companions`, `.build_companion_instruction`, `.build_background_summary_instruction`, `.build_initial_world_time_instruction`, `.build_character_identity_block`, `.build_spells_known_block`, `.build_god_mode_directives_block` | Pass A: companion instructions, background summaries, first-turn world-time establishment, identity blocks, spells-known blocks, and god-mode directives blocks are the dynamic prompt content a turn needs beyond static files. Pass B: serializing state the model authored (companions, background, identity, spells, directives) into prompt blocks is faithful assembly; the god-mode block renders directives verbatim (§3.1). **KEEP** |
| `PromptBuilder.build_world_sim_schedule_reminder` | Pass A: world-sim scheduling needs factual anchors (schedule date, timeline high-water boundary, existing coverage) or the model schedules against stale coverage. Pass B: the anchors are server-scheduler facts — durable/scheduler state, not campaign-domain decisions — rendered onto the uncached request tail. **KEEP** (as factual scheduler context; the scheduling *decision* stays model-owned) |
| `PromptBuilder.build_temporal_enforcement_reminder`, `.build_continuation_reminder`, `.build_faction_continuation_reminder`, `.build_arc_completion_reminder`, `.build_living_world_instruction`, `.build_combat_state_reminder`, `._build_tail_reminder`, `.build_level_up_announcement_reminder`, `.build_pcd_crossing_completeness_reminder`, `.build_deferred_rewards_instruction`, `.build_deferred_rewards_block`, `.build_rag_output_contract_block`, `.build_graveyard_context` | Pass A: tail reminders are how per-turn obligations (temporal consistency, continuation, faction continuation, arc completion, living-world policy, combat state, level-up announcement, crossing completeness, deferred rewards, RAG contract, graveyard) reach the model on the turn they matter, instead of living only in a static file the model may not re-read. Pass B: loading shared per-turn reminder assets and formatting them with state values is prompt assembly; each reminder's *content* is verdict in §5, and none of these builders filters or rewrites model-authored values. **KEEP** (as assemblers; content verdicts in §5) |
| `PromptBuilder.build_companion_arc_cadence_reminder`, `.build_pc_arc_context` | Pass A: companion-arc cadence and PC-arc context are trigger-based obligations that must fire on their trigger turn or arcs stall silently. Pass B: trigger-keyed assembly (turn number / arc state) is scheduling, not a decision about arc content — the content is model-owned. **KEEP** |
| `PromptBuilder._typed_class_level`, `._typed_subclass`, `._build_next_level_class_row`, `.build_level_up_repair_class_row`, `._build_saved_progression_fact`, `.build_owed_level_up_reminder`, `.build_level_up_amendment_completeness_reminder` | Pass A: level-up turns need the SRD progression row for the next level and the saved level/XP fact, or the model levels from invented numbers. Pass B: these are the field-aware core of the builder — they select progression facts by saved class/level and project saved grants onto the tail. They pass only as the §3.1 capacity/state exception: rows keyed to the *saved* sheet (durable state), never to a server recomputation of level or XP, with the saved sheet authoritative. **ADAPT** (keep saved-sheet-keyed rows; delete any recomputed level/XP or inferred grant) |
| `PromptBuilder.should_include_deferred_rewards` | Pass A: the deferred-rewards instruction must appear only when the turn warrants it, or every turn pays its cost. Pass B: a turn-number-based inclusion gate is scheduling metadata. **KEEP** |
| `PromptBuilder.finalize_instructions` | Pass A: finalization adds world instructions and the dynamic tail to the assembled instruction, producing the single string the model receives. Pass B: assembly passes, but finalization is also the last place a field-aware filter could hide — the current pipeline (world instructions + tail) contains no such filter, so it passes as written. **KEEP** (as written; any future filter added here is DELETE by default) |
| `get_static_prompt_parts` | Pass A: non-timeline prompt parts (rules, world, state scaffolding) must be generatable independently of the current turn for caching and budgeting. Pass B: static-part assembly is transport/capacity (it feeds the cached prefix). **KEEP** |
| `get_current_turn_prompt` | Pass A: the current-turn text (user input + mode framing) is what distinguishes this turn from the static prefix. Pass B: formatting user input and an explicit mode into turn text is transport; it does not reinterpret the input. **KEEP** |
| `build_temporal_correction_prompt`, `build_temporal_warning_message` | Pass A: when a temporal violation is detected, the model needs a correction prompt and the player needs a warning, or time inconsistencies silently persist. Pass B: a correction notice grounded in durable world_time/location state is state-consistency transport; the user-facing warning is UX text, not a domain decision. **ADAPT** (keep as state-consistency notices; delete any correction that rewrites a model-authored time value rather than asking the model to reconcile it) |
| `build_graveyard_prompt_context` | Pass A: the deceased ledger must reach the model or the dead return to scenes. Pass B: rendering a durable ledger verbatim into prompt context is faithful assembly. **KEEP** |
| `ESTABLISH_WORLD_TIME_REMINDER`, `CHARACTER_CREATION_HANDOFF_TURN_LIMIT`, `CHARACTER_CREATION_HANDOFF_REMINDER`, `_PROMPT_TYPE_STORY_CONTINUATION_REMINDER` | Pass A: first-turn world-time establishment, creation-handoff turn limits, and continuation reminders are the small constants that make dynamic blocks fire correctly. Pass B: constants naming prompt fragments and limits are assembly metadata. **KEEP** |

## §4 — Phase 2: the five run-1-untouched files + README (full text read)

### §4.1 `prompt_loader.py` (90 lines, full text)

| Symbol | Justification + verdict |
|---|---|
| `DiceStrategy` (Literal: `code_execution`, `tool_requests`, `native`, `native_two_phase`) | Pass A: the variant loader needs a closed strategy vocabulary or a typo silently loads the wrong dice prompt. Pass B: an execution-path enum is transport metadata. **KEEP** |
| `load_prompt_variant` | Pass A: dice-strategy variants and scene prompts are the only prompt paths this loader serves; deleting it breaks code-execution dice prompts and scene-image prompts, which the model cannot repair from inside a turn. Pass B: verbatim file reads, a documented fallback (variant → default, with a warning log), and one documented placeholder substitution (`{{LEVELING_PACE_CONTRACT}}`) are transport — no filtering, reordering, or field-aware rewriting occurs. **KEEP** |

### §4.2 `entity_instructions.py` (674 lines, full text)

Live consumers: `llm_service.py` imports `EntityInstructionGenerator`
(and instantiates it alongside the preloader shim); tests cover the
generator, preloader, and tracking. The `entity_preloader`/`location_enforcer`
globals are re-exported through the `entity_preloader.py` shim.

| Symbol | Justification + verdict |
|---|---|
| `EntityInstruction` (dataclass: entity_name, instruction_type, specific_instruction, priority) | Pass A: generated instructions need a typed carrier or they degrade into unformatted strings. Pass B: a data shape carries no judgement. **KEEP** |
| `EntityInstructionGenerator.__init__`, `._build_instruction_templates`, `._build_entity_priorities` | Pass A: prompt templates per entity situation and a priority table are what make generated instructions consistent across turns. Pass B: template text is prompt data, and priority ordering of *sections* (not filtering of entities) is assembly — every entity still reaches the model. **KEEP** |
| `EntityInstructionGenerator.generate_entity_instructions` | Pass A: per-entity mandatory/conditional/background sections plus an enforcement clause are what keep referenced entities present in the response; a bare log drops them. Pass B: assembling caller-provided entity lists into prompt sections is prompt data assembly — the caller, not this function, supplies the entity list, so the function invents nothing. **KEEP** (as an assembler; its categorization input is verdict in the next row) |
| `EntityInstructionGenerator._create_entity_instruction` | Pass A: per-entity categorization is what turns a name list into differentiated instructions. Pass B: the categorization currently branches on `_is_player_character` (heuristic) and `_is_location_owner` (disabled) — the heuristic branch is a server guess about identity, and the disabled branch is dead weight. **ADAPT** (keep template rendering; replace heuristic categorization with explicit caller-supplied categories or state identity; delete the location-owner branch outright) |
| `EntityInstructionGenerator._is_player_character` | Pass A: the model does not need this function at all — the player character's identity is in state (`player_character_data`), so a name-matching heuristic adds no capability. Pass B: matching entity names against "player/pc/hero/protagonist/you" and phrases like "your character" is keyword classification of identity — the banned shape, and a wrong match mislabels an NPC as the player. **DELETE** (replace with a state-identity lookup; the function's own comment admits it is a heuristic "until full game state integration") |
| `EntityInstructionGenerator._is_location_owner` | Pass A: it always returns `False` by design ("currently disabled"), so deleting it changes no turn whatsoever. Pass B: dead code that exists only to be a branch target is not a decision — it is clutter. **DELETE** |
| `EntityInstructionGenerator.create_location_specific_instructions` | Pass A: a single generic location instruction ("ensure entities appropriate to this setting are present") covers the need without any dispatch. Pass B: the current implementation dispatches on substrings in the location name (throne/study/chamber/archive/temple/market/tavern) to pick canned setting text — keyword routing on a domain field, and the canned text invents setting inhabitants the state never named. **DELETE** (as written; its replacement is one static generic line in a prompt file, not a function) |
| `EntityEnforcementChecker.__init__`, `._build_compliance_patterns`, `.check_instruction_compliance`, `._check_entity_compliance` | Pass A: post-hoc compliance scoring produces no player-visible capability — it does not change the response, only scores it after the fact, and no turn path was found consuming the score to improve a turn. Pass B: regex-scanning model narrative for entity mentions/dialogue/action patterns is server second-guessing of model output by narrative parsing — the exact shape strict ZFC and the repo's regex-narrative ban reject — and a "non-compliant" verdict on a response the player already received helps nobody. **DELETE** (all four symbols; if a consumer needs presence assurance, it belongs in the prompt, not in a post-hoc regex) |
| `EntityPreloader.__init__`, `.generate_entity_manifest`, `.get_entity_count`, `.clear_cache` | Pass A: a session/turn-keyed manifest cache prevents rebuilding the entity manifest per turn, and counts/clearing support logging and tests. Pass B: bounded caching and counting are capacity/observability; the cache key is (session, turn), not content, so it cannot serve a stale manifest to a different turn. **KEEP** |
| `EntityPreloader.create_entity_preload_text` | Pass A: the preload text (PCs with HP/status, NPCs with HP/status/location, location entities, plus an enforcement clause) is the manifest's prompt surface — without it the manifest never reaches the model. Pass B: serializing a state-derived manifest verbatim is faithful assembly; the enforcement clause is prompt text. **KEEP** (subject to the next row's deletion) |
| `EntityPreloader._get_location_entities` | Pass A: resident matching (NPCs whose stored location matches the scene) is state-derived and needed. Pass B: the function also appends server-invented ambiance entities ("Court guards (background)", "Books and scholarly materials", "Personal furnishings", "Religious symbols and atmosphere") based on location substrings — entities no state record names, invented by the server and then enforced as present. **ADAPT** (keep resident matching; DELETE the invented-ambiance branches) |
| `LocationEntityEnforcer.__init__`, `.get_required_entities_for_location`, `.validate_location_entities`, `.generate_location_enforcement_text` | Pass A: with `location_rules = {}` always empty, every method is a no-op — required entities are always `{}`, validation always passes, enforcement text is always "(no specific entity requirements)" — so deletion changes no turn. Pass B: a no-op enforcer is dead code wearing an enforcement name; keeping it invites a future rule table that would be server-side entity enforcement by location keyword. **DELETE** (all four symbols, plus the `location_enforcer` global; the shim re-export must be updated on the same PR) |
| Globals `entity_instruction_generator`, `entity_enforcement_checker`, `entity_preloader`, `location_enforcer` | Pass A: singletons avoid rebuilding templates/caches per turn. Pass B: globals are instantiation, not decisions. **KEEP** for the generator and preloader globals; **DELETE** for the checker and enforcer globals (with their classes). |

### §4.3 `context_compaction.py` (1,598 lines, full text)

Budget constants as a group (`BUDGET_*`, `TURNS_TO_KEEP_AT_START/END` =
20/20, `SYSTEM_INSTRUCTION_BUDGET_QUANTUM_TOKENS` = 1,000): **KEEP** as
capacity arithmetic, except the protected-floor constants below, which are
**ADAPT** (move to a prompt manifest). Game-state priority tiers
(`GAME_STATE_PRIORITY_CRITICAL/HIGH/MEDIUM/LOW`): **ADAPT** — see
`_compact_game_state`. `SCENE_LEDGER_MAX_CHARS` (4,000) and
`SCENE_LEDGER_HEADER`: **KEEP** (bounded verbatim projection).

| Symbol | Justification + verdict |
|---|---|
| `BudgetAllocation.utilization_pct` | Pass A: utilization reporting is what makes budget logs interpretable. Pass B: pure arithmetic on measured/allocated tokens, division-guarded. **KEEP** |
| `RequestBudgetResult.get_story_budget`, `.get_allocation`, `.log_summary`, `.to_bq_fields` | Pass A: the turn path and BigQuery forensics both need story budgets, per-component lookups, human-readable summaries, and structured BQ fields. Pass B: accessors and formatting of already-computed allocations decide nothing. **KEEP** |
| `MandatoryContextCapacityError.__init__` | Pass A: when mandatory instruction plus fixed content exceed capacity, the request cannot be sent as-is, and a typed 422 error is more operable than a silent truncation. Pass B: raising instead of silently truncating mandatory instructions is the honest capacity behaviour; the UX tension with the repo's UX-first rule is flagged in §1, not resolved by hiding the error. **KEEP** |
| `_allocate_request_budget` | Pass A: without min-first/fill-to-max allocation across system/state/memories/entities/story, one component can starve the rest and long campaigns break. Pass B: token arithmetic plus warnings is capacity allocation; the measured-story slice is the fixed 20+20 candidate slice (not the whole archive), which the comments show was fixed precisely to avoid false compaction warnings. **KEEP** |
| `_quantize_system_instruction_budget` | Pass A: unquantized budgets drift a few tokens per turn, moving every truncation cut-point and breaking implicit-cache prefix stability (the file documents 7/7 same-agent turns diverging). Pass B: snapping down to a 1,000-token quantum is cache-stability capacity engineering, never giving the caller more than allocated. **KEEP** |
| `_system_instruction_file_name`, `_split_system_instruction`, `_SYSTEM_FILE_PATTERN`, `_SYSTEM_TRUNCATION_MARKER`, `_SYSTEM_SECTION_MARKER` | Pass A: file-aware compaction needs file boundaries (`# File: <name>.md`) and visible truncation markers, or truncation silently mangles prompt sections. Pass B: splitting on markers and labelling cuts is formatting/capacity with disclosure built in. **KEEP** |
| `_compact_unsegmented_system_instruction` | Pass A: instructions without file boundaries still need an emergency compaction path or an over-budget turn has no fallback. Pass B: keeping 60% head / 40% tail around a truncation marker is neutral positional trimming, not content selection. **KEEP** |
| `_critical_system_segments`, `_compact_critical_overflow`, `_protected_floor_reservations`, `_compact_noncritical_segments`, `_trim_excess_from_segment`, `_drop_segments_to_reclaim`, `_is_protected_compaction_segment`, `_trim_compacted_system_instruction`, `_compact_system_instruction` | Pass A: emergency system-instruction compaction (>100k tokens) is the last defence before a turn cannot be sent; critical files must survive in full and non-critical files must shrink proportionally with floors, or a single oversized file eats the prompt. Pass B: this family is capacity machinery, but its *policy* — which files are "critical" (master, game_state, planning, SRD, living_world, god-mode contract, dialog, RAG contract, combat contract, level-up set, conclude set, leveling pace, mechanics appendix, canonical anchor, witness continuity, world-event effects, plus banned-names when the god-mode contract is present) and which files get protected floors (narrative 20,000 chars, faction 4,000, god-mode 5,000) — is prompt policy hardcoded as code literals. The machinery passes; the policy location fails the repo's own no-hardcoded-prompt-shape rule. **ADAPT** (keep the machinery; move the critical-file list and floor specs into a prompt manifest loaded as data, so prompt edits do not require code edits) |
| `NARRATIVE_FILES`, `NARRATIVE_BODY_FLOOR_CHARS`, `FACTION_FILES`, `FACTION_BODY_FLOOR_CHARS`, `GOD_MODE_FILES`, `GOD_MODE_BODY_FLOOR_CHARS`, `_FLOOR_SPECS`, `_floor_chars_for` | Pass A: floors are what keep load-bearing narrative examples and faction/god-mode sections alive under truncation pressure (each floor's comment cites measured marker positions). Pass B: floors are capacity reservations, but as code literals they are prompt policy in the wrong layer. **ADAPT** (same manifest move as above; the floor values themselves are evidence-backed and stay) |
| `_compact_game_state` | Pass A: over-budget game state must shrink or the turn cannot be sent, and dropping low-priority fields first preserves playability better than blind truncation. Pass B: this is the file's one genuinely field-aware transform — CRITICAL/HIGH/MEDIUM/LOW tiers choose which model-authored fields the model re-sees, plus a nested world-data legacy-alias migration and an injury-field allowlist. It passes only as a disclosed capacity exception (drop only when over budget, never drop critical fields or deceased/injured identities, never emit invalid JSON — unparseable state returns untouched), and the tier list belongs in the same manifest as the critical files. **ADAPT** (keep as a disclosed capacity exception; move tiers to the manifest; delete the legacy-alias rewriting in favour of a storage-layer migration if one is ever needed) |
| `split_memory_entries`, `_compact_core_memories` | Pass A: core memories must fit a budget without losing the newest curated facts or model-flagged retained memories, and without letting the scene-ledger tail masquerade as newest curated memory. Pass B: recency ordering plus model-flagged `retain: true` prioritization, with the ledger ranked last and its header re-attached only if a recap survives, is the ZFC-clean shape — no keyword or substring exemption exists anywhere in this path, by the function's own documented design. **KEEP** |
| `_select_lines_within_char_budget`, `format_scene_ledger_for_prompt` | Pass A: the scene ledger (raw per-scene recaps, growing for the life of a campaign) must reach the model bounded, or its measured size inflates the core-memories budget every turn. Pass B: newest-first selection within 4,000 chars, one line per entry with internal newlines collapsed, is verbatim bounded projection of model-authored lines — no summarization, no rewriting. **KEEP** |
| `_filter_persisted_warnings`, `_save_warning_persist_keys` | Pass A: budget warnings must show once per session, not every turn, and the suppression keys must persist in state or the same warning spams the player. Pass B: warning suppression is durable-write bookkeeping piggybacked on the existing save (no extra turn-path write), and it never alters prompt content. **KEEP** (logging per §6 decision 1; no async change needed since no new turn-path write is introduced) |

### §4.4 `prompt_context_metrics.py` (345 lines, full text) — all KEEP

`STABLE_PREFIX_FIELDS` (game_mode, user_id, selected_prompts,
use_default_world, story_history, core_memories, sequence_ids) is the
cache-boundary field set: a capacity classification, not a content filter —
**KEEP**. `_select_instruction_from_container`,
`_select_raw_system_instruction`, `_extract_text_from_part`,
`_extract_ordered_text`, `_extract_system_instruction_text`,
`_extract_system_instruction_with_presence`: key-presence precedence
(config-then-top-level, snake-then-camel) mirroring the provider wire
projection, with presence kept distinct from truthiness so an explicitly
empty instruction is not confused with an absent one — pure parsing of
already-captured payloads, never mutating a live prompt — **KEEP**.
`_sha256_json`: canonical-JSON hashing of the exact components used for
estimates — **KEEP**. `_parse_json_object`, `_find_envelope_in_item`,
`_extract_envelope`: structural envelope extraction with explicit
`ok`/`no_envelope`/`malformed_json` statuses, never inventing an envelope —
**KEEP**. `estimate_gameplay_request_breakdown`: token breakdown
(system/story/envelope/stable-prefix/dynamic-tail) for BQ forensic rows,
returning `None` buckets (not zeros) when no envelope parses — **KEEP**.
`normalize_optional_token_count`, `sum_optional_token_counts`,
`cache_hit_rate_pct`, `breakdown_percentages`: pure arithmetic that returns
`None` on unknown/invalid input (including the code-execution denominator
subtlety: Gemini's `prompt_token_count` excludes `tool_use_prompt_token_count`,
so the cost-relevant denominator sums them) — **KEEP**.

### §4.5 `prompt_cache_usage_semantics.py` (204 lines, full text) — all KEEP

`SUPPORTED_GEMINI_TELEMETRY_PROVIDERS` (gemini + gemini_sdk): provider
allowlist for telemetry classification — **KEEP**. `UsageStatus`,
`UsageUnavailableReason`, `UsageClassification` (frozen dataclass): typed
classification vocabulary with stable reason codes, including explicit
`economic_input: None` until a versioned pricing mapping exists — **KEEP**.
`_classify_ordinary`: complete/consistent coverage only, `None` on
incomplete input, invalid denominator on non-positive or cached>prompt —
**KEEP**. `_classify_code_execution`: raw-only local ratio
(cached/(prompt+tool_use)) with undocumented-shape handling when cached
exceeds prompt — **KEEP**. `compute_warm_code_execution_averages`: averages
only `CODE_EXECUTION_COMPLETE_RAW_ONLY` rows with known percentages, and
returns `None` for the all-warm average unless every row qualifies — a
discipline against averaging over unknowns — **KEEP**. `classify_usage`:
provider/model gating first, then ordinary vs. code-execution dispatch, with
normalized counts throughout — **KEEP**.

### §4.6 `PROMPTS_README.md` (255 lines, full text) — DELETE (shipped path)

Per-section verdicts: Overview + Directory Structure + Prompt Files (8
entries) — **DELETE** as a coverage claim (stale: 8 vs. 128, §1); as prose
the 8 per-file purpose summaries are still roughly accurate for those 8
files, but that does not rescue the section. Loading Order + Conditional
Loading — **DELETE** (claims "Always Loaded: master, game_state, dnd_srd"
and loading via `llm_service.py`, both contradicted by per-agent
`REQUIRED_PROMPT_ORDER` and `agent_prompts.py` `PATH_MAP`). Prompt
Management (format/encoding/structure/length) — **DELETE** as shipped doc
(length claim "500–3000 words each" fails for the 98KB game-state file and
the 1-line fragments). Version Control, Prompt Architecture (hierarchy),
Development Guidelines, Content Standards — **DELETE** as shipped doc
(the hierarchy itself survives in `master_directive.md`, which is the live
authority; this restatement can drift from it). Archived Prompts —
**DELETE** (names files that do not exist on disk; archival reasons are
unverifiable from the tree). Performance Considerations (token usage
"~15,000–20,000 tokens") — **DELETE** (contradicted by current prompt
sizes). Testing Prompts, Maintenance, Quality Metrics, Integration
("Loading: handled by `llm_service.py`", "Constants: prompt paths defined
in `constants.py`" — the latter half-true, the former false) — **DELETE**.
Net: the file's only honest future is a rewritten developer note that points
at `prompts/AGENTS.md` and `agent_prompts.py` `PATH_MAP` as the live sources,
or deletion. **DELETE** (shipped path; doc-only if rewritten).

## §5 — Phase 2: prompt files (per file; sections grouped where they share one verdict)

Reading rule used here: a file's sections are listed individually only when
they differ in verdict; sections sharing a verdict and a rationale are
grouped in one row with every heading named, so that every section is
accounted for without 800 near-identical rows. Verdict question per section
throughout: what breaks if the model never sees this section? Breaks
parsing, breaks mechanics, or breaks anti-cheat = keep; changes only prose,
duplicates another file, or restates the schema = slim or delete.
"KEEP" for a prompt file means: keep as prompt data (the model owns it);
it never means "keep as code". Line counts are `wc -l` on the local tree.

### §5.1 Top-level prompt files

| File (lines) | Sections + justification + verdict |
|---|---|
| `master_directive.md` (166) | All sections — Canonical NPC Status; Companion Boundary & Departure Lifecycle; Companion Injuries; Player Agency (Literal Action Authority, Zero Persona Overriding); Scene Focus/Presence/Continuity; Secret Persona Invariant (MBTI & Alignment, internal only); Critical Loading Order and Precedence + Conflict Resolution Rules; D&D 5E SRD System Authority; Universal Naming Rules; Data Query Response Protocol (numeric answers first); ACTION RESOLUTION PROTOCOL (Interpret → Resolve → Audit → Narrate) + Dice Output (Single Source of Truth); CAMPAIGN INTEGRITY GUIDELINES; IMMERSIVE NARRATIVE STYLE; Narrator Objectivity (Zero Moral Verdicts); Companion Records (Identity Record Required). If the model never sees the precedence/conflict rules, a player instruction can override a safety/mechanics rule mid-turn; if it never sees the action-resolution protocol and dice single-source-of-truth, it narrates outcomes before rolls resolve, breaking anti-cheat narration discipline. Style and persona sections change prose quality, but they are the stable GM voice across turns, which a bare log does not preserve. **KEEP** (run-1 KEEP confirmed; the hierarchy here is the live authority the README merely restates) |
| `game_state_instruction.md` (1,364) | Shape/protocol core — Identity Provenance Policy; Core Memories Replace Dropped Middle Story Entries + NPC reconciliation; Game State Schema Reference (entity types, campaign tier progression, Lite Canonical Schema); Routing Control; Turn vs Scene vs Sequence numbering; Dice Values Are UNKNOWABLE (tool-requests flow, forbidden patterns, how dice must work); JSON Communication Protocol + required fields; Interaction Modes; Planning Block Protocol; State Authority and Timeline; Safe State Update Patterns; Location Field Format; Schema-Generated Examples; Equipment Slots (canonical); Sanctuary Mode; Relationship Update Rules; Input Schema (system corrections, NPC data, army/faction data); D&D 5E Rules (attribute management, entity IDs, PC schema, proficiencies/resistances/senses, hit dice, active effects, status conditions). If the model never sees the schema/protocol sections, the parser has nothing stable to parse and sheets/inventory/combat state shown in the UI break; if it never sees the dice-unknowable sections, it fabricates rolls. These are transport (response shape) plus delegation (server dice), not server recomputation. **KEEP** for the core. Faction Minigame Activation block (~160 lines inside this file, §"Faction Minigame Activation" under JSON protocol): if the model never sees it here, it still sees it in `faction_minigame_instruction.md` — this is the second home for faction activation, violating the one-shared-rule-one-file policy. **ADAPT** for that block only (move it to the faction file; the file-level verdict is therefore ADAPT, with the core KEEP) |
| `game_state_examples.md` (227) | Response-format examples (combat phase examples with tool-requests/code-execution stripping markers, plus `{{STATE_EXAMPLE:...}}` placeholders). If the model never sees worked examples, it must infer the exact JSON envelope from prose alone, and format compliance degrades on edge cases. Examples are schema-faithful illustrations, not new rules. **KEEP** |
| `game_state_mechanics_appendix.md` (288) | Resource Registry, spell/resource/combat-state/encounter mechanics extracted from the base game-state prompt. If the model never sees it, mechanics-capable agents lose detailed rules that the base file deliberately no longer carries — extraction, not duplication, since the base file points here. **KEEP** |
| `narrative_system_instruction.md` (906) | Anti-exploit freeform stat claims; narrative length discipline; required `narrative_response_schema` + worked examples; combat & dice narrative rules; rewards & XP protocol (story mode); Master Game Weaver philosophy; GM protocols (unforeseen complications, NPC autonomy & agency); player action guardrails + action-resolution audit; SOCIAL HP system (friction heuristic, anti-paper-tiger, difficulty scaling, complex skill challenges, resistance indicators, recovery, victory ripple); NPC hard limits + forbidden paper-tiger patterns; meta-instruction separation; god-mode directive compliance; narrative consistency; victory detection; social & skill victory XP; living-world mission system + proactivity engine + living-world narrative integration (mandatory every turn); narrative consistency anchors (co-presence, god-mode compliance, cover identity, NPC status alignment); story-mode style. If the model never sees the anti-exploit/social-HP/hard-limit sections, players can talk their way to permanent stats and yes-man NPCs; if it never sees the schema section, narrative shape breaks. The proactivity engine's "forced initiative" is model behaviour stated as a prompt, so it stays model-owned. **KEEP** for all sections except the living-world visibility material, which duplicates `living_world_instruction.md` (see that row) — **ADAPT** for the living-world sections only (single-home the visibility contract) |
| `narrative_lite_system_instruction.md` (221) | Dialog-length guidance (~500 words, flexible target), lite narrative directives for dialog/portrait paths. If the model never sees it, dialog turns lose their length/style guidance and default to full narrative weight. It is a distinct audience (dialog/portrait), not a duplicate of the full narrative file. **KEEP** |
| `mechanics_system_instruction.md` (8) | Pure include manifest: `shared/mechanics_system_protocol.md`, combat-roll display rules, leveling protocol intro + rewards body. If the model never sees the wrapper, it never sees the four shared fragments, which carry the mechanics. The wrapper adds no content of its own, so its verdict is the verdict of its includes. **KEEP** (run-1 ADAPT revised: the adaptation, if any, lives in the shared fragments, not here) |
| `mechanics_system_instruction_code_execution.md` (13) | Include manifest: mechanics protocol + code-execution dice section + leveling intro/body. Same reasoning as the tool-requests wrapper, for the code-execution path; the two wrappers differ only in their dice fragment, which is a genuine execution-path difference. **KEEP** (run-1 merge candidate rejected, §1 conflicts) |
| `dice_system_instruction.md` (90) | Dice & Mechanics (tool-requests mandatory, absolute no-model-roll rule); MODAL/TIME-FREEZE EXCEPTION; procedure (identify need via zero-roll rule, populate `tool_requests`, wait for server, narrate from result); critical-hit bonus-damage flag rule (`is_critical` + base notation, server doubles); DC fairness warning (set DC before requesting, never adjust after); per-tool arg contracts (skill checks, saves); forbidden fabrication vs. correct tool-request examples; separate-roll rule for feature dice; display rules (no roll arithmetic in narrative; client dice panel shows it); advantage/disadvantage, opposed checks, social checks; plus includes of `shared/dice_notation_contract.md` and `shared/dc_calibration.md`. If the model never sees any of this, it invents rolls and breaks anti-cheat outright; every section is delegation to server dice on the turn path. No model-roll fallback was found in the full text. **KEEP** (run-1 ADAPT revised up: the file is already a clean delegation instruction) |
| `dice_system_instruction_code_execution.md` (17) | Dice & Mechanics (nat-20-always-succeeds / nat-1-always-fails success rule); MODAL/TIME-FREEZE EXCEPTION; includes of `shared/dice_code_execution.md` and `shared/dice_notation_contract.md`. If the model never sees it, code-execution turns lose the unknowability rule and the nat-20/1 rule, and dice become model-narrated. The modal exception is identical to the tool-requests file's, which is correct (modals freeze dice in both paths). **KEEP** |
| `character_template.md` (73) | Core Identity; Psychology; Behavior & Speech; Backstory; Game Mechanics; Deep Character Framework (psychological sketch, persona vs. interior, relational script, core unconscious beliefs, personal myth, break-point); Prose Example. If the model never sees the template, character facts arrive in inconsistent shapes and the sheet/parser break; progression sections state rules, not server verdicts. **KEEP** (run-1 KEEP confirmed) |
| `dnd_srd_instruction.md` (77) | Core Rules; proficiency bonus (only when proficient); roll formulas; class save proficiencies; quick examples (level-1 bard); social checks (non-CHA stat support). If the model never sees it, rulings fall back to uneven memorized rules. The file is already a 77-line compact reference, not a full SRD dump, so the run-1 capacity slimming has nothing to slim. **KEEP** (run-1 ADAPT revised up) |
| `character_creation_instruction.md` (417) | Character creation & level-up flow under D&D 5e rules (core principle, creation steps, level-up flow). If the model never sees it, creation turns lose their focused flow and level-up turns lose their procedure. The file's defect is structural, not content: it mixes creation and level-up in one file while `level_up_instruction.md` exists as a separate home. **ADAPT** (split creation sections from level-up sections into their home files; keep all content) |
| `character_creation_conclude_instruction.md` (101) | Finalize-turn domain header ("Apply Recommended Options and Return to Game" / "Finish Character Creation and Start Game"), applying the shared conclude core. If the model never sees it, the creation finalize turn has no canonical commit target. No semantic-exit language found. **KEEP** |
| `_conclude_core.md` (72) | Shared conclude core: commit the canonical target; mandatory cascade (recompute proficiency bonus, max HP, spell slots, hit dice, class resources from the committed level/class); canonical field is truth, not narrative milestone; clear the modal flags; final-output contract overriding generic wording. If the model never sees it, finalize turns commit nothing, cascade nothing, echo story numbers into mechanical level, or leave the player stuck in the modal. This is the prompt side of the explicit-only conclude decision, and it is already explicit-signal clean. **KEEP** |
| `level_up_instruction.md` (119) | Level-Up State Contract: canonical authoring surface (`state_updates.reward_event.xp` as model-authored award; server materializes cumulative XP); saved-sheet authority. If the model never sees it, level-up turns lack the award surface and the server/materialization boundary blurs. **KEEP** |
| `level_up_audit_instruction.md` (139) | Level-Up Repair During Gameplay: saved sheet authoritative; review pending advancement using saved grant context, campaign rules, current sheet; repair model-owned inconsistencies. If the model never sees it, repair turns have no procedure and no authority rule. **KEEP** |
| `level_up_modal_override_instruction.md` (16) | Optional Level-Up Review: granted sheet already saved; per explicit review choice, author the mechanic change immediately; retain saved level/XP/unrelated mechanics/spent resources; record the selected alternative in `level_up_session.selections`; do not author other server-owned session/control fields; review notice does not pause ordinary gameplay; only an explicit review selection may be a presentation action without time advancement. If the model never sees it, review choices either stage a second sheet or pause gameplay they should not pause. Explicit-choice language throughout. **KEEP** |
| `level_up_conclude_instruction.md` (7) | Level-Up Review Closure: closure is presentation only — grants no XP, applies no mechanics, clears no pending repair, gates no ordinary action; legacy requests resolve the player's actual action under the ordinary contract with the saved sheet as authority. If the model never sees it, closing a review could be mistaken for granting or clearing. **KEEP** |
| `level_up_audit_schema.json` (50) + `level_up_response_contract.json` (215) | Model-authored repair result schema; explicit level-up review amendments schema (server owns every other session field). If the model never sees the shapes, repair/review responses cannot be parsed. Both schemas name server-owned fields as server-owned rather than inviting model authorship. **KEEP** (both) |
| `leveling_pace_contract.md` (102) | Leveling Pace Contract governing all XP awards (fair-DM thinking, edition/rules-as-written, campaign overrides, server limits). If the model never sees it, XP awards lose their pacing authority and drift. It is substituted into prompts via placeholder by both `prompt_loader.py` and `agent_prompts.py`. **KEEP** |
| `combat_system_instruction.md` (483) | Combat Action Output Protocol (always show attack + damage rolls, every combat action); combat procedures, turn order, HP tracking, enemy handling. If the model never sees it, combat turns lose their output protocol and HP/turn-order discipline, and the UI's combat display has nothing stable to show. **KEEP** |
| `dialog_system_instruction.md` (461) | Conversation excellence (primary directive, core philosophy, character interaction standards). If the model never sees it, dialog turns lose their quality bar and NPC voices flatten to story narration. **KEEP** |
| `heavy_dialog_system_instruction.md` (70) | Escalated dialog scenes (major relationship moments, companion discussions, faction parleys with consequences, betrayal confrontations). If the model never sees it, high-stakes dialog is served with ordinary dialog weight. Distinct audience from the base dialog file. **KEEP** |
| `spicy_mode_instruction.md` (66) | Literary intimate content system instruction, branching on `spicy_mode` enabled/disabled. If the model never sees it, spicy-mode turns have no content policy or literary standard, and the toggle's two branches collapse. **KEEP** |
| `think_mode_instruction.md` (129) | Think Mode: mental pause for the character; planning-block schema reference; risk levels; no narrative advancement. If the model never sees it, think turns advance story they must not advance. **KEEP** |
| `planning_protocol.md` (300) | Planning Protocol (unified): single source of truth for planning-block structure/rules across modes; time-handling differences per mode. If the model never sees it, planning blocks diverge per mode and the parser cannot rely on their shape. **KEEP** |
| `god_mode_instruction.md` (312) | God Mode: administrative pause menu; story frozen during admin changes; XP-threshold crossing handling; directive application. If the model never sees it, admin turns narrate story they must not narrate, or admin changes lack their procedure. Product promise (God Mode Directives) carried as prompt data behind authorization. **KEEP** |
| `god_mode_output_contract.md` (119) | God Mode JSON envelope contract + request classification. If the model never sees it, admin responses lack a parseable envelope and classification diverges. **KEEP** |
| `living_world_instruction.md` (667) | Living World Advancement Protocol: 24-hour game-time trigger (legacy 3-turn cadence removed); visibility contract (unconditional); advancement procedures; mission system. If the model never sees it, living-world turns have no trigger, no visibility rule, and no advancement procedure — and per §6 decision 3 this prompt is the merge surface for async background ticks. Its visibility material duplicates the narrative file's living-world sections. **ADAPT** (keep as the async-tick merge surface; single-home the visibility contract here and remove it from the narrative file; slim the 667 lines only by dedupe, not by dropping the trigger or visibility rule) |
| `faction_management_instruction.md` (115) | Faction & Army Management: faction minigame suggestion protocol (primary task — on any faction status query, suggest/route the minigame); army/faction state handling. If the model never sees it, faction queries get no minigame suggestion and army state has no management procedure. **KEEP** |
| `faction_minigame_instruction.md` (144) | Faction Management Mini-Game: mandatory intel resolution contract (ordering spies is not resolving contested intelligence — emit `faction_intel_operation` in `tool_requests`); turn processing, commands, header, turn-number rules. If the model never sees it, intel operations are narrated instead of tool-executed, breaking the tool-execution boundary for contested intel. **KEEP** (and receive the game-state file's activation block per §5.1) |
| `background_routine.md` (9) | Background simulation lane for the living world: per selected entity, decide whether/what to simulate; `SERVER_REQUEST_JSON.context.faction_roster` as the frozen authoritative roster for the window. If the model never sees it, background ticks have no lane definition and no roster authority. **KEEP** (async lane definition per §6 decision 3) |
| `relevance_highlights.md` (3) | Author possible new player-relevant developments for living-world simulation (not extraction of prior events) + include of `shared/world_sim_realism.md`. If the model never sees it, relevance highlights collapse into summaries of old events. **KEEP** |
| `world_sim_setup.md` (15) | World Sim Setup: set up a campaign's living-world simulation once from campaign data in `SERVER_REQUEST_JSON`; `living_world_conflict_profile` choice (noncombat vs. other profiles). If the model never sees it, simulation setup has no profile choice and no one-time-setup discipline. **KEEP** |
| `world_sim_schedule_instruction.md` (13) | World Sim scheduling basis (factual context): schedule date, timeline high-water boundary, existing coverage. If the model never sees it, scheduling decisions lack their factual anchors. **KEEP** (factual scheduler context; the scheduling decision stays model-owned) |
| `relationship_instruction.md` (142) | Relationship mechanics (detailed): relationships as active mechanics, not flavour; schema pointer to game-state relationships object (required for recurring NPCs). If the model never sees it, relationship state is written as flavour and never drives mechanics. **KEEP** |
| `reputation_instruction.md` (175) | Reputation system (detailed): two layers (publicly known vs. privately known per group); schema pointer to game-state reputation schema (required). If the model never sees it, reputation collapses to a single public number and private knowledge leaks or vanishes. **KEEP** |
| `rewards_system_instruction.md` (101) | Rewards State Contract: completed combats/encounters/quests/milestones/reward-eligible events; model calculates and writes resulting character state; server persists. If the model never sees it, reward turns lack their calculation procedure and the model/server boundary for rewards blurs. **KEEP** |
| `deferred_rewards_instruction.md` (33) | Deferred Rewards State Contract: find genuinely completed loot/currency missed in recent story turns; do not double-count an already-credited event; canonical output shape. If the model never sees it, deferred checks either double-count or miss genuinely owed rewards. **KEEP** |
| `player_character_arcs.md` (93) | PC Quest Arcs: every PC must have a personal quest arc unfolding across the campaign; freeform arc type, canonical phase. If the model never sees it, PC arcs never start or never progress canonically. **KEEP** |
| `initial_world_time_instruction.md` (20) | First-turn-only: establish initial `world_time` in `state_updates.world_data` (complete object required). If the model never sees it on turn one, the campaign has no time origin and temporal enforcement has nothing to enforce. **KEEP** |
| `temporal_enforcement_instruction.md` (11) | Temporal Consistency Enforcement: current story state (time/location), hidden microsecond timestamp (think-block uniqueness), time boundary the response must respect. If the model never sees it, time-advancing turns drift. **KEEP** |
| `story_continuation_priority.md` (1) | Critical: resolve only the current user_action; use current structured game_state fields and current planning block. If the model never sees it, continuation turns re-litigate old actions instead of resolving the current one. **KEEP** |
| `integrity_protocol.md` (19) | Preserve established continuity while honouring the player's requested scene focus; no verbatim repetition of earlier paragraphs/dialogue/action descriptions. If the model never sees it, continuation turns pad by copying earlier text. **KEEP** |
| `social_hp_phase2_instruction.md` (1) | Phase 2 Social HP Output Contract: when the authoritative game_state contains an active social_hp_challenge, include the phase-2 output. If the model never sees it, phase-2 challenges are silently dropped from output. **KEEP** |
| `world_event_effects_instruction.md` (1) | World Event Effects (write first): before the narrative, fill `world_event_effects` with one entry per delivered event. If the model never sees it, delivered events never ground into structured effects. **KEEP** |
| `companion_field_contract.json` (85) | Ordered companion projection fields and bounds for `build_companion_instruction()`, with context heading. If the model never sees its *effects* (via the builder), companion blocks lose their field order and bounds; the JSON itself is a contract, not prose. **KEEP** |
| `schema_doc_placeholders.json` (4) | Lite `$defs` whose field docs in `game_state_instruction.md` already document their whole definition (currently: `SocialHPChallenge`). If the builder never reads it, lite stubs duplicate docs the prompt already carries. **KEEP** |
| `portrait_generator_instruction.md` (12) | Portrait generation assistance: stay faithful to supplied game state when writing/interpreting portrait descriptions. If the model never sees it, portrait descriptions drift from the character's stored state. **KEEP** |
| `portrait_canon_franchise_guidance.txt` (5), `portrait_player_precedence.txt` (4), `portrait_request_guard.txt` (9), `portrait_style.txt` (11), `portrait_style_avatar.txt` (1), `portrait_suggest_description_system.txt` (20) | Franchise/canon character guidance (honour explicit opt-outs); player-description precedence (explicit player choices win; published-media characters/NPCs handled per policy); request guard (exactly one fictional portrait; brief is the complete rendering instruction with bracketed slots); style (semi-realistic digital painting, close-up to upper-body; generic non-canon NPC beauty rule); avatar style variant; suggest-description system (single JSON object, exact keys, plain prose). If the model never sees each, portraits lose canon handling, player precedence, single-image discipline, style consistency, or parseable description shape respectively. None is gameplay-turn content; all are portrait-path prompts. **KEEP** (all six) |
| `scene_ablation_presence.md` (1), `scene_brief_system.md` (1), `scene_brief_user.md` (6), `scene_image.md` (27), `scene_image_legacy.md` (5), `scene_presence_after_scene.md` (1), `scene_presence_current.md` (1), `scene_presence_parallel.md` (1), `scene_section_background.md` (1), `scene_section_current.md` (1) | Scene-image pipeline prompts: presence rule (characters mentioned only in recent context must not appear); brief-writer system/user prompts (~120-word visual brief); image prompt (player pose/gaze, reference image as identity only); legacy image prompt (reference as authoritative likeness, 16:9 cinematic); presence rules per mode (after-scene / current / parallel — depict only physically present characters); section labels (background continuity-only vs. current scene to paint). If the model never sees each, scene images gain absent characters, lose the brief discipline, or paint background as foreground. **KEEP** (all ten; they are image-path prompts, not gameplay-turn prompts, and their 1-line presence rules are load-bearing) |
| `prompts/AGENTS.md` (50) + symlinks `prompts/CLAUDE.md`, `prompts/GEMINI.md` | Campaign-Agnostic Prompt Contract: developer/agent policy, explicitly "not gameplay LLM input"; runtime loading via `PATH_MAP` + agent orders (directory not concatenated); one-shared-rule-one-file under `shared/`; campaign-neutrality bans (named characters/mechanics/locations/thresholds, even in examples); runtime authoring rules (no version history, changelogs, meta-commentary, TODOs; no code/commands in prompt bodies); schema coupling (backend gating on a model-authored field requires an emission instruction); user-story gate trigger for `prompts/**`. If the *model* never sees it, nothing breaks — it is never sent to the model, and that exclusion is itself documented here. Its value is entirely as developer policy. **DELETE** from any runtime/prompt-set claim (it is already excluded from loading and linting); **KEEP** as repo documentation only. The two symlinks are the same file and share this verdict. |

### §5.2 `divine/` and `multiverse/` (ascension tiers)

| File (lines) | Sections + justification + verdict |
|---|---|
| `divine/divine_ascension_ceremony.md` (96) | Divine Ascension Ceremony: level-up-into-godhood event, setting-agnostic, activation conditions and ceremony procedure. If the model never sees it, godhood transitions have no ceremony procedure. **KEEP** |
| `divine/divine_leverage_system.md` (252) | Divine Leverage System: canonical mechanic for the god-mechanics campaign tier (L20+ play, demi-/god-tier leverage). If the model never sees it, L20+ play has no leverage mechanic. Setting-agnostic per its header. **KEEP** |
| `multiverse/sovereign_ascension_ceremony.md` (272) | Sovereign Ascension Ceremony: transition from Divine Leverage tier to Sovereign Protocol (multiversal campaign); trigger conditions, ceremony procedure. If the model never sees it, the multiversal transition has no procedure. **KEEP** |
| `multiverse/sovereign_system.md` (127) | Sovereign Protocol System: complete mechanics for the multiversal campaign tier, used by StoryModeAgent after sovereign ascension; competitive multiversal protocol. If the model never sees it, post-ascension play has no mechanics. **KEEP** |

### §5.3 `injection/` (AGY bulk / dynamic-tail fragments)

| File (lines) | Justification + verdict |
|---|---|
| `injection/agy_bulk_instruction_directive.md` (1) | Treat the `--prompt` value as the request; produce only the requested JSON response. If the bulk model never sees it, bulk requests lose their request/response framing. **KEEP** |
| `injection/agy_bulk_response_format.md` (2) | Response format: single JSON object matching the requested schema, no markdown fences. If the model never sees it, bulk responses are unparseable. **KEEP** |
| `injection/agy_bulk_runtime_request_tail.md` (1) | Answer only the request below using the provided instructions and required JSON schema. If the model never sees it, bulk tails drift into unrelated generation. **KEEP** |
| `injection/agy_bulk_tool_activity_boundary.md` (1) | Do not wait for, request, mention, summarize, or depend on file search, workspace inspection, or command execution. If the model never sees it, bulk turns stall waiting for tools that will never arrive. **KEEP** |
| `injection/agy_final_output_contract.md` (13) | Final output contract: exactly one JSON object for WorldArchitect to parse; top-level keys are the gameplay response envelope. If the model never sees it, bulk final outputs are unparseable. **KEEP** |
| `injection/companion_arc_cadence.md` (6) | Companion quest cadence per-turn obligation: on the trigger turn (`current_turn`), honour the cadence when `next_companion_arc_turn` is set and equal. If the model never sees it, companion arcs miss their trigger turns. **KEEP** |
| `injection/companion_generation.md` (27) | Companion generation activated: generate exactly 3 unique starting companions with mandatory requirements. If the model never sees it, generation count and uniqueness requirements are unenforced. **KEEP** |
| `injection/field_doc_dedupe_pointer.md` (1) | Dropped-field pointer line: N shared field definitions omitted here, identical to the earlier definition. If the model never sees it, deduped fields read as missing rather than deliberately omitted. **KEEP** |
| `injection/story_continuation_reminder.md` (10) | Continuation reminder: mandatory planning-block field every story-mode response; mandatory narrative field every response. If the model never sees it, continuation responses drop required fields. **KEEP** |

### §5.4 `shared/` (47 fragments — the one-home rule's test)

| File (lines) | Justification + verdict |
|---|---|
| `shared/action_resolution_example.md` (10) | Worked `action_resolution` JSON example (persuasion attempt, reinterpreted, skill-check mechanics, audit flag `player_declared_outcome`). If the model never sees it, action-resolution shape must be inferred from prose. **KEEP** |
| `shared/agency_check.md` (7) | Agency Check (`/agency rewind`): when the model narrates player thoughts/words/actions, the player may issue `AGENCY_CHECK: <sentence>` and the next response must remove and replace it. If the model never sees it, agency violations have no rewind procedure. **KEEP** |
| `shared/ai_generated_mystery_and_internal_drive_plot_arc.md` (97) | AI-generated mystery & internal-drive plot arcs: seed mysteries without waiting to be asked; internal-only design data as background material. If the model never sees it, arcs wait passively for player prompts instead of driving. **KEEP** |
| `shared/banned_names_instruction.md` (11) | Critical naming restrictions from `banned_names.md` (with `{banned_names}` slot) + enforcement note. If the model never sees it, banned names re-enter narration. The `{banned_names}` slot is filled by the builder (`_add_banned_names_to_system`), not by the file. **KEEP** |
| `shared/canonical_state_anchor.md` (27) | Canonical State Anchor (named entities): before stating a fact about a named entity the player could have established, check canonical sources (`core_memories`, entity manifest, named-NPC/faction data, setting). If the model never sees it, named-entity facts drift from canon. This file is on the compaction critical list for good reason. **KEEP** |
| `shared/character_value_invariants.md` (65) | Character Value Invariants (mandatory, every turn writing `player_character_data`): ability scores, gold, spells and other field values governed per-field, not per-phase. If the model never sees it, sheet values drift turn by turn. **KEEP** |
| `shared/class_resource_pool_rule.md` (1) | Any class feature (new level or earlier) granting limited uses per rest draws from the class resource pool. If the model never sees it, limited-use features double-count pools. **KEEP** |
| `shared/combat_state_contract.md` (146) | Combat State Session Tracking: complements enemy HP tracking; initiative-based tactical combat contract (turn order, session state). If the model never sees it, tactical combat loses session tracking and turn order. On the compaction critical list. **KEEP** |
| `shared/combat_state_reminder.md` (7) | Combat State Enforcement: if the turn narrates the start of tactical combat (initiative rolled, turn order matters), enforce the contract; quick/single-turn combat distinguished. If the model never sees it, combat starts are narrated without the contract. **KEEP** |
| `shared/companion_arc_event_example.md` (35) | Companion Arc Event canonical output envelope (companion, arc_type, phase, …). If the model never sees it, arc events arrive in ad-hoc shapes. **KEEP** |
| `shared/companion_persona_privacy.md` (1) | Secret Persona Invariant: never reveal MBTI letters/codes or alignment labels. If the model never sees it, internal persona data leaks into narrative. **KEEP** |
| `shared/dc_calibration.md` (80) | Canonical DC Calibration & Strategy Ledger: calibrate final DC dynamically for execution checks/contests/operations; base DC, strategy/argument adjustment, ledger discipline. If the model never sees it, DCs are set by feel and drift with roll knowledge (the dice file's fairness warning depends on this ledger). **KEEP** |
| `shared/dice_code_execution.md` (177) | Dice Values Are Unknowable (code_execution): cannot know dice values without executing code; quantum-random framing; code-execution procedure, stdout contract references, result handling. If the model never sees it, code-execution turns narrate invented dice. **KEEP** |
| `shared/dice_notation_contract.md` (52) | Dice Notation Contract & Resolution Rules: exactly one dice term per notation (`1d20`, `1d20+5`, `2d6kh1`, …); separate feature-granted dice are separate roll entries. If the model never sees it, notations arrive unparseable or bundled. Shared by both dice files — the dedupe run 1 asked for already exists. **KEEP** |
| `shared/dice_stdout_contract.md` (8) | Every dice code block emits exactly one valid JSON object/array with the roll records, via the standard JSON encoder, printed once; no prose, f-strings, or raw dicts. If the model never sees it, code-execution dice output is unparseable. **KEEP** |
| `shared/fair_high_power_challenge.md` (44) | Fair High-Power Challenge: no stat inflation to match player tier; challenges must stay fair when the player is far above baseline difficulty. If the model never sees it, high-tier play degenerates into inflated opponents. **KEEP** |
| `shared/graveyard_instructions.md` (6) | Deceased Characters (permanent death — do not reanimate): listed NPCs cannot speak, act, appear, or be interacted with; `{deceased_list}` slot. If the model never sees it, the dead return. **KEEP** |
| `shared/hidden_identity_knowledge_boundaries.md` (50) | Hidden-Identity Knowledge Boundaries: every NPC's knowledge of the player's true identity/capabilities/allegiances/reputation is bounded by direct observation and established channels. If the model never sees it, NPCs act on knowledge they cannot have. **KEEP** |
| `shared/lethal_opening_server_tool_protocol.md` (24) | Lethal Episode Opening Protocol (the one exception): a player-initiated lethal opening requests the roll in the same response object — declare intent, set the structured conflict fields, request the roll. If the model never sees it, lethal openings either stall a turn or resolve without a server roll. **KEEP** (narrow exception to the usual declare-then-wait flow, stated as such) |
| `shared/level_up_amendment_completeness_reminder.md` (4) | Level-Up Amendment Must Change a Mechanic: if the context shows an explicit review and the response amends selected mechanics, `state_updates` must reflect a mechanic change; every sheet-changing review alternative in `planning_block` must be complete. If the model never sees it, amendments arrive as no-op reviews. **KEEP** |
| `shared/level_up_announcement_contract.md` (19) | Level-Up Announcement: applies only to narrative-emitting gameplay turns (god mode excluded); when the model authors a higher level than the incoming sheet, announce per contract. If the model never sees it, level-ups pass without announcement or announce on admin turns. **KEEP** |
| `shared/level_up_announcement_reminder.md` (5) | Level-Up Announcement Enforcement: if this response's level exceeds the incoming sheet's, announce; an open/committed/persisted review alone does not trigger. If the model never sees it, the announcement trigger is misread as review state. **KEEP** |
| `shared/mechanics_combat_roll_display_rules.md` (13) | Mandatory Combat Roll and HP Display Rules, regardless of dice strategy: always show attack and damage rolls; `action_resolution` display discipline. If the model never sees it, combat display loses its both-rolls rule on one strategy path. **KEEP** |
| `shared/mechanics_leveling_protocol_intro.md` (22) | Leveling Tiers table (Local 1–4, Regional 5–10, …) plus tier scope/threats. If the model never sees it, leveling rewards lack their tier frame. **KEEP** |
| `shared/mechanics_leveling_rewards_body.md` (312) | Level and reward mechanics: model emits its reward decision once in `reward_event` (`xp.gained`, `xp.tier`); cumulative character XP is server-owned and derived; tier/threat/reward tables and procedures. If the model never sees it, reward decisions scatter across fields and cumulative XP is double-authored. The server-owned-cumulative-XP note is delegation language, not a server recomputation instruction. **KEEP** |
| `shared/mechanics_system_protocol.md` (68) | Game Mechanics Protocol: no narrative during character creation (meta-game only: stats/abilities/equipment); opening protocol; campaign setup; mechanics procedures. If the model never sees it, creation turns narrate story and mechanics turns lose their opening discipline. **KEEP** |
| `shared/no_forced_ruler_progression.md` (47) | No Forced Ruler Progression: model must not steer the player toward rulership/sovereign authority or "you are the only one who can lead"; NPCs do not volunteer rulership. If the model never sees it, campaigns drift into forced-ruler arcs. **KEEP** |
| `shared/npc_canon_anchoring.md` (25) | NPC Canon Anchoring (mandatory): ground every NPC behaviour, prop, and equipment item in context already provided (`core_memories`, entity manifest, named-NPC/faction data, setting). If the model never sees it, NPCs acquire ungrounded gear and habits. **KEEP** |
| `shared/npc_knowledge_boundaries.md` (63) | NPC Knowledge Boundaries (general rule): every NPC's knowledge of the player (identity, capabilities, allegiances, reputation, specific scene facts) is bounded by direct observation and established channels. If the model never sees it, NPC omniscience breaks continuity. (Distinct from the hidden-identity file, which covers concealed identity specifically — the pair is a general/specific split, not a duplicate.) **KEEP** |
| `shared/npc_personality_trifecta.md` (35) | NPC Personality Trifecta (Want / Fear / Boundary): every named NPC must have a three-axis personality record driving decisions independently of the player. If the model never sees it, NPC decisions collapse to player-pleasing. **KEEP** |
| `shared/npc_visual_identity.md` (1) | When multiple focal NPCs are visibly present, make each response's prose self-contained with brief nose/jaw/hair cues (so image and prose agree per NPC). If the model never sees it, multi-NPC prose loses visual distinguishability. **KEEP** |
| `shared/owed_level_up_reminder.md` (2) | Owed Level-Up: saved sheet level vs. saved grant level earned but not applied. If the model never sees it, owed level-ups are forgotten between turns. **KEEP** |
| `shared/pcd_crossing_completeness_reminder.md` (10) | Level-Crossing Sheet Completeness: on every ordinary turn, compare current canonical level/XP against the sheet and complete hit dice, resources, and derived fields on crossing. If the model never sees it, level crossings leave half-updated sheets. **KEEP** |
| `shared/rag_output_contract.md` (8) | Output Contract (always enforced): author ordinary numeric XP awards only in `reward_event` (`xp.gained`, `xp.tier`) per the Leveling Pace Contract; never repeat XP/level progress in a header, narrative, or other field. If the model never sees it, XP leaks into prose and double-counts. On the compaction critical list. **KEEP** |
| `shared/require_reward_event.md` (1) | Mandatory: `state_updates.reward_event` is required in every response; do not omit it. If the model never sees it, reward decisions go missing on turns where nothing else forces the field. **KEEP** |
| `shared/rest_anchored_dialog.md` (26) | Rest-Anchored Companion Dialog Opportunities: trigger (rest-anchored beat — long/short rest, meals, morning watch, …) plus dialog opportunity rules. If the model never sees it, companion dialog never fires on rests. **KEEP** |
| `shared/reward_event_contract.md` (123) | Reward Event Contract (sole reward-authoring surface): on every time-advancing gameplay turn, make an explicit reward decision in `state_updates.reward_event`; the server materializes cumulative state from it. If the model never sees it, reward authoring scatters and the server/materialization boundary collapses. **KEEP** |
| `shared/saved_default_pacing_note.md` (24) | Default Significance Pacing (active D&D 5e Leveling Pace Contract only): for a tracked challenge/objective, structured state must record completion; narrative progress or initiation alone is not completion. If the model never sees it, objectives complete on narration. **KEEP** |
| `shared/saved_progression_fact.md` (2) | Saved Progression: saved sheet level and cumulative XP, for the model's active-rule calculation. If the model never sees it, progression math starts from invented numbers. **KEEP** |
| `shared/skill_selection_rules.md` (8) | Skill Selection & Schema Coexistence Rules (mandatory): canonical `skills` list must be non-empty skill IDs; D&D 5e classes pick N skills from their lists. If the model never sees it, skill lists arrive empty or freeform and break the schema. **KEEP** |
| `shared/social_hp_no_cooldown.md` (3) | Social HP Damage Rule (binding across all prompt variants): if a turn's roll meets/beats `roll_dc`, `social_hp_damage` must be ≥ 1 (1–2 by margin); if the roll fails, the complementary rule applies. If the model never sees it, social-HP damage is optional and the system is toothless. **KEEP** |
| `shared/tier_pressure.md` (43) | Tier Pressure (anti-scaling whiff + consequence-hiding): shared by Story, Dialog, HeavyDialog, and Spicy agents so the parity band holds across modes; tier compression rules. If the model never sees it on a dialog-mode turn, tier parity holds in story but not in dialog. **KEEP** |
| `shared/user_directive_supremacy.md` (70) | User Directive Supremacy (mandatory): if the player's freeform input explicitly names values for any character-creation field (ability scores, etc.), those values are authoritative. If the model never sees it, explicit player choices are overridden by defaults or suggestions. **KEEP** |
| `shared/witness_based_reveal_continuity.md` (47) | Witness-Based Reveal Continuity: when a reveal happens (hidden ability, concealed identity, true allegiance), persist the witness set and honour it in later turns. If the model never sees it, reveals are forgotten and NPCs un-know what they witnessed. On the compaction critical list. **KEEP** |
| `shared/world_sim_candidate_faction_tool.md` (1) | When selecting a rival/target from existing factions, emit a read-only faction-selection tool call (separate from the narrative decision). If the model never sees it, faction targeting is narrated without the tool record. **KEEP** |
| `shared/world_sim_realism.md` (27) | World Simulation Realism Contract: before proposing a world development or assessing plausibility, separate known facts, reported beliefs, and inferences, and check causality. If the model never sees it, world developments assert inference as fact. **KEEP** |
| `shared/zero_roll_rule.md` (22) | Trivial/Routine Action Zero-Roll Rule: under D&D 5e (PHB p. 174), a check/roll is called for only when the action is meaningfully uncertain or consequential; trivial/routine/within-authority actions auto-succeed without a roll. If the model never sees it, every action rolls and trivial play grinds to dice. **KEEP** |

## §6 — Verdict counts (Phase 2)

Counts below are tallies of table rows in §§2–5, verified by script against
this file: every data row was counted once per bold verdict it states. A
row sometimes groups a family of symbols (e.g. the 7 level-up-cache symbols
in one §2 row, the 18 companion-rendering helpers in one §3 row, the 13
semantic symbols in one §2 row, the 6 portrait text files in one §5 row,
the 10 scene files in one §5 row, the 2 level-up JSON schemas in one §5
row). Grouped rows therefore undercount symbols/files relative to a
per-symbol expansion, but the verdicts do not change under expansion, since
every grouped row states one verdict for all its members. Row counts are
exact; expanded symbol counts are strictly larger for the grouped rows
only.

- **§2 `agents.py` (70 rows): KEEP 51, ADAPT 12, DELETE 7.** DELETE rows
  (7): the 3 classifier thresholds, `character_creation_semantic_completion_allowed`,
  `_should_skip_classifier_context`, `_resolve_semantic_classification`,
  and the 13-symbol semantic-dispatch row. ADAPT rows (12): the
  `_detect_conclude_signal` row (explicit-choice branch only),
  `_resolve_conclude_phases`, `_resolve_character_creation_completion`,
  `_resolve_rewards`, the `_resolve_character_creation_state` /
  `_resolve_dialog_state` row, `_resolve_rewards_fallback`,
  `_extract_routing_state`, `_RoutingState`, `_ROUTING_RESOLVERS`,
  `get_agent_for_input`, the `LEVEL_UP_AUTHORING_EXEMPT_AGENTS` /
  `NON_TURN_ROUTING_AGENT_NAMES` row, and `PortraitGeneratorAgent`
  (truncation). The single largest DELETE mass in the whole audit is the
  semantic routing family.
- **§3 `agent_prompts.py` (45 rows): KEEP 36, ADAPT 8, DELETE 1.**
  (The DELETE count is rows, not symbols: the
  `_is_companion_shaped` / `_has_ambiguous_entity_identity` row deletes 2
  symbols. ADAPT rows are the location-schema filter, the lite-schema
  family, the SRD feature block, the companion projection family, the
  high-tier-NPC reminder family, the level-up row family, the DC-ledger
  extractor, and the temporal-correction builders.)
- **§4 (28 rows): KEEP 18, ADAPT 5, DELETE 6.** By file: `prompt_loader.py`
  KEEP 2; `entity_instructions.py` KEEP 6, ADAPT 2, DELETE 6 (the globals
  row states both a KEEP and a DELETE, hence 29 verdict mentions over 28
  rows); `context_compaction.py` KEEP 10, ADAPT 3. `prompt_context_metrics.py`
  and `prompt_cache_usage_semantics.py` are verdict in prose in §§4.4–4.5
  (all KEEP: 15 metric functions + 1 constant set; 3 enums/dataclass +
  5 functions + 1 provider set), and `PROMPTS_README.md` is DELETE
  (shipped path) in §4.6 prose — neither is in the 28-row table count.
- **§5 prompt files (113 rows covering all 128 regular files): KEEP 123
  files, ADAPT 4 files, DELETE-from-runtime 1 file.** ADAPT files:
  `game_state_instruction.md` (faction block move),
  `narrative_system_instruction.md` (living-world dedupe),
  `living_world_instruction.md` (async-merge surface + dedupe),
  `character_creation_instruction.md` (creation/level-up split). DELETE
  from the runtime prompt set: `prompts/AGENTS.md` only (documentation,
  already excluded from loading; its 2 symlink aliases `CLAUDE.md` /
  `GEMINI.md` share the verdict and are not separate files). No gameplay
  prompt file is deleted. The 113 rows cover 128 files because 3 rows
  group multiple files (2 level-up JSON schemas, 6 portrait text files,
  10 scene files: 18 files in 3 rows).
- **§7 `prompt_utils.py` extra (8 verdict rows): KEEP 7, ADAPT 1
  (`prepare_story_context_entries_for_prompt`, serializer-only flag),
  DELETE 0.**
- **Phase 1 file verdicts (for comparison):** KEEP 3, ADAPT 2, DELETE 1,
  SPLIT 2 (§§1–2 above). Phase 1 and Phase 2 counts are not additive —
  Phase 2 rows are the decomposition of the Phase 1 file verdicts.

## §7 — Discovered adjacent file: `prompt_utils.py` (extra, outside run-1 scope)

`prompt_utils.py` (429 lines) builds campaign prompts and story-context
entries for prompts; it is not in run 1's group list, but `llm_service.py`
and the Dragon Knight template code call it on the prompt path, so leaving
it unexamined would leave a prompt-path gap. Its symbols, briefly (same
two-pass format, condensed because this file is an extra):

| Symbol | Justification + verdict |
|---|---|
| `RANDOM_CHARACTERS`, `RANDOM_SETTINGS`, `SEPARATOR`, `logger` | Random filler content constants (copied from `world_logic.py` to avoid circular imports) and a logger. Pass A: filler examples seed random campaigns; deleting them removes the random-seed path. Pass B: static example lists are prompt data, not decisions. **KEEP** |
| `resolve_wizard_ip_fields` | Returns normalized custom-wizard IP fields (universe/timeline/plot), stripped or empty. Pass A: wizard intake needs clean IP fields or campaign setup carries whitespace/garbage. Pass B: stripping whitespace is normalization — which alone never justifies a field-aware transform, but this function transforms *form* (whitespace), not *values*, and its docstring documents a prior silent-drop bug it deliberately avoids (it does not force-clear on an unconfirmed Dragon Knight flag). **KEEP** (as form normalization only) |
| `stamp_wizard_intake_answers` | Persists structured IP intake, skipping persistence on a confirmed Dragon Knight match, gated by the confirmed match rather than the caller's `is_dragon_knight` claim. Pass A: intake answers must persist for custom campaigns or the share payload loses them. Pass B: persistence gated by a confirmed canonical match is durable-write integrity, not a domain guess — the gate prevents a caller's claim from laundering non-canonical inputs into a genuine DK campaign. **KEEP** |
| `_convert_and_format_field` | Converts/formats a single campaign-prompt field value. Pass A: campaign prompt construction needs field formatting. Pass B: formatting, not value selection. **KEEP** |
| `_build_campaign_prompt`, `_build_campaign_prompt_impl` | Build the campaign prompt from character/setting/description/old_prompt/universe/timeline/plot, including the verbatim-`old_prompt` return path on a confirmed canonical-template match. Pass A: campaign creation needs a prompt; the verbatim path preserves a canonical template exactly. Pass B: verbatim return of a confirmed canonical template is faithful transport; the impl split exists to separate matching from building. **KEEP** |
| `parse_campaign_prompt` | Parses a campaign prompt string back into fields. Pass A: legacy prompts must be readable as fields for migration/display. Pass B: parsing stored text into fields is serialization, not authorship. **KEEP** |
| `_deduplicate_story_entry_description`, `_is_canonical_initial_story_entry` | Deduplicate a story entry's description against its text; recognize the canonical initial story entry. Pass A: duplicated descriptions bloat story context; the canonical-entry check protects the first entry from dedupe. Pass B: dedupe of identical text is formatting; canonical-entry recognition is a structural check on position/shape, not a content judgement. **KEEP** |
| `prepare_story_context_entries_for_prompt` | Prepares story-context entries for prompt inclusion (with god-mode description handling). Pass A: story context must reach the prompt in prepared form or turns lose history. Pass B: preparation/serialization of model-authored history is assembly; the function must not filter entries by content (no such filter is present in its signature/docstring, but its body was only skimmed — flagged). **ADAPT** (keep as a serializer; delete any content-based entry filtering if a full read finds one) |
| (Unverified tail) | `prompt_utils.py` may contain further helpers below the skimmed head (the AST inventory in the working notes lists exactly the 10 symbols above plus constants, so no tail is unaccounted for — the "skimmed body" flag above applies to `prepare_story_context_entries_for_prompt`'s body only, not to the inventory). |

## Coverage statement (exact)

- **Code files:** `agents.py` — AST-complete inventory (17 agent classes +
  `PortraitGeneratorAgent`, 17 dispatch resolvers, 11 semantic handlers, all
  module helpers/constants); per-symbol verdict rows in §2; sequential
  line-by-line full read NOT claimed (see Coverage). `agent_prompts.py` —
  AST-complete inventory (`AgentProtocol`, ~90 module functions, 59
  `PromptBuilder` methods); per-symbol verdict rows in §3; sequential
  line-by-line full read NOT claimed. `prompt_loader.py`, `entity_instructions.py`,
  `context_compaction.py`, `prompt_context_metrics.py`,
  `prompt_cache_usage_semantics.py` — full text read, per-symbol rows in §4.
  `prompt_utils.py` — AST inventory + skimmed bodies, rows in §7 (extra).
- **Prompt files:** 128 regular files under `mvp_site/prompts/` — every file
  has a row in §5 (top level §5.1, divine/multiverse §5.2, injection §5.3,
  shared §5.4), with headings/sections accounted for per file (grouped
  where they share a verdict). Plus `prompts/AGENTS.md` and its 2 symlink
  aliases, verdict as documentation only. Plus `PROMPTS_README.md`, verdict
  in §4.6. Total paths accounted for: 128 + 1 policy file + 2 aliases +
  1 README = 132 paths, 130 of them under `prompts/`.
- **Untouched scope (nothing hidden):** (a) the sequential full read of
  `agents.py` and `agent_prompts.py` (caveat above); (b) `modal_conclude_policy.py`
  bodies (only the `agents.py` wrapper's classifier arguments were
  verdict here); (c) `entity_preloader.py` shim internals beyond its
  re-export role; (d) the body of `PromptBuilder._resolve_campaign_tier`
  (read-vs-compute flag in §3.3) and of `prepare_story_context_entries_for_prompt`
  (filter flag in §7). No verdict in this file depends on (b)–(d) except
  where the row explicitly flags the dependency; no verdict is fabricated
  for any of them.
- **Out-of-scope files noticed but not verdict:** `portrait_generator_agent.py`,
  `scene_prompt_ablation.py`, `scene_illustration_policy.py` (code; their
  prompt files are verdict in §5), `intent_classifier.py` /
  `intent_classifier_warmup.py` (separate pilot; referenced only as the
  deleted routing source).
- **Repo files changed:** none. This file (`~/workspace/plans/audit/agents-prompts.md`)
  is the only file written by this run.

## Evidence log (this run, read-only, local tree only)

- Local tree: `~/workspace/repos/worldarchitect.ai` (main-branch ZIP tree).
  Zero GitHub API/MCP calls; zero browser actions.
- Run-1 file read: `~/workspace/plans/audit/agents-prompts.md` (provisional
  verdicts + checklist), superseded by this rewrite.
- Local reads: `mvp_site/agents.py` (header, dispatch table, routing
  greps, per-class docstrings, `get_agent_for_input` tail),
  `mvp_site/agent_prompts.py` (`PATH_MAP`, loader pipeline, per-function
  docstrings), `mvp_site/prompt_loader.py` (full),
  `mvp_site/entity_instructions.py` (full),
  `mvp_site/context_compaction.py` (full),
  `mvp_site/prompt_context_metrics.py` (full),
  `mvp_site/prompt_cache_usage_semantics.py` (full),
  `mvp_site/PROMPTS_README.md` (full), `mvp_site/prompts/**` (heading
  inventory + first-content survey of all 130 paths; full text of the 8
  README files, conclude/level-up set, both dice files, both mechanics
  files, and all fragments under 30 lines), `mvp_site/prompts/AGENTS.md`
  (full), `mvp_site/AGENTS.md` and `mvp_site/AGENTS.md`'s parent
  `AGENTS.md` (house rules, read per runtime note; audit scope and
  read-only posture unchanged by them).
- Reference counts: full-tree `grep`/`rglob` searches over `mvp_site/`
  (production + tests) for the symbols in §§2–3, and a basename +
  `PROMPT_INCLUDE` graph over `mvp_site/prompts/` for §1.
- No repo writes, commits, pushes, deletes, or changes were made or
  attempted. No browser navigation, purchase, sign-in, click, or form
  action was attempted.
