#!/usr/bin/env python3
"""Récupère une voix DÉJÀ générée dans l'historique ElevenLabs (aucune nouvelle génération de voix)
et recalcule l'horodatage des lettres par alignement forcé, pour la réutiliser dans un épisode.
Usage : python3 engine/recover_voice.py <dossier_episode> <voice_id>
Écrit <dossier>/voice/voice.mp3 + alignment.json."""
import json, os, sys, pathlib, urllib.request, urllib.error, uuid
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from tts import phrases_of, full_text

KEY = os.environ["ELEVENLABS_API_KEY"]
def get(url, raw=False):
    req = urllib.request.Request(url, headers={"xi-api-key": KEY})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            b = r.read(); return b if raw else json.loads(b)
    except urllib.error.HTTPError as e:
        print(f"::error title=ElevenLabs {e.code}::{e.read()[:300].decode(errors='replace')}"); raise SystemExit(1)

ep_dir = pathlib.Path(sys.argv[1]); vid = sys.argv[2]
ep = json.loads((ep_dir / "episode.json").read_text()); text = full_text(phrases_of(ep))
items, after = [], None
for _ in range(10):
    u = f"https://api.elevenlabs.io/v1/history?page_size=1000&voice_id={vid}" + (f"&start_after_history_item_id={after}" if after else "")
    d = get(u); items += d.get("history", [])
    if not d.get("has_more"): break
    after = d.get("last_history_item_id")
print(f"{len(items)} générations trouvées pour la voix {vid}")
for it in items[:8]: print(" -", it.get("date_unix"), len(it.get("text", "")), repr(it.get("text", "")[:70]))
match = [it for it in items if it.get("text", "").strip() == text.strip()]
if not match:
    print(f"::error title=Voix introuvable::aucune génération de cette voix avec exactement le texte de l'épisode ({len(text)} car.)"); raise SystemExit(1)
it = max(match, key=lambda i: i.get("date_unix", 0))
print("Génération retenue :", it["history_item_id"], it.get("date_unix"))
audio = get(f"https://api.elevenlabs.io/v1/history/{it['history_item_id']}/audio", raw=True)

# alignement forcé (pas de génération de voix)
b = uuid.uuid4().hex
body = (f"--{b}\r\nContent-Disposition: form-data; name=\"text\"\r\n\r\n{text}\r\n"
        f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"voice.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n").encode() + audio + f"\r\n--{b}--\r\n".encode()
req = urllib.request.Request("https://api.elevenlabs.io/v1/forced-alignment", data=body,
                             headers={"xi-api-key": KEY, "Content-Type": f"multipart/form-data; boundary={b}"})
try:
    with urllib.request.urlopen(req, timeout=300) as r: fa = json.loads(r.read())
except urllib.error.HTTPError as e:
    print(f"::error title=Alignement {e.code}::{e.read()[:300].decode(errors='replace')}"); raise SystemExit(1)
chars = fa["characters"]
print(f"Alignement : {len(chars)} caractères (texte : {len(text)})")
starts, ends = [], []
k = 0
for ch in text:   # recalage caractère par caractère
    j = k
    while j < len(chars) and chars[j]["text"] != ch and j < k + 3: j += 1
    if j < len(chars) and chars[j]["text"] == ch: k = j
    c = chars[min(k, len(chars) - 1)]
    starts.append(c["start"]); ends.append(c["end"]); k += 1
vdir = ep_dir / "voice"; vdir.mkdir(exist_ok=True)
(vdir / "voice.mp3").write_bytes(audio)
(vdir / "alignment.json").write_text(json.dumps({"text": text, "voice": {**ep.get("voice", {}), "id": vid},
    "starts": starts, "ends": ends, "source": "historique ElevenLabs + alignement forcé"}, ensure_ascii=False))
print("Voix récupérée :", vdir)
