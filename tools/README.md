# tools (측정 스크립트, 2026-10-19)
조사용 computed-style 측정 스크립트. 구현 코드가 아니라 근거 재현용이다.
- 환경: Linux 헤드리스 Chrome(`playwright-core` + 시스템 google-chrome), locale ko-KR, 뷰포트 1440x900 / 390x844.
- `measure.js <urls.json> <viewportWidth> <light|dark> <out.json>`: 첫 h1/p, 버튼, 헤더(블러), 글자크기·반경·그림자·트랜지션 상위 빈도, 작은 터치 타겟 비율.
- `article.js <urls.json> <width> <out.json>`: 글 본문 단락의 폰트·행간·폭·실제 첫 줄 글자 수(Range로 측정).
- `top.js <urls.json> <width> <out.json>`: 화면에서 가장 큰 텍스트 5개(히어로 타입 스케일).
- `summarize.js <out.json...>`: 한 줄 요약.
한계: "첫 번째로 보이는 요소" 기반이라 사이트 전체를 대표하지 않는다. 광고/AB/지역에 따라 값이 달라질 수 있다. 원본 JSON은 `data/2026-10-19/`.
실행: `npm i playwright-core` 후 `node tools/measure.js urls.json 1440 light out.json` (urls.json: {"이름":"URL"}).
