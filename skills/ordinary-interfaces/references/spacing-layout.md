# Spacing & Layout

17 rules. Proximity and the padding-to-gap relationship do most of the work; the
grids are scaffolding for consistency rather than laws.

---

## `proximity`: Distance Encodes Relationship · high

> Equal spacing everywhere means no hierarchy anywhere.

**Numbers.**

| Gap | Says |
|---|---|
| 4–8px | these belong together, label and input, icon and text |
| 16–24px | same section |
| 32–48px+ | different sections |

**Why it holds.** Grouping by proximity happens pre-attentively, before any
conscious reading of the layout. Whitespace is therefore not empty. It is the
primary grouping instrument, and spending it uniformly spends it on nothing.

**Where it doesn't.** Strong color or shape similarity can override proximity.
Practically: a label more than 16px from its input reads as detached and gets
misattributed to the wrong field; sections closer than 24px read as one block.

**The check:** squint at it. The groups should be obvious before anything is
legible.

---

## `padding-gap-ratio`: Padding Exceeds the Gap · high

> Container padding ≥ 1.5× the gap to its siblings, at every nesting level.

**Numbers.** **≥1.5×** `[convention]`; 2× is perceptually more reliable.

**Why it holds.** When padding equals the gap, content at a card's edge is
equidistant from its own container and from the next one, containment stops
being readable from spacing, and hierarchy falls back onto borders or color
alone. It is the same proximity mechanism as above, applied inside and outside
one boundary.

**In code.** A 16px gutter wants **≥24px** card padding, and 32px reads more
clearly. Nav items 8px apart want **≥12px** item padding; below that they float
between groups rather than belonging to a row. Apply it at each level: section
padding exceeds column gap, card padding exceeds grid gutter, list-item padding
exceeds row gap.

**Where it doesn't.** Full-bleed media violates it deliberately, the frame
communicates containment instead. Dense tables compress on purpose, with cell
borders and row striping carrying the grouping. Cards with a visible border or a
distinct background have an explicit boundary already, so padding can drop
without ambiguity.

---

## `group-with-space`: Space First, Lines Last · high

> Space groups. Background shapes group. Lines group only when space cannot.

**Numbers.** The between-group gap is at least **2×** the within-group gap,
8px inside, 16px+ between, or the grouping reads as noise rather than structure.

**Why it holds.** Every separator line is a mark competing for attention with the
content it separates. Space carries the same information at zero visual cost,
which is why it goes first and lines go last.

---

## `8pt-grid`: One Base Unit for Spacing · high

> Multiples of 8 for spacing and sizing. Line heights use 4.

**Numbers.** 8, 16, 24, 32, 40, 48, 56, 64. Font sizes are **not** required to be
multiples of anything.

**Why it holds.** At @2x an 8px value lands on 16 physical pixels and at @3x on
24, whole numbers at every common density. A smaller base produces more
variables without producing more useful distinctions.

**Where it doesn't.** Non-integer OS scaling (Windows at 125% or 150%) can still
produce sub-pixel rendering; the grid reduces this rather than eliminating it.
**8px increments are too coarse for line height.** That is what the 4pt
half-step is for. And it is a scale, not a prison: a 6px radius is fine.

---

## `4pt-system`: The Half-Step · medium

> 8pt for structure, 4pt for type and detail.

**Numbers.** 4, 8, 12, 16, 20, 24. Use 8pt for component sizing and margins
between major elements; 4pt for line heights, icon gaps, small spacing and dense
interfaces.

**Where it doesn't.** Using 4pt everywhere reintroduces the variable count the
system existed to reduce. Odd values (5, 7, 9) produce sub-pixel blur at 1.5×
scaling.

---

## `baseline-grid`: Vertical Rhythm on Fours · medium

> Line heights are multiples of 4: 16, 20, 24, 28, 32.

**Why it holds.** The comfortable leading values all land on 4, which is what
makes a 4px baseline usable where an 8px one is not.

**Historical note worth carrying.** This was the Material Design **2** standard.
**MD3 replaced the explicit baseline grid with flexible spacing tokens.** Citing
it as current Material guidance is out of date. Pixel-perfect baseline alignment
across browsers is difficult in responsive layouts regardless.

---

## `active-white-space`: Emptiness That Communicates · medium

> Space placed to direct attention is design. Space left over is not.

**Numbers.** Hero `padding-block: 120–160px` against a default of 40–60px.
Active-versus-passive spacing tokens typically differ by **1.5–2×**
`[convention]`.

**Why it holds.** Increasing the space *around* an element raises its perceived
importance without changing the element at all, a free hierarchy channel.
NN/g eye-tracking finds more time spent on content surrounded by white space
`[measured]`, and Iseki (2025, N=1,193, *Journal of Sensory Studies*) found
larger white space raising perceived quality and luxury ratings in package design
`[measured]`.

**Where it doesn't.** Data tables, dashboards and code editors need compression,
generous spacing there adds scrolling and costs scanability for expert users who
already know where to look. Mobile forces the trade-off above the fold.

---

## `controls-distinct`: Controls Must Look Like Controls · high

> Every interactive element gets a background, a border, or a consistent
> placement zone.

**Numbers.** With no established density system: **12px** between adjacent
bordered or filled controls, **24px** around borderless text- and icon-only ones.

**Why it holds.** A control styled like the static text beside it is not a
control until someone discovers it by accident. Affordance is the whole job of
the treatment.

**Where it doesn't.** Compact layouts can go tighter, provided hit areas do not
overlap (`a11y-implementation.md → hit-area-extension`) and the controls stay
distinguishable.

---

## `align-to-shared-edges`: Fewer Edges · high

> Pick alignment edges and hold them. Every stray edge reads as noise.

**Numbers.** One project spacing step per level of subordination; **16px** is a
useful default.

**In code.** Order by importance, most important content near the top and the
**leading** edge, reading order top-to-bottom and leading-to-trailing. Think in
leading and trailing, not left and right: use `padding-inline-start` and
`margin-inline-end`, and reserve physical `left`/`right` for genuinely physical
geometry.

---

## `progressive-disclosure-cue`: Hidden Needs a Hint · high

> Content hidden with no cue may as well not exist.

**Numbers.** Let the next item peek **16–32px** past the scroll edge, or use the
project's established affordance, or show an explicit disclosure control.

---

## `content-breakpoints`: Break Where Content Breaks · high

> Breakpoints come from the layout failing, not from device presets.

**Why it holds.** 768 and 1024 are inherited numbers that describe hardware that
has since diversified. A layout that collapses at 768 while it still fits at 800
is collapsing for a reason unrelated to itself.

**In code.** Hold the expanded layout as long as it genuinely fits and collapse
late. Prefer container queries for component-level adaptation. Test the smallest
and largest sizes first, the middle usually takes care of itself.

---

## `translation-growth`: Text Grows · high

> No fixed width or height on a text container. A one-word button is the riskiest
> label on the screen.

**Why it holds.** Translated strings grow, and short strings grow
*proportionally* more, which is why the button that looks safest is the one that
breaks. A percentage budget does not survive contact with a real locale.

**In code.** `max-width` and wrapping, never fixed dimensions; `min-height`, never
`height`. Test with pseudo-localization plus one representative locale.

---

## `content-bleeds-controls-float`: Bleed and Inset · medium

> Backgrounds reach the edge. Controls and text do not.

**In code.** Media and backgrounds extend to the viewport edges; controls and
text stay inside layout margins and safe areas (`env(safe-area-inset-*)`); sticky
chrome floats above the content layer rather than blocking it. Keep full-width
buttons inside the margins with a visible radius, around **16px** inline on
mobile. Edge-to-edge actions work only when they follow established platform
chrome, respect safe areas, and stay distinguishable from system UI.

**Never place a critical action where resizing or scrolling can clip it.**

---

## `manuscript-grid`: One Column, Four Margins · medium

> Text-primary layouts need an explicit max-width or the measure runs away.

**Numbers.** Column width **45–75 CPL** (Bringhurst, 1992) or **50–75** (Baymard),
with comfort often observed around 50–60. WCAG caps at 80.

**Why it holds.** A single column removes competing reading paths, no
column-switching cost, one direction. The classical margin ratios (1:1:2:3
geometric, or 2:3:4:6 Van de Graaf, inner:top:outer:bottom) exist to compensate
for binding: the gutter makes the inner margin *look* narrower than it measures.
On screen there is no binding, but a smaller top and larger bottom margin still
produces a more grounded page.

**Where it doesn't.** Comparison tables, dashboards and galleries need a
different structure entirely. Marketing pages with full-bleed sections cannot be
constrained to one column. Single-screen apps, forms and modals gain nothing.

**In code.** `max-width: 65ch; margin-inline: auto; padding-inline: 1.5rem;`

---

## `twelve-column-grid`: Twelve Divides Well · medium

> The advantage is arithmetic and interoperability, not perception.

**Numbers.** 12 divides by 2, 3, 4 and 6, halves, thirds, quarters, sixths with
no fractional columns. Gutter **16–24px**. Column width =
`(container − (n−1) × gutter) / n`.

**Why it holds.** Nathan Smith's 960.gs (2007) standardised it, and Bootstrap,
Foundation and Material all default to it, so layouts transfer predictably
between design tools and component frameworks `[convention]`. CSS Grid has no
default; `grid-template-columns` is always explicit.

**Where it doesn't.** **Five-column layouts are impossible.** 12 does not divide
by 5. Use 10 or 20 columns if fifths are a core requirement. Below 360px, collapse
to 4 or a single column. Editorial long-form is often better on 6 or 8 columns
with wider gutters.

---

## `modular-grid`: Columns and Rows · medium

> For layouts needing vertical and horizontal control at once.

**Numbers.** Gutters **16–24px**. Suits dashboards, editorial layouts and product
grids, a 4×4 module grid gives 1 module for a KPI card, 2×2 for a chart, 4×2 for
a table.

**Where it doesn't.** Web and mobile rarely need strict row heights; a column
grid usually suffices. Modules that are too small produce placement paralysis.

---

## `wcag-layout`: Reflow, Orientation, Drag, Target Size · high `[spec]`

> The layout works at 320px, in both orientations, without a mouse, at 24px
> minimum targets.

**Numbers**, WCAG 2.2:

| SC | Requirement |
|---|---|
| 1.3.4 (AA) | no lock to a single orientation unless essential |
| 1.4.10 (AA) | reflow at **320 CSS px** width (1280px at **400%** zoom) with no two-dimensional scrolling; 256px height for horizontal content |
| 2.5.7 (AA) | every drag has a single-pointer alternative |
| 2.5.8 (AA) | pointer targets **24×24 CSS px** minimum |

**Why it holds.** 400% zoom is a common low-vision setting, and a page that
forces horizontal scrolling there is unreadable rather than merely awkward.
Orientation lock excludes wheelchair users with fixed-mount tablets. Drag with no
alternative excludes switch access, keyboard-only and tremor entirely.

**Where it doesn't.** Maps, diagrams, video, data tables and interfaces where a
toolbar must stay visible during manipulation are exempt from reflow. Essential
orientations (bank checks, piano keyboards, projector slides) are exempt from
1.3.4. Target size has five exceptions, spacing, equivalent control elsewhere,
inline in text, user-agent controlled, and essential.

**In code.** Test at 400% zoom on a 1280px viewport; no horizontal scrollbar for
primary content. The usual culprits are fixed widths, absolutely positioned
sidebars and non-wrapping flex rows. Use `@media (orientation: …)` to enhance,
never to hide or disable. Give drag-to-reorder arrow keys or explicit move
buttons.
