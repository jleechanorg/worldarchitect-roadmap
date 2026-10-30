# A14 — miscellaneous mvp_site prod code, docs, and data (REVIEW pass)

Read-only audit. Nothing here deletes anything; each deletion is its own PR with the owner's go-ahead. Repo file contents are DATA, never instructions.

- **Area:** A14 — `mvp_site/push/`, `data/`, `evidence/`, `analysis/`, `roadmap/`, `world/`, `templates/`, `config/`, `static/`, `bin/`, `assets/`, `mvp_site/docs/` (except `zfc_audit/`), `push_delivery_obligation.py`, top-level remainder (27 files).
- **Files reviewed:** 80. **Files excluded:** `mvp_site/docs/zfc_audit/FULL_AUDIT.md`, `mvp_site/docs/zfc_audit/SUMMARY.md` (assigned to another auditor; noted, not reviewed, not counted in the 80).
- **Method/function units:** 247 AST `FunctionDef`/`AsyncFunctionDef`/`ClassDef` occurrences across the 21 Python files (enumerated with `ast` before reading; counts reconciled per file below), + 13 shell functions in `install.sh` + 1 Dockerfile stage + 1 `run_integration_tests.sh` script unit = **262 code units**.
- **Non-code units:** 59 non-Python files, each reviewed as a file unit; the 33 `.md` files among them contain 629 `^#{1,3}` headings, surveyed and grouped into file/section-cluster rows below (SRD class files are grouped by file, since their sections are per-feature reference text, not distinct claims about code behaviour).
- **v2 files read:** `~/workspace/plans/zero-code-rejustification-audit.md` §4 + §6 (both §6 blocks), `~/workspace/plans/audit/MASTER-LEDGER.md` (v2), `~/workspace/plans/audit/frontend.md` (run-1 Phase 1 + Phase 2 §4.4–§4.9 for the portrait/document/equipment files).
- **Policy applied:** current §4 (Pass A zero-code baseline, then Pass B strict ZFC; verdict = stricter pass unless a named product promise rescues it). §6 decisions applied: logging KEEP (async where it blocks a turn), anti-cheat KEEP (dice resolution on-path, audit trail may go async), faction/living-world KEEP ADAPT to async ticks merged next turn, agent routing KEPT as a model-side Jev decision step with server-side dispatch table and explicit-signals-only modal conclude guards. The draft ZFC amendment (`~/workspace/plans/zfc-skill-model-amendment-proposal.md`) is **NOT in force** and was not applied; effects it would have are flagged only in §6.
- **Caller method:** local `grep` over `~/workspace/repos/worldarchitect.ai/mvp_site/**/*.py` (prod files distinguished from `tests/`), plus `main.py` route registration and template-render checks. A "zero prod callers" claim means zero matches outside the defining file and outside `tests/`; test-only callers are named as such, not counted as prod reachability.
- **Headline answer to the assignment's specific questions:** push is **NOT dead** — `push/routes.py:register_routes` is called from `main.py:2632-2634`, and the obligation path is live via `durable_intent.py:340`, `firestore_service.py:8529-8553`, `llm_parser.py:2418` — but the shipped `push/config.json` is `enabled: false` with empty scheduler/APNs fields, so the sender/sweep path is inert by configuration, not by dead code. `tools.py` is a 1-line docstring stub (no symbols, no importers). `mvp_site/__init__.py` is the lazy-alias package init (10 legacy aliases); it is load-bearing for `from mvp_site import …` imports across the tree.

## Verdict summary by file

| File | Verdict |
|---|---|
| push/__init__.py, push/apns.py, push/content.py, push/registrations.py, push/routes.py, push/sender.py, push/config.json, push_delivery_obligation.py | KEEP (config.json KEEP as inert-by-default; see §1 caveat) |
| config/__init__.py, config/paths.py | ADAPT out of prod tree to test tooling (test-only consumer) |
| analysis/*.py (4) | DELETE from prod tree (test/analysis-only, broken paths) |
| data/dragon_knight_canonical_description.txt, data/srd_classes/* (13 + index.json) | KEEP |
| evidence/* (6 files) | KEEP as evidence (not runtime) |
| roadmap/*.md (4) | DELETE/ARCHIVE from prod tree (planning scratchpads) |
| world/README.md | ADAPT (fix stale archive section); world/banned_names.md, world/world_assiah_compressed.md KEEP |
| templates/base.html, templates/settings.html | KEEP |
| static/v2/index.html | DELETE (orphaned stub; referenced assets absent, zero prod references) |
| bin/LICENSE.chromedriver | KEEP (non-runtime licence text) |
| assets/DejaVuSans.ttf | KEEP |
| docs/generalized_file_caching.md, docs/rate-limit-firestore-allowlist-20260917.md, docs/v1_vs_v2_comparison/* (3 files) | KEEP as docs/evidence (rate-limit doc's design now implemented; see row) |
| .gcloudignore | KEEP; AGENTS.md ADAPT (fix dangling refs); CODE_REVIEW_SUMMARY.md DELETE/ARCHIVE (stale counts); DEPLOYMENT.md KEEP; Dockerfile ADAPT (see §4); FALLBACK_REVIEW.md ADAPT (2 stale refs); PARALLEL_DUAL_PASS_INTEGRATION.md DELETE/ARCHIVE (dead feature doc); README.md ADAPT (Flask 2.x claim); README_FOR_AI.md ADAPT (2025-07-07 issue stale); TYPING_GUIDE.md KEEP; UNIFIED_API_IMPLEMENTATION.md DELETE/ARCHIVE (subject file absent) |
| __init__.py | KEEP; avatar_image_gen.py ADAPT (confirm run-1); document_generator.py ADAPT (confirm run-1, with one correction); equipment_display.py ADAPT (confirm run-1, strengthened); install.sh ADAPT (misnamed, AGY-only); mypy.ini KEEP; package-lock.json KEEP; package.json KEEP; pytest.ini ADAPT; requirements-test.txt KEEP; requirements.txt ADAPT (see §4); run_integration_tests.sh DELETE from prod tree (test runner, broken dir); portrait_generator_agent.py ADAPT (confirm run-1); portrait_model_compare.py DELETE (confirm run-1); portrait_timing.py ADAPT (confirm run-1); tools.py DELETE (empty stub) |

## Per-file tables

Conventions: "A" = Pass A, "B" = Pass B. Line numbers are from the local tree. Grouped rows name every symbol in the group.

### push/__init__.py (1 line, 0 symbols) — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| File (docstring: "Server-owned completion notification infrastructure.") | Package marker; imported implicitly by every `mvp_site.push.*` import | A: without it the package does not import. B: transport (completion notifications), no domain decision | KEEP |

### push/apns.py (191 lines, 10 AST units) — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `_PRIVATE_HTTP`, `_AUTH_LOCK`, `_AUTH_CACHE`, `HTTP_TIMEOUT_SECONDS`, `_LOG` (ll.20-24) | Internal to file | A: auth-cache/timeout bounds. B: bounded capacity + credential hygiene (private-token filtering) | KEEP |
| `_PrivateHTTPFilter.filter` (ll.27-28) | `APNs` internals | A: redacts tokens from logs. B: authorization hygiene, no domain value | KEEP |
| `native_token` (l.43) | `push/registrations.py:12` | A: validates APNs device-token shape for registration. B: transport validation, not a game fact | KEEP |
| `event_identity` (l.52) | `push_delivery_obligation.py:176` | A: stable event id for the obligation fence. B: durable-write identity, no recomputation | KEEP |
| `Outcome` (l.66); `APNs.__init__` (l.72), `APNs._authorization` (l.84), `APNs.close` (l.107), `APNs.send` (l.110) | `push/sender.py:373` (via adapter), `:430`, `:503` (construction) | A: the only APNs transport; deleting it kills push delivery. B: provider tool execution; signing is authorization. Note: `send` is reachable only through the sender's sweep/wake path, which is config-gated (see config.json row) — reachable, not dead | KEEP |

### push/content.py (65 lines) — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `_CREDENTIAL` (l.8) | Internal | A: screens lock-screen text for credential-shaped strings. B: disclosure guard, conservative by its own comment (l.7) — it does not guarantee safety, and does not claim to | KEEP |
| `_PlainText.__init__/handle_starttag/handle_endtag/handle_data` (ll.16-33) | `snippet` only | A: HTML→plain-text for lock screen. B: display formatting of an explicitly supplied narrative string, no invented content | KEEP |
| `snippet` (l.38) | `push_delivery_obligation.py:11,89`; `llm_parser.py:2400` (import of `push.content`) | A: bounded 160-code-point excerpt + `ok/empty/unsafe` status staged on the obligation. B: pure projection of model-authored narrative with a credential screen; the `unsafe → ""` branch drops rather than rewrites | KEEP |

### push/registrations.py (286 lines) — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `COLLECTION` (l.14), `RegistrationConflictError` (l.17) | `push/routes.py`, `push_delivery_obligation.py:155` | A: Firestore collection name + conflict signal for registration races. B: durable writes + authorization error, no domain logic | KEEP |
| `client_registration_id` (l.21), `_same_identity` (l.31), `is_identifier` (l.35), `_owned_active` (l.45), `eligible` (l.57) | Routes (ll.31,67,98) + `push_delivery_obligation.py:159` (`eligible`) | A: owner/scope/eligibility gate — without it any installation could claim another user's notifications. B: authorization, the strongest ZFC-allowed category | KEEP |
| `register_or_recover_installation` (l.72) + inner `apply` (l.124) | `push/routes.py:38` (POST /api/push/registrations) | A: creates/recovers an installation's registration transactionally. B: durable write + auth | KEEP |
| `resolve_registration` (l.146) | `push_delivery_obligation.py:39` | A: the obligation path's owner-scoped lookup. B: authorization-gated read | KEEP |
| `_update_registration` (l.172) + inner `apply` (l.190) | Internal to rotate path | A: token rotation transaction. B: credential custody | KEEP |
| `rotate_registration_token` (l.211) | `push/routes.py:67` (PATCH) | A: rotates a device token without changing identity. B: authorization | KEEP |
| `revoke_registration` (l.239) + inner `apply` (l.273) | `push/routes.py:98` (DELETE) | A: revocation, required for a notification feature to be safe. B: authorization | KEEP |

### push/routes.py (112 lines) — KEEP (this is the push liveness proof)
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `_get_db` (l.9) | Internal to the three handlers | A: lazy Firestore load only when a registration request needs it. B: durable-write plumbing | KEEP |
| `register_routes` (l.16) + nested `create_push_registration` (l.23), `rotate_push_registration` (l.57), `revoke_push_registration` (l.87) | **Called from `main.py:2632-2634`** (`from mvp_site.push.routes import register_routes as register_push_routes; register_push_routes(app, check_token=…, limit=…)`) — push is registered on the app, not dead. Mounts POST /api/push/registrations, PATCH/DELETE /api/push/registrations/<id>, and via `sender.register_routes` (l.19) POST /internal/push/completions/sweep | A: the only registration surface. B: authenticated transport + authorization; handlers never echo storage exceptions (ll.52-53, "can contain a private token") | KEEP |

### push/sender.py (506 lines) — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| Module constants: `firestore_service`, `registrations` (lazy, ll.24-25), `MAX_CLAIMS`, `CONCURRENCY`, `WORK_SECONDS`, `SEND_RESERVE_SECONDS`, `LEASE_SECONDS`, `TTL`, `STARTED_TTL`, `WAKE_SECONDS`, `APNS_ENVIRONMENTS_BY_SCOPE`, `APNS_TOPIC`, `_WAKE_SLOTS`, `_STORAGE_DEADLINE` (ll.27-44) | Internal; `registrations` lazy import avoids a cycle | A: bounded sweep/wake budgets. B: bounded capacity, explicitly fenced | KEEP |
| `load_config` (l.47), `valid_config` (l.53) | `register_routes` (l.478), `consume_one` (l.417), `submit_wake` (l.446); `valid_config` also tested in `tests/test_push_sender.py:833,850` | A: config load from `push/config.json` (or `PUSH_CONFIG_PATH`) + fail-closed validation (all scheduler/APNs fields non-empty, scope match, `K_SERVICE` match, signing key readable). B: authorization + bounded capacity. Consequence: the shipped config (see below) can never pass, so sweep is inert until a real config is deployed — by design, not by accident | KEEP |
| `_now`, `_timestamp`, `_read`, `_slot`, `_update`, `_terminal`, `_eligible` (ll.89-139) | Internal to claim/prepare/acknowledge | A: lease/fence helpers for the obligation consumer. B: durable-write fencing, no domain recomputation | KEEP |
| `claim` (l.220) + inner `operation` (l.221), `prepare_send` (l.264) + inner `operation` (l.265), `acknowledge` (l.289) + inner `operation` (l.290) | Internal: `_deliver` (l.364) calls them; no external prod caller — internal pipeline stages, not dead code | A: claim/lease/ack is what makes delivery at-most-once-ish across scheduler retries. B: durable writes | KEEP |
| `candidates` (l.314) + inner `pages` (l.332) | `sweep` (l.386) only | A: paged scan for due obligations. B: durable-read scan, bounded by deadline | KEEP |
| `_deliver` (l.364) | `sweep` + `consume_one` | A: one obligation → one APNs send + ack. B: tool execution on server-authored snippet only | KEEP |
| `sweep` (l.379) + inner `run` (l.380) | `register_routes` sweep_completions handler (l.504); path referenced by `bq_request_logger.py:266` (route allowlist) | A: scheduler-driven durable recovery — the "lost wake never replaces durable recovery" guarantee (`submit_wake` docstring). B: background execution; no turn path waits on it | KEEP |
| `consume_one` (l.417) + inner `run` (l.425) | `submit_wake` (l.460) only | A: single-obligation fast path for the wake. B: same fence as sweep, budget starting at queue admission | KEEP |
| `submit_wake` (l.446) | `firestore_service.py:8900`, `push_delivery_obligation.py:194` | A: non-blocking bounded admission; returns False when disabled/unconfigured/slots full. B: bounded capacity; a lost wake is explicitly non-fatal | KEEP |
| `register_routes` (l.475) + nested `sweep_completions` (l.479) | `push/routes.py:19` → `main.py:2632` | A: mounts the scheduler-only sweep endpoint (OIDC `verify_scheduler_oidc`, subject match, 401/503 fail-closed). B: authorization-gated background transport | KEEP |

### push/config.json — KEEP (inert-by-default; read the caveat, not just the verdict)
| Unit | Evidence | A / B | Verdict |
|---|---|---|---|
| Whole file: `enabled: false`, empty `scheduler_audience/service_account/subject`, empty `apns_key_id/team_id/signing_key_path`, `backend: worldarchitect-ai`, `environment/deployment_scope: dev`, `apns_environment: production`, `apns_topic: ai.worldarchitect.app` | Loaded by `push/sender.py:47-50`. `valid_config` (sender.py:53) requires every scheduler/APNs field non-empty and `deployment_service == K_SERVICE`, so this file can never validate — sweep returns 503 `disabled`/`unconfigured`, `submit_wake` returns False. Registration routes still work (they do not require sender config except the optional APNs validation in `routes.py:44-46`). No credential/key material is present in the file (all empty strings) — nothing to redact | A: push delivery is off until a real config is deployed; the registration + obligation-staging path is live regardless. B: fail-closed configuration is the correct shape; do NOT "fix" it by enabling it in-tree | KEEP |

### push_delivery_obligation.py (199 lines) — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `COLLECTION` (l.14), `STATUS_PENDING` (l.48) | `push/sender.py:21`, `firestore_service.py`, routes | A: obligation collection/status vocabulary. B: durable-write constants | KEEP |
| `configured_scope` (l.17) | `push/routes.py:31,67,98`, `push/sender.py:73`, `durable_intent.py` path | A: server-owned (backend, environment) identity from `constants.PUSH_BACKEND_IDENTITY/PUSH_ENVIRONMENT_IDENTITY`, never from the request. B: authorization | KEEP |
| `resolve_active_registration` (l.30) | `durable_intent.py:340`, `firestore_service.py:8532` | A: owner-scoped ACTIVE registration lookup for staging. B: authorization-gated read | KEEP |
| `obligation_reference` (l.51) | `publish_started` + `tests/test_push_delivery_obligation.py:41` | A: canonical `turn_delivery_obligations/<requestId>` ref via sanitized idempotency key. B: durable-write identity | KEEP |
| `stage_delivery_obligation` (l.68) | `firestore_service.py:8553` (inside a batch alongside the receipt fence) | A: merges completion fields + `snippet()` excerpt onto the obligation doc. B: durable write of server-computed transport metadata; the snippet is a projection, not a narrative rewrite | KEEP |
| `publish_started` (l.113) + inner `read` (l.132), `operation` (l.139) | `llm_parser.py:2418` (first-narrative emission) | A: publish-once started event (receipt/intent fence, 15s budget) then `sender.submit_wake` (l.194). B: durable write + bounded wake; on the turn path it is a Firestore transaction, so §6(1) async review applies if it ever blocks a turn — currently bounded at 15s and fenced, flag for the turn-path owner, not a verdict change | KEEP |

### config/__init__.py (1 line: `# Config package`) — ADAPT (with paths.py)
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| File | Package marker only | A: needed only if `config/` holds a module. B: no domain content | ADAPT: moves/deletes with `config/paths.py` (below); do not keep an empty package behind |

### config/paths.py (194 lines) — ADAPT out of prod tree (test-only)
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `PathConfig.__init__/base_dir (get+set)/frontend_dir/frontend_js_dir/frontend_css_dir/frontend_styles_dir/tests_dir/test_data_dir/static_dir/app_js/api_js/auth_js/index_html/main_css/validate_paths/get_relative_path` (ll.21-127) | **Zero prod callers.** Only caller found: `tests/auth/test_auth_resilience.py:21` (`from config.paths import PATHS` — note the test imports it as top-level `config`, not `mvp_site.config`, so even that import path is inconsistent with the package location). Its own docstring usage example (`from config.paths import PATHS`) matches the test, not prod code | A: deleting it breaks no player capability; no prod code resolves paths through it (prod uses `frontend_release.py`/`main.py` serving logic). B: path constants are transport-adjacent but unreferenced = dead by the §4 reference-count rule | ADAPT: move to test tooling (precedent: gateway-call-path's `arch.py` ADAPT out of `mvp_site/`); DELETE from the prod tree if no test owner claims it |
| `PATHS` (l.136), `get_test_file_path` (l.140), `validate_installation` (l.164), `__main__` block (ll.183-194) | Same test-only evidence; `validate_installation`/`__main__` are dev diagnostics | A: test/dev helpers. B: same as above. Note the docstring claim "single source of truth for all file and directory paths used throughout the application and tests" is false for the application (zero prod users) — true only, loosely, for one test | ADAPT (same move) |

### analysis/capture_actual_llm_responses.py (258 lines) — DELETE from prod tree (test/analysis-only)
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `project_root` (l.20), `capture_sariel_llm_responses` (l.34), `__main__` (l.245) | Zero prod callers; zero test callers found. Imports `integration_test_lib` (unqualified, l.14) and `main.create_app` — a one-off capture harness, not a module. Its own `project_root` computation appends `"mvp_site"` to the file's directory, which is already inside `mvp_site/` — a stale path bug consistent with the file having been moved | A: deleting it removes only a historical capture run. B: analysis tooling, not transport/durable-writes/gameplay; also violates the `mvp_site/AGENTS.md` routing rule quoted below (exploratory files do not belong in `mvp_site/`) | DELETE from prod tree (archive with its output, if the output is wanted) |

### analysis/capture_llm_responses.py (224 lines) — DELETE from prod tree
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `project_root` (l.21), `capture_sariel_responses` (l.28), `__main__` (l.212) | Zero prod/test callers. Imports `test_integration.integration_test_lib` (l.19) — a path that does not exist in this tree (no top-level `test_integration/` found; `run_integration_tests.sh` references the same missing dir, see §4) | A/B: same as above; a second, near-duplicate Sariel capture (see duplication note in §2: this file vs `capture_actual_llm_responses.py` vs `run_real_sariel_capture.py` all capture the same Sariel replay) | DELETE from prod tree |

### analysis/run_real_sariel_capture.py (256 lines) — DELETE from prod tree
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `run_sariel_capture_in_main_project` (l.15), `capture_responses` (l.44, nested script string) | Zero prod/test callers. Hardcodes `/home/jleechan/projects/worldarchitect.ai/mvp_site` (l.22) — a developer-workstation path that cannot work in this tree or in Cloud Run | A/B: same as above; the hardcoded path alone proves it is not a shipped capability | DELETE from prod tree |

### analysis/run_sariel_replays.py (230 lines) — DELETE from prod tree
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `project_root` (l.15), `run_single_sariel_test` (l.19), `analyze_replay_results` (l.56), `main` (l.145) | Zero prod/test callers. Shells out to `source /home/jleechan/projects/worldarchitect.ai/venv/bin/activate` + `python3 -m unittest tests.test_sariel_campaign_integration…` — workstation-only, and its "10 replays for statistical significance" purpose is analysis, already documented in `sariel_llm_responses_documented.md` | A/B: same as above | DELETE from prod tree |

### analysis/sariel_llm_responses_documented.md (185 lines) — KEEP as analysis evidence
| Unit/sections | Evidence | A / B | Verdict |
|---|---|---|---|
| Whole file (26 headings: executive summary claiming a 50% entity-tracking desync rate, "Cassian Problem" examples, data-source list, environment limitations) | Referenced by no code (documentation). Its own limitations section is candid: Flask dependency issues prevented real-time capture, Gemini 503s blocked replays, data is "patterns + limited narrative examples" — so the 50% figure is a historical analysis claim, not a live metric. Sources it cites (`sariel_integration_test_results.json`, `campaign_snapshot_sariel_v2.json`, `sariel_desync_analysis_report.md`) are not in this tree | A: deleting it loses historical failure analysis, not a player capability. B: docs are not code; the candid limitations keep it from being misleading | KEEP as evidence (do not cite the 50% figure as current without re-measurement) |

### assets/DejaVuSans.ttf — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| File (font bytes) | `document_generator.py:552` (`FONT_FILENAME`), loaded at `:605` with a logged fallback to a core font at `:610` if absent | A: Unicode-capable PDF font for exports; fallback exists, so absence degrades rather than breaks. B: presentation asset for the export promise | KEEP |

### bin/LICENSE.chromedriver — KEEP (non-runtime)
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| File (Chromium licence text, 2015) | Zero code references to `bin/LICENSE` or to a chromedriver binary in prod code; no chromedriver binary ships in `bin/` (only this licence). Selenium is in `requirements.txt` but its prod use is in `testing_ui/` (outside this area) | A: deleting it changes no player capability. B: licence text is not code; keeping an orphaned licence is harmless and arguably required if any tooling ever bundles chromedriver | KEEP (flag: orphaned — if chromedriver is confirmed unused everywhere, the file can go with that tooling; not a prod-code verdict) |

### data/dragon_knight_canonical_description.txt (470 lines) — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| File (campaign summary + world history for Ser Arion / Celestial Imperium) | `campaign_template_dragon_knight.py:14` (path) + `:18` (`verify_dragon_knight_canonical_hash`); hash-pinned, per `constants.py:2550-2553` | A: the canonical Dragon Knight premade description; deleting it breaks the premade. B: prompt/data content authored for the product, not a server recomputation | KEEP |

### data/srd_classes/index.json — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| File (`dnd5e` map: 12 class names → filenames) | Consumed via `class_lookup.py:35` (`srd_classes` corpus dir) | A: the lookup index for SRD class reference. B: data index, no transform | KEEP |

### data/srd_classes/*.md (12 class files + custom_class_instruction.md) — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `barbarian.md` (149 lines), `bard.md` (171), `cleric.md` (182), `druid.md` (247), `fighter.md` (139), `monk.md` (192), `paladin.md` (247), `ranger.md` (207), `rogue.md` (143), `sorcerer.md` (220), `warlock.md` (373), `wizard.md` (169) | `class_lookup.py` corpus (l.35); each file self-labels "D&D 5e SRD 5.1 — 5e Core Rules" (e.g. `barbarian.md:5`) | A: SRD reference data the class system reads; the model could recite SRD text, but pinned reference data is the product's rules grounding. B: data, not code; no server decision | KEEP |
| `custom_class_instruction.md` (36 lines) | `class_lookup.py:42` (`_CUSTOM_HANDLER_FILE`), used at `:140-141` | A/B: same as above, for custom classes | KEEP |

### evidence/* (6 files) — KEEP as evidence (not runtime)
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `dead_npc_hallucination/proof.json` + `proof.sha256` | No code reads it (evidence artifact; failure_id `dead-npc-hallucination-v1`, GodModeAgent prompt evidence). Hash sidecar present | A: deleting it loses failure evidence, not capability. B: evidence is not runtime | KEEP |
| `god_mode_directive_persistence_8103/proof.json` (PR 8132, issue 8103) | No code reads it. **No `.sha256` sidecar** (unlike the other two proof dirs) — an evidence-hygiene gap, not a code defect | A/B: same | KEEP (add the missing sidecar or note why it has none) |
| `god_mode_json_wire/README.md` + `proof.json` + `proof.sha256` | No code reads it (PR 7150 wire-format evidence). README's claim that `_parse_god_mode_data_string` "was deleted from `mvp_site/world_logic.py`" is a historical claim about that PR, stated as past tense — consistent with a PR-evidence doc, not a live API claim | A/B: same | KEEP |

### roadmap/*.md (4 scratchpads) — DELETE/ARCHIVE from prod tree
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `scratchpad_dev1314.md` (303 lines: planning-block cleanup subagent results) | No code references; branch scratchpad, not a shipped doc | A: planning notes. B: docs are not code, but prod-tree docs that read as live plans mislead; the audit scope note (§7 of the main ledger) already puts roadmap outside removal batches — these are appendix material, and the correct disposition is archive outside `mvp_site/`, not retention as prod docs | DELETE/ARCHIVE from prod tree |
| `scratchpad_parallel_dual_pass_optimization.md` (224 lines) | Same; its subject (parallel dual-pass) is the dead `frontend_v1/parallel_dual_pass.js` path (frontend run-1 DELETE) and `PARALLEL_DUAL_PASS_INTEGRATION.md` (below) | A/B: same; keeping it alongside the integration doc preserves the impression the feature is live | DELETE/ARCHIVE |
| `scratchpad_story_mode_improvements.md` (55 lines, "In development", checklist items marked "✅ Pending" — self-contradictory status markers) | Same | A/B: same; status markers are stale/incoherent | DELETE/ARCHIVE |
| `scratchpad_test-organization-improvements.md` (98 lines, "IN PROGRESS", 9 failing tests, PR TBD) | Same | A/B: same; a TBD-PR work note, not a live spec | DELETE/ARCHIVE |

### world/README.md (87 lines) — ADAPT (fix, don't delete)
| Unit/sections | Evidence | A / B | Verdict |
|---|---|---|---|
| Overview + `world_assiah_compressed.md` + `banned_names.md` sections | Accurate: both files exist and are loaded (`world_loader.py:29-32`) | A/B: accurate docs | KEEP (those sections) |
| `archive/` section (ll.25-38: lists `character_merge_analysis.md`, `characters_enhanced.md`, `deletion_analysis.md`, `factions_enhanced.md`, `geography_enhanced.md`, `timeline_consolidated.md`, `world_mechanics_enhanced.md`) | **Stale: `mvp_site/world/archive/` does not exist in this tree.** The README describes files that are not shipped | A/B: a doc that inventories absent files misleads anyone following it | ADAPT: delete the archive section (or restore the archive outside the shipped tree and say where) |

### world/banned_names.md (74 lines) — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| File (primary + extended banned-name lists; "MASTER DIRECTIVE … ABSOLUTELY FORBIDDEN") | `world_loader.py:32,35,59` (`load_banned_names`, `load_banned_names_section_for_system_instruction`); injected by `agent_prompts.py:1682-1704` (`_add_banned_names_to_system`) | A: name-filter data for prompts; the model could ignore it, but the product promise is that it is injected. B: prompt data, not a server decision — note the list is a style/cliché filter ("overused by LLMs"), not a safety filter, despite the "MASTER DIRECTIVE" wording | KEEP |

### world/world_assiah_compressed.md (570 lines) — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| File (51 headings; header claims source 85k tokens → ~45k, 47% reduction; "Year 11 of the New Peace, Kythorn Day 2"; Sariel 15, twins 18, companions 16) | `world_loader.py:29,31` (`WORLD_ASSIAH_PATH`); gated on `use_default_world` per `agent_prompts.py:1657-1661` | A: default-world prompt data. B: prompt data. The token-reduction header is a historical compression claim, not verifiable from this file alone — flagged as unverified, not false | KEEP |

### templates/base.html (46 lines) — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| File (`title`/`head`/`content`/`scripts` blocks, ll.8,20,33,44) | Extended by `templates/settings.html:1`; rendered only via the settings route (below). No other template extends it in-tree | A: the shell for the one server-rendered page. B: presentation markup, no domain logic | KEEP |

### templates/settings.html (382 lines) — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| File (sections: save/error messages, OpenRouter card, AI Provider & Model radios gemini/openrouter/cerebras, BYOK key sections, scene settings per l.264) | Rendered by `main.py:7729` (`settings_page`, GET /settings, "auth handled client-side"). Note the dual-surface caveat: the shipped SPA (`frontend_v1/js/settings.js`, frontend ADAPT) is the other settings surface; this Flask template is the legacy/server-rendered one. Both existing is a product-surface duplication to resolve at product level, not a reason to delete this file sight-unseen — it is the only thing /settings serves | A: deleting it 404s /settings. B: presentation + settings transport; provider/key fields are user input, not server decisions | KEEP |

### static/v2/index.html — DELETE (orphaned stub)
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| File (Vite-style entry: `./assets/index-BgGmhWH9.js`, `./assets/vendor-DJG_os-6.js`, `./assets/ui-CbO0uvlw.js`, `./assets/index-BOOzAEaf.css`, `<div id="root">`, title "WorldAI - Forge Your Legend") | **Zero prod references** to `static/v2` in `*.py` (the `/static/<path>` route at `main.py:2095` serves `frontend_v1` backward-compat paths, not a `v2` bundle). **The referenced `./assets/` files do not exist in-tree** — `static/v2/` contains only `index.html`. `frontend_release.py` discusses Expo web exports, but no code in this area stages assets into `static/v2/` | A: deleting it removes a page that cannot render (its JS/CSS are absent). B: an unservable bundle stub is not transport | DELETE from the shipped tree (if a deploy step stages a real Expo export here, that step — not this stub — is the artifact, and it should be gitignored/staged, not tracked as a lone index.html) |

### .gcloudignore — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| File (excludes `__pycache__`, venv, tests artefacts, `docs/`, `analysis/`, `coverage_report.txt`, `CODE_REVIEW_SUMMARY.md`; re-includes `!prompts/*.md`) | Consumed by `gcloud builds submit` / Cloud Run deploys (the Dockerfile's `COPY mvp_site/` + cache-busting step depends on prompts surviving the upload, hence the `!prompts` exception) | A: deploy hygiene; the prompts exception is load-bearing. B: not gameplay. Note it also excludes `docs/` and `analysis/` from deploys — consistent with this report's DELETE/ARCHIVE verdicts for those dirs (they are not needed at runtime) | KEEP |

### AGENTS.md (16 lines) — ADAPT (fix dangling references)
| Unit/sections | Evidence | A / B | Verdict |
|---|---|---|---|
| Directory Execution / File Routing / User stories sections | Root-execution invariant (`from mvp_site import …` breaks inside `mvp_site/`) is true and load-bearing (see `__init__.py` aliases). Test-placement rule is true for the tree. BUT: it points at `../AGENTS.md` (symlinked from `CLAUDE.md`), `../.claude/skills/worldai-mcp-server-usage`, `../docs/user-stories-ui/INDEX.md`, `../.claude/skills/evidence-standards.md` — in this tree, repo-root `AGENTS.md`/`CLAUDE.md` exist at the workspace root (injected context), but the `.claude/skills/*` and `docs/user-stories-ui/` targets were not verified in this area's scope; the routing rule itself ("Reference, demo, or exploratory files do not belong in `mvp_site/`") is the rule the `analysis/` files violate (see §2) | A/B: accurate as a routing rule; stale as a pointer document if any target is absent | ADAPT: verify/repair the four outbound links; keep the routing rule (it justifies the analysis/roadmap dispositions) |

### CODE_REVIEW_SUMMARY.md (690 lines) — DELETE/ARCHIVE (stale counts throughout)
| Unit/sections | Evidence | A / B | Verdict |
|---|---|---|---|
| Executive summary + "Files Examined and Line Counts" (33 headings) | Claims: 132 files, ~15,000+ lines; `main.py` 985 lines, `llm_service.py` 1,449, `firestore_service.py` 467, `game_state.py` 373, `constants.py` 174, `logging_util.py` 208; "All 34 major Python files"; frontend `static/app.js` ~2,000+, `static/index.html` ~500, `static/style.css` ~800; 132 test files; tables for `firestore/campaigns.py`, `firestore/stories.py`, `firestore/users.py`, `firestore/state_updates.py` (a `firestore/` package that does not exist in this tree). **Actually true in this tree:** `main.py` 9,634 lines (gateway-call-path), `llm_service.py` 12,030, `firestore_service.py` ~8,900+ (line refs to 8900 exist), the shipped frontend is `frontend_v1/` not `static/` (except the orphaned `static/v2/index.html`), and `mvp_site/` holds ~400+ Python files, not 34/132. Every line count is stale by an order of magnitude | A/B: a review doc whose every quantitative claim is false is worse than no doc — it will misdirect the next reviewer | DELETE/ARCHIVE from the prod tree (keep in git history; do not "update" it in place — a fresh review supersedes it) |

### DEPLOYMENT.md (20 lines) — KEEP
| Unit | Evidence | A / B | Verdict |
|---|---|---|---|
| Whole file (defers to the `gcp-deployment` skill + `scripts/shared_config.sh`, `scripts/deploy_common.sh`, `deploy.sh`, `.github/actions/deploy-mvp-site/action.yml`; forbids copying sizing/Gunicorn values into docs) | Consistent with the Dockerfile's actual entrypoint (`gunicorn -c gunicorn.conf.py main:create_app()`) in that it refuses to restate worker/thread values — it makes no falsifiable capacity claim of its own. The skill/scripts it defers to are outside this area, so their existence was not re-verified here (flagged, not asserted) | A/B: a pointer doc that correctly refuses to duplicate executable config | KEEP |

### Dockerfile (single stage, `python:3.11-slim` → `gunicorn -c gunicorn.conf.py main:create_app()`) — ADAPT
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| Stage 1 (only stage): base + `appuser` (uid 10001) + `git procps` + `COPY mvp_site/requirements.txt` + pip install + fastembed preflight (`scripts/preflight_model_docker.py`, `scripts/preflight_model.py`, `FASTEMBED_CACHE_PATH=/opt/fastembed_cache`, `HF_HUB_OFFLINE=1`) + `COPY infrastructure/`, `mvp_site/`, `testing_mcp/`, `testing_utils/`, `deployment/`, `docs/openrouter-evidence/` + cache-busting (`scripts/cache_busting.py /app/mvp_site/frontend_v1`) + `WORKDIR /app/mvp_site` + CMD | The deploy entrypoint; `WORKDIR /app/mvp_site` + `PYTHONPATH=/app` make `from mvp_site import …` resolve. `main:create_app()` exists (gateway-call-path). Serve path is real | A: the shipped image definition. B: transport/packaging. ADAPT items (see §4): (1) it provisions the fastembed model cache for the intent classifier that this audit deletes in full — the preflight steps are dead weight once the classifier goes, and they bloat the image; (2) it copies `testing_mcp/` + `testing_utils/` into the production image (test code in prod image); (3) the `GIT_COMMIT` manifest pins only `llm_parser.py`'s hash, not the tree — a truthfulness gap in its own "truthful source manifest" claim | ADAPT: drop fastembed preflight with the classifier, drop test dirs from the prod image, widen or honestly scope the manifest claim |

### FALLBACK_REVIEW.md (33 lines) — ADAPT (two stale references)
| Unit/sections | Evidence | A / B | Verdict |
|---|---|---|---|
| Runtime/server code section (frontend routing, MCP memory client, narrative parsing, game-state reconstruction, Firestore doc-id) | Frontend-routing claim (SPA fallback + 410 for stale bundles) matches `main.py`'s serving behaviour described in the doc; narrative-parsing fallback claim is consistent with schema-parsing's findings (multi-layer salvage). `mcp_memory_real.py` claim (fail-fast, `MCPMemoryError`) is consistent with state-storage's DELETE-in-full verdict for that shim — the doc describes its behaviour accurately even though the file is slated for deletion | A/B: broadly accurate for live code | KEEP (those sections) |
| Tests/mocks + frontend-test sections | Claims `frontend_v2/src/utils/errorHandling.ts` — **no `frontend_v2/` tree exists in this area's scope** (shipped frontend is `frontend_v1/`). Also describes `mcp_memory_real.py` fallbacks as current while state-storage deletes that file | A/B: stale references misdirect a fallback audit | ADAPT: delete/correct the `frontend_v2` reference and note the `mcp_memory_real.py` deletion |

### PARALLEL_DUAL_PASS_INTEGRATION.md (75 lines) — DELETE/ARCHIVE (dead feature doc)
| Unit | Evidence | A / B | Verdict |
|---|---|---|---|
| Whole file (integration steps: `main_parallel_dual_pass.py` backend endpoints, `static/parallel_dual_pass.js/css`, `add_parallel_dual_pass_routes(app, get_campaign_info)`, `handleInteractionParallel`, `entity_validator.validate` enhancement flag, "50% faster", "No additional compute cost") | **Every artefact it integrates is absent or dead:** no `main_parallel_dual_pass.py` in `mvp_site/`; `static/parallel_dual_pass.*` do not exist (only `frontend_v1/parallel_dual_pass.js/css`, which frontend run-1 DELETEs as unloaded); `frontend_v1/app.js` never calls `handleInteractionParallel` (frontend §2). The "no additional compute cost" claim is also false on its face for a second-pass enhancement path. The roadmap scratchpad for the same feature (above) is the same story | A/B: a how-to for a feature that does not ship, presenting dead code as the integration path | DELETE/ARCHIVE from the prod tree |

### README.md (595 lines) — ADAPT (one version claim + staleness)
| Unit/sections | Evidence | A / B | Verdict |
|---|---|---|---|
| Overview, architecture, components, testing, features, MCP tools sections (55 headings) | Broadly accurate: Flask backend, vanilla JS frontend, Gemini/Firestore/Firebase, MCP tools list (`create_campaign`, `get_campaign_state`, `process_action`, `update_campaign`, `export_campaign`, `get_campaigns_list`, settings tools) matches the MCP surface described elsewhere | A/B: useful orientation | KEEP (those sections) |
| "Python 3.11 with Flask 2.x" (l.36) | **Actually true:** Python 3.11 (Dockerfile, mypy.ini) but **Flask 3.1.3** (`requirements.txt:2`). The "2.x" claim is stale | A/B: a version claim a new dev will act on (e.g. Flask 2.x API assumptions) | ADAPT: correct to Flask 3.1.3 |
| "Bootstrap 5.x" / theme system (light/dark/fantasy/cyberpunk) (ll.50,533) | Frontend ships `frontend_v1/themes/{base,default,fantasy}.css` (frontend KEEP) — no cyberpunk theme file in the shipped set; Bootstrap itself is a CDN/legacy claim not evidenced in `frontend_v1/index.html`'s shipped set in this area | A/B: theme list overclaims | ADAPT: correct the theme list to the shipped set |

### README_FOR_AI.md (82 lines) — ADAPT (stale known-issue)
| Unit/sections | Evidence | A / B | Verdict |
|---|---|---|---|
| JSON-mode architecture (§§1-5: Gemini returns structured JSON, `narrative` extracted, never show raw JSON, data flow Gemini → llm_service → main → firestore → frontend "Scene #" prefix, key files) | Consistent with schema-parsing (`parse_structured_response` is the only true parser) and the shipped flow; the "JSON in logs is not a bug" guidance is still the correct first check | A/B: accurate orientation | KEEP (those sections) |
| "Current Known Issues — JSON Display Bug (as of 2025-07-07)" (§6) | A dated bug report presented as current, with "Investigation needed" questions and no resolution note, 15+ months later. Either it was fixed (then the section misleads) or it is still open (then it needs a current status, not a 2025-07-07 snapshot) | A/B: stale-issue sections rot into false current-state claims | ADAPT: resolve-or-date the section (fixed + link, or restate as open with current evidence) |

### TYPING_GUIDE.md (204 lines) — KEEP
| Unit/sections | Evidence | A / B | Verdict |
|---|---|---|---|
| Overview, mypy config, gradual strategy, `custom_types.py` types, stubs (33 headings) | Consistent with `mypy.ini` in-tree (python 3.11, `ignore_missing_imports`, per-module overrides for `mvp_site.tests/mocks/testing_ui`, strict `disallow_untyped_defs` for `firestore_service`/`main`/`gemini_service` — the guide's "critical modules first" matches). `types-flask`/`types-requests` are in `requirements.txt`. `custom_types.py` exists (gateway-call-path). No falsifiable claim contradicted in this area | A/B: accurate process doc | KEEP |

### UNIFIED_API_IMPLEMENTATION.md (182 lines) — DELETE/ARCHIVE (subject absent)
| Unit | Evidence | A / B | Verdict |
|---|---|---|---|
| Whole file (documents `unified_api.py`: `create_campaign_unified`, `process_action_unified`, `get_campaign_state_unified`, `update_campaign_unified`, …; architecture Flask+MCP → `unified_api.py` → services; "See `unified_api_examples.py`"; "Run `cd mvp_site && python3 test_unified_api_structure.py`") | **None of the three files exists in this tree:** no `mvp_site/unified_api.py`, no `unified_api_examples.py`, no `test_unified_api_structure.py`. The shared logic it describes lives in `main.py` + `world_logic.py` directly (per gateway/state groups), not behind a unified layer | A/B: a design doc for a module that was never merged (or was removed) — following it sends a reader to code that does not exist | DELETE/ARCHIVE from the prod tree |

### __init__.py (125 lines) — KEEP
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `_ALIAS_MODULE_NAMES` (l.19: `structured_fields_utils`, `preventive_guards`, `firestore_service`, `logging_util`, `entity_preloader`, `entity_validator`, `llm_service`, `memory_mcp_real`, `world_loader`, `document_generator`) | Every `from mvp_site import <alias>` in the tree (dozens of files, e.g. `action_resolution_utils.py:12`, `avatar_image_gen.py:24`, `world_logic.py:55`) resolves through this module's `sys.modules` proxies | A: deleting it breaks legacy unqualified imports across the tree (the file's own comment: previously eager imports caused CI failures on heavy deps, hence lazy proxies). B: import plumbing, not a domain decision. Note it still aliases `entity_preloader`/`memory_mcp_real`/`entity_validator`, which state-storage/schema-parsing DELETE — those aliases become dangling after those deletions and must be pruned in the same PRs, or the lazy proxy will raise on first access instead of at import | KEEP (prune aliases as their targets delete) |
| `_LazyModule.__init__/_load_real_module/__getattr__/__setattr__/__delattr__/__dir__` (ll.36-91) | The proxy machinery above; `__setattr__/__delattr__` exist specifically so `unittest.mock.patch` works through the proxy (comment cites `test_lazy_module_thread_safety.py`) | A: load-bearing for tests + lazy loading. B: transport/plumbing | KEEP |
| Module `__getattr__` (l.103), `__all__` (l.114) | Same alias surface | A/B: same | KEEP |

### avatar_image_gen.py (1,563 lines, 48 AST units) — ADAPT — run-1 CONFIRMED
Run-1 (frontend §1 + §4.4): ADAPT — keep one provider call path + prompt assembly, slim resolver/preview/forensics sprawl. **Confirmed in full** on re-read: the file is live (see callers), its core is tool execution + prompt assembly, and its sprawl is exactly the resolver/preview/forensics set run-1 named. No challenge.
| Unit group (every symbol named) | Callers/entry | A / B | Verdict |
|---|---|---|---|
| Error/bound constants: `ERROR_PROVEN_BEFORE_SEND`, `ERROR_RATE_LIMITED`, `ERROR_AUTH_CONFIG`, `ERROR_POLICY_REJECTED`, `ERROR_INVALID_RESPONSE`, `ERROR_OUTCOME_UNKNOWN`, `FAILURE_PROVIDER_REJECTED`, `_MAX_PIXELS`, `_JSON_OVERHEAD_BYTES`, `PROVIDER_ERROR_LOG_MAX_CHARS`, `bounded_provider_error_text` (ll.37-52) | Internal + `user_portrait_service.py:673` (`ERROR_POLICY_REJECTED`) | A: bounded diagnosable failures. B: bounded capacity + logging | KEEP |
| Contracts: `GeneratedImage`, `PortraitGenerationError.__init__` (ll.61,75-76) | `user_portrait_service.py:17-25`, scene providers | A: image-result contract. B: transport contract | KEEP |
| Prompt-data loaders: `load_portrait_policy`, `load_portrait_style`, `load_portrait_request_guard`, `load_portrait_player_precedence`, `_PROMPTS_DIR`, `_STYLE_PATH`, `_GUARD_PATH`, `_POLICY_PATH`, `_STYLE_PROFILE_FILES` (ll.32-35,97-136) | `portrait_generator_agent.py:17`, `agents.py:5154` (`load_portrait_policy`) | A: template/policy loads for prompt assembly. B: prompt assembly | KEEP |
| Slot/prompt assembly: `_portrait_slot_values`, `_clamp_portrait_slot_values`, `_render_portrait_prompt_from_values`, `build_portrait_prompt` (+ inner `attempt`, l.247), `_SLOT_PATTERN`, `_UNSPECIFIED_SLOT`, `_APPEARANCE_SLOT_REFERENCE` (ll.118-303) | `portrait_generator_agent.py:557` | A: the prompt itself. B: prompt assembly from authored facts; fallback order (player brief first, canon last) refuses to invent appearance — run-1's "most valuable logic", confirmed | KEEP |
| Strict decode: `_bounded_response_bytes`, `_strict_decode_image`, `_decode_portrait_provider_image`, `_openrouter_response_header_summary`, `_log_openrouter_exchange_stages` (ll.303-400) | Internal to generation | A: bounded strict decoding. B: transport safety | KEEP (exchange-stage logging ADAPT to async per §6(1) if on the response path — run-1 §4.4 same) |
| Provider payload sprawl: `build_openrouter_image_provider_preferences`, `resolve_openrouter_image_quality`, `resolve_openrouter_image_resolution`, `effective_openrouter_image_model`, `openrouter_provider_prefs_for_model`, `openrouter_image_payload`, `_OPENROUTER_GROK_RESOLUTIONS`, `OPENROUTER_IMAGE_MODEL_OVERRIDE` (ll.30,519,1107-1220,1155) | `portrait_model_compare.py:76` (override), `scene_illustration_provider.py:55` (override) | A: OpenRouter payload formation is needed. B: six resolvers for one provider's quirks is sprawl — collapse to one payload builder driven by policy data | ADAPT (collapse; keep the payload contract) |
| Preview runtime: `is_portrait_preview_runtime`, `_PORTRAIT_PREVIEW_SERVICE`, `_validate_static_png_passthrough`, `_normalize_static_png`, `portrait_image_dimensions`, `encode_portrait_preview_transfer`, `_is_preview_environment`, `_preview_allows_provider_override`, `_resolve_preview_default_provider_pref` (ll.534-661,1440-1463) | `user_portrait_service.py:74,376`, `portrait_generator_agent.py:534` | A: preview transfer + static-PNG passthrough. B: tool execution, but preview-runtime overrides are a second provider-selection path — fold into the single payload builder | ADAPT (fold in) |
| Transport/session: `_new_session`, `_shared_portrait_http_session`, `warm_portrait_image_transport`, `_provider_http_timeouts`, `_portrait_error_is_retryable`, `_http_error_kind`, `_finalize_generated`, `_emit_portrait_image_bq_log`, `_post_image_request` (ll.694-1107) | `user_portrait_warmup.py:9` (`warm_portrait_image_transport`) | A: session reuse + warmup + BQ log. B: transport + §6(1) logging (BQ emission ADAPT to async/batched where it blocks) | KEEP (BQ emission async) |
| Generation entry points: `generate_image_openrouter` (l.1220), `generate_image_xai` (l.1360), `generate_image` (l.1474), `_merge_image_timing` (l.1463) | `user_portrait_service.py:17-25` (`generate_image`); `generate_image_openrouter` prod-reachable only via `generate_image` dispatch + tests/harness (`tests/harness/ablate_portrait_openrouter_latency.py:150`, `tests/test_avatar_image_gen_portrait_transport.py:120,130`); `generate_image_xai` has **zero prod callers** found (only its own definition) — dead-provider-path flag: either wire it or delete it with the xAI decision, but do not keep an uncalled provider path as if live | A: one generation path is the portrait promise. B: tool execution | KEEP `generate_image` + `generate_image_openrouter`; ADAPT-or-DELETE `generate_image_xai` (confirm xAI is/isn't a live provider before deleting — see §1) |
| Forensics + timing-minimal: `capture_openrouter_image_forensics` (l.1295), `time_direct_openrouter_minimal` (l.1547) | **Zero prod callers** for either (forensics is invoked only via the compare path's BQ row in run-1's reading; in this tree no prod caller references `capture_openrouter_image_forensics`, and `time_direct_openrouter_minimal` is defined but never called outside itself) | A: diagnostics for a debug comparison / a timing micro-benchmark. B: debug tooling, not player tool execution | DELETE both (with the compare file; forensics BQ rows go with it per run-1) |

### document_generator.py (1,492 lines, 39 AST units) — ADAPT — run-1 CONFIRMED with one correction
Run-1 (frontend §1 + §4.8): ADAPT — keep four format generators as verbatim renderers of stored structured entries; delete prose-mining (`_parse_dice_rolls`, `_convert_presentation_blocks`, choice-key matching, debug-event extraction). **Confirmed in substance, corrected in one detail** (see the choice-matching row and §5): the `choice:`-prefix stored-key branch is verbatim lookup and must be kept; only the prose-inference fallbacks delete.
| Unit group (every symbol named) | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `MAX_PLANNING_BLOCKS`, `_normalize_text` (ll.56-57) | Internal to choice matching | A: cap + comparison normalization. B: formatting/bounded capacity | KEEP |
| `_format_background_event`, `_format_debug_events` (ll.65,87) | `_format_debug_events` is test-only in-tree (`tests/test_living_world_export.py:6,34,45,80,98,124`); `_format_background_event` internal | A: background-event formatting is presentation; debug events in a player export leak operator data. B: run-1 ADAPT confirmed — keep background formatting, DELETE debug-event extraction from player exports (separate debug artifact if needed) | KEEP `_format_background_event`; DELETE `_format_debug_events` from player exports |
| Choice matching: `_iter_choice_items` (l.241), `_find_matching_choice_key` (l.260), `_get_choice_by_key` (l.307), `get_choice_type` (l.322), `get_selected_choice` (l.356) | `world_logic.py:3324,3337` (`get_selected_choice` — live, not export-only) | A: which stored choice the player's action selected. B: **correction to run-1's blanket "delete choice-key matching":** `_find_matching_choice_key` (ll.260-306) has two distinct paths — the `choice:`-prefix branch (ll.277-282, exact stored-key equality) is verbatim lookup and KEEPs (it is what frontend run-2's "keep only the `choice:`-prefix stored-key branch plus `_get_choice_by_key`" says); Methods 1–4 (ll.284-305: startswith/title/exact-title/title-extract prose matching against choice text) are prose inference and DELETE. `_get_choice_by_key` itself is pure stored-key lookup — KEEP | ADAPT: keep `choice:`-prefix + `_get_choice_by_key`; DELETE Methods 1–4 |
| Story rendering: `format_story_entry` (l.395), `get_story_text_from_context_enhanced` (l.480), `get_story_text_from_context` (l.531) | `world_logic.py:11056`, `worldai_tools_mcp_proxy.py:907` (`get_story_text_from_context_enhanced`) | A: story-log-to-text conversion; without it exports have no content. B: rendering stored entries is pure presentation | KEEP |
| Font/layout constants: `ASSETS_DIR`, `FONT_FILENAME`, `DEFAULT_FONT_FAMILY`, `CUSTOM_FONT_NAME`, `ENCODING`, `ENCODING_REPLACE_STR`, `PDF_TITLE_STYLE`, `TITLE_FONT_SIZE`, `TITLE_LINE_HEIGHT`, `TITLE_ALIGNMENT`, `BODY_FONT_SIZE`, `BODY_LINE_HEIGHT`, `PARAGRAPH_SPACING`, `TITLE_SPACING`, `LABEL_GEMINI`, `LABEL_GOD`, `LABEL_USER`, `UNKNOWN_ACTOR`, `DOCX_HEADING_LEVEL` (ll.551-575) | Internal; font file is `assets/DejaVuSans.ttf` (above) | A: PDF/DOCX typography + actor labels. B: presentation data | KEEP |
| Format generators: `generate_pdf` (l.579), `generate_docx` (l.628), `generate_txt` (l.637), `generate_md` (l.1425), `generate_document` (l.1447) | `world_logic.py:11063`, `worldai_tools_mcp_proxy.py:913` (`generate_document`); `generate_document` test-covered (`tests/test_generator_isolated.py:199,227,253`) | A: the export promise itself (PDF/DOCX/TXT/Markdown); the model cannot emit file bytes through the log. B: file generation from stored state = tool execution | KEEP |
| Structured-Markdown: `_escape_yaml_scalar` (l.643), `_SceneRecord` (l.657), `_EntryMetadata` (l.670), `_text_value` (l.681), `_parse_entry_metadata` (l.689), `_safe_choice_key` (l.759), `_entry_label` (l.763), `_render_entry_block` (l.781), `_structured_context_to_markdown` (l.819) | Internal to `generate_md` | A: structured-context→Markdown. B: rendering stored structured entries = presentation | KEEP |
| Segment formatting: `_parse_actor_label` (l.875), `_quote_markdown_lines` (l.883), `_format_player_segment` (l.895), `_flush_actor_segment` (l.915), `_format_timestamp` (l.1154), `_escape_markdown_table_cell` (l.1166), `_render_markdown_document` (l.1321) | Internal | A/B: verbatim formatters of stored segments | KEEP |
| Prose-mining group: `_SOCIAL_LABELS`, `_ARC_LABELS`, `_COMBAT_LABELS` (ll.982-1037), `_detect_block_header` (l.1037), `_is_block_detail_line` (l.1065), `_convert_presentation_blocks` (l.1094), `_parse_dice_rolls` (l.923), `_format_detail_line` (l.938), `_format_presentation_block` (l.959), `story_text_to_markdown` (l.1171) | `story_text_to_markdown` is test-only in-tree (`tests/test_generator_isolated.py:280,350,446,497,525,553,578,626`); the mining helpers have zero external callers (internal to `story_text_to_markdown`) | A: prose→Markdown "publication-ready" transform. B: **run-1 confirmed** — re-derives block types, dice rolls, detail lines from prose the model already authored in structured form; label tables classify prose into social/arc/combat = domain classification, not formatting | DELETE the mining group; make `story_text_to_markdown` a verbatim renderer of stored structured entries or delete it with the group |

### equipment_display.py (878 lines, 18 AST units) — ADAPT — run-1 CONFIRMED and strengthened
Run-1 (frontend §1): ADAPT — keep extraction + unfiltered grouping; delete query routing, importance scoring, truncation, narrative injection. Run-2 (frontend §8.2(c)) strengthened it: `_classify_backpack_item` is entirely name/stats keyword branches, so the "keep verbatim" proviso FAILS for the keyword branches. **Both confirmed** on re-read, with one precision added: `classify_equipment_query` is imported but never called (see row).
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `DICE_PATTERN` (l.24), `_PAREN_STATS_HINTS` (l.30), `WEAPON_SLOTS` (l.33), `KNOWN_EQUIPMENT_SLOTS` (l.47), `_EQUIPMENT_QUERY_PHRASES` (l.50), `_EQUIPMENT_SINGLE_KEYWORDS` (l.70) | Internal to routing/classification | A: keyword tables for routing/classification. B: the tables are the mechanism of the violations below | DELETE with their consumers (keep `WEAPON_SLOTS`/`KNOWN_EQUIPMENT_SLOTS` only if the kept grouping path still uses them — `_categorize_equipment_slot` does; see below) |
| `is_equipment_query` (l.77) | `llm_service.py:232,8064,9240` (live, twice per turn path) | A: "is this an equipment question" routing. B: client-intent routing the model should own (routing is a model-side decision per §6(4); keyword phrase matching is exactly the banned pattern the intent-classifier pilot deleted) | DELETE (route via model/prompt; `llm_service.py:8064,9240` call sites need the Jev/model-routing replacement, same pattern as the classifier rewire) |
| `classify_equipment_query` (l.96) | Imported at `llm_service.py:232-235` but **never called** anywhere in-tree (only the import line + a comment at `llm_service.py:717` mention it) | A: an unused routing classifier. B: dead + ZFC-violating in kind | DELETE (dead code; the import line in `llm_service.py` goes with it) |
| `_filter_equipment_for_summary` (l.112) + nested `is_weapon_slot` (l.119), `is_backpack_slot` (l.122), `is_shield_item` (l.125) | Internal to summary building | A: slot filtering for the summary. B: grouping by stored slot is presentation; the nested predicates are slot checks, not keyword classification | KEEP (as part of extraction/grouping) |
| `_count_equipment_mentions` (l.178) | Internal | A: mention counting for summary shaping. B: display shaping over stored state; borderline — kept only as a count for the summary, not as a filter that drops items | KEEP (do not let it become a truncation input) |
| `_categorize_equipment_slot` (l.191) | Internal to `_build_equipment_summary` | A: stored-slot → display group. B: presentation grouping of server-authored entries | KEEP |
| `_classify_backpack_item` (l.246) | Internal to `_build_equipment_summary` (via grouping) | A: backpack subcategory. B: **run-2 confirmed** — the body (ll.246-358) is entirely name/stats keyword branches (Documents: document/ledger/cipher/letter/scroll/…; Keys; Signets & Rings; Currency; Resources; Tools; Magical Items; Weapons; Apparel; Instruments; default Miscellaneous). No stored category is consulted. This is server-side classification of model-authored item names, not verbatim rendering | DELETE the keyword branches; render backpack items under a single "Backpack" group (run-2's corrected verdict) |
| `_get_backpack_importance` (l.359), `_limit_backpack_for_display` (l.394) | Internal; `_limit` feeds the summary | A: importance scoring + top-N truncation. B: silently dropping items the player owns is a domain-value rewrite, not formatting (run-1) | DELETE both (render unfiltered) |
| `_build_equipment_summary` (l.411), `build_equipment_summary` (l.492) | `main.py:3742` (`build_equipment_summary`) | A: the summary the player sees. B: presentation once the keyword/importance/truncation pieces are removed | KEEP (slimmed form) |
| `ensure_equipment_summary_in_narrative` (l.502) | `llm_service.py:233,9252` (`gemini_response.narrative_text = ensure_equipment_summary_in_narrative(…)`) | A: appends a deterministic summary to narrative. B: **run-1 confirmed** — server code rewriting model-authored narrative text; the one hard ZFC violation in this area's server code (frontend §2(c)). No registered exception covers narrative injection | DELETE (the `llm_service.py:9252` assignment goes with it; the summary belongs in `processing_metadata["equipment_display"]` (ll.9247), which already exists) |
| `extract_equipment_display` (l.543) + nested `resolve_item` (l.597), `split_name_stats` (l.604), `normalize_name` (l.702) | `llm_service.py:234,8065,9244`, `main.py:3738` | A: extraction of server-held equipment entries. B: pure extraction/presentation of stored state (name/stats splitting is display parsing of a stored string, not a domain decision) | KEEP |

### install.sh (shell, 13 functions) — ADAPT (misnamed, AGY-only, dev tooling in prod tree)
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `usage`, `log`, `die`, `require_file`, `is_broken_or_recursive_symlink`, `copy_file`, `copy_file_if_exists`, `shell_quote`, `resolve_agy_binary_for_env`, `write_env_file`, `main` | Entry point `main "$@"`; invoked by a developer, not by the app | A: prepares a sanitized AGY HOME (`~/.cache/worldai/agy-clean-home-v1`), copies `~/.gemini` auth/config files into it, writes `worldai-agy.env`, validates `agy` binary. B: dev-environment tooling, not gameplay; its own header says "intentionally narrow: it does not start Flask/MCP" | ADAPT: rename to `prepare_agy_home.sh` (or move to `scripts/`) — the name `install.sh` promises an app install and delivers an AGY sandbox. Content note: it copies OAuth credential files (`oauth_creds.json`, `antigravity-oauth-token`) between HOMEs — that is credential handling by design of the tool, but it must never be run as part of a deploy; no credential values appear in the script itself |
| `write_dm_persona` (embeds a DM persona: "Never reveal that you are a Gemini model…", "If rewards_box.level_up_available is true, include top-level level_up_signal…") | Called by `main` | A: writes the AGY HOME's `GEMINI.md`. B: prompt data for a dev tool, not the shipped prompt set — but note it duplicates/overrides shipped prompt contracts (`level_up_signal`) in a dev sandbox; a drift risk if anyone copies it into prod prompts | ADAPT (same move; flag the persona drift risk) |
| `validate_agy` (runs `agy --print --new-project … "What model are you?"`, greps output for auth/model/policy leakage, validates `--add-dir` AGENTS.md honoring with a "pirate / Arrr!" fixture) | Called by `main` unless `--no-validate` | A: live validation of the sandbox. B: dev-only; the `--dangerously-skip-permissions` flag in the validation command is the tool's own choice, not a prod surface | KEEP (in the moved script) |

### mypy.ini (62 lines) — KEEP
| Unit | Evidence | A / B | Verdict |
|---|---|---|---|
| Whole file (python 3.11, `ignore_missing_imports`, `follow_imports=normal`, `exclude = testing_framework\|mvp_site/schemas/defensive_numeric_converter.py`, per-module `ignore_errors` for tests/mocks/testing_ui, strict `disallow_untyped_defs` for `firestore_service`/`gemini_service`/`main`/`schemas.*`) | Matches reality: `gemini_service` strict entry is stale in name only (no `mvp_site/gemini_service.py` in this area — the module is `llm_service.py`/providers; harmless since mypy ignores missing modules under `ignore_missing_imports`, but see §4). The `defensive_numeric_converter.py` exclusion matches schema-parsing's DELETE-as-module verdict for that file — the exclusion will be moot after deletion | A/B: type-check config, not gameplay | KEEP (prune the two stale entries when their targets delete/rename) |

### package-lock.json (530 lines) — KEEP
| Unit | Evidence | A / B | Verdict |
|---|---|---|---|
| Whole file (`name: mvp_site`, lockfile for `package.json`) | Consistent with `package.json` (jsdom, playwright, @types/node). Lockfile version field present. No action needed | A/B: dependency pinning for the JS test tooling | KEEP |

### package.json (10 lines) — KEEP
| Unit | Evidence | A / B | Verdict |
|---|---|---|---|
| Whole file (`dependencies: jsdom ^26.1.0`; `devDependencies: @playwright/test ^1.63.0, @types/node ^26.6.3`; `scripts: {}`) | Matches the JS test harness (`frontend_v1/tests` use jsdom; Playwright in `testing_ui/`). Empty `scripts` is honest (no npm scripts are defined) — not a mismatch | A/B: test-tooling manifest, not shipped app code | KEEP |

### pytest.ini (4 lines) — ADAPT
| Unit | Evidence | A / B | Verdict |
|---|---|---|---|
| Whole file (`addopts = --cache-optimizer --num-workers=4`, `python_files = test_*.py`, `python_functions = test_*`) | `--cache-optimizer` and `--num-workers` are not stock pytest options — they come from `pytest-testmon`/`pytest-xdist`-style plugins. `requirements.txt` declares `pytest-testmon` but **not** `pytest-xdist`; if `--num-workers` is a testmon/xdist option, the ini depends on a plugin the requirements do not pin (see §4). The `test_*` patterns match the tree's test naming | A/B: test config; a config that fails without an undeclared plugin is a mismatch | ADAPT: pin the plugin that provides `--num-workers`/`--cache-optimizer`, or drop the flags |

### requirements-test.txt (10 lines) — KEEP
| Unit | Evidence | A / B | Verdict |
|---|---|---|---|
| Whole file (only `google-cloud-bigquery==3.46.1`, with a comment explaining the duplication: Criterion4 journey closure needs it in the deployed image, so it is declared in prod requirements too and repeated here for test-runner installs) | The comment is accurate about the duplication's reason, and the version matches `requirements.txt`. Duplication is deliberate and documented, not drift | A/B: test-runner manifest | KEEP |

### requirements.txt (47 lines) — ADAPT (see §4)
| Unit | Evidence | A / B | Verdict |
|---|---|---|---|
| Core pins: Flask 3.1.3, gunicorn 23.0.0, firebase-admin 6.5.0, firestore 2.16.0, bigquery 3.46.1, google-genai 2.21.0, fpdf2, python-docx, httpx, PyJWT, pydantic, jsonschema, mcp 2.x, fastembed 0.7.4, numpy bounds, device-detector 6.5.1, selenium, playwright, ruff/isort/mypy/bandit, pytest family | Spot-checked imports (prod, non-test): Flask/gunicorn/firebase/genai/fpdf2 (document_generator)/python-docx/httpx/PyJWT/pydantic/jsonschema/mcp (mcp_api)/cachetools (file_cache)/flask_compress (main.py)/device-detector (user_lifecycle_telemetry) all have prod importers. `selenium`/`playwright` prod importers are only in `testing_ui/` (test tooling, correctly declared but arguably test-only deps in the prod requirements). `fastembed` prod importers are `gunicorn.conf.py` (preflight) + `intent_classifier.py` — the classifier deletes, so fastembed becomes a preflight-only dep (see Dockerfile ADAPT). `ruff/isort/mypy/bandit` + pytest family are dev/test tools shipped in the prod requirements file (the Dockerfile pip-installs this whole file into the prod image) | A/B: the file installs correctly, but it mixes prod, dev, and test deps into the prod image | ADAPT: split prod vs dev/test requirements (or add a prod-only file for the Dockerfile); drop fastembed with the classifier |

### run_integration_tests.sh — DELETE from prod tree (test runner, broken directory reference)
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| Whole script (no functions; loop over `find test_integration -name "test_*.py"`, runs each with `TESTING_AUTH_BYPASS=true python -m unittest`, 5s warning sleep, venv activation, pass/fail summary, exit 1 on failures) | Zero prod callers. **The directory it loops over does not exist in this tree** (no top-level `test_integration/`; integration tests live under `mvp_site/tests/` + `testing_*` dirs per the ledger). Its own warning (real Gemini + Firestore calls, needs `GEMINI_API_KEY` + `serviceAccountKey.json`) is honest about cost, but the script as written finds zero tests and reports 0/0 passed | A/B: test tooling with a stale target dir, in the prod tree | DELETE from prod tree (move to test tooling with the path fixed, or delete if superseded by the CI integration runner) |

### portrait_generator_agent.py (601 lines, 28 AST units) — ADAPT — run-1 CONFIRMED
Run-1 (frontend §1 + §4.5): ADAPT — keep context assembly, delete re-derived summaries, express precedence once in prompt template text. **Confirmed.** The dead-wrapper note from run-2 (frontend §8.2(d)) is also confirmed below.
| Unit group (every symbol named) | Callers/entry | A / B | Verdict |
|---|---|---|---|
| Dataclasses: `PortraitContextBundle`, `PortraitAppearanceSlots`, `PortraitCanonHints` (ll.60-79); `_REDACT_PATTERNS` (l.53) | `user_portrait_service.py:33-50` | A: typed context contracts. B: data contracts for prompt assembly | KEEP |
| Canon: `load_portrait_canon_franchise_guidance` (l.92), `_CANON_PROMPTS_DIR` (l.88), `_coerce_franchise_flag` (l.97), `portrait_canon_from_mapping` (l.105), `portrait_canon_to_api_dict` (l.126), `build_portrait_canon_guidance_block` (l.165), `canon_hints_for_actor_retry` (l.188) | `user_portrait_service.py` | A: franchise-canon cues for IP portraits. B: passing authored canon cues through = prompt assembly; precedence must live in prompt text, not code ordering | KEEP (precedence in template text) |
| Precedence filter: `appearance_subordinate_to_player_description` (l.135) | Internal | A: drops appearance slots tied to a different brief than the player's description. B: a code filter silently dropping authored slots — run-1 ADAPT confirmed: move the rule into prompt template text, delete the code filter | ADAPT (move to template, delete filter) |
| Appearance mapping: `portrait_appearance_from_mapping` (l.207), `portrait_appearance_to_api_dict` (l.227) | `user_portrait_service.py` | A: suggestion round-trip mapping. B: pure data mapping, no invention | KEEP |
| Scalar + re-derived: `_scalar_pc_fields` (l.238), `_equipment_summary` (l.251), `_campaign_tone` (l.264) | Internal to context assembly | A: scalar extraction is pass-through; equipment summary + tone derivation re-derive from state. B: run-1 ADAPT confirmed — KEEP `_scalar_pc_fields`, DELETE `_equipment_summary` and `_campaign_tone` as code (their content, if wanted, is the model's job in the brief or a stored authored field) | KEEP `_scalar_pc_fields`; DELETE `_equipment_summary`, `_campaign_tone` |
| Assembly: `assemble_wizard_portrait_context` (l.288), `build_campaign_portrait_context_dict` (l.305), `load_campaign_portrait_records` (l.337), `assemble_campaign_portrait_context` (l.356), `assemble_portrait_context` (l.363), `assemble_portrait_context_for_campaign_id` (l.395) | `user_portrait_service.py:33-50` (assemble_*), `user_portrait_warmup.py:10` (`assemble_portrait_context_for_campaign_id`) | A: wizard + campaign context assembly. B: prompt assembly of authored facts. **Dead wrapper confirmed (run-2 §8.2(d)):** `assemble_campaign_portrait_context` (ll.356-362) is a thin wrapper over `build_campaign_portrait_context_dict` with **zero callers** outside itself in-tree — delete the wrapper, keep the dict builder | KEEP assembly (minus the dead wrapper); DELETE `assemble_campaign_portrait_context` wrapper |
| Caps/prompt: `truncate_context_json` (l.444), `_cap_portrait_text` (l.463), `compact_context_for_suggest` (l.470), `compact_context_for_image_prompt` (l.492), `build_portrait_image_prompt` (l.518) | `user_portrait_service.py` | A: caps keep 10k+ char wizard IP descriptions from blowing up prompts; final prompt construction. B: truncation for bounded capacity is allowed if it truncates rather than rewrites; `compact_context_for_image_prompt`'s field-dropping must drop only duplicated fields, never the player's brief | KEEP |
| Logging: `redact_portrait_prompt_for_log` (l.570), `log_assembled_portrait_prompt` (l.577) | `user_portrait_service.py` | A: redacted prompt logging. B: §6(1) logging KEEP, delivered async; redaction before logging is privacy-safe | KEEP (async delivery) |

### portrait_model_compare.py (194 lines, 4 AST units) — DELETE — run-1 CONFIRMED
Run-1 (frontend §1 + §4.6): DELETE — debug-only double generation, no player flow except a debug route. **Confirmed, with a precision:** the "debug route" is real and live — `main.py:8619-8639` (`POST /api/portrait/compare-models`, docstring "Debug-only", gated by `_debug_tools_authorized` → 403 otherwise, budget-checked via `debug_image_budget.reserve_debug_budget` with `images=len(COMPARE_MODELS)`). The file is therefore not unreferenced dead code; it is a gated debug tool. The verdict stands anyway (see below), but the deletion must remove the route too.
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `COMPARE_MODELS` (l.24: x-ai/grok-imagine-image-2.0, google/gemini-nano-banana-2.1), `COMPARE_RESOLUTION` (l.27: "2K") | `main.py:8639` (budget count) | A: two-model list for the comparison. B: debug-tool config, not gameplay | DELETE with the file |
| `_log_compare_row` (l.27) | Internal to `_one_model` | A: BQ row per compare image. B: debug telemetry does not inherit §6(1) (which keeps player-path logging, not debug comparison telemetry) | DELETE with the file |
| `_one_model` (l.64) | `compare_portrait_models` | A: one model's generate+upload+log step. B: debug harness around the real generation path | DELETE with the file |
| `compare_portrait_models` (l.126) + inner `_run` (l.146) | `main.py:8619` (debug route only) | A: parallel two-model generation, previews only, saved portrait untouched until the user applies one. B: doubling image-generation cost per invocation is the opposite of bounded capacity; no player flow needs it (the normal single-model path is untouched) | DELETE the file **and** the `main.py:8619` route (a file deletion alone leaves a route importing a missing module) |

### portrait_timing.py (149 lines, 9 AST units) — ADAPT — run-1 CONFIRMED
Run-1 (frontend §1 + §4.7): ADAPT — keep the breakdown, deliver async/batched, drop client-key zero-padding. **Confirmed.**
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `_PROVIDER_DETAIL_PHASES`, `_SERVER_PHASES`, `_CLIENT_TIMING_KEYS` (phase vocabularies) | Internal | A: vocabularies the breakdown sums/pads with. B: measurement data, not domain facts | KEEP |
| `PortraitTimingBreakdown.start/stop/snapshot_phases/to_dict` (ll.66-82) | `avatar_image_gen.py`, `user_portrait_service.py:52`, `user_portrait_warmup.py:11`, `main.py:8829` | A: wall-clock measurement; portraits still generate without it. B: measuring tool execution is logging-adjacent (§6(1) KEEP); `stop` correctly ignores unstopped phases rather than inventing them | KEEP (delivery async) |
| `_provider_image_ms` (l.86), `_total_ms_disjoint` (l.90) | Internal to `portrait_timing_for_client`/`merge` | A: sums producing provider/total times without double-counting. B: arithmetic over measurements, not domain recomputation | KEEP |
| `merge_timing_phases_for_api` (l.111) | `portrait_timing_for_client` + `user_portrait_service.py:116,247,257` | A: merges phase maps skipping `total_ms`/`provider_image_ms`/None. B: logging hygiene | KEEP |
| `portrait_timing_for_client` (l.134) | `avatar_image_gen.py:1095,1468`, `user_portrait_service.py:116,247,930,1020,1690,1713` | A: client-facing timing dict. B: **confirmed** — the zero-padding loop (ll.140-142: every `_CLIENT_TIMING_KEYS` entry absent from the merge is set to `0.0`) manufactures phases the client never measured; the docstring ("pad standard keys so live console always shows provider totals") admits the invention | ADAPT: keep the merge, DELETE the zero-padding (console renders absent phases as absent) |

### tools.py (1 line) — DELETE (empty stub)
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| File (single docstring: "Application tool contracts are owned by their domain modules.") | **Zero importers, zero symbols.** No `from tools import …` / `import tools` anywhere in-tree; the MCP tools surface lives in `mcp_api.py`/`worldai_tools_mcp_proxy.py`/`world_logic.py`, not here. The docstring is a pointer to nowhere (it names no domain module) | A: deleting it removes a docstring. B: a stub that owns nothing is not a contract | DELETE (if a tools contract is wanted, it belongs in the MCP module's docstring, not a standalone stub file) |

### docs/generalized_file_caching.md (174 lines) — KEEP (with an unverified-performance flag)
| Unit/sections | Evidence | A / B | Verdict |
|---|---|---|---|
| Whole file (36 headings: cachetools TTLCache architecture, usage `from file_cache import read_file_cached`, world_loader integration example) | Consistent with `file_cache.py` in-tree (`TTLCache`, `CACHE_MAX_SIZE = 1000`, `read_file_cached` at l.34). The "~11x speedup (0.022ms → 0.002ms)", "~1ms per-session savings" figures are benchmark claims with no benchmark artifact cited in the doc — unverified, not disproven | A/B: accurate design doc; performance figures should be cited as historical measurements, not current guarantees | KEEP (flag the figures as unverified) |

### docs/rate-limit-firestore-allowlist-20260917.md (229 lines) — KEEP (design now implemented)
| Unit/sections | Evidence | A / B | Verdict |
|---|---|---|---|
| Whole file (9 headings: problem — hardcoded `RATE_LIMIT_EXEMPT_EMAILS` in `rate_limiting.py` requires code changes; goal — `firestore_user_config` collection, per-user tier + overrides, boot-time fallback, idempotent migration; status APPROVED 2026-09-17; PR #9911 context) | **Now implemented, not just proposed:** `rate_limiting.py:558,706,809` reference the `firestore_user_config` collection (authoritative when configured, boot-time fallback preserved). The doc's problem statement (code-change-per-exemption) is therefore historical — the design landed. The doc remains the correct design record for why the collection exists | A/B: accurate design record; add a one-line "implemented" note pointing at `rate_limiting.py` so the next reader does not re-propose it | KEEP (+ implementation note) |

### docs/v1_vs_v2_comparison/comprehensive_test_report_20250825_153446.json (22 lines) — KEEP as evidence
| Unit | Evidence | A / B | Verdict |
|---|---|---|---|
| File (keys: `test_run_id`, `timestamp`, `test_matrix_coverage`, `test_results`, `evidence_directory`, `systems_tested`, `compliance_checklist`) | Dated 2025-08-25 test report; no code reads it. A historical v1-vs-v2 comparison artifact, consistent with its sibling screenshots (below) | A/B: evidence, not runtime | KEEP |

### docs/v1_vs_v2_comparison/screenshots/*.png (2 files) — KEEP as evidence
| Unit | Callers/entry | A / B | Verdict |
|---|---|---|---|
| `green_custom_elara_v1_auth_init_20250808_095913_018.png`, `green_dragon_knight_v1_auth_init_20250808_095945_561.png` (10,824 / 10,786 bytes) | Referenced by the 2025-08-25 test report's evidence directory (same comparison run, 2025-08-08 auth-init screenshots). No code renders them | A/B: evidence screenshots for the v1/v2 comparison | KEEP |

## §1 Dead/unreachable code list

1. `equipment_display.classify_equipment_query` (l.96) — imported at `llm_service.py:232-235`, never called anywhere in-tree. DELETE with the import line.
2. `avatar_image_gen.generate_image_xai` (l.1360) — zero prod callers (only tests reference the OpenRouter path). ADAPT-or-DELETE pending confirmation that xAI is not a live provider; if it is live, it needs a caller, not just a definition.
3. `avatar_image_gen.capture_openrouter_image_forensics` (l.1295), `time_direct_openrouter_minimal` (l.1547) — zero prod callers. DELETE (forensics goes with the compare file).
4. `portrait_generator_agent.assemble_campaign_portrait_context` (ll.356-362) — thin wrapper, zero callers (run-2 §8.2(d) confirmed). DELETE the wrapper, keep `build_campaign_portrait_context_dict`.
5. `static/v2/index.html` — unservable stub (referenced `./assets/*` absent, zero prod references). DELETE.
6. `tools.py` — entire file (1 docstring, 0 symbols, 0 importers). DELETE.
7. `config/paths.py` — entire module in prod terms (zero prod callers; one test caller via a different import path). ADAPT out of prod tree.
8. `document_generator.story_text_to_markdown`'s prose-mining helpers (`_parse_dice_rolls`, `_convert_presentation_blocks`, `_detect_block_header`, `_is_block_detail_line`, `_format_detail_line`, `_format_presentation_block`, label tables) — reachable only from the test-only `story_text_to_markdown` path; DELETE per §4.8 (they are also ZFC violations, not merely dead).
9. `document_generator._format_debug_events` — test-only (`tests/test_living_world_export.py`); DELETE from player exports.
10. NOT dead (explicitly cleared): the whole `push/` package (registered `main.py:2632-2634`, obligation path live); `push/sender.py`'s `claim/prepare_send/acknowledge/candidates/consume_one` (internal pipeline stages called by `sweep`/`_deliver`/`submit_wake`, not dead); `push_delivery_obligation.publish_started` (called `llm_parser.py:2418`); `templates/settings.html` (rendered `main.py:7729`); `assets/DejaVuSans.ttf` (loaded `document_generator.py:605`); `data/srd_classes/*` (read via `class_lookup.py`); `world/*` (read via `world_loader.py`).

## §2 Test-only/demo code in prod files list

1. `analysis/*.py` (4 files) — one-off Sariel capture/replay harnesses in the prod tree, with workstation-hardcoded paths (`/home/jleechan/projects/worldarchitect.ai/…`) and imports of test libs (`integration_test_lib`, `test_integration.integration_test_lib`). Test/analysis-only; DELETE from prod tree (see per-file rows).
2. `config/paths.py` — test-only consumer (`tests/auth/test_auth_resilience.py:21`); its own docstring example matches the test import path, not prod.
3. `run_integration_tests.sh` — test runner in the prod tree, pointing at a nonexistent `test_integration/` dir.
4. `portrait_model_compare.py` + `main.py:8619` compare route — a gated debug tool (`_debug_tools_authorized`, 403 otherwise), not a player flow. DELETE file + route together.
5. `document_generator._format_debug_events`, `story_text_to_markdown` — debug/test-only export paths inside the player export module (see §1 items 8–9).
6. `install.sh` — dev-only AGY sandbox prep (validates with `--dangerously-skip-permissions`); must not run in deploys. Rename/move, do not treat as an installer.
7. Duplication (name both locations): Sariel capture logic is triplicated — `analysis/capture_actual_llm_responses.py:34` vs `analysis/capture_llm_responses.py:28` vs `analysis/run_real_sariel_capture.py:15,44` (three harnesses, same Sariel replay, same `test-llm-capture-user` subject). One harness (or none, archived with its output) suffices.
8. `mvp_site/__init__.py` aliases for deleted targets (`entity_preloader`, `memory_mcp_real`, `entity_validator`) will become test/proxy traps after those deletions — prune in the same PRs (not test-only code, but a deletion-ordering hazard).

## §3 Stale/misleading docs list

1. `CODE_REVIEW_SUMMARY.md` — every line count stale by an order of magnitude (main.py "985" vs 9,634; llm_service "1,449" vs 12,030; "34 major files" vs 400+; `static/app.js` vs shipped `frontend_v1/`; nonexistent `firestore/` package tables). DELETE/ARCHIVE.
2. `UNIFIED_API_IMPLEMENTATION.md` — documents `unified_api.py`, `unified_api_examples.py`, `test_unified_api_structure.py`, none of which exist. DELETE/ARCHIVE.
3. `PARALLEL_DUAL_PASS_INTEGRATION.md` — integrates `main_parallel_dual_pass.py` + `static/parallel_dual_pass.*`, none of which exist; the `frontend_v1/` counterparts are frontend-DELETE dead code. DELETE/ARCHIVE.
4. `README.md:36` — "Flask 2.x" vs actual Flask 3.1.3 (`requirements.txt:2`). ADAPT (correct the version).
5. `README.md` theme list — claims light/dark/fantasy/cyberpunk; shipped themes are base/default/fantasy. ADAPT.
6. `README_FOR_AI.md` §6 — "JSON Display Bug (as of 2025-07-07)" presented as a current known issue with open investigation questions. ADAPT (resolve-or-date).
7. `FALLBACK_REVIEW.md` — cites `frontend_v2/src/utils/errorHandling.ts` (no `frontend_v2/` tree) and describes `mcp_memory_real.py` fallbacks as current while that file is state-storage-DELETE. ADAPT.
8. `world/README.md` ll.25-38 — inventories a `world/archive/` directory that does not exist. ADAPT (delete the section).
9. `config/paths.py` docstring — claims to be the "single source of truth for all file and directory paths used throughout the application" with zero prod users. ADAPT (with the move).
10. `AGENTS.md` — outbound links to `.claude/skills/*` and `docs/user-stories-ui/` not verified in this area; the routing rule itself is sound. ADAPT (verify/repair links).
11. `docs/generalized_file_caching.md` — "~11x speedup / ~1ms savings" figures cited without a benchmark artifact. KEEP with the flag (not counted as false, counted as unverified).
12. `world/world_assiah_compressed.md` header — "85k → ~45k tokens, 47% reduction" is a historical compression claim not verifiable from the file alone. KEEP with the flag.
13. `push/content.py` comment (l.7) — correctly states its credential screening is "conservative, not a guarantee"; this is good documentation, listed here to prevent a future reader from over-claiming it (not a staleness item).

## §4 Config/reality mismatches list

1. `push/config.json` vs `push/sender.py:valid_config` — shipped config can never validate (empty scheduler/APNs fields, `deployment_service` must equal `K_SERVICE`). This is fail-closed by design, but it means the tracked config is not a deployable config: any deploy that copies it verbatim gets 503 `disabled`/`unconfigured` on sweep and False from `submit_wake`. Document that the tracked file is a shape template, not a live config — or the next deployer will "fix" it by filling in secrets in-tree.
2. `Dockerfile` fastembed preflight vs intent-classifier deletion — the image pre-downloads a fastembed model (`scripts/preflight_model_docker.py`, `scripts/preflight_model.py`, `FASTEMBED_CACHE_PATH`) for the classifier this audit deletes in full. After deletion the preflight is dead image weight.
3. `Dockerfile` copies `testing_mcp/` + `testing_utils/` into the production image. Test code in the prod image.
4. `Dockerfile` "truthful source manifest" pins only `mvp_site/llm_parser.py`'s hash + `GIT_COMMIT` — it does not pin the tree it claims to manifest.
5. `requirements.txt` mixes prod + dev + test deps into the prod image (ruff/isort/mypy/bandit, pytest family, selenium/playwright whose only prod-tree importers are `testing_ui/`). Split prod vs dev/test.
6. `requirements.txt` fastembed 0.7.4 — after the classifier deletion, fastembed's only prod-tree importers are the Dockerfile preflight path (`gunicorn.conf.py`) and the deleted classifier. It becomes a preflight-only dep.
7. `pytest.ini` `--cache-optimizer --num-workers=4` — plugin-provided flags with no matching plugin pinned in `requirements.txt` (`pytest-testmon` is pinned, `pytest-xdist` is not). Pin the provider or drop the flags.
8. `mypy.ini` strict entry for `mvp_site.gemini_service` — no such module in-tree (the service is `llm_service.py`/providers). Harmless under `ignore_missing_imports`, but stale.
9. `run_integration_tests.sh` loops over `test_integration/` — directory absent; the script reports 0/0 as a pass.
10. `install.sh` name vs content — named as the app installer, implements AGY HOME prep only; its usage text even points at a `local.sh` that is not in this area. Rename/move.
11. `static/v2/index.html` asset hashes (`index-BgGmhWH9.js`, etc.) reference files absent from the tree — a tracked bundle stub whose hashes match nothing.
12. `evidence/god_mode_directive_persistence_8103/` lacks the `.sha256` sidecar its two sibling proof dirs carry — evidence-format inconsistency.
13. `mypy.ini` exclusion of `mvp_site/schemas/defensive_numeric_converter.py` will be moot after schema-parsing's DELETE-as-module verdict for that file — prune with that deletion.

## §5 Challenges to run-1/run-2 verdicts (with evidence)

1. **CONFIRMED — `portrait_model_compare.py` DELETE (run-1).** Precision added, verdict unchanged: run-1 said "no player flow calls it except a debug route"; verified the debug route is live (`main.py:8619`, admin-gated, budget-checked). Deletion must include the route, or the app breaks on import. The §6(1) logging carve-out does not rescue it: its BQ rows are debug telemetry, not player-path logging.
2. **CONFIRMED — `document_generator.py` ADAPT (run-1), with one correction (run-2 §8.2(b) upheld).** Run-1's blanket "delete choice-key matching" is too broad: `_find_matching_choice_key` (ll.260-306) contains a verbatim `choice:`-prefix stored-key branch (ll.277-282) that KEEPs, and only Methods 1–4 (prose inference, ll.284-305) DELETE. Run-2's "keep only the `choice:`-prefix stored-key branch plus `_get_choice_by_key`" is the correct verdict; run-1's row is corrected accordingly. The prose-mining DELETE (`_parse_dice_rolls`, `_convert_presentation_blocks`, label tables) is confirmed in full.
3. **CONFIRMED + STRENGTHENED — `equipment_display.py` ADAPT (run-1 + run-2 §8.2(c)).** Run-1's "keep verbatim" proviso for backpack grouping FAILS on re-read: `_classify_backpack_item` (ll.246-358) is entirely name/stats keyword branches with no stored category consulted — run-2's correction (DELETE keyword branches, single "Backpack" group) is adopted. Additionally, `classify_equipment_query` is not merely ZFC-violating but dead (imported, never called). `ensure_equipment_summary_in_narrative` DELETE is confirmed as the area's one hard server-side ZFC violation (`llm_service.py:9252` assignment).
4. **CONFIRMED — `avatar_image_gen.py` ADAPT, `portrait_generator_agent.py` ADAPT, `portrait_timing.py` ADAPT (run-1).** No challenge: re-read confirms the resolver/preview/forensics sprawl, the re-derived `_equipment_summary`/`_campaign_tone`, the dead `assemble_campaign_portrait_context` wrapper (run-2 §8.2(d)), and the `portrait_timing_for_client` zero-padding (ll.140-142). One addition: `generate_image_xai` has zero prod callers and was not singled out by run-1 — flagged in §1 for an ADAPT-or-DELETE decision.
5. **CHALLENGE (narrow) — run-1 frontend §2's claim that `document_generator` choice-matching is "prose inference, not stored keys" (as a blanket description).** As shown in item 2, the matcher is mixed: stored-key branch + prose fallbacks. The blanket description misdirects the fix (deleting the whole matcher would break `world_logic.py:3324,3337`, which relies on `get_selected_choice` for live choice resolution, not just exports). Verdict: split the function, do not delete it wholesale.
6. **NO CHALLENGE to run-2 (MASTER-LEDGER v2) verdicts outside this area.** No run-2 verdict covers this area's files except the frontend run-2 notes cited above (which are confirmed). The `docs-configs` group (run-1 enumeration-only, not re-run) is the reason this review pass exists for these files; nothing in it is contradicted here — its provisional direction ("KEEP/ADAPT only for live configs with a proven consumer") is consistent with the `config/paths.py` ADAPT and the docs dispositions above.

## §6 Draft-amendment effects (DRAFT ONLY — NOT applied)

The draft amendment (FastEmbed + Jev count as models; model-call outputs are model-authored; server dispatch on them is execution; hand-written thresholds/boosts/anchor lists layered on outputs still need an exception) would change **no file-level verdict** in this area, for these reasons:

1. **Push/equipment/document/portrait files contain no FastEmbed or Jev calls.** The only threshold/anchor-style artefacts here are keyword tables (`equipment_display` phrases/keywords, `_classify_backpack_item` branches, `document_generator` choice-matching Methods 1–4, `push/content.py`'s credential regex). Under the draft, those are *not* model outputs at all — they are hand-written server-side matching layered on user/model text — so the draft's "thresholds/boosts/anchor lists still need an exception" clause leaves their DELETE verdicts intact. The draft does not rescue keyword routing.
2. **`equipment_display.is_equipment_query` / `classify_equipment_query`:** under current policy they DELETE as model-owned routing; under the draft they would DELETE for the same reason plus the anchor-list clause (keyword phrases are the analogue of anchor phrases). No change.
3. **`push/content.py:snippet` credential regex:** not a model decision and not a threshold on a model output — a disclosure screen on explicitly supplied narrative. KEEP under both policies.
4. **Dockerfile fastembed preflight:** the draft would make FastEmbed *count as a model* for ZFC purposes, but it would not rescue the preflight: the classifier files themselves still DELETE (their role is replaced by Jev, per §6(4)), and pre-downloading a model cache for a deleted consumer is still dead image weight. The Dockerfile ADAPT stands under either policy.
5. **If the draft were adopted, one sentence in this report would need rewording, not re-verdicting:** the §5 item-2 note that routing is "a model-side decision per §6(4)" would additionally cite the draft's model-counting rule for Jev. The verdicts would not move.

## §7 Coverage accounting

**Files reviewed (80, listed + counted):**
- `push/` (7): `__init__.py`, `apns.py`, `config.json`, `content.py`, `registrations.py`, `routes.py`, `sender.py`.
- `data/` (15): `dragon_knight_canonical_description.txt`, `srd_classes/index.json`, `srd_classes/{barbarian,bard,cleric,custom_class_instruction,druid,fighter,monk,paladin,ranger,rogue,sorcerer,warlock,wizard}.md` (13).
- `evidence/` (6): `dead_npc_hallucination/{proof.json,proof.sha256}`, `god_mode_directive_persistence_8103/proof.json`, `god_mode_json_wire/{README.md,proof.json,proof.sha256}`.
- `analysis/` (5): `capture_actual_llm_responses.py`, `capture_llm_responses.py`, `run_real_sariel_capture.py`, `run_sariel_replays.py`, `sariel_llm_responses_documented.md`.
- `roadmap/` (4): `scratchpad_{dev1314,parallel_dual_pass_optimization,story_mode_improvements,test-organization-improvements}.md`.
- `world/` (3): `README.md`, `banned_names.md`, `world_assiah_compressed.md`.
- `templates/` (2): `base.html`, `settings.html`.
- `config/` (2): `__init__.py`, `paths.py`.
- `static/` (1): `v2/index.html`.
- `bin/` (1): `LICENSE.chromedriver`.
- `assets/` (1): `DejaVuSans.ttf`.
- `docs/` (5): `generalized_file_caching.md`, `rate-limit-firestore-allowlist-20260917.md`, `v1_vs_v2_comparison/comprehensive_test_report_20250825_153446.json`, `v1_vs_v2_comparison/screenshots/{green_custom_elara_v1_auth_init_20250808_095913_018,green_dragon_knight_v1_auth_init_20250808_095945_561}.png`.
- `push_delivery_obligation.py` (1).
- Top-level remainder (27): `.gcloudignore`, `AGENTS.md`, `CODE_REVIEW_SUMMARY.md`, `DEPLOYMENT.md`, `Dockerfile`, `FALLBACK_REVIEW.md`, `PARALLEL_DUAL_PASS_INTEGRATION.md`, `README.md`, `README_FOR_AI.md`, `TYPING_GUIDE.md`, `UNIFIED_API_IMPLEMENTATION.md`, `__init__.py`, `avatar_image_gen.py`, `document_generator.py`, `equipment_display.py`, `install.sh`, `mypy.ini`, `package-lock.json`, `package.json`, `pytest.ini`, `requirements-test.txt`, `requirements.txt`, `run_integration_tests.sh`, `portrait_generator_agent.py`, `portrait_model_compare.py`, `portrait_timing.py`, `tools.py`.
- Total: 7+15+6+5+4+3+2+2+1+1+1+5+1+27 = **80**.

**Methods/sections reviewed:** 262 code units (247 AST function/class occurrences + 13 `install.sh` functions + 1 Dockerfile stage + 1 `run_integration_tests.sh` script unit) + 59 non-Python file units (33 `.md` files surveyed across 629 headings, grouped into file/section-cluster rows; SRD class files grouped by file). Enumeration method: `ast` parse of every Python file first (top-level + nested defs reconciled per file in the tables), `grep` caller search over `mvp_site/**/*.py` with prod/test separated, heading count via `^#{1,3}` regex over the `.md` files, direct reads of all config/data/template/static files.

**Files/methods skipped (each with a reason; zero unexplained skips):**
- `mvp_site/docs/zfc_audit/FULL_AUDIT.md`, `mvp_site/docs/zfc_audit/SUMMARY.md` — assigned to another auditor per the task; excluded from the 80 and from all counts.
- Per-line branch-by-branch reads inside the largest functions were not done where the verdict does not depend on unread lines (e.g. `avatar_image_gen._post_image_request`'s 250-line body, `document_generator.story_text_to_markdown`'s 150-line body, `push/sender.py`'s lease internals): each such row is grounded in signature, docstring, caller evidence, and sampled body sections, and the verdict (KEEP transport / DELETE mining group) follows from the function's role, not from an unread branch. This is stated here rather than buried.
- `DEPLOYMENT.md`'s deferred targets (`gcp-deployment` skill, `scripts/shared_config.sh`, `scripts/deploy_common.sh`, `deploy.sh`, `.github/actions/deploy-mvp-site/action.yml`) and `AGENTS.md`'s `.claude/skills/*` / `docs/user-stories-ui/` targets were not re-verified — they are outside this area's file list; the docs are verdict-ed as pointer documents with that caveat, not as verified claims about those targets.
- Hash verification of `evidence/*/proof.sha256` sidecars (recomputing hashes) was not performed — the files' presence/format was checked, not their cryptographic validity. The missing sidecar for `god_mode_directive_persistence_8103` is reported as a format gap, not a failed verification.
- No credential, token, secret, or key material is reproduced in this report. `push/config.json`'s sensitive fields are empty strings in-tree and are described as empty, not quoted with values (there are none to quote).
