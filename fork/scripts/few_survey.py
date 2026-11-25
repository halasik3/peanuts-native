#!/usr/bin/env python3
# FORK: the first steps of a new game's profile (peanuts/docs/NEW-GAME.md, steps 1-3) in one run, for Windows without a build toolchain.
#   few_survey.py <folder>   the folder holds the game's .nsp/.nsz/.xci/.xcz files (base + update) and prod.keys
# Writes <folder>\FEW-results.zip: the survey, the provisional profile with its shader tables, and the logs. None of it is game data
# (upstream commits these same tables to dm/games). The .nup is kept beside the game files; the extracted dump is deleted at the end.
# Run through FEW-Survey.bat, which starts it with the packer's Python (scripts\bananative.bat python).
import os, shutil, subprocess, sys, time, types, zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'peanuts' / 'scripts'))
import peanuts_build as pb   # noqa: E402  the builder's importer helpers: find_importer, probe, choose, nup_path, import_nup

GAME_EXTS = ('.nsp', '.nsz', '.xci', '.xcz')
LOG = None


def say(msg):
    line = f'[{time.strftime("%H:%M:%S")}] {msg}'
    print(line, flush=True)
    if LOG: LOG.write(line + '\n'); LOG.flush()


def step(name, cmd, env=None, ok_codes=(0,)):
    """Runs a tool, its output into logs/<name>.log and the console's last lines on failure"""
    say(f'{name}: {" ".join(map(str, cmd))[:300]}')
    log = LOGS / f'{name}.log'
    t = time.monotonic()
    with open(log, 'w', encoding='utf-8', errors='replace') as f:
        rc = subprocess.run([str(c) for c in cmd], stdout=f, stderr=subprocess.STDOUT, env={**os.environ, **(env or {})}, cwd=REPO).returncode
    tail = log.read_text(encoding='utf-8', errors='replace').strip().splitlines()[-6:]
    say(f'{name}: exit code {rc}, {time.monotonic() - t:.0f} s')
    if rc not in ok_codes:
        for l in tail: say(f'  | {l}')
    return rc


def results_zip(folder, app, work, dump):
    out = folder / 'FEW-results.zip'
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(LOGS.glob('*.log')): z.write(p, f'logs/{p.name}')
        if app:
            prof = work / 'profile' / app
            for p in sorted(prof.glob('*')) if prof.is_dir() else []:
                if p.is_file() and p.suffix in ('.tsv', '.md', '.txt'): z.write(p, f'profile/{app}/{p.name}')
            surv = dump / f'{app}_survey'
            for p in sorted(surv.rglob('*')) if surv.is_dir() else []:
                if p.is_file() and p.suffix in ('.md', '.tsv', '.txt', '.json') and p.stat().st_size < 20 << 20:
                    z.write(p, f'survey/{p.relative_to(surv)}')
            for p in sorted((work / 'logs').glob('*')) if (work / 'logs').is_dir() else []:
                if p.is_file() and p.stat().st_size < 20 << 20: z.write(p, f'build-logs/{p.name}')
    return out


def main():
    global LOG, LOGS
    if len(sys.argv) < 2: sys.exit('usage: few_survey.py <folder with the game files and prod.keys>')
    folder = Path(sys.argv[1]).expanduser().resolve()
    LOGS = folder / 'FEW-logs'
    LOGS.mkdir(parents=True, exist_ok=True)
    LOG = open(LOGS / 'few-survey.log', 'w', encoding='utf-8')
    say(f'folder {folder}, repository {REPO}, Python {sys.version.split()[0]}')

    keys = folder / 'prod.keys'
    if not keys.is_file(): sys.exit(f'[RED] no prod.keys in {folder}: copy yours there (the one Eden or Peanuts uses)')
    files = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in GAME_EXTS)
    if not files: sys.exit(f'[RED] no .nsp, .nsz, .xci or .xcz files in {folder}')
    for f in files: say(f'game file: {f.name} ({f.stat().st_size / 1073741824:.1f} GB)')

    free = shutil.disk_usage(folder).free
    need = sum(f.stat().st_size for f in files) * 2.2
    say(f'free space {free / 1073741824:.0f} GB, about {need / 1073741824:.0f} GB needed while it runs')
    if free < need: say('[RED] the drive may be too small: free some space or move the folder to a bigger drive')

    # 1. the .nup (the builder's own importer steps)
    args = types.SimpleNamespace(importer=None, keys=str(keys), update=None, nup=str(folder))
    importer = pb.find_importer(args)
    say(f'importer {importer}')
    titles = pb.probe(importer, keys, files)
    plan = pb.choose(titles, args)
    app = plan.app
    say(f'game {app} "{plan.name}", update v{plan.version or 0}')
    if (REPO / 'dm' / 'games' / app / 'game.tsv').is_file():
        say(f'note: {app} already has a profile in dm/games (this run surveys it again)')
    nup = pb.nup_path(args, plan, files[0])
    pb.import_nup(importer, keys, nup, plan, False, False)

    # 2. the dump folder the survey and the split read (deleted at the end)
    dump = folder / f'{app}-dump'
    work = folder / f'{app}-work'
    if not (dump / 'base').is_dir():
        if dump.exists(): shutil.rmtree(dump)
        rc = step('extract', [sys.executable, REPO / 'peanuts/scripts/nup-extract.py', nup, dump])
        if rc: return finish(folder, app, work, dump, False)
    else:
        say(f'reusing the extracted files in {dump}')

    # 3. the survey, then the provisional profile (it stops at the first iPhone-only step after writing it; that stop is expected).
    # Both are kept in the work folder: a second run goes straight to the split
    prof = work / 'profile' / app
    if (prof / 'game.tsv').is_file() and (dump / f'{app}_survey' / 'survey.md').is_file():
        say(f'reusing the survey and the provisional profile in {prof}')
    else:
        step('survey', [sys.executable, REPO / 'scripts/build_ipa_from_nsp.py', dump, '--survey-only', '--work-dir', work, '--progress', 'lines'])
        step('profile', [sys.executable, REPO / 'scripts/build_ipa_from_nsp.py', dump, '--work-dir', work, '--no-heap-check', '--progress', 'lines'],
             ok_codes=(0, 1))
    if not (prof / 'game.tsv').is_file():
        say('[RED] no provisional profile was written (see logs/profile.log)')
        return finish(folder, app, work, dump, False)

    # 4. the shader split into the profile's tables (NEW-GAME.md step 3): one romfs and one main per version in the profile's shader_versions
    # (an update's folder holds the whole RomFS and the code; the base game's has no main once an update replaces it)
    want = []
    for line in (prof / 'game.tsv').read_text(encoding='utf-8', errors='replace').splitlines():
        f = line.split('\t')
        if f[0] == 'shader_versions': want = [v for x in f[1:] for v in x.split()]
    vers = [dump / 'base' if v in ('v0', '0') else dump / 'updates' / v.lstrip('v') for v in want] or [dump / 'base']
    for v in vers: say(f'split reads {v}')
    romfs = ','.join(str(v / 'romfs') for v in vers)
    mains = ','.join(str(v / 'exefs' / 'main') for v in vers)
    pkg = work / 'split' / 'pkg'
    rc = step('split', [sys.executable, REPO / 'dm/gfx/tools/shader_split.py', romfs, mains, pkg,
                        prof / 'shader_map.tsv', prof / 'shader_facts.tsv', prof / 'shader_pairs.tsv', prof / 'pso_pairs.tsv'],
              env={'DM_GAMES_DIR': str(work / 'profile'), 'DM_GAME': app})
    last = (LOGS / 'split.log').read_text(encoding='utf-8', errors='replace').strip().splitlines()[-1:] or ['']
    say(f'split: {last[0][:200]}')
    return finish(folder, app, work, dump, rc == 0)


def finish(folder, app, work, dump, ok):
    out = results_zip(folder, app, work, dump)
    if ok and dump.exists():
        say(f'deleting the extracted files {dump}')
        shutil.rmtree(dump, ignore_errors=True)
    if not ok and dump.exists(): say(f'the extracted files stay in {dump}, so the next run starts from them')
    say(('DONE' if ok else 'STOPPED WITH AN ERROR') + f': send {out} ({out.stat().st_size / 1048576:.1f} MB)')
    LOG.close()
    with zipfile.ZipFile(out, 'a') as z: z.write(LOGS / 'few-survey.log', 'logs/few-survey.log')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
