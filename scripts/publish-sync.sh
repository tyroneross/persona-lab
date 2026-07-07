#!/usr/bin/env bash
# Sync this dev copy of persona-lab to the standalone published repo and push.
#
# The dev source of truth is this plugin dir (inside the AI User Personas repo).
# The marketplace publishes from the standalone repo (github.com/tyroneross/persona-lab).
# This keeps the two in sync so the marketplace never lags the dev copy.
#
# Usage: scripts/publish-sync.sh ["commit message"]
#   PERSONA_LAB_STANDALONE overrides the standalone repo path.
set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STANDALONE="${PERSONA_LAB_STANDALONE:-$HOME/dev/git-folder/persona-lab}"
MSG="${1:-sync persona-lab from dev copy}"

if [ ! -d "$STANDALONE/.git" ]; then
  echo "persona-lab: standalone repo not found at $STANDALONE" >&2
  echo "Set PERSONA_LAB_STANDALONE or clone github.com/tyroneross/persona-lab there first." >&2
  exit 1
fi

# Mirror the plugin into the standalone repo. Never touch its .git or .gitignore.
rsync -a --delete \
  --exclude '.git/' \
  --exclude '.gitignore' \
  --exclude 'node_modules/' \
  --exclude '.DS_Store' \
  "$PLUGIN_DIR"/ "$STANDALONE"/

cd "$STANDALONE"
git add -A
if [ -z "$(git status --porcelain)" ]; then
  echo "persona-lab: standalone already in sync. Nothing to push."
  exit 0
fi

git commit -q -m "$MSG"
git push
echo "persona-lab: synced and pushed -> $(git remote get-url origin)"
