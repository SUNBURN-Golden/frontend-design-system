import json,glob,sys
d={}
for f in sorted(glob.glob('fo_*.json')):
    try:d.update(json.load(open(f)))
    except: pass
def card(h):
    cs=h.get('cards') or []
    if not cs: return 'cards0'
    rs=[c['ratio'] for c in cs if c.get('ratio')]
    tl=[c['titleLines'] for c in cs if c.get('titleLines')]
    lf=[c['textLeafCount'] for c in cs]
    return f"cards{h.get('cardCountInVp')} ratio~{sorted(rs)[len(rs)//2] if rs else None} titleLines~{sorted(tl)[len(tl)//2] if tl else None} leaf~{sorted(lf)[len(lf)//2]}"
for k,v in d.items():
    print('=====',k,v.get('articleUrl'))
    for key in ['home1440','home390']:
        h=v.get(key)
        if not h: print(' ',key,'-');continue
        if 'error' in h: print(' ',key,h['error']);continue
        L=h['largest'] or {}
        print(' ',key,f"words{h['words']} vpLinks{h['vpLinks']} nav{h['navLinks']} cta{h['ctaCount']}{h['ctas'][:3]} inputs{h['inputs']} largest{L.get('fs')}px/{L.get('len')}ch h1len{h['h1len']} {card(h)} pageH/vh={round(h['pageH']/h['vh'],1)} bg{h['bodyBg']}")
    for key in ['artDetail1440','artDetail390']:
        a=v.get(key)
        if a: print(' ',key,json.dumps({k:a.get(k) for k in ['fs','lh','ff','w','firstLineChars','korean','align','time','byline','progressBar','toc','h1']},ensure_ascii=False))
    for key in ['article1440']:
        a=v.get(key)
        if a and 'error' not in a: print('  art-first-screen',f"words{a['words']} links{a['vpLinks']} nav{a['navLinks']} cta{a['ctaCount']}")
