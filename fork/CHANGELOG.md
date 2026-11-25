# Peanuts FEW: changelog

The first section below goes at the top of every release's notes. Keep it current: it is the one place that says how far
Fire Emblem Warriors has got. Older entries move under "History".

## Status: Fire Emblem Warriors (Switch, update 1.5.0)

- **Plays: menus, movies, text and battles** (AYN Odin 3, Turnip). The 7 run-time shaders are captured by Build.
- **This build stops the freeze and crash during special attacks.** Their particle effects are drawn with vertex counts the GPU
  computes, and the host read them too early, which made it draw billions of quads. Those draws are now skipped, so some special-attack
  particles may be missing until the proper fix: the GPU reads the counts itself.
- Not tested yet: the system driver, the AYN Thor.

## History

### Text, movies, battles

- The in-app capture of the 7 run-time shaders fixed the menu text and the movies.
- A freeze and GPU hang during special attacks: GPU-written indirect quad records read stale on the CPU. Such draws are skipped for now (workaround).

### First boot

- Boots to the menus at 60 fps on the Odin 3 (Turnip Gen8 V39). Missing: the 7 run-time GLSLC shaders (no menu text, black movie). Their keys match Hyrule Warriors: Definitive Edition's, so the profile now lists them for the in-app capture.

### Fire Emblem Warriors profile

- Survey of 1.5.0 on Windows with the fork's survey kit; provisional profile and shader tables in `dm/games/0100F15003E64000`.
- Added to `fork/extra-titles.txt`, so Peanuts FEW builds include it.

### Fork set up

- Fork of igawa6/peanuts-native, synced with upstream every 6 hours (`.github/workflows/fork-sync.yml`).
- Each sync or push to main builds **Peanuts FEW** (`dev.nxnative.android.peanutsfew`), which installs beside the official app,
  and publishes it as a release (`.github/workflows/fork-release.yml`).
