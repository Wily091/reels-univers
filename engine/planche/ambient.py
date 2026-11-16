#!/usr/bin/env python3
"""Musique d'ambiance originale « cloud / univers / apesanteur » (aucun kick, aucun clap, aucune percussion).
Générée entièrement par ce script : 100 % libre de droits (création originale).

Usage : python3 ambient.py <durée_s> <sortie.wav> [style]
  style = numéro 0..N-1 (ou texte quelconque, ex. le slug de l'épisode : le style est alors choisi par hachage).
"""
import sys, wave, zlib
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SR = 44100
# Chaque style : tonalité de base (Hz), progression d'accords (demi-tons depuis la base), durée par accord, couleur.
STYLES = [
    dict(name="nuage",      root=130.81, chords=[[0,4,7,11,14],[9,12,16,19,23],[5,9,12,16,19],[7,11,14,17,21]], bar=7.0, bright=2200, shimmer=1.6),
    dict(name="apesanteur", root=110.00, chords=[[0,3,7,10,14],[5,8,12,15,19],[-2,2,5,9,12],[3,7,10,14,17]],   bar=8.0, bright=1800, shimmer=2.2),
    dict(name="orbite",     root=146.83, chords=[[0,4,7,11,16],[5,9,12,16,21],[2,5,9,12,16],[7,11,14,18,21]],  bar=6.5, bright=2600, shimmer=1.3),
    dict(name="nébuleuse",  root=123.47, chords=[[0,7,11,14,19],[-3,4,7,11,16],[5,9,12,16,19],[-5,2,7,11,14]], bar=7.5, bright=2000, shimmer=1.9),
    dict(name="aurore",     root=98.00,  chords=[[0,4,7,14,19],[7,11,14,18,23],[9,12,16,19,24],[5,9,12,16,21]],  bar=8.5, bright=1600, shimmer=2.6),
]

def lowpass(x, fc, order=2):
    return sosfilt(butter(order, fc / (SR / 2), output="sos"), x, axis=0)

def build(D, style):
    s = STYLES[style]
    rng = np.random.default_rng(1234 + style)
    n = int(SR * D); t = np.arange(n) / SR
    out = np.zeros((n, 2))
    # --- nappe : accords qui se fondent les uns dans les autres (fondus de 3 s)
    bar, fade = s["bar"], 3.0
    k = 0; start = -fade / 2
    while start < D:
        ch = s["chords"][k % len(s["chords"])]
        a, b = max(0, start), min(D, start + bar + fade)
        i0, i1 = int(a * SR), int(b * SR); tt = t[i0:i1] - start
        env = np.clip(tt / fade, 0, 1) * np.clip((bar + fade - tt) / fade, 0, 1)
        env = np.sin(env * np.pi / 2) ** 2
        seg = np.zeros((i1 - i0, 2))
        for j, semi in enumerate(ch):
            f = s["root"] * 2 ** (semi / 12)
            for side, det in ((0, -0.0025), (1, 0.0025)):
                ff = f * (1 + det + 0.0012 * np.sin(2 * np.pi * (0.13 + 0.05 * j) * tt))
                ph = 2 * np.pi * np.cumsum(ff) / SR + rng.uniform(0, 6.28)
                tone = sum(np.sin(h * ph) / h ** 1.6 for h in range(1, 7))
                seg[:, side] += tone * (0.9 if j == 0 else 0.55)
        out[i0:i1] += seg * env[:, None]
        start += bar; k += 1
    out = lowpass(out, s["bright"]) * 0.18
    # --- basse très douce (fondamentale de l'accord, sinus pur)
    k = 0; start = -fade / 2
    while start < D:
        f = s["root"] / 2 * 2 ** (s["chords"][k % len(s["chords"])][0] / 12)
        a, b = max(0, start), min(D, start + bar + fade); i0, i1 = int(a * SR), int(b * SR); tt = t[i0:i1] - start
        env = np.sin(np.clip(tt / fade, 0, 1) * np.clip((bar + fade - tt) / fade, 0, 1) * np.pi / 2) ** 2
        out[i0:i1] += (np.sin(2 * np.pi * f * tt) * env * 0.12)[:, None]
        start += bar; k += 1
    # --- scintillements : notes cristallines aléatoires de l'accord en cours (2 octaves au-dessus)
    tnote = 1.0
    while tnote < D - 1:
        k = int((tnote + fade / 2) // bar); ch = s["chords"][k % len(s["chords"])]
        f = s["root"] * 4 * 2 ** (rng.choice(ch) / 12)
        L = int(min(4.0, D - tnote) * SR); tt = np.arange(L) / SR
        bell = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt)) * np.clip(tt / 0.04, 0, 1) * np.exp(-tt * 1.1)
        pan = rng.uniform(0.2, 0.8); i0 = int(tnote * SR)
        out[i0:i0 + L, 0] += bell * (1 - pan) * 0.05; out[i0:i0 + L, 1] += bell * pan * 0.05
        tnote += s["shimmer"] * rng.uniform(0.6, 1.4)
    # --- souffle d'air (bruit filtré, lent)
    air = lowpass(rng.standard_normal((n, 2)), 900) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.04 * t + 1))[:, None]
    out += air * 0.03
    # --- grande réverbération (espace)
    L = int(4.5 * SR); tt = np.arange(L) / SR
    ir = rng.standard_normal((L, 2)) * np.exp(-tt * 1.4)[:, None]; ir = lowpass(ir, 5000); ir /= np.abs(ir).sum(0) ** 0.5 * 30
    wet = np.stack([fftconvolve(out[:, c], ir[:, c])[:n] for c in range(2)], 1)
    out = out * 0.55 + wet * 0.9
    # --- fondus d'entrée/sortie et normalisation
    out *= (np.clip(t / 1.5, 0, 1) * np.clip((D - t) / 2.0, 0, 1))[:, None]
    return out / (np.abs(out).max() * 1.12)

if __name__ == "__main__":
    D = float(sys.argv[1]); dst = sys.argv[2]; st = sys.argv[3] if len(sys.argv) > 3 else "0"
    style = int(st) % len(STYLES) if st.isdigit() else zlib.crc32(st.encode()) % len(STYLES)
    x = build(D, style)
    with wave.open(dst, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
    print(f"Musique « {STYLES[style]['name']} » (style {style}) : {D:.1f} s → {dst}")
