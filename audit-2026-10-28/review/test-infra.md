# A13 — Test infrastructure living in the prod tree

- **Area:** A13 — `mvp_site/testing_framework/`, `mvp_site/testing_ui/`, `mvp_site/mocks/`
- **Files reviewed:** 32 (list in §6; every file under the three dirs in
  `~/workspace/plans/audit/review/_file_list.txt` for these prefixes)
- **Units reviewed:** 284 code units — 274 AST-enumerated defs/classes
  (see §6 enumeration method) + 10 module-level fixture constants
  (`mocks/data_fixtures.py`: 6; `mocks/structured_fields_fixtures.py`: 4)
  — plus 10 Markdown files judged file-by-file and section-by-section.
- **File verdicts:** DELETE-from-prod-tree (relocate, capability kept) 28 /
  ADAPT 4 / KEEP 0. **Unit verdicts:** DELETE 267 / ADAPT 17 / KEEP 0
  (the 2 `testing_ui/` Markdown files are ADAPT at file level and are not
  in the 284-unit count).
- **Scope exclusion (by construction, NOT skipped):**
  `mvp_site/testing_framework/tests/` (6 files: `__init__.py`,
  `test_capture.py`, `test_factory.py`, `test_integration_example.py`,
  `test_mock_provider.py`, `test_real_provider.py`),
  `mvp_site/testing_framework/test_*.py` (3 files), and
  `mvp_site/testing_ui/test_*.py` (16 files) — 25 files excluded from this
  area's list. They are referenced below only as importer evidence.
- **Read-only, local tree only:** `~/workspace/repos/worldarchitect.ai`
  (main-branch ZIP tree). Zero GitHub API/MCP calls, no repo files changed.
- **Method:** Pass A zero-code baseline, then Pass B strict ZFC, per
  `~/workspace/plans/zero-code-rejustification-audit.md` §4, with §6
  decisions applied. **DELETE here means "does not belong in the shipped
  prod tree"** (test-only code should live in the test tree), NOT "delete
  the test capability" — relocation is stated explicitly per file. The
  ZFC skill amendment draft (`plans/zfc-skill-model-amendment-proposal.md`)
  is DRAFT ONLY and was NOT applied; §5 records the one place it was
  considered and why it changes nothing.
- **Headline finding (overrides a run-2 claim):** run 2 `scripts-tests.md`
  §3 said the mocks "are imported by offline/function tests only; no player
  turn path imports them in production." That is **wrong for two files**.
  `mvp_site/llm_providers/provider_gateway.py:21` imports
  `MockLLMClient` from `mocks/mock_llm_service.py` and `:22` imports
  `FULL_STRUCTURED_RESPONSE` from `mocks/structured_fields_fixtures.py`,
  and both are executed on the shipped mock-services path (see §2).
  Everything else in this area is test-only-in-prod-tree.

## Importer-search method (reproducible)

- Prod search: `grep -rn --include='*.py' -E 'testing_framework|from mocks|import mocks|mock_firestore|mock_llm|testing_ui' mvp_site/`
  with `testing_framework/`, `mocks/`, `testing_ui/` and `tests/`/`test_*.py`
  hits removed, plus targeted greps for each module name across
  `mvp_site/` and `tests/`.
- Result: the ONLY prod-code (non-test, non-test-framework) importer of
  anything in this area is `mvp_site/llm_providers/provider_gateway.py`
  (lines 21–22, used at lines 272/289 and 298/479). No file in
  `mvp_site/testing_framework/` is imported by any prod file. No file in
  `mvp_site/testing_ui/` is imported by any Python prod file (the only
  prod references are string paths in `mvp_site/main.py:9421,9445` inside
  `run_test_command`, pointing at `testing_ui/run_all_browser_tests.py`,
  which **does not exist anywhere in the tree** — dead reference, out of
  this area's file list but flagged in §4).
- Transitive-load caveat: importing any `mvp_site.mocks.*` submodule
  executes `mvp_site/mocks/__init__.py`, which imports both wrapper
  modules, which import both mock clients. So in a prod process that
  imports `provider_gateway`, the whole `mocks/` package is *loaded* —
  but only `MockLLMClient` and `FULL_STRUCTURED_RESPONSE` are ever
  *called* on a prod path. Load ≠ use; the distinction is stated per row.

## Per-file tables

Conventions: grouped rows name EVERY symbol they cover (line numbers from
AST). "Prod" = importer outside tests/test-framework; "Test" = importer
inside `mvp_site/tests/`, `testing_framework/tests/`, `test_*.py`, or the
test framework itself. Lens A = executability/reachability; Lens B = docs
accuracy. Verdicts are under current §4 policy.

### 1. `mvp_site/mocks/__init__.py` (27 lines, 0 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| Module re-exports: `MockLLMClient`, `MockLLMResponse`, `MockFirestoreClient`, `MockFirestoreDocument`, `SAMPLE_*` (lines 6–27) | None directly; loaded transitively whenever `provider_gateway.py:21` imports a mocks submodule | `mvp_site/tests/test_structured_fields_storage.py:13` (`from mocks import mock_firestore_service`); test-framework `mock_provider.py` imports submodules directly, not via this package | Pure re-export surface for test code. Deleting it from `mvp_site/` breaks only test imports, which move with it. Its one prod-adjacent role (transitive load) is not a use. | Docstring "Mock libraries for function testing" is accurate. | **DELETE** — relocate the whole `mocks/` package to the test tree; repoint `provider_gateway.py:21–22` to the smoke module per file 5/7 below, otherwise the smoke path breaks. |

### 2. `mvp_site/mocks/data_fixtures.py` (176 lines, 6 constants) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `SAMPLE_CAMPAIGN`, `SAMPLE_GAME_STATE`, `SAMPLE_STORY_CONTEXT`, `SAMPLE_AI_RESPONSES`, `SAMPLE_STATE_UPDATES`, `DISCREPANCY_SCENARIOS` | None as a direct import; `SAMPLE_AI_RESPONSES` is transitively prod-loaded because `mock_llm_service.py:10` imports it and `provider_gateway.py:21` imports that module, and `SAMPLE_AI_RESPONSES[...]` IS read on the smoke path (`mock_llm_service.py:195,199,203,207`) | `mock_firestore_service.py:14`, `mock_llm_service.py:10`, `mocks/__init__.py:7–13`, plus tests via those | Static test data, not a transform. No player capability breaks if it moves — the smoke path's reads move with `mock_llm_service`. `DISCREPANCY_SCENARIOS` has no reader in `mocks/` at all (dead fixture — confirm against tests before deleting it outright; relocation preserves it either way). | Module docstring "data fixtures file, not a test file" is honest about what it is, and that is exactly why it does not belong in the shipped tree. | **DELETE** — relocate to the test tree alongside `mock_llm_service`; if the smoke extraction (file 5) keeps `SAMPLE_AI_RESPONSES`, that one constant moves with the smoke module instead. |

### 3. `mvp_site/mocks/mock_firestore_service.py` (407 lines, 29 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `MockFirestoreDocument`: `__init__@22`, `to_dict@27`, `get@31`, `exists@49`, `id@54`; `MockFirestoreClient`: `__init__@65`, `_initialize_sample_data@78`, `get_campaigns_for_user@115`, `get_campaign_by_id@125`, `get_campaign_game_state@141`, `update_campaign_game_state@155`, `create_campaign@165`, `add_story_entry@211`, `update_campaign_title@253`, `update_campaign@263`, `delete_campaign@275`, `get_game_state@292`, `update_game_state@300`, `get_story_context@315`, `reset@338`, `get_operation_stats@347`, `set_campaign_data@359`, `set_game_state_data@366`, `set_story_context@373`; module fns `get_mock_firestore_client@385`, `add_story_entry@391`, `get_campaign_by_id@405` | **None.** No prod file imports this module and no prod call site exists (the `firestore_service.py:1226 reset_mock_firestore` name match is unrelated real-service code). Loaded transitively via `mocks/__init__.py` in a `provider_gateway`-importing process, never called. | `testing_framework/mock_provider.py:23`; `mvp_site/tests/test_structured_fields_storage.py:13,26,47,56` (module fns); `mocks/__init__.py:14` | In-memory fake of the real `firestore_service.py` interface (same method names: `get_campaign_by_id`, `create_campaign`, `add_story_entry`, `get_game_state`, …) — duplicated logic, test-only. Pass A: deleting it from prod breaks no player capability; tests move with it. Pass B: a fake durable-write layer is not transport/durable-writes for players. | Docstrings describe a mock accurately; no stale claim found in code. (The stale claims are in the READMEs, §4.) | **DELETE** — relocate to the test tree. This corrects the run-2 framing only in location: run 2 `scripts-tests` KEEP for this file was a "keep the test capability" verdict; under this pass's definition the capability is kept, the location is not. |

### 4. `mvp_site/mocks/mock_firestore_service_wrapper.py` (199 lines, 14 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `get_client@20`, `get_campaigns_for_user@32`, `get_campaign_by_id@38`, `create_campaign@44`, `update_campaign@67`, `delete_campaign@73`, `get_game_state@82`, `update_game_state@88`, `update_state_with_changes@94`, `get_campaign_game_state@115`, `update_campaign_game_state@122`, `add_story_entry@131`, `get_story_context@169`, `_truncate_log_json@175` | **None** (no direct importer anywhere; loaded only via `mocks/__init__.py:6`) | None direct — only `mocks/__init__.py:6` | A second fake of the same real-service surface (cf. file 3's client methods and real `firestore_service.py`), differing only by module-function shape plus `_truncate_log_json` (1000-char log cap, a test-log bound). No test file imports it directly in the grep; its only consumer is the package `__init__`. Pass A/B as file 3. | Docstring "provides the same interface as the real firestore_service module" is accurate in intent; `DELETE_FIELD = object()` sentinel (line ~13) is a rough stand-in for the real sentinel, noted not judged. | **DELETE** — relocate with the package; on relocation, drop it if no test imports it directly (verify at PR time — its functions are reachable only through the package import, which no test uses for this module's names). |

### 5. `mvp_site/mocks/mock_llm_service.py` (277 lines, 17 defs) — ADAPT (smoke-path extraction)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `MockLLMResponse`: `__init__@17`, `__str__@20`; `MockLLMClient`: `__init__@30`, `generate_content@45`, `_determine_response_type@72`, `_generate_initial_story@97`, `_generate_continue_story@163`, `_generate_hp_discrepancy@197`, `_generate_location_mismatch@201`, `_generate_mission_completion@205`, `_generate_validation_response@209`, `set_response_mode@224`, `reset@228`; module fns `get_mock_client@239`, `parse_state_updates_from_response@244` | **YES — prod-reachable, gated.** `llm_providers/provider_gateway.py:21` imports `MockLLMClient`; `MockGeminiClient` (provider_gateway.py:272) instantiates it and calls `generate_content` at `:289`. Gate: `provider_gateway.is_mock_services_mode()` (`:209–225`: env `MOCK_SERVICES_MODE` or Flask `g.mock_services_mode`, set by `main.py:2414` only on the SMOKE_TOKEN bypass path with `X-Mock-Services: true`); `gemini_provider.py:1408–1412` dispatches to it; `llm_service.py:672,679,2680,5004,5428,9945` branch on it. This is a dev/smoke gate, not gameplay — but it IS executed by shipped code. | `testing_framework/mock_provider.py:24`; `mocks/__init__.py:15`; `mock_llm_service_wrapper.py` | Pass A: deleting the client breaks the mock-services smoke path (a real, shipped, gated execution path), so the client itself cannot be a pure relocate. Pass B: it is a fake model, not a server transform of model output — its keyword dispatch (`_determine_response_type@72`: "start a story", "unconscious", "forest"+"tavern", "dragon"+"treasure") selects canned fixtures, never a live campaign fact; that is fixture selection, not prod intent classification (see §5 draft-amendment note). Duplication: its `generate_content`/`get_initial_story`/`continue_story` shape duplicates the real `llm_service` interface, by design for a double. | Docstring "simulates AI responses based on prompt patterns… for testing purposes" understates the prod smoke use — it should name the mock-services gate. Otherwise accurate. | **ADAPT** — keep the smoke execution, but extract `MockLLMClient` + `MockLLMResponse` + the `_generate_*` fixture generators + `SAMPLE_AI_RESPONSES` reads into an explicitly-named, gated smoke/dev module outside `mocks/` (or keep the file with a gate banner and a comment at `provider_gateway.py:21`); move `set_response_mode`/`reset` test scaffolding with the tests if the smoke path does not need them. **`parse_state_updates_from_response@244`: DELETE outright** — zero importers anywhere (grep over `mvp_site/` + `tests/` returns only its definition); agrees with run-2 scripts-tests DELETE for this function (a mirror of a deprecated parser). |

### 6. `mvp_site/mocks/mock_llm_service_wrapper.py` (231 lines, 4 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `get_client@26`, `generate_content@35`, `get_initial_story@62`, `continue_story@159` (which internally reads `FULL_STRUCTURED_RESPONSE` at lines 196–204) | **None** (no direct importer; loaded only via `mocks/__init__.py:6`). Note: the prod smoke path does NOT use this wrapper — it uses `MockLLMClient` directly via `provider_gateway`. | None direct — only `mocks/__init__.py:6` | Module-function-shaped duplicate of the real `llm_service` surface (`generate_content` accepting but ignoring temperature/top_p/schema, `:35–60` docstring admits this) plus story entry points. No consumer found outside the package import. Pass A/B as file 3. | Docstring claims are accurate about the mock; the "accepted but not used" parameter note is honest. | **DELETE** — relocate with the package; on relocation, drop if no test imports it directly (none found). Do NOT confuse with file 5: this wrapper is not the smoke path. |

### 7. `mvp_site/mocks/structured_fields_fixtures.py` (194 lines, 4 constants) — ADAPT (split)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `FULL_STRUCTURED_RESPONSE` | **YES — prod-reachable.** `provider_gateway.py:22` imports it; `provider_gateway.py:298` and `:479` `json.dumps()` it as the mock-Gemini response text on the smoke path. | `mock_llm_service.py:11`, `mock_llm_service_wrapper.py:8` | The one fixture in this area that shipped code serializes as a fake model reply. Pass A: deleting it breaks the smoke path. Pass B: static expected output, not a decision. | Module docstring "all 10 fields from game_state_instruction.md" — not field-count-verified in this pass; flagged as unverified, not proven stale (the constant is large; a field-count check is PR-time work, not a verdict changer). | **ADAPT (split)** — `FULL_STRUCTURED_RESPONSE` KEEPs with the smoke extraction (file 5); `INITIAL_CAMPAIGN_RESPONSE`, `GOD_MODE_RESPONSE`, `MINIMAL_STRUCTURED_RESPONSE` DELETE-from-prod-tree (relocate to the test tree; no prod importer). |

### 8. `mvp_site/mocks/README.md` (283 lines) — DELETE (relocate with package)

Sections judged: Overview; Directory Structure; Mock Services (`mock_firestore_service.py`, `mock_llm_service.py`, `data_fixtures.py`); Usage Patterns (unit/integration/development testing); Mock Design Principles; Mock Configuration; Test Scenarios. Lens A: docs for test code, not gameplay. Lens B — **stale, two counts**: (1) "Mock Configuration / Environment Variables" (lines ~145–151) lists `USE_MOCK_SERVICES`, `MOCK_FIRESTORE`, `MOCK_GEMINI` — **no `getenv` call in any `mocks/*.py` reads any of them** (grep over `mocks/*.py` returns zero `getenv`); the real gate is `MOCK_SERVICES_MODE` in `provider_gateway.py:211`. (2) "Configuration Options" (lines ~153–160) instantiates `MockFirestoreService(response_delay=…, error_rate=…, max_campaigns=…)` — **no such class or parameters exist**; the class is `MockFirestoreClient` with no such constructor args. Development-testing section's "Application will use mocks instead of real services" is true only via the `provider_gateway` smoke gate, which the README never names. **DELETE** — relocate with the package and fix both stale sections on relocation (or delete the README if the test tree already documents the mocks).

### 9. `mvp_site/mocks/README_GRANULAR_MOCKS.md` (114 lines) — DELETE (relocate with package)

Sections judged: Overview; Environment Variables (individual service control); Legacy Support; Using `run_ui_tests.sh`; Why Granular Control; Implementation Details; Testing; Common Use Cases. Lens A: docs for test/dev modes. Lens B — **stale**: the env vars it documents (`USE_MOCK_FIREBASE`, `USE_MOCK_GEMINI`, lines 8–35) are **not read by any `mocks/*.py` or `testing_framework/*.py` code** (grep returns no matches); the implemented gate is `MOCK_SERVICES_MODE` (+ `X-Mock-Services` header). The `run_ui_tests.sh` workflows (lines 41–64) cannot be verified from this area's files (no such script under `mvp_site/` in this list) — flagged unverified, not proven false. **DELETE** — relocate with the package; on relocation, either delete (superseded by the real gate) or rewrite around `MOCK_SERVICES_MODE`.

### 10. `mvp_site/testing_framework/__init__.py` (26 lines, 0 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| Re-exports: `TestConfig`, `get_service_provider`, `get_current_provider`, `set_service_provider`, `reset_global_provider`, `MockServiceProvider`, `RealServiceProvider`, `TestServiceProvider` (lines 6–15) | **None** | `testing_framework/tests/*`, `test_*_validation.py` (excluded files) — no prod consumer | Pure test-framework public surface. Pass A/B: deleting it from prod breaks no player capability; the framework moves as a unit. | Docstring accurate ("switching between mock and real services for testing"). | **DELETE** — relocate with the framework to the test tree. Note: `MockServiceProvider` here is `mock_provider.py`'s class, while `factory.py` internally shadows that name with the simple provider (file 14) — the `__init__` export and the factory default are DIFFERENT classes, a latent confusion the relocation should resolve by deleting one provider. |

### 11. `mvp_site/testing_framework/capture.py` (419 lines, 32 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `CaptureManager`: `__init__@18`, `capture_interaction@30`, `record_response@73`, `save_captures@93`, `_sanitize_data@113`, `get_summary@164`; `CaptureFirestoreClient`: `__init__@207`, `collection@211`, `document@217`, `__getattr__@223`; `CaptureCollectionReference`: `__init__@231`, `add@238`, `document@252`, `stream@259`, `get@276`, `__getattr__@293`; `CaptureDocumentReference`: `__init__@301`, `set@306`, `get@319`, `update@335`, `delete@348`, `__getattr__@359`; `CaptureGeminiClient`: `__init__@367`, `generate_content@371`, `__getattr__@394`; module fns `load_capture_data@399`, `cleanup_old_captures@405` | **None** | `real_provider.py:8` (capture wrappers + manager); `testing_framework/tests/test_capture.py:16`; `capture_cli.py` (via `cleanup_old_captures`, broken import — §4) | Recording wrappers around real clients, used only when a test runs in `capture` mode (`real_provider.py:37–38,67–68`). `_sanitize_data@113` redacts password/secret/token/api_key patterns — a test-artifact privacy measure, not a player-path guard. Pass A: no player capability breaks. Pass B: capture is test instrumentation, not transport/durable-writes for players. | Docstrings accurate as far as read (`capture_interaction` context manager, sanitization). No stale claim in code; the stale capture claims live in the Markdown (§4). | **DELETE** — relocate to the test tree with `real_provider`. |

### 12. `mvp_site/testing_framework/capture_analysis.py` (387 lines, 12 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `CaptureAnalyzer`: `__init__@17`, `analyze_captures@20`, `_get_recent_capture_files@37`, `_analyze_interactions@53`, `compare_with_mock@132`, `_compare_responses@199`, `_compare_dicts@228`, `_compare_lists@264`, `_truncate_data@288`, `generate_report@295`; module fn `create_mock_baseline@360` | **None** | `capture_cli.py:20`; `testing_framework/tests/test_capture.py:22`; `examples/capture_example.py:20` | Offline analysis of capture JSON: accuracy score = matches/total over successful interactions (`compare_with_mock@132`), first-successful-response baselines (`create_mock_baseline@360`). Pure test tooling; no prod caller, no player capability. | Docstrings accurate. `create_mock_baseline`'s "first successful response wins" rule is a simplification the docstring does not warn about — minor, not a verdict changer. | **DELETE** — relocate to the test tree. |

### 13. `mvp_site/testing_framework/capture_cli.py` (202 lines, 6 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `analyze_command@23`, `compare_command@36`, `baseline_command@79`, `cleanup_command@93`, `list_command@104`, `main@134` | **None** | None (CLI entry point; invoked by humans/CI, referenced only in `capture_example.py:261–289` printouts) | Argparse CLI over files 11–12. **Additionally broken as shipped:** line 13 `from capture import cleanup_old_captures` executes BEFORE the `sys.path` insert at lines 15–17, so `python -m mvp_site.testing_framework.capture_cli` fails at import while running from inside the directory succeeds — the import order contradicts the "add current directory to path" comment. Pass A/B: test tooling, no player capability. | Docstring "Command-line interface for capture analysis" is accurate; the CLI help text is the only doc. The `capture_example.py` printouts that advertise `python -m mvp_site.testing_framework.capture_cli …` commands would hit the broken import — stale-by-bug, see §4. | **DELETE** — relocate to the test tree and fix the import order (move the `sys.path` insert above line 13, or use a relative import) if the CLI is to survive at all. |

### 14. `mvp_site/testing_framework/config.py` (51 lines, 4 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `TestConfig`: `get_real_service_config@14`, `validate_real_service_config@35`, `get_test_collection_name@47` | **None** | `real_provider.py:9`; `testing_framework/__init__.py:6` | Test-only env config: `TEST_FIRESTORE_PROJECT` (default `worldarchitect-test`), `TEST_GEMINI_API_KEY`, `test_` collection prefix, fixed test user/session ids. No prod reader. | **Stale in one detail:** `get_real_service_config@14` pins model `gemini-1.5-flash` ("Use cheaper model for testing") — an old model name that no prod path uses; harmless in tests but stale as documentation of the test setup. `validate_real_service_config` checks only the Gemini key, despite the name implying full validation — minor overclaim. | **DELETE** — relocate to the test tree; update the model pin on relocation. |

### 15. `mvp_site/testing_framework/examples/capture_example.py` (329 lines, 4 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `demo_capture_mode@24`, `demo_mock_capture@97`, `demo_cli_tools@255`, `main@292` (plus `__main__` guard) | **None** | None (demo script; imports `capture_analysis.py:20` and `factory.py:21` for its own demos) | Demo/example code, executed only via `__main__`. Prints CLI invocations (lines 261–289) including the broken `capture_cli` module path (file 13). Pass A/B: no player capability; example, not infrastructure. | Docstrings are demo narration, accurate as narration; the printed "Next steps" (lines ~315–322) advertise `TEST_MODE=capture` runs, which is real framework behavior. The CLI printouts are stale-by-bug per file 13. | **DELETE** — relocate to the test tree's examples/docs, or delete outright if the Markdown already covers the demos (the CAPTURE_README duplicates this content). Demo code has no business in the shipped tree under any verdict. |

### 16. `mvp_site/testing_framework/factory.py` (64 lines, 4 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `get_service_provider@29`, `set_service_provider@45`, `get_current_provider@51`, `reset_global_provider@59`; plus module state `_current_provider`, `_use_full_mocks` | **None** | `fixtures.py:12`, `pytest_integration.py:13`, `integration_utils.py:15`, `examples/capture_example.py:21`, `testing_framework/tests/test_factory.py:19` | The framework's mode switch (`TEST_MODE` env, default `mock`: `get_service_provider@29–43`). **Two latent bugs, both test-only:** (1) line 9 imports `MockServiceProvider` from `mock_provider`, line 10 immediately shadows it with `SimpleMockServiceProvider as MockServiceProvider` — so `get_service_provider("mock")` returns the SIMPLE provider, while `testing_framework/__init__.py` exports the FULL one; tests importing each get different classes. (2) lines 23–26 `try: _use_full_mocks = True except ImportError:` can never raise (no import inside the try) — dead flag, read only by `tests/test_factory.py:36`. Pass A/B: test routing, no player capability. | Docstring "Manages global provider state for tests" accurate. The shadow import is undocumented — a reader of `__init__.py` + `factory.py` together will conclude the wrong provider is the default. | **DELETE** — relocate to the test tree; on relocation, delete one of the two mock providers (file 19 vs file 22) and the dead `_use_full_mocks` flag so the default is unambiguous. |

### 17. `mvp_site/testing_framework/fixtures.py` (195 lines, 20 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| Pytest fixtures `service_provider@21`, `firestore_client@37`, `gemini_client@43`, `auth_service@49`, `test_mode@55`, `is_real_service@61`; `BaseTestCase`: `setUp@81`, `tearDown@89`; `IsolatedTestCase`: `setUp@102`, `tearDown@107`; module fns `setup_test_services@118`, `cleanup_test_services@138`, `get_test_client_for_mode@148`; `MockCompatibilityMixin`: `__init__@177`, `mock_firestore@183`, `mock_gemini@188`, `mock_auth@193` | **None** | `migration_examples.py:11,17`; `test_basic_validation.py:15`; `test_integration_validation.py:21` (excluded files) | Pytest/unittest scaffolding that yields providers per `TEST_MODE`. `MockCompatibilityMixin` here DUPLICATES `integration_utils.py:130`'s same-named mixin with a different mechanism (provider properties vs `setUp` attributes) — two compatibility layers for the same migration, a genuine duplication (file 18). Pass A/B: test-only. | Docstrings accurate; usage examples in docstrings match the fixture names. No stale claim found. | **DELETE** — relocate to the test tree; on relocation, merge the two `MockCompatibilityMixin` classes into one. |

### 18. `mvp_site/testing_framework/integration_utils.py` (335 lines, 28 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `dual_mode_test@29` (+ nested `wrapper@38`), `skip_in_real_mode@48` (+ `decorator@57`, nested `wrapper@58`), `real_mode_only@69` (+ `decorator@78`, nested `wrapper@79`); `DualModeTestMixin`: `setUp@103`, `tearDown@108`, `_setup_dual_mode@114`; `MockCompatibilityMixin`: `setUp@136`, `_setup_mock_compatibility@141`; `SmartPatcher`: `__init__@164`, `__enter__@175`, `__exit__@197`; `smart_patch@204`, `convert_test_class@221`, `update_test_imports@246`; `TestResourceManager`: `__init__@268`, `create_test_collection@272`, `cleanup@285`; `validate_test_environment@307`, `get_test_mode_info@327` | **None** | `test_basic_validation.py:20`, `test_integration_validation.py:12,22` (excluded files) | Migration decorators/mixins + a `SmartPatcher` context manager + test-resource cleanup. **Hazard:** line 13 `import main` ("fail fast if not available") imports the entire 9,634-line gateway at test-util import time — importing this helper has prod-module side effects (env checks, module-level init in `main.py`) for zero test benefit, since nothing in this file's bodies (as read) needs `main`'s names beyond the comment's claim. Pass A/B: test-only migration glue. | Docstring "helpers for gradual migration and backwards compatibility" accurate. The `import main` comment ("fail fast") does not justify importing the gateway; it is a smell, not a doc error per se — flagged here so the relocation removes it. | **DELETE** — relocate to the test tree; on relocation, remove `import main` and merge `MockCompatibilityMixin` with file 17's. |

### 19. `mvp_site/testing_framework/migration_examples.py` (282 lines, 20 defs) — DELETE (relocate or delete)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `TraditionalCharacterTestBefore`: `setup_method@32`, `test_api_accepts_character_setting_params_old_way@38`; `ModernCharacterTestAfter`: `setUp@84`, `test_api_accepts_character_setting_params_new_way@91`, `_run_character_setting_test@107`; `test_character_creation_pytest_old@137`, `test_character_creation_pytest_new@146`; `GradualMigrationExample`: `setup_method@171`, `test_legacy_with_compatibility_helper@177`, `_run_existing_test_logic@197`; `BackwardsCompatibleTest`: `setup_method@210`, `teardown_method@226`, `test_existing_code_unchanged@231`; `RealModeSafetyExample`: `test_with_resource_limits@248`, `test_with_isolation@268` | **None** | None — and, critically, **not collected as tests**: the file is not named `test_*.py`, so default pytest discovery (`python_files = test_*.py`, cf. `pytest_integration.py:configure_pytest_ini`) never runs these classes; they are documentation in code form. Imports `fixtures.py:11,17` and `main.create_app:22` for the examples. | Before/after migration examples. Pass A/B: no player capability, no test execution either — dead as tests, alive only as reading material. | The file's own framing as examples is accurate; but a reader may assume these tests run — they do not under default discovery. That is a doc-behavior mismatch worth one line on relocation. | **DELETE** — relocate to test-tree docs/examples, or delete outright if `MIGRATION_GUIDE.md` (file 27) already carries the same patterns (it does, in prose). Either way it leaves the shipped tree. |

### 20. `mvp_site/testing_framework/mock_provider.py` (57 lines, 7 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `MockServiceProvider`: `__init__@32`, `get_firestore@37`, `get_gemini@41`, `get_auth@45`, `cleanup@49`, `is_real_service@55` (property); module const `project_root` (duplicated sys.path block, lines 12–22, twice) | **None** | `factory.py:9` (shadowed — see file 16); `testing_framework/__init__.py:13`; `testing_framework/tests/test_mock_provider.py:12` | Full mock provider: instantiates `MockFirestoreClient` + `MockLLMClient` (`:32–35`), `get_auth` returns `None` ("Use existing mock auth" — i.e. no auth double at all), `cleanup` resets both. Duplicates file 22's provider (same interface, richer doubles). Pass A/B: test-only. | Docstring accurate, including the honest `get_auth` gap (returns `None`). The duplicated `sys.path` insertion block (lines 12–22, written twice with different comments) is sloppy but not a doc falsehood. | **DELETE** — relocate with the framework; on relocation, keep exactly one mock provider (this or file 22 — this one has the real mock clients; file 22 has no external deps). |

### 21. `mvp_site/testing_framework/pytest_integration.py` (322 lines, 26 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| Fixtures `test_mode@22`, `service_provider@28`, `isolated_service_provider@41`, `firestore_client@58`, `gemini_client@64`, `auth_service@70`, `is_real_service@76`, `test_services@82`; hooks `pytest_configure@107`, `pytest_runtest_setup@113`; fixture `all_modes_service_provider@132`; helpers `_has_real_service_config@151`, `skip_if_real_mode@163`, `skip_if_mock_mode@169`, `requires_real_services@175`, `mock_only@180`, `expensive_test@185`, `test_mode_info@196`, `validate_test_environment@203`, `configure_pytest_ini@218`; `example_test_functions@263` (+ nested `test_basic_usage@267`, `test_mock_specific_behavior@276`, `test_real_integration@282`, `test_cross_mode_compatibility@288`, `test_with_cleanup@301`) | **None** (pytest plugin hooks fire only if the file is loaded as a plugin/conftest — no prod loader does) | Any test run that loads it as a plugin (by convention, not by import found in grep) | Pytest hooks/markers/fixtures for mode-skipping (`pytest_runtest_setup@113` skips `mock_only` in real mode and `real_only` in mock mode). Duplicates file 17's fixtures (`test_mode`, `firestore_client`, `gemini_client`, `auth_service`, `is_real_service` exist in both) — a second fixture set for the same modes. `example_test_functions@263`'s nested `test_*` functions are never collected (nested, not module-level). `configure_pytest_ini@218` **writes `pytest.ini` into the current working directory** — a side-effecting helper in a library module. Pass A/B: test-only. | Docstrings accurate for hooks/fixtures. `configure_pytest_ini`'s generated config claims `testpaths = mvp_site` + `python_files = test_*.py`, which is consistent with file 19's non-collection note. | **DELETE** — relocate to the test tree (as a conftest/plugin, not a shipped module); on relocation, deduplicate fixtures against file 17 and either delete `example_test_functions` or move it to docs. |

### 22. `mvp_site/testing_framework/real_provider.py` (161 lines, 11 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `RealServiceProvider`: `__init__@16`, `get_firestore@31`, `get_gemini@56`, `get_auth@86`, `cleanup@101`, `_cleanup_collection@117`, `track_test_collection@140`, `is_real_service@147` (property), `get_capture_summary@151`, `save_capture_data@157` | **None** | `factory.py:19`; `testing_framework/__init__.py:14`; `testing_framework/tests/test_real_provider.py:15` | Real-service test provider: constructs real Firestore (`firestore.Client`, `:23–34`) and Gemini (`genai.Client`, `:49–62`) clients, wraps them in capture clients in capture mode, and `cleanup@101` saves captures then deletes tracked `test_`-prefixed collections. Test isolation is by naming convention + explicit cleanup, not by a sandbox project. Pass A/B: test-only; its real clients are test clients, not the game's call path (`llm_service`/`firestore_service` are separate). | Docstring "Uses actual services with test isolation and cleanup" accurate. `get_auth@86` returns a stub `TestAuth` object carrying the fixed
  test user/session ids from `config.py`, not a verified credential — the docstring does not claim verification, so no falsehood, but a reader should not mistake it for auth. | **DELETE** — relocate to the test tree. |

### 23. `mvp_site/testing_framework/service_provider.py` (32 lines, 6 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `TestServiceProvider` (ABC): `get_firestore@14`, `get_gemini@18`, `get_auth@22`, `cleanup@26`, `is_real_service@31` (all abstract) | **None** | Every provider + fixture file in this area (`factory.py:20`, `fixtures.py:13`, `mock_provider.py:26`, `real_provider.py:10`, `simple_mock_provider.py:8`, `pytest_integration.py:14`) | Abstract interface only — no behavior, no player capability. Pass A/B: test scaffolding. | Docstring accurate. | **DELETE** — relocate with the framework (it is the framework's interface; it moves as a unit, not as a deletion of the abstraction). |

### 24. `mvp_site/testing_framework/simple_mock_provider.py` (129 lines, 30 defs) — DELETE (relocate)

| Symbols | Prod importers | Test importers | Lens A | Lens B | Verdict |
|---|---|---|---|---|---|
| `SimpleMockDocument`: `__init__@14`, `set@18`, `get@22`, `to_dict@25`, `reference@29`; `SimpleMockCollection`: `__init__@36`, `document@40`, `stream@45`; `SimpleMockFirestore`: `__init__@52`, `reset@57`, `collection@62`, `get_campaigns_for_user@67`; `SimpleMockGemini`: `__init__@75`, `generate_content@78`, `reset@82`; `SimpleMockAuth`: `__init__@89`, `verify_id_token@92`, `reset@96`; `SimpleMockServiceProvider`: `__init__@103`, `get_firestore@108`, `get_gemini@112`, `get_auth@116`, `cleanup@120`, `is_real_service@127` (property) | **None** | `factory.py:10` (as the shadowed default — this IS the provider `get_service_provider("mock")` actually returns); `testing_framework/tests/test_factory.py:39,45` | A third fake of the same surfaces (cf. files 3 and 20), dependency-free by design ("Avoids dependency issues"). `SimpleMockGemini.generate_content@78` returns a canned response without the scenario dispatch of file 5; `SimpleMockAuth.verify_id_token@92` is a stub accept. Pass A/B: test-only; the duplication across files 3/20/24 (three Firestore fakes, two Gemini fakes, two providers) is the area's largest redundancy. | Docstring "Simplified… Avoids dependency issues while providing the same interface" accurate. | **DELETE** — relocate with the framework; on relocation, keep exactly one mock provider (see files 16/20). |

### 25–30. `mvp_site/testing_framework/*.md` (6 files) — DELETE (relocate with framework)

Judged per file, with section-level claims. All are docs for the test
framework, not gameplay; all move with it. Lens B findings (the substance):

- **25. `README.md` (195 lines)** — Sections: Overview; Quick Start; Service Modes (mock/real/capture); API Reference; Configuration; Directory Structure; Testing the Framework; Usage Patterns. **Stale/incomplete:** the Directory Structure listing (lines 101–117) omits `capture.py`, `capture_analysis.py`, `capture_cli.py`, `fixtures.py`, `integration_utils.py`, `pytest_integration.py`, `migration_examples.py`, `examples/`, and the three `test_*_validation.py` files; "Testing the Framework" (lines 118–129) tells the reader to run `python3 test_integration_demo.py` and `python3 simple_test.py` — **neither file exists** in `testing_framework/` (the real files are `test_integration_validation.py` and the `tests/` suite). Mode descriptions themselves match `factory.py:29–43`. **DELETE** (relocate, fixing the listing and commands).
- **26. `CAPTURE_README.md` (394 lines)** — Sections: Overview; Quick Start; Captured Data Format; Core Components (`CaptureManager`, Service Wrappers, Analysis Tools); CLI; plus later sections. **Stale:** Quick Start step 1 says "Use the `/testerc` command" (lines 15–21) — **no `/testerc` command exists anywhere in `mvp_site/*.py`** (grep returns only these Markdown mentions); capture mode is actually entered via `TEST_MODE=capture` (factory) / `RealServiceProvider(capture_mode=True)`, which the same doc also mentions, so the doc contradicts itself. Core Components accurately describe `capture.py`'s classes. **DELETE** (relocate, replacing `/testerc` with the env-var path).
- **27. `CAPTURE_IMPLEMENTATION.md` (275 lines)** — Sections: Mission Complete; Deliverables (core framework, analysis tools, CLI, RealServiceProvider integration, testing, docs); Technical Implementation (data format, "transparent integration", analysis workflow); Validation Results ("All Success Criteria Met", testing results); Usage Patterns (dev workflow, CI/CD). **Stale-by-assertion:** "Transparent Integration" claims "Code remains unchanged, capture happens transparently" (line 118) — true only in the narrow sense that capture wraps clients in `real_provider.py`; it is not a property of the game path (no prod code is capture-wrapped). Validation Results (lines 141–185) report success criteria as met without naming the run, date, or command — unverifiable completion claims. **DELETE** (relocate; completion reports belong in test docs, not the shipped tree).
- **28. `IMPLEMENTATION_SUMMARY.md` (227 lines)** — Sections: Overview; Completed Deliverables (interface, mock provider, real provider, factory, config, capture framework, unit tests); Key Features; Validation Results; File Structure; Usage Examples. **Stale:** "Commands Phase: Slash commands (`/teste`, `/tester`, `/testerc`)… COMPLETED" (line 215) — same `/testerc` problem as file 26; no such commands exist in the tree. File Structure repeats file 25's omission pattern. **DELETE** (relocate).
- **29. `INTEGRATION_SUMMARY.md` (267 lines)** — Sections: Integration Agent Deliverables (fixtures, unittest integration, high-value test updates, safety features, migration docs, pytest integration, validation); Framework Architecture; Backwards Compatibility ("Zero Breaking Changes"); Migration Approaches. **Stale/overclaim:** "Zero Breaking Changes ✅" (line 144) is a process claim about a migration, not a property of the current tree, and it sits alongside the file-16 shadow-provider behavior (two different "mock" providers depending on import path), which IS a breaking-behavior difference for anyone migrating. "High-Value Test Updates ✅ COMPLETED" names no test files. **DELETE** (relocate).
- **30. `MIGRATION_GUIDE.md` (383 lines)** — Sections: Quick Start (minimal/fixtures); Test Modes; Migration Patterns (class-level, method-level, gradual); Service Access Patterns (Firestore/Gemini); Safety Features (resource limits, automatic cleanup, test isolation); Decorators (`@skip_in_real_mode`, `@real_mode_only`). **Mostly accurate:** mode names, decorator names, and provider behavior match `factory.py`, `integration_utils.py`, `fixtures.py`. Two soft spots: "Resource Limits" (lines 170–187) describes limits the code enforces only partially (`config.py`'s `max_requests_per_test: 10` is a config value, not an enforced counter in `real_provider.py` as read); "Automatic Cleanup" overstates `real_provider.cleanup` (deletes only collections explicitly tracked via `track_test_collection`). Neither is a verdict changer. **DELETE** (relocate — the guide is the one doc worth keeping, in the test tree).

### 31. `mvp_site/testing_ui/README_TEST_MODE.md` (156 lines) — ADAPT (keep in test area, fix refs)

Sections judged: Overview; How It Works (server setup, browser navigation, frontend behavior, backend validation); Example Playwright Test; Browser Test Helper Library; Campaign Creation Wizard Steps (5 steps); Common Issues Resolved; Security Notes; Common Issues; Files Involved. Lens A: this file already lives in a test directory (`testing_ui/`), not the game path — it is not test-only-in-prod-tree in the same sense as the framework; it documents the browser-test auth bypass that prod code actually implements (`main.py:387–390` `TESTING_AUTH_BYPASS_MODE`, `:1486` prod warning, `:1826–1830` dev-mode check). Lens B — **two path problems**: (1) "Browser Test Helper Library" (lines 76–113) imports `from testing_ui.browser_test_helpers import BrowserTestHelper` — that module exists only at repo-root `testing_ui/browser_test_helpers.py`, NOT under `mvp_site/testing_ui/`; from inside `mvp_site/` the import as written resolves to the wrong tree (or fails), so the example is misleading as placed. (2) "Files Involved" (lines 151–156) lists `static/auth.js`, `static/api.js`, `static/app.js` paths that do not match the shipped `mvp_site/frontend_v1/` layout as named — flagged unverified (frontend layout was not re-audited here). Security Notes ("test mode ONLY works when server is started with `TESTING_AUTH_BYPASS=true`") match `main.py:387`. **ADAPT** — keep in the test area, fix the helper import path (repo-root vs `mvp_site` tree) and verify the static-file paths.

### 32. `mvp_site/testing_ui/wizard_test_instructions.md` (159 lines) — ADAPT (keep in test area, prune)

Sections judged: Prerequisites; Test Scenarios (wizard init, input fields, form validation, preview system); Puppeteer MCP Implementation; Test Coverage Matrix; Manual Testing Checklist; Integration with CI/CD; Notes. Lens A: manual/automated browser-test instructions; no executable code; no prod importer (it is prose). Lens B: the "Puppeteer MCP Implementation" section (lines 89–121) prescribes a Puppeteer-MCP workflow; the repo's browser tests in this tree are Playwright-style `test_*.py` files (excluded from this area) and the `main.py:9421` runner reference is dead (§4) — so the prescribed toolchain does not match the tree's actual test runner layout. The wizard-step scenarios themselves are consistent with the 5-step wizard described in file 31. **ADAPT** — keep in the test area, prune/replace the Puppeteer-MCP section with the actual runner, or mark it historical.

## (1) Test-only code in the prod tree (with importer evidence)

Everything below is DELETE-from-prod-tree (relocate, capability kept)
except where noted. "No prod importer" means the grep in the header
section found no non-test, non-framework importer.

- `mvp_site/mocks/__init__.py` — test importers: `tests/test_structured_fields_storage.py:13`; loaded transitively by prod only via `provider_gateway.py:21` submodule import, never called directly.
- `mvp_site/mocks/data_fixtures.py` — importers: `mock_firestore_service.py:14`, `mock_llm_service.py:10`, `mocks/__init__.py:7`; no prod importer of its own (transitive smoke load via file 5 noted in its table).
- `mvp_site/mocks/mock_firestore_service.py` — importers: `mock_provider.py:23`, `tests/test_structured_fields_storage.py:13,26,47,56`, `mocks/__init__.py:14`; **no prod importer, no prod call site**.
- `mvp_site/mocks/mock_firestore_service_wrapper.py` — importer: `mocks/__init__.py:6` only; **no direct importer anywhere, no prod call site**.
- `mvp_site/mocks/mock_llm_service_wrapper.py` — importer: `mocks/__init__.py:6` only; **no direct importer anywhere, no prod call site** (the prod smoke path bypasses it).
- `mvp_site/mocks/README.md`, `README_GRANULAR_MOCKS.md` — docs for the above; move with the package.
- `mvp_site/testing_framework/` in full except the smoke-adjacent files
  (none — the framework has no prod importer at all): `__init__.py`,
  `capture.py`, `capture_analysis.py`, `capture_cli.py`, `config.py`,
  `factory.py`, `fixtures.py`, `integration_utils.py`,
  `migration_examples.py`, `mock_provider.py`, `pytest_integration.py`,
  `real_provider.py`, `service_provider.py`, `simple_mock_provider.py`,
  `examples/capture_example.py`, and the six `*.md` files — importers
  are exclusively `testing_framework/tests/*`, `test_*_validation.py`
  (excluded), other framework files, and (for the examples) nobody.
- NOT test-only (the exceptions, §2): `mock_llm_service.py` (client) and
  `structured_fields_fixtures.py` (`FULL_STRUCTURED_RESPONSE` only).

## (2) Prod-reachable test-framework code (with the prod importer for each)

- `mvp_site/mocks/mock_llm_service.py` — `MockLLMClient`, `MockLLMResponse`,
  `_determine_response_type`, `_generate_*` — prod importer:
  `mvp_site/llm_providers/provider_gateway.py:21`; executed at
  `provider_gateway.py:272,289` (`MockGeminiClient.generate_content`),
  dispatched from `gemini_provider.py:1408–1412`, gated by
  `provider_gateway.is_mock_services_mode()` (`:209–225`) and
  `main.py:2414` (SMOKE_TOKEN + `X-Mock-Services: true`). Verdict ADAPT
  (smoke extraction), not DELETE — deleting it without touching the gate
  breaks the shipped smoke path.
- `mvp_site/mocks/structured_fields_fixtures.py` —
  `FULL_STRUCTURED_RESPONSE` only — prod importer:
  `mvp_site/llm_providers/provider_gateway.py:22`; serialized at
  `provider_gateway.py:298,479`. Verdict ADAPT (split); the other three
  constants are test-only (§1).
- `mvp_site/mocks/data_fixtures.py` — `SAMPLE_AI_RESPONSES` only, and
  only transitively: read on the smoke path at
  `mock_llm_service.py:195,199,203,207` once `provider_gateway` loads the
  module. Listed here for completeness; its verdict is DELETE-relocate
  *with* the smoke extraction, not a standalone prod KEEP.
- `mvp_site/testing_ui/*.md` — not Python-imported by prod, but they
  document a prod-implemented bypass (`main.py:387–390`,
  `TESTING_AUTH_BYPASS_MODE`); verdict ADAPT (fix refs), not relocate.
- Nothing in `mvp_site/testing_framework/` is prod-reachable.

## (3) Dead / unreachable code

- `mocks/mock_llm_service.py:244 parse_state_updates_from_response` —
  zero importers/callers anywhere (`mvp_site/` + `tests/` grep returns
  only the definition). **DELETE outright** (not relocate). Agrees with
  run-2 scripts-tests DELETE for this function.
- `mocks/mock_firestore_service_wrapper.py` and
  `mocks/mock_llm_service_wrapper.py` (all functions) — no direct
  importer anywhere; reachable only through `mocks/__init__.py:6`,
  whose re-exported names no test uses for these modules. Dead as an
  import surface; relocate-or-drop at PR time (verdict DELETE either way).
- `testing_framework/factory.py:23–26 _use_full_mocks` — try/except that
  cannot raise; read only by excluded `tests/test_factory.py:36`. Dead
  flag; delete with the file's relocation.
- `testing_framework/factory.py:9` first `MockServiceProvider` import —
  shadowed by line 10; the full provider is unreachable through the
  factory default (it is reachable through `__init__.py` and direct test
  imports, so this is a live confusion, not a dead class).
- `testing_framework/capture_cli.py:13` — import-before-path-insert bug;
  the CLI as invoked via `python -m mvp_site.testing_framework.capture_cli`
  is unreachable (ImportError); only directory-local invocation works.
- `testing_framework/migration_examples.py` test classes — never
  collected by default pytest discovery (file is not `test_*.py`); dead
  as tests, alive only as prose.
- `testing_framework/pytest_integration.py:263 example_test_functions`
  nested `test_*` functions — never collected (nested definitions).
- `testing_framework/integration_utils.py:13 import main` — no body in
  the file uses `main`'s names as read; the import's only effect is
  gateway side effects at import time. Remove on relocation.
- `mocks/data_fixtures.py:DISCREPANCY_SCENARIOS` — no reader in `mocks/`;
  presumed dead or test-only; verify against `tests/` at PR time
  (relocation preserves it either way, so this is not a deletion claim).
- Cross-area dead reference (not in this file list, flagged for the
  owner): `mvp_site/main.py:9421,9445 run_test_command` points at
  `testing_ui/run_all_browser_tests.py`, which exists nowhere in the
  tree (repo-wide `find` returns nothing). The `testui`/`testuif`
  commands are therefore dead ends as shipped.
- NOT dead (correction of an apparent finding):
  `testing_ui/browser_test_helpers.py` as cited in
  `testing_ui/README_TEST_MODE.md:78,91` DOES exist — at repo-root
  `testing_ui/browser_test_helpers.py`, imported by
  `tests/harness/submit_scroll_controlled.py` and
  `tests/test_browser_test_helpers.py`. The README's defect is the
  tree-relative path, not a missing module (§4).

## (4) Stale / misleading docs

| Location | Claim | What the code actually does | Severity |
|---|---|---|---|
| `mocks/README.md:145–151` | Env vars `USE_MOCK_SERVICES`, `MOCK_FIRESTORE`, `MOCK_GEMINI` enable mocks | No `getenv` in any `mocks/*.py`; the implemented gate is `MOCK_SERVICES_MODE` (`provider_gateway.py:211`) + `X-Mock-Services` header (`main.py:2414`) | Stale — rewrite on relocation |
| `mocks/README.md:153–160` | `MockFirestoreService(response_delay=…, error_rate=…, max_campaigns=…)` | No such class/params; class is `MockFirestoreClient` with no such constructor args | Stale — false API |
| `mocks/README_GRANULAR_MOCKS.md:8–35` | `USE_MOCK_FIREBASE` / `USE_MOCK_GEMINI` granular control | Neither var is read by any `mocks/*.py` or `testing_framework/*.py` code | Stale — superseded by `MOCK_SERVICES_MODE` |
| `testing_framework/README.md:101–117` | Directory structure listing | Omits `capture.py`, `capture_analysis.py`, `capture_cli.py`, `fixtures.py`, `integration_utils.py`, `pytest_integration.py`, `migration_examples.py`, `examples/`, `test_*_validation.py` | Incomplete |
| `testing_framework/README.md:118–129` | Run `test_integration_demo.py`, `simple_test.py` | Neither file exists in `testing_framework/` (real: `test_integration_validation.py`, `tests/`) | Stale commands |
| `testing_framework/CAPTURE_README.md:15–21` | "Use the `/testerc` command" | No `/testerc` command exists in `mvp_site/*.py`; capture mode is `TEST_MODE=capture` / `RealServiceProvider(capture_mode=True)` | Stale, self-contradicting |
| `testing_framework/IMPLEMENTATION_SUMMARY.md:215` | Slash commands `/teste`, `/tester`, `/testerc` COMPLETED | No such commands in the tree | Stale completion claim |
| `testing_framework/CAPTURE_IMPLEMENTATION.md:118` | "Code remains unchanged, capture happens transparently" | Capture wraps clients only inside test `real_provider.py`; no prod code is capture-wrapped | Misleading scope |
| `testing_framework/CAPTURE_IMPLEMENTATION.md:141–185` | "All Success Criteria Met" + testing results | No run, date, or command named — unverifiable | Unverifiable claim |
| `testing_framework/INTEGRATION_SUMMARY.md:144` | "Zero Breaking Changes ✅" | Factory default (simple provider) differs from `__init__` export (full provider) — a real behavior difference for migrators | Overclaim |
| `testing_framework/MIGRATION_GUIDE.md:170–187` | "Resource Limits" | `max_requests_per_test: 10` (`config.py:14`) is a config value, not an enforced counter in `real_provider.py` as read | Soft overclaim |
| `testing_framework/config.py:14` (code comment as doc) | Model `gemini-1.5-flash` "for testing" | Old model pin, unused by any prod path; stale as test-setup documentation | Minor stale |
| `mocks/mock_llm_service.py` docstring | "for testing purposes" | Also the shipped smoke-path model double (`provider_gateway.py:21,272,289`) | Understates prod use |
| `testing_ui/README_TEST_MODE.md:76–113` | `from testing_ui.browser_test_helpers import …` in `mvp_site/testing_ui/` context | Module lives at repo-root `testing_ui/`, not `mvp_site/testing_ui/` | Wrong-tree path |
| `testing_ui/wizard_test_instructions.md:89–121` | Puppeteer MCP implementation workflow | Tree's browser tests are Playwright `test_*.py`; `main.py`'s runner reference (`run_all_browser_tests.py`) does not exist | Toolchain mismatch |
| `testing_framework/capture_cli.py` + `examples/capture_example.py:261–289` | Printed `python -m mvp_site.testing_framework.capture_cli …` commands | That invocation fails at line 13's pre-path import (see §3) | Stale-by-bug |

Docstrings inside the `.py` files were otherwise accurate as read; no
other docstring falsehood was found. (`.md` files outside this area's
list were not judged.)

## (5) Draft-amendment effects

The draft at `~/workspace/plans/zfc-skill-model-amendment-proposal.md`
(would count FastEmbed/Jev outputs as model-authored, with hand-written
thresholds/boosts/anchors still needing an exception) was NOT applied.
Considered and rejected as a verdict-changer here:

- `mock_llm_service.MockLLMClient._determine_response_type@72` does
  keyword matching ("unconscious" → hp_discrepancy, etc.). Under the
  draft it would still not be model output — it is a hand-written
  fixture selector inside a test double, not a model call — and under
  current policy it is fixture selection, not prod intent classification
  (no player turn reaches it except via the gated smoke path, where it
  is the *fake model itself*, not a routing layer over a real model).
  Verdict unchanged (ADAPT, smoke extraction).
- No file in this area calls FastEmbed, Jev, or any embedding scorer;
  no verdict depends on whether a model call's output counts as
  model-authored. **Draft-amendment effect on this area: none — zero
  verdicts would change if the draft were adopted.**
- §6 decision interaction (not a draft effect): the smoke path's
  existence is a dev-mode product choice, not a §6 decision. If the
  owner decides smoke mode is not a shipped promise, files 5 and 7
  flip from ADAPT to DELETE (relocate + delete the `provider_gateway`
  mock branch and the `main.py:2414` header activation) — that is a
  product decision for the owner, flagged here, not taken here.

## (6) Coverage accounting

**Files reviewed (32, all in the assigned list, none added, none skipped):**

`mvp_site/mocks/` (9): `README.md`, `README_GRANULAR_MOCKS.md`,
`__init__.py`, `data_fixtures.py`, `mock_firestore_service.py`,
`mock_firestore_service_wrapper.py`, `mock_llm_service.py`,
`mock_llm_service_wrapper.py`, `structured_fields_fixtures.py`.

`mvp_site/testing_framework/` (21): `CAPTURE_IMPLEMENTATION.md`,
`CAPTURE_README.md`, `IMPLEMENTATION_SUMMARY.md`,
`INTEGRATION_SUMMARY.md`, `MIGRATION_GUIDE.md`, `README.md`,
`__init__.py`, `capture.py`, `capture_analysis.py`, `capture_cli.py`,
`config.py`, `examples/capture_example.py`, `factory.py`, `fixtures.py`,
`integration_utils.py`, `migration_examples.py`, `mock_provider.py`,
`pytest_integration.py`, `real_provider.py`, `service_provider.py`,
`simple_mock_provider.py`.

`mvp_site/testing_ui/` (2): `README_TEST_MODE.md`,
`wizard_test_instructions.md`.

**Methods reviewed (284 units + 10 Markdown files' sections):**
enumeration by `ast.parse` over each `.py` file (every
`FunctionDef`/`AsyncFunctionDef`/`ClassDef`, including nested defs and
dunders, with line numbers — totals: `mocks/` 64 defs + 10 constants;
`testing_framework/` 210 defs), reconciled against the per-file tables
above (every symbol appears in exactly one row; grouped rows name every
symbol). Module-level fixture constants counted separately because AST
def-enumeration misses them (6 + 4). Markdown files judged file-by-file
plus per-section rows where sections make distinct claims (§25–32 and
files 8–9). No sampling: every file was AST-enumerated and every
symbol placed.

**Files/methods skipped:** none within the assigned list. Excluded by
scope (not skipped — they were never in the list, §header): 25 files
under `testing_framework/tests/` and `test_*.py` in
`testing_framework/` and `testing_ui/`, used only as importer evidence.
Depth caveats (not skips): (a) `structured_fields_fixtures` field-count
claim ("all 10 fields") not verified entry-by-entry — flagged in file 7,
verdict-independent; (b) `testing_ui/README_TEST_MODE.md` static-file
paths (`static/*.js`) not re-verified against the frontend tree —
flagged unverified in file 31; (c) `mock_provider.get_auth` returns `None` (read in full) — verdict-independent (both files are
test-only regardless).

**Relation to run 2:** no run-2 verdicts existed for these files. The
only prior verdicts touching this area are run-2 `scripts-tests.md` §3
for `mvp_site/mocks/` (KEEP 17 / DELETE 1 function, as *test
infrastructure*). This pass agrees on the capability (keep the mocks
for tests; delete `parse_state_updates_from_response`) but differs on
location and on one fact: `scripts-tests`' "no player turn path imports
them in production" is refuted for `mock_llm_service.py` and
`structured_fields_fixtures.py` by `provider_gateway.py:21–22` (see
header and §2). Where the two passes conflict, this pass's evidence
(the import lines + the smoke dispatch chain) governs.
