#!/usr/bin/env python3
"""첫 화면(스크롤 전) '깔끔함' 지표 측정. 조사용, 구현 코드 아님. 의존성: playwright(python) + 시스템 Chrome.
사용: python clean_measure.py urls.json out.json   (urls.json: {"이름":"URL"})
지표(390x844, 1440x900): words(공백 단어+한글은 어절), uniqueLinks(고유 href), ctas(채움 배경/테두리 있는 버튼형 a·button),
fontSizes(텍스트 글자크기 종류), textColors(텍스트 색 종류), accents(채도 높은 색상군 수: 텍스트·채움 hue 30도 버킷),
sectionGapMedian(인접 블록 간 세로 간격 중앙값 px), maxTextWidth(40자 이상 단락의 최대 폭 px), h1(px)."""
import sys, json, colorsys
from playwright.sync_api import sync_playwright
JS = r"""()=>{
const vh=innerHeight,vw=innerWidth,cs=e=>getComputedStyle(e);
const inView=r=>r.width>0&&r.height>0&&r.top<vh&&r.bottom>0&&r.left<vw&&r.right>0;
const vis=e=>{const s=cs(e);return s.visibility!=='hidden'&&s.display!=='none'&&+s.opacity>0.05&&inView(e.getBoundingClientRect())};
let words=0;const sizes=new Set(),colors=new Set(),sat=[];
const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
while(w.nextNode()){const n=w.currentNode,t=n.textContent.trim();if(!t)continue;const p=n.parentElement;if(!p||/SCRIPT|STYLE|NOSCRIPT/.test(p.tagName))continue;
 const rg=document.createRange();rg.selectNodeContents(n);if(!inView(rg.getBoundingClientRect())||!vis(p))continue;
 words+=t.split(/\s+/).filter(Boolean).length;const s=cs(p);sizes.add(Math.round(parseFloat(s.fontSize)));colors.add(s.color);sat.push(s.color);}
const act=[...document.querySelectorAll('a[href],button,[role=button],input[type=submit],input[type=search],input[type=text]')].filter(vis);
const links=new Set(act.filter(e=>e.tagName==='A').map(e=>e.getAttribute('href')));
const ctas=act.filter(e=>{if(!/^(A|BUTTON)$/.test(e.tagName))return false;const s=cs(e),r=e.getBoundingClientRect();const filled=s.backgroundColor!=='rgba(0, 0, 0, 0)'&&s.backgroundColor!==cs(document.body).backgroundColor;const bord=parseFloat(s.borderTopWidth)>0&&parseFloat(s.borderTopLeftRadius)>0;return (filled||bord)&&r.height>=28&&r.width<vw*0.9&&(e.innerText||'').trim().length>0&&(e.innerText||'').trim().length<30});
const fills=[...document.querySelectorAll('body *')].filter(vis).slice(0,3000).map(e=>{const r=e.getBoundingClientRect();return r.width*r.height<vw*vh*0.5&&r.width*r.height>200?cs(e).backgroundColor:null}).filter(Boolean);
const paras=[...document.querySelectorAll('p,li,dd')].filter(e=>vis(e)&&(e.innerText||'').trim().length>=40).map(e=>Math.round(e.getBoundingClientRect().width));
const blocks=[...document.querySelectorAll('main > *, main section, body > section, body > div > section, header + *, section, article')].filter(vis).map(e=>e.getBoundingClientRect()).sort((a,b)=>a.top-b.top);
const gaps=[];for(let i=1;i<blocks.length;i++){const g=blocks[i].top-blocks[i-1].bottom;if(g>0&&g<400)gaps.push(Math.round(g))}gaps.sort((a,b)=>a-b);
const h1=[...document.querySelectorAll('h1')].find(vis);
const inp=[...document.querySelectorAll('input[type=search],input[type=text],input:not([type])')].filter(vis).map(e=>Math.round(e.getBoundingClientRect().width));
return {title:document.title.slice(0,60),words,uniqueLinks:links.size,interactive:act.length,ctas:ctas.length,ctaTexts:ctas.slice(0,4).map(e=>e.innerText.trim().slice(0,20)),
fontSizes:[...sizes].sort((a,b)=>a-b),textColors:[...colors],fills:[...new Set(fills)].filter(c=>c!=='rgba(0, 0, 0, 0)'),sectionGapMedian:gaps.length?gaps[gaps.length>>1]:null,
maxTextWidth:paras.length?Math.max(...paras):null,h1:h1?{px:Math.round(parseFloat(cs(h1).fontSize)),text:h1.innerText.trim().slice(0,40)}:null,searchInputWidth:inp.length?Math.max(...inp):0,
scrollW:document.documentElement.scrollWidth,docH:document.documentElement.scrollHeight}}"""
def rgb(c):
    import re; v=[float(x) for x in re.findall(r'[\d.]+',c)]
    return v if len(v)>=3 and (len(v)<4 or v[3]>0.3) else None
def accents(cols):
    b=set()
    for c in cols:
        v=rgb(c)
        if not v: continue
        h,l,s=colorsys.rgb_to_hls(*(x/255 for x in v[:3]))
        if s>0.35 and 0.15<l<0.85: b.add(int(h*12)%12)
    return len(b)
if __name__=='__main__':
    urls=json.load(open(sys.argv[1])); out={}
    with sync_playwright() as pw:
        br=pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        for n,u in urls.items():
            for vw,vh in ((390,844),(1440,900)):
                ctx=br.new_context(viewport={'width':vw,'height':vh},locale='ko-KR',user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36')
                pg=ctx.new_page()
                try:
                    pg.goto(u,wait_until='domcontentloaded',timeout=30000); pg.wait_for_timeout(3000)
                    m=pg.evaluate(JS); m['accentHues']=accents(m['textColors']+m['fills']); m['nTextColors']=len(m['textColors']); m['nFontSizes']=len(m['fontSizes'])
                    del m['fills']
                except Exception as e: m={'error':str(e)[:120]}
                m['url']=u; out[f'{n}@{vw}']=m; ctx.close()
                print(n,vw,{k:m.get(k) for k in ('words','uniqueLinks','ctas','nFontSizes','accentHues','sectionGapMedian','maxTextWidth','error')},flush=True)
        br.close()
    json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
