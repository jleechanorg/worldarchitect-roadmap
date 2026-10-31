
## 2026-10-31 (Grok Scenes)
- When Grok Bot usage runs out, background work dies silently, sometimes after a partial write (for example, the Firestore cadence stamp was written but never reported). Read back the state before redoing anything.
- Several agents drive the same stack. Check commit authors before trusting stage labels, and keep each agent's attribution in the handoff doc.
- UI video evidence needs Send and typing on screen; a recording at 1 fps or one that starts after Send fails the mpdecimate frame rule. Record at 10 fps with /health showing the build SHA.
- The /static-review template lives only on jleechan-skills #624's branch until it merges; fetch it with ?ref=<sha>.
