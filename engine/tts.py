#!/usr/bin/env python3
"""Voix off d'un épisode : UNE seule génération ElevenLabs pour tout le texte (voix fluide, sans montage),
avec l'horodatage caractère par caractère renvoyé par l'API pour caler les titres.
Ensuite accélération x1,1 (atempo, comme la lecture 1,1x de l'appli) et calcul du début/fin de chaque phrase.

Usage : python engine/tts.py episodes/AAAA-MM-JJ [--mock]
  --mock : pas d'appel API, durées estimées et audio silencieux (pour tester le montage).
Variable d'environnement requise (sauf --mock) : ELEVENLABS_API_KEY
"""
import base64, json, os, subprocess, sys, time, urllib.request, urllib.error, wave, pathlib

SR = 44100
LEAD_IN = 0.15
TAIL = 1.0

def phrases_of(ep):
    out = []
    for si, sc in enumerate(ep["scenes"]):
        for pi, item in enumerate(sc["say"]):
            text = (item if isinstance(item, str) else item["text"]).strip()
            out.append({"scene": si, "idx": pi, "text": text})
    return out

def spoken(text):
    """Texte réellement envoyé à la voix : on retire ce qui crée des silences en pleine phrase.
    « … » en milieu de phrase devient une virgule, en fin de phrase un point (même longueur, positions conservées)."""
    out = list(text)
    for i, ch in enumerate(out):
        if ch == "…":
            nxt = text[i+1:].lstrip()
            out[i] = "." if (not nxt or nxt[0].isupper()) else ","
    return "".join(out)

def full_text(ph):
    """Texte complet envoyé en une fois (tout sur une ligne, séparé par des espaces)
    + position (début, fin) de chaque phrase dans ce texte."""
    parts, pos = [], 0
    for i, p in enumerate(ph):
        if i:
            parts.append(" "); pos += 1
        t = spoken(p["text"])
        p["c0"], p["c1"] = pos, pos + len(t)
        parts.append(t); pos += len(t)
    return "".join(parts)

def tts_with_timestamps(text, voice):
    key = os.environ["ELEVENLABS_API_KEY"]
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice['id']}/with-timestamps?output_format=mp3_44100_128"
    vs = {"stability": voice.get("stability", 0.5), "similarity_boost": voice.get("similarity", 0.75),
          "style": voice.get("style", 0.0), "use_speaker_boost": True, "speed": voice.get("api_speed", 1.1)}
    body = {"text": text, "model_id": voice.get("model", "eleven_multilingual_v2"), "voice_settings": vs}
    if voice.get("language"): body["language_code"] = voice["language"]
    data = json.dumps(body).encode()
    for attempt in range(6):
        req = urllib.request.Request(url, data=data, headers={"xi-api-key": key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            msg = e.read()[:400]
            if e.code in (429, 500, 502, 503) and attempt < 5:
                wait = 20 * (attempt + 1)
                print(f"  ElevenLabs {e.code}, nouvel essai dans {wait}s : {msg}", flush=True)
                time.sleep(wait); continue
            print(f"::error title=ElevenLabs {e.code}::{msg.decode(errors='replace')}", flush=True)
            raise SystemExit(f"Erreur ElevenLabs {e.code}: {msg}")
    raise SystemExit("ElevenLabs : échec après plusieurs essais")

def read_mono(path):
    import numpy as np
    with wave.open(str(path)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return x

def write_mono(path, x):
    import numpy as np
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())

def tighten(x, text, starts, ends, keep=0.10, keep_end=0.16, min_sil=0.16):
    """Raccourcit les silences : toute pause > min_sil est ramenée à keep (keep_end après . ? !).
    Renvoie l'audio resserré et la fonction de correspondance temps d'origine -> nouveau temps."""
    import numpy as np
    hop = int(0.01 * SR); n = len(x) // hop
    rms = np.sqrt(np.maximum(np.array([np.mean(x[i*hop:(i+1)*hop]**2) for i in range(n)]), 1e-12))
    thr = np.percentile(rms, 95) * 10 ** (-32 / 20)
    quiet = rms < thr
    runs, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]: j += 1
            runs.append((i * 0.01, j * 0.01)); i = j
        else: i += 1
    ends_punct = [(e, c) for c, e in zip(text, ends) if c in ".?!"]
    cuts = []  # (début coupe, fin coupe) en temps d'origine
    total = len(x) / SR
    for a, b in runs:
        if a <= 0.001:            # silence de début : on enlève tout sauf 0
            cuts.append((0.0, b)); continue
        if b >= total - 0.011:    # silence de fin
            cuts.append((a, total)); continue
        if b - a < min_sil: continue
        k = keep_end if any(abs(e - a) < 0.25 for e, c in ends_punct) else keep
        cuts.append((a + k / 2, b - k / 2))
    # assemblage avec micro-fondus
    pieces, last, fade = [], 0.0, int(0.004 * SR)
    for a, b in cuts:
        if a > last:
            seg = x[int(last*SR):int(a*SR)].copy()
            if len(seg) > 2*fade:
                seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
            pieces.append(seg)
        last = max(last, b)
    if last < total: pieces.append(x[int(last*SR):])
    y = np.concatenate(pieces) if pieces else x
    def tmap(t):
        removed = 0.0
        for a, b in cuts:
            if t >= b: removed += b - a
            elif t > a: removed += t - a
        return max(0.0, t - removed)
    print(f"Silences resserrés : {total:.1f}s -> {len(y)/SR:.1f}s", flush=True)
    return y, tmap

def main():
    ep_dir = pathlib.Path(sys.argv[1]); mock = "--mock" in sys.argv
    ep = json.loads((ep_dir / "episode.json").read_text())
    voice = ep.get("voice") or {}
    voice.setdefault("id", "pFZP5JQG7iQjIQuC4Bku")
    tempo = float(voice.get("tempo", 1.1))      # accélération appliquée après génération
    work = ep_dir / "build"; work.mkdir(exist_ok=True)
    ph = phrases_of(ep); text = full_text(ph)
    (work / "voice_text.txt").write_text(text)

    if mock:
        # durée estimée (voix rapide, pauses courtes)
        t = 0.0; starts = []; ends = []
        for ch in text:
            starts.append(t); t += 1 / 17.0
            if ch in ".?!": t += 0.14
            elif ch in ",:": t += 0.06
            ends.append(t)
        import numpy as np
        y = np.zeros(int(t * SR), dtype=np.float32); tmap = lambda v: v; tempo_eff = 1.0
    else:
        vdir = ep_dir / "voice"; stored = vdir / "alignment.json"
        if stored.exists() and json.loads(stored.read_text()).get("text") == text and (vdir / "voice.mp3").exists():
            print("Voix stockée réutilisée (aucun crédit ElevenLabs consommé)", flush=True)
            al = json.loads(stored.read_text())
        else:
            if "--stored-only" in sys.argv:
                print("::error title=Voix manquante::aucune voix stockée pour cet épisode (ou texte modifié depuis)", flush=True)
                raise SystemExit("Voix stockée absente ou périmée")
            print(f"Génération ElevenLabs en une fois : {len(text)} caractères, voix {voice['id']}, modèle {voice.get('model', 'eleven_multilingual_v2')}", flush=True)
            res = tts_with_timestamps(text, voice)
            a = res.get("alignment") or res.get("normalized_alignment")
            if "".join(a["characters"]) != text:
                print("  attention : alignement renvoyé différent du texte envoyé, recalage par longueur", flush=True)
            vdir.mkdir(exist_ok=True)
            (vdir / "voice.mp3").write_bytes(base64.b64decode(res["audio_base64"]))
            al = {"text": text, "voice": voice, "starts": a["character_start_times_seconds"], "ends": a["character_end_times_seconds"]}
            stored.write_text(json.dumps(al, ensure_ascii=False))
        if "--voice-only" in sys.argv:
            print(f"Voix stockée : {vdir}"); return
        starts, ends = al["starts"], al["ends"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vdir / "voice.mp3"), "-ac", "1", "-ar", str(SR), str(work / "voice_raw.wav")], check=True)
        y, tmap = tighten(read_mono(work / "voice_raw.wav"), text, starts, ends)
        tempo_eff = tempo

    write_mono(work / "voice_tight.wav", y)
    af = (f"atempo={tempo_eff}," if tempo_eff != 1.0 else "") + f"adelay={int(LEAD_IN*1000)},apad=pad_dur={TAIL}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(work / "voice_tight.wav"), "-af", af, "-ac", "1", "-ar", str(SR), str(work / "voice.wav")], check=True)
    with wave.open(str(work / "voice.wav")) as w: duration = w.getnframes() / w.getframerate()

    conv = lambda v: round(LEAD_IN + tmap(v) / tempo_eff, 3)
    cs = [conv(v) for v in starts]; ce = [conv(v) for v in ends]
    n = len(cs)
    for p in ph:
        a = min(p["c0"], n - 1); b = min(max(p["c1"] - 1, a), n - 1)
        while a < b and text[a].isspace(): a += 1
        p["s"], p["e"] = cs[a], ce[b]
    (work / "phrases.json").write_text(json.dumps({"duration": round(duration, 3), "phrases": ph, "text": text, "cs": cs},
                                                  ensure_ascii=False))
    print(f"Voix : {duration:.1f}s, {len(ph)} phrases, {len(text)} caractères")

if __name__ == "__main__":
    main()
