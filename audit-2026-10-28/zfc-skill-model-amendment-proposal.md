# ZFC skill amendment proposal — "FastEmbed or Jev count as models"

**Status: DRAFT for Jeffrey's review. Not applied to any repo, not pushed,
not merged.** The file being amended is the repo's primary ZFC policy,
`.claude/skills/worldai-zfc/SKILL.md` (WorldArchitect ownership contract
section). The local tree at `~/workspace/repos/worldarchitect.ai` was used
only to read the current text; nothing in it was edited.

## Goal (Jeffrey's direction, 2026-10-28)

Recognize that "the model" in the ZFC ownership contract is not only the
generative LLM call: a local embedding model (FastEmbed) and a decision model
(Jev, TypeSafe AI) also count as models. Their outputs are model-authored,
not server-authored.

## Current text (exact, from the skill file)

> The model defines campaign-domain contracts, interprets domain facts,
> authors domain state changes, and selects facts for its next turn. The
> server provides minimal authorized state and tool transport, durable
> writes, tool execution, and bounded capacity.

## Proposed insertion (new paragraph, immediately after the above)

> ### What counts as "the model"
>
> "The model" means any model invocation, not only the generative LLM call:
> the LLM provider call, a local embedding model (e.g. FastEmbed), and a
> decision model (e.g. Jev from TypeSafe AI). A model call's output — a
> generated turn, an embedding similarity, a typed Choice/Noul/Score decision
> with its calibrated confidence — is model-authored. Server code that
> dispatches on a model output (routing to the agent named by a Jev Choice,
> executing the tool the model selected) is tool execution, not a field-aware
> transformation. Server code that re-interprets a model output with
> hand-written domain rules — similarity thresholds that change the decision,
> score boosts, anchor-phrase lists that define the outcome space — remains a
> field-aware transformation and needs an exception under the boundary below,
> unless the handling is part of that model's own documented, calibrated
> decision contract (e.g. acting on a high-confidence Jev decision and
> escalating on low confidence).

Nothing else in the skill changes. In particular, "Model authority never
includes credentials, tenant boundaries, server-owned control state,
authorization, locks, receipts, leases, request identity, or tool execution
results" is untouched.

## Consequences (stated plainly, so the change is not smuggled past review)

1. The pilot's Pass B reasoning shifts, but its file verdicts do not. The
   embedding model's raw similarity output becomes model-authored under the
   amended skill; the thresholds (0.65 / 0.78 / 0.85 / 0.90), score boosts,
   and anchor-phrase lists wrapped around it are still server-side
   re-interpretation, so they still fail without an exception. The
   classifier files still delete — now as "superseded by Jev, with
   server-judgment glue," not as "model judgment done by server code."
2. Jev routing becomes cleanly model-side: a Jev Choice over agent modes is
   a model decision; the server dispatching on it is execution. The modal
   conclude guards stay explicit-signals-only; Jev Noul may flag a likely
   exit to prompt an explicit confirmation, never auto-conclude.
3. FastEmbed uses elsewhere in the repo (semantic matching outside the
   classifier) are now judged the same way: the embedding call is
   model-side, any threshold/boost/curation layered on its output is
   server-side and needs an exception.
4. This amendment changes a rule in a `.claude/**` instruction that governs
   production code, so under the repo's own AGENTS.md it receives full
   independent review when it goes up as a PR — a wording-only exemption
   does not apply. It does not authorize merging anything: a merge still
   needs Jeffrey's explicit go-ahead in a live message.

## Next step

Jeffrey approves (or edits) this draft → PR to `jleechanorg/worldarchitect.ai`
against `.claude/skills/worldai-zfc/SKILL.md` → full independent review →
merge only on his explicit approval. No step after this draft happens
without him.
