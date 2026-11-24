#!/bin/sh
# FORK: writes a release's notes to stdout.
# Usage: release-notes.sh [<previous release tag>]   (run in the repository; upstream/main fetched beforehand)
#   1. the "Status" section of fork/CHANGELOG.md (the Fire Emblem Warriors progress, kept by hand)
#   2. this fork's own commits since the previous release (not upstream's, not merges)
#   3. upstream's commits that came in with the syncs since the previous release
set -u
prev="${1:-}"
range="${prev:+$prev..}HEAD"
up=""
git rev-parse --verify -q upstream/main >/dev/null && up="upstream/main"

awk '/^## /{n++} n==1' fork/CHANGELOG.md
echo

echo "## Fork changes since ${prev:-the start}"
echo
if [ -n "$up" ]; then
  own=$(git log --no-merges --format='- %s (`%h`)' "$range" --not "$up")
else
  own=$(git log --no-merges --format='- %s (`%h`)' "$range")
fi
[ -n "$own" ] && echo "$own" || echo "- none"
echo

if [ -n "$up" ]; then
  base_now=$(git merge-base HEAD "$up")
  if [ -z "$prev" ]; then
    echo "## Upstream base"
    echo
    echo "- igawa6/peanuts-native at \`$(git rev-parse --short "$base_now")\`: $(git log -1 --format='%s' "$base_now")"
    echo
    echo "---"
    echo "Installs as **Peanuts FEW** beside the official Peanuts Native (its own data, keys and saves). Each release installs over the previous one."
    exit 0
  fi
  upr="$(git merge-base "$prev" "$up")..$base_now"
  count=$(git rev-list --no-merges --count "$upr" 2>/dev/null || echo 0)
  echo "## From upstream (igawa6/peanuts-native): $count commits"
  echo
  if [ "$count" -gt 0 ]; then
    git log --no-merges --format='- %s (`%h`)' "$upr" | head -40
    [ "$count" -gt 40 ] && echo "- … and $((count - 40)) more"
  else
    echo "- no new upstream commits"
  fi
  echo
fi

echo "---"
echo "Installs as **Peanuts FEW** beside the official Peanuts Native (its own data, keys and saves). Each release installs over the previous one."
