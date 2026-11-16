#!/usr/bin/env python3
"""Musique officielle unique : « orbite » (assets/music/orbite.wav, création originale, libre de droits).
Elle est répétée en boucle (fondu enchaîné de 0,5 s à chaque raccord) jusqu'à la fin du reel.
Usage : python3 music_loop.py <durée_s> <sortie.wav>"""
import sys, wave, pathlib
import numpy as np
SRC = pathlib.Path(__file__).resolve().parents[2] / "assets" / "music" / "orbite.wav"
XF = 0.5  # secondes de fondu enchaîné au raccord
with wave.open(str(SRC)) as w:
    sr, ch = w.getframerate(), w.getnchannels()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, ch).astype(np.float64) / 32768
D = float(sys.argv[1]); n = int(D * sr); xf = int(XF * sr); cyc = len(x) - xf
out = np.zeros((n + len(x), ch)); fin = np.sin(np.linspace(0, np.pi / 2, xf)) ** 2
pos = 0
while pos < n:
    seg = x.copy()
    if pos > 0: seg[:xf] *= fin[:, None]          # entrée en fondu sur la fin du tour précédent
    seg[cyc:] *= (1 - fin)[:, None]                # sortie en fondu
    out[pos:pos + len(seg)] += seg; pos += cyc
out = out[:n]; out[:int(.8 * sr)] *= np.linspace(0, 1, int(.8 * sr))[:, None]
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(ch); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print(f"Musique « orbite » en boucle : {D:.1f} s ({D / (cyc / sr):.1f} tours) → {sys.argv[2]}")
