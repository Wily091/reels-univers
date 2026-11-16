// Prépare les données du rendu générique : <ep>/build/data.js (épisode + calage voix + photos recadrées).
// Usage : node engine/planche/make_data.js <dossier_episode>
const fs=require('fs'),path=require('path'),{execFileSync}=require('child_process');
const ROOT=path.resolve(__dirname,'../..');const D=path.resolve(process.argv[2]);const B=path.join(D,'build');
const EP=JSON.parse(fs.readFileSync(path.join(D,'episode.json'),'utf8'));
const PH=JSON.parse(fs.readFileSync(path.join(B,'phrases.json'),'utf8'));
fs.mkdirSync(path.join(B,'img'),{recursive:true});const IMG={};
for(const im of EP.images||[]){
  const src=path.resolve(ROOT,im.file);if(!fs.existsSync(src)){console.error(`::error title=Photo manquante::${im.file} (lancer le workflow « Télécharger des images officielles »)`);process.exit(1)}
  const out=path.join(B,'img',im.id+'.jpg');const vf=[];
  if(im.crop){const [x,y,w,h]=im.crop;vf.push(`crop=iw*${w}:ih*${h}:iw*${x}:ih*${y}`)}
  if(im.pad)vf.push("pad='max(iw,ih)':'max(iw,ih)':'(ow-iw)/2':'(oh-ih)/2':black");
  vf.push("scale='min(1000,iw)':-2");
  execFileSync('ffmpeg',['-v','error','-y','-i',src,'-vf',vf.join(','),'-q:v','3',out]);
  IMG[im.id]={src:'file://'+out,credit:im.credit};
}
fs.writeFileSync(path.join(B,'data.js'),`window.EP=${JSON.stringify(EP)};window.PH=${JSON.stringify(PH)};window.IMG=${JSON.stringify(IMG)};`);
console.log(`data.js prêt (${Object.keys(IMG).length} photo(s), ${PH.phrases.length} phrases, voix ${PH.duration}s)`);
