# In-scene illustrations design (PR #10564)

**Status:** Implementation in flight on [worldarchitect.ai PR #10564](https://github.com/jleechanorg/worldarchitect.ai/pull/10564) (`cursor/scene-example-gha-0dd5`). This roadmap copy is the engineering plan / status mirror for the feature; the code-repo canonical design lives at `docs/design/in-scene-illustration-design.md` on that branch.
**Pinned head (review B):** `6ec063aa38d5bc8646217caa1e6b23913e287258` (2026-10-18).
**Related:** user story `docs/user-stories-ui/NEW-in-scene-illustration-cadence.md`; follow-ups [worldarchitect.ai #10608](https://github.com/jleechanorg/worldarchitect.ai/issues/10608) (NPC portraits), [worldai_frontend #120](https://github.com/jleechanorg/worldai_frontend/pull/120) (iOS parity).
**Authorization:** docs-only in this repo. Runtime deploy, provider spend, and production settings changes stay on the code-repo PR.

---

## 1. Goals and user requirements

Players with a campaign portrait get a cinematic **1K 16:9** illustration on cadence GM scenes, placed **above the planning choices**, without slowing the narrator.

| Requirement | Spec |
|---|---|
| Image | 1K, `aspect_ratio: 16:9`, quality `low`, OpenRouter only |
| Placement | Narrative → 16:9 slot → choices (streaming uses the same order) |
| Spinner | Reserved aspect-ratio frame shows **"Painting scene…"** while pending |
| Reference | Campaign **portrait** as `input_references` via OpenRouter Grok Imagine Image 2.0 |
| Mode (Settings) | **Off** (default) / **Parallel** / **After scene** |
| Cadence | Every **N** turns (`scene_illustrations_every_n`, default **5**, allowed 1–20) |
| First story scene | When mode is on, the **first post–character-creation** GM scene always gets an image (once); opening scene when CC is skipped also qualifies |
| Latency | **No added user-visible latency** to first text, choices, or input unlock |
| Telemetry | **BigQuery** logs full image/brief requests and responses (image bytes redacted) |

User-facing story: *As a player with a campaign portrait, I want a cinematic illustration every Nth GM scene so key story beats feel visual without slowing down the narrator.*

---

## 2. Architecture

### 2.1 Modules

| Module | Role |
|---|---|
| `mvp_site/scene_illustration_service.py` | Eligibility, coordinator job, OpenRouter 1K + portrait ref, poll/retry, attempt ordering |
| `mvp_site/llm_parser.py` | Parallel/after-scene kickoff; SSE `scene_image` multiplex; persist snapshot without waiting |
| `mvp_site/schemas/scene_illustration_policy.json` | Model, resolution, timeouts, brief model, GCS prefix, debug cost caps |
| `mvp_site/frontend_v1/js/scene-illustration.js` | Slot, spinner, lightbox, poll, Retry, debug buttons |
| `mvp_site/frontend_v1/js/settings.js` | Mode / N / advanced context controls; per-key dirty generations |
| `mvp_site/firestore_service.py` | GCS upload, scene doc upsert, story-entry patch |
| `mvp_site/portrait_bq_logging.py` | BQ image/brief exchange rows (`scene_illustrations_mode`, `extra.scene_context`) |

### 2.2 Parallel kickoff (first story chunk)

In **Parallel** mode the coordinator is created with `defer_start=True` and the image job starts at the **first story chunk**, so image setup cannot delay time-to-first-text. The spinner appears immediately. `SCENE_TIMING` log lines record story-path setup, kickoff, and per-stage job timings.

### 2.3 After-scene flow

In **After scene** mode the job starts once the narrative is available (thread spawn just before `done`). The brief can use the finished GM text. Choices and `done` still must not wait on the image HTTP call.

### 2.4 Delivery

1. **In-stream:** `scene_image` SSE events update the streaming slot when the image finishes before the stream closes.
2. **Stream end:** preferred path closes the SSE right after `done` + persistence warnings (no multi-minute drain that locks the composer).
3. **Held / long-poll:** `GET /api/campaigns/<id>/scene-illustration?user_scene_number=N&idempotency_key=K&wait=20&requested_at=…` long-polls the live job (max ~25s). Needed on Cloud Run request-based CPU so a post-stream job keeps getting CPU **when the poll lands on the same instance**.
4. **Client poll fallback:** after `done`, the client polls ~every 2s (budget ~120–150s, then Retry), targeting `.story-scene-illustration-host` on the final entry (not only the streaming slot). History reload polls up to ~12 pending slots.
5. Early failures (rate limit, no portrait, no key) persist a terminal failed snapshot so polls terminate.

### 2.5 Persistence

- Story entry field `scene_illustration`: `{status, url, error, idempotency_key, requested_at, …}` (`pending` → `ready` / `failed`).
- Firestore doc under `users/{uid}/campaigns/{cid}/scene_illustrations/{user_scene_number}`.
- Worker owns write-back via `patch_story_entry_scene_illustration` so the turn persist path only snapshots pending state.

### 2.6 GCS paths

```
campaign_scene_illustrations/{user_id}/{campaign_id}/{n}{attempt_tag}.{ext}
```

Debug ablation writes sibling blobs only: `{n}-ablation-{letter}{run}.{ext}` (no scene doc / story patch).

### 2.7 Idempotency

- Each attempt carries `idempotency_key` + `requested_at`.
- Newest attempt wins (`scene_attempts` / guarded writes): late results from aborted turns or older retries are dropped; a terminal state is never reverted to pending; stalled heal never downgrades a terminal result.
- Blob names include an attempt tag derived from key + `requested_at` so CDN `Cache-Control` cannot show a stale image after Retry.

---

## 3. Prompt structure

### 3.1 CURRENT SCENE vs BACKGROUND

After s9 Death Note scene 213 painted Misa into a scene where Light was alone (raw “Recent story context” weighted equally with the GM response), prompts use two labeled sections:

- `=== CURRENT SCENE (paint this) ===` — player action + this turn’s GM response (after_scene) or latest GM entry (parallel).
- `=== BACKGROUND (continuity only, do not depict unless present in CURRENT SCENE) ===` — prior non-god entries (trimmed in after_scene raw) or the brief.

**Presence rule:** paint ONLY characters physically present in CURRENT SCENE; if the PC is alone, paint them alone. The brief LLM gets the same rule. Portrait text is labeled as describing only the player character.

### 3.2 God-mode filtering

`filter_scene_context_entries` drops god-mode turns (`GOD MODE:` / `mode=god` player entries and their GM replies, or any entry with `god_mode_response`) and system/meta entries. Illustrated turns skip entirely when the current turn is god-mode.

### 3.3 Context depth / style (experimental)

| Setting | Values | Default |
|---|---|---|
| `scene_illustrations_context_depth` | 5 / 10 / 20 | 5 |
| `scene_illustrations_context_style` | `raw` / `brief` | `raw` |

- **raw:** labeled excerpts → “Recent story context”.
- **brief:** background-thread OpenRouter chat (`brief.model` from policy, 8s timeout) condenses excerpts + action + GM narrative into a ~120-word visual brief; on any error falls back to raw.

Retry regenerates with the user’s **current** mode / N / depth / style. BQ `extra.scene_context` carries depth, style, effective_style, brief_text, brief_model, brief_request/response, brief_latency_ms, brief_cost_usd, brief_fallback_reason.

---

## 4. Settings keys and validation

| Key | Validation | Notes |
|---|---|---|
| `scene_illustrations_mode` | `off` \| `parallel` \| `after_scene` | Default **off**. Legacy `scene_illustrations_enabled: true` reads as `parallel`. |
| `scene_illustrations_every_n` | int 1–20 | Default **5**. UI options 1,2,3,5,10,15,20; hidden when Off. Server 400 outside 1–20. |
| `scene_illustrations_context_depth` | 5 \| 10 \| 20 | Advanced (experimental). |
| `scene_illustrations_context_style` | `raw` \| `brief` | Advanced (experimental). |
| `scene_illustrations_enabled` | legacy bool | Accepted for migration; prefer mode. |

Settings page: per-key user-change generation so a late `loadSettings()` cannot overwrite a user edit; saves serialize with captured values; await prior `settingsSaveInFlight` before POST.

**Deploy caution (review B1):** settings API rejecting unknown keys breaks existing iOS clients that still send `openclaw_gateway_port` / `openclaw_gateway_url`. Fix by silent-filter or an accepted-but-ignored set before shipping.

---

## 5. Debug tooling and cost caps

| Tool | Where | Behavior |
|---|---|---|
| **Prompt ablation** | Under scene image when `debug_mode` | Variants A–E (`scene_prompt_ablation.py`); dry run then generating run; sibling `-ablation-` blobs only |
| **Compare models** (scene) | Next to ablation | e.g. Grok 2.0 + Nano Banana 2.1 with structured variant |
| **Compare models** (portrait) | Portrait dialog | 2K previews per model; apply only on **Use this** |

Policy `debug_image_tools` (`scene_illustration_policy.json`):

- ≤ **10** images per ablation request (`max_images_per_request`; default `runs=1` → 5 images).
- **3** generating ablation runs and **40** debug images per user per UTC day (`users/{uid}/debug_image_budget/{date}`).
- Each ablation image also consumes one `scene_illustration` quota unit; portrait compare consumes portrait quota.
- `prompt_override` limited to allow-listed emails/UIDs (policy + `DEBUG_PROMPT_OVERRIDE_EMAILS` / `DEBUG_PROMPT_OVERRIDE_UIDS`).

Non-debug users never see the buttons and get 403 from the server. Review **B2** originally found unmetered ablation; the caps above are the intended control plane (verify present on the merge head).

---

## 6. Cost per image

Current production path: OpenRouter `x-ai/grok-imagine-image-2.0`, 1K low, 16:9, xAI-only routing.

| Component | List price (OpenRouter / vendor) |
|---|---|
| Output 1K low | **$0.04** |
| Per input reference | **$0.01** |
| Typical scene (PC portrait only) | **≈ $0.05** |
| Planned multi-ref (PC + 2 NPCs, #10608) | **≈ $0.07** |
| Optional brief LLM | OpenRouter `usage.cost` on chat model (`google/gemini-3.8-flash` in policy) |

Portraits remain **2K** under `user_portrait_policy.json` (~$0.06–0.08 low).

---

## 7. Latency (s9 measurements)

Steering rule: **no added user-visible latency** vs Off for first text / done / input unlock.

| Build | Condition | First text | Done |
|---|---|---|---|
| `312205b` (before) | Off | **10.7s** | **20.7s** |
| `312205b` | Parallel | **10.3s** | **21.6s** |
| `ec73408` (regression) | Image turns | **37–46s** first text | — |
| `6ec063a` (fixed) | Image turns | **7.0–9.8s** | — |
| `6ec063a` | Non-image turns | **7.0–11.3s** | — |

Root causes of the regression / lock (see also `ROOT_CAUSES.md` diagnosis): parallel kickoff before first chunk; pre-done `sleep(0.15)` on persist; post-done SSE drain holding the fetch open so `onStreamEnd` delayed `restoreUiState`. Fix direction: kickoff at first chunk, no persist sleep, close SSE after done (+warnings), client poll / long-poll for late images.

---

## 8. Known issues and in-progress work

### 8.1 After-scene first-try failures (Cloud Run CPU + orphaned jobs)

**Symptom:** After-scene (and Parallel jobs that outlive the SSE) often stall on the first try: spinner → timeout → Retry; user pays twice.

**Cause:** Cloud Run s-pool uses **request-based CPU** and **no session affinity**. After the stream closes, the job’s instance is throttled unless a request is open **on that same instance**. A poll on another instance sees Firestore `pending` with no live `_ACTIVE_JOBS` entry and returns immediately; the worker starves until the 180s stalled heal.

**Fix in progress:**

1. Keep the stream open after `done` long enough for after-scene jobs **or** ensure held long-poll affinity / CPU-always-allocated / Cloud Tasks worker (deploy decision).
2. **Firestore-lease single-flight** so retries and concurrent polls do not start a second generation; reuse an in-flight attempt (live job or fresh pending doc) instead of double spend.

Code mitigations already described on the branch: pending scene doc with instance id; client poll budget ≥ worst-case job; stalled heal at 180s; retry reuse of in-flight attempts; newest-attempt-wins writes.

### 8.2 Review findings B1–B7

From independent `/ready` reviewer B (2026-10-18) against head `6ec063a`:

| ID | Severity | Summary |
|---|---|---|
| **B1** | BLOCKER | Settings API 400 on unknown keys breaks shipped iOS (`openclaw_gateway_*`). Restore silent filter or accepted-but-ignored set. |
| **B2** | BLOCKER | Debug prompt ablation was unmetered on the server OpenRouter key (up to 20 images/request). Enforce allowlist / quota / daily caps / restrict `prompt_override` (see §5). |
| **B3** | should-fix | Stale poll can overwrite a newer READY scene with `failed/stalled` when poller key ≠ doc key. Only stall when doc absent or still pending. |
| **B4** | should-fix | Aborted turn’s image can land on the replacement entry; retries reused the same public URL (CDN cache). Attempt-tagged blobs + key-checked patch. |
| **B5** | should-fix | Completing a post-`done` job depends on poll landing on the same instance (CPU affinity). Session affinity, CPU-always, or Tasks/worker. |
| **B6** | should-fix | Blocking retry joins up to ~130s; concurrent retries not deduplicated. If `active_scene_job` alive, return/long-poll that snapshot. |
| **B7** | should-fix | Client poll timeout (~120s) below server worst case (brief 8s + image up to 90–120s + upload). Align deadlines. |

Nits B8–B13 (dead `scene_illustrations_enabled` write, mixed-case mode 500, non-numeric `runs` 500, cancelled job left pending, throwaway proxy in tree, bundled CI change) are tracked on the code PR.

---

## 9. Model alternatives (research summary)

Researched 2026-10-18 for multi-character scenes (#10608). Full write-up: workspace `image-api-research/report.md`.

**Current:** `x-ai/grok-imagine-image-2.0` — max **3** `input_references` on OpenRouter; AA edit Elo 1118; p50 latency often high (~75s in one window); ~$0.04 + $0.01/ref.

**Leading candidate: Nano Banana 2.1** (`google/gemini-nano-banana-2.1`):

- 14 refs (Google: ≤**4** character-consistent; rest objects/style)
- ≈ **$0.0336**/1K image (often ~$0.04–0.045 with refs) — ~40% cheaper than 3-ref Grok
- AA edit Elo **1152**; p50 ~**22s**
- SynthID watermark; fewer IP refusals than GPT Image in third-party tests

**Recommendation for scenes:** switch to NB 2.1 with PC + top 3 present NPCs as individual refs + one composite sheet; keep Grok as fallback on safety/error. **Premium A/B:** `openai/gpt-image-2.5-sunburst` (Elo 1199) if fantasy-violence / canon refusals are acceptable.

No model reliably keeps ~10 identities intact in one image (CogCanvas / MultiBind). Plan remains: individual refs for prominent characters + composite for the rest.

---

## 10. Follow-ups

| Work | Tracking |
|---|---|
| **NPC portraits** (max 10/campaign, auto `portrait_worthy`, multi-ref scene images) | [worldarchitect.ai #10608](https://github.com/jleechanorg/worldarchitect.ai/issues/10608) |
| **iOS parity** (settings UI, poll with `wait` + `requested_at`, scene slot) | [worldai_frontend PR #120](https://github.com/jleechanorg/worldai_frontend/pull/120) — blocked on long-poll contract (F1) and settings key contract (F2/B1) |
| Code-repo design mirror | `docs/design/in-scene-illustration-design.md` on PR #10564 |
| User story | `docs/user-stories-ui/NEW-in-scene-illustration-cadence.md` |

---

## 11. Policy snapshot (merge-head intent)

```json
{
  "openrouter": {
    "model": "x-ai/grok-imagine-image-2.0",
    "resolution": "1K",
    "aspect_ratio": "16:9",
    "quality": "low"
  },
  "provider_timeout_seconds": 90,
  "gcs_path_prefix": "campaign_scene_illustrations",
  "brief": { "model": "google/gemini-3.8-flash", "timeout_seconds": 8 },
  "debug_image_tools": {
    "max_images_per_request": 10,
    "default_runs": 1,
    "daily_ablation_runs": 3,
    "daily_images": 40
  }
}
```

Re-read `mvp_site/schemas/scene_illustration_policy.json` on the implementation head before treating numbers as contractual.
