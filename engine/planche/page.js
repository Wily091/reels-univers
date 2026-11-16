// Ouvre la planche d'un épisode dans Chromium et attend qu'elle soit prête.
const {chromium}=require('playwright');const path=require('path');
module.exports=async(dir)=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:1080,height:1920}});
  const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+path.join(__dirname,'planche.html')+'?data='+encodeURIComponent(path.resolve(dir,'build','data.js')));
  await p.waitForFunction(()=>window.ready===true,null,{timeout:60000});await p.evaluate(()=>document.fonts.ready);
  const err=(await p.evaluate(()=>window.ERR||[])).concat(errs);return {b,p,err}};
