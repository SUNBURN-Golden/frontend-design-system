#!/usr/bin/env python3
"""첫 화면 5초 테스트 반자동 점검. 렌더된 첫 화면(스크롤 전)을 측정하고 스크린샷을 남긴다.
사용: python first_screen_audit.py out_dir name=dist_dir [name=dist_dir ...] [--chrome /usr/bin/google-chrome]
측정: title/h1/리드 문장, 첫 화면 단어 수, 클릭 요소 수(고유 href 수), 내비 링크 수, CTA 후보 수·최대 CTA 면적 비율, 이미지/아이콘 수, 글자 크기 종류.
임계값(BUDGET)은 [짐작] 초기값. 실제 사용자 5초 테스트 결과로 보정할 것. 위반해도 종료코드는 예산 초과 개수(0이면 통과)."""
import sys, json, threading, http.server, socketserver, functools
from pathlib import Path
from playwright.sync_api import sync_playwright
BUDGET = {  # [짐작] 초기 예산 - 모바일 390x844 기준. 보정 필요.
 'h1_words_max': 12, 'h1_visible': True, 'lead_words_max': 30, 'words_above_fold_max': 80,
 'clickables_above_fold_max': 8, 'cta_candidates_range': (1, 2), 'font_sizes_max': 5, 'images_min': 1}
JS = """()=>{
 const vh=innerHeight, vw=innerWidth;
 const vis=e=>{const r=e.getBoundingClientRect();const s=getComputedStyle(e);return r.width>0&&r.height>0&&r.top<vh&&r.bottom>0&&r.left<vw&&s.visibility!=='hidden'&&s.display!=='none'};
 const area=e=>{const r=e.getBoundingClientRect();return Math.round(Math.max(0,Math.min(r.right,vw)-Math.max(r.left,0))*Math.max(0,Math.min(r.bottom,vh)-Math.max(r.top,0)))};
 const wc=t=>t.trim().split(/\\s+/).filter(Boolean).length;
 let words=0,sizes=new Set();
 const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
 while(w.nextNode()){const n=w.currentNode,t=n.textContent.trim();if(!t)continue;const p=n.parentElement;if(!p||['SCRIPT','STYLE','NOSCRIPT'].includes(p.tagName))continue;
  const rg=document.createRange();rg.selectNodeContents(n);const r=rg.getBoundingClientRect();if(r.width>0&&r.top<vh&&r.bottom>0){words+=wc(t);sizes.add(getComputedStyle(p).fontSize);}}
 const act=[...document.querySelectorAll('a[href],button,[role=button],input[type=submit]')].filter(vis);
 const hrefs=new Set(act.map(e=>e.getAttribute('href')||('#btn:'+(e.innerText||'').trim())));
 const navLinks=[...document.querySelectorAll('nav a[href],header a[href]')].filter(vis);
 const cta=act.filter(e=>/btn|cta|button|pin/i.test(e.className)||e.tagName==='BUTTON').filter(e=>!navLinks.includes(e)||/btn|cta/i.test(e.className));
 const ctaAreas=cta.map(area).sort((a,b)=>b-a);
 const h1=document.querySelector('h1'); const h1v=h1&&vis(h1)&&h1.getBoundingClientRect().bottom<=vh;
 let lead=''; if(h1){let n=h1.nextElementSibling;while(n&&!(n.tagName==='P'&&vis(n)))n=n.nextElementSibling;if(!n){const nx=h1.parentElement&&h1.parentElement.querySelector('p');n=nx&&vis(nx)?nx:null}lead=n?n.innerText.trim():''}
 const imgs=[...document.querySelectorAll('img,svg,picture,video')].filter(vis).length;
 return {title:document.title,h1:h1?h1.innerText.trim():'',h1Words:h1?wc(h1.innerText):0,h1VisibleAboveFold:!!h1v,leadWords:wc(lead),lead:lead.slice(0,80),
  wordsAboveFold:words,fontSizeKinds:sizes.size,clickablesAboveFold:act.length,uniqueTargetsAboveFold:hrefs.size,navLinksVisible:navLinks.length,
  ctaCandidates:cta.length,ctaTexts:cta.slice(0,4).map(e=>e.innerText.trim().slice(0,30)),largestCtaAreaPctOfViewport:ctaAreas.length?+(100*ctaAreas[0]/(vw*vh)).toFixed(1):0,
  imagesOrIconsAboveFold:imgs}}"""
def check(m):
    b = BUDGET; f = []
    if m['h1Words'] > b['h1_words_max']: f.append('h1 너무 김')
    if not m['h1VisibleAboveFold']: f.append('h1이 첫 화면에 없음')
    if m['leadWords'] == 0: f.append('h1 아래 한 줄 설명 없음')
    elif m['leadWords'] > b['lead_words_max']: f.append('설명 문장 김')
    if m['wordsAboveFold'] > b['words_above_fold_max']: f.append('첫 화면 단어 많음')
    if m['clickablesAboveFold'] > b['clickables_above_fold_max']: f.append('첫 화면 클릭 대상 많음')
    lo, hi = b['cta_candidates_range']
    if not lo <= m['ctaCandidates'] <= hi: f.append(f'CTA 후보 {m["ctaCandidates"]}개(권장 {lo}~{hi})')
    if m['fontSizeKinds'] > b['font_sizes_max']: f.append('글자 크기 종류 많음')
    if m['imagesOrIconsAboveFold'] < b['images_min']: f.append('이미지/아이콘 없음(텍스트 only)')
    return f
if __name__ == '__main__':
    args = [a for a in sys.argv[1:]]; chrome = '/usr/bin/google-chrome'
    if '--chrome' in args: i = args.index('--chrome'); chrome = args[i + 1]; del args[i:i + 2]
    out = Path(args[0]); out.mkdir(parents=True, exist_ok=True); sites = dict(x.split('=', 1) for x in args[1:])
    res = {}; over = 0
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=chrome, args=['--no-sandbox'])
        for n, root in sites.items():
            class H(http.server.SimpleHTTPRequestHandler):
                def log_message(self, *a): pass
            httpd = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(H, directory=root)); threading.Thread(target=httpd.serve_forever, daemon=True).start()
            port = httpd.server_address[1]
            for vw, vh in ((390, 844), (1440, 900)):
                pg = br.new_page(viewport={'width': vw, 'height': vh}); pg.goto(f'http://127.0.0.1:{port}/'); pg.wait_for_timeout(400)
                m = pg.evaluate(JS); m['violations'] = check(m) if vw == 390 else []
                pg.screenshot(path=str(out / f'{n}-{vw}-first-screen.png')); res[f'{n}@{vw}'] = m; over += len(m['violations']); pg.close()
            httpd.shutdown(); httpd.server_close()
        br.close()
    (out / 'first_screen.json').write_text(json.dumps(res, ensure_ascii=False, indent=1))
    for k, v in res.items(): print(k, json.dumps({x: v[x] for x in v if x not in ('lead',)}, ensure_ascii=False))
    sys.exit(min(over, 99))
