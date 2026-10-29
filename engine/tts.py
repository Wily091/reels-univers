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
LEAD_IN = 0.30
TAIL = 1.40

def phrases_of(ep):
    out = []
    for si, sc in enumerate(ep["scenes"]):
        for pi, item in enumerate(sc["say"]):
            text = (item if isinstance(item, str) else item["text"]).strip()
            out.append({"scene": si, "idx": pi, "text": text})
    return out

def full_text(ph):
    """Texte complet envoyé en une fois + position (début, fin) de chaque phrase dans ce texte.
    Phrases d'une même scène séparées par une espace, scènes séparées par un retour à la ligne."""
    parts, pos = [], 0
    for i, p in enumerate(ph):
        if i:
            sep = "\n" if ph[i]["scene"] != ph[i-1]["scene"] else " "
            parts.append(sep); pos += len(sep)
        p["c0"], p["c1"] = pos, pos + len(p["text"])
        parts.append(p["text"]); pos += len(p["text"])
    return "".join(parts)

def tts_with_timestamps(text, voice):
    key = os.environ["ELEVENLABS_API_KEY"]
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice['id']}/with-timestamps?output_format=mp3_44100_128"
    vs = {"stability": voice.get("stability", 0.5), "similarity_boost": voice.get("similarity", 0.75),
          "style": voice.get("style", 0.0), "use_speaker_boost": True, "speed": voice.get("api_speed", 1.0)}
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
        # durée estimée : ~14,5 caractères/s à vitesse x1,1, pauses selon la ponctuation
        t = 0.0; starts = []; ends = []
        for i, ch in enumerate(text):
            starts.append(t)
            t += 1 / 14.5 * (1.1 / tempo)
            if ch in ".?!…": t += 0.35
            elif ch in ",:": t += 0.12
            elif ch == "\n": t += 0.2
            ends.append(t)
        raw_dur = t
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", f"{raw_dur:.3f}", str(work / "voice_raw.wav")], check=True)
        tempo_eff = 1.0
    else:
        # Voix déjà générée et stockée (stock d'avance) → aucun appel API
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
        tempo_eff = tempo

    # x1,1 + temps de lancement au début + silence de fin
    af = f"atempo={tempo_eff},adelay={int(LEAD_IN*1000)},apad=pad_dur={TAIL}" if tempo_eff != 1.0 else f"adelay={int(LEAD_IN*1000)},apad=pad_dur={TAIL}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(work / "voice_raw.wav"), "-af", af, "-ac", "1", "-ar", str(SR), str(work / "voice.wav")], check=True)
    with wave.open(str(work / "voice.wav")) as w: duration = w.getnframes() / w.getframerate()

    n = len(starts)
    for p in ph:
        a = min(p["c0"], n - 1); b = min(max(p["c1"] - 1, a), n - 1)
        while a < b and text[a].isspace(): a += 1
        p["s"] = round(LEAD_IN + starts[a] / tempo_eff, 3)
        p["e"] = round(LEAD_IN + ends[b] / tempo_eff, 3)
    (work / "phrases.json").write_text(json.dumps({"duration": round(duration, 3), "phrases": ph}, ensure_ascii=False, indent=1))
    print(f"Voix : {duration:.1f}s, {len(ph)} phrases, {len(text)} caractères")

if __name__ == "__main__":
    main()
