# GitHub 자료 스카우팅 (2026-10-19, 준태님 지시 11:40 + 11:54 추가 기준)

탐색과 평가만 했고 사이트 코드는 수정하지 않았습니다. 구현은 Devin swe-2 전용입니다.

**라벨**: `[측정함]` 직접 잰 수치 / `[문서근거]` 공식 문서·README·라이선스 원문 / `[추정]` 근거로 추론 / `[짐작]` 근거 약함, 검증 필요.
**수치 출처**: stars, push일, 라이선스, archived는 모두 `gh api repos/<owner>/<repo>` (2026-10-19 11:4x~11:5x KST), 패키지 크기·라이선스·engines는 `npm view` (같은 날). 별 수는 GitHub가 돌려준 값 그대로입니다.

**최우선 기준 (준태님 11:54)**: 설명 없이 바로 이해되는 직관적·소비자 친화·최대한 단순한 UI, 글을 많이 읽지 않아도 한눈에 파악. 그래서 판정표에 `직관성 기여`(높음/중간/낮음/없음) 열을 두고 이 기준에 기여하는 자료에 가중치를 줬습니다.

**직관성 기여 열의 해석 (준태님 정정 11:59)**: 핵심은 화면 꾸밈이 아니라 **UX 흐름 단순화**, 즉 첫 5초 안에 (1) 무슨 사이트인지 (2) 누르고 싶은 것이 무엇인지가 보이는 것입니다. 그래서 `직관성 기여`는 `첫인상 / 정보구조(내비) / 흐름 단순화(클릭 대상 수, 선택지 수)를 검증하게 해 주는가`로 평가했고, 색·그림자 같은 장식 자료는 높게 주지 않았습니다. 이 관점의 검증 방법(5초 테스트 자동/반자동)은 `tooling-plan.md` 3장에 있습니다.

**우리 제약**: 프레임워크 없는 정적 사이트, 사이트 배포물에 의존성 추가 금지, CSP `default-src 'self'`(외부 CDN·폰트·스크립트 금지, 인라인 style/script 금지), 트래커 금지, 한국어 `keep-all`, 다크모드, WCAG AA, 서버 비용 없음.

---

## 0. 먼저 측정한 우리 사이트 현황 (파일럿)

후보를 평가하는 기준점으로, 후보 도구를 실제로 우리 빌드 결과물에 돌려 봤습니다. 대상은 Goal Lit(`/workspace/lit-hub/site/dist`, 104페이지), 피치보드(`/workspace/pitchboard-site/dist`, 101페이지), HANSET(레포 `main`을 임시 폴더에 `--release`로 빌드, 45페이지). 모두 읽기 전용으로 복사본에서 돌렸고 사이트 코드는 건드리지 않았습니다. 프로덕션과 다를 수 있습니다(`[추정]`: Goal Lit/피치보드는 현재 로컬 원본 기준, HANSET은 레포 main 기준).

| 측정 항목 | Goal Lit | 피치보드 | HANSET |
|---|---|---|---|
| 다크모드 CSS(`prefers-color-scheme`) | 없음 `[측정함]` | 없음 | 없음 |
| 라이트/다크 에뮬레이션 axe 결과 | 두 모드 동일 → 다크모드 미구현 `[측정함]` | 동일 | 동일 |
| axe 위반(8페이지 x 라이트/다크 x 390/1440) | color-contrast, heading-order, region | frame-title, heading-order, scrollable-region-focusable | heading-order, region |
| 실제 대비 위반 | `.eyebrow` 글자 #5b3fb5 on 배경 #a78bfa = **2.73:1**(기준 4.5:1) `[측정함]` | - | - |
| Lighthouse(모바일) 성능/접근성/권장사항 | 99 / 92 / 100 | 100 / 96 / 75 | 99 / 100 / 100 |
| 첫 화면 단어 수(390px / 1440px) | 111 / 234 | 99 / 148 | 104 / 118 |
| 첫 화면 서로 다른 글자 크기 종류 | 10 / 13 | 10 / 11 | 12 / 14 |
| 첫 화면 클릭 가능한 요소 수 | 10 / 13 | 15 / 17 | 14 / 20 |
| 첫 화면 이미지·아이콘 수 | 0 / 0 | 0 / 0 | 0 / 0 |
| 44px 미만 터치 요소(첫 화면, 인라인 링크 포함이라 근사) | 9 / 11 | 15 / 17 | 11 / 11 |
| 원색 hex가 `:root` 밖 CSS에 직접 쓰인 곳 | 54(정규식) / stylelint 29건 | 25 | 39 / stylelint 17건 |
| `!important` | 2 | 0 | 2 |
| 4px 격자에서 벗어난 padding/margin/gap px 값 | 96 / 153 | 측정 불가(px 값 0, 다른 단위) | 104 / 158 |
| HTML의 CSP 위반 마크업 | 0 | 외부 스크립트(beehiiv, 의도된 것, CSP 헤더 없음) + 인라인 핸들러 1 | 인라인 `onsubmit` 1, `<html lang>`·h1·viewport 없는 페이지 1(`google1cc…html` 인증 파일) |

핵심 발견 (직관성 관점 포함):
1. **첫 화면이 글 위주입니다.** 첫 화면 단어 100~230개, 글자 크기 10~14종, 이미지/아이콘 0개 `[측정함]`. 우리 `apple-style-ui-audit`의 "화면당 크기 3~4종" 기준과 크게 차이납니다. 직관성 목표에는 글자 줄이기, 위계 줄이기, 아이콘·라벨 패턴 도입이 필요합니다.
1-1. **첫 5초 점검 결과(`first_screen_audit.py`, 390px, 스크린샷 육안 확인 포함)** `[측정함]`:
   - Goal Lit: h1이 사이트 성격을 말함(좋음). 하지만 CTA 후보 0개(버튼형 주요 행동 없음, 클래스명 기반 근사), 상단에 노란 프리뷰 안내 줄+헤더+내비 8개+라벨+h1+설명+카드 순서라 "누를 것"이 분명치 않음. 가장 눈에 띄는 버튼은 검은 `편집 원칙`(독자 목적이 아님).
   - HANSET: CTA 2개(`레이스 위크 가이드`, `드롭인 박스 찾기`)는 좋으나 **h1이 `하이록스 서울 (시즌 26/27)`이라 사이트 정체(웰니스 매거진)는 h1이 아니라 title에만 있음**. `Drop-in & Sauna Finder`가 헤더 버튼과 하단 고정 버튼으로 **같은 대상이 2번** 노출.
   - 피치보드: h1이 목적을 설명(좋음), 첫 화면 CTA 후보 4개, 클릭 대상 14개로 선택지가 많음.
   - 공통: 첫 화면 이미지·아이콘 0개, 글자 크기 10~12종, 단어 99~111개(390px).
2. **HANSET `/finder/` 실제 버그**: 검색창에서 Enter를 누르면 인라인 `onsubmit="return false"`가 CSP(`script-src 'self'`)에 막히고 폼 전송도 `form-action 'none'`으로 막힙니다. 콘솔 에러 2건을 재현했습니다 `[측정함]`. 페이지 로드만으로는 안 잡히고 정적 스캔으로만 잡힙니다. 그래서 정적 검사와 실제 브라우저 검사를 둘 다 둬야 합니다.
3. **Goal Lit 대비 위반 1건은 실제입니다**(2.73:1). 린트가 있었다면 막혔을 항목입니다.
4. **다크모드는 세 사이트 모두 없음.**
5. 피치보드 Lighthouse 권장사항 75는 beehiiv 서드파티 쿠키·콘솔 에러 때문입니다(샌드박스 네트워크 영향 가능, `[추정]`). Goal Lit SEO 54는 전 페이지 noindex 때문에 정상입니다(noindex 사이트는 SEO 카테고리를 빼고 돌릴 것).

---

## A. 디자인 시스템 / 토큰 / CSS 레퍼런스

| 후보 | 용도 | 라이선스 | 최근 활동 | 크기/의존성 | 우리 제약 적합성 | 적용 방법 | 위험 | 직관성 기여 | 판정 |
|---|---|---|---|---|---|---|---|---|---|
| **Radix Colors** (`radix-ui/colors`, 1707★) | 12단계 접근 가능 색 스케일, 라이트/다크 쌍. 단계별 용도 고정(1~2 배경, 3~5 컴포넌트, 6~8 테두리, 9~10 면색, 11~12 글자) | MIT `[측정함]` | push 2025-12-17, npm 3.0.0 2025-12-24 `[측정함]` | 순수 CSS 값, npm 620KB unpacked. 배포물에는 필요한 값만 복사 | 적합. 값만 복사하면 의존성 0, 외부 로드 없음, 다크 쌍이 이미 있음 | 우리 보라 계열(Violet/Iris) 한 스케일과 중립(Slate/Mauve) 스케일의 라이트·다크 값만 `:root` 토큰으로 복사, MIT 고지 한 줄 포함 | 11·12단계는 APCA 기준 보장이지 WCAG 2 4.5:1 보장이 아님 `[문서근거]` → 조합마다 대비 검사 필수. 우리 브랜드 보라(#A78BFA) 대신 쓸지 별도 결정 | 중간(역할이 고정된 토큰이라 위계가 일관됨. 시각적 일관성에 기여) | **즉시 적용(값만)** |
| **Open Props** (`argyleink/open-props`, 5548★) | CSS 변수 세트(색, 그림자, 이징, 크기, 서체 등) | MIT | GH push 2026-10-11, npm 1.7.23 2026-01-31(GH 릴리스 태그 v1.6.0 2023-09, 태그 방식이 낡음) `[측정함]` | npm 1.29MB unpacked/330파일. 개별 CSS 파일만 복사하는 방식이 가능 `[추정]` | CSP 호환(순수 CSS, 자체 호스팅). 단 패키지 통째 도입은 불필요 | 이징·그림자 값만 참고. `:where()` 스코프 변형(`gen:nowhere`)이 있음 | 기본값이 Apple식이 아님(색 팔레트가 크고 선택지가 많음 → 오히려 선택지 증가). 이미 토큰이 있는 사이트에 중복 | 낮음 | **참고만(값)** |
| **Pico CSS** (`picocss/pico`, 16843★) | 시맨틱 HTML용 미니멀 프레임워크 | MIT | **archived: true**, README에 "저장소 아카이브, 새 릴리스 없음, 프로젝트 유지 종료" 명시 `[측정함][문서근거]` | 10MB repo | 구조 변경 필요 | - | 유지 종료, 우리는 이미 자체 CSS 보유 | 낮음 | **사용 금지(부적합)** → rejected.md |
| **MVP.css** (`andybrewer/mvp`, 5129★) | 클래스 없는 시맨틱 CSS | MIT | 릴리스 v1.18 2026-09-14 `[측정함]` | 순수 CSS | 가능하나 우리 사이트에 이미 컴포넌트 CSS 존재 | 참고 | 전면 교체 부담 | 낮음 | 참고만 |
| **Simple.css** (`kevquirk/simple.css`, 5020★) | 시맨틱 CSS | MIT | v2.3.7 2025-05-29, push 2026-07-19 | 순수 CSS | 동일 | 참고 | 동일 | 낮음 | 참고만 |
| **Water.css** (`kognise/water.css`, 8653★) | 클래스 없는 CSS | MIT | push 2024-02-11, 약 2년 7개월 정체 `[측정함]` | - | - | - | 정체 | 낮음 | 참고만(도입 비권장) |
| Sakura (`oxalorg/sakura`, 4388★) | 미니 CSS | MIT | 1.5.1 2025-06-24 | - | - | - | - | 낮음 | 참고만 |
| **sanitize.css** (`csstools/sanitize.css`, 5311★) / normalize.css | 리셋 | CC0-1.0 | push 2026-03-26, 마지막 릴리스 v13 2021-09 | 순수 CSS | 이미 자체 리셋 | - | 효익 작음 | 낮음 | 참고만 |
| modern-css-reset (`Andy-set-studio`, 2955★) | 리셋 | MIT | **archived: true**, push 2023-09 | 33KB | - | - | 유지 종료 | 낮음 | 사용 금지(부적합) |
| **Adobe Leonardo** (`adobe/leonardo`, 2158★) | 목표 대비값(WCAG) 기준으로 색 스케일 생성 | Apache-2.0 | push 2026-07-08 | repo 14MB, 개발 시점 생성기 | 값만 뽑아 쓰면 의존성 0 | 브랜드 보라에서 4.5:1 보장 스케일을 한 번 생성해 값만 토큰화 | 생성 결과 검증은 우리 대비 스크립트로 | 중간(대비 보장 팔레트) | 개발 환경만(1회 생성용) |
| Open Color (`yeun/open-color`, 5576★) | 색 팔레트 | MIT | push 2023-12, 릴리스 2018 | - | - | - | 정체 | 낮음 | 참고만 |
| Tailwind (`tailwindlabs/tailwindcss`, 97923★) | 유틸리티 CSS | MIT | v4.3.3 2026-07-16 | 빌드 도구 필요 | 프레임워크 없는 Python 빌더와 맞지 않음 | - | 의존성·빌드 체인 추가 | 없음 | 사용 금지(우리 구조에 부적합, 스타일 값 참고도 불필요) |
| **Pretendard** (`orioncactus/pretendard`, 3620★) | 한국어 서체 | SIL OFL 1.1(README, npm `pretendard` license OFL-1.1, GH API는 NOASSERTION) | push 2026-07-23, 최신 릴리스 v1.3.9 2023-11-05 | repo 1.4GB(**clone 금지**), npm 97.6MB unpacked/1826파일 | README의 사용법은 jsDelivr/cdnjs/unpkg CDN → **CSP 위반**. 자체 호스팅만 가능 | 이미 자체 호스팅 subset woff2 사용 중(Goal Lit 86KB x 2파일) | 아래 "OFL 예약 글꼴명" 주의 | 중간(한글 가독성의 기반) | **즉시 점검 필요**(이름 문제, §E) |

### Radix Colors: 값만 활용 가능한가 (라이선스 확인)
- `[측정함]` GitHub API 라이선스 MIT, npm `@radix-ui/colors` 3.0.0 license MIT.
- MIT는 복사·수정·재배포 허용, 저작권 및 라이선스 고지 포함 조건입니다. 값(hex/oklch)만 복사해도 CSS 주석에 출처와 MIT 고지 한 줄을 남기면 됩니다 `[문서근거: MIT 표준 조건]`.
- 제약: 11/12단계 글자 대비는 APCA(Lc 60/90) 기준으로 보장됩니다 `[문서근거]`(https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale). 우리 기준은 WCAG 2 AA(4.5:1)라서 사용 조합은 반드시 별도 대비 검사를 통과해야 합니다.

### 타입 스케일/간격 스케일 생성기
- Utopia(유동 타입 스케일 계산기), Modular Scale 등은 웹 도구가 중심이라 이번에 GitHub 실측은 하지 못했습니다(`측정하지 못함`).
- 대안: 우리 토큰에 **고정 스케일**(예: 글자 4종, 4px 격자)을 먼저 정하고 stylelint로 강제하는 것이 직관성 목표에 더 직접적입니다. 측정치(첫 화면 글자 크기 10~14종)가 이유입니다.

---

## B. 자동 검증 도구 (가장 중요)

공통 사실: 박스에 Node v20.19.2, Python 3.13, `/usr/bin/google-chrome`, Python Playwright(pwvenv 1.64.0)가 있습니다. pwvenv의 Playwright 1.64.0이 기대하는 번들 Chromium(1248)이 캐시에 없어(1208만 있음) 기본 실행은 실패했고, **`executable_path=/usr/bin/google-chrome`로 해결**했습니다. 브라우저 대용량 다운로드는 하지 않았습니다 `[측정함]`.

| 후보 | 용도 | 라이선스 | 최근 활동 | 크기/의존성 | 우리 제약 적합성 | 적용 방법 | 위험 | 직관성 기여 | 판정 |
|---|---|---|---|---|---|---|---|---|---|
| **axe-core** (`dequelabs/axe-core`, 7668★) | 렌더된 DOM의 WCAG 위반 검출(대비, 헤딩 순서, 랜드마크, 이름 없는 요소 등) | MPL-2.0(수정 없이 개발 도구로 사용, 배포물에 미포함이라 문제 없음) | push 2026-10-15, v4.14.0 2026-10-05 | **의존성 0개**, npm 3.4MB unpacked | 적합. 정적 사이트에 설치 불필요(임시 폴더의 `axe.min.js`를 Playwright로 주입) | `scouting/drafts/axe_audit.py`. 8페이지 x 라이트/다크 x 390/1440 = 32회 실행에 Goal Lit 22.8초, 피치보드 34.4초, HANSET 14.6초 `[측정함]` | 자동 검출은 WCAG 문제의 일부만 잡음(`[문서근거]` axe 자체 문서 취지), 수동·스크린샷 검증 병행 | 중간(헤딩 위계·랜드마크·라벨 누락은 스캔성에 직결) | **개발 환경만(핵심)** |
| **@axe-core/playwright** (axe-core-npm, 727★) | axe의 공식 Playwright(Node) 래퍼 | MPL-2.0 | v4.14.0 2026-10-15 | npm 48KB | 우리는 Python Playwright를 이미 쓰므로 불필요 | Node 테스트 러너로 갈 때만 | - | - | 참고만(Node로 갈 경우) |
| **Lighthouse** (`GoogleChrome/lighthouse`, 30906★) | 성능·접근성·권장사항 점수 | Apache-2.0 | push 2026-10-18 | npm 최신 13.5.0은 **Node >=22.19 필요**(박스 Node 20 → 12.8.2 설치됨) `[측정함]`, 19MB | 가능(시스템 Chrome 사용) | 6회(3사이트 x 모바일/데스크톱) 실행 성공, 위 §0 표 | noindex 사이트는 SEO 카테고리 제외. 점수에 집착하지 말고 실패 항목만 사용 | 낮음~중간 | 개발 환경만 |
| **Lighthouse CI** (`lighthouse-ci`, 7115★) | CI에서 Lighthouse 예산·회귀 | Apache-2.0 | 마지막 릴리스 v0.15.1 **2025-06-26**(약 16개월 전), 번들 lighthouse **12.6.1 고정** `[측정함]` | repo 97MB | 로컬 일회성은 Lighthouse 직접 실행이 더 가벼움 | 보류 | 정체, 서버 업로드 옵션은 쓰지 않을 것 | 낮음 | 참고만 |
| **stylelint** (`stylelint/stylelint`, 11537★) | CSS 린트 | MIT | push 2026-10-18, 17.16.0 2026-10-01, engines Node >=20.19.0 | npm 987KB, 의존성 약 30개 | 개발 전용. 박스 Node 20.19.2는 조건 충족 | `scouting/drafts/stylelint.config.mjs` | - | 중간(글자 크기·색 토큰 강제 = 위계 단순화 강제) | **개발 환경만(핵심)** |
| **stylelint-declaration-strict-value** (145★) | 색 등 속성에 변수만 허용 | MIT | v1.12.1 2026-08-24, peer stylelint 16~17 | 의존성 1개 | 적합 | 파일럿 결과: 색 하드코딩 경고 Goal Lit 29건, 피치보드 15건, HANSET 17건. `!important` 금지 규칙 오류는 Goal Lit·HANSET 각 2건, 피치보드 0건 `[측정함]` | 규칙 이름이 `scale-unlimited/declaration-strict-value` 형태(설정 시 주의) | 중간 | **개발 환경만(핵심)** |
| stylelint-config-standard (1418★) | 기본 규칙 묶음 | MIT | 40.0.0 2026-01-15 | 9KB | 켜면 기존 CSS(압축 한 줄 스타일)에서 대량 스타일 경고 가능 `[추정]` | 보류, 필요한 규칙만 개별 | 노이즈 | 낮음 | 참고만 |
| stylelint-use-logical (76★) | 논리 속성 강제 | CC0-1.0 | v2.1.3 2026-02-04 | - | 한국어 단일 방향 사이트에선 효익 작음 | - | - | 없음 | 참고만 |
| stylelint-a11y (`double-great`, 12★) | CSS 접근성 규칙 | MIT | v3.8.1 2026-10-11 | - | 별 수 낮음, axe와 중복 | - | 커뮤니티 규모 작음 | 낮음 | 참고만 |
| **@google/design.md** (`google-labs-code/design.md`, 28418★) | DESIGN.md의 토큰 검증: 깨진 참조, **컴포넌트 글자/배경 대비(WCAG AA)**, 미사용 토큰, 버전 diff | Apache-2.0(GH). npm 필드는 비어 있음 | v0.4.0 2026-07-27, 스펙 version `alpha` | npm 1.6MB, 의존성 9개 | 개발 전용. 파일럿 정상 동작 | 사이트별 `DESIGN.md`(YAML 토큰 + 근거 글)를 레포에 두고 `npx design.md lint`/`diff`. 파일럿: Goal Lit 토큰 샘플에서 흰 글자 on #A78BFA = 2.72:1 경고 재현 `[측정함]` | **alpha 스펙**. 투명 배경을 #00000000으로 계산해 오탐(Apple 추출 파일 린트 시 3.77:1 경고가 투명 배경 컴포넌트에서 나옴) `[측정함]` | 중간(토큰·위계를 에이전트가 따르게 하는 계약 파일) | **개발 환경만** |
| **html-validate** (npm 11.16.4, GitHub 쪽 19★: 미러로 `[추정]`) | HTML 린트(정적) | MIT | npm 2026-10-18 | 8MB | 정적 HTML에 적합, 개발 전용 | 보류(미파일럿) | GH 별 수는 미러 기준 낮음 | 중간(시맨틱 구조) | 개발 환경만(후순위) |
| Nu HTML Checker (`validator/validator`, 1990★) / vnu-jar | W3C 수준 HTML 검증 | MIT | push 2026-10-12, npm 26.10.12 | jar 32MB, Java 필요 | Java 설치 여부 미확인 | 보류 | 크기·런타임 | 낮음 | 참고만 |
| pa11y / pa11y-ci (4578★/642★) | axe + HTML_CodeSniffer 러너 | **LGPL-3.0**(개발 도구로 쓰면 무방, 배포물 미포함) | pa11y 10.0.0 2026-08-28, pa11y-ci 5.0.0 2026-10-05 | **puppeteer 25 동봉(Chromium 다운로드 시도 가능)**, axe-core ~4.13 고정 `[측정함]` | axe와 대부분 중복. Chromium 자동 다운로드는 디스크 제한상 금지 | 쓰려면 `PUPPETEER_SKIP_DOWNLOAD`+시스템 Chrome 필요(`[짐작]`) | 중복, 대용량 다운로드 위험 | 낮음 | 사용 보류(참고만) |
| Playwright (`microsoft/playwright`, 98030★) | 스크린샷, 뷰포트, 색 모드 에뮬레이션 | Apache-2.0 | push 2026-10-18, npm 1.64.1 | npm playwright 5MB(+브라우저 별도) | pwvenv에 Python 1.64.0 설치됨 | 실제 스크린샷 검증, 대비·오버플로 측정에 사용. 시각 회귀 `toHaveScreenshot`은 Node 테스트 러너 기능이며 Python 쪽 지원 여부는 **확인하지 못함** `[짐작]` → 우리 스크립트는 Pillow 픽셀 비교로 대체 가능 | - | 중간(실제 화면 증거) | 개발 환경만(이미 사용 중) |
| pixelmatch (`mapbox/pixelmatch`, 6994★) | 이미지 픽셀 차이 | ISC | v8.0.0 2026-10-06 | 소형 | Node용. Python 쪽은 Pillow `ImageChops`로 충분 | - | - | 낮음 | 참고만 |
| reg-suit (1301★) | 시각 회귀 + 클라우드 저장소 | MIT | v0.14.6 2026-03-16 | 외부 스토리지 연동 | 서버/외부 서비스 연동 → 비용·외부 전송 | - | 외부 전송 | 낮음 | 사용 보류 |
| BackstopJS (7186★) | 시각 회귀 | MIT | push 2026-10-10, 릴리스 태그는 2019(방식 낡음), repo 62MB | puppeteer 계열 | 무겁고 우리 요구에 과함 | - | 대용량, 정체된 릴리스 방식 | 낮음 | 사용 보류 |
| **자체 정적 검사** `static_check.py` | CSP 위반 마크업, 외부 리소스, lang/h1/viewport, 다크모드·reduced-motion·keep-all·focus-visible 존재, 원색 hex·격자 위반 | (자체 작성, stdlib만) | 2026-10-19 | 단일 파일 | **의존성 0**, 빌더 테스트에 바로 편입 가능 | `python static_check.py dist` | 정규식 기반이라 근사. 오탐은 외부 canonical 링크를 제외하도록 보정함 | 중간 | **즉시 적용** |
| **자체 CSP 런타임 검사** `csp_runtime.py` | 사이트 `_headers`의 CSP를 붙여 실제 Chromium에서 위반 수집 | (자체) | 2026-10-19 | 단일 파일 | 의존성 0 | 로드 시 위반만 잡음. Goal Lit 103페이지, HANSET 43페이지 로드 에러 0 `[측정함]`. **이벤트 발생 시 위반(Enter 제출)은 로드로는 안 잡힘** → 정적 검사와 병행 | - | 낮음 | 즉시 적용(스크립트) |
| google/csp-evaluator (406★) | CSP 문자열 취약점 평가 | Apache-2.0 | v1.1.8 2026-05-26 | npm 437KB | 우리 CSP는 이미 엄격(`'self'`만). 얻을 것 적음 | 보류 | - | 없음 | 참고만 |
| mozilla/http-observatory | 보안 헤더 점검 | MPL-2.0 | **archived: true**, push 2024-10-22 | - | - | - | 유지 종료 | 없음 | 사용 금지(부적합) |
| 색 대비/변환 라이브러리: culori(1241★, MIT, 2026-10-15), color.js(2313★, MIT, 2026-10-16), wcag-contrast(BSD-2, 2022) | 대비 계산 | MIT/BSD | - | culori 1.1MB, colorjs.io 15.8MB | **Python으로 직접 계산(상대 휘도 공식)이면 의존성 0** `[추정]` | 토큰 파일 → 대비 표 스크립트 | - | 중간 | 참고만(자체 계산 권장) |
| Myndex/apca-w3 (214★) | APCA 대비 | GitHub API 라이선스 NOASSERTION(확인 불가) | push 2026-05-06 | - | 우리 기준은 WCAG 2 AA | 라이선스 원문 미확인으로 사용 보류 | 라이선스 불명 | 낮음 | 사용 보류 |
| linkinator (npm 8.1.0, MIT), lychee (4022★, Apache-2.0), hyperlink(229★) | 깨진 링크 검사 | MIT/Apache | 2026-08~2026-10 | lychee는 Rust 바이너리 | 우리 3사이트 모두 정적 → 후순위 | - | - | 낮음(사용성에는 간접) | 개발 환경만(후순위, 미파일럿) |

---

## C. 에이전트/AI UI 디자인 스킬, 가이드, DESIGN.md

직관성 목표에 가장 가까운 자료는 사용성 휴리스틱(스캔성, 위계, 라벨, 상태)을 규칙으로 쓴 문서입니다. GitHub에서 "usability heuristics checklist"로 검색한 결과 상위 항목은 별 1~2개 수준이었습니다 `[측정함]`(lari-pellini/ux-heuristics-checklist 2★ MIT 등). 신뢰할 만한 휴리스틱 원문(NN/g 10 휴리스틱)은 GitHub 자료가 아니라 웹 문서이므로 이번 범위에서는 확인하지 못했습니다.

| 후보 | 용도 | 라이선스 | 최근 활동 | 크기/의존성 | 우리 제약 적합성 | 적용 방법 | 위험 | 직관성 기여 | 판정 |
|---|---|---|---|---|---|---|---|---|---|
| **vercel-labs/web-interface-guidelines** (1009★) | 인터랙션·접근성·레이아웃 규칙 목록(키보드, 포커스링, 터치 44px, 모바일 입력 16px, 줌 금지, 상태 지속, 로딩 상태, 확인 대화 등) | MIT | push 2026-10-05, 118KB | 문서 1개 | 프레임워크 무관 규칙이 다수(일부 React/Next 전용) | 규칙을 우리 `apple-style-ui-audit`에 발췌해 합치고, 측정 가능한 것(44px, 포커스링, 16px, overscroll)은 스크립트화 | 일부 항목은 React 전용이라 선별 필요 | **높음**(터치 목표·상태·포커스·로딩 피드백은 설명 없이 쓰게 하는 규칙) | **즉시 적용(체크리스트로 발췌)** |
| **anthropics/skills `frontend-design`** (anthropics/skills 182019★, 라이선스: 스킬 폴더 LICENSE.txt는 Apache 2.0 `[측정함]`, repo 최상위 API는 none) | 디자인 스킬(두 단계: 계획→브리프와 대조→구현, 템플릿 티 안 나게 하기) | Apache-2.0 | push 2026-10-09 | SKILL.md 1개 | 규칙은 이식 가능 | "AI 생성물의 흔한 티" 목록(크림 배경+세리프, 모두 같은 둥근 카드, 대문자 눈썹 라벨 등)과 "품질 바닥선(반응형, 포커스, reduced-motion, 접근성)", "한 곳에만 대담함" 원칙을 감사 항목으로 반영 | 핵심 기조가 **"독특한 개성, 미학적 위험 감수"**라 우리 목표(설명 없이 이해되는 단순함, Apple식 일관성)와 방향이 다름 `[문서근거]` → 그대로 채택 금지, 감사 목록만 차용 | 중간(눈썹 라벨 남발·장식 제거는 단순화에 기여) | **참고만(항목 차용)** |
| **pbakaus/impeccable** (82743★) | 디자인 스킬 + 결정적 탐지 규칙 61개(`npx impeccable detect`, 소스·렌더 DOM 검사), `critique/distill/clarify/harden` 명령 | Apache-2.0 | push 2026-10-19, CLI 4.6.0 2026-10-15, repo 748MB | npm 패키지는 56KB(shim)이지만 **엔진은 플랫폼 바이너리**(첫 실행 시 `~/.impeccable/bin/` 다운로드), 소스는 Rust | 렌더 DOM 검사가 가능해 우리 목적에 가까움 | **박스에서 실행하지 않았음**(출처 확인 전 바이너리 실행 금지 규칙). 규칙 이름·문서만 읽고 `static_check.py`/`scan_metrics.py`에 해당 규칙을 자체 구현하는 방식 권장 | 텔레메트리: 스킬이 디자인을 시작할 때 `impeccable.style` roll API를 호출하며 기본은 익명 기록 전송, `DO_NOT_TRACK=1`로 끄는 방식 `[문서근거]`. 훅이 파일 편집에 개입 | **중간~높음**(`clarify`, `distill`, 줄 길이, 터치 목표, 헤딩 건너뜀 등 규칙 영역이 직관성과 겹침, 단 규칙 61개 목록 자체는 열어보지 못함) | **참고만**(CLI는 소스 검토 후 격리 환경에서만, 보류) |
| **VoltAgent/awesome-design-md** (122112★) | 84개 브랜드의 DESIGN.md 추출본(Apple, Linear, Stripe, Vercel, Notion 등) | MIT(README) | push 2026-10-14, 2.4MB | 문서 | 형식은 google design.md 스펙과 호환(Apple 파일을 `design.md lint`로 돌려 에러 0, 경고 8 `[측정함]`) | 형식·섹션 구성(토큰 + 근거 + 하지 말 것 + 에이전트 프롬프트)만 참고해 우리 사이트별 `DESIGN.md`를 쓴다 | **브랜드 사이트를 추출한 파일이라 저작권·상표 문제 가능성**, README에 상표 고지 없음 `[측정함]`. Apple 파일은 SF Pro 지정 + Apple 색값 포함 → 우리 규칙상 값 복사 금지. 한국 서비스(토스 등)는 목록에 없음 `[측정함]` | 중간(구성 형식은 위계 명시에 유용) | **참고만(값 복사 금지)** |
| **google-labs-code/design.md** (28418★) | DESIGN.md **스펙 + 린터** | Apache-2.0 | v0.4.0 2026-07-27, 스펙 alpha | §B 참조 | 위 참조 | 사이트별 DESIGN.md 형식 표준으로 채택 검토 | alpha → 포맷이 바뀔 수 있음 | 중간 | 개발 환경만 |
| VoltAgent/official-design-md (524★) | 기업이 직접 낸 DESIGN.md 목록 | MIT | push 2026-09-21, 7KB | 링크 목록 | Ant Design, Atlassian, Vercel, Mintlify 등 | 출처가 명확한 공식 문서를 참고하려면 이쪽 | - | 중간 | 참고만 |
| **nextlevelbuilder/ui-ux-pro-max-skill** (137270★) | UI 스타일 79종, 규칙 192개, CSV 데이터 + Python 검색 스크립트 | MIT | push 2026-10-15, v2.15.0 2026-08-13, 8.3MB | Python 스크립트 + CSV | `typography.csv`의 폰트 추천 URL이 **Google Fonts CDN**(CSP 위반) `[측정함]`, 한국어 관련 키워드는 typography.csv·ux-guidelines.csv 각각 1줄뿐 | `ux-guidelines.csv`(Do/Don't/코드 예시/심각도 구조)만 구조 참고 | 후원 링크·타 제품 광고성 문구가 README에 있음 `[측정함]`. 규칙이 영어 서비스·서구 폰트 중심 | 중간(ux-guidelines는 사용성 Do/Don't 모음) | **참고만** |
| Leonxlnx/taste-skill (98901★) | "AI 슬롭 방지" 프리미엄 프런트엔드 스킬 | MIT | push 2026-10-18 | 40MB | - | - | README 상단이 스폰서·자체 데스크톱 앱 홍보 중심 `[측정함]`. 내용 검증 미실시 | 낮음 | 참고만(미검토 영역 있음) |
| mattpocock/skills (296310★), PatrickJS/awesome-cursorrules (40959★, CC0), vercel-labs/agent-skills (32609★, 라이선스 none) | 범용 스킬/룰 모음 | MIT/CC0/none | 2026-05~2026-10 | - | UI 전용 아님. vercel-labs/agent-skills는 라이선스 미표기라 복사 금지 | - | 라이선스 불명(agent-skills) | 없음 | 참고만(복사 금지) |

### 우리 스킬 보강 맵
- `apple-style-ui-audit`에 추가할 것: (1) 수치 항목 — 첫 화면 단어 수, 글자 크기 종류, 클릭 요소 수, 이미지·아이콘 유무를 **측정값으로** 기록(`scan_metrics.py`). (2) Vercel 가이드에서 발췌한 상태·포커스·터치 규칙. (3) frontend-design의 "AI 티" 목록(대문자 눈썹 라벨, 모든 카드가 같은 모양 등). 이번 측정에서 Goal Lit 첫 화면에 `.eyebrow` 라벨이 실제로 있고 그것이 대비 위반 대상이었음.
- `design-tokens-bootstrap`에 추가할 것: 토큰을 `DESIGN.md`(google 스펙) 또는 `:root`에 모으고 stylelint 규칙으로 원색 직접 사용 금지, `design.md lint`로 컴포넌트 쌍 대비 검증.
- `frontend-lesson-to-structure`에 추가할 것: 이번 HANSET 인라인 핸들러 사례 같은 교훈은 `static_check.py` 규칙으로 구조화하는 것이 정석 사례.

---

## E. 한국어 웹 타이포 / 한글 UI 자료

| 후보 | 용도 | 라이선스 | 최근 활동 | 크기 | 우리 제약 적합성 | 적용 방법 | 위험 | 직관성 기여 | 판정 |
|---|---|---|---|---|---|---|---|---|---|
| **CSS `word-break: keep-all`** (이미 사용) | 한글을 어절 단위로 줄바꿈 | 웹 표준 | - | 0 | 적합 | 유지. 긴 단어/URL은 `overflow-wrap:break-word` 병행(Goal Lit 이미 적용) | - | 중간(끊김 없는 문장은 훑어 읽기 쉬움) | 즉시 적용(유지) |
| **`text-wrap: balance`(제목) / `pretty`(본문)** | 제목 줄 균형, 마지막 줄 외톨이 단어 방지 | 웹 표준, MDN "Baseline 2024 Newly available(2024-10부터)" `[문서근거]` https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap-style | - | 0 | 순수 CSS 한 줄. `balance`는 Chromium 6줄 이하만 적용 `[문서근거]` | 제목에 `balance`, 긴 본문에 `pretty`. 세 사이트 CSS 모두 아직 미사용 `[측정함]`(`text-wrap-balance|pretty`: false) | **한국어(keep-all)에서 효과는 검증 못 함** `[짐작]` → 스크린샷 비교 필수. `pretty`는 느릴 수 있음(문서) | 중간(헤드라인이 한눈에 읽힘) | **즉시 적용(스크린샷 검증 조건)** |
| **Pretendard** (§A) 자체 호스팅 서브셋 | 본 서체 | OFL 1.1 | §A | Goal Lit 서브셋 86KB x 2(Regular, Bold), 1,310글리프 `[측정함]` | 서브셋 woff2가 이미 CSP 호환 | 유지하되 아래 이름 문제 처리 | 아래 참조 | 중간 | 즉시 점검 |
| **fonttools** (`fonttools/fonttools`, 5294★) | `pyftsubset`으로 서브셋 + woff2(brotli) | MIT | 4.67.0 2026-10-14, push 2026-10-18 `[측정함]` | 파이썬 패키지 | **Goal Lit·HANSET 빌더가 이미 사용 중**(HANSET requirements `fonttools>=4.50`, `brotli>=1.1`) | 기존 방식 유지. 빌드 결과물에서 사용한 글자만 서브셋(빌드가 이미 HTML에서 글자 수집) | 서브셋 후 글자 누락 시 두부(□) 출력 → 새 글자가 생기는 페이지 빌드마다 재서브셋 필요(이미 빌드에 포함) | 낮음 | 즉시 적용(유지) |
| glyphhanger (`zachleat/glyphhanger`, 906★) | 페이지에서 쓰인 글자 추출 + 서브셋 | MIT | v6.0.0 2026-06-05 | Node, 브라우저 구동 | fonttools 빌드가 이미 같은 일을 함 | 불필요 | 중복, 헤드리스 브라우저 의존 | 낮음 | 참고만 |
| subset-font (npm 2.9.0) | Node 서브셋 | BSD-3-Clause | 2026-09-20 | 27KB | 파이썬 빌더에는 불필요 | - | - | 낮음 | 참고만 |
| **SUIT** (`sun-typeface/SUIT`, 312★) | 한국어 산세리프 대안 | OFL-1.1 | push 2024-07-13, v2.0.5 | repo 120MB | OFL, 자체 호스팅 가능 | 서체 교체 필요 시에만 | 정체 2년+, 서체 교체는 디자인 결정 | 낮음 | 참고만 |
| Spoqa Han Sans (`spoqa/spoqa-han-sans`, 412★) | 한국어 서체 | OFL-1.1 | push 2022-06-15 | repo 825MB | 정체 4년+ | - | 정체 | 낮음 | 참고만(도입 비권장) |
| Noto Sans KR via `@fontsource-variable/noto-sans-kr` | 폴백/대안 | OFL-1.1 | 5.3.1 2026-10-11 | 3.8MB unpacked(가변), 정적판 51.6MB | 자체 호스팅 가능, 쪼갠 unicode-range 파일 다수 | 폴백 스택에는 이미 `"Noto Sans KR"` 이름만 있음(시스템 설치 의존) | 대용량 | 낮음 | 참고만 |
| **W3C klreq** (`w3c/klreq`, 34★) | 한국어 텍스트 레이아웃 요구사항(줄바꿈, 문장부호, 여백) | GitHub API 라이선스 NOASSERTION(W3C 문서 정책 추정) | push 2026-03-21 | 문서 | 문서 참고 | 줄 간격·문장부호·줄바꿈 판단 근거로 읽기 | 라이선스 불명확하므로 복사 금지, 읽기만 | 낮음 | 참고만 |
| naver/nanumfont | 나눔 폰트 | GitHub API 라이선스 none, repo 6KB | push 2016-11 | - | 라이선스·원본 불명 | - | 라이선스 불명, 정체 | - | 사용 금지(부적합) → rejected.md |

### Pretendard OFL 예약 글꼴명 문제 (즉시 점검 항목)
- `[측정함]` Pretendard `LICENSE`는 "with Reserved Font Name 'Pretendard'"를 선언합니다.
- `[측정함]` Goal Lit이 배포하는 서브셋(`Pretendard-Regular.subset.woff2`, 1,310글리프)의 font `name` 테이블은 여전히 `Pretendard`, `Pretendard Regular`, `Pretendard-Regular`입니다(`fontTools`로 확인). CSS `font-family`도 `"Pretendard"`입니다.
- `[문서근거]` OFL FAQ 2.6은 "웹폰트 서브셋은 수정이며, 보통 예약 글꼴명(RFN)을 쓸 수 없다", 2.5는 "최적화/서브셋 버전은 Modified Version이므로 적절히 이름을 바꿔야 한다", 2.8은 기능 동등성(전체 문자 지원 등)을 유지하는 최적화만 이름 유지가 가능하다고 설명합니다(https://openfontlicense.org/ofl-faq/).
- `[측정함]` OFL 라이선스 텍스트 파일(`Pretendard-OFL-LICENSE.txt`)은 이미 `assets/fonts/`에 동봉되어 있고 Goal Lit·HANSET 양쪽 모두 확인했습니다. 이 부분은 문제 없습니다.
- `[추정]` 즉, 서브셋을 "Pretendard" 이름으로 배포하는 것은 엄격한 해석에서 OFL 위반 소지가 있고, 실무 위험은 낮아 보입니다(저자가 공식 서브셋도 배포하고 이름도 유지하는 관행이 있음). **법률 자문은 아닙니다.** 안전한 방법은 (a) 서브셋 woff2의 name 테이블과 CSS 이름을 예약명이 들어가지 않는 이름(예: `Lit Sans`)으로 바꾸거나, (b) 저자가 배포하는 공식 서브셋·가변 다이나믹 서브셋 파일을 **자체 호스팅**으로 그대로 쓰는 것입니다(README의 CDN 주소는 CSP 때문에 쓸 수 없음). 어느 쪽이든 구현 결정이므로 Devin swe-2/운영 봇과 협의할 사항입니다.
- 우선순위: 낮음~중간. 직관성 목표(첫 5초)와는 무관하므로 PR 순서에서 뒤로 미뤄도 됩니다.

### CDN 사용 금지 메모
- Pretendard README의 모든 사용 예(`jsdelivr`, `cdnjs`, `unpkg`)와 ui-ux-pro-max `typography.csv`의 Google Fonts URL은 우리 CSP(`font-src 'self'`, `style-src 'self'`)에 막힙니다 `[측정함: README 문자열 확인]`. 반드시 파일을 받아 `assets/fonts/`에 둔 뒤 `@font-face`로 참조해야 합니다.
