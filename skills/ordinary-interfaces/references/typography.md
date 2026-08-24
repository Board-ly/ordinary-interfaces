# Typography

23 rules. Measure, leading and hierarchy carry the reading experience; the rest
is craft and delivery.

---

## `type-hierarchy`: Build the Scale From a Ratio · high

> Pick one ratio, generate every size from it, and never skip a heading level.

**Numbers.** A modular scale at **1.25** (major third) is the web default: 16px
body yields 20, 25, 31, 39, **49**. On mobile 1.25 compounds too fast, drop to
**1.20** and cap at three levels. The floor for a readable category break is
about **1.20** `[convention]`.

**Why it holds.** Size perception is roughly logarithmic, so a fixed pixel
addition does not produce a fixed perceptual step: +2px reads as a rendering
wobble, not a level. Skipping heading levels is a separate failure with a
separate cost: screen readers navigate by level, and a gap reads as content
that failed to load (W3C WAI) `[spec]`.

**In code.** Two custom properties run the whole scale, `--base: 1rem` and
`--ratio: 1.25`. Prefer `rem` or `clamp()`: `px` honours browser zoom but ignores
the reader's OS font-size preference. Below H4, separate levels by weight and
color rather than by shrinking further.

---

## `line-length`: Cap the Measure · high

> `max-width: 65ch` on anything anyone will read a paragraph of.

**Numbers.**

| Value | Meaning |
|---|---|
| 50–75 CPL | comfortable range for body text |
| ~66 CPL | the commonly cited optimum (Bringhurst, *The Elements of Typographic Style*, 1992) |
| **80 CPL** | hard ceiling, WCAG 2.2 SC 1.4.8, 40 for CJK `[spec]` |
| 30–50 CPL | typical on mobile |

**Why it holds.** The return sweep is the expensive movement in reading: the
longer the line, the more often the eye lands on the wrong one coming back. Past
roughly 80 characters, the start of a sentence has begun to decay before its end
arrives. Under 45 the opposite failure appears, meaning fragments and sweep
count climbs.

**Where it doesn't.** Buttons, navigation and microcopy are outside this
entirely. Editorial display text runs 30–45 deliberately.

**In code.** `ch` is the width of a zero, so 65ch lands somewhere around 60–75
actual characters depending on the face, close enough, and it adapts to font
size for free.

---

## `line-height`: Leading Runs Inverse to Size · high

> Bigger text, tighter leading. Set it unitless.

**Numbers.**

| Text | Leading |
|---|---|
| Headings (H1–H3) | 1.1–1.3 |
| Body, 16–18px | 1.5–1.6 |
| Small, 12–14px | 1.5–1.7 |
| Narrow columns (<40 CPL) | 1.3–1.45 |
| Mobile body | 1.4–1.5 |

**Why it holds.** Leading exists to make the return sweep unambiguous, and the
sweep gets harder as lines get longer, not as type gets bigger, so a headline
needs proportionally less and a small-text column needs more. The browser default
of 1.2 is below the floor for body text; lines visibly merge.

**In code.** Unitless (`1.5`, not `1.5em`) so it scales correctly through
children. Note that WCAG SC 1.4.12 requires the layout to **survive** a
user-imposed 1.5 override `[spec]`. That is a robustness requirement on the
implementation, not an instruction to ship 1.5 as the design value.

---

## `three-line-leading`: Leading Floor for Wrapping Text · high

> Anything that wraps to three lines or more gets at least 1.4, whatever the row
> height wants.

**Why it holds.** Tight leading is affordable on one or two lines because there
is no sustained sweep to support. At three lines it becomes a block of text, and
a block of text at `leading-none` is a readability bug regardless of how well it
fits the card.

This is the most common leading failure in component libraries, and it hides
because the design mock had a two-line description.

---

## `text-alignment`: Left, With Few Exceptions · high

> Body copy is left-aligned in LTR. Centered text stops at three lines. Numbers
> go right.

**Numbers.** Centered text: **1–3 lines maximum**. Justified: avoid on the web,
it can fail WCAG 2.2 F88 / SC 1.4.8 (AAA) `[spec]`.

**Why it holds.** The return sweep needs a fixed anchor, and left alignment
supplies one on every line. Justification removes that reliability by varying
word spacing, producing rivers of white that worsen above 200% zoom, and the web
lacks the hyphenation control that makes justification work in print. Ling & van
Schaik (2007, n=65) measured better accuracy and response time on left-aligned
text than justified `[measured]`, **while participants reported preferring
justified**. Preference and performance diverge here, so do not settle it by
survey.

**In code.** Right-align numeric columns, headers included, so place value lines
up. Set RTL with `dir="rtl"` in markup rather than flipping alignment by hand.
Scope any justification to `@media print` with `hyphens: auto`.

---

## `font-weight-contrast`: Two Steps Between Levels · high

> Body 400, headings 600 or above. Adjacent weights do not read as rank.

**Numbers.** At least **200 units** apart on the 100–900 scale `[convention]`.
Three levels covers most systems: 400, 600, 700–800. Reserve 900 for display.

**Why it holds.** Weight contrast is relative, not absolute. A 500 next to a 400
occupies the same perceptual category and reads as inconsistency rather than
hierarchy, Gestalt similarity groups near-identical weights as equivalent
instead of ranking them. Enough separation pushes them into distinct groups,
where rank becomes readable.

**Where it doesn't.** Two-weight families (400/700) clear the gap automatically.
Display contexts can use adjacent weights when a large size difference carries
the hierarchy instead, 48px/500 over 16px/400 reads as distinct.

**Note.** WCAG treats bold ≥14pt or regular ≥18pt as large text, relaxing
contrast from 4.5:1 to 3:1 `[spec]`, weight has an accessibility consequence,
not just a visual one.

---

## `weight-size-floor`: Weight Floors by Size · high

> Nothing under 400 below 18px. Nothing under 300 outside display.

**Numbers.** Below **18px**, weight **400 or heavier**. Weights under **300** are
display-only, at **28px+**. Long-form body starts at **16px**; UI text can go to
**14px** for inputs and menus, **13px** for captions, and rarely below **12px**.

**Why it holds.** Thin strokes lose to anti-aliasing and pixel grids before they
lose to the eye. A 200-weight at 14px is not subtle, it is partially missing.

**Where it doesn't.** Moving off a 16px body baseline is fine for a nameable
reason, the face runs small, the measure is narrow, the product is a dense
professional tool. "It looked cleaner" is not one.

---

## `x-height`: Perceived Size Is X-Height · medium

> Two faces at the same point size are not the same size.

**Numbers.** X-height typically runs **45–75% of cap height**, varying widely by
face. Over **90% of running text is lowercase** (Jones & Mewhort, corpus
analysis, 2004) `[measured]`.

**Why it holds.** If nine tenths of what people read sits between baseline and
x-height, that distance (not cap height, not point size) is what determines
apparent size and small-size legibility.

**In code.** Under 14px, choose a high x-height face (Inter, Verdana) over a low
one (Garamond). Above about 67% the gain reverses: ascender and descender
distinction compresses and `h` versus `n` gets harder.

---

## `font-pairing`: Match Proportion, Contrast Function · medium

> Similar x-heights, clearly different jobs. Two faces, rarely three.

**Numbers.** **Maximum two typefaces** in a system `[convention]`; rarely more
than three anywhere.

**Why it holds.** Pairs fail in two directions. Too similar and there is no
hierarchy; it reads as indecision, or as a mistake. Too different and the system
fragments. Matching x-heights keeps running text harmonious even when the styles
diverge, which is why superfamilies (IBM Plex, Source) are the safe route: shared
metrics by construction.

**Where it doesn't.** Display faces survive about three lines of body text before
readability collapses. Keep them for short accents.

---

## `wcag-typography`: Text Must Survive the Reader · high `[spec]`

> The layout does not break when someone zooms to 200% or overrides spacing.

**Numbers**, WCAG 2.2:

| SC | Requirement |
|---|---|
| 1.4.4 (AA) | text resizes to **200%** without loss of content or function |
| 1.4.5 (AA) | real text, not images of text, logotypes excepted |
| 1.4.12 (AA) | nothing breaks when the reader sets line-height ≥**1.5×**, paragraph spacing ≥**2×**, letter-spacing ≥**0.12×**, word-spacing ≥**0.16×** |

**Why it holds.** Readers with low vision routinely work at 200%+; readers with
dyslexia routinely override spacing. Both are common, both are one browser
setting away, and a rigid container turns either into an unusable page. Note that
1.4.12 does not ask the design to *use* those values, only to survive them.

**Where it breaks.** Fixed-height containers with `overflow: hidden` clip
reflowed text. Absolutely positioned elements collide at 200%. Single-line
navigation that cannot wrap forces horizontal scroll. Icon fonts standing in for
informational text cannot be restyled or read. Use SVG with a text alternative.
PDF, canvas and raster SVG text are out of scope for 1.4.12.

**In code.** Relative units throughout. `overflow-wrap: break-word` on text
containers. Test at 200% on every key screen, and use the Text Spacing
bookmarklet to apply all four overrides at once.

---

## `text-wrap`: Four Declarations, Four Jobs · high

| Declaration | Job |
|---|---|
| `text-wrap: balance` | even line lengths, **headings** |
| `text-wrap: pretty` | no orphan on the last line, **descriptions** |
| `overflow-wrap: break-word` | long words, URLs and IDs that would escape |
| `white-space: nowrap` | labels and badges where a break looks broken |

**Where it doesn't.** Skip `balance` and `pretty` in long-form text, they cost
layout work per paragraph and the benefit is a headline effect.

**Truncation:** `text-overflow: ellipsis` with `overflow: hidden` and
`white-space: nowrap` for one line, `line-clamp` for several. Truncation hides
content, so **keep the full value reachable** when it matters. Two rules from
`states.md → overflow-pressure` apply here too: never truncate a number, and a
two-line clamp beats a one-line ellipsis on titles.

---

## `letter-spacing-by-size`: Tracking Follows Size · medium

> Negative on large headings, positive on small caps labels, nothing on body.

**Why it holds.** Tracking is drawn into a face for its intended size. Scaled up,
the built-in spacing reads loose; scaled down and capitalised, it reads cramped.
The adjustment is a correction, not a style.

Consistent with `small-caps` (+0.05–0.08em) and `all-caps-fatigue`.

---

## `all-caps-fatigue`: Caps for Labels Only · medium

> Short labels, tags, single-line headings. Never a paragraph.

**Numbers.** All caps reads **9.5–19% slower** (Tinker, 1955, 20-minute print
study) `[measured]`, with roughly **12% more fixations** (Tinker, 1949). No
screen study replicates this at that precision, treat it as directional. It also
consumes materially more horizontal space (~35% is widely repeated, with no
confirmed primary source) `[convention]`.

**Why it holds.** Ascenders and descenders give words distinct silhouettes.
Capitals give every word the same rectangle, which removes word-shape recognition
and forces letter-by-letter processing.

**In code.** Always `text-transform: uppercase` rather than typing capitals, the
source stays mixed case, so screen readers (whose all-caps handling varies by
software and setting) receive the right input.

---

## `ios-input-zoom`: 16px Inputs on Mobile · high

> Below 16px, iOS Safari zooms the entire page on focus.

**Two fixes, which look different: ask which the design wants:**

1. **Size the input up on mobile.** `text-base sm:text-sm`. Changes the small-screen appearance.
2. **Hold `font-size: 16px` and render the intended size with `transform: scale()`**, compensating width and line-height. Identical at every viewport, more to maintain.

---

## `variable-fonts`: Worth It From Three Weights · medium

> Below three weights, a subsetted static file is usually smaller.

**Numbers.** The crossover sits at **3 or more weights** (Google / web.dev, 2020)
`[convention]`. The `wght` axis runs **1–1000** per OpenType 1.8; declare the
range in `@font-face` as `font-weight: 100 900`. Browser support is above **94%**
(Can I Use, 2026); IE11 has none.

**Why it holds.** One file, one request, and every intermediate instance
interpolated at render time. `opsz` additionally adjusts stroke contrast and
spacing per size range, replacing the separate optical cuts classical families
shipped as distinct fonts.

**Where it doesn't.** A variable font loaded for a single weight is typically
larger than a subsetted static one. Hinting at small sizes can trail
purpose-hinted static cuts depending on the face, test at 12–14px on Windows
Chrome. **Axes fail silently when absent**, so verify availability before
designing against one.

---

## `typeface-vs-font`: The Distinction That Matters in CSS · medium

> A typeface is the design; a font is one instance of it. CSS matches on the
> family name and picks the instance.

**Numbers.** `font-weight` 100–900 in CSS (1–1000 in OpenType); `font-stretch`
50–200%; five registered axes, `wght`, `wdth`, `ital`, `slnt`, `opsz`.

**Why it matters practically.** **Every family + weight + style combination needs
its own `@font-face`.** Without one, the browser *synthesizes*, thickening
strokes or slanting glyphs, and synthesized bold differs from a drawn bold at
the glyph level in ways that read as cheap without being nameable. Generic
keywords (`sans-serif`, `serif`, `monospace`) are classification categories, not
faces: no defined metrics, no glyph guarantees.

---

## `font-synthesis`: Load the Real Faces · high

> Ship the cuts the design uses. Do not let the browser invent them.

**Why it holds.** Synthesis is silent. Nothing errors, nothing logs, the type
just renders subtly wrong, and it renders wrong differently on each platform.

**Where it doesn't.** `font-synthesis: none` disables the invention, but **it
erases emphasis rather than reporting it**, bold simply stops looking bold. Set
it only after confirming every required bold, italic, small-cap, superscript and
subscript form stays distinct across the whole fallback stack.

---

## `css-properties-over-tags`: Properties Over Feature Tags · medium

> If a CSS property exists for it, use the property.

| Use | Not |
|---|---|
| `font-weight: 650` | `font-variation-settings: "wght" 650` |
| `font-optical-sizing: auto` | `font-variation-settings: "opsz" …` |
| `font-variant-numeric: tabular-nums` | `font-feature-settings: "tnum" 1` |

**Why it holds.** Properties degrade correctly when a non-variable fallback
renders; raw tags do not. Reserve the low-level syntax for custom axes
(`"GRAD" 80`) and niche features (`"ss01" 1`) that have no property.

**Delivery:** `.woff2` on the web, Brotli compression, universal support.
`.woff` is a legacy fallback; `.ttf` and `.otf` are desktop formats with no web
compression.

---

## `smart-punctuation`: Real Punctuation, Natural Case · medium

> Store text in natural case; control presentation in CSS.

- Curly quotes in prose, straight quotes in code.
- En dash for ranges: `2010–2020`.
- The single ellipsis character, not three periods.
- `&nbsp;` to hold `16 px` together across a break.
- `&shy;` to mark where a long word may break.

**Why the case rule.** Applying capitalisation with `text-transform` means a
redesign never becomes a copy rewrite, and it keeps screen reader input correct
(`all-caps-fatigue`).

---

## `underline-metrics`: Underlines From the Font · medium

> Take position and thickness from the face's own metrics.

```css
text-underline-position: from-font;
text-decoration-thickness: from-font;
text-decoration-skip-ink: auto;   /* stops the line cutting descenders */
```

`text-decoration-style: dotted` is a well-established hint that a word carries
extra information, an abbreviation, a defined term.

**The animation caveat:** **color is the only part of a real underline that
animates reliably.** If anything other than color needs to animate, build the
underline as a separate element.

---

## `small-caps`: True Small Caps Only · low

> `font-variant-caps: small-caps`, plus tracking. Verify the face has `smcp`.

**Numbers.** Add **0.05–0.08em** letter-spacing `[convention]`. Below about
10–12px the distinction stops being perceptible.

**Why it holds.** Scaling capitals down reduces stroke width proportionally, so
faux small caps render lighter than the text around them, visible as a patch of
weaker color in a line. True small caps are drawn with strokes calibrated to the
face.

**The trap:** a font without `smcp` **synthesizes silently**. Confirm in DevTools
rather than assuming. `all-small-caps` (c2sc + smcp) converts lowercase *and*
uppercase, for all-caps contexts only.

---

## `ligatures`: Defaults Are Right; Know When to Switch Off · low

> Standard ligatures stay on. Discretionary and historical stay off. Both are
> already the browser default.

**Numbers.** Five OpenType ligature tags; `rlig` is mandatory. `liga` + `clig`
(standard) and `contextual` are active under `font-variant-ligatures: normal`;
`dlig` and `hlig` are not.

**Where to disable.** Anywhere letterforms must stay separable and countable:
monospace and code, logotypes, tightly tracked all-caps.
`font-variant-ligatures: no-common-ligatures no-discretionary-ligatures`, with
`font-feature-settings: "liga" 0, "dlig" 0` as the low-level fallback.

**Where it doesn't matter.** Many contemporary sans-serifs draw `f` without an
overhanging arm, so the collision ligatures were invented to fix never occurs.

---

## `font-smoothing`: Root-Level Rendering Settings · low

> Set smoothing once on the root. Never per component.

```css
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
```

macOS renders text heavier than intended; this corrects it globally. Tailwind's
`antialiased` covers both.

**Two neighbours worth setting at the same level.** Keep text selectable,
`user-select: none` belongs on a draggable or gesture surface, never across the
interface and never because a label can be highlighted. And set `lang` so
pronunciation, quotes and hyphenation resolve correctly, with `dir` at whatever
boundary direction changes and `<bdi>` around mixed-direction values.
