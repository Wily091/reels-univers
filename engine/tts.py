#!/usr/bin/env python3
"""Voix off d'un épisode : génère chaque phrase avec ElevenLabs, coupe les silences,
assemble avec des pauses calibrées, et écrit voice.wav + phrases.json (début/fin de chaque phrase).

Usage : python engine/tts.py episodes/AAAA-MM-JJ [--mock]
  --mock : pas d'appel API, durées estimées et audio silencieux (pour tester le montage).
Variable d'environnement requise (sauf --mock) : ELEVENLABS_API_KEY
"""
import json, os, subprocess, sys, time, urllib.request, urllib.error, wave, struct, pathlib

SR = 44100
LEAD_IN = 0.30
TAIL = 1.40

def phrases_of(ep):
    out = []
    for si, sc in enumerate(ep["scenes"]):
        n = len(sc["say"])
        for pi, item in enumerate(sc["say"]):
            text = item if isinstance(item, str) else item["text"]
            pause = None if isinstance(item, str) else item.get("pause")
            out.append({"scene": si, "idx": pi, "text": text, "pause": pause, "last": pi == n - 1})
    return out

def default_pause(p):
    t = p["text"].rstrip()
    if t.endswith("…") or t.endswith("..."): g = 0.45
    elif t.endswith(","): g = 0.14
    elif t[-1:] in "?!": g = 0.32
    elif t.endswith(".") : g = 0.28
    elif t.endswith(":"): g = 0.22
    else: g = 0.18
    if p["last"]: g += 0.08
    return g

def tts_call(text, prev_text, next_text, voice):
    key = os.environ["ELEVENLABS_API_KEY"]
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice['id']}?output_format=mp3_44100_128"
    body = {
        "text": text,
        "model_id": voice.get("model", "eleven_multilingual_v2"),
        "voice_settings": {"stability": voice.get("stability", 0.40), "similarity_boost": voice.get("similarity", 0.75),
                           "style": voice.get("style", 0.35), "use_speaker_boost": True, "speed": voice.get("speed", 1.08)},
    }
    if prev_text: body["previous_text"] = prev_text
    if next_text: body["next_text"] = next_text
    data = json.dumps(body).encode()
    for attempt in range(6):
        req = urllib.request.Request(url, data=data, headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            msg = e.read()[:300]
            if e.code in (429, 500, 502, 503) and attempt < 5:
                wait = 15 * (attempt + 1)
                print(f"  ElevenLabs {e.code}, nouvel essai dans {wait}s : {msg}", flush=True)
                time.sleep(wait); continue
            raise SystemExit(f"Erreur ElevenLabs {e.code}: {msg}")
    raise SystemExit("ElevenLabs : échec après plusieurs essais")

def to_trimmed_wav(mp3_path, wav_path):
    af = ("silenceremove=start_periods=1:start_threshold=-48dB:start_silence=0.02,areverse,"
          "silenceremove=start_periods=1:start_threshold=-48dB:start_silence=0.04,areverse")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3_path, "-af", af, "-ac", "1", "-ar", str(SR), wav_path], check=True)

def read_wav(path):
    with wave.open(path) as w:
        return w.readframes(w.getnframes()), w.getnframes() / w.getframerate()

def main():
    ep_dir = pathlib.Path(sys.argv[1]); mock = "--mock" in sys.argv
    ep = json.loads((ep_dir / "episode.json").read_text())
    voice = ep.get("voice") or {"id": "pFZP5JQG7iQjIQuC4Bku"}
    work = ep_dir / "build"; work.mkdir(exist_ok=True)
    ph = phrases_of(ep)
    pcm = bytearray(); cursor = 0.0
    def silence(sec):
        nonlocal cursor
        n = int(round(sec * SR)); pcm.extend(b"\x00\x00" * n); cursor += n / SR
    silence(LEAD_IN)
    for i, p in enumerate(ph):
        if mock:
            dur = max(0.6, len(p["text"]) / 14.5)
            frames = b"\x00\x00" * int(dur * SR)
        else:
            print(f"[{i+1}/{len(ph)}] {p['text']}", flush=True)
            prev_t = " ".join(q["text"] for q in ph[max(0, i-2):i]) or None
            next_t = " ".join(q["text"] for q in ph[i+1:i+3]) or None
            mp3 = work / f"p{i:02d}.mp3"; wav = work / f"p{i:02d}.wav"
            mp3.write_bytes(tts_call(p["text"], prev_t, next_t, voice))
            to_trimmed_wav(str(mp3), str(wav))
            frames, dur = read_wav(str(wav))
        p["s"] = round(cursor, 3); pcm.extend(frames); cursor += len(frames) / 2 / SR; p["e"] = round(cursor, 3)
        silence(p["pause"] if p["pause"] is not None else default_pause(p))
    silence(TAIL)
    with wave.open(str(work / "voice.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(bytes(pcm))
    (work / "phrases.json").write_text(json.dumps({"duration": round(cursor, 3), "phrases": ph}, ensure_ascii=False, indent=1))
    print(f"Voix : {cursor:.1f}s, {len(ph)} phrases, {sum(len(p['text']) for p in ph)} caractères")

if __name__ == "__main__":
    main()
