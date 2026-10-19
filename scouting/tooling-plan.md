# 자동 검증 도구 최소 세트와 도입 순서 (Goal Lit, HANSET, 피치보드)

목적: 같은 지적이 두 번 나오지 않도록 **린트/스크립트로 구조화**하고, 준태님 기준(11:59)인 **UX 흐름 단순화 = 첫 5초 안에 무슨 사이트인지, 누를 것이 보임**을 자동/반자동으로 점검합니다.
라벨: `[측정함]` 이번에 실제로 돌려 본 것 / `[문서근거]` / `[추정]` / `[짐작]`(임계값 등 보정이 필요한 초기값).
이 문서는 계획이며 사이트 코드는 수정하지 않았습니다. `scouting/drafts/`의 스크립트는 **파일럿으로 실제 실행해 본 초안**입니다(사이트 레포에는 아직 넣지 않음).

## 1. 설계 원칙

1. **사이트 레포에는 의존성을 넣지 않는다.** 모든 도구는 이 레포(`frontend-design-system`)의 `scouting/drafts/`(나중에 `tools/`로 이동)와 임시 폴더(`/tmp/axe`, `/tmp/uxcheck`)에서만 돌고, 사이트의 `dist/`만 읽습니다. 배포물·CSP·"의존성 추가 금지" 규칙과 충돌이 없습니다.
2. **의존성 0 단계 먼저.** 파이썬 표준 라이브러리만으로 되는 정적 검사부터(즉시 도입), 그다음 브라우저 측정, 마지막에 Node 도구.
3. **브라우저는 시스템 Chrome 사용.** 박스의 pwvenv Playwright(1.64.0)는 번들 Chromium 1248이 없어 기본 실행이 실패했고, `executable_path=/usr/bin/google-chrome`로 해결했습니다. 브라우저 대용량 다운로드 금지 `[측정함]`.
4. **정적 검사 + 실제 브라우저 검사 둘 다.** HANSET의 인라인 `onsubmit`은 로드 시 CSP 에러가 없고(103/43페이지 로드 에러 0), Enter를 눌러야 위반이 나옵니다. 정적 스캔이 잡고, 런타임은 동작을 확인합니다 `[측정함]`.
5. **임계값은 처음엔 경고, 보정 후 실패로.** 5초 테스트 예산은 `[짐작]`이므로 먼저 보고용으로 돌리고, 준태님·실사용자 확인 후 PR 차단 기준으로 올립니다.

## 2. 최소 도구 세트 (이번에 모두 실행해 봄)

| 층 | 도구 | 설치 | 사이트당 소요(측정) | 무엇을 잡나 |
|---|---|---|---|---|
| L0 | `static_check.py` (자체, stdlib) | 없음 | 1초 미만 | 인라인 style/script/이벤트 핸들러, 외부 리소스, `lang`/`h1`/viewport, 다크모드·reduced-motion·keep-all·focus-visible 존재 여부, `:root` 밖 원색 hex, 4px 격자 위반 |
| L1 | `axe_audit.py` + axe-core 4.14.0 | `npm i --prefix /tmp/axe axe-core`(의존성 0개) | 32회 실행 15~34초 | 대비, 헤딩 순서, 랜드마크, iframe 제목, 스크롤 영역 포커스 등 WCAG 위반, 가로 오버플로 |
| L1 | `first_screen_audit.py` (자체, Playwright) | pwvenv 사용 | 약 5초(3사이트) | **첫 화면 5초 테스트 지표**(§3), 스크린샷 저장 |
| L1 | `scan_metrics.py` (자체) | 〃 | 약 2초 | 첫 화면 단어 수, 글자 크기 종류, 44px 미만 터치 요소, 아이콘 단독 버튼 |
| L1 | `csp_runtime.py` (자체) | 〃 | 6초(103+43페이지) | 사이트 `_headers`의 CSP를 붙여 로드 시 위반 수집 |
| L2 | stylelint 17.16 + `stylelint-declaration-strict-value` | `npm i --prefix /tmp/stylelint stylelint stylelint-declaration-strict-value` (Node >=20.19) | 약 1~2초 | 색 하드코딩, `!important`, `outline:none`, `transition:all` |
| L3(선택) | Lighthouse 12.x | `npm i --prefix /tmp/lh lighthouse`(Node 20에서는 12.8.2가 설치됨, 13.x는 Node >=22.19 필요) | 모바일·데스크톱 각 수십 초 | 성능, 콘솔 에러, 링크 텍스트. noindex 사이트는 SEO 카테고리 제외 |
| L3(선택) | `@google/design.md` 0.4.0 lint | `npm i --prefix /tmp/dmd @google/design.md` | 1초 | `DESIGN.md` 토큰의 컴포넌트 대비(WCAG), 깨진 참조, 미사용 토큰. alpha 스펙, 투명 배경 오탐 있음 |

HTML 린터(`html-validate`), 링크 검사(`linkinator`, `lychee`)는 후순위로 두었고 **파일럿하지 않았습니다**.

## 3. 첫 화면 5초 테스트: 자동/반자동 점검

### 3-1. 자동 측정 (`drafts/first_screen_audit.py`)
390x844(모바일, 판정 기준)와 1440x900(데스크톱, 참고)에서 스크롤 전 화면을 렌더해 아래를 측정하고 스크린샷을 `first-screen.png`로 남깁니다.

| 지표 | 5초 테스트에서의 의미 | 초기 예산 `[짐작]` |
|---|---|---|
| `title` / `h1` / 리드 문장 | "무슨 사이트인지"가 h1과 한 줄 설명에 있는가 | h1 ≤ 12단어, 첫 화면에 보임, 리드 1~30단어 |
| 첫 화면 단어 수 | 읽어야 하는 글 양 | ≤ 80 |
| 첫 화면 클릭 요소 수, 고유 대상 수 | 선택지 과다 | ≤ 8 |
| 내비 링크 수 | 정보구조 복잡도 | 참고용(우리 3사이트 모두 8) |
| CTA 후보 수, 가장 큰 CTA의 면적 비율 | "누르고 싶은 것"이 하나로 모이는가 | 1~2개 |
| 이미지/아이콘 수 | 글만으로 이해시키는지 | ≥ 1 |
| 글자 크기 종류 | 위계 단순성 | ≤ 5 |

한계 `[측정함/추정]`: CTA 후보는 **클래스명(`btn|cta|button|pin`)과 `<button>` 기반 근사**라서 사이트 마크업이 다르면 0으로 나올 수 있습니다(Goal Lit이 0으로 나옴, 스크린샷에서도 주요 행동 버튼이 뚜렷하지 않아 실제 문제와 일치). 사이트별로 CTA에 `data-cta` 속성을 붙이면 정확해지지만 이는 구현 단계 결정입니다.

### 3-2. 현재 3사이트 측정 결과 (390px, 2026-10-19)
| 사이트 | h1 | 리드 단어 | 첫 화면 단어 | 클릭 요소/고유 대상 | CTA 후보 | 글자 크기 종류 | 이미지·아이콘 | 예산 위반 |
|---|---|---|---|---|---|---|---|---|
| Goal Lit | "작품은 이렇게 읽혔다 — 한국 문학·웹툰·웹소설 평론" 7단어 | 13 | 111 | 10 / 10 | 0 | 10 | 0 | 단어, 클릭 수, CTA 0, 글자 종류, 이미지 없음 |
| 피치보드 | "Where to pitch book reviews and cultural criticism." 8단어 | 28 | 99 | 14 / 10 | 4 | 10 | 0 | 단어, 클릭 수, CTA 4, 글자 종류, 이미지 없음 |
| HANSET | "하이록스 서울 (시즌 26/27)" 4단어 | 19 | 104 | 14 / 10 | 3 | 12 | 0 | 단어, 클릭 수, CTA 3, 글자 종류, 이미지 없음 |

수치 외에 **스크린샷으로 확인한 것**(`scouting/data/first-screen/*.png`) `[측정함: 육안]`:
- Goal Lit: 노란 프리뷰 안내 줄, 헤더, 내비 5개(모바일에서 가로 스크롤), 라벨(`PREVIEW · 평론 웹진`), h1, 설명, 오늘의 평론 카드 순서. h1이 사이트 성격을 말하는 점은 좋지만 **눌러야 할 주 행동이 없음**. 라벨의 대비 2.73:1 위반도 이 화면에 있음.
- HANSET: 주 CTA 2개 모두 뚜렷함(좋음). 다만 **h1은 사이트가 아니라 이벤트(`하이록스 서울`)를 말하고**, `Drop-in & Sauna Finder`가 헤더 버튼과 하단 고정 버튼에 중복 노출.
- 피치보드: 스크린샷은 찍었으나 본 보고서에서는 수치 중심으로만 판단(육안 비교는 `data/first-screen/pitch-390-first-screen.png`).

### 3-3. 반자동 체크리스트 (스크린샷을 사람/에이전트가 5초 보고 답한다)
스크립트가 못 재는 부분입니다. `first-screen.png`(390)를 5초만 보고 아래를 **글로 한 줄씩** 답하고, 정답과 다르면 실패로 기록합니다.

1. 이 사이트는 무엇인가? (한 문장) → 사이트가 의도한 한 문장과 일치?
2. 누구를 위한 것인가?
3. 가장 먼저 누르고 싶은 것은? → 의도한 주 행동과 일치?
4. 같은 대상이 두 번 이상 보이는가? (중복 CTA)
5. 읽지 않고도 구역이 구분되는가? (제목, 아이콘, 색 면으로)
6. 비어 있어도 되는 줄(안내문, 라벨, 눈썹 문구)이 있는가? 지우면 이해가 줄어드는가?
7. 모바일에서 주 행동이 엄지 영역에 있고 44px 이상인가?
8. 정보 확인용 숫자·날짜·상태가 글이 아니라 배지/숫자로 한눈에 보이는가?

기록 형식: `scouting/data/first-screen/<사이트>-<PR>.md`에 질문 8개 답과 스크린샷 경로. 가능하면 **서로 다른 에이전트/사람 3명**이 답한 뒤 일치율을 봅니다 `[짐작: 일치율 기준은 보정 필요]`.

### 3-4. 실사용자 5초 테스트 (초기 1회, 보정용)
- 준태님 또는 가족/지인 5명에게 첫 화면 스크린샷 1장만 5초 보여주고 3-3의 1~3번을 묻는다. 정답률이 낮은 사이트를 우선 개선하고, 이 결과로 3-1의 예산을 보정한다.
- GitHub와 Hugging Face에서 5초 테스트·정보구조(트리 테스트)·카드 소팅용 쓸 만한 오픈소스/데이터는 찾지 못했습니다(검색 결과가 무관한 저장소뿐, HF 0건, 2026-10-19 `[측정함]`). 그래서 자체 스크립트 + 사람 확인 조합을 권장합니다.

## 4. 도입 순서

| 단계 | 내용 | 완료 기준 | 이유 |
|---|---|---|---|
| 1 | L0 `static_check.py`를 각 사이트 `tests/`(또는 빌드 후 검사)에 호출 연결 | CSP 위반 마크업 0, `lang`/`h1`/viewport 누락 0 | 의존성 0, 즉시 효과. HANSET `onsubmit`과 `google1cc…html` 예외는 먼저 허용 목록으로 처리 |
| 2 | L1 `run_all.sh`(axe + 첫 화면 + 스크린샷)를 PR 전에 수동 실행하고 결과를 PR 본문에 첨부 | 모든 UI PR에 5초 테스트 표와 스크린샷 | 사용자 기준(첫 5초)을 PR마다 증거로 남김 |
| 3 | 사이트별 `DESIGN.md`(또는 `:root` 토큰) 정리 + stylelint 색 하드코딩 금지 | 하드코딩 경고 0(Goal Lit 29, HANSET 17, 피치보드 15에서 감소) | 토큰 강제로 글자 크기·색 종류 축소를 강제 |
| 4 | axe 위반 수정 후 axe를 **실패 기준**으로 승격 | critical/serious 0 | 현재 실제 위반: Goal Lit 대비 2.73:1, 피치보드 iframe 제목·스크롤 영역 |
| 5 | 5초 테스트 예산 보정(3-4) 후 경고→실패로 | 사이트별 예산 확정 | `[짐작]` 값을 실측 기반으로 교체 |
| 6 | 다크모드 도입 후 `static_check.py`의 `prefers-color-scheme` 검사와 axe 다크 실행을 필수화 | 3사이트 다크 axe 위반 0 | 현재 세 사이트 모두 다크모드 없음 |
| 7(선택) | Lighthouse, `design.md lint`, 링크 검사 | 점수가 아니라 실패 항목만 | 후순위 |

## 5. 실행 명령 초안

공통 준비(임시 폴더, 전역 설치 없음):
```bash
npm i --prefix /tmp/axe axe-core                                   # 의존성 0
npm i --prefix /tmp/stylelint stylelint stylelint-declaration-strict-value
export PY=/workspace/pwvenv/bin/python AXE=/tmp/axe/node_modules/axe-core/axe.min.js \
       STYLELINT=/tmp/stylelint/node_modules/.bin/stylelint CHROME=/usr/bin/google-chrome
```

사이트별(빌드 명령은 각 운영 봇이 알려 준 방식):
```bash
# Goal Lit
cd goal-lit-site && /workspace/lit-venv/bin/python site/build_site.py
scouting/drafts/run_all.sh goal-lit site/dist site/static/css/site.css

# HANSET (반드시 --release, 레포 밖 임시 출력으로)
cd hanset-site/site && .venv/bin/python build_site.py --release --out /tmp/hanset-dist
scouting/drafts/run_all.sh hanset /tmp/hanset-dist site/static/css/site.css

# 피치보드 (python3 build.py, 의존성 없음)
cd pitchboard-site && python3 build.py
scouting/drafts/run_all.sh pitchboard dist static/style.css
```
> 주의: HANSET 빌드는 이번에 임시 폴더 복사본에서 `--out`으로 실행했고 레포를 수정하지 않았습니다. 각 사이트의 CSS 경로는 파일럿에서 확인한 위치(Goal Lit `site/static/css/site.css`, HANSET `site/static/css/site.css`로 추정 `[추정]`, 피치보드 `static/style.css`)이며 실제 실행 전 확인하세요.

개별 실행:
```bash
python3 scouting/drafts/static_check.py dist                       # L0
$PY scouting/drafts/axe_audit.py dist --axe $AXE --chrome $CHROME  # L1
$PY scouting/drafts/first_screen_audit.py out/first-screen name=dist --chrome $CHROME
$PY scouting/drafts/scan_metrics.py name=dist
$PY scouting/drafts/csp_runtime.py dist 8801                        # dist/_headers 필요(피치보드는 없음)
$STYLELINT --config scouting/drafts/stylelint.config.mjs --config-basedir /tmp/stylelint site.css
```

## 6. 교훈 → 구조화 매핑 (frontend-lesson-to-structure용)

| 이번에 발견한 것 | 구조화 규칙(실패하게 만들 곳) |
|---|---|
| 인라인 핸들러가 CSP에 막힘(HANSET `/finder/` Enter) | `static_check.py`의 `inline-event-handler`를 빌드 후 실패로 |
| 라벨 대비 2.73:1(Goal Lit) | axe `color-contrast`를 실패로, `design.md lint`로 토큰 쌍 사전 검증 |
| 첫 화면이 글 위주, 주 행동 불명확(Goal Lit) | `first_screen_audit.py` 예산: CTA 1~2, 단어 ≤ 80 |
| h1이 사이트 정체를 말하지 않음(HANSET) | 3-3 체크리스트 1번, h1+리드에 사이트 한 문장 포함 규칙 |
| 같은 CTA 중복(HANSET) | `uniqueTargetsAboveFold`와 `clickablesAboveFold` 차이 표시(향후: 동일 href 중복 경고 추가) |
| 원색 hex 직접 사용 | stylelint `declaration-strict-value` |
| 다크모드 없음 | `static_check.py`의 `prefers-color-scheme-dark` 필수화(도입 후) |
| OFL 예약 글꼴명(`Pretendard`) 서브셋 | 빌드 시 woff2 name 테이블이 예약명이면 경고하는 검사 추가(§E, 구현 후보) |

## 7. 한계와 미검증

- 임계값은 `[짐작]`. 실제 5초 테스트 결과로 보정 필요.
- axe 등 자동 도구는 WCAG 문제 일부만 잡습니다. 스크린샷 육안 확인 병행이 필요합니다.
- 시각 회귀(스크린샷 diff)는 이번에 구현하지 않았습니다. Playwright Python의 내장 스냅샷 비교 지원 여부는 확인하지 못했고, Pillow `ImageChops` 기반 자체 비교가 현실적입니다.
- HANSET은 레포 main을 빌드한 결과이고 프로덕션(Cloudflare 최신 배포)과 같다는 확인은 하지 않았습니다.
- 피치보드에는 `_headers`가 없어 CSP 런타임 검사 불가(beehiiv 외부 스크립트가 의도된 요구사항).
- impeccable, html-validate, vnu, linkinator, lychee, pa11y는 실행하지 않았습니다.
