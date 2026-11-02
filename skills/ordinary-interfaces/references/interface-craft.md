# System Craft

8 rules on layering and tokens, what separates a system from a pile of
components. All `[convention]`: practitioner craft, mostly from dark-mode product
UI.

---

## `surface-elevation`: Layering Should Whisper · high

> You should barely notice the system working.

**Numbers.** In dark mode, each elevation step is **a few percentage points**
lighter, invisible in isolation, legible when stacked.

| Element | Treatment |
|---|---|
| Sidebars | same background as the canvas, separated by a border |
| Dropdowns | one level above their parent |
| Inputs | slightly **darker** than their surroundings |

**Why each one.** A sidebar in a different color fragments the visual space into
two competing regions rather than one page with a division. A dropdown at the
same level as its parent blends into it and stops reading as a layer. Inputs are
*inset*, recessed things are darker, which is the same physics as
`raised-vs-inset`.

**Keep one hue across surfaces and shift only lightness.** Different hues per
surface is the fastest way to make a system look accidental.

**Where it doesn't.** Dramatic surface jumps are as much a failure as no
hierarchy. Elevation is a whisper; if you can name the step while using the
product, it is too loud.

---

## `border-discipline`: Findable, Not Visible · high

> If borders are the first thing you see, they are too strong.

**In code.** Use **low-opacity `rgba` over solid hex.** A solid border carries
the same weight onto every surface it lands on, while a translucent one adapts.
Build a progression: standard separation → softer separation → emphasis → focus
ring.

**The test:** blur your eyes. Hierarchy should still be perceptible and nothing
should jump out. (The same squint test verifies grouping, `proximity`.)

Avoid harsh borders and thick decorative ones. Where a border exists only for
depth, `surfaces.md → shadow-as-border` replaces it.

**A sub-pixel hairline is a device question, not a style one.** At
`devicePixelRatio: 1` a `0.5px` border rounds up to `1px` or disappears
depending on the engine, so it is specified as `1px` at low opacity and dropped
to `0.5px` only behind `@media (min-resolution: 2dppx)`. The worked example is
in `data-display.md → table-chrome`, where hairlines carry the most weight.

---

## `depth-strategy`: Pick One · high

| Strategy | Reads as | Suits |
|---|---|---|
| Borders only | clean, technical | dense tools |
| Subtle shadows | soft lift | approachable products |
| Layered shadows | premium, dimensional | marketing, consumer |
| Surface color shifts | tints carry hierarchy | dark-mode apps |

**Do not mix.** Mixed depth strategies are among the clearest signals that a UI
was assembled rather than designed, each individual choice is defensible and the
result is incoherent.

Also avoid: dramatic drop shadows, pure white cards on colored backgrounds, and
large radius on small elements (`corner-radius-tone` caps it at 50% of the
shortest dimension).

---

## `token-architecture`: The Roles a Product UI Actually Needs · high

> Every color traces to a primitive. No literal hex in a component.

**The roles**, extending `color.md → color-naming`:

- **Foreground:** primary, secondary, tertiary, muted: **four levels minimum**.
- **Background:** the elevation scale.
- **Border:** the progression scale.
- **Brand:** **one** accent. Multiple accents dilute focus.
- **Semantic:** destructive, warning, success.
- **Control tokens:** dedicated tokens for control background, control border and focus state. **Do not reuse surface tokens for interactive elements.** They will diverge, and the divergence will arrive as a bug.

**Spacing tokens by context, not only by number:** micro (icon gaps), component
(inside buttons and cards), section (between groups), major (between areas).
Random values signal no system.

**Naming.** Token names should sound like they belong to **this** product
(`--ink`, `--parchment`) rather than to any project (`--gray-700`,
`--surface-2`). **The test:** read your variable names aloud. Do they name this
product, or every product?

---

## `interactive-states`: Five, Plus Three for Data · high

> **default · hover · active · focus · disabled.** And for anything rendering
> data, **loading · empty · error**.

**Missing states feel broken**, and this is the most common gap in component work
as well as the cheapest to close. Treatments with numbers are in
`interaction.md → button-design`; the data states in full are `states.md`.

**Gradients and color are never decoration: color must mean something.**

---

## `tabular-numerals`: Fixed-Width Figures Wherever They Stack · medium

> `font-variant-numeric: tabular-nums` on tables, totals, counters, timers,
> badges and prices.

**Why it holds.** Proportional digits have different widths by design, so a
column of figures will not align on the decimal and a live counter visibly
twitches on every update. Tabular figures are drawn to one width specifically to
solve this.

Pair with reserving the width for the plausible maximum, so 9 → 10 does not
resize the container (`motion.md → numbers-in-motion`).

---

## `icon-restraint`: Icons Clarify or Go · medium

> If removing the icon loses no meaning, remove it.

**One icon set, period.** Mixed sets are visible immediately, including to people
who cannot say what is wrong. Standalone icons get a subtle background container
for presence. Sizing, stroke and optical alignment are in `depth-and-icons.md`.

---

## `default-tells`: Recognise Your Own Defaults · medium

> Ordinary is decided. Generic is undecided. They look different.

AI-generated design currently clusters around three looks. Each is legitimate for
*some* brief, and each appears regardless of subject, which is what makes them
defaults rather than choices:

1. **Warm cream background** near `#F4F1EA`, high-contrast serif display, terracotta accent near `#D97757`, the last being Anthropic's own interaction accent, so on a user's brief it reads as a tell.
2. **Near-black background** with a single bright acid-green or vermilion accent.
3. **Broadsheet layout.** Hairline rules, zero radius, dense newspaper columns.
4. **Violet-to-blue gradient with glass.** A gradient from roughly `#6366F1` to `#A855F7`, translucent blurred cards, a radial glow behind a centred hero. The most generated-looking of the four, because the gradient, the glass and the glow arrive together as one preset.

**Where a brief specifies a direction, follow it exactly, the brief's own words
always win, including when it asks for one of these.** Where the brief leaves an
axis free, do not spend that freedom on a default.

**The swap test:** replace each choice with the most common alternative. Anything
that would not meaningfully change the result is a place you defaulted.

**And then remove one thing.** Spend boldness in one place; let the signature
element be the memorable one and keep everything around it quiet.

Arriving at a non-default direction (domain exploration, the signature test) is
`design-engineering` and `frontend-design`. This rule is only the recognition
step.
