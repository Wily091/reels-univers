#!/usr/bin/env bash
# Chaîne complète d'un épisode, DA « planche de notes » (docs/STYLE_PLANCHE.md) :
# voix stockée → calage → mise en page + contrôle → musique « orbite » en boucle → mixage fixe → images → encodage → contrôle son.
# Usage : engine/build.sh <dossier_episode> [--mock | --stored-only]
#   --mock        : sans voix (calage estimé, aucun crédit) → s'arrête après le contrôle de mise en page (aperçu).
#   --stored-only : n'utilise que la voix déjà stockée dans <ep>/voice/ (jamais de crédits ElevenLabs).
set -euo pipefail
trap 'echo "::error title=Échec du rendu::étape en échec ligne $LINENO : $BASH_COMMAND"' ERR
D="${1%/}"; MODE="${2:-}"
B="$D/build"; mkdir -p "$B"
P=engine/planche
node $P/validate_ep.js "$D"
python3 engine/tts.py "$D" $MODE
node $P/make_data.js "$D"
node $P/check_layout.js "$D"
[ "$MODE" = "--mock" ] && { echo "Aperçu : $B/preview.jpg"; exit 0; }
END=$(python3 -c "import json;print(json.load(open('$B/layout.json'))['END'])")
python3 $P/music_loop.py "$END" "$B/music.wav"
bash $P/mix.sh "$B/voice.wav" "$B/music.wav" "$END" "$B/mix.wav"
N=$(python3 -c "import math;print(math.ceil($END*30))")
rm -rf "$B/frames"; mkdir -p "$B/frames"
T=$(( (N + 2) / 3 ))
node $P/render_ep.js "$D" "$B/frames" 0 $T &
node $P/render_ep.js "$D" "$B/frames" $T $((2*T)) &
node $P/render_ep.js "$D" "$B/frames" $((2*T)) $N &
wait %1 && wait %2 && wait %3
[ "$(ls "$B/frames" | wc -l)" -eq "$N" ] || { echo "::error title=Images manquantes::$(ls "$B/frames" | wc -l)/$N"; exit 1; }
bash $P/encode.sh "$B/frames" "$B/mix.wav" "$B/reel.mp4"
bash $P/check_audio.sh "$B/reel.mp4"
# couverture = dernière image (planche complète)
LAST=$(ls "$B/frames" | tail -1); cp "$B/frames/$LAST" "$B/cover.jpg"
python3 - "$B" "$N" "$END" <<'EOF'
import json,sys
b,n,end=sys.argv[1],int(sys.argv[2]),float(sys.argv[3])
json.dump({'duration':end,'coverMs':int((n-1)/30*1000)},open(b+'/meta.json','w'))
EOF
rm -rf "$B/frames"
ls -la "$B/reel.mp4" "$B/cover.jpg"
