# Controls, Forms & Navigation

8 rules. Hit area is a gate; button states are where most component work actually
goes wrong.

---

## `touch-target`: Size the Hit Area, Not the Glyph · **critical** `[spec]`

> 24×24 is the floor. 44×44 on touch and 40×40 on desktop is the target. Padding
> counts.

**Numbers.**

| Value | Source |
|---|---|
| **24×24px** | WCAG 2.2 AA floor, SC 2.5.8 |
| **44×44px** | WCAG 2.2 AAA (SC 2.5.5), and Apple HIG |
| **48×48dp** | Material Design |
| **8px** | minimum spacing between adjacent targets |
| 76×76dp | driving and in-motion contexts (Google Design for Driving) |

**Why it holds.** A finger pad is 10–14mm, which at the 96 DPI CSS reference
pixel is roughly **38–53px** `[measured]`, the 44px recommendation sits at the
low end of the range people actually present to the screen. Below it, error rates
rise measurably, and they rise fastest for users with reduced motor precision.
Touch accuracy declines about **15% per decade after 40**, so this degrades with
the audience rather than staying fixed.

**In code.** A 24px icon with 10px padding all round is a 44px hit zone, that is
the correct construction, and the visible glyph stays small. Spacing can also
substitute for size: an undersized target passes when 24px of clear space
surrounds it.

**Where it doesn't.** Instagram's like button works small because of the spacing
buffer around it, not because 20px is fine. The exception proves the spacing
rule rather than the size one.

Implementation, collision rules and the spacing exception in detail:
`a11y-implementation.md → hit-area-extension`.

---

## `button-design`: Six States, All Defined · high

> A button with three states is a button that feels broken in the other three.

**Numbers.**

| State | Treatment |
|---|---|
| Normal | solid fill, label at ≥**4.5:1** `[spec]` |
| Hover | darken **10–15%** HSL-L (lighten on dark surfaces), `cursor: pointer`, ~150ms |
| Focus | **2px** outline, **2px** offset, ≥**3:1** against adjacent background (SC 2.4.11) `[spec]` |
| Active | darken **20–30%**; optionally 1px inset shadow and 1px `translateY` |
| Disabled | **40% opacity** on the whole button `[convention]`, `cursor: not-allowed`, `aria-disabled="true"` |
| Loading | label → spinner, stays disabled |

**Hierarchy:** at most **one primary and one secondary per section**. Never two
equally weighted calls to action. That is not a choice, it is a stall.

**Why each one earns its place.** Hover confirms the target before commitment;
active confirms the press registered, closing the feedback loop; loading prevents
the double-submit race, which is a correctness issue rather than a polish one.
Focus exists for keyboard and switch users, and missing or inadequate focus
indicators rank among the most common failures in WebAIM's 2024 survey
`[measured]`.

**Disabled is opacity, not color.** Take the normal state and set opacity to 0.4.
Changing hue instead produces a state that reads as "different" rather than
"unavailable", and it fails for color-blind users specifically.

**Where it doesn't.** Dark mode inverts the hover direction, define both, do not
assume. Destructive actions are always two-step: red plus a confirmation, never
one irreversible click. Icon-only buttons need `aria-label` and a 44×44 target
even at a 24px glyph. Ghost buttons over images need their border checked against
whatever sits behind it.

**Tiers:** primary is a solid fill, one per section; secondary is outline or
ghost at the same size and lower weight; tertiary is text only.

---

## `button-padding`: Compensate for the Icon's Mass · high

> Symmetric padding centres geometry, not visual weight.

**Numbers.**

| Case | Padding |
|---|---|
| Text only | 8–12px vertical, 16–24px horizontal, desktop `8px 16px`, touch `10px 24px` |
| Leading icon | reduce icon-side padding by the gap value, MD3: 24dp text side, **8dp gap**, 16dp icon side |
| Trailing icon | the same, mirrored |
| Icon only | `(target − icon) / 2`, a 48px target with a 24px icon is 12px all round |

**Why it holds.** An icon adds mass on one side and the gap between icon and
label inflates that side further, so equal numeric padding lands the optical
centre off-centre. This is a Gestalt effect `[convention]`, MD3 applies the
compensation consistently; neither Apple HIG nor WCAG require it.

A simpler heuristic that works: **icon-side padding = text-side − 2px.**

**Where it doesn't.** Large icons (20–24px) with full gap compensation
over-correct, back off 2–4px. Filled icons carry more optical weight than
outline and need slightly more. **RTL:** use `padding-inline-start`/`-end` so the
asymmetry flips automatically. All values are approximate; fine-tune ±2–4px by
eye.

---

## `link-design`: The Underline Is the Affordance · medium

> Inline links are underlined. Removing it on hover is backwards.

**Why it holds.** Color alone fails SC 1.4.1 `[spec]`, and a link must be
distinguishable from surrounding text at **3:1** without relying on color at all.
The underline is the non-color channel; taking it away on hover removes the
affordance at the exact moment the user is confirming the target.

**In code.** Inline links always underlined. Standalone and navigation links can
use color plus a hover underline. **Visited state is required.** It is spatial
orientation, telling people where they have already been. `target="_blank"`
announces itself via `aria-label` or visually-hidden text; an icon alone is not
sufficient for screen reader users (WCAG G201).

**Where it doesn't.** Actions use buttons, navigation uses links, semantically
distinct and not interchangeable. Too many inline links destroys the scan path
regardless of styling.

---

## `wcag-forms`: Label, Describe, Don't Re-Ask · high `[spec]`

| SC | Requirement |
|---|---|
| 3.3.1 (A) | the failing item is identified and the error described **in text** |
| 3.3.2 (A) | every input that requires input has a label or instruction |
| 3.3.3 (AA) | when a correction is known, offer it |
| 3.3.7 (A) | data already given in the same process is auto-filled or selectable |
| 3.3.8 (AA) | no cognitive-function test at any authentication step without an alternative |

**Why it holds.** Unlabelled inputs are announced as "edit, blank", the user
cannot determine what to type. Errors carried by color alone reach neither screen
reader users nor color-blind users. Re-entry places disproportionate cost on
users with cognitive and motor disabilities. And CAPTCHA blocks a large share of
users with cognitive, visual and motor disabilities outright, password manager
support, paste, passkeys and magic links all qualify as alternatives.

**The failures that actually occur.** Red border with no text. **Placeholder as
the only label**, it disappears on input and most browsers do not expose it as
an accessible name. Inline validation that clears the error before the user can
navigate to it. Multi-step checkout re-asking for an address. Password fields
blocking paste, which breaks password managers.

WebAIM's 2024 survey found missing form labels on **over 45%** of home pages
`[measured]`.

**In code.** `<label for>` or `aria-label`/`aria-labelledby` on every input.
Prefix errors with "Error:", place them adjacent to the field, and use
`role="alert"` so they announce on injection. Adding `autocomplete` attributes
satisfies 3.3.7 for the common cases on its own.

---

## `wcag-navigation`: Predictability Across Pages · high `[spec]`

| SC | Requirement |
|---|---|
| 2.4.2 (A) | descriptive `<title>` identifying the page distinctly |
| 2.4.4 (A) | link purpose determinable from the text or its programmatic context |
| 2.4.6 (AA) | headings and labels describe their topic or purpose |
| 3.2.3 (AA) | repeated navigation appears in the same relative order on every page |
| 3.2.4 (AA) | the same function is labelled identically everywhere |

**Why it holds.** The page title is the first thing a screen reader announces, so
a framework default ("React App") starts every visit with nothing. Generic link
text is useless in the links-list navigation pattern, which is a standard way to
move through a page. Consistency is not tidiness. It is what users with memory
and cognitive impairments rely on to carry a model between sessions.

**In code.** `"[Page], [Site]"`, updated programmatically on client-side
navigation. `aria-label` or visually-hidden text on "Read more" links. One `<h1>`,
levels nested without skipping, and never a heading tag chosen for its default
size. **Lock the DOM order** and reposition visually with flex `order` or Grid
placement. Reordering the DOM per breakpoint fails 3.2.3. Keep a controlled
vocabulary for component labels: "Search" on one page and "Find" on another fails
3.2.4.

---

## `wcag-images`: Equivalent Purpose, Not Description · **critical** `[spec]`

> The alternative serves the same *purpose*. For a control, that is the action.

| Content | Requirement |
|---|---|
| Informational image | text conveying the information |
| Control or input | a name describing its **purpose** |
| Time-based media | at minimum descriptive identification |
| Test or exercise | descriptive identification only |
| Sensory content | descriptive identification |
| CAPTCHA | identify the purpose **and** provide an alternative modality |
| Decorative | `alt=""`, or `aria-hidden="true"` on inline SVG |

**Why it holds.** Without an alternative, a screen reader announces the filename,
uninformative and frequently disruptive. Missing alt text is the most common
WCAG failure globally: **over 54%** of home pages (WebAIM, 2024) `[measured]`.

**The failures worth naming.** `alt` set to the filename or the URL. CSS
background images carrying information, they cannot take an alt, so move them
into `<img>`. Inline SVG with no `aria-label` on the parent button, no `<title>`,
and no `aria-hidden`. **Chart alt naming the chart type without the data**,
"Bar chart showing Q3 revenue up 14% year over year", not "bar chart image"; for
complex charts, provide the table or a prose summary adjacent. And **an image
button with `alt=""`**, which strips the accessible name from a control that
requires one.

**Automated tools catch structure and cannot judge quality.** An `alt="image"`
passes axe and fails 1.1.1 in substance. Every image needs a human read.

---

## `wcag-motion`: Flashing and Vestibular Safety · **critical** `[spec]`

> Nothing flashes more than three times a second. Non-essential motion is
> disableable.

**Numbers.** SC 2.3.1 (A): no more than **3 flashes per second**, unless below
both the general flash threshold (flashing area under **25%** of the 10-degree
visual field) and the red flash threshold. SC 2.3.3 (AAA): interaction-triggered
motion animation can be disabled unless essential.

**Why these are not conservative padding.** Photosensitive epilepsy affects
roughly **1 in 4,000**, and the thresholds come from seizure-induction research
`[measured]`. Vestibular disorders affect roughly **35% of adults over 40**, and
motion triggers vertigo and nausea independently of photosensitivity
`[measured]`. 2.3.1 is a **non-interference** criterion, it applies to all
content on the page, including content otherwise out of scope.

**Essential versus not.** Progress indicators, video playback and scroll position
feedback are essential. Parallax, decorative entrance transitions and
scroll-triggered fade-ins are not.

**In code.** Build motion to **opt in.** A no-motion baseline, with motion added
under `prefers-reduced-motion: no-preference`. Carousels and animated banners
need pause/stop/hide controls (SC 2.2.2). **Visual inspection is not a valid test
for flashing**, run PEAT on any suspect content, GIFs and autoplaying video
included. A content advisory is not a substitute.
