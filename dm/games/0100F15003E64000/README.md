<!-- PEANUTS: added by the halasik3/peanuts-native fork (Peanuts FEW) -->
# Fire Emblem Warriors (`0100F15003E64000`)

Update 1.5.0 (v327680) over the base game, SDK 3.7.0. Koei Tecmo's KTGL engine on NVN (Omega Force and Team Ninja, the Hyrule Warriors team). Modules `main`, `subsdk0` (GLSLC, NVN's run-time shader compiler), `subsdk1` (the movie library, NintendoSDK_movie 3.7.0) and `sdk`. Started from the NSP script's provisional profile, made on Windows from a dump of update 1.5.0.

Status: boots and plays on Android (2026-11-25, AYN Odin 3, Adreno 830, Turnip Gen8 V39): the opening movie, the title and the menus at 60 fps (movies at 30, the game's own present interval 2), sound, a controller. The first build lacked the 7 run-time shaders: no menu text and a black movie picture, 15 % of draws skipped. Their rows are now in the map (see Shaders). Not yet tested: the system driver, a battle, the AYN Thor (Adreno 740).

## Builds

| Version | `main` build ID | Notes |
|---|---|---|
| 1.5.0 (v327680) | `1953770037acc52a4e28bf7aa5968c03` | the only build in the profile; the base game alone (v0) is not registered |

## Shaders

- The split of 1.5.0 found 656 shaders (compute 40, geometry 2, pixel 386, vertex 228): 574 in the RomFS's `nx/shader` packages (`.spkg`) and 82 GLSLC outputs in `main`, as in the other KTGL games.
- **7 run-time shaders** (current): `main` holds 7 GLSL sources that it compiles with its own GLSLC (`subsdk0`) at boot. The first run's log named four of them as missing from the library (`8f8eab868b7515ae`, `4ebb90a8d0ce4166`, `4a9827c6eb662959`, `24344858e2453d06`), and all four are [Hyrule Warriors: Definitive Edition](../0100AE00096EA000/README.md)'s run-time keys: the two games compile the same 7 sources to the same outputs, although their GLSLC builds differ (SDK 3.7.0 and 3.5.1). The map has Hyrule Warriors' 7 `/glslc_capture/` rows (`vs_runtime.bin` 1, `ps_runtime.bin` 6; `shader_groups … /glslc_capture/=runtime`, as Fire Emblem: Three Houses), so the app's Build captures them on the device after Prepare. Without them the host skipped the menus' text draws and the movies' picture.

## Memory

- 4 GB layout as the provisional profile guessed it: `mem_reserve 0x100000000`, `mem_alias 0x10000000`, `mem_stack 0x10000000`, `app_pool 0xCD500000`, `sys_resource 0x0` (the NPDM declares no system resource). The same values as Hyrule Warriors: Definitive Edition's; not measured on this game yet.

## Found on this game

- The run-time GLSLC outputs are byte for byte Hyrule Warriors: Definitive Edition's (see Shaders).
- SDK 3's `movie::Decoder` (taken over for Hyrule Warriors: Definitive Edition) decodes the movies on the phone's hardware decoder (`c2.qti.avc.decoder`, 1920×1080 High profile).

## Open

- A build with the run-time capture: the menus' text and the movies' picture.
- A battle; the system driver; the AYN Thor.
