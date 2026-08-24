# Color

21 rules. Two are gates you cannot ship past; the rest build a palette that
survives a theme change.

Every rule below follows one schema: **the ruling** (one line, quotable), **the
numbers**, **why it holds** with a primary citation, **where it doesn't**, and
**in code**.

---

## `wcag-contrast`: Contrast Ratio · **critical** `[spec]`

> Body text clears 4.5:1 against what it actually renders on. Large text and any
> control that carries meaning clear 3:1.

**Numbers.** W3C, *WCAG 2.2*, SC 1.4.3 and 1.4.11 (2023):

| Ratio | Applies to | Level |
|---|---|---|
| **4.5:1** | text below 24px regular / 18.66px bold | AA |
| **3:1** | text at or above that, plus UI components, form borders, meaningful icons | AA |
| **7:1** | body text | AAA |
| **4.5:1** | large text | AAA |

Non-text contrast has no AAA tier, 3:1 is the ceiling the spec defines.

The ratio is `(L₁ + 0.05) / (L₂ + 0.05)` over relative luminance, so it runs 1:1
to 21:1. **The margins are one hex digit wide.** `#777777` on white computes to
4.478 and fails; `#767676` computes to 4.542 and passes. Round nothing, and
compute rather than estimate. `scripts/contrast.py` exists for this, and every
ratio in this file came out of it.

**Why it holds.** Luminance ratio is the only contrast model WCAG defines
normatively, and contrast is the failure that actually happens: WebAIM's 2024
*Million* survey found insufficient text contrast on over 80% of home pages
tested, the single most common violation on the web `[measured]`.

**Where it doesn't.** Purely decorative elements, inactive controls and
logotypes are exempt. **A disabled control that still carries information is
not**, greying out the only copy of a value does not make the value optional.
Gradients must be measured at their worst point rather than averaged, which is
where automated checkers quietly pass things. Dark mode is a separate
measurement, never an inversion of a light-mode pair.

APCA models size and stroke weight better than the WCAG formula does, but **it is
not normative for WCAG 2.x** and cannot stand in during an audit or a legal
question. Read it as extra insight, not as a substitute.

**In code.** `#333` on white is 12.63:1 and clears everything. A `#0066cc` focus
ring on white is 5.57:1, AA yes, AAA no; `#0056b3` reaches 7.04:1 if AAA is the
target. Give text and border roles **separate tokens**: `#777777` is a perfectly
good input border at 3:1 and fails as the label sitting above it.

**Two neighbours in the same family.** SC 1.4.1 (A) forbids color as the sole
carrier of meaning, see `red-green-color-blindness`. SC 1.4.13 (AA) requires
hover- and focus-triggered content to be dismissible without moving the pointer,
hoverable (the pointer can travel onto it without it vanishing), and persistent
until dismissed or invalidated.

---

## `red-green-color-blindness`: Never Color Alone · **critical** `[spec]`

> Any state encoded in color carries a second signal: a label, an icon, a
> pattern, or a position.

**Numbers.** Red-green deficiency affects roughly **8% of men and 0.5% of
women**, a 16× gap, because the genes sit on the X chromosome and one working
copy is enough (Birch, *JOSA A* 29(3), 2012) `[measured]`. Deuteranomaly alone,
the milder reduced-sensitivity form, accounts for about 5% of men.

**Why it holds.** Deuteranopia and protanopia collapse red, orange, yellow and
green into one muddy band. Two states a trichromat reads instantly become the
same state. Protanopia additionally *dims* red, so a saturated red that looked
emphatic loses luminance as well as hue, check it against SC 1.4.3 separately,
not just against the color rule.

**Where it doesn't.** This governs **functional** color: status, validation,
data series, selection. Decorative color is unaffected, a green hero background
needs no icon bolted to it. A palette with no red/green pair carrying distinct
meanings is also unaffected.

**In code.** Validation gets a color *and* a ✓/✗ glyph *and* a text label. A
status dot gets a word next to it; a bare colored dot is not accessible. Verify
with a simulator (macOS Color Filters or a Figma plugin) before release, not
after.

---

## `dark-mode-color-adaptation`: Three Axes, Three Jobs · high

> Hold hue, cut chroma, raise tone until it measures. Never invert lightness and
> call it done.

**Numbers.** Reduce chroma by roughly **20–30%** `[convention]`, then lift tone
until the pair clears 4.5:1 for text or 3:1 for controls `[spec]`.

| Axis | Move | Protects |
|---|---|---|
| Hue | unchanged | brand recognition |
| Chroma | −20–30% | perception, kills the neon glow |
| Tone | up, until measured | legibility |

**Why it holds.** On a dark field, high-chroma color appears to emit light
independently of its actual luminance, the Helmholtz-Kohlrausch effect. Cutting
chroma removes the glow without touching hue or the contrast ratio, which is why
the three axes are worth separating rather than eyeballing one blended
adjustment.

**Where it doesn't.** Source colors already low in chroma go muddy under a flat
20–30% cut, scale it proportionally instead. Chroma and tone interact, so a
chroma reduction shaves a little luminance contrast off; re-measure after both
moves, never after one.

**In code.** Hold the hue angle, cut chroma about a quarter, lift tone until
white-on-fill clears 4.5:1 and fill-on-background clears 3:1. Two cautions: CSS
`oklch()` chroma runs roughly **0–0.4**, so a three-digit chroma from a design
tool is a different scale and will not paste in, convert first. And contrast is
measured on the **rendered** result, so resolve overlays and opacity before you
check. Never ship a dark-mode token on an estimate.

---

## `luminance-vs-lightness`: Lightness Is Not Luminance · medium

> Never reason about contrast in HSL.

**Numbers.** `Y = 0.2126R + 0.7152G + 0.0722B`, computed on **linearized**
(gamma-decoded) sRGB. Green carries 71% of perceived brightness; blue carries 7%.

**Why it holds.** HSL's L is a geometric convenience with no photometric basis.
Yellow and blue both sit at L 50% and differ in actual luminance by about 12.8×,
which is how you get a 1.07:1 pair that looks like it should be fine. CIELAB's L*
is perceptual lightness and is closer, but WCAG is defined on Y, so Y is what an
audit computes.

**Where it doesn't.** Y under-predicts the apparent brightness of saturated blues
and magentas (Helmholtz-Kohlrausch again), and CIELAB does not model that either.
Neither is a licence to go below the floor.

---

## `cielab-color-space`: Perceptually Uniform Spaces · medium

> Use CIELAB or OKLCH for color *difference*; use luminance for contrast. They
> answer different questions.

**Numbers.** L* runs 0–100; a* is green↔red, b* is blue↔yellow, against a stated
white point (D50 or D65). Difference is ΔE. Industry practice reads **ΔE00 ≈ 2**
as an acceptable match and **≈ 5** as visibly different `[convention]`.

**Why it holds.** MacAdam (*JOSA* 32(5), 1942) measured just-noticeable color
differences and found them forming ellipses of varying size in CIE space, so
Euclidean distance there does not track perception. CIELAB (CIE, 1976) reshapes
the space so those ellipses come closer to circles. The 1976 ΔE formula is still
non-uniform at high chroma, which CIEDE2000 (Luo, Cui & Rigg, *Color Research &
Application* 26(5), 2001) corrects with chroma- and hue-weighted terms.

**Where it doesn't.** ΔE values from different formulas are not comparable, and
**a ΔE or an L* delta is never a substitute for a WCAG ratio**. Lab values are
only comparable under the same white point.

**In code.** Generate tint and shade ramps in a uniform space so each step reads
as an equal jump instead of bunching at one end. CSS takes it directly:
`lab(52.2% 40.2 60)`, `lch(52.2% 72.8 56.2deg)`.

---

## `ramp-structure`: A System Is Ramps, Not Colors · high

> One neutral ramp, one accent ramp, and only the status ramps the product
> actually renders.

**Numbers.**

| Ramp | Count | Carries |
|---|---|---|
| Neutral | 1 | 80–90% of the interface |
| Accent | 1 | the brand hue; interactive and selected |
| Status | 0–4 | danger, warning, success, info |

A `warning` ramp nothing imports is maintenance for zero pixels. A second accent
hue earns its place only when two things must be told apart at a glance, and must
never sit adjacent to the first.

**Every step has a job.** A ramp is not a gradient to pick from by eye:

| Role | Tailwind | Radix |
|---|---|---|
| Page background | `50` | `1` |
| Subtle background | `50` | `2` |
| Component background | `100` | `3` |
| Component hover | `200` | `4` |
| Component active / selected | `200` | `5` |
| Subtle border | `200` | `6` |
| Border, separator | `300` | `7` |
| Strong border, focus ring | `400` | `8` |
| Solid fill | `500` | `9` |
| Solid fill hover | `600` | `10` |
| Low-contrast text | `700` | `11` |
| High-contrast text | `900` | `12` |

**Why it holds.** The two conventions differ in kind, not just in numbering.
Radix names its twelve steps **by role**, so step 9 is "the solid fill" in every
ramp and every appearance, the dark scale reuses the numbers and component CSS
never changes. Tailwind names its eleven steps **by lightness**, so this mapping
holds in light mode and **inverts in dark**. For a new system, prefer the
role-named model: a role survives a theme flip, a lightness value does not.

**Where it doesn't.** Eleven steps cover twelve roles, so some do double duty. A
design that needs subtle-border and component-hover to be distinguishable needs
a twelve-step ramp, and squeezing it into eleven is a real loss rather than a
tidy-up.

**In code.** Neutrals carry the most roles, so **never generate fewer neutral
steps than accent steps**. A pure gray ramp is a fine default. Tinting toward the
accent is a style choice, not a correction, but hold whichever you choose across
the whole ramp: a warm border on a cool background is visible even when neither
color is nameable on its own.

---

## `ramp-construction`: Hold the Hue · high

> Even perceived steps, constant hue, vividness peaking in the middle, and
> neither end reaching pure black or white.

**Numbers.** Four properties define a well-formed ramp:

1. Steps advance evenly in **perceived** lightness, not in whatever the notation calls lightness.
2. Hue holds constant end to end.
3. Vividness peaks mid-ramp and falls away at both ends.
4. Steps sit denser at the light end than at the dark end.

**Why it holds.** Both ends stop short of pure black and white because neither
can carry hue at all, a ramp that runs to `#000` loses its identity in its last
step. The density asymmetry follows from perception being non-linear in
lightness: equal numeric steps read as bunched at the top.

**Where it doesn't.** Nothing here is eyeball-able reliably. Use a color library.
For a new system `oklch()` is the best default because its numbers behave the way
these four rules describe, but read `match-the-project` in `SKILL.md` before
introducing a second notation into a codebase that already has one.

---

## `color-naming`: Primitives Hold Values, Semantics Hold Jobs · medium

> A component never references a primitive.

**Numbers.** Two tiers. Primitives name a value: `--blue-500`. Semantics name a
job: `--color-text-secondary`. Format the second tier
`[element]/[purpose]/[state]`, `Text/Primary/Hover`.

**Why it holds.** That seam is the whole of theming. `Text/Primary` points at
`Neutral/900` in light and `Neutral/100` in dark, and nothing downstream changes.
Without the seam, dark mode means auditing every usage to work out which ones
meant "the accent" and which just wanted blue. A rebrand is one primitive edit
rather than a search-and-replace.

**Where it doesn't.** Too many semantic tokens produce decision paralysis of
their own. And naming by appearance rather than function, `DarkBlue` instead of
`Text/Primary`, fails on the first rebrand.

---

## `token-role-discipline`: Use a Token Only in Its Role · high

> Never borrow a token because its value happens to be right today.

**Why it holds.** A separator token used as a text color works exactly until
borders get lighter, and then the text goes with them, in a change nobody
connected to text. The value was never a promise; the role was.

**In code.** If a role has no token, **add the token**. That is a smaller change
than the bug you are otherwise scheduling.

---

## `one-color-one-meaning`: One Color, One Meaning · high

> Treat anything within 15° of hue as the same color, and give it one job across
> the whole interface.

**Why it holds.** If the accent means interactive, that hue on static text tells
people to click something that will not respond, and an interactive element
rendered neutral misleads exactly as much in the other direction. Both are the
same error: the color stopped predicting anything.

**Where it doesn't.** Color is never the only carrier (SC 1.4.1), so this rule
constrains the color channel, it does not license leaning on it.

---

## `fill-one-action`: Fill Exactly One Action Per View · high

> The color goes on the background, not on the label.

**Why it holds.** A filled button reads as primary from across the room. Accent
text on a neutral button reads as a link, the same pixels, a different promise.
One primary action gets the fill and its peers stay neutral, for the same reason
one isolate per group works and two cancel (`von-restorff-effect`).

**Where it doesn't.** Several colored backgrounds are fine when they encode
**distinct states or categories** rather than competing as peers. A status board
is not a page with four primary buttons.

---

## `color-scale`: Building the Ramp · medium

> Start at the middle, fix the ends, then fill in.

**Numbers.** Nine steps, 100–900. Start at **500**. Set the ends first, 900 for
text, 100 for backgrounds, then divide evenly. In use: 100–300 backgrounds,
400–600 fills and badges, 700–900 text and emphasis.

**Where it doesn't.** HSL is not perceptually uniform, so equal lightness steps
read unequal across hues and blues drift, light toward cyan, dark toward violet.
Compensate with manual hue rotation, or build in OKLCH. **Verify every step by
measurement, not by counting.**

---

## `greyscale`: Structure Before Color · medium

> If the hierarchy fails in grey, color will not rescue it.

**Numbers.** Nine steps available, **4–6 per screen**. Add 2–10% saturation to
every neutral; pure grey reads cold and lifeless, and the dark end (700–900)
needs more saturation than the light end to look equally neutral.

**Why it holds.** This is a working method, not a perceptual law `[convention]`:
finishing the layout in grey forces spacing, size and weight to carry the
structure, and color then becomes an enhancement rather than a patch over a
hierarchy that was never built.

---

## `60-30-10`: Proportion the Palette · medium

> The accent works because it is rare.

**Numbers.** 60% dominant surface, 30% secondary, 10% accent `[convention]`,
traceable to Itten, *The Art of Color* (1961), with no controlled study behind
the specific split.

**Why it holds.** At half the surface an accent carries no signal; it is just
another background. The ratio is a way of keeping the loudest color scarce enough
to still mean something.

**Where it doesn't.** Monochromatic systems vary lightness instead of hue.
Editorial and illustration work runs different proportions on purpose.

---

## `color-temperature-dominance`: Let One Temperature Win · medium

> Avoid a 50/50 warm/cool split at similar luminance.

**Numbers.** One temperature group holds roughly **60%+** of the area
`[convention]`.

**Why it holds.** Warm/cool contrast engages the same occipito-parietal regions
as binocular depth processing (Cauquil et al., *Neuropsychologia*, 2009, N=25;
Faubert, *Vision Research*, 1994) `[measured]`. At equal area and similar
luminance, neither depth plane resolves and edges visibly oscillate, Albers
documented this in *Interaction of Color* (1963) long before the imaging.
Harmony ratings track it: Lin et al. (*Frontiers in Psychology*, 2022, N=84)
found dominance above ~60% area correlating with higher ratings `[measured]`.

**Where it doesn't.** The effect is absent or inverted in roughly 10–15% of
observers (Simonet & Campbell, 1990). Poster and editorial work exploits the
conflict deliberately, visual tension is a legitimate goal, just not an
accidental one.

---

## `saturation-control`: Saturation by Role · medium

> Backgrounds calm, controls moderate, calls to action loud.

**Numbers**, HSL saturation only, OKLCH chroma is a different scale and does not
map at the same percentage:

| Range | Use |
|---|---|
| 0–25% | backgrounds, body text, layout |
| 25–60% | buttons, links, cards |
| 60–100% | CTAs, errors, warnings |

**Why it holds.** Saturation is an attention channel. Spent everywhere it encodes
nothing, and in long-session tools it accumulates as fatigue.

**Where it doesn't.** Saturation is not contrast, a vivid pair can still fail
4.5:1, and frequently does.

---

## `simultaneous-contrast`: Color Is Read Relatively · medium

> Test brand colors on the surfaces they will actually sit on, never in
> isolation.

**Why it holds.** Lateral inhibition in the retina means the visual system
computes ratios, not absolutes. The same grey reads lighter on dark and darker on
light, and neither reading is the true one. A neutral grey on red picks up a
green cast from the opponent channel. Chevreul described the effect
systematically in 1839 while running the Gobelins dye works; Albers turned it
into a teachable method in 1963.

**Where it doesn't.** The effect is strongest at the shared border and fades with
distance and across large uniform fields.

**The consequence that matters:** WCAG is computed from absolute luminance and
models none of this, so **a pair that measures 4.5:1 can still read badly**
surrounded by a competing hue. Adjust tokens per surface rather than globally.

---

## `color-constancy`: Colors Move Under Real Light · medium

> Check the palette under warm light before shipping it.

**Numbers.** Test at **6500K** (daylight, D65), **2700K** (warm incandescent) and
in a dim room. Warm light is the stress case for cool palettes.

**Why it holds.** The visual system discounts the illuminant, but only partly,
strong or spectrally extreme sources drag perceived color toward the light's own
hue. Wide-gamut and OLED displays reproduce colors that never existed under
natural illumination, which is outside the range the mechanism was calibrated on.
People with color vision deficiencies have less cone redundancy to work with, so
their perception moves further under non-daylight sources.

**In code.** Any token that loses its identity at 2700K needs either more
saturation or a luminance-based fallback. f.lux or a warm bulb is sufficient
apparatus.

---

## `color-psychology`: Associations Are Conventions · medium

> Treat color meaning as a Western market convention you are choosing to use, not
> a constant you can rely on.

**Numbers.** Red urgency, blue trust, green confirmation, amber warning, black
and white for restraint. **Never run all four signal colors on one page.** With
four signals, none of them signals.

**Why it holds: and how far.** Elliot et al. (2007, n=71) found red triggering
avoidance motivation and measurably impairing performance in achievement contexts
`[measured]`. That is one effect in one context, not a general theory of color
and emotion. Blue's dominance in finance and tech is an observed industry pattern
`[convention]`, not a measured psychological constant, and repeating it as one is
how this topic earned its reputation.

**Where it doesn't.** Cultural variation is large and not decorative: white
signals mourning across much of Asia, purple in parts of Latin America, green
carries religious weight in Islamic contexts. Validate outside Western markets
rather than porting the table. Separately, yellow's luminance is so high (Y ≈
0.93) that it collapses against white regardless of what it is supposed to mean.

---

## `gradient-interpolation`: Choose the Interpolation Space · medium

> The space is a look, not a correctness setting.

| Space | Behavior |
|---|---|
| `in oklab` | best default, even brightness, no hue surprises |
| `in oklch` | travels **around** the hue wheel rather than through it; stays vivid and sweeps intermediate hues. Use when a two-hue gradient greys out in the middle |
| sRGB (default) | darkens and mutes the midpoint. What most interfaces already have, because it is what you get without asking |

---

## `rgb-vs-cmyk`: Emitted and Reflected Are Different Gamuts · medium

> CMYK without a named profile is undefined.

**Numbers.** sRGB exceeds FOGRA39 across most of the diagram; the widest gaps are
saturated greens, blues and violets. Proof-to-print tolerance is **ΔE00 ≤ 3.0**
(ISO 12647-2:2013) `[spec]`.

**Why it holds.** Displays run 80–500 cd/m²; print reflects roughly 60–100 cd/m²
under ISO 3664 viewing conditions. That gap raises apparent brightness and
contrast on screen in a way print cannot match (the Stevens effect; Fairchild,
*Color Appearance Models*, 3rd ed., 2013) `[measured]`, and no adaptation closes
it. Display-P3 covers roughly 25% more volume than sRGB, so vivid P3 color can
sit entirely outside CMYK.

**In code.** Screen: sRGB IEC61966-2-1, embedded. Coated offset: ISO Coated v2
300% (FOGRA39); optically brightened stock: PSO Coated v3 (FOGRA51). Export
PDF/X-4 with the profile embedded. Text under 12pt goes K-only (0/0/0/100) to
dodge registration error.

**WCAG ratios are defined on sRGB luminance and do not transfer to print.**
