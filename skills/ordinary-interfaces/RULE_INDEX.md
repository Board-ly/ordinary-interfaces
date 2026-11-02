# Rule Index

All 211 rules by id. `!` marks a critical rule (an accessibility gate).

Generated from the reference files' own headings, so it cannot drift from them.
Regenerate with `scripts/build-index.py`.

## Color: `references/color.md`

| Id | Rule | Pri |
|---|---|---|
| `wcag-contrast` ! | Contrast Ratio | critical |
| `red-green-color-blindness` ! | Never Color Alone | critical |
| `dark-mode-color-adaptation` | Three Axes, Three Jobs | high |
| `luminance-vs-lightness` | Lightness Is Not Luminance | medium |
| `cielab-color-space` | Perceptually Uniform Spaces | medium |
| `ramp-structure` | A System Is Ramps, Not Colors | high |
| `ramp-construction` | Hold the Hue | high |
| `color-naming` | Primitives Hold Values, Semantics Hold Jobs | medium |
| `token-role-discipline` | Use a Token Only in Its Role | high |
| `one-color-one-meaning` | One Color, One Meaning | high |
| `fill-one-action` | Fill Exactly One Action Per View | high |
| `color-scale` | Building the Ramp | medium |
| `greyscale` | Structure Before Color | medium |
| `60-30-10` | Proportion the Palette | medium |
| `color-temperature-dominance` | Let One Temperature Win | medium |
| `saturation-control` | Saturation by Role | medium |
| `simultaneous-contrast` | Color Is Read Relatively | medium |
| `color-constancy` | Colors Move Under Real Light | medium |
| `color-psychology` | Associations Are Conventions | medium |
| `gradient-interpolation` | Choose the Interpolation Space | medium |
| `rgb-vs-cmyk` | Emitted and Reflected Are Different Gamuts | medium |

## Typography: `references/typography.md`

| Id | Rule | Pri |
|---|---|---|
| `type-hierarchy` | Build the Scale From a Ratio | high |
| `line-length` | Cap the Measure | high |
| `line-height` | Leading Runs Inverse to Size | high |
| `three-line-leading` | Leading Floor for Wrapping Text | high |
| `text-alignment` | Left, With Few Exceptions | high |
| `font-weight-contrast` | Two Steps Between Levels | high |
| `weight-size-floor` | Weight Floors by Size | high |
| `x-height` | Perceived Size Is X-Height | medium |
| `font-pairing` | Match Proportion, Contrast Function | medium |
| `wcag-typography` | Text Must Survive the Reader | high |
| `text-wrap` | Four Declarations, Four Jobs | high |
| `letter-spacing-by-size` | Tracking Follows Size | medium |
| `all-caps-fatigue` | Caps for Labels Only | medium |
| `ios-input-zoom` | 16px Inputs on Mobile | high |
| `variable-fonts` | Worth It From Three Weights | medium |
| `typeface-vs-font` | The Distinction That Matters in CSS | medium |
| `font-synthesis` | Load the Real Faces | high |
| `css-properties-over-tags` | Properties Over Feature Tags | medium |
| `smart-punctuation` | Real Punctuation, Natural Case | medium |
| `underline-metrics` | Underlines From the Font | medium |
| `small-caps` | True Small Caps Only | low |
| `ligatures` | Defaults Are Right; Know When to Switch Off | low |
| `font-smoothing` | Root-Level Rendering Settings | low |

## Spacing & Layout: `references/spacing-layout.md`

| Id | Rule | Pri |
|---|---|---|
| `proximity` | Distance Encodes Relationship | high |
| `padding-gap-ratio` | Padding Exceeds the Gap | high |
| `group-with-space` | Space First, Lines Last | high |
| `8pt-grid` | One Base Unit for Spacing | high |
| `4pt-system` | The Half-Step | medium |
| `baseline-grid` | Vertical Rhythm on Fours | medium |
| `active-white-space` | Emptiness That Communicates | medium |
| `controls-distinct` | Controls Must Look Like Controls | high |
| `align-to-shared-edges` | Fewer Edges | high |
| `progressive-disclosure-cue` | Hidden Needs a Hint | high |
| `content-breakpoints` | Break Where Content Breaks | high |
| `translation-growth` | Text Grows | high |
| `content-bleeds-controls-float` | Bleed and Inset | medium |
| `manuscript-grid` | One Column, Four Margins | medium |
| `twelve-column-grid` | Twelve Divides Well | medium |
| `modular-grid` | Columns and Rows | medium |
| `wcag-layout` | Reflow, Orientation, Drag, Target Size | high |

## Controls, Forms & Navigation: `references/interaction.md`

| Id | Rule | Pri |
|---|---|---|
| `touch-target` ! | Size the Hit Area, Not the Glyph | critical |
| `button-design` | Six States, All Defined | high |
| `button-padding` | Compensate for the Icon's Mass | high |
| `link-design` | The Underline Is the Affordance | medium |
| `wcag-forms` | Label, Describe, Don't Re-Ask | high |
| `wcag-navigation` | Predictability Across Pages | high |
| `wcag-images` ! | Equivalent Purpose, Not Description | critical |
| `wcag-motion` ! | Flashing and Vestibular Safety | critical |

## Overlays & Dialogs: `references/overlays.md`

| Id | Rule | Pri |
|---|---|---|
| `overlay-taxonomy` | Four Elements, Four Jobs | high |
| `backdrop-spec` | Dim Enough to Mean It | medium |
| `dialog-to-sheet` | Below 600px a Dialog Is a Sheet | medium |
| `sheet-drag-contract` | The Sheet Follows the Finger | high |
| `grab-handle` | An Affordance With a Hit Area | medium |
| `scroll-lock` | Lock Without the Shift | high |
| `anchor-collision` | Flip, Then Shift, Then Clamp | medium |
| `focus-not-obscured` | Nothing Covers What the Keyboard Reached | high |
| `dismiss-contract` | Esc Always, Backdrop Sometimes | high |
| `overlay-stacking` | Three Tiers, Depth Two | medium |
| `overlay-surface` | An Overlay Declares Its Level | medium |
| `toast-budget` | Three Visible, Then Queue | medium |

## Surfaces: `references/surfaces.md`

| Id | Rule | Pri |
|---|---|---|
| `concentric-radius` | Outer Equals Inner Plus Padding | high |
| `shadow-as-border` | Shadows for Depth, Borders for Structure | high |
| `image-outlines` | A Neutral Hairline, Never Tinted | medium |
| `press-scale` | 0.96 on Click | medium |
| `theme-switch-suppression` | Suppress Transitions on the Flip | high |

## System Craft: `references/interface-craft.md`

| Id | Rule | Pri |
|---|---|---|
| `surface-elevation` | Layering Should Whisper | high |
| `border-discipline` | Findable, Not Visible | high |
| `depth-strategy` | Pick One | high |
| `token-architecture` | The Roles a Product UI Actually Needs | high |
| `interactive-states` | Five, Plus Three for Data | high |
| `tabular-numerals` | Fixed-Width Figures Wherever They Stack | medium |
| `icon-restraint` | Icons Clarify or Go | medium |
| `default-tells` | Recognise Your Own Defaults | medium |

## Depth & Icons: `references/depth-and-icons.md`

| Id | Rule | Pri |
|---|---|---|
| `shadow-fundamentals` | One Light, From Above | high |
| `elevation-system` | Five or Six Levels, Tokenised | medium |
| `raised-vs-inset` | Z-Axis Is Not Decoration | medium |
| `icon-stroke-weight` | Match the Adjacent Text | high |
| `icon-bounding-box` | One Frame, Variable Padding | medium |
| `icon-optical-balance` | Centre by Mass, Not by Box | medium |
| `icon-alignment` | Align to Cap Height | medium |
| `icon-color-states` | One SVG, Recolored | high |
| `icon-render-size` | Design at the Size It Ships | medium |
| `icons-rtl` | Flip Only What Reading Direction Owns | medium |

## Motion: `references/motion.md`

| Id | Rule | Pri |
|---|---|---|
| `animation-necessity` | Ask Whether, Before Asking Which | high |
| `animation-duration` | Under 300ms | high |
| `easing-curves` | Ease-Out by Default | high |
| `enter-exit-asymmetry` | Slow to Decide, Fast to Respond | high |
| `subtle-exit` | Exits Do Not Fight for Attention | medium |
| `never-scale-zero` | Nothing Appears From Nothing | high |
| `transform-origin` | Popovers Scale From Their Trigger | medium |
| `stagger` | Cap the Run | medium |
| `staged-enter` | Split Semantic Chunks | medium |
| `icon-transitions` | Contextual Icon Swaps | medium |
| `spring-physics` | Springs for Interruptible Motion | medium |
| `gesture-physics` | Drag Should Obey Physics | medium |
| `animation-performance` | Transform and Opacity Only | high |
| `transition-specificity` | Name the Properties | high |
| `will-change-discipline` | A Hint, Not a Habit | medium |
| `hover-gating` | Gate Hover to Real Pointers | high |
| `motion-restraint` | Motion Is Never the Only Channel | high |
| `reduced-motion` ! | Gentler, Not Absent | critical |
| `seam-principle` | Most Transition Problems Are Layout Problems | high |
| `reveal-choreography` | Group by Perceptual Unit | high |
| `state-transition-timing` | The Reference Table | high |
| `numbers-in-motion` | Changing Values Jitter | medium |

## Non-Happy States: `references/states.md`

| Id | Rule | Pri |
|---|---|---|
| `state-ledger` | Decide Every State, in Writing | high |
| `empty-states` | Empty Is Three States | high |
| `loading-strategy` | Choose by Layout Knowability | high |
| `partial-data` | Real Records Have Holes | high |
| `error-taxonomy` | Kind First, Then Placement | high |
| `optimistic-rollback` | The Reverse Is the Hard Part | high |
| `overflow-pressure` | The Layout Under Load | high |
| `offline-stale` | Is This Screen Lying? | medium |
| `permission-states` | 403 and 404 Are a Design Decision | medium |
| `end-of-list` | Terminus, Settled, and Continuity | medium |

## Tables & Dense Data: `references/data-display.md`

| Id | Rule | Pri |
|---|---|---|
| `table-chrome` | Hairlines and a Frame, Not a Grid | medium |
| `column-alignment` | Numbers Right, Text Left, Nothing Centred | high |
| `row-density` | Three Densities, One Per Table | medium |
| `sticky-chrome` | The Header Sticks, Identity Sticks on Narrow | medium |
| `cell-truncation` | One Column May Truncate | medium |
| `status-encoding` | A Dot and a Word | high |
| `selection-without-shift` | Reserve the Column | medium |
| `sort-affordance` | One Sorted Column, Announced | medium |
| `table-empty-and-loading` | Keep the Columns | medium |

## Accessibility in Practice: `references/a11y-implementation.md`

| Id | Rule | Pri |
|---|---|---|
| `native-elements-first` ! | Don't Rebuild What Ships | critical |
| `focus-visible` ! | Style the Right Pseudo-Class | critical |
| `keyboard-patterns` ! | Follow the APG | critical |
| `focus-trap` | Trap on Open, Restore on Close | high |
| `hit-area-extension` | Grow the Target, Not the Glyph | high |
| `form-controls` | Label, Type, and Never Block Paste | high |
| `error-announcement` | Enabled Until Submitted | high |
| `live-regions` | Three Mechanisms, Three Jobs | high |
| `alt-by-purpose` ! | Describe the Job, Not the Picture | critical |

## Interface Copy: `references/writing.md`

| Id | Rule | Pri |
|---|---|---|
| `voice-and-tone` | One Voice, Tone Flexes With Stakes | high |
| `consistent-vocabulary` | One Noun, One Verb, Per Concept | high |
| `verb-first-buttons` | Start With the Verb | high |
| `link-text` | Make Sense Out of Context | high |
| `error-copy` | Say How to Fix It, Where It Broke | high |
| `empty-state-copy` | Orientation Plus a Next Step | high |
| `toggle-labels` | Describe the ON State | medium |
| `capitalization-policy` | One Policy Per Element Type | medium |
| `no-string-concatenation` | Never Assemble a Sentence | high |

## Hierarchy & Emphasis: `references/composition.md`

| Id | Rule | Pri |
|---|---|---|
| `emphasis` | Emphasis Is Relative | high |
| `visual-weight` | Six Channels, Honestly Labelled | high |
| `hierarchy-channels` | Separate Levels on More Than One Channel | high |
| `rule-of-thirds` | A Heuristic With Weak Evidence | medium |
| `golden-ratio` | A Proportioning Start, Not a Guarantee | low |
| `rule-of-odds` | Odd Groups Resolve Faster | low |
| `corner-radius-tone` | Radius Carries Tone, Consistency Carries More | low |
| `pie-chart-problem` | Encode on the Accurate Channels | medium |
| `handmade-vs-polished` | Register Is a Choice, Not a Quality Level | medium |

## Cognition & Behaviour: `references/ux-laws.md`

| Id | Rule | Pri |
|---|---|---|
| `jakobs-law` | Convention Is Accumulated Learning | high |
| `millers-law` | Working Memory Is Small, and Chunks Are the Unit | high |
| `chunking` | Group Before You Place | high |
| `hicks-law` | Choice Cost Is Logarithmic | high |
| `subitizing` | Four Is Instant; Five Is Counting | medium |
| `von-restorff-effect` | One Isolate Per Group | high |
| `banner-blindness` | Ad-Shaped Things Are Not Seen | high |
| `inattentional-blindness` | Visible Is Not Seen | high |
| `default-effect` | Preselection Persists | medium |
| `decoy-effect` | Asymmetric Dominance Shifts Choice | medium |
| `peak-end-rule` | Memory Keeps the Peak and the Ending | medium |
| `picture-superiority` | Distinctiveness, Not Imagery | medium |
| `stroop-effect` | Keep Color and Meaning Congruent | medium |
| `reward-anticipation` | Anticipation, With an Ethical Boundary | medium |
| `ebbinghaus-illusion` | Size Is Judged Against Neighbours | medium |
| `optical-center` | The Visual Centre Sits High | medium |
| `center-bias` | First Fixation Lands High of Centre | medium |
| `muller-lyer-illusion` | Cap Direction Biases Perceived Length | low |
| `irradiation-illusion` | Light on Dark Reads Larger | low |
| `bouba-kiki-effect` | Curvature Carries Tone | low |

## Agent Tells: `references/ai-tells.md`

| Id | Rule | Pri |
|---|---|---|
| `one-spacing-value` | Rhythm, Not a Constant | high |
| `one-shadow-everywhere` | Elevation Has to Mean Something | medium |
| `border-instead-of-surface` | Everything Outlined | medium |
| `hover-without-press` | No State for the Finger | high |
| `centred-everything` | Centring as the Default Axis | medium |
| `three-equal-cards` | The Feature Grid Reflex | medium |
| `load-animation-on-everything` | Entrances Nobody Asked For | high |
| `mixed-icon-sets` | Two Libraries and an Emoji | medium |
| `form-tells` | The Label Is Not Optional | high |
| `happy-path-only` | One State Shipped | high |

## Beyond the Screen (appendix): `references/beyond-screen.md`

| Id | Rule | Pri |
|---|---|---|
| `viewing-distance` | Distance Sets Everything Else | high |
| `visual-angle-arcminutes` | The Eye Measures Angle | high |
| `aspect-ratios` | Ratio Belongs to Context | medium |
| `logo-clearspace` | A Protected Zone, Defined as a Ratio | medium |
| `logo-variations` | Six Types, Three Lockups | medium |
| `joint-cropping` | Do Not Cut at a Joint | low |
| `dieline-bleed` | Errors Become Physical | high |
| `cmyk-vs-pantone` | Spec Both, Always | high |
| `iso-216` | The Only Self-Similar Ratio | medium |
