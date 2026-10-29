#!/usr/bin/env python3
"""Complète un épisode du stock : voix/thème depuis config.json, conclusion douce standard en dernière scène.
Usage : python3 engine/finalize.py backlog/NNN-slug"""
import json, sys, pathlib
d = pathlib.Path(sys.argv[1]); f = d / "episode.json"
ep = json.loads(f.read_text()); cfg = json.loads(pathlib.Path("config.json").read_text())
ep.setdefault("date", None)
ep["theme"] = cfg["theme"]
ep["voice"] = {"id": cfg["voice_id"], "model": "eleven_multilingual_v2", "tempo": 1.1}
OUTRO = {
    "say": ["Si ça t'a plu, tu peux t'abonner pour d'autres histoires sur l'univers.",
            "Et si tu connais quelqu'un que ça pourrait faire rêver… partage-lui."],
    "ghost": "UNIVERS", "il": {"type": "horizon"},
    "lines": [{"text": "SI ÇA T'A PLU…", "at": 0}, {"text": "D'AUTRES HISTOIRES", "at": [0, 0.5]},
              {"text": "[SUR L'UNIVERS.]", "at": [0, 0.75]}, {"text": "[PARTAGE-LA.]", "at": [1, 0.6], "gap": 30, "max": 140}]}
if not ep["scenes"] or ep["scenes"][-1].get("ghost") != "UNIVERS":
    ep["scenes"].append(OUTRO)
order = ["date", "title", "theme", "voice", "caption", "hashtags", "sources", "scenes"]
ep = {k: ep[k] for k in order if k in ep} | {k: v for k, v in ep.items() if k not in order}
def dump(ep):
    out = ["{"]; keys = list(ep)
    for i, k in enumerate(keys):
        comma = "," if i < len(keys) - 1 else ""
        if k == "scenes":
            out.append(' "scenes": [')
            out += ["  " + json.dumps(sc, ensure_ascii=False) + ("," if j < len(ep[k]) - 1 else "") for j, sc in enumerate(ep[k])]
            out.append(" ]" + comma)
        else:
            out.append(f' {json.dumps(k)}: {json.dumps(ep[k], ensure_ascii=False)}{comma}')
    return "\n".join(out + ["}"]) + "\n"
f.write_text(dump(ep))
