---
name: frontend-lesson-to-structure
description: >-
  Use when a frontend mistake or review comment repeats, or a lesson is learned,
  to turn it into a lint, test or script and record it.
---
# Frontend lesson to structure

1. State the lesson in one line: what went wrong, where, and the measured evidence.
2. Check whether the same point has come up before (search this skill's log below and the repo history). Second occurrence means a sentence rule is not enough.
3. Convert it into something that fails automatically: a lint rule, a style test, a screenshot or measurement script, or a CI check. Prefer the repo's existing tooling.
4. Add the check in a small PR, run it against the current code, and confirm it catches the original mistake.
5. Append a dated entry to the lesson log in this skill via UpdateSkill: lesson, structure that now enforces it, link to the PR.

# Lesson log
(empty)
