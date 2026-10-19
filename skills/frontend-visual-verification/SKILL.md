---
name: frontend-visual-verification
description: >-
  Use after any frontend change, before claiming a UI is done or opening a PR,
  to prove it with real screenshots.
---
# Frontend visual verification

'Build passed' is not evidence. Only screenshots and measurements are.

1. Start the dev server or preview build in the background (block_until_ms 0). Note the URL.
2. Capture the changed screens with a headless browser (Playwright or Puppeteer) in four combinations: mobile 390x844 and desktop 1440x900, each in light and dark (`colorScheme` emulation). Add 320px width for overflow checks. Save to a folder named by date and PR, e.g. shots/<pr>/<screen>-<viewport>-<scheme>.png.
3. Measure what can be measured by script: horizontal overflow (`scrollWidth > clientWidth`), touch target sizes (>= 44px), computed contrast against WCAG AA, focus ring visible after Tab, behaviour with `prefers-reduced-motion: reduce`.
4. Read each screenshot and compare against the apple-style-ui-audit checklist. Mark every claim measured, inferred or guess.
5. Report failures with the screenshot path and fix; fix and re-shoot until clean. Do not hand a check you could run yourself to a person.
6. Attach the key screenshots to the PR description or the report.
