#!/usr/bin/env python3
"""한국어 문구 기계 점검(번역투·상투어·광고투·어미 혼용). 표준 라이브러리만 사용.
사용: python ko_lint.py PATH [PATH ...] [--json] [--top N]
PATH: .html(태그 제거 후 본문 텍스트) / .json(모든 문자열 값) / .py(문자열 리터럴 안 한글) / 디렉터리(재귀).
출력: 규칙별 건수와 예시. 종료코드 0(보고용). 규칙은 studies/ko-voice.md 4장과 같다.
주의: 인용된 원문(평론 인용, 투고 규정 등)과 고유명사도 걸릴 수 있다. 수치는 '후보 수'로 읽는다."""
import sys, re, json, html, ast, collections
from pathlib import Path
RULES = [  # (id, 설명, 정규식)
 ('via', "번역투 '~를 통해'", r'[을를]\s?통해(서)?'),
 ('in_regard', "번역투 '~에 있어(서)'", r'에\s?있어(서|\s)'),
 ('about', "번역투 '~에 대해(서)/대한'", r'에\s?대(해|한|하여)(서)?'),
 ('by_means', "번역투 '~에 의해/의한'", r'에\s?의(해|한|하여)'),
 ('passive_do', "이중피동 '~되어지/되어진'", r'되어지|되어진'),
 ('making', "번역투 '~로 하여금/~을 가지다'", r'로\s?하여금|[을를]\s?가지(고|는|다)\s?(있|해)'),
 ('of_of', "'~의 ~의' 연쇄", r'\S+의\s\S+의\s'),
 ('can', "'~할 수 있습니다/있어요' 완곡", r'[가-힣]\s수\s?있(습니다|어요)'),
 ('cliche_various', "상투어 '다양한/다채로운'", r'다양한|다채로운|다양하게'),
 ('cliche_hype', "광고투(최고·완벽·놀라운·지금 바로·만나보세요)", r'최고의|완벽한|놀라운|지금\s?바로|만나\s?보세요|확인해\s?보세요|즐겨\s?보세요'),
 ('cliche_meaning', "상투어 '의미 있는/특별한/진정한'", r'의미\s?있는|특별한|진정한'),
 ('filler', "군더더기 '것 같다/~하는 것이다'", r'것\s?같(다|아요|습니다)|하는\s?것이다'),
 ('progressive', "번역투 진행형 '~하고 있다'", r'하고\s?있(다|어요|습니다)'),
 ('pron', "대명사 직역 '그것은/그녀는'", r'그것은|그녀(는|가|의)'),
 ('ending_haeyo', "해요체 어미(-요.)", r'[가-힣]요[.!?]'),
 ('ending_hamnida', "합니다체 어미(-니다.)", r'[가-힣]니다[.!?]'),
 ('ending_da', "평서체 어미(-다.)", r'[가-힣](?<!니)다[.!?]'),
]
CRE = [(i, d, re.compile(p)) for i, d, p in RULES]
def texts(p):
    s = p.suffix
    try: raw = p.read_text(encoding='utf-8')
    except Exception: return []
    if s == '.html':
        raw = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', raw); raw = html.unescape(re.sub(r'<[^>]+>', '\n', raw))
        return [t.strip() for t in raw.split('\n') if re.search('[가-힣]', t)]
    if s == '.json':
        out = []
        def w(x):
            if isinstance(x, str):
                if re.search('[가-힣]', x): out.append(x)
            elif isinstance(x, dict): [w(v) for v in x.values()]
            elif isinstance(x, list): [w(v) for v in x]
        try: w(json.loads(raw))
        except Exception: pass
        return out
    if s == '.py':
        try: tree = ast.parse(raw)
        except Exception: return []
        return [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str) and re.search('[가-힣]', n.value)]
    return []
def scan(paths):
    cnt = collections.Counter(); ex = collections.defaultdict(list); n = 0
    for a in paths:
        P = Path(a); files = [P] if P.is_file() else [f for f in P.rglob('*') if f.suffix in ('.html', '.json', '.py')]
        for f in files:
            for t in texts(f):
                n += 1
                for i, d, r in CRE:
                    for m in r.finditer(t):
                        cnt[i] += 1
                        if len(ex[i]) < 3: ex[i].append(t[max(0, m.start()-15):m.end()+15].replace('\n', ' '))
    e = {k: cnt[k] for k in ('ending_haeyo', 'ending_hamnida', 'ending_da')}; tot = sum(e.values()) or 1
    mix = round(100 * (tot - max(e.values())) / tot, 1)
    return {'strings': n, 'counts': {i: cnt[i] for i, _, _ in CRE}, 'ending_mix_pct': mix, 'examples': dict(ex),
            'issues_total': sum(v for k, v in cnt.items() if not k.startswith('ending_'))}
if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]; r = scan(args)
    if '--json' in sys.argv: print(json.dumps(r, ensure_ascii=False, indent=1)); sys.exit(0)
    print(f"문자열 {r['strings']}개, 금지어 후보 합계 {r['issues_total']}건, 어미 혼용률 {r['ending_mix_pct']}%")
    for i, d, _ in RULES:
        if r['counts'][i]: print(f"  {i:16s} {r['counts'][i]:5d}  {d}  예: {' | '.join(r['examples'][i][:2])}")
