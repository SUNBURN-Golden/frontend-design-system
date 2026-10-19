const { chromium } = require('playwright-core');
const fs=require('fs');
const urls=JSON.parse(fs.readFileSync(process.argv[2]));const vw=+process.argv[3]||1440;
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const out={};
for(const[k,u]of Object.entries(urls)){const c=await b.newContext({viewport:{width:vw,height:vw<600?844:900},locale:'ko-KR',userAgent:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'});const p=await c.newPage();
try{await p.goto(u,{waitUntil:'domcontentloaded',timeout:30000});await p.waitForTimeout(3000);
out[k]=await p.evaluate(()=>{
 const cs=e=>getComputedStyle(e);
 // choose the p with longest text among paragraphs, group by parent
 const ps=[...document.querySelectorAll('p,div[class*=wrap_body] > *, article span')].filter(e=>{const r=e.getBoundingClientRect();return r.width>200&&(e.innerText||'').trim().length>80&&e.children.length<12});
 if(!ps.length)return null;
 // pick median-ish: first with length>150
 const el=ps.find(e=>e.innerText.trim().length>150)||ps[0];
 const s=cs(el),r=el.getBoundingClientRect();
 // first line char count via Range
 const tn=[...el.childNodes].find(n=>n.nodeType===3&&n.textContent.trim().length>20)||(function w(n){const t=document.createTreeWalker(n,NodeFilter.SHOW_TEXT);let x;while(x=t.nextNode()){if(x.textContent.trim().length>20)return x}})(el);
 let first=null;
 if(tn){const rg=document.createRange();const txt=tn.textContent;let top=null,count=0;for(let i=0;i<txt.length;i++){rg.setStart(tn,i);rg.setEnd(tn,i+1);const rr=rg.getClientRects()[0];if(!rr)continue;if(top===null)top=rr.top;if(Math.abs(rr.top-top)>4)break;count++}first=count}
 const h1=document.querySelector('h1');const hs=h1?cs(h1):null;
 const art=el.closest('article')||el.parentElement;
 const ar=art.getBoundingClientRect();
 const nextP=el.nextElementSibling?cs(el.nextElementSibling):null;
 return {sample:el.innerText.trim().slice(0,25),fs:s.fontSize,lh:s.lineHeight,ls:s.letterSpacing,fw:s.fontWeight,ff:s.fontFamily.split(',')[0],color:s.color,bg:cs(document.body).backgroundColor,pWidth:Math.round(r.width),firstLineChars:first,wordBreak:s.wordBreak,mb:s.marginBottom,pad:s.padding,textAlign:s.textAlign,h1:hs&&{fs:hs.fontSize,lh:hs.lineHeight,ls:hs.letterSpacing,fw:hs.fontWeight,ff:hs.fontFamily.split(',')[0],ta:hs.textWrap},artWidth:Math.round(ar.width)};
});}catch(e){out[k]={error:String(e).slice(0,80)}}
await c.close().catch(()=>{});fs.writeFileSync(process.argv[4],JSON.stringify(out,null,1))}
await b.close();process.exit(0)})();
