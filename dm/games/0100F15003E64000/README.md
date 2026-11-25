<!-- PEANUTS: new profile, provisional -->
# Fire Emblem Warriors (`0100F15003E64000`)

Update 1.5.0 (v327680) over the base game, SDK 3.7.0. Koei Tecmo's KTGL engine on NVN (Omega Force and Team Ninja, the Hyrule Warriors team). Modules `main`, `subsdk0` (GLSLC, NVN's run-time shader compiler), `subsdk1` (the movie library, NintendoSDK_movie 3.7.0) and `sdk`. Started from the NSP script's provisional profile, made on Windows from a dump of update 1.5.0.

Status: plays on Android on Turnip (2026-11-25, AYN Odin 3, Adreno 830, Android, Turnip Gen8 V39): the opening movie, the title and the menus at 60 fps (movies at 30, the game's own present interval 2), sound, a controller, and whole missions (chapters 1 and 2) with special attacks at about 59 fps. It needs two changes to the Vulkan replay that have pull requests of their own: indirect quads converted on the GPU (`DM_VK_QUAD_IND`) and storage-buffer stores ordering buffer-texture reads (`DM_VK_TBUF_GW_SB`, which this profile turns on). Qualcomm's own driver does not reach a battle (see Effects): Turnip is recommended. Not tested: the AYN Thor (Adreno 740), chapters past 2.

## Builds

| Version | `main` build ID | Notes |
|---|---|---|
| 1.5.0 (v327680) | `1953770037acc52a4e28bf7aa5968c03` | the only build in the profile; the base game alone (v0) is not registered |

## Shaders

- The split of 1.5.0 found 656 shaders (compute 40, geometry 2, pixel 386, vertex 228): 574 in the RomFS's `nx/shader` packages (`.spkg`) and 82 GLSLC outputs in `main`, as in the other KTGL games.
- **7 run-time shaders**: `main` holds 7 GLSL sources that it compiles with its own GLSLC (`subsdk0`) at boot. The first run's log named four of them as missing from the library (`8f8eab868b7515ae`, `4ebb90a8d0ce4166`, `4a9827c6eb662959`, `24344858e2453d06`), and all four are [Hyrule Warriors: Definitive Edition](../0100AE00096EA000/README.md)'s run-time keys: the two games compile the same 7 sources to the same outputs, although their GLSLC builds differ (SDK 3.7.0 and 3.5.1). The map has Hyrule Warriors' 7 `/glslc_capture/` rows (`vs_runtime.bin` 1, `ps_runtime.bin` 6; `shader_groups … /glslc_capture/=runtime`, as Fire Emblem: Three Houses), so the app's Build captures them on the device after Prepare. Without them the host skipped the menus' text draws and the movies' picture (15 % of draws).

## Memory

- 4 GB layout as the provisional profile guessed it: `mem_reserve 0x100000000`, `mem_alias 0x10000000`, `mem_stack 0x10000000`, `app_pool 0xCD500000`, `sys_resource 0x0` (the NPDM declares no system resource). The same values as Hyrule Warriors: Definitive Edition's; not measured on this game yet.

## Found on this game

- The run-time GLSLC outputs are byte for byte Hyrule Warriors: Definitive Edition's (see Shaders).
- Indirect quads whose records the GPU writes, converted on the GPU ("Indirect quads converted on the GPU" in docs/reference/rendering.md), and buffer textures written through storage buffers ("Storage-buffer stores and buffer textures"): see Effects.
- SDK 3's `movie::Decoder` (taken over for Hyrule Warriors: Definitive Edition) decodes the movies on the phone's hardware decoder (`c2.qti.avc.decoder`, 1920×1080 High profile).

## Effects

- **GPU particles drawn as indirect quads.** The special attacks' and hits' effects are `DrawArraysIndirect` quads whose record the GPU writes in the same submission. The Vulkan replay made quad indices on the CPU, so it read the record there ([Indirect draws and dispatches read by the GPU](../../../docs/reference/rendering.md#indirect-draws-and-dispatches-read-by-the-gpu)) and got stale bytes: `indirect draws of quads or a line loop read their record on the CPU at replay (first: 1077952577 vertices, 1027424064 instances)`, `scratch block of 6-11 GB not allocated`, and once such an expansion fit, a GPU hang during a special attack (2026-11-25, Odin 3, Turnip). A size guard alone let a whole mission play, with black squares flashing around torches during hits (the previous frame's records). The fix converts such records on the GPU ("Indirect quads converted on the GPU" in docs/reference/rendering.md, `DM_VK_QUAD_IND`): no hang and no black squares since. Eden's [GPU device loss during special attacks](https://github.com/eden-emulator/Issue-Reports/issues/510) looks like the same pattern.
- **Particle data a few frames old.** With the conversion in, the torches still flickered off (while attacking and while the camera panned), leaving a dark spot, and lights flickered while panning (2026-11-25, Odin 3, Turnip). The log named five 16384x65 buffer textures (format `0xb`, with a 256x1 `0x2e` view at the same start, ~4 MB each) that compute writes through storage buffers: `a GPU write into its storage (store …) is done, re-uploaded`, 65,536 re-uploads in 13 minutes. The draws read them as images, and the row image of a buffer texture takes the CPU's bytes at recording unless a storage *texel* buffer's stores are pending, so with five buffers in turn they showed the particles of five frames before while the counts (read on the GPU) were this frame's. The fix ("Storage-buffer stores and buffer textures" in docs/reference/rendering.md, `DM_VK_TBUF_GW_SB=1`) is off by default for other games; this profile turns it on with an `option` row (**Fresh particle data**) and a `recommend` row for every phone. With it the torches and lights are steady, about 59 fps in battle.
- **Dark captains are the game's look**, not a bug: the captain Myrmidons in chapter 2 have a black body with white and steel armour on the Switch too (console footage, 2026-11-25); `DM_VK_TEX_TRACK=0` and `DM_VK_POOL_FB=0` changed nothing.
- **Distant mountains** appear and disappear with the camera's distance: the game's own draw distance as far as seen.
- **Qualcomm's driver: Turnip recommended** (2026-11-25, Odin 3, driver version `0x80320048`). The compiler took 5-17 s for a graphics pipeline, so the menus missed draws for a while (`5 % of draws skipped … pipelines not made 17777`), and 16-52 s for `main`'s GLSLC compute shaders (`0363622862290bff`, `bd764467d27cda5c`, `5b9f2890c1bf019a`, `164b9d837b592136`), three of which failed (`compute pipeline …: -13; its dispatches are skipped`). Its allocations filled the process's memory maps (66,084 of 65,530, 63,271 of them outside the guest block, mostly anonymous 64 KiB and `scudo:secondary`), and the run ended in `std::bad_alloc` / `FATAL pthread_create` during a special attack. `game.tsv` recommends Turnip on driver ID 8.

## Open

- The AYN Thor (Adreno 740); a newer Qualcomm driver; chapters past 2.
- The memory layout is the provisional profile's guess (see Memory).
