"""직관성/스캔성 지표(첫 화면 기준) - 렌더된 페이지에서 측정."""
import sys,json,threading,http.server,socketserver,functools
from playwright.sync_api import sync_playwright
JS="""()=>{
 const vh=innerHeight, vw=innerWidth;
 const vis=e=>{const r=e.getBoundingClientRect();const s=getComputedStyle(e);return r.width>0&&r.height>0&&r.top<vh&&r.bottom>0&&r.left<vw&&s.visibility!=='hidden'&&s.display!=='none'};
 // words in visible text nodes above the fold
 let words=0, sizes=new Set(), maxLine=0;
 const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
 while(w.nextNode()){const n=w.currentNode;const t=n.textContent.trim();if(!t)continue;const p=n.parentElement;if(!p||['SCRIPT','STYLE','NOSCRIPT'].includes(p.tagName))continue;
  const rg=document.createRange();rg.selectNodeContents(n);const r=rg.getBoundingClientRect();if(r.width>0&&r.top<vh&&r.bottom>0){words+=t.split(/\\s+/).length;sizes.add(getComputedStyle(p).fontSize);}}
 const act=[...document.querySelectorAll('a[href],button,input,select,textarea,[role=button]')].filter(vis);
 const ps=[...document.querySelectorAll('p,li')].filter(e=>e.innerText.length>0);
 const longestP=Math.max(0,...ps.map(e=>e.innerText.trim().split(/\\s+/).length));
 const h1=document.querySelector('h1');
 const small=act.filter(e=>{const r=e.getBoundingClientRect();return r.height<44||r.width<44}).length;
 const iconOnly=act.filter(e=>!e.innerText.trim()&&!e.getAttribute('aria-label')&&!e.getAttribute('title')&&e.tagName!=='INPUT').length;
 const imgs=[...document.querySelectorAll('img,svg')].filter(vis).length;
 return {wordsAboveFold:words,distinctFontSizesAboveFold:sizes.size,actionsAboveFold:act.length,smallTargets_lt44px:small,iconOnlyNoLabel:iconOnly,imagesAboveFold:imgs,h1Words:h1?h1.innerText.trim().split(/\\s+/).length:0,longestParagraphWords:longestP,totalWordsPage:document.body.innerText.trim().split(/\\s+/).length}}"""
# 사용: python scan_metrics.py name=dist [name=dist ...]
sites=dict(x.split('=',1) for x in sys.argv[1:])
out={}
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for i,(n,root) in enumerate(sites.items()):
        class H(http.server.SimpleHTTPRequestHandler):
            def log_message(self,*a): pass
        httpd=socketserver.TCPServer(('127.0.0.1',0),functools.partial(H,directory=root)); threading.Thread(target=httpd.serve_forever,daemon=True).start(); port=httpd.server_address[1]
        for vw,vh in ((390,844),(1440,900)):
            pg=b.new_page(viewport={'width':vw,'height':vh}); pg.goto(f'http://127.0.0.1:{port}/'); pg.wait_for_timeout(400)
            out[f'{n}@{vw}']=pg.evaluate(JS); pg.close()
        httpd.shutdown(); httpd.server_close()
    b.close()
for k,v in out.items(): print(k,json.dumps(v))
