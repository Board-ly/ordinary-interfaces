# Motion

20 rules. Almost all `[convention]`, practitioner craft from shipped products
rather than perception studies. Still specific, still checkable, which is what
matters. The one hard `[spec]` is `prefers-reduced-motion`.

**Every value here is exact, not a range to approximate.**
`cubic-bezier(0.2, 0, 0, 1)` is not `cubic-bezier(0.4, 0, 0.2, 1)`.

---

## `animation-necessity`: Ask Whether, Before Asking Which · high

> Frequency decides. The first question is never the easing curve.

| Frequency | Decision |
|---|---|
| **100+/day.** Shortcuts, command palette | **Never animate** |
| **Tens/day.** Hover, list navigation | remove or drastically reduce |
| **Occasional.** Modals, drawers, toasts | standard animation |
| **Rare.** Onboarding, celebration | delight is allowed |

**Why it holds.** An animation is a cost paid on every repetition, and charm
amortises badly. Raycast has no open/close animation, which is correct for
something opened hundreds of times a day. **Never animate keyboard-initiated
actions**, the user who reached for a shortcut was optimising for speed.

**Every animation answers "why does this animate?"** Valid answers: spatial
consistency (a toast entering and leaving the same way makes swipe-to-dismiss
obvious), state indication, feedback, or preventing a jarring cut. **If the only
answer is "it looks cool" and users see it often, do not animate it.**

---

## `animation-duration`: Under 300ms · high

| Element | Duration |
|---|---|
| Button press | **100–160ms** |
| Tooltip, small popover | **125–200ms** |
| Dropdown, select | **150–250ms** |
| Modal, drawer | **200–500ms** |
| Marketing, explanatory | longer is fine |

**UI animation stays under 300ms** `[convention]`. A 180ms select feels more
responsive than a 400ms one, and *feels* is the entire measure, since both
complete faster than the user can act on either.

---

## `easing-curves`: Ease-Out by Default · high

| Situation | Curve |
|---|---|
| Entering or exiting | **ease-out.** Starts fast, reads as responsive |
| Moving on screen | ease-in-out |
| Hover, color change | ease |
| Constant motion | linear |

**Never `ease-in` for UI.** It starts slow and reads as sluggish: a 300ms
`ease-in` dropdown *feels* slower than a 300ms `ease-out` one at identical
duration. That is the whole argument, perceived responsiveness is set by the
first frames.

**Built-in CSS easings lack punch.** Use custom curves:

```css
--ease-out:    cubic-bezier(0.23, 1, 0.32, 1);
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);  /* iOS-like */
```

---

## `enter-exit-asymmetry`: Slow to Decide, Fast to Respond · high

> Exit is faster than enter. The user has already committed.

```css
.overlay                { transition: clip-path 200ms ease-out; }  /* release: snap */
.button:active .overlay { transition: clip-path 2s linear; }       /* press: deliberate */
```

Identical enter and exit timing is a reliable tell that the timings were never
considered.

---

## `subtle-exit`: Exits Do Not Fight for Attention · medium

> Small fixed `translateY`, around −12px. Never the full container height.

**Numbers.** Exit **150ms** against an enter of **300ms**. `ease-out` in both
directions. Keep some directional movement so the departure has a direction.

**Sometimes `display: none` is correct.** Remove immediately when motion adds no
information, the interaction repeats frequently, or reduced motion is requested.
Reserve a full slide-out for cases where spatial context matters: a card
returning to a list, a drawer closing.

---

## `never-scale-zero`: Nothing Appears From Nothing · high

> Start at `scale(0.95)` with `opacity: 0`.

```css
/* Bad  */ .entering { transform: scale(0); }
/* Good */ .entering { transform: scale(0.95); opacity: 0; }
```

**Press feedback is the same principle inverted:** `scale(0.96)` on `:active` at
~160ms `ease-out`. Below 0.95 the press reads as exaggerated. See
`surfaces.md → press-scale`.

---

## `transform-origin`: Popovers Scale From Their Trigger · medium

```css
/* Radix   */ .popover { transform-origin: var(--radix-popover-content-transform-origin); }
/* Base UI */ .popover { transform-origin: var(--transform-origin); }
```

**Modals keep `transform-origin: center`.** They are not anchored to anything,
so a directional origin is wrong rather than merely unnecessary.

**Tooltips skip the delay on subsequent hovers.** The first takes a delay, which
prevents accidental activation; once one is open, neighbours open instantly with
no animation, `.tooltip[data-instant] { transition-duration: 0ms; }`.

---

## `stagger`: Cap the Run · medium

> **30–80ms** between items `[convention]`, capped at about **6 items / 180ms**.
> Everything after lands at once.

Staggering 40 rows produces a ~1.2s wipe that reads as slow; staggering 500 is a
performance bug. **Stagger is decorative and must never block interaction while
it plays.**

---

## `staged-enter`: Split Semantic Chunks · medium

> For an infrequent staged entrance where sequence communicates hierarchy.

**Numbers.** Split the container into semantic chunks, title, description,
buttons, and stagger by **~100ms**. For titles, consider splitting into words at
**~80ms**. Combine `opacity`, `blur(4px→0)` and `translateY(12px→0)`.

Animating one container gets you less for the same cost. **Never stagger routine
interactions**, row hovers, keystrokes, repeated tab changes.

**The three stagger numbers in this skill describe different things and all
three stand:** ~100ms between semantic chunks on a staged entrance, 80ms between
words in a split title, 30–80ms capped at ~6 between list items. The cap matters
most for lists.

---

## `icon-transitions`: Contextual Icon Swaps · medium

> Animate `opacity`, `scale` and `blur`. Never toggle visibility.

| Property | From → To |
|---|---|
| `scale` | **0.25 → 1** |
| `opacity` | **0 → 1** |
| `blur` | **4px → 0px** |

**With a motion library**, match the package's own import path and use
`transition: { type: "spring", duration: 0.3, bounce: 0 }`. **Bounce is always
0.** **Without one**, keep both icons in the DOM with one absolutely positioned
and cross-fade with `cubic-bezier(0.2, 0, 0, 1)`, enter and exit, no dependency.

Use this for the outline↔fill state swap
(`depth-and-icons.md → icon-color-states`).

---

## `spring-physics`: Springs for Interruptible Motion · medium

> Springs maintain velocity when interrupted. CSS animations restart from zero.
> That is the entire reason to reach for one.

**Use for:** drag with momentum, elements that should feel alive, gestures
interruptible mid-flight, decorative mouse tracking.

```js
{ type: "spring", duration: 0.5, bounce: 0.2 }            // Apple-style
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }  // traditional
```

**Bounce 0.1–0.3, subtle.** Avoid bounce in most UI, reserve it for
drag-to-dismiss and deliberately playful interactions.

---

## `gesture-physics`: Drag Should Obey Physics · medium

- **Momentum dismiss:** `velocity = |distance| / elapsedMs`. Above **0.11**, dismiss regardless of the distance threshold, a flick should be enough.
- **Damp at boundaries:** dragging past a limit gets diminishing returns. Real objects slow before stopping; they do not hit walls.
- **Capture the pointer** once a drag starts, so it survives the pointer leaving the element.
- **Ignore additional touch points** after a drag begins, or switching fingers makes the element jump.

---

## `animation-performance`: Transform and Opacity Only · high

> They skip layout and paint and run on the GPU. Everything else triggers all
> three rendering steps.

- **CSS beats JS under load.** CSS animations run off the main thread; when the browser is busy, JS animations drop frames and CSS stays smooth. Use CSS for predetermined animation, JS for dynamic or interruptible.
- **Framer Motion caveat:** the `x` / `y` / `scale` shorthand is **not** hardware-accelerated, it runs `requestAnimationFrame` on the main thread. Use `animate={{ transform: "translateX(100px)" }}` where frames matter.
- **CSS variables inherit**, so setting one on a container triggers recalculation on every child. During a drag, set the transform on the element itself.
- **WAAPI** gives JS control at CSS performance: `element.animate([...], { duration, easing, fill: 'forwards' })`.
- **Prefer percentage translates.** `translateY(100%)` is relative to the element's own size and works at any dimension.
- **Keep `blur()` under 20px** (Safari). A 2px blur during an awkward crossfade is a legitimate way to mask a transition that will not tune cleanly.

**Use transitions, not keyframes, for interruptible UI.** Transitions retarget
mid-flight; keyframes restart from zero. For anything firing rapidly, toasts,
state toggles, transitions are visibly smoother.

`@starting-style` handles enter states without the mount dance.

---

## `transition-specificity`: Name the Properties · high

> Never `transition: all`, and never Tailwind's `transition-all`.

```css
/* Good */ .button { transition-property: scale, background-color; transition-duration: 150ms; }
/* Bad  */ .button { transition: all 150ms ease-out; }
```

`all` makes the browser watch every property, produces transitions on properties
you never intended to animate, and blocks optimisation.

**Tailwind specifics.** Bare `transition` maps to a curated list, colors,
opacity, shadow, transforms, rather than `all`; better, but still name what
changes. `transition-transform` covers `transform, translate, scale, rotate`. For
several non-transform properties use `transition-[scale,opacity,filter]`.

---

## `will-change-discipline`: A Hint, Not a Habit · medium

> Only `transform`, `opacity` and `filter`. Never `all`. Add it when you observe
> first-frame stutter, not before.

`will-change` pre-promotes an element to its own GPU layer. Without it the
browser promotes when the animation starts, and that one-time promotion can cause
a micro-stutter on the first frame. For properties the GPU cannot composite it
does nothing at all, and a permanent layer on many elements costs memory.

---

## `hover-gating`: Gate Hover to Real Pointers · high

```css
@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.05); }
}
```

**Touch triggers hover on tap.** An ungated hover animation fires as a false
positive on every mobile tap and frequently sticks until the next tap elsewhere.

---

## `motion-restraint`: Motion Is Never the Only Channel · high

> Every animated state change also carries a static cue: color, an icon, or a
> label.

**That second half is an accessibility requirement, not a preference.** A user
with reduced motion set, or anyone who looked away during the transition, gets no
information at all from motion alone. It is the motion counterpart of "never
color alone" (SC 1.4.1).

**High-frequency interactions get instant feedback**, or a transition of **150ms
or less** on opacity and color. A custom animation there charges its attention
cost on every trigger.

**Skip animation on first render.** `initial={false}` on `AnimatePresence`, then
check it left intentional page entrances intact.

**When reviewing, slow it down.** What feels off at 10% speed in the browser's
Animations panel is what is subtly wrong at full speed.

---

## `reduced-motion`: Gentler, Not Absent · **critical** `[spec]`

> `prefers-reduced-motion: reduce` means fewer and gentler. **Never no feedback.**

- **Keep** opacity and color transitions, not vestibular triggers, and they still hide seams.
- **Drop** translate, scale and stagger. Reveal groups at once.
- **Replace** a rollback animation with a static marker held longer (~600ms). The user still needs to perceive that something reverted.
- **Skeletons stay; the shimmer goes.**

**A state change with no perceptible signal is worse than an animated one.**

Two rules hold **regardless** of the preference: autoplaying media needs a
visible pause control, and toasts carrying an action or an error stay until
dismissed.

Flash thresholds and SC references: `interaction.md → wcag-motion`.

---

## `seam-principle`: Most Transition Problems Are Layout Problems · high

> Three ways to handle a cut, in order of preference.

1. **No seam.** The two states occupy identical geometry, so the swap is imperceptible. A skeleton row exactly the height of a real row needs no transition at all. **This is a layout decision, not a motion one, and it is always best.**
2. **Soft seam.** Geometry differs slightly: fade the incoming content **only**. **Never crossfade.** Two overlapping opacity ramps produce a muddy midpoint where both are half-visible.
3. **Loud seam.** Geometry differs a lot and the change is meaningful. Animate deliberately so the user can track what moved. Reserved for changes the user caused and should notice.

**Before tuning a curve, check whether the two states could simply be the same
size.** If you are reaching for a loud seam on a state the user did not trigger,
the state was probably designed wrong.

---

## `reveal-choreography`: Group by Perceptual Unit · high

> The staircase is the most common smoothness failure in an otherwise well-built
> page.

Header at 200ms, sidebar at 400ms, content at 600ms, avatars at 900ms: four
layout shifts, every region individually correct, and the page visibly assembling
itself.

- **Group by perceptual unit, not by request.** Regions that read as one thing reveal as one thing, even when fed by three endpoints.
- **Coherence window ~120ms.** Once the first member resolves, wait up to 120ms for the rest, then reveal what you have and let stragglers fill in.
- **Rank the groups.** Primary content first, always. Chrome, counts, avatars and secondary metadata after. Never before.
- **Reserve everything above the fold.** Anything with knowable dimensions holds its box from first paint. A reveal that shifts layout is not a reveal, it is a jump.

---

## `state-transition-timing`: The Reference Table · high

Starting values `[convention]`, tune to the product's tempo, but **keep the
relationships between them**.

| Transition | Duration | Easing | Note |
|---|---|---|---|
| Loader delay guard | **250ms** | n/a | before showing anything |
| Loader minimum display | **400ms** | n/a | measured from appearance |
| Skeleton → content, geometry matches | **0ms** | n/a | just swap |
| Skeleton → content, geometry differs | 150ms | ease-out | fade content in only |
| Spinner → content | 150ms | ease-out | always needed |
| Empty → first item | 200ms | ease-out | with `scale(0.98→1)` |
| Empty state out | 100ms | ease-in | before the item enters |
| Last item removed → hold | 150ms | n/a | then collapse |
| Error in | 120ms | ease-out | opacity only |
| Error out on success | 100ms | ease-in | no toast |
| Optimistic apply | 120ms | ease-out | |
| Optimistic rollback | **300ms** | ease-in-out | deliberately slower |
| Stagger step | 30ms | n/a | cap at 6 items |
| Group coherence window | 120ms | n/a | then reveal partial |
| Value change highlight | 400ms | ease-out | flash, do not count up |

**Do not animate the skeleton out.** It is scaffolding, and watching scaffolding
leave draws attention to the fact it was there. **Stop the shimmer before
removal** or it flickers.

**The minimum-display floor is measured from when the loader appears**, not from
request start, and holds through the fade. Otherwise a 410ms response produces a
loader that appears and immediately begins dissolving.

---

## `numbers-in-motion`: Changing Values Jitter · medium

- **Tabular numerals, always.** Proportional digits make a counter twitch on every change.
- **Reserve width for the plausible maximum.** 9 → 10 should not resize the container.
- **Do not roll digits** on a frequently-changing value. Odometer animations are charming once and nauseating on a live figure.
- **A brief highlight beats a count-up.** Flash the changed value for ~400ms rather than animating through intermediate numbers the reader may take as real.
- **Zero gets the same slot.** A badge that appears and disappears reflows its neighbours; fade opacity instead.
