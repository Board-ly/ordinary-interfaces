# Surfaces

5 rules on radius, depth and press feedback. `transition-specificity` and
`will-change-discipline` moved to `motion.md`, where the performance rules live.

**These values are exact, not ranges.** `0.96` is not `0.95`.

---

## `concentric-radius`: Outer Equals Inner Plus Padding · high

> `outerRadius = innerRadius + padding`

**Mismatched radii on nested elements is the single most common thing that makes
an interface feel subtly wrong**, and it is invisible until you know to look,
because every individual value is defensible.

```css
/* Good */                                    /* Bad */
.card       { border-radius: 20px; padding: 8px; }   .card       { border-radius: 12px; padding: 8px; }
.card-inner { border-radius: 12px; }                 .card-inner { border-radius: 12px; }
```

Tailwind: `rounded-2xl p-2` (16px radius, 8px padding) wraps `rounded-lg` (8px).

**Why it holds.** The two curves are concentric arcs only when the outer radius
accounts for the offset between them. Equal radii mean the gap between the curves
varies around the corner (narrowing at 45°) which reads as a squeeze without
being nameable.

**Where it doesn't.** Past **24px of padding**, treat the layers as separate
surfaces and choose each radius independently rather than forcing the arithmetic.
Keep an established component token where the layers are independent or the
padding is deliberately asymmetric.

Radius *values* and what they signal: `composition.md → corner-radius-tone`.

---

## `shadow-as-border`: Shadows for Depth, Borders for Structure · high

> Where a border exists only to create depth, replace it with a layered
> transparent shadow.

| Use shadows | Use borders |
|---|---|
| Cards and containers with depth | Dividers between list items |
| Buttons with bordered styles | Table cell boundaries |
| Elevated elements, dropdowns, modals | Form input outlines |
| Elements over varied backgrounds | Hairline separators in dense UI |

**Why it holds.** Shadows are transparent, so they adapt to whatever they land
on. A fixed border color was chosen against one background and is now sitting on
an image, or on the second background color someone added later.

**Light mode: three layers:** a 1px ring, a subtle lift, ambient depth.

```css
--shadow-border:
  0px 0px 0px 1px oklch(0 0 0 / 0.06),
  0px 1px 2px -1px oklch(0 0 0 / 0.06),
  0px 2px 4px 0px  oklch(0 0 0 / 0.04);
```

**Dark mode: collapse to one white ring.** Layered depth shadows are invisible
against a dark background, so the extra layers are cost with no effect:

```css
--shadow-border:       0 0 0 1px oklch(1 0 0 / 0.08);
--shadow-border-hover: 0 0 0 1px oklch(1 0 0 / 0.13);
```

Transition `box-shadow` at 150ms `ease-out` for hover.

**Never apply this to dividers.** `border-b`, `border-t`, or any border whose
job is separation rather than depth. Those stay borders, because they are
communicating structure and structure should not be transparent.

---

## `image-outlines`: A Neutral Hairline, Never Tinted · medium

> 1px at 0.1 opacity. Pure black in light, pure white in dark.

```css
img { outline: 1px solid oklch(0 0 0 / 0.1); outline-offset: -1px; }  /* light */
img { outline: 1px solid oklch(1 0 0 / 0.1); outline-offset: -1px; }  /* dark  */
```

**The color rule is not stylistic.** Never a near-black or tinted neutral, no
`slate-900`, `zinc-900`, `#0a0a0a`, `#111827`, `#f5f5f7`, and never the brand
accent. **A tinted outline picks up the surface underneath and reads as dirt on
the image edge.** The outline is a separator, not a themed element.

**Why `outline` rather than `border`.** Outline never affects layout at any
offset, and `outline-offset: -1px` draws the ring just inside the edge so it hugs
the corner radius instead of squaring it off.

---

## `press-scale`: 0.96 on Click · medium

> Tactile confirmation that the interface registered the press.

```css
.button        { transition-property: scale; transition-duration: 150ms; transition-timing-function: ease-out; }
.button:active { scale: 0.96; }
```

**Always 0.96.** Below 0.95 the press reads as exaggerated. Provide a `static`
prop or class to switch it off where motion would distract.

**On the two numbers in this skill:** `motion.md → never-scale-zero` gives
0.95–0.98 from a different source. **0.96 sits inside that band.** Use it as the
default and treat the band as tolerance when matching an existing product's
motion language.

---

## `theme-switch-suppression`: Suppress Transitions on the Flip · high

> Inject `transition: none`, **force a reflow**, then remove it on the next
> frame.

**Why it holds.** A theme flip changes color, background, border and shadow on
nearly every element simultaneously. Every transition on those properties fires
at once and the switch smears instead of snapping.

**The forced reflow is the part people leave out**, and without it the browser
batches the style change so the suppression never applies at all, which looks
exactly like not having written it.

```js
const style = document.createElement('style');
style.textContent = '*,*::before,*::after{transition:none !important}';
document.head.appendChild(style);
document.body.offsetHeight;               // force reflow. Do not remove
requestAnimationFrame(() => style.remove());
```
