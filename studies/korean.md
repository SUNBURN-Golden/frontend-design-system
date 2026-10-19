# 한국어/한국 사례 스터디 (토스, 카카오, 네이버, 당근, 리디, 브런치, 문장웹진)
측정 2026-10-19 (헤드리스 Chrome, ko-KR). 라벨: [문서] [측정] [추정] [짐작].

## 1. 공개 디자인 시스템 문서
| 출처 | 내용 | 라벨 |
|---|---|---|
| 토스 TDS Typography (tossmini-docs.toss.im/tds-mobile/foundation/typography) | Typography1 30/40, 2 26/35, 3 22/31, 4 20/29, 5 17/25.5(일반 본문), sub8 19/28 … 값은 하드코딩 금지, 토큰 사용. 시스템 "더 큰 글자" 비율(110~310%)을 웹에도 적용하라고 명시 | [문서] |
| 토스 UX 라이팅 (developers-apps-in-toss.toss.im/design/consumer-ux-guide) | 해요체 통일, 능동형, 긍정형, 과한 경어 금지(~시겠어요? 지양), `{명사}+{명사}` 지양, "되어요→돼요", 다이얼로그 왼쪽 버튼은 "닫기"(취소는 작업 취소로 오해), CTA는 다음 행동을 예측 가능하게. 아이콘 24~40px, 한 번에 하나. 다크패턴 금지(진입 즉시 바텀시트, 이탈 막기 등) | [문서] |
| 토스 서체 (cho.sh 정리) | Toss Product Sans: 숫자·영문을 한글보다 약간 굵고 크게, 기호 여백 넓게, 한글 수직 중앙 보정. 오픈소스 대안으로 Pretendard 언급 | [문서, 2차 출처] |
| 당근 SEED (seed-design.io/foundations/typography) | 글자 11/12/13/14/16/18/20/22/24/26/28/32/40/48px, line-height 15/16/18/19/22/24/27/30/32/35/38/42/52/60px(≈1.2~1.4), weight 400/500/700, rem 기반(사용자 폰트 설정 존중) + static(px) 변형. t11 이상은 sm 브레이크포인트 이상에서만 권장 | [문서] |
| Pretendard (github.com/orioncactus/pretendard) | "어느 플랫폼에서든 사용할 수 있는 system-ui 대체 글꼴" (저장소 설명). 라이선스 OFL은 Goal Lit 운영 봇 설명 기준 | [문서] 설명만 확인 |

카카오/네이버: 공개 디자인 시스템 문서는 **확인하지 못했다**(조사 범위에서 검색하지 않음). 아래는 사이트 실측만.

## 2. 실측 (한글 사이트)
| 사이트 | 값 | 라벨 |
|---|---|---|
| toss.im 홈 | h1 80/96px(1.2) w700, 서브 40/56px ls -0.8px(-2%), 본문 16/25.6px(1.6) ls -0.32px(-2%), Toss Product Sans, 헤더 64px, 반경 12/40px, 그림자 없음, 트랜지션 background 0.3s ease | [측정] |
| toss.tech 글 상세 | 본문 17/27.2px(1.6) #333d4b(흰 배경 대비 11.0:1), 글 폭 700px → 첫 줄 59자, `keep-all`, 문단 간격 8px, h1 48/60px w700(모바일 32/40px). 모바일 본문 폭 348px → 첫 줄 29자 | [측정] |
| tech.kakao.com 글 | 본문 15.96/27.93px(1.75) KakaoBig, 폭 768px → 첫 줄 68자, `word-break: normal`, 문단 간격 14px, h1 28/30.8px | [측정] |
| kakaocorp.com | h1 28/42px(1.5) w700 KakaoSmall, 헤더 72px, 반경 999/18/16px | [측정] |
| naver.com | 기본 14.7px, 헤드 라벨 ls -0.4px(-2.7%) w700, 반경 4px(37개)/8px, 트랜지션 transform 0.2s cubic-bezier(.165,.84,.44,1) | [측정] |
| series.naver.com (웹소설 디렉터리) | 본문 12px 나눔고딕, 매우 높은 밀도 | [측정] |
| daangn.com | 본문 16px, 반경 4/8/16px, 그림자 rgba(0,0,0,.05) 0 1px 1px, 트랜지션 .15s | [측정] |
| medium.com/daangn 글(한글) | 본문 20/32px(1.6) **세리프(source-serif-pro)**, 폭 680px → 첫 줄 47자, h1 42/52px(모바일 32/38px) | [측정] |
| ridibooks.com (웹소설/도서 디렉터리) | Pretendard Variable, h1 28px ls -0.84px(-3%), 본문 14px, 반경 4px(380개: 표지 썸네일), 20px, pill, 그림자 rgba(0,0,0,.06) 2 4 8 | [측정] |
| brunch.co.kr 글 | 본문 14.67/29.33px(행간 2.0) ls +0.8px **justify**, 폭 700px → 첫 줄 61자, 제목 명조(Nanum Myeongjo) 45/53px ls -1% | [측정] |
| munjang.or.kr (문장웹진) | Pretendard, 홈 본문 18/28px, 반경 18px. **글 상세 본문은 선택이 푸터로 잘못 잡혀 미측정** | [측정] 부분 |
| Goal Lit (참고) | Pretendard 17/28.05px(1.65), keep-all, h1 33.6/43.7px(글 상세), 본문 폭 1044px → 첫 줄 89자 | [측정] |

### 도출한 수치
- **한글 평균 글자 폭 ≈ 0.70em/자(공백·숫자·문장부호 포함)**: Toss 11.9px@17px, Kakao 11.3px@15.96px, Goal Lit 11.7px@17px(각각 폭÷첫줄 글자수) [측정으로 도출]. 따라서 `max-width: 36em`(17px에서 612px)은 약 50자 [추정].
- **줄 길이**: WCAG 1.4.8(AAA)은 CJK 40자 이하 [문서: w3.org/WAI/WCAG22/Understanding/visual-presentation]. 한글 웹 독해 연구는 50자/줄에서 읽기 속도 개선 보고(신종현·박민용, 대한산업공학회지 29(3), DBpia) [문서: 초록]. 실측 사이트는 47~68자(Toss 59, Brunch 61, Kakao 68, 당근 블로그 47). → 권장 **40~55자, 상한 60자** [추정].
- **행간**: 한글 본문 1.5~1.75 (Toss 1.6, Goal Lit 1.65, Kakao 1.75, Brunch 2.0). W3C klreq 예시는 160%, WCAG AAA는 최소 1.5 [문서]. → **본문 1.6~1.7** [추정].
- **자간**: 한국 사이트는 제목에 -1~-3%(Toss -2%, Ridi -3%, Brunch -1%, Naver -2.7%) 사용. 본문은 0~-2%. 라틴 히어로의 -6%(Vercel)는 한글에 부적합 [추정].
- **word-break**: `keep-all` + `overflow-wrap: break-word` 조합이 어절 단위 줄바꿈(조사 한 글자 고아 방지)에 안전 [문서: MDN word-break; design.solhun.com 해설]. Toss tech/Goal Lit는 keep-all, Kakao tech는 normal [측정].
- **본문 크기**: 17px(Toss, TDS 일반 본문 17/25.5), 16px(SEED t5, 당근), 14~15px(Kakao tech 15.96, Brunch 14.67, Ridi 14)은 밀집형. 긴 글 기본은 **17px**가 합리적 [추정]. 모바일 16px 이상.
- **한글 폰트**: Pretendard가 Ridi/Brunch/Goal Lit/문장웹진 등 실사용 [측정]. 시스템 폴백은 Apple SD Gothic Neo, Malgun Gothic, Noto Sans KR [Goal Lit CSS 측정]. 카카오는 자체 서체(KakaoBig/Small), 토스는 Toss Product Sans(공개 배포 안 함) → 우리는 Pretendard.
- **세리프 제목/본문**: 문학 성격 콘텐츠에서 Brunch(명조 제목), 당근 블로그(세리프 본문)가 사용. Goal Lit 평론 제목에 명조/세리프 도입은 선택지 [짐작: 브랜드 결정 필요].

## 3. 한글 UI 문구 톤 (Goal Lit 적용)
- 해요체 + 능동 + 긍정. Goal Lit 404 "페이지를 찾을 수 없어요", 푸터 "출처와 확인일을 붙여요"는 이미 해요체 [측정].
- 에러는 해결 행동 포함("홈으로"), 부정형 최소화. 닫기/취소 구분: 작업 취소와 창 닫기를 혼동시키지 않기 [문서: Toss].
- 평론 글(본문)은 해요체가 아닌 에디토리얼 문어체가 자연스러울 수 있음 [짐작: Goal Lit 편집 원칙은 운영 봇이 결정].

## 4. 측정하지 못한 것
- 카카오·네이버 공식 디자인 시스템 문서, 당근 컴포넌트 수치(SEED 타이포 외), 토스 TDS 간격/반경 토큰.
- 문장웹진·씨네21(타임아웃) 글 상세. 카카오페이지/네이버웹툰 앱 UI.
- Toss Product Sans 파일은 라이선스상 사용 불가라 시도하지 않음.
