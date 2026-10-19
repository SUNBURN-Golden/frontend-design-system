# apple-style-ui-audit 체크리스트 추가/수정 제안
기존 스킬(`skills/apple-style-ui-audit/SKILL.md`)은 이 PR에서 수정하지 않았다. 아래는 제안이며 반영 여부는 준태님 결정.
"자동"은 Playwright computed-style 스크립트로 pass/fail 판정 가능(가능=✅, 부분=△, 수동=✋).

## 수정 제안 (기존 항목 정밀화)
| # | 기존 | 제안 | 근거 | 자동 |
|---|---|---|---|---|
| M1 | "Body 16px or more on mobile" | 본문 모바일 ≥16px, **긴 글 상세 본문 17px 권장**, 어떤 텍스트도 11px 미만 금지 | HIG min 11pt, TDS 17, SEED | ✅ |
| M2 | "line-height 1.5-1.7" | 한글 본문 1.6~1.7 (최소 1.5), 제목 1.2~1.4 | Toss 1.6, Kakao 1.75, klreq 160% | ✅ |
| M3 | "tight tracking only on large headings" | 한글 제목 -0.01~-0.03em, **-0.04em 미만 금지**, 본문 자간 -0.02em 초과 금지 | Toss/Ridi/Naver 실측 | ✅ |
| M4 | "WCAG AA contrast" | 본문 4.5 필수 + **긴 글 7:1 목표**, UI 경계·아이콘 3:1, 강조색이 텍스트로 쓰이면 별도 검사 | HIG, WCAG 1.4.11 | ✅ |
| M5 | "Touch targets at least 44x44" | 주요 컨트롤 44, **전체 최소 24(WCAG 2.5.8, 간격 예외 포함)**, 인라인 링크 제외 | WCAG 2.5.8 | △ |
| M6 | "150-400ms" | 마이크로 100~160ms, 표준 200~320ms, 큰 전환 ≤400ms. 전환 속성은 color/background/opacity/transform 중심, `all` 금지 | 실측 | ✅ |
| M7 | "large radii 12-24px" | 3단(8/12~16/20~28) + pill, 같은 레이어 혼용 금지, 스케일 외 값 플래그 | 실측 | ✅ |
| M8 | "Max 3-4 sizes per screen" | 화면당 **고유 font-size 값 ≤ 8개**(분수 px 금지)로 측정 가능하게 | Goal Lit 분수 px 다수 | ✅ |

## 신규 항목
| # | 항목 | 기준 | 근거 | 자동 |
|---|---|---|---|---|
| N1 | 본문 폭(measure) | 글 상세 본문 단락 한 줄 **한글 40~60자**(영문 45~75자). 측정: Range로 첫 줄 글자 수 | WCAG 1.4.8, 연구 50자, 실측 47~68자 | ✅ (`tools/article.js` 참고) |
| N2 | 양끝정렬 금지 | 본문 `text-align: justify` 없음 | WCAG 1.4.8 | ✅ |
| N3 | keep-all 완전성 | `word-break: keep-all` + `overflow-wrap: break-word`, 좁은 요소(배지/태그)에서 가로 오버플로 없음 | MDN | ✅ |
| N4 | 한글 폴백 스택 | Pretendard → Apple SD Gothic Neo → Malgun Gothic → Noto Sans KR → system-ui | Goal Lit 실측 | ✅ |
| N5 | 폰트 로딩 | `font-display: swap`, 서브셋 woff2, preload 1~2개, 폴백 지표 일치로 CLS 최소 | web.dev | △ |
| N6 | 헤더 | 고정 헤더 높이 ≤64px, 블러+솔리드 폴백, **포커스 요소가 헤더에 가려지지 않음**(2.4.11) | 실측, WCAG 2.2 | △ (스크롤+tab 시뮬레이션) |
| N7 | 포커스 | 모든 상호작용 요소에 `:focus-visible` 스타일, 3:1, 키보드 경로 완주 | WCAG 2.4.7 | △ |
| N8 | reduced-motion | `prefers-reduced-motion: reduce`에서 transition/animation/smooth-scroll 해제 | HIG, WCAG 2.3.3 | ✅ (emulateMedia) |
| N9 | 다크모드 | 지원하면 시맨틱 토큰 쌍, 대비 재검사. 지원 안 하면 `color-scheme: light` 명시 | HIG | ✅ (emulateMedia dark) |
| N10 | 텍스트 간격 주입 | 행간 1.5·문단 2x·자간 .12em·어간 .16em 주입 시 잘림/겹침 없음 | WCAG 1.4.12 | ✅ |
| N11 | 리플로우 | 320px 폭, 가로 스크롤 없음; 200% 확대 | WCAG 1.4.10/1.4.4 | ✅ |
| N12 | 그림자/깊이 | 그림자 종류 ≤2, 블러 반경 ≤32px, 큰 면적 카드에 강한 그림자 금지(표면색/1px 라인 우선) | 실측 | ✅ |
| N13 | 상태 완전성 | 목록·검색 뷰에 로딩/빈/에러 화면 존재, 에러 문구에 다음 행동 | HIG, Toss | △ (라우트 목록 필요) |
| N14 | UI 문구 톤 | 해요체 통일, "~시겠어요?" 등 과한 경어/수동·부정 남발 탐지, 닫기/취소 구분 | Toss UX writing | △ (정규식 린트, 문맥은 수동) |
| N15 | CTA 라벨 | 버튼이 다음 행동을 말함(예: "평론 더 보기"), 동일 문구 반복 금지 | Toss 가이드 | ✋ |
| N16 | 다크패턴 금지 | 진입 즉시 모달/바텀시트, 이탈 방해, 거절 불가 CTA 없음 | Toss 가이드 | ✋ |
| N17 | 이미지 | 폭·높이 지정(CLS), `alt`, `loading=lazy`(첫 화면 제외), 표지 비율 고정 | web.dev CLS | ✅ |
| N18 | 성능 예산 | Lighthouse 모바일: LCP ≤2.5s, CLS ≤0.1, TBT 대체 지표 | web.dev | ✅ (Lighthouse CI 필요, 현재 미구축) |
| N19 | 콘텐츠 신뢰 요소 (에디토리얼) | 출처 티어·확인일·정정 링크 위치/대비 검사 (Goal Lit 규칙과 연동) | Goal Lit PLAN | ✅(존재 검사) |
| N20 | 측정 근거 기록 | 모든 PASS/FAIL에 값+URL+날짜+라벨(측정/추정/짐작) | 스킬 출력 규칙 | ✋ |

## 스크립트화 우선순위 제안 (frontend-lesson-to-structure 연계)
1. N1 본문 폭 + M8 폰트 크기 종류 수 + M4 대비: Goal Lit에서 즉시 실패가 나오는 항목(측정으로 확인됨). 한 개의 `audit-measure.js`로 CI 후보.
2. N8/N9/N11/N10: `emulateMedia`와 뷰포트 변경만으로 자동화 가능.
3. N6/N7: 키보드 시뮬레이션 필요, 2단계.
