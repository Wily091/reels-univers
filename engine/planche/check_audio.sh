#!/bin/bash
# Contrôle des niveaux sonores d'un reel (à lancer sur CHAQUE vidéo avant publication).
# Cible fixe : -16 LUFS intégré (tolérance ±1), crête vraie ≤ -1,0 dBTP. Sinon : ne pas publier, refaire le mixage avec mix.sh.
F=$1
J=$(ffmpeg -nostats -i "$F" -af loudnorm=print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
I=$(echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['input_i'])")
TP=$(echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['input_tp'])")
LRA=$(echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['input_lra'])")
echo "Volume : $I LUFS | crête : $TP dBTP | dynamique : $LRA LU"
python3 -c "import sys;i,tp=float('$I'),float('$TP');ok=-17<=i<=-15 and tp<=-1.0;print('OK' if ok else 'HORS NORME');sys.exit(0 if ok else 1)"
