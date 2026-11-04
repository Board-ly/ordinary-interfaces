---
name: space
description: 'Measures spacing against padding-gap-ratio, 8pt-grid and 4pt-system: whether a container''s padding exceeds the gap between its children, which spacing steps the project actually uses, and which fall off the scale. Takes a path to scan or one padding/gap pair to check. Use when deciding how much padding a container needs, when a layout reads as a flat list of boxes, or when a spacing scale needs auditing.'
argument-hint: '[path] or [padding] [gap]'
allowed-tools: Bash Read Glob Grep
---

# Space

Target: `$ARGUMENTS`. A path scans it; two numbers check that one pair. If
empty, scan the working directory.

```bash
python3 .claude/skills/ordinary-interfaces/scripts/spacing.py .
python3 .claude/skills/ordinary-interfaces/scripts/spacing.py --pair 16 24
```

## What it decides, and what it cannot

The scan pairs a container's padding with the gap between its children wherever
both sit on the same element: one class list holding `p-4` and `gap-6`, or one
CSS block holding `padding` and `gap`. That pairing is the whole trick, and it
is the only part of `padding-gap-ratio` that is decidable without rendering.

It reports the axis, because a `gap` on a flex row opens space between columns
and none between rows. Comparing that gap against the vertical padding compares
a number against nothing, and it is the failure that turns this check into
noise. Elements that declare padding and a gap but no `flex` or `grid` are
skipped and counted, not guessed at: without a layout mode on the same element
the gap separates nothing there.

Variant-prefixed utilities are ignored, `md:gap-12` and `hover:p-4` with them.
They belong to a breakpoint or a state this read is not in, and folding them
into one container's numbers produces a ratio that is true at no viewport.

**What it cannot see:** a class list assembled by `cva` or a variant helper, a
value arriving through a token or a CSS variable, and anything decided at
runtime. It also cannot see the rule's own exemptions, which is the important
one. Full-bleed media breaks the ratio deliberately, a dense table compresses
on purpose (`data-display.md → row-density`), and a container with a border or
its own background already states its boundary. Confirm which applies before
moving a number.

## Reading the output

Findings are ordered by **how many px of padding are missing**, not by the
ratio. A badge at 2px against an 8px gap has the worse ratio; a card at 8px
against a 24px gap is the one anybody can see. The worst ratios are almost
always the smallest components, and leading with them is how a spacing audit
gets ignored.

The scale section is the more useful half on a first run. A project with 40
distinct spacing values has no scale, whatever its config file says, and that
is `ai-tells.md → one-spacing-value` from the other direction: that rule catches
one value used everywhere, this catches every value used once.

## Rules behind it

| | |
|---|---|
| `padding-gap-ratio` | ≥1.5× `[convention]`, 2× reads more clearly |
| `8pt-grid` | 8, 16, 24, 32, 40, 48, 56, 64 |
| `4pt-system` | 4pt for type, icon gaps and dense UI; 8pt for structure |
| `proximity` | why the ratio exists: distance encodes relationship |

All three spacing rules are `[convention]`. Say "convention is" and not
"must", and never report a ratio finding as a failure in the sense that a
contrast finding is one. `spacing-layout.md` holds the full rules with their
exemptions; read it before writing up more than a number.
