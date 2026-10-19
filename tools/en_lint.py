#!/usr/bin/env python3
"""English copy check (cliches, hype, filler, hedging) — the ko-voice principles applied to English. stdlib only.
Usage: python en_lint.py PATH [PATH ...]   (.html text / .py string literals / dirs). Counts are candidates, not verdicts."""
import sys, re, html, ast, collections
from pathlib import Path
RULES = [
 ('hype', 'hype/superlatives', r'\b(best|ultimate|amazing|incredible|perfect|seamless|game[- ]chang\w*|world[- ]class|cutting[- ]edge|revolutionary|unlock|supercharge)\b'),
 ('cliche', 'cliches', r'\b(a wide (range|variety) of|various|diverse|robust|leverage|in order to|at the end of the day|journey|dive (in|into)|whether you\'re)\b'),
 ('filler', 'filler/intensifiers', r'\b(very|really|simply|just|actually|basically|truly|quite)\b'),
 ('hedge', 'stacked hedging (may/might/could)', r'\b(may|might|could) (possibly|potentially)\b|\bpotentially\b'),
 ('passive', 'passive "is/are/was/were + -ed by"', r'\b(is|are|was|were|been) \w+ed by\b'),
 ('cta_push', 'pushy CTA', r'\b(don\'t miss|act now|hurry|sign up now|join thousands)\b'),
 ('exclaim', 'exclamation marks', r'!'),
]
CRE=[(i,d,re.compile(p,re.I)) for i,d,p in RULES]
def texts(f):
    raw=f.read_text(encoding='utf-8',errors='ignore')
    if f.suffix=='.html':
        raw=re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>',' ',raw); return [t.strip() for t in html.unescape(re.sub(r'<[^>]+>','\n',raw)).split('\n') if re.search('[A-Za-z]{3}',t)]
    if f.suffix=='.py':
        try: return [n.value for n in ast.walk(ast.parse(raw)) if isinstance(n,ast.Constant) and isinstance(n.value,str) and ' ' in n.value]
        except Exception: return []
    return []
cnt=collections.Counter(); ex=collections.defaultdict(list); n=0
for a in sys.argv[1:]:
    P=Path(a)
    for f in ([P] if P.is_file() else [x for x in P.rglob('*') if x.suffix in ('.html','.py')]):
        for t in texts(f):
            n+=1
            for i,d,r in CRE:
                for m in r.finditer(t):
                    cnt[i]+=1
                    if len(ex[i])<2: ex[i].append(t[max(0,m.start()-25):m.end()+25].replace('\n',' '))
print(f"strings {n}, candidates {sum(cnt.values())}")
for i,d,_ in RULES:
    if cnt[i]: print(f"  {i:9s} {cnt[i]:4d}  {d}  e.g. {' | '.join(ex[i])}")
