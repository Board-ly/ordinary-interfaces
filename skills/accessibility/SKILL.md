---
name: accessibility
description: 'Checks only the seven non-negotiables from ordinary-interfaces: contrast, never colour alone, hit areas, text alternatives, visible focus, motion safety, and reflow. These are accessibility floors with legal weight, not the aesthetic conversation. Use as the ship gate before release.'
argument-hint: '[file, component, or path]'
disable-model-invocation: true
allowed-tools: Bash Read Glob Grep
---

# The seven gates

Check `$ARGUMENTS` against the seven non-negotiables and nothing else. This is a
pass/fail on the floors, not a design review. For the full review use
`/ordinary-interfaces:review`.

Read `references/accessibility.md` and `references/a11y-implementation.md` from
the ordinary-interfaces skill for the detail behind each one.

1. **Contrast.** 4.5:1 normal text, 3:1 large text (≥24px regular / ≥18.66px
   bold) and UI components. Measure the rendered value, at the worst point of any
   gradient, in both themes independently. Verify with
   `python3 .claude/skills/ordinary-interfaces/scripts/contrast.py "#fg" "#bg"`
   rather than by eye. `wcag-contrast`
2. **Never colour alone.** Every colour-coded state needs a second channel: text,
   icon, underline, pattern. `red-green-color-blindness`, SC 1.4.1
3. **Hit areas.** 24×24px floor (SC 2.5.8); 44×44 touch and 40×40 desktop are the
   real targets, 8px between. Padding counts. `touch-target`,
   `hit-area-extension`
4. **Text alternatives.** Every informational image, icon button and chart.
   Functional images name the action ("Search", not "magnifying glass").
   `wcag-images`, `alt-by-purpose`
5. **Visible focus.** `:focus-visible` styled, never `outline: none` without a
   verified replacement. 2px outline, 2px offset, 3:1 against every adjacent
   colour. `focus-visible`, `button-design`
6. **Motion.** Nothing flashes more than three times a second; non-essential
   animation sits behind `prefers-reduced-motion`, which means gentler rather
   than absent; every animated state change also needs a static cue.
   `wcag-motion`, `reduced-motion`, `motion-restraint`
7. **Reflow.** Works at 320 CSS px (1280px at 400% zoom) without two-dimensional
   scrolling, and at 200% text zoom. `wcag-layout`

## Reporting

One line per gate: `PASS`, `FAIL` with the measured value and the fix, or
`UNVERIFIED` with what you would need to check it. A gate you could not test from
the material given is `UNVERIFIED`, never `PASS`.

Close with a single verdict sentence. All seven pass or they do not; there is no
score and no partial credit. A house convention does not repeal WCAG, so a
project system that conflicts with a gate loses.
