---
name: design-tokens-bootstrap
description: >-
  Use when a frontend repo has scattered colors, spacing, fonts, radii, shadows
  or motion values and needs a single design-token source.
---
# Design tokens bootstrap

1. Read the repo first: existing CSS variables, Tailwind config, theme files, shared components. Reuse and consolidate before inventing anything. Obey AGENTS.md and repo locks.
2. Inventory raw values in components (hex colors, px spacing, font sizes, radii, shadows, durations) with ripgrep and list the duplicates.
3. Create one token file (CSS custom properties, or the repo's existing theme mechanism) covering: color (semantic: bg, surface, text, muted, border, accent, danger, success; light and dark), spacing (4/8pt scale), typography (system font stack with Korean fallback, size/line-height scale), radius (12-24 cards, pill), shadow (soft layered), motion (150-400ms, ease-out curves, reduced-motion override), z-index.
4. Dark mode is its own set of semantic values, not an inversion; check WCAG AA contrast in both.
5. Replace raw values in components with tokens in small PRs (one area per PR). Never push to main.
6. Add a lint or test that fails on raw hex colors and off-grid spacing in components, so the rule is enforced by tooling.
7. Verify with the frontend-visual-verification skill.
