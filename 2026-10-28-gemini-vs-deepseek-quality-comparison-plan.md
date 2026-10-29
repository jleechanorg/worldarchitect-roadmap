# Gemini 3.8 Flash vs DeepSeek V4.1 Flash — Quality Comparison Plan

**App:** WorldArchitect.AI (digital D&D 5e Game Master, `jleechanorg/worldarchitect.ai`)
**Question:** Can DeepSeek V4.1 Flash replace Gemini 3.8 Flash for WorldAI traffic, and for which agent classes?
**Date:** 2026-10-28
**Status:** Plan only. No model traffic has been moved. No production setting changes in this plan.

## Why this comparison, why now

- October 2026 GCP spend hit 444% of the $1,000 budget. The Gemini API line alone was
  $2,645.88 for Oct 1–28 (2.65B uncached input tokens, 5.77B cached input tokens,
  95M output tokens).
- At the same token volumes, DeepSeek V4.1 Flash prices to ~$471 off-peak / ~$942 peak
  for the same 28 days — roughly $1,700–$2,175 saved per period.
- Gemini 3.8 Flash list prices double on Jan 1, 2027 ($0.75/$3.75 → $1.50/$7.50 per
  million input/output tokens). The decision should land before that date.
- Public benchmarks are mixed, not decisive: the two models are near-tied on agentic
  coding suites (Terminal-Bench 2.1, DeepSWE), DeepSeek leads the hardest suite
  (Terminal-Bench 4.0), Gemini leads knowledge/reasoning suites (GPQA, ARC-AGI-2)
  and APEX-Agents. No public benchmark measures GM narration or multi-session
  world consistency, which is exactly what this app sells. Hence: measure it ourselves.

## What "quality" means for this app

These are the dimensions that matter, grounded in how the app is built:

1. **Mechanical integrity (hard gate).** Model output must parse into the canonical
   narrative response schema (`mvp_site/narrative_response_schema.py`): state updates,
   planning blocks, rewards, god-mode directives. The server executes dice itself, so
   any model-claimed roll or mechanic contradicting server state is a defect, not a
   style difference.
2. **Rules adherence.** D&D 5e rules, campaign rules, and player-invented God Mode
   Directives must be respected, including when they conflict with what the player
   just asked for.
3. **Continuity.** NPCs, factions (12 autonomous factions per campaign), world state,
   and memories must stay consistent across turns and sessions. Contradictions with
   established state count against the model.
4. **Narrative quality.** Voice, pacing, NPC dialog distinctness, and quality of the
   choices offered in planning blocks. Judged blinded (see below).
5. **Reliability.** Schema-valid rate, JSON-parse fallback rate, retry rate, latency
   (p50/p95), and streaming stalls. A cheaper model that falls back often is not cheaper.
6. **Cost per turn.** Tokens in/out/cached and dollars per turn, by agent, at observed
   DeepSeek cache-hit and peak-hour rates — not assumed ones.

## Method: paired comparison on identical inputs

- **Same input, both models.** Every eval case runs once on Gemini 3.8 Flash and once
  on DeepSeek V4.1 Flash, with production prompts, production temperature, and
  production effort settings. Model identity is hidden from judges (A/B labels only).
- **Golden set from real traces.** Build eval cases from production run bundles
  (same pattern as the autor-eval repo's trace-to-eval-case conversion: run artifacts
  → normalized eval-case JSON). Cover all agent classes and modes: Story, Combat,
  Dialog, Character Creation, Level-Up, Rewards, Info, God Mode, Planning (think
  mode), Faction, Campaign Upgrade, Spicy. Include edge cases: long campaigns with
  large cached context, multi-faction scenes, level-up with rewards pending, and
  god-mode directive conflicts.
- **Two prompt arms.** Arm 1: byte-identical prompts on both models. Arm 2: a light
  DeepSeek-adapted prompt variant (formatting only, no content change). Report both,
  so prompt-tuning differences are not mistaken for model differences.
- **Effort arms.** Test DeepSeek at production-equivalent effort, not only max effort
  (max effort costs ~2.5x output tokens in vendor reports). Add one max-effort arm
  for Planning/think mode only, where reasoning matters most and output is small.
- **Judges.** (a) Automated: schema parse validity, dice/mechanics audit against
  server state, state-diff vs expected updates, tool-call correctness.
  (b) LLM judge with a fixed rubric on blinded outputs. (c) Human spot-check on a
  sample, focused on narrative quality and continuity — the dimensions automation
  cannot see.
- **Version pinning.** Record exact model IDs in every run (`deepseek-flash` serving
  V4.1 Flash; `gemini-3.8-flash`). Re-run if either vendor ships a new checkpoint
  mid-evaluation. Sanitize real-campaign eval cases before they leave GCP.

## Metrics and proposed decision bars (confirm before Phase 1)

| Metric | Proposed bar for DeepSeek to pass, per agent class |
|---|---|
| Schema-valid rate | No more than 1 point below Gemini |
| JSON-parse fallback rate | No higher than Gemini |
| Mechanics defects (fabricated dice/rules) | No increase over Gemini; any increase fails that agent class |
| State-continuity errors per 100 turns | Within 10% of Gemini |
| Blinded narrative rubric (0–100) | Within 5 points of Gemini mean |
| Latency p95 | Within 2x of Gemini (streaming UX) |
| Cost per turn | Reported, not gated — the savings are already quantified |

Bars are per agent class, not all-or-nothing: Story/Dialog may pass while
Combat/Planning does not, and that is a valid outcome.

## Phases

- **Phase 0 — Provider wiring (no traffic change).** Add a DeepSeek provider module
  on the existing OpenAI-compatible provider layer (`mvp_site/llm_providers/`, which
  already serves Cerebras and OpenRouter). Feature-flag model selection per agent.
  Verify: auth, streaming, JSON structured output against the narrative schema,
  tool calls, and cache behavior on a handful of manual turns.
- **Phase 1 — Offline paired eval.** Run the golden set through both models in the
  autor-eval repo. Publish a per-agent scorecard on the metrics above. This is the
  main decision input; do not skip it for a live test.
- **Phase 2 — Shadow pilot.** DeepSeek runs alongside Gemini on live Story/Dialog
  traffic only. Its outputs are logged, never served. Compare on real distributions
  (including cache-hit rates and peak-hour mix) that the golden set cannot reproduce.
- **Phase 3 — Live A/B.** A small share of campaigns gets DeepSeek for Story/Dialog.
  Guardrails: automatic fallback to Gemini on any schema failure; alerts on fallback
  rate, latency, and player reports. Pre-registered stop rule: halt the arm if
  fallback rate or mechanics defects exceed Gemini's baseline.
- **Phase 4 — Expand or hold.** Extend to Combat/Planning/rules-critical agents only
  if their Phase 1 bars are met. Keep Gemini as fallback and for the highest-stakes
  turns regardless. Revisit the whole decision before Jan 1, 2027.
- **Phase 5 — Decision doc.** Per-agent verdict (adopt / hold / reject), observed
  cost per turn, and the rollout or rollback plan. File it in this repo.

## Risks and confounds to track explicitly

- **Cache semantics differ.** Gemini's cache vs DeepSeek's automatic prefix cache:
  measure observed DeepSeek hit rates; never assume Gemini's 69% cache-read share
  transfers.
- **Peak pricing.** DeepSeek rates double in weekday peak windows, which include
  overnight PDT (11pm–3am). Break cost down by hour; nightly jobs may price worse
  than daytime traffic.
- **Tokenizer differences.** Compare on identical scenarios and report tokens per
  turn, not just dollars. A model that uses more tokens per turn can erase a
  per-token price edge.
- **Prompt tuning.** The 30 prompt files (17,369 lines) were tuned for Gemini.
  Arm 2 exists for this reason; a gap that closes with formatting-only adaptation
  is a prompt problem, not a model verdict.
- **Version drift.** Both vendors ship new checkpoints. Pin IDs, log versions, and
  treat a mid-eval checkpoint change as a re-run trigger.
- **Image/video.** Current usage is tiny (image ~3M tokens, video ~0). DeepSeek
  Flash accepts image input; if any agent path needs video or audio, it stays on
  Gemini — verify before moving any multimodal path.
- **Quality is not one number.** A single blended score would hide a failure in
  Combat behind a win in Story. All reporting is per agent class.

## Deliverables

1. Golden eval set + harness changes (autor-eval repo).
2. Per-agent scorecard (this plan's metrics, both prompt arms).
3. Shadow-pilot report (real cache rates, peak-hour cost, fallback rate).
4. Decision doc + rollout/rollback plan (this repo).
