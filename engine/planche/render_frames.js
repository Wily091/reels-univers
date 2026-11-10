const {chromium}=require('playwright');const fs=require('fs');(async()=>{const [,,dir,a,b,step]=process.argv;const fps=30;
const br=await chromium.launch();const p=await br.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+__dirname+'/'+(process.env.PAGE||'planche_anim.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
await p.evaluate(()=>{});fs.mkdirSync(dir,{recursive:true});
for(let i=+a;i<+b;i+=(+step||1)){await p.evaluate(t=>window.renderAt(t),i/fps);await (await p.$('#v')).screenshot({path:`${dir}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92})}await br.close()})();
