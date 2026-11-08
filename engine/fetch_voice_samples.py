#!/usr/bin/env python3
"""Télécharge, SANS générer de voix, l'aperçu d'une voix ElevenLabs et ses dernières générations (historique).
Usage : python3 engine/fetch_voice_samples.py <voice_id> <dossier_sortie>"""
import json, os, sys, pathlib, urllib.request, urllib.error
import traceback
sys.excepthook=lambda t,e,tb: print(f"::error title=Script::{t.__name__}: {e} | "+" ".join(traceback.format_tb(tb)[-1].split()))
KEY = os.environ["ELEVENLABS_API_KEY"]; vid, out = sys.argv[1], pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
def get(url, raw=False, auth=True):
    req = urllib.request.Request(url, headers={"xi-api-key": KEY} if auth else {})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            b = r.read(); return b if raw else json.loads(b)
    except urllib.error.HTTPError as e:
        print(f"::warning title=ElevenLabs {e.code}::{url[:80]} {e.read()[:200].decode(errors='replace')}"); return None
    except Exception as e:
        print(f"::warning title=Réseau::{url[:80]} {e}"); return None
v = get(f"https://api.elevenlabs.io/v1/voices/{vid}")
info = {"name": v.get("name"), "category": v.get("category"), "labels": v.get("labels"), "settings": v.get("settings"),
        "samples": [{k: s.get(k) for k in ("file_name", "size_bytes", "mime_type")} for s in (v.get("samples") or [])]} if v else {}
if v and v.get("preview_url"):
    b = get(v["preview_url"], raw=True, auth=False)
    if b: (out / "preview.mp3").write_bytes(b)
h = get(f"https://api.elevenlabs.io/v1/history?page_size=5&voice_id={vid}") or {}
info["history"] = []
for i, it in enumerate(h.get("history", [])[:3]):
    b = get(f"https://api.elevenlabs.io/v1/history/{it['history_item_id']}/audio", raw=True)
    if b: (out / f"history_{i}.mp3").write_bytes(b)
    info["history"].append({"text": (it.get("text") or "")[:200], "source": it.get("source"), "date_unix": it.get("date_unix"), "settings": it.get("settings"), "model": it.get("model_id")})
(out / "info.json").write_text(json.dumps(info, ensure_ascii=False, indent=1))
print(json.dumps(info, ensure_ascii=False)[:1500])
