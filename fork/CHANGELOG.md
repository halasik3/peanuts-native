# Peanuts FEW: changelog

The first section below goes at the top of every release's notes. Keep it current: it is the one place that says how far
Fire Emblem Warriors has got. Older entries move under "History".

## Status: Fire Emblem Warriors (Switch, update 1.5.0)

- **Profile added; first boot test next.** This build includes Fire Emblem Warriors (`0100F15003E64000`) with a provisional profile
  made from the 1.5.0 survey. It's based on Hyrule Warriors: Definitive Edition: same KTGL engine, same memory layout.
- Shaders: 656 found in the game's files. The 7 shaders the game compiles at boot aren't captured yet, so expect some 2D or text
  draws to be missing even if it boots.
- How to test: add the base game and the 1.5.0 update in Peanuts FEW, **Build** (Turnip driver first), Play, then Share log.
- Device: AYN Thor (Adreno 740).

## History

### Fire Emblem Warriors profile

- Survey of 1.5.0 on Windows with the fork's survey kit; provisional profile and shader tables in `dm/games/0100F15003E64000`.
- Added to `fork/extra-titles.txt`, so Peanuts FEW builds include it.

### Fork set up

- Fork of igawa6/peanuts-native, synced with upstream every 6 hours (`.github/workflows/fork-sync.yml`).
- Each sync or push to main builds **Peanuts FEW** (`dev.nxnative.android.peanutsfew`), which installs beside the official app,
  and publishes it as a release (`.github/workflows/fork-release.yml`).
