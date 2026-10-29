#!/usr/bin/env python3
"""Nappe musicale originale (drone + pulsation + souffles aux coupes + impacts sur les scènes fortes).
Usage : python engine/music.py episodes/AAAA-MM-JJ"""
import json, sys, wave, pathlib
import numpy as np

d = pathlib.Path(sys.argv[1]) / "build"
tl = json.loads((d / "timeline.json").read_text())
SR = 44100; D = tl["duration"] + 0.2; n = int(SR * D); t = np.arange(n) / SR
rng = np.random.default_rng(len(tl["scenes"]) * 7 + int(D))

def lp(x, a):
    from scipy.signal import lfilter
    return lfilter([a], [1, a - 1], x)

env = np.clip(t / 3, 0, 1) * np.clip((D - t) / 1.5, 0, 1)
drone = (np.sin(2*np.pi*36.7*t)*0.5 + np.sin(2*np.pi*73.4*t)*0.35 + np.sin(2*np.pi*110*t + 0.3*np.sin(2*np.pi*0.1*t))*0.18
         + np.sin(2*np.pi*146.8*t*1.002)*0.08) * (0.75 + 0.25*np.sin(2*np.pi*0.07*t))
air = lp(rng.standard_normal(n), 0.02) * 0.25 * (0.6 + 0.4*np.sin(2*np.pi*0.05*t + 1))
mix = (drone + air) * env * 0.5

def add(at, sig):
    i = int(at * SR)
    if i >= n: return
    j = min(n, i + len(sig));
    if i < 0: sig = sig[-i:]; i = 0
    mix[i:j] += sig[:j - i]

beat = 60 / 90
for k in np.arange(2.0, D - 1.5, beat):
    L = int(0.35*SR); tt = np.arange(L)/SR; f = 45 + 60*np.exp(-tt*30)
    add(k, np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-tt*9) * 0.55)
noise = rng.standard_normal(int(0.5*SR)); tt = np.arange(len(noise))/SR
wh = lp(noise, 0.15) * np.clip(tt/0.4, 0, 1)**2 * np.exp(-np.clip(tt-0.4, 0, None)*25) * 0.35
hits = []
for sc in tl["scenes"][1:]:
    add(sc["s"] - 0.4, wh)
for sc in tl["scenes"]:
    if sc.get("hit"): hits.append((sc["s"], 1.0))
    for L in sc["lines"]:
        if L.get("punch") and sc.get("hit"): hits.append((L["t"], 0.8))
for h, amp in hits:
    L = int(1.6*SR); tt = np.arange(L)/SR; f = 40 + 90*np.exp(-tt*18)
    boom = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*2.5)*0.9 + lp(rng.standard_normal(L), 0.15)*np.exp(-tt*12)*0.5
    add(h, boom*amp)
mix /= np.max(np.abs(mix)) * 1.05
with wave.open(str(d / "music.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print(f"Musique : {D:.1f}s, {len(hits)} impacts")
