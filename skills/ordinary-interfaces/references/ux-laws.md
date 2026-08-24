# Cognition & Behaviour

19 rules. These are the most quoted and worst quoted findings in design. The
evidence grade matters more here than anywhere else in the skill, and several
widely repeated figures are marked below as unsupported rather than dropped,
knowing a number is fake is more useful than never having heard it.

---

## `jakobs-law`: Convention Is Accumulated Learning · high

> People spend nearly all their time in other products. Yours is judged against
> the habits those built.

**Why it holds.** Familiar patterns cost nothing to learn, which leaves the
user's attention on their task instead of on your navigation. A design that is
10% better can still lose, because the learning cost is paid up front and the
benefit accrues later.

**Where it doesn't.** Deviate when the improvement is substantial and the
replacement pattern is itself tested. Platform conventions (Apple HIG, Material)
outrank general web habit on their own platforms.

---

## `millers-law`: Working Memory Is Small, and Chunks Are the Unit · high

> Structure beats count. Ten organised items beat five chaotic ones.

**Numbers.** Miller's **7±2** (1956) is the famous figure; Cowan's **~4** (2001)
is the modern estimate `[measured]`. Unrehearsed content decays in **20–30
seconds** (Peterson & Peterson, 1959).

**The misreading to refuse.** "Navigation must have exactly seven items" is not
what the paper says, and Miller himself called the number coincidental. There is
no hard limit, what counts as one chunk depends entirely on expertise. `FBI` is
one chunk to an agent and three letters to everyone else; `(555) 123-4567` is
three chunks where `5551234567` is ten.

---

## `chunking`: Group Before You Place · high

> Three to five per group, and a gap between groups at least 1.5× the gap within.

**Numbers.** **3–5 items** per chunk `[convention]`; between-group gap
**1.5–2×** the within-group gap `[convention]`.

**Why it holds.** Perceived complexity tracks the number of *chunks*, not the
number of items, so grouping reduces apparent load without removing anything.
Proximity does the grouping pre-attentively (Wertheimer, 1923), before any border
or label confirms it, which is why whitespace alone is sufficient to create a
boundary.

**Where it doesn't.** **Chunking is not collapsing.** Hiding items behind an
accordion adds navigation cost and organises nothing. If the grouping logic is
not evident on sight, the boundaries are pure overhead. And chunking reorganises
volume without reducing it. For genuine overload it helps but does not solve.

**In code.** Checkout as Personal / Shipping / Payment. Note that alphabetical
ordering is *sorting*, not chunking: it produces no meaningful group.

---

## `hicks-law`: Choice Cost Is Logarithmic · high

> Doubling the options adds a constant, not a doubling.

**Numbers.** `RT = a + b·log₂(n)` `[measured]`. Two to four costs what four to
eight costs.

**Where it doesn't.** The law assumes options are equiprobable and the user does
not yet know their target. Alphabetical lists and familiar choices break both
assumptions, which is why it governs navigation and action bars and says almost
nothing about a contacts list.

---

## `subitizing`: Four Is Instant; Five Is Counting · medium

> Keep anything meant to be grasped at a glance at four or fewer.

**Numbers.** **1–4** items register instantly and accurately, under 250ms. Past
four, each additional item costs roughly **250–350ms** and accuracy drops
(Kaufman et al., 1949; Mandler & Shebo, 1982; Trick & Pylyshyn, 1993)
`[measured]`. Visualization work finds task accuracy declining once categories
reach **six** (VIS, 2025) `[measured]`.

**Why it holds.** Within the subitizing range all items are processed in
parallel, with no attentional shift between them. Beyond it the system switches
to serial counting, which is a different and slower operation.

**In code.** Top-level navigation at four or fewer registers; five works; six
forces scanning. Badge counts exact to 9, then `9+`. Chart legends past five slow
comprehension, group the tail.

**Where it doesn't.** Regular arrangements (dice patterns, grids) extend the
range slightly. Domain expertise extends it further. It applies to discrete
countable items, not to continuous quantities like bar length.

---

## `von-restorff-effect`: One Isolate Per Group · high

> A second highlight cancels the first.

**Why it holds.** Distinctiveness is relational, not absolute, an element is
isolated only against its immediate neighbours. Each additional outlier shifts
the group average, and the advantage collapses (Von Restorff, 1933; Hunt, 1995)
`[measured]`. The benefit operates at **encoding**: the isolated item is
processed more deeply on first sight, not retrieved better later.

**In code.** Prefer **one** differentiating channel, color, size, shape, or
motion, with others reinforcing rather than competing. Pricing tables: the
recommended tier gets a filled card and every other stays outlined. Three
highlighted tiers means none is highlighted.

**Where it doesn't.** Color alone fails for ~8% of men, so isolation by color
always carries a second channel. And memorability is not action, an isolated
element still needs a clear affordance and label.

---

## `banner-blindness`: Ad-Shaped Things Are Not Seen · high

> The shape and position get filtered, not the content.

**Why it holds.** Years of exposure train an involuntary suppression of ad-like
regions, top horizontal bars and right-hand columns are systematically skipped
in eye-tracking `[measured]`, and users cannot easily override it consciously
even when told to.

**Where it doesn't: and this matters.** The foundational studies (Benway & Lane,
1998; NN/g, 2010) ran on visually simple, text-heavy pages. On modern image-dense
interfaces the ad/content boundary is far blurrier. **The effect is well
established; its current magnitude is not precisely quantified.** Empty pages and
first sessions both show weaker blindness.

**In code.** Put cookie consent, outage notices and anything else critical into
flowing UI rather than a banner rectangle in the top-left or top-right.

---

## `inattentional-blindness`: Visible Is Not Seen · high

> Salience is necessary and not sufficient. Match the alert to the task's
> features.

**Numbers.** **46–56%** of observers miss a fully visible object while occupied
with a demanding task `[measured]`. Feature-matching the unexpected object to the
primary task raises detection odds about **5×** (odds ratio 5.02; Bredemeier &
Simons, *Psychological Bulletin*, 2022) `[measured]`.

**Three findings that overturn the intuitive account:**

- **It is situational, not a trait.** Cognitive ability and personality do not predict who misses things (Simons, Hults & Ding, 2024; 74 samples, 38 studies) `[measured]`.
- **Expertise does not protect.** Expert-versus-novice odds ratio 1.33, not significant (Ekelund et al., 2022; 14 studies, N=1,153). Radiologists missed a gorilla 48× the size of the target nodule in **83%** of cases, most having fixated its location (Drew et al., 2013) `[measured]`.
- **Salience alone is not enough.** ~30% missed a bright red cross that was the only colored thing on screen (Most et al., 2001).

**The honest limit.** The evidence base is basketball videos and CT scans. **No
peer-reviewed study has measured this for specific UI layouts under real task
conditions.** Do not quote a UI-specific figure.

**In code.** If active fields carry a blue border, inline validation at the field
beats a red toast in the corner. That is feature-matching in practice. For
connection loss or session timeout, place the alert inline and add
`role="alert" aria-live="assertive"`.

---

## `default-effect`: Preselection Persists · medium

> Defaults are a design decision with a legal boundary.

**Numbers, both of them.** The headline meta-analysis reports **d = 0.68**, 95%
CI [0.53–0.83] (Jachimowicz et al., 2019; k=58, N=73,675) `[measured]`. Corrected
for publication bias, Mertens et al. (*PNAS*, 2022; N=2,148,439) estimate the
true effect at **d = 0.08–0.31** `[measured]`. **Quote both, or neither.**

**The number to refuse.** "85% of users keep the default" has **no primary
source**. It is not a benchmark.

**Why it holds.** Three additive mechanisms: the physical effort of opting out,
the cognitive effort where no preference exists, and **implied endorsement**,
the user reads the default as a recommendation (Dinner et al., 2011). The
strongest field evidence is organ donation: opt-out countries run **≥60
percentage points** higher, controlling for infrastructure and education (Johnson
& Goldstein, *Science*, 2003) `[measured]`.

**The legal boundary, not optional.** Pre-checked consent for cookies, data
sharing or marketing is **void under GDPR Recital 32**, confirmed by CJEU
*Planet49* (C-673/17, 2019) `[spec]`. The element is visually identical to a
legitimate nudge, legality turns on context, not appearance. **Every consent
checkbox ships unchecked.**

**Where it doesn't.** ~15% of studies found null or reverse effects, concentrated
in high-involvement decisions with strong prior preferences. Reactance is real:
once a default is read as serving the provider, it can invert.

**In code.** Notifications default off. Set a data-driven default only from
actual usage (N≥100 minimum), and record the source and date in the design
system.

---

## `decoy-effect`: Asymmetric Dominance Shifts Choice · medium

> A third option that is clearly worse than the target makes the target win the
> comparison.

**Numbers.** Introducing a dominated alternative raises the dominating option's
share by **10–15%** on average (Huber, Payne & Puto, 1982) `[measured]`.

**Why it holds.** Preferences are constructed at decision time rather than
retrieved from stable internal values (Ariely, Loewenstein & Prelec, 2003)
`[measured]`, which is exactly what makes them sensitive to the comparison set.

**Where it doesn't: including the ethical edge.** Experienced buyers and B2B
procurement with formal criteria are resistant. With no asymmetric dominance
there is no direction. And **if the decoy is too obvious, half the features at
90% of the price, people recognise the manipulation and trust the interface
less.** The mechanism works by being invisible, which is worth being uneasy
about.

---

## `peak-end-rule`: Memory Keeps the Peak and the Ending · medium

> Design those two moments. The average is not remembered.

**Why it holds.** Kahneman, Fredrickson, Schreiber & Redelmeier (1993) established
it on cold-water pain; Redelmeier & Kahneman (1996) showed colonoscopy patients
remembering a **longer** procedure as less painful when discomfort tapered at the
end `[measured]`. Duration is largely neglected in retrospective judgement, the
experiencing self and the remembering self are separable, and design reaches them
differently.

**Where it doesn't.** Repeated routine tasks average out across accurate memory.
Committee and checklist evaluation overrides emotional recall. Interactions under
about ten seconds may not establish a peak distinct from the end.

**In code.** Make the onboarding "aha" an explicit peak, and **end on a positive
summary. Never on a form or an error**.

---

## `picture-superiority`: Distinctiveness, Not Imagery · medium

> An image beats a word when the image is distinctive and relevant. Otherwise it
> does not.

**Numbers.** Shepard (1967): forced-choice recognition ~**98%** pictures, ~**90%**
words, ~**88%** sentences `[measured]`, one small study, orientation only.
Standing (1973): **73–83%** accuracy after ~2 days across up to 10,000 photos
`[measured]`.

**Two things to stop repeating.**

- **"People remember 10% after three days, 65% with an image."** Traces to Medina's *Brain Rules*, with no peer-reviewed method or sample. It is a marketing statistic.
- **Imagery is not automatically helpful.** Mayer's coherence principle describes the reverse failure: an interesting but irrelevant image does not transfer its memorability, and Rey's meta-analysis (2012) found a small-to-medium **negative** effect on retention and transfer `[measured]`.

**The mechanism is contested.** Paivio's dual-coding is the classic account;
recent work argues **distinctiveness** does the work, since the advantage shrinks
when words are made equally distinctive (Higdon et al., 2025).

**In code.** Icon **plus** label beats either alone. In onboarding, one concrete
illustration tied to that step's content, not a generic graphic. In dense
text-native contexts (legal, technical), illustrative images show no measured
recall benefit and cost information density.

---

## `stroop-effect`: Keep Color and Meaning Congruent · medium

> Success is green, error is red, warning is amber. Do not recolor them for the
> palette.

**Numbers.** MacLeod (1991) reviewed **700+** studies; the interference is among
the most reliably replicated effects in experimental psychology `[measured]`.

**Why it holds.** Reading is over-learned and hard to suppress, so word meaning
interferes with color naming far more than the reverse, the interference is
**asymmetric** and specifically **semantic**, appearing with real color words and
not with matched letter strings.

**The honest caveat.** Stroop measured single color words in a naming task, not
interfaces. **Applying it to status badges is a reasonable extension, not a
tested UI result** `[convention]`. Bilingual and lower-fluency readers show
weaker interference in their less dominant language; red-green deficiencies can
remove it entirely.

---

## `reward-anticipation`: Anticipation, With an Ethical Boundary · medium

> Uncertainty before an outcome drives engagement. That is a reason to be careful
> with it, not a licence to use it.

**Why it holds.** Schultz, Dayan & Montague (1997) recorded midbrain dopamine
neurons firing to a **cue predicting** reward rather than to its delivery, with
the signal largest when the outcome is uncertain `[measured]`. Separately,
Skinner and Ferster's variable-ratio work (1950s) showed unpredictable
reinforcement producing steadier, more extinction-resistant responding
`[measured]`.

**These are two research programmes.** Pigeons and rats decades apart from
primate neurons, routinely merged into one narrative in design writing.
**Neither measured a consumer app, a notification badge, or any UI pattern.**
"Gives users a dopamine hit" misstates the finding.

**The rules that follow.** Predictable, fixed delivery is correct for anything
transactional, checkout, submit, save. Use a variable reveal only where it
reflects real processing or the user controls repetition. **Any variable reward
must leave the user able to stop without penalty.**

**The boundary.** Engineered unpredictability that extends session time or
spending without user benefit sits inside Brignull's deceptive-pattern definition
(2010). Belgium's Gaming Commission ruled (April 2018) that paid randomised
rewards can constitute unlicensed gambling `[spec]`, that covers *monetised*
randomisation specifically.

---

## `ebbinghaus-illusion`: Size Is Judged Against Neighbours · medium

> Keep sibling elements the same size when their size means something.

**Why it holds.** A circle among larger circles reads smaller than an identical
circle among smaller ones. Magnitude varies with the ratio, count, spacing and
arrangement, and **there is no fixed percentage distortion** `[convention]`.
Aglioti, DeSouza & Goodale (1995) reported reduced effects on grip aperture
versus conscious judgement, evidence for partly separable perception and action
pathways `[measured]`, an interpretation later work has contested on both
strength and framing.

**In code.** Keep avatar and icon sizes consistent within a list. In bubble
charts, avoid placing comparison targets among strongly different-sized
neighbours, or add numeric labels.

---

## `optical-center`: The Visual Centre Sits High · medium

> `align-items: center` reads as sagging.

**Numbers.** The optical centre sits roughly **44–47% from the top.** A **2–6%**
upward offset `[convention]`, from print framing rather than screen research.

**Why it holds.** The visual system overestimates vertical extent in the upper
field (the horizontal-vertical illusion; Stacey, 1969). Locher, Stappers &
Overbeeke (1999) found lay observers at 55% and professionals at 64% detecting
compositional correctness above chance `[measured]`, perceptual, not learned.

**Where it doesn't.** Single focal elements only. High-salience content, a face,
strong contrast, motion, captures first fixation regardless of position. The 44%
figure is print-derived and no controlled study has checked it on mobile
portrait.

**In code.** `transform: translateY(-4%)` on a hero. Percentage *margins*
reference container **width**, not height, so they are unreliable for vertical
offsets.

---

## `center-bias`: First Fixation Lands High of Centre · medium

> Put the primary call to action at 45–48% of height, not 50%.

**Numbers.** First fixation lands around **50–60% of width and 40% of height**,
roughly **10% above** the geometric midpoint `[measured]`.

**Why it holds.** Tatler (2007) found the central bias persisting regardless of
image content, pointing to the screen centre as a convenient oculomotor starting
position rather than a foveal advantage `[measured]`.

**Where it doesn't.** Text-dense interfaces shift toward F-pattern scanning and
the bias weakens. On mobile it strengthens, the visual field being narrower.

---

## `muller-lyer-illusion`: Cap Direction Biases Perceived Length · low

> Keep arrow and chevron caps consistent across elements meant to compare.

**Why it holds: and how weakly.** Outward fins read longer than inward fins at
equal length (Müller-Lyer, 1889), and the distortion survives measurement.
Magnitude varies substantially with fin angle, length, method and culture, with **no
agreed percentage** `[convention]`. The mechanism is unsettled: Gregory's (1963)
depth-cue account competes with an endpoint-displacement account. Segall,
Campbell & Herskovits (1966) found substantially weaker effects in less
"carpentered" societies `[measured]`, implying a learned component.

**Applying it to progress bars and connectors is an extrapolation, not a
validated interface finding.** Where line length must communicate a quantity, add
a numeric label rather than trusting the geometry.

---

## `irradiation-illusion`: Light on Dark Reads Larger · low

> Reversed type and icons may need marginally less weight. Judge it visually.

**Why it holds.** Noted by Galileo (1632), named by Helmholtz. Modern support is
better than the old light-scatter account: ON (light-detecting) receptive fields
are larger than OFF fields from retina through cortex.

**The number to refuse.** **No modern study establishes an agreed percentage.**
Treat any specific figure for this illusion as unverified. Long & Murtagh (1984)
found the effect under forced-choice comparison but **not** under absolute size
estimation. It is task-dependent, not a fixed distortion.

**In code.** Some foundries reduce the size or stroke of reversed glyphs
slightly. There is no documented industry percentage; use your eyes.

---

## `bouba-kiki-effect`: Curvature Carries Tone · low

> Round reads approachable, angular reads precise, until color and weight say
> otherwise.

**Numbers.** ~**95%** of Western-educated participants match "bouba" to round and
"kiki" to angular (Ramachandran & Hubbard, 2001) `[measured]`. **Cross-cultural
replications show lower rates**, consistent in direction, variable in magnitude.
Maurer et al. (2006) found it in children as young as 2.5 `[measured]`,
suggesting early perceptual grounding rather than pure cultural learning.

**Where it doesn't.** Applying it to corner radius, logos and icons is a design
extension, **not an empirically tested use**, and no source establishes a radius
threshold for "rounded". Color, texture and weight routinely override it, a
rounded mark in black with sharp heavy type reads aggressive despite the curves.
