// Convertit episode.json + build/phrases.json en build/timeline.json (temps absolus en secondes).
// Usage : node engine/build_timeline.js episodes/AAAA-MM-JJ
const fs = require('fs'), path = require('path');
const dir = process.argv[2];
const ep = JSON.parse(fs.readFileSync(path.join(dir, 'episode.json'), 'utf8'));
const ph = JSON.parse(fs.readFileSync(path.join(dir, 'build', 'phrases.json'), 'utf8'));

const byScene = ep.scenes.map(() => []);
// calage au mot près : on cherche le premier mot du titre dans la phrase prononcée
const norm = w => w.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
const TXT = ph.text || '', CS = ph.cs || [];
function tokens(c0, c1) { const out = []; const re = /[A-Za-zÀ-ÿŒœ0-9]+/g; let m; const sub = TXT.slice(c0, c1);
  while ((m = re.exec(sub))) out.push({ w: norm(m[0]), c: c0 + m.index }); return out; }
function wordTime(L, si, fb) {
  // le mot du titre le plus proche du moment prévu (fb) ; refusé s'il est trop loin
  if (!CS.length || L.count) return null;
  const words = (L.text || '').replace(/[\[\]]/g, ' ').split(/[\s'’\-]+/).map(norm).filter(w => w.length >= 2);
  if (!words.length || /^[0-9]/.test(words[0])) return null;
  const list = byScene[si]; const toks = tokens(list[0].c0, list[list.length - 1].c1);
  for (let k = 0; k < Math.min(words.length, 3); k++) {
    let best = null;
    for (const t of toks) if (t.w === words[k]) { const tt = CS[t.c] - 0.06 - k * 0.18; if (!best || Math.abs(tt - fb) < Math.abs(best - fb)) best = tt; }
    if (best !== null && Math.abs(best - fb) < 1.6) return +Math.max(list[0].s - 0.05, best).toFixed(3);
  }
  return null;
}
for (const p of ph.phrases) byScene[p.scene].push(p);

function at(spec, si, fallback) {
  // spec : index de phrase dans la scène, ou [index, fraction 0..1], ou {phrase, frac, delay}
  const list = byScene[si];
  let idx = 0, frac = 0, delay = 0;
  if (spec === undefined || spec === null) return fallback;
  if (typeof spec === 'number') idx = spec;
  else if (Array.isArray(spec)) { idx = spec[0]; frac = spec[1] || 0; delay = spec[2] || 0; }
  else { idx = spec.phrase || 0; frac = spec.frac || 0; delay = spec.delay || 0; }
  idx = Math.max(0, Math.min(list.length - 1, idx));
  const p = list[idx];
  return +(p.s + (p.e - p.s) * frac + delay).toFixed(3);
}

const scenes = ep.scenes.map((sc, si) => {
  const first = byScene[si][0];
  const s = si === 0 ? 0 : +(first.s - 0.08).toFixed(3);
  const hit = !!sc.hit;
  let prevT = -1;
  const lines = (sc.lines || []).map((L, li) => {
    const o = { ...L };
    const fb = at(L.at, si, +(first.s + li * 0.35).toFixed(3));
    const wt = wordTime(L, si, fb);
    o.t = wt !== null ? wt : fb;
    if (li && o.t < prevT + 0.12) o.t = +(prevT + 0.12).toFixed(3);
    prevT = o.t;
    delete o.at;
    if (L.strike !== undefined) o.strike = at(L.strike, si);
    return o;
  });
  let kickers = [];
  if (typeof sc.kicker === 'string') kickers = [{ t: s, text: sc.kicker }];
  else if (Array.isArray(sc.kicker)) kickers = sc.kicker.map(k => ({ t: at(k.at, si, s), text: k.text }));
  let il = sc.il ? { ...sc.il } : null;
  if (il && il.sw !== undefined) il.sw = at(il.sw, si);
  return { s, hit, y: sc.y || (hit ? 600 : 470), ghost: sc.ghost || '', kickers, il, lines };
});
for (let i = 0; i < scenes.length; i++) scenes[i].e = i + 1 < scenes.length ? scenes[i + 1].s : ph.duration;

const tl = { theme: ep.theme || 'nebuleuse', duration: ph.duration, scenes };
fs.writeFileSync(path.join(dir, 'build', 'timeline.json'), JSON.stringify(tl, null, 1));
console.log(`Timeline : ${scenes.length} scènes, ${ph.duration}s`);
