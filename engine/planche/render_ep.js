// Rend les images d'un épisode : node render_ep.js <dossier_episode> <dossier_images> <début> <fin>  (images à 30 i/s)
const fs=require('fs');const open=require('./page');(async()=>{const [,,dir,out,a,b]=process.argv;const {b:br,p,err}=await open(dir);
if(err.length){console.error('ERREUR planche :',err.join(' | '));process.exit(1)}fs.mkdirSync(out,{recursive:true});await p.waitForTimeout(300);const el=await p.$('#v');
for(let i=+a;i<+b;i++){await p.evaluate(t=>window.renderAt(t),i/30);await el.screenshot({path:`${out}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92})}await br.close()})();
