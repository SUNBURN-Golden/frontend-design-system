---
name: apple-style-ui-audit
description: >-
  Use this when auditing or building a web or app UI to Apple-style design
  quality, before changing screens or reviewing a frontend PR.
---
# Apple-style UI audit

Score each item pass / fail / n.a. with evidence (screenshot path or measured value). Never mark pass from reading code alone.

## Layout and spacing
- 8pt grid: all margins, padding, gaps are multiples of 4 or 8. Flag one-off values.
- Generous whitespace; one clear focal point per screen; content first, chrome second.
- Consistent max content width, aligned edges, no orphan elements.

## Typography
- System font stack first (-apple-system, BlinkMacSystemFont, system-ui, then a Korean-capable fallback such as Pretendard or Noto Sans KR). Never ship SF Pro files, Apple logos, icons or photos (licensing).
- Clear hierarchy: large title, headline, body, caption. Max 3-4 sizes per screen. Body 16px or more on mobile.
- Korean text: `word-break: keep-all`, line-height 1.5-1.7, no mid-word breaks, tight tracking only on large headings.

## Color and depth
- Neutral base with one accent color. Semantic tokens only (no raw hex in components).
- WCAG AA contrast (4.5:1 body, 3:1 large text) in light and dark.
- Dark mode is designed, not inverted: elevated surfaces lighter, softer borders.
- Blur / translucency only for overlays, nav bars and sheets; always with a solid fallback.
- Soft, low-opacity layered shadows; large radii (12-24px cards, pill buttons) used consistently.

## Motion
- 150-400ms, ease-out or spring-like curves; animate transform and opacity only.
- Motion explains state change; no decorative loops.
- Respect `prefers-reduced-motion`.

## Interaction and accessibility
- Touch targets at least 44x44px; visible focus ring; full keyboard path.
- Labels for icon-only buttons; alt text; correct landmarks and heading order.
- Every state exists: loading (skeleton), empty, error, disabled, hover, pressed.
- Safe areas on mobile, no horizontal scroll, works at 320px to 1440px.

## Output
Reply with: table of failed items (item, evidence, fix), then the smallest ordered list of fixes. Label each claim measured, inferred or guess. Do not hand back a check you could run yourself.
