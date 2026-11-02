# Overlays

12 rules on the things that open on top: tooltips, popovers, menus, dialogs,
sheets and toasts. Timing lives in `motion.md`, focus handling in
`a11y-implementation.md`, and this file assumes both. What is here is the part
neither covers: which element the job calls for, what sits behind it, how it is
dismissed, and where it is allowed to appear.

Most overlay bugs are one mistake made early, picking the wrong element, and
every rule below reads better once `overlay-taxonomy` is settled.

---

## `overlay-taxonomy`: Four Elements, Four Jobs · high

> A tooltip labels, a popover holds content, a menu holds actions, a dialog
> blocks. Using one for another's job is the root cause, not a style question.

**Numbers.**

| Element | Triggered by | Interactive inside | Blocks the page | Focus |
|---|---|---|---|---|
| Tooltip | hover and focus | no | no | stays on the trigger |
| Popover | click | yes | no | moves in, page stays reachable |
| Menu | click | yes, one list of actions | no | roving within the list |
| Dialog | click | yes | yes | trapped, see `focus-trap` |

**Why it holds.** The four differ in what the keyboard and the screen reader
have to do, not in appearance, so an element chosen by look sets up behaviour
that cannot be patched later. A tooltip that holds a link is unreachable,
because focus never enters it. A menu built as a dialog traps focus for a
one-click action. A dialog built as a popover leaves the page behind it
operable, so a destructive confirm can be bypassed by clicking past it.

**Where it doesn't.** A tooltip on a focusable trigger that contains only a
short label is the one case where nothing interactive is lost, and that is
exactly the case the native `title` attribute was meant for and still does
badly, see `form-tells` in `ai-tells.md`.

**In code.** Hover- and focus-triggered content must be dismissible without
moving the pointer, hoverable (the pointer can travel onto it without it
vanishing), and persistent until dismissed or invalidated, SC 1.4.13 (AA)
`[spec]`. A tooltip that disappears when the pointer crosses the gap between
trigger and bubble fails it, and the usual cause is a gap with no padding
bridging it.

---

## `backdrop-spec`: Dim Enough to Mean It · medium

> The backdrop says the page behind is out of play. If it reads as a tint, it
> is not doing that.

**Numbers.** **25 to 50% black** over the page `[convention]`. Material's scrim
sits at 32%, which is a reasonable default for light mode.

**Dark mode is a separate value, not the same one.** Over a near-black page a
32% black scrim moves almost nothing, so the separation has to come from the
overlay's own surface and shadow instead, see `overlay-surface`. Raising the
scrim toward 60% on dark is the usual mistake: it darkens an already dark page
and the overlay still does not separate.

**Why it holds.** The backdrop carries two jobs at once, saying the page is
inactive and raising the overlay's apparent contrast against it. A value chosen
for the first without checking the second produces the familiar result of a
dialog that is legible but does not feel on top of anything.

**Where it doesn't.** A non-modal popover or menu gets **no backdrop at all**.
Dimming the page behind a thing that does not block the page is a lie about what
is interactive. A transparent click-catching layer for outside-press detection
is not a backdrop and must not be visible.

**In code.** `backdrop-filter: blur()` is a per-frame compositing cost over the
whole covered area, see `motion.md → animation-performance`, so it is the first
thing to drop on a low-end device rather than the thing to add for polish.
**Animate the backdrop's opacity, never the sheet's transform and the backdrop
together on one property**, or the backdrop drags with the gesture and the page
appears to move.

---

## `dialog-to-sheet`: Below 600px a Dialog Is a Sheet · medium

> On a phone a centred dialog is in the wrong place. The same content belongs
> at the bottom edge.

**Numbers.** Switch at the **600px** viewport width `[convention]`, which is
also where `spacing-layout.md → content-breakpoints` puts the single-column
boundary, so the two should not be separate numbers in one project.

**Why it holds.** Three things change at once on a phone. The software keyboard
takes the lower half of the screen and a vertically centred dialog ends up
behind it. The thumb reaches the bottom of the screen and not the middle. And a
dialog narrower than the viewport wastes the only dimension there is. A sheet
answers all three without a second layout.

**Where it doesn't.** An **alert** stays centred at every width. It is short,
it demands a decision before anything continues, and a sheet reads as
dismissible in a way an alert must not. Keep the sheet for content and forms.

**In code.** One component, two presentations, chosen by a media query rather
than by user agent. The dismiss contract changes with the presentation, see
`dismiss-contract`: a sheet gains drag-to-dismiss, which a centred dialog has
no gesture for.

---

## `sheet-drag-contract`: The Sheet Follows the Finger · high

> One to one with the finger while dragging, physics on release, and never a
> fight with the content inside it.

**Numbers.**

| Behaviour | Value |
|---|---|
| Dismiss by distance | past **25%** of the sheet's height `[convention]` |
| Dismiss by velocity | above **0.11px/ms**, see `motion.md → gesture-physics` `[convention]` |
| Resistance above the top edge | diminishing, roughly **a third** of the travel |
| Release below both thresholds | springs back, see `motion.md → spring-physics` |

**Velocity has to be checked independently of distance.** A quick flick that
travels 10% of the height is a dismiss, and a slow drag past 40% that stops and
reverses is not.

**Why it holds.** A sheet is the one overlay the user holds. Any lag between
finger and surface is read as the device being slow rather than the animation
being wrong, which is why the drag runs on the compositor and not through a
state update per pointer event.

**Where it doesn't.** **A sheet with its own scrolling content does not drag
from everywhere.** Start the drag only when the inner scroller is at
`scrollTop: 0`, and otherwise let the scroll win. Getting this wrong is the
single most common sheet bug: the user tries to scroll back up and dismisses the
sheet instead, losing what they typed.

**In code.** `touch-action: none` belongs on the handle and the non-scrolling
header, **never on the scrollable body**, where it disables scrolling outright.
Capture the pointer on drag start and ignore additional touch points, both per
`gesture-physics`. A sheet that can be dragged must still be dismissible by
keyboard, see `dismiss-contract`.

---

## `grab-handle`: An Affordance With a Hit Area · medium

> The handle is how a sheet says it can be dragged. It is also a button.

**Numbers.** A bar of roughly **32 to 40px wide and 4px tall**, centred, with
**at least 8px of clearance** above and below `[convention]`. Its interactive
area is the full width of the sheet header and **at least 44px tall**, see
`interaction.md → touch-target` and `a11y-implementation.md →
hit-area-extension`.

**Why it holds.** Drag is invisible until tried. The handle is the only part of
a sheet that advertises the gesture, and a 4px bar with a 4px hit area
advertises something the user then cannot grab.

**Where it doesn't.** A sheet that cannot be dismissed by dragging must not show
a handle. The handle is a claim about behaviour and an inert one is worse than
none, which is also why a decorative handle on a desktop dialog reads as broken.

**In code.** **Tapping the handle closes the sheet.** Users try it before they
try dragging, and a handle that ignores a tap looks unresponsive. Give it a real
accessible name, not an empty `div`, see `native-elements-first`.

---

## `scroll-lock`: Lock Without the Shift · high

> Locking the page behind an overlay is one line. Doing it without moving the
> page is the rule.

**Numbers.** `overflow: hidden` on the document removes the scrollbar, and on a
pointer platform that scrollbar occupies **12 to 17px** of layout width, so
every centred element behind the overlay jumps sideways as it opens `[measured,
per platform]`.

**In code.**

```css
html { scrollbar-gutter: stable; }   /* reserve it always, CSS Overflow 3 [spec] */
```

Reserving the gutter at the document level costs nothing while unlocked and
removes the shift entirely. The alternative, adding `padding-right:
scrollbarWidth` at open time, has to be undone on close and has to be applied to
every fixed element as well, which is why it is usually applied to one of them
and the header still jumps.

**Why it holds.** The shift happens at the exact moment attention moves to the
overlay, so it is rarely noticed in review and consistently noticed in use. It
is also a layout shift in the `content-bleeds-controls-float` sense: the page
moved without the user asking.

**Where it doesn't.** A non-modal popover locks nothing. If the page cannot be
scrolled while a menu is open, the menu is behaving as a dialog and should be
one, see `overlay-taxonomy`.

**And the background must not scroll through the overlay.**
`overscroll-behavior: contain` on the overlay's scroller, per `focus-trap`,
stops the scroll chaining out of it when it reaches its own end.

---

## `anchor-collision`: Flip, Then Shift, Then Clamp · medium

> An anchored overlay never renders off screen, and it never covers its own
> trigger.

**Numbers.** In order: **flip** to the opposite side when the preferred side
does not fit, **shift** along the cross axis to stay inside, then **clamp** the
height to the space left and scroll inside. Keep **8 to 16px of collision
padding** from the viewport edge `[convention]`.

**Why it holds.** The three steps are ordered by how much they distort the
relationship between trigger and overlay. Flipping keeps the connection,
shifting weakens it, clamping changes the overlay itself. Doing them in the
wrong order produces a menu that scrolls internally when it could simply have
opened upward.

**Where it doesn't.** A tooltip **shifts but does not flip** if flipping would
put it where the pointer is travelling, and a long menu on a short viewport
clamps rather than flipping, because a flipped long menu runs off the other
edge.

**In code.** Scale from the trigger using the positioning library's own origin
variable, per `motion.md → transform-origin`, and set the clamp with the
available-space variable rather than a fixed `max-height`:

```css
.menu { max-height: var(--radix-popper-available-height); overflow-y: auto; }
```

**The focused control must not end up hidden behind it.** SC 2.4.11 Focus Not
Obscured (Minimum), AA in WCAG 2.2 `[spec]`, is failed by a sticky overlay that
covers the element the keyboard just reached, see `focus-not-obscured`.

---

## `focus-not-obscured`: Nothing Covers What the Keyboard Reached · high `[spec]`

> If the focused element can be completely hidden by a sticky bar, a toast or a
> panel, the keyboard user is operating blind.

**Numbers.** SC 2.4.11 Focus Not Obscured (Minimum) is **AA in WCAG 2.2**: no
part of the focused component may be entirely hidden by author-created content.
SC 2.4.12 raises it to **no part obscured at all** at AAA `[spec]`.

**Why it holds.** It is a keyboard-only failure, invisible to anyone testing
with a mouse, and sticky headers plus toasts plus skip links make it common.
Tabbing into a form behind a bottom-anchored toast is the standard
reproduction.

**Where it doesn't.** Content the user can dismiss, and content that moved there
because the user opened it, are judged on whether the dismissal is reachable,
not on the overlap alone. A modal dialog does not fail this for the page behind
it, because that content is `inert` and holds no focus.

**In code.** `scroll-margin-top` equal to the sticky header's height keeps
scrolled-to targets clear of it:

```css
:target, [tabindex], a, button { scroll-margin-top: var(--header-h); }
```

Toasts anchored to an edge need the same clearance against whatever is focusable
underneath, which is the practical reason for `toast-budget`'s cap.

---

## `dismiss-contract`: Esc Always, Backdrop Sometimes · high

> Every overlay states, before it is built, how it can be left. The three ways
> are not interchangeable.

**Numbers.**

| Overlay | Esc | Outside press | Close button |
|---|---|---|---|
| Tooltip, popover | yes | yes | not needed |
| Menu | yes | yes | no |
| Dialog, sheet | yes | **only when nothing is lost** | yes |
| Destructive confirm | yes, cancels | **no** | yes, labelled |

**Why it holds.** Esc is the one dismissal every keyboard user already knows and
it costs nothing, which is why it has no exception in the table. Outside press
is the one that silently destroys work: a half-filled form in a dialog, closed
by a misplaced click, with no undo. The cost of the mistake, not the type of the
overlay, decides whether it is allowed.

**Where it doesn't.** An overlay the flow depends on, a required consent step or
a blocking error, has no dismissal other than its own actions, and then **the
actions must be the only way out and must be visible without scrolling.**

**In code.** Return focus to the trigger on every path out, per `focus-trap`,
including Esc and outside press, which are the two paths that usually skip it.
Where outside press is disabled, a nudge animation on the attempt tells the user
the click registered and was refused, which is better than nothing happening.

---

## `overlay-stacking`: Three Tiers, Depth Two · medium

> Overlays live in a small number of named tiers, and an overlay that opens an
> overlay is usually a flow that was never designed.

**Numbers.** Three tokenised tiers `[convention]`: **page chrome** (sticky
headers, fixed bars), **overlay** (popovers, menus, dialogs, sheets), and
**notification** (toasts, critical banners), which sits above the others so a
toast is visible over a dialog. **Nesting stops at depth two.**

**Why it holds.** Raw `z-index` numbers in component files are the reason
products end up with `9999` and then `10000`. Tiers are a vocabulary, so the
question becomes which tier this belongs in, which has an answer, rather than
which number is high enough, which does not.

Depth is a separate limit. A dialog opening a dialog means the first one asked
for something it did not have, and the user now has two states to unwind and two
Esc presses to remember.

**Where it doesn't.** A **select inside a dialog** is depth two and legitimate,
as is a confirm on top of a form dialog, which is the canonical case for
spending the second level. A third level is a redesign, not a z-index.

**In code.** Render overlays in a portal at the document root so stacking is
decided by the tier and not by a parent's `overflow` or `transform`. An ancestor
with `transform` creates a containing block that a fixed overlay inside it
cannot escape, which is the usual cause of a dialog clipped by a card.

---

## `overlay-surface`: An Overlay Declares Its Level · medium

> The shadow says what kind of overlay this is. Giving a menu the modal's
> shadow makes it read as a modal.

**Numbers.** Per `depth-and-icons.md → elevation-system`: **menus and dropdowns
at level 2 to 3, dialogs and sheets at 4 to 5.** The overlay's own background
is **opaque**, or its text contrast depends on whatever happens to be behind it,
which cannot be measured, see `color.md → wcag-contrast`.

**Why it holds.** Elevation is the only cue that separates a transient surface
from a blocking one before the user interacts. When both carry the same shadow,
the backdrop becomes the only signal, and non-modal overlays have no backdrop.

**Where it doesn't.** A translucent material (`backdrop-filter` plus a tinted
background) is a deliberate platform look, and then **the tint has to be heavy
enough that the worst case behind it still clears 4.5:1**, measured over the
busiest content it can sit on rather than over a neutral page.

**In code.** A shadow token per tier, never a hardcoded shadow in an overlay
component, per `elevation-system`. On dark surfaces the shadow does little and
the separation comes from a lighter surface plus a hairline, see
`interface-craft.md → border-discipline` and `surfaces.md → shadow-as-border`.

---

## `toast-budget`: Three Visible, Then Queue · medium

> A toast is for something that happened outside the user's focus, and it is
> never where a decision goes.

**Numbers.** At most **three visible at once**, queue the rest.
**4 to 6 seconds** for an informational toast, long enough to read a short
sentence twice `[convention]`. **Errors and anything with an action do not
auto-dismiss.** Hover, focus or a touch on the stack pauses every timer.

**Why it holds.** Toasts arrive unannounced, so the user's reading starts after
the animation, not with it. A timed dismissal is a race against a reader who did
not know the race began, which is why the only safe auto-dismissal is one where
missing the message costs nothing.

**Where it doesn't.** A confirmation of something the user just did needs no
toast at all. The content arriving is the confirmation, and a toast on top of it
is a second notification of the same event, see `states.md` on retries.

**In code.** Announce them in a polite live region, per `a11y-implementation.md
→ live-regions`, not in an alert region, which interrupts. Stack them in one
region rather than mounting several, or screen readers announce the container
each time. Keep them clear of focusable content underneath, per
`focus-not-obscured`.
