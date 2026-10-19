# Apple 스터디 (HIG 문서 + apple.com/kr 실측)
작성 2026-10-19 · 라벨: **[문서]** 공식 문서, **[측정]** 직접 측정(헤드리스 Chrome, 1440x900 / 390x844, ko-KR), **[추정]** 근거에서 도출, **[짐작]** 근거 약함.
저작물(SF Pro 파일, 로고, 아이콘, 사진)은 복사하지 않았고 수치와 원칙만 기록한다.

## 1. HIG 핵심 원칙 (문서)
출처: developer.apple.com/design/human-interface-guidelines 의 typography, color, dark-mode, motion, accessibility, layout 페이지(공개 JSON 엔드포인트로 본문 확인, 2026-10-19).

| 영역 | 원칙 | 라벨 |
|---|---|---|
| 타이포 | iOS 기본 본문 17pt, 최소 11pt. 텍스트 스타일(Large Title 34/41, Title1 28/34, Title2 22/28, Title3 20/25, Headline 17/22 semibold, Body 17/22, Callout 16/21, Subhead 15/20, Footnote 13/18, Caption 12/16, 11/13). 크기와 leading은 한 쌍으로 정의 | [문서] typography |
| 타이포 | 얇은 커스텀 폰트는 권장 크기보다 크게. 큰 글자 설정에서도 잘림 최소화, 200% 확대 지원 권장 | [문서] typography, accessibility |
| 색 | 의미 기반(semantic) 색 사용, 라이트/다크/고대비 변형을 모두 정의. 의미를 재정의하지 않기. 강조색은 꼭 필요한 곳에만 | [문서] color |
| 다크모드 | 시스템 설정을 따르고 앱 전용 외관 설정은 피함. 다크는 반전이 아니라 "어두운 배경 + 밝은 전경". 대비 최소 4.5:1, 작은 글자는 7:1 지향. 흰 배경 이미지는 약간 어둡게 | [문서] dark-mode |
| 모션 | 목적 있는 모션만. 모션은 유일한 정보 수단이 되면 안 됨. 짧고 정확한 피드백. 자주 하는 상호작용엔 모션 추가 지양. 사용자가 기다리지 않게 취소 가능 | [문서] motion |
| 접근성 | 대비: 17pt 이하 4.5:1, 18pt 이상 3:1, Bold 3:1. 컨트롤 크기: iOS 기본 44x44pt, 최소 28x28pt, macOS 28/20. 컨트롤 간격 약 12pt(베젤 있음) / 24pt(베젤 없음). Reduce Motion 시 반복·자동 애니메이션 감소 | [문서] accessibility |
| 레이아웃 | 정렬로 위계 표현, 여백/구분선/컨테이너로 그룹. 세이프에어리어 존중, 읽기용 가이드로 텍스트 폭 제한 | [문서] layout |

## 2. apple.com/kr 공개 페이지 실측 (1440px 데스크톱)
URL: /kr/ , /kr/iphone/ , /kr/newsroom/ (2026-10-19 측정)

| 항목 | 값 | 라벨 |
|---|---|---|
| 히어로 h1 (iPhone 페이지) | 80px / line-height 92px(1.15) / weight 600 / letter-spacing normal (모바일 390px: 48px/57px) | [측정] |
| 섹션 헤드라인 | 56px/66px(1.18), 40px/44px(1.1), 28px, 24px 순. 모두 weight 600 | [측정] |
| 본문/리드 | body 17px/27px(1.59), 리드 21px/28.6px, 캡션 12px/16px, 14px/22px | [측정] |
| 한글 줄바꿈 | `word-break: keep-all` | [측정] |
| 텍스트 색 | #1d1d1f(잉크), #6e6e73(보조, 흰 배경 대비 5.07:1), 링크 #0066cc(5.57:1), CTA 배경 #0071e3 + 흰 글자(4.70:1) | [측정] 색, 대비는 계산 |
| 배경 | #fff, #f5f5f7, #fafafc, 검정 섹션 교대 | [측정] |
| 글로벌 내비 | 높이 44px(모바일 48px), `backdrop-filter: saturate(1.8) blur(20px)`, 배경 rgba(255,255,255,.8) (newsroom은 rgba(0,0,0,.8)) | [측정] |
| 카드/미디어 곡률 | iPhone 페이지 28px(40개), 20px, 36px. 모바일에서 20px→12px로 축소. 버튼 pill 980px | [측정] |
| CTA 버튼 | 17px, padding 11px 21px, 높이 44px, radius 980px | [측정] |
| 그림자 | 상위 4000개 요소 중 box-shadow 거의 없음(none). 깊이는 배경색 차이로 표현 | [측정] |
| 트랜지션 | 색 0.32s cubic-bezier(.4,0,.6,1)(194개), opacity+transform 0.16~0.32s ease | [측정] |
| 터치 타겟 | 높이 44px 미만 a/button 비율 200/313(홈), 242/380(iPhone). 인라인/내비 링크 포함이라 WCAG 위반 수치는 아님 | [측정] 주의 |
| 폰트 | 자체 웹폰트("SF Pro KR" 등) 로드, 한글 폴백 "Apple Gothic", "HY Gulim". 우리는 사용 불가 → Pretendard | [측정] |

주의: /kr/ 홈의 h1은 시각적으로 숨겨진(1px) 요소라 히어로 크기로 쓰지 않았고, 상위 큰 텍스트(top.js)로 56px/40px를 확인했다.
다크모드: apple.com 마케팅 페이지는 `prefers-color-scheme: dark`에서 배경이 바뀌지 않음(light 고정) [측정].

## 3. 시사점
- [추정] Apple식 품질은 "그림자 대신 배경 대비 + 큰 곡률 + 큰 헤드라인 + 짧은 모션"의 조합이다. 카드 깊이를 그림자로 만들지 말고 표면색 단계로.
- [추정] 헤드라인은 크기 단계를 크게 벌리고(80/56/40/28/24) 굵기는 600 하나로 통일.
- 고정 헤더 블러는 44px 낮은 바 + 80% 불투명 + blur 20px 조합. 고정색 폴백 필요(HIG에서도 reduce transparency 대응 언급).

## 4. 측정하지 못한 것
- 스크롤 연동 모션(스크롤 트리거 애니메이션)의 타이밍/이징: 미측정.
- apple.com 간격 시스템(섹션 패딩) 일반화: top.js의 section padding만 확인(60px 상단 등), 일관된 규칙으로 보기엔 표본 부족 [짐작].
- HIG 간격(spacing) 수치 표: 문서에서 tvOS 외에는 확인 못함.
