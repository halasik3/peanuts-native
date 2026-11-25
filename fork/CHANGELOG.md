# Peanuts FEW: changelog

The first section below goes at the top of every release's notes. Keep it current: it is the one place that says how far
Fire Emblem Warriors has got. Older entries move under "History".

## Status: Fire Emblem Warriors (Switch, update 1.5.0)

- **Plays: menus, movies, text, whole missions** (AYN Odin 3, Turnip), about 60 fps in battle.
- **This build draws the special-attack and hit particles properly.** Their vertex counts are computed on the GPU, and now the GPU also
  turns them into the draw (before, the CPU guessed them too early: a hang, later black squares around torches during hits).
- **Torches and lights no longer flicker** (few.9): particle data computed on the GPU was read from a copy several frames old.
- Open: dark / shadowed enemies.

## History

### Buffer textures written by storage buffers

- A storage buffer's pending stores now send buffer textures over that memory to the GPU's copy instead of the CPU's bytes (`vka_draw.c` `stage_writes`). The few.8 run: torches flickered off with a dark spot, lights and mountains flickered while panning; five 16384x65 particle buffers were re-uploaded after GPU stores 65,536 times.

### Particles on the GPU

- Non-indexed indirect quad draws are converted by a compute pass into indexed indirect draws (`vka_exec.c` `qix_convert`, `quad_indirect.comp`), so their counts are read by the GPU. `DM_VK_QUAD_IND=0` turns it off.

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
