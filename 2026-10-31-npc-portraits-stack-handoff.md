# NPC portraits / scene stack: handoff (2026-10-31 12:10 PM PT)

Grok Scenes has paused coding at Jeffrey's request. Read this first, then the detailed doc copied below (from `roadmap/npc-portraits-stack-status.md` on #10953's branch).

## Current state (live from GitHub, 2026-10-31 ~12:05 PM PT)
| PR | Branch | Head | Draft | Label |
|---|---|---|---|---|
| #10970 S1 present_characters schema | feat/npc-portraits-10608-s1-schema-presence | ded86788 | no | stage:5-final-approval |
| #10971 S2 portrait backend | feat/npc-portraits-10608-s2-portrait-backend | c8797360 | no | stage:5-final-approval |
| #10972 S3 scene reference faces | feat/npc-portraits-10608-s3-scene-references | d5d27344 | no | stage:5-final-approval |
| #10613 S4 portrait strip UI | feat/npc-portraits-10608 | 43d1738c | yes | stage:3-evidence-review |
| #10953 NPC auto-portraits | feat/npc-auto-portraits-all-present | 23756564 | no | stage:3-evidence-review |

## Important: other agents pushed after Grok Scenes' last action
Since 2026-10-30 ~2 PM PT, other coders (commit prefixes "gemini/gemini-3.8-flash", "[gemini][gemini-3-flash]", "gemini-3.7-flash") pushed merges of main and fixes to #10970, #10971, and #10953 (and #10613 moved to 43d1738c). Those pushes also undrafted the PRs and moved them to stage 5. Grok Scenes did not make those stage/undraft changes and has NOT verified them. Per standing rules, a resumer must re-verify every gate at the current heads before merging.

## Grok Scenes' last verified results (at the old heads)
- #10970 @86ce9fe3: two cold /static-review seats NOT APPROVED. P1s: stale prompt_tool_contracts.json hash, conflict with main, evidence bound to 8b71a6ba, missing BQ-logged live rows, AGY waiver needed a recorded source (Jeffrey 2026-10-29: "Use gemini api"). Some of these appear addressed by later commits fde181f6/c712301f/aac4465d/ded86788 (author unverified).
- /er: #10970 PASS; #10971/#10972/#10613 PARTIAL (no visual review, evidence from the stack-top preview); #10953 PARTIAL (no auto-portrait proof; jleechantest lacks admin claim).
- Preview evidence gist: https://gist.github.com/jleechan2015/828e46c70eef07b99ca24f8d2ccdfcf6 (manual portraits, scene 6 reference faces + composite, scenes 7-9 cadence).
- New, NOT yet uploaded: /workspace/evidence/s10run4/ (build 5b4db48b, scenes 10-11, typing + Send + image appear; mpdecimate 1100/1582 unique). Passes the ui-video-evidence frame rule.
- The /static-review skill exists only on jleechan-skills #624's branch (ab22bc9); #624 is unmerged.

## Test override still active (revert when done)
Firestore `users/<jleechantest uid>` settings.scene_illustrations_cadence_revision is stamped so jleechantest gets cadence 1. To revert, delete that field; every_n was already 1. A backup is at /workspace/evidence/cadence_backup.json on the box.

## Next steps for a resumer
1. Verify who pushed the new heads and whether those stage-5 labels are earned. Run /er, then two cold /static-review seats at each current head.
2. Upload s10run4 to gist 828e46c7 and run visual verification for #10613, #10953, and #10972.
3. #10953 auto-portraits: Jeffrey decides between an admin claim for jleechantest and accepting manual-only evidence.
4. Merge bottom-up at verified stage 5 (pre-approved). Then #624: second vote, CodeRabbit, merge, hermes install.

---

# NPC portraits stack (#10608): status and handoff

Last updated: 2026-10-30 ~14:40 PDT (executor /prw pass; see "/prw pass 2026-10-30 14:40" below). Lives only on the top-of-stack branch
`feat/npc-auto-portraits-all-present` (#10953) so it is not copied into the lower PRs.
Refresh it every ~20 min of work (push first, then update this file).

## Stack (bottom → top, merge bottom-up)

| PR | Branch | One-line summary | Prod LOC* | Non-prod LOC* | /prw stage | Head |
|----|--------|------------------|-----------|---------------|-----------|------|
| #10970 | `feat/npc-portraits-10608-s1-schema-presence` (base main) | Slice 1/4: model-authored current-scene NPC presence (schema) | +334/-22 | +8767/-2888 | 3 evidence review (ready, not draft) | `86ce9fe3900e314953e0c65d4271baa9e84d6895` |
| #10971 | `feat/npc-portraits-10608-s2-portrait-backend` | Slice 2/4: portrait backend, per-campaign cap + API | +1882/-30 | +2425/-21 | 3 evidence review (draft) | `2d1b7a2bd9de3123c71e1dbe99a095fb030051cd` |
| #10972 | `feat/npc-portraits-10608-s3-scene-references` | Slice 3/4: scene NPC reference faces + composite sheet | +1000/-37 | +1631/-29 | 3 evidence review (draft) | `2690e37569e775146e9a843ba7278f2031382204` |
| #10613 | `feat/npc-portraits-10608` | Slice 4/4: 50 portraits per campaign, bounded scene references, portrait strip UI | +544/-1 | +1301/-0 | 3 evidence review (draft) | `6ca0fc415ae5d802c52f8116c3bf9489b84b5011` |
| #10953 | `feat/npc-auto-portraits-all-present` | Auto portraits for every present NPC (admin-gated toggle) | +243/-48 | +4962/-5295 | 3 evidence review (ready) | `5b4db48b3956190d8056501cc4487421d43b57a0` (before this doc commit) |

\* From the GitHub PR files API vs each PR's base. Heuristic: tests, `roadmap/`, `docs/`, `*.md`
and `*.json` count as non-prod, so the generated `gemini_schema_acceptance.json` manifest
lands in non-prod here (PR bodies count it as prod). Re-check with
`gh api repos/jleechanorg/worldarchitect.ai/pulls/<n>/files`.

## Evidence gists (gist.github.com/jleechan2015/<id>)

- Local CI at head: #10970 `1680b1412987cea366bbda94e59b21c9`, #10971 `8b3c3943045e7ce679adfa2a17a58ed0`,
  #10972 `5fe9682b1bbc43f8955cf8148c1d5c53`, #10613 `c5b515972cedddf8b9ec59c28b8ab7d3`,
  #10953 `ce3d9578784ecd8fedbf3f8b0fe80986`.
- Main baseline (JS baseline + first-chunk order-dependence proof): `d2963d73168da8aa455b9376fe3ac1e7`.
- Live Gemini production-path repair-turn (#10970): `c4d6f49c938d2cc439c4ede96e11f295`.
- Preview s10 live evidence (runs 1–3, checksums.sha256): `828e46c70eef07b99ca24f8d2ccdfcf6`.

Remote CI: red checks fail in "Set up job" (self-hosted runner `Device or resource busy`),
infrastructure only; local-CI gists are the test evidence.

## Preview environment

- URL: https://mvp-site-app-s10-i6xf2p72ka-uc.a.run.app (slot **s10**, `/health` git_commit `5b4db48b…`).
- Test account: **jleechantest** (no admin claim). Campaign: `gPsRFywvRE0jn3r9L2Dt` ("S10 Portrait Evidence Test").

## Proven (gist 828e46c7)

1. Manual NPC portraits (Misa, Captain Rorik, Alden Vance): live suggest + image generation, HTTP 200, stored ready in Firestore; portrait strip renders.
2. Scene 6: illustration request carried reference faces (1 individual portrait + composite sheet of the other 2); composite built, public, sha-bound to the stored image.
3. Every-scene cadence: scenes 7, 8, 9 each illustrated on consecutive turns, 13:47–13:51 PDT 2026-10-30 (run 3).

## Cadence test override (prod Firestore — the only allowed write)

- `users/0wf6sCREyLcgynidU5LjyZEfm7D2` → `settings.scene_illustrations_cadence_revision` was stamped so the account's saved every_n=1 applies.
- **Revert:** delete that one field. Backup of the prior settings: `/workspace/evidence/cadence_backup.json` (on the agent box, not in the repo).

## Left to do (in order)

1. **Auto-portraits live proof** needs an admin claim on jleechantest — Jeffrey's call. Do not grant it yourself, do not bypass auth.
2. **/er** (independent evidence review) at the current heads of all five PRs.
3. **Fresh /static-review seats** at current heads, plus the asks in Slack #dot-coordination
   (channel `C0C7SF0S4JH`, thread `1793249612.849529`).
4. **Visual verification** seats for #10613, #10953 and #10972 (screenshots/clips in gist 828e46c7).
5. **#10970:** capture the model-routing evidence, and narrow the AGY claim in the PR body to unit tests
   (live Gemini, gist c4d6f49c, stands in for AGY per Jeffrey).
6. **Stage 4:** undraft #10971/#10972/#10613, CI/readiness; then **bottom-up merge**
   #10970 → #10971 → #10972 → #10613 → #10953 (merge pre-approved once stage 5 is reached).
7. **jleechan-skills #624:** second /advice vote, CodeRabbit re-review, merge, then hermes install.


## /prw pass 2026-10-30 14:40 PDT (executor subagent)

Heads checked, unchanged since the table (no foreign pushes): #10970 `86ce9fe3`, #10971 `2d1b7a2b`,
#10972 `2690e375`, #10613 `6ca0fc41`, #10953 `310a6c74` (= 5b4db48b + this doc only).

Skills fetched from jleechan-skills: prw, pr-lifecycle, evidence-review, evidence-standards, ui-video-evidence.
**`.claude/skills/static-review/SKILL.md` returns 404** (no `static-review` dir in the repo), so the
static-review revision preamble and template are unavailable. /advice seats were **not run**, and nothing was reconstructed.
The executor also cannot spawn cold seats, and there is no `ai_orch`, `codex` or `claude` CLI on the box.

/er lane: executor subagent. It did not produce the evidence (the parent's browser runs did), but it is the same bot, and the
codex dispatch was unavailable. Treat the lane as weakly independent.

| PR | /er raw verdict | Gaps |
|----|-----------------|------|
| #10970 | PASS (non-UI) | Routing capture is 1 run/case at 8b71a6ba. It applies to 86ce9fe3 by delta (one non-prod file, `testing_mcp/schema/gemini_schema_incremental.py`, +9). The PR body now says this, and the AGY claim is narrowed to unit tests. /advice is retained at 3200161e and not restamped. |
| #10971 | PARTIAL | Live evidence is from preview at the stack top 5b4db48b (derived for this head). No /visual-verification seat. |
| #10972 | PARTIAL | run2_clip_scene6 kept 38/486 (7.8%), mostly the Alden dialog. The Send action is not frame-verified. BQ ref/composite sha binding is strong. No visual seat. |
| #10613 | PARTIAL | clip_strip kept 50/400. No visual seats (two needed: headline is user-visible). |
| #10953 | PARTIAL | Auto-portraits are unproven (admin claim, Jeffrey's call). run3_session.mp4 is INSUFFICIENT (below). No visual seats. |

mpdecimate (kept/nominal): manual_generate 471/760, scene_turn 76/555, strip 50/400, run2_alden 262/320,
run2_scene6 38/486, **run3_session 40/1060 (3.8%)**.

**run3 judgment:** the URL bar is visible, and so are the before state (Scene 6 header, 0–20 s) and after states (Scene 7 at 54 s, Scene 8 at 150 s, Scene 9 at 183 s, each with an
illustration). 16 of the 40 kept frames are the loading spinner (0–12 s). **No frame shows the input/choice being entered or Send
being clicked.** The player text is already submitted by 20.4 s and at every later turn. This fails "Action must be in the window".
**Recapture needs:** a fresh x11grab at ≥5 fps from the same build, with the composer visible (scroll to bottom). Typing the action and the
Send click must be on screen for each of ≥1 (ideally 3) turns, followed by the streamed reply and the scene illustration appearing, with the Scene N header
in frame. Also needed: a caption naming the Send and image-appear timestamps, and the /health SHA shown in the session.

Stage 4/5 eligibility: **none** (all lack /advice at head and visual seats; the lower three also lack PASS /er).

## Standing rules

- No auth bypass; no granting claims or minting tokens.
- Prod is read-only, except the single cadence stamp above.
- Normal commits and pushes only: no rebase, no force-push.
- Before pushing to any stack branch, fetch; if someone else pushed since the heads above, **stop and report**.
- Never open `.env` files; no secrets in files, gists or PR text.

## Resume checklist

```bash
export GH_TOKEN=$(cat ~/.gh_token_wa)   # never echo
for p in 10970 10971 10972 10613 10953; do
  gh pr view $p -R jleechanorg/worldarchitect.ai --json headRefOid,labels,isDraft; done
```
Local checkouts with these branches live under `/workspace` (e.g. `wt-pc`, `stk-s1`..`stk-s5`,
`sf/split/*`); as of this update none had unpushed or uncommitted work.
