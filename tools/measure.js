const { chromium } = require('playwright-core');
const fs=require('fs');
const urls = JSON.parse(fs.readFileSync(process.argv[2]));
const vw = +process.argv[3]||1440, vh = vw<600?844:900;
const scheme = process.argv[4]||'light';
(async()=>{
 const browser = await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const out={};
 for (const [name,url] of Object.entries(urls)){
  const ctx = await browser.newContext({viewport:{width:vw,height:vh},colorScheme:scheme,locale:'ko-KR',userAgent:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'});
  const page = await ctx.newPage();
  try{
   await page.goto(url,{waitUntil:'domcontentloaded',timeout:30000});
   await page.waitForTimeout(2500);
   out[name]=await page.evaluate(()=>{
    const cs=e=>getComputedStyle(e);
    const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0};
    const pick=e=>{if(!e)return null;const s=cs(e),r=e.getBoundingClientRect();return {tag:e.tagName,text:(e.innerText||'').trim().slice(0,30),fs:s.fontSize,lh:s.lineHeight,ls:s.letterSpacing,fw:s.fontWeight,ff:s.fontFamily.slice(0,70),color:s.color,wordBreak:s.wordBreak,w:Math.round(r.width),h:Math.round(r.height),mt:s.marginTop,mb:s.marginBottom,tt:s.textWrap}};
    const h1=[...document.querySelectorAll('h1')].filter(vis)[0];
    const h2=[...document.querySelectorAll('h2')].filter(vis)[0];
    const ps=[...document.querySelectorAll('p')].filter(e=>vis(e)&&(e.innerText||'').length>40);
    const p=ps[0];
    // text line length of p
    let cpl=null; if(p){const t=p.innerText.length; const r=p.getBoundingClientRect(); const s=cs(p); cpl={chars:t,width:Math.round(r.width),fs:s.fontSize, approxCharsPerLine: Math.round(r.width/(parseFloat(s.fontSize)*(/[가-힣]/.test(p.innerText)?1:0.5)))}}
    const all=[...document.querySelectorAll('body *')].filter(vis).slice(0,4000);
    const hist=(f)=>{const m={};all.forEach(e=>{const v=f(e);if(v)m[v]=(m[v]||0)+1});return Object.entries(m).sort((a,b)=>b[1]-a[1]).slice(0,8)};
    const radius=hist(e=>{const v=cs(e).borderTopLeftRadius;return v&&v!=='0px'?v:null});
    const shadow=hist(e=>{const v=cs(e).boxShadow;return v&&v!=='none'?v.slice(0,90):null});
    const trans=hist(e=>{const s=cs(e);const v=s.transitionDuration;return v&&v!=='0s'?(s.transitionProperty.slice(0,40)+' | '+v+' | '+s.transitionTimingFunction.slice(0,50)):null});
    const sizes=hist(e=>{ if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))return null; return cs(e).fontSize});
    const colors=hist(e=>{ if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))return null; return cs(e).color});
    const bgs=hist(e=>{const v=cs(e).backgroundColor;return v&&v!=='rgba(0, 0, 0, 0)'?v:null});
    const fonts=hist(e=>{ if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))return null; return cs(e).fontFamily.split(',')[0]});
    const hdr=document.querySelector('header,nav');
    const hs=hdr?cs(hdr):null;
    const btn=[...document.querySelectorAll('a,button')].filter(e=>vis(e)&&cs(e).borderTopLeftRadius!=='0px'&&cs(e).backgroundColor!=='rgba(0, 0, 0, 0)')[0];
    // sticky header w/ blur
    let blur=null; for(const e of document.querySelectorAll('header,nav,header *,nav *')){const s=cs(e);if((s.backdropFilter&&s.backdropFilter!=='none')||(s.webkitBackdropFilter&&s.webkitBackdropFilter!=='none')){blur={tag:e.tagName,bf:s.backdropFilter,bg:s.backgroundColor,pos:s.position};break}}
    const minTouch=[...document.querySelectorAll('a,button')].filter(vis).map(e=>e.getBoundingClientRect()).filter(r=>r.height<44).length;
    const totalTouch=[...document.querySelectorAll('a,button')].filter(vis).length;
    return {title:document.title.slice(0,60),lang:document.documentElement.lang,bodyBg:cs(document.body).backgroundColor,htmlBg:cs(document.documentElement).backgroundColor,body:pick(document.body),h1:pick(h1),h2:pick(h2),p:pick(p),cpl,btn:pick(btn)&&{...pick(btn),radius:cs(btn).borderRadius,bg:cs(btn).backgroundColor,pad:cs(btn).padding},hdrH:hdr?Math.round(hdr.getBoundingClientRect().height):null,blur,sizes,colors,bgs,fonts,radius,shadow,trans,smallTargets:minTouch+'/'+totalTouch,scrollW:document.documentElement.scrollWidth,hasMetaDark:!!document.querySelector('meta[name=color-scheme]'),rootVars:(()=>{const s=cs(document.documentElement);return ['--bg','--fg'].length&&null})()};
   });
   out[name].url=url;
  }catch(e){out[name]={error:String(e).slice(0,150),url}}
  await ctx.close().catch(()=>{});
  fs.writeFileSync(process.argv[5],JSON.stringify(out,null,1));
 }
 await browser.close();process.exit(0);
 
})();
