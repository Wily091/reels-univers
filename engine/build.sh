#!/usr/bin/env bash
# Chaîne complète pour un épisode : validation → voix → timeline → rendu → musique → mixage.
# Usage : engine/build.sh episodes/AAAA-MM-JJ [--mock]
set -euo pipefail
D="$1"; MOCK="${2:-}"
B="$D/build"; mkdir -p "$B"
node engine/validate.js "$D"
python3 engine/tts.py "$D" $MOCK
node engine/build_timeline.js "$D"
node engine/render.js "$D"
python3 engine/music.py "$D"
DUR=$(python3 -c "import json;print(json.load(open('$B/timeline.json'))['duration'])")
ffmpeg -v error -y -i "$B/video.mp4" -i "$B/voice.wav" -i "$B/music.wav" -filter_complex \
  "[1:a]loudnorm=I=-15:TP=-1.5:LRA=7,apad,asplit[v1][v2];[2:a]volume=0.22[m];[m][v1]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=300[md];[v2][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t "$DUR" -movflags +faststart "$B/reel.mp4"
# image de couverture : début de la première scène « forte », sinon 1 s
python3 - "$B" <<'EOF'
import json,sys
b=sys.argv[1];tl=json.load(open(b+'/timeline.json'))
hit=[s for s in tl['scenes'] if s.get('hit')]
t=(hit[0]['lines'][-1]['t']+0.6) if hit and hit[0]['lines'] else 1.0
json.dump({'duration':tl['duration'],'coverMs':int(t*1000)},open(b+'/meta.json','w'))
EOF
ffmpeg -v error -y -ss "$(python3 -c "import json;print(json.load(open('$B/meta.json'))['coverMs']/1000)")" -i "$B/reel.mp4" -frames:v 1 -q:v 3 "$B/cover.jpg"
ls -la "$B/reel.mp4" "$B/cover.jpg"
