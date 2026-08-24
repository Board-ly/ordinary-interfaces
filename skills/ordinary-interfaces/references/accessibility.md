# Accessibility: WCAG 2.2 Cross-Index

The WCAG rules live with their subject matter. This file is the map: find the
success criterion, go to the file that covers it. Everything here is `[spec]`.

## The audit order

Run in this order, a failure high in the list makes the ones below it moot.

| # | Check | SC | Where |
|---|---|---|---|
| 1 | Text contrast 4.5:1 / 3:1 | 1.4.3, 1.4.11 | `color.md → wcag-contrast` |
| 2 | Information never by color alone | 1.4.1 | `color.md → wcag-contrast`, `red-green-color-blindness` |
| 3 | Text alternatives on all non-text content | 1.1.1 | `interaction.md → wcag-images` |
| 4 | Pointer targets ≥24×24, primary 44×44 | 2.5.8, 2.5.5 | `interaction.md → touch-target` |
| 5 | Visible focus, 2px/2px, 3:1 | 2.4.11 | `interaction.md → button-design` |
| 6 | Flashing ≤3/s; motion disableable | 2.3.1, 2.3.3 | `interaction.md → wcag-motion` |
| 7 | Reflow at 320px, no 2D scroll | 1.4.10 | `spacing-layout.md → wcag-layout` |
| 8 | Text resize to 200% | 1.4.4 | `typography.md → wcag-typography` |
| 9 | Text spacing overrides do not break layout | 1.4.12 | `typography.md → wcag-typography` |
| 10 | Every input labelled; errors described in text | 3.3.1, 3.3.2 | `interaction.md → wcag-forms` |
| 11 | Descriptive page title; link purpose in context | 2.4.2, 2.4.4 | `interaction.md → wcag-navigation` |
| 12 | Consistent navigation and identification | 3.2.3, 3.2.4 | `interaction.md → wcag-navigation` |
| 13 | Orientation not locked | 1.3.4 | `spacing-layout.md → wcag-layout` |
| 14 | Drag has a single-pointer alternative | 2.5.7 | `spacing-layout.md → wcag-layout` |
| 15 | Redundant entry avoided; auth without cognitive test | 3.3.7, 3.3.8 | `interaction.md → wcag-forms` |
| 16 | Hover/focus content dismissible, hoverable, persistent | 1.4.13 | `color.md → wcag-contrast` |
| 17 | Real text over images of text | 1.4.5 | `typography.md → wcag-typography` |

## By success criterion

**Perceivable.** 1.1.1 alt text · 1.3.4 orientation · 1.4.1 use of color ·
1.4.3 contrast minimum · 1.4.4 resize text · 1.4.5 images of text · 1.4.8 visual
presentation (AAA: 80 CPL, 1.5 line-height, no justify) · 1.4.10 reflow · 1.4.11
non-text contrast · 1.4.12 text spacing · 1.4.13 content on hover or focus

**Operable.** 2.2.2 pause stop hide · 2.3.1 three flashes · 2.3.3 animation from
interactions (AAA) · 2.4.2 page titled · 2.4.4 link purpose · 2.4.6 headings and
labels · 2.4.11 focus not obscured · 2.5.5 target size enhanced (AAA, 44×44) ·
2.5.7 dragging movements · 2.5.8 target size minimum (24×24)

**Understandable.** 3.2.3 consistent navigation · 3.2.4 consistent
identification · 3.3.1 error identification · 3.3.2 labels or instructions ·
3.3.3 error suggestion · 3.3.7 redundant entry · 3.3.8 accessible authentication

## Code-level checks (reviewing markup, JSX, or components)

The rules above are design constraints. These are the failures that only show up
in code, ordered by severity. Source: the Rams review protocol in
`design-engineering`.

**Critical: must fix:**

| Check | SC | Look for |
|---|---|---|
| Image without alt | 1.1.1 | `<img>` with no `alt` attribute |
| Icon-only button with no name | **4.1.2** | `<button>` containing only an SVG, no `aria-label` |
| Input without a label | 1.3.1 | `<input>`/`<select>`/`<textarea>` with no label or `aria-label` |
| Non-semantic click target | **2.1.1** | `<div onClick>` with no `role`, `tabIndex`, or `onKeyDown` |
| Link without href | **2.1.1** | `<a>` driven only by `onClick`, not keyboard reachable, not in the links list |

**Serious:**

| Check | SC | Look for |
|---|---|---|
| Focus outline removed | **2.4.7** | `outline: none` with no visible replacement |
| Missing keyboard handler | 2.1.1 | interactive `onClick` with no `onKeyDown` |
| Color-only information | 1.4.1 | status or error carried by color alone |
| Touch target under 44×44 | 2.5.5 | see the note below |

**Moderate:**

| Check | SC | Look for |
|---|---|---|
| Skipped heading level | 1.3.1 | `h1` → `h3` |
| Positive `tabIndex` | **2.4.3** | `tabIndex > 0`, overrides natural order and is almost always a bug |
| Role missing required attributes | 4.1.2 | `role="button"` without `tabIndex="0"` |

**A note on the 44×44 line.** SC 2.5.5 is **AAA**; the AA floor is 24×24
(SC 2.5.8). Treating 44×44 as a "serious" finding is a stricter house standard
than WCAG AA requires, a defensible one, since 44 is also the Apple HIG minimum,
but report it as a house standard rather than as an AA violation. See
`interaction.md → touch-target`.

## Baseline facts worth stating in an audit

From WebAIM Million 2024, on tested homepages `[measured]`:

| Failure | Share of homepages |
|---|---|
| Low contrast text | **>80%** |
| Missing image alt text | **>54%** |
| Missing form labels | **>45%** |

These are the failures to check first, because they are the failures that
actually happen. Missing or inadequate focus indicators also rank among the top
failures.

## What automated tools can and cannot do

- **Reliable:** axe and WAVE catch structural failures, missing labels, missing alt attributes, computable contrast on solid backgrounds.
- **Not reliable:** alt text *quality* (an alt of `"image"` passes structurally and fails 1.1.1 in substance); contrast over gradients, images, or semi-transparent overlays; whether a color-coded state has a genuine second channel; whether reflow preserves *functionality* rather than merely avoiding a scrollbar.
- **Visual inspection is not a valid test for flashing.** Use PEAT.

Say which findings are tool-verified and which are judgement.

## Scope and honesty

- **WCAG 2.2 Level AA is the current legal benchmark in most jurisdictions as of 2026.** AAA criteria are marked as such. Do not report an AAA miss as a violation.
- **APCA is not normative for WCAG 2.x** and cannot substitute for it in an audit or legal context. A value passing WCAG can fail APCA; use APCA additively for insight.
- Genuine exemptions exist and flagging them is noise: decorative elements, inactive components, logotypes (contrast); maps, diagrams, video, data tables, and manipulation toolbars (reflow); essential orientations and essential animation. Check the exemption before writing the finding.
