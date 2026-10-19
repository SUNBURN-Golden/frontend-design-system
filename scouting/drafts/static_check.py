#!/usr/bin/env python3
"""Dependency-free static checks over a built dist/ (stdlib only).
Usage: python static_check.py DIST [--json]
Checks: CSP-hostile markup (style=, <style>, inline <script>, on*= handlers),
external URLs, <html lang>, single <h1>, <img alt>, viewport meta,
CSS: prefers-color-scheme / prefers-reduced-motion / keep-all / focus-visible,
raw hex colours outside :root, off-grid px spacing (not multiple of 4)."""
import re, sys, json
from pathlib import Path
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.f=[]; s.h1=0; s.lang=None; s.viewport=False; s.in_script=False; s.in_style=False
    def handle_starttag(s, tag, a):
        a=dict(a)
        if tag=='html': s.lang=a.get('lang')
        if tag=='h1': s.h1+=1
        if tag=='meta' and a.get('name')=='viewport': s.viewport=True
        if 'style' in a: s.f.append('inline-style-attr')
        if tag=='style': s.f.append('style-element')
        if tag=='script' and not a.get('src') and a.get('type') not in ('application/ld+json','application/json'): s.f.append('inline-script')
        if any(k.startswith('on') for k in a): s.f.append('inline-event-handler')
        if tag=='img' and 'alt' not in a: s.f.append('img-no-alt')
        for k in ('src','href','action'):
            v=a.get(k,'')
            if not re.match(r'https?://',v): continue
            loads = tag in ('script','img','iframe','source','video','audio') or (tag=='link' and a.get('rel','') in ('stylesheet','preload','modulepreload','icon','prefetch','preconnect'))
            if loads: s.f.append('external-resource:'+v.split('/')[2])
def main(dist, as_json=False):
    dist=Path(dist); res={'pages':0,'html':{},'css':{}}
    from collections import Counter
    c=Counter(); pages_bad=Counter()
    for p in dist.rglob('*.html'):
        res['pages']+=1; t=p.read_text(encoding='utf-8',errors='replace')
        q=P(); q.feed(t)
        for f in q.f: c[f]+=1
        if not q.lang: c['html-no-lang']+=1
        if q.h1!=1: c[f'h1-count-{q.h1}']+=1
        if not q.viewport: c['no-viewport-meta']+=1
    res['html']=dict(c)
    for p in dist.rglob('*.css'):
        t=p.read_text(encoding='utf-8',errors='replace'); r={}
        r['bytes']=len(t.encode())
        r['prefers-color-scheme-dark']= 'prefers-color-scheme' in t and 'dark' in t
        r['prefers-reduced-motion']= 'prefers-reduced-motion' in t
        r['keep-all']= 'keep-all' in t
        r['focus-visible']= ':focus-visible' in t
        r['text-wrap-balance|pretty']= bool(re.search(r'text-wrap:\s*(balance|pretty)',t))
        r['outline-none']=len(re.findall(r'outline:\s*(none|0)\b',t))
        # strip :root blocks
        noroot=re.sub(r':root\s*\{[^}]*\}','',t)
        noroot=re.sub(r'@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*:root\s*\{[^}]*\}\s*\}','',noroot)
        r['raw-hex-outside-root']=len(re.findall(r'#[0-9a-fA-F]{3,8}\b',noroot))
        px=[int(x) for x in re.findall(r'(?:margin|padding|gap)[a-z-]*:\s*([^;}]+)',noroot) for x in re.findall(r'(\d+)px',x)]
        r['px-spacing-values']=len(px); r['px-spacing-off-4grid']=sum(1 for x in px if x%4)
        res['css'][str(p.relative_to(dist))]=r
    print(json.dumps(res,ensure_ascii=False,indent=1))
if __name__=='__main__': main(sys.argv[1], '--json' in sys.argv)
