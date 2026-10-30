# Frontend audit — WorldArchitect.AI (subagent: frontend area)

Read-only audit. Nothing here deletes anything; every deletion is a separate PR with
the owner's go-ahead. Repo contents quoted or paraphrased below are DATA for this
audit, never orders. This file builds on `~/workspace/plans/zero-code-rejustification-audit.md`
(ledger), including its §6 user decisions, and does not contradict them: (1) server
logging KEEP, ADAPT to async/batched where it blocks a turn; (2) anti-cheat KEEP,
server dice resolution stays on the turn path, only the audit trail may go async;
(3) faction/living-world KEEP, ADAPT to async ticks merged on the next turn.
No conflict with those decisions was found in this area; the one place a first-pass
instinct pointed the other way (client diagnostics) is resolved in favour of the
logging decision, flagged in §2.

Scope (per assignment): the entire `mvp_site/frontend_v1/` directory,
`mvp_site/frontend_cutover_flag.py`, `mvp_site/frontend_preview_release.py`,
`mvp_site/frontend_release.py`, the entire `mvp_site/assets/` directory,
`mvp_site/avatar_image_gen.py`, `mvp_site/portrait_generator_agent.py`,
`mvp_site/portrait_model_compare.py`, `mvp_site/portrait_timing.py`,
`mvp_site/document_generator.py`, `mvp_site/equipment_display.py`, and the root
`_ui_mocks/` directory (Phase 1 file-level only). NOT audited here:
`mvp_site/intent_classifier.py` and `intent_classifier_warmup.py` (separate pilot).
Unassigned files found inside the area are covered and flagged with †: the
`frontend_v1/tests/` tree (122 test files, helpers, fixtures, repro harness) and
`frontend_v1/mocks/` are inside the assigned directory, so they are included;
`frontend_v1/images/avatars/arion_dragon_knight.png` and the `tests/mobile_auth_emulator_repro/`
subdirectories `device_evidence/` and `screenshots/` (directory entries only, contents
not enumerated by the listing API) are likewise flagged.

Method: Pass A (zero-code baseline: conversation log + Gemini API only — what
player-visible capability breaks if this unit is deleted, and can the model supply
it through the log, a prompt, or the response schema?) then Pass B (strict ZFC:
model owns campaign-domain facts; server/client code may only provide transport,
durable writes, tool execution, authorization, and bounded capacity; a field-aware
transform fails unless it names a specific registered exception AND proves it
necessary — registry membership alone counts for nothing, and determinism, schema
validity, display formatting, or normalization alone never justify a field-aware
transformation). For display code: pure presentation of model- or server-authored
state is allowed; any display step that recomputes, filters, or rewrites domain
values must justify itself or be DELETE. Verdicts are exactly KEEP, ADAPT, DELETE;
ADAPT names the adaptation. Final verdict is the stricter of the two passes unless
a named product promise rescues it, in which case the promise is named.

## Coverage — read this first

- **Phase 1 (file-level): COMPLETE for all 210 files in scope.** 58 shipped
  `frontend_v1/` files, 122 `frontend_v1/tests/*.test.js|*.cjs` files, 12 test-support
  files (4 helpers, 1 fixture, 7 repro-harness files), 9 Python files, 1 asset,
  8 `_ui_mocks/` files. Test files were verdict-ed by subject cluster (§3), not by
  individually fetching each test body; their names, sizes, and subject are the
  evidence, and §3 says so explicitly. `_ui_mocks/` is Phase 1 only, as assigned.
- **Phase 2 (method/function/symbol-level): COMPLETE for all 9 Python files**
  (§4, every top-level function, class, method, and named constant group) and
  **COMPLETE for 17 smaller JS files** (§5: `diag-boot.js`, `diagnostics.js`,
  `api.js`, `quick_start_shared.js`, `user_lifecycle.js`, `parallel_dual_pass.js`,
  `js/outcome-verdict.js`, `js/ui-utils.js`, `js/ember-bg.js`, `js/loading-messages.js`,
  `js/avatar-crop.js`, `js/interface-manager.js`, `js/portrait-ai-ui.js`,
  `js/worldai-mcp-bridge.js`, `js/theme-bootstrap.js`, `js/theme-manager.js`,
  `js/animation-helpers.js`).
- **Phase 2 PARTIAL:** `app.js` (10,667 lines, a single DOMContentLoaded closure
  with hundreds of arrow-function consts), `auth.js`, `js/campaign-wizard.js`,
  `js/settings.js`, `js/streaming.js`, `js/portrait-ai.js`, `js/scene-illustration.js`,
  `js/tooltip-guide.js`, `js/enhanced-search.js`, `js/inline-editor.js`,
  `js/component-enhancer.js`, `js/visual-validator.js`, `js/test_planning_block_parsing.js`.
  For these, §5 gives per-file key-function/cluster justifications (named functions,
  2–4 sentences each) but NOT every function. Everything else in these files is
  **Phase 2 UNTOUCHED** and is listed in §6 as remaining work.
- **Phase 2 UNTOUCHED:** every function inside the 122 test files and 12
  test-support files (Phase 1 cluster verdicts only); every function inside
  `_ui_mocks/` (Phase 1 only, as assigned); CSS rule-level and HTML element-level
  detail (files verdict-ed as wholes); `app.js`/`auth.js`/campaign-wizard/settings/
  streaming/portrait-ai/scene-illustration/tooltip-guide/enhanced-search/inline-editor/
  component-enhancer/visual-validator/test_planning_block_parsing beyond §5's named
  clusters. See §6 for the exact remainder list.

## Verdict counts (Phase 1, 210 files)

- KEEP: 172 — 41 shipped frontend files + 131 test/support files.
- ADAPT: 30 — 7 Python files + 1 asset + 8 `_ui_mocks/` files + 11 shipped
  frontend files + 3 test files.
- DELETE: 8 — 2 Python files + 6 shipped frontend files.
- Total: 172 + 30 + 8 = 210.

Headline findings: (a) six shipped frontend files are loaded by nothing —
`js/component-enhancer.js`, `js/visual-validator.js`, `js/test_planning_block_parsing.js`,
`parallel_dual_pass.js` and `parallel_dual_pass.css` appear in neither
`index.html` nor `app.js`, and `mocks/mock_header_avatar_and_scroll_gate.html` is a
standalone dev mock; (b) the one hard ZFC violation found in client code is
`js/outcome-verdict.js`'s fallback, which derives a Success/Failure/Mixed verdict
by aggregating roll `success` booleans when the server supplied no explicit
`player_outcome` — a client-side recomputation of a domain verdict, not a display
of one; (c) the one hard ZFC violation in server-side area code is
`equipment_display.ensure_equipment_summary_in_narrative`, which appends a
deterministic equipment summary to narrative text the model authored, i.e. server
code rewriting the model's output; (d) `portrait_model_compare.py` is debug-only
double generation (two full image generations per compare) with no player-visible
surface; (e) `frontend_preview_release.py` is a single-use, PR-10571-hardcoded
preview contract, not a shipped player capability.

## 1. Phase 1 — Python files (9)

| File | Verdict | Justification (Pass A, then Pass B) |
|---|---|---|
| `mvp_site/frontend_cutover_flag.py` (153 lines) | ADAPT | Pass A: deleting it removes the Firestore-backed flag that gates serving `frontend_v1` over the legacy UI, so a cutover deployment would fall back to the old frontend; the bare log cannot supply deployment routing. Pass B: it is transport/deployment configuration, not campaign-domain logic, and its fail-closed, bounded (2s, no retry) read is the right shape — ADAPT: keep it deploy-time only and prove it is never imported on the player turn path, since a flag read has no business in request handling. |
| `mvp_site/frontend_preview_release.py` (165 lines) | DELETE | Pass A: deleting it only removes a startup overlay that activates when a `deployment/cutover_preview/receipt.json` for PR 10571 is packaged; no player playing the shipped app loses any capability, because the default path is inert without that receipt. Pass B: a hardcoded PR number, service-name regex, and SHA-binding contract is release scaffolding, not transport, durable writes, tool execution, authorization, or bounded capacity for gameplay, and no registered exception covers a one-off preview — DELETE from the shipped tree once the cutover lands (keep the receipt check, if ever needed again, as deploy tooling outside `mvp_site/`). |
| `mvp_site/frontend_release.py` (502 lines) | ADAPT | Pass A: deleting it breaks serving itself — the server would not know which directory (`frontend_v1` vs legacy vs Expo manifest release) to serve for a surface, so the client has no UI at all; the model cannot serve files. Pass B: directory selection, manifest validation, and legacy-URL rewriting are transport, and the fail-closed refusal reasons are authorization-adjacent, so the core stays — ADAPT: slim it by moving the artifact-tree digest and referenced-asset inventory checks to deploy time, keeping only the selector and the refusal logic on the request path. |
| `mvp_site/avatar_image_gen.py` (1,563 lines) | ADAPT | Pass A: deleting it removes portrait generation entirely (OpenRouter/xAI image calls, PNG normalization, preview transfer encoding); the text model cannot return image bytes through the log, so portraits are a genuine non-log capability. Pass B: provider transport, bounded responses, and strict decoding are legitimate tool execution, but the file also carries provider-specific preference resolvers, quality/resolution policy tables, preview-runtime overrides, and a forensics entry point that duplicate each other — ADAPT, rescued by the portrait product promise (ledger §3: OPTIONAL, keep only if portraits are a promise): keep one provider call path plus prompt assembly, slim the resolver/preview/forensics sprawl into policy data. |
| `mvp_site/portrait_generator_agent.py` (601 lines) | ADAPT | Pass A: deleting it removes the portrait context bundle (player description, campaign tone, canon hints, appearance slots) that the image prompt is built from, so generated portraits would lose identity continuity with the campaign; a bare log has no image-prompt assembly step. Pass B: assembling a prompt from already-authored player/campaign facts is prompt assembly, which the ledger allows, but `_equipment_summary` and `_campaign_tone` re-derive summaries from state instead of passing authored facts through, and the canon/appearance precedence machinery second-guesses which authored fact wins — ADAPT: keep context assembly, delete the re-derived summaries, and express precedence once in the prompt template text. |
| `mvp_site/portrait_model_compare.py` (194 lines) | DELETE | Pass A: deleting it removes only the debug comparison that generates the same description with two image models in parallel and uploads both as previews; no player flow calls it except a debug route, and the normal single-model portrait path is untouched. Pass B: it is not transport, durable writes, tool execution for a player action, authorization, or bounded capacity — it is the opposite of bounded capacity, doubling image-generation cost per invocation for an operator comparison — DELETE, with its BQ row logging going with it (the §6 logging decision keeps player-path logging, not debug comparison telemetry). |
| `mvp_site/portrait_timing.py` (149 lines) | ADAPT | Pass A: deleting it removes the wall-clock breakdown shown in the portrait console/API, but portraits still generate; only diagnostic visibility is lost, which the model cannot supply but the player does not play through. Pass B: timing is measurement of tool execution, adjacent to the §6 logging decision (KEEP), so it survives in kind — ADAPT: keep the breakdown, deliver it async/batched off the portrait response path, and drop the client-key padding in `portrait_timing_for_client`, which manufactures zero-valued phases the client never measured. |
| `mvp_site/document_generator.py` (1,492 lines) | ADAPT | Pass A: deleting it removes campaign export (PDF/DOCX/TXT/Markdown of the story log); the model can author prose but cannot produce a PDF/DOCX file, so export is a genuine non-log capability. Pass B: rendering stored entries into a document is pure presentation and stays, rescued by the export promise (ledger §3: OPTIONAL, keep only if export is a promise) — ADAPT: keep the four format generators as verbatim renderers of stored structured entries, and delete the prose-mining machinery (`_parse_dice_rolls`, `_convert_presentation_blocks`, choice-key matching, debug-event extraction) that re-derives structure from text the model already authored in structured form. |
| `mvp_site/equipment_display.py` (878 lines) | ADAPT | Pass A: deleting it removes the equipment/inventory summary the player sees when asking "what am I carrying"; the model could answer that question in prose, but a deterministic summary of server-held state is a presentation the log alone does not guarantee. Pass B: extracting and grouping server-authored equipment entries is pure presentation and stays, but `is_equipment_query`/`classify_equipment_query` are client-intent routing the model should own, `_get_backpack_importance`/`_limit_backpack_for_display` silently drop items the player owns (top-3 truncation is a domain-value rewrite, not formatting), and `ensure_equipment_summary_in_narrative` appends server text to model-authored narrative — ADAPT: keep extraction plus unfiltered grouping, delete query routing, importance scoring, truncation, and narrative injection. |

## 2. Phase 1 — shipped `frontend_v1/` files (58)

General rule applied here: a file the page never loads cannot be player-visible,
however good its code is; a file that only presents server/model-authored values
is KEEP; a file that derives a new domain value from those values is ADAPT
(strip the derivation) or DELETE.

| File | Verdict | Justification |
|---|---|---|
| `.gitignore` (251 B) | KEEP | Pass A: deleting it changes nothing the player sees; it only keeps generated files out of version control, which is repository hygiene, not gameplay. Pass B: it touches no domain value and no request path, so there is nothing for ZFC to forbid — KEEP as a non-runtime file. |
| `README.md` (10,212 B) | KEEP | Pass A: deleting it removes developer documentation of the static-assets layout; the player experience is unchanged, and the log cannot document a codebase. Pass B: documentation is not code and rewrites no domain value — KEEP, noting it is already partly stale (it describes a `static/` layout the current tree does not use) and should be corrected when the directory is next touched, not as a separate task. |
| `api.js` (566 lines) | KEEP | Pass A: deleting it breaks every authenticated API call from the client — clock-skew compensation, backend health checks, and online/offline status all ride on it, so the client could not reach the log at all. Pass B: it is pure transport (fetch wrapper, auth headers, network status), with no domain computation beyond compensating clock skew for token expiry — KEEP. |
| `app.js` (10,667 lines, 438 KB) | ADAPT | Pass A: deleting it deletes the game itself on the client — dashboard, campaign list, story rendering, composer, choices, downloads, quota banner, and turn locking all live in this one DOMContentLoaded closure. Pass B: the bulk is transport plus pure presentation of server state and therefore stays in kind, but a 438 KB monolith that also embeds first-turn coaching, reading-anchor restoration, debug-tools eligibility, and BYOK/settings loading has absorbed other modules' jobs — ADAPT: decompose by subsystem (dashboard, reader, composer, settings loader) without changing behaviour, and move debug-only eligibility out of the shipped bundle. |
| `auth.js` (2,043 lines) | ADAPT | Pass A: deleting it removes sign-in/sign-out, Firebase session handling, waitlist gating, and OpenRouter OAuth finish handling, so no player could establish the identity the server uses to separate logs. Pass B: identity and tenant separation are explicitly allowed server/client categories, so the core stays — ADAPT: slim the duplicated OpenRouter finish/welcome flows, the iOS-persistence workarounds, and the test-mode bypass surface into one auth path, since three ways to finish the same sign-in is the size scandal, not the existence of auth. |
| `campaign-click-fix.css` (1,191 B) | KEEP | Pass A: deleting it risks campaign list items becoming unclickable (its stated purpose, and it is linked from `index.html`); the player-visible effect is that the dashboard works. Pass B: CSS positioning/pointer rules present existing elements and rewrite no domain value — KEEP. |
| `css/avatar.css` (22,958 B) | KEEP | Pass A: deleting it unstyles avatar display, cropping, and portrait panels; portraits still exist, but their presentation breaks. Pass B: pure presentation of image state — KEEP. |
| `css/inline-editor.css` (5,310 B) | KEEP | Pass A: deleting it unstyles the inline story editor; editing still functions, but the affordance degrades. Pass B: pure presentation — KEEP. |
| `css/pagination-styles.css` (2,020 B) | KEEP | Pass A: deleting it unstyles story pagination controls, making long stories harder to navigate. Pass B: pure presentation of the stored log — KEEP. |
| `css/tooltip-guide.css` (2,252 B) | KEEP | Pass A: deleting it unstyles the onboarding tooltip guide; guidance still exists, but unreadably. Pass B: pure presentation — KEEP. |
| `diag-boot.js` (37 lines) | KEEP | Pass A: deleting it loses only the earliest page-load telemetry events (boot, DOMContentLoaded, load) that occur before `diagnostics.js` loads; the game still plays. Pass B: it is client logging, rescued by the §6 logging decision (KEEP), and it never touches domain values — KEEP as-is, noting it already queues rather than blocks. |
| `diagnostics.js` (435 lines) | KEEP | Pass A: deleting it removes client error/telemetry reporting (beacon + keepalive flush, boot-queue drain, error handlers); the game still plays, but failures become invisible to operators. Pass B: logging is KEEP per §6, and this implementation already uses non-blocking `sendBeacon`/keepalive delivery rather than holding a turn — KEEP, with no async adaptation needed because it is already async. |
| `dragon-favicon.svg` (110 B) | KEEP | Pass A: deleting it removes the tab icon; trivially player-visible, trivially cheap. Pass B: pure brand presentation — KEEP. |
| `images/twin_dragon.png` (2,532,010 B) | ADAPT | Pass A: deleting it alone breaks nothing if the WebP twin is served, since both depict the same brand art and the page can reference one file. Pass B: a 2.5 MB PNG duplicating a 105 KB WebP is bounded-capacity waste, not a domain question — ADAPT: drop the PNG from the served set and serve the WebP only (or prove a client that needs the PNG). |
| `images/twin_dragon.webp` (105,188 B) | KEEP | Pass A: deleting it removes the brand hero art the dashboard shows. Pass B: pure presentation — KEEP. |
| `images/avatars/arion_dragon_knight.png` † (257,559 B) | KEEP | Pass A: deleting it removes the default Dragon Knight premade avatar shown during campaign creation; the wizard could fall back to generated art, but the canonical premade look is a product asset. Pass B: pure presentation of a premade's art — KEEP. |
| `index.html` (44,310 B) | KEEP | Pass A: deleting it deletes the entire client entry point — every script, stylesheet, Firebase SDK, and view container is referenced from here, so there is no game UI without it. Pass B: markup plus script/style references are transport/presentation, not domain logic — KEEP; note the file itself proves which JS is actually shipped (see the DELETE rows: component-enhancer, visual-validator, test-planning, parallel-dual-pass are absent from its script list). |
| `js/animation-helpers.js` (306 lines) | ADAPT | Pass A: deleting it removes animated view transitions, button feedback, and story loading spinners; the app still functions, but transitions become abrupt. Pass B: animation is pure presentation and stays, but `interceptViewSwitching` monkey-patches view switching and `enhanceExistingFunctionality` rewrites existing handlers at runtime, which is behaviour interception, not presentation — ADAPT: keep the animation helpers, delete the interception/patching hooks. |
| `js/avatar-crop.js` (205 lines) | KEEP | Pass A: deleting it removes the pointer-driven crop UI for uploaded avatars, so players could not frame their own portrait image. Pass B: cropping is a pure client-side transform of a player-supplied image, not a campaign-domain fact — KEEP. |
| `js/campaign-wizard.js` (3,598 lines) | ADAPT | Pass A: deleting it removes campaign creation itself (steps, validation, launch, avatar handlers, portrait prefetch, preview editing); without it no new campaign can start from the UI. Pass B: collecting player choices and posting them to the server is transport plus presentation, so the wizard stays in kind, but 3,598 lines embedding premade descriptions, telemetry, scroll-locking, and portrait orchestration has absorbed content and other modules — ADAPT: slim it by moving premade copy to data, telemetry to the logging path, and portrait work to `portrait-ai.js`, keeping only step flow, validation, and the launch POST. |
| `js/component-enhancer.js` (618 lines) | DELETE | Pass A: deleting it breaks nothing the player can observe, because `index.html` never loads it and `app.js` never references it; its ripple effects, card/form/modal enhancements, and mutation-observer re-enhancement currently run nowhere in the shipped page. Pass B: unloaded code is not transport, presentation, or anything else in the running product — it is dead weight that can only confuse a future loader — DELETE from the shipped directory (archive in git history, which already preserves it). |
| `js/ember-bg.js` (193 lines) | KEEP | Pass A: deleting it removes the fantasy-theme ember particle background; the game still plays, minus ambience. Pass B: canvas decoration driven by `Math.random` is presentation only — its randomness is visual noise, not a game roll, and it never feeds a domain value — KEEP. |
| `js/enhanced-search.js` (713 lines) | KEEP | Pass A: deleting it removes dashboard search, filter, and sort over the player's own campaign list, making a large campaign list unnavigable. Pass B: filtering/sorting a list of the player's own campaigns by text and date is presentation of already-authored list state, not a recomputation of any campaign fact — KEEP. |
| `js/inline-editor.js` (393 lines) | KEEP | Pass A: deleting it removes in-place editing of story text, so players could not correct or annotate their own log from the reader. Pass B: editing stored text the player authored, with server acceptance still authoritative, is durable-write presentation, not a domain recomputation — KEEP (the server side must remain the authority on what an edit persists, which is outside this area). |
| `js/interface-manager.js` (182 lines) | KEEP | Pass A: deleting it removes modern/classic mode switching and the feature toggles (animations, enhanced components, interactive features) the settings UI exposes. Pass B: mode and toggle state is client presentation preference persisted in `localStorage`, not campaign-domain state — KEEP. |
| `js/loading-messages.js` (141 lines) | KEEP | Pass A: deleting it removes rotating loading messages during waits; the wait itself is unchanged. Pass B: pure presentation — KEEP. |
| `js/opening_story.js` (392 lines) | KEEP | Pass A: deleting it breaks the opening-story handoff — composer locking, submit sync, and the single streaming run that delivers a campaign's first story beat would race or double-submit. Pass B: turn-path transport and concurrency control (locks, telemetry beacons) are allowed categories, and the file does not author story content — KEEP. |
| `js/outcome-verdict.js` (40 lines) | ADAPT | Pass A: deleting it removes only the Success/Failure/Mixed badge on outcome cards; the story, rolls, and explicit outcome (when the server supplies one) remain. Pass B: the explicit-`player_outcome` branch is pure presentation and stays, but the fallback aggregates roll `success` booleans (excluding saves by regex) to invent a verdict the server never authored — that is exactly the field-aware recomputation Pass B forbids, with no registered exception — ADAPT: keep the badge for explicit outcomes only, delete the roll-aggregation fallback (and its save-detection regex). |
| `js/portrait-ai-ui.js` (174 lines) | KEEP | Pass A: deleting it removes the portrait panel markup, counters, and preview state the portrait modal shows; generation still works, but the player cannot see or apply its result cleanly. Pass B: pure presentation of portrait-generation state — KEEP. |
| `js/portrait-ai.js` (1,337 lines) | ADAPT | Pass A: deleting it removes the portrait AI modal, description suggestion, preview generation, compare UI, and wizard prefetch; portraits fall back to upload/crop only. Pass B: client transport to the portrait endpoints plus presentation stays under the portrait promise, but `composePortraitProseFromAppearance` rebuilds prose from appearance slots when the server suggestion is not displayable, and the suggest-cache/prefetch/warm layers duplicate each other — ADAPT: keep transport plus panel wiring, delete the client-side prose recomposition (the server suggestion or the player's own text is the description), and collapse prefetch to one path. |
| `js/scene-illustration.js` (624 lines) | ADAPT | Pass A: deleting it removes scene-illustration slots, polling, lightbox, and retry UI; stories still stream, but no illustration ever appears. Pass B: polling plus presentation of a server-generated image is tool-execution presentation and stays under the scene-illustration promise, but the prompt-ablation panel, cost/latency formatting, and debug-tool eligibility checks are operator tooling embedded in the player UI — ADAPT: keep slot render/poll/lightbox, move ablation and debug eligibility behind a debug flag or out of the shipped bundle. |
| `js/settings.js` (2,240 lines) | ADAPT | Pass A: deleting it removes the settings page (provider/BYOK keys, OpenRouter linking, scene-illustration toggles, onboarding reset); players could not change provider or key settings from the UI. Pass B: settings transport plus presentation stays, but the file duplicates OpenRouter OAuth link/finish handling already in `auth.js`, and embeds scene-advanced visibility policy — ADAPT: keep one settings load/save path, delete the duplicated OpenRouter link flow (call `auth.js`), and move scene-visibility policy to the server response. |
| `js/streaming.js` (1,625 lines) | ADAPT | Pass A: deleting it removes the streaming client itself — SSE handling, narrative extraction from structured envelopes, planning-block rendering, dice/faction inline display, quota banner updates, and turn-lock release; without it a turn cannot be played. Pass B: streaming transport plus pure extraction/presentation of the server envelope is the core allowed category, and dice/faction inline blocks only display tool results — ADAPT: keep the client, slim the duplicated telemetry/beacon paths and the terminal-outcome inference helpers so the client renders what the server declared rather than inferring completion state from text shapes. |
| `js/test_planning_block_parsing.js` (639 lines) | DELETE | Pass A: deleting it breaks nothing player-visible: it is a self-contained `PlanningBlockTestSuite` (assert/test/run) with HTML-entity and JSON parsing helpers, loaded by neither `index.html` nor `app.js`, and the shipped planning-block parsing already lives in `streaming.js`. Pass B: a test harness shipped inside the product directory is not player transport or presentation, and duplicating the parser it tests is the opposite of slim — DELETE from the shipped directory (its assertions belong in `tests/`, if anywhere). |
| `js/theme-bootstrap.js` (97 lines) | KEEP | Pass A: deleting it removes the early theme decision (fantasy vs default from storage/flags) before first paint, causing a theme flash. Pass B: pure presentation preference — KEEP. |
| `js/theme-manager.js` (133 lines) | KEEP | Pass A: deleting it removes runtime theme switching and persistence. Pass B: pure presentation preference — KEEP. |
| `js/tooltip-guide.js` (559 lines) | ADAPT | Pass A: deleting it removes the onboarding tooltip guide (hydration from server settings, card rendering, positioning, completion tracking); new players lose guided first-run help. Pass B: onboarding presentation plus server-settings hydration stays, but the file carries two hydration paths (server merge plus local completion state) and its own event-flush pipeline duplicating `diagnostics.js` — ADAPT: keep one hydration path and route guide events through the shared diagnostics pipeline. |
| `js/ui-utils.js` (104 lines) | KEEP | Pass A: deleting it breaks wiki/Reddit/Discord link hydration (anchors keep `href="#"`) and collapsible descriptions. Pass B: setting canonical URLs on marked anchors and toggling a CSS class presents existing markup; it rewrites no campaign value — KEEP. |
| `js/visual-validator.js` (424 lines) | DELETE | Pass A: deleting it breaks nothing player-visible: it is a layout QA tool (overlap detection, contrast ratios, checkbox alignment, spinner checks) loaded by neither `index.html` nor `app.js`, and its `run`/`captureState` entry points have no shipped caller. Pass B: developer QA tooling is not player transport or presentation — DELETE from the shipped directory (keep, if wanted, under `tests/` or tooling, not the served bundle). |
| `js/worldai-mcp-bridge.js` (90 lines) | KEEP | Pass A: deleting it removes the client's MCP tool calls for tooltip events and user settings, which the tooltip guide depends on. Pass B: it is a thin transport shim to server tools, authoring no domain fact itself — KEEP. |
| `loading-messages.css` (2,832 B) | KEEP | Pass A: deleting it unstyles loading messages. Pass B: pure presentation — KEEP. |
| `mocks/mock_header_avatar_and_scroll_gate.html` † (14,357 B) | DELETE | Pass A: deleting it removes a standalone development mock of a header avatar and scroll gate; no shipped page links to it and the real header ships in `index.html`/`app.js`. Pass B: a mock is not player transport or presentation in the running product — DELETE from the shipped directory (its assertions, if any remain valuable, live in `tests/`). |
| `parallel_dual_pass.css` (1,373 B) | DELETE | Pass A: deleting it removes styles for an enhancement indicator that no shipped page renders, because its JS companion is never loaded (see next row). Pass B: unreferenced presentation is not presentation — DELETE with its JS companion. |
| `parallel_dual_pass.js` (220 lines) | DELETE | Pass A: deleting it breaks nothing the player can observe: `index.html` never loads it, `app.js` never calls `handleInteractionParallel`, and the shipped turn path runs through `streaming.js`; the only in-repo references found are the file itself and a historical integration doc outside this area. Pass B: a second, parallel turn-submission path that posts to `/api/campaigns/<id>/interaction` and then swaps in a background "enhancement" is both dead and, if ever wired up, a second author of story entries competing with the streaming path — DELETE rather than revive. |
| `quick_start_shared.js` (216 lines) | KEEP | Pass A: deleting it breaks quick-start banner dismissal, dashboard URL building, and new-campaign scroll targeting shared by the dashboard and wizard. Pass B: URL building and banner state are navigation/presentation, not domain logic — KEEP. |
| `style.css` (90,732 B) | KEEP | Pass A: deleting it unstyles essentially the whole application. Pass B: pure presentation — KEEP (size is a bundling/minification question, not a ZFC question). |
| `styles/animations.css` (8,958 B) | KEEP | Pass A: deleting it removes keyframe/animation definitions used across views. Pass B: pure presentation — KEEP. |
| `styles/bridge.css` (916 B) | KEEP | Pass A: deleting it removes the small compatibility shim between style generations. Pass B: pure presentation — KEEP. |
| `styles/components.css` (13,002 B) | KEEP | Pass A: deleting it unstyles shared components. Pass B: pure presentation — KEEP. |
| `styles/enhanced-components.css` (15,705 B) | KEEP | Pass A: deleting it unstyles enhanced components. Pass B: pure presentation — KEEP. |
| `styles/globals.css` (6,313 B) | KEEP | Pass A: deleting it removes global tokens/base rules other sheets depend on. Pass B: pure presentation — KEEP. |
| `styles/interactive-features.css` (21,686 B) | KEEP | Pass A: deleting it unstyles interactive features. Pass B: pure presentation — KEEP. |
| `styles/planning-blocks.css` (26,879 B) | KEEP | Pass A: deleting it unstyles planning/thinking blocks rendered during streaming. Pass B: pure presentation of server-authored planning content — KEEP. |
| `terms-of-use.html` (8,140 B) | KEEP | Pass A: deleting it removes the legal terms page players can open. Pass B: static legal presentation, no domain logic — KEEP. |
| `themes/base.css` (2,250 B) | KEEP | Pass A: deleting it removes base theme tokens. Pass B: pure presentation — KEEP. |
| `themes/default.css` (3,970 B) | KEEP | Pass A: deleting it removes the default theme. Pass B: pure presentation — KEEP. |
| `themes/fantasy.css` (33,679 B) | KEEP | Pass A: deleting it removes the fantasy theme players can select. Pass B: pure presentation — KEEP. |
| `user_lifecycle.js` (592 lines) | ADAPT | Pass A: deleting it removes anonymous visitor/session identity, screen-view and onboarding telemetry, and auth-linking of that identity; pre-auth analytics and session continuity go dark. Pass B: identity for a session is an allowed category and telemetry is KEEP per §6, but the file also collects acquisition/source fields and maintains its own storage/rotation scheme alongside Firebase auth — ADAPT: keep visitor/session identity and auth linking, deliver events through the shared async diagnostics pipeline, and drop acquisition-source collection that no product decision in this area justifies. |

## 3. Phase 1 — `frontend_v1/tests/` and test-support files † (134 files, clustered)

These files are not shipped player code (the ledger defers the test-share question
to a later pass), so the Phase 1 verdict here is about the test's own standing:
KEEP means the test guards shipped behaviour and stays with its subject;
ADAPT means the test must change when its subject changes (named below);
DELETE would mean the test guards nothing shipped. No test file was individually
fetched; verdicts rest on file names, sizes, and subjects, and §6 records
individual test-function audit as untouched. Cluster file counts sum to 134
(122 test files + 4 helpers + 1 fixture + 7 repro files).

| Cluster (files) | Verdict | Justification |
|---|---|---|
| Auth & access (11): `auth_domain_resolution`, `auth_ios_persistence`, `auth_mobile_redirect`, `fetchapi_public_optin`, `no_campaign_redirect`, `redirect_param_allowlist`, `openrouter_byok_cta`, `openrouter_finish_states`, `openrouter_oauth`, `openrouter_status_contrast`, `waitlist_access` | KEEP | Pass A: deleting these removes the only automated guard on sign-in, redirect allowlists, waitlist gating, and OpenRouter finish states; a regression there locks players out, which is player-visible even though the tests themselves never ship. Pass B: tests author no domain value and their subjects are allowed identity/transport categories — KEEP with their subjects (noting `settings.js`/`auth.js` ADAPT work must update the OpenRouter tests, not delete them). |
| Campaign wizard (13): `campaign_create_nav_before_avatar`, `campaign_wizard_ai_avatar_size`, `campaign_wizard_avatar_launch`, `campaign_wizard_default_order`, `campaign_wizard_dragon_knight_canonical`, `campaign_wizard_dragon_knight_submit`, `campaign_wizard_scroll_indicator`, `campaign_wizard_step2_no_duplicate_enter`, `campaign_wizard_url_prefill_race`, `test_ip_tv_show_wizard`, `test_wizard_setting_visible_on_dragon_knight`, `test_quick_start_wizard_click_8ce37`, `share_token_prefill_ip_wizard_9727` | KEEP | Pass A: deleting these removes guards on the only campaign-creation path, including canonical premade submission and URL-prefill races that previously corrupted launches. Pass B: they guard transport/presentation behaviour, not domain facts — KEEP, with wizard ADAPT work (premade copy to data) updating the canonical/dragon-knight tests rather than removing them. |
| Story rendering & streaming (16): `narrative_markdown_render`, `narrative_prose_layout`, `narrative_streaming_blocks`, `narrative_streaming_handoff`, `streaming_extraction`, `streaming_paragraph_stability`, `streaming_beacon_auth`, `streaming_completion_phantom_dice_roll`, `streaming_error_surfacing`, `streaming_telemetry_boundary`, `story_pagination_identity_race`, `keep_reading_scroll_only`, `submit_expand_scroll_bugs`, `test_resume_campaign_stream_race`, `turn_lock_until_server_turn_ends`, `interaction_draft_persistence` | KEEP | Pass A: deleting these removes guards on the turn path itself — extraction, streaming handoff, turn locking, and draft persistence are exactly where a regression strands a player mid-turn. Pass B: they guard transport and pure presentation of server envelopes — KEEP, and the phantom-dice-roll test is evidence the streaming client must not invent rolls, which supports the §5 streaming ADAPT. |
| Choices & composer (14): `choice_detail_inline`, `choice_token_story_display`, `composer_bounded_correction`, `composer_choices_mobile_cap`, `desktop_choice_shortcuts`, `latest_turn_choices_inline`, `mode_switch_hide_choices_and_wrap`, `mode_tooltips_and_hints`, `planning_block_text_size`, `planning_choices_composer`, `planning_choices_composer_workflow_contract`, `planning_composer_dom`, `play_screen_overlap_contracts`, `turn_mode_label` | KEEP | Pass A: deleting these removes guards on choice display, composer behaviour, and planning-block composition, which are the player's primary actions each turn. Pass B: they guard presentation of server-authored choices, not the choices' content — KEEP. |
| Opening story & first turn (7): `opening_story`, `opening_story_avatar_persist_race`, `opening_story_resume`, `first_turn_coach`, `first_turn_coach_auth_race`, `quick_start_auto_redirect`, `test_quick_start_resume_scroll_0vsxl` | KEEP | Pass A: deleting these removes guards on campaign start and resume, where a race loses the opening beat or the avatar the player just chose. Pass B: they guard transport/concurrency, not domain authorship — KEEP. |
| Quick start & dashboard (10): `quick_start_banner_reshow_symmetry`, `quick_start_button`, `quick_start_dashboard_param_preservation`, `quick_start_shared_helpers`, `quickstart_url_capu1`, `test_quick_start_banner_dismiss_pycqp`, `test_quick_start_scroll_ectdj`, `client_asset_load_failed`, `quota_banner`, `review_save_failed_request_id` | KEEP | Pass A: deleting these removes guards on quick-start navigation, banner state, and failure surfacing (quota, failed saves) that players hit on the dashboard. Pass B: they guard navigation/presentation and error transport — KEEP. |
| Portrait AI (14): `portrait_ai_auto_suggest`, `portrait_ai_compare_models`, `portrait_ai_first_open`, `portrait_ai_first_open_segment`, `portrait_ai_loading`, `portrait_ai_modal_reset`, `portrait_ai_nodelist_segment`, `portrait_ai_panel_suppression`, `portrait_ai_refresh_suggest`, `portrait_ai_suggest_timeout`, `portrait_ai_use_preview`, `portrait_ai_wizard_prefetch_dedupe`, `portrait_default_and_display_scale`, `avatar_crop_zone_overflow` | KEEP | Pass A: deleting these removes guards on the portrait modal, suggestion caching, and preview application; a regression there breaks the portrait promise's UI. Pass B: they guard presentation/transport of image state — KEEP, except the compare-models test follows its subject: if `portrait_model_compare.py` is deleted, that test goes with it (see ADAPT note below, counted separately in the totals as part of this cluster's KEEP-with-subject rule rather than double-counted). |
| Settings, scene, stats (10): `scene_illustration_poll`, `scene_illustration_ui`, `scene_settings_admin_visibility`, `settings_indicators_migration`, `settings_listeners`, `stats_features_rendering`, `rewards_box_level_up_banner_rendering`, `spicy_header_indicator`, `system_notice_theme_tokens`, `timer_info_debug_only` | KEEP | Pass A: deleting these removes guards on settings persistence, scene-illustration polling, and HUD/level-up banner rendering. Pass B: they guard presentation and settings transport — KEEP; the level-up banner test guards display of a server-declared level-up, not a client computation of one, which is why it survives while outcome-verdict's fallback does not. |
| Editor, tooltip, misc UI (23): `inline_editor_comment_accuracy`, `inline_editor_mobile_width`, `test_inline_editor_no_duplicate`, `inline_play_completion_gaps`, `collapsible_debug_panels_dom`, `debug_mode_implicit_cache`, `debug_mode_initial_load`, `default_gemini_fallback`, `header_avatar_mount`, `header_hud_layout`, `hud_menu_mobile_qa`, `keyboard_inset`, `test_mobile_input_focus_collapses_choices.cjs`, `tooltip_guide_bootstrap`, `test_tooltip_guide_e2e.js`, `test_tooltip_guide_unit.js`, `diagnostics.test.js`, `instrumentation.test.js`, `user_lifecycle_telemetry.test.js`, `undo_story_idtoken.test.js`, `test_campaign_export_ui.test.js`, `test_issue_9498_long_prompt_keepalive.test.js` | KEEP | Pass A: deleting these removes guards on editing, tooltips, HUD layout, diagnostics, telemetry, undo, and export UI — all player-visible surfaces. Pass B: they guard presentation, logging (KEEP per §6), and transport — KEEP. |
| Mock-structure tests (3): `desktop_mock_structure`, `phone_mock_structure`, `desktop_room` | ADAPT | Pass A: deleting these removes structural guards on mock phone/desktop rooms, which are not the shipped `index.html` page; their player value is indirect (they guard design fixtures). Pass B: mocks are presentation fixtures, not the product, so the tests survive only if their mock targets are still real fixtures — ADAPT: confirm each mock target exists and is still referenced, otherwise DELETE the test with its mock instead of keeping a guard on a ghost. |
| Outcome verdict test (1): `outcome_verdict.test.js` | ADAPT | Pass A: deleting it removes the guard on the outcome badge, which is still a shipped display. Pass B: the test currently guards the fallback aggregation that §2/§5 verdict DELETE, so the test cannot stay as written — ADAPT: rewrite it to explicit-outcome-only cases and delete the roll-aggregation cases with the fallback. |
| Test support (12): `helpers/extract_fn.js`, `helpers/jsdom_loader.js`, `helpers/narrative_helpers.js`, `helpers/streaming_test_harness.js`, `fixtures/streamed_social_turn_chunks.json`, repro `.gitignore`, repro `README.md`, repro `emu_app.html`, repro `emu_e2e.mjs`, repro `firebase.json`, repro `proxy_server.mjs`, repro `run_repro.mjs` | KEEP | Pass A: deleting these removes the harness the test clusters run on (jsdom loading, streaming harness, social-turn fixture) and the mobile-auth emulator repro, which reproduces a real sign-in failure class. Pass B: harness and repro tooling author no domain value and never ship to players — KEEP as tooling (the repro's `device_evidence/` and `screenshots/` subdirectories were listed as directories only and are not individually verdict-ed; see §6). |

Cluster-count reconciliation: 11 + 13 + 16 + 14 + 7 + 10 + 14 + 10 + 23 + 3 + 1 + 12 = 134, matching 122 test files + 4 helpers + 1 fixture + 7 repro files.

## 4. Phase 2 — Python, every function/symbol

Verdict key: KEEP = stays as written; ADAPT = needed in kind, change named;
DELETE = remove. Each row covers Pass A then Pass B in 2–4 sentences and ends
in the verdict. Constant groups are verdict-ed as groups where they are a single
policy table; individually named constants that are pure status strings are
grouped with their function.

### 4.1 `frontend_cutover_flag.py` — ADAPT (deploy-time only)

- `FLAG_DOC_ID` ("config/frontend_cutover"), `DocumentReader` type, `_document_reader` global: Pass A: without the doc id and reader slot the flag cannot be read at all, so cutover gating collapses to OFF. Pass B: this is deployment configuration, not a campaign fact, and the injectable-reader design keeps Firestore out of the module — KEEP as the flag contract.
- `set_document_reader` / `reset_document_reader`: Pass A: deleting them removes the only way to install or clear the reader, so tests and server wiring cannot exercise or shut off the flag. Pass B: pure wiring with no domain logic — KEEP.
- `read_flag(env)`: Pass A: deleting it removes the flag decision itself, leaving the selector blind. Pass B: it validates shape (`enabled` bool, `envs` list) and fails closed to None/OFF without inventing a policy — validation of a config document, not a domain transform — KEEP.
- Status constants (`STATUS_DISABLED_*`, `STATUS_READER_INSTALLED`) + `STARTUP_FLAG_READ_TIMEOUT_SECONDS` (2.0): Pass A: deleting them removes the diagnosable startup states and the bound that stops a slow Firestore read from killing a Cloud Run revision at probe deadline. Pass B: bounded capacity and diagnosability for deployment wiring — KEEP.
- `firestore_reader(client, timeout)` (+ inner `_read`): Pass A: deleting it removes the only production reader, so the flag could never be ON in a real deployment. Pass B: it is a bounded, non-retrying durable read with fail-closed semantics — KEEP, with the file-level ADAPT that it must not be called on the turn path.
- `initialize_server_flag(environ, client_factory)`: Pass A: deleting it removes startup wiring, so the reader is never installed and cutover never activates. Pass B: it checks environment identity first (absent/stable/unknown all refuse before constructing a client) and never raises — deployment authorization in the right order — KEEP.

### 4.2 `frontend_preview_release.py` — DELETE (whole file; rows show why no part rescues it)

- `PreviewReleaseError`: Pass A: deleting it only removes the error type for a preview contract nobody in the player path raises. Pass B: an exception type for release scaffolding is not a gameplay category — DELETE with the file.
- `_digest(path)`: Pass A: deleting it removes SHA-256 digests used to verify overlay bytes; no player capability depends on overlay verification. Pass B: integrity checking of a one-off preview artifact is deploy tooling, not player transport — DELETE with the file.
- `preview_manifest_path(environ, repo_root)`: Pass A: deleting it makes the preview overlay inert (returns None today when no receipt exists, which is the shipped default); players lose nothing. Pass B: it enforces a single-PR, single-environment receipt contract — release process, not a product promise — DELETE with the file.
- `_receipt_frontend`, `_verify_inventory`, `_verified_manifest`: Pass A: deleting them removes receipt schema, inventory, and manifest binding checks for that same one-off overlay; the normal manifest path in `frontend_release.py` is unaffected. Pass B: they are deploy-time verification for a preview that has served its purpose, and the hardcoded PR 10571 / service regex proves they were never meant as durable product logic — DELETE with the file.
- `_PreviewFlagSnapshot.to_dict`, `_PreviewFlagClient.document/get`, `create_preview_flag_client`: Pass A: deleting them removes the synthetic flag source that pretends the preview flag is ON; without the verified receipt it already refuses. Pass B: a synthetic identity source for a preview environment is test/deploy scaffolding, not player authorization — DELETE with the file.

### 4.3 `frontend_release.py` — ADAPT (selector stays; deploy-time checks move out)

- `SCHEMA_VERSION`, `REPO_ROOT`, `DEFAULT_MANIFEST_PATH`, `VALID_SURFACES`, `DEFAULT_SURFACE`: Pass A: deleting them removes the manifest contract and default surface the selector needs to serve anything. Pass B: serving configuration, not domain state — KEEP.
- `LOAD_OK/LOAD_MISSING/LOAD_INVALID`, `REASON_*` (v1 default/missing/invalid, surface disabled, artifact missing/incomplete, Expo selected, enabled-release invalid), `is_refusal_reason`: Pass A: deleting them removes the fail-closed refusal vocabulary that stops the server silently falling back to the wrong frontend. Pass B: refusing to serve rather than serving the wrong UI is transport safety — KEEP.
- `ENV_STABLE`, `CUTOVER_ENVS`, `ENV_IDENTITY_VAR`, `deployment_env`, `resolve_cutover_enabled`: Pass A: deleting them removes deployment-identity detection and the cutover decision, so preview/stable routing collapses. Pass B: environment identity is deployment authorization, and stable-exclusion is a safety policy for the cutover, not a campaign rule — KEEP.
- `select_frontend_dir_for_deployment`, `select_frontend_dir`: Pass A: deleting them removes the serving decision itself — no directory, no UI. Pass B: pure transport selection — KEEP, with the file-level ADAPT that digest/inventory validation (below) should not run per request.
- `LEGACY_*` constants, `legacy_asset_relative_path`, `rewrite_legacy_asset_urls`, `resolve_legacy_request`, `legacy_serving_target`: Pass A: deleting them breaks old `frontend_v1/` asset URLs that existing clients and bookmarks still request, so legacy players would get 404s for assets. Pass B: URL rewriting for backward compatibility is transport — KEEP while legacy URLs are still served, then DELETE as a set when legacy serving ends.
- `LEGACY_REQUIRED_RUNTIME_ASSETS`, `EXPO_STATIC_ROOT`, `_required_runtime_assets`: Pass A: deleting them removes the runtime-asset inventory a release must contain to be servable. Pass B: serving inventory is transport, but it is a deploy-time invariant, not a per-request computation — ADAPT: evaluate at release packaging time, not on every selection.
- `REASON_FLAG_*` constants: Pass A: deleting them removes the flag-specific refusal reasons that distinguish env-absent/unknown/stable-excluded from a plain disabled flag. Pass B: diagnosable transport refusal — KEEP.
- `_manifest_shape_is_valid`, `load_manifest`: Pass A: deleting them removes manifest loading/validation, so a malformed manifest could select a broken release. Pass B: manifest validation is transport safety and fails closed without raising — KEEP (at deploy/selection time, not per turn).
- `_resolve_artifact_dir`, `_index_sha256`, `_artifact_tree_digest`, `_artifact_tree_digest_or_none`: Pass A: deleting them removes whole-artifact binding (not just `index.html`), so a partially corrupted release could serve. Pass B: integrity is transport safety, but hashing a whole tree per selection is bounded-capacity waste on the request path — ADAPT: compute once at packaging and verify the stored digest at selection.
- `_FrontendAssetParser.__init__/handle_starttag`, `_referenced_assets_exist`, `_validate_runtime_assets`, `_validate_release`: Pass A: deleting them removes the check that every asset `index.html` references actually exists in the release, so a release missing a JS bundle could be selected. Pass B: this is deploy-time release validation, not gameplay, and parsing HTML per selection repeats deploy work — ADAPT: run at packaging/CI time and keep only the cached pass/fail at selection.

### 4.4 `avatar_image_gen.py` — ADAPT (one provider path; slim resolvers/preview/forensics)

- Error constants (`ERROR_PROVEN_BEFORE_SEND`, `ERROR_RATE_LIMITED`, `ERROR_AUTH_CONFIG`, `ERROR_POLICY_REJECTED`, `ERROR_INVALID_RESPONSE`, `ERROR_OUTCOME_UNKNOWN`, `FAILURE_PROVIDER_REJECTED`), `_MAX_PIXELS`, `_JSON_OVERHEAD_BYTES`, `PROVIDER_ERROR_LOG_MAX_CHARS`, `bounded_provider_error_text`: Pass A: deleting them removes the bounded, never-silently-truncated provider error reporting the portrait path uses to fail diagnosably. Pass B: bounded logging of tool execution is allowed, and capping error text is bounded capacity — KEEP.
- `GeneratedImage` (dataclass), `PortraitGenerationError.__init__`: Pass A: deleting them removes the image result/error contract every portrait caller depends on (bytes, provider, model, dimensions, cost, hash). Pass B: a tool-result contract is transport, not a domain fact — KEEP.
- `load_portrait_policy`, `load_portrait_style`, `load_portrait_request_guard`, `load_portrait_player_precedence`, `_PROMPTS_DIR`, `_STYLE_PATH`, `_GUARD_PATH`, `_POLICY_PATH`: Pass A: deleting them removes the policy/style/guard template files the prompt is built from, so prompt assembly has no template. Pass B: prompt templates are data, and loading them is prompt assembly — KEEP.
- `_portrait_slot_values`, `_clamp_portrait_slot_values`, `_SLOT_PATTERN`, `_UNSPECIFIED_SLOT`, `_APPEARANCE_SLOT_REFERENCE`: Pass A: deleting them removes slot extraction/clamping from appearance text, so the template cannot be filled. Pass B: filling a template from player-authored appearance text is prompt assembly, and clamping to policy length is bounded capacity — KEEP.
- `_render_portrait_prompt_from_values`, `build_portrait_prompt`: Pass A: deleting them removes portrait prompt construction itself (brief + guard + precedence + canon, with fallbacks that shed context, then canon, then trim the description). Pass B: prompt assembly from authored facts is allowed, and the fallback order (player brief first, canon last) correctly refuses to invent appearance — KEEP, noting the fallback chain is the file's most valuable logic and must survive any slimming.
- `_bounded_response_bytes`, `_strict_decode_image`, `_decode_portrait_provider_image`: Pass A: deleting them removes bounded, strict decoding of provider image payloads, so malformed provider output could crash or bloat the portrait path. Pass B: strict decoding of a tool result is transport safety and bounded capacity — KEEP.
- `_openrouter_response_header_summary`, `_log_openrouter_exchange_stages`, `_emit_portrait_image_bq_log`: Pass A: deleting them removes provider-exchange diagnostics and BQ portrait logging; portraits still generate. Pass B: logging is KEEP per §6, but exchange-stage logging on the generation path must not hold the response — ADAPT: keep, deliver async/batched.
- `build_openrouter_image_provider_preferences`, `resolve_openrouter_image_quality`, `resolve_openrouter_image_resolution`, `effective_openrouter_image_model`, `openrouter_provider_prefs_for_model`, `openrouter_image_payload`, `_OPENROUTER_GROK_RESOLUTIONS`: Pass A: deleting them removes OpenRouter routing/quality/resolution/payload construction, so OpenRouter generation cannot be formed. Pass B: provider payload construction is tool execution, but six resolvers for one provider's quirks (Grok low/medium quality, 2K, xAI pinning) is provider-specific sprawl — ADAPT: collapse into one provider-payload builder driven by policy data, keeping the payload contract testable.
- `is_portrait_preview_runtime`, `resolve_portrait_image_provider_preference`, `_is_preview_environment`, `_preview_allows_provider_override`, `_resolve_preview_default_provider_pref`, `_PORTRAIT_PREVIEW_SERVICE`: Pass A: deleting them removes preview-runtime provider defaulting; production generation is unaffected. Pass B: preview-only routing is deploy/environment behaviour, not player gameplay, and a second override layer invites preview/prod divergence — ADAPT: keep only if preview deployments still exist, otherwise DELETE this group as a set, keeping the explicit client preference path.
- `_validate_static_png_passthrough`, `_normalize_static_png`, `portrait_image_dimensions`, `encode_portrait_preview_transfer`: Pass A: deleting them removes static-PNG validation/normalization and preview-transfer encoding, so uploaded/static portraits cannot be safely served as previews. Pass B: image validation and bounded encoding (downscale only when policy allows) are tool-execution safety — KEEP.
- `_new_session`, `_shared_portrait_http_session`, `warm_portrait_image_transport`, `_provider_http_timeouts`: Pass A: deleting them removes TLS session reuse and warmup, so each generation pays full handshake cost. Pass B: connection reuse and timeouts are transport and bounded capacity — KEEP.
- `_portrait_error_is_retryable`, `_http_error_kind`, `_finalize_generated`: Pass A: deleting them removes retry classification and result finalization (hash, dimensions, cost), so failures could retry wrongly or succeed without a verifiable result. Pass B: retry policy for tool execution plus result attestation is allowed transport/tool logic — KEEP.
- `_post_image_request`, `generate_image_openrouter`, `generate_image_xai`, `generate_image`: Pass A: deleting them removes portrait generation itself via OpenRouter, direct xAI, and the dispatcher between them. Pass B: these are the tool-execution core under the portrait promise — KEEP in kind, with the ADAPT that two full provider implementations should collapse to one provider abstraction if one provider is dropped (a product decision, not this audit's).
- `capture_openrouter_image_forensics`, `time_direct_openrouter_minimal`: Pass A: deleting them removes diagnosis-only direct POSTs that bypass the normal path; no player flow needs them. Pass B: forensics/diagnosis tooling is not player tool execution — DELETE both (their logic duplicates `_post_image_request` and can be reproduced from its logs).
- `_merge_image_timing`: Pass A: deleting it removes timing merging for the portrait response; generation itself is unaffected. Pass B: timing measurement is logging-adjacent (KEEP per §6) — ADAPT: keep, but merge once and deliver with the async logging path, not inline in the generation response.

### 4.5 `portrait_generator_agent.py` — ADAPT (keep assembly; delete re-derived summaries)

- `PortraitContextBundle`, `PortraitAppearanceSlots`, `PortraitCanonHints` (dataclasses): Pass A: deleting them removes the typed context/appearance/canon contracts the portrait pipeline passes around. Pass B: data contracts for prompt assembly, not domain decisions — KEEP.
- `_REDACT_PATTERNS`, `redact_portrait_prompt_for_log`, `log_assembled_portrait_prompt`: Pass A: deleting them removes redacted logging of the assembled prompt; portraits still generate. Pass B: logging is KEEP per §6, and redaction before logging is privacy-safe transport — KEEP, delivered async per the file-level logging rule.
- `load_portrait_canon_franchise_guidance`, `_CANON_PROMPTS_DIR`, `_coerce_franchise_flag`, `portrait_canon_from_mapping`, `portrait_canon_to_api_dict`, `build_portrait_canon_guidance_block`, `canon_hints_for_actor_retry`: Pass A: deleting them removes franchise-canon guidance (e.g. IP-specific cues) from portrait prompts, so IP portraits lose canon fidelity. Pass B: passing authored canon cues through to a prompt is prompt assembly, and serializing them intact (not rewriting them) is the right shape — KEEP, with precedence owned by the prompt text, not by code ordering tricks.
- `appearance_subordinate_to_player_description`: Pass A: deleting it removes the rule that drops appearance slots tied to a different brief than the player's description, so stale slots could override the player's own words. Pass B: this is a precedence decision, and precedence belongs in the prompt/template (as `avatar_image_gen` already states), not in a code filter that silently drops authored slots — ADAPT: move the rule into the prompt template text and delete the code filter.
- `portrait_appearance_from_mapping`, `portrait_appearance_to_api_dict`: Pass A: deleting them removes appearance mapping to/from API dicts, breaking the portrait suggestion round-trip. Pass B: pure data mapping with no value invention — KEEP.
- `_scalar_pc_fields`, `_equipment_summary`, `_campaign_tone`: Pass A: deleting them removes the scalar-field extraction, equipment summary, and tone derivation fed into portrait context; the prompt would lose campaign flavour. Pass B: scalar extraction is pass-through, but `_equipment_summary` and `_campaign_tone` re-derive summaries from state instead of passing authored facts, which is exactly the server-side recomputation Pass B forbids without a registered exception — ADAPT: keep `_scalar_pc_fields`, DELETE `_equipment_summary` and `_campaign_tone` as code (their content, if wanted, is the model's job in the brief, or a stored authored field).
- `assemble_wizard_portrait_context`, `build_campaign_portrait_context_dict`, `load_campaign_portrait_records`, `assemble_campaign_portrait_context`, `assemble_portrait_context`, `assemble_portrait_context_for_campaign_id`: Pass A: deleting them removes portrait context assembly for the wizard and for existing campaigns, so prompts would be built from the description alone. Pass B: assembling already-authored facts into a prompt context is prompt assembly — KEEP, slimmed to one assembly entry point if the six wrappers prove to be thin aliases (verify callers before collapsing).
- `truncate_context_json`, `_cap_portrait_text`, `compact_context_for_suggest`, `compact_context_for_image_prompt`: Pass A: deleting them removes the caps that keep wizard IP descriptions (10k+ chars) from blowing up suggest/image prompts. Pass B: truncation for bounded capacity is allowed, provided it truncates rather than rewrites — KEEP, noting `compact_context_for_image_prompt`'s field-dropping must drop only duplicated fields, never the player's brief.
- `build_portrait_image_prompt`: Pass A: deleting it removes the final image-prompt construction from context, so no portrait can be requested. Pass B: prompt assembly under the portrait promise — KEEP.

### 4.6 `portrait_model_compare.py` — DELETE (whole file)

- `COMPARE_MODELS`, `COMPARE_RESOLUTION` ("2K"): Pass A: deleting them removes the two-model list and fixed resolution the comparison runs at; no player flow references them. Pass B: comparison configuration for a debug tool is not a gameplay category — DELETE with the file.
- `_log_compare_row`: Pass A: deleting it removes the BQ row linking a compare image to model/cost/latency/preview URL; the comparison itself would still run, just unlogged. Pass B: debug telemetry for a debug tool does not inherit the §6 player-path logging decision — DELETE with the file.
- `_one_model`: Pass A: deleting it removes one model's generation+upload+log step; the comparison collapses. Pass B: it is a debug harness around the real generation path, not a player action — DELETE with the file.
- `compare_portrait_models`: Pass A: deleting it removes parallel two-model generation that never persists (previews only, saved portrait untouched until the user applies one); the normal portrait path is untouched. Pass B: doubling bounded capacity for an operator comparison is the opposite of the capacity category — DELETE with the file.

### 4.7 `portrait_timing.py` — ADAPT (async delivery; drop manufactured zero phases)

- `_PROVIDER_DETAIL_PHASES`, `_SERVER_PHASES`, `_CLIENT_TIMING_KEYS`: Pass A: deleting them removes the phase vocabularies the breakdown sums and pads with; timing would be an unstructured bag. Pass B: measurement vocabularies are logging data, not domain facts — KEEP as data.
- `PortraitTimingBreakdown.start/stop/snapshot_phases/to_dict`: Pass A: deleting them removes wall-clock measurement itself; portraits still generate, but no phase can be timed. Pass B: measuring tool execution is logging-adjacent (KEEP per §6) and `stop` correctly ignores unstopped phases rather than inventing them — KEEP, with delivery async per the file verdict.
- `_provider_image_ms`, `_total_ms_disjoint`: Pass A: deleting them removes the sums that produce `provider_image_ms` and the disjoint total (preferring server wall time, else provider wall + server phases, else detail + server phases). Pass B: summing measured phases without double-counting `total_ms` is arithmetic over measurements, not a domain recomputation — KEEP.
- `merge_timing_phases_for_api`: Pass A: deleting it removes the merge that combines phase maps while skipping `total_ms`/`provider_image_ms` and None values, so API timing would double-count or drop phases. Pass B: merging measurements without double-counting is logging hygiene — KEEP.
- `portrait_timing_for_client`: Pass A: deleting it removes the client-facing timing dict (merged phases plus padded standard keys and wall-time fallback) that the live console renders. Pass B: padding unmeasured keys with 0.0 manufactures phases the client never measured, which is display formatting inventing data — ADAPT: keep the merge, DELETE the zero-padding (the console should render absent phases as absent).

### 4.8 `document_generator.py` — ADAPT (verbatim renderers stay; prose-mining goes)

- `MAX_PLANNING_BLOCKS`, `_normalize_text`: Pass A: deleting them removes the planning-block cap and the HTML-entity/whitespace normalization used for comparison; exports still generate, but comparisons could mismatch on entities. Pass B: normalization for comparison is formatting, not a domain rewrite — KEEP, with the cap kept as bounded capacity.
- `_format_background_event`, `_format_debug_events`: Pass A: deleting them removes background-event and debug-event formatting from exports; story exports lose debug context. Pass B: formatting stored events is presentation, but debug events in a player export are operator data leaking into a player artifact — ADAPT: keep background-event formatting, DELETE debug-event extraction from player exports (debug exports, if needed, are a separate debug artifact).
- `_iter_choice_items`, `_find_matching_choice_key`, `_get_choice_by_key`, `get_choice_type`, `get_selected_choice`: Pass A: deleting them removes planning-choice matching (which choice the player's action selected) from exports; exports would list actions without their choice context. Pass B: matching a stored action to a stored choice key is presentation of stored structure, but only if the keys are stored — if the matcher is instead inferring the choice from prose, it is recomputation — ADAPT: keep only the stored-key lookup path, DELETE any prose-inference fallback (verify which path is live before deleting).
- `format_story_entry`, `get_story_text_from_context_enhanced`, `get_story_text_from_context`: Pass A: deleting them removes story-log-to-text conversion itself, so no export has story content. Pass B: rendering stored entries (scene numbers, session headers, resources, dice rolls as stored) is pure presentation — KEEP.
- Font/layout constants (`ASSETS_DIR`, `FONT_FILENAME`, `DEFAULT_FONT_FAMILY`, `CUSTOM_FONT_NAME`, `ENCODING`, `PDF_TITLE_STYLE`, sizes/line-heights/spacing, `LABEL_GEMINI/GOD/USER`, `UNKNOWN_ACTOR`, `DOCX_HEADING_LEVEL`): Pass A: deleting them removes PDF/DOCX typography and actor labels, so exports lose formatting and attribution. Pass B: typography and labels are presentation data — KEEP (the font file itself is `mvp_site/assets/DejaVuSans.ttf`, verdict-ed in §7).
- `generate_pdf`, `generate_docx`, `generate_txt`: Pass A: deleting them removes three export formats outright. Pass B: file generation from stored state is the export promise's tool execution — KEEP.
- `_escape_yaml_scalar`: Pass A: deleting it risks malformed YAML in any export embedding scalars. Pass B: escaping for a file format is presentation safety — KEEP.
- `_SceneRecord`, `_EntryMetadata`, `_text_value`, `_parse_entry_metadata`, `_safe_choice_key`, `_entry_label`, `_render_entry_block`, `_structured_context_to_markdown`: Pass A: deleting them removes structured-context-to-Markdown conversion, so Markdown exports lose structure. Pass B: rendering stored structured entries is pure presentation — KEEP.
- `_parse_actor_label`, `_quote_markdown_lines`, `_format_player_segment`, `_flush_actor_segment`, `_format_timestamp`, `_escape_markdown_table_cell`, `_render_markdown_document`, `generate_md`, `generate_document`: Pass A: deleting them removes actor attribution, segment formatting, timestamp rendering, and the Markdown dispatcher (which also generates a companion `.md` for every format). Pass B: these are verbatim formatters of stored segments — KEEP, noting the companion-`.md`-for-every-format behaviour should be confirmed as wanted (it doubles export output) before the next export change, not as a deletion now.
- `_SOCIAL_LABELS`, `_ARC_LABELS`, `_COMBAT_LABELS`, `_detect_block_header`, `_is_block_detail_line`, `_convert_presentation_blocks`, `_parse_dice_rolls`, `_format_detail_line`, `_format_presentation_block`, `story_text_to_markdown`: Pass A: deleting them removes the prose-to-Markdown transformation that turns raw exported story text into "publication-ready" Markdown with social/arc/combat block labels and parsed dice rolls. Pass B: this is the file's hard violation — it re-derives structure (block types, dice rolls, detail lines) from prose the model already authored in structured form, and label tables that classify prose into social/arc/combat are domain classification, not formatting — DELETE this group, and make `story_text_to_markdown` a verbatim renderer of stored structured entries or delete it with the group.

### 4.9 `equipment_display.py` — ADAPT (extraction + unfiltered grouping stay; routing/scoring/truncation/injection go)

- `DICE_PATTERN`, `_PAREN_STATS_HINTS`, `WEAPON_SLOTS`, `KNOWN_EQUIPMENT_SLOTS`, `MAX_BACKPACK_ITEMS_DISPLAY` (= 3): Pass A: deleting the slot tables removes the vocabulary for grouping equipment; deleting the cap alone would show all backpack items instead of three. Pass B: slot vocabularies are presentation data, but the top-3 cap is a domain-value truncation disguised as display — KEEP the tables, DELETE the cap (see `_limit_backpack_for_display`).
- `_EQUIPMENT_QUERY_PHRASES`, `_EQUIPMENT_SINGLE_KEYWORDS`, `is_equipment_query`, `classify_equipment_query`: Pass A: deleting them removes client-intent detection for "what am I carrying" questions, so the server would not know to attach a summary. Pass B: intent routing is the model's job from the log (the file's own comments admit bare-substring routing is a ZFC violation, and its phrase-list workaround is still server-side intent classification) — DELETE this group and let the model request the summary through the log/schema.
- `_filter_equipment_for_summary`: Pass A: deleting it removes scope filtering (backpack/weapons/equipped/all) of the summary. Pass B: filtering a player's own equipment list by a scope the player asked for is presentation — but only if the scope comes from the model/server decision, not from the deleted classifier above — ADAPT: keep the filter as a pure function of an explicitly supplied scope, DELETE its coupling to `classify_equipment_query`.
- `_count_equipment_mentions`: Pass A: deleting it removes the count of distinct item names appearing in narrative text, used to decide whether a summary is needed. Pass B: counting mentions in model-authored prose to decide whether to inject a summary is server second-guessing of the model's narrative — DELETE with `ensure_equipment_summary_in_narrative`.
- `_categorize_equipment_slot`, `_classify_backpack_item`: Pass A: deleting them removes slot-to-category mapping and backpack subcategorization, so summaries lose grouping. Pass B: grouping by stored slot/category is pure presentation of stored state — KEEP, provided classification uses stored slot/category fields and not name/stats heuristics that re-derive a category the model never assigned (verify the name-based branches before keeping them verbatim).
- `_get_backpack_importance`, `_limit_backpack_for_display`: Pass A: deleting them removes importance scoring and top-3 truncation, so summaries show all backpack items instead of a ranked three. Pass B: an importance score invented by the server that silently drops items the player owns is a domain-value rewrite with no registered exception — DELETE both.
- `_build_equipment_summary`, `build_equipment_summary`: Pass A: deleting them removes summary construction itself, so no equipment summary can be rendered. Pass B: grouping stored entries by category for display is pure presentation — KEEP, unfiltered and untruncated.
- `ensure_equipment_summary_in_narrative`: Pass A: deleting it removes the deterministic summary appended to narrative when the narrative omits item names; the narrative itself is unchanged. Pass B: appending server text to model-authored narrative is server rewriting of the model's output — the clearest ZFC violation in this area, with no registered exception — DELETE.
- `extract_equipment_display`: Pass A: deleting it removes extraction of equipment from game state into display format, so no summary input exists. Pass B: extraction that preserves stored values is pure parsing/presentation — KEEP.

## 5. Phase 2 — JavaScript, complete files and partial-file key clusters

§5.1 covers every function in the 17 complete JS files, grouped by role with all
members named; each group justification is 2–4 sentences covering Pass A then
Pass B and ends in the verdict. §5.2 covers key clusters only in the 13 partial
files; the rest of those files is untouched (§6).

### 5.1 Complete JS files

**`diag-boot.js` — KEEP (whole file).** `boot(name, extra)` plus the IIFE wiring
(`page.boot_inline`, `DOMContentLoaded`, `load`) and the `window.__diagBoot` /
`window.__diagQueue` exports: Pass A: deleting them loses only the earliest
telemetry events before `diagnostics.js` loads, and the queue is what prevents
that loss. Pass B: client logging is KEEP per §6, the events carry ready-state,
user-agent prefix, and visibility only (no campaign facts), and the try/catch
silently swallows failures so telemetry can never break a turn — KEEP.

**`diagnostics.js` — KEEP (whole file).** `safeStringify`, `envCapture`, `nowMs`,
`event`, `setContext`, `getContext`, `buildPayload`, `sendBeacon`,
`fetchKeepalive`, `flush`, `clearSent`, `installErrorHandlers`,
`installFlushTimer`, `drainBootQueue`, plus the internal `_buffer`/`_bufferSize`/
`_reset`/`_setFetch`/`_setSendBeacon`/`_sessionId` surface: Pass A: deleting them
removes client error/telemetry reporting and boot-queue replay, so operator
visibility into player failures disappears while the game itself keeps playing.
Pass B: logging is KEEP per §6, delivery is already non-blocking (beacon or
keepalive fetch, buffered flush, timer), and no function reads or rewrites a
campaign value — KEEP, with no async adaptation outstanding.

**`api.js` — KEEP (whole file).** `detectClockSkew`, `applyClockSkewCompensation`,
`handleClockSkewError`, `fetchApi`, `checkBackendHealth`,
`detachNetworkStatusListeners`, `attachNetworkStatusListeners`,
`getConnectionStatus`, `safeDiag`, `handleOnline`, `handleOffline`: Pass A:
deleting them breaks authenticated fetching, token-expiry handling under clock
skew, health checks, and online/offline status — the client cannot reliably
reach the log at all. Pass B: all of this is transport (fetch, auth headers,
network state) plus logging, with no domain computation — KEEP.

**`quick_start_shared.js` — KEEP (whole file).** `bannerDismissedKey`,
`scrollToCharacterCreation`, `resolveNewCampaignScrollTarget`,
`dismissFirstRunBanner`, `isFirstRunBannerDismissed`, `normalizeQuickStartPath`,
`buildDashboardSearch`, `buildDashboardHref`: Pass A: deleting them breaks
quick-start banner state, dashboard URL building, and scroll targeting shared
by dashboard and wizard, so new players land in the wrong place or re-see a
dismissed banner. Pass B: navigation and banner preference are presentation,
and the `localStorage` keys are client preference, not campaign state — KEEP.

**`user_lifecycle.js` — ADAPT (keep identity/link; slim acquisition; shared pipeline).**
`now`, `randomUuid`, `readStorage`, `writeStorage`, `parseStoredJson`,
`validUuid`, `createVisitor`, `loadVisitor`, `makeSession`, `loadSession`:
Pass A: deleting them removes anonymous visitor/session creation and persistence,
so pre-auth sessions cannot be continued or linked after sign-in. Pass B:
session identity is an allowed category, and storage helpers are pure transport
— KEEP this group. `snapshotFrom`, `snapshotHeaders`, `touchSession`,
`getIdentity`, `sanitizeScalar`, `getAcquisition`, `acquisitionFromLocation`:
Pass A: deleting them removes session snapshots, header attachment, and
acquisition capture; the identity itself survives without acquisition. Pass B:
snapshots/headers are transport, but acquisition-source fields (where the
player came from) are analytics collection no product decision in this area
justifies — ADAPT: keep snapshots/headers/sanitization, DELETE acquisition
capture. `eventFields`, `currentAuthUser`, `bodyString`, `boundedJoinId`,
`sendWithIdentity`, `record`, `getRequestHeaders`, `screenIdForView`,
`recordScreenViewed`, `recordOnboardingStep`: Pass A: deleting them removes
screen-view and onboarding telemetry events. Pass B: telemetry is KEEP per §6,
but this file maintains its own send path instead of the shared diagnostics
pipeline — ADAPT: route events through `diagnostics.js` delivery.
`rotateIdentity`, `linkAuthenticatedSession`, `handleAuthState`, `logout`,
`userLifecycle` (exported surface): Pass A: deleting them breaks linking an
anonymous session to the authenticated user and clearing it on logout, so
pre-auth progress would orphan or leak across users. Pass B: identity linking
and logout clearing are authorization-adjacent and required for tenant
separation — KEEP.

**`parallel_dual_pass.js` — DELETE (whole file).** `handleInteractionParallel`,
`enhanceStoryInBackground`, `replaceStoryEntry`, `showEnhancementIndicator`,
`hideEnhancementIndicator`, `showEnhancementSuccess`, `parallelDualPass`
(export), `pendingEnhancements` map: Pass A: deleting them breaks nothing
observable, because no shipped page loads the file and the turn path runs
through `streaming.js`; the functions' own POST to `/api/campaigns/<id>/interaction`
and background "enhancement" swap-in are unreachable. Pass B: dead code is not
transport in the running product, and if revived it would be a second story-entry
author competing with the streaming path — DELETE as a set (with its CSS).

**`js/outcome-verdict.js` — ADAPT (explicit branch stays; fallback goes).**
`deriveOutcomeVerdict`, `outcomeVerdictBadgeHtml`, `isSave` (regex helper),
`LABELS`: Pass A: deleting the whole file removes only the outcome badge; the
story and rolls remain. Pass B: the explicit-`player_outcome` branch is pure
presentation of a server-authored verdict and stays, while the fallback that
aggregates non-save roll `success` booleans into success/failure/mixed — with
save exclusion guessed by a label regex — is a client recomputation of a domain
verdict with no registered exception — ADAPT: keep the explicit branch and
badge HTML, DELETE the fallback and the save regex with it.

**`js/ui-utils.js` — KEEP (whole file).** `applyWikiLinks`, `applySocialLinks`,
`setupCollapsibleDescription`, `WORLDAI_WIKI_URL`, `WORLDAI_REDDIT_URL`,
`WORLDAI_DISCORD_URL`, `window.UIUtils` export: Pass A: deleting them leaves
wiki/social anchors at `href="#"` and breaks collapsible descriptions, so
players cannot reach the knowledge base or community links from the UI.
Pass B: setting canonical URLs on already-marked anchors and toggling a CSS
class presents existing markup and rewrites no campaign value — KEEP.

**`js/ember-bg.js` — KEEP (whole file).** `spawnParticle`, `initParticles`,
`prefersReducedMotion`, `buildGradient`, `drawStatic`, `resize`, `draw`,
`animate`, `isFantasyTheme`, `start`, `stop`, `onMotionChange`: Pass A:
deleting them removes the fantasy-theme ember particle background; the game
plays identically without it. Pass B: canvas ambience driven by `Math.random`
is presentation-only visual noise — its randomness never becomes a game roll,
a stat, or any stored value — KEEP (with the reduced-motion respect kept as
accessibility, not as a domain rule).

**`js/loading-messages.js` — KEEP (whole file).** `LoadingMessages` class
(`constructor`, `start`, `stop`, `showMessage`, `getMessageElement`,
`showSingle`), `loadingMessages` singleton: Pass A: deleting them removes
rotating loading messages during waits; waits themselves are unchanged.
Pass B: pure presentation of wait state — KEEP.

**`js/avatar-crop.js` — KEEP (whole file).** `AvatarCrop` class (`show`,
`_doCrop`, `getCroppedFile`, `getCroppedUrl`, `destroy`, `onPointerDown`,
`onPointerMove`, `onPointerUp`): Pass A: deleting them removes pointer-driven
framing of an uploaded avatar, so players cannot crop their own portrait
image. Pass B: cropping is a client-side transform of a player-supplied image,
not a campaign-domain fact, and the cropped file/URL are the player's own
upload — KEEP.

**`js/interface-manager.js` — KEEP (whole file).** `InterfaceManager` class
(`constructor`, `init`, `setMode`, `applyMode`, `enableModernMode`,
`disableAnimations`, `enableAnimations`, `disableEnhancedComponents`,
`enableEnhancedComponents`, `disableInteractiveFeatures`,
`enableInteractiveFeatures`, `setupEventListeners`, `getCurrentMode`,
`getModeInfo`, `isModernMode`, `isFeatureEnabled`, `trackModeUsage`),
`interfaceManager` singleton: Pass A: deleting them removes modern/classic
mode switching and feature toggles, so the settings UI's mode choices stop
working. Pass B: mode/toggle state is client presentation preference in
`localStorage`, not campaign state, and `trackModeUsage` is telemetry (KEEP
per §6) — KEEP.

**`js/portrait-ai-ui.js` — KEEP (whole file).** `getUi`, `updateCounter`,
`panelMarkup`, `setSuggestLoading`, `setGenerateLoading`, `clearPreview`,
`setPendingPreview`, `showPreviewFromResult`: Pass A: deleting them removes
the portrait panel markup, counters, loading states, and preview display, so
generation results cannot be shown or applied cleanly. Pass B: pure
presentation of portrait-generation state under the portrait promise — KEEP.

**`js/worldai-mcp-bridge.js` — KEEP (whole file).** `callTool`,
`mcp__worldai__record_tooltip_event`, `mcp__worldai__get_user_settings`,
`mcp__worldai__reset_tooltip_state`: Pass A: deleting them removes the
client's MCP calls for tooltip events and settings that the tooltip guide
depends on. Pass B: a thin transport shim to server tools, authoring no domain
fact itself — KEEP.

**`js/theme-bootstrap.js` — KEEP (whole file).** `toBoolean`,
`isFantasyThemeEnabled`, `activateAsyncCSS`, `__WORLDAI_FANTASY_THEME_ENABLED`,
`__WORLDAI_THEME_BOOTSTRAP_THEME`: Pass A: deleting them removes the
pre-paint theme decision, causing a visible theme flash on load. Pass B: pure
presentation preference resolved before first paint — KEEP.

**`js/theme-manager.js` — KEEP (whole file).** `ThemeManager` class
(`getDefaultTheme`, `isFantasyThemeEnabled`, `isAllowedTheme`, `constructor`,
`init`, `loadSavedTheme`, `setTheme`, `setupEventListeners`,
`updateThemeIcon`, `destroy`), `themeManager` singleton,
`__WORLDAI_FANTASY_THEME_ENABLED`: Pass A: deleting them removes runtime
theme switching and persistence. Pass B: pure presentation preference —
KEEP, noting `isAllowedTheme` is an allowlist for presentation values, not a
domain rule.

**`js/animation-helpers.js` — ADAPT (animations stay; interception goes).**
`smoothScrollTo`, `showView`, `animatedShowSpinner`,
`animatedHideSpinner`, `fadeOutView`, `fadeInView`, `setupLoadingStates`,
`addButtonLoadingState`, `removeButtonLoadingState`, `setupViewTransitions`,
`enhanceButtonFeedback`, `animateButtonClick`, `showStoryLoading`,
`hideStoryLoading`, `AnimationHelpers` class (`constructor`, `init`,
`enhanceExistingFunctionality`, `animatedShowView`, `getAPI`), `animations`/
`animationHelpers` singletons, `originalSpinnerShow`/`originalSpinnerHide`
captures: Pass A: deleting the whole file removes animated transitions,
button feedback, and story loading spinners; the app functions without them
but abruptly. Pass B: animation and loading-state presentation stays, but
`interceptViewSwitching` (noted in the file's view-switching interception)
and `enhanceExistingFunctionality`'s runtime patching of existing handlers
are behaviour interception, not presentation, and the captured
original-spinner references exist only to support that patching — ADAPT: keep
the animation/loading helpers, DELETE the interception/patching hooks and the
original-function captures.

### 5.2 Partial files — key clusters only (rest untouched, §6)

**`app.js` — ADAPT (decompose; key clusters verdict-ed).** Dashboard/campaign-list
cluster (`renderCampaignListUI`, `showDuplicateCampaignModal`,
`handleCampaignDetailsClick`, `showSuccessToast`, `showErrorToast`): Pass A:
deleting them removes the dashboard itself, the player's campaign list and
detail navigation. Pass B: list rendering and toasts present server state —
KEEP this cluster. Story/download cluster (`getFormattedStoryText`,
`downloadSingleFormat`, `downloadFile`, `handleDownloadClick`,
`handleShareStory`/`handleShareStoryConfirm`/`handleShareStoryCopy`,
`handleUndoStory`): Pass A: deleting them removes story export/download,
sharing, and undo from the reader. Pass B: downloading/sharing stored text and
undoing via the server are durable-write/presentation operations — KEEP this
cluster (undo must remain server-authoritative; the client only requests it).
Quota/mode cluster (`updateQuotaBanner`/`renderQuotaBanner`/`resolveQuotaLimits`,
`showRateLimitModal`, `showSpicyModeToast`, `handleSpicyModeToggle`,
`loadSpicyModeState`, `handleMechanicsHiddenToggle`,
`loadMechanicsHiddenState`, `navigateToSettings`): Pass A: deleting them
removes quota/rate-limit surfacing and the spicy/mechanics-hidden toggles
players use to control display. Pass B: quota display is bounded-capacity
presentation and the toggles are display preferences — KEEP this cluster.
Reading-anchor cluster (`buildNarrativeTextIndex`, `captureReadingTextAnchor`,
`restoreReadingTextAnchor`, `updateReaderFollowing`,
`resumeReaderFollowingAtLiveBottom`, scroll/following helpers): Pass A:
deleting them removes reading-position restoration across re-renders, so
players lose their place on every streaming update. Pass B: scroll/anchor
management is pure reader presentation — KEEP this cluster. Debug cluster
(`refreshDebugToolsEligibility`, `createHudSessionHeaderState`,
`removeDebugControlsFromRenderedEntries`/`addDebugControlsToRenderedEntries`):
Pass A: deleting them removes debug-tools eligibility and debug controls from
rendered entries; the game plays without them. Pass B: operator tooling
embedded in the player bundle is not player presentation — ADAPT: move this
cluster behind a debug flag or out of the shipped bundle. First-turn-coach /
`__firstTurnCoachState` / `syncFirstTurnCoach` cluster: Pass A: deleting it
removes guided first-turn help for new players. Pass B: onboarding presentation
stays, but its state machine duplicates tooltip-guide onboarding — ADAPT:
merge first-turn coaching into the tooltip-guide path or prove the two
onboarding systems do not overlap. Everything else in `app.js` (hundreds of
remaining arrow-function consts: view switching, forms, search params,
pending-login redirect, avatar persistence, campaign creation wiring,
settings lazy-loading) is UNTOUCHED — see §6.

**`auth.js` — ADAPT (one auth path; key clusters verdict-ed).** Firebase
sign-in/out cluster (`signIn`, `signOut`, `registerAuthObserver`/
`registerAuthObserverOnce`, `getBaseAuthHeaders`, `authTokenManager`):
Pass A: deleting them removes identity entirely, so no log can be separated
per player. Pass B: identity/tenant separation is an allowed category —
KEEP this cluster. Waitlist cluster (`getWaitlistStatus`, `hasSiteAccess`,
`submitWaitlistRequest`, `renderWaitlistRequestView`,
`getWaitlistRequestMarkup`, `wireWaitlistRequestMarkup`,
`getLoggedOutAuthMarkup`, `getEffectiveWaitlistUid`): Pass A: deleting them
removes waitlist gating and the logged-out view, so gated players see a
broken entry. Pass B: access gating is authorization — KEEP this cluster.
OpenRouter finish cluster (`isOpenRouterFinishPage`,
`cleanOpenRouterFinishUrl`, `renderOpenRouterFinishing`,
`renderOpenRouterFinish`, `openRouterFinishStateForError`,
`revealOpenRouterWelcomeIfAvailable`, `startOpenRouterWelcomeSignIn`,
`completeOpenRouterWelcomeSignIn`): Pass A: deleting them breaks the
OpenRouter OAuth return journey (finish page, welcome sign-in). Pass B: OAuth
finish handling is authorization transport, but it duplicates the welcome/link
flows in `settings.js` — ADAPT: keep one finish path shared by both files.
Popup/iOS cluster (`getPopupDiagFields`, `schedulePopupPendingDiag`,
`handlePopupPageLifecycle`, `logAuthReturnContext`,
`isAffectedIOSWebKitBrowser`, `handleVisibilityRecovery`,
`__authPersistenceForcedLocalStorage`, test-mode helpers
`canEnableTestMode`, `__ALLOW_TEST_MODE__`, `testAuthBypass`,
`getTestModeParams`): Pass A: deleting them removes popup-lifecycle
diagnostics and iOS persistence workarounds, so some mobile sign-ins fail
opaquely. Pass B: diagnostics are KEEP per §6 and workarounds are transport,
but a test-mode bypass surface in shipped auth code is an authorization risk
disguised as convenience — ADAPT: keep the popup/iOS handling, DELETE or
gate the test-mode bypass out of production builds. Rest of `auth.js`
UNTOUCHED (§6).

**`js/campaign-wizard.js` — ADAPT (slim; key clusters verdict-ed).**
`CampaignWizard` class core (`constructor`, `init`, `setupWizard`,
`generateWizardHTML`, `setupStepNavigation`, `setupEventListeners`,
`nextStep`, `previousStep`, `goToStep`, `updateProgress`,
`validateCurrentStep`, `validateLaunchReadiness`, `collectFormData`,
`launchCampaign`, `attemptLaunch`, `resetWizard`): Pass A: deleting them
removes campaign creation itself — no new campaign can start from the UI.
Pass B: step flow, validation of required fields, and the launch POST are
transport plus presentation — KEEP this cluster. Avatar/portrait cluster
(`setupAvatarHandlers`, `handleAvatarFile`, `clearAvatar`,
`uploadCampaignAvatar`, `_kickWizardPortraitPrefetch`,
`_scheduleWizardPortraitPrefetch`, `_loadArionAvatar`,
`getWizardPortraitSuggestPayload`, `setAvatarSourceMode`,
`wizardPortraitButtons`, `refreshWizardPortraitSuggestion`,
`generateWizardPortrait`, `ensureWizardPortraitPanel`,
`setupPortraitAiWizardHandlers`, `commitWizardPortraitPreview`,
`commitPendingPreviewEdits`): Pass A: deleting them removes wizard avatar
choice, upload, and AI-portrait suggestion/prefetch/commit. Pass B: avatar
handling is presentation/transport under the portrait promise, but the
prefetch/suggest/commit layering duplicates `portrait-ai.js` — ADAPT:
collapse wizard portrait work to calls into `portrait-ai.js`.
Preview/edit cluster (`updatePreview`, `setupEditablePreview`,
`toggleEditMode`, `getFormValueForField`, `syncEditToForm`,
`updatePreviewFromForm`, `populateOriginalForm`, `populateFromOriginalForm`,
`restoreOriginalForm`, `replaceOriginalForm`, `_formatDescription`,
`_formatCharacter`, `_handleIPFieldChange`, `applyUrlParams`,
`_clearPrefilledShareFields`, `loadInitialCampaignContent`): Pass A:
deleting them removes the live preview and edit-in-place experience of the
wizard, including share-token/URL prefill. Pass B: preview rendering of
player-entered form data is presentation, but `_formatDescription`/
`_formatCharacter` reformat player prose for display and the IP-field handling
embeds premade/IP content in code — ADAPT: keep preview/edit mechanics,
move premade/IP copy to data files. Telemetry/scroll cluster
(`logWizardTelemetry`, `__waWizardTelemetry`, scroll-indicator and
mobile-scroll-lock helpers): Pass A: deleting them removes wizard telemetry
and scroll affordances. Pass B: telemetry is KEEP per §6 via the shared
pipeline, and scroll locking is presentation — ADAPT: route telemetry
through `diagnostics.js`. Rest of `campaign-wizard.js` UNTOUCHED (§6).

**`js/settings.js` — ADAPT (one settings path; key clusters verdict-ed).**
Settings load/save cluster (`loadSettings`, `saveSettings`,
`attachSettingsListeners`, `initializeSettingsControls`, `readEntryValue`/
`readRawEntryValue`/`applyEntryValue`/`setEntryDisabled`/`getElementsForEntry`,
`getRadioGroup`/`getSelectedRadioValue`/`setRadioGroupValue`/`setSelectValue`,
`readResponsePayload`, `extractErrorMessage`, `showSaveMessage`,
`showErrorMessage`, `showLoadingIndicator`, `SETTINGS_SCHEMA`): Pass A:
deleting them removes the settings page's ability to load, edit, and save
any setting. Pass B: settings transport plus presentation is allowed, and
schema-driven entry handling is data-driven, not domain logic — KEEP this
cluster. BYOK/key cluster (`setup_byok_event_listeners`,
`setApiKeyFieldVisible`, `reveal_stored_api_key`,
`toggle_api_key_visibility`, `clear_api_key`, `probe`, `dumpByokBindings`,
`logByokBindingSnapshot`): Pass A: deleting them removes bring-your-own-key
management, so players cannot use their own provider keys. Pass B: key
management is authorization/transport, and the binding snapshot is logging
(KEEP per §6) — KEEP this cluster, delivered via the async logging path.
OpenRouter link cluster (`setOpenRouterOAuthStatus`,
`clearPendingOpenRouterConnect`, `hasPendingOpenRouterConnect`,
`consumePendingOpenRouterConnect`, `setOpenRouterAccountLinkStatus`,
`revealOpenRouterAccountLinkIfAvailable`, `startOpenRouterAccountLink`,
`cancelOpenRouterAccountLink`, `applyOpenRouterLinkProvider`,
`refreshOpenRouterLinkedSettings`, `persistOpenRouterLinkProviderChoice`,
`confirmOpenRouterAccountLink`, `resumeOpenRouterAccountLink`,
`currentSettingsUid`): Pass A: deleting them breaks OpenRouter account
linking from settings. Pass B: OAuth linking is authorization transport, but
this cluster duplicates `auth.js`'s finish/welcome flows — ADAPT: keep one
link implementation shared by both files. Scene cluster
(`sceneModeIsOn`, `syncSceneIllustrationToggle`,
`refreshSceneAdvancedVisibility`, `waitForSceneEligibilitySettled`,
`handleSceneSettingsAuthChange`, `bindSceneIllustrationToggle`,
`updateSceneEveryNVisibility`, `__sceneAdvancedAllowed`): Pass A: deleting
them removes scene-illustration settings toggles and their visibility rules.
Pass B: toggle presentation stays, but scene-advanced visibility policy
(eligibility, admin-only advanced settings) is a server decision the client
re-implements — ADAPT: render visibility from the server response instead of
computing eligibility client-side. Rest of `settings.js` UNTOUCHED (§6).

**`js/streaming.js` — ADAPT (keep client; slim inference/telemetry; key clusters verdict-ed).**
`StreamingClient` core (`constructor`, `sendMessage`, `send`,
`_processSSEMessage`, `_handleEvent`, `cancel`, `isActive`): Pass A:
deleting them removes turn submission and streaming itself — no turn can be
played. Pass B: streaming transport is the core allowed category — KEEP this
cluster. Extraction cluster (`_getStreamingDisplayText`,
`_getStreamingDisplay`, `_getStructuredEnvelopePlaceholder`,
`_looksLikeIncompleteStructuredEnvelope`,
`_extractNarrativeFromParsedEnvelope`, `_extractNarrativeFromRawEnvelope`,
`_readJsonStringPrefix`, `_extractPlanningThinking`,
`_getPlanningBlockDepthAtPosition`, `_isEscapedQuote`,
`renderPlanningThinkingBlock`, `createStreamingHandler`): Pass A: deleting
them removes narrative/planning-block extraction from streamed envelopes, so
turns arrive as raw JSON or not at all. Pass B: extraction that preserves
server-authored values is pure parsing (allowed), and planning-block rendering
presents server-authored planning content — KEEP this cluster, with the
caveat that any extraction branch that invents text when the envelope is
incomplete must be deleted, not "repaired" by guessing. Tool-inline cluster
(dice `roll_dice` inline block, `faction_*` inline summaries,
`_getClientTelemetryMetrics`, `getBrowserTraceOffsets`,
`markRenderComplete`, `markComposerReleased`, `noteVisibleRender`,
`getTerminalOutcome`, `getTerminalErrorType`, `_reportClientOutcome`,
`beaconClientStreamLatency`, `showRateLimitModal`, `updateQuotaBanner`):
Pass A: deleting them removes dice/faction inline display, quota/rate-limit
surfacing, and completion bookkeeping during streaming. Pass B: displaying
tool results is presentation, quota display is bounded-capacity presentation,
and client telemetry is KEEP per §6 — but `getTerminalOutcome`/
`getTerminalErrorType` infer a terminal state from client observations rather
than rendering a server-declared one, which risks contradicting the server —
ADAPT: keep display/telemetry/quota, DELETE terminal-outcome inference in
favour of the server's declared outcome. Rest of `streaming.js` UNTOUCHED (§6).

**`js/portrait-ai.js` — ADAPT (transport stays; prose recomposition goes; key clusters verdict-ed).**
Transport cluster (`withTimeout`, `getAuthHeaders`,
`getAuthHeadersWithTimeout`, `postJson`, `fetchPreviewBytesFromServer`,
`previewResultToFile`, `base64ToFile`, `warmPortraitTransport`,
`warmCampaignPortrait`, `prefetchCampaignPortraitPipeline`,
`prefetchWizardPortraitSuggestion`, `prefetchCampaignPortraitPipeline`):
Pass A: deleting them removes portrait API transport, timeouts, preview
bytes, and warmup, so suggestions/generation cannot run. Pass B: transport
plus bounded timeouts is allowed — KEEP this cluster, collapsed to one
prefetch path. Suggestion cluster (`isDisplayablePortraitDescription`,
`composePortraitProseFromAppearance`, `sanitizeSuggestApiResult`,
`suggestCacheKey`, `getCachedSuggest`, `invalidateSuggestCache`,
`rememberSuggest`, `suggestDescription`, `ensurePortraitSuggestionFilled`,
`prefetchCampaignSuggestion`, `applyCachedPortraitSuggestion`,
`resolveSuggestContext`, `runSuggestWithUI`, `resolveDescriptionInput`,
`fillDescriptionInput`, `loadSuggestion`, `revealAiPanelWithSuggestion`):
Pass A: deleting them removes description suggestion, caching, and
prefill, so players must write every portrait description from scratch.
Pass B: caching/transport of a server suggestion is presentation, but
`composePortraitProseFromAppearance` rebuilds prose from appearance slots
when the server text is not displayable, and `sanitizeSuggestApiResult`
substitutes that rebuilt prose — that is client-side authoring of the
description the image model will use — ADAPT: keep suggestion transport and
caching, DELETE the prose recomposition (fall back to the player's own text
or to no suggestion, never to client-composed prose). Generate/apply
cluster (`portraitSuggestExtrasForGenerate`,
`portraitProviderPreferencePayload`, `generatePreview`, `generateForCampaign`,
`applyCampaignPortraitPreview`, `ensurePortraitCommitWiring`, `runGenerateWithUI`,
`run`, `ensureModalPanelMarkup`, `bindModalPortraitContext`,
`waitForPortraitPanel`, `suppressExternalPortraitPanels`,
`restoreExternalPortraitPanels`, `ensureChoiceModal`, `openPortraitChoice`,
`closeModal`, `setPortraitChoiceMode`, `renderPortraitCompareResults`,
`ensurePortraitCompareControl`, `escapeCompareHtml`): Pass A: deleting them
removes preview generation, compare choice, and preview application.
Pass B: generation transport plus choice presentation under the portrait
promise stays, and compare rendering presents server results — KEEP this
cluster, with the compare control following the fate of
`portrait_model_compare.py` (DELETE) if the compare endpoint goes with it.
Timing cluster (`cloneServerTimingMs`, `logPortraitTimingMs`,
`logWarmTiming`, `logPortraitSuggestTiming`, `logPortraitGenerateTiming`,
`setStatusLoading`, `setButtonsDisabled`, `clearPortraitLoading`,
`ensureStatusUI`, `panelUi`, `ui`, `setSuggestLoading`/`setGenerateLoading`
equivalents): Pass A: deleting them removes portrait status/timing display
and logging. Pass B: timing/logging is KEEP per §6 via the async path, and
status presentation stays — KEEP this cluster routed async. Rest of
`portrait-ai.js` UNTOUCHED (§6).

**`js/scene-illustration.js` — ADAPT (slot/poll/lightbox stay; ablation/debug go; key clusters verdict-ed).**
Slot/poll cluster (`normalizeState`, `isStalePending`,
`renderSceneIllustrationSlot`, `updateSceneIllustrationSlot`,
`ensureStreamingSceneSlot`, `resolveSceneHost`, `defaultAuthHeaders`,
`pollSceneIllustration`, `startPollForEntry`, `pollPendingSceneSlots`,
`retrySceneIllustration`, `safeImageUrl`, `sceneSlotHost`): Pass A:
deleting them removes scene-illustration display and polling entirely.
Pass B: polling plus presentation of a server-generated image is
tool-execution presentation under the scene-illustration promise — KEEP this
cluster. Lightbox/format cluster (`closeSceneLightbox`, `openSceneLightbox`,
`escapeHtml`, `escapeAttr`, `formatCostLatency`): Pass A: deleting them
removes full-size viewing and cost/latency display. Pass B: lightbox and
escaping are presentation; cost/latency formatting presents server numbers
— KEEP this cluster. Ablation/debug cluster (`renderAblationControl`,
`renderAblationControlIfAllowed`, `loadDebugToolEligibility`,
`renderAblationPanel`, `runPromptAblation`, `finish`, `tick`, `call`):
Pass A: deleting them removes prompt-ablation experimentation and debug
eligibility from the player UI; illustrations still render. Pass B: operator
experimentation tooling embedded in the player UI is not player presentation
— ADAPT: move behind a debug flag or out of the shipped bundle. Rest of
`scene-illustration.js` UNTOUCHED (§6).

**`js/tooltip-guide.js` — ADAPT (one hydration path; key clusters verdict-ed).**
Hydration cluster (`getState`, `currentAuthUserId`, `beginTooltipHydration`,
`finishTooltipHydration`, `tooltipInteractionReady`,
`mergeHydratedSettings`, `hydrateFromServer`, `bootstrapTooltipGuide`):
Pass A: deleting them removes server-settings hydration for the guide, so
tooltips show the wrong state or re-show completed guides. Pass B: hydration
of server settings is transport/presentation, but two hydration sources
(server merge plus local completion) can disagree — ADAPT: keep one
hydration path with the server as authority. Guide cluster (`TooltipGuide`
class, `attachAll`, `_bindSingle`, `_bindGuides`, `_observeGuideEntry`,
`startGuide`, `_renderGuideCard`, `_positionCard`, `reset`,
`isInteractionReady`, `isGuideCompleted`, `markGuideCompleted`,
`resetGuideBindings`, `safeAttach`, `show`, `close`, `onKey`,
`__TOOLTIPS_DISABLED__`): Pass A: deleting them removes the guide itself —
cards, binding, positioning, completion tracking. Pass B: onboarding
presentation stays — KEEP this cluster. Events cluster (`recordEvent`,
`flushPending`, `dispatchEvent`, `setImmediate`, `setTimeout`): Pass A:
deleting them removes guide interaction events. Pass B: guide telemetry is
KEEP per §6, but this file's own flush pipeline duplicates `diagnostics.js`
— ADAPT: route through the shared diagnostics pipeline. Rest of
`tooltip-guide.js` UNTOUCHED (§6).

**`js/enhanced-search.js` — KEEP (key clusters verdict-ed; rest untouched).**
`EnhancedSearch` class (`constructor`, `init`, `checkIfEnabled`, `enable`,
`disable`, `setupSearchInterface`, `removeSearchInterface`,
`generateSearchHTML`, `setupEventListeners`, `observeCampaignList`,
`refreshCampaignData`, `parseDateFromElement`, `extractCreatedDate`,
`buildSearchText`, `applyFilters`, `sortCampaigns`, `updateDisplay`,
`showNoResultsMessage`, `updateStats`, `updateFilterTags`, `removeFilter`,
`clearAllFilters`, `syncFormControls`, `search`, `setFilter`, `getResults`,
`getTotalCount`, `getFilteredCount`, `getActiveFilterCount`,
`updateFilterBadge`, `updateSortOrderLabel`, `debounce`, `later`,
`enhancedSearch` singleton): Pass A: deleting them removes dashboard
search/filter/sort over the player's campaign list. Pass B: filtering and
sorting a list of the player's own campaigns by text/date is presentation of
already-authored list state, not a recomputation of any campaign fact —
KEEP this cluster (and, by the same reasoning, the file's verdict in §2).

**`js/inline-editor.js` — KEEP (key clusters verdict-ed; rest untouched).**
`InlineEditor` class (`constructor`, `init`, `handleMouseEnter`,
`handleMouseLeave`, `startEdit`, `createEditContainer`, `handleKeydown`,
`handleInput`, `handleOutsideClick`, `save`, `cancel`, `completeEdit`,
`cleanupOutsideClickHandler`, `validate`, `showError`, `removeError`,
`setLoading`, `destroy`): Pass A: deleting them removes in-place story-text
editing from the reader. Pass B: editing player-authored stored text, with
`validate` limited to format/emptiness checks and the server authoritative on
persistence, is durable-write presentation, not domain recomputation —
KEEP this cluster.

**`js/component-enhancer.js`, `js/visual-validator.js`, `js/test_planning_block_parsing.js` — DELETE (whole files; clusters confirm no shipped caller).**
Component-enhancer cluster (`ComponentEnhancer` class: `constructor`,
`isFeatureEnabled`, `init`, `loadEnhancedCSS`, `enhanceExistingComponents`,
`enhanceButtons`, `enhanceCards`, `enhanceForms`, `enhanceModals`,
`enhanceNavigation`, `enhanceContent`, `enhanceLoadingStates`,
`createRippleEffect`, `handleButtonLoading`, `handleFormFocus`,
`handleFormBlur`, `handleModalShow`, `handleModalHide`, `playHoverSound`,
`setupEventListeners`, `setupMutationObserver`, `enhanceNewElement`,
`handleKeyboardNavigation`, `handleScroll`, `handleThemeChange`, `debounce`,
`enable`, `disable`, `toggle`, `cleanup`, `getStatus`): Pass A: deleting them
breaks nothing observable, because the file is never loaded by `index.html`
or referenced by `app.js`. Pass B: unloaded enhancement code is not running
presentation — DELETE. Visual-validator cluster (`overlappingElements`,
`textReadability`, `checkboxAlignment`, `modernModeDefault`, `spinnerCheck`,
`highlightElement`, `getContrastRatio`, `getRGB`, `getLuminance`, `run`,
`captureState`): Pass A: deleting them removes layout QA checks with no
shipped caller and no player-visible effect. Pass B: developer QA tooling is
not player transport or presentation — DELETE. Test-planning cluster
(`decodeHtmlEntities`, `sanitizeHtml`, `escapeHtmlAttribute`,
`parsePlanningBlocksJson`, `queryHTML`, `sanitizeIdentifier`,
`PlanningBlockTestSuite` with `constructor`/`test`/`assert`/`assertContains`/
`assertNotContains`/`run`): Pass A: deleting them removes a self-contained
test harness whose subject (planning-block parsing) already ships in
`streaming.js`, and which no shipped page loads. Pass B: a test harness in
the served directory duplicates shipped parsing logic without serving a
player — DELETE from the shipped directory (assertions, if kept, belong in
`tests/`).

## 6. What remains (exact)

Phase 2 untouched — a follow-up auditor must cover these before this area can
be called complete:

1. `app.js`: every arrow-function const and handler not named in §5.2
   (view switching, form handling, search-param restore, pending-login
   redirect, avatar persistence, campaign-creation wiring, settings
   lazy-loading, and all remaining helpers — hundreds of functions in the
   10,667-line closure). Estimated largest single remainder.
2. `auth.js`: every function not named in §5.2 (header helpers, diag-pathname
   and sign-in-attempt helpers, popup timers, visibility recovery details,
   waitlist markup variants).
3. `js/campaign-wizard.js`: every method/helper not named in §5.2 (scroll
   indicator internals, step-field renumbering, detailed spinner/progress
   animation, portrait panel root helpers, form-value helpers beyond those named).
4. `js/settings.js`: every function not named in §5.2 (provider-section
   toggles, key-field visibility details, load-state guards, confirm-modal
   handlers).
5. `js/streaming.js`: every function/helper not named in §5.2 (SSE detail
   helpers, display-text edge cases, telemetry metric details).
6. `js/portrait-ai.js`: every function not named in §5.2 (modal panel
   markup details, description-input resolution details, compare-control
   wiring details).
7. `js/scene-illustration.js`: every function not named in §5.2 (slot-host
   resolution details, ablation tick/call internals beyond the cluster).
8. `js/tooltip-guide.js`: every function not named in §5.2 (card
   positioning details, guide-entry observation details).
9. `js/enhanced-search.js`, `js/inline-editor.js`: detail beyond the §5.2
   clusters is small (both classes are fully listed there); remainder is
   confirmation that no helper outside the listed class methods exists.
10. All 122 test files and 12 test-support files: individual test-function
    audit (Phase 1 cluster verdicts only, §3).
11. `_ui_mocks/`: any method/function-level audit (assigned Phase 1 only;
    the mocks are static HTML/CSS with no JS functions to audit beyond their
    markup, but that claim itself was not verified function-by-function).
12. CSS/HTML detail: rule-level audit of all CSS files and element-level audit
    of `index.html`, `terms-of-use.html`, and the mock HTML files (files
    verdict-ed as wholes in §2/§7).
13. `tests/mobile_auth_emulator_repro/device_evidence/` and `screenshots/`
    subdirectories: contents not enumerated by the directory listing; confirm
    empty or verdict their contents.
14. Cross-area verification before any DELETE PR: (a) confirm no caller in
    `mvp_site/main.py` or elsewhere loads `component-enhancer.js`,
    `visual-validator.js`, `test_planning_block_parsing.js`, or
    `parallel_dual_pass.js` dynamically (this audit checked `index.html` and
    `app.js` only, plus a repo search for `parallel_dual_pass` that found only
    its own file and a historical integration doc); (b) confirm
    `document_generator`'s choice-matching uses stored keys, not prose
    inference, before deleting the prose-inference fallback; (c) confirm
    `equipment_display._classify_backpack_item`'s name-based branches before
    keeping them verbatim; (d) confirm `portrait_generator_agent`'s six
    assembly wrappers are not all thin aliases before collapsing them.

## 7. Phase 1 — `mvp_site/assets/` and root `_ui_mocks/` (Phase 1 only for `_ui_mocks/`)

| File | Verdict | Justification |
|---|---|---|
| `mvp_site/assets/DejaVuSans.ttf` (757,076 B) | ADAPT | Pass A: deleting it breaks PDF export, because `document_generator.py` registers this font for PDF rendering and has no fallback named in its constants. Pass B: a font is presentation data for the export promise, not a domain value — ADAPT: keep the font, subset it to the glyphs actually used in exports to cut 757 KB of shipped weight, since a full Unicode font for story text is bounded-capacity waste. |
| `_ui_mocks/README.md` (17,748 B) | ADAPT | Pass A: deleting it removes the design index comparing five premade-surfacing mock variants (A–E) and their effort estimates; no player page links to it. Pass B: design documentation is not player transport or presentation, so it does not belong in the shipped tree — ADAPT: move the whole `_ui_mocks/` directory (this README with it) to a design archive outside the product tree, preserving the comparison for design decisions. |
| `_ui_mocks/_ui_mocks.css` (15,540 B) | ADAPT | Pass A: deleting it unstyles all six mock pages, which share this sheet; no shipped page uses it. Pass B: mock-only presentation is not product presentation — ADAPT: move with the mocks to the design archive. |
| `_ui_mocks/mock_A_premade_shelf.html` (7,890 B) | ADAPT | Pass A: deleting it removes the "Premade Shelf" carousel-hero variant; the shipped dashboard does not render it. Pass B: a design variant is not a shipped UI — ADAPT: move to the design archive. |
| `_ui_mocks/mock_B_premades_are_dashboard.html` (5,948 B) | ADAPT | Pass A: deleting it removes the "Premades are the dashboard" variant (3 big hero cards + strip of 5); the shipped dashboard does not render it. Pass B: a design variant, not a shipped UI — ADAPT: move to the design archive. |
| `_ui_mocks/mock_C_wizard_tile_picker.html` (5,803 B) | ADAPT | Pass A: deleting it removes the "Wizard Tile Picker" variant (tiles replacing radio buttons, marked ~0.5 day and starred in the README); the shipped wizard does not render it. Pass B: a design variant, not a shipped UI — ADAPT: move to the design archive, noting this variant is the README's recommended one if premade surfacing is ever revisited. |
| `_ui_mocks/mock_D_dedicated_page.html` (7,791 B) | ADAPT | Pass A: deleting it removes the "Dedicated /campaigns page" variant; no shipped `/campaigns` page renders it. Pass B: a design variant, not a shipped UI — ADAPT: move to the design archive. |
| `_ui_mocks/mock_E_tabs.html` (5,943 B) | ADAPT | Pass A: deleting it removes the "Tabs (Premades \| Mine \| Custom)" variant with continue pin; the shipped dashboard does not render it. Pass B: a design variant, not a shipped UI — ADAPT: move to the design archive. |
| `_ui_mocks/mock_mobile_bottom_sheet_choices.html` (26,247 B) | ADAPT | Pass A: deleting it removes the native-mobile bottom-sheet mock for strategic choices; the shipped mobile choice UI does not render this mock. Pass B: a design variant, not a shipped UI — ADAPT: move to the design archive. |

---
*End of frontend audit. Method note: file listings and contents were obtained
read-only via the GitHub MCP `get_file_contents` (directory listings) and
`search_code` tools at the repo's pinned commit for this session; large JS
files were symbol-extracted locally rather than pasted in full. One transient
HTTP 429 was observed on a single directory listing during enumeration and did
not recur on retry at a slower pace; no write, commit, push, delete, or repo
change was made.*

---

## 8. Phase 2 completion (run 2) — remainder of the 13 partial files, tests, CSS/HTML, `_ui_mocks/`, device evidence

Method note for run 2: all reads were from the local copy at `~/workspace/repos/worldarchitect.ai` (main-branch ZIP tree, no `.git` history); no GitHub API/MCP calls were made. Function lists were extracted from the local files (named `function` declarations, arrow-function consts, class/object methods); duplicate names in separate closures (notably `cleanup`, `fmtMod`, `toNum` in `app.js`, and `resolveCtx`/`run` in `portrait-ai.js`) are counted as separate occurrences and share the verdict of their cluster. Anonymous callbacks (e.g. `setTimeout`/`setImmediate` fallbacks inside `tooltip-guide.js` `flushPending`) are not separate units and are covered under their enclosing named function. Every cluster row below names all its members, covers Pass A then Pass B in 2–4 sentences, and ends in the verdict. File-level verdicts from §2/§5 are unchanged by run 2 except where a correction is flagged explicitly in §8.2/§9/§10. Repo house rules were read (`worldarchitect.ai/AGENTS.md`, `mvp_site/AGENTS.md`); this audit made no repo changes, so its merge, network-request, and PR rules were not triggered, and nothing here authorises a code change.

### 8.1 The 13 partial JS files — every remaining function/symbol, by cluster

**`app.js` — ADAPT (file verdict unchanged; new ADAPT finding: terminal-outcome inference).** All 27 named functions and 230 arrow-function const occurrences are covered below; §5.2 clusters are not repeated except where run 2 changes them.

- Toasts/modals — `showSuccessToast`, `showErrorToast`, `showDuplicateCampaignModal`, `showCancelPendingModal`: Pass A: deleting them removes user feedback and the duplicate/cancel confirmations, so actions would appear to silently do nothing. Pass B: toasts and confirm dialogs present server/client operation results and rewrite no campaign fact — KEEP.
- Dashboard list — `renderCampaignListUI`, `renderCampaignList`, `ensureDashboardNodes`, `ensureElement`, `refreshDashboardOpenRouterStatus`, `getByokProviderActiveStatus`: Pass A: deleting them removes the campaign list and the BYOK/OpenRouter status surfacing on the dashboard. Pass B: list rendering and provider-status display present server state — KEEP.
- Campaign-create wiring — `resetNewCampaignForm`, `enableCampaignWizard`, `setupCampaignTypeHandlers`, `quickStartCampaign`, `returnToDashboardAfterQuickStartFailure`, `handleBannerDismiss`, `campaignIdFromPath`, `restorePendingLoginRedirect`, `clearPendingRedirect`, `hasRestorableSearchParams`: Pass A: deleting them breaks quick-start navigation, pending-login redirect restore, and banner dismissal, stranding new players. Pass B: navigation, redirect restore, and banner preference are transport/presentation, not domain logic — KEEP.
- HUD text — `paint`, `headingTime`, `usableHeader`, `renderHudSubline`, `getLevelUpNoticeKey`, `isLevelUpNoticeDismissed`, `updateRuntimeIndicators`, `setTimerInfo`: Pass A: deleting them removes HUD sublines, level-up notice dismissal state, and timer display. Pass B: they present server-declared HUD values (a level-up notice key is display state for a server-declared event, not a client computation of a level-up) — KEEP.
- Debug cluster — `removeDebugControlsFromRenderedEntries`, `addDebugControlsToRenderedEntries`, `refreshDebugToolsEligibility`, `createHudSessionHeaderState`, `renderDebugDetails`, `getDebugMarkerPairs`, `splitDebugMarkers`: Pass A: deleting them removes debug controls/markers from rendered entries; the game plays without them. Pass B: operator tooling embedded in the player bundle is not player presentation, even though the debug payload itself is server-authored — ADAPT: move behind a debug flag or out of the shipped bundle (same ADAPT as §5.2).
- Reading anchor/scroll — `scrollToBottom`, `isNearLiveBottom`, `buildNarrativeTextIndex`, `matchingSuffixLength`, `matchingPrefixLength`, `resolveSemanticTextOffset`, `words`, `captureReadingTextAnchor`, `captureVisibleReadingAnchor`, `releaseReadingTailSpace`, `updateReadingTailSpace`, `restoreReadingTextAnchor`, `cancelActiveReadingAnchorTransaction`, `isEditableEventTarget`, `isScrollIntentKeyEvent`, `beginReadingAnchorTransaction`, `cleanup`, `restore`, `cancelOnScrollKey`, `armExpiry`, `refreshReaderTextAnchor`, `scheduleReaderTextAnchorRefresh`, `resetReaderScrollIntent`, `cancelReaderFollowing`, `resumeReaderFollowingAtLiveBottom`, `resumeReaderFollowingOnNextScroll`, `onScroll`, `handleReaderWheelIntent`, `handleReaderGestureIntent`, `matchingTouch`, `matchesGesture`, `onMove`, `onEnd`, `onCancel`, `isDownwardScrollIntentKeyEvent`, `updateReaderFollowing`, `ensureReaderPill`, `setUnread`, `arrow`, `releaseReaderPill`: Pass A: deleting them removes reading-position restoration across streaming re-renders, so players lose their place on every update. Pass B: scroll, anchor, and gesture handling is pure reader presentation over text the server already authored — KEEP (duplicate `cleanup`/`onScroll`/etc. names are separate per-closure instances, each covered here).
- Drafts — `clearDraft`, `clearPendingDraftTimer`, `stopDraftRecovery`: Pass A: deleting them leaves stale composer drafts and timers that could resubmit or resurrect text after a turn ends. Pass B: draft hygiene is client-side durable-write bookkeeping, not a domain decision — KEEP.
- Spinners/perf — `showSpinner`, `hideSpinner`, `_perfNow`: Pass A: deleting them removes loading spinners and the performance clock used by timing displays. Pass B: wait-state presentation and measurement — KEEP.
- Quota — `showRateLimitModal`, `resolveQuotaLimits`, `renderQuotaBanner`, `updateQuotaBanner`: Pass A: deleting them removes quota/rate-limit surfacing, so players hit silent turn failures. Pass B: quota display is bounded-capacity presentation of server values — KEEP.
- Info/stats panels — `handleInfoQuery`, `renderInfoTable`, `buildStatsHTML`, `parsePythonReprDict`, `skipWs`, `parseString`, `parseValue`, `parseList`, `parseDict`, `fmtMod`, `getStat`, `firstString`, `buildEquipmentHTML`, `buildSpellsHTML`, `normalizeSpell`, `groupSpells`, `renderSpellGroup`, `toNum`: Pass A: deleting them removes the character info/stats/equipment/spells panels, a core reader surface. Pass B: they parse and group server-provided structured data for display — `buildEquipmentHTML` was brace-verified to render the full `equipment_list` with no slice/limit/truncation (unlike the server `equipment_display` truncation, which is the violation, not this client renderer), and `groupSpells` groups by a stored level field — KEEP.
- Views/routing/settings lazy-load — `showView`, `handleRouteChange`, `loadSettingsPage`, `initializeSettings`, `setupSettingsEventListeners`, `navigateToSettings`, `isMechanicsHiddenActive`: Pass A: deleting them removes view switching, routing, and lazy settings-page loading. Pass B: navigation and display-preference loading are presentation/transport; the settings duplication (this loader vs `settings.js`) is a decompose concern under the file ADAPT, not a separate violation — KEEP.
- Structured fields — `formatRecordedRollFields`, `generateStructuredFieldsPreNarrative`, `getActionResolutionNarrative`, `usable`, `formatRollObject`, `getActionResolutionRollObjects`, `naturalD20Face`, `toDiceRolls`, `escapeRecordedText`, `isWireObject`, `renderImplicitCacheUsage`, `hasOwn`, `firstKnown`, `formatTokenBreakdown`, `generateStructuredFieldsPostNarrative`, `renderPlanningBlock`, `renderEntitiesMentioned`, `generateStructuredFieldsHTML`, `getStoryLabel`: Pass A: deleting them removes structured-field panels (rolls, entities, tokens, action resolution) from story entries. Pass B: they format recorded, server-supplied field values for display — `naturalD20Face` formats a recorded face value and performs no roll, so the §6 anti-cheat rule (server dice resolution) is untouched — KEEP.
- Story rendering — `buildStoryEntryHtml`, `attachStoryEntryHandlers`, `renderStoryEntryElement`, `appendToStory`, `loadOlderStoryEntries`, `updateLoadOlderButton`, `syncLoadOlderVisibility`, `renderNarrativeMarkdown`, `renderNarrativeHtml`, `renderStreamingNarrative`, `streamingRenderCutoff`, `parsePlanningBlocks`, `parsePlanningBlocksJson`, `renderPlanningProse`, `decodeHtmlEntities`, `sanitizeHtml`, `escapeHtmlAttribute`, `sanitizeIdentifier`: Pass A: deleting them removes story rendering, pagination, and planning-block choice rendering from the reader. Pass B: they present server-authored entries and choices; the planning/HTML helpers here are the live reader copies, so unlike the unloaded `test_planning_block_parsing.js` copies they stay — KEEP, with the duplication against `streaming.js` extraction noted as maintenance debt under the file ADAPT, not a deletion.
- Review/choices — `resetReviewState`, `setReviewPhase`, `markTakenChoice`, `resetChoiceSendingState`, `initChoiceDetailViewport`, `sync`, `toggleChoiceDetail`, `choiceKeepsMode`, `markReviewSaveFailed`, `handleChoiceClick`, `renderComposerChoices`, `selectionLabel`, `selectionKeyLabel`, `demoteInlineEntry`, `resetComposerTurnTracking`: Pass A: deleting them removes choice detail disclosure, review-phase tracking, and composer choice rendering — the player's primary action surface. Pass B: choice UI state and display labels present server-authored choices, and sending remains server-authoritative — KEEP.
- Composer/mode — `setSpicySwitchChecked`, `setSpicyModeIndicator`, `getComposerInteractionMode`, `syncComposerPlaceholder`, `syncChoiceButtonsEnabled`, `syncComposerInteractionMode`, `isServerFlagTrue`, `isServerFlagFalse`, `resolveCharCreationState`, `isWideChoiceViewport`, `showSpicyModeToast`, `handleSpicyModeToggle`, `loadSpicyModeState`, `handleMechanicsHiddenToggle`, `loadMechanicsHiddenState`, `getInteractionSubmitButton`, `resizeComposerInput`, `syncComposerSubmitState`, `clearInteractionSubmitLoading`, `cleanupComposerPendingState`, `initComposerKeyboardSubmit`, `initKeyboardInset`, `update`: Pass A: deleting them removes composer mode switching, spicy/mechanics-hidden toggles, keyboard submit, and submit-state sync. Pass B: display preferences plus composer transport, with server flags read (not invented) via `isServerFlagTrue/False` — KEEP.
- First-turn coach — `readFirstTurnCoachCompletion`, `currentFirstTurnCoachUser`, `initializeFirstTurnCoach`, `syncFirstTurnCoach`: Pass A: deleting them removes guided first-turn help for new players. Pass B: onboarding presentation stays, but the state machine duplicates tooltip-guide onboarding — ADAPT: merge into the tooltip-guide path or prove non-overlap (same ADAPT as §5.2).
- Avatar — `flushPendingAvatarPersist`, `resumeCampaign`, `isCurrentResume`, `_avatarUrlWithCacheBust`, `getHeaderAvatarHost`, `setupGameAvatar`, `openIngamePortraitAi`, `expandAvatar`, `collapseAvatar`: Pass A: deleting them removes resume, header avatar display, and avatar expand/collapse. Pass B: avatar display plus background (non-blocking) persist is presentation/transport under the portrait promise, consistent with the `campaign_create_nav_before_avatar` guard that navigation must not await persist — KEEP.
- HUD controls/menus/tooltips — `initModeHelp`, `close`, `initModeTooltips`, `keepOffEdge`, `tip`, `describeRadio`, `initHudControls`, `closeMenu`, `syncMenuRows`, `syncSpicyRow`, `initDesktopChoiceKeys`: Pass A: deleting them removes HUD menus, mode help/tooltips, and desktop choice shortcuts. Pass B: menu/tooltip/shortcut presentation over existing controls — KEEP.
- Opening/turn lifecycle — `openingFlowHoldsComposer`, `removeRejectedTurnEntries`, `handOffOpeningNotReady`, `restoreUiState`, `syncTurnCancelButton`, `setTurnLocked`, `reconcileCancelledTurn`, `stillCurrent`, `restoreSubmittedActionOnCapacityError`, `handleStreamingInteraction`, `handleRegularInteraction`, `registerAppAuthObserver`: Pass A: deleting them removes turn locking, cancel/reconcile handling, and opening-story handoff, so turns could double-submit or strand. Pass B: turn-path transport and concurrency control are allowed categories, and the code authors no story content — KEEP.
- Terminal outcome — `clientTerminalOutcome`, `clientTerminalErrorType`, `deriveTerminalOutcome`: Pass A: deleting them removes only the client's terminal-state label for a finished stream; the story and server payload remain. Pass B: this is a NEW ADAPT finding in run 2, mirroring the `streaming.js` inference: `deriveTerminalOutcome` correctly trusts `payload.success`/`terminal_outcome`/error fields first, but then infers `"success"` from mere presence of narrative text (`hasCompletedText`) and falls back to the mutable client descriptor, so a cleanup abort or a partial render could be labelled a completed turn the server never declared — ADAPT: keep the server-field branches, DELETE the `hasCompletedText → success` fallback and the client-descriptor fallback.
- Completion telemetry/render — `flushCompletionTelemetry`, `queueCompletionTelemetry`, `settleCompletionWithoutRender`, `markRenderSettled`, `runCompletionRender`: Pass A: deleting them removes completion bookkeeping and the final render step after a stream ends. Pass B: telemetry is KEEP per §6 via the async path and final rendering presents the completed server payload — KEEP.
- Streaming session render — `ownsStreamingEntry`, `scheduleInitialNarrativeReveal`, `holdLockWhileServerTurnRuns`, `buildStreamingSessionHeaderHtml`, `renderStreamingPreSections`, `reconcileStreamingPreSections`, `formatStreamingErrorMessage`, `cleanupStreamingPlaceholder`, `markStreamingEntryUnsaved`, `recoverFailedTurn`, `finalizeCompletionRender`: Pass A: deleting them removes streaming session headers, pre-sections, error formatting, and failed-turn recovery from the reader. Pass B: rendering/transport plus re-presentation of a failed turn (no invented content) — KEEP.
- Downloads/share/undo — `getFormattedStoryText`, `downloadSingleFormat`, `downloadFile`, `handleDownloadClick`, `handleCampaignDetailsClick`, `handleShareStory`, `handleShareStoryConfirm`, `handleShareStoryCopy`, `handleUndoStory`: already verdict-ed KEEP in §5.2; run 2 confirms no additional members exist in this cluster — KEEP.
- Model constants + diagnostics — `loadModelConstants`, `safeDiag`: Pass A: deleting them removes server model-constant loading (with the fallback the `default_gemini_fallback` test pins) and the local diagnostics shim. Pass B: server-config transport plus logging (KEEP per §6); the fallback constant is a configuration default, not a campaign fact — KEEP.

**`auth.js` — ADAPT (file verdict unchanged).** All 10 named functions and 36 arrow-function consts are covered below; §5.2 clusters are not repeated except the test-mode correction.

- Auth domain — `resolveAuthDomain`: Pass A: deleting it breaks auth-domain resolution for custom/preview hosts, so sign-in targets the wrong Firebase project. Pass B: identity configuration transport — KEEP.
- iOS/popup diagnostics — `isAffectedIOSWebKitBrowser`, `isMobileUserAgent`, `getNowMs`, `nextSigninAttemptId`, `getDiagPathname`, `getAuthCallbackDeltaSincePopupStart`, `isCurrentAuthCallback`, `skipStaleAuthCallback`, `getSigninContextFields`, `getPopupDiagFields`, `flushDiagNow`, `clearPopupPendingTimer`, `schedulePopupPendingDiag`, `handlePopupPageLifecycle`, `logAuthReturnContext`, `handleVisibilityRecovery`, `safeDiag`, `markForceGoogleAccountSelect`, `shouldForceGoogleAccountSelect`, `clearForceGoogleAccountSelect`: Pass A: deleting them removes popup-lifecycle diagnostics, stale-callback suppression, and iOS WebKit workarounds, so mobile sign-ins fail opaquely (the exact failure class the emulator repro in §8.5 documents). Pass B: diagnostics are KEEP per §6 and the workarounds are sign-in transport, authoring no domain value — KEEP.
- Auth core + waitlist — `registerAuthObserver`, `registerAuthObserverOnce`, `signIn`, `signOut`, `getBaseAuthHeaders`, `getEffectiveWaitlistUid`, `getWaitlistStatus`, `hasSiteAccess`, `submitWaitlistRequest`, `getLoggedOutAuthMarkup`, `getWaitlistRequestMarkup`, `wireWaitlistRequestMarkup`, `renderWaitlistRequestView`, `getConnectingMarkup`, `OPENROUTER_FINISH_SHELL`: Pass A: deleting them removes sign-in/out, auth observation, waitlist gating, and the logged-out/connecting views entirely. Pass B: identity, tenant separation, and access gating are allowed categories — KEEP.
- Test-mode bypass — `canEnableTestMode`, `getTestModeParams` (plus the §5.2-named `__ALLOW_TEST_MODE__`/`testAuthBypass` surface): Pass A: deleting them removes only the test sign-in bypass; real sign-in is unaffected. Pass B: a test-mode bypass in shipped auth code is an authorization risk disguised as convenience — ADAPT: DELETE or gate it out of production builds (same ADAPT as §5.2; run 2 confirms `canEnableTestMode`/`getTestModeParams` are the live gates for it).

**`js/campaign-wizard.js` — ADAPT (file verdict unchanged).** All 5 top-level functions, 4 top-level consts, and 66 class methods are covered below; §5.2 clusters are not repeated.

- IP-marker wire format — `formatIpMarker`, `extractIpFieldsFromDescription`, `buildMarkerBlock`, `descriptionIsMarkerPure`, `getStructuredCreateFields`: Pass A: deleting them breaks the wizard's structured-field round-trip (universe/timeline/character/plot fields serialised into the description and parsed back, including share-token/URL prefill). Pass B: this is a serialisation contract for player-entered field values, not a recomputation of any campaign fact — the code invents no universe, timeline, or character, it only encodes and decodes what the player entered — KEEP, with the contract documented wherever the server parses the markers, since a silent format change would corrupt prefill.
- Campaign-type UI — `handleCampaignTypeChange`, `syncCampaignTypeUI`, `resetCampaignTypeState`, `forceCleanRecreation`, `checkIfEnabled`, `enable`, `disable`, `updateUI`, `getDefaultTitle`: Pass A: deleting them removes campaign-type switching and recreation, so choosing Custom vs Dragon Knight vs IP would leave stale form state. Pass B: form-state presentation and type switching — KEEP.
- Scroll indicator — `setupScrollIndicator`, `isMobileViewport`, `applyMobileScrollLock`, `releaseMobileScrollLock`, `isScrolledToBottom`, `updateScrollIndicator`, `onScroll`, `onResize`, `updateProgress`, `setIfPresent`: Pass A: deleting them removes the mobile scroll chevron/lock affordances in the wizard. Pass B: scroll presentation — KEEP.
- Launch/spinner/portrait-panel wiring — `showDetailedSpinner`, `animateCreationProgress`, `completeProgress`, `setLaunchButtonsDisabled`, `resetLaunchState`, `setWizardPortraitStatus`, `wizardPortraitPanelRoot`, `ensureWizardPortraitPanel`: Pass A: deleting them removes launch progress/spinner and button disabling during launch, so double-launch and dead-spinner states return. Pass B: progress presentation and launch-button concurrency control — KEEP (portrait-panel wiring itself is presentation; the portrait work behind it follows the §5.2 collapse ADAPT).
- Step-field helpers — `renumberVisibleFields`, `getFormValueForField`: Pass A: deleting them breaks visible-field numbering and generic form reads the preview/edit flow depends on. Pass B: form mechanics, no domain values — KEEP.
- Wizard telemetry — `logWizardTelemetry`: Pass A: deleting it removes wizard telemetry only. Pass B: telemetry is KEEP per §6, but only via the shared pipeline — ADAPT: route through `diagnostics.js` (same ADAPT as §5.2).
- Core/avatar/preview clusters — §5.2 verdicts stand (core KEEP, avatar/portrait ADAPT collapse into `portrait-ai.js`, preview/edit ADAPT move premade/IP copy to data); run 2 confirms no further methods exist outside the clusters named here and in §5.2.

**`js/settings.js` — ADAPT (file verdict unchanged).** All 49 named functions and 5 consts are covered below; §5.2 clusters are not repeated.

- Provider-section toggle — `toggleProviderSections`: Pass A: deleting it leaves all provider sections visible regardless of the selected provider, confusing BYOK setup. Pass B: show/hide of settings sections by a selected provider is presentation — KEEP.
- Auth headers — `getAuthHeaders`: Pass A: deleting it breaks every authenticated settings call, since it delegates to `window.authTokenManager`. Pass B: pure auth-header transport — KEEP.
- Onboarding reset + confirm modal — `handleResetOnboarding`, `show_confirmation_modal`, `onConfirm`, `onCancel`: Pass A: deleting them removes the "restore tips" reset and the generic confirm dialog settings actions use. Pass B: onboarding-reset transport (via the tooltip MCP tools) plus dialog presentation — KEEP.
- Fetch-abort classification + load guards — `isBenignSettingsFetchAbort`, `isCurrentLoad`, `cleanup`: Pass A: deleting them turns benign aborts (e.g. navigating away mid-load) into error toasts and lets stale loads overwrite newer settings. Pass B: fetch hygiene and stale-write guards for settings transport, not campaign state — KEEP.
- Remaining clusters — §5.2 verdicts stand (load/save + entry/radio helpers KEEP, BYOK KEEP with async logging, OpenRouter link ADAPT dedup into `auth.js`, scene ADAPT render visibility from the server response); run 2 confirms `logByokBindingSnapshot`, `setup_byok_event_listeners`, `setApiKeyFieldVisible`, `reveal_stored_api_key`, `toggle_api_key_visibility`, `clear_api_key`, and `probe` all sit inside those clusters — KEEP in kind.

**`js/streaming.js` — ADAPT (file verdict unchanged).** All class methods, 3 top-level functions, and 5 consts are covered below; §5.2 clusters are not repeated.

- Core + handlers — `constructor`, `sendMessage`, `send`, `_processSSEMessage`, `_handleEvent`, `cancel`, `isActive`, `createStreamingHandler`, `_renderFinalEntryInPlace`: Pass A: deleting them removes turn submission, SSE processing, cancellation, and final-entry rendering — no turn can be played. Pass B: streaming transport is the core allowed category — KEEP.
- Extraction internals — `_getStreamingDisplayText`, `_getStreamingDisplay`, `_getStructuredEnvelopePlaceholder`, `_looksLikeIncompleteStructuredEnvelope`, `_extractNarrativeFromParsedEnvelope`, `_extractNarrativeFromRawEnvelope`, `_readJsonStringPrefix`, `_extractPlanningThinking`, `_isEscapedQuote`, `_getPlanningBlockDepthAtPosition`, `offset`, `pendingJsonOpening`, `extractAt`, `renderPlanningThinkingBlock`: Pass A: deleting them removes narrative/planning extraction from streamed envelopes, so turns arrive as raw JSON or not at all. Pass B: extraction preserving server-authored values is pure parsing; the incomplete-envelope placeholder must stay a placeholder and never be "repaired" by guessing text — KEEP with that guard (same caveat as §5.2).
- Telemetry/completion bookkeeping — `_getClientTelemetryMetrics`, `getBrowserTraceOffsets`, `markRenderComplete`, `markComposerReleased`, `noteVisibleRender`, `_reportClientOutcome`, `beaconClientStreamLatency`: Pass A: deleting them removes client stream telemetry and render-completion bookkeeping. Pass B: telemetry/logging is KEEP per §6 via the async path — KEEP.
- Terminal inference — `getTerminalOutcome`, `getTerminalErrorType`: Pass A: deleting them removes only the client's terminal label; the server payload and story remain. Pass B: inferring a terminal state from client observations rather than rendering a server-declared outcome risks contradicting the server — ADAPT: DELETE the inference in favour of the server's declared outcome (same ADAPT as §5.2, now confirmed as the mirror of the `app.js` `deriveTerminalOutcome` finding).

**`js/portrait-ai.js` — ADAPT (file verdict unchanged).** All 68 arrow-function const occurrences are covered below; §5.2 clusters are not repeated except the compare correction.

- Transport — `withTimeout`, `getAuthHeaders`, `getAuthHeadersWithTimeout`, `postJson`, `fetchPreviewBytesFromServer`, `previewResultToFile`, `base64ToFile`, `warmPortraitTransport`, `warmCampaignPortrait`, `prefetchCampaignPortraitPipeline`, `prefetchWizardPortraitSuggestion`, `prefetchWizardPortraitPipeline`: Pass A: deleting them removes portrait API transport, timeouts, preview bytes, and warmup, so suggestions/generation cannot run. Pass B: transport plus bounded timeouts is allowed — KEEP in kind, collapsed to one prefetch path (same ADAPT as §5.2).
- Suggestion guard + cache — `looksLikeRawPortraitJson`, `isDisplayablePortraitDescription`, `suggestCacheKey`, `getCachedSuggest`, `invalidateSuggestCache`, `rememberSuggest`, `suggestDescription`, `ensurePortraitSuggestionFilled`, `prefetchCampaignSuggestion`, `applyCachedPortraitSuggestion`, `resolveSuggestContext`, `runSuggestWithUI`, `resolveDescriptionInput`, `fillDescriptionInput`, `loadSuggestion`, `revealAiPanelWithSuggestion`: Pass A: deleting them removes description suggestion, caching, and prefill, so players must write every portrait description from scratch. Pass B: caching/transport/presentation of a server suggestion stays; `looksLikeRawPortraitJson` is a display guard that refuses to show leaked raw JSON, it rewrites nothing — KEEP, except the §5.2 prose-recomposition pair (`composePortraitProseFromAppearance` DELETE, `sanitizeSuggestApiResult` ADAPT to remove the substitution).
- Timing — `cloneServerTimingMs`, `logPortraitTimingMs`, `logWarmTiming`, `logPortraitSuggestTiming`, `logPortraitGenerateTiming`: Pass A: deleting them removes portrait timing display/logging only. Pass B: timing/logging is KEEP per §6 via the async path — KEEP.
- Generate/apply — `portraitSuggestExtrasForGenerate`, `portraitProviderPreferencePayload`, `generatePreview`, `generateForCampaign`, `applyCampaignPortraitPreview`, `ensurePortraitCommitWiring`, `runGenerateWithUI`, `run`, `resolveCtx`: Pass A: deleting them removes preview generation and preview application. Pass B: generation transport plus choice presentation under the portrait promise — KEEP (the duplicated `run`/`resolveCtx` names are separate per-closure instances, each covered here).
- Modal/panel — `ui`, `ensureStatusUI`, `setStatusLoading`, `setButtonsDisabled`, `panelUi`, `clearPortraitLoading`, `ensureModalPanelMarkup`, `bindModalPortraitContext`, `nextFrame`, `waitForPortraitPanel`, `suppressExternalPortraitPanels`, `restoreExternalPortraitPanels`, `ensureChoiceModal`, `openPortraitChoice`, `setPortraitChoiceMode`, `closeModal`, `actionButtons`, `wirePanelActions`, `currentDescription`: Pass A: deleting them removes the portrait modal, status/loading states, and panel wiring. Pass B: pure presentation of portrait-generation state — KEEP.
- Compare — `escapeCompareHtml`, `renderPortraitCompareResults`, `ensurePortraitCompareControl`: Pass A: deleting them removes only the model-compare choice UI; single-model generation is untouched. Pass B: compare rendering presents server results, but its subject (`portrait_model_compare.py`) is DELETE — ADAPT, corrected from §5.2's conditional note: DELETE `renderPortraitCompareResults` and `ensurePortraitCompareControl` with the compare endpoint, and keep only `escapeCompareHtml` (generic escaping, KEEP) if it is used elsewhere, otherwise DELETE it with the pair.

**`js/scene-illustration.js` — ADAPT (file verdict unchanged).** All 23 named functions and 3 consts are covered below; §5.2 clusters are not repeated except to confirm completeness.

- Slot/poll — `normalizeState`, `isStalePending`, `renderSceneIllustrationSlot`, `updateSceneIllustrationSlot`, `ensureStreamingSceneSlot`, `resolveSceneHost`, `defaultAuthHeaders`, `pollSceneIllustration`, `startPollForEntry`, `pollPendingSceneSlots`, `retrySceneIllustration`, `safeImageUrl`, `sceneSlotHost`: Pass A: deleting them removes scene-illustration display and polling entirely. Pass B: polling plus presentation of a server-generated image is tool-execution presentation under the scene-illustration promise — KEEP.
- Lightbox/format/escaping — `closeSceneLightbox`, `openSceneLightbox`, `escapeHtml`, `escapeAttr`, `formatCostLatency`: Pass A: deleting them removes full-size viewing and cost/latency display. Pass B: lightbox, escaping, and formatting of server numbers are presentation — KEEP.
- Ablation/debug — `renderAblationControl`, `renderAblationControlIfAllowed`, `loadDebugToolEligibility`, `renderAblationPanel`, `runPromptAblation`, `finish`, `tick`, `call`: Pass A: deleting them removes prompt-ablation experimentation and debug eligibility from the player UI; illustrations still render. Pass B: operator experimentation tooling embedded in the player UI is not player presentation — ADAPT: move behind a debug flag or out of the shipped bundle (run 2 confirms `finish`/`tick`/`call` are ablation internals, not separate player features).

**`js/tooltip-guide.js` — ADAPT (file verdict unchanged).** All 14 top-level functions and the 16 `TooltipGuide` object methods are covered below; §5.2 clusters are not repeated except to confirm completeness.

- Hydration — `getState`, `currentAuthUserId`, `beginTooltipHydration`, `finishTooltipHydration`, `tooltipInteractionReady`, `mergeHydratedSettings`, `hydrateFromServer`, `bootstrapTooltipGuide`: Pass A: deleting them removes server-settings hydration, so tooltips show wrong state or re-show completed guides. Pass B: hydration of server settings is transport/presentation, but two hydration sources (server merge plus local completion) can disagree — ADAPT: keep one path with the server as authority (same ADAPT as §5.2).
- Guide object — `TooltipGuide` object plus `attachAll`, `_bindSingle`, `_bindGuides`, `_observeGuideEntry`, `startGuide`, `_renderGuideCard`, `positionCard` (named `_positionCard` in §5.2), `reset`, `isInteractionReady`, `isGuideCompleted`, `markGuideCompleted`, `resetGuideBindings`, `safeAttach`, `show`, `close`, `onKey`, `escapeHtml`: Pass A: deleting them removes the guide itself — cards, binding, positioning, completion tracking, keyboard handling. Pass B: onboarding presentation stays — KEEP.
- Events — `recordEvent`, `flushPending`, `dispatchEvent` (the `wa:tooltip-hydrated` dispatch), plus the anonymous `setImmediate`/`setTimeout` fallback callbacks inside `flushPending`: Pass A: deleting them removes guide interaction events. Pass B: guide telemetry is KEEP per §6, but this file's own flush pipeline duplicates `diagnostics.js` — ADAPT: route through the shared diagnostics pipeline (same ADAPT as §5.2; the anonymous callbacks are covered here, not as separate units).

**`js/enhanced-search.js` — KEEP (Phase 2 now complete; file verdict unchanged).** Run 2 confirms the §5.2 cluster is exhaustive: the file contains only the `EnhancedSearch` class (33 methods: `constructor`, `init`, `checkIfEnabled`, `enable`, `disable`, `setupSearchInterface`, `removeSearchInterface`, `generateSearchHTML`, `setupEventListeners`, `observeCampaignList`, `refreshCampaignData`, `parseDateFromElement`, `extractCreatedDate`, `buildSearchText`, `applyFilters`, `sortCampaigns`, `updateDisplay`, `showNoResultsMessage`, `updateStats`, `updateFilterTags`, `removeFilter`, `clearAllFilters`, `syncFormControls`, `search`, `setFilter`, `getResults`, `getTotalCount`, `getFilteredCount`, `getActiveFilterCount`, `updateFilterBadge`, `updateSortOrderLabel`, `debounce`) plus the `later` helper const and the `enhancedSearch` singleton, and no other top-level helper exists. Pass A: deleting any of them degrades dashboard search/filter/sort over the player's campaign list. Pass B: filtering/sorting already-authored list state by text/date is presentation, not a recomputation of any campaign fact — KEEP, all members.

**`js/inline-editor.js` — KEEP (Phase 2 now complete; file verdict unchanged).** Run 2 confirms the file contains only the `InlineEditor` class (19 methods) and no other top-level helper. The §5.2 list covered 18; the one additional method is `attachOrReplace`: Pass A: deleting it removes the static guard that prevents double-attaching an editor to the same element (the issue #9116 fix its test pins), so duplicate editors could stack. Pass B: attach-dedup is presentation hygiene over the player's own stored text, with the server authoritative on persistence — KEEP. All other 18 methods stand as §5.2 verdict-ed — KEEP, all members.

**`js/component-enhancer.js` — DELETE (whole file; Phase 2 now complete).** All 31 class methods (`constructor`, `isFeatureEnabled`, `init`, `loadEnhancedCSS`, `enhanceExistingComponents`, `enhanceButtons`, `enhanceCards`, `enhanceForms`, `enhanceModals`, `enhanceNavigation`, `enhanceContent`, `enhanceLoadingStates`, `createRippleEffect`, `handleButtonLoading`, `handleFormFocus`, `handleFormBlur`, `handleModalShow`, `handleModalHide`, `playHoverSound`, `setupEventListeners`, `setupMutationObserver`, `enhanceNewElement`, `handleKeyboardNavigation`, `handleScroll`, `handleThemeChange`, `debounce`, `enable`, `disable`, `toggle`, `cleanup`, `getStatus`) plus the `later` helper and the `window.ComponentEnhancer`/`window.componentEnhancer` exports (instantiated at load): Pass A: deleting them breaks nothing observable, because `index.html` never loads the file and no shipped code references the export (the only in-tree mention is a `themeChanged` comment in `theme-manager.js`, which dispatches an event and does not load this file). Pass B: unloaded enhancement code is not running presentation — DELETE, all members.

**`js/visual-validator.js` — DELETE (whole file; Phase 2 now complete).** The `VisualValidator` object literal: 5 checks (`overlappingElements`, `textReadability`, `checkboxAlignment`, `modernModeDefault`, `spinnerCheck`), helpers (`highlightElement`, `getContrastRatio`, `getRGB`, `getLuminance`), entry points (`run`, `captureState`), and data (`config`, `results`): Pass A: deleting them removes layout QA checks with no shipped caller and no player-visible effect (its `spinnerCheck` even reaches for `window.campaignWizard`, a dev-only probe). Pass B: developer QA tooling is not player transport or presentation — DELETE, all members.

**`js/test_planning_block_parsing.js` — DELETE (whole file; Phase 2 now complete).** `decodeHtmlEntities`, `sanitizeHtml`, `escapeHtmlAttribute`, `parsePlanningBlocksJson`, `queryHTML`, `sanitizeIdentifier`, and `PlanningBlockTestSuite` (`constructor`, `test`, `assert`, `assertContains`, `assertNotContains`, `run`) plus the self-executing `suite.run()` and the `module.exports` of `parsePlanningBlocksJson`/`PlanningBlockTestSuite`: Pass A: deleting them removes a self-contained test harness whose subject (planning-block parsing) already ships in `streaming.js` and `app.js`, and which no shipped page loads (its only self-reference is its own run comment). Pass B: a test harness in the served directory duplicates shipped parsing logic without serving a player — DELETE from the shipped directory, all members (assertions, if kept, belong in `tests/`). Note the `app.js` copies of `decodeHtmlEntities`/`sanitizeHtml`/`escapeHtmlAttribute`/`sanitizeIdentifier`/`parsePlanningBlocks` are live reader code and are KEEP under §8.1 above; only these unloaded copies go.
### 8.2 Test files — verdict by function, grouped by file

Grouping rule, stated exactly: within one file, all `test()`/`it()` calls are grouped into a single row because they are trivially parallel — same subject file, same subject code under test, same Pass A/B reasoning, same verdict — except the two files split per test below the table. Counts are `test(`+`it(` matches in the local file; three files contain no `test()` calls and instead run node `assert` blocks, noted as such. Many files open with a `(skipped: jsdom not installed)` guard test; the verdict rests on the file's substantive tests, and the skip guard itself changes nothing (it asserts nothing about the product when jsdom is absent). Run 1 cluster verdicts are preserved except the two corrections flagged here and in §10: the three mock-structure files are KEEP (their targets are the shipped `index.html`/CSS geometry, not ghost mocks), and `faction_objective_rendering.test.js` — unlisted in run 1's cluster names — is KEEP (see its row).

| File | n | Verdict | Basis (first test / subject) |
|---|---|---|---|
| `auth_domain_resolution.test.js` | 8 | KEEP | production custom domain resolves authDomain to the serving origin |
| `auth_ios_persistence.test.js` | 4 | KEEP | persistence is set to LOCAL before the auth observer is registered |
| `auth_mobile_redirect.test.js` | 25 | KEEP | getRedirectResult() is called once on init after persistence settles |
| `avatar_crop_zone_overflow.test.js` | 4 | KEEP | avatar.css declares an .avatar-crop-zone block |
| `campaign_create_nav_before_avatar.test.js` | 2 | KEEP | campaign create navigates before background avatar persist |
| `campaign_wizard_ai_avatar_size.test.js` | 2 | KEEP | handleAvatarFile rejects manual uploads over 5MB |
| `campaign_wizard_avatar_launch.test.js` | 2 | KEEP | commitWizardPortraitPreview stores preview URL ref without avatarFile |
| `campaign_wizard_default_order.test.js` | 15 | KEEP | first .campaign-type-card is Custom, second is Dragon Knight |
| `campaign_wizard_dragon_knight_canonical.test.js` | 1 | KEEP | dragon-knight campaign type fills description from canonical source |
| `campaign_wizard_dragon_knight_submit.test.js` | 4 | KEEP | Dragon Knight submit preserves edited description text |
| `campaign_wizard_scroll_indicator.test.js` | 26 | KEEP | isMobileViewport: true on a 390-wide viewport via matchMedia stub |
| `campaign_wizard_step2_no_duplicate_enter.test.js` | 5 | KEEP | wizard template contains exactly one <button id= |
| `campaign_wizard_url_prefill_race.test.js` | 16 | KEEP | applyUrlParams() populates custom inputs and stashes instance variables |
| `choice_detail_inline.test.js` | 8 | KEEP | choice_detail_inline (skipped: jsdom not installed) |
| `choice_token_story_display.test.js` | 5 | KEEP | choice_token_story_display (skipped: jsdom not installed) |
| `client_asset_load_failed.test.js` | 1 | KEEP | production streaming path does not fabricate asset terminal evidence |
| `collapsible_debug_panels_dom.test.js` | 9 | KEEP | collapsible_debug_panels_dom (skipped: jsdom not installed) |
| `composer_bounded_correction.test.js` | 14 | KEEP | composer_bounded_correction (skipped: jsdom not installed) |
| `composer_choices_mobile_cap.test.js` | 4 | KEEP | mobile inline choices have no height cap or nested auto-scroll |
| `debug_mode_implicit_cache.test.js` | 5 | KEEP | generateStructuredFieldsPostNarrative renders implicit cache hit rate in debug m |
| `debug_mode_initial_load.test.js` | 2 | KEEP | initial story load reads top-level debug_mode fail-closed |
| `default_gemini_fallback.test.js` | 1 | KEEP | app fallback matches the server Gemini default when constants fetch fails |
| `desktop_choice_shortcuts.test.js` | 5 | KEEP | desktop_choice_shortcuts (skipped: jsdom not installed) |
| `desktop_mock_structure.test.js` | 7 | KEEP | desktop header is a flush 52px row: no padding, margin or divider width |
| `desktop_room.test.js` | 6 | KEEP | desktop_room (skipped: jsdom not installed) |
| `diagnostics.test.js` | 30 | KEEP | diag.event appends to the buffer |
| `faction_objective_rendering.test.js` | 3 | KEEP | renders persisted objective with current_objective precedence |
| `fetchapi_public_optin.test.js` | 4 | KEEP | fetchApi({public: true}) sends NO Authorization header to the backend |
| `first_turn_coach.test.js` | 27 | KEEP | first_turn_coach (skipped: jsdom not installed) |
| `first_turn_coach_auth_race.test.js` | 8 | KEEP | normal startup waits for auth initialization rather than reading local storage |
| `header_avatar_mount.test.js` | 6 | KEEP | header avatar mount (skipped: jsdom not available) |
| `header_hud_layout.test.js` | 19 | KEEP | header_hud_layout (skipped: jsdom not installed) |
| `hud_menu_mobile_qa.test.js` | 22 | KEEP | hud_menu_mobile_qa (skipped: jsdom not installed) |
| `inline_editor_comment_accuracy.test.js` | 5 | KEEP | source files exist and are readable |
| `inline_editor_mobile_width.test.js` | 10 | KEEP | InlineEditor.startEdit() inserts editContainer as adjacent sibling for #game-tit |
| `inline_play_completion_gaps.test.js` | 9 | KEEP | inline_play_completion_gaps (skipped: jsdom not installed) |
| `instrumentation.test.js` | 10 | KEEP | auth.js emits all 37 instrumentation points claimed in the PR |
| `interaction_draft_persistence.test.js` | 34 | KEEP | level-up Finish submits its story choice and keeps the unrelated draft |
| `keep_reading_scroll_only.test.js` | 8 | KEEP | keep_reading_scroll_only (skipped: jsdom not installed) |
| `keyboard_inset.test.js` | 7 | KEEP | keyboard_inset (skipped: jsdom not installed) |
| `latest_turn_choices_inline.test.js` | 31 | KEEP | latest_turn_choices_inline (skipped: jsdom not installed) |
| `mode_switch_hide_choices_and_wrap.test.js` | 7 | KEEP | mode_switch_hide_choices_and_wrap (skipped: jsdom not installed) |
| `mode_tooltips_and_hints.test.js` | 11 | KEEP | mode_tooltips_and_hints (skipped: jsdom not installed) |
| `narrative_markdown_render.test.js` | 22 | KEEP | narrative_markdown_render (skipped: jsdom) |
| `narrative_prose_layout.test.js` | 6 | KEEP | narrative_prose_layout (skipped: jsdom) |
| `narrative_streaming_blocks.test.js` | 15 | KEEP | narrative_streaming_blocks (skipped: jsdom) |
| `narrative_streaming_handoff.test.js` | 52 | KEEP | narrative_streaming_handoff (skipped: jsdom) |
| `no_campaign_redirect.test.js` | 5 | KEEP | SPA dashboard routing redirects to /new-campaign if user has 0 campaigns |
| `opening_story.test.js` | 28 | KEEP | needsOpeningStory only for non-ready statuses; absent means ready |
| `opening_story_avatar_persist_race.test.js` | 5 | KEEP | onStreamStarting fires before sendMessage resolves (stream POST begins) |
| `opening_story_resume.test.js` | 12 | KEEP | after done the reload shows the persisted opening without a second overlay |
| `openrouter_byok_cta.test.js` | 9 | KEEP | stored OpenRouter credential counts as an active key |
| `openrouter_finish_states.test.js` | 8 | KEEP | error is read before flow: rate_limited without a flow is unavailable |
| `openrouter_oauth.test.js` | 42 | KEEP | account-link action starts a separate server-owned link flow |
| `openrouter_status_contrast.test.js` | 1 | KEEP | status color overrides never apply outside the fantasy theme |
| `outcome_verdict.test.js` | 4 | ADAPT | see per-test split below the table |
| `phone_mock_structure.test.js` | 8 | KEEP | narrow desktop and mobile game view collapses site navbar and places theme toggl |
| `planning_block_text_size.test.js` | 3 | KEEP | --composer-choice-font token equals 1rem (16px at base, matches narrative) |
| `planning_choices_composer.test.js` | 11 | KEEP | interactiveOnly emits clickable .choice-button elements |
| `planning_choices_composer_workflow_contract.test.js` | 1 | KEEP | CI runs the collapsible debug DOM contract on PRs and dev pushes |
| `planning_composer_dom.test.js` | 57 | KEEP | planning_composer_dom (skipped: jsdom not installed) |
| `play_screen_overlap_contracts.test.js` | 17 | KEEP | Add Avatar placeholder paints nothing outside its 44px header circle |
| `portrait_ai_auto_suggest.test.js` | 1 | KEEP | openDirectToAi auto-loads campaign suggestion |
| `portrait_ai_compare_models.test.js` | 3 | ADAPT | see per-test split below the table |
| `portrait_ai_first_open.test.js` | 1 | KEEP | first in-game open waits for new modal panel before auto-suggest fills |
| `portrait_ai_first_open_segment.test.js` | 1 | KEEP | first open via AI segment auto-suggests after modal create |
| `portrait_ai_loading.test.js` | 4 | KEEP | postJson aborts hung requests and surfaces timeout message |
| `portrait_ai_modal_reset.test.js` | 1 | KEEP | opening portrait choice clears a prior campaign description |
| `portrait_ai_nodelist_segment.test.js` | 1 | KEEP | AI segment click auto-suggests when choice buttons are a NodeList |
| `portrait_ai_panel_suppression.test.js` | 1 | KEEP | openPortraitChoice marks body portrait-modal-active and suppresses wizard host |
| `portrait_ai_refresh_suggest.test.js` | 2 | KEEP | refresh button forces a new suggest request and replaces cached text |
| `portrait_ai_suggest_timeout.test.js` | 1 | KEEP | auth header timeout clears shimmer and surfaces Try again |
| `portrait_ai_use_preview.test.js` | 2 | KEEP | previewResultToFile uses server fetch-preview for GCS preview URLs |
| `portrait_ai_wizard_prefetch_dedupe.test.js` | 1 | KEEP | ensurePortraitSuggestionFilled awaits in-flight prefetch without second POST |
| `portrait_default_and_display_scale.test.js` | 4 | KEEP | wizard defaults avatar source mode to AI with AI segment first and active |
| `quick_start_auto_redirect.test.js` | 3 | KEEP | First-time user (0 campaigns) auto-redirects to /new-campaign (not /quick-start) |
| `quick_start_banner_reshow_symmetry.test.js` | 1 | KEEP | a dismissal on campaign A does not leave the banner permanently hidden for campa |
| `quick_start_button.test.js` | 4 | KEEP | Quick Start button click does not POST and redirects to /new-campaign |
| `quick_start_dashboard_param_preservation.test.js` | 4 | KEEP | wordmark link href preserves test_mode/test_user_id and strips qs when the game |
| `quick_start_shared_helpers.test.js` | 12 | KEEP | scrollToCharacterCreation scrolls to the second story entry (character-creation |
| `quickstart_url_capu1.test.js` | 3 | KEEP | /quickstart (no hyphen) redirects to /new-campaign without POSTing to /api/campa |
| `quota_banner.test.js` | 7 | KEEP | updateQuotaBanner: hides banner when data is empty or missing quota fields |
| `redirect_param_allowlist.test.js` | 10 | KEEP | a real share link is restorable |
| `review_save_failed_request_id.test.js` | 1 | KEEP | failed regular interaction marks review save failed with the resolved request id |
| `rewards_box_level_up_banner_rendering.test.js` | 24 | KEEP | renders canonical living-world event title and description |
| `scene_illustration_poll.test.js` | 20 | KEEP | poll renders the ready image once the server reports ready |
| `scene_illustration_ui.test.js` | 0 | KEEP | node assert block (no test() calls): slot render + XSS escaping |
| `scene_settings_admin_visibility.test.js` | 13 | KEEP | settings template keeps the simple toggle public and gates scene mode and advanc |
| `settings_indicators_migration.test.js` | 10 | KEEP | game-view header no longer carries #debug-indicator |
| `settings_listeners.test.js` | 80 | KEEP | makeElement.click returns cross-realm onclick promises |
| `share_token_prefill_ip_wizard_9727.test.js` | 14 | KEEP | applyUrlParams with share_token leaves absent structured fields empty even when |
| `spicy_header_indicator.test.js` | 2 | KEEP | scene-line chili starts hidden and has an accessible name |
| `stats_features_rendering.test.js` | 10 | KEEP | renders structured features with names and descriptions cleanly |
| `story_pagination_identity_race.test.js` | 1 | KEEP | same identity appends history stamped with current debug capability |
| `streaming_beacon_auth.test.js` | 3 | KEEP | beaconClientStreamLatency: authenticated caller sends via fetch with Authorizati |
| `streaming_completion_phantom_dice_roll.test.js` | 26 | KEEP | streaming_completion_phantom_dice_roll (skipped: jsdom not installed) |
| `streaming_error_surfacing.test.js` | 22 | KEEP | streaming_error_surfacing (skipped: jsdom not installed) |
| `streaming_extraction.test.js` | 57 | KEEP | _extractPlanningThinking: extracts complete thinking from full JSON |
| `streaming_paragraph_stability.test.js` | 2 | KEEP | streaming_paragraph_stability (skipped: jsdom) |
| `streaming_telemetry_boundary.test.js` | 20 | KEEP | streaming telemetry boundary (skipped: jsdom) |
| `submit_expand_scroll_bugs.test.js` | 12 | KEEP | focus-collapse wiring is absent |
| `system_notice_theme_tokens.test.js` | 3 | KEEP | notice markup in app.js carries no inline light colors |
| `test_campaign_export_ui.test.js` | 5 | KEEP | source files exist and are readable |
| `test_inline_editor_no_duplicate.test.js` | 5 | KEEP | InlineEditor exposes a static attachOrReplace helper (issue #9116 fix) |
| `test_ip_tv_show_wizard.test.js` | 13 | KEEP | generateWizardHTML: includes all 6 TV show / IP wizard fields |
| `test_issue_9498_long_prompt_keepalive.test.js` | 4 | KEEP | issue #9498 — network-drop retry strips keepalive so iOS Safari opens a fresh TC |
| `test_quick_start_banner_dismiss_pycqp.test.js` | 3 | KEEP | Lane 2 / rev-pycqp: X dismisses the banner and persists qs_banner_dismissed:<cam |
| `test_quick_start_resume_scroll_0vsxl.test.js` | 4 | KEEP | resolveNewCampaignScrollTarget: qs=1 wins even when isNewCampaign is false (post |
| `test_quick_start_scroll_ectdj.test.js` | 3 | KEEP | scrollToCharacterCreation lands on the SECOND story entry (character-creation di |
| `test_quick_start_wizard_click_8ce37.test.js` | 1 | KEEP | dashboard Quick Start button is disabled and redirects without POSTing |
| `test_resume_campaign_stream_race.test.js` | 0 | KEEP | node assert block (no test() calls): resumeCampaign async ownership |
| `test_wizard_setting_visible_on_dragon_knight.test.js` | 7 | KEEP | wizard HTML has a VISIBLE Setting textarea, not a hidden input |
| `timer_info_debug_only.test.js` | 6 | KEEP | timer_info_debug_only (skipped: jsdom) |
| `tooltip_guide_bootstrap.test.js` | 13 | KEEP | MCP bridge preserves authTokenManager authorization on late hydration |
| `turn_lock_until_server_turn_ends.test.js` | 8 | KEEP | a failed stream holds the lock while the server turn is in flight, then releases |
| `turn_mode_label.test.js` | 8 | KEEP | turn_mode_label (skipped: jsdom) |
| `undo_story_idtoken.test.js` | 17 | KEEP | handleUndoStory does not surface the swallowed |
| `user_lifecycle_telemetry.test.js` | 10 | KEEP | creates separate bounded visitor and tab-session identities and emits entry fact |
| `waitlist_access.test.js` | 19 | KEEP | auth homepage copy advertises request waitlist in waitlist mode |
| `test_mobile_input_focus_collapses_choices.cjs` | 3 | KEEP | mobile_input_focus_collapses_choices (skipped: jsdom not installed) |
| `test_tooltip_guide_e2e.js` | 14 | KEEP | tooltip guide E2E (skipped: jsdom not available) |
| `test_tooltip_guide_unit.js` | 0 | KEEP | node assert block (no test() calls): static tooltip-guide checks |

Totals: 122 files, 1,268 `test()`/`it()` calls (1,265 KEEP, 3 DELETE as split below), plus 3 assert-block files (KEEP). Per-test splits:

- `outcome_verdict.test.js` (4 tests) — ADAPT as a file: `aggregates roll results` DELETE and `no label without usable rolls; saves excluded` DELETE (both guard the roll-aggregation fallback that §2/§5 verdict DELETE); `explicit player_outcome wins` KEEP and `badge html is accessible` KEEP (explicit-outcome display plus accessibility of the badge). Pass A: the badge survives without the fallback. Pass B: only the explicit branch is presentation of a server-authored verdict.
- `portrait_ai_compare_models.test.js` (3 tests) — ADAPT as a file: `compare control is not rendered for non-debug users` KEEP (suppression behaviour), `debug compare generates both models side by side and only saves the picked one` DELETE with `portrait_model_compare.py` (it guards the debug double-generation subject), `app.js passes debugMode into the in-game portrait dialog` KEEP (debugMode plumbing is used beyond compare). Pass A: deleting the generation test removes a guard on deleted behaviour only. Pass B: tests author no domain value; they follow their subjects.

Test-support files (Phase 2, all KEEP as tooling — they never ship to players and author no domain value): `helpers/extract_fn.js` — `extractFn`, `reviewStateSource` (extract a named function body from a source file for tests; deleting it breaks tests that run production code in a VM, not the product); `helpers/jsdom_loader.js` — `loadJsdom` (optional jsdom loader behind the skip guards); `helpers/narrative_helpers.js` — `loadUmdCode`, `loadNarrativeUmds` (load narrative UMD bundles into a sandbox); `helpers/streaming_test_harness.js` — `createStreamingHarness` plus inner `flushAnimationFrames` (DOM double + streaming harness); `fixtures/streamed_social_turn_chunks.json` — recorded chunk events from one real Gemini SDK social-persuasion turn (`source` + `chunks` with `t_ms`/text), the streaming-extraction fixture; repro files are covered in §8.5.


### 8.3 CSS rule detail and HTML element detail (shipped files)

Verdict method for CSS/HTML: verdict by rule/element cluster where individual rules are not meaningfully separable, and this paragraph says so — a stylesheet's rules share one purpose (e.g. all fantasy-theme overrides), and an HTML view's elements form one container, so per-rule/per-element verdicts would repeat the same Pass A/B reasoning hundreds of times. Every file below is therefore verdict-ed cluster by cluster, with all clusters named; unsectioned rules are grouped with their nearest commented section. All shipped CSS clusters are pure presentation (no rule computes, filters, or rewrites a campaign value), so all are KEEP except the already-DELETE `parallel_dual_pass.css`. Two cautions are recorded, not new verdicts: `style.css` defines some structured-field backgrounds twice (noted in `themes/fantasy.css` itself), and `style.css` at 3,089 lines is a bundling/minification question, not a ZFC question (same as §2).

- `style.css` (3,089 lines) — KEEP, all clusters: logged-out nav override; scrollable textarea; debug-mode styles (presentation of debug state, behind the debug flag per §8.1); dice-roll styling; story-entry container; session snapshot wrapping (explicitly preserves server text); planning-block styling; structured-fields styling (God Mode, entities, location, dice, system warnings, rewards box, system notices/level-up banner, equipment display, state updates, planning block, choice buttons, debug info, DM notes, state rationale); mechanics-hidden outcome-card collapse; OpenRouter/BYOK CTA styling incl. fantasy overrides; view management + game-view viewport/keyboard/scrollbar guards; inline-coach visuals; chili-slot reservation; phone/landscape/narrow-desktop responsive rules; narrative prose; streaming layout/badge/skeleton/caret; icon buttons; navbar/brand; campaign-list styling; splash/logged-out view; dragon background; cards; welcome sign-in buttons; rate-limit modal; wiki/Reddit/Discord nav links; Dragon Knight locked-input styles; creation CTA pair + glass sheen + shimmer. Pass A: deleting any cluster unstyles or mislays its surface. Pass B: layout, colour, and responsive rules present existing elements — KEEP.
- `css/avatar.css` (1,138 lines) — KEEP, all clusters: upload zone (wizard step); in-game modal owns portrait panel / hide wizard duplicates; in-game crop overlay (viewport-height cap, the `avatar_crop_zone_overflow` test's subject); hidden file input; upload preview; change-photo chip; remove overlay; constraints text; skip hint; in-game thumbnail; default placeholder; player message row avatar; expanded avatar card overlay; header HUD avatar; avatar action buttons; empty-state add-avatar circle; mobile header scaling; toast; mobile responsive; upload-in-flight spinner. Pass A: deleting any cluster breaks avatar presentation/framing. Pass B: pure presentation of player-supplied or server images — KEEP.
- `css/inline-editor.css` (238 lines) — KEEP, all clusters: edit container; button container; error display; campaign-specific styles; game-view title editing; dashboard campaign-list editing; fantasy focus ring + invalid-state ring; responsive adjustments; smooth-transition animation; save-button loading state. Pass A: deleting them unstyles in-place editing. Pass B: pure presentation — KEEP.
- `css/pagination-styles.css` (125 lines) — KEEP, all clusters: story pagination; smooth scroll indicator; loading animation; pagination info animation; load-more button states; error styling; responsive adjustments. Pass A: deleting them unstyles pagination controls. Pass B: pure presentation of the stored log — KEEP.
- `css/tooltip-guide.css` (98 lines) — KEEP, single cluster: legacy guide presentation sharing the inline-coach palette. Pass A: deleting it unstyles legacy guide cards. Pass B: pure presentation — KEEP.
- `styles/animations.css` (384 lines) — KEEP, all clusters: animation variables; view transitions; active-view animations; loading overlay; button hover/loading; form focus; campaign-card hover; dropdown; modal + backdrop; spinner; story loading; checkbox/radio; link hover; navbar brand; campaign-list stagger; reduced-motion respect; GPU acceleration; story text appear; timer pulse. Pass A: deleting them removes transitions/animations only. Pass B: pure presentation, with reduced-motion kept as accessibility — KEEP.
- `styles/bridge.css` (33 lines) — KEEP, clusters: CSS-variable bridge (old → new design system) + fantasy adjustments. Pass A: deleting it breaks token mapping for older rules. Pass B: pure presentation tokens — KEEP.
- `styles/components.css` (583 lines) — KEEP, all clusters: typography reset; cards (incl. glass variant); buttons (primary/secondary/success/danger/outline/sizes); form controls + select; list group; modal; navbar; dropdown; badge; alert; progress; spinner; text/background utilities; fantasy special effects; rate-limit modal + soft-warn banner + primary CTA + BYOK hint spacing. Pass A: deleting them unstyles shared components. Pass B: pure presentation — KEEP.
- `styles/enhanced-components.css` (694 lines) — KEEP, all clusters: button base/hover/variants; ripple container; button loading state; list-group campaign items; form controls/labels/checkboxes/radios/input groups; modals; story content area; shadows/gradients/glass; dropdown interference guards; focus indicators; reduced-motion support; toggle-switch track/thumb + dark override; mobile collapsible campaign filters. Pass A: deleting them unstyles enhanced components (note: this sheet is loaded even though `component-enhancer.js` is not — the CSS is live presentation, the JS is dead; their fates differ and are verdict-ed separately). Pass B: pure presentation — KEEP.
- `styles/globals.css` (230 lines) — KEEP, clusters: design tokens (light-theme colours, palette, gradients, shadows, radius, typography scale, spacing, z-index, animation, backdrop filters, glass/shadow/radius/gradient aliases) + fantasy "Arcane Scholar" token set. Pass A: deleting them removes the token system other sheets depend on. Pass B: pure presentation data — KEEP.
- `styles/interactive-features.css` (960 lines) — KEEP, all clusters: modern-mode gating; wizard layout (scrollable step content, pinned navigation); wizard progress + step indicators; wizard steps; personality cards; campaign-type cards; option cards; campaign preview; editable preview items; launch actions; wizard navigation; mobile stacking; TV/IP wizard styling; campaign-list enhancements; mobile title improvements; checkbox alignment fixes; wizard scroll-indicator chevron (fade masks, bounce, GH-8015 scroll-container rules). Pass A: deleting them unstyles wizard/interactive surfaces. Pass B: pure presentation — KEEP.
- `styles/planning-blocks.css` (1,025 lines) — KEEP, all clusters: planning-block choice buttons; composer choice-type token (one token drives choice scale); thinking-text paragraphs; collapsed vertical space; per-row disclosure; expanded choice-title wrapping. Pass A: deleting them unstyles planning/thinking blocks rendered during streaming. Pass B: pure presentation of server-authored planning content — KEEP.
- `themes/base.css` (111 lines) — KEEP, single cluster: core layout/structure applying default-theme variables. Pass B: pure presentation — KEEP.
- `themes/default.css` (110 lines) — KEEP, clusters: default-theme custom properties (backgrounds, text, accent, borders, panel/character info, buttons, system notices, shared play-control token contract). Pass B: pure presentation tokens — KEEP.
- `themes/fantasy.css` (1,121 lines) — KEEP, all clusters: "Arcane Scholar" palette + tokens (backgrounds, WCAG-AA text, gold accent, purple decoration, 3:1 borders, buttons, shared play-control contract); ember-canvas fallback; transparent logged-out/game containers; story transparency; campaign-list dark styling; title/timestamp/form/heading styling; structured-field dark overrides (noting style.css's double definition); legacy choice states; character info; separators; login transparency; frosted-glass cards; white Google button; standalone settings route; wizard alignment; "Begin Adventure" purple primary; dark alert-danger. Pass A: deleting them removes the selectable fantasy theme. Pass B: pure presentation — KEEP.
- `campaign-click-fix.css` (55 lines), `loading-messages.css` (138 lines) — KEEP, single cluster each (clickability fix; loading-message styling), as §2 — KEEP.
- `parallel_dual_pass.css` (75 lines) — DELETE with its JS companion (§2/§8.1): styles for an enhancement indicator no shipped page renders — KEEP of the file would be unreferenced presentation, which is not presentation.
- `index.html` (718 lines) — KEEP, by element cluster: `<head>` (meta, title, all shipped CSS/JS/Firebase/CDN references — the load manifest that proves §9(a)); hidden `agent-readable-summary` main; navbar (brand, wiki/Reddit/Discord links, theme switcher, user menu); `loading-overlay`; `main-content` views — `auth-view`/`auth-container` (logged-out/welcome), `dashboard-view`/`campaign-list` (incl. `data-tooltip-id="play-cta"` and `"settings-shortcut"` targets), `new-campaign-view`/`new-campaign-form` (description container, wizard host), `game-view` (first-run banner, header avatar slot, HUD subline, BYOK CTA, HUD more/menu, `story-content`, stream status, timer info, `interaction-form` with `data-guide-id="first-game-tour"`, first-turn coach note, composer stack, pending status, loading spinner); `avatar-overlay`; share-story sections (normal + legacy confirm); modals/overlays referenced by `app.js`; footer/legal links (`/privacy`, `/terms` via `terms-of-use.html`). Pass A: deleting any cluster removes a view or its controls. Pass B: markup plus script/style references are transport/presentation, not domain logic — KEEP. No script tag in this file references any §9(a) file (verified in §9).
- `terms-of-use.html` (71 lines) — KEEP, clusters: header/brand + "How to start" sections (the file carries a duplicated `<h1>` brand block, a cosmetic duplication, not a verdict change). Pass A: deleting it removes the legal terms page. Pass B: static legal presentation — KEEP.

### 8.4 Root `_ui_mocks/` — Phase 2 (beyond Phase 1 file verdicts)

Phase 1 verdict for the whole directory was ADAPT (move to a design archive outside the product tree); run 2 confirms that verdict at element/function level and adds one correction: run 1 said the mocks have "no JS functions to audit beyond their markup" — that is true for five of six mocks but false for the sixth (see bottom-sheet row). Shared CSS clusters are verdict-ed once here, not per mock.

- `_ui_mocks.css` — ADAPT (move with the mocks): clusters header; main; hero (Mock B); shelf 3-card row (A/E); trio vertical cards (B); generic card; per-setting emoji placeholders; UGC badge + top banner (C/E, reusable as footer on A/B/D); buttons/CTAs; dashboard (A/D); catalog grid (A/D); featured banner (D); mini-home (D homepage); page (D `/campaigns`); resume/strip (B); wizard tile picker (C); tabs (E); footer mock notes; responsive. Pass A: deleting it unstyles all six mock pages and nothing shipped. Pass B: mock-only presentation is not product presentation — ADAPT: move to the design archive.
- `mock_A_premade_shelf.html` — ADAPT (move): elements "Premade Campaigns" hero/shelf, "My Campaigns", "All Premade Campaigns" catalog; no `<script>` functions. Pass A/B: a design variant, not a shipped UI — ADAPT: move to the archive.
- `mock_B_premades_are_dashboard.html` — ADAPT (move): hero "Pick a story. Play in 30 seconds." + 3 hero cards (Dragon Knight, The Skywalker's Choice, Dragon's Crucible) + strip of 5; no `<script>` functions — ADAPT: move to the archive.
- `mock_C_wizard_tile_picker.html` — ADAPT (move): "Start a New Campaign" tile picker replacing radio buttons (README's recommended variant, ~0.5 day, starred); no `<script>` functions — ADAPT: move to the archive, noting the recommendation survives as a design decision, not as shipped code.
- `mock_D_dedicated_page.html` — ADAPT (move): "My Campaigns" + "Premade Campaigns" dedicated `/campaigns` page variant; no `<script>` functions — ADAPT: move to the archive.
- `mock_E_tabs.html` — ADAPT (move): Tabs (Premades | Mine | Custom) variant with continue pin; no `<script>` functions — ADAPT: move to the archive.
- `mock_mobile_bottom_sheet_choices.html` — ADAPT (move), with the run-1 correction: this mock DOES contain JS — `CHOICES_DATA` (3 choices with title/risk/desc/pro/con, incl. DC checks and a "CS +25%" pro line) plus `openSheet(index, trigger)`, `closeSheet()`, `confirmAction()`, `quickSelect(text)`, and an Escape-key listener, rendering a ~75%-viewport bottom sheet with description, DC check, pros/cons, and Confirm into a `mockInput`. Pass A: deleting it removes a design mock only; the shipped mobile choice UI does not render it. Pass B: the mock's choice data is invented design copy (including a fabricated +25% figure) presented as if it were a game outcome — exactly why it must never be wired into the product — and its functions are mock-only presentation — ADAPT: move to the archive with the other mocks, and never promote `CHOICES_DATA` into product code. File verdict unchanged (ADAPT), but the "no JS" claim in §6 item 11 is corrected.
- `_ui_mocks/README.md` — ADAPT (move with the directory), as §7; no functions to verdict.

### 8.5 Test-support remainder: emulator repro, device evidence, screenshots

- `tests/mobile_auth_emulator_repro/emu_app.html` (84 lines) — KEEP as tooling: `setStatus(s)`, `isMobileUserAgent()`, `onAuthStateChanged` handler + `getRedirectResult()` chain, sign-in click handler (`signInWithRedirect`, popup fallback). Pass A: deleting it removes the minimal repro app that demonstrates the iOS WebKit cross-site auth failure. Pass B: repro tooling authors no domain value and never ships — KEEP.
- `tests/mobile_auth_emulator_repro/proxy_server.mjs` (49 lines) — KEEP as tooling: a top-level `http.createServer` callback (no named functions) serving `emu_app.html` at :8799 and proxying everything else to the auth emulator at :9099, making the handler first-party (the GREEN topology). Pass A/B: as above — KEEP.
- `tests/mobile_auth_emulator_repro/emu_e2e.mjs` (122 lines) — KEEP as tooling: `log(...)` plus the Playwright/WebKit RED/GREEN driver flow. Pass B: repro driver, no domain value — KEEP.
- `tests/mobile_auth_emulator_repro/run_repro.mjs` (105 lines) — KEEP as tooling: `waitForPort(port, path, tries, delayMs)`, `run(env)`, `resolves(host)`, `cleanup()`. Pass B: repro orchestration — KEEP.
- `tests/mobile_auth_emulator_repro/firebase.json` — KEEP as tooling: emulator config only (auth host 127.0.0.1:9099, UI disabled) — KEEP. Repro `.gitignore` + `README.md` — KEEP as tooling docs (the README also documents the repro's open caveats: incognito specificity unclosed, real-Google-IdP prod confirmation still manual).
- `tests/mobile_auth_emulator_repro/device_evidence/` — KEEP as evidence (all 6 entries): `README.md` (iPhone 16 Plus simulator, iOS 18.6, real iOS WebKit + real ITP; RED cross-site `sslip.io` → `READY_NO_PENDING_REDIRECT`, not signed in; GREEN same-origin `nip.io` → `REDIRECT_RESULT_USER:<uid>`, signed in; plus an honestly recorded transient GREEN stall cleared by relaunching MobileSafari); `ios_sim_RED_01_handler_on_sslip-io_crosssite.png` (1290×2796 PNG), `ios_sim_RED_02_FAIL_ready_no_pending_redirect.png` (1290×2796 PNG), `ios_sim_GREEN_01_handler_on_nip-io_sameorigin.png` (1290×2796 PNG), `ios_sim_GREEN_02_PASS_redirect_result_user.png` (1290×2796 PNG), `ios_sim_auth_repro_red_to_green.gif` (540×1290 GIF). Pass A: deleting them removes the only real-device-engine evidence for the same-origin-handler fix. Pass B: evidence images author no domain value and never ship — KEEP. (The UID string inside the GREEN screenshots/README is a test-account emulator UID from the repro, not a player credential; it is evidence text, not a secret to act on.)
- `tests/mobile_auth_emulator_repro/screenshots/` — NO VERDICT NEEDED, confirmed empty: the directory contains only a 0-byte `.gitkeep` and no screenshots. Run 1 §6 item 13 is closed as "empty", not as "contents verdict-ed".

## 9. Verification results (run-1 caveats, resolved from the local copy)

- (a) **Does `mvp_site/main.py` dynamically load the five unreferenced files? VERIFIED: NO.** Searched `mvp_site/main.py`, `mvp_site/frontend_release.py`, `mvp_site/frontend_cutover_flag.py`, `frontend_v1/index.html`, all shipped `frontend_v1/*.js` and `frontend_v1/js/*.js` for the basenames `parallel_dual_pass`, `component-enhancer`, `visual-validator`, `test_planning_block_parsing`, `mock_header_avatar`. Hits: only (i) each file's own content/self-reference, (ii) a `themeChanged` comment in `theme-manager.js` mentioning `component-enhancer` as an example listener (it dispatches an event; it does not load the file), and (iii) an unrelated `settings.js` value `"parallel"` in a scene-mode normaliser. `main.py`'s serving route (`/frontend_v1/<path:filename>`, `send_from_directory`) is generic: it serves any file under the selected frontend folder on direct request, and it names no asset except the tooltip kill-switch assets (`js/tooltip-guide.js`, `css/tooltip-guide.css`). It never constructs, imports, or injects any of the five names, and `frontend_release.py`'s referenced-asset inventory names none of them. Consequence, stated precisely: the five files are **never loaded by the shipped page or app**, but they **are retrievable by direct URL** while they sit in the served directory — which strengthens, not weakens, the DELETE verdicts (removal from the shipped directory is the fix; a loader change is not needed). Update (repo-wide grep completed after the first §9 draft): a full-tree grep for the five basenames finds only documentation/README/deep-dive mentions (including `mvp_site/PARALLEL_DUAL_PASS_INTEGRATION.md`, which describes a legacy `static/` layout and a `main_parallel_dual_pass.py` that does not exist in this local tree), a docstring mention in `mvp_site/tests/test_css_variable_coverage.py` (whose test reads `styles/globals.css` and loads no enhancer JS), and one historical evidence page (`repro/evidence/quota_banner_modal_cta_2026_06_30/demo.html`) linking `/parallel_dual_pass.css` — an evidence artifact, not a shipped page. None of these is a loader, and none changes any DELETE verdict.
- (b) **Does `document_generator` choice-matching use stored keys? VERIFIED: NO — it uses prose inference, so the run-1 ADAPT stands and the fallback must go.** `_find_matching_choice_key(user_normalized, user_title, choices)` (lines ~260–304) first honours an explicit `choice:` prefix against stored keys (that one branch IS a stored-key lookup and is the only part worth keeping), but then falls through to four prose-inference methods: direct `startswith` of the normalised choice text, choice-text-starts-with-user-title, exact title equality, and title-before-`" - "` equality — all comparing the player's free text against stored choice *text* to recover a key the player never supplied. `_get_choice_by_key` itself is a pure stored-key/dict-id lookup and stays; `get_choice_type`/`get_selected_choice` inherit the inference through `_find_matching_choice_key`. Pass B conclusion: the inference branches re-derive which stored choice was taken from prose, which is exactly the recomputation the run-1 ADAPT ordered deleted; keep only the `choice:`-prefix stored-key branch (plus `_get_choice_by_key`), and let the model supply the choice key through the log/schema when no prefix is present.
- (c) **Does `equipment_display._classify_backpack_item` use name branches? VERIFIED: YES — extensively, so the run-1 "keep verbatim" proviso FAILS and the function must change.** `_classify_backpack_item(name, stats)` (lines ~246–352) classifies purely from lower-cased name+stats substrings, in order: Documents (document/ledger/cipher/letter/scroll/note/journal/book/tome/manuscript/deed/contract), Keys (key/bypass/lockpick/access), Signets & Rings (signet/ring), Currency (coin/gold/platinum/gem/jewel/currency/purse), Resources (shard/crystal/soul/essence/potion), Tools (kit/tools/thieves/disguise/artisan/instrument), Magical Items (magical/artifact/enchanted/+1/+2/+3/dc/spell/arcane/focus/lens/scepter/amulet, evaluated before weapons so e.g. "Wand of Magic +1 spell DC" lands as magical, with dice notation stripped first via `DICE_PATTERN`), Weapons (dagger/sword/rapier/crossbow/bow/staff/wand/d4–d12/piercing/slashing/bludgeoning), Apparel (clothes/robe/cloak/boots/gloves), Instruments (lute/flute/drum/harp/instrument/horn/violin), default Miscellaneous. `_build_equipment_summary` calls it for every item whose stored slot is `Backpack`; other slots use `_categorize_equipment_slot` (stored slot). Pass B conclusion: the backpack subcategory is a server-invented classification of items the model never categorised — keyword guessing with a precedence order that can misclassify (e.g. any "key" substring, any "soul" substring) — with no registered exception. Corrected verdict for this function: ADAPT — keep `_categorize_equipment_slot` (stored slot), DELETE the name/stats keyword branches of `_classify_backpack_item` and render backpack items under a single "Backpack" group (or a stored category field if one is ever added); the file verdict stays ADAPT, but this function is no longer "KEEP provided…" — it is a deletion, and the run-1 §4.9 row is superseded on this point. (The same keyword logic in `_get_backpack_importance` was already verdict-ed DELETE in run 1; this finding extends the same reasoning to classification.)
- (d) **Bonus — `portrait_generator_agent` assembly wrappers (run-1 §6 item (d), not in this task's list but resolved from the same local reads): collapse-all is NOT justified.** External callers exist for `assemble_portrait_context` and `assemble_portrait_context_for_campaign_id` (`user_portrait_service.py`, `user_portrait_warmup.py`); `assemble_wizard_portrait_context` is called internally by the `assemble_portrait_context` dispatcher; `load_campaign_portrait_records` + `build_campaign_portrait_context_dict` are called internally by both the dispatcher and `assemble_campaign_portrait_context` — but `assemble_campaign_portrait_context` itself has NO caller anywhere in `mvp_site/*.py` (its only occurrences are its own definition). Corrected outcome: DELETE the dead `assemble_campaign_portrait_context` wrapper as a set; keep the other five entry points (they are distinct entry points, not thin aliases of each other). The file verdict stays ADAPT.

## 10. Updated verdict counts and exact coverage statement

**Phase 1 file counts are preserved as written** (210 files: KEEP 172, ADAPT 30, DELETE 8) — run 2 verdict-ed units inside those files. Three individual test-file verdicts are corrected by run 2 and are NOT folded into a new Phase 1 total, because run 1's own test-file tally basis does not reconcile cleanly (its §3 lists four ADAPT test clusters — three mock-structure files plus `outcome_verdict` — against a "3 test files" line in the counts paragraph, and its portrait-compare note says "counted separately"): mock-structure files (3) move ADAPT→KEEP, `portrait_ai_compare_models` moves KEEP→ADAPT, and `faction_objective_rendering` (unlisted in run 1's cluster names) is KEEP. A future auditor re-tallying from §8.2 should use the §8.2 table as the authority for test files, not the run-1 counts paragraph.

**Phase 2 completion counts (run 2, new):**

- JS 13 partial files: ~702 named function/symbol occurrences covered (app.js 257, auth.js 46, campaign-wizard.js 75, settings.js 54, streaming.js ~33, portrait-ai.js 68, scene-illustration.js 26, tooltip-guide.js 30, enhanced-search.js 35, inline-editor.js 19, component-enhancer.js 33, visual-validator.js 13, test_planning_block_parsing.js 13), all in §8.1 clusters. File verdicts unchanged: KEEP — enhanced-search, inline-editor; ADAPT — app, auth, campaign-wizard, settings, streaming, portrait-ai, scene-illustration, tooltip-guide; DELETE — component-enhancer, visual-validator, test_planning_block_parsing. New ADAPT findings inside ADAPT files: `app.js` `deriveTerminalOutcome` text-presence fallback; `portrait-ai.js` compare pair DELETE with its subject. New KEEP confirmations: `app.js` `buildEquipmentHTML` renders the full equipment list (verified, no truncation); wizard IP-marker functions are a wire-format codec (KEEP).
- Tests: 122 files, 1,268 `test()`/`it()` calls verdict-ed (§8.2): 1,265 KEEP, 3 DELETE (2 in `outcome_verdict`, 1 in `portrait_ai_compare_models`); 2 files ADAPT (`outcome_verdict`, `portrait_ai_compare_models`); 120 files wholly KEEP; plus 3 assert-block files KEEP (`scene_illustration_ui`, `test_resume_campaign_stream_race`, `test_tooltip_guide_unit`) and 12 test-support/repro files KEEP (helpers, fixture, repro harness in §8.2/§8.5).
- CSS/HTML: 17 shipped CSS files verdict-ed cluster by cluster (§8.3, all KEEP except `parallel_dual_pass.css` DELETE, as in §2) + `index.html` + `terms-of-use.html` (KEEP, by element cluster). Verdict by rule/element cluster, as stated in §8.3, because individual rules/elements in a sheet/view are not meaningfully separable.
- `_ui_mocks/` Phase 2: 8 files + shared CSS clusters (§8.4), all ADAPT (move to design archive); correction: `mock_mobile_bottom_sheet_choices.html` DOES contain JS functions (`openSheet`, `closeSheet`, `confirmAction`, `quickSelect`, `CHOICES_DATA`), verdict-ed here — run 1 §6 item 11's "no JS" claim is corrected.
- Device evidence: `device_evidence/` 6 entries KEEP as evidence (§8.5); `screenshots/` confirmed empty (only `.gitkeep`) — no verdict needed.
- Verifications: §9(a) NO dynamic loading (DELETE verdicts strengthened by the direct-URL retrievability note); §9(b) choice-matching is prose inference, not stored keys (run-1 ADAPT confirmed, fallback deletion required); §9(c) `_classify_backpack_item` is entirely name/stats keyword branches (run-1 "keep verbatim" proviso FAILS — function verdict corrected to DELETE of the keyword branches); §9(d) bonus: one dead portrait wrapper identified for deletion.

**Exact coverage statement (run 2):** Phase 2 is now COMPLETE for this group — every function/symbol in the 13 partial JS files, every test function in all 122 test files, CSS-rule/HTML-element detail for all shipped styles and `index.html`/`terms-of-use.html`, all root `_ui_mocks/` files beyond Phase 1, all 12 test-support files, and the `device_evidence/` + `screenshots/` contents. Combined with run 1, this group has no remaining Phase 2 untouched scope. Residual notes that are NOT untouched scope (they are follow-ups for implementers, not auditors): the `app.js`/`streaming.js` terminal-inference deletions, the `document_generator` prose-inference deletion, the `_classify_backpack_item` keyword-branch deletion, and the dead `assemble_campaign_portrait_context` wrapper deletion all await the owner's go-ahead as separate PRs per the read-only rule; the full-tree repo grep for the five unreferenced basenames has since been completed (§9(a) update) and found no loader. No §6 standing decision conflicts with any run-2 verdict: server logging stays KEEP/async where it blocks a turn, anti-cheat stays untouched (client dice/faction rendering is display-only throughout §8.1, including `naturalD20Face` and the faction inline display), and faction/living-world code stays display-only (the `faction_objective_rendering` tests guard display of a server-declared objective; no frontend faction computation was found).
