---
name: ordinary-interfaces
description: 'Evidence-graded UI constraints with concrete numbers: contrast, type scale, line length, spacing and grids, hit areas, component states, animation duration and easing, surfaces and radius, tokens, icons, empty/loading/error states, and interface copy. Use when choosing a UI value (how much padding, which line-height, what contrast, how big a tap target, how long an animation, what radius on a nested card), when auditing a screen, component, CSS, or JSX for design and WCAG 2.2 problems, when building or reviewing a design system, tokens, or component states, and when someone asks whether a UI "looks right" and the answer needs to be defensible instead of taste. Reference values only. design-engineering and frontend-design own aesthetic direction, sad-paths owns the state-audit workflow.'
---

# Ordinary Interfaces

180 UI rules with hard numbers, graded by how well each is actually evidenced.

The point is not to have opinions about design. It is to replace "this feels a
bit tight" with "container padding must exceed the sibling gap, heuristic 1.5×,
so a 16px gutter needs ≥24px padding (`padding-gap-ratio`)."

**Ordinary is the goal, and it is not the same as generic.** An ordinary
interface is unremarkable *in use*. It behaves the way people already expect
(`jakobs-law`), it matches the system the project already has
(`match-the-project`), its hit areas are where fingers go, its errors appear
where the user is looking. That is the whole content of this skill: the
accumulated, checkable defaults that let an interface get out of the way.

Generic is the opposite failure, reaching for the same warm-cream-and-terracotta
palette regardless of subject, the same three-column card grid, because nothing
was decided (`default-tells`). Ordinary is decided; it just doesn't announce
itself. Where an interface should be distinctive, that judgement lives in
`frontend-design` and `design-engineering`, not here. This skill makes sure the
thousand small things underneath are right, so the one distinctive thing has
somewhere to stand.

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

Six sub-skills run one part of this on demand, without pulling in the whole
skill. Reach for one when the task is a single step rather than a whole review.

| Command | Does |
|---|---|
| `/ordinary-interfaces:read-project` | Step 0 above, on its own |
| `/ordinary-interfaces:accessibility` | The seven non-negotiables only, pass/fail/unverified |
| `/ordinary-interfaces:review` | The full audit below, in the documented format |
| `/ordinary-interfaces:new-screen` | The build workflow below |
| `/ordinary-interfaces:contrast` | A colour pair through `contrast.py`, with `--fix` |
| `/ordinary-interfaces:find-rule` | One rule by id: value, grade, and where it stops applying |

## Routing

Load only what the task touches.

| Working on | Read |
|---|---|
| Palette, ramps, tokens, dark mode, contrast | `references/color.md` |
| Type scale, line height, measure, wrapping, web font details | `references/typography.md` |
| Padding, gaps, grids, breakpoints, RTL, translation growth | `references/spacing-layout.md` |
| Buttons, links, inputs, forms, nav, component states | `references/interaction.md` |
| Radius, shadows, image outlines, press feedback, theme switch | `references/surfaces.md` |
| Elevation, borders, depth strategy, tokens, defaults | `references/interface-craft.md` |
| Shadows, elevation scale, icon sizing, stroke, optical alignment | `references/depth-and-icons.md` |
| Animation, easing, duration, transitions, gestures | `references/motion.md` |
| Empty, loading, error, partial, overflow, offline states | `references/states.md` |
| Focus, keyboard, ARIA, live regions, hit areas, implementation | `references/a11y-implementation.md` |
| WCAG success criteria, audit order, code-level checks | `references/accessibility.md` |
| Button labels, errors, empty-state copy, capitalization | `references/writing.md` |
| Hierarchy, emphasis, focal points, charts, radius tone | `references/composition.md` |
| Choice counts, memory load, attention, optical centre | `references/ux-laws.md` |
| Print, packaging, logo, photography (**outside the UI focus**) | `references/beyond-screen.md` |
| Finding a rule by name | `RULE_INDEX.md` |

## Building a screen

1. **Run `project-system.py`.** Adopt what exists before adding anything.
2. Read the non-negotiables. They constrain the solution space before you draw.
3. Load the reference files for the surfaces involved.
4. **Take values from the project, then the reference, never from memory.** The
   whole point is that these numbers are checked. Guessing "probably 1.4
   line-height" defeats it.
5. Work greyscale first. If hierarchy fails without color, color will not fix it
   (`greyscale`). Then apply the 60-30-10 split.
6. **Enumerate the non-happy states before writing markup** (`state-ledger`) and
   build the hardest one first. A layout that survives its worst state survives
   its best; the reverse is not true.
7. Verify contrast with `scripts/contrast.py` before claiming a pair passes.

## Auditing a screen, component, CSS, or screenshot

Run `project-system.py` first, then produce a checklist ordered
`critical → high → medium → low`. For each finding: rule id, what is wrong, the
concrete fix, the number.

```
CRITICAL  wcag-contrast      #777777 label on #fff is 4.48:1, fails AA (needs 4.5:1)
                             → #767676 or darker; separate token for text vs border
HIGH      concentric-radius  Card is rounded-xl with p-2, inner is rounded-xl
                             → outer 24px = inner 16px + 8px padding
HIGH      line-length        Article body runs 108 CPL at 1440px
                             → max-width: 65ch on the container
MEDIUM    padding-gap-ratio  Card padding 16px equals the 16px grid gutter
                             → 24px padding (1.5× heuristic)
```

Rules for the audit:

- **Do not invent findings to fill the list.** An empty CRITICAL section is a result, and saying so plainly beats padding.
- **Do not score the design out of 10.** There is no evidence base for that number and it obscures which fixes matter.
- **Check the `When It Breaks` notes before flagging.** Full-bleed media, dense data tables, disabled controls and decorative elements have real exemptions, and flagging them is noise that trains people to ignore the whole audit.
- **Say what you could not verify.** With only CSS or a description, separate verified findings from inferred ones. Replay motion at 10% speed before judging it; what feels off at 10% is what is subtly wrong at full speed.
- **One row per root cause**, listing every location it appears in, rather than one row per occurrence.

## Scripts

```bash
python3 .claude/skills/ordinary-interfaces/scripts/project-system.py .          # step 0, always
python3 .claude/skills/ordinary-interfaces/scripts/contrast.py "#777" "#fff"    # ratio + AA/AAA
python3 .claude/skills/ordinary-interfaces/scripts/contrast.py "#a5a8f0" "#fff" --fix
```

`contrast.py` reports the ratio and pass/fail for normal text, large text and UI
components; `--fix` walks the foreground to the nearest passing value, keeping
hue. Both are dependency-free and read-only.

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
| `dataviz` | Chart palettes, encodings, dashboards. The one chart rule here (`pie-chart-problem`) is only the perceptual-accuracy ranking |

Two things to keep straight:

- **Numbers here, taste there.** If a value in this skill would produce a competent-but-generic result, that is the skill working as intended. Nothing here tells you what the design should *be*.
- **Not a substitute for looking.** Every optical rule (icon centering, optical center, simultaneous contrast, elevation) ends in "verify visually". The numbers are a starting point; the eye is the check.
