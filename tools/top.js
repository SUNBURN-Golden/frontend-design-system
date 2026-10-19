const { chromium } = require('playwright-core');
const urls = JSON.parse(require('fs').readFileSync(process.argv[2]));
const vw=+process.argv[3]||1440;
(async()=>{
 const b = await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const out={};
 for(const [n,u] of Object.entries(urls)){
  const ctx=await b.newContext({viewport:{width:vw,height:vw<600?844:900},locale:'ko-KR',userAgent:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'});
  const p=await ctx.newPage();
  try{ await p.goto(u,{waitUntil:'load',timeout:35000}); await p.waitForTimeout(2500);
   out[n]=await p.evaluate(()=>{
    const els=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>5&&r.height>5&&[...e.childNodes].some(x=>x.nodeType===3&&x.textContent.trim().length>1)});
    const rows=els.map(e=>{const s=getComputedStyle(e);return {t:e.innerText.trim().slice(0,22).replace(/\n/g,' '),tag:e.tagName,fs:parseFloat(s.fontSize),lh:s.lineHeight,ls:s.letterSpacing,fw:s.fontWeight,top:Math.round(e.getBoundingClientRect().top+scrollY)}});
    rows.sort((a,b)=>b.fs-a.fs);
    // section spacing: gaps between top-level sections
    const secs=[...document.querySelectorAll('main > section, section')].slice(0,6).map(e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return {pt:s.paddingTop,pb:s.paddingBottom,h:Math.round(r.height),w:Math.round(r.width)}});
    return {top:rows.slice(0,5),secs};
   });
  }catch(e){out[n]={error:String(e).slice(0,100)}}
  await ctx.close();
 }
 await b.close(); require("fs").writeFileSync(process.argv[4],JSON.stringify(out));process.exit(0);
})();
