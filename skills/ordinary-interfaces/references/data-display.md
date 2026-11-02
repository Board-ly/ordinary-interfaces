# Data Display

9 rules on tables and dense data. Charts are `dataviz`'s subject, not this
file's, and the one chart rule here stays in `composition.md`. What is covered
is the table: its chrome, its alignment, how much of it fits, and what it looks
like while it has nothing to show.

A table is the surface where the general rules bend most. Three of them name a
table as their own exemption, so the compressions below are intended rather than
tolerated.

---

## `table-chrome`: Hairlines and a Frame, Not a Grid · medium

> Draw the fewest lines the data needs. A line around every cell is the default
> of a tool, not a decision.

**Numbers.** **Horizontal dividers only**, at the same low-opacity value the
rest of the system uses for separation, see `interface-craft.md →
border-discipline`. One frame around the table, or a shadow instead of one, see
`surfaces.md → shadow-as-border`. **Vertical dividers only where two adjacent
columns are genuinely confusable**, which is usually two numeric columns of
similar magnitude.

**Why it holds.** Rows are what the eye follows, and horizontal dividers support
that reading while vertical ones cut across it. A full grid gives every
boundary the same weight, so the structure has to be worked out rather than
seen, which is the cost that shows up as a table feeling heavy.

**Where it doesn't.** A spreadsheet is a grid on purpose, because the cell is
the unit of work and its boundaries are the thing being pointed at. Financial
statements keep rules under totals for the same reason: the line is content.

**In code.** A hairline below `1px` is a device question, not a style one. At
`devicePixelRatio: 1` a `0.5px` border rounds to `1px` or vanishes depending on
the engine, so specify `1px` at low opacity and only drop to `0.5px` behind a
query:

```css
.row { border-bottom: 1px solid rgb(0 0 0 / 0.08); }
@media (min-resolution: 2dppx) { .row { border-bottom-width: 0.5px; } }
```

---

## `column-alignment`: Numbers Right, Text Left, Nothing Centred · high

> Alignment is how a column is compared. Centring a column of values removes
> the only edge that made them comparable.

**Numbers.** Numeric and date columns **right-aligned with tabular figures**,
see `interface-craft.md → tabular-numerals`. Text **left-aligned**. The header
takes the alignment of its own column, not the opposite one. **Centre only
single-glyph columns**, a status dot, a checkbox, an icon action.

**Why it holds.** Digits carry place value from the right, so a right edge puts
ones over ones and thousands over thousands, and a column scan becomes a
comparison of lengths. Centring destroys both edges at once, which is why a
centred numeric column has to be read value by value.

**Where it doesn't.** An identifier that happens to be numeric, an order number
or a postcode, is text and aligns left, because nobody compares its magnitude.
Mixed-unit columns with the unit in the cell ("2 days", "4 h") align left as
well, since the right edge is the unit and not the quantity.

**In code.** `font-variant-numeric: tabular-nums` on the whole table rather than
per cell, so a filtered or sorted view cannot lose it. Right-aligning without it
produces a column whose digits still shift, which looks like a rendering fault.

---

## `row-density`: Three Densities, One Per Table · medium

> Density is a property of the data and the task, not a slider someone forgot
> to set.

**Numbers.** Three row heights `[convention]`:

| Density | Row height | For |
|---|---|---|
| Comfortable | **48px** | few rows, read once, touch |
| Default | **40px** | the normal case |
| Compact | **32px** | scanning and comparing many rows |

Below 32px the row is shorter than the 40px desktop target, see
`interaction.md → touch-target`, so a compact table's rows must not be the
click target for navigation. Put the action on a cell, not the row.

**Why it holds.** The number of rows visible at once decides whether comparison
happens in the eye or in memory. For scanning tasks more rows beat more padding,
which is the exact inversion of the usual spacing advice and why tables need a
rule of their own.

**Where it doesn't.** **A table is the documented exemption to
`spacing-layout.md → padding-gap-ratio`.** Cell padding equal to or below the
divider rhythm is correct here, because the dividers and the alignment carry the
grouping that padding carries elsewhere.

**In code.** One density per table, chosen for the task. A per-user density
toggle is a real feature in a data tool and a tell everywhere else, since it
pushes the decision onto the user.

---

## `sticky-chrome`: The Header Sticks, Identity Sticks on Narrow · medium

> A column of numbers with the header off screen is a column of numbers with no
> meaning.

**Numbers.** `position: sticky` on the header cells once the table scrolls past
**roughly one and a half screens** of rows `[convention]`. When the table
scrolls horizontally, the **first column**, the one that identifies the row,
sticks as well.

**Why it holds.** Both cases are the same failure: the data loses the label that
makes it readable. Vertically it is the column name, horizontally it is the row
name, and in both the user compensates by scrolling back and forth, which is the
behaviour the stickiness removes.

**Where it doesn't.** A table of fewer than about fifteen rows gains nothing and
pays the complexity. And **two sticky axes on a phone leave very little**: when
the identity column plus the header would take more than a third of the
viewport, drop the table layout and show rows as cards instead.

**In code.** A sticky cell needs its **own opaque background** or the rows
scroll through it, and the usual symptom is text overlapping on scroll because
the header inherited a transparent background. Sticky elements also obscure
focus, so pair this with `overlays.md → focus-not-obscured` and reserve
`scroll-margin-top` for the header's height.

```css
thead th { position: sticky; top: 0; background: var(--surface); z-index: 1; }
```

---

## `cell-truncation`: One Column May Truncate · medium

> Decide which column loses characters before the data decides for you.

**Numbers.** **The identity or description column truncates.** Numbers,
statuses, dates and units never do, see the rule against truncating a number in
`states.md → overflow-pressure`. Wrapping to **two lines** is usually better
than an ellipsis, and a hard cap at two keeps the row height predictable.

**Why it holds.** An ellipsis is a promise that the rest is available somewhere.
When it lands on a value rather than a label, the promise cannot be kept by
reading more carefully, and the user has to leave the table to find a figure
they were shown.

**Where it doesn't.** A column whose values are all short does not need the
decision, and a table designed around a long free-text field should not be a
table. One long column of prose inside a grid of short values reads as a layout
that outgrew its format.

**In code.** **`title` is not an accessible fallback.** It is unavailable on
touch, unreliable on keyboard, and not announced consistently, so a truncated
cell whose full value exists only in a `title` has no accessible full value. Put
it in a popover with a real trigger, see `overlays.md → overlay-taxonomy`, or
make the cell expandable.

---

## `status-encoding`: A Dot and a Word · high

> A column of coloured dots with the legend somewhere else is a colour-only
> encoding with extra steps.

**Numbers.** Status cells carry **a shape and a label in the cell**, not colour
alone, SC 1.4.1 (A) `[spec]`, see `color.md → red-green-color-blindness`. An
**8px** dot plus the word reads at every density `[convention]`.

**Why it holds.** Status is the column people filter and scan by, so it is the
column where a colour-only encoding costs the most. Around 8% of men cannot
separate red from green, and in a dense table the dots are small and adjacent,
which is the condition under which the distinction gets hardest.

**Where it doesn't.** Where the same status appears on every row of a filtered
view, the column is redundant and should be in the filter's own label instead.
And a single-state indicator, present or absent, can be shape-only, since there
is nothing to confuse it with.

**In code.** Keep the dot's colour inside the system's one-meaning-per-colour
discipline, see `color.md → one-color-one-meaning`, so the green in a status
column is the same green as every other success in the product. The dot is
decorative once the word is present, so it takes `aria-hidden="true"` rather
than a redundant label.

---

## `selection-without-shift`: Reserve the Column · medium

> A control that appears on hover moves the data under the pointer.

**Numbers.** The selection control's column is **always present**, at its full
width, whether or not anything is selected. Row actions reserve their width the
same way, **right-aligned in a fixed slot**.

**Why it holds.** Appearing on hover looks tidy in a static review and shifts
the grid in use, because every column after it moves by the control's width at
the moment the pointer arrives. It is also unreachable: hover is not a state a
keyboard or a touch screen has, see `motion.md → hover-gating`.

**Where it doesn't.** Opacity may change on hover, since that moves nothing. A
checkbox at low opacity until hover or focus, at full opacity when checked, is
the version of this pattern that works, and it still occupies its column at all
times.

**In code.** Fixed width plus `flex-shrink: 0` on the control slots, so the
columns line up across rows rather than being distributed by content. Selection
state belongs on the row element for the screen reader,
`aria-selected`, not only on the checkbox.

---

## `sort-affordance`: One Sorted Column, Announced · medium

> Sorting is a property of the table the user can see and the screen reader can
> hear.

**Numbers.** **One column sorted at a time**, with its direction shown in its
own header, and `aria-sort="ascending" | "descending"` on that header cell,
ARIA 1.2 `[spec]`. Every other sortable header is a button with no direction
shown.

**Why it holds.** A sort that is not visible in the header is invisible, and the
user's next question, why is this row first, has no answer on screen. Putting
the control in a separate dropdown above the table separates the action from the
thing it changes, which is why the header is the place for it.

**Where it doesn't.** A stable secondary sort is fine and need not be shown, but
it must not change between renders, or the order appears random on refresh. A
table whose order is semantic, a ledger by date or a ranked list, is not
sortable by default and should say what it is sorted by rather than offering to
change it.

**In code.** The whole header cell is the button, not an icon inside it, so the
target is the full cell, see `a11y-implementation.md → hit-area-extension`.
Keep the direction glyph in a reserved slot, or the header text shifts when the
glyph appears, which is `selection-without-shift` again in a different column.

---

## `table-empty-and-loading`: Keep the Columns · medium

> The table's structure is the one thing that does not change when the data is
> missing.

**Numbers.** Loading shows **skeleton rows at the real row height and the real
column widths**, see `states.md → loading-strategy`. Empty shows a message
**inside the table frame, below the header**, not instead of the table.

**Why it holds.** Keeping the chrome keeps the layout stable across all three
states, so nothing jumps when data arrives, and it keeps the column headers
visible, which is what tells the user what they are waiting for or what they
filtered away.

**Where it doesn't.** A first-run table with no columns configured yet has no
structure to keep, and that is a configuration state rather than an empty one.

**In code.** **Filtered-empty and never-had-data are different states with
different copy**, see `states.md → empty-states` and
`writing.md → empty-state-copy`. Filtered-empty offers to clear the filter;
never-had-data offers to create the first row. Shipping one message for both is
the usual shortcut and it tells the user to create something they already have.
