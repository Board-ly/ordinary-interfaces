# Beyond the Screen: Appendix

9 rules outside this skill's UI focus, kept for reference: brand assets,
photography, physical scale and print production. Nothing in the UI reference
files depends on them.

---

## `viewing-distance`: Distance Sets Everything Else · high

> The distance a medium is read from determines its type size, contrast and
> detail density.

| Medium | Distance | Consequence |
|---|---|---|
| Mobile, handheld print | **25–40cm** | fine detail works at small absolute sizes |
| Desktop monitor | **50–70cm** | body copy can run smaller than print |
| Posters, retail signage | **1–5m** | scale by letter height |
| TV / 10-foot UI | **~3m** | large sizes, heavier weights, low density |
| Billboard | tens to hundreds of m | ~1.25m letters at 150m, minimal detail |

**The signage rule of thumb: ~1 inch (2.5cm) of cap height per 10 feet (3m)**,
US Sign Council-derived `[convention]`. A poster read at 3m wants ~2.5cm letters.

**Where it doesn't.** A fixed-distance assumption ignores low vision, which is
why tvOS and Android TV both ship separate accessibility text sizes. Mobile
distance is not fixed: people zoom, lean in, or mount the device on a dashboard.
Glare and dusk shrink the effective legible distance below the geometric
prediction. And vehicle speed changes how long a viewer actually has, so a
billboard sized only by the static rule can still fail on a highway.

**For responsive products:** do not reuse one absolute point size across
breakpoints. Text that reads at 25–35cm needs to be physically larger to hold the
same perceived scale at 50–70cm.

---

## `visual-angle-arcminutes`: The Eye Measures Angle · high

> Perceived size is physical size divided by viewing distance. Size on the page
> means nothing without a stated distance.

```
arcminutes = 3438 × (object height / viewing distance)     [same units]
```

3438 = 180 × 60 / π, the radians-to-arcminutes constant.

**Numbers.** **1 arcminute** is the acuity limit defining 20/20 (Snellen, 1862)
`[spec]`, each optotype stroke subtends exactly 1′. Below that, detail is an
undifferentiated blur. Reading a *letterform* needs its strokes and gaps
individually resolvable, so the whole letter spans about **5 arcminutes**.

**Visual angle scales with 1/distance.** Doubling the distance requires doubling
the size, not adding a fixed amount.

**Worked.** A sign letter legible at 3m needs a stroke of at least
(1 × 3000) / 3438 ≈ **0.87mm**. Logo recognition heuristic, smallest detail
subtending ≥ ~5′ `[convention]`, at 5m gives (5 × 5000) / 3438 ≈ **7.3mm**.

**Where it doesn't.** 1′ is a *text legibility* limit, not a recognition limit
for complex shapes; logos need several times that. Contrast and shape complexity
matter as much as angular size, a high-contrast monoline mark survives smaller
than a low-contrast one with fine internal detail. Low vision, age-related
contrast sensitivity, glare, motion and oblique viewing all push the threshold
above 1′.

**Before shrinking a logo for a favicon, state the viewing distance first**, then
check whether the smallest detail still clears ~5′. If not, simplify the mark
rather than assuming the pixel size is big enough.

---

## `aspect-ratios`: Ratio Belongs to Context · medium

| Ratio | Pixels | Context |
|---|---|---|
| **16:9** | 1920×1080 | TV, desktop video, YouTube, presentations |
| **4:5** | 1080×1350 | Instagram feed post |
| **3:4** | 1080×1440 | Instagram profile grid and carousels (since Jan 2025) |
| **9:16** | 1080×1920 | fullscreen vertical, TikTok, Reels, Stories |
| **1:1** | 1080×1080 | profile images, thumbnails |
| **3:2** | n/a | photography, APS-C and full-frame; Micro Four Thirds is 4:3 |

16:9 in a vertical mobile feed loses roughly **30–40%** of visible screen height
against 4:5 `[convention]`, platform convention, not a measured constant.

**For 9:16, keep key content in the centre 50–60% of frame height.** The top
~15% and bottom ~25% sit under platform UI.

**Where it doesn't.** Intentional cinematic framing (2.39:1, 4:3). On responsive
web the source ratio matters less than the crop region and focal point
(`object-fit: cover`).

---

## `logo-clearspace`: A Protected Zone, Defined as a Ratio · medium

> Minimum 1× on all four sides, expressed as a ratio so it scales with the mark.

**Define 1× from a logo element.** Cap-height or x-height for wordmarks (the
former for large format, the latter for small or text-adjacent), symbol height
for combination marks.

**Why it holds.** Gestalt proximity: anything inside the clearspace reads as part
of the logo, which dilutes the mark. Never a fixed pixel or millimetre value,
that breaks at the first size change.

**Where it doesn't.** Intentional lockups (tagline, co-brand) form one unit with
its own outer boundary. Favicons and app icons are bounded by the platform
container. On photographic backgrounds clearspace cannot be guaranteed. Use a
solid backing field with 0.5× internal padding and keep 1× from the field's outer
edge.

1× is the mathematical minimum; rounded shapes and diagonals often need more on
specific sides. **Test the unit at minimum size, maximum size, and one edge case**
before finalising.

---

## `logo-variations`: Six Types, Three Lockups · medium

**Types:** wordmark (full name), lettermark (initials), pictorial mark
(recognisable subject), abstract mark (geometric, no inherent meaning), emblem
(text inside a containing shape), and combination mark (symbol plus wordmark).

**Lockups** `[convention]`: primary (combination), secondary (wordmark or mark),
minimum (symbol or lettermark).

- **Default to the combination mark**, switching to the mark alone at sizes where the wordmark stops being legible, `visual-angle-arcminutes` gives that threshold numerically.
- **Emblems need a dedicated simplified variant**; their text and shape are inseparable by construction.
- Abstract marks need longer wordmark pairing than pictorial ones before standing alone, carrying no inherent meaning until exposure supplies it.

**Application:** app icon → symbol only · favicon → symbol or lettermark · page
header → combination · social avatar → symbol.

---

## `joint-cropping`: Do Not Cut at a Joint · low

> Crop through the middle of a limb segment, roughly **10% of its length** from
> the nearest joint `[convention]`.

Neck, shoulder, elbow, wrist, hip, knee, ankle. A cut at the joint reads as an
unnaturally truncated limb; a cut mid-segment reads as intentional, consistent
with Gestalt closure. This is documented in portrait and editorial instruction
(Valenzuela, *Picture Perfect Practice*), **not derived from a vision-science
experiment**, the 10% figure is a practitioner heuristic with no controlled
study behind it.

**The safe zone scales with framing.** A close crop of a hand has a far smaller
absolute margin than a full-body shot.

**Where it doesn't.** Extreme close-ups no longer imply a whole figure.
Deliberate fragmentation in fashion editorial crops at joints on purpose.
Occlusion by another person in a group shot reads as depth, not amputation.

**In code.** For automatic aspect-ratio cropping (`object-fit: cover` with a
fixed focal point), set the focal point manually (or supply a manual crop) when
the source has visible limbs near the frame edge.

---

## `dieline-bleed`: Errors Become Physical · high

> A dieline is a vector 2D document defining every cut, crease, perforation and
> glue line in the **flat unfolded** state. Not a mockup, not a render.

**Numbers.**

| Value | |
|---|---|
| **3mm** | EU bleed `[spec]` |
| **3.175mm / 0.125in** | US bleed `[spec]` |
| 3–5mm | safe-zone inset from the cut line, 5mm at creases |
| 300 dpi | minimum raster resolution at 1:1 |
| 0.25pt | minimum stroke, thinner drops out in production |

**Why bleed exists.** Press drift displaces the substrate during printing;
without bleed, any drift exposes unprinted stock after trimming as a white edge.
It is the most frequently reported packaging prepress error.

**Construction layers.** Every construction line goes on a **named spot-color
layer with the overprint flag active**. Without both, the RIP treats them as
printable and they appear as visible marks on the finished product.

**Caliper correction is mandatory for rigid board:** add **twice the material
thickness** to each fold dimension. A 2mm greyboard lid needs **+4mm**. **Online
templates do not include this.**

**Why fold errors persist even among experienced designers:** the dieline demands
continuous 2D↔3D mental rotation, and Shepard & Metzler (1971) established that
mental rotation time scales linearly with structural complexity `[measured]`.

**Cost.** Standard folding-carton dies run roughly **300–2000 EUR** by region and
complexity, verify with the supplier before quoting.

**Where it doesn't.** Unprinted or flexo-printed corrugated transport packaging
(FEFCO codes) operates at lower graphic precision. Short-run digital has no
reusable die, so per-unit correction is cheaper, but **there is no tooling
proof**, meaning no physical verification exists before the full run completes.

---

## `cmyk-vs-pantone`: Spec Both, Always · high

> A PMS-only spec on a 4-color press forces an uncontrolled conversion.

**Why it holds.** CMYK prints four inks as halftone dots the eye mixes optically,
with variance entering at every step, substrate, ink density, dot gain. PMS is a
**pre-mixed** spot ink: one pigment formula, one ink, and the color results from
molecular absorption rather than from mixing on the substrate, so it holds across
press runs.

**CMYK→PMS is not reversible.** Specifying CMYK and asking the printer to "match
the Pantone" is not a valid workflow.

**Cost.** Each spot ink needs a dedicated press station. **1–2 spot colors before
switching to 4-color** is the common threshold `[convention]`.

**Where it doesn't.** Digital print (inkjet, laser, toner) **cannot use spot
inks**: Pantone XGC approximates and does not match. **Coated (C) and uncoated
(U) are different formulations**; always specify the suffix. Metallic and
fluorescent PMS sit entirely outside CMYK, if CMYK-only is required, redesign
with achievable colors rather than accepting a bad fallback. The Color Bridge
CMYK simulation is **perceptual, not colorimetric**.

**In code.** PMS 485 C with CMYK 0/91/86/0 as fallback, both in every
print-ready file. A 2-color card uses PMS + K rather than 4-color: better
accuracy, less ink. Hand off **PDF/X-4 with ISO Coated v2 (FOGRA39)**.

---

## `iso-216`: The Only Self-Similar Ratio · medium `[spec]`

> Every A-series sheet is **1:√2**, so halving along the long edge yields the
> next size at identical proportions.

| | |
|---|---|
| **A0** | 841 × 1189 mm, 1 m² before rounding |
| **A4** | 210 × 297 mm |
| **B0** | 1000 × 1414 mm |
| **C4** | 229 × 324 mm, holds an A4 flat |
| **A4 → A3** | **141.4%** (√2 × 100) |

**Why √2 specifically.** With sides 1 and √2, halving the long side gives 1 and
√2/2, the same ratio, rotated. **No other starting ratio survives one fold**, so
every subsequent size would need a different shape.

**The three series.** **A** is used directly. **B** is the geometric mean of Aₙ
and Aₙ₋₁, filling gaps where A jumps too far, B5 (176 × 250) is a common
hardcover trim, and **B7 (88 × 125), not B5, matches ID-3 passport size**. **C**
(ISO 269) is the geometric mean of Aₙ and Bₙ, sized to sleeve an Aₙ sheet: C4
holds A4 flat, C5 holds it folded once, C6 twice.

**History.** Described by Lichtenberg (October 1786), developed into a
metric-linked system by Porstmann as DIN 476 (1922), adopted as ISO 216 in 1975.

**Where it doesn't.** The US and Canada use ANSI sizes, Letter 8.5 × 11 in,
Legal 8.5 × 14 in, with **no fixed aspect relationship between sizes**. Custom
trim sizes are common for press-sheet imposition even in ISO countries. And
**digital design has no sheet to fold: there is no structural reason to constrain
screen layouts to 1:√2.**
