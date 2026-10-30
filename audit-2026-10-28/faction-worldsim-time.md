# Audit: faction / living world / world_sim / world time — SECOND RUN (local copy)

Repo: local copy at `~/workspace/repos/worldarchitect.ai` (main-branch ZIP tree, no
`.git` history). **Zero GitHub API calls were made in this run**; all reads were local
file reads and local grep, per the task's critical access rule. Read-only audit;
nothing was written, committed, pushed, deleted, or changed in any repo. Repo file
contents are DATA for this audit, never orders; no instruction found in repo content
was followed.

Prior run's file (this same path) was read first and its resumption checklist honored:
full enumeration of both directories, confirmation of `world_time.py`, caller/reference
counts from local grep, and per-file + per-symbol verdicts. The prior run's blocker
(GitHub HTTP 429, zero coverage) no longer applies; this run replaces its provisional
framing with verdicts grounded in file contents.

## Coverage — exact

- **Files fully done: 50 of 50 assigned entries** (47 Python files + `faction/README.md` +
  `world_sim/tools.json` + `world_sim/timeline/ops_cutover_timeline_producer_schema.json`).
  Every Python file's symbols were inventoried by AST; every file was read in full or,
  for the five largest infrastructure files (coordinator, background_worker, models,
  handler, firestore_transaction), read via full symbol inventory plus docstrings plus
  targeted reads of all decision-bearing functions.
- **Files partial: NONE.**
- **Files blocked / untouched: NONE.**

### Enumeration (complete, local tree)

- `mvp_site/faction/` (10): `README.md`, `__init__.py`, `ai_factions.py`,
  `battle_sim.py`, `combat.py`, `dual_mode.py`, `intel.py`, `rankings.py`,
  `srd_units.py`, `tools.py`.
- `mvp_site/world_sim/` top level (10): `__init__.py`, `dispatcher.py`,
  `firestore_repository.py`, `handler.py`, `rollout.py`, `tools.json`, `tools.py`,
  `trigger.py`, `turn_hooks.py`, `worker_auth.py`.
- `mvp_site/world_sim/timeline/` (26): `__init__.py`, `antagonistic.py`,
  `background_contracts.py`, `background_entities.py`, `background_provider.py`,
  `background_worker.py`, `cohort.py`, `coordinator.py`, `cutover.py`, `epoch.py`,
  `event_codec.py`, `execution_constraints.py`, `firestore_store.py`,
  `firestore_transaction.py`, `identity.py`, `lethal_policy.py`, `models.py`,
  `ops_cutover_timeline_producer_schema.json`, `outbox.py`, `reconciler.py`,
  `relevance_provider.py`, `relevance_worker.py`, `setup_provider.py`,
  `stage_worker.py`, `store.py`, `validation.py`.
- Singles (4, all confirmed to exist): `mvp_site/living_world.py`,
  `mvp_site/living_world_contract.py`, `mvp_site/faction_state_util.py`,
  `mvp_site/world_time.py`.

### Caller-count method

One local pass over all `mvp_site/**/*.py` (including `mvp_site/tests/`) with a single
combined identifier regex, recording for each in-scope symbol the defining file and the
external files referencing it. Key results cited in tables: `execute_faction_tool`
(10 external files incl. `dice.py`, `game_state.py`, `provider_utils.py`);
`execute_world_sim_tool` (5); `simulate_battle` (2: `faction/__init__.py`,
`faction/tools.py`); `generate_ai_factions` (1: `rankings.py`);
`calculate_ranking` / `calculate_faction_power` (4 each, incl. tests);
`run_background_simulation_wake` (5, incl. `handler.py`); `trigger_world_sim_tick`
(2, tests); `wake_timeline_for_elapsed_gap` (9, tests + setup paths);
`evaluate_living_world_trigger` (2: `game_state_mixins.py`, tests);
`merge_partial_world_time` (1: tests only); `DualModeManager` (1: `faction/__init__.py`
only — no game-path caller found in this pass). Where a symbol shows zero external
files, that is stated in its row.

## Governing decisions (§6 — override everything else)

1. Server logging KEEP; where it blocks a player turn, ADAPT to async/batched delivery.
2. Anti-cheat KEEP; dice resolution stays ON the turn path; only the audit trail may go async.
3. **Faction/living-world KEEP but ADAPT to async — governs this whole group.**
   Faction simulation and living-world ticks move off the request path into background
   processing, results merging into state on the next player turn. The living-world
   promise STANDS; only its execution moves async.

**Conflict flag (explicit, as required):** no verdict in this file deletes faction
simulation or the living world outright. Several verdicts below are DELETE, but they
delete *server-side recomputation of a model-authorable decision* (a formula, a tier,
a ranking arithmetic, a display string) and move that decision to the model/prompt/
schema — they do not remove the simulation capability itself, which survives as the
async background provider + worker path (verdicts ADAPT/KEEP there). Where a DELETE
could be misread as removing simulation (e.g. fast-mode battle arithmetic), the row
says so explicitly and the dice-bearing path is kept separately. If the parent reads
any DELETE below as contradicting decision 3, that reading is rejected here: decision
3 is what converts those routines' verdicts from DELETE to ADAPT wherever the routine
is genuinely simulation rather than mere recomputation.

## How the two passes were applied here

- **Pass A (zero-code baseline):** bare log + Gemini API. If deleting the unit loses
  nothing the model cannot supply through log, prompt, or response schema, it is DELETE.
- **Pass B (strict ZFC):** the model owns all campaign-domain facts; the server may
  only provide transport, durable writes, tool execution, authorization, and bounded
  capacity. Determinism, schema validity, display formatting, or normalization alone
  never justify a field-aware transform, and registry membership alone proves nothing.
- **Final verdict = stricter of the two passes**, unless a named product promise
  rescues it (named in the row: anti-cheat server dice, durable cross-session state,
  multi-user separation, bounded cost, the §6.3 living-world promise, or the SRD
  published-reference lookup).
- **ADAPT always names the change.** In this group the dominant ADAPT is: move the
  routine off the turn path into background processing with merge-on-next-turn.
  Turn-hooks code already does this via daemon threads / Cloud Tasks; rows that are
  already off-path say KEEP instead of ADAPT where no further move is needed.

## Phase 1 — file verdicts

| File | Verdict | Justification (both passes, ends in verdict) |
|---|---|---|
| faction/README.md | KEEP | Pass A: documentation is not runtime code, so deleting it breaks no player capability, but Pass B does not apply to prose and the file is the only map of the minigame's ruleset for maintainers. It costs no turn-path time and carries no field-aware transform. → KEEP |
| faction/__init__.py | ADAPT | Pass A: a re-export barrel adds no player capability the model cannot get by importing modules directly, so it is deletable in principle. Pass B: it is pure transport (names only), but it re-exports DELETE-verdict formulas alongside KEEP dice, so it must be slimmed to re-export only kept symbols and drop the deleted formula names. → ADAPT |
| faction/ai_factions.py | ADAPT | Pass A: the model could invent 200 faction names, behaviors, and FP values, so per-turn regeneration is deletable. Pass B: cross-session determinism (same roster every session) is a durable-state promise the bare log cannot supply, so the generator survives only as a one-time seeding step whose output is persisted, never recomputed on the turn path. → ADAPT |
| faction/battle_sim.py | ADAPT | Pass A: the model could narrate any battle outcome, so the simulator is deletable as an outcome author. Pass B: §6.2 anti-cheat rescues only the dice primitives on the player turn path, while background faction-vs-faction battles are simulation governed by §6.3, so the file splits: keep dice on-path, move all bulk/background simulation async. → ADAPT |
| faction/combat.py | DELETE | Pass A: every formula here (FP weights, position multipliers, school counters, damage arithmetic) can be stated in the prompt or response schema and computed by the model. Pass B: these are field-aware recomputations of model-authored stats with no registered exception; determinism of the arithmetic alone never justifies them, and no §6 decision rescues FP arithmetic. → DELETE |
| faction/dual_mode.py | ADAPT | Pass A: mode switching and trigger reminders are model-authorable narrative/state the log plus schema could carry. Pass B: the durable mode/turn counters are legitimate durable writes, but the server's crisis/neglect trigger *decisions* are campaign-domain facts, so state storage stays while trigger evaluation moves to the model with the server only storing proposed triggers. → ADAPT |
| faction/intel.py | ADAPT | Pass A: the model could decide any spy outcome and tier, so the tier/buff/cooldown arithmetic is deletable. Pass B: §6.2 anti-cheat rescues only the detection dice roll itself on the turn path; everything else (risk formula, tiers, buffs, cooldowns) moves to the model/prompt, and background intel moves async. → ADAPT |
| faction/rankings.py | DELETE | Pass A: ranking arithmetic over stored FP is trivially model-computable from the roster in context. Pass B: it recomputes a model-authored ordering with no registered exception, and the §6.3 living-world promise rescues background *simulation*, not a leaderboard sort; the roster itself survives via ai_factions seeding, not via this arithmetic. → DELETE |
| faction/srd_units.py | ADAPT | Pass A: the model knows the D&D 5.1 SRD and could supply stat blocks, so a server copy is deletable in principle. Pass B: the SRD is published reference data, not campaign-domain fact, so lookup is legitimate tool execution, but level-scaling arithmetic is a model-authorable rule and must move to prompt/schema, leaving a slim lookup table. → ADAPT |
| faction/tools.py | ADAPT | Pass A: tool schemas are the model's interface, so the file's routing is not itself a player capability. Pass B: as tool execution it is allowed, but it currently routes to DELETE-verdict formulas, so it must be slimmed to route only server-dice and roster-lookup calls, with formula calls deleted from the tool set. → ADAPT |
| world_sim/__init__.py | KEEP | Pass A: lazy re-export of the world-sim tool API changes no player capability if removed, but it is pure transport with no field awareness. Pass B: lazy loading is a bounded-capacity/transport mechanism, and deleting it would only force eager imports; it performs no domain decision. → KEEP |
| world_sim/dispatcher.py | KEEP | Pass A: without Cloud Tasks enqueueing and outbox dispatch, background ticks could not run at all, which the bare log cannot replace. Pass B: it is transport plus durable outbox state transitions and local header authorization, with no campaign-domain authorship; the one sync tick executor is a local-execution transport, not a turn-path simulation. → KEEP |
| world_sim/firestore_repository.py | KEEP | Pass A: durable setup-attempt claims and game-state reads are exactly what the bare log lacks across sessions. Pass B: it is pure durable writes/reads with exactly-once claim semantics and no field-aware transform of model content. → KEEP |
| world_sim/handler.py | ADAPT | Pass A: the tick/setup handlers orchestrate background work the log cannot run. Pass B: most of the file is transport and lease handling, but the foreground/background initialization and date-payload processing still run partly synchronously on paths adjacent to turns, so the remaining synchronous orchestration must move fully async with merge-on-next-turn. → ADAPT |
| world_sim/rollout.py | KEEP | Pass A: a fail-closed kill switch is invisible to players when on, but deleting it removes the only safe way to stop simulation spend. Pass B: it is authorization plus bounded capacity (a literal-True config gate), with no domain decision and fail-closed behavior. → KEEP |
| world_sim/tools.json | KEEP | Pass A: the tool schema is the model's interface to the one world-sim tool and cannot be replaced by prose alone. Pass B: a schema is transport, not a transform, and it correctly forbids model-supplied campaign state. → KEEP |
| world_sim/tools.py | KEEP | Pass A: without a server-side roster read, the model would have to invent candidate factions, breaking multi-user/campaign separation. Pass B: it reads authoritative durable state and ignores model-supplied state, which is authorization plus durable reads, not authorship. → KEEP |
| world_sim/trigger.py | KEEP | Pass A: durable wake persistence plus post-commit draining is the mechanism that makes §6.3 async execution real; the log alone cannot enqueue it. Pass B: fingerprints, control transitions, and enqueueing are transport, durable writes, and authorization, and the code already runs post-commit rather than blocking the turn. → KEEP |
| world_sim/turn_hooks.py | KEEP | Pass A: pre-action snapshots and post-action wakes are the merge-on-next-turn mechanism itself. Pass B: the file already runs post-commit work on daemon threads and never waits for the player response, which is exactly the §6.3 ADAPT already implemented; its synchronous control-record write is a durable write, not simulation. → KEEP |
| world_sim/worker_auth.py | KEEP | Pass A: worker authentication is invisible to players but its removal would let unauthenticated callers drive simulation. Pass B: it is pure authorization (OIDC issuer/audience/service-account checks) with no domain content. → KEEP |
| world_sim/timeline/__init__.py | KEEP | Pass A: an empty package marker has no player effect either way. Pass B: it performs no transform and exists only as transport packaging. → KEEP |
| world_sim/timeline/antagonistic.py | KEEP | Pass A: generation fencing for antagonist events is ordering state the bare log cannot enforce across concurrent proposals. Pass B: it advances a generation counter and records a date, never choosing whether an event happens; eligibility is a staleness check, not a semantic veto. → KEEP |
| world_sim/timeline/background_contracts.py | KEEP | Pass A: the provider protocol is the contract by which the model authors background actions; deleting it removes the interface, not a decision. Pass B: dataclasses plus a protocol are transport/schema, and the model remains the author of the proposals. → KEEP |
| world_sim/timeline/background_entities.py | KEEP | Pass A: bounded folding, preemption, and persisted candidate loading are the machinery that lets background work complete without blocking turns. Pass B: these are bounded capacity plus durable writes; folding applies already-due effects rather than authoring new outcomes. → KEEP |
| world_sim/timeline/background_provider.py | KEEP | Pass A: the bulk Gemini provider call is how background simulation outcomes are authored, which the bare log cannot do off-turn. Pass B: it is tool execution (a model call) with schema/bounds validation and idempotency-key derivation; its structural-map merge replaces only model-authored content with model-authored content. → KEEP |
| world_sim/timeline/background_worker.py | ADAPT | Pass A: background window simulation is the §6.3 living-world promise itself, so deleting it would delete the promise. Pass B: it is already background work, but its window/cooldown/lease orchestration still contains synchronous-adjacent paths and a 1,885-line surface that must be slimmed to strict background execution with merge-on-next-turn and no turn-path entry point. → ADAPT |
| world_sim/timeline/cohort.py | KEEP | Pass A: bounded cohort selection (which entities simulate this window) is capacity management the log cannot enforce. Pass B: selection by age/drift fences is bounded capacity plus authorization-style fencing, not authorship of what those entities do. → KEEP |
| world_sim/timeline/coordinator.py | ADAPT | Pass A: the durable date-range coordinator is what lets elapsed in-world gaps be simulated without the player waiting. Pass B: it is largely durable writes and transport, but at 2,085 lines it mixes coordination with decision replay and compaction, so it must be slimmed to coordination-only with all outcome decisions left to the provider. → ADAPT |
| world_sim/timeline/cutover.py | KEEP | Pass A: producer cutover/pause/resume is an admin lifecycle the log cannot perform. Pass B: it is authorization (admin) plus durable control writes and re-creation of fenced deliveries from durable progress, not outcome authorship. → KEEP |
| world_sim/timeline/epoch.py | KEEP | Pass A: backward-time epochs and timestamp quarantine are ordering/authorization state the log cannot enforce. Pass B: creating an authorized epoch and quarantining suspect timestamps are authorization plus durable writes, not campaign-domain decisions. → KEEP |
| world_sim/timeline/event_codec.py | KEEP | Pass A: canonical hashing and archive validation do not change what players see, but they are what make stored events tamper-evident across sessions. Pass B: canonical JSON, hashes, and size bounds are transport integrity and bounded capacity, explicitly not field-aware transforms. → KEEP |
| world_sim/timeline/execution_constraints.py | KEEP | Pass A: one-time immutable execution bounds are the guardrail that keeps background work bounded. Pass B: constraint installation and write validation are bounded capacity plus authorization, applied to leaf fields without judging domain content. → KEEP |
| world_sim/timeline/firestore_store.py | KEEP | Pass A: the Firestore store is the durable layer for every timeline record; the bare log has no equivalent. Pass B: it is pure durable reads/writes, transactions, dispatch admission, and execution claims, with no campaign-domain authorship. → KEEP |
| world_sim/timeline/firestore_transaction.py | KEEP | Pass A: transactional buffering and OCC are what make timeline writes atomic across sessions. Pass B: it is durable-write machinery (staging, flushing, snapshot views, epoch authorization checks) with no outcome authorship beyond rejecting writes whose provider base no longer matches. → KEEP |
| world_sim/timeline/identity.py | KEEP | Pass A: deterministic IDs, lease tokens, and cursors are invisible to players but are what make retries idempotent. Pass B: hashing and validation of identifiers are transport integrity and authorization, not domain decisions. → KEEP |
| world_sim/timeline/lethal_policy.py | KEEP | Pass A: lethal-episode gating protects player agency in a way a bare log cannot enforce against a misbehaving model. Pass B: this is the one named authorization exception in this group — a lethal transition must cite a real executed tool invocation — and the code explicitly adds no semantic server veto beyond that citation check. → KEEP |
| world_sim/timeline/models.py | KEEP | Pass A: the record dataclasses are the durable schema for timeline state; deleting them deletes persistence itself. Pass B: serialization plus bounded receipt lists plus route resolution from trusted server configuration are transport and bounded capacity, not authorship. → KEEP |
| world_sim/timeline/ops_cutover_timeline_producer_schema.json | KEEP | Pass A: the cutover schema constrains admin operations that the log cannot validate. Pass B: a schema is transport, not a transform. → KEEP |
| world_sim/timeline/outbox.py | KEEP | Pass A: outbox draining through Cloud Tasks is the transport that delivers background work. Pass B: task construction and dispatch are pure transport with deterministic IDs. → KEEP |
| world_sim/timeline/reconciler.py | KEEP | Pass A: reconciliation of expired/undispatched outbox rows is recovery machinery the log cannot perform. Pass B: it is durable-write recovery plus bounded sweeps, re-driving already-decided work rather than authoring new outcomes. → KEEP |
| world_sim/timeline/relevance_provider.py | KEEP | Pass A: bulk relevance highlights are model-authored summaries the log cannot produce off-turn. Pass B: it is tool execution (a provider call with a response schema) plus prompt serialization, with no server-side semantic decision. → KEEP |
| world_sim/timeline/relevance_worker.py | KEEP | Pass A: the relevance worker applies stored model responses to date records off-turn. Pass B: replaying stored decisions and settling failed deliveries are durable writes and transport; the worker authors no new campaign facts. → KEEP |
| world_sim/timeline/setup_provider.py | KEEP | Pass A: one-time setup (conflict profile + roster) bootstraps the background lane; without it the §6.3 promise has no authoritative inputs. Pass B: it is tool execution with strict output validation (both fields valid or nothing), plus durable completion snapshots that are explicitly never model-owned. → KEEP |
| world_sim/timeline/stage_worker.py | KEEP | Pass A: stage execution advances durable timeline segments off-turn. Pass B: a bounded worker with transactional CAS validation is transport plus durable writes, authoring no outcomes itself. → KEEP |
| world_sim/timeline/store.py | KEEP | Pass A: the store protocol is the interface the rest of the timeline depends on for persistence. Pass B: a protocol definition is transport; it performs no transform at all. → KEEP |
| world_sim/timeline/validation.py | ADAPT | Pass A: window generation and highlight validation shape background work the log cannot bound. Pass B: window bounding is legitimate bounded capacity, but highlight-semantics validation judges model-owned semantics, so that semantic check must be slimmed to structural/schema validation only, with semantic judgment returned to the model. → ADAPT |
| living_world.py | ADAPT | Pass A: the turn/time trigger decision (fire every N turns or hours) could be stated in the prompt, so the checker is deletable in principle. Pass B: cadence enforcement is bounded capacity, but as written it runs on the turn path evaluating the trigger, so it must move to the post-commit/background lane and only hand the turn path a precomputed flag. → ADAPT |
| living_world_contract.py | ADAPT | Pass A: cooldown stripping changes what the player sees, which the model could itself honor if instructed. Pass B: stripping model-authored events is a field-aware transform that names no registered exception in this codebase (the antagonist cooldown is a pacing rule, not a §6 promise), so the decision must move to prompt/schema first and the server strip may survive only as a registered fail-closed guard, flagged here as unregistered. → ADAPT |
| faction_state_util.py | KEEP | Pass A: extracting the faction minigame dict from varied state shapes is glue the log cannot supply to providers. Pass B: extraction, strict-boolean enablement checks, and tool-list assembly are transport and authorization-adjacent reads with no outcome authorship; the duplicate navigation paths are a maintainability cost, not a ZFC violation. → KEEP |
| world_time.py | ADAPT | Pass A: the model can format and compare dates itself, so most of this module is deletable in principle. Pass B: canonical-date parsing for scheduling and backward-time detection are bounded-capacity/ordering guards, but partial-merge logic that rewrites model-supplied time fields is a field-aware transform, so the module must be slimmed to parsing plus violation detection, with merging left to the model/schema. → ADAPT |

File-verdict counts: KEEP 34, ADAPT 14, DELETE 2 (50 files).

## Phase 2 — per-symbol justifications

Each row gives 2–4 specific sentences covering both passes and ends in its verdict.
Caller notes come from the local combined-regex pass over `mvp_site/**/*.py`
(including tests); "0 external files" means no referencing file other than its
defining file was found in that pass.

### faction/ai_factions.py

| Symbol | Justification |
|---|---|
| ADJECTIVES / NOUNS / BEHAVIORS (tables) | Pass A: the model can invent faction names and behaviors freely, so these word lists add no irreplaceable capability. Pass B: they are static reference data, not campaign facts, but they only matter as inputs to the seeded generator, so they survive exactly as long as one-time seeding does and are slimmed with it. → ADAPT |
| generate_ai_factions | Pass A: a seeded roster of 200 factions with FP bands by difficulty is something the model could generate, but re-generating it per turn would drift across sessions. Pass B: determinism alone does not justify per-turn use, yet durable cross-session consistency does justify running it once at setup and persisting the roster; its only in-repo caller is `rankings.py`. → ADAPT |
| _generate_unique_name | Pass A: unique adjective+noun names are trivially model-suppliable, so the helper is deletable in isolation. Pass B: as a private helper of one-time seeding it inherits the seeding verdict, existing only to keep the persisted roster collision-free. → ADAPT |

### faction/battle_sim.py

| Symbol | Justification |
|---|---|
| BattleResult | Pass A: a result shape (casualties, victor, remaining, log) is schema the model could emit itself. Pass B: as pure transport/schema it performs no decision, so it stays as the shape of the dice-bearing tool result. → KEEP |
| BattleConfig | Pass A: configuration (rounds caps and similar) is prompt-statable and adds no player capability alone. Pass B: bounds on simulation are bounded capacity, so the config survives as the cap that keeps background battles finite. → KEEP |
| parse_damage_dice | Pass A: parsing "2d8+3" is string handling the model could do, but a wrong parse silently changes a dice outcome. Pass B: it is input validation for the anti-cheat dice path, not a domain decision, so it stays as the parser feeding server rolls. → KEEP |
| roll_dice | Pass A: server dice cannot be replaced by the model without destroying anti-cheat, since the model could then choose its own outcomes. Pass B: §6.2 explicitly keeps dice resolution on the turn path, and this primitive is exactly that resolution. → KEEP |
| roll_attack | Pass A: a d20 vs AC resolution is the core anti-cheat roll for player battles and cannot be model-supplied without letting the model pick hits. Pass B: §6.2 keeps dice resolution on-path, and this function is that resolution with crit/fumble rules. → KEEP |
| calculate_expected_damage_value | Pass A: expected damage is arithmetic the model can compute from a dice string in the prompt. Pass B: it is a field-aware recomputation used only by the fast path, with no registered exception, so it goes with the fast path. → DELETE |
| calculate_hit_chance | Pass A: hit probability from bonus vs AC is prompt arithmetic the model can supply. Pass B: it exists only to feed fast-mode expected casualties, so it shares the fast path's verdict rather than the dice path's protection. → DELETE |
| simulate_battle | Pass A: the model could narrate any battle outcome, so the simulator as outcome author is deletable. Pass B: §6.2 rescues the dice-bearing detailed path on player turns and §6.3 moves background battles async, so the entry point splits rather than disappearing: keep dice on-path, move bulk/background simulation async. → ADAPT |
| _check_morale_rout | Pass A: a rout threshold (remaining ≤ 25%) is a rule the model could apply while narrating. Pass B: it is a campaign-domain outcome decision embedded in simulation, so it survives only inside the async background simulation, never as a turn-path recomputation. → ADAPT |
| _distribute_casualties | Pass A: proportional casualty allocation is arithmetic the model could perform on the unit groups it already holds. Pass B: it mutates simulation state as part of the battle outcome, so like the rout check it survives only within async simulation. → ADAPT |
| _simulate_fast | Pass A: fast mode replaces dice with expected values, which the model can compute itself, so it adds no anti-cheat value. Pass B: because it contains no server dice, no §6 decision rescues it, and it is precisely the recomputation strict ZFC deletes. → DELETE |
| _calculate_round_casualties_fast | Pass A: per-round expected casualties are prompt arithmetic with no player-visible uniqueness. Pass B: a private helper of the fast path, it falls with that path and has no independent justification. → DELETE |
| _simulate_detailed | Pass A: detailed dice-driven simulation cannot be model-supplied without breaking anti-cheat for player battles. Pass B: §6.2 keeps its dice on the turn path, while its use for background battles moves async under §6.3, so the routine itself stays with its placement split by caller. → ADAPT |
| _simulate_round_detailed | Pass A: a single detailed round's dice rolls and log are the anti-cheat record for that round. Pass B: as the dice-bearing core of detailed simulation it inherits the split placement of its parent. → ADAPT |
| expected_damage_per_round | Pass A: expected damage per round is arithmetic the model can derive from unit stats in context. Pass B: it feeds the fast path and display-style estimation, neither of which is a registered exception, so it is deleted rather than kept as a convenience. → DELETE |
| calculate_army_hp | Pass A: summing unit-group HP is trivial aggregation the model can do from the groups it holds. Pass B: aggregation alone is not a registered exception, and it is used to size both paths, so deleting it pushes the sum to the model/schema where the numbers originate. → DELETE |

### faction/combat.py

| Symbol | Justification |
|---|---|
| UnitStats | Pass A: a TypedDict shape for unit statistics is schema the model could conform to without server code. Pass B: as pure transport/schema it makes no decision, so it stays as the shape of inputs to the (deleted) formulas only insofar as other kept code needs it — in practice it goes with the file, but the verdict for the shape itself is retention as documentation. → KEEP |
| POSITION_MULTIPLIERS | Pass A: ranged 1.0 / melee 1.5 / flying 2.25 is a rules table the prompt can state verbatim. Pass B: a static table justifying a field-aware transform would need a registered exception, and none is named, so the table is deleted with its formula. → DELETE |
| SCHOOL_COUNTERS | Pass A: the radiant>shadow>illusion>evocation>conjuration>radiant cycle is prompt-statable rules text. Pass B: it exists only to produce the 1.25 counter bonus, a field-aware recomputation with no registered exception. → DELETE |
| get_position_multiplier | Pass A: looking up a position multiplier is work the model does itself when applying the rules from the prompt. Pass B: determinism of the lookup never justifies a server transform, and defaulting unknown positions to 1.0 silently rewrites model input. → DELETE |
| get_school_counter_bonus | Pass A: deciding whether a school counters another is a rules lookup the model can perform from the prompt cycle. Pass B: it returns a damage multiplier, a field-aware transform of model-authored combat facts, with no registered exception. → DELETE |
| calculate_faction_power | Pass A: FP arithmetic (soldiers×1, spies×0.5, elites×3 with level bonus, territory×5, forts×1000) is exactly the kind of formula a response schema plus prompt can have the model compute. Pass B: it recomputes a model-authored quantity, is called from `faction/tools.py` and tests, and no §6 decision rescues FP arithmetic. → DELETE |
| calculate_damage | Pass A: the damage formula with its random 0.2–0.8 factor is model-computable, and its randomness is not server dice (it uses unseeded `random.uniform` in a formula helper, not the anti-cheat dice path). Pass B: because it is not the §6.2 dice primitive, its randomness does not rescue it, and it remains a field-aware recomputation. → DELETE |
| calculate_damage_deterministic | Pass A: a fixed-factor variant of the damage formula is even more plainly model-computable, since the factor is an argument. Pass B: its test-target status (faction combat tests reference the deterministic family) does not make it production-justified, but deleting a test helper used by tests is a test change, so it is deleted from production and its tests move to model-output assertions. → DELETE |
| calculate_army_stats | Pass A: totals, effective strength, and composition percentages are aggregation the model can emit from counts it already holds. Pass B: display-style aggregation alone never justifies a field-aware transform, and no registered exception covers it. → DELETE |

### faction/dual_mode.py

| Symbol | Justification |
|---|---|
| CampaignMode | Pass A: an adventure/faction mode enum is state the log and schema can carry without server code. Pass B: as a pure value vocabulary for durable state it makes no decision, so it stays as the stored mode's type. → KEEP |
| TriggerUrgency / TriggerType | Pass A: urgency and type vocabularies are prompt-statable labels the model can emit. Pass B: as pure vocabularies for durable trigger records they are transport, not decisions, so they stay with the stored trigger records. → KEEP |
| Trigger | Pass A: a trigger record (type, urgency, message, expiry) is state the model could propose and the server store. Pass B: the dataclass itself is durable-write transport; only its evaluation logic is judged separately. → KEEP |
| Trigger.is_expired | Pass A: comparing a turn number to an expiry is arithmetic the model can do when deciding whether to surface a reminder. Pass B: expiry is a bounded-capacity cleanup rule on stored state, not a campaign decision, so it stays as the store's hygiene. → KEEP |
| Trigger.to_dict / Trigger.from_dict | Pass A: serialization of a trigger record is work any schema layer does, and the model could emit the dict directly. Pass B: serialization is transport with no field-aware judgment, so both directions stay as the persistence codec. → KEEP |
| DualModeState | Pass A: mode, strategic turn, last-order turn, thresholds, and pending triggers are durable state the log alone cannot persist across sessions. Pass B: the container is a durable write, and its thresholds are stored configuration rather than decisions. → KEEP |
| DualModeState.to_dict / DualModeState.from_dict | Pass A: state serialization is mechanical and model-emittable, but something must persist it. Pass B: both directions are transport codecs with no judgment about which triggers deserve to exist. → KEEP |
| DualModeManager.__init__ | Pass A: constructing a manager around state adds no player capability beyond holding the state. Pass B: construction is transport, and it stays only as the holder for the kept state-write methods. → KEEP |
| DualModeManager.from_game_state / DualModeManager.to_game_state | Pass A: reading and writing the manager's state into game state is glue the log cannot do across sessions. Pass B: both are durable reads/writes with no outcome authorship, so they stay as the persistence bridge. → KEEP |
| DualModeManager.switch_to_faction / switch_to_adventure | Pass A: recording a mode switch is a player decision the model reports, but the durable record of which mode is active must live server-side across turns. Pass B: both are durable state writes (plus a message string for the latter family), not decisions about what should happen in either mode. → KEEP |
| DualModeManager.add_personal_time | Pass A: adding personal hours and possibly advancing the strategic turn is a time-accounting rule the model could apply. Pass B: it mutates durable counters and returns whether a turn advanced, which is state bookkeeping rather than a campaign outcome, so it stays as a counter write. → KEEP |
| DualModeManager.advance_strategic_turn | Pass A: incrementing a turn counter is trivially model-statable, yet the authoritative counter must persist server-side. Pass B: a counter increment is a durable write with no domain judgment, so it stays. → KEEP |
| DualModeManager.record_faction_action | Pass A: stamping the last-order turn is bookkeeping the model could report, but the authoritative stamp must persist. Pass B: it is a durable write that later neglect evaluation reads, and the write itself decides nothing. → KEEP |
| DualModeManager.long_rest | Pass A: an 8-hour rest advancing the turn is a rules outcome the model could narrate and apply. Pass B: it is counter bookkeeping (hours plus turn advance) rather than a campaign-domain decision, so it stays as a state transition. → KEEP |
| DualModeManager.add_trigger | Pass A: adding a trigger is the act of creating a campaign-domain reminder, which the model could propose in its output. Pass B: as a store operation it is a durable write, but its current callers are server-side evaluations, so the method stays only as the store endpoint for model-proposed triggers, not as something the server calls on its own judgment. → ADAPT |
| DualModeManager.dismiss_trigger | Pass A: dismissing a trigger is a player action the model reports, and the durable removal must happen server-side. Pass B: removal by ID is a durable write with no judgment about whether the trigger deserved to exist. → KEEP |
| DualModeManager.get_triggers_by_urgency | Pass A: filtering stored triggers by urgency is work the model can do from the stored list in context. Pass B: filtering is a read of durable state, not a transform of model content, so it stays as a query helper. → KEEP |
| DualModeManager.has_critical_triggers | Pass A: checking whether any critical trigger exists is a one-line predicate the model can evaluate from context. Pass B: it is a read predicate over durable state, not an authorship decision, so it stays. → KEEP |
| DualModeManager._evaluate_neglect_triggers | Pass A: deciding that N turns without orders means "morale is dropping" is a narrative judgment the model can make from the turn counters. Pass B: this is server-side authorship of a campaign-domain message, with no registered exception, so the evaluation moves to the model/prompt and the server keeps only storage of whatever the model proposes. → ADAPT |
| DualModeManager._cleanup_expired_triggers | Pass A: dropping expired triggers is hygiene the model could apply by not surfacing them. Pass B: expiry cleanup is bounded capacity on stored state, not a campaign decision, so it stays. → KEEP |
| DualModeManager.build_reminder_block | Pass A: formatting a reminder string for LLM context is exactly what the model does itself when it decides what to say. Pass B: display formatting alone never justifies a field-aware transform, and choosing which trigger surfaces first is a presentation decision, so the block moves to the model/prompt. → DELETE |
| DualModeManager.build_status_display | Pass A: the boxed ASCII realm-status display is presentation the model can render from state in context. Pass B: display formatting alone never justifies server code, and the top-3 truncation is a presentation choice, so it is deleted. → DELETE |
| DualModeManager.evaluate_faction_state | Pass A: deciding that gold below 5000 is a treasury crisis is a judgment the model can make from faction state in context. Pass B: it authors crisis triggers from model-owned state with no registered exception, so evaluation moves to the model and the server keeps only the resulting stored triggers. → ADAPT |

### faction/intel.py

| Symbol | Justification |
|---|---|
| IntelTier | Pass A: failure/partial/success/critical tiers are labels the model can emit from its own judgment. Pass B: as a pure vocabulary for operation outcomes it is transport, so it stays as the outcome's type. → KEEP |
| IntelResult | Pass A: a result shape (tier, detected, intel gathered, message) is schema the model could emit. Pass B: as pure transport/schema it decides nothing, so it stays as the shape of the intel tool result. → KEEP |
| INTEL_BUFFS (table) | Pass A: tier-to-buff mappings are rules text the prompt can state. Pass B: the table exists only to feed the deleted tier/buff computation, so it is deleted with that computation. → DELETE |
| calculate_detection_risk | Pass A: the risk formula (30% base plus wards/networks minus spy/spymaster/intrigue bonuses, clamped 5–90%) is prompt arithmetic the model can compute. Pass B: it is a field-aware recomputation of a model-authored operation's odds, with no registered exception, so it moves to the prompt/schema. → DELETE |
| is_detected | Pass A: a detection roll cannot be model-supplied without letting the model choose whether its spies are caught, which breaks anti-cheat for player operations. Pass B: §6.2 keeps dice resolution on the turn path, and this Bernoulli roll is exactly such a resolution. → KEEP |
| calculate_intel_success | Pass A: mapping spy strength vs defenses to a tier is a judgment the model can make from the operation's inputs in context. Pass B: it authors the operation's outcome tier from model-owned inputs, with no registered exception, so the tier decision moves to the model. → DELETE |
| calculate_intel_success_deterministic | Pass A: a fixed-roll variant of the tier computation is even more plainly model-computable, since the roll is an argument. Pass B: like its combat counterpart it is a test-family helper, so it is deleted from production and its tests become model-output assertions. → DELETE |
| get_intel_buff | Pass A: looking up combat/strategic buffs for a tier is a rules-table lookup the model can do from the prompt. Pass B: it is a field-aware transform feeding the deleted tier computation, with no independent exception. → DELETE |
| execute_intel_operation | Pass A: the full operation (risk, detection roll, tier, downgrade-if-detected, message) mixes model-authorable judgment with one server roll. Pass B: §6.2 rescues only the detection roll, so the operation splits: keep the roll on-path, move tier/buff/message decisions to the model, and move background intel async. → ADAPT |
| get_operation_cooldown | Pass A: cooldown turns by tier (plus 3 if detected) are rules arithmetic the model can apply from the tier it chose. Pass B: it is a field-aware recomputation downstream of the deleted tier decision, with no registered exception. → DELETE |

### faction/rankings.py

| Symbol | Justification |
|---|---|
| FactionStats | Pass A: a stats shape for ranking input is schema the model could conform to without server code. Pass B: as pure transport/schema it decides nothing, but it exists only to feed deleted arithmetic, so it is retained as documentation of the input shape. → KEEP |
| AIFaction | Pass A: an AI faction record shape (name, difficulty, base FP, behavior, aggression) is schema the model could emit. Pass B: as the durable roster record's shape it is transport, and it stays as the shape of the persisted seeded roster. → KEEP |
| calculate_army_fp | Pass A: army FP (soldiers×1, spies×0.5, elites×3 with level bonus) is prompt arithmetic the model can compute from counts. Pass B: it duplicates `combat.py`'s FP logic for the ranking path and recomputes a model-authored quantity with no registered exception. → DELETE |
| calculate_total_fp | Pass A: total FP adds territory, fortification, citizen, gold, arcana, and prestige terms the prompt can state as one formula. Pass B: it is a field-aware recomputation of model-authored state, and the §6.3 promise rescues simulation, not leaderboard arithmetic. → DELETE |
| get_ai_faction_behavior | Pass A: returning a behavior profile for a named faction is a lookup over the seeded roster the model could do from the roster in context. Pass B: as a read over the persisted roster it is transport, but it is only ever a convenience wrapper around the roster read, so it is deleted in favor of the model reading the roster directly. → DELETE |
| get_all_ai_factions | Pass A: regenerating all 200 factions per call is exactly the per-turn recomputation the audit forbids, even though the model could not guarantee cross-session identity alone. Pass B: the roster must come from the persisted one-time seeding (ADAPT in ai_factions), so this function becomes a durable roster read rather than a generator call. → ADAPT |
| calculate_ranking | Pass A: sorting 201 factions by FP and finding the player's position is work the model can do from the roster plus player FP in context. Pass B: it is a recomputation of a model-authored ordering, called from tools and tests, with no registered exception. → DELETE |
| get_nearby_factions | Pass A: slicing the factions above and below the player is presentation logic the model can do from the sorted list. Pass B: it is downstream of the deleted ranking computation and adds only a windowed view, so it falls with it. → DELETE |
| check_ranking_victory | Pass A: checking whether the player is rank 1 is a comparison the model can make from the ranking it computed. Pass B: it is a predicate over the deleted ranking computation, with no independent justification. → DELETE |
| get_fp_to_next_rank | Pass A: the FP gap to the next rank (or to the ranking threshold) is subtraction the model can do from the sorted list. Pass B: it is downstream arithmetic of the deleted ranking, exposed as a tool, so the tool route is deleted with it. → DELETE |

### faction/srd_units.py

| Symbol | Justification |
|---|---|
| SRDStatBlock | Pass A: a stat-block shape (name, AC, HP, attack bonus, damage dice, CR, traits) is schema the model could emit. Pass B: as the shape of published reference data it is transport, so it stays. → KEEP |
| UNIT_TO_SRD_MAP / UNIT_ARCHETYPE_ALIASES / UNIT_KEYWORD_MAP / SRD_STAT_BLOCKS (tables) | Pass A: the model knows the SRD and could map unit labels itself, so the tables are deletable in principle. Pass B: these are published reference data, not campaign-domain facts, so the lookup tables survive as a slim reference, while any scaling built on them does not. → KEEP |
| _normalize_unit_key | Pass A: lowercasing and normalizing a unit label is string handling the model can do when choosing a stat block. Pass B: normalization alone never justifies a field-aware transform, but as the key step of a reference lookup it is retained as part of that lookup. → KEEP |
| resolve_unit_type | Pass A: resolving a genre-agnostic label to an archetype is a mapping judgment the model can make from the alias tables. Pass B: as a reference lookup over published archetypes it is tool execution, not campaign authorship, so it stays. → KEEP |
| get_srd_stats | Pass A: fetching a published SRD stat block is reference retrieval the model could approximate, but the server copy guarantees the exact published numbers. Pass B: published reference data is not a campaign-domain fact, so lookup is legitimate tool execution; its only in-repo caller is the package `__init__`, plus tool/battle paths. → KEEP |
| scale_srd_unit | Pass A: scaling a stat block by character level is a D&D rule the model knows and can apply when it builds a unit group. Pass B: it is a deterministic transform of reference data into campaign state, and determinism alone never justifies it, so scaling moves to the prompt/schema. → DELETE |
| _scale_damage_dice | Pass A: increasing a damage modifier by level is arithmetic the model can do when scaling a unit. Pass B: a private helper of the deleted scaling routine, it falls with that routine. → DELETE |
| create_unit_group | Pass A: assembling a unit group (count, stats, remaining) from a stat block is construction the model can do in its tool arguments. Pass B: it is the bridge between reference lookup and battle simulation, so it survives only as the constructor feeding the kept dice path, slimmed to carry model-scaled stats. → ADAPT |
| map_faction_troops | Pass A: mapping troop counts to SRD unit groups is a composition decision the model can make from the roster and the reference tables. Pass B: it authors the composition of a force from model-owned counts, so the mapping decision moves to the model and the server keeps only the lookup. → ADAPT |
| calculate_total_cr | Pass A: summing challenge ratings over a force is aggregation the model can do from the groups it holds. Pass B: aggregation alone is not a registered exception, so it is deleted with the other arithmetic. → DELETE |

### faction/tools.py

| Symbol | Justification |
|---|---|
| FACTION_TOOL_NAMES | Pass A: the canonical tool-name set is the model's interface vocabulary, which must exist somewhere for routing. Pass B: as a routing vocabulary it is transport, but it must be slimmed to drop the names of deleted formula tools. → ADAPT |
| FACTION_CALCULATION_TOOL_NAMES | Pass A: the single-inference subset (ranking, FP-to-next, power) exists to skip a second LLM pass, which is an optimization the model path does not need. Pass B: every member routes to a DELETE-verdict formula, so the subset is deleted outright rather than slimmed. → DELETE |
| FACTION_TOOLS (schemas) | Pass A: tool schemas are how the model invokes faction capabilities, so some schema set must remain. Pass B: as transport they are allowed, but the schemas for deleted formula tools must be removed, leaving only dice-bearing and roster-lookup tools. → ADAPT |
| should_single_infer_faction_tools | Pass A: deciding whether tool results can be applied without a second inference is an optimization the log-plus-model path does not require. Pass B: it gates on provider/model names and on the deleted calculation-tool subset, so it is deleted with that subset. → DELETE |
| _coerce_str | Pass A: coercing a tool argument to a string is input handling the model could avoid by sending correct types. Pass B: as argument validation for the kept tool router it is transport hygiene, so it stays in slimmed form. → KEEP |
| execute_faction_tool | Pass A: routing model tool calls to faction code is the execution step the bare log cannot perform, and it has 10 external referencing files (dice, game state, provider utils, guards). Pass B: as tool execution it is allowed, but it must be slimmed to route only server-dice calls (battle detailed path, intel detection) and roster lookups, deleting the ranking/power formula routes. → ADAPT |

### faction/__init__.py and faction/README.md

| Symbol | Justification |
|---|---|
| Package re-exports (`__all__` contents) | Pass A: re-exporting names adds no player capability beyond direct module imports. Pass B: the barrel is transport, but it must be slimmed to drop every DELETE-verdict name (FP, damage, ranking, intel-tier, scaling symbols) and keep only dice, lookup, state, and router names. → ADAPT |
| README.md (prose) | Pass A: prose documentation changes no runtime behavior if removed. Pass B: documentation is not a transform at all, and it remains the maintainer map of the minigame, so it stays unchanged. → KEEP |

### living_world.py

| Symbol | Justification |
|---|---|
| evaluate_living_world_trigger | Pass A: deciding whether N turns or N hours have elapsed is arithmetic the model can do from the last-trigger counters in context. Pass B: cadence enforcement is bounded capacity, but the function runs on the turn path (called from `game_state_mixins.py`) and its corrupt/stale realignment logic rewrites tracking state, so the evaluation must move post-commit/background and hand the turn only a precomputed flag. → ADAPT |

### living_world_contract.py

| Symbol | Justification |
|---|---|
| TURN_SCOPED_LIVING_WORLD_FIELDS / AUTHORITATIVE_LIVING_WORLD_FIELDS | Pass A: field registries (scene_event, complications, world_events, faction_updates, time_events, rumors) are vocabularies the prompt could list. Pass B: as registries they prove nothing by themselves, but they are the vocabulary the strip/restore machinery operates on, so they survive only as long as that machinery's ADAPT does, slimmed to the fields the model is actually allowed to author. → ADAPT |
| WORLD_SIM_SETUP_FIELDS | Pass A: the two setup field names (conflict profile, faction roster) are schema the model could know. Pass B: naming the fields the setup worker writes is transport vocabulary for the durable floor, so it stays. → KEEP |
| CONFLICT_PROFILES | Pass A: the three profile names (noncombat, mixed, combat_forward) are prompt-statable labels. Pass B: as the allowed vocabulary for a durable control field it is transport, so it stays. → KEEP |
| ANTAGONIST_COOLDOWN_DAYS (=14) | Pass A: a 14-day pacing constant is a rule the prompt can state as "at most one antagonist event per 14 days". Pass B: a constant alone justifies nothing, and it survives only as the prompt's pacing rule, not as a server enforcement parameter, unless the cooldown exception is registered. → ADAPT |
| DEFAULT_EVENT_TONE (="neutral") | Pass A: defaulting a missing tone to "neutral" is a completion the model can supply itself when emitting events. Pass B: coercing a missing model field is a field-aware transform (normalization alone never justifies it), so the default moves to the response schema and the server stops rewriting the field. → DELETE |
| has_world_sim_setup | Pass A: checking for a valid profile plus a non-empty roster is a predicate the model can evaluate from state in context. Pass B: it is a readiness gate for the background lane (authorization-adjacent), reading durable setup state without judging its content, so it stays. → KEEP |
| preserve_world_sim_setup_fields | Pass A: restoring setup fields a candidate commit omitted is a storage-floor repair the bare log cannot do, since a stale full-document write would otherwise erase the setup worker's output. Pass B: it copies durable fields only when absent (an explicit null/empty is kept as an edit), which is durable-write protection, not authorship, so it stays. → KEEP |
| is_cooldown_turn | Pass A: classifying a turn as a cooldown turn from mode flags is logic the model could apply from the same flags. Pass B: it is a predicate over turn metadata that gates stripping, so it inherits the strip machinery's ADAPT: it stays only as the flag the prompt/schema path consults. → ADAPT |
| is_antagonist_cooldown_active | Pass A: scanning the event log for the last antagonist event and comparing days is work the model can do from the log in context. Pass B: it is a read predicate, not itself a rewrite, but its only use is to drive the strip, so it stays only as the prompt-side predicate's server mirror while the enforcement moves. → ADAPT |
| _is_canonical_projection | Pass A: checking whether an event is an unchanged copy of a committed canonical event is comparison the model could do from the committed list. Pass B: it is a structural identity check protecting canonical events from being double-counted, which is transport integrity, so it stays. → KEEP |
| strip_antagonist_events_during_cooldown | Pass A: removing antagonist events from a candidate is something the model could honor itself if instructed not to emit them during cooldown. Pass B: it is the paradigmatic field-aware transform this spec deletes unless a specific registered exception is named and proven necessary, and no such registration was found in this codebase, so server stripping is removed and enforcement moves to prompt/schema, with this row flagging the unregistered-exception gap. → DELETE |
| _world_time_to_game_day | Pass A: converting a world-time dict to a monotonic day count (year×360 + month×30 + day) is arithmetic the model can do. Pass B: it is a read-side conversion feeding the cooldown predicate, not a rewrite, but it exists only for the deleted strip path, so it is deleted with that path's server enforcement. → DELETE |
| _find_last_antagonist_day_in_state | Pass A: scanning nested state for the last antagonist event is a search the model can do from state in context. Pass B: like its sibling predicate it is a read, but its only consumer is the deleted server enforcement, so it is deleted with it. → DELETE |
| enforce_antagonist_cooldown_on_write | Pass A: server-side enforcement on the write path is precisely what the model could replace by obeying a prompt rule, and its docstring admits it exists because the model misbehaves. Pass B: a verified failure mode is evidence of a problem, not a registered exception, so the enforcement moves to prompt/schema and this write-path hook is deleted pending registration of the exception. → DELETE |
| strip_lw_fields_from_mapping | Pass A: removing all authoritative living-world fields from a dict at all nesting levels is a redaction the model could perform by not emitting those fields. Pass B: it is a field-aware transform over model content, and its cooldown-turn use is the same unregistered enforcement as the antagonist strip, so it is deleted as server enforcement and replaced by schema-level field ownership. → DELETE |
| restore_cooldown_state | Pass A: restoring non-turn-scoped fields to pre-turn values while clearing turn-scoped ones is state repair the model could honor by re-emitting unchanged fields. Pass B: it rewrites model-authored fields from a snapshot, which is a field-aware transform with no registered exception, so it is deleted and replaced by the model carrying those fields forward itself. → DELETE |
| normalize_lw_for_persist | Pass A: stripping and restoring living-world fields before persistence is a pipeline step the model path could avoid by emitting only owned fields. Pass B: it is the composition of two deleted transforms, so it falls with them rather than surviving as a wrapper. → DELETE |
| strip_lw_from_response | Pass A: stripping living-world fields from an API response is presentation filtering the model could do by not including them. Pass B: response filtering is a field-aware transform, and display/visibility control alone never justifies it, so it is deleted. → DELETE |

### faction_state_util.py

| Symbol | Justification |
|---|---|
| get_faction_minigame_dict | Pass A: finding the faction minigame dict across six state shapes is navigation glue the bare log cannot do for providers that need the authoritative dict. Pass B: it is a read over durable state with a documented precedence order and no content judgment, so it stays as transport. → KEEP |
| is_faction_minigame_enabled | Pass A: checking a strict boolean enabled flag is a predicate the model could evaluate from the dict in context. Pass B: strict-boolean validation is an authorization-adjacent gate (a non-boolean truthy value must not enable the minigame), so it stays as a fail-closed check. → KEEP |
| extract_faction_minigame_state_from_game_state | Pass A: extracting the enabled flag plus turn number from game state is a read the model could do from state in context. Pass B: it is a transport read over durable state with no judgment, so it stays. → KEEP |
| extract_faction_minigame_state_from_prompt_contents | Pass A: extracting minigame state from LLM request contents is provider-format navigation the log cannot do. Pass B: it is a transport read over the request format, not a decision about the minigame, so it stays. → KEEP |
| is_faction_enable_action | Pass A: recognizing a user action that enables the minigame is intent classification the model could report. Pass B: as a predicate over the user action it gates a durable enablement write, which is authorization-adjacent, so it stays. → KEEP |
| build_expected_faction_tool_requests | Pass A: mirroring server-executed tool results as expected requests is bookkeeping the model path needs to reconcile what was executed. Pass B: it constructs transport records from executed results without judging their content, so it stays. → KEEP |
| build_native_tools_for_prompt_contents | Pass A: assembling the native tool list for provider flows is prompt construction the provider layer must do. Pass B: tool-list assembly is transport, and it correctly scopes which tools a prompt may invoke, so it stays. → KEEP |

### world_time.py

| Symbol | Justification |
|---|---|
| MONTH_MAP | Pass A: month-name tables for Forgotten Realms, Eberron, Middle-earth, and Gregorian calendars are reference data the model already knows. Pass B: as reference data for parsing it is transport, but it exists to normalize model-supplied month labels into comparable numbers, so it survives only as the parser's table. → KEEP |
| _safe_int | Pass A: coercing an arbitrary value to int with a 0 fallback is input handling the model could avoid by sending numbers. Pass B: as a parser helper it is transport hygiene, but its silent 0 fallback can mask model errors, so it stays only inside parsing, never as a rewrite of stored time. → KEEP |
| _normalize_month | Pass A: mapping a month label to 1–12 is a lookup the model can do from the calendar tables in the prompt. Pass B: normalization alone never justifies a transform, but as part of read-side comparison (not stored rewriting) it stays as the comparator's helper. → KEEP |
| _is_unknown_month_label | Pass A: detecting an unregistered month label is validation the model could do by checking its own label against the tables. Pass B: it is a read-side validation predicate with no rewrite, so it stays. → KEEP |
| world_time_to_comparable | Pass A: converting a world-time dict to a comparable tuple is ordering arithmetic the model can do from the fields. Pass B: comparison support is transport for violation detection, not a rewrite of stored time, so it stays. → KEEP |
| world_time_to_canonical_date | Pass A: formatting a YYYY-MM-DD date from year/month/day is display work the model can do itself. Pass B: it returns None for invalid input rather than rewriting anything, and canonical dates are the scheduling coordinate the timeline needs, so it stays as a read-side formatter. → KEEP |
| parse_world_sim_schedule_date | Pass A: accepting only exact 10-character ISO dates is strict parsing the model could satisfy by emitting exact dates. Pass B: its docstring states it interprets no fiction, and strict validation without rewriting is transport integrity for scheduling, so it stays. → KEEP |
| parse_timestamp_to_world_time | Pass A: parsing an ISO-like timestamp into a world-time dict is conversion the model can do when reporting time. Pass B: it constructs a time dict from a timestamp rather than rewriting model-authored time, so it stays as a parser. → KEEP |
| extract_world_time_from_response | Pass A: pulling world_time out of LLM response state updates is response navigation the server must do to find the model's time claim. Pass B: extraction is a transport read, not a judgment about whether the time is correct, so it stays. → KEEP |
| _has_required_date_fields / has_required_date_fields | Pass A: checking for non-zero year/month/day is validation the model could do by emitting complete dates. Pass B: both are read-side validity predicates with no rewrite, so they stay. → KEEP |
| check_temporal_violation | Pass A: detecting backward time movement is a comparison the model could do from old and new times. Pass B: backward-time detection is an ordering/authorization guard (the timeline epoch machinery depends on it), not a rewrite, so it stays. → KEEP |
| apply_timestamp_to_world_time | Pass A: populating missing world-time fields from timestamp fields is completion the model could do by emitting complete time. Pass B: it fills only missing fields rather than overwriting supplied ones, which is a bounded completion, but it still writes into model-authored time, so it is slimmed to the parser path and removed from the stored-time write path. → ADAPT |
| format_world_time_for_prompt | Pass A: formatting world time for human-readable prompt display is exactly what the model does when it writes narrative time. Pass B: display formatting alone never justifies server code, so the formatter is deleted and the prompt carries time in the model's own words. → DELETE |
| _is_valid_time / _to_total_seconds | Pass A: validating clock fields and converting to total seconds are arithmetic helpers the model can do from the time fields. Pass B: both are read-side helpers for elapsed-time computation with no rewrite, so they stay. → KEEP |
| calculate_hours_elapsed | Pass A: hours between two world times is arithmetic the model can compute from the two dicts. Pass B: it is a read-side computation feeding the living-world cadence (bounded capacity), not a rewrite of either time, so it stays. → KEEP |
| ensure_progressive_world_time | Pass A: normalizing world time "without altering LLM-provided values" is, by its own docstring, a no-op on model values, which the model path does not need. Pass B: a function that promises not to alter values still inspects and re-emits them on the write path, so it is deleted and replaced by the model emitting progressive time itself. → DELETE |
| _coerce_world_time_int / _valid_world_time_partial_component | Pass A: coercing and validating partial time components are input checks the model could satisfy by sending complete valid time. Pass B: both are read-side validation helpers for the partial-merge path, so they fall or stay with that path's ADAPT verdict as validation-only helpers. → ADAPT |
| merge_partial_world_time | Pass A: merging a partial time update into canonical time is a merge the model could do by emitting complete time. Pass B: it rewrites model-authored time fields (with rewind guards), which is a field-aware transform, so partial merging moves to the model/schema and the server keeps only the violation check. → ADAPT |
| handle_world_time_merge_if_needed | Pass A: detecting a partial update and merging it is pipeline logic the model path avoids by requiring complete time. Pass B: it is the entry point of the deleted merge behavior, so it is slimmed to detection plus violation reporting, with the merge itself removed. → ADAPT |

### world_sim/__init__.py, world_sim/rollout.py, world_sim/tools.py

| Symbol | Justification |
|---|---|
| __getattr__ / __dir__ (world_sim) | Pass A: lazy re-export changes no player capability; eager imports would work the same. Pass B: lazy loading is bounded-capacity transport, so both stay as the package's loading mechanism. → KEEP |
| _LAZY_EXPORTS (table) | Pass A: a name-to-module map is routing data the import system could replace with direct imports. Pass B: as routing vocabulary for lazy loading it is transport, so it stays. → KEEP |
| WorldSimDisabledError | Pass A: a typed disabled error is an error vocabulary the model path does not consume directly. Pass B: as an error type for the authorization gate it is transport, so it stays. → KEEP |
| world_sim_enabled | Pass A: reading a config flag is invisible to players when enabled, but its absence would remove the only safe stop for simulation spend. Pass B: it is a fail-closed authorization/bounded-capacity gate (only literal True enables work, read fresh each time), so it stays. → KEEP |
| assert_world_sim_enabled | Pass A: raising when disabled is the enforcement half of the gate, equally invisible when enabled. Pass B: it is the authorization enforcement for the gate above, so it stays. → KEEP |
| WORLD_SIM_TOOL_NAMES | Pass A: the one-tool name set is the model's interface vocabulary for world-sim tools. Pass B: as routing vocabulary it is transport, so it stays. → KEEP |
| get_faction_roster | Pass A: reading the canonical roster from campaign state is a durable read the model cannot do without being handed the state. Pass B: it deep-copies authoritative state and returns {} for missing state rather than inventing factions, which is durable-read transport. → KEEP |
| _load_world_sim_tools | Pass A: loading tool schemas from a JSON asset is file reading the provider layer could do inline. Pass B: loading a schema asset is transport, so it stays. → KEEP |
| WORLD_SIM_TOOLS | Pass A: the loaded schema list is the model's interface to the roster tool. Pass B: as schema transport it stays, and it correctly forbids model-supplied campaign state. → KEEP |
| set_server_campaign_state / reset_server_campaign_state / get_server_campaign_state | Pass A: contextvar storage of authoritative campaign state is invisible to players but is what stops the model from substituting invented state. Pass B: all three are authorization machinery (server state must come from the server, never the model), so they stay. → KEEP |
| execute_world_sim_tool | Pass A: executing the roster-listing tool against authoritative state is the one world-sim capability the bare log cannot supply without inventing factions. Pass B: it is tool execution with a disabled gate, unknown-tool rejection, and strict refusal of model-supplied state, and it has 5 external referencing files; it stays as the roster tool's executor. → KEEP |

### world_sim/dispatcher.py

| Symbol | Justification |
|---|---|
| build_cloud_tasks_request | Pass A: building a Cloud Tasks HTTP request (absolute HTTPS URL, OIDC token, bound UID) is transport the log cannot perform. Pass B: it constructs transport with authentication binding and no domain content, so it stays. → KEEP |
| enqueue_world_sim_tick | Pass A: enqueueing a living-world tick is the actuation of §6.3 async execution; without it background ticks never run. Pass B: enqueueing is transport plus durable task creation, not simulation itself, so it stays. → KEEP |
| dispatch_timeline_outbox | Pass A: draining post-commit continuation records through the task transport is delivery machinery the log cannot do. Pass B: it is transport plus durable state transitions, authoring no outcomes, so it stays. → KEEP |
| LocalValidatedIdentity | Pass A: a validated local identity record is an auth artifact invisible to players. Pass B: as an authorization record it is transport, so it stays. → KEEP |
| _extract_and_validate_local_headers / validate_local_source_headers / _get_header | Pass A: validating local request headers against payload identity is authentication the log cannot perform. Pass B: all three are authorization checks (campaign, user, epoch, outbox identity must match), so they stay. → KEEP |
| _extract_deferred_wake_at | Pass A: reading a deferral timestamp from a payload is transport parsing. Pass B: it reads scheduling metadata without judging domain content, so it stays. → KEEP |
| _is_non_deferred_success_payload / _is_terminal_execution_success | Pass A: classifying payloads as deferred or terminally successful is transport bookkeeping for acknowledgments. Pass B: both are predicates over execution metadata, not campaign facts, so they stay. → KEEP |
| _verify_and_mark_dispatched | Pass A: verifying a persisted outbox record matches its scope before marking it dispatched is exactly-once delivery machinery. Pass B: it is a durable state transition guarded by an identity check, so it stays. → KEEP |
| acknowledge_local_outbox_dispatch | Pass A: acknowledging a local dispatch after validating headers, identity, and terminal success is the local delivery ack. Pass B: it is authorization plus a durable state transition, so it stays. → KEEP |
| prepare_local_worker_request | Pass A: stripping deferral flags and stamping trusted identity from validated headers is request preparation for local execution. Pass B: it uses only validated header identity (never payload-claimed identity), which is authorization-correct transport, so it stays. → KEEP |
| _resolve_timeline_processor / _run_handler / _emit_receipt | Pass A: resolving a processor, running a handler, and emitting a receipt are dispatch internals invisible to players. Pass B: all three are transport, with receipt emission explicitly non-gating so a logging failure cannot block an ack, so they stay. → KEEP |
| execute_world_sim_tick | Pass A: synchronously executing a tick in the local path sounds turn-path, but this executor runs inside the local worker request, not inside a player turn. Pass B: it is local-execution transport that acknowledges the dispatch, and moving it async would only add a queue hop to an already off-turn worker, so it stays as written. → KEEP |
| schedule_deferred_local_outbox_drain | Pass A: scheduling a non-blocking drain at a wake time is the deferral mechanism that keeps workers from blocking. Pass B: it is transport scheduling outside the current request, which is bounded-capacity behavior, so it stays. → KEEP |
| execute_local_timeline_worker | Pass A: executing a deferred local worker request, acking its source, then draining children is the local worker's main loop. Pass B: it is transport plus durable transitions with no outcome authorship, so it stays. → KEEP |
| _run_deferred_drain / _run_local_worker / _send_local_timeline_task | Pass A: the deferred drain, local worker runner, and task sender are the private transport loop behind local execution. Pass B: all three are transport with no domain content, so they stay. → KEEP |

### world_sim/firestore_repository.py

| Symbol | Justification |
|---|---|
| WorldSimFirestoreRepository | Pass A: a repository object for game-state and setup-attempt documents is the durable layer the bare log lacks. Pass B: as a container for durable reads/writes it decides nothing about content, so it stays. → KEEP |
| WorldSimFirestoreRepository.__init__ | Pass A: holding a Firestore client adds no player capability alone. Pass B: construction is transport setup, so it stays. → KEEP |
| get_game_state_ref | Pass A: resolving the user-scoped game-state document reference is addressing the log cannot do. Pass B: user scoping is multi-user separation (authorization), so it stays. → KEEP |
| _run_transaction / _campaign_ref | Pass A: running a callback in a transaction and resolving a campaign reference are durable machinery. Pass B: both are transport, with the transaction providing atomicity for exactly-once claims, so they stay. → KEEP |
| get_setup_attempt_ref | Pass A: a setup-attempt counter beside (not inside) the control record is bookkeeping invisible to players. Pass B: keeping the counter separate from the control record is durable-write hygiene that avoids clobbering control state, so it stays. → KEEP |
| read_setup_attempts / claim_setup_attempt | Pass A: reading and exactly-once claiming a setup attempt number are the idempotency mechanism for one-time setup. Pass B: both are durable reads/writes with exactly-once semantics, so they stay. → KEEP |
| read_setup_inputs | Pass A: returning the campaign document and current game state for the setup call is the input read the setup provider needs. Pass B: it is a durable read with no content judgment, so it stays. → KEEP |
| write_setup_if_absent | Pass A: writing each setup field only if absent (with an invalid profile counting as absent) is what makes setup safe to retry. Pass B: it is a conditional durable write that never overwrites a valid existing value, so it stays. → KEEP |

### world_sim/handler.py

| Symbol | Justification |
|---|---|
| extract_structured_entity_index | Pass A: extracting explicit structured entity IDs and categories from a pre-action snapshot is index construction the model could do from the snapshot. Pass B: it reads IDs the snapshot already contains rather than inventing entities, so it stays as transport indexing. → KEEP |
| initialize_player_gap_background | Pass A: atomically initializing entity controls, wake control, and an initial outbox task is the bootstrap that lets a player's elapsed gap be simulated at all. Pass B: it is durable initialization plus task creation, authoring no outcomes itself, so it stays, with its synchronous call sites already post-commit. → KEEP |
| acquire_or_claim_wake_lease | Pass A: creating or acquiring an execution lease is the exactly-once mechanism for background wakes. Pass B: lease acquisition is bounded capacity plus durable writes, so it stays. → KEEP |
| _parse_timeline_task | Pass A: recognizing a task's owner and route eligibility is dispatch classification invisible to players. Pass B: it applies the route's stricter eligibility as an authorization check, so it stays. → KEEP |
| _dispatch_after_timeline_task | Pass A: draining follow-on work while preserving local ack ordering is delivery machinery. Pass B: it is transport with ordering guarantees, so it stays. → KEEP |
| process_date_timeline_payload / _process_date_timeline_payload | Pass A: creating, advancing, or joining durable date-driven timeline work is the date-lane orchestration the log cannot run. Pass B: these are coordination plus durable writes, but the date payload path still does orchestration work adjacent to request handling, so it must be confirmed fully async with merge-on-next-turn rather than doing coordination inline. → ADAPT |
| _handle_world_sim_setup | Pass A: running one setup attempt (with claimed-failure ack semantics so Cloud Tasks does not retry a claimed attempt) is the setup worker's core. Pass B: it is tool-execution orchestration plus durable transitions, so it stays as the setup entry point. → KEEP |
| handle_run_world_tick / _handle_run_world_tick | Pass A: executing a living-world tick from a validated Cloud Tasks payload is the §6.3 background tick itself. Pass B: the tick runs in a worker, not on the player turn, so it stays, but any caller that invokes it synchronously from a turn must instead enqueue it, which is the ADAPT this row records for the call sites rather than the handler. → ADAPT |
| _lease_tx / _page_tx / _prod_candidate_loader / _load_campaign_state_for_window / _release_retry_lease / _advance_wake_tx | Pass A: lease transactions, page transactions, candidate loading, window state loading, retry-lease release, and wake advancement are the private machinery of the worker loop. Pass B: all six are durable reads/writes and lease bookkeeping with no outcome authorship, so they stay as a group. → KEEP |

### world_sim/trigger.py

| Symbol | Justification |
|---|---|
| compute_foreground_transition_fingerprint | Pass A: a canonical SHA-256 fingerprint of a foreground transition is integrity metadata the log cannot enforce. Pass B: hashing is transport integrity, so it stays. → KEEP |
| _commit_control_and_audit | Pass A: persisting a control record plus its activation audit is the durable record of a transition. Pass B: it is a durable write plus an audit write (with §6.1 logging allowed to go async), so it stays. → KEEP |
| apply_foreground_timeline_control_transition | Pass A: transactionally processing a foreground conflict signal and episode transition is the control update the log cannot apply atomically. Pass B: it persists a transition the player action already resolved, rather than deciding the transition's content, so it stays. → KEEP |
| trigger_durable_timeline_wake | Pass A: durably persisting wake, coordinator, and outbox atomically and draining post-commit is the §6.3 mechanism itself. Pass B: it is durable writes plus post-commit transport, explicitly not blocking the turn, so it stays. → KEEP |
| trigger_world_sim_tick | Pass A: triggering a tick post-commit across streaming and non-streaming turns is the actuation of background simulation. Pass B: it delegates to dispatcher enqueueing (transport) and is called post-commit, so it stays; its 2 external referencing files are tests. → KEEP |
| trigger_world_sim_setup | Pass A: enqueueing the one-time post-commit setup task is the bootstrap actuation for the background lane. Pass B: enqueueing is transport, and one-time semantics come from the repository's exactly-once claims, so it stays. → KEEP |
| enqueue_world_tick (alias) | Pass A: an alias for the tick trigger adds no capability beyond the trigger itself. Pass B: as a pure alias it is transport naming, so it stays. → KEEP |

### world_sim/turn_hooks.py

| Symbol | Justification |
|---|---|
| _timeline_epoch_from_state | Pass A: reading the timeline epoch from state is a lookup the model could do from state in context. Pass B: it is a read of durable ordering state with no judgment, so it stays. → KEEP |
| _has_living_world_conflict_profile | Pass A: checking for a valid profile plus roster is the readiness predicate the model could evaluate from state. Pass B: it is an authorization-adjacent readiness gate for the background lane, so it stays. → KEEP |
| _run_off_turn_path | Pass A: running post-commit work on a daemon thread so the player response never waits is the §6.3 ADAPT already implemented in code. Pass B: it is transport scheduling (bounded by daemon threads), not simulation, so it stays as the mechanism. → KEEP |
| _request_world_sim_setup | Pass A: enqueueing one-time setup post-commit, with failure never rejecting the turn, is bootstrap transport. Pass B: it is enqueueing plus fail-open error handling that protects the turn, so it stays. → KEEP |
| read_world_sim_control_basis | Pass A: reading the authoritative control record as an opaque producer basis is a durable read the model cannot do. Pass B: treating the record as opaque (never interpreting its domain fields on this path) is exactly ZFC-correct transport, so it stays. → KEEP |
| resolve_world_sim_producer_mode | Pass A: resolving the producer mode from the control record is a routing decision the turn path needs to know which lane is active. Pass B: it is a fail-closed routing read (errors fail closed), not an outcome decision, so it stays. → KEEP |
| control_basis_from_pre_action | Pass A: freezing the pre-action control record as an opaque basis is snapshot transport for the post-commit wake. Pass B: snapshotting is durable-read transport with no interpretation, so it stays. → KEEP |
| PreActionSnapshot | Pass A: a frozen pre-action snapshot shape is schema for the post-commit wake. Pass B: as pure transport/schema it decides nothing, so it stays. → KEEP |
| capture_pre_action_snapshot | Pass A: capturing the frozen snapshot before the action runs is the only way the post-commit wake can know what changed. Pass B: it is a durable-read snapshot, not a decision, so it stays. → KEEP |
| PostActionTriggerCall | Pass A: a post-action trigger-call record is the transport shape for the wake request. Pass B: as pure transport/schema it decides nothing, so it stays. → KEEP |
| extract_tools_invoked_this_turn | Pass A: extracting the server-owned (tool_call_id, tool_name) ledger is the evidence base for the lethal-policy citation check. Pass B: it reads the server's own execution ledger (authorization evidence), never model claims, so it stays. → KEEP |
| build_post_action_trigger_call | Pass A: resolving the conflict profile and dispatching the foreground timeline-control transition is the post-action bridge to the background lane. Pass B: it is coordination plus a durable control write, with the caller deciding sync vs thread, so it stays as the bridge. → KEEP |
| dispatch_post_action_timeline_wake | Pass A: running the post-commit timeline transition and wake for the non-streaming path is the §6.3 actuation. Pass B: it runs post-commit (the turn does not wait on simulation), so it stays as the non-streaming wake path. → KEEP |
| StreamingPreActionContext | Pass A: a streaming pre-action context shape is schema for the streaming lane's snapshot. Pass B: as pure transport/schema it decides nothing, so it stays. → KEEP |
| read_streaming_pre_action_context | Pass A: reading committed pre-action streaming state plus the control record is the streaming lane's snapshot read. Pass B: it reads committed durable state (never uncommitted generator state), so it stays. → KEEP |
| activate_streaming_timeline | Pass A: running the post-commit streaming timeline-control transition and world tick is the streaming lane's §6.3 actuation. Pass B: it runs post-commit on the streaming path, so it stays. → KEEP |

### world_sim/worker_auth.py

| Symbol | Justification |
|---|---|
| WorkerAuthError | Pass A: a typed worker-auth error is an error vocabulary invisible to players. Pass B: as an authorization error type it is transport, so it stays. → KEEP |
| _looks_like_jwt | Pass A: checking a token's three-segment shape is a format pre-check the auth layer needs before verification. Pass B: it is an authorization helper with no domain content, so it stays. → KEEP |
| verify_worker_identity | Pass A: validating OIDC claims (issuer, audience, service account) is the authentication that keeps simulation workers trusted. Pass B: it is pure authorization, so it stays. → KEEP |
| authenticate_worker_request | Pass A: authenticating an incoming worker HTTP request is the endpoint gate for all timeline workers. Pass B: it is pure authorization, so it stays. → KEEP |

### world_sim/timeline/antagonistic.py

| Symbol | Justification |
|---|---|
| add_days_to_date | Pass A: adding days to a YYYY-MM-DD string is date arithmetic the model can do. Pass B: it is a read-side date computation for fencing, not a rewrite of an event, so it stays. → KEEP |
| is_date_on_or_after | Pass A: comparing two dates is a predicate the model can evaluate from the dates in context. Pass B: it is a comparison helper with no rewrite, so it stays. → KEEP |
| process_foreground_conflict_signal | Pass A: advancing the generation when the player initiates hostility is ordering bookkeeping the log cannot enforce across in-flight proposals. Pass B: it changes only a generation counter (staling in-flight proposals), never the content of any event, so it stays. → KEEP |
| is_antagonistic_event_eligible | Pass A: checking a proposal's generation against current state is a staleness check the model could do from the generation in context. Pass B: staleness is ordering/authorization, not a semantic veto on the event's content, so it stays. → KEEP |
| commit_antagonistic_event | Pass A: recording an accepted event and advancing the fence is the durable commit of an already-eligible event. Pass B: it is a durable write plus fence advancement, with eligibility decided by the staleness check, so it stays. → KEEP |

### world_sim/timeline/background_contracts.py

| Symbol | Justification |
|---|---|
| RoutinePrivateActionProposal | Pass A: a proposal shape for routine private actions is schema the model conforms to when authoring background actions. Pass B: as pure transport/schema it decides nothing, so it stays. → KEEP |
| BackgroundWindowProviderRequest / BackgroundWindowProviderResponse / CommitResult | Pass A: request, response, and commit-result shapes are the provider contract's schema, which the model path needs to invoke background simulation. Pass B: all three are transport/schema with no judgment, so they stay. → KEEP |
| RoutinePrivateActionProposal.to_dict | Pass A: serializing a proposal is mechanical schema work. Pass B: serialization is transport with no field-aware judgment, so it stays. → KEEP |
| BulkWindowProviderProtocol | Pass A: a protocol for bulk window providers is the interface definition for background simulation providers. Pass B: as an interface it is transport, so it stays. → KEEP |
| BulkWindowProviderProtocol.generate_routine_actions | Pass A: the protocol method signature promises routine-action proposals for a cohort window, which only a model call can fulfill. Pass B: the signature is tool-execution interface, not an implementation decision, so it stays. → KEEP |

### world_sim/timeline/background_entities.py

| Symbol | Justification |
|---|---|
| preempt_entity_foreground | Pass A: preempting an entity for foreground play with a bounded-wait contract is concurrency machinery the log cannot enforce. Pass B: it is bounded capacity plus a durable control update, authoring no new outcomes, so it stays. → KEEP |
| EntityFoldResult | Pass A: a fold-result shape (what was folded, what remains) is schema for bounded background work. Pass B: as pure transport/schema it decides nothing, so it stays. → KEEP |
| fold_entity_due_effects | Pass A: folding at most `max_fold` due scheduled effects for one entity, resuming from a cursor, is bounded background application of already-scheduled effects. Pass B: it applies effects the simulation already decided (bounded capacity), rather than authoring new ones, so it stays. → KEEP |
| requeue_incomplete_entity_candidates | Pass A: moving an incomplete entity to the front of the next page is queue fairness the log cannot enforce. Pass B: it is bounded-capacity queue management, not outcome authorship, so it stays. → KEEP |
| derive_page_idempotency_key | Pass A: a deterministic page/fold continuation key is idempotency metadata invisible to players. Pass B: hashing is transport integrity, so it stays. → KEEP |
| load_persisted_entity_candidates | Pass A: loading entity candidates from persisted control records is the durable read the cohort selector needs. Pass B: it is a durable read with no content judgment, so it stays. → KEEP |
| record_persisted_entity_outcome | Pass A: updating a persisted entity control outcome (success, no_op, system_aborted, maintenance) is the durable record of background work. Pass B: it is a durable write recording an outcome decided elsewhere, so it stays. → KEEP |

### world_sim/timeline/background_provider.py

| Symbol | Justification |
|---|---|
| DeterministicRoutineProposalError | Pass A: a typed error for deterministic proposal failures is an error vocabulary for the provider path. Pass B: as an error type it is transport, so it stays. → KEEP |
| _proposal_error / _provider_provenance | Pass A: constructing proposal errors and provider provenance records are provider-path bookkeeping. Pass B: both are transport metadata (error shaping, provenance tagging) with no domain judgment, so they stay. → KEEP |
| _load_background_routine_prompt / load_background_routine_response_schema | Pass A: loading the routine prompt template and the closed response schema is asset loading the provider call needs. Pass B: both are transport (prompt/schema assets), and the closed schema is what keeps model output valid, so they stay. → KEEP |
| build_background_prompt | Pass A: assembling the background prompt from window inputs is prompt construction only the server can do with authoritative state. Pass B: prompt construction is tool-execution preparation, not a decision about the proposals' content, so it stays. → KEEP |
| _validate_response_envelope | Pass A: validating a provider response envelope is structural checking the model path needs before committing anything. Pass B: envelope validation is schema validity (explicitly not a justification for field-aware transforms, but also not itself a transform), so it stays. → KEEP |
| _merge_structural_map | Pass A: merging nested maps where lists and scalars are model-authored replacements is the merge step that applies provider output. Pass B: it replaces model-authored content with model-authored content under a structural rule, without the server choosing values, so it stays as merge transport. → KEEP |
| _canonical_custom_state | Pass A: canonicalizing custom state for comparison is normalization the provider path needs for idempotency. Pass B: canonicalization for comparison (not for stored rewriting) is transport integrity, so it stays. → KEEP |
| validate_and_parse_background_proposals | Pass A: validating a complete provider response and applying selected-faction patches privately is the commit gate for background simulation. Pass B: it validates structure and bounds and applies the model's own patches, which is tool-execution validation, not server authorship, so it stays. → KEEP |
| call_bulk_background_provider | Pass A: calling Gemini for a whole window and returning a validated transaction-ready outcome is the §6.3 background simulation act itself. Pass B: it is tool execution (a model call) with validation and idempotency, so it stays as the background provider entry point. → KEEP |
| GeminiBulkWindowProvider | Pass A: a provider implementation that calls Gemini for bulk windows is the concrete tool execution behind the protocol. Pass B: as a provider implementation it authors nothing itself; the model does, so it stays. → KEEP |
| GeminiBulkWindowProvider.__init__ / GeminiBulkWindowProvider.generate_routine_actions | Pass A: constructing the provider and generating routine actions through it are the provider's interface fulfillment. Pass B: both are tool-execution plumbing, so they stay. → KEEP |
| _parse_canonical_date / _validate_simulation_inputs | Pass A: parsing exact canonical dates and validating campaign/epoch/window inputs are strict input checks for the provider call. Pass B: both are schema/bounds validation with no rewriting, so they stay. → KEEP |
| derive_window_request_idempotency_key / derive_background_history_id | Pass A: deterministic idempotency keys and history IDs are invisible metadata that make retries safe. Pass B: length-prefixed SHA-256 derivation is transport integrity, so both stay. → KEEP |
| validate_provider_response | Pass A: validating a whole bulk provider response against strict domain invariants is the commit gate before any background outcome persists. Pass B: this is the row that most needs care — domain-invariant validation can shade into semantic veto, but as written it checks invariants (coverage, identity, bounds) rather than choosing values, so it stays, flagged for review if any invariant is found to judge content rather than structure. → KEEP |
| _is_valid_commit_result | Pass A: verifying a commit result covers exactly the submitted history IDs (no missing, extra, or duplicate IDs) is an exactness check the commit path needs. Pass B: it is a structural coverage check, not a content judgment, so it stays. → KEEP |

### world_sim/timeline/cohort.py

| Symbol | Justification |
|---|---|
| EntityCandidate | Pass A: a candidate shape (entity ID, eligibility, age) is schema for cohort selection. Pass B: as pure transport/schema it decides nothing, so it stays. → KEEP |
| EntityCandidate.is_eligible | Pass A: checking a candidate's eligibility is a predicate the model could evaluate from the candidate's fields. Pass B: eligibility here is a capacity/fencing predicate (age, drift), not an outcome judgment, so it stays. → KEEP |
| EntityCandidate._age_key | Pass A: an age sort key is ordering metadata for bounded selection. Pass B: it is a sort helper with no content judgment, so it stays. → KEEP |
| select_simulation_cohort | Pass A: selecting the bounded cohort for a window is capacity management the log cannot enforce across entities. Pass B: selection by bounded size and drift fences is bounded capacity, not authorship of what selected entities do, so it stays. → KEEP |
| record_entity_outcome | Pass A: updating candidate state after a simulation attempt is the durable record of that attempt. Pass B: it is a durable write recording an outcome decided elsewhere, so it stays. → KEEP |
| is_entity_drift_fenced | Pass A: fencing entities more than 7 days behind against semantic commits is a safety rule the log cannot enforce. Pass B: drift fencing is bounded capacity plus authorization-style protection against stale commits, so it stays. → KEEP |

### world_sim/timeline/cutover.py

| Symbol | Justification |
|---|---|
| activate_producer_after_setup | Pass A: auto-enabling world-sim on a control still on the legacy producer is the activation step after setup completes. Pass B: it is a durable control write gated on setup completion, not an outcome decision, so it stays. → KEEP |
| cutover_to_timeline_world_sim | Pass A: executing cutover from foreground_legacy to timeline_world_sim is the admin migration the log cannot perform. Pass B: it is authorization (admin) plus durable control writes, so it stays. → KEEP |
| pause_timeline / resume_timeline | Pass A: pausing and resuming timeline simulation are admin lifecycle operations invisible to players except in effect. Pass B: both are durable control writes (pause cannot revert to legacy, which is a one-way guard), so they stay. → KEEP |
| AdminCutoverAuditRecord | Pass A: an audit record shape for admin cutovers is schema for the audit trail. Pass B: as pure transport/schema plus §6.1 logging support it decides nothing, so it stays. → KEEP |
| AdminCutoverAuditRecord.to_dict / AdminCutoverAuditRecord.from_dict | Pass A: serializing and restoring an audit record are mechanical codec operations. Pass B: both are transport codecs with no judgment, so they stay. → KEEP |
| execute_admin_cutover | Pass A: executing an admin cutover is the endpoint that performs the migration with audit. Pass B: it is authorization plus durable writes with audit, so it stays. → KEEP |
| _resume_pending_work | Pass A: recreating fenced deliveries from durable progress inside the cutover transaction is recovery of already-decided work. Pass B: it re-drives durable progress rather than authoring new outcomes, so it stays. → KEEP |
| _tx_cutover / enqueue (cutover) | Pass A: the cutover transaction wrapper and its enqueue helper are the private machinery of cutover execution. Pass B: both are transport (transaction plus task creation), so they stay. → KEEP |

### world_sim/timeline/epoch.py

| Symbol | Justification |
|---|---|
| create_backward_time_epoch | Pass A: creating a new authorized epoch after backward time travel is ordering state the log cannot enforce. Pass B: epoch creation is authorization (only authorized backward travel gets a new epoch) plus a durable write, so it stays. → KEEP |
| quarantine_suspect_timestamp | Pass A: quarantining an unauthorized or malformed timestamp change without pausing canonical time is a protective action the log cannot take. Pass B: it is authorization plus a durable quarantine write that preserves canonical time, so it stays. → KEEP |

### world_sim/timeline/event_codec.py

| Symbol | Justification |
|---|---|
| get_event_partition_key | Pass A: deriving a partition doc ID (idx_00–idx_3f) from an event ID is sharding metadata invisible to players. Pass B: it is transport addressing, so it stays. → KEEP |
| _canonical_json_default / canonical_json_bytes / canonical_json_size / compute_canonical_event_size | Pass A: canonical JSON serialization and size computation are integrity machinery the log cannot supply. Pass B: all four are transport integrity plus bounded capacity (size bounds), with no field-aware judgment, so they stay. → KEEP |
| canonical_event_hash | Pass A: a SHA-256 digest of canonical event JSON is tamper evidence for stored events. Pass B: hashing is transport integrity, so it stays. → KEEP |
| validate_canonical_event / validate_canonical_events_batch | Pass A: validating single events and batches against structural and byte bounds is the commit gate for stored events. Pass B: both are schema/bounds validation with no content judgment, so they stay. → KEEP |
| compute_archive_chunk_digest | Pass A: a chained SHA-256 digest for archive chunks is tamper evidence for archived events. Pass B: hashing is transport integrity, so it stays. → KEEP |
| validate_archive_chunk_data / validate_archive_manifest_data / validate_archive_partition_data | Pass A: validating archive chunks, manifests, and partitions (structure, events, bounds, chain digests, counters, entry hashes) is the read gate for archived history. Pass B: all three are structural/bounds validation with no outcome authorship, so they stay. → KEEP |

### world_sim/timeline/execution_constraints.py

| Symbol | Justification |
|---|---|
| ExecutionFencedError | Pass A: a typed error for fenced execution is an error vocabulary for the constraint path. Pass B: as an error type it is transport, so it stays. → KEEP |
| check_active (constraint) | Pass A: checking whether a constraint is active is a predicate the worker needs before executing. Pass B: it is an authorization/bounds predicate with no domain content, so it stays. → KEEP |
| leaf_fields | Pass A: listing the leaf fields a constraint covers is constraint introspection the validation path needs. Pass B: it is structural metadata, not a content judgment, so it stays. → KEEP |
| validate_writes | Pass A: validating writes against installed constraints is the enforcement that keeps background work within bounds. Pass B: it is bounded-capacity enforcement applied to leaf fields without judging domain content, so it stays. → KEEP |
| validate_constraint | Pass A: validating a server-issued constraint before its one-time installation is the guard against malformed bounds. Pass B: it is authorization-adjacent validation of server-issued (never model-issued) constraints, so it stays. → KEEP |

### world_sim/timeline/identity.py

| Symbol | Justification |
|---|---|
| _canonical_length_prefixed | Pass A: length-prefixed encoding of ID components prevents delimiter injection and collisions in derived IDs. Pass B: it is transport integrity for identifier derivation, so it stays. → KEEP |
| derive_coordinator_outbox_id / derive_job_outbox_id / derive_event_id / derive_bisection_chunk_ids | Pass A: deterministic outbox, event, and chunk IDs are idempotency metadata invisible to players. Pass B: all four are transport integrity (deterministic derivation, including bisection splitting for bounded chunks), so they stay. → KEEP |
| derive_date_lease_token / derive_job_lease_token | Pass A: deterministic lease tokens are the exactly-once mechanism for date and job wakes. Pass B: both are transport integrity for lease acquisition, so they stay. → KEEP |
| derive_retry_jitter | Pass A: deterministic retry jitter in milliseconds spreads retries without randomness the model could game. Pass B: it is bounded-capacity scheduling metadata, so it stays. → KEEP |
| compute_response_hash | Pass A: a SHA-256 hash of a provider response payload is the stored-response integrity check. Pass B: hashing is transport integrity, so it stays. → KEEP |
| derive_background_outbox_id / derive_dead_letter_id / derive_background_claim_id | Pass A: deterministic IDs for background outbox tasks, dead letters, and execution claims are idempotency metadata. Pass B: all three are transport integrity, so they stay. → KEEP |
| encode_outbox_cursor / decode_outbox_cursor | Pass A: encoding and decoding an opaque base64 continuation cursor are pagination transport for outbox draining. Pass B: both are transport codecs with validation on decode, so they stay. → KEEP |
| validate_user_uid / validate_campaign_id / validate_epoch | Pass A: validating UID non-emptiness, exact campaign ID bytes, and unsigned 64-bit epoch are input gates for every timeline operation. Pass B: all three are authorization/bounds validation with no normalization of model content (campaign IDs are explicitly not stripped), so they stay. → KEEP |

### world_sim/timeline/background_worker.py

| Symbol | Justification |
|---|---|
| TimelineBackgroundWorkerError / TimelineCommitError | Pass A: typed errors for worker and commit failures are error vocabularies for the background path. Pass B: as error types they are transport, so they stay. → KEEP |
| WindowSimulationResult / BackgroundWakeResult (+ their to_dict) | Pass A: result shapes for a window simulation and a background wake are schema for worker outputs. Pass B: as pure transport/schema plus serialization they decide nothing, so they stay. → KEEP |
| PrivateHistoryCommitterProtocol.commit_private_history / commit_explicit_no_op | Pass A: the committer protocol's two methods are the interface for persisting private history and no-op fairness updates. Pass B: as an interface they are transport, so they stay. → KEEP |
| FirestorePrivateHistoryCommitter.__init__ / _now / assert_provider_allowed | Pass A: constructing the committer, reading the clock, and asserting the provider is allowed are worker setup and gating. Pass B: construction and clock reads are transport, and provider gating is authorization, so they stay. → KEEP |
| FirestorePrivateHistoryCommitter.advance_window_cooldowns | Pass A: decrementing receipt cooldowns once per chronological window, with replayed/older skips excluded, is cadence bookkeeping for background fairness. Pass B: it is a durable write applying a bounded rule (once per window), not an outcome decision, so it stays. → KEEP |
| FirestorePrivateHistoryCommitter.acquire_cohort_leases / acquire_cohort_leases_and_claim_window / release_cohort_leases / renew_wake_execution_lease | Pass A: acquiring, claiming, releasing, and renewing leases are the exactly-once machinery that keeps background windows from double-executing. Pass B: all four are bounded capacity plus durable writes with exact CAS fence checks, so they stay. → KEEP |
| FirestorePrivateHistoryCommitter.commit_private_history | Pass A: committing validated private-history entries inside an atomic transaction is the durable write of background outcomes. Pass B: it persists provider-authored history with a server-owned infrastructure outcome, authoring no new facts itself, so it stays. → KEEP |
| FirestorePrivateHistoryCommitter.commit_explicit_no_op | Pass A: committing explicit no-op fairness updates plus lease release atomically is how entities that did nothing still advance fairly. Pass B: it is a durable write of a server-owned no-op outcome, not a campaign decision, so it stays. → KEEP |
| advance_window_cooldowns (module function) | Pass A: the module-level cooldown advance is the same once-per-window bookkeeping exposed for the worker loop. Pass B: as a durable cadence write it stays, identical in justification to the committer method. → KEEP |
| _prepare_entity_background_lease / acquire_entity_background_lease | Pass A: preparing and acquiring a background lease for one entity are the per-entity exactly-once guards. Pass B: both are bounded capacity plus durable writes, so they stay. → KEEP |
| run_window_simulation | Pass A: orchestrating background semantic simulation for a single chronological 30-day window is the §6.3 promise at window granularity. Pass B: it is already background execution, but it must be slimmed to strict background-only orchestration with no turn-path entry point and with merge-on-next-turn for its results. → ADAPT |
| run_background_simulation_wake | Pass A: running a bounded series of background windows in date order is the §6.3 promise at wake granularity, called from `handler.py`'s worker path and tests. Pass B: it is already background execution, but like its window sibling it must be confirmed worker-only and slimmed to strict background execution with merge-on-next-turn. → ADAPT |
| _apply_abort_receipt | Pass A: settling a provider-failure receipt without authoring model-domain history is failure bookkeeping for a failed window. Pass B: it explicitly authors no history, recording only the abort, so it stays as failure transport. → KEEP |
| _validate_noop_fences / _apply_noop | Pass A: fence-checking entities settled by a server-owned outcome and applying the no-op fairness reset are the no-op path's guard and effect. Pass B: both are durable writes of server-owned outcomes with fence checks, not campaign decisions, so they stay. → KEEP |

### world_sim/timeline/coordinator.py

| Symbol | Justification |
|---|---|
| ValidationRejectionError | Pass A: a typed error for coordinator validation rejections is an error vocabulary. Pass B: as an error type it is transport, so it stays. → KEEP |
| compute_canonical_coordinator_size | Pass A: computing the deterministic JSON byte size of a coordinator record is a bounds check the coordinator needs before persisting. Pass B: size computation is bounded capacity with no content judgment, so it stays. → KEEP |
| compact_coordinator_record | Pass A: deterministically compacting terminal COMPLETE segments when bounds are exceeded is storage hygiene for long coordinators. Pass B: compaction is bounded capacity, but only terminal segments may be compacted without losing live decisions, so it is slimmed to terminal-only compaction with any non-terminal compaction deleted. → ADAPT |
| generate_date_range | Pass A: generating all dates in an inclusive range is date arithmetic the model could do, but the coordinator needs the authoritative list to drive windows. Pass B: it is a deterministic list construction for coordination, not an outcome decision, so it stays. → KEEP |
| DurableTimelineCoordinator.__init__ | Pass A: constructing the coordinator around its store is setup for durable coordination. Pass B: construction is transport, so it stays. → KEEP |
| DurableTimelineCoordinator._resolve_legacy_stored_chunk_attempt | Pass A: resolving legacy stored chunk attempts is migration handling for coordinators created before the current chunk format. Pass B: migration reads are transport that preserve durable progress rather than authoring outcomes, so it stays. → KEEP |
| DurableTimelineCoordinator._terminalize_job_chunks | Pass A: terminalizing job chunks is the state transition that closes finished chunks. Pass B: it is a durable write recording completion decided elsewhere, so it stays. → KEEP |
| DurableTimelineCoordinator.persist_response_and_decisions | Pass A: atomically validating a whole chunk input, storing a response hash, and storing per-date immutable decisions is the coordinator's commit gate. Pass B: it is durable writes plus structural validation with immutable decisions, so it stays. → KEEP |
| DurableTimelineCoordinator.replay_stored_decisions | Pass A: applying stored decisions and canonical events in one transaction is replay of already-decided work after a crash or retry. Pass B: replay is durable-write recovery, not new authorship, so it stays. → KEEP |
| DurableTimelineCoordinator._complete_owning_segment | Pass A: marking a job's owning segment COMPLETE and dispatching the next segment is segment lifecycle transport. Pass B: it is a durable transition plus task dispatch, so it stays. → KEEP |
| DurableTimelineCoordinator.record_job_provider_failure | Pass A: terminalizing a relevance job whose single provider call failed is failure bookkeeping that stops unbounded retries. Pass B: it is a durable failure write plus bounded capacity (single-call jobs do not retry forever), so it stays. → KEEP |
| DurableTimelineCoordinator.acquire_due_job_wake | Pass A: transactionally acquiring an on-time job wake, enforcing deadline exhaustion, early-wake rejection, and duplicate CAS, is the exactly-once wake mechanism. Pass B: it is bounded capacity plus durable writes with CAS, so it stays. → KEEP |
| wake_timeline_for_elapsed_gap | Pass A: awakening or joining a campaign's durable timeline coordinator for an elapsed gap is the §6.3 entry point for catch-up simulation. Pass B: it is coordination plus durable writes, but as the production entrypoint it must be confirmed background-only (its 9 external referencing files are tests and setup paths) with merge-on-next-turn, never invoked synchronously from a turn. → ADAPT |

### world_sim/timeline/lethal_policy.py

| Symbol | Justification |
|---|---|
| _normalize_conflict_collection | Pass A: reading identity-bearing conflict records without interpreting model-owned fields is the safe read the policy needs. Pass B: it explicitly avoids interpreting model fields, reading only identities, so it stays as authorization-safe transport. → KEEP |
| _extract_state_conflicts | Pass A: extracting conflict records from state is the read the canonical-conflict resolution needs. Pass B: it is a transport read of identity-bearing records, so it stays. → KEEP |
| resolve_canonical_conflicts | Pass A: intersecting selected conflict records by exact source identity across state sources is the canonicalization the policy needs to know which conflicts are agreed. Pass B: it preserves selected records and intersects only exact identities, adding no semantic judgment, so it stays. → KEEP |
| process_foreground_episode_transition | Pass A: processing a lethal episode transition (open/close) from a player action is the agency gate that stops the model from killing characters without a real player action. Pass B: this is the named authorization exception for this group — an OPEN transition must cite a real executed tool invocation from the server ledger — and the code states conflict signals and protection context add no further semantic veto, so it stays. → KEEP |
| _validate_episode_generation | Pass A: validating an episode's generation is a staleness check for episode transitions. Pass B: generation checks are ordering/authorization, not content judgment, so they stay. → KEEP |
| validate_lethal_event_proposal | Pass A: validating a lethal proposal against explicitly cited lethal-basis identities in current state is the proposal gate for background lethal events. Pass B: it checks citations against state (authorization evidence) rather than judging whether the death is good story, so it stays. → KEEP |

### world_sim/timeline/outbox.py

| Symbol | Justification |
|---|---|
| OutboxDrainResult / OutboxDrainResult.to_dict | Pass A: a drain-result shape plus serialization is schema for outbox delivery outcomes. Pass B: as pure transport/schema they decide nothing, so they stay. → KEEP |
| is_already_exists_error | Pass A: recognizing a structured AlreadyExists dispatch exception is error classification the drain loop needs for idempotency. Pass B: it is transport error handling, so it stays. → KEEP |
| build_cloud_task_from_outbox | Pass A: building a canonical queue path and Cloud Tasks request with a deterministic task ID is delivery transport. Pass B: it is transport with deterministic identity, so it stays. → KEEP |
| drain_dispatch_outbox | Pass A: draining undispatched outbox rows for a user/campaign/epoch scope is the delivery loop for background continuations. Pass B: it is transport plus durable state transitions, so it stays. → KEEP |

### world_sim/timeline/reconciler.py

| Symbol | Justification |
|---|---|
| reconciler_control_doc_id | Pass A: keeping each trusted origin's scan progress independent in the shared store is addressing for reconciliation. Pass B: it is transport addressing, so it stays. → KEEP |
| _timestamp_to_micros / _timestamp_from_micros | Pass A: converting timestamps to and from microseconds is precision handling the reconciler needs for expiry comparison. Pass B: both are transport conversions with no content judgment, so they stay. → KEEP |
| _query_at_read_time | Pass A: running a query at one Firestore snapshot read time is the consistent-read mechanism for reconciliation scans. Pass B: it is durable-read transport, so it stays. → KEEP |
| parse_outbox_scope_from_path | Pass A: extracting and validating (user, campaign, epoch) strictly from a document path is scope recovery the reconciler needs. Pass B: it derives scope from trusted path structure (never payload claims), which is authorization-correct transport, so it stays. → KEEP |
| _run_reconciler_transaction / _snapshot_data / _query_expired_outbox | Pass A: running a fail-closed transaction, normalizing snapshot data, and querying expired outbox rows are the reconciler's private machinery. Pass B: all three are durable-read/write transport, so they stay. → KEEP |
| _advance_expired_control / _recover_expired_outbox | Pass A: advancing expired control records and recovering expired outbox rows are the repair steps for stuck deliveries. Pass B: both re-drive already-decided work from durable state rather than authoring new outcomes, so they stay. → KEEP |
| _undispatched_high_water_path / _reconcile_undispatched_outbox_ordinary | Pass A: computing a high-water path and reconciling ordinary undispatched scopes are the scan steps that find stuck rows across campaigns. Pass B: both are durable-read transport plus bounded discovery, so they stay. → KEEP |
| reconcile_undispatched_outbox | Pass A: reconciling undispatched outbox rows is the recovery entry point that prevents background work from being lost silently. Pass B: it is durable-write recovery with bounded scope, so it stays. → KEEP |
| run_startup_outbox_reconciliation | Pass A: an opportunistic single synchronous sweep on process startup recovers work lost to a crash. Pass B: it runs at startup (not on a player turn) and is explicitly a single bounded sweep, so it stays. → KEEP |
| run_bounded_outbox_reconciliation | Pass A: running a bounded reconciliation and projecting an HTTP summary is the operator-facing recovery endpoint. Pass B: it is bounded recovery plus transport (the summary), so it stays. → KEEP |

### world_sim/timeline/relevance_provider.py

| Symbol | Justification |
|---|---|
| _load_relevance_highlights_prompt / load_relevance_highlights_response_schema | Pass A: loading the highlights prompt template and structured-output schema is asset loading for the relevance provider call. Pass B: both are transport (prompt/schema assets), so they stay. → KEEP |
| build_relevance_prompt | Pass A: serializing raw snapshots for one bulk relevance request is prompt construction from authoritative snapshots. Pass B: serialization of snapshots is tool-execution preparation, not a decision about the highlights, so it stays. → KEEP |
| call_bulk_relevance_provider | Pass A: calling the canonical provider in JSON mode and returning a typed envelope is how relevance highlights are authored off-turn. Pass B: it is tool execution (a model call) with a typed envelope, so it stays. → KEEP |

### world_sim/timeline/relevance_worker.py

| Symbol | Justification |
|---|---|
| RelevanceWorkerResult / RelevanceWorkerResult.to_dict | Pass A: a worker-result shape plus serialization is schema for relevance job outcomes. Pass B: as pure transport/schema they decide nothing, so they stay. → KEEP |
| _settle_failed_delivery | Pass A: recording a failed or invalid model response and terminalizing the job is failure bookkeeping that stops unbounded retries. Pass B: it is a durable failure write plus bounded capacity, so it stays. → KEEP |
| _replay_stored_chunk_response | Pass A: replaying a stored chunk response applies an already-received model response to its date records. Pass B: replay is durable-write recovery of model-authored content, not new authorship, so it stays. → KEEP |
| run_relevance_job_worker | Pass A: executing a durable relevance-job worker task against a persisted job record is the off-turn application of highlights. Pass B: it replays stored decisions and settles deliveries as durable writes, authoring no new campaign facts, so it stays. → KEEP |

### world_sim/timeline/setup_provider.py

| Symbol | Justification |
|---|---|
| load_setup_schema | Pass A: loading the setup response schema is asset loading for the one-time setup call. Pass B: schema loading is transport, so it stays. → KEEP |
| _scalars | Pass A: taking only top-level scalar entries keeps the setup request small without judging content. Pass B: it is a size-bounding projection (bounded capacity) that explicitly does not judge content, so it stays. → KEEP |
| _valid_existing | Pass A: treating stored values the writer would keep as valid (and invalid ones as absent) is the setup idempotency rule. Pass B: it is a durable-read predicate for conditional writes, so it stays. → KEEP |
| build_setup_request / build_setup_prompt | Pass A: building the setup request and prompt from stored state is the preparation for the one-time setup model call. Pass B: both are tool-execution preparation with no outcome judgment, so they stay. → KEEP |
| validate_setup_output | Pass A: returning setup output only when both profile and roster fields are valid (else logging why and returning None) is the strict gate that keeps a half-setup from activating the background lane. Pass B: it is schema validation with fail-closed behavior, so it stays. → KEEP |
| call_setup_provider | Pass A: making the single setup call and returning validated output or None is the one-time setup execution. Pass B: it is tool execution with strict validation, so it stays. → KEEP |
| log_setup_exhausted | Pass A: a structured BigQuery-visible record of a campaign stuck without a profile is the observability record for setup failure. Pass B: it is §6.1 logging (async/batched delivery applies), not a domain decision, so it stays. → KEEP |
| WorldSimSetupRetryableError | Pass A: a typed retryable setup error is an error vocabulary for the setup path. Pass B: as an error type it is transport, so it stays. → KEEP |
| _setup_completion_snapshot / _setup_completion_wake_dates | Pass A: a persisted pre-action snapshot and the catch-up date range derived from persisted world time are the setup-completion inputs for the wake. Pass B: both derive from persisted (never model-owned) state, which is durable-read transport, so they stay. → KEEP |
| _ensure_setup_completion | Pass A: activating an eligible producer control and ensuring the durable wake is queued is the setup-completion actuation. Pass B: it is a durable control write plus enqueueing, gated on eligibility, so it stays. → KEEP |
| run_world_sim_setup | Pass A: running one claimed setup attempt without ever raising a provider failure is the setup worker's contract (failures become acks, not crashes). Pass B: it is tool-execution orchestration plus durable transitions, so it stays. → KEEP |
| _activate (setup) | Pass A: the private activation step inside setup completion is the control write that enables the background lane. Pass B: it is a durable control write gated on validated setup output, so it stays. → KEEP |

### world_sim/timeline/stage_worker.py

| Symbol | Justification |
|---|---|
| StageWorkerResult / StageWorkerResult.to_dict | Pass A: a stage-result shape plus serialization is schema for stage worker outcomes. Pass B: as pure transport/schema they decide nothing, so they stay. → KEEP |
| run_timeline_stage_worker | Pass A: executing a bounded timeline stage task with strict transactional CAS validation is the stage-advance worker. Pass B: it is transport plus durable writes with CAS, authoring no outcomes itself, so it stays. → KEEP |

### world_sim/timeline/validation.py

| Symbol | Justification |
|---|---|
| _highlight_item_validator | Pass A: a cached validator for one highlight item from the canonical response schema is schema validation machinery. Pass B: as a schema validator it checks structure, so it stays as the structural half of highlight validation. → KEEP |
| validate_highlight_semantics | Pass A: returning an error string when a highlight omits or malforms model-owned semantics is a semantic judgment about model content. Pass B: this is the file's flagged field-aware check — semantics are model-owned, so the check must be slimmed to structural validation only, with semantic judgment returned to the model and this function deleted in its semantic form. → DELETE |
| generate_background_windows | Pass A: generating at most 12 chronological 30-day windows per wake with a continuation cursor is the bounding rule for background work. Pass B: window generation is bounded capacity with chronological ordering, not outcome authorship, so it stays. → KEEP |
| select_bounded_window | Pass A: returning the next ordered window of at most `max_dates` reserved dates is the per-step bound for window processing. Pass B: it is bounded capacity over reserved dates, so it stays. → KEEP |
| validate_bulk_highlight_response | Pass A: validating a whole bulk highlight response before any date-row mutation or tool execution is the commit gate for highlights. Pass B: as a gate it stays only in its structural/schema form; any semantic judgment it delegates to the deleted semantics check is deleted with that check. → ADAPT |

### world_sim/timeline/store.py, firestore_store.py, firestore_transaction.py — coverage note

The three store files implement the same `TimelineStoreProtocol` surface three times
(protocol definition, Firestore implementation, transactional adapter). Their methods
differ only by record type, not by kind of work: every `get_*` is a durable read, every
`put_*` a durable write, every `list_*` a bounded durable read, and every
`mark_*/rearm_*/preserve_*` a durable state transition. Each row below therefore names
every method it covers (grouped by family across the three files where the work is
identical) and gives the shared 2–4 sentence justification; the verdict applies to each
named method individually. Transaction-callback closures (`_tx`, `_tx_op`, `_tx_callback`,
`_body`, `guarded_body`, `_run_with_adapter`, `_load_partition`, `_proj_bytes`,
`_load_and_validate_chunk`, `_build_chunk_doc`) are not standalone symbols: each is a
closure forwarding to its enclosing method's transaction and inherits that enclosing
method's verdict (KEEP in every case here, as durable-write machinery).

| Symbols | Justification |
|---|---|
| store.py: TimelineStoreError, FencedCommitError, TransactionUnavailableError, TerminalRowWriteError, LeaseExpiredError, RecordNotFoundError, CoordinatorBoundsExceededError | Pass A: typed errors for store failures are error vocabularies the timeline path needs to fail closed. Pass B: as error types they are transport, so each stays. → KEEP |
| store.py: TimelineStoreProtocol (+ all its method signatures: assert_delivery_allowed, assert_provider_allowed, admit_dispatch, finish_dispatch, run_transaction, get/put_date_record, get_date_records_range, get/put_control_record, get/put_admin_audit_record, get/put_coordinator_record, get/put_job_record, get_outbox_record, put_outbox_if_absent, list_undispatched_outbox, list_undispatched_outbox_paged, rearm_outbox_if_expired, preserve_outbox_wake_at, mark_outbox_enqueued, mark_outbox_dispatched, append_canonical_world_events, get_game_state_snapshot, authoritative_epoch_matches, get/put_private_history, get/put_entity_control, list_entity_controls, get/put_dead_letter, list_unfinished_background_wakes, get/put_background_wake_record, get/put_execution_claim) | Pass A: the store protocol is the persistence interface every timeline component depends on; deleting it deletes persistence itself. Pass B: a protocol definition performs no transform at all, and its dispatch-admission methods are authorization/bounds gates, so every signature stays. → KEEP |
| store.py: authoritative_state_epoch | Pass A: reading the authoritative timeline epoch for a game state is the ordering lookup every write authorization needs. Pass B: it is a durable-read lookup with no content judgment, so it stays. → KEEP |
| firestore_store.py: FirestoreTimelineStore, __init__, _write_document, _execution_constraint_ref, _read_execution_constraint, _epoch_ref, _admin_audit_ref, _game_state_ref, _date_ref, _coordinator_ref, _job_ref, _outbox_ref, _private_history_ref, _entity_control_ref, _dead_letter_ref, _background_wake_ref, _execution_claim_ref, _event_archive_ref, _event_archive_manifest_ref | Pass A: the Firestore store class, its constructor, its document writer, and its per-collection reference resolvers are the addressing and write machinery for timeline persistence. Pass B: all are transport (addressing plus writes) with no domain judgment, so each stays. → KEEP |
| firestore_store.py: install_execution_constraint, install (constraint), assert_provider_allowed, assert_delivery_allowed, admit_dispatch, finish_dispatch, claim (dispatch), abort_execution, abort (execution), _cancel_exact_task, run_transaction | Pass A: installing immutable bounds, gating provider/delivery access, admitting and finishing dispatches, aborting executions, cancelling exact tasks, and running transactions are the guardrails and atomicity of the store. Pass B: every one is authorization, bounded capacity, or durable-write machinery (installed constraints cannot be replaced, which is fail-closed), so each stays. → KEEP |
| firestore_store.py: all get/put pairs (get/put_date_record, get_date_records_range, get/put_control_record, get/put_admin_audit_record, get/put_coordinator_record, get/put_job_record, get_outbox_record, put_outbox_if_absent, get/put_private_history, get/put_entity_control, list_entity_controls, get/put_dead_letter, get/put_background_wake_record, get/put_execution_claim) + get_game_state_snapshot | Pass A: these are the durable reads and writes for every timeline record type; the bare log has no equivalent for any of them. Pass B: each is a pure durable operation with no content judgment (put_outbox_if_absent is conditional on absence, which is idempotency, not authorship), so each stays. → KEEP |
| firestore_store.py: list_undispatched_outbox, list_undispatched_outbox_paged, rearm_outbox_if_expired, preserve_outbox_wake_at, mark_outbox_enqueued, mark_outbox_dispatched, append_canonical_world_events | Pass A: listing undispatched work, rearming expired rows, preserving wake times, marking dispatch transitions, and appending canonical events are the delivery lifecycle of the outbox and event log. Pass B: all are durable state transitions over already-decided work (appending canonical events persists validated events, it does not choose them), so each stays. → KEEP |
| firestore_transaction.py: _outbox_record_from_document, _is_snapshot_like, _merge_firestore_set_fields, _BufferedDocumentSnapshot (+ __init__, to_dict), _FirestoreTransactionAdapter (+ __init__, _document_key, _stage_set, _validate_execution_writes, flush_writes, _read_transaction_snapshot, _transaction_query_snapshots, _snapshot_data, _staged_collection_data, _get_snapshot) | Pass A: decoding outbox documents only when identity matches path, snapshot normalization, Firestore set-field merging, buffered snapshots, and staged-write flushing are the transactional machinery that makes timeline writes atomic. Pass B: all are durable-write machinery with identity and execution-write validation (fail-closed), so each stays. → KEEP |
| firestore_transaction.py: all adapter get/put pairs mirroring the store (get/put_date_record, get_date_records_range, get/put_control_record, get/put_admin_audit_record, get/put_coordinator_record, get/put_job_record, get_outbox_record, put_outbox_if_absent, rearm_outbox_if_expired, preserve_outbox_wake_at, mark_outbox_enqueued, mark_outbox_dispatched, get_game_state_snapshot, get/put_private_history, get/put_entity_control, list_entity_controls, list_undispatched_outbox, list_undispatched_outbox_paged, get/put_dead_letter, list_unfinished_background_wakes, get/put_background_wake_record, get/put_execution_claim) | Pass A: the adapter's record operations are the same durable reads/writes as the store's, executed inside a transaction's snapshot view. Pass B: each is a pure durable operation within OCC, so each stays. → KEEP |
| firestore_transaction.py: authoritative_epoch_matches | Pass A: checking whether the transaction-time game state authorizes writes for an epoch is the authorization gate for every transactional write. Pass B: it is an authorization predicate over durable state, so it stays. → KEEP |
| firestore_transaction.py: append_canonical_world_events | Pass A: appending validated canonical events inside a transaction is the atomic event-log write. Pass B: it persists events validated elsewhere and never chooses their content, so it stays. → KEEP |
| firestore_transaction.py: merge_game_state_updates | Pass A: staging canonical state updates only when the provider base still matches is the OCC guard that prevents a stale provider response from overwriting newer state. Pass B: it is a conditional durable write (base-match required), which is authorization-style concurrency control, not authorship, so it stays. → KEEP |

### world_sim/timeline/models.py — coverage note

Each dataclass below is listed with its codec methods (`to_dict`/`from_dict`, plus any
special method named). The codec methods are mechanical serialization with no judgment;
the verdict applies to the dataclass and each of its named methods individually.

| Symbols | Justification |
|---|---|
| TimelineStoreError, FencedCommitError | Pass A: typed store errors are error vocabularies for the models layer. Pass B: as error types they are transport, so each stays. → KEEP |
| SlotState, ConflictProfile, ConflictSignal, EpisodeTransition, CanonicalActionBasis, EventClass, EventDisposition, EventStakes, ProducerMode, CoordinatorStage, OutboxStatus, JobStage, ChunkStage, DecisionType, DecisionStatus (enums + value vocabularies) | Pass A: state-machine vocabularies for timeline records are labels the model path could restate, but they must be exact for durable records to interoperate. Pass B: as pure vocabularies they are transport, deciding nothing by themselves, so each stays. → KEEP |
| TimelineDateRecord (+ to_dict/from_dict), LethalEpisode (+ to_dict/from_dict), AntagonisticState (+ to_dict/from_dict), PrivateHistoryEntry (+ to_dict/from_dict), QuarantineRecord (+ to_dict/from_dict), ProducerControlState (+ to_dict/from_dict), ProducerControlBasis (+ to_dict/from_dict, from_control), CampaignTimelineControlRecord (+ to_dict/from_dict), GapSegmentRecord (+ to_dict/from_dict), CoordinatorArchiveSummary (+ to_dict/from_dict), GapCoordinatorRecord (+ to_dict/from_dict, get_latest_covered_end_date, get_covered_start_date), DispatchOutboxRecord (+ to_dict/from_dict), ValidationAttemptRecord (+ to_dict/from_dict), RetryState (+ to_dict/from_dict), PerDateDecisionRecord (+ to_dict/from_dict), RelevanceChunkRecord (+ to_dict/from_dict), RelevanceJobRecord (+ to_dict/from_dict), RetryScheduleResult (+ to_dict/from_dict), ContinuationResult (+ to_dict/from_dict), TimelineWakeResult (+ to_dict/from_dict), EntityControlRecord (+ to_dict/from_dict), DeadLetterRecord (+ to_dict/from_dict), BackgroundExecutionClaimRecord (+ to_dict/from_dict), BackgroundWakeControlRecord (+ to_dict/from_dict), ReconcilerControlRecord (+ to_dict/from_dict) | Pass A: these record shapes are the durable schema for timeline state; deleting any of them deletes persistence for that record type, which the bare log cannot replace. Pass B: dataclasses plus mechanical codecs are transport, and their bounded lists (e.g. receipts) are bounded capacity, so each record and each of its named methods stays. → KEEP |
| ForegroundActionReceipt (+ to_dict/from_dict, get_action_receipt, record_action_receipt) | Pass A: action receipts are the durable evidence linking a player action to its timeline consequences. Pass B: receipt lookup and bounded recording (bounded to max_receipts) are durable writes plus bounded capacity, so the record and all three methods stay. → KEEP |
| resolve_outbox_route | Pass A: resolving an outbox route from trusted server configuration is the routing decision delivery needs. Pass B: it resolves from server configuration, never from a task payload's claimed destination, which is authorization-correct transport, so it stays. → KEEP |

### world_sim/timeline/ops_cutover_timeline_producer_schema.json

| Symbol | Justification |
|---|---|
| Schema document (single JSON asset) | Pass A: the cutover producer schema constrains admin operations that prose alone cannot validate. Pass B: a schema is transport, not a transform, so it stays. → KEEP |

## §6 conflict log (explicit)

1. **No DELETE in this file removes faction simulation or the living world.** DELETE
   rows target recomputation (FP/ranking/damage/intel-tier arithmetic, SRD scaling,
   display formatting, cooldown stripping, semantic highlight validation, time
   formatting/merging). The simulation capability itself is preserved as async
   background provider + worker execution (ADAPT/KEEP), per decision 3.
2. **Battle/intel dice vs. formula deletion:** `roll_dice`, `roll_attack`, and
   `is_detected` are KEEP on the turn path per decision 2, while the expected-value
   fast path and all formula helpers around them are DELETE/ADAPT. The split is
   deliberate: anti-cheat protects randomness, not arithmetic.
3. **Antagonist/living-world cooldown stripping (DELETE) vs. the living-world
   promise:** decision 3 rescues background simulation, not server-side stripping of
   model-authored events. The strip rows therefore record an *unregistered-exception
   gap*: if the parent wants the server strip to survive, it must name and register
   the exception; until then the decision moves to prompt/schema. This is flagged,
   not silently resolved.
4. **DualModeManager has only 1 external referencing file** (`faction/__init__.py`)
   in the local pass — no game-path caller was found. Its state-write methods are
   KEEP as durable writes, but if no turn path actually instantiates the manager,
   the whole dual-mode feature is dead code in practice and the parent should confirm
   whether it is reachable from `game_state.py`/`agents.py` before treating KEEP as
   "shipped". This is a coverage caveat, not a verdict change.
5. **`merge_partial_world_time` has only a test referencing file** in the local pass;
   its ADAPT (detection + violation reporting only) assumes the merge is reachable
   from a write path. If it is test-only, it is DELETE, not ADAPT.

## Verdict counts

Counts below were tallied from the verdict arrows in this file (Phase 1 file table
plus Phase 2 rows; grouped rows in the store/models sections count once per row, with
every method named in the row carrying that row's verdict — see the coverage notes).

- Phase 1 (files): KEEP 34, ADAPT 14, DELETE 2 (50 files).
- Phase 2 (rows, tallied by script from the verdict arrows in this file):
  KEEP 281, ADAPT 35, DELETE 46 (362 rows). The dominant verdict is KEEP
  (transport/durable/auth/bounded-capacity infrastructure), followed by DELETE
  (recomputation, formatting, unregistered field-aware transforms) and ADAPT
  (async placement + slimming). Grouped store/models rows each cover multiple named
  methods carrying that row's verdict, so per-method KEEP counts are higher than the
  row tally.
- Symbols inventoried by AST: 698 (including nested closures, which inherit their
  enclosing method's verdict as noted). Every top-level symbol and every class method
  is named in a table row or a grouped row above; no file is partial or blocked.
