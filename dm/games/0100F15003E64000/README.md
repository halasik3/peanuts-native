<!-- PEANUTS: added by the halasik3/peanuts-native fork (Peanuts FEW) -->
# Fire Emblem Warriors (`0100F15003E64000`)

Update 1.5.0 (v327680) over the base game, SDK 3.7.0. Koei Tecmo's KTGL engine on NVN (Omega Force and Team Ninja, the Hyrule Warriors team). Modules `main`, `subsdk0` (GLSLC, NVN's run-time shader compiler), `subsdk1` (the movie library, NintendoSDK_movie 3.7.0) and `sdk`. Started from the NSP script's provisional profile, made on Windows from a dump of update 1.5.0.

Status: profile only (2026-11-25). Not yet booted on Android. The target device is an AYN Thor (Adreno 740), tested on Turnip and on the system driver.

## Builds

| Version | `main` build ID | Notes |
|---|---|---|
| 1.5.0 (v327680) | `1953770037acc52a4e28bf7aa5968c03` | the only build in the profile; the base game alone (v0) is not registered |

## Shaders

- The split of 1.5.0 found 656 shaders (compute 40, geometry 2, pixel 386, vertex 228): 574 in the RomFS's `nx/shader` packages (`.spkg`) and 82 GLSLC outputs in `main`, as in the other KTGL games.
- **Open: 7 run-time shaders.** `main` holds 7 GLSL sources that it compiles with its own GLSLC (`subsdk0`) at boot, like [Hyrule Warriors: Definitive Edition](../0100AE00096EA000/README.md)'s 7 built-in shaders. The profile has no `/glslc_capture/` rows for them yet, so the pack lacks them and the host skips their draws. Their keys come from one capture run (`DM_GLSLC_CAPTURE`); Hyrule Warriors' keys are not reused, because its GLSLC is another build (SDK 3.5.1).

## Memory

- 4 GB layout as the provisional profile guessed it: `mem_reserve 0x100000000`, `mem_alias 0x10000000`, `mem_stack 0x10000000`, `app_pool 0xCD500000`, `sys_resource 0x0` (the NPDM declares no system resource). The same values as Hyrule Warriors: Definitive Edition's; not measured on this game yet.

## Found on this game

- Nothing yet.

## Open

- First boot on Android, then the run-time shader capture.
- The movies (`nx/movie/*.mp4`, 36 files): SDK 3's `movie::Decoder`, taken over for Hyrule Warriors: Definitive Edition ([Movies](../0100AE00096EA000/README.md#movies)).
