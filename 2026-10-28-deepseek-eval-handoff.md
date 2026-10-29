# DeepSeek eval handoff (2026-10-28)

Self-contained brief for the agent taking over the DeepSeek-vs-Gemini evaluation.

## Goal
Decide, **per agent**, whether DeepSeek can replace Gemini before Gemini's price doubles on **Jan 1, 2027**.

Existing plan: [2026-10-28-gemini-vs-deepseek-quality-comparison-plan.md](https://github.com/jleechanorg/worldarchitect-roadmap/blob/main/2026-10-28-gemini-vs-deepseek-quality-comparison-plan.md). Where it conflicts with this brief, follow this brief.

## Review corrections to the plan
- There are **15 concrete agents**, including DeferredRewards, HeavyDialog and Portrait.
- There are **128 prompt files**.
- `AI_FACTION_COUNT=200`, not 12.
- The eval repo is **jleechanorg/worldarchitect-autor-eval**. It has **no LLM judge**, so you need to build one (see Judge).
- The cost baseline is **about $2,777 at list prices**, not $2,645.88.
- **Cached input doubles too.** Include it in the post-Jan-1 projection.

## Dice confound (critical)
- Gemini uses `code_execution`. Non-Gemini providers use `native_two_phase` (`mvp_site/dice_strategy.py`).
- `CODE_EXECUTION_KILL_SWITCH_MODELS` can force Gemini onto two-phase. Use it for the Gemini two-phase arm so the dice path is controlled.
- Research: the DeepSeek API has **no server-side code execution**, only client function calls (https://api-docs.deepseek.com/guides/tool_calls). Alibaba Model Studio's `code_interpreter` and OpenRouter's beta shell tool exist, but both are Responses-API-only and slow.
- **Recommended:** the server pre-rolls the dice and injects them into the prompt. **Fallback:** two-phase.

## Structured output
- DeepSeek strict mode is beta and lives at `/beta`.
- The openai-compatible core **drops `response_format` when streaming**. Fix or account for this.
- Add a DeepSeek schema acceptance manifest like `gemini_schema_acceptance.json`.

## Round 1 (decided by the user)
- Arms:
  1. Gemini, current setup (code execution)
  2. Gemini, two-phase (kill switch)
  3. DeepSeek, two-phase
  4. *(optional)* DeepSeek with pre-rolled dice
- **Spend cap: $30 total for round 1.** Track spend as you go and stop before the cap.

## Stats
- Use non-inferiority margins with confidence intervals.
- The full run needs about **60 paired cases per agent class**.
- Round 1 is a small pilot that fits within the $30 cap.

## Judge
- Use a third model family (neither Gemini nor DeepSeek).
- Normalize outputs before judging, and randomize their order.

## Privacy
- The user must decide whether real traces may go to DeepSeek **before any real-trace eval**.
- Until then, use synthetic campaigns or owner-only campaigns.

## Rules
- Don't touch prod data or campaign `BvAezUphceUtghL587QQ`.
- The Gemini key comes from GCP Secret Manager `gemini-api-key`.
- **Stop at the first provider or auth failure** and report it. Don't work around it.

## Definition of done (round 1)
1. A results table (agent × arm, with quality scores, CIs and the non-inferiority verdict).
2. A cost receipt (actual spend per arm, within $30).

## Related open work in jleechanorg/worldarchitect.ai
- #10734 register OpenRouter `deepseek/deepseek-v4.1-flash` (settings)
- #9844 add deepseek v4.1 flash to OpenRouter
- Most other PRs tagged `[deepseek-4.1-flash]` were written by agents running on DeepSeek. They aren't DeepSeek provider work.
