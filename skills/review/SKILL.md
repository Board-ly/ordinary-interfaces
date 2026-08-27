---
name: review
description: 'Full ordinary-interfaces review of a screen, component, CSS or screenshot. Runs the project scan first, then produces a checklist ordered critical to low, each finding carrying a rule id, the measured value, and the concrete fix. Use for a design and WCAG 2.2 review that has to be defensible rather than a matter of taste.'
argument-hint: '[file, component, or screenshot]'
disable-model-invocation: true
allowed-tools: Bash Read Glob Grep
---

# Audit

Target: `$ARGUMENTS`. If empty, ask what to review rather than guessing.

## Order

1. **Run the project scan first.**
   `python3 .claude/skills/ordinary-interfaces/scripts/project-system.py .`
   A finding is "this breaks the project's own system" first, and "this differs
   from the reference" only second. The first is nearly always the more useful
   sentence.
2. **Check the seven gates.** They constrain everything else. See
   `/ordinary-interfaces:accessibility`.
3. **Load only the reference files the target touches.** The routing table in the
   ordinary-interfaces skill maps surface to file.
4. **Measure rather than estimate.** Contrast goes through `contrast.py`. A value
   you did not measure is an inferred finding and must be labelled as one.

## Output

```
CRITICAL  wcag-contrast      #777777 label on #fff is 4.48:1, fails AA (needs 4.5:1)
                             → #767676 or darker; separate token for text vs border
HIGH      concentric-radius  Card is rounded-xl with p-2, inner is rounded-xl
                             → outer 24px = inner 16px + 8px padding
MEDIUM    padding-gap-ratio  Card padding 16px equals the 16px grid gutter
                             → 24px padding (1.5× heuristic)
```

## Rules for the audit

- **Do not invent findings to fill the list.** An empty CRITICAL section is a
  result, and saying so plainly beats padding.
- **Do not score the design out of 10.** There is no evidence base for that
  number and it obscures which fixes matter.
- **Check the `When It Breaks` notes before flagging.** Full-bleed media, dense
  data tables, disabled controls and decorative elements have real exemptions,
  and flagging them trains people to ignore the whole audit.
- **Carry the evidence grade.** `[spec]` is required, `[measured]` cites its
  study, `[convention]` is a reasonable default. Never launder a convention into
  a law, and never hedge a spec.
- **Say what you could not verify.** With only CSS or a description, separate
  verified findings from inferred ones. Replay motion at 10% speed before judging
  it: what feels off at 10% is what is subtly wrong at full speed.
- **One row per root cause**, listing every location it appears in.
