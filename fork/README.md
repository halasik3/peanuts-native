# Peanuts FEW (halasik3's fork of Peanuts Native)

This fork tracks [igawa6/peanuts-native](https://github.com/igawa6/peanuts-native) and adds **Fire Emblem Warriors** (Switch, update 1.5.0).
For its status, see [CHANGELOG.md](CHANGELOG.md).

## Installing

- Download the APK from [Releases](https://github.com/halasik3/peanuts-native/releases/latest). It installs as **Peanuts FEW** *beside* the official Peanuts Native, with its own
  keys, firmware, saves and packs. The official app is left alone.
- The official app's signing key is private, so no fork can install over it. This one is signed with its own key (`fork/debug.keystore`),
  so every Peanuts FEW release installs over the previous one.
- Automatic updates: add this repository to **Obtainium** (GitHub source). The in-app update check only covers the official package.
- Settings › Library › Build folder can point both apps at the same folder, so a game built in one app doesn't have to be built again in the other.

## How the fork stays current

| Workflow | When | What |
|---|---|---|
| `fork-sync.yml` | every 6 hours, or by hand | merges upstream `main`, then starts a release build. A conflict or refused push opens an issue labelled `sync` |
| `fork-release.yml` | after a sync, on every push to `main`, or by hand | builds the APK (`peanuts-few-<version>-few.<n>-<commit>.apk`) and publishes a release with notes: the status above, this fork's commits, and upstream's commits |

Fork-only files live in `fork/` and `.github/workflows/fork-*.yml`, so upstream merges don't conflict with them. Game work follows upstream's
own rules (`peanuts/docs/NEW-GAME.md`, `PEANUTS` markers), so it can go upstream later.

An optional `SYNC_TOKEN` secret (a fine-grained token with Contents and Workflows write on this repository) lets the sync push upstream changes to
`.github/workflows`. Without it, use **Sync fork** on the repository page when the bot opens an issue about it.
