const { chromium } = require('playwright-core');const fs=require('fs');
const urls=JSON.parse(fs.readFileSync(process.argv[2]));const outf=process.argv[3];const scheme=process.argv[4]||'light';
const UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36';
function metrics(){
 const cs=e=>getComputedStyle(e);const vh=innerHeight,vw=innerWidth;
 const inVp=r=>r.width>1&&r.height>1&&r.bottom>0&&r.top<vh&&r.right>0&&r.left<vw;
 const vis=e=>{const r=e.getBoundingClientRect();return inVp(r)&&cs(e).visibility!=='hidden'&&cs(e).display!=='none'};
 // words in viewport
 let words=0,chars=0;const tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=tw.nextNode()){const t=n.textContent.trim();if(!t)continue;const pe=n.parentElement;if(!pe||['SCRIPT','STYLE','NOSCRIPT'].includes(pe.tagName))continue;const rg=document.createRange();rg.selectNodeContents(n);const r=rg.getBoundingClientRect();if(inVp(r)&&cs(pe).visibility!=='hidden'&&cs(pe).display!=='none'&&cs(pe).opacity!=='0'){words+=t.split(/\s+/).length;chars+=t.length}}
 const links=[...document.querySelectorAll('a[href]')].filter(vis);const uniq=new Set(links.map(a=>a.href));
 const hdr=document.querySelector('header')||document.querySelector('nav');
 let nav=0;if(hdr){const navEl=hdr.querySelector('nav')||hdr;nav=[...navEl.querySelectorAll('a')].filter(a=>{const r=a.getBoundingClientRect();return r.width>0&&r.height>0&&(a.innerText||'').trim().length>0}).length}
 const btnLike=[...document.querySelectorAll('a,button,[role=button]')].filter(e=>{if(!vis(e))return false;const s=cs(e);return s.backgroundColor!=='rgba(0, 0, 0, 0)'&&parseFloat(s.borderTopLeftRadius)>=3&&(e.innerText||'').trim().length>0&&(e.innerText||'').trim().length<40});
 const ctas=btnLike.map(e=>(e.innerText||'').trim().replace(/\s+/g,' ').slice(0,24));
 const inputs=[...document.querySelectorAll('input:not([type=hidden]),textarea')].filter(vis).length;
 // largest text
 let best=null;for(const e of document.querySelectorAll('h1,h2,h3,p,div,span,a')){if(![...e.childNodes].some(x=>x.nodeType===3&&x.textContent.trim().length>2))continue;const r=e.getBoundingClientRect();if(!inVp(r))continue;const fs=parseFloat(cs(e).fontSize);if(!best||fs>best.fs)best={fs,len:e.innerText.trim().length,tag:e.tagName,t:e.innerText.trim().replace(/\s+/g,' ').slice(0,40)}}
 const h1=document.querySelector('h1');
 // cards: anchors w/ img in viewport or article elements
 const cardEls=[...document.querySelectorAll('article, li, a')].filter(e=>vis(e)&&e.querySelector('img,picture,video')&&e.getBoundingClientRect().width>100&&e.getBoundingClientRect().width<vw*0.8&&e.getBoundingClientRect().height>80&&(e.innerText||'').trim().length>8);
 // dedupe nested: keep those without a card descendant in set
 const set=new Set(cardEls);const leafCards=cardEls.filter(e=>![...e.querySelectorAll('*')].some(x=>set.has(x)));
 const cards=leafCards.slice(0,40).map(e=>{const img=e.querySelector('img,picture,video');const ir=img.getBoundingClientRect();const hd=e.querySelector('h1,h2,h3,h4,[class*=title],[class*=Title],[class*=headline],[class*=Headline]');let lines=null,tfs=null;if(hd){const s=cs(hd);const lh=parseFloat(s.lineHeight)||parseFloat(s.fontSize)*1.3;lines=Math.round(hd.getBoundingClientRect().height/lh);tfs=s.fontSize}
  const leaf=[...e.querySelectorAll('*')].filter(x=>x.children.length===0&&(x.innerText||'').trim().length>0).length;
  return {w:Math.round(e.getBoundingClientRect().width),imgW:Math.round(ir.width),imgH:Math.round(ir.height),ratio:ir.height?+(ir.width/ir.height).toFixed(2):null,titleLines:lines,titleFs:tfs,textLeafCount:leaf,chars:(e.innerText||'').trim().length}});
 const dark=cs(document.documentElement).colorScheme;
 return {words,chars,vpLinks:uniq.size,navLinks:nav,ctaCount:ctas.length,ctas:ctas.slice(0,6),inputs,largest:best,h1len:h1?h1.innerText.trim().length:null,cards:cards.slice(0,12),cardCountInVp:leafCards.length,pageH:document.documentElement.scrollHeight,vh,bodyBg:cs(document.body).backgroundColor,colorScheme:dark,lang:document.documentElement.lang,
  hasDarkQuery:null};
}
function findArticle(){
 const cs=e=>getComputedStyle(e);const ok=a=>{const r=a.getBoundingClientRect();if(r.width<5||r.height<5)return false;const t=(a.innerText||'').trim();if(t.length<22||t.length>200)return false;if(a.closest('header,nav,footer'))return false;let u;try{u=new URL(a.href)}catch(e){return false}if(u.origin!==location.origin)return false;const segs=u.pathname.split('/').filter(Boolean);if(segs.length<1||u.pathname===location.pathname)return false;if(/\.(png|jpg|pdf)$/.test(u.pathname))return false;if(/(tag|category|topic|section|author|about|subscribe|newsletter|search|login)(\/|$)/i.test(u.pathname)&&segs.length<3)return false;return true};
 const as=[...document.querySelectorAll('a[href]')].filter(ok);
 // prefer anchors in heading tags
 const h=as.find(a=>a.closest('h1,h2,h3')||a.querySelector('h1,h2,h3'));return (h||as[0]||{}).href||null}
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const out={};
for(const[k,u]of Object.entries(urls)){out[k]={};
 for(const vw of [1440,390]){
  const c=await b.newContext({viewport:{width:vw,height:vw<600?844:900},colorScheme:scheme,userAgent:UA,locale:'en-US'});const p=await c.newPage();
  try{await p.goto(u,{waitUntil:'domcontentloaded',timeout:30000});await p.waitForTimeout(3500);
   try{await p.keyboard.press('Escape')}catch(e){}
   const m=await p.evaluate(metrics);const art=await p.evaluate(findArticle);out[k]['home'+vw]=m;if(vw===1440)out[k].articleUrl=art;}
  catch(e){out[k]['home'+vw]={error:String(e).slice(0,80)}}
  await c.close().catch(()=>{});
  fs.writeFileSync(outf,JSON.stringify(out,null,1));
 }
 // article page first screen
 const au=out[k].articleUrl;if(au){for(const vw of [1440,390]){const c=await b.newContext({viewport:{width:vw,height:vw<600?844:900},colorScheme:scheme,userAgent:UA,locale:'en-US'});const p=await c.newPage();
  try{await p.goto(au,{waitUntil:'domcontentloaded',timeout:30000});await p.waitForTimeout(3500);out[k]['article'+vw]=await p.evaluate(metrics);
   out[k]['artDetail'+vw]=await p.evaluate(()=>{const cs=e=>getComputedStyle(e);const hasTime=!!document.querySelector('time');const by=!!document.querySelector('[rel=author],[class*=byline],[class*=Byline],[class*=author],[class*=Author],[itemprop=author]');const ps=[...document.querySelectorAll('article p, main p, p')].filter(e=>{const r=e.getBoundingClientRect();return r.width>200&&e.innerText.trim().length>120});const el=ps[0];let o={time:hasTime,byline:by,progressBar:!!document.querySelector('[role=progressbar],[class*=progress]'),toc:!!document.querySelector('[class*=toc],[class*=Toc],[class*=table-of-contents]')};if(el){const s=cs(el);const r=el.getBoundingClientRect();const tn=(function w(n){const t=document.createTreeWalker(n,NodeFilter.SHOW_TEXT);let x;while(x=t.nextNode()){if(x.textContent.trim().length>20)return x}})(el);let first=null;if(tn){const rg=document.createRange();const txt=tn.textContent;let top=null,cnt=0;for(let i=0;i<txt.length;i++){rg.setStart(tn,i);rg.setEnd(tn,i+1);const rr=rg.getClientRects()[0];if(!rr)continue;if(top===null)top=rr.top;if(Math.abs(rr.top-top)>4)break;cnt++}first=cnt}o={...o,fs:s.fontSize,lh:s.lineHeight,ff:s.fontFamily.split(',')[0],color:s.color,w:Math.round(r.width),firstLineChars:first,korean:/[가-힣]/.test(el.innerText),mb:s.marginBottom,align:s.textAlign,bg:cs(document.body).backgroundColor}}const h1=document.querySelector('h1');if(h1){const s=cs(h1);o.h1={fs:s.fontSize,lh:s.lineHeight,fw:s.fontWeight,ff:s.fontFamily.split(',')[0],len:h1.innerText.trim().length,lines:Math.round(h1.getBoundingClientRect().height/(parseFloat(s.lineHeight)||parseFloat(s.fontSize)*1.2))}}return o});}
  catch(e){out[k]['article'+vw]={error:String(e).slice(0,80)}}
  await c.close().catch(()=>{});fs.writeFileSync(outf,JSON.stringify(out,null,1))}}
}
await b.close();process.exit(0)})();
