# Hierarchy & Emphasis

8 rules on directing attention within a screen. `optical-center` and
`center-bias` moved to `ux-laws.md`, where the perceptual findings live.

---

## `emphasis`: Emphasis Is Relative · high

> One primary focal point per functional layout. Everything else supports it.

**Numbers.** One primary, at most two secondary, the rest subordinate. **One
filled button per view** is a reliable default `[convention]`, not a law.

**Why it holds.** Size, color and luminance contrast are detected
pre-attentively, in roughly **50–250ms**, before conscious attention engages,
emphasis borrows that channel to place the eye before the user decides anything.
When everything carries equal weight the system falls back to serial search:
Treisman & Gelade (1980) measured conjunction search at about **60ms per item**
`[measured]`, which is the cost of a screen with no focal point.

**In code.** Contrast can come from size, weight, color, position, whitespace,
shape or texture. They interact non-linearly, aligning several strengthens a
focal point, but they do not simply add.

**Where it doesn't.** Editorial and poster work uses ambiguous hierarchy for
tension deliberately. And over-emphasis is its own failure: several competing
"urgent" elements desensitise the reader until the signal is noise, which is the
point where emphasis becomes a dark pattern.

---

## `visual-weight`: Six Channels, Honestly Labelled · high

> Size, saturation, luminance contrast, position, isolation, shape.

**Why it holds: and how firmly.** This is Arnheim's framework (1954): an
influential theory, **not a set of measured constants** `[convention]`. Aligning
several channels in one direction strengthens a focal point; a CTA that is large,
saturated, high-contrast, isolated and compact is unambiguous because nothing
contradicts anything.

**Three caveats worth carrying, because they are usually dropped:**

- **Winner et al. (1987) found no empirical support** for Arnheim's claim that elements on the right appear heavier. Do not state right-is-heavier as fact.
- Helmholtz-Kohlrausch means saturated blues and magentas look brighter than their luminance, pure luminance math under-predicts them.
- Left-right weight distribution varies with reading direction, so it is not a universal.

**Post-attentive weight is a separate channel.** A face attracts the eye
regardless of pixel size, which overrides everything above.

Eye-tracking (MDPI *Symmetry*, 2026, n=30, 120Hz) found a yellow background
producing the fastest initial fixation (0.65s) against black's slowest (1.75s), a
~2.7× spread `[measured]`, n=30, directional only.

---

## `hierarchy-channels`: Separate Levels on More Than One Channel · high

> Combine size, weight and letter-spacing. Never rely on size alone.

| Role | Treatment |
|---|---|
| Headlines | weight plus tight tracking, for presence |
| Body | comfortable weight, for reading |
| Labels | medium weight that still works small |
| Data | monospace with tabular numerals |

**Why it holds.** Two levels separated on one channel are one adjustment away
from collapsing into each other, a user zoom, a font fallback, a dense
breakpoint. Two channels degrade gracefully.

Quantified thresholds live in `typography.md`: `type-hierarchy` (1.25 scale) and
`font-weight-contrast` (≥200 units).

---

## `rule-of-thirds`: A Heuristic With Weak Evidence · medium

> Try it, then try centred, then decide. It is not a law and it has no normative
> backing.

**Numbers.** Grid lines at **33.33%** and **66.67%**, four intersections. Related
to but distinct from the golden ratio (33.3% versus 38.2%).

**The honest evidence.** Amirshahi et al. (2014) found only a **weak** correlation
between rule-of-thirds score and aesthetic quality `[measured]`. A low score often
does correlate with a weaker composition; a high score guarantees nothing.

**Where it actively loses: these findings are stronger than the rule itself:**

- **Single isolated objects:** Hoh et al. (SIGGRAPH Asia, 2023) found users overwhelmingly preferring **centred** placement `[measured]`.
- **Vertical video (9:16):** eye-tracking favours central vertical placement.
- **Data UIs:** readability and alignment win outright; the rule does not apply.
- **Symmetrical subjects.** Logos, frontal portraits, product shots, are usually stronger centred.

---

## `golden-ratio`: A Proportioning Start, Not a Guarantee · low

> 61.8 / 38.2 is a reasonable place to begin a two-column split. That is the
> whole claim.

**Numbers.** φ = 1.618. Two-column split 61.8% / 38.2%. Type scale ×1.618 per
step: 16px → 26px.

**The evidence, stated accurately.** De Bartolo (2022, *PsyCh Journal*) found a
statistically significant but **modest** preference, 53%, p < 0.001, holding
for humanoid and organic stimuli and **not** for abstract geometric figures
`[measured]`. UI rectangles are abstract geometric figures.

**Where it doesn't.** Grids need integer columns and φ produces irrationals that
round inconsistently across breakpoints. Accessibility outranks it, a layout
passing WCAG at non-φ proportions beats a φ layout that fails. Attributing
conversion or usability gains to φ without testing is unsupported.

---

## `rule-of-odds`: Odd Groups Resolve Faster · low

> Three is the smallest group that establishes a hierarchy.

**Why it holds.** An odd group resists pairing, so the eye finds a centre flanked
by subordinates; an even group splits into pairs with no natural focus. This is a
practitioner observation grounded in Gestalt `[convention]`, not a controlled
perception experiment.

**Where it doesn't.** Comparative layouts, pricing tables, feature comparisons,
map naturally to even columns. Navigation counts are governed by memory load, not
aesthetics: five tabs beat six for `subitizing` reasons, not this one. The rule
describes **groupings**, not total element count.

---

## `corner-radius-tone`: Radius Carries Tone, Consistency Carries More · low

| Radius | Reads as |
|---|---|
| 0–2px | formal, technical, authoritative |
| 4–8px | neutral, professional |
| 12–24px | friendly, approachable |
| 32px+ / pill | energetic, playful |

`[convention]`. No empirical source for these bands. Supported directionally by
Bouba-Kiki (Köhler, 1947; Ramachandran & Hubbard, 2001) and by Bar & Neta (2006),
who found consistent preference for curved over angular objects.

**Consistency within a tier matters more than the value chosen.** Mixing very
rounded cards with square buttons reads as incoherence, not as contrast.

**In code.** Token by tier, `--radius-sm: 4px; --radius-md: 12px; --radius-lg:
20px; --radius-pill: 9999px`. **Cap radius at 50% of the shortest dimension**: a
24px radius on a 28px chip is a pill whatever you intended. Audit every
interactive element for consistency before shipping.

**Where it doesn't.** Other properties override the tone signal, a black pill
button in heavy condensed type reads assertive despite the curves. Dense data UIs
gain density from reduced radius at negligible brand cost. And nesting has its
own arithmetic: see `surfaces.md → concentric-radius`.

---

## `pie-chart-problem`: Encode on the Accurate Channels · medium

> Angle and arc are near the bottom of the perceptual accuracy ranking. Use a bar
> chart on a shared baseline.

**The ranking**, most to least accurate (Cleveland & McGill, *JASA*, 1984)
`[measured]`:

> position on a common scale → length → angle → area → color saturation

**The one case pies work:** showing that a single category is a clear majority,
with five or fewer slices. **Donut charts do not fix this.** Removing the centre
reduces area cues without improving angle judgement.

**Where the criticism over-reaches.** Very different magnitudes read fine without
comparison accuracy. For rapid approximate estimation where only one or two
slices matter, a pie can be faster. And the bar advantage rests on the **shared
baseline**, stacked or unaligned bars perform comparably to pies in the same
study.

**In code.** A six-slice pie becomes a horizontal bar chart sorted by value, with
labels on the bars and the legend removed.

---

## `handmade-vs-polished`: Register Is a Choice, Not a Quality Level · medium

> Neither is better. Context decides which one earns trust.

**Why it holds.** Polish signals precision and institutional credibility;
irregularity signals human involvement and therefore individual care. NN/g (2024)
report handmade aesthetics increasingly functioning as a trust signal, as high
polish reads as potentially AI-generated or corporate `[measured]`.

**The condition that decides it.** **The distinction must be intentional.**
Accidental imperfection reads as incompetence; deliberate imperfection reads as
character, and making imperfection look intentional takes more craft, not less.

**Where it doesn't.** Finance, healthcare and legal audiences expect precision,
and handmade reads as unreliable there. **Accessibility is never traded for
texture:** irregular typography and low-contrast grain routinely fail contrast.
