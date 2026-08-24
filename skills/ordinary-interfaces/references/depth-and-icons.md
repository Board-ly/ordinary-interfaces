# Depth & Icons

10 rules. Shadows simulate one light source; the icon rules are optical
corrections that all end in "look at it".

---

## `shadow-fundamentals`: One Light, From Above · high

> Shadows point down. Depth starts at the edge, not at the shadow.

**Why it holds.** The visual system carries a prior expectation of overhead
light. Sun et al. (*PNAS*, 2010) showed it encoded in early visual areas
independently of perceived shape, and Ramachandran (1988) showed it persisting
when head orientation changes `[measured]`. It is not a learned convention you
can redesign around.

**In code.** Top edges lighter (facing the light), bottom edges darker. **Never
pure black**, `rgba(0,0,0,0.1–0.3)` so the shadow blends into whatever
background it lands on.

**Where it doesn't.** Multiple light sources produce contradictory depth cues.
And shadows cannot rescue bad geometry, they reinforce depth that edge contrast
already establishes, they do not substitute for it.

---

## `elevation-system`: Five or Six Levels, Tokenised · medium

> Higher elevation means larger blur and offset, softer and lighter, the light
> is further away.

**Numbers.**

| Level | Use |
|---|---|
| 0–1 | buttons, cards |
| 2–3 | dropdowns, menus |
| 4–5 | modals, dialogs |

Reference systems: **MD2** used dp shadows at 0, 1, 2, 4, 6, 8, 16, 24. **MD3**
uses Levels 0–5 (0, 1, 3, 6, 8, 12dp) **with a tonal color overlay rather than
shadow alone**, worth knowing before citing "Material elevation".

**Why it holds.** Consistency matters more than physical realism here. More than
six levels produces decision paralysis and inconsistent application, which
undermines the hierarchy the levels existed to create.

**In code.** Tokens, `shadow/low`, `shadow/medium`, `shadow/high`. Never
hardcode a shadow value inside a component. On colored backgrounds, tint the
shadow toward the background hue.

---

## `raised-vs-inset`: Z-Axis Is Not Decoration · medium

> Raised: shadow below, light top edge. Inset: shadow above, light bottom edge.

**Why it holds.** A raised element sits above the surface, so light strikes its
top and the shadow falls below. A recessed element has an upper lip blocking the
light, so the shadow appears at the top. Getting this backwards is immediately
legible as wrong without being nameable.

**In code.** Raised, drop shadow plus `inset 0 1px rgba(255,255,255,0.2)`.
Inset, `inset 0 1px 2px rgba(0,0,0,0.3)` plus a light bottom edge. Pressed
removes the drop shadow and deepens the inset; `translateY(1px)` with a reduced
shadow reads as a physical press. Hover increases size and blur, the element
lifts.

**Where it doesn't.** Inconsistent light direction between raised and inset
elements destroys the illusion entirely. And excessive realism becomes noise,
clarity outranks physical accuracy.

---

## `icon-stroke-weight`: Match the Adjacent Text · high

> Icon weight is a function of the label beside it, not an independent choice.

**Numbers**, on a 24px grid:

| Adjacent text | Icon stroke |
|---|---|
| Regular (400), 14–16px | **1.5px** |
| Medium / Semibold (500–600) | **2px** |
| Bold (700), or emphasised standalone | **2.5px** |

**Why it holds.** Visual weight is a similarity cue processed early in
perception. Text and icons at mismatched weights read as belonging to different
systems even when color, size and alignment all match, a hairline glyph beside
semibold text reads as broken rather than as subtle.

**Vendor systems that encode this.** Apple's SF Symbols ships **9 weights**
mapped 1:1 to San Francisco's own weights. Google's Material Symbols exposes
weight as a variable axis from **100 to 700**, deliberately the same numeric
scale as CSS `font-weight`, so an icon can bind to the same token as its text.

**Where it doesn't.** Solid glyphs have no stroke to match. Use the fill axis
and match perceived boldness through area. At very small sizes anti-aliasing
erases fine weight differences; check the render rather than assuming a cutoff.
A single-weight brand set should pick the one weight to match dominant body text
and accept the mismatch in bold contexts rather than shipping per-weight assets.

**One optical strategy per surface.** Never mix icon libraries with
incompatible stroke conventions on one toolbar.

---

## `icon-bounding-box`: One Frame, Variable Padding · medium

> Fixed frame across the set; padding varies by optical weight.

**Numbers.** Frames of 16, 20, 24, 32 or 48px. Starting padding: 16px frame → 1px,
24px → 2px, 48px → 4px. Live area = frame − padding.

**Why it holds.** Without a fixed frame, spacing between icons drifts across
contexts and nothing lines up twice. Circles need more padding than squares
because they carry less optical mass in the same box, mathematically equal is
not optically equal, ever.

**The test:** blur the whole set by 2px. Equal apparent mass confirms the
balance.

---

## `icon-optical-balance`: Centre by Mass, Not by Box · medium

> Offset 1–3px toward the lighter side. No formula covers every shape.

**Numbers.** **1–3px** for icons at 16–48px `[convention]`. The correction is
**scale-independent.** The proportional offset holds from 16px to 512px.

**Why it holds.** The eye finds the centroid of filled area, not the midpoint of
extremities (Arnheim, 1974). A play triangle's centroid sits at one third of its
height from the base, so coordinate-centring places it visibly low and left. Shao,
Che & Lu (*Displays* 80, 2023) measured alignment adjustment factors across icon
types `[measured]`, and Apple HIG, Material and IBM Carbon all specify optical
centring `[spec]`.

**Where it doesn't.** Symmetric shapes (circles, squares, plus signs) have
coincident geometric and visual centroids, so an offset there **introduces**
error. Below 16px sub-pixel offsets produce no visible gain and can cause
rendering artifacts; correct at the design grid instead. Animated icons shift
mass during motion, verify at rest and at key frames.

---

## `icon-alignment`: Align to Cap Height · medium

> Not the baseline, and not the em box.

**Numbers.** Target the **cap-height midpoint.** Between baseline and cap
height. Circular icons need **1–2px upward** beyond mathematical centre. Size
inline icons to the typeface's cap height, typically **1em–1.25em**, so the pair
scales together.

**The specific trap:** `vertical-align: middle` aligns to the middle of the **em
square**, not to cap height, which under-aligns in most typefaces and needs
manual correction. Baseline alignment is worse, it places the icon visually
below the text body.

**In code.** `display: flex; align-items: center;` plus a manual 1px nudge for
circles. Complex shapes have no formula; every icon-size and text-size
combination needs its own check.

---

## `icon-color-states`: One SVG, Recolored · high

> Never ship separate assets for hover, selected and disabled.

**In code.** One SVG drawn with `currentColor`; CSS state drives the color.
Hardcoded fills inside the SVG (`fill="#666"`) break this, strip them to
`currentColor` on import.

```css
.icon-button                      { color: var(--fg-muted); }
.icon-button:hover                { color: var(--fg-primary); }
.icon-button[aria-pressed="true"] { color: var(--accent); }
.icon-button:disabled             { opacity: 0.4; }
```

**Outline default, fill active.** Where a set offers both, use them as a **state
pair, never interchangeably**, outline for default (toolbars, list rows, inline)
and fill for selected (the active tab, a toggled bookmark). Filled icons
everywhere leaves the active tab with no state signal at all. Animate the swap
with `motion.md → icon-transitions`.

---

## `icon-render-size`: Design at the Size It Ships · medium

> An icon that reads at 48px can be mush at 16px.

**Why it holds.** Thin interior lines, tight counters and fine texture all blur
or alias at small sizes. Scaling detailed artwork down does not simplify it, it
just makes the detail illegible while keeping the cost.

**In code.** Test every icon at its smallest render size, often **16px**. Prefer
simplified glyphs for small contexts over shrunken detailed ones. Keep icons on
the pixel grid at render size, a 16px icon drawn on a 24px grid with fractional
scaling renders soft, so use native grids (**16, 20, 24**). Always SVG, never
raster, so one asset stays crisp at every density.

---

## `icons-rtl`: Flip Only What Reading Direction Owns · medium

| Flip | Leave alone |
|---|---|
| Back and forward arrows, navigation chevrons | Logos and brand marks |
| Text-block glyphs, alignment, lists, indent | Checkmarks |
| Speaker and volume waves (they emanate along reading direction) | Physical objects, clocks, cups, pencils |
| "Send"-style directional glyphs | Media playback (play and rewind refer to tape direction; convention keeps them LTR) |

```css
[dir="rtl"] .icon-directional { scale: -1 1; }
```

**Analyse composite icons part by part.** A badge or slash overlay may keep its
position even when the base glyph flips.
