// Contrôle gratuit d'une planche (avant voix ou avant rendu) : erreurs, chevauchements, à-coups de caméra,
// et aperçu de l'image finale (<ep>/build/preview.jpg) + 4 images clés (<ep>/build/key_*.jpg).
// Usage : node check_layout.js <dossier_episode>   → code de sortie 1 si problème.
const fs=require('fs'),path=require('path');const open=require('./page');(async()=>{const dir=process.argv[2];const {b,p,err}=await open(dir);if(err.length){err.forEach(x=>console.error('::error title=Planche::'+x));await b.close();process.exit(1)}
const r=await p.evaluate(()=>{let prev=null,maxJ=0,at=0;const n=Math.ceil(window.END*30);for(let i=0;i<n;i++){const t=i/30;window.renderAt(t);const m=document.getElementById('cam').getAttribute('transform').match(/[-\d.]+/g).map(Number);
 if(prev){const d=Math.hypot(m[3]-prev[3],m[4]-prev[4])*m[2]+Math.abs(m[2]-prev[2])*1500;const dd=Math.abs(d-(prev.d||0));if(dd>maxJ){maxJ=dd;at=t}m.d=d}prev=m}
 return {END:window.END,OV:window.OVERLAPS,PLAN:window.PLAN,jump:[+maxJ.toFixed(2),+at.toFixed(2)]}});
const B=path.join(dir,'build');const el=await p.$('#v');
for(const [nm,t] of [['key_1',0],['key_2',r.END*.3],['key_3',r.END*.6],['key_4',r.END*.85],['preview',r.END-1/30]]){await p.evaluate(t=>window.renderAt(t),t);await el.screenshot({path:path.join(B,nm+'.jpg'),type:'jpeg',quality:88})}
await b.close();const bad=[...err,...r.OV];if(r.jump[0]>6)bad.push(`à-coup caméra ${r.jump[0]} px/image à ${r.jump[1]} s`);
fs.writeFileSync(path.join(B,'layout.json'),JSON.stringify({...r,errors:bad},null,1));
console.log(`Planche : ${r.END}s, saut caméra max ${r.jump[0]} px/image, plan ${JSON.stringify(r.PLAN)}`);
if(bad.length){bad.forEach(x=>console.error('::error title=Planche::'+x));process.exit(1)}console.log('Mise en page OK (aucun chevauchement)')})();
