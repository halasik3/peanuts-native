# Peanuts FEW: changelog

The first section below goes at the top of every release's notes. Keep it current: it is the one place that says how far
Fire Emblem Warriors has got. Older entries move under "History".

## Status: Fire Emblem Warriors (Switch, update 1.5.0)

- **Boots and runs at 60 fps in the menus** (first test on the AYN Odin 3, Turnip). Sound, controller and the movie decoder work.
- **This build adds the 7 shaders the game compiles at boot.** They're the same as Hyrule Warriors: Definitive Edition's. On the first
  build they were missing, which left the menus without text and the opening movie black. **Build** the game again in Peanuts FEW:
  after Prepare, the app starts the game once by itself to capture them (about a minute). Then the pack is finished.
- Not tested yet: a battle, the system driver, the AYN Thor.

## History

### First boot

- Boots to the menus at 60 fps on the Odin 3 (Turnip Gen8 V39). Missing: the 7 run-time GLSLC shaders (no menu text, black movie). Their keys match Hyrule Warriors: Definitive Edition's, so the profile now lists them for the in-app capture.

### Fire Emblem Warriors profile

- Survey of 1.5.0 on Windows with the fork's survey kit; provisional profile and shader tables in `dm/games/0100F15003E64000`.
- Added to `fork/extra-titles.txt`, so Peanuts FEW builds include it.

### Fork set up

- Fork of igawa6/peanuts-native, synced with upstream every 6 hours (`.github/workflows/fork-sync.yml`).
- Each sync or push to main builds **Peanuts FEW** (`dev.nxnative.android.peanutsfew`), which installs beside the official app,
  and publishes it as a release (`.github/workflows/fork-release.yml`).
