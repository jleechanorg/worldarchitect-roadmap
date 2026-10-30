# Alexiel SpriteBuilder approach (worldai_claw) — 2026-10-30

How the repo's own sprite builder works, what was verified against it on
2026-10-30, and where it fits next to the LPC composer. Recorded after the
camp2/camp3 demo iterations, which tested both methods on the same camp map.

## What SpriteBuilder is

- The repo's layered-clip composer: `packages/web/src/spritebuilder/`
  (`SpriteBuilderScreen.tsx`, `compose.ts`, `validate.ts`, `export.ts`,
  `loadAssets.ts`, `playback.ts`, `types.ts`), route `/game/sprite-builder`.
- It composes `dk.layered-clip/v1` packages instead of redrawing a character
  on equipment change. The Alexiel package lives at
  `packages/web/public/assets/spritebuilder/alexiel/` (`manifest.json` +
  `hero.png` atlas, 8561x200, plus CREDITS).
- Package facts (verified from the manifest): canvas 256x256, root [128,232],
  8 facings, actions idle + walk, 102 regions, 9 plane slots. Defaults:
  body-base / head-base / hair-base / garment-base / hat-a / weapon-a.
- Compose math (from `compose.ts`): direct cel offset = trimOrigin +
  localOffset; dest = screenRoot + (cel offset - root) * scale, with
  image smoothing off; mirrored cels reflect across root.x.

## What was built and verified 2026-10-30

- Composed idle + walk frames for south/east/west/north from the package
  (walk = walk body plane + idle other-planes in idle draw order).
- The flagship 1024px stills (walk front/back/left/right + idle) were used
  as the camp2 demo hero. Their "magenta background" is actually alpha=0,
  so no chroma-keying is needed.
- A side-by-side showcase (SpriteBuilder vs LPC composer) was built the
  same day: flagship still, composed walk frame, composed idle frame,
  LPC hero sheet, and enlarged LPC frames, plus the camp dialog text style.

## Limits found in the package (not guesses)

- Walk timelines carry ONLY the body plane (8 frames x facings, drawOrder
  `["body"]`). Only the body-base variant has walk cels; head, garment,
  hair, hat, and weapon variants are idle-only.
- Consequence: the walk cycle is subtle (garment covers the legs), and
  side views lack swords.
- Idle draw order (south): hair-back, body, garment-front, head,
  hair-front, hat, weapon-back, weapon-front (8 planes). Idle east/west/
  north have only 4 planes (no hair-front, hat, or weapon).
- Single character: only Alexiel exists in this style. More characters
  in this language require new generation; they cannot be composed from
  existing parts the way LPC characters can.

## Verdict

- SpriteBuilder/Alexiel wins on fidelity: the most detailed character art
  in the repo. Best use is hero close-ups and portraits.
- The LPC composer wins for a walking cast and world coherence: real
  8-frame leg cycles, a new character in minutes, and one visual language
  with the LPC terrain. The camp3 demo (all LPC, 128px, new purple/auburn
  hero) reads as one game for exactly this reason.
- Do not mix the two on one screen. The camp2 demo (detailed anime hero
  over chibi LPC NPCs on chunky terrain) was judged "still looks terrible"
  twice; dropping Alexiel for an all-LPC cast was the fix that landed.

## Open threads this does not decide

- True higher-res terrain: no higher-res terrain exists in the repo; the
  camp demos upscale 32px source cells. New terrain art needs generation
  (the repo's proven image path is Grok; the code default
  `GROK_IMAGE_MODEL` is `grok-imagine-image`, while the proven recipe used
  `grok-imagine-image-quality`).
- Whether to push the camp demos to the repo as a PR (asked, unanswered
  as of 2026-10-30).
