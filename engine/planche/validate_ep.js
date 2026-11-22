// Contrôle d'un épisode au format « planche » (docs/STYLE_PLANCHE.md + docs/LEGENDES.md). Sortie 1 si erreur.
// Usage : node engine/planche/validate_ep.js <dossier_episode>
const fs=require('fs'),path=require('path');const D=process.argv[2];const ROOT=path.resolve(__dirname,'../..');
const ep=JSON.parse(fs.readFileSync(path.join(D,'episode.json'),'utf8'));const E=[],Wn=[];
// Fin courte (format 20–30 s, validé par William le 22/11) ; l'ancienne fin longue reste acceptée pour les épisodes déjà publiés.
const FIN="Abonne-toi pour d'autres histoires sur l'univers, et envoie la vidéo à quelqu'un que ça va faire rêver.";
const FIN_OLD="Si ça t'a plu, abonne-toi pour d'autres histoires sur l'univers, et si tu connais quelqu'un que ça pourrait faire rêver, partage-lui la vidéo.";
if(ep.format!=='planche')E.push('format doit valoir "planche" (ancien style interdit)');
if(!ep.num)E.push('num (numéro de planche) manquant');
if(!ep.subject||ep.subject.length>14)E.push('subject (titre central, ≤ 14 caractères) manquant ou trop long');
if((ep.voice||{}).id!=='TojRWZatQyy9dujEdiQ1')E.push('voix : Koraly Storyteller TojRWZatQyy9dujEdiQ1 obligatoire');
const sc=ep.scenes||[];const says=sc.flatMap(s=>s.say||[]);
if(!sc.length||!/\?$/.test(sc[0].say[0].trim()))E.push('la 1re phrase doit être une question d\'accroche');
const last=sc[sc.length-1];if(!last||!last.fin||(last.say.join(' ')!==FIN&&last.say.join(' ')!==FIN_OLD))E.push('dernière scène : fin standard exacte avec "fin": true');
says.forEach(t=>{if(/…|\.\.\./.test(t))E.push(`points de suspension interdits : « ${t.slice(0,40)}… »`);if(/\d/.test(t))E.push(`chiffres en lettres dans la voix : « ${t.slice(0,50)} »`)});
const chars=says.join(' ').length;const est=chars/22.8;   // calé sur la référence Vénus : 880 caractères ≈ 38,6 s
if(est<18||est>32)E.push(`durée estimée ${est.toFixed(0)} s (format court : viser 20–30 s, ≈ 460–680 caractères)`);
const hk=ep.hook;if(!hk||!Array.isArray(hk.lines)||!hk.lines.length||hk.lines.length>3)E.push('hook : accroche écrite obligatoire (1 à 3 lignes, voir docs/FORMAT_PLANCHE.md)');
const notes=sc.filter(s=>s.note);if(notes.length<4||notes.length>6)E.push(`4 à 6 notes attendues (${notes.length})`);
const ids=new Set((ep.images||[]).map(i=>i.id));
(ep.images||[]).forEach(im=>{['id','file','credit','page','license'].forEach(k=>{if(!im[k])E.push(`image ${im.id||'?'} : champ ${k} manquant`)});if(im.file&&!fs.existsSync(path.join(ROOT,im.file)))Wn.push(`photo à télécharger : ${im.file}`)});
if(ep.center&&ep.center.photo&&!ids.has(ep.center.photo))E.push('center.photo inconnue');
notes.forEach(s=>s.note.forEach(it=>{if(!['text','sketch','photo','round'].includes(it.t))E.push('élément inconnu : '+it.t);if((it.t==='photo'||it.t==='round')&&!ids.has(it.img))E.push('photo inconnue : '+it.img)}));
const cap=ep.caption||'';const l1=cap.split('\n')[0];
if(l1.length>125)E.push(`légende : 1re ligne > 125 caractères (${l1.length})`);
if(cap.length<600||cap.length>1200)E.push(`légende : ${cap.length} caractères (600–1 200 attendus)`);
const h=ep.hashtags||[];if(h.length<1||h.length>5)E.push('hashtags : 5 maximum');
if(!h.includes('#universenbref'))E.push('hashtag #universenbref obligatoire');
h.forEach(x=>{if(!/^#[a-z0-9]+$/.test(x))E.push(`hashtag invalide (minuscules, sans accent) : ${x}`)});
if(!(ep.sources||[]).length)E.push('sources manquantes');
Wn.forEach(x=>console.log('::warning title=Épisode::'+x));
if(E.length){E.forEach(x=>console.error('::error title=Épisode invalide::'+x));process.exit(1)}
console.log(`Épisode OK : ${ep.title} (${says.length} phrases, ~${est.toFixed(0)} s, ${notes.length} notes, ${(ep.images||[]).length} photo(s))`);
