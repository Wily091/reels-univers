const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+__dirname+'/planche_anim.html');await p.evaluate(()=>document.fonts.ready);
const r=await p.evaluate(()=>{const out=[];let prev=null,maxJ=0,at=0;for(let i=0;i<1439;i++){const t=i/30;window.renderAt(t);const m=document.getElementById('cam').getAttribute('transform').match(/[-\d.]+/g).map(Number);
 if(prev){const d=Math.hypot(m[3]-prev[3],m[4]-prev[4])*m[2]+Math.abs(m[2]-prev[2])*1500;const dd=Math.abs(d-(prev.d||0));if(dd>maxJ){maxJ=dd;at=t}m.d=d}prev=m}return [maxJ,at]});console.log('saut de vitesse max (px/image):',r);await b.close()})();
