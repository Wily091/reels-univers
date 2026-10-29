// Rendu vidéo (sans son) d'un timeline. Plusieurs navigateurs en parallèle, segments concaténés.
// Usage : node engine/render.js episodes/AAAA-MM-JJ [fps]
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');

const dir = path.resolve(process.argv[2]);
const FPS = +(process.argv[3] || 30);
const build = path.join(dir, 'build');
const tl = JSON.parse(fs.readFileSync(path.join(build, 'timeline.json'), 'utf8'));
const N = Math.round(tl.duration * FPS);
const WORKERS = Math.max(1, Math.min(4, os.cpus().length));
const engine = 'file://' + path.resolve(__dirname, 'engine.html');

async function segment(browser, k, from, to) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => { console.error('ERREUR PAGE', e.message); process.exit(1); });
  await page.goto(engine); await page.evaluate(() => window.ready);
  await page.evaluate(tl => window.setTimeline(tl), tl);
  const out = path.join(build, `seg${k}.mp4`);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', String(FPS), out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = from; i < to; i++) {
    await page.evaluate(t => window.render(t), i / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (k === 0 && (i - from) % 150 === 0) console.log(`  segment 0 : ${i - from}/${to - from}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await page.close();
  return out;
}

(async () => {
  const t0 = Date.now();
  const browser = await chromium.launch();
  const per = Math.ceil(N / WORKERS);
  const parts = await Promise.all([...Array(WORKERS)].map((_, k) => segment(browser, k, k * per, Math.min(N, (k + 1) * per))));
  await browser.close();
  fs.writeFileSync(path.join(build, 'concat.txt'), parts.map(p => `file '${p}'`).join('\n'));
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', path.join(build, 'concat.txt'), '-c', 'copy', path.join(build, 'video.mp4')]);
  console.log(`Rendu : ${N} images, ${WORKERS} workers, ${((Date.now() - t0) / 1000).toFixed(0)}s`);
})();
