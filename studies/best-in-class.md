# 비 Apple 최상급 사례 (Linear, Stripe, Vercel, Notion, Airbnb, Raycast)
측정: 2026-10-19, 헤드리스 Chrome, 1440x900(데스크톱) / 390x844(모바일), 첫 화면 기준. 라벨: [측정] [문서] [추정] [짐작]. 원본: `data/2026-10-19/`.

## 1. 측정 표 (데스크톱 히어로·본문·컴포넌트)
| 사이트 | 히어로 h1 | 본문/리드 | 폰트 | 반경(빈도 상위) | 그림자 | 트랜지션 | 헤더 |
|---|---|---|---|---|---|---|---|
| Linear (linear.app) | 64/64px, ls -1.408px(-2.2%), w510 | 15/24px, ls -0.165px | Inter Variable | 9999(pill) 72, 8px 27, 12px 25 | 내부 inset 글로우 위주 | color 0.1s cubic-bezier(.25,.46,.45,.94) | 73px, blur(20px), 다크 기본 bg #08090a |
| Stripe (stripe.com) | 48/55.2px(1.15), ls -0.96px, w300 | 리드 32/35px w300 | sohne-var | 4px 57, 6px 40 | rgba(50,50,93,.12) 0 16px 32px | color/fill 0.3s cubic-bezier(.25,1,.5,1) | 76px |
| Vercel | 64/64px(1.0), ls -3.84px(-6%), w400 | 24/32px ls -0.96px | Geist | 6px 44, pill 21, 8px 6 | 0 0 0 1px 링 위주(거의 투명) | 0.1~0.15s cubic-bezier(.4,0,.2,1) | 64px, bg #fafafa(라이트)→#000(다크) |
| Notion (/ko) | 96/100px, ls -4.6px(-4.8%), w600 | 20/28px | NotionInter | 8px 64, 4px 22, 12px 21 | rgba(0,0,0,.01~) 초박 멀티레이어 | 0.2s cubic-bezier(.42,0,1,1) | 64px |
| Airbnb (.co.kr) | 28/40px w700 | body 14px | Airbnb Cereal VF | 20px 76(카드), 50%, 8px | 0 0 0 1px rgba(0,0,0,.02) + 멀티레이어 | transform 0.25s cubic-bezier(.2,0,0,1) | 96px(검색 포함) |
| Raycast | 64/70.4px(1.1), w600 | 18px ls 0.2px | Inter | 11px 159, 8px 107, 6px | 0 1.5px .5px 2.5px 링 + 멀티레이어 | 0.2~0.4s cubic-bezier(.23,1,.32,1) | n/a |
| (참고) Goal Lit 홈 | 40/52px(1.3), ls -0.4px(-1%), w700 | 17/28.05px(1.65) | Pretendard | 6px 78, 14px 36, 999 27 | none | 없음 | 69px, blur(8px), bg rgba(245,243,250,.96) |

모바일(390): Linear h1 38/41.8px, Stripe 34/35px, Vercel 24/32px(Geist), Notion 42/48px, Raycast 36/39.6px [측정]. 데스크톱 대비 히어로는 약 55~65% 크기.
다크: Vercel은 `prefers-color-scheme`에 반응(#fafafa→#000), Linear/Raycast는 다크가 기본, Apple/Stripe/Notion/Airbnb 첫 화면은 변화 없음 [측정].

## 2. 무엇이 좋은가 (패턴으로 정리)
1. **위계는 크기·굵기·자간으로, 색 수는 적게.** 히어로 헤드라인은 큰 음수 자간(-2~-6%)과 line-height 1.0~1.15로 단단하게. 본문은 14~16px/1.5, 보조 텍스트는 같은 뉴트럴 계열 한 단계 밝게 [측정]. (라틴 기준. 한글에는 -6% 같은 값 금지 → korean.md)
2. **밀도 두 단계.** 마케팅은 여백 크게+큰 헤드라인, 제품 UI는 15px/24px 본문, 8px 반경 컨트롤로 촘촘하게(Linear 15/24, Notion 14, Airbnb 14) [측정].
3. **경계는 그림자보다 1px 링/표면색.** Vercel, Airbnb, Raycast 모두 0 0 0 1px 링 + 매우 약한 그림자. 큰 블러 그림자는 Stripe의 일부 카드에만 [측정].
4. **마이크로 인터랙션은 100~300ms, ease-out 계열.** Linear/Vercel 100~150ms(색 변화), Stripe/Notion/Apple 200~320ms, Raycast 최대 400ms. 거의 `color`/`background`/`opacity`/`transform`만 전환 [측정].
5. **색은 의미 단위 토큰 + 지각 균일 색공간.** Linear는 LCH로 테마를 base/accent/contrast 3변수로 생성, 고대비 테마도 자동 [문서: linear.app/now/how-we-redesigned-the-linear-ui]. Stripe는 CIELAB 기반으로 색 5단계 차이면 소형 텍스트 대비 4.5:1 보장 [문서: stripe.com/blog/accessible-color-systems].
6. **헤딩 전용 서체 변형.** Linear는 헤딩에 Inter Display, 나머지는 Inter [문서].
7. **카드 곡률은 용도별 3단.** 컨트롤 6~8, 카드 12~20, 미디어/히어로 20~28 + pill [측정].

## 3. 상태(빈/로딩/에러)
- Linear 리디자인 문서는 상태 전반 점검(Inbox/Triage/Roadmap 등 모든 뷰에서 테스트)을 프로세스로 명시 [문서]. 개별 빈/로딩/에러 화면의 시각 수치는 **측정하지 못했다**(로그인 필요 영역).
- 공개 페이지에서 확인 가능한 것은 Goal Lit 404("페이지를 찾을 수 없어요" + 홈으로 링크, 해요체) 정도 [측정].

## 4. 측정하지 못한 것
- Arc: 웹 사이트가 아닌 앱이라 미측정. Raycast 웹만 측정(앱 UI 아님).
- Notion/Linear/Stripe 앱 내부(로그인 필요) UI, 빈/로딩/에러 상태: 미측정.
- Airbnb 모바일 히어로 h1(28px)은 검색 UI 중심이라 비교 가치 낮음. 첫 보이는 요소 기준 한계.
