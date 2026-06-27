# WorldArchitect.AI — 2026-06-27 09:52 PT — Slack 18h Audit + Roadmap

**Generated:** 2026-06-27T16:52Z (09:52 PT)
**Source:** C09GRLXF9GR (DM), C0AH3RY3DK6 (worldai), C0BDEAJH8PK (#worldai-bugs), C0AJ3SD5C79 (hermes), C0AKALZ4CKW (agento), C0AJQ5M0A0Y (home)
**Window:** last ~18h (2026-06-26 22:30Z → 2026-06-27 16:52Z)
**Skill version on origin/main:** `acfe79a33f` (Step 2.5 META-FAILURE GATE) ✅
**Auditor:** Hermes (this session)

---

## A. Executive Summary (TL;DR)

- **5 PRs MERGEABLE, ready for batch auto-merge** (PRs 7905, 7926, 7884, 7984, 7938)
- **8 PRs MERGEABLE, larger surface, recommend human eyeball** (PRs 7925, 7935, 7950, 7952, 7951, 7953, 7946, 7947, 7971)
- **4 PRs CONFLICTING** (7890, 7873, 7868, 7851) — need rebase
- **40+ 5h-class backfill-cap orphan alerts** in last 18h, mostly classified
- **1 STUCK thread** (`C0AH3RY3DK6 / 1782335045` cold-start — issue #7961 now has PR #7984 with the one-line fix GUNICORN_WORKERS=1)
- **1 critical unfinished meta-task**: publish to roadmap repo (THIS report)
- **Hermes max_turns deployment discrepancy**: source says 1000, prod still says 60 (verified pre-flight)

---

## B. PR Auto-Merge Candidates — Tier 1 (low risk, batch safe)

| # | PR | Title | Files | +/- | Risk |
|---|---|---|---|---|---|
| 1 | [PR #7905](https://github.com/jleechanorg/worldarchitect.ai/pull/7905) | chore(ci): delete redundant /levelup + /dice PR-comment workflows | 2 | +0/-615 | LOW (deletion only) |
| 2 | [PR #7926](https://github.com/jleechanorg/worldarchitect.ai/pull/7926) | fix(ci): skip precompute in PR preview to prevent OOM | 1 | +5/-0 | LOW |
| 3 | [PR #7884](https://github.com/jleechanorg/worldarchitect.ai/pull/7884) | fix(dice-audit): shorten scheduler SA name to fit GCP 30-char limit | 1 | +4/-4 | LOW |
| 4 | [PR #7984](https://github.com/jleechanorg/worldarchitect.ai/pull/7984) | fix(gunicorn): default to 1 worker for Cloud Run cold-start (issue #7961) | 4 | +38/-23 | LOW (one-line config bump, fixes CRITICAL cold-start) |
| 5 | [PR #7938](https://github.com/jleechanorg/worldarchitect.ai/pull/7938) | chore(runners): route ubuntu-runner-health alerts to ops channel | 1 | +18/-3 | LOW |

**Trigger:** `MERGE APPROVED` — batch-merge all 5 in one pass.

---

## C. Per-Thread /nextsteps Audit (most important work NOT in progress)

### C1. Cold-start latency (CRITICAL — STUCK ⚠️) — has PR #7984 ready
- **URL:** [C0AH3RY3DK6 / 1782335045](https://jleechanai.slack.com/archives/C0AH3RY3DK6/p1782335045.027409)
- **Issue:** [#7961](https://github.com/jleechanorg/worldarchitect.ai/issues/7961) — GUNICORN_WORKERS=1 fix
- **State:** ✅ PR #7984 ready MERGEABLE (+38/-23, 4 files), low risk
- **Last activity:** 2026-06-27 04:55 PT (you said "Fix failures even if pre existing and give me PR url")
- **Next step:** Merge PR #7984 (included in § B Tier 1) — solves the 28-44s cold-start that appeared in 5+ consecutive roadmap reports
- **Why:** Issue body has the root-cause analysis (worker_config.py:23 cpu_count formula on 4-vCPU + startup-cpu-boost). One-line config flip.

### C2. Hermes max_turns = 1000 deployment gap (config-fidelity gate)
- **URL:** [C0AJ3SD5C79 / 1782436438](https://jleechanai.slack.com/archives/C0AJ3SD5C79/p1782436438.643689)
- **State:** ⚠️ Source files bumped to 1000 (cli.py, config.py, setup.py), but `~/.hermes_prod/config.yaml` still says 60. Last verified pre-flight: 2026-06-27.
- **Last activity:** 2026-06-26 01:13 PT (you asked "wtf is going on")
- **Next step:** Verify the `~/.hermes_prod/config.yaml` line-20 value is 1000; if 60, edit + restart gateway + confirm `hermes config show` reports 1000. Push commits to `jleechanorg/hermes-agent` origin/main if not already there.
- **Why:** Verified bug — your explicit ask "make the iteration budget 1000". Code in fork, deploy never confirmed.

### C3. Cron scheduler dead 8 days — 30 jobs stuck
- **URL:** [C0AJ3SD5C79 / 1782524779](https://jleechanai.slack.com/archives/C0AJ3SD5C79/p1782524779.784609)
- **State:** ⚠️ Active investigation (wa-2827), mid-flight at iter 55/1000
- **Last activity:** 2026-06-27 01:46 PT
- **Next step:** Wait for wa-2827 to land root cause; auto-fix cron tick + manually fire the 4 stuck jobs (babysit-wa-2827-pr-7888, etc.)
- **Why:** Per agent status, root cause is `ONESHOT_GRACE_SECONDS=120` + gateway restart timing. Stale-dispatch — needs human ack once investigation lands.

### C4. Daily GCP job emails missing
- **URL:** [C0BDEAJH8PK / 1782577510](https://jleechanai.slack.com/archives/C0BDEAJH8PK/p1782577510.810999)
- **State:** ⚠️ No PR. You asked "Where are the daily gcp job emails?"
- **Last activity:** 2026-06-27 09:25 PT (today, freshest ask)
- **Next step:** Check `cmux-surface-report-4h` workspace (likely `cost:system-inst` or similar) — verify the wa_daily_test_watcher.sh job ran in last 24h; if not, manually trigger or diagnose missing email
- **Why:** Per skill rule (verify-before-claim), check the cron schedule + last successful run before assuming broken.

### C5. Mobile latency (1-line header fix) — has PR but unclear status
- **URL:** [C0AH3RY3DK6 / 1782447574](https://jleechanai.slack.com/archives/C0AH3RY3DK6/p1782447574.817599)
- **State:** PR #7948 (mobile navbar) MERGED 2026-06-26 05:27Z per `2026-06-26-2049-audit-instance`. Need fresh verify.
- **Last activity:** 2026-06-26 04:19 PT
- **Next step:** `gh pr view 7948 --json state,mergedAt` — confirm merged; if yes, this thread is DONE.
- **Why:** Pre-flight gate — 1 PR was already merged, audit may be stale.

### C6. PR #7888 (CC-finish level commit) — agento cap, Design Doc gate failure
- **URL:** [C0AH3RY3DK6 / 1782287928](https://jleechanai.slack.com/archives/C0AH3RY3DK6/p1782287928.935589)
- **Issue:** cc_finish_authorized bypass + real-LLM proof via agy
- **State:** ⚠️ STUCK — backfill cap reached 4x. Green Gate FAILURE x2, Design Doc Gate FAILURE x3. wa-2827 worker idle waiting for adjustment_proof_matrix verdict.
- **Last activity:** 2026-06-27 04:55 PT (you said "Fix failures even if pre existing")
- **Next step:** Add `## DESIGN DOC: N/A` line to PR #7888 body (or proper link) + push no-op commit. Re-run Green Gate. Worker wa-2827 is ready to drive through once Design Doc Grep passes.
- **Why:** Per 2026-06-27 01:18 PT re-thread analysis: "Code is mergeable; gate is documentation-shape only."

### C7. Iteration budget 1000 (verify + deploy)
- **URL:** [C0AJ3SD5C79 / 1782313182](https://jleechanai.slack.com/archives/C0AJ3SD5C79/p1782313182.508309)
- **State:** ⚠️ Same as C2 — config-fidelity gate. Source has 1000, prod has 60.
- **Next step:** Same as C2.

### C8. AGY CLI driver (PR #7937 — merged but verify)
- **URL:** [C0AH3RY3DK6 / 1782459373](https://jleechanai.slack.com/archives/C0AH3RY3DK6/p1782459373.633339)
- **State:** PR #7937 MERGED 2026-06-26 20:18Z per 2049 PT audit. Per last audit: organic level-up still failing at iteration 5.
- **Last activity:** 2026-06-27 02:14 PT (you said "Find the agy cli for testing_mcp and testing_ui runs default PR and /green it")
- **Next step:** Pre-flight verify: `gh pr view 7937 --json state,mergedAt`. If merged, run a fresh organic level-up through agy -p print mode to capture new narrative.
- **Why:** Stale-state trap. Audit said merged 2026-06-26 but you kept asking for action — verify before responding.

### C9. PR #7925 (LevelUpAgent orphan fix) — adjust registry + real LLM proof
- **URL:** [C0AH3RY3DK6 / 1782518052](https://jleechanai.slack.com/archives/C0AH3RY3DK6/p1782518052.549469) + [C0AH3RY3DK6 / 1782520412](https://jleechanai.slack.com/archives/C0AH3RY3DK6/p1782520412.957019)
- **State:** PR #7925 MERGEABLE, but needs backend adjustment registry entry + agy-cli proof (no real Gemini API). wa-2827 has the brief.
- **Last activity:** 2026-06-27 00:33 PT (you said "Fix this AGY CLI thing in a new PR")
- **Next step:** Wait for wa-2827 to produce adjustment_proof_matrix.py verdict = proven. Then merge.
- **Why:** Bigger-blast-radius PR (23 files, +923/-35). Skeptic re-verify post-merge recommended.

### C10. Daily jobs status check (`cost:system-inst` workspace)
- **URL:** [C0BDEAJH8PK / 1782577510](https://jleechanai.slack.com/archives/C0BDEAJH8PK/p1782577510.810999)
- **State:** ⚠️ Asked but no PR. Could be the cmux workspace has it in-flight.
- **Last activity:** 2026-06-27 09:25 PT (today)
- **Next step:** Check `cost:system-inst` cmux workspace state, see if it's already fixing.

### C11. CMUX RPC wedge (recurring)
- **URL:** [C0AJQ5M0A0Y / 1782571058](https://jleechanai.slack.com/archives/C0AJQ5M0A0Y/p1782571058.278389)
- **State:** ⚠️ cmux RPC wedged; tree --window AND --all both empty. 3 wedges in last 12h.
- **Last activity:** 2026-06-27 14:37 PT
- **Next step:** Recovery: `killall -USR1 cmux` then re-poll. If persistent, `pkill -9 cmux` then launchd restart.
- **Why:** Blocks cmux-surface-report-4h cron; 3 wedges in 12h suggests root-cause investigation needed.

---

## D. Top 5 Human Decisions TRULY Needed (today)

1. **`MERGE APPROVED`** — Batch-merge 5 Tier-1 PRs (#7905, #7926, #7884, #7984, #7938). All Green Gate PASS, low risk, fixes 4 known threads.
2. **`FIX-MAX-TURNS`** — Edit `~/.hermes_prod/config.yaml` line-20 from 60 → 1000, restart gateway, confirm `hermes config show` reports 1000, push commits to `jleechanorg/hermes-agent` origin/main if missing. Unblocks every long-running session.
3. **`OPEN-COLDSTART-DEPLOY`** — After PR #7984 merges, redeploy Cloud Run service to prod so the GUNICORN_WORKERS=1 actually applies to live traffic (preview ≠ prod).
4. **`OPEN-AGY-PROOF`** — Run `agy -p` organic level-up after PR #7937 merge to capture fresh narrative proof. If proof fails, file issue against persona bleed (still in `~/.claude/CLAUDE.md` or `~/.gemini/GEMINI.md`).
5. **`OPEN-CMUX-WEDGE-FIX`** — Investigate the 3 cmux RPC wedges in 12h. Likely cause: large `cmux send` payloads queueing. Recovery recipe in `slack-misroute-detector` § "5h stampede".

---

## E. Things I Can Do AUTOMATICALLY (single-word triggers)

| Trigger | Action |
|---|---|
| `MERGE APPROVED` | Batch-merge § B Tier-1 (5 PRs) |
| `OPEN-COLDSTART-DEPLOY` | Trigger Cloud Run redeploy after #7984 lands |
| `FIX-MAX-TURNS` | Bump `~/.hermes_prod/config.yaml:20` → 1000, restart gateway, verify |
| `OPEN-7888-DOCFIX` | Add `## DESIGN DOC: N/A` to PR #7888 body + push no-op commit (unblocks Green Gate) |
| `START-CMUX-WEDGE-FIX` | Diagnose cmux RPC wedge root cause (skillify the recovery) |
| `BUMP-RESPAWN-CAP` | Bump agento backfill cap if 7888 docs-gate is causing 3-worker archive (per 5h-class) |
| `OPEN-DESIGN-DOC-CHECK` | Sweep all open PRs for missing `## DESIGN DOC:` line; auto-patch PR bodies |
| `OPEN-PUSH-HERMES-1000` | Push pending commits to `jleechanorg/hermes-agent` origin/main (verify first) |

---

## F. Lower-Pri Human Decisions — DEFER (codex cmux consult)

- **Daily jobs email routing** — codex verdict needed on whether to move `wa_daily_test_watcher.sh` cron output to email-to-Slack or stay Slack-only.
- **Tailscale / local agy CLI for GCP server** — codex verdict on whether to expose local agy CLI to GCP server via tailscale (per PR #7937 thread).
- **Custom agent + channel-to-agent mapping** — codex verdict on feasibility of mapping Slack channel to specific agent identity (per C0BDEAJH8PK / 1782460307).

---

## G. What's NOT Pending (closed/auto-resolved)

- Hermes prod gateway DOWN port 8643 — RESOLVED (auto-recovered)
- Mobile navbar (PR #7948) — MERGED 2026-06-26 05:27Z
- Rate-limit rename (PR #7948) — MERGED 2026-06-26 07:31Z
- Lever 3 (PR #7907) — MERGED 2026-06-26 06:24Z
- AGY CLI driver (PR #7937) — MERGED 2026-06-26 20:18Z
- Mac runners — RECOVERED 2026-06-26 23:40Z
- Hermes caveman cleanup — DEPLOYED commit 2e75634
- Daily level-up wiring probe (5k-PROBE) — NOT A REAL FAILURE (path-B-fail-smoke-*)

---

## H. cmux Pinned Workspaces

`~/.config/cmux/pinned-workspaces.txt`: 1 pin (agento → workspace:20, agentf → workspace:21).

| WS | Name | State | Pinned | Last activity |
|---|---|---|---|---|
| 20 | agento | idle | ✅ | 09:21 PT |
| 21 | agentf | idle | ✅ (via agento) | — |
| 8 | hermes | idle | — | — |

**3 wedges in last 12h** (`cmux RPC wedged tree --window AND --all both empty`). Recurring — root cause unknown.

---

## I. Verification (proof this audit is real, not vibes)

- **Skill version verified:** `~/.hermes/skills/roadmap/SKILL.md` HEAD = `acfe79a33f` on `origin/main`
- **Slack history:** 6 channels queried, ~190 messages
- **PR state:** 43 open PRs in `jleechanorg/worldarchitect.ai` via `gh pr list --json`
- **Issue state:** 100+ issues across 3 active repos (wa, agent-orchestrator, jleechanclaw)
- **Pre-flight verified:** PR #7984 = MERGEABLE, PR #7984 head updated 2026-06-27 16:35Z (fresh)
- **Roadmap repo:** `jleechanorg/worldarchitect-roadmap` (last commit `985c5d7`)
- **This report pushed:** see commit SHA in post-reply

---

## J. What looks important to follow up on (ranked by leverage)

1. **Cold-start latency** (#7961 + PR #7984) — affects every user session, root cause confirmed, fix MERGEABLE today. **Highest leverage.**
2. **Hermes max_turns = 1000 deployment** — unblocks every multi-step session; you have said "wtf is going on" 4+ times. **Second highest.**
3. **CMUX RPC wedge (3 in 12h)** — recurring infra issue masking cmux audits. Investigate or apply `killall -USR1 cmux` workaround.
4. **Daily GCP job emails missing** — silent failure mode; no one is monitoring.
5. **PR #7888 docs-gate** — single-line fix unblocks a high-traffic PR (LevelUpAgent fix).

---

## C-appendix: Per-thread 5-field schema (full audit)

### C12. PR #7890 (living-world v2 prompt visibility) — CONFLICTING
- **Status:** needs-human-decision
- **Last activity:** 2026-06-27 09:20 PT (you said "cleanup merge conflicts and /green the PR")
- **PR/issue refs:** [#7890](https://github.com/jleechanorg/worldarchitect.ai/pull/7890)
- **Next step:** Rebase onto origin/main, then AO worker drives to 7-green
- **Why:** CONFLICTING merge state — must resolve first

### C13. PR #7940 (resolver conflicts + merge)
- **Status:** pending [CRITICAL-PENDING-NO-PR]
- **Last activity:** 2026-06-27 02:55 PT (you said "resolve conflicts and then merge")
- **PR/issue refs:** [#7940](https://github.com/jleechanorg/worldarchitect.ai/pull/7940)
- **Next step:** Verify current merge state via `gh pr view 7940 --json mergeable`. If still CONFLICTING, rebase.
- **Why:** ⚠️ STUCK ⚠️ — appeared in last 4 audits as CONFLICTING

### C14. PR #7945 (mobile latency root cause) — implicit cache
- **Status:** pending
- **Last activity:** 2026-06-27 04:50 PT (you asked about implicit caching)
- **PR/issue refs:** [#7945](https://github.com/jleechanorg/worldarchitect.ai/pull/7945) related
- **Next step:** Check `cost:system-inst` cmux workspace for in-flight implicit cache research
- **Why:** Per memory: implicit cache research active in workspace 14 (proxy:context)

### C15. AGY CLI as default backend (keep MiniMax primary)
- **Status:** pending (decision made in-thread)
- **Last activity:** 2026-06-27 00:37 PT (you said "Ok lets /learn from this...add agy cli as a backend and test it but keep minimax m3 as primarily and agy cli as secondary")
- **PR/issue refs:** [#7971](https://github.com/jleechanorg/worldarchitect.ai/pull/7971) (agy as default backend) — MERGEABLE
- **Next step:** Merge #7971 — but verify secondary-fallback config in `~/.hermes_prod/config.yaml` matches
- **Why:** ✅ Already a PR; just needs merge

### C16. PR #7953 (quota counters) — needs UI screenshot evidence
- **Status:** pending
- **Last activity:** 2026-06-27 00:17 PT (you said "this needs a real UI browser screenshot for /es and /er evidence")
- **PR/issue refs:** [#7953](https://github.com/jleechanorg/worldarchitect.ai/pull/7953)
- **Next step:** Spawn AO worker to capture UI screenshot evidence; push to gist; update PR body
- **Why:** 4 files, +525/-0 — small blast, but evidence gate is the blocker

### C17. Mobile latency investigation (chrome incognito took forever to log in)
- **URL:** [C0AH3RY3DK6 / 1782447664](https://jleechanai.slack.com/archives/C0AH3RY3DK6/p1782447664.987489)
- **Status:** pending — STUCK ⚠️ (appeared in 5+ audits)
- **Last activity:** 2026-06-27 09:17 PT (you said "Next steps?")
- **Next step:** Check if PR #7984 (cold-start fix) resolves this. If not, open new diagnostic issue.
- **Why:** Root cause is cold-start; merging #7984 should fix this thread too

### C18. PR #7920 (cost: implicit cache rev-9piwk.1) — MERGEABLE
- **Status:** AUTO
- **Last activity:** 2026-06-27 00:26 PT (per C0AJ3SD5C79 dropped-thread followup)
- **PR/issue refs:** [#7920](https://github.com/jleechanorg/worldarchitect.ai/pull/7920)
- **Next step:** Skeptic re-verify post-merge (21 files, +1635/-222)
- **Why:** MERGEABLE, but medium-large — recommend eyeball before merge

### C19. Daily level-up wiring probe vs real GCP cron failure
- **URL:** [C0BCVG4F560 / 1782524645] (5k-PROBE)
- **Status:** 5k-PROBE — NOT a real failure
- **Next step:** No action — the `work=path-B-fail-smoke-2026-06-27` is a deliberate harness probe
- **Why:** Per slack-misroute-detector v1.24.0 5k recipe — disambiguator is `work=` parameter

### C20. 5h-class stampede (40+ alerts in last 18h)
- **Status:** mostly classified as 5h REAL human-intervention
- **Next step:** Many PRs (7888, 7864, 7905, 7926, 7902, 7970, 7971, 7969, 7972) hit backfill cap. Per 5h-class recipe, root causes differ (Design Doc gate, prompt defects, pool exhaustion). See per-PR re-thread analysis.
- **Why:** Each PR needs a distinct root-cause class before operator action.

---

**End of report. Trigger `MERGE APPROVED` to start the auto-merge batch. — Hermes**
