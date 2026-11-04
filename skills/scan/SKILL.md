---
name: scan
description: 'Step 0 of ordinary-interfaces. Reports what this codebase already decided about tokens, radius and spacing scales, colour notation, type sizes, breakpoints and motion, so a review adopts the project system instead of overwriting it. Run before quoting any reference value.'
argument-hint: '[path, default .]'
allowed-tools: Bash Read Glob Grep
---

# Read the project's system first

Run the scanner on the path in `$ARGUMENTS`, or `.` if empty:

```bash
python3 .claude/skills/ordinary-interfaces/scripts/project-system.py $ARGUMENTS
```

Installed as a plugin instead of through `npx skills add`, the script is at
`${CLAUDE_PLUGIN_ROOT}/skills/ordinary-interfaces/scripts/project-system.py`.

Then report, in this order:

1. **What the project has decided.** Token families, radius and spacing scales,
   colour notation, type sizes, breakpoints, motion durations and curves.
2. **What is missing.** Absent `:focus-visible`, `prefers-reduced-motion` or
   `tabular-nums` are the three that matter most, because each one is a rule in
   this skill that the project currently cannot satisfy.
3. **Which scales the reference values would collide with.** Name them
   explicitly so later findings can be phrased against the project's own system
   rather than against the reference.

On a shadcn project also run `npx shadcn@latest info --json` for resolved paths
and installed components.

`match-the-project` is the highest-precedence rule in the skill. A 7px radius in
a system built on 7px is correct, and "should be 8px per the grid" is noise. Do
not recommend a value this scan shows the project has already settled.
