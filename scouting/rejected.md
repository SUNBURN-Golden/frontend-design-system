# 사용 금지 / 부적합 (이유 포함)

판정 라벨: **사용 금지**(라이선스·출처·규칙 위반 또는 위험), **부적합**(우리 구조/목표와 안 맞음), **보류**(정보 부족). 근거는 `scouting/github.md`, `huggingface.md`의 같은 항목 참조. 모든 수치는 2026-10-19 측정.

| 대상 | 판정 | 이유 | 근거 라벨 |
|---|---|---|---|
| Apple 저작물(SF Pro 폰트 파일, Apple 로고·아이콘·사진), `awesome-design-md/apple`의 값을 그대로 복사한 토큰 | **사용 금지** | 우리 규칙(Apple 저작물 금지). 해당 파일은 SF Pro 지정과 Apple 색값 포함. 상표 고지가 README에 없음. 형식과 구성만 참고 | 측정함(파일 내용, README 확인) |
| VoltAgent/awesome-design-md의 브랜드 추출 DESIGN.md 전반(값 복사) | **사용 금지(복사)** / 참고만 | 브랜드 사이트를 추출한 자료라 저작권·상표 불확실. MIT 표기는 추출 파일 자체에 대한 것 | 측정함, 추정 |
| 시스템 대체로 SF Pro를 지정하는 코드(`SF Pro Display` 등 명시) | **사용 금지** | Apple 서체 파일은 재배포 불가. 시스템 스택(`-apple-system`)만 사용 | 문서근거(우리 스킬 규칙) |
| Pico CSS | **부적합** | archived, README에 "새 릴리스 없음, 유지 종료" 명시. 이미 자체 CSS 보유 | 측정함, 문서근거 |
| Andy-set-studio/modern-css-reset | **부적합** | archived(push 2023-09) | 측정함 |
| mozilla/http-observatory | **부적합** | archived(push 2024-10) | 측정함 |
| Tailwind CSS | **부적합** | 빌드 체인·의존성이 필요, 프레임워크 없는 Python 빌더 구조와 충돌 | 추정(구조 판단) |
| Pretendard README의 CDN(jsDelivr, cdnjs, unpkg) 로딩 코드, Google Fonts `<link>`/`@import`, ui-ux-pro-max `typography.csv`의 폰트 URL | **사용 금지** | CSP `default-src 'self'` 및 `font-src 'self'` 위반, 외부 서비스에 방문자 IP 노출 | 측정함(문자열), 규칙 |
| Pretendard 저장소 전체 clone (1.4GB), npm `pretendard` 전체(97.6MB) 설치 | **사용 금지(다운로드)** | 디스크 24GB 여유 제한, 필요한 파일만 쓰면 됨 | 측정함 |
| `naver/nanumfont` | **사용 금지** | GitHub 라이선스 없음, 원본 정체 2016-11 | 측정함 |
| `Myndex/apca-w3`(APCA) | **보류** | GitHub 라이선스 NOASSERTION, 라이선스 원문 확인 못 함. 우리 기준은 WCAG 2 AA(대비 4.5:1) | 측정함 |
| pa11y / pa11y-ci | **보류** | axe와 중복. puppeteer 25 동봉(Chromium 다운로드 시도 가능, 디스크 제약), axe-core 4.13 고정. LGPL은 개발 도구라 문제 없음 | 측정함 |
| BackstopJS, reg-suit | **보류** | 무겁거나(62MB repo, puppeteer) 클라우드 저장소 연동(외부 전송, 비용) | 측정함, 문서근거 |
| Lighthouse CI(`@lhci/cli`) | **보류** | 마지막 릴리스 2025-06-26(약 16개월), lighthouse 12.6.1 고정. 로컬은 Lighthouse 직접 실행이 더 가볍다 | 측정함 |
| 일반 버전 Lighthouse 13.x | **보류** | Node >=22.19 필요(박스 Node 20.19.2). 12.x 사용 | 측정함 |
| impeccable CLI(`npx impeccable detect`) 실행 | **보류** | 엔진이 플랫폼 바이너리로, 첫 실행에 `~/.impeccable/bin/`에 다운로드. 소스 검토 전 바이너리 실행 금지 규칙. 텔레메트리(디자인 시작 시 roll API 호출, `DO_NOT_TRACK=1`로 비활성)와 편집 훅 개입. 문서·규칙 아이디어만 사용 | 문서근거 |
| anthropics/skills `frontend-design`의 "독특한 개성과 미학적 위험 감수" 기조 | **부적합(기조)** | 우리 목표(UX 흐름 단순화, 첫 5초 이해, Apple식 일관성)와 방향이 다름. "AI 티" 목록과 품질 바닥선만 차용 | 문서근거 |
| revelohq/ui-quality-bench 루브릭을 최적화 목표로 삼기 | **부적합** | "기본 중앙 그리드를 넘어서는 구성" 30%, 색 "과감함" 25%를 보상 → 단순화 목표와 역방향 | 문서근거 |
| taste-skill, mattpocock/skills 등 범용 스킬 모음 | **참고만(미검토)** | 상단이 스폰서/자사 앱 홍보 중심이거나 UI 전용이 아님. 내용 전부 검토하지 못함 | 측정함(README), 짐작 |
| vercel-labs/agent-skills 파일 복사 | **사용 금지(복사)** | GitHub 라이선스 none | 측정함 |
| `biglab/UIClip` 로컬 설치·의존 | **부적합** | 영어 전용, 224px 입력, PyTorch 필요(가중치 605MB), 우리 기준(첫 5초 이해)을 재지 못함. 공개 화면 한정 Space 비교 실험만 선택 | 문서근거, 추정 |
| `Qwen/Qwen2.5-VL-3B-Instruct` | **사용 금지** | 라이선스 `qwen-research`(연구용), 7.5GB | 측정함 |
| `ronantakizawa/webui` 데이터의 코드 복사 | **사용 금지(복사)** | 카드상 MIT이나 원본은 MIT/Apache/GPL 혼합 | 문서근거 |
| `HuggingFaceM4/WebSight` | **부적합** | 현재 파일 317GB, 코드 생성 학습용 | 측정함 |
| `biglab/webui-350k` | **사용 금지** | 라이선스 `other`, 용량 큼(`usedStorage` 약 465GB) | 측정함 |
| `mrtoy/mobile-ui-design` | **사용 금지** | 모바일 앱 이미지 모음, 출처 불명 자산 가능성 | 추정 |
| `Tesslate/WEBGEN-4B`, `UIGEN-X-4B`, UI-TARS, ShowUI, OmniParser(원본 `icon_detect`는 AGPL-3.0) | **부적합** | 코드 생성/GUI 조작 에이전트용, 크기 큼, 구현은 Devin swe-2 전용 규칙, AGPL 혼재 | 측정함, 문서근거 |
| `newazhala/ui-design-audit-dataset` 라벨을 접근성/UX 근거로 인용 | **부적합** | 카드가 "합성 규칙 라벨, 사람 UX 판단·접근성 준수 증거가 아님"이라고 명시 | 문서근거 |
