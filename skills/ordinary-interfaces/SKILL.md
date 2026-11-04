---
name: ordinary-interfaces
description: 'Evidence-graded UI constraints with concrete numbers: contrast, type scale, line length, spacing and grids, hit areas, component states, animation duration and easing, surfaces and radius, tokens, icons, empty/loading/error states, and interface copy. Use when choosing a UI value (how much padding, which line-height, what contrast, how big a tap target, how long an animation, what radius on a nested card), when auditing a screen, component, CSS, or JSX for design and WCAG 2.2 problems, when building or reviewing a design system, tokens, or component states, and when someone asks whether a UI "looks right" and the answer needs to be defensible instead of taste. Reference values only. design-engineering and frontend-design own aesthetic direction, sad-paths owns the state-audit workflow.'
---

# Ordinary Interfaces

202 UI rules with hard numbers, graded by how well each is actually evidenced.

The point is not to have opinions about design. It is to replace "this feels a
bit tight" with "container padding must exceed the sibling gap, heuristic 1.5×,
so a 16px gutter needs ≥24px padding (`padding-gap-ratio`)."

**Ordinary is the goal, and it is not the same as generic.** Ordinary is
unremarkable *in use*: it behaves the way people already expect (`jakobs-law`)
and matches the system the project already has (`match-the-project`). Generic is
the same warm-cream palette and three-column card grid whatever the subject,
because nothing was decided (`default-tells`). Ordinary is decided; it just does
not announce itself. Where an interface should be distinctive, that judgement
lives in `frontend-design` and `design-engineering`, not here.

## Step 0: read the project's system first

**Run this before quoting any default:**

```bash
python3 .claude/skills/ordinary-interfaces/scripts/project-system.py .
```

It reports what the codebase already decided: token families, radius and spacing
scales, colour notation, type sizes, breakpoints, motion durations and curves,
plus whether `:focus-visible`, `prefers-reduced-motion` and `tabular-nums` appear
at all. On a shadcn project it will point you at `npx shadcn@latest info --json`
for resolved paths and installed components.

**`match-the-project` is the highest-precedence rule in this skill.**

- **Where the project has a scale, match it.** A 7px radius in a system built on 7px is correct; "should be 8px per the grid" is noise.
- **Where the project has none, the reference values apply.**
- **Reuse the project's notation and tokens.** A second colour representation added to fix one value makes the palette harder to reason about. A consistent hex system beats hex with `oklch()` scattered through it.
- **A finding is "this breaks the project's own system" first, and "this differs from the reference" only second.** The first is nearly always the more useful sentence.

The exceptions that override the project: the seven non-negotiables below, and
anything tagged `[spec]`. A house convention does not repeal WCAG.

## Three rules of use

**1. Carry the evidence grade.** Every number is tagged:

| Tag | Meaning | How to speak about it |
|---|---|---|
| `[spec]` | Normative: WCAG 2.2, ISO, OpenType | "required", "fails AA" |
| `[measured]` | From a study, with the sample where it matters | "measured at", cite the finding |
| `[convention]` | Industry practice, no primary source | "convention is", "a reasonable default" |

Never launder a `[convention]` into a law. The 8pt grid and the 1.5× padding
ratio are conventions with good reasoning, not perceptual facts, and saying
otherwise is how design advice stops being trustworthy. Equally: do not hedge a
`[spec]`. 4.5:1 is not a preference.

**2. Critical rules are gates.** The seven below are checked before anything
ships. They are accessibility floors with legal weight in most jurisdictions, not
part of the aesthetic conversation.

**3. Cite the rule id.** Write `(touch-target)` or `(concentric-radius)` after a
claim so the reader can check it. Ids are in `RULE_INDEX.md`.

## The seven non-negotiables

Details in `references/accessibility.md`.

1. **Contrast.** 4.5:1 normal text, 3:1 large text (≥24px regular / ≥18.66px bold) and UI components. Measure the rendered value, worst point of any gradient, both themes independently. `wcag-contrast`
2. **Never color alone.** Every color-coded state needs a second channel: text, icon, underline, pattern. ~8% of men cannot separate red from green. `red-green-color-blindness`, SC 1.4.1
3. **Hit areas.** 24×24px floor (SC 2.5.8), 44×44 touch / 40×40 desktop the real target, 8px between. Padding counts. `touch-target`, `hit-area-extension`
4. **Text alternatives.** Every informational image, icon button and chart. Functional images name the **action** ("Search", not "magnifying glass"). `wcag-images`, `alt-by-purpose`
5. **Visible focus.** Style `:focus-visible`, never `outline: none` without a verified replacement. 2px outline, 2px offset, 3:1 against every adjacent color. `focus-visible`, `button-design`
6. **Motion.** Nothing flashes >3×/second; non-essential animation sits behind `prefers-reduced-motion`, which means *gentler*, not *absent*; **every animated state change also needs a static cue**. `wcag-motion`, `reduced-motion`, `motion-restraint`
7. **Reflow.** Works at 320 CSS px (1280px at 400% zoom) without 2D scrolling, and at 200% text zoom. `wcag-layout`

## Commands

Seven sub-skills run one part of this on demand, without pulling in the whole
skill. Reach for one when the task is a single step rather than a whole review.

| | Does |
|---|---|
| `scan` | Step 0 above, on its own |
| `a11y` | The seven non-negotiables only, pass/fail/unverified |
| `review` | The full audit, in the documented format |
| `build` | The workflow for new UI |
| `contrast` | A colour pair through `contrast.py`, with `--fix` |
| `space` | Padding against the gap it contains, and the scale in use |
| `rule` | One rule by id: value, grade, and where it stops applying |

All seven take the `/ordinary-interfaces:` prefix. `scan`, `contrast`, `space`
and `rule` are available without being asked for; the three workflows are not.

## Routing

Load only what the task touches.

| Working on | Read |
|---|---|
| Palette, ramps, tokens, dark mode, contrast | `references/color.md` |
| Type scale, line height, measure, wrapping, web font details | `references/typography.md` |
| Padding, gaps, grids, breakpoints, RTL, translation growth | `references/spacing-layout.md`, measured by `space` |
| Buttons, links, inputs, forms, nav, component states | `references/interaction.md` |
| Tooltips, popovers, menus, dialogs, sheets, toasts, backdrops | `references/overlays.md` |
| Radius, shadows, image outlines, press feedback, theme switch | `references/surfaces.md` |
| Elevation, borders, depth strategy, tokens, defaults | `references/interface-craft.md` |
| Shadows, elevation scale, icon sizing, stroke, optical alignment | `references/depth-and-icons.md` |
| Animation, easing, duration, transitions, gestures | `references/motion.md` |
| Empty, loading, error, partial, overflow, offline states | `references/states.md` |
| Tables, row density, sticky chrome, cell truncation, status columns | `references/data-display.md` |
| Focus, keyboard, ARIA, live regions, hit areas, implementation | `references/a11y-implementation.md` |
| WCAG success criteria, audit order, code-level checks | `references/accessibility.md` |
| Button labels, errors, empty-state copy, capitalization | `references/writing.md` |
| Hierarchy, emphasis, focal points, charts, radius tone | `references/composition.md` |
| Choice counts, memory load, attention, optical centre | `references/ux-laws.md` |
| Whether a UI reads as agent-built, with greppable cues | `references/ai-tells.md` |
| Finding a rule by name | `RULE_INDEX.md` |

## Workflows

Both of these live in their own sub-skill rather than here, so running one costs
the workflow and not this file.

| | |
|---|---|
| Building new UI | `/ordinary-interfaces:build` |
| Auditing existing UI | `/ordinary-interfaces:review` |

The short version of both: run `project-system.py`, let the seven gates
constrain the solution space before drawing, load only the reference files the
surfaces touch, take values from the project first and the reference second,
never from memory, and measure contrast rather than estimating it.

## Scripts

`project-system.py` is step 0 above. `contrast.py` reports the ratio and
pass/fail for normal text, large text and UI components, with `--fix` walking
the foreground to the nearest passing value while keeping hue. `spacing.py`
pairs a container's padding with the gap between its children wherever both
sit on one element, on the axis the gap actually separates. All three are
dependency-free and read-only.

```bash
python3 .claude/skills/ordinary-interfaces/scripts/contrast.py "#777" "#fff"
python3 .claude/skills/ordinary-interfaces/scripts/contrast.py "#a5a8f0" "#fff" --fix
python3 .claude/skills/ordinary-interfaces/scripts/spacing.py src
python3 .claude/skills/ordinary-interfaces/scripts/spacing.py --pair 16 24
```

## Boundaries with the other design skills

This skill holds **checkable constraints**: values, thresholds, and the
exemptions to them. It does not carry the process or philosophy those constraints
came from. Reach for the source skill when the question is *how to decide*
rather than *what the value is*.

| Go to | For |
|---|---|
| `design-engineering` | Intent-first questioning, domain exploration, the signature test, pre-build checkpoint, Rams review format |
| `sad-paths` | The state-audit workflow, its critical gate, hostile fixtures, agentic surfaces, and `scripts/scan.py`. **Run that scanner rather than grepping for missing states by hand** |
| `frontend-design` | Aesthetic direction for a brief, taking a justified risk |
| `dataviz` | Chart palettes, encodings, dashboards. The one chart rule here (`pie-chart-problem`) is only the perceptual-accuracy ranking. `data-display.md` holds tables, which are UI rather than charts |
| `mobile-native` | Platform behaviour on a phone: safe areas, tap highlight, viewport units, touch-action, keeping the keyboard open. **This skill deliberately holds none of it.** `dialog-to-sheet` and `sheet-drag-contract` are the overlap, and they stop at the overlay |
| `animate` | Motion craft, interruptibility, how to build a specific transition. `motion.md` holds the durations and the easing bands only |
| `scroll-animations` | Scroll-linked and scroll-triggered motion, `animation-timeline`, thresholds. This skill holds one position on it, in `ai-tells.md → load-animation-on-everything`: content above the fold does not animate in |
| `stageshow` | Faux UI for marketing stills, demos and bento grids. Nothing here applies to an interface that is a picture of an interface |
| `beyond-screen` | Print, packaging, logo and photography. These were an appendix here until 2.0.0. `viewing-distance` and `visual-angle-arcminutes` are the overlap: a screen read from further away than a desk takes its minimum type size from there |

Two things to keep straight:

- **Numbers here, taste there.** If a value in this skill would produce a competent-but-generic result, that is the skill working as intended. Nothing here tells you what the design should *be*.
- **Not a substitute for looking.** Every optical rule (icon centering, optical center, simultaneous contrast, elevation) ends in "verify visually". The numbers are a starting point; the eye is the check.
