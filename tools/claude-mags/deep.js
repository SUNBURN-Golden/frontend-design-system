const { chromium } = require('playwright-core');
const fs=require('fs');
const urls=JSON.parse(fs.readFileSync(process.argv[2]));const vw=+process.argv[3]||1440;const scheme=process.argv[4]||'light';const outf=process.argv[5];
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const out={};
for(const[k,u]of Object.entries(urls)){const c=await b.newContext({viewport:{width:vw,height:vw<600?844:900},colorScheme:scheme,locale:'en-US',userAgent:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'});const p=await c.newPage();
try{const resp=await p.goto(u,{waitUntil:'domcontentloaded',timeout:30000});await p.waitForTimeout(3500);
out[k]=await p.evaluate((status)=>{
 const cs=e=>getComputedStyle(e);const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0};
 const all=[...document.querySelectorAll('body *')].filter(vis).slice(0,5000);
 const vh=innerHeight, vwid=innerWidth;
 // area by bg color within first viewport
 const area={};let tot=vwid*vh;
 const rgba=s=>s;
 for(const e of all){const s=cs(e);const bg=s.backgroundColor;if(bg==='rgba(0, 0, 0, 0)')continue;const r=e.getBoundingClientRect();const w=Math.max(0,Math.min(r.right,vwid)-Math.max(r.left,0)),h=Math.max(0,Math.min(r.bottom,vh)-Math.max(r.top,0));const a=w*h;if(a>0)area[bg]=(area[bg]||0)+a}
 const areaTop=Object.entries(area).sort((a,b)=>b[1]-a[1]).slice(0,8).map(([c,a])=>[c,(a/tot*100).toFixed(1)+'%']);
 const hist=(f,n=8)=>{const m={};all.forEach(e=>{const v=f(e);if(v)m[v]=(m[v]||0)+1});return Object.entries(m).sort((a,b)=>b[1]-a[1]).slice(0,n)};
 const hasText=e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());
 const textColors=hist(e=>hasText(e)?cs(e).color:null);
 const borders=hist(e=>{const s=cs(e);return s.borderTopWidth!=='0px'&&s.borderTopStyle!=='none'?s.borderTopWidth+' '+s.borderTopColor:null});
 const radius=hist(e=>{const v=cs(e).borderTopLeftRadius;return v!=='0px'?v:null});
 const shadow=hist(e=>{const v=cs(e).boxShadow;return v!=='none'?v.slice(0,100):null});
 const trans=hist(e=>{const s=cs(e);return s.transitionDuration!=='0s'?s.transitionProperty.slice(0,30)+'|'+s.transitionDuration.slice(0,12)+'|'+s.transitionTimingFunction.slice(0,40):null});
 const sizes=hist(e=>hasText(e)?cs(e).fontSize:null);
 const fonts=hist(e=>hasText(e)?cs(e).fontFamily.slice(0,60):null,5);
 const root=cs(document.documentElement);
 const vars={};
 try{for(const sh of document.styleSheets){let rules;try{rules=sh.cssRules}catch(e){continue}for(const r of rules){if(r.selectorText&&/^(:root|html|\.dark|\[data-theme|body)/.test(r.selectorText)&&r.style){for(const n of r.style){if(n.startsWith('--')&&/(bg|background|surface|text|fg|border|accent|brand|primary|color|clay|kraft|ivory|slate|cloud|oat|focus)/i.test(n))vars[n]=r.style.getPropertyValue(n).trim().slice(0,60)}}}}}catch(e){}
 const varKeys=Object.keys(vars);
 const pick=e=>{if(!e)return null;const s=cs(e);return {t:(e.innerText||'').trim().slice(0,28),fs:s.fontSize,lh:s.lineHeight,ls:s.letterSpacing,fw:s.fontWeight,ff:s.fontFamily.slice(0,60),color:s.color,w:Math.round(e.getBoundingClientRect().width)}};
 const h1=[...document.querySelectorAll('h1')].find(vis);const h2=[...document.querySelectorAll('h2')].find(vis);
 const p=[...document.querySelectorAll('p')].find(e=>vis(e)&&e.innerText.length>40);
 const btns=[...document.querySelectorAll('button,a')].filter(e=>vis(e)&&cs(e).backgroundColor!=='rgba(0, 0, 0, 0)').slice(0,6).map(e=>{const s=cs(e);const r=e.getBoundingClientRect();return {t:(e.innerText||'').trim().slice(0,22),bg:s.backgroundColor,color:s.color,radius:s.borderTopLeftRadius,h:Math.round(r.height),w:Math.round(r.width),fs:s.fontSize,fw:s.fontWeight,pad:s.padding}});
 const links=[...document.querySelectorAll('a')].filter(vis).slice(0,40).map(e=>cs(e).color);
 const linkColors={};links.forEach(c=>linkColors[c]=(linkColors[c]||0)+1);
 const inputs=[...document.querySelectorAll('textarea,input[type=text],input[type=email],[contenteditable=true]')].filter(vis).slice(0,2).map(e=>{const s=cs(e);const r=e.getBoundingClientRect();return {tag:e.tagName,ph:(e.getAttribute('placeholder')||e.getAttribute('aria-label')||e.getAttribute('data-placeholder')||'').slice(0,60),bg:s.backgroundColor,border:s.borderTopWidth+' '+s.borderTopColor,radius:s.borderTopLeftRadius,shadow:s.boxShadow.slice(0,100),fs:s.fontSize,h:Math.round(r.height),w:Math.round(r.width)}});
 const textLen=document.body.innerText.length;const words=document.body.innerText.split(/\s+/).filter(Boolean).length;
 // first viewport words
 let vwords=0;for(const e of all){if(hasText(e)){const r=e.getBoundingClientRect();if(r.top<vh&&r.bottom>0)vwords+=(e.innerText||'').split(/\s+/).filter(Boolean).length>0?[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim().split(/\s+/).filter(Boolean).length).reduce((a,b)=>a+b,0):0}}
 return {status,title:document.title.slice(0,70),url:location.href,bodyBg:cs(document.body).backgroundColor,htmlBg:root.backgroundColor,colorScheme:root.colorScheme,metaColorScheme:document.querySelector('meta[name=color-scheme]')?.content||null,themeColor:document.querySelector('meta[name=theme-color]')?.content||null,areaTop,textColors,borders,radius,shadow,trans,sizes,fonts,vars:varKeys.length?vars:null,h1:pick(h1),h2:pick(h2),p:pick(p),btns,linkColors,inputs,viewportWords:vwords,totalWords:words};
 },resp&&resp.status());}catch(e){out[k]={error:String(e).slice(0,100)}}
await c.close().catch(()=>{});fs.writeFileSync(outf,JSON.stringify(out,null,1))}
await b.close();process.exit(0)})();
