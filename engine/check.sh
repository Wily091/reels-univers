#!/usr/bin/env bash
# Contrôle gratuit d'épisodes du stock : finalise, valide, simule la voix et produit un aperçu.
# Usage : engine/check.sh backlog/NNN-a backlog/NNN-b ...
set -e
for d in "$@"; do
  python3 engine/finalize.py "$d"
  node engine/validate.js "$d"
  python3 engine/tts.py "$d" --mock >/dev/null
  node engine/build_timeline.js "$d" >/dev/null
  node engine/preview.js "$d" >/dev/null
done
