"""Load pages in real Chromium with the site's CSP header and collect violations."""
import sys,re,threading,http.server,socketserver,functools
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(sys.argv[1]); port=int(sys.argv[2])
csp=re.search(r'Content-Security-Policy:\s*(.+)',(root/'_headers').read_text()).group(1).strip()
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Content-Security-Policy',csp); super().end_headers()
    def log_message(self,*a): pass
httpd=socketserver.TCPServer(('127.0.0.1',port),functools.partial(H,directory=str(root))); threading.Thread(target=httpd.serve_forever,daemon=True).start()
pages=sorted(root.rglob('index.html')); urls=['/'+str(p.relative_to(root).parent).replace('.','')+'/' for p in pages]
urls=[u.replace('//','/') for u in urls]
msgs={}
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox']); pg=b.new_page()
    cur=['']
    pg.on('console',lambda m: msgs.setdefault(m.text[:160],[]).append(cur[0]) if m.type in('error','warning') else None)
    pg.on('pageerror',lambda e: msgs.setdefault('PAGEERROR '+str(e)[:140],[]).append(cur[0]))
    for u in urls:
        cur[0]=u; pg.goto(f'http://127.0.0.1:{port}{u}'); 
        if 'filter' in pg.content() or True:
            pass
    b.close()
print('pages',len(urls)); print('CSP:',csp[:80],'...')
for k,v in msgs.items(): print(len(v),'x',k,'e.g.',v[0])
if not msgs: print('no console errors/warnings')
