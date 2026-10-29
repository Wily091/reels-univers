// Vérifie un episode.json AVANT de dépenser des crédits ElevenLabs.
// Usage : node engine/validate.js episodes/AAAA-MM-JJ
const fs = require('fs'), path = require('path');
const dir = process.argv[2];
const errs = [], warns = [];
let ep;
try { ep = JSON.parse(fs.readFileSync(path.join(dir, 'episode.json'), 'utf8')); }
catch (e) { console.error('JSON invalide : ' + e.message); process.exit(1); }
const html = fs.readFileSync(path.join(__dirname, 'engine.html'), 'utf8');
const ilBlock = html.slice(html.indexOf('const IL={'), html.indexOf('// ---------- timeline'));
const IL = [...ilBlock.matchAll(/^\s{2}(\w+)\(t/gm)].map(m => m[1]);

for (const k of ['date', 'title', 'caption', 'scenes']) if (!ep[k]) errs.push(`champ manquant : ${k}`);
if (!Array.isArray(ep.sources) || ep.sources.length < 1) errs.push('au moins une source vérifiée est requise dans "sources"');
let chars = 0;
(ep.scenes || []).forEach((sc, i) => {
  const where = `scène ${i + 1}`;
  if (!Array.isArray(sc.say) || !sc.say.length) { errs.push(`${where} : "say" vide`); return; }
  const n = sc.say.length;
  sc.say.forEach(s => { const t = typeof s === 'string' ? s : s.text; if (!t || !t.trim()) errs.push(`${where} : phrase vide`); else { chars += t.length; if (/\d/.test(t)) warns.push(`${where} : chiffre dans la voix off ("${t}") → écrire les nombres en lettres`); } });
  const chk = (spec, what) => { if (spec === undefined) return; const idx = typeof spec === 'number' ? spec : Array.isArray(spec) ? spec[0] : spec.phrase; if (!(idx >= 0 && idx < n)) errs.push(`${where} : ${what} pointe vers la phrase ${idx} (il y en a ${n})`); };
  if (sc.il) { if (!IL.includes(sc.il.type)) errs.push(`${where} : illustration inconnue "${sc.il.type}" (dispo : ${IL.join(', ')})`); chk(sc.il.sw, 'il.sw'); }
  if (!Array.isArray(sc.lines) || !sc.lines.length) errs.push(`${where} : aucun titre à l'écran`);
  (sc.lines || []).forEach((L, j) => {
    if (!L.text && !L.count) errs.push(`${where}, ligne ${j + 1} : texte manquant`);
    if (L.text && L.text !== L.text.toUpperCase()) warns.push(`${where}, ligne ${j + 1} : le texte à l'écran devrait être en MAJUSCULES`);
    if (L.text && L.text.replace(/[\[\]]/g, '').length > 24) warns.push(`${where}, ligne ${j + 1} : ligne longue (${L.text.length} car.), elle sera petite`);
    if (L.count && (!L.count.fmt || !L.count.fmt.includes('{v}'))) errs.push(`${where}, ligne ${j + 1} : count.fmt doit contenir {v}`);
    chk(L.at, 'at'); chk(L.strike, 'strike');
  });
  if (Array.isArray(sc.kicker)) sc.kicker.forEach(k => chk(k.at, 'kicker.at'));
  if ((sc.lines || []).length > 5) warns.push(`${where} : plus de 5 lignes, ça va être chargé`);
});
const est = chars / 14.5 + (ep.scenes || []).reduce((a, s) => a + (s.say || []).length * 0.25, 0);
if (chars > 1400) errs.push(`voix off trop longue : ${chars} caractères (max 1400)`);
if (est < 35 || est > 80) warns.push(`durée estimée ${est.toFixed(0)}s (cible 45–70s)`);
warns.forEach(w => console.log('⚠ ' + w));
if (errs.length) { errs.forEach(e => console.error('✗ ' + e)); process.exit(1); }
console.log(`✓ épisode valide : ${ep.scenes.length} scènes, ${chars} caractères, ~${est.toFixed(0)}s`);
