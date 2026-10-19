# 접근성·성능 기준 스터디
라벨: [문서] 공식 문서, [측정], [추정], [짐작]. 조사일 2026-10-19.

## 1. WCAG 2.2 AA 핵심 (문서: w3.org/TR/WCAG22, w3.org/WAI/WCAG22/Understanding/*)
| SC | 기준 | 레벨 | 자동 측정 |
|---|---|---|---|
| 1.4.3 Contrast (Minimum) | 일반 텍스트 4.5:1, 큰 텍스트(≥24px 또는 ≥18.66px bold) 3:1 | AA | 가능(computed color 대비) |
| 1.4.11 Non-text Contrast | UI 컴포넌트 경계/아이콘/포커스 3:1 | AA | 부분 |
| 1.4.4 / 1.4.10 | 텍스트 200% 확대, 320px 폭 리플로우(가로 스크롤 없음) | AA | 가능(320px에서 scrollWidth) |
| 1.4.12 Text Spacing | 행간 1.5, 문단 2x, 자간 0.12em, 어간 0.16em 적용해도 깨지지 않기 | AA | 가능(스타일 주입 후 오버플로 검사) |
| 2.4.7 Focus Visible | 키보드 포커스 표시 | AA | 부분(:focus-visible 규칙 존재) |
| 2.4.11 Focus Not Obscured (Minimum) | 포커스 요소가 고정 헤더 등에 완전히 가려지지 않기 (2.2 신규) | AA | 가능(스크롤 후 rect 비교) |
| 2.5.8 Target Size (Minimum) | 포인터 타겟 24x24 CSS px 이상, 예외: 간격 24px 원 비교차, 인라인, 대체 컨트롤 등 (2.2 신규) | AA | 가능(예외 처리 필요) |
| 2.5.7 Dragging Movements | 드래그 대안 제공 (2.2 신규) | AA | 수동 |
| 3.3.8 Accessible Authentication | 인지 테스트 의존 인증 금지 (2.2 신규) | AA | 수동 |
| 1.4.8 Visual Presentation (참고) | 폭 80자(CJK 40자), 양끝정렬 금지, 행간 1.5, 문단 간격 ≥1.5×행간 | AAA | 부분 |
| 2.3.3 Animation from Interactions (참고) | 모션 비활성화 가능 | AAA | 가능(prefers-reduced-motion 규칙) |
우리 기준은 AA를 필수, 1.4.8의 폭·행간은 한글 에디토리얼에서 목표로 채택 [추정].
※ 2.4.11, 2.5.7, 2.5.8, 3.3.8이 AA임은 W3C Understanding 페이지 각각에서 직접 확인(2026-10-19) [문서].

## 2. 플랫폼 기준값
| 항목 | 값 | 라벨 |
|---|---|---|
| 터치 타겟 | Apple HIG iOS 기본 44x44pt, 최소 28x28pt; 간격 약 12pt(베젤) / 24pt(무베젤) | [문서] HIG accessibility |
| 터치 타겟 | WCAG 2.5.8 최소 24x24 CSS px (AAA 2.5.5는 44x44) | [문서] |
| 대비 | HIG: 최소 4.5:1, 소형 텍스트 7:1 지향; 17pt 이하 4.5:1, 18pt 3:1, Bold 3:1 | [문서] |
| 다크모드 | 시스템 설정 따르기, 반전 금지, 흰 배경 이미지 완화, 고대비 모드 함께 검증 | [문서] HIG dark-mode |
| 다크 구현 | Linear: base/accent/contrast 3변수로 LCH 기반 테마 생성(고대비 테마 포함). Vercel은 prefers-color-scheme 반응 | [문서]/[측정] |
| 모션 | Reduce Motion 시 자동/반복 애니메이션 감소, 스프링 바운스 축소, 큰 이동 대신 페이드 | [문서] HIG accessibility |
| 모션 CSS | `@media (prefers-reduced-motion: reduce)`로 전환/스무스 스크롤 해제 | [문서] 표준(MDN) |

## 3. Core Web Vitals (문서: web.dev/articles/vitals, support.google.com/webmasters/answer/9205520)
| 지표 | Good | Needs improvement | Poor | 기준 |
|---|---|---|---|---|
| LCP | ≤ 2.5s | ≤ 4s | > 4s | 75퍼센타일, 모바일/데스크톱 분리 |
| INP | ≤ 200ms | ≤ 500ms | > 500ms | 〃 |
| CLS | ≤ 0.1 | ≤ 0.25 | > 0.25 | 〃 |
정적 사이트(Goal Lit)는 폰트 `font-display: swap` + 서브셋 woff2 preload로 LCP/CLS 유리. 폰트 대체 시 CLS 방지를 위해 size-adjust 폴백 고려 [추정].

## 4. 실측 스냅샷 (접근성 관련, 2026-10-19)
| 항목 | 결과 | 라벨 |
|---|---|---|
| Apple 보조 텍스트 #6e6e73 / 흰 | 5.07:1 (AA 통과, 7:1 미달) | [측정 색 + 계산] |
| Apple CTA 흰 글자 / #0071e3 | 4.70:1 | 〃 |
| Goal Lit accent #A78BFA / 배경 #F5F3FA | **2.47:1** (텍스트로 사용 시 AA 실패, 큰 글자 3:1도 미달) | [측정 색 + 계산] |
| Goal Lit 흰 글자 / #A78BFA | 2.72:1 (버튼은 어두운 글자 #1A1A1A 사용 중) | 〃 |
| Goal Lit accent-d #5B3FB5 / 배경 | 6.76:1, ink #1A1A1A / 배경 15.82:1 | 〃 |
| 문장웹진 푸터 #acacac / 흰 | 2.27:1 (공개 사이트에도 흔한 실패 유형) | 〃 |
| Goal Lit CSS | prefers-reduced-motion 1곳, :focus-visible 1곳, prefers-color-scheme 0, transition 0, min-height 44 규칙 0 | [측정: site.css 14.5KB grep] |
| Goal Lit 작은 타겟 | a/button 73/75가 높이 44px 미만(인라인 링크 포함이라 WCAG 위반 수치 아님) | [측정] 주의 |
| 모바일 가로 스크롤 | Goal Lit 390px에서 scrollWidth 정상 | [측정] |

## 5. 측정하지 못한 것
- 실제 CWV(LCP/INP/CLS): 실사용(CrUX) 데이터와 Lighthouse를 돌리지 않았음. 임계값은 문서로만.
- 스크린리더/키보드 전 경로, 포커스 링 시각 수치(두께, 오프셋), 고대비 모드, 확대 200% 시 동작.
- 2.4.11 가림 여부(스크롤 상태 측정), 1.4.12 텍스트 간격 주입 테스트.
