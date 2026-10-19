#!/usr/bin/env python3
"""axe-core를 Playwright(Python)로 dist/ 정적 사이트에 돌린다. 사이트 레포에 의존성 추가 없음(개발 환경 전용).
사용: python axe_audit.py DIST_DIR [--axe path/to/axe.min.js] [--chrome /usr/bin/google-chrome]
준비(임시 폴더): npm i --prefix /tmp/axe axe-core   (의존성 0개, MPL-2.0, 배포물에 포함되지 않음)
출력: 규칙별 위반 수 (라이트/다크 x 390/1440). 위반이 있으면 종료코드 1."""
import sys, json, argparse, threading, http.server, socketserver, functools, collections
from pathlib import Path
from playwright.sync_api import sync_playwright
ap = argparse.ArgumentParser(); ap.add_argument('dist'); ap.add_argument('--axe', default='/tmp/axe/node_modules/axe-core/axe.min.js')
ap.add_argument('--chrome', default='/usr/bin/google-chrome'); ap.add_argument('--max-pages', type=int, default=8); ap.add_argument('--port', type=int, default=0)
a = ap.parse_args(); root = Path(a.dist); AXE = Path(a.axe).read_text()
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x): pass
httpd = socketserver.TCPServer(('127.0.0.1', a.port), functools.partial(H, directory=str(root))); threading.Thread(target=httpd.serve_forever, daemon=True).start(); a.port = httpd.server_address[1]
pages = sorted(root.rglob('index.html')); pages.sort(key=lambda p: len(p.relative_to(root).parts))
urls = [('/' + str(p.relative_to(root).parent) + '/').replace('/./', '/') for p in pages][:a.max_pages]
agg = collections.Counter(); ex = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=a.chrome, args=['--no-sandbox'])
    for scheme in ('light', 'dark'):
        for vw, vh in ((390, 844), (1440, 900)):
            pg = b.new_context(viewport={'width': vw, 'height': vh}, color_scheme=scheme).new_page()
            for u in urls:
                pg.goto(f'http://127.0.0.1:{a.port}{u}'); pg.add_script_tag(content=AXE)
                r = pg.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}})")
                for v in r['violations']:
                    k = (v['id'], v['impact'], scheme, vw); agg[k] += len(v['nodes']); ex.setdefault(k, (u, v['nodes'][0]['html'][:100]))
                if pg.evaluate('document.documentElement.scrollWidth>innerWidth'):
                    k = ('horizontal-overflow', '-', scheme, vw); agg[k] += 1; ex.setdefault(k, (u, ''))
    b.close()
for k, n in sorted(agg.items()): print(*k, 'nodes=%d' % n, ex[k])
print('violation groups:', len(agg)); sys.exit(1 if agg else 0)
