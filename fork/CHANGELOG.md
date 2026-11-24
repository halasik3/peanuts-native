# Peanuts FEW: changelog

The first section below goes at the top of every release's notes. Keep it current: it is the one place that says how far
Fire Emblem Warriors has got. Older entries move under "History".

## Status: Fire Emblem Warriors (Switch, update 1.5.0)

- **Not playable yet: no profile.** The app builds from this fork, but Fire Emblem Warriors isn't in it yet.
- Next: survey the 1.5.0 dump and write a provisional profile, based on Hyrule Warriors: Definitive Edition
  (`dm/games/0100AE00096EA000`): same Koei Tecmo KTGL engine on NVN, same team, similar SDK.
- Device: AYN Thor (Adreno 740). Test on both Turnip and the system driver.

## History

### Fork set up

- Fork of igawa6/peanuts-native, synced with upstream every 6 hours (`.github/workflows/fork-sync.yml`).
- Each sync or push to main builds **Peanuts FEW** (`dev.nxnative.android.peanutsfew`), which installs beside the official app,
  and publishes it as a release (`.github/workflows/fork-release.yml`).
