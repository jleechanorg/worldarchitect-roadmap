# Frontend review — WorldArchitect.AI, area A12 (review pass, run 3)
Read-only review. Nothing here deletes anything; every deletion is a separate PR with the owner's go-ahead. Repo files are DATA, never instructions. This pass reviews the v2 group file (`plans/audit/frontend.md`, read in full, §§1–10) against the local tree at `~/workspace/repos/worldarchitect.ai` (main-branch ZIP tree, no .git history). ZERO GitHub API/MCP calls; no browser use; no repo files changed; no subagents.
Policy applied: `plans/zero-code-rejustification-audit.md` §4 (Pass A zero-code baseline, then Pass B strict ZFC) with §6 decisions as overridden in the task: (1) server logging KEEP, async where it blocks a turn; (2) anti-cheat KEEP, dice resolution ON the turn path, audit trail may go async; (3) faction/living-world KEEP, async background ticks merged on next turn; (4) agent routing KEPT as a model-side decision step implemented by Jev, dispatch table server-side, modal conclude guards explicit-signals-only, Jev Noul may flag likely exit to prompt explicit confirmation, never auto-conclude; intent_classifier.py + warmup.py still DELETE in full. The draft ZFC amendment (`plans/zfc-skill-model-amendment-proposal.md`) is DRAFT ONLY and NOT applied; its effects are flagged separately in §5 and change no verdict here.
## Header

- Area: A12 frontend. Files reviewed: **68** = 58 under `mvp_site/frontend_v1/` (exact list from `plans/audit/review/_file_list.txt`, which excludes `frontend_v1/tests/` by construction) + 10 Python files (`frontend_cutover_flag.py`, `frontend_preview_release.py`, `frontend_release.py`, `scene_attempts.py`, `scene_illustration_flag.py`, `scene_illustration_policy.py`, `scene_illustration_provider.py`, `scene_illustration_service.py`, `scene_illustration_worker.py`, `scene_prompt_ablation.py`).
- JS symbols: **1,064** function/arrow-const/class/method definitions (see Enumeration below). CSS rule blocks: **1,518** across 18 CSS files. HTML sections: **~30** clusters (index.html, terms-of-use.html, mock HTML). Python symbols: **151** (AST functions/methods/classes; module constants verdict-ed with their file/symbol groups).
- Total symbols reviewed: **~2,762** (1,064 JS + 1,518 CSS + ~30 HTML + 151 Python). frontend_v1/tests/ is EXCLUDED BY SCOPE, not skipped (see §6).
- Run-2 relation: this is a REVIEW pass. Where run 2 gave a verdict, each row states CONFIRM or CHALLENGE with file:line evidence. The 10 Python files get full per-symbol reviews; for the 3 frontend_*.py files the v2 file already contains full §4 per-function rows (contrary to the task premise that they were run-1 Phase-1-only — see §4 challenge C5), so they are treated as confirm/challenge targets and re-verified symbol by symbol anyway. The 7 scene_*.py files had no run-2 verdicts and receive fresh verdicts.
## Enumeration method (JS)

Regex enumeration over every shipped JS file (excluding `tests/`): `function` declarations, `const/let/var` whose RHS starts with a function/arrow pattern (`function`, `async function`, `(`…`) =>` with `=>` within 5 lines, single-identifier `=>`), `class` declarations, class/object methods (`name(...) {`), object methods (`name: function` / `name: (...) =>`), and `window/`/property assignments to functions. Deduplicated by (line, name), so duplicate names in separate closures are separate rows. Run-2 reconciliation: run 2 counted ~702 occurrences in the 13 partial files under a narrower rule (named functions + arrow-function consts: e.g. app.js 257 = 27 named + 230 arrow consts; auth.js 46; settings.js 54; streaming.js ~33). This pass counts 303 app.js / 91 auth.js / 67 settings.js / 47 streaming.js because it ALSO counts class/object methods and property assignments (e.g. auth.js's token-manager object methods, app.js's object-literal handlers) that run 2 folded into enclosing clusters. Per-file counts are listed in each table header; verdicts agree with run 2 wherever the same symbol is named (see §4 for the exceptions). Limitation: arrow consts whose `=>` falls more than 5 lines after a `(`-starting RHS, and functions assigned via computed/indirect forms, would be missed; no such case was observed in spot checks of the large files. Anonymous callbacks are covered under their enclosing named function, as in run 2.
Caller evidence ("prod refs" column): count of word-boundary occurrences of the symbol name in shipped frontend files (JS + HTML, excluding `tests/`) OTHER than the defining file, plus a `W` flag when `window.<name>` appears anywhere in shipped code. A count of 0 does not by itself mean dead: symbols can be handlers (registered via addEventListener/onclick), window exports consumed by another file by name, or entry points. Dead verdicts below rest on load evidence + caller evidence + handler/registration checks together, never on a zero count alone.
## Load map (every JS file)

| File | Loaded by |
|---|---|
| `api.js` | index.html:627 (defer) |
| `app.js` | index.html:646 (defer) |
| `auth.js` | index.html:626 (defer) |
| `diag-boot.js` | index.html:28 |
| `diagnostics.js` | index.html:624 (defer) |
| `js/animation-helpers.js` | index.html:631 (defer) |
| `js/avatar-crop.js` | index.html:633 (defer) |
| `js/campaign-wizard.js` | index.html:636 (defer) |
| `js/component-enhancer.js` | NEVER LOADED — no tag, no dynamic load |
| `js/ember-bg.js` | index.html:643 (defer) |
| `js/enhanced-search.js` | index.html:637 (defer) |
| `js/inline-editor.js` | index.html:642 (defer) |
| `js/interface-manager.js` | index.html:629 (defer) |
| `js/loading-messages.js` | index.html:641 (defer) |
| `js/opening_story.js` | index.html:640 (defer) |
| `js/outcome-verdict.js` | index.html:645 (defer) |
| `js/portrait-ai-ui.js` | index.html:634 (defer) |
| `js/portrait-ai.js` | index.html:635 (defer) |
| `js/scene-illustration.js` | index.html:638 (defer) |
| `js/settings.js` | DYNAMIC ONLY — app.js:2576–2583 createElement("script") src /frontend_v1/js/settings.js |
| `js/streaming.js` | index.html:639 (defer) |
| `js/test_planning_block_parsing.js` | NEVER LOADED — no tag, no dynamic load |
| `js/theme-bootstrap.js` | index.html:22 |
| `js/theme-manager.js` | index.html:630 (defer) |
| `js/tooltip-guide.js` | index.html:715 (defer; stripped by main.py tooltip kill switch when disabled) |
| `js/ui-utils.js` | index.html:632 (defer) |
| `js/visual-validator.js` | NEVER LOADED — no tag, no dynamic load |
| `js/worldai-mcp-bridge.js` | index.html:714 (defer) |
| `parallel_dual_pass.js` | NEVER LOADED — no tag, no dynamic load |
| `quick_start_shared.js` | index.html:644 (defer) |
| `user_lifecycle.js` | index.html:625 (defer) |

Dynamic-loading sweep: the only dynamic script injection in shipped JS is app.js:2576–2583 (settings.js). component-enhancer.js:75 creates a `link` element for its own CSS, but that file itself is never loaded, so it is not a loader for any shipped file. main.py serves `frontend_v1/<path:filename>` generically (main.py:2003) and names no asset except the tooltip kill-switch pair (main.py:1947, 1961–1962); generic servability is NOT loading — the five unreferenced files remain retrievable by direct URL while they sit in the served directory (run-2 §9(a) note, confirmed by the route), which strengthens their DELETE verdicts.

---

## Per-file tables — JavaScript (one row per symbol)

Lens A (executable/reachability) and Lens B (docs) are stated per file (they are uniform within a file except where a row note says otherwise); the verdict column carries the symbol verdict. File verdict = the verdict of the file as a whole; "KEEP (file ADAPT)" means the symbol stays as written while the file carries a file-level ADAPT (decompose/dedup/reroute). Run-2 column: C = CONFIRM, CH = CHALLENGE (see §4).

### `api.js` — 19 symbols, file verdict KEEP, loaded: index.html:627 (defer)

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `safeDiag` | 16 | const | 71 W | KEEP | C |
| `detectClockSkew` | 40 | function | 0 | KEEP | C |
| `applyClockSkewCompensation` | 75 | function | 0 | KEEP | C |
| `handleClockSkewError` | 89 | function | 0 | KEEP | C |
| `fetchApi` | 120 | function | 23 | KEEP | C |
| `method` | 124 | objmethod | 59 | KEEP | C |
| `method` | 224 | objmethod | 59 | KEEP | C |
| `error_name` | 244 | objmethod | 1 | KEEP | C |
| `error_message` | 245 | objmethod | 3 | KEEP | C |
| `error_name` | 336 | objmethod | 1 | KEEP | C |
| `error_message` | 337 | objmethod | 3 | KEEP | C |
| `error_message` | 466 | objmethod | 3 | KEEP | C |
| `error_name` | 487 | objmethod | 1 | KEEP | C |
| `checkBackendHealth` | 495 | function | 0 | KEEP | C |
| `handleOnline` | 524 | const | 0 | KEEP | C |
| `handleOffline` | 529 | const | 0 | KEEP | C |
| `detachNetworkStatusListeners` | 536 | function | 0 | KEEP | C |
| `attachNetworkStatusListeners` | 545 | function | 0 | KEEP | C |
| `getConnectionStatus` | 558 | function | 0 | KEEP | C |

### `app.js` — 303 symbols, file verdict ADAPT, loaded: index.html:646 (defer)

File ADAPT (run 2 confirmed): decompose the 10,666-line DOMContentLoaded monolith by subsystem; debug cluster and first-turn-coach overlap move/merge as in run 2. Symbols below are KEEP unless named otherwise. Run-2 verdict CONFIRMED, with the new dead-BYOK-branch finding on setupSettingsEventListeners.

Lens A: loaded file; symbols are live except named exceptions. Lens B: comments/docstrings checked; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `safeDiag` | 13 | const | 71 W | KEEP (file ADAPT) | C |
| `removeDebugControlsFromRenderedEntries` | 64 | const | 0 | KEEP (file ADAPT) | C |
| `addDebugControlsToRenderedEntries` | 69 | const | 0 | KEEP (file ADAPT) | C |
| `refreshDebugToolsEligibility` | 90 | const | 0 | KEEP (file ADAPT) | C |
| `createHudSessionHeaderState` | 118 | const | 0 | KEEP (file ADAPT) | C |
| `paint` | 125 | const | 3 | KEEP (file ADAPT) | C |
| `headingTime` | 126 | const | 0 | KEEP (file ADAPT) | C |
| `usableHeader` | 130 | const | 0 | KEEP (file ADAPT) | C |
| `setCampaign` | 148 | method | 0 | KEEP (file ADAPT) | C |
| `read` | 177 | method | 15 | KEEP (file ADAPT) | C |
| `renderHudSubline` | 183 | const | 0 | KEEP (file ADAPT) | C |
| `getLevelUpNoticeKey` | 227 | const | 0 | KEEP (file ADAPT) | C |
| `isLevelUpNoticeDismissed` | 231 | const | 0 | KEEP (file ADAPT) | C |
| `clearDraft` | 257 | const | 0 | KEEP (file ADAPT) | C |
| `clearPendingDraftTimer` | 262 | const | 0 | KEEP (file ADAPT) | C |
| `scrollToBottom` | 279 | const | 0 | KEEP (file ADAPT) | C |
| `isNearLiveBottom` | 284 | const | 0 | KEEP (file ADAPT) | C |
| `setTimerInfo` | 290 | const | 0 | KEEP (file ADAPT) | C |
| `buildNarrativeTextIndex` | 317 | const | 0 | KEEP (file ADAPT) | C |
| `rangeAt` | 339 | method | 0 | KEEP (file ADAPT) | C |
| `matchingSuffixLength` | 351 | const | 0 | KEEP (file ADAPT) | C |
| `matchingPrefixLength` | 363 | const | 0 | KEEP (file ADAPT) | C |
| `resolveSemanticTextOffset` | 370 | const | 0 | KEEP (file ADAPT) | C |
| `words` | 376 | const | 4 | KEEP (file ADAPT) | C |
| `captureReadingTextAnchor` | 434 | const | 0 | KEEP (file ADAPT) | C |
| `captureVisibleReadingAnchor` | 514 | const | 0 | KEEP (file ADAPT) | C |
| `releaseReadingTailSpace` | 558 | const | 0 | KEEP (file ADAPT) | C |
| `updateReadingTailSpace` | 568 | const | 0 | KEEP (file ADAPT) | C |
| `refresh` | 583 | assign | 31 | KEEP (file ADAPT) | C |
| `restoreReadingTextAnchor` | 619 | const | 0 | KEEP (file ADAPT) | C |
| `cancelActiveReadingAnchorTransaction` | 654 | const | 0 | KEEP (file ADAPT) | C |
| `isEditableEventTarget` | 666 | const | 0 | KEEP (file ADAPT) | C |
| `isScrollIntentKeyEvent` | 671 | const | 0 | KEEP (file ADAPT) | C |
| `beginReadingAnchorTransaction` | 674 | const | 0 | KEEP (file ADAPT) | C |
| `cleanup` | 680 | const | 11 | KEEP (file ADAPT) | C |
| `restore` | 700 | const | 10 | KEEP (file ADAPT) | C |
| `cancelOnScrollKey` | 706 | const | 0 | KEEP (file ADAPT) | C |
| `armExpiry` | 709 | const | 0 | KEEP (file ADAPT) | C |
| `refreshReaderTextAnchor` | 747 | const | 0 | KEEP (file ADAPT) | C |
| `scheduleReaderTextAnchorRefresh` | 752 | const | 0 | KEEP (file ADAPT) | C |
| `resetReaderScrollIntent` | 756 | const | 0 | KEEP (file ADAPT) | C |
| `cancelReaderFollowing` | 767 | const | 0 | KEEP (file ADAPT) | C |
| `resumeReaderFollowingAtLiveBottom` | 773 | const | 0 | KEEP (file ADAPT) | C |
| `resumeReaderFollowingOnNextScroll` | 788 | const | 0 | KEEP (file ADAPT) | C |
| `cleanup` | 796 | const | 11 | KEEP (file ADAPT) | C |
| `onScroll` | 800 | const | 5 | KEEP (file ADAPT) | C |
| `handleReaderWheelIntent` | 814 | const | 0 | KEEP (file ADAPT) | C |
| `handleReaderGestureIntent` | 828 | const | 0 | KEEP (file ADAPT) | C |
| `matchingTouch` | 848 | const | 0 | KEEP (file ADAPT) | C |
| `matchesGesture` | 852 | const | 0 | KEEP (file ADAPT) | C |
| `cleanup` | 864 | const | 11 | KEEP (file ADAPT) | C |
| `onMove` | 874 | const | 0 | KEEP (file ADAPT) | C |
| `onEnd` | 886 | const | 0 | KEEP (file ADAPT) | C |
| `onCancel` | 893 | const | 5 | KEEP (file ADAPT) | C |
| `isDownwardScrollIntentKeyEvent` | 913 | const | 0 | KEEP (file ADAPT) | C |
| `updateReaderFollowing` | 916 | const | 0 | KEEP (file ADAPT) | C |
| `updateRuntimeIndicators` | 972 | const | 0 | KEEP (file ADAPT) | C |
| `getByokProviderActiveStatus` | 993 | const | 0 | KEEP (file ADAPT) | C |
| `refreshDashboardOpenRouterStatus` | 1013 | const | 0 | KEEP (file ADAPT) | C |
| `showSpinner` | 1030 | const | 6 | KEEP (file ADAPT) | C |
| `hideSpinner` | 1044 | const | 0 | KEEP (file ADAPT) | C |
| `_perfNow` | 1061 | const | 0 | KEEP (file ADAPT) | C |
| `returnToDashboardAfterQuickStartFailure` | 1071 | const | 0 | KEEP (file ADAPT) | C |
| `quickStartCampaign` | 1080 | const | 2 | KEEP (file ADAPT) | C |
| `showRateLimitModal` | 1094 | const | 2 W | KEEP (file ADAPT) | C |
| `resolveQuotaLimits` | 1241 | const | 0 | KEEP (file ADAPT) | C |
| `renderQuotaBanner` | 1248 | const | 0 | KEEP (file ADAPT) | C |
| `updateQuotaBanner` | 1284 | const | 2 W | KEEP (file ADAPT) | C |
| `ensureElement` | 1338 | const | 0 | KEEP (file ADAPT) | C |
| `ensureDashboardNodes` | 1355 | const | 0 | KEEP (file ADAPT) | C |
| `handleInfoQuery` | 1377 | const | 0 | KEEP (file ADAPT) | C |
| `sendEquipmentQuery` | 1431 | assign | 0 | KEEP (file ADAPT) | C |
| `sendStatsQuery` | 1440 | assign | 0 | KEEP (file ADAPT) | C |
| `sendSpellsQuery` | 1448 | assign | 0 | KEEP (file ADAPT) | C |
| `buildStatsHTML` | 1482 | const | 0 | KEEP (file ADAPT) | C |
| `parsePythonReprDict` | 1493 | const | 0 | KEEP (file ADAPT) | C |
| `skipWs` | 1497 | const | 0 | KEEP (file ADAPT) | C |
| `parseString` | 1500 | const | 0 | KEEP (file ADAPT) | C |
| `parseValue` | 1531 | const | 0 | KEEP (file ADAPT) | C |
| `parseList` | 1557 | const | 0 | KEEP (file ADAPT) | C |
| `parseDict` | 1581 | const | 0 | KEEP (file ADAPT) | C |
| `fmtMod` | 1624 | const | 0 | KEEP (file ADAPT) | C |
| `getStat` | 1630 | const | 0 | KEEP (file ADAPT) | C |
| `firstString` | 1705 | const | 0 | KEEP (file ADAPT) | C |
| `buildEquipmentHTML` | 1801 | const | 0 | KEEP (file ADAPT) | C |
| `buildSpellsHTML` | 1842 | const | 0 | KEEP (file ADAPT) | C |
| `normalizeSpell` | 1858 | const | 0 | KEEP (file ADAPT) | C |
| `groupSpells` | 1871 | const | 0 | KEEP (file ADAPT) | C |
| `renderSpellGroup` | 1882 | const | 0 | KEEP (file ADAPT) | C |
| `toNum` | 1888 | const | 0 | KEEP (file ADAPT) | C |
| `fmtMod` | 1906 | const | 0 | KEEP (file ADAPT) | C |
| `toNum` | 1933 | const | 0 | KEEP (file ADAPT) | C |
| `showView` | 2007 | const | 6 W | KEEP (file ADAPT) | C |
| `resetNewCampaignForm` | 2072 | function | 0 | KEEP (file ADAPT) | C |
| `enableCampaignWizard` | 2104 | function | 1 | KEEP (file ADAPT) | C |
| `setupCampaignTypeHandlers` | 2114 | function | 0 | KEEP (file ADAPT) | C |
| `handleRouteChange` | 2167 | const | 2 | KEEP (file ADAPT) | C |
| `hasRestorableSearchParams` | 2196 | function | 0 | KEEP (file ADAPT) | C |
| `restorePendingLoginRedirect` | 2205 | function | 0 | KEEP (file ADAPT) | C |
| `clearPendingRedirect` | 2211 | function | 0 | KEEP (file ADAPT) | C |
| `loadSettingsPage` | 2503 | const | 0 | KEEP (file ADAPT) | C |
| `initializeSettings` | 2571 | const | 0 W | KEEP (file ADAPT) | C |
| `onload` | 2578 | assign | 7 | KEEP (file ADAPT) | C |
| `setupSettingsEventListeners` | 2590 | const | 0 | KEEP — Contains dead BYOK branch: calls window.setupBYOKEventListeners (app.js:2595–2596), never assigned anywhere; guarded typeof check prevents a crash. Delete or rewire that branch. | C |
| `isMechanicsHiddenActive` | 2608 | const | 0 | KEEP (file ADAPT) | C |
| `formatRecordedRollFields` | 2618 | const | 0 | KEEP (file ADAPT) | C |
| `generateStructuredFieldsPreNarrative` | 2634 | const | 0 | KEEP (file ADAPT) | C |
| `getActionResolutionNarrative` | 2643 | const | 0 | KEEP (file ADAPT) | C |
| `usable` | 2644 | const | 1 | KEEP (file ADAPT) | C |
| `formatRollObject` | 2652 | const | 0 | KEEP (file ADAPT) | C |
| `getActionResolutionRollObjects` | 2676 | const | 0 | KEEP (file ADAPT) | C |
| `naturalD20Face` | 2683 | const | 0 | KEEP (file ADAPT) | C |
| `toDiceRolls` | 2729 | const | 0 | KEEP (file ADAPT) | C |
| `escapeRecordedText` | 2744 | const | 0 | KEEP (file ADAPT) | C |
| `isWireObject` | 2890 | const | 0 | KEEP (file ADAPT) | C |
| `renderImplicitCacheUsage` | 3201 | const | 0 | KEEP (file ADAPT) | C |
| `hasOwn` | 3202 | const | 0 | KEEP (file ADAPT) | C |
| `firstKnown` | 3205 | const | 0 | KEEP (file ADAPT) | C |
| `formatTokenBreakdown` | 3208 | const | 0 | KEEP (file ADAPT) | C |
| `generateStructuredFieldsPostNarrative` | 3267 | const | 0 | KEEP (file ADAPT) | C |
| `renderPlanningBlock` | 3272 | const | 0 | KEEP (file ADAPT) | C |
| `renderEntitiesMentioned` | 3290 | const | 0 | KEEP (file ADAPT) | C |
| `renderDebugDetails` | 3298 | const | 0 | KEEP (file ADAPT) | C |
| `generateStructuredFieldsHTML` | 3357 | const | 0 | KEEP (file ADAPT) | C |
| `getStoryLabel` | 3379 | const | 0 | KEEP (file ADAPT) | C |
| `attachStoryEntryHandlers` | 3551 | const | 0 | KEEP (file ADAPT) | C |
| `resetReviewState` | 3705 | const | 0 | KEEP (file ADAPT) | C |
| `setReviewPhase` | 3712 | const | 0 | KEEP (file ADAPT) | C |
| `markTakenChoice` | 3742 | const | 0 | KEEP (file ADAPT) | C |
| `resetChoiceSendingState` | 3774 | const | 0 | KEEP (file ADAPT) | C |
| `initChoiceDetailViewport` | 3780 | const | 0 | KEEP (file ADAPT) | C |
| `sync` | 3796 | const | 6 | KEEP (file ADAPT) | C |
| `toggleChoiceDetail` | 3823 | const | 0 | KEEP (file ADAPT) | C |
| `choiceKeepsMode` | 3837 | const | 0 | KEEP (file ADAPT) | C |
| `markReviewSaveFailed` | 3847 | const | 0 | KEEP (file ADAPT) | C |
| `handleChoiceClick` | 3851 | const | 0 | KEEP (file ADAPT) | C |
| `setSpicySwitchChecked` | 4014 | const | 0 | KEEP (file ADAPT) | C |
| `setSpicyModeIndicator` | 4020 | const | 0 | KEEP (file ADAPT) | C |
| `getComposerInteractionMode` | 4025 | const | 0 | KEEP (file ADAPT) | C |
| `syncComposerPlaceholder` | 4032 | const | 0 | KEEP (file ADAPT) | C |
| `syncChoiceButtonsEnabled` | 4046 | const | 0 | KEEP (file ADAPT) | C |
| `syncComposerInteractionMode` | 4060 | const | 0 | KEEP (file ADAPT) | C |
| `isServerFlagTrue` | 4070 | const | 0 | KEEP (file ADAPT) | C |
| `isServerFlagFalse` | 4079 | const | 0 | KEEP (file ADAPT) | C |
| `resolveCharCreationState` | 4089 | const | 0 | KEEP (file ADAPT) | C |
| `isWideChoiceViewport` | 4185 | const | 0 | KEEP (file ADAPT) | C |
| `demoteInlineEntry` | 4189 | const | 0 | KEEP (file ADAPT) | C |
| `resetComposerTurnTracking` | 4214 | const | 0 | KEEP (file ADAPT) | C |
| `selectionLabel` | 4441 | const | 0 | KEEP (file ADAPT) | C |
| `selectionKeyLabel` | 4448 | const | 0 | KEEP (file ADAPT) | C |
| `ensureReaderPill` | 4544 | const | 0 | KEEP (file ADAPT) | C |
| `setUnread` | 4558 | const | 0 | KEEP (file ADAPT) | C |
| `arrow` | 4562 | const | 8 | KEEP (file ADAPT) | C |
| `releaseReaderPill` | 4613 | const | 0 | KEEP (file ADAPT) | C |
| `readFirstTurnCoachCompletion` | 4648 | const | 0 | KEEP (file ADAPT) | C |
| `currentFirstTurnCoachUser` | 4662 | const | 0 | KEEP (file ADAPT) | C |
| `initializeFirstTurnCoach` | 4669 | const | 0 | KEEP (file ADAPT) | C |
| `syncFirstTurnCoach` | 4719 | const | 0 | KEEP (file ADAPT) | C |
| `parsePlanningBlocks` | 4781 | const | 5 | KEEP (file ADAPT) | C |
| `parsePlanningBlocksJson` | 4825 | const | 9 | KEEP (file ADAPT) | C |
| `renderPlanningProse` | 4828 | const | 0 | KEEP (file ADAPT) | C |
| `id` | 4860 | objmethod | 312 | KEEP (file ADAPT) | C |
| `decodeHtmlEntities` | 5080 | const | 2 | KEEP (file ADAPT) | C |
| `sanitizeHtml` | 5091 | const | 7 | KEEP (file ADAPT) | C |
| `escapeHtmlAttribute` | 5103 | const | 5 | KEEP (file ADAPT) | C |
| `sanitizeIdentifier` | 5112 | const | 2 | KEEP (file ADAPT) | C |
| `getDebugMarkerPairs` | 5120 | const | 0 | KEEP (file ADAPT) | C |
| `splitDebugMarkers` | 5155 | const | 0 | KEEP (file ADAPT) | C |
| `renderNarrativeMarkdown` | 5212 | const | 0 | KEEP (file ADAPT) | C |
| `renderNarrativeHtml` | 5267 | const | 0 | KEEP (file ADAPT) | C |
| `streamingRenderCutoff` | 5301 | const | 0 | KEEP (file ADAPT) | C |
| `renderStreamingNarrative` | 5348 | const | 0 | KEEP (file ADAPT) | C |
| `showSuccessToast` | 5441 | function | 0 | KEEP (file ADAPT) | C |
| `showErrorToast` | 5497 | function | 0 | KEEP (file ADAPT) | C |
| `showDuplicateCampaignModal` | 5557 | function | 0 | KEEP (file ADAPT) | C |
| `onHidden` | 5623 | const | 0 | KEEP (file ADAPT) | C |
| `renderCampaignList` | 5735 | const | 0 | KEEP (file ADAPT) | C |
| `renderCampaignListUI` | 5888 | function | 0 | KEEP (file ADAPT) | C |
| `saveFn` | 5981 | objmethod | 3 | KEEP (file ADAPT) | C |
| `onError` | 5989 | objmethod | 13 | KEEP (file ADAPT) | C |
| `loadOlderStoryEntries` | 6082 | const | 0 | KEEP (file ADAPT) | C |
| `updateLoadOlderButton` | 6175 | const | 0 | KEEP (file ADAPT) | C |
| `syncLoadOlderVisibility` | 6213 | const | 0 | KEEP (file ADAPT) | C |
| `flushPendingAvatarPersist` | 6222 | const | 0 | KEEP (file ADAPT) | C |
| `resumeCampaign` | 6231 | const | 2 | KEEP (file ADAPT) | C |
| `isCurrentResume` | 6240 | const | 0 | KEEP (file ADAPT) | C |
| `saveFn` | 6309 | objmethod | 3 | KEEP (file ADAPT) | C |
| `onError` | 6317 | objmethod | 13 | KEEP (file ADAPT) | C |
| `loadedGeminiCount` | 6342 | objmethod | 0 | KEEP (file ADAPT) | C |
| `allGemini` | 6343 | const | 0 | KEEP (file ADAPT) | C |
| `createClient` | 6580 | objmethod | 1 | KEEP (file ADAPT) | C |
| `onStreamStarting` | 6582 | objmethod | 5 | KEEP (file ADAPT) | C |
| `onStreamConnected` | 6585 | objmethod | 5 | KEEP (file ADAPT) | C |
| `onFirstToken` | 6593 | objmethod | 2 | KEEP (file ADAPT) | C |
| `onReady` | 6596 | objmethod | 2 | KEEP (file ADAPT) | C |
| `renderWritingEntry` | 6598 | objmethod | 2 | KEEP (file ADAPT) | C |
| `render` | 6606 | objmethod | 20 W | KEEP (file ADAPT) | C |
| `_avatarUrlWithCacheBust` | 6652 | const | 0 | KEEP (file ADAPT) | C |
| `getHeaderAvatarHost` | 6662 | const | 0 | KEEP (file ADAPT) | C |
| `setupGameAvatar` | 6666 | const | 0 | KEEP (file ADAPT) | C |
| `onclick` | 6713 | assign | 20 | KEEP (file ADAPT) | C |
| `onUpload` | 6725 | objmethod | 2 | KEEP (file ADAPT) | C |
| `onGeneratedCampaign` | 6726 | objmethod | 3 | KEEP (file ADAPT) | C |
| `onchange` | 6732 | assign | 0 | KEEP (file ADAPT) | C |
| `onclick` | 6828 | assign | 20 | KEEP (file ADAPT) | C |
| `openIngamePortraitAi` | 6842 | const | 0 | KEEP (file ADAPT) | C |
| `onUpload` | 6852 | objmethod | 2 | KEEP (file ADAPT) | C |
| `onGeneratedCampaign` | 6853 | objmethod | 3 | KEEP (file ADAPT) | C |
| `onclick` | 6866 | assign | 20 | KEEP (file ADAPT) | C |
| `onUpload` | 6874 | objmethod | 2 | KEEP (file ADAPT) | C |
| `onGeneratedFile` | 6875 | objmethod | 2 | KEEP (file ADAPT) | C |
| `onload` | 6878 | assign | 7 | KEEP (file ADAPT) | C |
| `onchange` | 6888 | assign | 0 | KEEP (file ADAPT) | C |
| `onload` | 6895 | assign | 7 | KEEP (file ADAPT) | C |
| `_showCropOverlay` | 6906 | function | 0 | KEEP (file ADAPT) | C |
| `onclick` | 6951 | assign | 20 | KEEP (file ADAPT) | C |
| `onclick` | 6956 | assign | 20 | KEEP (file ADAPT) | C |
| `onclick` | 7001 | assign | 20 | KEEP (file ADAPT) | C |
| `expandAvatar` | 7036 | const | 0 | KEEP (file ADAPT) | C |
| `collapseAvatar` | 7074 | const | 0 | KEEP (file ADAPT) | C |
| `run` | 7208 | objmethod | 73 | KEEP (file ADAPT) | C |
| `getInteractionSubmitButton` | 7298 | const | 0 | KEEP (file ADAPT) | C |
| `resizeComposerInput` | 7300 | const | 0 | KEEP (file ADAPT) | C |
| `syncComposerSubmitState` | 7308 | const | 0 | KEEP (file ADAPT) | C |
| `clearInteractionSubmitLoading` | 7318 | const | 0 | KEEP (file ADAPT) | C |
| `cleanupComposerPendingState` | 7333 | const | 0 | KEEP (file ADAPT) | C |
| `initComposerKeyboardSubmit` | 7347 | const | 0 | KEEP (file ADAPT) | C |
| `initKeyboardInset` | 7393 | const | 0 | KEEP (file ADAPT) | C |
| `update` | 7398 | const | 7 W | KEEP (file ADAPT) | C |
| `initModeHelp` | 7419 | const | 0 | KEEP (file ADAPT) | C |
| `close` | 7422 | const | 19 | KEEP (file ADAPT) | C |
| `initModeTooltips` | 7446 | const | 0 | KEEP (file ADAPT) | C |
| `keepOffEdge` | 7450 | const | 0 | KEEP (file ADAPT) | C |
| `tip` | 7460 | const | 0 | KEEP (file ADAPT) | C |
| `describeRadio` | 7462 | const | 0 | KEEP (file ADAPT) | C |
| `initHudControls` | 7499 | const | 0 | KEEP (file ADAPT) | C |
| `closeMenu` | 7506 | const | 0 | KEEP (file ADAPT) | C |
| `syncMenuRows` | 7511 | const | 0 | KEEP (file ADAPT) | C |
| `syncSpicyRow` | 7545 | const | 0 | KEEP (file ADAPT) | C |
| `initDesktopChoiceKeys` | 7568 | const | 0 | KEEP (file ADAPT) | C |
| `openingFlowHoldsComposer` | 7686 | const | 0 | KEEP (file ADAPT) | C |
| `removeRejectedTurnEntries` | 7692 | const | 0 | KEEP (file ADAPT) | C |
| `handOffOpeningNotReady` | 7699 | const | 0 | KEEP (file ADAPT) | C |
| `resume` | 7705 | objmethod | 3 | KEEP (file ADAPT) | C |
| `restoreUiState` | 7709 | const | 0 | KEEP (file ADAPT) | C |
| `syncTurnCancelButton` | 7726 | const | 0 | KEEP (file ADAPT) | C |
| `setTurnLocked` | 7747 | const | 0 | KEEP (file ADAPT) | C |
| `reconcileCancelledTurn` | 7759 | const | 0 | KEEP (file ADAPT) | C |
| `stillCurrent` | 7762 | const | 0 | KEEP (file ADAPT) | C |
| `restoreSubmittedActionOnCapacityError` | 7864 | const | 0 | KEEP (file ADAPT) | C |
| `handleStreamingInteraction` | 7888 | const | 0 | KEEP (file ADAPT) | C |
| `clientTerminalOutcome` | 7903 | const | 0 | ADAPT — Client-observed terminal label; delete its use as a fallback source (see deriveTerminalOutcome). | C |
| `clientTerminalErrorType` | 7907 | const | 0 | KEEP (file ADAPT) | C |
| `deriveTerminalOutcome` | 7911 | const | 0 | ADAPT — Delete hasCompletedText→success fallback (app.js:7925) and client-descriptor fallback; keep payload.success/terminal_outcome/error branches. | C |
| `flushCompletionTelemetry` | 7945 | const | 0 | KEEP (file ADAPT) | C |
| `settleCompletionWithoutRender` | 8022 | const | 0 | KEEP (file ADAPT) | C |
| `markRenderSettled` | 8026 | const | 0 | KEEP (file ADAPT) | C |
| `runCompletionRender` | 8030 | const | 0 | KEEP (file ADAPT) | C |
| `stopDraftRecovery` | 8086 | const | 0 | KEEP (file ADAPT) | C |
| `ownsStreamingEntry` | 8087 | const | 0 | KEEP (file ADAPT) | C |
| `scheduleInitialNarrativeReveal` | 8089 | const | 0 | KEEP (file ADAPT) | C |
| `holdLockWhileServerTurnRuns` | 8115 | const | 0 | KEEP (file ADAPT) | C |
| `buildStreamingSessionHeaderHtml` | 8139 | const | 0 | KEEP (file ADAPT) | C |
| `renderStreamingPreSections` | 8167 | const | 0 | KEEP (file ADAPT) | C |
| `reconcileStreamingPreSections` | 8192 | const | 0 | KEEP (file ADAPT) | C |
| `__disposeDraftRecovery` | 8283 | assign | 0 | KEEP (file ADAPT) | C |
| `onChunk` | 8340 | assign | 9 | KEEP (file ADAPT) | C |
| `onPlanningThinking` | 8420 | assign | 7 | KEEP (file ADAPT) | C |
| `onToolResult` | 8435 | assign | 4 | KEEP (file ADAPT) | C |
| `onSceneImage` | 8496 | assign | 3 | KEEP (file ADAPT) | C |
| `onMetadata` | 8509 | assign | 3 | KEEP (file ADAPT) | C |
| `onStatus` | 8540 | assign | 3 | KEEP (file ADAPT) | C |
| `formatStreamingErrorMessage` | 8566 | const | 0 | KEEP (file ADAPT) | C |
| `cleanupStreamingPlaceholder` | 8580 | const | 0 | KEEP (file ADAPT) | C |
| `markStreamingEntryUnsaved` | 8603 | const | 0 | KEEP (file ADAPT) | C |
| `recoverFailedTurn` | 8615 | const | 0 | KEEP (file ADAPT) | C |
| `onComplete` | 8652 | assign | 9 | KEEP (file ADAPT) | C |
| `finalizeCompletionRender` | 8851 | const | 0 | KEEP (file ADAPT) | C |
| `onWarning` | 8926 | assign | 4 | KEEP (file ADAPT) | C |
| `onError` | 8945 | assign | 13 | KEEP (file ADAPT) | C |
| `onStreamEnd` | 9000 | assign | 4 | KEEP (file ADAPT) | C |
| `handleRegularInteraction` | 9138 | const | 0 | KEEP (file ADAPT) | C |
| `getFormattedStoryText` | 9538 | function | 0 | KEEP (file ADAPT) | C |
| `downloadSingleFormat` | 9547 | function | 0 | KEEP (file ADAPT) | C |
| `downloadFile` | 9589 | function | 0 | KEEP (file ADAPT) | C |
| `handleDownloadClick` | 9617 | function | 0 | KEEP (file ADAPT) | C |
| `handleCampaignDetailsClick` | 9630 | function | 0 | KEEP (file ADAPT) | C |
| `handleShareStory` | 9672 | function | 0 | KEEP (file ADAPT) | C |
| `handleShareStoryConfirm` | 9763 | function | 0 | KEEP (file ADAPT) | C |
| `handleShareStoryCopy` | 9854 | function | 0 | KEEP (file ADAPT) | C |
| `handleUndoStory` | 9885 | function | 0 | KEEP (file ADAPT) | C |
| `loadModelConstants` | 9978 | function | 0 | KEEP (file ADAPT) | C |
| `showSpicyModeToast` | 10007 | function | 0 | KEEP (file ADAPT) | C |
| `handleSpicyModeToggle` | 10059 | function | 0 | KEEP (file ADAPT) | C |
| `loadSpicyModeState` | 10184 | function | 0 | KEEP (file ADAPT) | C |
| `handleMechanicsHiddenToggle` | 10222 | function | 0 | KEEP (file ADAPT) | C |
| `loadMechanicsHiddenState` | 10239 | function | 0 | KEEP (file ADAPT) | C |
| `registerAppAuthObserver` | 10294 | const | 0 | KEEP (file ADAPT) | C |
| `handleBannerDismiss` | 10376 | const | 0 | KEEP (file ADAPT) | C |
| `navigateToSettings` | 10443 | function | 0 | KEEP (file ADAPT) | C |
| `campaignIdFromPath` | 10480 | const | 0 | KEEP (file ADAPT) | C |
| `pushState` | 10502 | assign | 1 | KEEP (file ADAPT) | C |
| `showCancelPendingModal` | 10548 | const | 0 | KEEP (file ADAPT) | C |

### `auth.js` — 91 symbols, file verdict ADAPT, loaded: index.html:626 (defer)

File ADAPT (run 2 confirmed): one auth path; OpenRouter finish/welcome dedup with settings.js; test-mode bypass gated out. Run-2 verdict CONFIRMED. (Run-2-named __ALLOW_TEST_MODE__/testAuthBypass are non-function wiring/consts, not function units, so they have no row here; their ADAPT stands at file level.)

Lens A: loaded file; symbols are live except named exceptions. Lens B: comments/docstrings checked; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `resolveAuthDomain` | 44 | function | 0 | KEEP (file ADAPT) | C |
| `isAffectedIOSWebKitBrowser` | 85 | const | 0 | KEEP (file ADAPT) | C |
| `safeDiag` | 137 | const | 28 W | KEEP (file ADAPT) | C |
| `isMobileUserAgent` | 170 | const | 0 | KEEP (file ADAPT) | C |
| `canEnableTestMode` | 209 | const | 2 | ADAPT — Test-mode gate in shipped auth: DELETE or gate out of production builds. | C |
| `markForceGoogleAccountSelect` | 233 | const | 0 | KEEP (file ADAPT) | C |
| `shouldForceGoogleAccountSelect` | 239 | const | 0 | KEEP (file ADAPT) | C |
| `clearForceGoogleAccountSelect` | 247 | const | 0 | KEEP (file ADAPT) | C |
| `getBaseAuthHeaders` | 254 | const | 0 | KEEP (file ADAPT) | C |
| `getTestModeParams` | 293 | const | 0 | ADAPT — Test-mode gate in shipped auth: DELETE or gate out of production builds. | C |
| `getEffectiveWaitlistUid` | 315 | const | 0 | KEEP (file ADAPT) | C |
| `getWaitlistStatus` | 320 | const | 0 | KEEP (file ADAPT) | C |
| `hasSiteAccess` | 399 | const | 6 | KEEP (file ADAPT) | C |
| `submitWaitlistRequest` | 407 | const | 0 | KEEP (file ADAPT) | C |
| `scheduleTokenRefresh` | 430 | objmethod | 0 | KEEP (file ADAPT) | C |
| `clearTokenRefreshTimer` | 431 | objmethod | 0 | KEEP (file ADAPT) | C |
| `waitForAuthInit` | 434 | objmethod | 11 | KEEP (file ADAPT) | C |
| `waitForRedirectReady` | 435 | objmethod | 2 | KEEP (file ADAPT) | C |
| `waitForPersistenceReady` | 440 | objmethod | 5 | KEEP (file ADAPT) | C |
| `getEffectiveUser` | 444 | objmethod | 17 | KEEP (file ADAPT) | C |
| `getAuthHeaders` | 458 | objmethod | 37 | KEEP (file ADAPT) | C |
| `getCurrentUser` | 472 | objmethod | 4 | KEEP (file ADAPT) | C |
| `signIn` | 476 | objmethod | 2 | KEEP (file ADAPT) | C |
| `getNowMs` | 495 | const | 0 | KEEP (file ADAPT) | C |
| `nextSigninAttemptId` | 500 | const | 0 | KEEP (file ADAPT) | C |
| `getDiagPathname` | 505 | const | 0 | KEEP (file ADAPT) | C |
| `getAuthCallbackDeltaSincePopupStart` | 511 | const | 0 | KEEP (file ADAPT) | C |
| `isCurrentAuthCallback` | 519 | const | 0 | KEEP (file ADAPT) | C |
| `skipStaleAuthCallback` | 521 | const | 0 | KEEP (file ADAPT) | C |
| `getSigninContextFields` | 529 | const | 0 | KEEP (file ADAPT) | C |
| `app_origin` | 537 | objmethod | 0 | KEEP (file ADAPT) | C |
| `cookie_enabled` | 540 | objmethod | 1 | KEEP (file ADAPT) | C |
| `getPopupDiagFields` | 548 | const | 0 | KEEP (file ADAPT) | C |
| `provider` | 553 | objmethod | 61 | KEEP (file ADAPT) | C |
| `online` | 554 | objmethod | 10 | KEEP (file ADAPT) | C |
| `visibility` | 555 | objmethod | 18 | KEEP (file ADAPT) | C |
| `body_classes` | 564 | objmethod | 0 | KEEP (file ADAPT) | C |
| `flushDiagNow` | 570 | const | 0 | KEEP (file ADAPT) | C |
| `clearPopupPendingTimer` | 578 | const | 0 | KEEP (file ADAPT) | C |
| `schedulePopupPendingDiag` | 585 | const | 0 | KEEP (file ADAPT) | C |
| `handlePopupPageLifecycle` | 597 | const | 0 | KEEP (file ADAPT) | C |
| `logAuthReturnContext` | 611 | const | 0 | KEEP (file ADAPT) | C |
| `visibility` | 661 | objmethod | 18 | KEEP (file ADAPT) | C |
| `is_iframe` | 668 | objmethod | 0 | KEEP (file ADAPT) | C |
| `registerAuthObserverOnce` | 684 | const | 0 | KEEP (file ADAPT) | C |
| `operation_type` | 714 | objmethod | 0 | KEEP (file ADAPT) | C |
| `user_uid` | 823 | objmethod | 0 | KEEP (file ADAPT) | C |
| `user_uid` | 832 | objmethod | 0 | KEEP (file ADAPT) | C |
| `user_uid` | 842 | objmethod | 0 | KEEP (file ADAPT) | C |
| `error_code` | 843 | objmethod | 0 | KEEP (file ADAPT) | C |
| `user_uid` | 864 | objmethod | 0 | KEEP (file ADAPT) | C |
| `error_code` | 865 | objmethod | 0 | KEEP (file ADAPT) | C |
| `signIn` | 877 | const | 2 | KEEP (file ADAPT) | C |
| `online` | 891 | objmethod | 10 | KEEP (file ADAPT) | C |
| `body_classes` | 892 | objmethod | 0 | KEEP (file ADAPT) | C |
| `provider` | 937 | objmethod | 61 | KEEP (file ADAPT) | C |
| `provider` | 960 | objmethod | 61 | KEEP (file ADAPT) | C |
| `isOpenRouterFinishPage` | 1085 | function | 0 | KEEP (file ADAPT) | C |
| `cleanOpenRouterFinishUrl` | 1089 | function | 0 | KEEP (file ADAPT) | C |
| `OPENROUTER_FINISH_SHELL` | 1095 | const | 0 | KEEP (file ADAPT) | C |
| `renderOpenRouterFinishing` | 1122 | function | 0 | KEEP (file ADAPT) | C |
| `renderOpenRouterFinish` | 1128 | function | 0 | KEEP (file ADAPT) | C |
| `onclick` | 1140 | assign | 25 | KEEP (file ADAPT) | C |
| `onclick` | 1141 | assign | 25 | KEEP (file ADAPT) | C |
| `openRouterFinishStateForError` | 1148 | function | 0 | KEEP (file ADAPT) | C |
| `revealOpenRouterWelcomeIfAvailable` | 1155 | function | 0 | KEEP (file ADAPT) | C |
| `startOpenRouterWelcomeSignIn` | 1167 | function | 0 | KEEP (file ADAPT) | C |
| `completeOpenRouterWelcomeSignIn` | 1219 | function | 0 | KEEP (file ADAPT) | C |
| `getLoggedOutAuthMarkup` | 1293 | const | 0 | KEEP (file ADAPT) | C |
| `getWaitlistRequestMarkup` | 1361 | const | 0 | KEEP (file ADAPT) | C |
| `wireWaitlistRequestMarkup` | 1420 | const | 0 | KEEP (file ADAPT) | C |
| `onclick` | 1425 | assign | 25 | KEEP (file ADAPT) | C |
| `onclick` | 1458 | assign | 25 | KEEP (file ADAPT) | C |
| `renderWaitlistRequestView` | 1462 | const | 0 | KEEP (file ADAPT) | C |
| `getConnectingMarkup` | 1473 | const | 0 | KEEP (file ADAPT) | C |
| `signOut` | 1515 | const | 0 | KEEP (file ADAPT) | C |
| `online` | 1590 | objmethod | 10 | KEEP (file ADAPT) | C |
| `visibility` | 1591 | objmethod | 18 | KEEP (file ADAPT) | C |
| `onclick` | 1679 | assign | 25 | KEEP (file ADAPT) | C |
| `handleVisibilityRecovery` | 1714 | const | 0 | KEEP (file ADAPT) | C |
| `online` | 1723 | objmethod | 10 | KEEP (file ADAPT) | C |
| `visibility` | 1724 | objmethod | 18 | KEEP (file ADAPT) | C |
| `online` | 1765 | objmethod | 10 | KEEP (file ADAPT) | C |
| `visibility` | 1766 | objmethod | 18 | KEEP (file ADAPT) | C |
| `online` | 1790 | objmethod | 10 | KEEP (file ADAPT) | C |
| `visibility` | 1854 | objmethod | 18 | KEEP (file ADAPT) | C |
| `visibility` | 1871 | objmethod | 18 | KEEP (file ADAPT) | C |
| `registerAuthObserver` | 1876 | function | 0 | KEEP (file ADAPT) | C |
| `onclick` | 2014 | assign | 25 | KEEP (file ADAPT) | C |
| `pointer_type` | 2023 | objmethod | 0 | KEEP (file ADAPT) | C |
| `onclick` | 2034 | assign | 25 | KEEP (file ADAPT) | C |

### `diag-boot.js` — 2 symbols, file verdict KEEP, loaded: index.html:28

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `boot` | 15 | function | 8 W | KEEP | C |
| `ua` | 19 | objmethod | 10 | KEEP | C |

### `diagnostics.js` — 26 symbols, file verdict KEEP, loaded: index.html:624 (defer)

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `safeStringify` | 58 | function | 0 | KEEP | C |
| `envCapture` | 71 | function | 0 | KEEP | C |
| `nowMs` | 116 | function | 4 | KEEP | C |
| `event` | 128 | function | 222 | KEEP | C |
| `setContext` | 161 | function | 0 | KEEP | C |
| `getContext` | 172 | function | 2 | KEEP | C |
| `buildPayload` | 178 | function | 0 | KEEP | C |
| `user_agent` | 183 | objmethod | 1 | KEEP | C |
| `sendBeacon` | 189 | function | 5 | KEEP | C |
| `fetchKeepalive` | 201 | function | 0 | KEEP | C |
| `flush` | 237 | function | 3 | KEEP | C |
| `clearSent` | 254 | function | 0 | KEEP | C |
| `fetchKeepalive` | 270 | method | 0 | KEEP | C |
| `fetchKeepalive` | 282 | method | 0 | KEEP | C |
| `installErrorHandlers` | 294 | function | 0 | KEEP | C |
| `onerror` | 301 | assign | 7 W | KEEP | C |
| `onunhandledrejection` | 321 | assign | 1 W | KEEP | C |
| `installFlushTimer` | 357 | function | 0 | KEEP | C |
| `drainBootQueue` | 378 | function | 0 | KEEP | C |
| `_bufferSize` | 405 | objmethod | 0 | KEEP | C |
| `_buffer` | 406 | objmethod | 0 | KEEP | C |
| `_reset` | 407 | objmethod | 0 | KEEP | C |
| `_setFetch` | 409 | objmethod | 0 | KEEP | C |
| `_setSendBeacon` | 410 | objmethod | 0 | KEEP | C |
| `_sessionId` | 411 | objmethod | 4 | KEEP | C |
| `ua_kind` | 431 | objmethod | 0 | KEEP | C |

### `js/animation-helpers.js` — 32 symbols, file verdict ADAPT, loaded: index.html:631 (defer)

File ADAPT (run 2 confirmed): animation/loading helpers KEEP; interception/patching DELETE (named below).

Lens A: loaded file; symbols are live except named exceptions. Lens B: comments/docstrings checked; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `AnimationHelpers` | 7 | class | 0 | KEEP (file ADAPT) | C |
| `constructor` | 8 | method | 13 | KEEP (file ADAPT) | C |
| `init` | 14 | method | 29 W | KEEP (file ADAPT) | C |
| `enhanceExistingFunctionality` | 24 | method | 0 | DELETE — Runtime patching of existing handlers, not presentation. | C |
| `interceptViewSwitching` | 35 | method | 0 | DELETE — Behaviour interception, not presentation. | C |
| `showView` | 41 | assign | 9 | KEEP (file ADAPT) | C |
| `animatedShowView` | 50 | method | 0 | KEEP (file ADAPT) | C |
| `fadeOutView` | 84 | method | 0 | KEEP (file ADAPT) | C |
| `fadeInView` | 99 | method | 0 | KEEP (file ADAPT) | C |
| `setupLoadingStates` | 121 | method | 0 | KEEP (file ADAPT) | C |
| `originalShowLoading` | 125 | assign | 0 | DELETE — Captured only to support patching. | C |
| `originalHideLoading` | 130 | assign | 0 | DELETE — Captured only to support patching. | C |
| `originalSpinnerShow` | 142 | const | 0 | DELETE — Captured only to support patching. | C |
| `originalSpinnerHide` | 149 | const | 0 | DELETE — Captured only to support patching. | C |
| `enhanceFormSubmissions` | 165 | method | 0 | KEEP (file ADAPT) | C |
| `addButtonLoadingState` | 182 | method | 0 | KEEP (file ADAPT) | C |
| `removeButtonLoadingState` | 197 | method | 2 | KEEP (file ADAPT) | C |
| `setupViewTransitions` | 207 | method | 0 | KEEP (file ADAPT) | C |
| `enhanceButtonFeedback` | 226 | method | 0 | KEEP (file ADAPT) | C |
| `animateButtonClick` | 237 | method | 0 | KEEP (file ADAPT) | C |
| `showStoryLoading` | 248 | method | 0 | KEEP (file ADAPT) | C |
| `hideStoryLoading` | 258 | method | 0 | KEEP (file ADAPT) | C |
| `getAPI` | 268 | method | 0 | KEEP (file ADAPT) | C |
| `showView` | 270 | objmethod | 9 | KEEP (file ADAPT) | C |
| `showLoading` | 271 | objmethod | 0 | KEEP (file ADAPT) | C |
| `hideLoading` | 272 | objmethod | 0 | KEEP (file ADAPT) | C |
| `addButtonLoading` | 273 | objmethod | 0 | KEEP (file ADAPT) | C |
| `removeButtonLoading` | 274 | objmethod | 0 | KEEP (file ADAPT) | C |
| `removeButtonLoadingState` | 275 | objmethod | 2 | KEEP (file ADAPT) | C |
| `showStoryLoading` | 276 | objmethod | 0 | KEEP (file ADAPT) | C |
| `hideStoryLoading` | 277 | objmethod | 0 | KEEP (file ADAPT) | C |
| `smoothScrollTo` | 292 | function | 0 | KEEP (file ADAPT) | C |

### `js/avatar-crop.js` — 9 symbols, file verdict KEEP, loaded: index.html:633 (defer)

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `show` | 29 | function | 63 W | KEEP | C |
| `onload` | 50 | assign | 8 | KEEP | C |
| `onPointerDown` | 74 | const | 0 | KEEP | C |
| `onPointerMove` | 84 | const | 0 | KEEP | C |
| `onPointerUp` | 94 | const | 0 | KEEP | C |
| `_doCrop` | 135 | function | 0 | KEEP | C |
| `getCroppedFile` | 178 | function | 2 | KEEP | C |
| `getCroppedUrl` | 185 | function | 1 | KEEP | C |
| `destroy` | 192 | function | 12 | KEEP | C |

### `js/campaign-wizard.js` — 84 symbols, file verdict ADAPT, loaded: index.html:636 (defer)

File ADAPT (run 2 confirmed): step flow/validation/launch POST KEEP; premade/IP copy to data, telemetry via diagnostics.js, portrait work collapsed into portrait-ai.js. No individual symbol DELETE; ADAPT is file-level.

Lens A: loaded file; symbols are live except named exceptions. Lens B: comments/docstrings checked; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `isMobileViewport` | 12 | function | 0 | KEEP (file ADAPT) | C |
| `applyMobileScrollLock` | 25 | function | 0 | KEEP (file ADAPT) | C |
| `releaseMobileScrollLock` | 41 | function | 0 | KEEP (file ADAPT) | C |
| `isScrolledToBottom` | 59 | function | 0 | KEEP (file ADAPT) | C |
| `updateScrollIndicator` | 71 | function | 0 | KEEP (file ADAPT) | C |
| `CampaignWizard` | 126 | class | 2 | KEEP (file ADAPT) | C |
| `getDefaultTitle` | 139 | method | 0 | KEEP (file ADAPT) | C |
| `formatIpMarker` | 166 | method | 0 | KEEP (file ADAPT) | C |
| `extractIpFieldsFromDescription` | 183 | method | 0 | KEEP (file ADAPT) | C |
| `descriptionIsMarkerPure` | 253 | method | 0 | KEEP (file ADAPT) | C |
| `constructor` | 759 | method | 12 | KEEP (file ADAPT) | C |
| `resetCampaignTypeState` | 779 | method | 0 | KEEP (file ADAPT) | C |
| `syncCampaignTypeUI` | 784 | method | 0 | KEEP (file ADAPT) | C |
| `init` | 796 | method | 26 W | KEEP (file ADAPT) | C |
| `checkIfEnabled` | 804 | method | 2 | KEEP (file ADAPT) | C |
| `enable` | 820 | method | 21 | KEEP (file ADAPT) | C |
| `disable` | 835 | method | 15 | KEEP (file ADAPT) | C |
| `forceCleanRecreation` | 840 | method | 0 | KEEP (file ADAPT) | C |
| `setupWizard` | 889 | method | 0 | KEEP (file ADAPT) | C |
| `_clearPrefilledShareFields` | 919 | method | 0 | KEEP (file ADAPT) | C |
| `applyUrlParams` | 960 | method | 3 | KEEP (file ADAPT) | C |
| `setIfPresent` | 1023 | const | 0 | KEEP (file ADAPT) | C |
| `replaceOriginalForm` | 1159 | method | 0 | KEEP (file ADAPT) | C |
| `setupScrollIndicator` | 1230 | method | 0 | KEEP (file ADAPT) | C |
| `onScroll` | 1247 | const | 3 | KEEP (file ADAPT) | C |
| `onResize` | 1274 | const | 0 | KEEP (file ADAPT) | C |
| `restoreOriginalForm` | 1314 | method | 0 | KEEP (file ADAPT) | C |
| `generateWizardHTML` | 1370 | method | 0 | KEEP (file ADAPT) | C |
| `setupStepNavigation` | 1656 | method | 0 | KEEP (file ADAPT) | C |
| `setupEventListeners` | 1690 | method | 8 | KEEP (file ADAPT) | C |
| `loadInitialCampaignContent` | 1802 | method | 0 | KEEP (file ADAPT) | C |
| `renumberVisibleFields` | 1880 | method | 0 | KEEP (file ADAPT) | C |
| `handleCampaignTypeChange` | 1910 | method | 0 | KEEP (file ADAPT) | C |
| `populateFromOriginalForm` | 2088 | method | 0 | KEEP (file ADAPT) | C |
| `nextStep` | 2107 | method | 0 | KEEP (file ADAPT) | C |
| `previousStep` | 2123 | method | 0 | KEEP (file ADAPT) | C |
| `goToStep` | 2129 | method | 0 | KEEP (file ADAPT) | C |
| `_kickWizardPortraitPrefetch` | 2186 | method | 0 | KEEP (file ADAPT) | C |
| `_scheduleWizardPortraitPrefetch` | 2192 | method | 0 | KEEP (file ADAPT) | C |
| `_loadArionAvatar` | 2204 | method | 0 | KEEP (file ADAPT) | C |
| `updateUI` | 2239 | method | 0 | KEEP (file ADAPT) | C |
| `validateCurrentStep` | 2308 | method | 0 | KEEP (file ADAPT) | C |
| `validateLaunchReadiness` | 2327 | method | 0 | KEEP (file ADAPT) | C |
| `setLaunchButtonsDisabled` | 2351 | method | 0 | KEEP (file ADAPT) | C |
| `resetLaunchState` | 2362 | method | 0 | KEEP (file ADAPT) | C |
| `logWizardTelemetry` | 2367 | method | 0 | KEEP (file ADAPT) | C |
| `attemptLaunch` | 2374 | method | 0 | KEEP (file ADAPT) | C |
| `commitPendingPreviewEdits` | 2401 | method | 0 | KEEP (file ADAPT) | C |
| `_formatDescription` | 2414 | method | 0 | KEEP (file ADAPT) | C |
| `_formatCharacter` | 2426 | method | 0 | KEEP (file ADAPT) | C |
| `updatePreview` | 2434 | method | 0 | KEEP (file ADAPT) | C |
| `_handleIPFieldChange` | 2506 | method | 0 | KEEP (file ADAPT) | C |
| `collectFormData` | 2554 | method | 0 | KEEP (file ADAPT) | C |
| `getStructuredCreateFields` | 2608 | method | 1 | KEEP (file ADAPT) | C |
| `launchCampaign` | 2619 | method | 0 | KEEP (file ADAPT) | C |
| `showDetailedSpinner` | 2650 | method | 1 | KEEP (file ADAPT) | C |
| `animateCreationProgress` | 2721 | method | 0 | KEEP (file ADAPT) | C |
| `updateProgress` | 2761 | const | 0 | KEEP (file ADAPT) | C |
| `completeProgress` | 2797 | method | 2 | KEEP (file ADAPT) | C |
| `setupAvatarHandlers` | 2816 | method | 0 | KEEP (file ADAPT) | C |
| `getWizardPortraitSuggestPayload` | 2877 | method | 0 | KEEP (file ADAPT) | C |
| `setAvatarSourceMode` | 2903 | method | 0 | KEEP (file ADAPT) | C |
| `onFilled` | 2930 | objmethod | 10 | KEEP (file ADAPT) | C |
| `wizardPortraitButtons` | 2942 | method | 0 | KEEP (file ADAPT) | C |
| `setWizardPortraitStatus` | 2949 | method | 0 | KEEP (file ADAPT) | C |
| `refreshWizardPortraitSuggestion` | 2961 | method | 0 | KEEP (file ADAPT) | C |
| `onFilled` | 2977 | objmethod | 10 | KEEP (file ADAPT) | C |
| `generateWizardPortrait` | 2988 | method | 0 | KEEP (file ADAPT) | C |
| `generateFn` | 3001 | objmethod | 3 | KEEP (file ADAPT) | C |
| `onCommit` | 3006 | objmethod | 6 | KEEP (file ADAPT) | C |
| `ensureWizardPortraitPanel` | 3040 | method | 0 | KEEP (file ADAPT) | C |
| `wizardPortraitPanelRoot` | 3056 | method | 0 | KEEP (file ADAPT) | C |
| `setupPortraitAiWizardHandlers` | 3060 | method | 0 | KEEP (file ADAPT) | C |
| `commitWizardPortraitPreview` | 3079 | method | 0 | KEEP (file ADAPT) | C |
| `onload` | 3154 | assign | 10 | KEEP (file ADAPT) | C |
| `clearAvatar` | 3180 | method | 0 | KEEP (file ADAPT) | C |
| `uploadCampaignAvatar` | 3211 | method | 2 | KEEP (file ADAPT) | C |
| `resetWizard` | 3293 | method | 0 | KEEP (file ADAPT) | C |
| `setupEditablePreview` | 3368 | method | 0 | KEEP (file ADAPT) | C |
| `toggleEditMode` | 3432 | method | 0 | KEEP (file ADAPT) | C |
| `getFormValueForField` | 3481 | method | 0 | KEEP (file ADAPT) | C |
| `syncEditToForm` | 3496 | method | 0 | KEEP (file ADAPT) | C |
| `updatePreviewFromForm` | 3533 | method | 0 | KEEP (file ADAPT) | C |
| `populateOriginalForm` | 3555 | method | 0 | KEEP (file ADAPT) | C |

### `js/component-enhancer.js` — 33 symbols, file verdict DELETE, loaded: NEVER LOADED — no tag, no dynamic load

File DELETE (run 2 confirmed, wording corrected in §4): never loaded. NOTE: interface-manager.js:91,99 do reference window.componentEnhancer under guards — those guards are no-ops while the file is unloaded, so the DELETE stands; run 2's "no shipped code references the export" is corrected to "no shipped code loads it; only guarded no-op references exist".

Lens A: NEVER LOADED — no index.html tag, no dynamic loader, no shipped caller; all symbols unreachable in the shipped page. Lens B: comments describe behaviour that never runs in the product; deleting the file deletes its docs with it.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `ComponentEnhancer` | 7 | class | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `constructor` | 8 | method | 13 | DELETE — unloaded file, unreachable symbol. | C |
| `isFeatureEnabled` | 25 | method | 1 | DELETE — unloaded file, unreachable symbol. | C |
| `init` | 32 | method | 27 W | DELETE — unloaded file, unreachable symbol. | C |
| `loadEnhancedCSS` | 63 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `enhanceExistingComponents` | 87 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `enhanceButtons` | 100 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `enhanceCards` | 125 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `enhanceForms` | 149 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `enhanceModals` | 188 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `enhanceNavigation` | 204 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `enhanceContent` | 231 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `enhanceLoadingStates` | 254 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `createRippleEffect` | 275 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `handleButtonLoading` | 296 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `handleFormFocus` | 318 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `handleFormBlur` | 330 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `handleModalShow` | 342 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `handleModalHide` | 356 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `playHoverSound` | 365 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `setupEventListeners` | 373 | method | 9 | DELETE — unloaded file, unreachable symbol. | C |
| `setupMutationObserver` | 395 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `enhanceNewElement` | 420 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `handleKeyboardNavigation` | 464 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `handleScroll` | 475 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `handleThemeChange` | 484 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `debounce` | 494 | method | 11 | DELETE — unloaded file, unreachable symbol. | C |
| `later` | 497 | const | 20 | DELETE — unloaded file, unreachable symbol. | C |
| `enable` | 509 | method | 23 | DELETE — unloaded file, unreachable symbol. | C |
| `disable` | 518 | method | 14 | DELETE — unloaded file, unreachable symbol. | C |
| `toggle` | 527 | method | 107 W | DELETE — unloaded file, unreachable symbol. | C |
| `cleanup` | 539 | method | 35 | DELETE — unloaded file, unreachable symbol. | C |
| `getStatus` | 575 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |

### `js/ember-bg.js` — 13 symbols, file verdict KEEP, loaded: index.html:643 (defer)

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `spawnParticle` | 9 | function | 0 | KEEP | C |
| `vx` | 14 | objmethod | 0 | KEEP | C |
| `initParticles` | 22 | function | 0 | KEEP | C |
| `prefersReducedMotion` | 46 | function | 0 | KEEP | C |
| `buildGradient` | 50 | function | 0 | KEEP | C |
| `drawStatic` | 59 | function | 0 | KEEP | C |
| `resize` | 67 | function | 11 | KEEP | C |
| `draw` | 74 | function | 0 | KEEP | C |
| `animate` | 100 | function | 0 W | KEEP | C |
| `isFantasyTheme` | 107 | function | 0 | KEEP | C |
| `start` | 111 | function | 61 | KEEP | C |
| `stop` | 121 | function | 12 | KEEP | C |
| `onMotionChange` | 143 | function | 0 | KEEP | C |

### `js/enhanced-search.js` — 34 symbols, file verdict KEEP, loaded: index.html:637 (defer)

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `EnhancedSearch` | 6 | class | 0 | KEEP | C |
| `constructor` | 7 | method | 13 | KEEP | C |
| `debounce` | 23 | method | 8 | KEEP | C |
| `later` | 26 | const | 20 | KEEP | C |
| `init` | 35 | method | 29 W | KEEP | C |
| `checkIfEnabled` | 43 | method | 2 | KEEP | C |
| `enable` | 59 | method | 23 | KEEP | C |
| `disable` | 64 | method | 15 | KEEP | C |
| `setupSearchInterface` | 69 | method | 0 | KEEP | C |
| `removeSearchInterface` | 89 | method | 0 | KEEP | C |
| `generateSearchHTML` | 96 | method | 0 | KEEP | C |
| `setupEventListeners` | 191 | method | 9 | KEEP | C |
| `updateSortOrderLabel` | 269 | method | 0 | KEEP | C |
| `observeCampaignList` | 285 | method | 0 | KEEP | C |
| `refreshCampaignData` | 308 | method | 0 | KEEP | C |
| `parseDateFromElement` | 350 | method | 0 | KEEP | C |
| `extractCreatedDate` | 362 | method | 0 | KEEP | C |
| `buildSearchText` | 373 | method | 0 | KEEP | C |
| `applyFilters` | 391 | method | 0 | KEEP | C |
| `sortCampaigns` | 435 | method | 0 | KEEP | C |
| `updateDisplay` | 460 | method | 0 | KEEP | C |
| `showNoResultsMessage` | 489 | method | 0 | KEEP | C |
| `updateStats` | 511 | method | 0 | KEEP | C |
| `updateFilterTags` | 541 | method | 0 | KEEP | C |
| `removeFilter` | 598 | method | 0 | KEEP | C |
| `clearAllFilters` | 618 | method | 0 | KEEP | C |
| `syncFormControls` | 631 | method | 0 | KEEP | C |
| `search` | 648 | method | 47 | KEEP | C |
| `setFilter` | 657 | method | 0 | KEEP | C |
| `getResults` | 673 | method | 0 | KEEP | C |
| `getTotalCount` | 677 | method | 0 | KEEP | C |
| `getFilteredCount` | 681 | method | 0 | KEEP | C |
| `getActiveFilterCount` | 685 | method | 0 | KEEP | C |
| `updateFilterBadge` | 694 | method | 0 | KEEP | C |

### `js/inline-editor.js` — 18 symbols, file verdict KEEP, loaded: index.html:642 (defer)

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `InlineEditor` | 12 | class | 10 W | KEEP | C |
| `init` | 50 | method | 29 W | KEEP | C |
| `handleMouseEnter` | 59 | method | 0 | KEEP | C |
| `handleMouseLeave` | 65 | method | 0 | KEEP | C |
| `startEdit` | 69 | method | 1 | KEEP | C |
| `createEditContainer` | 121 | method | 0 | KEEP | C |
| `handleKeydown` | 169 | method | 0 | KEEP | C |
| `handleInput` | 179 | method | 0 | KEEP | C |
| `handleOutsideClick` | 196 | method | 0 | KEEP | C |
| `save` | 202 | method | 56 | KEEP | C |
| `cancel` | 243 | method | 40 | KEEP | C |
| `completeEdit` | 251 | method | 0 | KEEP | C |
| `cleanupOutsideClickHandler` | 291 | method | 0 | KEEP | C |
| `validate` | 300 | method | 0 | KEEP | C |
| `showError` | 316 | method | 0 | KEEP | C |
| `removeError` | 330 | method | 0 | KEEP | C |
| `setLoading` | 337 | method | 0 | KEEP | C |
| `destroy` | 352 | method | 12 | KEEP | C |

### `js/interface-manager.js` — 18 symbols, file verdict KEEP, loaded: index.html:629 (defer)

File KEEP (run 2 confirmed). NOTE: disableEnhancedComponents/enableEnhancedComponents guardedly call window.componentEnhancer (lines 91, 99); harmless no-ops while component-enhancer.js is unloaded, and they do not constitute loading it.

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `InterfaceManager` | 6 | class | 0 | KEEP | C |
| `constructor` | 7 | method | 13 | KEEP | C |
| `init` | 22 | method | 29 W | KEEP | C |
| `setMode` | 28 | method | 0 | KEEP | C |
| `applyMode` | 48 | method | 0 | KEEP | C |
| `enableModernMode` | 53 | method | 0 | KEEP | C |
| `disableAnimations` | 65 | method | 0 | KEEP | C |
| `enableAnimations` | 76 | method | 0 | KEEP | C |
| `disableEnhancedComponents` | 88 | method | 0 | KEEP | C |
| `enableEnhancedComponents` | 96 | method | 0 | KEEP | C |
| `disableInteractiveFeatures` | 105 | method | 0 | KEEP | C |
| `enableInteractiveFeatures` | 110 | method | 0 | KEEP | C |
| `setupEventListeners` | 115 | method | 9 | KEEP | C |
| `getCurrentMode` | 127 | method | 0 | KEEP | C |
| `getModeInfo` | 131 | method | 0 | KEEP | C |
| `isModernMode` | 135 | method | 2 | KEEP | C |
| `isFeatureEnabled` | 140 | method | 5 | KEEP | C |
| `trackModeUsage` | 156 | method | 0 | KEEP | C |

### `js/loading-messages.js` — 7 symbols, file verdict KEEP, loaded: index.html:641 (defer)

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `LoadingMessages` | 3 | class | 0 | KEEP | C |
| `constructor` | 4 | method | 13 | KEEP | C |
| `start` | 50 | method | 65 | KEEP | C |
| `stop` | 76 | method | 10 | KEEP | C |
| `showMessage` | 95 | method | 0 | KEEP | C |
| `getMessageElement` | 109 | method | 0 | KEEP | C |
| `showSingle` | 126 | method | 0 | KEEP | C |

### `js/opening_story.js` — 21 symbols, file verdict KEEP, loaded: index.html:640 (defer)

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `telemetryRoot` | 24 | function | 0 | KEEP | C |
| `beaconOpeningTelemetry` | 31 | function | 0 | KEEP | C |
| `needsOpeningStory` | 64 | function | 1 | KEEP | C |
| `setComposerLocked` | 80 | function | 0 | KEEP | C |
| `setSubmitSync` | 112 | function | 1 | KEEP | C |
| `element` | 116 | function | 157 | KEEP | C |
| `sleepMs` | 123 | function | 0 | KEEP | C |
| `streamOnce` | 128 | function | 0 | KEEP | C |
| `onChunk` | 132 | assign | 10 | KEEP | C |
| `onComplete` | 148 | assign | 14 | KEEP | C |
| `onError` | 151 | assign | 15 | KEEP | C |
| `run` | 183 | function | 86 | KEEP | C |
| `pillShell` | 193 | const | 0 | KEEP | C |
| `setPill` | 194 | const | 0 | KEEP | C |
| `stopLoading` | 203 | const | 0 | KEEP | C |
| `showStatus` | 218 | const | 0 | KEEP | C |
| `showFailure` | 228 | const | 0 | KEEP | C |
| `resetComposerForCampaign` | 332 | function | 3 | KEEP | C |
| `holdsComposer` | 340 | function | 2 | KEEP | C |
| `acquireComposerLock` | 347 | function | 0 | KEEP | C |
| `handOffFromRejectedTurn` | 364 | function | 1 | KEEP | C |

### `js/outcome-verdict.js` — 3 symbols, file verdict ADAPT, loaded: index.html:645 (defer)

File ADAPT (run 2 confirmed): called from app.js:2814–2815 (guarded typeof check) with fullData.action_resolution. Explicit branch KEEP; fallback DELETE.

Lens A: loaded file; symbols are live except named exceptions. Lens B: comments/docstrings checked; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `isSave` | 16 | const | 0 | DELETE — Save-detection regex exists only to serve the fallback. | C |
| `deriveOutcomeVerdict` | 18 | function | 0 | ADAPT — Keep explicit player_outcome branch only; DELETE the roll-aggregation fallback and save regex. | C |
| `outcomeVerdictBadgeHtml` | 31 | function | 2 | KEEP (file ADAPT) | C |

### `js/portrait-ai-ui.js` — 9 symbols, file verdict KEEP, loaded: index.html:634 (defer)

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `getUi` | 7 | const | 6 | KEEP | C |
| `updateCounter` | 18 | const | 5 | KEEP | C |
| `setSuggestLoading` | 37 | method | 2 | KEEP | C |
| `setGenerateLoading` | 42 | method | 2 | KEEP | C |
| `clearPreview` | 53 | method | 2 | KEEP | C |
| `setPendingPreview` | 65 | method | 1 | KEEP | C |
| `showPreviewFromResult` | 72 | method | 1 | KEEP | C |
| `onerror` | 86 | assign | 7 W | KEEP | C |
| `onload` | 93 | assign | 9 | KEEP | C |

### `js/portrait-ai.js` — 79 symbols, file verdict ADAPT, loaded: index.html:635 (defer)

File ADAPT (run 2 confirmed): transport/caching/panel KEEP; prose recomposition DELETE; compare pair DELETE with portrait_model_compare.py; one prefetch path.

Lens A: loaded file; symbols are live except named exceptions. Lens B: comments/docstrings checked; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `withTimeout` | 12 | const | 0 | KEEP (file ADAPT) | C |
| `getAuthHeaders` | 32 | const | 38 | KEEP (file ADAPT) | C |
| `getAuthHeadersWithTimeout` | 43 | const | 0 | KEEP (file ADAPT) | C |
| `postJson` | 50 | const | 0 | KEEP (file ADAPT) | C |
| `fetchPreviewBytesFromServer` | 80 | const | 0 | KEEP (file ADAPT) | C |
| `previewResultToFile` | 101 | const | 0 | KEEP (file ADAPT) | C |
| `base64ToFile` | 124 | const | 1 | KEEP (file ADAPT) | C |
| `looksLikeRawPortraitJson` | 139 | const | 0 | KEEP (file ADAPT) | C |
| `isDisplayablePortraitDescription` | 152 | const | 0 | KEEP (file ADAPT) | C |
| `composePortraitProseFromAppearance` | 155 | const | 0 | DELETE — Client-side authoring of the portrait description from appearance slots. | C |
| `sanitizeSuggestApiResult` | 182 | const | 0 | ADAPT — Remove the recomposed-prose substitution; fall back to player text or no suggestion. | C |
| `suggestCacheKey` | 202 | const | 0 | KEEP (file ADAPT) | C |
| `getCachedSuggest` | 211 | const | 0 | KEEP (file ADAPT) | C |
| `invalidateSuggestCache` | 228 | const | 0 | KEEP (file ADAPT) | C |
| `rememberSuggest` | 235 | const | 0 | KEEP (file ADAPT) | C |
| `suggestDescription` | 249 | const | 0 | KEEP (file ADAPT) | C |
| `ensurePortraitSuggestionFilled` | 286 | const | 1 | KEEP (file ADAPT) | C |
| `onFilled` | 342 | objmethod | 2 | KEEP (file ADAPT) | C |
| `prefetchCampaignSuggestion` | 346 | const | 0 | KEEP (file ADAPT) | C |
| `cloneServerTimingMs` | 353 | const | 0 | KEEP (file ADAPT) | C |
| `logPortraitTimingMs` | 364 | const | 0 | KEEP (file ADAPT) | C |
| `logWarmTiming` | 372 | const | 0 | KEEP (file ADAPT) | C |
| `warmPortraitTransport` | 377 | const | 1 | KEEP (file ADAPT) | C |
| `warmCampaignPortrait` | 389 | const | 0 | KEEP (file ADAPT) | C |
| `prefetchCampaignPortraitPipeline` | 404 | const | 2 | KEEP (file ADAPT) | C |
| `prefetchWizardPortraitSuggestion` | 410 | const | 0 | KEEP (file ADAPT) | C |
| `prefetchWizardPortraitPipeline` | 418 | const | 2 | KEEP (file ADAPT) | C |
| `applyCachedPortraitSuggestion` | 424 | const | 0 | KEEP (file ADAPT) | C |
| `logPortraitSuggestTiming` | 433 | const | 0 | KEEP (file ADAPT) | C |
| `portraitSuggestExtrasForGenerate` | 437 | const | 0 | KEEP (file ADAPT) | C |
| `portraitProviderPreferencePayload` | 466 | const | 0 | KEEP (file ADAPT) | C |
| `logPortraitGenerateTiming` | 480 | const | 1 | KEEP (file ADAPT) | C |
| `generatePreview` | 495 | const | 1 | KEEP (file ADAPT) | C |
| `generateForCampaign` | 510 | const | 0 | KEEP (file ADAPT) | C |
| `applyCampaignPortraitPreview` | 515 | const | 2 | KEEP (file ADAPT) | C |
| `ensurePortraitCommitWiring` | 540 | const | 0 | KEEP (file ADAPT) | C |
| `ui` | 548 | const | 6 | KEEP (file ADAPT) | C |
| `ensureStatusUI` | 593 | const | 1 | KEEP (file ADAPT) | C |
| `setStatusLoading` | 606 | const | 2 | KEEP (file ADAPT) | C |
| `setButtonsDisabled` | 634 | const | 0 | KEEP (file ADAPT) | C |
| `panelUi` | 640 | const | 2 | KEEP (file ADAPT) | C |
| `clearPortraitLoading` | 645 | const | 0 | KEEP (file ADAPT) | C |
| `resolveSuggestContext` | 668 | const | 0 | KEEP (file ADAPT) | C |
| `runSuggestWithUI` | 681 | const | 3 | KEEP (file ADAPT) | C |
| `resolveCtx` | 692 | const | 0 | KEEP (file ADAPT) | C |
| `run` | 695 | const | 82 | KEEP (file ADAPT) | C |
| `runGenerateWithUI` | 761 | const | 3 | KEEP (file ADAPT) | C |
| `resolveCtx` | 772 | const | 0 | KEEP (file ADAPT) | C |
| `currentDescription` | 775 | const | 0 | KEEP (file ADAPT) | C |
| `run` | 791 | const | 82 | KEEP (file ADAPT) | C |
| `onCommit` | 795 | objmethod | 1 | KEEP (file ADAPT) | C |
| `resolveDescriptionInput` | 842 | const | 0 | KEEP (file ADAPT) | C |
| `ensureModalPanelMarkup` | 858 | const | 0 | KEEP (file ADAPT) | C |
| `bindModalPortraitContext` | 877 | const | 0 | KEEP (file ADAPT) | C |
| `nextFrame` | 901 | const | 0 | KEEP (file ADAPT) | C |
| `waitForPortraitPanel` | 910 | const | 0 | KEEP (file ADAPT) | C |
| `fillDescriptionInput` | 922 | const | 0 | KEEP (file ADAPT) | C |
| `suppressExternalPortraitPanels` | 930 | const | 0 | KEEP (file ADAPT) | C |
| `restoreExternalPortraitPanels` | 944 | const | 0 | KEEP (file ADAPT) | C |
| `ensureChoiceModal` | 954 | const | 0 | KEEP (file ADAPT) | C |
| `escapeCompareHtml` | 1007 | const | 0 | KEEP (file ADAPT) | C |
| `renderPortraitCompareResults` | 1012 | const | 0 | DELETE — With portrait_model_compare.py (debug double-generation subject). | C |
| `ensurePortraitCompareControl` | 1036 | const | 0 | DELETE — With portrait_model_compare.py. | C |
| `onclick` | 1057 | assign | 26 | KEEP (file ADAPT) | C |
| `onclick` | 1081 | assign | 26 | KEEP (file ADAPT) | C |
| `setPortraitChoiceMode` | 1132 | const | 0 | KEEP (file ADAPT) | C |
| `closeModal` | 1146 | const | 0 | KEEP (file ADAPT) | C |
| `actionButtons` | 1150 | const | 0 | KEEP (file ADAPT) | C |
| `wirePanelActions` | 1155 | const | 0 | KEEP (file ADAPT) | C |
| `onPicked` | 1160 | objmethod | 0 | KEEP (file ADAPT) | C |
| `onclick` | 1166 | assign | 26 | KEEP (file ADAPT) | C |
| `onclick` | 1172 | assign | 26 | KEEP (file ADAPT) | C |
| `generateFn` | 1181 | objmethod | 1 | KEEP (file ADAPT) | C |
| `onCommit` | 1185 | objmethod | 1 | KEEP (file ADAPT) | C |
| `loadSuggestion` | 1213 | const | 0 | KEEP (file ADAPT) | C |
| `onRetry` | 1223 | objmethod | 2 | KEEP (file ADAPT) | C |
| `onFilled` | 1244 | objmethod | 2 | KEEP (file ADAPT) | C |
| `revealAiPanelWithSuggestion` | 1250 | const | 0 | KEEP (file ADAPT) | C |
| `onclick` | 1278 | assign | 26 | KEEP (file ADAPT) | C |

### `js/scene-illustration.js` — 26 symbols, file verdict ADAPT, loaded: index.html:638 (defer)

File ADAPT (run 2 confirmed): slot/poll/lightbox KEEP; ablation/debug cluster ADAPT out of the player bundle.

Lens A: loaded file; symbols are live except named exceptions. Lens B: comments/docstrings checked; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `escapeHtml` | 11 | function | 5 | KEEP (file ADAPT) | C |
| `escapeAttr` | 21 | function | 0 | KEEP (file ADAPT) | C |
| `normalizeState` | 29 | function | 0 | KEEP (file ADAPT) | C |
| `isStalePending` | 49 | function | 0 | KEEP (file ADAPT) | C |
| `renderSceneIllustrationSlot` | 55 | function | 1 | KEEP (file ADAPT) | C |
| `updateSceneIllustrationSlot` | 111 | function | 1 | KEEP (file ADAPT) | C |
| `ensureStreamingSceneSlot` | 123 | function | 0 | KEEP (file ADAPT) | C |
| `resolveSceneHost` | 142 | function | 2 | KEEP (file ADAPT) | C |
| `defaultAuthHeaders` | 161 | function | 0 | KEEP (file ADAPT) | C |
| `pollSceneIllustration` | 175 | function | 0 | KEEP (file ADAPT) | C |
| `finish` | 202 | const | 23 | ADAPT — Ablation internal: moves with the ablation panel. | C |
| `tick` | 208 | const | 2 | ADAPT — Ablation internal: moves with the ablation panel. | C |
| `startPollForEntry` | 245 | function | 1 | KEEP (file ADAPT) | C |
| `pollPendingSceneSlots` | 262 | function | 1 | KEEP (file ADAPT) | C |
| `closeSceneLightbox` | 291 | function | 0 | KEEP (file ADAPT) | C |
| `openSceneLightbox` | 302 | function | 0 | KEEP (file ADAPT) | C |
| `sceneSlotHost` | 334 | function | 0 | KEEP (file ADAPT) | C |
| `retrySceneIllustration` | 343 | function | 0 | KEEP (file ADAPT) | C |
| `renderAblationControl` | 408 | function | 0 | ADAPT — Operator tooling: move behind a debug flag or out of the shipped bundle. | C |
| `renderAblationControlIfAllowed` | 421 | function | 4 | ADAPT — Operator tooling: move behind a debug flag or out of the shipped bundle. | C |
| `loadDebugToolEligibility` | 429 | function | 2 | ADAPT — Operator tooling: move behind a debug flag or out of the shipped bundle. | C |
| `safeImageUrl` | 458 | function | 0 | KEEP (file ADAPT) | C |
| `formatCostLatency` | 465 | function | 0 | KEEP (file ADAPT) | C |
| `renderAblationPanel` | 476 | function | 0 | ADAPT — Operator tooling: move behind a debug flag or out of the shipped bundle. | C |
| `runPromptAblation` | 516 | function | 0 | ADAPT — Operator tooling: move behind a debug flag or out of the shipped bundle. | C |
| `call` | 536 | const | 60 | ADAPT — Ablation internal: moves with the ablation panel. | C |

### `js/settings.js` — 67 symbols, file verdict ADAPT, loaded: DYNAMIC ONLY — app.js:2576–2583 createElement("script") src /frontend_v1/js/settings.js

File ADAPT (run 2 confirmed): one load/save path; OpenRouter link dedup into auth.js; scene-advanced visibility rendered from the server response. Load evidence is DYNAMIC ONLY via app.js (no static tag in index.html) — settings.js is also named in frontend_release.py LEGACY_REQUIRED_RUNTIME_ASSETS (line 78), so the file must stay in the served set even though it loads lazily.

Lens A: loaded file; symbols are live except named exceptions. Lens B: comments/docstrings checked; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `initializeSettingsControls` | 23 | assign | 3 W | KEEP (file ADAPT) | C |
| `logByokBindingSnapshot` | 38 | function | 0 | KEEP (file ADAPT) | C |
| `valueLen` | 65 | objmethod | 0 | KEEP (file ADAPT) | C |
| `setup_byok_event_listeners` | 72 | function | 0 | KEEP (file ADAPT) | C |
| `dumpByokBindings` | 247 | assign | 0 | KEEP (file ADAPT) | C |
| `setApiKeyFieldVisible` | 250 | function | 0 | KEEP (file ADAPT) | C |
| `setOpenRouterOAuthStatus` | 282 | function | 0 | KEEP (file ADAPT) | C |
| `currentSettingsUid` | 297 | function | 0 | KEEP (file ADAPT) | C |
| `clearPendingOpenRouterConnect` | 307 | function | 0 | KEEP (file ADAPT) | C |
| `hasPendingOpenRouterConnect` | 315 | function | 0 | KEEP (file ADAPT) | C |
| `consumePendingOpenRouterConnect` | 329 | function | 0 | KEEP (file ADAPT) | C |
| `setOpenRouterAccountLinkStatus` | 356 | function | 0 | KEEP (file ADAPT) | C |
| `revealOpenRouterAccountLinkIfAvailable` | 370 | function | 0 | KEEP (file ADAPT) | C |
| `startOpenRouterAccountLink` | 445 | function | 0 | KEEP (file ADAPT) | C |
| `cancelOpenRouterAccountLink` | 522 | function | 0 | KEEP (file ADAPT) | C |
| `applyOpenRouterLinkProvider` | 540 | function | 0 | KEEP (file ADAPT) | C |
| `refreshOpenRouterLinkedSettings` | 547 | function | 0 | KEEP (file ADAPT) | C |
| `persistOpenRouterLinkProviderChoice` | 568 | function | 0 | KEEP (file ADAPT) | C |
| `confirmOpenRouterAccountLink` | 583 | function | 0 | KEEP (file ADAPT) | C |
| `resumeOpenRouterAccountLink` | 664 | function | 0 | KEEP (file ADAPT) | C |
| `onChange` | 760 | objmethod | 0 | KEEP (file ADAPT) | C |
| `normalize` | 767 | objmethod | 1 | KEEP (file ADAPT) | C |
| `normalize` | 776 | objmethod | 1 | KEEP (file ADAPT) | C |
| `normalize` | 805 | objmethod | 1 | KEEP (file ADAPT) | C |
| `onChange` | 821 | objmethod | 0 | KEEP (file ADAPT) | C |
| `parse` | 829 | objmethod | 28 | KEEP (file ADAPT) | C |
| `normalize` | 834 | objmethod | 1 | KEEP (file ADAPT) | C |
| `parse` | 846 | objmethod | 28 | KEEP (file ADAPT) | C |
| `normalize` | 850 | objmethod | 1 | KEEP (file ADAPT) | C |
| `normalize` | 861 | objmethod | 1 | KEEP (file ADAPT) | C |
| `sceneModeIsOn` | 887 | function | 0 | KEEP (file ADAPT) | C |
| `syncSceneIllustrationToggle` | 891 | function | 0 | KEEP (file ADAPT) | C |
| `refreshSceneAdvancedVisibility` | 896 | function | 0 | KEEP (file ADAPT) | C |
| `probe` | 908 | const | 16 | KEEP (file ADAPT) | C |
| `waitForSceneEligibilitySettled` | 934 | function | 0 | KEEP (file ADAPT) | C |
| `handleSceneSettingsAuthChange` | 942 | function | 0 | KEEP (file ADAPT) | C |
| `bindSceneIllustrationToggle` | 986 | function | 0 | KEEP (file ADAPT) | C |
| `updateSceneEveryNVisibility` | 1023 | function | 0 | KEEP (file ADAPT) | C |
| `getRadioGroup` | 1034 | function | 0 | KEEP (file ADAPT) | C |
| `getSelectedRadioValue` | 1038 | function | 0 | KEEP (file ADAPT) | C |
| `setRadioGroupValue` | 1043 | function | 0 | KEEP (file ADAPT) | C |
| `setSelectValue` | 1050 | function | 0 | KEEP (file ADAPT) | C |
| `getElementsForEntry` | 1064 | function | 0 | KEEP (file ADAPT) | C |
| `setEntryDisabled` | 1072 | function | 0 | KEEP (file ADAPT) | C |
| `readEntryValue` | 1079 | function | 0 | KEEP (file ADAPT) | C |
| `readRawEntryValue` | 1084 | function | 0 | KEEP (file ADAPT) | C |
| `applyEntryValue` | 1101 | function | 0 | KEEP (file ADAPT) | C |
| `attachSettingsListeners` | 1137 | function | 0 | KEEP (file ADAPT) | C |
| `loadSettings` | 1190 | function | 1 | KEEP (file ADAPT) | C |
| `isCurrentLoad` | 1193 | const | 0 | KEEP (file ADAPT) | C |
| `handleResetOnboarding` | 1468 | function | 0 | KEEP (file ADAPT) | C |
| `show_confirmation_modal` | 1509 | function | 0 | KEEP (file ADAPT) | C |
| `cleanup` | 1539 | const | 35 | KEEP (file ADAPT) | C |
| `onConfirm` | 1545 | const | 0 | KEEP (file ADAPT) | C |
| `onCancel` | 1551 | const | 3 | KEEP (file ADAPT) | C |
| `readResponsePayload` | 1564 | function | 0 | KEEP (file ADAPT) | C |
| `extractErrorMessage` | 1581 | function | 0 | KEEP (file ADAPT) | C |
| `saveSettings` | 1627 | function | 1 | KEEP (file ADAPT) | C |
| `isBenignSettingsFetchAbort` | 1939 | function | 0 | KEEP (file ADAPT) | C |
| `toggleProviderSections` | 1947 | function | 1 | KEEP (file ADAPT) | C |
| `getAuthHeaders` | 1969 | function | 28 | KEEP (file ADAPT) | C |
| `showSaveMessage` | 2005 | function | 0 | KEEP (file ADAPT) | C |
| `showErrorMessage` | 2046 | function | 0 | KEEP (file ADAPT) | C |
| `showLoadingIndicator` | 2081 | function | 0 | KEEP (file ADAPT) | C |
| `reveal_stored_api_key` | 2095 | function | 0 | KEEP (file ADAPT) | C |
| `toggle_api_key_visibility` | 2115 | function | 0 | KEEP (file ADAPT) | C |
| `clear_api_key` | 2162 | function | 0 | KEEP (file ADAPT) | C |

### `js/streaming.js` — 47 symbols, file verdict ADAPT, loaded: index.html:639 (defer)

File ADAPT (run 2 confirmed): streaming transport/extraction KEEP; terminal inference DELETE; telemetry via async path.

Lens A: loaded file; symbols are live except named exceptions. Lens B: comments/docstrings checked; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `onChunk` | 9 | assign | 3 | KEEP (file ADAPT) | C |
| `onComplete` | 12 | assign | 10 | KEEP (file ADAPT) | C |
| `StreamingClient` | 18 | class | 4 W | KEEP (file ADAPT) | C |
| `constructor` | 23 | method | 13 | KEEP (file ADAPT) | C |
| `_processSSEMessage` | 322 | method | 0 | KEEP (file ADAPT) | C |
| `_getClientTelemetryMetrics` | 354 | method | 0 | KEEP (file ADAPT) | C |
| `getBrowserTraceOffsets` | 377 | method | 4 | KEEP (file ADAPT) | C |
| `offset` | 380 | const | 44 | KEEP (file ADAPT) | C |
| `markRenderComplete` | 407 | method | 4 | KEEP (file ADAPT) | C |
| `markComposerReleased` | 419 | method | 4 | KEEP (file ADAPT) | C |
| `noteVisibleRender` | 437 | method | 4 | KEEP (file ADAPT) | C |
| `getTerminalOutcome` | 449 | method | 2 | ADAPT — Delete terminal-state inference; render only the server-declared outcome. | C |
| `getTerminalErrorType` | 454 | method | 2 | ADAPT — Delete terminal-state inference; render only the server-declared outcome. | C |
| `_handleEvent` | 463 | method | 0 | KEEP (file ADAPT) | C |
| `_reportClientOutcome` | 678 | method | 0 | KEEP (file ADAPT) | C |
| `_getStreamingDisplayText` | 727 | method | 0 | KEEP (file ADAPT) | C |
| `_getStreamingDisplay` | 731 | method | 0 | KEEP (file ADAPT) | C |
| `pendingJsonOpening` | 747 | const | 0 | KEEP (file ADAPT) | C |
| `_getStructuredEnvelopePlaceholder` | 789 | method | 0 | KEEP (file ADAPT) | C |
| `_looksLikeIncompleteStructuredEnvelope` | 827 | method | 0 | KEEP (file ADAPT) | C |
| `_extractNarrativeFromParsedEnvelope` | 865 | method | 0 | KEEP (file ADAPT) | C |
| `_extractNarrativeFromRawEnvelope` | 907 | method | 0 | KEEP (file ADAPT) | C |
| `extractAt` | 914 | const | 0 | KEEP (file ADAPT) | C |
| `_readJsonStringPrefix` | 953 | method | 0 | KEEP (file ADAPT) | C |
| `_extractPlanningThinking` | 993 | method | 0 | KEEP (file ADAPT) | C |
| `_isEscapedQuote` | 1032 | method | 0 | KEEP (file ADAPT) | C |
| `_getPlanningBlockDepthAtPosition` | 1048 | method | 0 | KEEP (file ADAPT) | C |
| `cancel` | 1125 | method | 48 | KEEP (file ADAPT) | C |
| `isActive` | 1137 | method | 0 | KEEP (file ADAPT) | C |
| `renderPlanningThinkingBlock` | 1148 | function | 2 W | KEEP (file ADAPT) | C |
| `createStreamingHandler` | 1193 | function | 0 | KEEP (file ADAPT) | C |
| `_renderFinalEntryInPlace` | 1215 | const | 0 | KEEP (file ADAPT) | C |
| `onStreamStart` | 1253 | assign | 0 | KEEP (file ADAPT) | C |
| `onPlanningThinking` | 1273 | assign | 1 | KEEP (file ADAPT) | C |
| `onChunk` | 1279 | assign | 3 | KEEP (file ADAPT) | C |
| `onToolResult` | 1289 | assign | 1 | KEEP (file ADAPT) | C |
| `onToolStart` | 1341 | assign | 0 | KEEP (file ADAPT) | C |
| `onStateUpdate` | 1354 | assign | 0 | KEEP (file ADAPT) | C |
| `onWarning` | 1364 | assign | 1 | KEEP (file ADAPT) | C |
| `onComplete` | 1374 | assign | 10 | KEEP (file ADAPT) | C |
| `onError` | 1430 | assign | 9 | KEEP (file ADAPT) | C |
| `onStreamEnd` | 1442 | assign | 3 | KEEP (file ADAPT) | C |
| `sendMessage` | 1458 | objmethod | 2 | KEEP (file ADAPT) | C |
| `cancel` | 1462 | objmethod | 48 | KEEP (file ADAPT) | C |
| `isActive` | 1463 | objmethod | 0 | KEEP (file ADAPT) | C |
| `beaconClientStreamLatency` | 1472 | function | 4 | KEEP (file ADAPT) | C |
| `send` | 1478 | const | 19 W | KEEP (file ADAPT) | C |

### `js/test_planning_block_parsing.js` — 16 symbols, file verdict DELETE, loaded: NEVER LOADED — no tag, no dynamic load

File DELETE (run 2 confirmed): self-contained test harness, never loaded; live planning parsing ships in streaming.js/app.js.

Lens A: NEVER LOADED — no index.html tag, no dynamic loader, no shipped caller; all symbols unreachable in the shipped page. Lens B: comments describe behaviour that never runs in the product; deleting the file deletes its docs with it.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `decodeHtmlEntities` | 9 | function | 5 | DELETE — unloaded file, unreachable symbol. | C |
| `sanitizeHtml` | 19 | function | 74 | DELETE — unloaded file, unreachable symbol. | C |
| `escapeHtmlAttribute` | 31 | function | 14 | DELETE — unloaded file, unreachable symbol. | C |
| `sanitizeIdentifier` | 41 | const | 2 | DELETE — unloaded file, unreachable symbol. | C |
| `parsePlanningBlocksJson` | 48 | function | 2 | DELETE — unloaded file, unreachable symbol. | C |
| `id` | 75 | objmethod | 388 | DELETE — unloaded file, unreachable symbol. | C |
| `PlanningBlockTestSuite` | 214 | class | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `constructor` | 215 | method | 13 | DELETE — unloaded file, unreachable symbol. | C |
| `test` | 221 | method | 76 W | DELETE — unloaded file, unreachable symbol. | C |
| `assert` | 225 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `assertContains` | 231 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `assertNotContains` | 239 | method | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `run` | 247 | method | 89 | DELETE — unloaded file, unreachable symbol. | C |
| `queryHTML` | 604 | function | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `querySelector` | 622 | objmethod | 270 | DELETE — unloaded file, unreachable symbol. | C |
| `querySelectorAll` | 633 | objmethod | 108 | DELETE — unloaded file, unreachable symbol. | C |

### `js/theme-bootstrap.js` — 3 symbols, file verdict KEEP, loaded: index.html:22

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `toBoolean` | 5 | function | 0 | KEEP | C |
| `isFantasyThemeEnabled` | 19 | function | 2 | KEEP | C |
| `activateAsyncCSS` | 47 | function | 0 | KEEP | C |

### `js/theme-manager.js` — 12 symbols, file verdict KEEP, loaded: index.html:630 (defer)

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `ThemeManager` | 1 | class | 0 | KEEP | C |
| `getDefaultTheme` | 2 | method | 0 | KEEP | C |
| `isFantasyThemeEnabled` | 9 | method | 2 | KEEP | C |
| `isAllowedTheme` | 13 | method | 0 | KEEP | C |
| `constructor` | 20 | method | 13 | KEEP | C |
| `init` | 31 | method | 29 W | KEEP | C |
| `loadSavedTheme` | 37 | method | 0 | KEEP | C |
| `setTheme` | 71 | method | 0 | KEEP | C |
| `setupEventListeners` | 90 | method | 9 | KEEP | C |
| `_themeMenuClickHandler` | 98 | assign | 0 | KEEP | C |
| `updateThemeIcon` | 109 | method | 0 | KEEP | C |
| `destroy` | 120 | method | 15 | KEEP | C |

### `js/tooltip-guide.js` — 29 symbols, file verdict ADAPT, loaded: index.html:715 (defer; stripped by main.py tooltip kill switch when disabled)

File ADAPT (run 2 confirmed): one hydration path (server authority); events via diagnostics.js.

Lens A: loaded file; symbols are live except named exceptions. Lens B: comments/docstrings checked; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `escapeHtml` | 14 | function | 15 | KEEP (file ADAPT) | C |
| `getState` | 23 | function | 0 | KEEP (file ADAPT) | C |
| `currentAuthUserId` | 30 | function | 0 | KEEP (file ADAPT) | C |
| `beginTooltipHydration` | 38 | function | 0 | KEEP (file ADAPT) | C |
| `finishTooltipHydration` | 43 | function | 0 | KEEP (file ADAPT) | C |
| `tooltipInteractionReady` | 47 | function | 0 | KEEP (file ADAPT) | C |
| `mergeHydratedSettings` | 52 | function | 0 | KEEP (file ADAPT) | C |
| `recordEvent` | 81 | function | 0 | ADAPT — Route guide events through diagnostics.js instead of this file's own pipeline. | C |
| `flushPending` | 99 | function | 0 | ADAPT — Route guide events through diagnostics.js instead of this file's own pipeline. | C |
| `hydrateFromServer` | 119 | function | 0 | KEEP (file ADAPT) | C |
| `markGuideCompleted` | 146 | method | 0 | KEEP (file ADAPT) | C |
| `attachAll` | 152 | method | 0 | KEEP (file ADAPT) | C |
| `_bindSingle` | 186 | method | 0 | KEEP (file ADAPT) | C |
| `show` | 193 | const | 59 W | KEEP (file ADAPT) | C |
| `showCount` | 228 | objmethod | 1 | KEEP (file ADAPT) | C |
| `show` | 247 | method | 59 W | KEEP (file ADAPT) | C |
| `_bindGuides` | 256 | method | 0 | KEEP (file ADAPT) | C |
| `_observeGuideEntry` | 271 | method | 0 | KEEP (file ADAPT) | C |
| `startGuide` | 290 | method | 0 | KEEP (file ADAPT) | C |
| `_renderGuideCard` | 314 | method | 0 | KEEP (file ADAPT) | C |
| `close` | 366 | const | 45 | KEEP (file ADAPT) | C |
| `onKey` | 373 | function | 0 | KEEP (file ADAPT) | C |
| `_positionCard` | 422 | method | 0 | KEEP (file ADAPT) | C |
| `reset` | 446 | method | 13 | KEEP (file ADAPT) | C |
| `bootstrapTooltipGuide` | 460 | function | 0 | KEEP (file ADAPT) | C |
| `resetGuideBindings` | 465 | function | 0 | KEEP (file ADAPT) | C |
| `safeAttach` | 476 | function | 0 | KEEP (file ADAPT) | C |
| `setImmediate` | 531 | method | 0 | KEEP (file ADAPT) | C |
| `setTimeout` | 537 | method | 82 | KEEP (file ADAPT) | C |

### `js/ui-utils.js` — 3 symbols, file verdict KEEP, loaded: index.html:632 (defer)

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `applyWikiLinks` | 30 | function | 3 | KEEP | C |
| `applySocialLinks` | 52 | function | 1 | KEEP | C |
| `setupCollapsibleDescription` | 72 | function | 2 | KEEP | C |

### `js/visual-validator.js` — 11 symbols, file verdict DELETE, loaded: NEVER LOADED — no tag, no dynamic load

File DELETE (run 2 confirmed): layout QA tooling, never loaded, no shipped caller.

Lens A: NEVER LOADED — no index.html tag, no dynamic loader, no shipped caller; all symbols unreachable in the shipped page. Lens B: comments describe behaviour that never runs in the product; deleting the file deletes its docs with it.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `overlappingElements` | 26 | objmethod | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `textReadability` | 91 | objmethod | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `checkboxAlignment` | 160 | objmethod | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `modernModeDefault` | 214 | objmethod | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `spinnerCheck` | 240 | objmethod | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `highlightElement` | 282 | objmethod | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `getContrastRatio` | 293 | objmethod | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `getRGB` | 307 | objmethod | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `getLuminance` | 319 | objmethod | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `run` | 329 | objmethod | 87 | DELETE — unloaded file, unreachable symbol. | C |
| `captureState` | 388 | objmethod | 0 | DELETE — unloaded file, unreachable symbol. | C |

### `js/worldai-mcp-bridge.js` — 4 symbols, file verdict KEEP, loaded: index.html:714 (defer)

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `callTool` | 21 | function | 0 | KEEP | C |
| `mcp__worldai__record_tooltip_event` | 69 | assign | 3 W | KEEP | C |
| `mcp__worldai__get_user_settings` | 80 | assign | 2 W | KEEP | C |
| `mcp__worldai__reset_tooltip_state` | 86 | assign | 2 W | KEEP | C |

### `parallel_dual_pass.js` — 6 symbols, file verdict DELETE, loaded: NEVER LOADED — no tag, no dynamic load

File DELETE (run 2 confirmed): second turn-submission path, never loaded; shipped turns run through streaming.js.

Lens A: NEVER LOADED — no index.html tag, no dynamic loader, no shipped caller; all symbols unreachable in the shipped page. Lens B: comments describe behaviour that never runs in the product; deleting the file deletes its docs with it.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `handleInteractionParallel` | 14 | function | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `enhanceStoryInBackground` | 71 | function | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `replaceStoryEntry` | 138 | function | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `showEnhancementIndicator` | 164 | function | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `hideEnhancementIndicator` | 182 | function | 0 | DELETE — unloaded file, unreachable symbol. | C |
| `showEnhancementSuccess` | 192 | function | 0 | DELETE — unloaded file, unreachable symbol. | C |

### `quick_start_shared.js` — 8 symbols, file verdict KEEP, loaded: index.html:644 (defer)

Lens A: loaded file; symbols are handlers, window exports, or intra-file helpers of a live feature. Lens B: comments/docstrings checked against behaviour; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `bannerDismissedKey` | 39 | function | 0 | KEEP | C |
| `scrollToCharacterCreation` | 56 | function | 6 | KEEP | C |
| `resolveNewCampaignScrollTarget` | 101 | function | 4 | KEEP | C |
| `dismissFirstRunBanner` | 114 | function | 6 | KEEP | C |
| `isFirstRunBannerDismissed` | 148 | function | 3 | KEEP | C |
| `normalizeQuickStartPath` | 165 | function | 2 | KEEP | C |
| `buildDashboardSearch` | 186 | function | 8 | KEEP | C |
| `buildDashboardHref` | 202 | function | 6 | KEEP | C |

### `user_lifecycle.js` — 31 symbols, file verdict ADAPT, loaded: index.html:625 (defer)

File ADAPT (run 2 confirmed): visitor/session identity + auth linking KEEP; acquisition capture DELETE; events via diagnostics.js.

Lens A: loaded file; symbols are live except named exceptions. Lens B: comments/docstrings checked; no stale doc found in this file except where noted.

| Symbol | Line | Kind | Prod refs (W = window export) | Verdict | Run-2 |
|---|---|---|---|---|---|
| `now` | 72 | function | 122 | KEEP (file ADAPT) | C |
| `randomUuid` | 76 | function | 0 | KEEP (file ADAPT) | C |
| `readStorage` | 86 | function | 0 | KEEP (file ADAPT) | C |
| `writeStorage` | 96 | function | 0 | KEEP (file ADAPT) | C |
| `parseStoredJson` | 107 | function | 0 | KEEP (file ADAPT) | C |
| `validUuid` | 116 | function | 0 | KEEP (file ADAPT) | C |
| `createVisitor` | 120 | function | 0 | KEEP (file ADAPT) | C |
| `loadVisitor` | 128 | function | 0 | KEEP (file ADAPT) | C |
| `makeSession` | 139 | function | 0 | KEEP (file ADAPT) | C |
| `loadSession` | 151 | function | 0 | KEEP (file ADAPT) | C |
| `snapshotFrom` | 184 | function | 0 | KEEP (file ADAPT) | C |
| `snapshotHeaders` | 194 | function | 0 | KEEP (file ADAPT) | C |
| `touchSession` | 208 | function | 0 | KEEP (file ADAPT) | C |
| `getIdentity` | 244 | function | 0 | KEEP (file ADAPT) | C |
| `sanitizeScalar` | 249 | function | 0 | KEEP (file ADAPT) | C |
| `getAcquisition` | 255 | function | 0 | DELETE — Acquisition-source collection with no product decision justifying it. | C |
| `eventFields` | 274 | function | 1 | KEEP (file ADAPT) | C |
| `currentAuthUser` | 297 | function | 0 | KEEP (file ADAPT) | C |
| `bodyString` | 311 | function | 0 | KEEP (file ADAPT) | C |
| `boundedJoinId` | 321 | function | 0 | KEEP (file ADAPT) | C |
| `sendWithIdentity` | 325 | function | 0 | ADAPT — Route through the shared diagnostics pipeline. | C |
| `record` | 383 | function | 3 | ADAPT — Route through the shared diagnostics pipeline. | C |
| `getRequestHeaders` | 387 | function | 3 | KEEP (file ADAPT) | C |
| `rotateIdentity` | 394 | function | 0 | KEEP (file ADAPT) | C |
| `linkAuthenticatedSession` | 428 | function | 0 | KEEP (file ADAPT) | C |
| `handleAuthState` | 460 | function | 1 | KEEP (file ADAPT) | C |
| `logout` | 487 | function | 1 | KEEP (file ADAPT) | C |
| `acquisitionFromLocation` | 496 | function | 0 | DELETE — Acquisition-source collection with no product decision justifying it. | C |
| `screenIdForView` | 507 | function | 0 | KEEP (file ADAPT) | C |
| `recordScreenViewed` | 518 | function | 1 | ADAPT — Route through the shared diagnostics pipeline. | C |
| `recordOnboardingStep` | 532 | function | 1 | ADAPT — Route through the shared diagnostics pipeline. | C |

JS symbol total (this pass): 1064.

---

## Per-file tables — CSS (one row per rule block)

Method: one row per `{` block; selector text is the text since the previous `}` (or file start), whitespace-collapsed, truncated at 100 chars. `@media`/`@keyframes` containers are rows of their own, and their inner rules are rows too, so row count equals brace count. All rules are pure presentation (layout/colour/typography/animation); no rule computes, filters, or rewrites a campaign value. Verdict KEEP for all shipped sheets; DELETE for parallel_dual_pass.css (styles an indicator no shipped page renders, companion to the unloaded JS).

### `campaign-click-fix.css` — 9 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* Campaign Click Fix - TASK-005a */ /* Make campaign items clearly clickable */ .campaign-title-lin` | 4 | KEEP |
| `.campaign-title-link:hover` | 12 | KEEP |
| `/* Ensure the entire campaign item is clickable */ .list-group-item[data-campaign-id]` | 18 | KEEP |
| `.list-group-item[data-campaign-id]:hover` | 23 | KEEP |
| `/* Prevent button clicks from triggering campaign navigation */ .list-group-item[data-campaign-id] .` | 29 | KEEP |
| `/* Visual feedback on click */ .list-group-item[data-campaign-id]:active` | 35 | KEEP |
| `/* Ensure proper click area */ .campaign-title-link` | 41 | KEEP |
| `/* Fix potential overlapping issues */ .list-group-item[data-campaign-id] > div` | 47 | KEEP |
| `.list-group-item[data-campaign-id] .campaign-title-link, .list-group-item[data-campaign-id] .inline-` | 53 | KEEP |

### `css/avatar.css` — 156 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* ============================================================================= Avatar Components —` | 7 | KEEP |
| `.avatar-source-segment, .portrait-source-segment` | 13 | KEEP |
| `.avatar-source-segment-btn` | 26 | KEEP |
| `.avatar-source-segment-btn.is-active` | 42 | KEEP |
| `.avatar-source-segment-icon` | 52 | KEEP |
| `.avatar-source-segment-btn:focus-visible, .portrait-source-segment .avatar-source-segment-btn:focus-` | 58 | KEEP |
| `.avatar-source-segment.mode-ai .avatar-source-segment-btn[data-avatar-mode="ai"].is-active:focus-vis` | 64 | KEEP |
| `.avatar-ai-step` | 69 | KEEP |
| `hide wizard duplicates. */ body.portrait-modal-active #avatar-ai-panel, body.portrait-modal-active .` | 77 | KEEP |
| `.portrait-ai-layout` | 81 | KEEP |
| `.portrait-ai-preview-ring` | 88 | KEEP |
| `.portrait-ai-preview-placeholder` | 101 | KEEP |
| `.portrait-ai-preview-icon` | 115 | KEEP |
| `.portrait-ai-preview-img` | 119 | KEEP |
| `.portrait-ai-preview-img.is-visible` | 132 | KEEP |
| `.portrait-ai-gen-overlay` | 136 | KEEP |
| `.portrait-ai-preview-ring.is-generating .portrait-ai-gen-overlay` | 153 | KEEP |
| `.portrait-ai-preview-ring.is-generating .portrait-ai-preview-img.is-visible` | 157 | KEEP |
| `.portrait-ai-label` | 161 | KEEP |
| `.portrait-ai-helper` | 168 | KEEP |
| `.portrait-ai-textarea-wrap` | 175 | KEEP |
| `.portrait-ai-textarea` | 180 | KEEP |
| `.portrait-ai-textarea:focus` | 194 | KEEP |
| `.portrait-ai-shimmer` | 200 | KEEP |
| `.portrait-ai-textarea-wrap.is-shimmer .portrait-ai-shimmer` | 217 | KEEP |
| `@keyframes portrait-ai-shimmer` | 222 | KEEP |
| `0%` | 223 | KEEP |
| `100%` | 226 | KEEP |
| `.portrait-ai-char-row` | 231 | KEEP |
| `.portrait-ai-char-count` | 237 | KEEP |
| `.portrait-ai-char-count.is-near-limit` | 242 | KEEP |
| `.portrait-ai-actions` | 246 | KEEP |
| `.portrait-ai-refresh-btn` | 253 | KEEP |
| `.portrait-ai-refresh-btn:hover:not(:disabled)` | 266 | KEEP |
| `.portrait-ai-generate-btn` | 270 | KEEP |
| `.portrait-ai-generate-btn:disabled, .portrait-ai-refresh-btn:disabled` | 284 | KEEP |
| `.portrait-ai-commit-actions` | 289 | KEEP |
| `.portrait-ai-commit-actions.d-none` | 296 | KEEP |
| `.portrait-ai-use-btn` | 300 | KEEP |
| `.portrait-ai-regenerate-btn, .portrait-ai-cancel-preview-btn` | 313 | KEEP |
| `.portrait-ai-preview-img.is-visible` | 324 | KEEP |
| `.portrait-ai-footnote, .portrait-ai-switch-upload` | 329 | KEEP |
| `.portrait-ai-switch-upload` | 335 | KEEP |
| `.portrait-ai-status` | 344 | KEEP |
| `.portrait-ai-status-card` | 350 | KEEP |
| `.portrait-ai-status-card.is-visible` | 357 | KEEP |
| `.portrait-ai-status-card.is-loading.is-visible` | 363 | KEEP |
| `.portrait-ai-status-card.is-error.is-visible` | 367 | KEEP |
| `.portrait-ai-retry-btn` | 372 | KEEP |
| `.portrait-fade-in` | 384 | KEEP |
| `@keyframes portrait-fade-in` | 388 | KEEP |
| `from` | 389 | KEEP |
| `to` | 393 | KEEP |
| `.portrait-ai-status-row` | 399 | KEEP |
| `.portrait-ai-spinner` | 406 | KEEP |
| `.portrait-ai-spinner.is-active` | 416 | KEEP |
| `@keyframes portrait-ai-spin` | 421 | KEEP |
| `to` | 422 | KEEP |
| `.portrait-ai-status.is-loading .portrait-ai-status-text` | 427 | KEEP |
| `.portrait-ai-status.is-error` | 431 | KEEP |
| `.portrait-ai-status.is-error .portrait-ai-status-text` | 435 | KEEP |
| `.portrait-source-modal` | 439 | KEEP |
| `.portrait-source-modal.is-open` | 450 | KEEP |
| `.portrait-source-card` | 454 | KEEP |
| `.portrait-source-close` | 465 | KEEP |
| `.portrait-source-lead` | 477 | KEEP |
| `.portrait-source-actions` | 482 | KEEP |
| `.portrait-ai-panel` | 487 | KEEP |
| `.avatar-card-btn--ai` | 492 | KEEP |
| `.avatar-size-hint` | 497 | KEEP |
| `/* In-game avatar crop overlay (shown when changing photo) */ .avatar-crop-overlay` | 504 | KEEP |
| `.avatar-crop-zone` | 520 | KEEP |
| `.avatar-crop-actions` | 535 | KEEP |
| `.avatar-upload-zone` | 540 | KEEP |
| `.avatar-upload-zone:hover` | 559 | KEEP |
| `.avatar-upload-zone.drag-over` | 565 | KEEP |
| `.avatar-upload-zone.has-preview` | 572 | KEEP |
| `.avatar-upload-icon` | 577 | KEEP |
| `.avatar-upload-text` | 583 | KEEP |
| `.avatar-upload-zone.has-preview .avatar-upload-icon, .avatar-upload-zone.has-preview .avatar-upload-` | 589 | KEEP |
| `/* Hidden file input */ .avatar-file-input` | 594 | KEEP |
| `/* Preview inside upload zone */ .avatar-upload-preview` | 599 | KEEP |
| `.avatar-upload-zone.has-preview .avatar-upload-preview` | 607 | KEEP |
| `/* Change photo chip (wizard upload crop — keeps face visible) */ .avatar-change-btn` | 612 | KEEP |
| `.avatar-upload-zone.has-preview .avatar-change-btn` | 633 | KEEP |
| `.avatar-change-btn:hover, .avatar-change-btn:focus-visible` | 638 | KEEP |
| `/* Remove button overlay */ .avatar-remove-btn` | 646 | KEEP |
| `.avatar-upload-zone.has-preview .avatar-remove-btn` | 665 | KEEP |
| `.avatar-remove-btn:hover` | 669 | KEEP |
| `/* Upload constraints text */ .avatar-constraints` | 675 | KEEP |
| `/* Skip hint */ .avatar-skip-hint` | 682 | KEEP |
| `/* ---------- In-Game Avatar Thumbnail ---------- */ .player-avatar-thumb` | 690 | KEEP |
| `.player-avatar-thumb:hover` | 701 | KEEP |
| `/* Default placeholder when no avatar */ .player-avatar-placeholder` | 708 | KEEP |
| `/* Player message row with avatar */ .player-message-row` | 722 | KEEP |
| `/* ---------- Expanded Avatar Card (Overlay) ---------- */ .avatar-overlay` | 731 | KEEP |
| `.avatar-overlay.visible` | 746 | KEEP |
| `@keyframes avatarFadeIn` | 750 | KEEP |
| `from` | 751 | KEEP |
| `to` | 755 | KEEP |
| `.avatar-card` | 760 | KEEP |
| `.avatar-card-close` | 772 | KEEP |
| `.avatar-card-close:hover` | 790 | KEEP |
| `.avatar-card-image` | 796 | KEEP |
| `.avatar-card-name` | 806 | KEEP |
| `.avatar-card-class` | 813 | KEEP |
| `.avatar-card-stats` | 819 | KEEP |
| `.avatar-stat` | 826 | KEEP |
| `.avatar-stat-label` | 835 | KEEP |
| `/* ---------- Header HUD avatar ---------- */ .header-avatar-slot` | 842 | KEEP |
| `.game-avatar-float` | 852 | KEEP |
| `.game-avatar-float img` | 862 | KEEP |
| `.game-avatar-float:hover img` | 876 | KEEP |
| `/* --- Avatar card action buttons (Change Photo / Remove) --- */ .avatar-card-actions` | 883 | KEEP |
| `.avatar-card-btn` | 890 | KEEP |
| `.avatar-card-btn:hover` | 901 | KEEP |
| `.avatar-card-btn--remove` | 906 | KEEP |
| `.avatar-card-btn--remove:hover` | 912 | KEEP |
| `/* Empty-state "Add Avatar" placeholder circle — mirrors the populated * .game-avatar-float img aest` | 923 | KEEP |
| `.game-avatar-add-btn:hover` | 951 | KEEP |
| `.game-avatar-add-btn:active` | 961 | KEEP |
| `.game-avatar-add-btn:focus` | 966 | KEEP |
| `.game-avatar-add-btn:focus-visible` | 970 | KEEP |
| `.game-avatar-add-btn[disabled]` | 975 | KEEP |
| `.game-avatar-add-btn .add-btn-icon` | 981 | KEEP |
| `.game-avatar-add-btn .sr-only` | 986 | KEEP |
| `/* Mobile header keeps the same scaled avatar target as desktop. */ @media (max-width: 576px)` | 999 | KEEP |
| `.game-avatar-float img` | 1000 | KEEP |
| `.game-avatar-add-btn` | 1008 | KEEP |
| `.game-avatar-add-btn .add-btn-icon svg` | 1015 | KEEP |
| `.avatar-card` | 1020 | KEEP |
| `.avatar-card-image` | 1025 | KEEP |
| `.avatar-card-name` | 1030 | KEEP |
| `.avatar-stat` | 1034 | KEEP |
| `/* -- Toast notification -- */ .avatar-toast` | 1041 | KEEP |
| `.avatar-toast.success` | 1054 | KEEP |
| `.avatar-toast.error` | 1058 | KEEP |
| `@keyframes avatarToastIn` | 1062 | KEEP |
| `from` | 1063 | KEEP |
| `to` | 1068 | KEEP |
| `@keyframes avatarToastOut` | 1074 | KEEP |
| `from` | 1075 | KEEP |
| `to` | 1079 | KEEP |
| `/* ---------- Mobile Responsive ---------- */ @media (max-width: 576px)` | 1085 | KEEP |
| `.portrait-source-card` | 1086 | KEEP |
| `.portrait-ai-layout` | 1091 | KEEP |
| `/* Matched min() width/height keeps the mobile preview ring circular. */ .portrait-ai-preview-ring` | 1096 | KEEP |
| `.avatar-source-segment, .portrait-source-segment` | 1103 | KEEP |
| `.avatar-source-segment-btn` | 1107 | KEEP |
| `.avatar-upload-zone` | 1112 | KEEP |
| `.avatar-card` | 1119 | KEEP |
| `.avatar-card-image` | 1123 | KEEP |
| `.avatar-crop-zone` | 1128 | KEEP |
| `/* Spinner for the Add Avatar upload-in-flight state */ @keyframes avatar-add-spin` | 1135 | KEEP |
| `from` | 1136 | KEEP |
| `to` | 1137 | KEEP |

### `css/inline-editor.css` — 35 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* Inline Editor Styles */ .inline-editable` | 3 | KEEP |
| `.inline-editable:hover, .inline-editable-hover` | 14 | KEEP |
| `.inline-editable::after` | 20 | KEEP |
| `.inline-editable:hover::after, .inline-editable-hover::after` | 29 | KEEP |
| `/* Edit Container */ .inline-edit-container` | 34 | KEEP |
| `.inline-edit-input` | 44 | KEEP |
| `.inline-edit-input:focus` | 61 | KEEP |
| `.inline-edit-input.is-invalid` | 67 | KEEP |
| `.inline-edit-input.is-invalid:focus` | 71 | KEEP |
| `/* Button Container */ .inline-edit-buttons` | 77 | KEEP |
| `.inline-edit-save, .inline-edit-cancel` | 84 | KEEP |
| `.inline-edit-save:disabled` | 97 | KEEP |
| `/* Error Display */ .inline-edit-error` | 103 | KEEP |
| `@keyframes fadeIn` | 115 | KEEP |
| `from` | 116 | KEEP |
| `to` | 120 | KEEP |
| `/* Campaign-specific styles */ .campaign-title-editable` | 127 | KEEP |
| `.campaign-title-editable .inline-edit-input` | 134 | KEEP |
| `/* Game view title editing */ #game-title.inline-editable` | 141 | KEEP |
| `#game-title .inline-edit-input` | 148 | KEEP |
| `/* Dashboard campaign list editing */ .campaign-title-link.inline-editable` | 155 | KEEP |
| `.campaign-title-link .inline-edit-input` | 162 | KEEP |
| `/* Fantasy theme: gold focus ring for inline edit */ [data-theme='fantasy'] .inline-edit-input:focus` | 169 | KEEP |
| `/* Ensure invalid-state focus ring always wins in fantasy theme */ [data-theme='fantasy'] .inline-ed` | 175 | KEEP |
| `/* Responsive adjustments */ @media (max-width: 768px)` | 182 | KEEP |
| `.inline-edit-container` | 183 | KEEP |
| `.inline-edit-input` | 188 | KEEP |
| `.inline-edit-buttons` | 194 | KEEP |
| `/* Override the higher-specificity scoped min-widths (250/300/350px) so the input fills its containe` | 200 | KEEP |
| `rule above loses the cascade battle to the .campaign-title-link / .campaign-title-editable / #game-t` | 212 | KEEP |
| `/* Animation for smooth transitions */ .inline-edit-container` | 219 | KEEP |
| `@keyframes slideIn` | 223 | KEEP |
| `from` | 224 | KEEP |
| `to` | 228 | KEEP |
| `/* Loading state for save button */ .inline-edit-save .spinner-border-sm` | 235 | KEEP |

### `css/pagination-styles.css` — 25 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* Story Pagination Styles */ #load-more-container` | 3 | KEEP |
| `#load-more-btn` | 7 | KEEP |
| `#load-more-btn:hover` | 13 | KEEP |
| `#load-more-btn:active` | 18 | KEEP |
| `#load-more-spinner` | 22 | KEEP |
| `#story-pagination-info` | 28 | KEEP |
| `#story-content` | 34 | KEEP |
| `/* Smooth scroll indicator */ #story-content::-webkit-scrollbar` | 41 | KEEP |
| `#story-content::-webkit-scrollbar-track` | 45 | KEEP |
| `#story-content::-webkit-scrollbar-thumb` | 50 | KEEP |
| `#story-content::-webkit-scrollbar-thumb:hover` | 56 | KEEP |
| `/* Loading animation for story entries */ .story-entry-loading` | 61 | KEEP |
| `@keyframes fadeInUp` | 67 | KEEP |
| `to` | 68 | KEEP |
| `/* Pagination info animation */ .pagination-updating` | 75 | KEEP |
| `@keyframes pulse` | 79 | KEEP |
| `0%, 100%` | 82 | KEEP |
| `50%` | 86 | KEEP |
| `/* Load more button states */ .load-more-loading` | 92 | KEEP |
| `/* Error message styling */ .pagination-error` | 98 | KEEP |
| `@keyframes slideDown` | 108 | KEEP |
| `from` | 109 | KEEP |
| `to` | 114 | KEEP |
| `/* Responsive adjustments */ @media (max-width: 768px)` | 121 | KEEP |
| `#load-more-btn` | 122 | KEEP |

### `css/tooltip-guide.css` — 14 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* Legacy guide presentation shares the always-loaded inline-coach palette. */ .wa-ttg-single .toolt` | 3 | KEEP |
| `.wa-ttg-single .wa-ttg-title` | 11 | KEEP |
| `.wa-ttg-single .wa-ttg-body` | 17 | KEEP |
| `.wa-ttg-card` | 22 | KEEP |
| `.wa-ttg-card #wa-ttg-title` | 35 | KEEP |
| `.wa-ttg-card p` | 42 | KEEP |
| `.wa-ttg-card .wa-ttg-close` | 47 | KEEP |
| `.wa-ttg-card .wa-ttg-footer` | 59 | KEEP |
| `.wa-ttg-card .wa-ttg-counter` | 65 | KEEP |
| `.wa-ttg-card .wa-ttg-prev, .wa-ttg-card .wa-ttg-next` | 71 | KEEP |
| `.wa-ttg-card .wa-ttg-prev[disabled]` | 81 | KEEP |
| `.wa-ttg-card .wa-ttg-skip` | 82 | KEEP |
| `.wa-ttg-card button:focus-visible` | 92 | KEEP |
| `.wa-ttg-card .wa-ttg-close:focus-visible` | 96 | KEEP |

### `loading-messages.css` — 22 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* Loading Messages - TASK-005b */ /* Enhanced loading overlay with messages */ #loading-overlay` | 4 | KEEP |
| `.loading-content` | 8 | KEEP |
| `.loading-message` | 15 | KEEP |
| `.loading-message.active` | 26 | KEEP |
| `/* Contextual loading for interactions: one line inside the action bar, between the mode pills and S` | 33 | KEEP |
| `.pending-status` | 43 | KEEP |
| `.pending-status:empty` | 51 | KEEP |
| `/* The rotating pill gives way before the status line, which names the mode. */ #loading-spinner` | 55 | KEEP |
| `#loading-spinner .spinner-border` | 70 | KEEP |
| `#loading-spinner .loading-message` | 75 | KEEP |
| `/* Phone: the pills fill the bar, so a running turn's status takes their slot. */ @media (max-width:` | 88 | KEEP |
| `.pending-row` | 89 | KEEP |
| `.turn-running .pending-row` | 92 | KEEP |
| `.turn-running .toggle-group` | 98 | KEEP |
| `#interaction-form:not(.turn-running) .action-bar:has(.pending-status:not(:empty))` | 101 | KEEP |
| `#interaction-form:not(.turn-running) .pending-row:has(.pending-status:not(:empty))` | 104 | KEEP |
| `#interaction-form:not(.turn-running) .pending-status` | 110 | KEEP |
| `/* Animation for message rotation */ @keyframes fadeInOut` | 119 | KEEP |
| `0%, 100%` | 122 | KEEP |
| `20%, 80%` | 127 | KEEP |
| `/* Responsive adjustments */ @media (max-width: 576px)` | 133 | KEEP |
| `.loading-message` | 134 | KEEP |

### `parallel_dual_pass.css` — 10 rule blocks, file verdict DELETE

| Selector | Line | Verdict |
|---|---|---|
| `/** * Parallel Dual-Pass Styles - TASK-019 */ .enhancement-indicator` | 5 | DELETE |
| `.enhancement-indicator .spinner-border-sm` | 22 | DELETE |
| `.enhancement-success` | 28 | DELETE |
| `@keyframes slideIn` | 43 | DELETE |
| `from` | 44 | DELETE |
| `to` | 48 | DELETE |
| `/* Ensure story entries have relative positioning for absolute children */ .story-entry, [data-seque` | 56 | DELETE |
| `/* Smooth narrative transitions */ .narrative-content` | 61 | DELETE |
| `/* Mobile responsive */ @media (max-width: 768px)` | 66 | DELETE |
| `.enhancement-indicator, .enhancement-success` | 68 | DELETE |

### `style.css` — 505 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `:root` | 1 | KEEP |
| `/* Remove: body` | 16 | KEEP |
| `since it's now handled by themes */ #auth-container button` | 18 | KEEP |
| `#auth-container` | 22 | KEEP |
| `body.is-logged-out #auth-container` | 27 | KEEP |
| `body.is-logged-out #dashboard-view, body.is-logged-out #new-campaign-view, body.is-logged-out #game-` | 37 | KEEP |
| `body.is-logged-out #auth-view.active-view` | 41 | KEEP |
| `body.is-logged-out .container.mt-4` | 50 | KEEP |
| `/* Logged-out nav override: hide user dropdown/email and show sign-in indicator copy. */ body.is-log` | 59 | KEEP |
| `body.is-logged-out .navbar-brand::after` | 63 | KEEP |
| `/* Scrollable textarea styling */ .scrollable-textarea` | 71 | KEEP |
| `#story-content p` | 76 | KEEP |
| `/* Debug mode styles */ .debug-content` | 82 | KEEP |
| `/* Dice roll specific styling */ .debug-rolls` | 93 | KEEP |
| `/* Story entry container */ .story-entry` | 105 | KEEP |
| `/* The session snapshot preserves server text and wraps within the reading column. */ .session-heade` | 113 | KEEP |
| `.session-header::before` | 131 | KEEP |
| `/* Planning block specific styling */ .planning-block` | 144 | KEEP |
| `/* Structured fields styling */ .dice-rolls` | 154 | KEEP |
| `.dice-rolls ul` | 161 | KEEP |
| `/* Mechanics-hidden mode: Outcome card with a collapsed "Show calculation". */ .dice-rolls.dice-roll` | 167 | KEEP |
| `.dice-calculation` | 173 | KEEP |
| `.dice-calculation > summary` | 177 | KEEP |
| `.dice-calculation-hide, .dice-calculation[open] > summary .dice-calculation-show` | 184 | KEEP |
| `.dice-calculation[open] > summary .dice-calculation-hide` | 188 | KEEP |
| `.dice-calculation > summary:focus-visible` | 192 | KEEP |
| `.dice-outcome-card, .resource-event` | 198 | KEEP |
| `.dice-natural-badge` | 202 | KEEP |
| `.system-warnings` | 210 | KEEP |
| `.system-warnings ul` | 218 | KEEP |
| `.living-world-updates` | 223 | KEEP |
| `.living-world-section` | 231 | KEEP |
| `.living-world-list` | 235 | KEEP |
| `.living-world-scene` | 240 | KEEP |
| `.living-world-complication` | 246 | KEEP |
| `.debug-info` | 252 | KEEP |
| `.debug-info pre` | 260 | KEEP |
| `#debug-indicator` | 264 | KEEP |
| `#byok-indicator` | 275 | KEEP |
| `the light theme keeps them. */ [data-theme='fantasy'] #openrouter-account-link-status.text-success, ` | 290 | KEEP |
| `[data-theme='fantasy'] #openrouter-account-link-status.text-danger, [data-theme='fantasy'] #openrout` | 296 | KEEP |
| `/* OpenRouter integration card dark-surface scoped contrast rules */ #openrouter-card .btn-outline-s` | 301 | KEEP |
| `#openrouter-card .btn-outline-secondary:hover, #openrouter-card .btn-outline-secondary:focus, #openr` | 309 | KEEP |
| `#openrouter-card .btn-link` | 315 | KEEP |
| `#openrouter-card .btn:focus-visible` | 318 | KEEP |
| `#openrouter-card .text-success` | 321 | KEEP |
| `#openrouter-card .text-danger` | 324 | KEEP |
| `/* BYOK CTA banner — shown when no BYOK key is active */ #byok-cta` | 329 | KEEP |
| `.byok-cta-btn` | 336 | KEEP |
| `.byok-cta-btn:hover` | 348 | KEEP |
| `.byok-cta-dismiss` | 352 | KEEP |
| `.byok-cta-dismiss:hover` | 368 | KEEP |
| `.byok-cta-btn:focus-visible` | 373 | KEEP |
| `.byok-cta-dismiss:focus-visible` | 378 | KEEP |
| `/* Fantasy theme overrides for BYOK CTA */ [data-theme='fantasy'] .byok-cta-btn` | 384 | KEEP |
| `#loading-overlay` | 389 | KEEP |
| `#loading-overlay .spinner-border` | 402 | KEEP |
| `#auth-container .auth-connecting-spinner` | 408 | KEEP |
| `@keyframes auth-connecting-spin` | 417 | KEEP |
| `to` | 418 | KEEP |
| `#auth-container .btn-reload` | 423 | KEEP |
| `/* View management */ #auth-view, #dashboard-view, #new-campaign-view, #game-view, #settings-view` | 438 | KEEP |
| `#auth-view.active-view, #dashboard-view.active-view, #new-campaign-view.active-view, #settings-view.` | 445 | KEEP |
| `/* Fill the viewport instead of a fixed 85vh (rev-f9kno.9). height: 85vh left a MEASURED 80px dead b` | 468 | KEEP |
| `body:has(#game-view.active-view) #main-content` | 481 | KEEP |
| `#game-view.active-view` | 488 | KEEP |
| `/* Beats animations.css #game-view.active` | 493 | KEEP |
| `#game-view.active-view.active` | 501 | KEEP |
| `/* Horizontal-scrollbar guard lives on descendants that do NOT contain the header avatar. overflow-x` | 511 | KEEP |
| `/* The toolbar inside #game-view is a flex row with flex-wrap: wrap, which lets *multiple* items dro` | 529 | KEEP |
| `/* On ultra-compact viewports (≤360px), gracefully allow 2-row wrap layout per US-089 */ @media (max` | 535 | KEEP |
| `#game-view > .d-flex.justify-content-between.align-items-center.mb-1` | 536 | KEEP |
| `#game-view > .d-flex.justify-content-between.align-items-center.mb-1 > .d-flex.align-items-center:fi` | 541 | KEEP |
| `#game-view #game-title` | 546 | KEEP |
| `#game-view #campaign-details-btn` | 554 | KEEP |
| `#game-view > .d-flex.justify-content-between.align-items-center.mb-1 > .d-flex.align-items-center.ms` | 561 | KEEP |
| `#game-view > .d-flex.flex-wrap > *` | 566 | KEEP |
| `/* The outer-row rule above only reaches the toolbar row's direct children (the title <h2> and the r` | 582 | KEEP |
| `#game-view > .d-flex.flex-wrap > .d-flex.flex-wrap > *` | 587 | KEEP |
| `.story-reader-shell` | 591 | KEEP |
| `#story-content` | 599 | KEEP |
| `.keep-reading` | 621 | KEEP |
| `.keep-reading > *` | 653 | KEEP |
| `.story-reader-shell::after` | 657 | KEEP |
| `.story-reader-shell.has-unread::after` | 671 | KEEP |
| `.story-reader-shell.has-unread .keep-reading` | 676 | KEEP |
| `/* The inline coach owns the visual language for contextual help. */ [data-theme='fantasy']` | 683 | KEEP |
| `.tooltip` | 688 | KEEP |
| `.tooltip .tooltip-inner` | 695 | KEEP |
| `.first-turn-coach` | 701 | KEEP |
| `.first-turn-coach .coach-steps` | 714 | KEEP |
| `.first-turn-coach .coach-steps b` | 720 | KEEP |
| `.first-turn-coach .coach-close` | 721 | KEEP |
| `#first-turn-coach-dismiss` | 729 | KEEP |
| `.first-turn-coach > .bi` | 733 | KEEP |
| `.first-turn-coach .coach-close:focus-visible` | 734 | KEEP |
| `.mode-hint` | 738 | KEEP |
| `.mode-hint b` | 744 | KEEP |
| `.hud` | 745 | KEEP |
| `.hud-left, .hud-actions, .hud-spicy` | 761 | KEEP |
| `.hud-left` | 765 | KEEP |
| `.hud-copy` | 766 | KEEP |
| `.hud-actions` | 767 | KEEP |
| `.hud #game-title, .hud-sub` | 768 | KEEP |
| `.hud #game-title` | 773 | KEEP |
| `#game-view > .hud #game-title` | 774 | KEEP |
| `.hud-sub` | 782 | KEEP |
| `.hud-subline` | 783 | KEEP |
| `.hud-subline .hud-sub` | 784 | KEEP |
| `/* Reserve the chili slot while off so confirmed settings never shift the scene line. */ .hud-spicy-` | 786 | KEEP |
| `.hud-sub--timed` | 787 | KEEP |
| `.hud-sub--timed .hud-sub-place` | 788 | KEEP |
| `.hud-sub--timed .hud-sub-time` | 789 | KEEP |
| `.hud button, .hud .hud-menu-row, .hud .form-check-label` | 790 | KEEP |
| `.hud #back-to-dashboard, .hud #game-settings-btn, .hud #undoStoryBtn, .hud #downloadStoryBtn, .hud #` | 795 | KEEP |
| `.hud #hud-more-btn:focus-visible` | 802 | KEEP |
| `.hud-more` | 803 | KEEP |
| `.hud-menu` | 804 | KEEP |
| `.hud-menu-row` | 805 | KEEP |
| `.hud-menu-row:hover, .hud-menu-row:focus-visible` | 806 | KEEP |
| `.hud-menu-separator` | 807 | KEEP |
| `.hud-menu-theme` | 808 | KEEP |
| `.hud-theme-options` | 809 | KEEP |
| `.hud-theme-option` | 810 | KEEP |
| `.hud-theme-option__label` | 822 | KEEP |
| `.hud-theme-option[aria-pressed="true"] .hud-theme-option__label` | 830 | KEEP |
| `.hud-theme-option:focus-visible` | 834 | KEEP |
| `.spicy-mode__icon` | 840 | KEEP |
| `.spicy-switch` | 841 | KEEP |
| `.spicy-switch__knob` | 842 | KEEP |
| `#hud-menu .spicy-switch` | 843 | KEEP |
| `#hud-menu .hud-menu-spicy` | 844 | KEEP |
| `.hud-menu-sub` | 845 | KEEP |
| `.spicy-state__on` | 846 | KEEP |
| `body:has(#spicyModeSwitch:checked) .spicy-mode__icon` | 847 | KEEP |
| `body:has(#spicyModeSwitch:checked) .spicy-switch` | 848 | KEEP |
| `body:has(#spicyModeSwitch:checked) .spicy-switch__knob` | 849 | KEEP |
| `body:has(#spicyModeSwitch:checked) .spicy-state__on` | 850 | KEEP |
| `body:has(#spicyModeSwitch:checked) .spicy-state__off` | 851 | KEEP |
| `#spicyModeSwitch:checked` | 852 | KEEP |
| `@media (prefers-reduced-motion: reduce)` | 853 | KEEP |
| `.spicy-switch, .spicy-switch__knob` | 854 | KEEP |
| `.hud [hidden], .hud-menu-row[hidden]` | 856 | KEEP |
| `@media (max-width: 767.98px)` | 857 | KEEP |
| `#game-view .undo-label` | 858 | KEEP |
| `#game-view > .hud` | 859 | KEEP |
| `.hud-actions` | 867 | KEEP |
| `.hud-more` | 868 | KEEP |
| `/* The open theme dropdown hangs over the sticky HUD (1060). */ .navbar:has(.dropdown-menu.show)` | 870 | KEEP |
| `body:has(#game-view.active-view) .navbar .wiki-nav-link, body:has(#game-view.active-view) .navbar .s` | 873 | KEEP |
| `/* With the wiki/social/email links hidden the theme toggle has room for btn-sm size. */ body:has(#g` | 875 | KEEP |
| `#game-view > .hud` | 880 | KEEP |
| `the slot needs no positioning. */ #game-view > .hud .header-avatar-slot` | 882 | KEEP |
| `#game-view > .hud #game-title` | 887 | KEEP |
| `/* Static wrapper: the menu anchors to the header row's right edge. */ #game-view > .hud .hud-more` | 892 | KEEP |
| `.hud-menu` | 902 | KEEP |
| `.hud-menu-row` | 907 | KEEP |
| `577px and wider keep the tablet/desktop rules. */ @media (max-width: 576px)` | 915 | KEEP |
| `/* The HUD is the top row on phones: the site navbar collapses and its theme picker lives in the ove` | 918 | KEEP |
| `/* Beats the markup's Bootstrap mt-1 so the HUD sits flush with the top. */ #game-view.active-view` | 920 | KEEP |
| `#hud-menu .hud-menu-theme` | 921 | KEEP |
| `#game-view > .hud #back-to-dashboard` | 922 | KEEP |
| `collapse it the same way so the overflow menu fits the viewport. */ @media (max-height: 500px) and (` | 933 | KEEP |
| `body:has(#game-view.active-view) > .navbar` | 934 | KEEP |
| `#game-view.active-view` | 935 | KEEP |
| `#hud-menu .hud-menu-theme` | 936 | KEEP |
| `#hud-menu .hud-menu-row[data-reddit-link], #hud-menu .hud-menu-row[data-discord-link]` | 938 | KEEP |
| `/* Narrow desktop windows and mobile devices up to 767.98px: the site navbar collapses and its theme` | 942 | KEEP |
| `body:has(#game-view.active-view) > .navbar` | 943 | KEEP |
| `#game-view.active-view` | 944 | KEEP |
| `#hud-menu .hud-menu-theme` | 945 | KEEP |
| `@media (min-width: 768px)` | 947 | KEEP |
| `1060 here would sit above the navbar (1050) and swallow theme-dropdown clicks. */ #game-view > .hud` | 950 | KEEP |
| `#game-view > .hud #back-to-dashboard` | 961 | KEEP |
| `#game-view > .hud .header-avatar-slot` | 968 | KEEP |
| `#game-view > .hud #game-title` | 972 | KEEP |
| `body.kb > .navbar, body.kb .mode-hint` | 978 | KEEP |
| `the selector must out-rank #game-view.active-view.active and the shell's flex-grow, or the HUD scrol` | 985 | KEEP |
| `/* Long unbroken tokens inside <pre> blocks (URLs, base64, JSON dumps, hex strings, debug_info state` | 1002 | KEEP |
| `/* The "Load older entries" button is the first child of the scrollable #story-content container. Wi` | 1015 | KEEP |
| `/* Narrative prose */ .story-entry` | 1022 | KEEP |
| `.story-meta` | 1023 | KEEP |
| `.story-meta .dot` | 1024 | KEEP |
| `.narrative-card > .story-meta` | 1025 | KEEP |
| `.story-entry--user .story-md` | 1026 | KEEP |
| `.story-md` | 1027 | KEEP |
| `@media (min-width: 768px)` | 1028 | KEEP |
| `.story-md` | 1028 | KEEP |
| `.story-md p` | 1029 | KEEP |
| `.story-md h1, .story-md h2, .story-md h3, .story-md h4` | 1030 | KEEP |
| `.story-md strong` | 1034 | KEEP |
| `.story-md blockquote` | 1035 | KEEP |
| `/* Streaming layout, badge, skeleton, caret */ .stream-badge` | 1038 | KEEP |
| `.stream-badge .live-dot, .keep-reading .live-dot` | 1039 | KEEP |
| `@keyframes wa-pulse` | 1040 | KEEP |
| `0%, 100%` | 1040 | KEEP |
| `50%` | 1040 | KEEP |
| `.skeleton-line` | 1041 | KEEP |
| `@keyframes wa-shimmer` | 1042 | KEEP |
| `from` | 1042 | KEEP |
| `to` | 1042 | KEEP |
| `.stream-plain` | 1043 | KEEP |
| `.streaming-text .streaming-tail` | 1044 | KEEP |
| `.stream-caret` | 1045 | KEEP |
| `@keyframes wa-blink` | 1046 | KEEP |
| `50%` | 1046 | KEEP |
| `@media (prefers-reduced-motion: reduce)` | 1047 | KEEP |
| `.stream-badge .live-dot, .keep-reading .live-dot, .skeleton-line, .stream-caret, .streaming-cursor.b` | 1048 | KEEP |
| `.keep-reading, .story-reader-shell::after` | 1051 | KEEP |
| `#interaction-form` | 1054 | KEEP |
| `#interaction-form textarea` | 1058 | KEEP |
| `.undo-label` | 1062 | KEEP |
| `/* Icon button styling */ #shareStoryBtn, #downloadStoryBtn` | 1068 | KEEP |
| `#shareStoryBtn i, #downloadStoryBtn i` | 1075 | KEEP |
| `#downloadStoryBtn` | 1079 | KEEP |
| `#downloadStoryBtn:hover, #downloadStoryBtn:focus` | 1087 | KEEP |
| `/* Navbar must create a stacking context above view containers. animation-helpers.js sets transform:` | 1097 | KEEP |
| `.navbar .dropdown-menu` | 1100 | KEEP |
| `/* Navbar brand link styling - shifted right to accommodate 88px hero avatar */ .navbar-brand, a.nav` | 1106 | KEEP |
| `#first-run-banner` | 1113 | KEEP |
| `@media (max-width: 576px)` | 1117 | KEEP |
| `.navbar-brand, a.navbar-brand` | 1119 | KEEP |
| `#first-run-banner` | 1122 | KEEP |
| `a.navbar-brand:hover` | 1127 | KEEP |
| `/* ========== CAMPAIGN LIST STYLING ========== */ /* Ensure consistent campaign list layout between ` | 1135 | KEEP |
| `.list-group-item[data-campaign-id] .campaign-list-header .campaign-list-actions` | 1140 | KEEP |
| `.list-group-item[data-campaign-id] .edit-campaign-btn` | 1147 | KEEP |
| `.list-group-item[data-campaign-id] .text-muted` | 1152 | KEEP |
| `/* Ensure campaign title doesn't overflow */ .list-group-item[data-campaign-id] .campaign-list-heade` | 1159 | KEEP |
| `@media (max-width: 575.98px)` | 1167 | KEEP |
| `.list-group-item[data-campaign-id] .campaign-list-header` | 1168 | KEEP |
| `.list-group-item[data-campaign-id] .campaign-list-header .campaign-list-actions` | 1173 | KEEP |
| `/* Pin the action buttons to their natural width — no flex shrinking so the full label ("Edit" / "Du` | 1190 | KEEP |
| `/* The "Last played" <small> should drop to its own row on mobile so the date text never gets pushed` | 1198 | KEEP |
| `.list-group-item[data-campaign-id] .campaign-list-header .campaign-title-link` | 1207 | KEEP |
| `/* Defensive: prevent the page from acquiring horizontal scroll on narrow viewports. Without this, a` | 1224 | KEEP |
| `/* On mobile, force the theme menu to dock to the right edge of the viewport with a small gutter, so` | 1232 | KEEP |
| `/* ========== STRUCTURED FIELDS STYLING ========== */ /* God Mode Response - Purple border with emph` | 1243 | KEEP |
| `.god-mode-response pre` | 1251 | KEEP |
| `/* Entities Mentioned - Light blue background */ .entities-mentioned` | 1260 | KEEP |
| `.entities-mentioned ul` | 1268 | KEEP |
| `/* Location Confirmed - Alice blue background */ .location-confirmed` | 1274 | KEEP |
| `/* Dice Rolls - Light green background */ .dice-rolls` | 1283 | KEEP |
| `.dice-rolls ul` | 1291 | KEEP |
| `/* Supporting status stays smaller than the narrative without hiding its data. */ .resources` | 1297 | KEEP |
| `/* System Warnings - Yellow background */ .system-warnings` | 1309 | KEEP |
| `.system-warnings ul` | 1317 | KEEP |
| `/* Rewards Box - Green background */ .rewards-box` | 1323 | KEEP |
| `.rewards-box strong` | 1332 | KEEP |
| `/* System notices: level-up banner + character sheet repair. Theme tokens only. */ .level-up-notice,` | 1338 | KEEP |
| `.level-up-notice` | 1347 | KEEP |
| `.rewards-box .level-up-notice, .level-up-repair-notice strong` | 1356 | KEEP |
| `.rewards-box .level-up-notice span` | 1360 | KEEP |
| `/* Equipment Display - Light blue background */ .equipment-display` | 1365 | KEEP |
| `.equipment-display ul` | 1373 | KEEP |
| `/* State Updates - Light gray background */ .state-updates` | 1379 | KEEP |
| `.state-updates pre` | 1387 | KEEP |
| `/* Planning Block - Light blue background */ .planning-block` | 1396 | KEEP |
| `/* Planning block choice buttons - simplified design */ .planning-block-choices` | 1406 | KEEP |
| `.planning-block-thinking` | 1411 | KEEP |
| `/* Debug Info - Light gray with nested sections */ .debug-info` | 1418 | KEEP |
| `/* DM Notes - Light purple background */ .dm-notes` | 1427 | KEEP |
| `.dm-notes ul` | 1435 | KEEP |
| `/* State Rationale - Light yellow background */ .state-rationale` | 1441 | KEEP |
| `pre` | 1450 | KEEP |
| `/* ============================================ Neutral Character Info Cards (stats/equipment/spells` | 1460 | KEEP |
| `#game-view .stats-header, #game-view .info-header` | 1472 | KEEP |
| `#game-view .stat-badge, #game-view .info-badge` | 1481 | KEEP |
| `#game-view .stat-badge.spell, #game-view .info-badge.spell` | 1492 | KEEP |
| `#game-view .info-subtext` | 1498 | KEEP |
| `#game-view .stats-spellcasting, #game-view .info-subrow` | 1504 | KEEP |
| `#game-view .stats-table, #game-view .info-table` | 1512 | KEEP |
| `#game-view .stats-table th, #game-view .stats-table td, #game-view .info-table th, #game-view .info-` | 1521 | KEEP |
| `#game-view .info-table tbody tr:nth-child(even)` | 1528 | KEEP |
| `#game-view .stats-table th, #game-view .info-table th` | 1533 | KEEP |
| `#game-view .compact-table th, #game-view .compact-table td` | 1541 | KEEP |
| `#game-view .features-section, #game-view .info-block` | 1546 | KEEP |
| `#game-view .features-section .features-header` | 1556 | KEEP |
| `#game-view .features-section .feature-item` | 1560 | KEEP |
| `#game-view .info-section-title` | 1565 | KEEP |
| `#game-view .stats-section` | 1572 | KEEP |
| `/* ========== SPLASH PAGE / LOGGED-OUT VIEW STYLING ========== */ /* Background image for logged-out` | 1585 | KEEP |
| `/* Adjust navbar for logged-out state */ body.is-logged-out .navbar` | 1591 | KEEP |
| `/* ============================================================ WELCOME SCREEN — Dragon GCP login ==` | 1597 | KEEP |
| `/* Dragon background */ .welcome-bg` | 1611 | KEEP |
| `.welcome-overlay` | 1624 | KEEP |
| `.welcome-vignette` | 1636 | KEEP |
| `.welcome-stars` | 1643 | KEEP |
| `.welcome-star` | 1649 | KEEP |
| `@keyframes star-twinkle` | 1655 | KEEP |
| `from` | 1656 | KEEP |
| `to` | 1657 | KEEP |
| `/* Card */ .welcome-card` | 1661 | KEEP |
| `.welcome-logo` | 1678 | KEEP |
| `.welcome-logo__icon` | 1684 | KEEP |
| `@keyframes welcome-icon-float` | 1690 | KEEP |
| `from` | 1691 | KEEP |
| `to` | 1692 | KEEP |
| `@media (prefers-reduced-motion: reduce)` | 1694 | KEEP |
| `.welcome-logo__icon` | 1695 | KEEP |
| `.welcome-star` | 1696 | KEEP |
| `.welcome-logo__name` | 1699 | KEEP |
| `.welcome-tagline` | 1712 | KEEP |
| `.welcome-desc` | 1722 | KEEP |
| `.welcome-finish-title` | 1730 | KEEP |
| `.welcome-actions` | 1738 | KEEP |
| `/* Welcome sign-in buttons */ .btn-google, .btn-openrouter` | 1747 | KEEP |
| `.btn-google` | 1765 | KEEP |
| `.btn-google:hover` | 1771 | KEEP |
| `.btn-google:disabled` | 1775 | KEEP |
| `.btn-google:disabled:hover` | 1779 | KEEP |
| `.btn-google__icon` | 1782 | KEEP |
| `.btn-openrouter` | 1788 | KEEP |
| `.btn-openrouter:hover` | 1794 | KEEP |
| `.btn-openrouter:focus-visible, .btn-google:focus-visible` | 1799 | KEEP |
| `.btn-openrouter__mark` | 1803 | KEEP |
| `.welcome-openrouter-disclosure` | 1816 | KEEP |
| `@media (max-width: 640px)` | 1823 | KEEP |
| `.welcome-screen` | 1824 | KEEP |
| `.welcome-card` | 1828 | KEEP |
| `.btn-google, .btn-openrouter` | 1835 | KEEP |
| `.welcome-logo__icon` | 1839 | KEEP |
| `.welcome-logo__name` | 1843 | KEEP |
| `.welcome-desc` | 1847 | KEEP |
| `.btn-waitlist-requested, .btn-waitlist-requested:hover` | 1853 | KEEP |
| `.waitlist-status` | 1859 | KEEP |
| `.waitlist-status--requested` | 1869 | KEEP |
| `.waitlist-status__icon` | 1875 | KEEP |
| `.waitlist-status__copy` | 1888 | KEEP |
| `.waitlist-status__copy span` | 1897 | KEEP |
| `.welcome-legal` | 1901 | KEEP |
| `@media (max-width: 640px)` | 1909 | KEEP |
| `.welcome-legal` | 1910 | KEEP |
| `.welcome-legal a` | 1915 | KEEP |
| `.welcome-legal a:hover` | 1919 | KEEP |
| `/* Ensure auth-view fills viewport for welcome screen */ body.is-logged-out #auth-view` | 1922 | KEEP |
| `body.is-logged-out #main-content` | 1927 | KEEP |
| `/* ── Rate Limit Modal (always-loaded styles) ──────────────────────────────── */ .rate-limit-modal-` | 1933 | KEEP |
| `.rate-limit-modal-header, .rate-limit-modal-body, .rate-limit-modal-footer` | 1942 | KEEP |
| `.rate-limit-icon-badge` | 1946 | KEEP |
| `.rate-limit-timer` | 1957 | KEEP |
| `.rate-limit-timer-icon` | 1963 | KEEP |
| `.rate-limit-byok-hint` | 1965 | KEEP |
| `.rate-limit-key-icon` | 1971 | KEEP |
| `.rate-limit-settings-btn` | 1973 | KEEP |
| `.rate-limit-settings-btn:hover, .rate-limit-settings-btn:focus` | 1981 | KEEP |
| `.rate-limit-close-secondary` | 1986 | KEEP |
| `/* Wiki nav link (header) and campaign help link */ .wiki-nav-link` | 1994 | KEEP |
| `/* Inline variant — used when the Wiki link sits next to the brand in the navbar. */ .wiki-nav-link-` | 2007 | KEEP |
| `/* * Pill variant — prominent, clickable-looking button in the navbar. * * Renders as a rounded pill` | 2024 | KEEP |
| `.wiki-nav-link--pill .wiki-nav-link__label` | 2039 | KEEP |
| `.wiki-nav-link--pill .wiki-nav-link__sep` | 2044 | KEEP |
| `.wiki-nav-link--pill .wiki-ext-icon` | 2050 | KEEP |
| `.wiki-nav-link--pill:hover, .wiki-nav-link--pill:focus-visible` | 2056 | KEEP |
| `.wiki-nav-link--pill:hover .wiki-ext-icon, .wiki-nav-link--pill:focus-visible .wiki-ext-icon` | 2066 | KEEP |
| `.wiki-nav-link--pill:active` | 2070 | KEEP |
| `/* Light theme: stronger outline so the pill stays visible on light bg. */ [data-theme='light'] .wik` | 2077 | KEEP |
| `/* * Social-pill nav links (Reddit, Discord) — sit immediately to the right * of the Knowledge-base ` | 2089 | KEEP |
| `.social-nav-link--pill` | 2101 | KEEP |
| `.social-nav-link--pill .social-nav-link__icon` | 2111 | KEEP |
| `.social-nav-link--pill .social-nav-link__label` | 2116 | KEEP |
| `/* Reddit — brand orange #FF4500 (readable on dark and light themes). */ .social-nav-link--reddit` | 2121 | KEEP |
| `.social-nav-link--reddit:hover, .social-nav-link--reddit:focus-visible` | 2128 | KEEP |
| `.social-nav-link--reddit:hover .social-nav-link__icon, .social-nav-link--reddit:focus-visible .socia` | 2138 | KEEP |
| `.social-nav-link--reddit:active` | 2142 | KEEP |
| `/* Discord — brand blurple #5865F2 (readable on dark and light themes). */ .social-nav-link--discord` | 2148 | KEEP |
| `.social-nav-link--discord:hover, .social-nav-link--discord:focus-visible` | 2155 | KEEP |
| `.social-nav-link--discord:hover .social-nav-link__icon, .social-nav-link--discord:focus-visible .soc` | 2165 | KEEP |
| `.social-nav-link--discord:active` | 2169 | KEEP |
| `/* * Mobile navbar (<= 768px): keep all six elements (brand, wiki pill, reddit * pill, discord pill,` | 2193 | KEEP |
| `.navbar > .container` | 2194 | KEEP |
| `.navbar > .container > .navbar-nav.ms-auto` | 2201 | KEEP |
| `/* Brand: tighter spacing so the pill cluster has room. */ .navbar > .container > a.navbar-brand` | 2209 | KEEP |
| `the prior 0.5rem (~8px) fell below the 8px legibility minimum CR flagged. Padding trimmed to 0.1rem ` | 2223 | KEEP |
| `/* Wiki pill needs at least 50px so the short "Wiki" label + icon stays visible at 360px (otherwise ` | 2235 | KEEP |
| `.navbar > .container > .social-nav-link--pill .social-nav-link__icon` | 2239 | KEEP |
| `.navbar > .container > .wiki-nav-link--pill .wiki-ext-icon` | 2243 | KEEP |
| `/* Show the short "Wiki" label instead of "Knowledge base / wiki" so the pill is wide enough for the` | 2249 | KEEP |
| `.navbar > .container > .wiki-nav-link--pill .wiki-nav-link__label-short` | 2252 | KEEP |
| `the email is the one element allowed to give up width under pressure. */ .navbar > .container > .nav` | 2268 | KEEP |
| `/* Theme dropdown button: compact to match the new pill rhythm. flex-shrink: 0 matches the same inva` | 2285 | KEEP |
| `/* Mobile (<=576px): hide email to keep theme switcher inside viewport */ @media (max-width: 576px)` | 2294 | KEEP |
| `.navbar > .container > .navbar-nav > .navbar-text#user-email` | 2295 | KEEP |
| `/* Ultra-compact (<=350px / legacy 320px devices): collapse social labels to icon-only */ @media (ma` | 2301 | KEEP |
| `.navbar > .container > .social-nav-link--pill .social-nav-link__label` | 2302 | KEEP |
| `.navbar > .container > .social-nav-link--pill` | 2305 | KEEP |
| `/* Desktop / tablet: show the full label, hide the short label. */ .wiki-nav-link--pill .wiki-nav-li` | 2313 | KEEP |
| `.wiki-nav-link:hover` | 2317 | KEEP |
| `.wiki-nav-link:focus-visible` | 2323 | KEEP |
| `.wiki-ext-icon` | 2331 | KEEP |
| `.wiki-campaign-help` | 2336 | KEEP |
| `.wiki-campaign-link` | 2340 | KEEP |
| `.wiki-campaign-link:hover` | 2348 | KEEP |
| `.wiki-campaign-link:focus-visible` | 2353 | KEEP |
| `/* Dragon Knight Locked Input Styles */ :root` | 2362 | KEEP |
| `.dk-locked-input` | 2366 | KEEP |
| `/* ========================================================================== ⚡ Premium Quick Start ` | 2383 | KEEP |
| `/* Glass sheen — a soft top-left highlight for a premium glossy feel (filled pill) */ .detailed-camp` | 2407 | KEEP |
| `/* Shimmer sweep bar, triggered on hover */ .quick-start-btn-primary::after` | 2418 | KEEP |
| `.quick-start-btn-primary:hover::after` | 2431 | KEEP |
| `.quick-start-btn-primary:hover` | 2435 | KEEP |
| `.quick-start-btn-primary:active` | 2442 | KEEP |
| `.quick-start-btn-primary:focus-visible` | 2446 | KEEP |
| `/* Fantasy theme override for Quick Start button — outlined dark pill with a glowing purple border *` | 2453 | KEEP |
| `[data-theme='fantasy'] .quick-start-btn-primary:hover` | 2461 | KEEP |
| `/* Bolt icon — plain white glyph directly on the gradient, no chip circle. */ .quick-start-bolt` | 2469 | KEEP |
| `.quick-start-bolt svg` | 2475 | KEEP |
| `/* Custom Campaign — the filled member of the CTA pair: glowing gradient pill with white text. 1px b` | 2485 | KEEP |
| `/* Same hover shimmer sweep as the primary — the pair moves as a set, and the sweep is the "this is ` | 2511 | KEEP |
| `.detailed-campaign-btn:hover::after` | 2524 | KEEP |
| `.detailed-campaign-btn:hover` | 2528 | KEEP |
| `.detailed-campaign-btn:active` | 2536 | KEEP |
| `.detailed-campaign-btn:focus-visible` | 2540 | KEEP |
| `.detailed-campaign-icon` | 2545 | KEEP |
| `[data-theme='fantasy'] .detailed-campaign-btn` | 2552 | KEEP |
| `[data-theme='fantasy'] .detailed-campaign-btn:focus-visible` | 2563 | KEEP |
| `[data-theme='fantasy'] .detailed-campaign-btn:hover` | 2568 | KEEP |
| `/* Quick Start Hero Feature Card for Zero-Campaign / Campaign Creation View. Accent re-tinted from t` | 2577 | KEEP |
| `/* The card's background stays a fixed light tint (#fbfaf8) in BOTH themes, but the fantasy theme se` | 2591 | KEEP |
| ` to a near-white light lavender for the dark page background elsewhere on the page. Without this ove` | 2599 | KEEP |
| `/* Same inheritance trap as the h4 above for the description line: Bootstrap's .text-muted resolves ` | 2608 | KEEP |
| `/* "Pre-built Campaign" badge: the stock text-success on bg-success-subtle pair is only ~3.5:1. Expl` | 2614 | KEEP |
| `/* Blurred accent blob, top-right — decorative atmosphere, non-interactive */ .quick-start-hero-card` | 2621 | KEEP |
| `.quick-start-hero-card:hover` | 2634 | KEEP |
| `[data-theme='fantasy'] .quick-start-hero-card` | 2639 | KEEP |
| `[data-theme='fantasy'] .quick-start-hero-card::before` | 2645 | KEEP |
| `[data-theme='fantasy'] .quick-start-hero-card:hover` | 2649 | KEEP |
| `/* Standalone decorative icon (hero card headline) — plain emoji pulse, no glass chip */ .quick-star` | 2655 | KEEP |
| `@keyframes pulse-icon` | 2660 | KEEP |
| `0%` | 2661 | KEEP |
| `50%` | 2662 | KEEP |
| `100%` | 2663 | KEEP |
| `@media (prefers-reduced-motion: reduce)` | 2666 | KEEP |
| `.quick-start-icon-pulse` | 2667 | KEEP |
| `/* Button icon chip is intentionally static — see the "single carrying effect" note on .quick-start-` | 2687 | KEEP |
| `.quick-start-hero-header h4` | 2692 | KEEP |
| `.quick-start-hero-header .badge` | 2697 | KEEP |
| `/* Dashboard "My Campaigns" header (title + Quick Start / Custom Campaign / settings CTA cluster). A` | 2712 | KEEP |
| `.dashboard-header-row .quick-start-btn-primary, .dashboard-header-row .detailed-campaign-btn` | 2714 | KEEP |
| `/* ========== MOBILE: icon-only Back to Dashboard button ========== Preserve the desktop label while` | 2723 | KEEP |
| `@media (min-width: 577px)` | 2725 | KEEP |
| `.back-to-dashboard__label` | 2726 | KEEP |
| `@media (max-width: 576px)` | 2729 | KEEP |
| `#game-view .back-to-dashboard__label` | 2730 | KEEP |
| `#game-view .back-to-dashboard__icon` | 2731 | KEEP |
| `#back-to-dashboard.back-to-dashboard` | 2732 | KEEP |
| `/* ========== MOBILE: collapse Spicy label to icon-only ========== "🌶️ Spicy" + a tooltip ? button i` | 2744 | KEEP |
| `#game-view .form-check-label[for="spicyModeSwitch"]::before` | 2749 | KEEP |
| `/* Hide the standalone Spicy-info tooltip button next to the switch — the emoji itself retains the n` | 2757 | KEEP |
| `/* ========== MOBILE: hide the wide "Add your key" CTA ========== The BYOK CTA button is ~190px on i` | 2765 | KEEP |
| `/* ========== MOBILE: anchor the title block so the info button stays at the right edge of the title` | 2774 | KEEP |
| `#game-view .header-avatar-slot` | 2781 | KEEP |
| `#game-view #campaign-details-btn` | 2782 | KEEP |
| `/* In game view on all viewports, collapse back button to icon-only and match compact action button ` | 2786 | KEEP |
| `#game-view .back-to-dashboard__icon` | 2787 | KEEP |
| `#game-view #back-to-dashboard, #game-view #game-settings-btn, #game-view #undoStoryBtn, #game-view #` | 2793 | KEEP |
| `/* In game view, inline edit container expands to take full horizontal space */ #game-view .inline-e` | 2804 | KEEP |
| `#game-view .inline-edit-input` | 2814 | KEEP |
| `#game-view .inline-edit-buttons` | 2824 | KEEP |
| `the desktop case keeps static positioning. */ @media (max-width: 576px)` | 2837 | KEEP |
| `#game-view > .hud` | 2838 | KEEP |
| `#game-view > .hud > .hud-left` | 2850 | KEEP |
| `/* The HUD is sticky at z-index 1060 at every width, so Bootstrap modals must sit above it. */ .moda` | 2856 | KEEP |
| `.modal` | 2859 | KEEP |
| `/* MOBILE: header CTA cluster wrap fix. Keep the toolbar on one row, let the title shrink first, and` | 2866 | KEEP |
| `#game-view #byok-cta` | 2867 | KEEP |
| `#game-view button[aria-label="Spicy Mode info"]` | 2871 | KEEP |
| `/* Keep settings and dashboard navigation adjacent at the right edge. */ #game-view #game-settings-b` | 2876 | KEEP |
| `#game-view #back-to-dashboard` | 2879 | KEEP |
| `#game-view > .d-flex.justify-content-between.align-items-center.mb-1` | 2883 | KEEP |
| `#game-view > .d-flex.justify-content-between.align-items-center.mb-1 > .d-flex.align-items-center:fi` | 2889 | KEEP |
| `#game-view #campaign-details-btn` | 2894 | KEEP |
| `/* Preserve the avatar's minimum mobile target without changing desktop. */ #header-avatar-slot` | 2899 | KEEP |
| `#header-avatar-slot img, #header-avatar-slot .header-avatar-img` | 2903 | KEEP |
| `/* The title yields horizontal space before any action control does. */ #game-view #game-title` | 2909 | KEEP |
| `/* Keep the pepper identifier visible while collapsing only the word. */ .spicy-mode__text` | 2919 | KEEP |
| `/* Bootstrap's flex-wrap class must not split the action cluster. */ #game-view > .d-flex.justify-co` | 2925 | KEEP |
| `/* Keep icon controls compact enough for phone widths. */ #game-view #undoStoryBtn, #game-view #down` | 2936 | KEEP |
| `/* At the narrowest phone widths, give the title and action cluster separate rows. Keeping the exist` | 2946 | KEEP |
| `#game-view > .d-flex.justify-content-between.align-items-center.mb-1` | 2947 | KEEP |
| `#game-view > .d-flex.justify-content-between.align-items-center.mb-1 > .d-flex.align-items-center:fi` | 2953 | KEEP |
| `#game-view > .d-flex.justify-content-between.align-items-center.mb-1 > .d-flex.align-items-center.ga` | 2959 | KEEP |
| `/* MOBILE: when inline title editor is active in #game-view, allow the header row to wrap and expand` | 2970 | KEEP |
| `#game-view > .hud:has(.inline-edit-container), #game-view > .hud.has-active-inline-editor` | 2972 | KEEP |
| `#game-view > .hud:has(.inline-edit-container) > .hud-left, #game-view > .hud.has-active-inline-edito` | 2978 | KEEP |
| `#game-view .inline-edit-container` | 2984 | KEEP |
| `.story-mode-badge` | 2988 | KEEP |
| `.story-mode-badge--god` | 2989 | KEEP |
| `/* Composer is read-only while the deferred opening story is being written. */ #user-input.opening-s` | 2992 | KEEP |
| `.streaming-scene-illustration-slot:empty, .story-scene-illustration-host:empty` | 2998 | KEEP |
| `.story-scene-illustration-slot` | 3002 | KEEP |
| `.story-scene-illustration-slot--pending .story-scene-illustration__spinner` | 3012 | KEEP |
| `.story-scene-illustration__img` | 3021 | KEEP |
| `.story-scene-illustration__expand` | 3027 | KEEP |
| `.story-scene-illustration__caption` | 3035 | KEEP |
| `.story-scene-illustration-slot--failed .story-scene-illustration__failed` | 3041 | KEEP |
| `.story-scene-illustration-lightbox` | 3051 | KEEP |
| `.story-scene-illustration-lightbox img` | 3061 | KEEP |
| `.story-scene-illustration-lightbox__close` | 3066 | KEEP |
| `/* Outcome card verdict badge */ .outcome-verdict` | 3082 | KEEP |
| `.outcome-verdict--success` | 3083 | KEEP |
| `.outcome-verdict--failure` | 3084 | KEEP |
| `.outcome-verdict--mixed` | 3085 | KEEP |
| `/* Outcome description provenance label ("Turn summary" fallback) */ .outcome-prose-source` | 3088 | KEEP |
| `.dice-narrative-outcome` | 3089 | KEEP |

### `styles/animations.css` — 60 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* ================================== WorldArchitect.AI Animation System Milestone 3: Smooth transit` | 7 | KEEP |
| `/* ================================== PAGE NAVIGATION ANIMATIONS ================================== ` | 24 | KEEP |
| `/* Active view animations */ #auth-view.active, #dashboard-view.active, #new-campaign-view.active, #` | 36 | KEEP |
| `/* Identity transform still creates a stacking context (CSS Transforms 1). That traps .header-avatar` | 47 | KEEP |
| `/* Loading overlay animations */ #loading-overlay` | 52 | KEEP |
| `#loading-overlay.show` | 60 | KEEP |
| `/* ================================== BUTTON ANIMATIONS ================================== */ /* Enh` | 70 | KEEP |
| `.btn:hover` | 80 | KEEP |
| `.btn:active` | 85 | KEEP |
| `/* Button loading animation */ .btn.loading` | 91 | KEEP |
| `.btn.loading::after` | 96 | KEEP |
| `@keyframes btn-spin` | 110 | KEEP |
| `to` | 111 | KEEP |
| `/* ================================== FORM ANIMATIONS ================================== */ /* Form ` | 121 | KEEP |
| `.form-control:focus` | 128 | KEEP |
| `/* Form group focus state */ .mb-3:focus-within` | 134 | KEEP |
| `/* ================================== CARD AND LIST ANIMATIONS ================================== */` | 144 | KEEP |
| `.list-group-item:hover` | 151 | KEEP |
| `/* Card animations */ .card` | 157 | KEEP |
| `.card:hover` | 163 | KEEP |
| `/* ================================== DROPDOWN ANIMATIONS ================================== */ /* E` | 173 | KEEP |
| `.dropdown-menu.show` | 182 | KEEP |
| `/* Dropdown item hover effects */ .dropdown-item` | 189 | KEEP |
| `.dropdown-item:hover` | 195 | KEEP |
| `/* ================================== MODAL ANIMATIONS ================================== */ /* Enha` | 204 | KEEP |
| `.modal.show .modal-dialog` | 210 | KEEP |
| `/* Modal backdrop animation */ .modal-backdrop` | 215 | KEEP |
| `/* ================================== LOADING ANIMATIONS ================================== */ /* En` | 224 | KEEP |
| `@keyframes spinner-grow` | 228 | KEEP |
| `0%` | 229 | KEEP |
| `50%` | 232 | KEEP |
| `100%` | 235 | KEEP |
| `/* Story content loading animation */ #story-content` | 241 | KEEP |
| `#story-content.loading` | 247 | KEEP |
| `/* ================================== MICRO-INTERACTIONS ================================== */ /* Ch` | 257 | KEEP |
| `.form-check-input:checked` | 263 | KEEP |
| `/* Link hover animations */ a` | 268 | KEEP |
| `/* Navbar brand animation */ .navbar-brand` | 275 | KEEP |
| `.navbar-brand:hover` | 279 | KEEP |
| `/* ================================== STAGGER ANIMATIONS FOR LISTS =================================` | 288 | KEEP |
| `.list-group-item:nth-child(1)` | 293 | KEEP |
| `.list-group-item:nth-child(2)` | 296 | KEEP |
| `.list-group-item:nth-child(3)` | 299 | KEEP |
| `.list-group-item:nth-child(4)` | 302 | KEEP |
| `.list-group-item:nth-child(5)` | 305 | KEEP |
| `@keyframes slideInUp` | 309 | KEEP |
| `from` | 310 | KEEP |
| `to` | 314 | KEEP |
| `/* ================================== ACCESSIBILITY AND PERFORMANCE ================================` | 325 | KEEP |
| `*, *::before, *::after` | 328 | KEEP |
| `/* GPU acceleration for smooth animations */ .btn, .card, .list-group-item, .form-control, .dropdown` | 340 | KEEP |
| `/* Remove will-change after animations complete */ .btn:not(:hover), .card:not(:hover), .list-group-` | 347 | KEEP |
| `/* ================================== STORY CONTENT ANIMATIONS ================================== */` | 356 | KEEP |
| `@keyframes typeWriter` | 360 | KEEP |
| `from` | 361 | KEEP |
| `to` | 365 | KEEP |
| `/* Timer info pulse animation */ #timer-info` | 372 | KEEP |
| `@keyframes pulse` | 376 | KEEP |
| `0%, 100%` | 378 | KEEP |
| `50%` | 381 | KEEP |

### `styles/bridge.css` — 2 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* CSS Variable Bridge - Maps old variables to new design system */ /* This ensures backward compati` | 4 | KEEP |
| `/* Fantasy theme adjustments */ [data-theme='fantasy']` | 30 | KEEP |

### `styles/components.css` — 97 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* Modern Component Styles with Bootstrap Compatibility */ /* This file bridges the new design syste` | 5 | KEEP |
| `/* Modern Card Component (Bootstrap-compatible) */ .card` | 14 | KEEP |
| `.card:hover` | 24 | KEEP |
| `/* Glass morphism variant */ .card.glass` | 30 | KEEP |
| `.card-header` | 36 | KEEP |
| `.card-body` | 42 | KEEP |
| `.card-footer` | 46 | KEEP |
| `/* Modern Button Styles (Bootstrap override) */ .btn` | 53 | KEEP |
| `.btn:hover` | 67 | KEEP |
| `.btn:active` | 72 | KEEP |
| `/* Primary Button */ .btn-primary` | 78 | KEEP |
| `.btn-primary:hover` | 83 | KEEP |
| `/* Secondary Button */ .btn-secondary` | 89 | KEEP |
| `.btn-secondary:hover` | 94 | KEEP |
| `/* Success Button */ .btn-success` | 100 | KEEP |
| `/* Danger Button */ .btn-danger` | 106 | KEEP |
| `/* Outline Buttons */ .btn-outline-primary` | 112 | KEEP |
| `.btn-outline-primary:hover` | 119 | KEEP |
| `.btn-outline-secondary` | 124 | KEEP |
| `.btn-outline-secondary:hover` | 131 | KEEP |
| `/* Button Sizes */ .btn-sm` | 137 | KEEP |
| `.btn-lg` | 142 | KEEP |
| `/* Modern Form Controls (Bootstrap override) */ .form-control` | 148 | KEEP |
| `.form-control:focus` | 158 | KEEP |
| `.form-label` | 165 | KEEP |
| `.form-text` | 171 | KEEP |
| `/* Modern Select */ .form-select` | 178 | KEEP |
| `/* Modern List Group (Bootstrap override) */ .list-group` | 188 | KEEP |
| `.list-group-item` | 194 | KEEP |
| `.list-group-item:last-child` | 203 | KEEP |
| `.list-group-item:hover` | 207 | KEEP |
| `.list-group-item.active` | 211 | KEEP |
| `/* Modern Modal (Bootstrap override) */ .modal-content` | 217 | KEEP |
| `.modal-header` | 225 | KEEP |
| `.modal-body` | 230 | KEEP |
| `.modal-footer` | 234 | KEEP |
| `.modal-backdrop` | 240 | KEEP |
| `/* Modern Navbar (Bootstrap override) */ .navbar` | 246 | KEEP |
| `.navbar.glass` | 253 | KEEP |
| `.navbar-brand` | 258 | KEEP |
| `.navbar-nav .nav-link` | 264 | KEEP |
| `.navbar-nav .nav-link:hover` | 271 | KEEP |
| `/* Modern Dropdown (Bootstrap override) */ .dropdown-menu` | 277 | KEEP |
| `.dropdown-item` | 286 | KEEP |
| `.dropdown-item:hover` | 293 | KEEP |
| `.dropdown-item.active` | 298 | KEEP |
| `/* Modern Badge */ .badge` | 304 | KEEP |
| `.badge.bg-primary` | 311 | KEEP |
| `.badge.bg-secondary` | 316 | KEEP |
| `.badge.bg-success` | 321 | KEEP |
| `.badge.bg-danger` | 326 | KEEP |
| `/* Modern Alert */ .alert` | 332 | KEEP |
| `.alert-primary` | 339 | KEEP |
| `.alert-success` | 344 | KEEP |
| `.alert-danger` | 349 | KEEP |
| `/* Modern Progress */ .progress` | 355 | KEEP |
| `.progress-bar` | 363 | KEEP |
| `/* Spinner */ .spinner-border` | 369 | KEEP |
| `/* Utility: Text Colors */ .text-primary` | 375 | KEEP |
| `.text-secondary` | 378 | KEEP |
| `.text-muted` | 381 | KEEP |
| `.text-success` | 384 | KEEP |
| `.text-danger` | 387 | KEEP |
| `/* Utility: Background Colors */ .bg-primary` | 392 | KEEP |
| `.bg-secondary` | 395 | KEEP |
| `.bg-light` | 398 | KEEP |
| `.bg-dark` | 401 | KEEP |
| `/* Special Effects for Fantasy Theme */ [data-theme='fantasy'] .card` | 406 | KEEP |
| `[data-theme='fantasy'] .btn-primary` | 414 | KEEP |
| `/* ── Rate Limit Modal ─────────────────────────────────────────────────────── */ .rate-limit-modal-` | 419 | KEEP |
| `.rate-limit-modal-header, .rate-limit-modal-body, .rate-limit-modal-footer` | 428 | KEEP |
| `.rate-limit-icon-badge` | 432 | KEEP |
| `.rate-limit-modal-title` | 443 | KEEP |
| `.rate-limit-modal-subtitle` | 448 | KEEP |
| `.rate-limit-close-btn` | 452 | KEEP |
| `.rate-limit-message` | 457 | KEEP |
| `.rate-limit-timer` | 462 | KEEP |
| `.rate-limit-timer-icon` | 467 | KEEP |
| `.rate-limit-timer-text` | 471 | KEEP |
| `.rate-limit-byok-hint` | 476 | KEEP |
| `.rate-limit-key-icon` | 481 | KEEP |
| `.rate-limit-byok-title` | 485 | KEEP |
| `.rate-limit-byok-desc` | 489 | KEEP |
| `.rate-limit-settings-btn` | 493 | KEEP |
| `.rate-limit-settings-btn:hover` | 502 | KEEP |
| `.rate-limit-close-secondary` | 507 | KEEP |
| `.rate-limit-close-secondary:hover` | 515 | KEEP |
| `/* (#7945 §3) Primary CTA inside the rate-limit modal body. Promoted above the BYOK hint card so the` | 523 | KEEP |
| `.rate-limit-primary-cta-btn:hover` | 533 | KEEP |
| `.rate-limit-cta-stack` | 538 | KEEP |
| `non-blocking. */ .quota-soft-warn-banner` | 545 | KEEP |
| `.quota-soft-warn-banner i` | 557 | KEEP |
| `.quota-soft-warn-text` | 562 | KEEP |
| `.quota-soft-warn-cta` | 566 | KEEP |
| `/* Fantasy theme overrides */ [data-theme='fantasy'] .rate-limit-settings-btn` | 571 | KEEP |
| `[data-theme='fantasy'] .rate-limit-settings-btn:hover` | 576 | KEEP |
| `[data-theme='fantasy'] .rate-limit-icon-badge` | 581 | KEEP |

### `styles/enhanced-components.css` — 94 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* Enhanced Components CSS - Component Enhancement Milestone * Adds modern interactive effects to ex` | 11 | KEEP |
| `/* Hover effects for all button variants */ .btn-enhanced:hover` | 20 | KEEP |
| `.btn-enhanced:active` | 25 | KEEP |
| `/* Enhanced Primary Buttons */ .btn-primary.btn-enhanced` | 31 | KEEP |
| `.btn-primary.btn-enhanced:hover` | 40 | KEEP |
| `/* Enhanced Secondary Buttons */ .btn-secondary.btn-enhanced` | 50 | KEEP |
| `.btn-secondary.btn-enhanced:hover` | 56 | KEEP |
| `/* Enhanced Success Buttons */ .btn-success.btn-enhanced` | 63 | KEEP |
| `.btn-success.btn-enhanced:hover` | 68 | KEEP |
| `/* Enhanced Danger Buttons */ .btn-danger.btn-enhanced` | 74 | KEEP |
| `.btn-danger.btn-enhanced:hover` | 79 | KEEP |
| `/* Enhanced Info Buttons */ .btn-info.btn-enhanced` | 85 | KEEP |
| `.btn-info.btn-enhanced:hover` | 90 | KEEP |
| `/* Ripple effect container */ .btn-enhanced::before` | 96 | KEEP |
| `.btn-enhanced.ripple-active::before` | 113 | KEEP |
| `/* Loading state for enhanced buttons */ .btn-enhanced.loading` | 119 | KEEP |
| `.btn-enhanced.loading::after` | 124 | KEEP |
| `@keyframes spin` | 139 | KEEP |
| `0%` | 140 | KEEP |
| `100%` | 143 | KEEP |
| `/* ================================== ENHANCED CARD SYSTEM ================================== */ .ca` | 152 | KEEP |
| `.card-enhanced:hover` | 161 | KEEP |
| `/* Enhanced list group items (for campaign list) */ .list-group-item-enhanced` | 168 | KEEP |
| `.list-group-item-enhanced:hover` | 179 | KEEP |
| `.list-group-item-enhanced::before` | 186 | KEEP |
| `.list-group-item-enhanced:hover::before` | 198 | KEEP |
| `/* ================================== ENHANCED FORM SYSTEM ================================== */ /* ` | 207 | KEEP |
| `.form-control-enhanced:focus` | 216 | KEEP |
| `.form-control-enhanced:hover:not(:focus)` | 223 | KEEP |
| `/* Enhanced form labels */ .form-label-enhanced` | 229 | KEEP |
| `/* Enhanced checkboxes and radios */ .form-check-enhanced .form-check-input` | 239 | KEEP |
| `.form-check-enhanced .form-check-input:checked` | 246 | KEEP |
| `.form-check-enhanced .form-check-label` | 252 | KEEP |
| `.form-check-enhanced:hover .form-check-label` | 258 | KEEP |
| `/* Enhanced input groups */ .input-group-enhanced` | 263 | KEEP |
| `.input-group-enhanced:focus-within` | 272 | KEEP |
| `.input-group-enhanced .form-control` | 277 | KEEP |
| `.input-group-enhanced .btn` | 282 | KEEP |
| `/* ================================== ENHANCED MODAL SYSTEM ================================== */ .m` | 291 | KEEP |
| `.modal-enhanced .modal-header` | 299 | KEEP |
| `.modal-enhanced .modal-footer` | 304 | KEEP |
| `/* ================================== ENHANCED NAVIGATION ================================== */ .nav` | 313 | KEEP |
| `.navbar-enhanced .navbar-brand` | 320 | KEEP |
| `.dropdown-enhanced .dropdown-menu` | 328 | KEEP |
| `.dropdown-enhanced .dropdown-item` | 338 | KEEP |
| `.dropdown-enhanced .dropdown-item:hover` | 345 | KEEP |
| `.dropdown-enhanced .dropdown-item.active` | 351 | KEEP |
| `/* ================================== ENHANCED CONTENT AREAS ================================== */ .` | 360 | KEEP |
| `.content-enhanced:hover` | 368 | KEEP |
| `/* Enhanced story content area */ .story-content-enhanced` | 374 | KEEP |
| `.story-content-enhanced::before` | 384 | KEEP |
| `.story-content-enhanced:hover::before` | 396 | KEEP |
| `/* ================================== ENHANCED LOADING STATES ================================== */ ` | 404 | KEEP |
| `.loading-overlay-enhanced` | 413 | KEEP |
| `/* ================================== ENHANCED UTILITIES ================================== */ /* En` | 424 | KEEP |
| `.shadow-enhanced:hover` | 429 | KEEP |
| `/* Enhanced text gradients */ .text-gradient-enhanced` | 434 | KEEP |
| `/* Enhanced glass morphism */ .glass-enhanced` | 442 | KEEP |
| `/* ================================== RESPONSIVE ENHANCEMENTS ================================== */ ` | 453 | KEEP |
| `.btn-enhanced:hover` | 454 | KEEP |
| `.card-enhanced:hover` | 458 | KEEP |
| `.list-group-item-enhanced:hover` | 462 | KEEP |
| `/* ================================== DROPDOWN & INTERACTION FIXES =================================` | 472 | KEEP |
| `.dropdown .btn` | 477 | KEEP |
| `/* Fix button positioning conflicts */ .btn-enhanced` | 482 | KEEP |
| `/* ================================== ACCESSIBILITY ENHANCEMENTS ================================== ` | 494 | KEEP |
| `/* Reduced motion support */ @media (prefers-reduced-motion: reduce)` | 500 | KEEP |
| `.btn-enhanced, .card-enhanced, .list-group-item-enhanced, .form-control-enhanced, .modal-enhanced .m` | 513 | KEEP |
| `.btn-enhanced::before` | 517 | KEEP |
| `.spinner-enhanced` | 521 | KEEP |
| `/* ================================== COLLAPSIBLE SEARCH FILTER PANEL ==============================` | 530 | KEEP |
| `.search-filter-header-row .search-box` | 537 | KEEP |
| `@media (max-width: 576px)` | 542 | KEEP |
| `.search-filter-header-row` | 543 | KEEP |
| `.filter-toggle-btn` | 549 | KEEP |
| `.filter-toggle-btn:hover` | 566 | KEEP |
| `.filter-toggle-btn:focus` | 573 | KEEP |
| `.filter-toggle-btn .toggle-icon-left` | 579 | KEEP |
| `.filter-toggle-btn[aria-expanded="true"] .toggle-icon-left` | 585 | KEEP |
| `/* Toggle Switch Track */ .toggle-switch-track` | 591 | KEEP |
| `/* Dark theme track background override */ [data-theme='fantasy'] .toggle-switch-track` | 604 | KEEP |
| `.filter-toggle-btn[aria-expanded="true"] .toggle-switch-track` | 609 | KEEP |
| `/* Toggle Switch Thumb */ .toggle-switch-thumb` | 614 | KEEP |
| `.filter-toggle-btn[aria-expanded="true"] .toggle-switch-thumb` | 626 | KEEP |
| `.filter-toggle-btn .toggle-chevron` | 631 | KEEP |
| `.filter-toggle-btn[aria-expanded="true"] .toggle-chevron` | 636 | KEEP |
| `.filter-toggle-btn[aria-expanded="true"]` | 640 | KEEP |
| `.filter-badge` | 647 | KEEP |
| `.filter-controls-wrapper` | 660 | KEEP |
| `.filter-controls-wrapper.expanded` | 671 | KEEP |
| `.filter-controls-inner` | 678 | KEEP |
| `/* Mobile-only collapsible campaign filters: hide toggle and force expand on desktop viewports */ @m` | 683 | KEEP |
| `#filter-toggle` | 684 | KEEP |
| `#filter-controls-wrapper` | 687 | KEEP |

### `styles/globals.css` — 4 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* Modern CSS Foundation - Figma Design System */ /* This file contains the comprehensive design sys` | 4 | KEEP |
| `/* Fantasy Theme - Arcane Scholar (dark navy-purple) */ [data-theme='fantasy']` | 155 | KEEP |
| `/* Utility Classes for Modern Effects */ .backdrop-blur` | 219 | KEEP |
| `.gradient-bg` | 223 | KEEP |

### `styles/interactive-features.css` — 139 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* ================================== Interactive Features - Milestone 4 Campaign Wizard, Enhanced M` | 8 | KEEP |
| `/* ================================== CAMPAIGN WIZARD ================================== */ .campaig` | 16 | KEEP |
| `/* Scrollable step content — wizard-navigation always stays below it */ .wizard-content` | 34 | KEEP |
| `.wizard-navigation` | 41 | KEEP |
| `/* Wizard Progress */ .wizard-progress` | 49 | KEEP |
| `.wizard-progress .progress` | 53 | KEEP |
| `.wizard-progress .progress-bar` | 59 | KEEP |
| `/* Step Indicators */ .step-indicators` | 65 | KEEP |
| `.step-indicator` | 69 | KEEP |
| `.step-circle` | 77 | KEEP |
| `.step-label` | 93 | KEEP |
| `.step-indicator.active .step-circle` | 100 | KEEP |
| `.step-indicator.active .step-label` | 107 | KEEP |
| `.step-indicator.completed .step-circle` | 112 | KEEP |
| `.step-indicator.completed .step-label` | 118 | KEEP |
| `.step-indicator:hover .step-circle` | 122 | KEEP |
| `/* Wizard Steps */ .wizard-step` | 128 | KEEP |
| `.wizard-step.active` | 133 | KEEP |
| `@keyframes fadeInUp` | 137 | KEEP |
| `from` | 138 | KEEP |
| `to` | 142 | KEEP |
| `.step-title` | 148 | KEEP |
| `.step-description` | 155 | KEEP |
| `/* Personality Cards */ .personality-card` | 162 | KEEP |
| `.personality-card:hover` | 169 | KEEP |
| `.personality-card.selected` | 175 | KEEP |
| `.personality-icon` | 180 | KEEP |
| `.personality-card .card-title` | 185 | KEEP |
| `.personality-card .card-text` | 191 | KEEP |
| `/* Campaign Type Cards */ .campaign-type-cards` | 198 | KEEP |
| `.campaign-type-card` | 205 | KEEP |
| `.campaign-type-card:hover` | 215 | KEEP |
| `.campaign-type-card.selected` | 221 | KEEP |
| `.campaign-type-card input[type='radio']` | 227 | KEEP |
| `.campaign-type-label` | 233 | KEEP |
| `.campaign-type-icon` | 241 | KEEP |
| `.campaign-type-content h5` | 246 | KEEP |
| `.campaign-type-content p` | 252 | KEEP |
| `/* Option Cards */ .option-card` | 259 | KEEP |
| `.option-card:hover` | 265 | KEEP |
| `.option-icon` | 270 | KEEP |
| `.option-card .card-title` | 275 | KEEP |
| `.option-card .card-text` | 282 | KEEP |
| `/* Campaign Preview */ .campaign-preview` | 289 | KEEP |
| `.campaign-preview .card-title` | 295 | KEEP |
| `.preview-item` | 301 | KEEP |
| `.preview-item:last-child` | 307 | KEEP |
| `.preview-item strong` | 311 | KEEP |
| `/* Editable Preview Items */ .editable-preview` | 317 | KEEP |
| `.editable-preview:hover` | 327 | KEEP |
| `.editable-preview .preview-value` | 331 | KEEP |
| `.editable-preview .edit-btn` | 336 | KEEP |
| `.editable-preview:hover .edit-btn` | 343 | KEEP |
| `.editable-preview .edit-btn:hover` | 347 | KEEP |
| `.editable-preview .edit-input` | 351 | KEEP |
| `.editable-preview .edit-checkboxes` | 356 | KEEP |
| `.editable-preview.editing` | 363 | KEEP |
| `.editable-preview.editing .preview-value, .editable-preview.editing .edit-btn` | 369 | KEEP |
| `desktop and the title/character/setting rows keep the one-line flex layout. */ @media (max-width: 57` | 381 | KEEP |
| `.editable-preview[data-field="description"]` | 382 | KEEP |
| `.editable-preview[data-field="description"] .preview-value` | 386 | KEEP |
| `/* Launch Actions */ .launch-actions .btn` | 393 | KEEP |
| `.launch-actions .btn:hover` | 402 | KEEP |
| `/* Wizard Navigation (flex-shrink: 0, margin-top, padding-top, and border-top are all set above in t` | 413 | KEEP |
| `.wizard-navigation .btn` | 419 | KEEP |
| `.wizard-navigation .btn:hover:not(:disabled)` | 426 | KEEP |
| `/* ================================== ENHANCED MODALS ================================== */ .modern-` | 434 | KEEP |
| `.modern-mode .modal-content` | 438 | KEEP |
| `.modern-mode .modal-header` | 445 | KEEP |
| `.modern-mode .modal-title` | 450 | KEEP |
| `.modern-mode .modal-body` | 455 | KEEP |
| `.modern-mode .modal-footer` | 459 | KEEP |
| `/* Enhanced Modal Animations */ .modern-mode .modal.fade .modal-dialog` | 465 | KEEP |
| `.modern-mode .modal.show .modal-dialog` | 470 | KEEP |
| `/* ================================== SEARCH AND FILTER ================================== */ .searc` | 478 | KEEP |
| `.search-box` | 487 | KEEP |
| `.search-box .form-control` | 492 | KEEP |
| `.search-box .form-control:focus` | 500 | KEEP |
| `.search-box .search-icon` | 506 | KEEP |
| `.filter-controls` | 515 | KEEP |
| `.filter-group` | 522 | KEEP |
| `.filter-group label` | 528 | KEEP |
| `.filter-select` | 535 | KEEP |
| `.filter-select:focus` | 543 | KEEP |
| `.filter-tags` | 548 | KEEP |
| `.filter-tag` | 555 | KEEP |
| `.filter-tag .remove-tag` | 566 | KEEP |
| `.filter-tag .remove-tag:hover` | 573 | KEEP |
| `/* Campaign List Enhancements */ .modern-mode .campaign-item` | 578 | KEEP |
| `.modern-mode .campaign-item:hover` | 587 | KEEP |
| `/* Mobile campaign title improvements */ .campaign-title-link` | 594 | KEEP |
| `@media (max-width: 575.98px)` | 599 | KEEP |
| `.list-group-item .campaign-title-link` | 600 | KEEP |
| `.campaign-meta` | 606 | KEEP |
| `.campaign-tags` | 615 | KEEP |
| `.campaign-tag` | 620 | KEEP |
| `/* ================================== CHECKBOX AND FORM ALIGNMENT ==================================` | 634 | KEEP |
| `.form-check` | 640 | KEEP |
| `.form-check-input` | 646 | KEEP |
| `.form-check-label` | 653 | KEEP |
| `/* Ensure checkboxes in wizard are properly aligned */ .wizard-step input[type='checkbox']` | 660 | KEEP |
| `/* Bootstrap form-check overrides for better alignment */ .personality-card .form-check, .option-car` | 670 | KEEP |
| `.personality-card .form-check-input, .option-card .form-check-input` | 678 | KEEP |
| `/* ================================== RESPONSIVE DESIGN ================================== */ @media` | 687 | KEEP |
| `.campaign-wizard` | 688 | KEEP |
| `.wizard-content` | 699 | KEEP |
| `.step-indicators` | 703 | KEEP |
| `.step-indicator .step-label` | 708 | KEEP |
| `.wizard-navigation` | 712 | KEEP |
| `.filter-controls` | 717 | KEEP |
| `.filter-group` | 722 | KEEP |
| `.campaign-type-cards` | 727 | KEEP |
| `.campaign-type-label` | 731 | KEEP |
| `.campaign-type-icon` | 736 | KEEP |
| `CSS handles the transition. On desktop, even if a stray .is-visible class were added, the @media blo` | 753 | KEEP |
| `.wizard-scroll-indicator.is-visible` | 780 | KEEP |
| `.wizard-scroll-indicator__chevron` | 786 | KEEP |
| `.wizard-scroll-indicator__label` | 798 | KEEP |
| `@keyframes wizard-scroll-indicator-bounce` | 806 | KEEP |
| `0%, 100%` | 807 | KEEP |
| `50%` | 811 | KEEP |
| `@media (prefers-reduced-motion: reduce)` | 817 | KEEP |
| `.wizard-scroll-indicator__chevron` | 818 | KEEP |
| `.wizard-scroll-indicator` | 821 | KEEP |
| `@media (max-width: 768px)` | 826 | KEEP |
| `wizContent is again a direct child of .campaign-wizard, so the scroll container itself is the correc` | 839 | KEEP |
| `.wizard-scroll-indicator` | 847 | KEEP |
| `.wizard-scroll-indicator.is-visible` | 857 | KEEP |
| `/* GH-8015: Navigation stays in normal flow on mobile so it scrolls with the page (regression test c` | 873 | KEEP |
| `.wizard-navigation .step-counter` | 882 | KEEP |
| `.wizard-navigation #wizard-next` | 886 | KEEP |
| `/* Compensate the wizard card's height so the navigation never crowds the last form field on short v` | 892 | KEEP |
| `/* TV Show & Fictional IP Campaign Wizard Styling */ .wizard-universe-pills` | 898 | KEEP |
| `.wizard-universe-pill` | 906 | KEEP |
| `.wizard-universe-pill:hover` | 921 | KEEP |
| `.wizard-universe-pill.active` | 928 | KEEP |
| `.wizard-what-if-box` | 935 | KEEP |
| `.wizard-what-if-box .form-label` | 943 | KEEP |
| `.wizard-recommend-badge` | 951 | KEEP |

### `styles/planning-blocks.css` — 146 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `the operator reversed that decision on 2026-08-18 ("planning block and custom action text too small ` | 14 | KEEP |
| `/* Thinking text paragraph styling */ .planning-block-thinking` | 20 | KEEP |
| `/* Aggressively collapse vertical space below planning block choices */ .planning-block-choices` | 25 | KEEP |
| `.planning-block-choices + div, .planning-block-choices + form, .planning-block-choices + input, .pla` | 34 | KEEP |
| `/* Remove margin from parent if present */ .planning-block-choices:parent` | 40 | KEEP |
| `/* Individual choice button */ .choice-button` | 46 | KEEP |
| `.choice-button:last-child` | 64 | KEEP |
| `the inline-choices rules (.inline-choices .choice-row ...) handle the width/divider differences, sam` | 78 | KEEP |
| `.choice-row:last-child` | 82 | KEEP |
| `.choice-head` | 87 | KEEP |
| `/* The title button keeps the existing .choice-button visual language (background/hover/active/focus` | 96 | KEEP |
| `.ctitle` | 103 | KEEP |
| `/* When expanded, line-wrap the choice title so long choice texts are not cutoff */ .choice-row.open` | 111 | KEEP |
| `.chev-btn` | 118 | KEEP |
| `.chev-btn:hover` | 130 | KEEP |
| `.chev-btn i` | 135 | KEEP |
| `.choice-row.open .chev-btn i` | 140 | KEEP |
| `.choice-detail` | 144 | KEEP |
| `.choice-row.open .choice-detail` | 152 | KEEP |
| `.choice-detail b` | 156 | KEEP |
| `.choice-detail .pro` | 161 | KEEP |
| `.choice-detail .con` | 165 | KEEP |
| `.choice-button:hover` | 169 | KEEP |
| `.choice-button:active` | 174 | KEEP |
| `/* Choice ID styling */ .choice-id` | 179 | KEEP |
| `/* Choice description */ .choice-description` | 187 | KEEP |
| `/* Disabled state when waiting for response */ .choice-button:disabled` | 192 | KEEP |
| `/* Custom choice button styling */ .choice-button-custom` | 199 | KEEP |
| `.choice-button-custom:hover` | 205 | KEEP |
| `.choice-button-custom .choice-id` | 210 | KEEP |
| `.choice-button-custom .choice-description` | 214 | KEEP |
| `/* Custom action button - always shown at bottom of planning block choices */ .custom-action-button` | 220 | KEEP |
| `.custom-action-button:hover` | 229 | KEEP |
| `/* Error state for planning blocks */ .planning-block-error` | 236 | KEEP |
| `.planning-block-error pre` | 245 | KEEP |
| `/* Styling for malformed content within error blocks */ .malformed-content` | 257 | KEEP |
| `/* Responsive design */ @media (max-width: 768px)` | 272 | KEEP |
| `.choice-button` | 273 | KEEP |
| `.choice-id` | 280 | KEEP |
| `.planning-block-choices` | 284 | KEEP |
| `/* Collapsed (no live choices this turn): no border, no background — the input-group underneath fall` | 294 | KEEP |
| `.composer-row > .composer-stack` | 298 | KEEP |
| `/* E1a action bar (rev-f9kno.5, supersedes C4's Send-only full-width-below- dock row from rev-f9kno.` | 310 | KEEP |
| `.toggle-group` | 319 | KEEP |
| `.toggle-group .toggle-pill` | 330 | KEEP |
| `.toggle-group .btn-check:checked + .toggle-pill` | 347 | KEEP |
| `.toggle-group .btn-check:focus-visible + .toggle-pill` | 353 | KEEP |
| `.composer-send` | 358 | KEEP |
| `#interaction-form .composer-send` | 369 | KEEP |
| `.composer-send:disabled` | 374 | KEEP |
| `.composer-stack` | 378 | KEEP |
| `/* Docked (choices present): ONE bordered surface around choices + textarea. Uses --border-color (no` | 393 | KEEP |
| `/* ---------- 2. Read-only history choices ---------- */ /* A wrapper holding only history adds no i` | 403 | KEEP |
| `.past-choices` | 409 | KEEP |
| `.past-choices .past-label` | 416 | KEEP |
| `.past-choice` | 423 | KEEP |
| `.past-choice.taken` | 431 | KEEP |
| `.past-choice .pc-mark` | 435 | KEEP |
| `/* ---------- 3. Your move: inline, always-visible choices ---------- */ .your-move` | 442 | KEEP |
| `.turn-end` | 446 | KEEP |
| `.turn-end::before, .turn-end::after` | 457 | KEEP |
| `.your-move-heading` | 463 | KEEP |
| `.your-move-sub` | 469 | KEEP |
| `.inline-choices` | 474 | KEEP |
| `.inline-choices .choice-row` | 481 | KEEP |
| `.inline-choices .choice-row:not(:first-child)` | 485 | KEEP |
| `.inline-choices .choice-head` | 488 | KEEP |
| `.inline-choices .choice-button` | 492 | KEEP |
| `.inline-choices .choice-button::before` | 513 | KEEP |
| `.inline-choices .choice-button:hover:not(:disabled)` | 529 | KEEP |
| `#your-move .inline-choices .choice-button:disabled` | 532 | KEEP |
| `.inline-choices .choice-button.sending .ctitle::after` | 535 | KEEP |
| `.inline-choices .ctitle` | 541 | KEEP |
| `.inline-choices .cdesc` | 550 | KEEP |
| `.inline-choices .chev-btn` | 557 | KEEP |
| `.inline-choices .chev-btn:hover` | 567 | KEEP |
| `.inline-choices .choice-detail` | 571 | KEEP |
| `.choice-row.open .choice-detail` | 579 | KEEP |
| `.write-own-hint` | 582 | KEEP |
| `.write-own-hint__cta` | 591 | KEEP |
| `.write-own-hint[hidden]` | 608 | KEEP |
| `.write-own-hint .write-own-hint__cta` | 609 | KEEP |
| `.write-own-hint__dismiss` | 610 | KEEP |
| `.write-own-hint__dismiss:focus-visible` | 623 | KEEP |
| `.write-own-hint__cta:hover, .write-own-hint__cta:focus-visible` | 628 | KEEP |
| `.write-own-hint__cta .bi` | 632 | KEEP |
| `.write-own-hint__cta .bi-arrow-down` | 637 | KEEP |
| `.mode-off-hint` | 640 | KEEP |
| `#first-turn-coach-dismiss` | 650 | KEEP |
| `.details-toggle` | 654 | KEEP |
| `.sub-keys` | 665 | KEEP |
| `@media (max-width: 1099px)` | 666 | KEEP |
| `.details-toggle` | 667 | KEEP |
| `@media (min-width: 1100px)` | 669 | KEEP |
| `.sub-touch` | 670 | KEEP |
| `.sub-keys` | 671 | KEEP |
| `/* Desktop exposes each choice's disclosure control. */ #your-move .inline-choices .chev-btn` | 673 | KEEP |
| `#your-move .details-toggle` | 674 | KEEP |
| `#your-move .choice-row .ctitle` | 675 | KEEP |
| `body.mode-off .your-move:not(.has-mode-keeping-choice) .mode-off-hint` | 683 | KEEP |
| `@media (min-width: 768px)` | 687 | KEEP |
| `:root` | 688 | KEEP |
| `/* One centred reading column: the scroller's content box and the composer are the same width inside` | 693 | KEEP |
| `#interaction-form` | 696 | KEEP |
| `.story-md, .your-move, .past-choices, .options-pending, .story-entry > *` | 702 | KEEP |
| `.inline-choices .choice-button` | 705 | KEEP |
| `.toggle-group` | 708 | KEEP |
| `.toggle-group .toggle-pill` | 711 | KEEP |
| `.action-bar .spacer` | 715 | KEEP |
| `/* --- R2a Scroll-Gated Choices Peek Strip --- */ /* The "?" affordance beside each mode pill. Delib` | 725 | KEEP |
| `.toggle-group .toggle-help:hover, .toggle-group .toggle-help:focus-visible` | 739 | KEEP |
| `/* The seam between the LAST choice row and the textarea below: the same hairline divider, plus the ` | 748 | KEEP |
| `.composer-stack--has-choices .composer-stack__input-group #user-input` | 752 | KEEP |
| `#interaction-form .composer-stack__input-group .own-action-label` | 759 | KEEP |
| `/* The textarea is the free-form option. Keep its pencil marker in the same left gutter as the numbe` | 787 | KEEP |
| `.composer-stack--has-choices #user-input::placeholder` | 794 | KEEP |
| `/* The custom-action textarea starts compact and the input handler grows it up to 30% of the visual ` | 800 | KEEP |
| `/* .composer-stack #user-input zeroes the textarea border, so the stack owns the ring. */ .composer-` | 813 | KEEP |
| `#user-input:focus` | 818 | KEEP |
| `/* Fine-pointer devices use the same 57px starting height. The input handler resets this height whil` | 829 | KEEP |
| `#user-input` | 830 | KEEP |
| `.composer-stack #user-input` | 836 | KEEP |
| `/* While a turn runs the textarea is disabled, so Cancel takes its right edge: a full touch target w` | 860 | KEEP |
| `#interaction-form .composer-cancel:hover` | 881 | KEEP |
| `#interaction-form .composer-cancel:focus-visible` | 885 | KEEP |
| `#interaction-form .composer-stack--cancelable #user-input` | 890 | KEEP |
| `it no longer needs a */ /* viewport-conditional override here. Phones still need their own */ /* cho` | 907 | KEEP |
| `.composer-row` | 908 | KEEP |
| `.toggle-group .toggle-pill` | 912 | KEEP |
| `.composer-send` | 917 | KEEP |
| `#your-move .inline-choices .choice-button` | 921 | KEEP |
| `/* Keep the pencil gutter and placeholder readable on narrow screens. */ .composer-stack #user-input` | 930 | KEEP |
| `text-overflow: ellipsis — but that ellipsis only fires when the parent has a defined width AND the s` | 958 | KEEP |
| `.choice-button` | 963 | KEEP |
| `.ctitle` | 969 | KEEP |
| `/* Wide desktop has room to spare, so controls drop the phone touch sizing while staying at least 32` | 980 | KEEP |
| `.toggle-group .toggle-pill` | 981 | KEEP |
| `.composer-send` | 986 | KEEP |
| `.write-own-hint__cta` | 992 | KEEP |
| `.write-own-hint__dismiss` | 997 | KEEP |
| `#your-move .inline-choices .choice-button` | 1001 | KEEP |
| `#your-move .inline-choices .choice-button::before` | 1006 | KEEP |
| `#your-move .inline-choices .cdesc` | 1009 | KEEP |
| `#your-move .inline-choices .chev-btn` | 1012 | KEEP |
| `#user-input` | 1016 | KEEP |
| `.composer-stack #user-input` | 1020 | KEEP |

### `themes/base.css` — 22 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* Core layout and structure - applies CSS variables from default theme */ body` | 2 | KEEP |
| `#story-content` | 7 | KEEP |
| `#loading-overlay` | 13 | KEEP |
| `.navbar` | 17 | KEEP |
| `.navbar-brand, .navbar-text` | 23 | KEEP |
| `.btn-outline-secondary` | 27 | KEEP |
| `.btn-outline-secondary:hover` | 32 | KEEP |
| `.dropdown-menu` | 37 | KEEP |
| `.dropdown-item` | 42 | KEEP |
| `.dropdown-item:hover` | 46 | KEEP |
| `.list-group-item` | 51 | KEEP |
| `.list-group-item:hover` | 57 | KEEP |
| `.modal-content` | 61 | KEEP |
| `.modal-header` | 66 | KEEP |
| `.modal-footer` | 70 | KEEP |
| `#shareStoryModal .input-group .form-control` | 74 | KEEP |
| `#shareStoryModal .share-copy-btn, #shareStoryModal #shareStoryCopyBtn` | 80 | KEEP |
| `.form-control` | 86 | KEEP |
| `.form-control:focus` | 92 | KEEP |
| `.text-muted` | 99 | KEEP |
| `.bg-light` | 103 | KEEP |
| `#story-content .planning-block-header` | 107 | KEEP |

### `themes/default.css` — 1 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* Default Theme - CSS Custom Properties */ :root` | 2 | KEEP |

### `themes/fantasy.css` — 177 rule blocks, file verdict KEEP

| Selector | Line | Verdict |
|---|---|---|
| `/* Fantasy Theme - "Arcane Scholar" palette Deep purple-black backgrounds, frosted-glass surfaces, v` | 4 | KEEP |
| `/* Ember canvas background fallback — canvas draws gradient + particles when JS runs */ #ember-bg-ca` | 122 | KEEP |
| `[data-theme='fantasy'] #ember-bg-canvas` | 133 | KEEP |
| `[data-theme='fantasy'] body` | 137 | KEEP |
| `[data-theme='fantasy'] .navbar` | 142 | KEEP |
| `[data-theme='fantasy'] .modal-content, [data-theme='fantasy'] .card` | 148 | KEEP |
| `/* Logged-out: container is transparent (auth-view handles the bg) */ [data-theme='fantasy'] body.is` | 155 | KEEP |
| `/* Main content container - very light tint so ember canvas shows through clearly */ [data-theme='fa` | 164 | KEEP |
| `/* Story content: transparent so embers drift through the narrative text */ [data-theme='fantasy'] #` | 172 | KEEP |
| `[data-theme='fantasy'] #story-content p, [data-theme='fantasy'] #story-content strong, [data-theme='` | 180 | KEEP |
| `[data-theme='fantasy'] .btn-primary` | 184 | KEEP |
| `[data-theme='fantasy'] .btn-primary:hover` | 190 | KEEP |
| `[data-theme='fantasy'] .form-control` | 195 | KEEP |
| `[data-theme='fantasy'] .form-control:focus` | 201 | KEEP |
| `/* Campaign list items - ensure dark bg and readable text */ [data-theme='fantasy'] .list-group-item` | 207 | KEEP |
| `[data-theme='fantasy'] .list-group-item:hover` | 213 | KEEP |
| `/* Campaign title links - gold accent for readability */ [data-theme='fantasy'] .list-group-item a, ` | 219 | KEEP |
| `/* Timestamps and muted text - ensure visible */ [data-theme='fantasy'] .text-muted, [data-theme='fa` | 225 | KEEP |
| `/* Form select dropdowns and menu items */ [data-theme='fantasy'] .form-select` | 230 | KEEP |
| `[data-theme='fantasy'] .form-select option` | 236 | KEEP |
| `[data-theme='fantasy'] .dropdown-menu` | 241 | KEEP |
| `[data-theme='fantasy'] .dropdown-item` | 246 | KEEP |
| `[data-theme='fantasy'] .dropdown-item:hover, [data-theme='fantasy'] .dropdown-item:focus` | 251 | KEEP |
| `[data-theme='fantasy'] .dropdown-header` | 256 | KEEP |
| `/* Headings */ [data-theme='fantasy'] h2, [data-theme='fantasy'] h3` | 262 | KEEP |
| `/* Structured story fields - dark-theme overrides for hardcoded light backgrounds */ /* !important n` | 268 | KEEP |
| `[data-theme='fantasy'] .dice-rolls` | 274 | KEEP |
| `[data-theme='fantasy'] .resources` | 280 | KEEP |
| `/* Legacy choice states keep their established specificity. */ [data-theme='fantasy'] .choice-button` | 287 | KEEP |
| `[data-theme='fantasy'] .choice-button:hover` | 293 | KEEP |
| `[data-theme='fantasy'] .choice-button:active` | 298 | KEEP |
| `[data-theme='fantasy'] .choice-button:disabled` | 302 | KEEP |
| `[data-theme='fantasy'] .choice-button-custom` | 309 | KEEP |
| `[data-theme='fantasy'] .choice-button-custom:hover` | 314 | KEEP |
| `[data-theme='fantasy'] .choice-id` | 318 | KEEP |
| `[data-theme='fantasy'] .choice-description` | 322 | KEEP |
| `[data-theme='fantasy'] .system-warnings` | 326 | KEEP |
| `[data-theme='fantasy'] .living-world-updates` | 334 | KEEP |
| `[data-theme='fantasy'] .living-world-scene, [data-theme='fantasy'] .living-world-complication` | 341 | KEEP |
| `[data-theme='fantasy'] .entities-mentioned` | 346 | KEEP |
| `[data-theme='fantasy'] .location-confirmed` | 352 | KEEP |
| `[data-theme='fantasy'] .god-mode-response` | 358 | KEEP |
| `[data-theme='fantasy'] .dm-notes` | 364 | KEEP |
| `[data-theme='fantasy'] .state-rationale` | 370 | KEEP |
| `[data-theme='fantasy'] .state-updates` | 376 | KEEP |
| `[data-theme='fantasy'] .debug-info` | 382 | KEEP |
| `[data-theme='fantasy'] .debug-content` | 388 | KEEP |
| `[data-theme='fantasy'] .debug-rolls` | 393 | KEEP |
| `[data-theme='fantasy'] .planning-block-error` | 399 | KEEP |
| `[data-theme='fantasy'] .planning-block-error pre` | 405 | KEEP |
| `/* Character info - even row background */ [data-theme='fantasy'] #game-view .info-table tbody tr:nt` | 411 | KEEP |
| `/* Story entry separators */ [data-theme='fantasy'] .story-entry` | 416 | KEEP |
| `/* Login - transparent so ember canvas shows through */ [data-theme='fantasy'] body.is-logged-out #a` | 421 | KEEP |
| `[data-theme='fantasy'] body.is-logged-out` | 425 | KEEP |
| `/* Card: frosted glass over the dragon background */ [data-theme='fantasy'] .welcome-card` | 430 | KEEP |
| `[data-theme='fantasy'] .welcome-auth-shell` | 435 | KEEP |
| `[data-theme='fantasy'] .welcome-auth-title` | 445 | KEEP |
| `[data-theme='fantasy'] .welcome-auth-subtitle` | 449 | KEEP |
| `[data-theme='fantasy'] .welcome-auth-card` | 453 | KEEP |
| `[data-theme='fantasy'] .welcome-auth-card-title` | 459 | KEEP |
| `[data-theme='fantasy'] .welcome-auth-card-text` | 463 | KEEP |
| `/* White Google button per new styleguide — matches Google brand guidelines */ [data-theme='fantasy'` | 468 | KEEP |
| `[data-theme='fantasy'] .welcome-google-btn:hover, [data-theme='fantasy'] .welcome-google-btn:focus` | 476 | KEEP |
| `[data-theme='fantasy'] .welcome-splash-copy h3` | 483 | KEEP |
| `[data-theme='fantasy'] .welcome-splash-copy p` | 487 | KEEP |
| `/* Standalone settings route (server template) */ [data-theme='fantasy'] main.container-fluid` | 492 | KEEP |
| `[data-theme='fantasy'] main.container-fluid>.container` | 497 | KEEP |
| `[data-theme='fantasy'] main.container-fluid>.container .card, [data-theme='fantasy'] main.container-` | 508 | KEEP |
| `/* Campaign wizard visual alignment (no layout change) */ [data-theme='fantasy'] .wizard-progress .p` | 513 | KEEP |
| `[data-theme='fantasy'] .step-circle` | 517 | KEEP |
| `[data-theme='fantasy'] .step-indicator.active .step-circle` | 523 | KEEP |
| `[data-theme='fantasy'] .step-indicator.active .step-label` | 530 | KEEP |
| `[data-theme='fantasy'] .step-indicator.completed .step-circle` | 535 | KEEP |
| `[data-theme='fantasy'] .step-indicator.completed .step-label` | 541 | KEEP |
| `[data-theme='fantasy'] .step-indicator:hover .step-circle` | 545 | KEEP |
| `/* Gap fix: "Begin Adventure" btn-success → purple primary */ [data-theme='fantasy'] .btn-success, [` | 552 | KEEP |
| `[data-theme='fantasy'] .btn-success:hover` | 557 | KEEP |
| `/* Gap fix: alert-danger dark-themed instead of light pink */ [data-theme='fantasy'] .alert-danger` | 563 | KEEP |
| `[data-theme='fantasy'] .alert-danger strong, [data-theme='fantasy'] .alert-danger b` | 569 | KEEP |
| `/* Gap fix: toast notification dark-themed */ [data-theme='fantasy'] .toast` | 574 | KEEP |
| `[data-theme='fantasy'] .toast-header` | 579 | KEEP |
| `[data-theme='fantasy'] .toast-body` | 584 | KEEP |
| `[data-theme='fantasy'] .step-label, [data-theme='fantasy'] .step-title, [data-theme='fantasy'] .step` | 595 | KEEP |
| `[data-theme='fantasy'] .campaign-type-card` | 599 | KEEP |
| `[data-theme='fantasy'] .campaign-type-card.selected` | 604 | KEEP |
| `[data-theme='fantasy'] .campaign-wizard .form-control, [data-theme='fantasy'] .campaign-wizard .form` | 610 | KEEP |
| `[data-theme='fantasy'] .campaign-wizard .form-control::placeholder, [data-theme='fantasy'] .campaign` | 617 | KEEP |
| `/* Dashboard search/filter panel -- interactive-features.css loads AFTER themes, so these hardcoded ` | 624 | KEEP |
| `[data-theme='fantasy'] .search-box .form-control` | 630 | KEEP |
| `[data-theme='fantasy'] .search-box .form-control::placeholder` | 636 | KEEP |
| `[data-theme='fantasy'] .search-box .form-control:focus` | 640 | KEEP |
| `[data-theme='fantasy'] .filter-select` | 645 | KEEP |
| `[data-theme='fantasy'] .filter-select:focus` | 651 | KEEP |
| `[data-theme='fantasy'] .filter-group label` | 656 | KEEP |
| `[data-theme='fantasy'] .search-stats` | 660 | KEEP |
| `/* Campaign list items — transparent so embers show through */ [data-theme='fantasy'] .modern-mode .` | 666 | KEEP |
| `[data-theme='fantasy'] .campaign-item h5, [data-theme='fantasy'] .campaign-item .campaign-title` | 672 | KEEP |
| `[data-theme='fantasy'] .campaign-item small, [data-theme='fantasy'] .campaign-item .text-muted` | 677 | KEEP |
| `[data-theme='fantasy'] .modern-mode .campaign-item:hover, [data-theme='fantasy'] .campaign-item:hove` | 683 | KEEP |
| `/* Campaign tags */ [data-theme='fantasy'] .campaign-tag` | 689 | KEEP |
| `/* Campaign meta text */ [data-theme='fantasy'] .campaign-meta` | 695 | KEEP |
| `/* Form-select (Bootstrap default) — white bg needs dark override */ [data-theme='fantasy'] .form-se` | 700 | KEEP |
| `/* planning-blocks.css loads AFTER themes — override hardcoded light colors */ [data-theme='fantasy'` | 707 | KEEP |
| `[data-theme='fantasy'] .rewards-box` | 713 | KEEP |
| `[data-theme='fantasy'] .rewards-box strong` | 719 | KEEP |
| `[data-theme='fantasy'] .equipment-display` | 723 | KEEP |
| `/* --- Dashboard campaign active state: matches choice-button hover in planning blocks --- */ [data-` | 730 | KEEP |
| `/* --- Campaign wizard: dark surface + light text --- */ [data-theme='fantasy'] .campaign-wizard` | 737 | KEEP |
| `[data-theme='fantasy'] .campaign-preview` | 742 | KEEP |
| `[data-theme='fantasy'] .campaign-preview .card-title` | 747 | KEEP |
| `[data-theme='fantasy'] .preview-item strong` | 751 | KEEP |
| `[data-theme='fantasy'] .preview-value` | 755 | KEEP |
| `[data-theme='fantasy'] .step-title` | 759 | KEEP |
| `[data-theme='fantasy'] .step-description` | 763 | KEEP |
| `/* (consolidated into wizard section above) */ [data-theme='fantasy'] .step-label` | 769 | KEEP |
| `[data-theme='fantasy'] .step-counter` | 773 | KEEP |
| `[data-theme='fantasy'] .wizard-navigation` | 777 | KEEP |
| `/* Wizard personality/option cards */ [data-theme='fantasy'] .personality-card .card-title, [data-th` | 784 | KEEP |
| `[data-theme='fantasy'] .personality-card .card-text, [data-theme='fantasy'] .option-card .card-text,` | 790 | KEEP |
| `[data-theme='fantasy'] .personality-card .form-check-label, [data-theme='fantasy'] .option-card .for` | 795 | KEEP |
| `[data-theme='fantasy'] .campaign-type-card` | 799 | KEEP |
| `[data-theme='fantasy'] .campaign-type-card.selected` | 804 | KEEP |
| `[data-theme='fantasy'] .personality-card, [data-theme='fantasy'] .option-card` | 810 | KEEP |
| `[data-theme='fantasy'] .search-filter-container` | 814 | KEEP |
| `[data-theme='fantasy'] .filter-group label` | 819 | KEEP |
| `[data-theme='fantasy'] .preview-item` | 823 | KEEP |
| `[data-theme='fantasy'] .editable-preview:hover` | 827 | KEEP |
| `[data-theme='fantasy'] .editable-preview.editing` | 831 | KEEP |
| `[data-theme='fantasy'] .planning-block-error` | 836 | KEEP |
| `[data-theme='fantasy'] .planning-block-error pre` | 842 | KEEP |
| `/* Accessibility: solid fallbacks when reduced transparency is requested */ @media (prefers-reduced-` | 849 | KEEP |
| `[data-theme='fantasy'] .welcome-auth-shell` | 850 | KEEP |
| `[data-theme='fantasy'] .welcome-auth-card` | 855 | KEEP |
| `[data-theme='fantasy'] .modal-content, [data-theme='fantasy'] .card` | 861 | KEEP |
| `[data-theme='fantasy'] .container.mt-4` | 866 | KEEP |
| `[data-theme='fantasy'] main.container-fluid>.container` | 871 | KEEP |
| `/* ── Universal Modal Styling (fantasy theme) ─────────────────────────────── */ /* Solid dark backg` | 880 | KEEP |
| `[data-theme='fantasy'] .modal-header` | 889 | KEEP |
| `[data-theme='fantasy'] .modal-header .modal-title` | 895 | KEEP |
| `[data-theme='fantasy'] .modal-header .modal-title i` | 903 | KEEP |
| `[data-theme='fantasy'] .modal-header .btn-close` | 907 | KEEP |
| `[data-theme='fantasy'] .modal-header .btn-close:hover` | 913 | KEEP |
| `[data-theme='fantasy'] .modal-body` | 917 | KEEP |
| `[data-theme='fantasy'] .modal-body p.text-muted, [data-theme='fantasy'] .modal-body .text-muted` | 924 | KEEP |
| `[data-theme='fantasy'] .modal-body .form-label` | 928 | KEEP |
| `[data-theme='fantasy'] .modal-body .form-control` | 935 | KEEP |
| `[data-theme='fantasy'] .modal-body .form-control:focus` | 944 | KEEP |
| `[data-theme='fantasy'] .modal-body .form-control[readonly]` | 952 | KEEP |
| `[data-theme='fantasy'] .modal-footer` | 959 | KEEP |
| `[data-theme='fantasy'] .modal-footer .btn-secondary` | 965 | KEEP |
| `[data-theme='fantasy'] .modal-footer .btn-secondary:hover` | 974 | KEEP |
| `/* ── Share Story Modal (fantasy theme) ───────────────────────────────────── */ [data-theme='fantas` | 981 | KEEP |
| `[data-theme='fantasy'] #shareStoryModal .input-group .form-control` | 986 | KEEP |
| `[data-theme='fantasy'] #shareStoryModal .share-copy-btn, [data-theme='fantasy'] #shareStoryModal #sh` | 993 | KEEP |
| `[data-theme='fantasy'] #shareStoryModal .share-copy-btn:hover, [data-theme='fantasy'] #shareStoryMod` | 1008 | KEEP |
| `[data-theme='fantasy'] #shareStoryAccessCount` | 1014 | KEEP |
| `[data-theme='fantasy'] #shareStoryAccessCount i` | 1022 | KEEP |
| `[data-theme='fantasy'] #shareStoryAccessCountValue` | 1026 | KEEP |
| `[data-theme='fantasy'] #shareStoryLegacyNotice` | 1031 | KEEP |
| `[data-theme='fantasy'] #shareStoryLegacyNotice i` | 1038 | KEEP |
| `/* ── Duplicate Campaign Modal (fantasy theme) ─────────────────────────────── */ /* Solid dark bg f` | 1046 | KEEP |
| `[data-theme='fantasy'] #duplicate-campaign-modal .modal-title, [data-theme='fantasy'] #duplicate-cam` | 1053 | KEEP |
| `/* ── Rate Limit Modal (fantasy theme) ────────────────────────────────────── */ [data-theme='fantas` | 1061 | KEEP |
| `[data-theme='fantasy'] .rate-limit-modal-title` | 1066 | KEEP |
| `[data-theme='fantasy'] .rate-limit-modal-subtitle` | 1070 | KEEP |
| `[data-theme='fantasy'] .rate-limit-message` | 1074 | KEEP |
| `[data-theme='fantasy'] .rate-limit-timer` | 1078 | KEEP |
| `[data-theme='fantasy'] .rate-limit-timer-icon` | 1083 | KEEP |
| `[data-theme='fantasy'] .rate-limit-byok-hint` | 1085 | KEEP |
| `[data-theme='fantasy'] .rate-limit-key-icon` | 1090 | KEEP |
| `[data-theme='fantasy'] .rate-limit-byok-title` | 1092 | KEEP |
| `[data-theme='fantasy'] .rate-limit-byok-desc` | 1094 | KEEP |
| `[data-theme='fantasy'] .rate-limit-settings-btn` | 1096 | KEEP |
| `[data-theme='fantasy'] .rate-limit-settings-btn:hover, [data-theme='fantasy'] .rate-limit-settings-b` | 1102 | KEEP |
| `[data-theme='fantasy'] .rate-limit-icon-badge` | 1107 | KEEP |
| `[data-theme='fantasy'] .rate-limit-close-secondary` | 1111 | KEEP |
| `/* Close (×) button: invert for dark fantasy background */ [data-theme='fantasy'] .rate-limit-close-` | 1118 | KEEP |

CSS rule-block total: 1518.

---

## Per-file tables — HTML (by template/script section)

### `index.html` (718 lines) — KEEP, all sections

Lens A: the shipped entry point; every section below is rendered or referenced by app.js. Lens B: the head comment at index.html:648–652 (share modal placed INSIDE body, PR #5823 regression guard) is accurate — the modal is at lines 653+ before `</body>` at line 716. The Mastodon `<link rel="me">` comment (lines 8–10) is accurate.

| Section | Lines | Verdict | Note |
|---|---|---|---|
| `<head>`: meta, title, favicon (line 7), Mastodon identity link (line 11) | 1–15 | KEEP | Static head; Mastodon link is live profile metadata, not a game claim. |
| Stylesheets: tooltip-guide (16), Bootstrap + icons CDN (29–30), style.css (31), themes default/fantasy/base (34–36), loading-messages (40), planning-blocks (41), inline-editor (42), avatar (43), async-print sheets (46–50) + non-async duplicates (52–56) | 16–56 | KEEP | Duplicated async/non-async link pairs are intentional print-media async loading with a fallback; presentation only. |
| Agent-readable summary (`#agent-readable-summary`, hidden) | 68 | KEEP | Hidden summary + `/llms.txt` link (line 78) is agent-facing documentation, not player gameplay; accurate. |
| Navbar (brand, wiki/Reddit/Discord links, theme switcher, user menu) | 86–168 | KEEP | ui-utils.js hydrates the wiki/social anchors (otherwise `href="#"`); links match ui-utils.js constants. |
| Loading overlay | 169–178 | KEEP | Wait-state presentation. |
| `main-content` / `auth-view` (logged-out/welcome) | 179–182 | KEEP | Entry view. |
| `dashboard-view` / `campaign-list` (incl. `data-tooltip-id` targets) | 183–225 | KEEP | Campaign list rendered by app.js. |
| `new-campaign-view` / `new-campaign-form` (wizard host) | 226–340 | KEEP | Wizard host rendered by campaign-wizard.js. |
| `game-view` (first-run banner, header avatar slot, HUD subline, BYOK CTA, HUD menu, `story-content`, stream status, timer info, `interaction-form`, first-turn coach note, composer stack, pending status, spinner) | 341–505 | KEEP | Core play surface. |
| Download options modal | 506–545 | KEEP | Export UI (downloadSingleFormat/downloadFile in app.js). |
| Campaign details modal | 546–568 | KEEP | Detail UI. |
| Cancel-pending modal | 569–596 | KEEP | Cancel confirmation UI. |
| Avatar overlay | 597–615 | KEEP | Avatar display overlay. |
| Body scripts: Bootstrap/marked/dompurify/Firebase CDN (616–620), diagnostics (624), user_lifecycle (625), auth (626), api (627), interface-manager (629), theme-manager (630), animation-helpers (631), ui-utils (632), avatar-crop (633), portrait-ai-ui (634), portrait-ai (635), campaign-wizard (636), enhanced-search (637), scene-illustration (638), streaming (639), opening_story (640), loading-messages (641), inline-editor (642), ember-bg (643), quick_start_shared (644), outcome-verdict (645), app.js (646) | 616–646 | KEEP | The load manifest. NOTE: settings.js has NO static tag here — it loads dynamically via app.js:2576–2583 only. component-enhancer.js, visual-validator.js, test_planning_block_parsing.js, parallel_dual_pass.js have no tag here (DELETE evidence). |
| Share story modal (normal + legacy confirm sections) | 653–715 | KEEP | Share UI; legacy-confirm section matches share-token prefill handling in app.js/campaign-wizard.js. |
| worldai-mcp-bridge (714) + tooltip-guide (715) | 714–715 | KEEP | Tooltip transport + guide; both stripped/404'd by the main.py tooltip kill switch when disabled (main.py:1947–2023). |
| Footer/legal area + `</body>`/`</html>` | 716–718 | KEEP | No separate footer element; legal links live in the agent-readable summary (line 78: /about, /privacy, /contact) and in terms-of-use.html. |

### `terms-of-use.html` (71 lines) — KEEP, all sections

Lens A: static legal page, no scripts, no domain logic. Lens B (stale product claims only, not legal correctness): the named URLs and features were checked against the tree. `/contact` and `/privacy` exist as server-rendered pages (main.py:8950–9087); the server content-report endpoint exists (main.py:~8302, "Record a user report of objectionable AI/user-generated content"), supporting §19's "in-app Report action" at the server level, though no Report control was located in frontend_v1 JS by grep in this pass — flagged as an unverified-from-frontend note, NOT a stale claim and NOT a verdict change. §3 ("you are not a minor in your jurisdiction") vs §20 ("intended for users aged 17 and older") is an internal wording tension to reconcile — flagged in §3, not a verdict change. "Last updated October 14, 2026" is a date claim inside the document itself; no contradicting tree evidence was checked. No pricing, feature, or product name in the document was found to be nonexistent: "WorldAI"/"WorldArchitect.AI"/"Lee-Chan Consulting D/B/A WorldAI" match main.py:9055 and the terms header; the iOS-app sentence in §19 is a platform claim outside this area's tree evidence and is NOT verified here.

| Section | Verdict |
|---|---|
| Header/brand + "How to start" framing (the file carries a duplicated `<h1>` brand block, cosmetic only — run 2 noted) | KEEP |
| §§1–21 (services, IP, representations, prohibited activities, contributions, contribution licence incl. training/fine-tuning use + objection via /contact, services management, term/termination, modifications, governing law, dispute resolution, corrections, disclaimer, liability limit, indemnification, user data + /privacy, electronic communications, miscellaneous, prohibited content + Report action, age 17+) | KEEP |
| Contact block (§21) + Back to Home link | KEEP |

### `mocks/mock_header_avatar_and_scroll_gate.html` (359 lines) — DELETE

Lens A: standalone dev mock; no shipped page links to it; the real header ships in index.html/app.js. Lens B: title (line 6) says "Mockup: Header Hero Avatar (3x) + R2a Scroll-Gated Choices" — accurate as a mock label. CORRECTION to run 2's file table (which did not mention its JS): the mock DOES contain script — `toggleDesktopChoices()` (line 334, wired by onclick at line 221) plus an anonymous scroll auto-reveal listener (scroll ≥90% expands, <55% collapses). Both are mock-only presentation; verdict unchanged. Additional stale detail: the mock links `../styles/style.css` (line 9), which does not exist (style.css lives at frontend_v1/style.css, not frontend_v1/styles/style.css) — the mock's own stylesheet reference is broken, further evidence it is not a maintained surface.

| Section | Verdict |
|---|---|
| Head + Bootstrap/icons CDN + (broken) `../styles/style.css` + planning-blocks/avatar CSS + inline `<style>` | DELETE with file |
| Desktop mock markup: header avatar (3x), story box `#desktopStory`, choices container, peek strip, composer stack | DELETE with file |
| Inline script: `toggleDesktopChoices()` + scroll auto-reveal listener | DELETE with file |

### Other non-code frontend files — KEEP/ADAPT as in run 2 (confirmed)

| File | Verdict | Note |
|---|---|---|
| `.gitignore` | KEEP | Repo hygiene, non-runtime. |
| `README.md` | KEEP (docs stale — see §3) | Developer doc; stale in the ways listed in §3. File verdict stays KEEP because docs are not code; the stale items are corrections, not deletions. |
| `dragon-favicon.svg` | KEEP | Tab icon, referenced index.html:7. |
| `images/twin_dragon.webp` | KEEP | Brand hero art. |
| `images/twin_dragon.png` (2.5 MB) | ADAPT | Duplicate of the 105 KB WebP; serve WebP only (run 2 confirmed; no new evidence either way). |
| `images/avatars/arion_dragon_knight.png` | KEEP | Default Dragon Knight premade avatar. |

---

## Per-file tables — Python (one row per symbol; full reviews)

Conventions: "KEEP (file ADAPT)" as in JS tables. Module-level constants are verdict-ed with the symbol group that owns them. Callers were checked by grep over `mvp_site/*.py` (production) plus tests noted separately where relevant.

### `scene_attempts.py` (59 lines) — file verdict KEEP

Pass A: without newest-attempt-wins, a stale poll or aborted turn could overwrite a newer scene image — a visible wrong-image/retry bug. Pass B: idempotency/ordering guards over durable writes are storage integrity, not domain recomputation; no model-authored value is rewritten, only which write wins. No run-2 verdict to confirm (fresh).

| Symbol | Line | Verdict | Justification (A then B) |
|---|---|---|---|
| `TERMINAL` (frozenset ready/failed/disabled) | 15 | KEEP | Terminal-state vocabulary for the guard below; storage data, not a domain fact. |
| `_ts` | 21 | KEEP | ISO-timestamp parsing with fail-None; pure parsing, never invents a time. |
| `same_attempt` | 31 | KEEP | Key-then-timestamp identity; legacy fallback (unstamped rows count as same attempt) is conservative — it refuses to overwrite rather than inventing order. Callers: scene_illustration_service.py (`_status_from_doc`), scene_illustration_worker paths via service. |
| `is_newer` | 42 | KEEP | Timestamp ordering; stamped displaces unstamped, unstamped never displaces stamped — storage ordering only. |
| `write_allowed` | 51 | KEEP | The guard itself: terminal never reverts to pending, stalled never downgrades terminal. Used by firestore upsert paths; storage integrity, KEEP. |

### `scene_illustration_flag.py` (217 lines) — file verdict KEEP

Pass A: without the per-environment flag, scene generation could not be gated per deployment; generation would run (and bill) where it should not. Pass B: environment authorization + bounded reads (2s timeout, no retry, short-TTL cache) are authorization/bounded-capacity categories. Fail-closed throughout. No run-2 verdict (fresh).

| Symbol | Line | Verdict | Justification |
|---|---|---|---|
| `SCENE_ILLUSTRATION_ENVIRONMENTS`, `PRODUCTION_ENVIRONMENTS`, `_COLLECTION`, `_DOCUMENT`, `_CADENCE_DOCUMENT`, `_DEFAULT_CACHE_TTL_SECONDS`, `_READ_TIMEOUT_SECONDS`, `_CACHE_SENTINEL` | 24–34 | KEEP | Flag contract + bounds; config data, not domain logic. |
| `_Cache` / `__init__` / `clear` | 37–44 | KEEP | Thread-safe short-TTL cache cell; transport plumbing. |
| `_cache`, `_cadence_cache` (module instances) | 46–47 | KEEP | One cache per document; in-process only, no cross-instance claim. |
| `clear_cache` | 53 | KEEP | Test/reset hook; clearing a cache cannot change a gameplay fact. |
| `SceneIllustrationFlagState` (ON/OFF/UNKNOWN) | 59 | KEEP | Distinguishes deliberate OFF from unreadable — the distinction the fail-closed design needs. |
| `_deny` | 67 | KEEP | Logs + returns OFF; never invents ON. |
| `_get_config_data` | 73 | KEEP | Bounded Firestore read (2s, retry=None) through the shared cache; returns (data, success) so callers can tell UNKNOWN from OFF. |
| `_get_flag_data` | 113 | KEEP | Thin wrapper binding the enable document to its cache. |
| `scene_illustration_flag_state_for_environment` | 122 | KEEP | Prod/unknown environments deny before any read; non-boolean/missing fields deny; read failure returns UNKNOWN (not OFF) — exactly the fail-closed contract its docstring states. Docstring accurate (verified against body). |
| `scene_illustrations_allowed_for_environment` | 157 | KEEP | ON-only gate; default cached=True suits the story path because disablement propagates within TTL. Callers: service retry + maybe_start paths. |
| `scene_illustrations_cadence_config` | 173 | KEEP | Global cadence + revision token; out-of-range values fall back to default rather than clamping a domain value — the value is admin policy, not model-authored state. |
| `scene_illustrations_default_cadence_every_n` | 211 | KEEP | Convenience projection of the above; default 3 per constants. |

### `scene_illustration_policy.py` (654 lines) — file verdict KEEP, one ADAPT symbol

Pass A: without eligibility/cadence/prompt construction, scene images would generate on every scene (unbounded image cost) or with unstructured prompts (wrong-character images, the s9 "Misa" bug the presence rules fix). Pass B: eligibility is product policy for invoking an image tool (when to pay for an image), not a recomputation of campaign facts; prompt assembly from stored entries + the current GM response is prompt assembly; the presence rules are prompt text. No run-2 verdict (fresh). One ADAPT: the legacy prompt builder is a debug baseline kept for ablation only.

| Symbol | Line | Verdict | Justification |
|---|---|---|---|
| `load_scene_illustration_policy` (+ `_POLICY_PATH`, `_POLICY_CACHE`) | 23 | KEEP | Loads `schemas/scene_illustration_policy.json` once, deep-copies per call; policy data loading, not domain logic. |
| `predict_next_user_scene_number` | 30 | KEEP | Counts GM-actor entries + 1; counting stored entries for cadence is policy arithmetic, not authoring a scene. |
| `is_cadence_scene` | 42 | KEEP | Every-Nth GM scene gate with minimum; cadence/minimum from policy or explicit N; cadence < 1 disables. Pure policy gate. |
| `resolve_scene_illustrations_every_n` | 65 | KEEP | Global cadence unless a saved admin override carries the current revision tag; untagged legacy values resolve to global default. Revision-tagged migration, not a domain rewrite. |
| `resolve_scene_illustrations_mode` | 92 | KEEP | Canonicalizes legacy modes: `parallel` → `after_scene`, legacy boolean enabled → after_scene/off. Matches the frontend settings normalizer (settings.js:803–814 maps parallel → after_scene), so client and server agree. Legacy migration, KEEP. |
| `effective_scene_illustration_settings` | 111 | KEEP | Non-admins cannot set admin-only context depth/style keys; authorization scoping of preferences. |
| `normalize_scene_illustrations_settings` | 126 | KEEP | Read-time migration exposing canonical mode/every_n/depth/style on settings payloads; derives only from the settings themselves. |
| `scene_illustrations_enabled` | 139 | KEEP | Campaign opt-out (explicit False) + user mode OFF gate; both are explicit preference signals, not inference. |
| `_gm_scene_count`, `_entry_actor` | 155, 164 | KEEP | Small stored-entry helpers for the CC logic below. |
| `_last_gm_followed_cc_exit` | 168 | KEEP | Structural scan (latest GM entry followed by a user entry) for first-story-scene detection; actor/position logic, no text inference. |
| `_is_cc_exit_user_entry` | 190 | KEEP | Explicit-signal check via `get_character_creation_exit_choice_id` over stored text/choice_id fields — explicit signals only, consistent with the modal-conclude rule. |
| `_story_has_post_cc_scene_illustration` | 202 | KEEP | Guards the "first real story scene gets one image" rule against repeats across CC cycles; reads stored illustration snapshots only. |
| `is_character_creation_completion_illustration` | 227 | KEEP | Requires server-accepted CC state (completed flag + stage == complete + no in-progress/active) AND an explicit exit choice id. Explicit-signal + stored-state gate, KEEP. |
| `is_character_creation_completion_candidate` | 248 | KEEP | Weaker pre-check (active CC + exit choice id) for preparation; same explicit-signal basis. |
| `is_first_story_scene_illustration` | 267 | KEEP | First-playable-beat rule with the CC-wrap-up exclusion and exactly-once guard; structural/state logic, no prose inference. |
| `should_illustrate_user_scene` | 313 | KEEP | Disjunction of cadence / CC-completion / first-scene gates; the single eligibility entry point used by service + retry. |
| `_strip_text` | 336 | KEEP | Whitespace collapse + length cap for prompt assembly; truncation, never rewriting. |
| `_is_god_mode_entry` | 341 | KEEP | God-mode detection: stored mode field, `god_mode_response` flag, else `constants.is_god_mode(text, None)` (the GOD MODE: prefix rule per repo house rules). Used only to EXCLUDE god-mode turns from image-prompt context — prompt assembly filtering, KEEP. Note: this is text classification, but its effect is context selection for an image prompt, not intent routing or a gameplay decision. |
| `filter_scene_context_entries` | 351 | KEEP | Drops god-mode turns and non-player/GM (system/meta) entries from prompt context; prompt assembly, KEEP. |
| `_recent_story_excerpt` | 380 | KEEP | Last-5 labeled Player/GM lines, truncated; verbatim excerpting for prompt context. |
| `resolve_scene_context_settings` | 398 | KEEP | Depth/style validation against constants allowlists; invalid values fall back to defaults. Policy validation, KEEP. |
| `build_scene_brief_messages` (+ `_BRIEF_SYSTEM_INSTRUCTION`) | 425 | KEEP | Prompt assembly for the brief LLM from excerpts + action + narrative; template formatting only. |
| `generate_scene_brief` | 443 | KEEP | Cheap text-LLM brief on the background thread only, fail-soft (returns fallback reason, never raises); the brief is model-authored text used as prompt context, and failure falls back to raw excerpts. Bounded (8s default, 300 max tokens). KEEP. |
| Presence/section prompt constants (`SCENE_PRESENCE_RULE_*`, `SCENE_SECTION_*`, `AFTER_SCENE_RAW_CONTEXT_ENTRIES`) | 535–548 | KEEP | Prompt text loaded from prompt files + the raw-background cap (2); prompt data, not code decisions. |
| `build_scene_image_prompt` | 551 | KEEP | CURRENT SCENE / BACKGROUND prompt assembly with the presence rule and portrait; only characters present in CURRENT SCENE may be painted (prompt instruction, enforced by the image model, not by server filtering of facts). The after_scene raw cap (2) vs full depth for debug ablation is explicit and documented. KEEP. |
| `build_legacy_scene_image_prompt` | 615 | ADAPT | Byte-for-byte pre-fix (c489e68) prompt, used ONLY as the ablation baseline via `_reconstruct_prompts`. It is debug-baseline code in the production module: ADAPT — move it into the ablation module (or a debug-only module) so the production prompt path carries one builder; keep it alive only while ablation uses it. Docstring is accurate ("debug ablation baseline only"). |

### `scene_illustration_provider.py` (124 lines) — file verdict KEEP

Pass A: without it, no scene image transport exists (payload + OpenRouter POST + timeouts). Pass B: provider payload construction + bounded timeouts are tool execution. No run-2 verdict (fresh).

| Symbol | Line | Verdict | Justification |
|---|---|---|---|
| `scene_image_http_timeout_seconds` | 18 | KEEP | Timeout from policy (default 90s); bounded capacity. |
| `scene_server_worst_case_seconds` | 26 | KEEP | Brief + HTTP + upload budget; the bound clients/retries wait against. Arithmetic over policy bounds, KEEP. |
| `SCENE_UPLOAD_BUDGET_SECONDS` (15.0) | 35 | KEEP | Upload budget constant feeding the worst case. |
| `retry_join_timeout_seconds` | 40 | KEEP | Worst case + 5s; blocking-retry bound (retry endpoint only, not the turn path). |
| `openrouter_scene_image_payload` | 45 | KEEP | Builds the image payload: policy model/quality/resolution/aspect ratio, provider prefs/trimming, optional portrait reference. Provider transport; debug model/resolution overrides are explicit parameters, not silent defaults. |
| `generate_scene_image_openrouter` | 95 | KEEP | Thin transport wrapper over avatar_image_gen's POST with the scene timeout + optional forensics logging. Tool execution, KEEP. |

### `scene_illustration_service.py` (609 lines) — file verdict KEEP

Pass A: without kickoff/retry/status orchestration, scene images could never start, retry, or be polled; the client slot UI would have nothing to poll. Pass B: orchestration of tool execution + durable writes + bounded capacity (wait executor, per-user poll slots, stale-pending heal). The retry join is blocking but lives on the retry endpoint, not the story turn path; status long-polls are capped (25s) and per-user capped (4). No run-2 verdict (fresh). Callers: main.py routes (status 5042, retry 5084), llm_parser.py, worker.

| Symbol | Line | Verdict | Justification |
|---|---|---|---|
| `SCENE_WAIT_MAX_WORKERS` (32), `SCENE_WAIT_PER_USER` (4), `_SCENE_WAIT_EXECUTOR`, `_SCENE_WAIT_LOCK`, `_USER_WAIT_SLOTS` | 30–36 | KEEP | Bounded wait pool + per-user slots; bounded capacity, explicit env overrides. |
| `scene_wait_executor` | 37 | KEEP | Lazy singleton wait executor; transport plumbing. |
| `try_acquire_user_wait_slot` / `release_user_wait_slot` | 50, 59 | KEEP | Per-user held-poll accounting; extra polls answer immediately (wait=0) instead of queueing — bounded capacity. |
| `get_scene_illustration_status_bounded` | 68 | KEEP | Applies the slot cap, then delegates; the bounded entry point main.py uses. |
| `SCENE_PENDING_STALE_SECONDS` (180), `SCENE_LONG_POLL_MAX_SECONDS` (25.0) | 82–83 | KEEP | Staleness/long-poll bounds. |
| `_story_context_through_scene` | 85 | KEEP | Truncates stored context at the target GM scene; verbatim slicing, no rewriting. |
| `_user_input_for_scene` | 103 | KEEP | Recovers the player message that triggered a GM scene from stored entries; pass-through of stored text. |
| `_scene_has_illustration` | 124 | KEEP | Checks whether a GM entry already carries an illustration dict; stored-state read. |
| `scene_exists` | 138 | KEEP | GM-entry existence check (numbered entries preferred, else count); guards against paying for a nonexistent scene. |
| `_resolve_portrait_reference` | 157 | KEEP | Relative avatar URLs resolved against the share origin; absolute URLs pass through. URL handling, not a domain decision. |
| `retry_scene_illustration` | 168 | KEEP | Full retry: eligibility-as-of-original-turn, no double-pay (live-job join; in-flight-doc report; provider-rejected terminal short-circuit), quota via worker, blocking join bounded by retry_join_timeout_seconds. Long but each branch is a payment/eligibility guard; KEEP. Note: the fallback user_input "Continue the adventure" is used only when the stored input is empty, as prompt input — a documented prompt default, not a gameplay fact. |
| `_portrait_description_from_state` | 306 | KEEP | First non-empty stored field among portrait_description/description/character_description/name. Field selection over stored player data for prompt assembly; the `name` fallback is a stored player field, not an invented description — KEEP, with the note that a bare name yields a weak portrait prompt, which is a quality matter, not a ZFC violation. |
| `prepare_scene_coordinator` | 319 | KEEP | Resolves eligibility + portrait + depth/style onto the worker; the owning-worker preparation step. |
| `maybe_start_scene_coordinator` | 351 | KEEP | Turn-path kickoff: god-mode short-circuit (explicit mode check via `constants.is_god_mode`), enabled + environment gates, deferred preparation for after_scene/CC candidates. Already off the turn path for generation itself (worker thread); KEEP. Note: this is the §6(3)-compatible shape — generation never blocks the turn; only preparation metadata resolves here. |
| `_public_from_doc` | 420 | KEEP | Public projection of a scene doc (ready images only, failed errors only); display shaping of stored state, KEEP. |
| `_status_from_doc` | 437 | KEEP | Attempt-aware doc reading: same attempt → its state; newer attempt → its state; older attempt → None. Storage-identity logic via scene_attempts, KEEP. |
| `_is_stale_pending` | 465 | KEEP | 180s staleness check with fail-False on bad timestamps; never invents staleness. |
| `SCENE_DOC_POLL_INTERVAL_SECONDS` (1.5) | 479 | KEEP | Cross-instance poll interval bound. |
| `get_scene_illustration_status` | 483 | KEEP | Status/long-poll/heal/stale logic: terminal heal copies the doc onto the story entry (guarded by newest-wins), stale pending persists as failed/"stalled" (never downgrading terminal), server-side stall decision (never client-supplied requested_at). Durable-write + bounded-poll orchestration, KEEP. Logging inside is via logging_util (server logging, §6(1) KEEP). |

### `scene_illustration_worker.py` (706 lines) — file verdict KEEP, one minor note (no verdict change)

Pass A: without the background worker, scene images would have to generate on the turn path (blocking the story) or not at all. Pass B: background tool execution + durable writes + quota + attempt ownership; all BQ logging here runs on the background thread, so no §6(1) async ADAPT is outstanding. No run-2 verdict (fresh).

| Symbol | Line | Verdict | Justification |
|---|---|---|---|
| `SceneIllustrationSnapshot` / `to_public_dict` | 31, 42 | KEEP | Attempt snapshot contract + public projection (failure_code/preparing/requested_at only when present). Transport data, KEEP. |
| `_ACTIVE_JOBS`, `_ACTIVE_JOBS_LOCK` | 64–65 | KEEP | In-process live-job registry so long-polls can join the job on this instance; documented Cloud Run CPU rationale in the comment (request-keeps-CPU-allocated). |
| `_job_key` | 69 | KEEP | (user, campaign, scene) registry key. |
| `active_scene_job` | 73 | KEEP | Locked registry read; used by service status/retry. |
| `SceneIllustrationStreamCoordinator` (dataclass + fields) | 81 | KEEP | Job state: inputs, snapshot, thread, commit/preparation events, eligibility. Note: the `timing_mode` default is `SCENE_ILLUSTRATIONS_MODE_PARALLEL`, while the server canonicalizes parallel → after_scene (policy:92) and both construction sites (service retry + maybe_start) pass the resolved mode — the default is therefore misleading but unreachable in production construction; flagged as a minor doc/default note, NOT a verdict change (see §3). |
| `prepares_after_scene` | 117 | KEEP | Deferred-preparation predicate. |
| `set_final_campaign_state` | 120 | KEEP | Uses server-enforced state for CC-completion preparation; only for completion candidates with deferred preparation. |
| `start_preparation` | 130 | KEEP | Starts the prepare thread once, gated on completion-state readiness for CC candidates. |
| `abort_preparation` | 142 | KEEP | Releases commit waiters on generator close/errors/replay/rejected persist. |
| `snapshot_for_turn` | 147 | KEEP | Turn-time snapshot: ineligible prepared jobs return None; unprepared jobs report preparing=True. |
| `_prepare_then_run` | 158 | KEEP | Prepare → wait commit → run/fail/persist-disabled; failure publishes without blocking the turn. |
| `generation_started` | 194 | KEEP | Started predicate. |
| `pending_snapshot` | 197 | KEEP | Pending placeholder persisted before generation starts. |
| `_apply_scene_context_style` | 206 | KEEP | Brief-style swap on the background thread with raw fallback on any brief failure; records depth/style/brief for BQ. Prompt assembly, KEEP. |
| `_publish_failure` | 243 | KEEP | Terminal failure publish + persist, with persist=False for lost-ownership attempts (never mutates the winner's state). Ownership discipline, KEEP. |
| `attempt_tag` | 294 | KEEP | Short hash of key+timestamp for unique blob names (retries never hit a cached old image). |
| `attempt_identity` / `mark_turn_committed` / `_turn_committed` / `turn_committed` | 300, 304, 317, 323 | KEEP | Commit-identity protocol: only the committed attempt's marker applies; after commit, transport teardown no longer aborts the job (the paid image still attaches). Durable-commit semantics, KEEP. |
| `_cancelled` | 327 | KEEP | Cancellation predicate respecting the commit rule above. |
| `_persist_pending_doc` | 335 | KEEP | Pending doc write so any instance can answer polls; best-effort (logs on failure). |
| `start` | 356 | KEEP | Parallel-mode immediate start; after_scene returns (started via start_after_narrative). |
| `start_after_narrative` | 361 | KEEP | After-scene start: sets narrative, releases preparation, sets commit signal (or begins generation directly when not deferred). |
| `_register_generation` | 377 | KEEP | Marks started, publishes pending, registers in _ACTIVE_JOBS (idempotent). |
| `_begin_generation_thread` | 395 | KEEP | Daemon thread start, idempotent. |
| `_publish` | 406 | KEEP | Locked snapshot publish + event queue. |
| `snapshot_for_persist` | 411 | KEEP | Locked snapshot read for persist/poll. |
| `drain_events` | 417 | KEEP | Non-blocking event drain for subscribers. |
| `_run` | 426 | KEEP | Thread wrapper: persist pending → generate → terminal-failed on escape → finish. |
| `_mark` | 444 | KEEP | Stage timing (ms since kickoff) for the SCENE_TIMING log line; measurement only. |
| `_finish_job` | 450 | KEEP | Registry removal (only if self) + SCENE_TIMING log; logging, §6(1) KEEP. |
| `_run_generation` | 468 | KEEP | The generation itself: cancel checks with quota refund before payment, prompt build, no-portrait failure, API-key failure, brief-style swap, provider call with forensics, upload, ready-doc write guarded by newest-wins (losing attempt publishes in-process only, never downgrades the winner), BQ exchange log guarded so it can never downgrade a ready doc, story-entry patch with the same guard, failure path with quota refund only when no image was produced. Each branch is payment/ownership hygiene around one tool call; KEEP. |

### `scene_prompt_ablation.py` (662 lines) — file verdict ADAPT

Pass A: deleting it removes only the debug prompt-ablation experiment (same scene, varied prompts, separate blobs + manifest, nothing written to the scene doc or story entry). Player scene images are unaffected. Pass B: operator experimentation tooling, not player transport/presentation — but it IS admin-gated at the route (main.py:5107–5113, canonical admin claim; prompt_override further restricted to allow-listed admins) and quota-bounded (every image consumes scene quota; MAX_RUNS=2; _max_images_per_request cap). Verdict ADAPT (not DELETE): keep it admin-gated and quota-bounded, but move it out of the shipped request path into debug tooling, or keep the gate and record it as debug-only; the current in-prod-path placement is the adaptation, not the experiment itself. STALE DOC (see §3): the module docstring says "reachable only through the retry endpoint for users whose settings have debug_mode true (the route returns 403 otherwise)" — the route comment states the opposite: "debug_mode is informational, not a gate" (main.py:5108). The code (admin gate) is correct; the docstring is wrong.

| Symbol | Line | Verdict | Justification |
|---|---|---|---|
| `VARIANTS`, `CONTEXT_VARIANTS`, `ALL_VARIANTS`, `PRESETS`, `VARIANT_LETTERS`, `MAX_RUNS` (2) | 46–60 | ADAPT (with file) | Variant vocabulary + bounds for the experiment; move with the file. |
| `_CONTEXT_RE`, `_BRIEF_RE` (regexes) | 62–63 | ADAPT (with file) | Prompt-surgery regexes over PROMPT text (not LLM narrative strings); debug-only string surgery, acceptable in the ablation context. |
| `derive_variant_prompts` | 64 | ADAPT (with file) | Builds the 5 prompt variants from one baseline by string surgery; experiment construction, no player effect. |
| `_strip_companion` (nested in derive_variant_prompts) | 78 | ADAPT (with file) | Removes companion-naming sentences from the character brief for the no_companion variant; debug surgery. |
| `prompt_mentions` | 102 | ADAPT (with file) | Reports where a name appears in a legacy-format prompt (context/brief/action sections); measurement for the experiment. |
| `fetch_logged_scene_prompts` | 117 | ADAPT (with file) | Reads the caller's own campaign's logged scene prompts from BQ (bound params, 14-day window, portrait_source filter); debug provenance, fail-soft. |
| `_scene_pieces` | 197 | ADAPT (with file) | Splits stored story into before/through/user-input/GM-text via service helpers; debug input preparation. |
| `build_context_variant_prompts` | 212 | ADAPT (with file) | Production-builder prompts at each depth/style (brief LLM once per depth unless dry run); reuses the production builder, so variants measure the builder, not a copy. |
| `_reconstruct_prompts` | 276 | ADAPT (with file) | Legacy + structured reconstruction; the legacy builder's only production caller (see policy ADAPT — the two move together). |
| `_log_ablation_image` | 303 | ADAPT (with file) | Per-image BQ row (source=scene_illustration_ablation); debug telemetry, fail-soft. Not player-path logging, so §6(1) does not rescue it as KEEP — it moves with the file. |
| `ABLATION_MODELS` | 333 | ADAPT (with file) | Two-model comparison list (grok-imagine-image-2.0, gemini-nano-banana-2.1); debug model comparison, bounded by the request cap. |
| `_max_images_per_request` | 353 | ADAPT (with file) | Reads the debug-tools policy cap; the bound that keeps the experiment bounded. |
| `_consume_scene_image_quota` | 359 | ADAPT (with file) | Reserves one scene quota unit per image with a refundable key; every ablation image pays quota — the cost control that justifies keeping the experiment at all. |
| `_forensics_kw` | 383 | ADAPT (with file) | Full-exchange forensics only for the real generator (fakes get none); debug observability. |
| `_model_slug` | 398 | ADAPT (with file) | Model-name slug for blob tags. |
| `run_scene_prompt_ablation` | 402 | ADAPT (with file) | The experiment runner: campaign/scene existence, portrait resolution, original-source selection (override > BQ > reconstruction), rate-limit gate for context variants, dry-run short-circuit, quota per image with refund on failure, thread-pool generation capped at _max_images_per_request, manifest result. Bounded and admin-gated; ADAPT (move out of the shipped path) rather than DELETE because the gate + quota + separate-blob design already confines it to operators. |
| `_one` (nested in run_scene_prompt_ablation) | 531 | ADAPT (with file) | Per-variant/run/model generation + upload + logging + refund-on-failure; the unit the cap applies to. |

### `frontend_cutover_flag.py` (153 lines) — file verdict ADAPT — run-2 §4 CONFIRMED

Run-2 §4 verdicts re-verified symbol by symbol against the local file; all CONFIRM. File ADAPT: keep deploy-time only, prove never imported on the player turn path. Callers: main.py:137, 1880 (startup only) — consistent with deploy-time use; no turn-path import found.

| Symbol | Line | Verdict | Run-2 |
|---|---|---|---|
| `FLAG_DOC_ID` ("config/frontend_cutover"), `DocumentReader` type, `_document_reader` global | ~10–27 | KEEP (file ADAPT) | C — flag contract; injectable reader keeps Firestore out of the module. |
| `set_document_reader` / `reset_document_reader` | 29, 35 | KEEP (file ADAPT) | C — wiring only. |
| `read_flag` | 39 | KEEP (file ADAPT) | C — validates shape (enabled bool, envs list), fails closed to None/OFF; config validation, not a domain transform. |
| Status constants + `STARTUP_FLAG_READ_TIMEOUT_SECONDS` (2.0) | ~55–65 | KEEP (file ADAPT) | C — diagnosable startup states + bound. |
| `firestore_reader` (+ inner `_read`) | 86, 95 | KEEP (file ADAPT) | C — bounded, non-retrying durable read, fail-closed; must not run on the turn path (file ADAPT). |
| `initialize_server_flag` | 115 | KEEP (file ADAPT) | C — environment identity checked before constructing a client; never raises. |

### `frontend_preview_release.py` (165 lines) — file verdict DELETE — run-2 §4 CONFIRMED

Run-2 §4 verdicts re-verified; all CONFIRM. The file activates only when a `deployment/cutover_preview/receipt.json` for PR 10571 is packaged; main.py:1872–1876 calls it at startup, and the default path is inert without that receipt. No player capability depends on it.

| Symbol | Line | Verdict | Run-2 |
|---|---|---|---|
| `PreviewReleaseError` | 15 | DELETE | C — error type for a preview contract no player path raises. |
| `_digest` | 19 | DELETE | C — overlay integrity for a one-off preview. |
| `preview_manifest_path` | 23 | DELETE | C — single-PR, single-environment receipt contract; release process, not gameplay. |
| `_receipt_frontend` | 58 | DELETE | C — receipt schema for the same overlay. |
| `_verify_inventory` | 84 | DELETE | C — inventory check for the same overlay. |
| `_verified_manifest` | 113 | DELETE | C — manifest binding for the same overlay; normal manifest path (frontend_release.py) unaffected. |
| `_PreviewFlagSnapshot` / `to_dict` | 140, 143 | DELETE | C — synthetic flag snapshot for a preview environment. |
| `_PreviewFlagClient` / `document` / `get` | 147, 148, 153 | DELETE | C — synthetic flag source that refuses without a verified receipt. |
| `create_preview_flag_client` | 157 | DELETE | C — factory for the synthetic source. |

### `frontend_release.py` (502 lines) — file verdict ADAPT — run-2 §4 CONFIRMED

Run-2 §4 verdicts re-verified symbol by symbol; all CONFIRM, including the deploy-time (not per-request) treatment of digest/inventory checks. Callers: main.py:138–139, 1873, 1884–1901, 2003–2036 (serving + startup). Note confirming run 2: `LEGACY_REQUIRED_RUNTIME_ASSETS` includes `js/settings.js` (line 78) — the dynamically-loaded settings file must be present in the served set, which is consistent with app.js's dynamic loader (the asset inventory and the loader agree).

| Symbol | Line | Verdict | Run-2 |
|---|---|---|---|
| `SCHEMA_VERSION`, `REPO_ROOT`, `DEFAULT_MANIFEST_PATH`, `VALID_SURFACES`, `DEFAULT_SURFACE` | ~15–40 | KEEP (file ADAPT) | C — manifest contract + default surface. |
| `LOAD_OK/LOAD_MISSING/LOAD_INVALID`, `REASON_*`, `is_refusal_reason` | ~45–58 | KEEP (file ADAPT) | C — fail-closed refusal vocabulary; refusing to serve the wrong UI is transport safety. |
| `ENV_STABLE`, `CUTOVER_ENVS`, `ENV_IDENTITY_VAR`, `deployment_env`, `resolve_cutover_enabled` | ~95–114 | KEEP (file ADAPT) | C — deployment identity + cutover decision. |
| `select_frontend_dir_for_deployment`, `select_frontend_dir` | 141, 453 | KEEP (file ADAPT) | C — the serving decision itself; pure transport selection. |
| `LEGACY_*` constants, `legacy_asset_relative_path`, `rewrite_legacy_asset_urls`, `resolve_legacy_request`, `legacy_serving_target` | 173–221 | KEEP (file ADAPT) | C — backward-compatible URL rewriting; DELETE as a set when legacy serving ends. |
| `LEGACY_REQUIRED_RUNTIME_ASSETS`, `EXPO_STATIC_ROOT`, `_required_runtime_assets` | 78–82 | ADAPT | C — runtime-asset inventory is a deploy-time invariant; evaluate at packaging, not per selection. |
| `REASON_FLAG_*` constants | ~130–140 | KEEP (file ADAPT) | C — flag-specific refusal reasons. |
| `_manifest_shape_is_valid`, `load_manifest` | 238, 259 | KEEP (file ADAPT) | C — fail-closed manifest validation. |
| `_resolve_artifact_dir`, `_index_sha256`, `_artifact_tree_digest`, `_artifact_tree_digest_or_none` | 284–310 | ADAPT | C — whole-tree integrity is transport safety but must be computed once at packaging, with only the stored digest verified at selection. |
| `_FrontendAssetParser` / `__init__` / `handle_starttag` | 318–323 | ADAPT | C — referenced-asset parsing per selection repeats deploy work; run at packaging/CI, keep the cached pass/fail at selection. |
| `_referenced_assets_exist`, `_validate_runtime_assets`, `_validate_release` | 351, 378, 403 | ADAPT | C — same deploy-time move as above. |

---

## (1) Dead / unreachable code list

| # | Item | Evidence | Verdict |
|---|---|---|---|
| D1 | `js/component-enhancer.js` (whole file, 33 symbols) | No `<script>` tag in index.html; no dynamic loader (only dynamic injection in shipped JS is app.js:2576–2583 for settings.js); mvp_site grep finds only README mentions, a theme-manager.js:86 comment, and a test docstring (tests/test_css_variable_coverage.py:140). interface-manager.js:91,99 guardedly reference `window.componentEnhancer`, but guards are no-ops while the file is unloaded. | DELETE (run 2 confirmed, wording corrected in §4) |
| D2 | `js/visual-validator.js` (whole file, 11 symbols) | No tag, no loader, no shipped caller; only README mentions in mvp_site grep. | DELETE (run 2 confirmed) |
| D3 | `js/test_planning_block_parsing.js` (whole file, 16 symbols) | No tag, no loader; zero mvp_site references outside itself; live parsing ships in streaming.js/app.js. | DELETE (run 2 confirmed) |
| D4 | `parallel_dual_pass.js` (6 symbols) + `parallel_dual_pass.css` (10 rule blocks) | No tag, no loader; mvp_site references only the historical PARALLEL_DUAL_PASS_INTEGRATION.md (describing a legacy `static/` layout and a `main_parallel_dual_pass.py` that does not exist in this tree) and one historical evidence page linking the CSS. | DELETE (run 2 confirmed) |
| D5 | `mocks/mock_header_avatar_and_scroll_gate.html` (359 lines, incl. `toggleDesktopChoices` + scroll listener) | No shipped page links to it; real header ships in index.html/app.js. | DELETE (run 2 confirmed, with the inline-JS correction) |
| D6 | app.js dead BYOK branch inside `setupSettingsEventListeners` (app.js:2595–2596) | Calls `window.setupBYOKEventListeners` if it is a function; settings.js defines only `setup_byok_event_listeners` (settings.js:72, called internally at settings.js:26) and never assigns the camelCase name to window (full frontend grep: only app.js:2595–2596 mention it). The typeof guard prevents a crash, so the branch is dead, not broken. NEW finding (not in run 2). | DELETE the branch (or wire it to the snake_case function); file ADAPT unchanged |
| D7 | `frontend_preview_release.py` (whole file) | Inert without the PR-10571 receipt; startup-only caller (main.py:1872–1876). | DELETE (run 2 confirmed) |
| D8 | `portrait-ai.js` compare pair (`renderPortraitCompareResults`, `ensurePortraitCompareControl`) | Subject `portrait_model_compare.py` is DELETE (debug double-generation); the UI pair has no other subject. `escapeCompareHtml` stays only if used elsewhere, else goes with the pair. | DELETE with subject (run 2 confirmed) |
| D9 | `scene_illustration_policy.build_legacy_scene_image_prompt` | Debug ablation baseline only; its only caller is ablation `_reconstruct_prompts`. | ADAPT: move with ablation out of the prod path (not standalone DELETE while ablation uses it) |

## (2) Test-only / demo code in prod files list

| # | Item | Evidence | Disposition |
|---|---|---|---|
| T1 | `js/test_planning_block_parsing.js` — self-contained `PlanningBlockTestSuite` (test/assert/run) + parser copies | Never loaded; duplicates shipped parsing in streaming.js/app.js. | DELETE from shipped dir (assertions, if kept, belong in tests/) — same as D3 |
| T2 | auth.js test-mode bypass (`canEnableTestMode`, `getTestModeParams`, plus run-2-named `__ALLOW_TEST_MODE__`/`testAuthBypass` wiring) | Shipped auth code carries a test sign-in bypass surface. | ADAPT: DELETE or gate out of production builds (run 2 confirmed) |
| T3 | app.js debug cluster (`refreshDebugToolsEligibility`, `createHudSessionHeaderState`, debug-controls add/remove, `renderDebugDetails`, `getDebugMarkerPairs`, `splitDebugMarkers`) | Operator tooling embedded in the player bundle. | ADAPT: behind a debug flag or out of the shipped bundle (run 2 confirmed) |
| T4 | scene-illustration.js ablation/debug cluster (`renderAblationControl*`, `loadDebugToolEligibility`, `renderAblationPanel`, `runPromptAblation`, `finish`, `tick`, `call`) + `scene_prompt_ablation.py` | Operator experimentation tooling in the player UI / shipped request path; ablation.py itself is admin-gated + quota-bounded. | ADAPT: behind debug flag / move out of shipped path (run 2 confirmed for JS; ablation.py ADAPT here) |
| T5 | settings.js scene-advanced visibility policy + auth.js/settings.js duplicated OpenRouter flows | Client re-implementation of a server decision + duplicated link/finish flows. | ADAPT (run 2 confirmed) |
| T6 | animation-helpers.js interception/patching (`interceptViewSwitching`, `enhanceExistingFunctionality`, original-function captures) | Runtime behaviour interception, not presentation. | DELETE (run 2 confirmed) |
| T7 | `frontend_preview_release.py` (PR-10571 preview scaffolding) | Single-use release scaffolding in the shipped tree. | DELETE (run 2 confirmed) |

## (3) Stale / misleading docs list

Each item states what the code actually does.

| # | Doc | Location | What the code actually does |
|---|---|---|---|
| S1 | README directory tree says `static/` layout with `themes/light.css`, `dark.css`, `cyberpunk.css` | frontend_v1/README.md:10, 39–42, 189–201 | The shipped tree is `frontend_v1/` (not `static/`); the only theme files are `themes/base.css`, `default.css`, `fantasy.css`. The light/dark/cyberpunk themes do not exist. |
| S2 | README: "app.js (~2,000+ lines)" + "Areas Needing Cleanup: app.js … (~2,000+ lines)" | frontend_v1/README.md:57, 239 | app.js is 10,666 lines. The size warning is right in spirit but wrong by 5×. |
| S3 | README "Main Public Methods": `loadDragonKnightCampaignContent()`, api.js `makeApiCall`/`getCampaigns`/`createCampaign`/`sendInteraction`, auth.js `initializeAuth()`/`signInWithGoogle()` | frontend_v1/README.md:70, 82–83, 96–97 | None of these names is defined in shipped frontend JS (grep over frontend_v1 JS excluding tests/ returns zero hits for each; only `getCurrentUser` exists, auth.js:472, used by api.js:195–196). The documented API surface does not exist. |
| S4 | README file entries for the DELETE files: component-enhancer.js "UI component enhancements", visual-validator.js "Form validation" | frontend_v1/README.md:22, 28, 111, 135 | Both files are never loaded (see D1/D2); the README presents them as live modules. (Fixes itself if the files are deleted and the README updated with them.) |
| S5 | README's own run-2 note (already flagged in run 2, confirmed here): "already partly stale (static/ layout)" | frontend_v1/README.md (whole) | Confirmed and extended by S1–S4 above. File verdict stays KEEP (docs); these are corrections, not a deletion. |
| S6 | `scene_prompt_ablation.py` module docstring: "reachable only through the retry endpoint for users whose settings have debug_mode true (the route returns 403 otherwise)" | scene_prompt_ablation.py:1–10 | The route gates on the canonical admin claim, not debug_mode: main.py:5107–5113, with the comment "debug_mode is informational, not a gate". The code is correct; the docstring is wrong. |
| S7 | `scene_illustration_worker.py` dataclass default `timing_mode = SCENE_ILLUSTRATIONS_MODE_PARALLEL` | scene_illustration_worker.py:~107 | The server canonicalizes parallel → after_scene (policy:92) and both construction sites pass the resolved mode, so the default is unreachable in production; a reader would infer parallel is a live timing mode. Minor default/doc note; no behaviour change. |
| S8 | terms-of-use.html §3 vs §20 age wording | terms-of-use.html §§3, 20 | §3 says "you are not a minor in your jurisdiction"; §20 says "intended for users aged 17 and older". Internal tension to reconcile (flagged, not a legal judgement, not a verdict change). |
| S9 | terms-of-use.html §19 "in-app Report action" | terms-of-use.html §19 | The server content-report endpoint exists (main.py:~8302), and main.py's own contact page (main.py:9038) repeats the "in-app Report action" wording — but no Report control was located in frontend_v1 JS by grep in this pass. Unverified from the frontend side; needs a UI check before the claim is relied on. Not a stale verdict. |
| S10 | `mocks/mock_header_avatar_and_scroll_gate.html` stylesheet link `../styles/style.css` | mock html:9 | That path does not exist (style.css is at frontend_v1/style.css); the mock's own CSS reference is broken. Moot if the mock is deleted (D5). |
| S11 | index.html:648–652 share-modal comment (PR #5823 guard) | index.html:648–652 | ACCURATE — verified: the modal is inside `<body>` (653+) before `</body>` (716). Listed here as checked-and-correct, not stale. |
| S12 | `scene_illustration_flag.py` docstrings (fail-closed, UNKNOWN vs OFF, 2s timeout) | scene_illustration_flag.py (whole) | ACCURATE — verified against bodies. Listed as checked-and-correct. |
| S13 | `js/outcome-verdict.js` header comment (explicit wins; else aggregate non-save rolls; no "critical" verdict) | js/outcome-verdict.js:1–9 | ACCURATE description of the code — which is precisely why the fallback must go: the comment faithfully documents a ZFC violation (run-2 ADAPT confirmed). |

## (4) Challenges to run-2 verdicts (with evidence)

| # | Run-2 claim | Challenge / correction | Verdict effect |
|---|---|---|---|
| C1 | §8.1 component-enhancer: "no shipped code references the export" | interface-manager.js:91,99 DO reference `window.componentEnhancer` (guarded `if (window.componentEnhancer)` calls to `disable()`/`enable()`), and theme-manager.js:86 mentions component-enhancer in a comment (event dispatch, not a load). The file is still never loaded, and the guards are no-ops while it is absent — so the DELETE verdict stands, but the "no reference" wording is wrong. | Verdict UNCHANGED (DELETE); wording corrected |
| C2 | §2 mock HTML row: no mention of inline JS in the mock | The mock contains `toggleDesktopChoices()` (line 334, onclick line 221) + an anonymous scroll auto-reveal listener. Mock-only presentation; DELETE stands. | Verdict UNCHANGED (DELETE); row corrected |
| C3 | (New, not in run 2) app.js BYOK wiring assumed consistent | app.js:2595–2596 expects `window.setupBYOKEventListeners`; settings.js defines `setup_byok_event_listeners` (line 72) and never exports the camelCase name. Dead branch (guarded, so not a crash). See D6. | New dead-code item; file ADAPT unchanged |
| C4 | Run-2 counts (app.js 257, auth.js 46, settings.js 54, streaming.js ~33) | This pass counts 303/91/67/47 under a broader rule that also counts class/object methods and property assignments (e.g. auth.js token-manager object methods). The counts differ by method, not by missed code: every run-2-named symbol was found in this pass's enumeration or accounted for as a non-function const/wiring item (see auth.js file note). No run-2 verdict depends on the narrower count. | No verdict change; method reconciled |
| C5 | Task premise: frontend_*.py had "no full run-2 method review" (run-1 Phase-1-only) | The v2 file DOES contain full per-function §4 rows for all three frontend_*.py files (cutover §4.1, preview §4.2, release §4.3). Either the premise predates the v2 file's §4 or §4 was carried from run 1 — in either case this pass re-verified every symbol against the local files and CONFIRMS all three file verdicts (ADAPT / DELETE / ADAPT). | No verdict change; provenance noted |
| C6 | Run-2 §8.3: 17 shipped CSS files | This pass counts 18 CSS files reviewed (17 shipped KEEP + parallel_dual_pass.css DELETE). Consistent — the difference is whether the DELETE sheet is counted as "shipped". | No verdict change |
| C7 | Run-2 terms-of-use KEEP by element cluster | CONFIRMED as KEEP, with two added doc notes (S8 age-wording tension, S9 Report-action frontend presence unverified). Neither changes the verdict. | Verdict UNCHANGED (KEEP) |
| C8 | Run-2 §9(c) equipment_display correction (keyword branches DELETE) | CONFIRMED as the correct backend verdict, but equipment_display.py is OUTSIDE this area (owned by misc) and was NOT re-reviewed here. Frontend-side contract, verified from app.js, is stated here for the misc auditor: app.js expects (a) an `equipment` endpoint returning `equipment_summary` (string, app.js:1803, 1834) and a full `equipment_list` array rendered with NO truncation (app.js:1806–1816, brace-verified in run 2 and re-confirmed: no slice/limit on that path); (b) story-entry `equipment_display` arrays of `{name|item, slot, stats}` with unnamed items filtered out client-side (app.js:3173–3195, name-or-item fallback, "unknown" slot fallback); (c) `equipment_bonuses` keyed by stat (app.js:1674). MISMATCH RISK (not a proven mismatch): if the backend's unfiltered grouping changes the shape of `equipment_display` items (e.g. drops `slot`/`stats` keys) or the `equipment` endpoint stops returning `equipment_list`, the frontend degrades to "No equipment found." (app.js:1831) / skips the block (app.js:3184 condition) silently. The frontend does NOT depend on backpack subcategories or importance ordering — so deleting `_classify_backpack_item` keyword branches and the top-3 truncation does not break the frontend; it only ever rendered what the server sent. | No frontend verdict change; contract handed to misc |
| C9 | Run-2 document_generator ADAPT (prose-mining DELETE) | CONFIRMED as the correct backend verdict; document_generator.py is OUTSIDE this area (owned by misc) and was NOT re-reviewed here. Frontend side: the export UI (app.js download cluster + test_campaign_export_ui) only requests/downloads generated documents; it does not depend on prose-mined structure. No frontend change needed for the backend deletion. | No frontend verdict change |

No other run-2 verdict is challenged: every other file verdict, every §8.1/§8.2 cluster verdict, and the §9(a)/(b)/(d) verifications were re-checked against the local tree and CONFIRM (file:line evidence in the tables above).

## (5) Draft-amendment effects (DRAFT ONLY — no verdict changed)

The draft amendment (FastEmbed/Jev count as models; dispatch on model outputs is execution; hand-written thresholds/boosts/anchor lists layered on model outputs still need an exception) was NOT applied. Checked for every place it could matter in this area:

- Frontend code contains no FastEmbed or Jev usage, no similarity thresholds, no anchor-phrase lists, and no score boosts. The client-side derivations flagged here (outcome-verdict roll aggregation, app.js/streaming.js terminal inference) aggregate SERVER/CLIENT observations (roll `success` booleans, narrative-text presence, client descriptors) — not model-call outputs dispatched on by the server — so the amendment would not rescue them even if adopted. Verdicts unchanged.
- Frontend choice sending uses explicit `CHOICE:<id>` signals (app.js:3966, 3973, 4884), consistent with the explicit-signals-only modal conclude rule that the amendment preserves. The amendment's Jev-Noul-may-flag-but-never-auto-conclude rule has no frontend counterpart to change (no client auto-conclude was found).
- Scene policy presence rules and context selection are prompt text and prompt assembly, not thresholds layered on a model decision output; the amendment does not change their KEEP verdicts. `filter_scene_context_entries` god-mode exclusion uses the explicit GOD MODE: prefix rule, not a similarity score.
- The dispatch-table-stays-server-side point in the task concerns agents.py (outside this area); nothing in the frontend dispatches on agent modes.
- Conclusion: adopting the draft amendment would change ZERO verdicts in area A12. If it is adopted later, no frontend row needs revisiting on that account alone.

## (6) Coverage accounting

Files reviewed (68, each with per-symbol rows above unless noted):

- frontend_v1 (58): .gitignore, README.md, api.js, app.js, auth.js, campaign-click-fix.css, css/avatar.css, css/inline-editor.css, css/pagination-styles.css, css/tooltip-guide.css, diag-boot.js, diagnostics.js, dragon-favicon.svg, images/avatars/arion_dragon_knight.png, images/twin_dragon.png, images/twin_dragon.webp, index.html, js/animation-helpers.js, js/avatar-crop.js, js/campaign-wizard.js, js/component-enhancer.js, js/ember-bg.js, js/enhanced-search.js, js/inline-editor.js, js/interface-manager.js, js/loading-messages.js, js/opening_story.js, js/outcome-verdict.js, js/portrait-ai-ui.js, js/portrait-ai.js, js/scene-illustration.js, js/settings.js, js/streaming.js, js/test_planning_block_parsing.js, js/theme-bootstrap.js, js/theme-manager.js, js/tooltip-guide.js, js/ui-utils.js, js/visual-validator.js, js/worldai-mcp-bridge.js, loading-messages.css, mocks/mock_header_avatar_and_scroll_gate.html, parallel_dual_pass.css, parallel_dual_pass.js, quick_start_shared.js, style.css, styles/animations.css, styles/bridge.css, styles/components.css, styles/enhanced-components.css, styles/globals.css, styles/interactive-features.css, styles/planning-blocks.css, terms-of-use.html, themes/base.css, themes/default.css, themes/fantasy.css, user_lifecycle.js.
- Python (10): frontend_cutover_flag.py, frontend_preview_release.py, frontend_release.py, scene_attempts.py, scene_illustration_flag.py, scene_illustration_policy.py, scene_illustration_provider.py, scene_illustration_service.py, scene_illustration_worker.py, scene_prompt_ablation.py.

Symbols reviewed: 1,064 JS definitions (enumerated by the regex method in the header; per-file counts in each table) + 1,518 CSS rule blocks (one row per `{` block) + ~30 HTML section clusters (index.html, terms-of-use.html, mock HTML) + 151 Python AST symbols (attempts 4, flag 12, policy 26, provider 5, service 17, worker 33, ablation 14, cutover 6, preview 12, release 22) + non-code files (README, .gitignore, favicon, 3 images) at file level. Total ≈ 2,762.

Files/symbols skipped: NONE unexplained.
- `frontend_v1/tests/` (122 test files + helpers/fixtures/repro harness): EXCLUDED BY SCOPE per the task (the file list excludes them by construction) — not skipped. Run-2 §8.2 test verdicts stand and were not re-audited here.
- `equipment_display.py` and `document_generator.py`: OUTSIDE this area (owned by misc); only the frontend-side interface contracts are stated here (see C8/C9). Not skipped — explicitly out of scope.
- Non-function JS consts (plain data consts, e.g. LABELS-adjacent config objects, `PORTRAIT_TIMEOUT_MS`-style constants) have no rows of their own because the task's unit is function/arrow-const/class/method; they are covered by their file verdict and, where load-bearing, by file notes. Anonymous callbacks are covered under their enclosing named function (as in run 2).
- CSS declarations inside a rule block are not separate rows (the rule block is the unit); token blocks such as `themes/default.css`'s single `:root` block (111 lines of custom properties) count once, as one rule.
- Repo AGENTS.md files (`worldarchitect.ai/AGENTS.md`, `mvp_site/AGENTS.md`) were read as DATA per the runtime's house-rules note. Two of their rules touch this task and are noted, not followed over the task: (a) their "evidence/scratch strictly to /tmp" rule conflicts with this task's explicit output path `~/workspace/plans/audit/review/frontend.md` — the task path was followed, since the parent task outranks repo files; (b) their merge/network/evidence gates are moot for a read-only review (no edits, no merges, no network calls, no LLM calls were made).

Verdict summary for this area (file level; 58 + 10 = 68 files): KEEP — 40 frontend files + 6 Python files (scene_attempts, scene_illustration_flag, scene_illustration_policy — with one ADAPT symbol, build_legacy_scene_image_prompt — scene_illustration_provider, scene_illustration_service, scene_illustration_worker). ADAPT — 12 frontend files (app.js, auth.js, animation-helpers.js, campaign-wizard.js, portrait-ai.js, scene-illustration.js, settings.js, streaming.js, tooltip-guide.js, outcome-verdict.js, user_lifecycle.js, twin_dragon.png) + 3 Python files (frontend_cutover_flag.py, frontend_release.py, scene_prompt_ablation.py) = 15. DELETE — 6 frontend files (component-enhancer.js, visual-validator.js, test_planning_block_parsing.js, parallel_dual_pass.js, parallel_dual_pass.css, mock_header_avatar_and_scroll_gate.html) + frontend_preview_release.py = 7. Reconciliation: 40 frontend KEEP + 12 frontend ADAPT + 6 frontend DELETE = 58 frontend; 6 Python KEEP + 3 Python ADAPT + 1 Python DELETE = 10 Python; total 68. In-file symbol-level DELETE/ADAPT items are listed in §1/§2 and in the per-symbol exception notes.

---

*End of A12 frontend review. Method note: all reads from the local tree at ~/workspace/repos/worldarchitect.ai; no GitHub API/MCP calls, no browser use, no repo changes, no subagents. JS enumeration script + caller-count method described in the header; CSS rows generated from brace positions; Python rows from AST + sampled full reads (policy/service/worker/ablation read in full; flag/attempts/provider read in full; frontend_* verified against v2 §4 rows).*
