const { chromium } = require('playwright-core');const fs=require('fs');
const urls=JSON.parse(fs.readFileSync(process.argv[2]));const scheme=process.argv[3];const vw=+process.argv[4]||1440;const outf=process.argv[5];
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const out={};
for(const[k,u]of Object.entries(urls)){const c=await b.newContext({viewport:{width:vw,height:vw<600?844:900},colorScheme:scheme,userAgent:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'});const p=await c.newPage();
try{await p.goto(u,{waitUntil:'domcontentloaded',timeout:30000});await p.waitForTimeout(3500);
const full=await p.evaluate(()=>document.documentElement.scrollHeight);
out[k]=await p.evaluate((full)=>{
 const parse=s=>{const m=s.match(/rgba?\(([^)]+)\)/);if(!m)return null;const a=m[1].split(/[ ,\/]+/).map(Number);return a};
 const isAccent=s=>{const a=parse(s);if(!a||a.length<3)return false;if(a.length>=4&&a[3]<0.5)return false;const [r,g,b]=a;const mx=Math.max(r,g,b),mn=Math.min(r,g,b);if(mx-mn<50)return false;return r>g&&g>b&&r>150}; // warm orange/clay family
 const vh=innerHeight,vw=innerWidth;const hits=[];
 const cs=e=>getComputedStyle(e);
 for(const e of document.querySelectorAll('body *')){const s=cs(e);const r=e.getBoundingClientRect();if(r.width<2||r.height<2)continue;
  const props={bg:s.backgroundColor,color:[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())?s.color:null,border:s.borderTopWidth!=='0px'?s.borderTopColor:null,fill:e instanceof SVGElement?s.fill:null,outline:s.outlineStyle!=='none'?s.outlineColor:null};
  for(const[kk,v]of Object.entries(props)){if(v&&isAccent(v)){const w=Math.max(0,Math.min(r.right,vw)-Math.max(r.left,0)),h=Math.max(0,Math.min(r.bottom+scrollY,full)-Math.max(r.top+scrollY,0));hits.push({prop:kk,val:v,tag:e.tagName,txt:(e.innerText||'').trim().slice(0,24),cls:(e.className&&e.className.baseVal===undefined?String(e.className):'').slice(0,40),area:Math.round(w*h),inVp:r.top<vh&&r.bottom>0})}}}
 const pageArea=vw*full;const bgHits=hits.filter(h=>h.prop==='bg');
 const sum=a=>a.reduce((x,y)=>x+y.area,0);
 const byProp={};hits.forEach(h=>byProp[h.prop]=(byProp[h.prop]||0)+1);
 // resolved CSS variables
 const root=cs(document.documentElement);const names=new Set();
 for(const sh of document.styleSheets){let rules;try{rules=sh.cssRules}catch(e){continue}const walk=rs=>{for(const r of rs){if(r.style){for(const n of r.style)if(typeof n==='string'&&n.startsWith('--'))names.add(n)}if(r.cssRules)walk(r.cssRules)}};walk(rules)}
 const want=[...names].filter(n=>/^--(cds-(page-bg|surface|text|border|ring|accent|brand|clay|link|button|btn|input|composer|sidebar|fizzy)|color-(clay|gray-(000|050|100|150|200|250|300|400|500|600|700|800|850|900|950)|slate-(000|050|100|150|200|300|500|600|700|800|900|950))|bg-|text-|border-|accent|brand)/.test(n)).slice(0,160);
 const rv={};want.forEach(n=>{const v=root.getPropertyValue(n).trim();if(v&&v.length<90)rv[n]=v});
 // composer-like container
 const ta=document.querySelector('textarea, [contenteditable=true]');let comp=null;if(ta){let e=ta;for(let i=0;i<8&&e;i++,e=e.parentElement){const s=cs(e);if(parseFloat(s.borderTopLeftRadius)>=10){const r=e.getBoundingClientRect();comp={tag:e.tagName,radius:s.borderTopLeftRadius,bg:s.backgroundColor,border:s.borderTopWidth+' '+s.borderTopColor,shadow:s.boxShadow.slice(0,160),w:Math.round(r.width),h:Math.round(r.height),pad:s.padding};break}}}
 return {pageH:full,accentHitCount:hits.length,byProp,accentBgAreaPctOfPage:+(sum(bgHits)/pageArea*100).toFixed(2),accentBgInViewport:bgHits.filter(h=>h.inVp).map(h=>[h.tag,h.txt,h.area,h.val]).slice(0,6),accentTextSamples:hits.filter(h=>h.prop==='color').slice(0,6).map(h=>[h.tag,h.txt,h.val]),accentOther:hits.filter(h=>!['bg','color'].includes(h.prop)).slice(0,6).map(h=>[h.prop,h.tag,h.txt,h.val]),resolvedVars:rv,composer:comp};
 },full);}catch(e){out[k]={error:String(e).slice(0,100)}}
await c.close().catch(()=>{});fs.writeFileSync(outf,JSON.stringify(out,null,1))}
await b.close();process.exit(0)})();
