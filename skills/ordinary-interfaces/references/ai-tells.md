# Agent Tells

10 rules on what marks an interface as agent-built. `interface-craft.md →
default-tells` covers the *aesthetic* defaults, the three or four looks that
arrive regardless of brief. This file covers the *mechanical* ones: what is
missing or uniform in the code rather than what the palette looks like.

**This is a detection layer.** Every rule names a measurable cue, a threshold,
and the rule elsewhere that fixes it. The cue is the part that is new here, and
it is written to be runnable against a codebase rather than judged by eye, so a
finding can be produced before anything has been looked at.

**Two notations.** Each cue is given for both stylesheet declarations and
utility classes, because a Tailwind project writes `p-4` and `hover:` where a
CSS file writes `padding:` and `:hover`. Running the stylesheet form against a
utility-class codebase returns nothing, and nothing reads as a clean result
rather than as an unrun check, which is the worst failure a detection layer can
have. `project-system.py` reports which notation the project uses. Take the
matching line, and run both where a project mixes them.

Run `scripts/project-system.py` first either way. Several cues are only
meaningful against what the project already decided.

---

## `one-spacing-value`: Rhythm, Not a Constant · high

> One spacing value used everywhere is not a system. It is the absence of one.

**The cue.** Count distinct spacing values in the styles and their frequency.
**If a single value covers more than 70% of all `padding`, `margin` and `gap`
declarations, there is no rhythm** `[convention]`.

```bash
# stylesheets
grep -rhoE '(padding|margin|gap)[^:]*:[^;]+' src | grep -oE '[0-9]+(px|rem)' \
  | sort | uniq -c | sort -rn | head
# utility classes
grep -rhoE '\b[mp][trblxyse]?-[0-9]+(\.[0-9]+)?\b|\bgap(-[xy])?-[0-9]+(\.[0-9]+)?\b' src \
  | sed -E 's/^[a-z]+-//' | sort | uniq -c | sort -rn | head
```

The utility form strips the property prefix first, so `p-4`, `px-4` and `mt-4`
count as the same step on the scale. That is the number the threshold is about:
how many steps the project actually uses, not how many properties it sets.

**Why it holds.** Grouping is carried by *differences* in space, see
`spacing-layout.md → proximity` and `padding-gap-ratio`. A constant removes
every difference, so nothing groups and the hierarchy falls back onto borders
and weight, which is why these layouts read as flat lists of boxes whatever
their content.

**Where it doesn't.** A deliberately uniform grid of equal tiles, a colour
palette, an icon picker, a photo wall, uses one gap on purpose, and the
container padding should still exceed it. A young project with a handful of
components may legitimately have few values; the cue is a ratio, not a count.

**The fix.** `proximity`, `padding-gap-ratio`, `group-with-space`, and the
project's own scale if `project-system.py` found one.

---

## `one-shadow-everywhere`: Elevation Has to Mean Something · medium

> If a card, a dropdown and a modal cast the same shadow, nothing is above
> anything.

**The cue.** Count distinct `box-shadow` values against the number of surface
levels the UI actually has. **One or two shadow values across cards, menus,
dialogs and toasts is the tell**, as is a shadow applied as a decoration to
elements that are not raised at all.

**Why it holds.** Elevation is the only cue that distinguishes a transient
surface from a blocking one before interaction, see
`overlays.md → overlay-surface`. Flattening it costs the user the ability to
predict whether clicking outside will dismiss the thing they are looking at.

**Where it doesn't.** A deliberately flat system that separates surfaces with
background steps and hairlines instead is a legitimate strategy, see
`interface-craft.md → depth-strategy`, and in that system *no* shadows is
correct and consistent. The failure is the mixture: one shadow standing in for a
depth system that was never chosen.

**The fix.** `depth-and-icons.md → elevation-system` for the ladder,
`depth-strategy` for picking one strategy and holding it.

---

## `border-instead-of-surface`: Everything Outlined · medium

> Every container wrapped in a 1px grey border is what a surface system looks
> like when there isn't one.

**The cue.** Ratio of `border` declarations to `background` declarations in
component styles. **More borders than backgrounds means containment is being
drawn rather than built**, and a solid mid-grey hex repeated across components
confirms it.

```bash
# stylesheets
grep -rhoE '^\s*border[^:]*:' src | wc -l ; grep -rhoE '^\s*background[^:]*:' src | wc -l
# utility classes
grep -rhoE '\bborder(-[trblxyse])?(-[0-9]+)?\b' src | wc -l ; grep -rhoE '\bbg-[a-z]' src | wc -l
```

**Why it holds.** A border separates two things at the same level. A surface
says one sits on the other. Using the first for the second gives every boundary
identical weight, so the screen becomes a set of equal rectangles and the eye
has nothing to rank, which is the same mechanism as `table-chrome` in
`data-display.md` at page scale.

**Where it doesn't.** Outlined is a real aesthetic, and a system committed to it
uses *graded* border strengths, a progression of opacities, not one value. Input
fields keep a border in nearly every system, because the affordance is the
boundary.

**The fix.** `interface-craft.md → border-discipline` for the progression and
the squint test, `surfaces.md → shadow-as-border` where the border exists only
for depth.

---

## `hover-without-press`: No State for the Finger · high

> A control with a hover state and no pressed state has been designed on a
> desktop and tested nowhere.

**The cue.** Count `:hover` rules against `:active` and `:focus-visible` rules.
**Hover styled while `:active` is absent is the tell**, and ungated hover, see
`motion.md → hover-gating`, usually appears with it.

```bash
# stylesheets
grep -rhoE ':hover' src | wc -l
grep -rhoE ':active|:focus-visible' src | wc -l
# utility classes
grep -rhoE '\bhover:' src | wc -l
grep -rhoE '\bactive:|\bfocus-visible:' src | wc -l
```

A ratio, not a count. Hover rules far outnumbering the other two is the tell,
and a zero in the second line of either pair is the strong form of it.

**Why it holds.** Hover is the one state a touch screen does not have and a
keyboard does not have. Building only that state means the majority of
interactions get no feedback at all, and on touch the hover style sticks after
the tap instead, which reads as the control being stuck.

**Where it doesn't.** A non-interactive element with a hover affordance, a row
that highlights to aid scanning, needs no pressed state because there is nothing
to press. Links are pressed by the browser's own activation and need focus, not
scale.

**The fix.** `interface-craft.md → interactive-states` for the full set,
`surfaces.md → press-scale` for the press itself, `hover-gating` for the query,
`a11y-implementation.md → focus-visible` for the keyboard.

---

## `centred-everything`: Centring as the Default Axis · medium

> Centre is where things go when no one decided where they go.

**The cue.** `text-align: center` on containers rather than on short display
text, every section built as a centred column, and **paragraphs over two lines
centred**, which is the version that costs reading speed.

```bash
grep -rhoE 'text-align:\s*center|\btext-center\b' src | wc -l
```

A count alone does not decide this one. Open the files it names and check
whether the centred element is a heading of a few words or a paragraph.

**Why it holds.** A centred block gives the eye no stable left edge to return
to, so every line starts at a new horizontal position, see
`typography.md → text-alignment`. At page level, centring everything also
removes the alignment relationships that would have shown what belongs
together, see `spacing-layout.md → align-to-shared-edges`.

**Where it doesn't.** Short display text, an empty state, a dialog's single
message, a hero headline of a few words, centres well and conventionally. Marketing
pages legitimately centre far more than product UI, and that judgement belongs
to `frontend-design`, not here.

**The fix.** `text-alignment` for the measure, `align-to-shared-edges` for the
layout, `ux-laws.md → optical-center` for the fact that geometric centre and
perceived centre differ.

---

## `three-equal-cards`: The Feature Grid Reflex · medium

> Three cards of equal weight is a layout chosen before anyone knew what went
> in it.

**The cue.** A grid of two to four items, equal size, equal type scale, equal
emphasis, with **no element carrying the hierarchy**. Icon, bold title, two
lines of body, repeated.

**Why it holds.** Equal weight states that the items are equally important,
which is almost never true, so the layout removes the ranking the content had.
It also makes the content fit the box: features get summarised to two lines
because the card has two lines, see `composition.md → emphasis` and
`hierarchy-channels`.

**Where it doesn't.** Genuinely parallel options, three pricing tiers, three
sizes of the same thing, are the case the pattern exists for, and even then one
tier is usually recommended and should look it. `composition.md → rule-of-odds`
is about grouping, and is not a licence for this.

**The fix.** `emphasis` and `hierarchy-channels` for deciding what leads, and
`default-tells`'s swap test: replace the grid with a list and see whether
anything is lost.

---

## `load-animation-on-everything`: Entrances Nobody Asked For · high

> Content that is present on first paint does not need to arrive.

**The cue.** Animations on elements that exist at first paint, fade-up on every
section, staggered reveals on page load, and **a scroll-triggered entrance on
content above the fold**, which animates something the user is already looking
at.

**Why it holds.** An entrance delays the content to show the transition, and on
first load the user is waiting for the content. It is also the most common
reduced-motion failure, because load animations are usually written outside the
component that would carry the query. Nothing about it is subtle: it is the
single most recognisable sign of a generated page.

**Where it doesn't.** Content that genuinely arrives, a list item added, a
dialog opening, a route transition, animates, see `motion.md →
animation-necessity`. A staged entrance for a deliberately cinematic landing
page is a direction, and `motion.md → staged-enter` has the constraints for
doing it once rather than on every section.

**The fix.** `animation-necessity` for whether at all, `reduced-motion` for the
query, `motion-restraint` for the budget. SC 2.3.3 Animation from Interactions
is AAA `[spec]`; `prefers-reduced-motion` is the practical floor.

---

## `mixed-icon-sets`: Two Libraries and an Emoji · medium

> Icons from different families in one interface read as a mistake even to
> people who cannot say why.

**The cue.** More than one icon package in the dependencies, emoji used as
interface icons, inline SVGs at different stroke widths, or icons at sizes the
set was not drawn for.

```bash
grep -E '"(lucide|@heroicons|react-icons|@tabler|feather|phosphor)' package.json
```

**Why it holds.** A set shares a stroke weight, a corner treatment, an optical
size and a grid. Mixing sets breaks all four at once, and the result is read as
inconsistency without the specific cause being identified. Emoji additionally
render differently per platform and carry an accessible name the author did not
write.

**Where it doesn't.** A brand mark, a product logo in a list of integrations, a
flag, comes from outside any set and should. One set plus a small number of
custom glyphs drawn on the same grid is normal and correct.

**The fix.** `depth-and-icons.md → icon-stroke-weight`, `icon-render-size` and
`icon-bounding-box` for the geometry, `interface-craft.md → icon-restraint` for
how many.

---

## `form-tells`: The Label Is Not Optional · high `[spec]`

> Three failures travel together, and each is a line of code rather than a
> judgement.

**The cue.** Three greppable facts:

| Cue | Fails |
|---|---|
| `<input placeholder=` with no associated `<label>` | SC 3.3.2 (A) `[spec]`, and the hint vanishes on first keystroke |
| `<div onClick=` on something that behaves as a button | keyboard operability, SC 2.1.1 (A) `[spec]` |
| No `autocomplete` on name, email, address or payment fields | SC 1.3.5 (AA) `[spec]` |

**Why it holds.** All three are produced by generating markup from appearance.
A placeholder looks like a label, a `div` with a click handler looks like a
button, and `autocomplete` has no visual result so nothing prompts it. The cost
lands entirely on keyboard users, screen reader users, and anyone filling a form
on a phone.

**Where it doesn't.** A placeholder as an *example* alongside a real label is
correct and useful, see `writing.md` on placeholders as examples. A `div` with a
click handler that is purely decorative, a card that navigates while also
containing a real link, is a different problem (nested interactives) and not
this one.

**The fix.** `a11y-implementation.md → form-controls` and
`native-elements-first`. The second is the general form: use the element that
already has the behaviour.

---

## `happy-path-only`: One State Shipped · high

> The populated state exists. The other eight were never considered.

**The cue.** A data-rendering component with **no branch for loading, empty or
error**. The strongest single cue is an early `if (!data) return null`, which
silently renders nothing for three different reasons.

```bash
grep -rn --include='*.tsx' --include='*.jsx' --include='*.vue' --include='*.svelte' \
  -E 'return null|return <></>|v-if="!' . | grep -v node_modules | head -20
```

Searching from the root rather than `src/components`, because a Next.js app
keeps components in `app/`, a monorepo in `packages/*/`, and the convention is
not worth guessing. The empty fragment is the same failure written differently.

**Why it holds.** Every state that was not designed still ships, as whatever the
code happens to do, which is usually a blank area with no explanation. It is
also the failure that is invisible in review, because review happens against
seeded data where the happy path is the only reachable state.

**Where it doesn't.** A presentational component that receives already-resolved
data has no states to handle, and pushing them into it is wrong. The states
belong at the boundary where the data is fetched.

**The fix.** `states.md → state-ledger` for the enumeration, and the whole of
`states.md` for the individual states. **`sad-paths` owns the workflow and
ships a scanner for exactly this cue**, so run that rather than grepping by hand
when it is available.
