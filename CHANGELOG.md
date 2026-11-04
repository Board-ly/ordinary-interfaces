# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) as applied to a rule
set:

- **major**: a rule id is removed or renamed, or a non-negotiable changes
- **minor**: rules or reference files added, scripts gain capabilities
- **patch**: a number corrected, a citation fixed, wording clarified

## [2.1.0] / 2026-11-04

### Changed

- **Four commands have shorter names.** `read-project` is `scan`,
  `accessibility` is `a11y`, `new-screen` is `build`, `find-rule` is `rule`.
  `review` and `contrast` were already short enough. With the
  `/ordinary-interfaces:` prefix the longest invocation went from 34 characters
  to 29, and in the README's table the prefix is now stated once above instead
  of repeated in every row, which is what actually made the column unreadable
  on a narrow screen.
- **The old names no longer work**, including
  `npx skills add ... --skill accessibility`, which is now `--skill a11y`. By
  the policy above this is a minor release, since that policy is written about
  rule ids and no rule id moved. It is listed here as plainly as a breaking
  change would be, because for anyone who typed the old names it behaves like
  one.

## [2.0.0] / 2026-11-04

A structural release. No UI rule changed its value; the rules moved, the cues
were repaired, and the entry points were re-sorted by what is cheap to load.

### Removed

- **`references/beyond-screen.md` and its 9 rule ids** leave this skill and
  become the standalone `beyond-screen` skill: `viewing-distance`,
  `visual-angle-arcminutes`, `aspect-ratios`, `logo-clearspace`,
  `logo-variations`, `joint-cropping`, `dieline-bleed`, `cmyk-vs-pantone`,
  `iso-216`. They were an appendix marked "outside the UI focus", nothing in
  the UI rules referenced them, and a print question is not a UI question. The
  ids are unchanged and the text is intact, so a reference to one still
  resolves, in the other skill. **This is why the major version moves**: ids
  left the index, which this changelog's own policy calls a breaking change.
  The rule count goes 211 to 202.

### Fixed

- **The `ai-tells.md` detection cues missed utility-class codebases.** Four of
  the cues matched only stylesheet syntax, so a Tailwind project returned no
  findings, and no findings reads as a clean result rather than as an unrun
  check. That is the worst failure available to a detection layer, and it hit
  the stack the skill's own step 0 expects, since `project-system.py` reports
  shadcn and Tailwind. Measured against one real codebase, the old hover cue
  found 53 of 335 actual occurrences. Every cue now carries both notations,
  `one-spacing-value` normalises `p-4`, `px-4` and `mt-4` to one step on the
  scale before counting, `happy-path-only` searches from the repository root
  instead of `src/components` and also catches the empty fragment, and
  `border-instead-of-surface` and `centred-everything` gained the runnable
  form they were described as having.

### Changed

- **`read-project`, `contrast` and `find-rule` lost `disable-model-invocation`.**
  All six commands were user-only, so the agent's only path was the expensive
  one: a single contrast check loaded `SKILL.md` plus a reference file when a
  33-line command sat next to it. These three return a measurement rather than
  an opinion. `accessibility`, `review` and `new-screen` stay locked, because a
  review is something a person starts.
- **`SKILL.md` is shorter by a sixth**, 200 lines to 168, 13,436 bytes to 11,232. The build workflow was
  duplicated between it and `new-screen`, the audit format and audit rules
  between it and `review`, with eleven lines character-identical. Each now
  lives in its sub-skill, where it is loaded by the workflow that uses it. What
  remains is what every task needs: step 0, the evidence grades, the seven
  gates, and the routing table.

## [1.2.0] / 2026-11-02

### Added

- **`references/overlays.md`, 12 rules.** The overlay layer had no coverage at
  all. Which of the four elements a job calls for and what that commits you to,
  backdrop values per mode, the 600px point where a dialog becomes a sheet, the
  sheet drag contract including the inner-scroll conflict that loses typed
  input, grab handles, scroll lock without the scrollbar shift, flip-shift-clamp
  for anchored overlays, SC 2.4.11 focus obscuring, the dismissal contract per
  overlay type, three stacking tiers with a depth limit of two, overlay
  elevation, and a toast budget.
- **`references/data-display.md`, 9 rules.** Tables were absent. Chrome,
  alignment, three row densities, sticky header and identity column, which
  column may truncate and why `title` is not a fallback, status as shape plus
  word, selection without layout shift, `aria-sort`, and keeping the columns
  while loading or empty.
- **`references/ai-tells.md`, 10 rules.** The mechanical markers of agent-built
  UI, as a detection layer: one spacing value, one shadow, borders instead of
  surfaces, hover without press, centring as the default axis, the feature-grid
  reflex, load animations, mixed icon sets, three form tells, and happy-path
  only. Each carries a greppable cue and a threshold, and points at the rule
  that fixes it. `interface-craft.md → default-tells` keeps the aesthetic
  defaults.

### Changed

- Boundaries table names `mobile-native`, `animate` and `stageshow`, so the
  skill stops where each of those starts. Phone platform behaviour is
  deliberately absent: `mobile-native` owns it.
- `border-discipline` carries the sub-pixel hairline question, which is a device
  question rather than a style one.
- `press-scale` states what the press does on a device with no hover.
- `default-tells` gains the fourth aesthetic default.

## [1.1.0] / 2026-08-28

### Fixed

- **`SKILL.md` could not be installed.** The `description` value contained
  `": "`, which YAML reads as a nested mapping, so `npx skills add` skipped the
  file and reported "No valid skills found". The value is now quoted. Every
  install route that parses the frontmatter was affected.

### Added

- **Six sub-skills**, each running one part of the skill on demand:
  `/ordinary-interfaces:read-project`, `:accessibility`, `:review`,
  `:new-screen`, `:contrast` and `:find-rule`. They carry `disable-model-invocation`, so they stay out of the way
  until invoked; the main skill still loads itself when a task calls for it.

## [1.0.0] / 2026-08-24

First public release.

### Added

- **180 rules** across 14 reference files: color, typography, spacing and layout,
  interaction, surfaces, interface craft, depth and icons, motion, states,
  accessibility, a11y implementation, writing, composition, UX laws, and one file
  of non-screen material kept explicitly outside the UI focus.
- **Evidence grading** on every number (`[spec]`, `[measured]`, `[convention]`)
  with primary sources cited inline.
- **Ten critical rules**, seven of them stated in `SKILL.md` as the
  non-negotiables checked before anything ships.
- **`match-the-project` precedence.** The project's own system outranks every
  reference default, enforced by `scripts/project-system.py` as step 0.
- **`contrast.py`.** WCAG 2.2 ratio, AA/AAA verdicts for text and UI components,
  and `--fix` to walk a foreground to the nearest passing value at constant hue.
- **`project-system.py`.** Detects token families, radius and spacing scales,
  color notation, type sizes, breakpoints, motion durations and curves, and
  whether `:focus-visible`, `prefers-reduced-motion` and `tabular-nums` appear.
- **`build-index.py`.** `RULE_INDEX.md` is generated from the rule headings, so
  it cannot drift from the rules.
- Claude Code **plugin and marketplace manifests**.

[1.1.0]: https://github.com/Board-ly/ordinary-interfaces/releases/tag/v1.1.0
[1.0.0]: https://github.com/Board-ly/ordinary-interfaces/releases/tag/v1.0.0
