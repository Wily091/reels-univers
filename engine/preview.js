// Planche d'aperçu : une image au milieu de chaque scène (après build_timeline).
// Usage : node engine/preview.js episodes/AAAA-MM-JJ  → build/preview.jpg
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path');
const dir = path.resolve(process.argv[2]); const build = path.join(dir, 'build');
const tl = JSON.parse(fs.readFileSync(path.join(build, 'timeline.json'), 'utf8'));
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => { console.error('ERREUR PAGE', e.message); process.exit(1); });
  await p.goto('file://' + path.resolve(__dirname, 'engine.html')); await p.evaluate(() => window.ready);
  await p.evaluate(tl => window.setTimeline(tl), tl);
  const pv = path.join(build, 'pv'); fs.mkdirSync(pv, { recursive: true });
  for (const f of fs.readdirSync(pv)) fs.unlinkSync(path.join(pv, f));
  let i = 0;
  for (const sc of tl.scenes) {
    const last = sc.lines.length ? Math.max(...sc.lines.map(l => l.t)) : sc.s;
    const t = Math.min(sc.e - 0.05, Math.max(last + 1.0, (sc.s + sc.e) / 2));
    await p.evaluate(t => window.render(t), t);
    await p.screenshot({ path: path.join(pv, `${String(i++).padStart(2, '0')}.jpg`), type: 'jpeg', quality: 80 });
  }
  await b.close();
  const cols = Math.min(6, i);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-pattern_type', 'glob', '-i', path.join(pv, '*.jpg'), '-vf', `scale=270:480,tile=${cols}x${Math.ceil(i / cols)}`, '-frames:v', '1', path.join(build, 'preview.jpg')]);
  console.log('Aperçu : ' + path.join(build, 'preview.jpg'));
})();
