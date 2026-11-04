---
name: contrast
description: 'Measures a colour pair against WCAG 2.2 and reports the ratio with pass or fail for normal text, large text and UI components. With --fix it walks the foreground to the nearest passing value while keeping the hue. Use instead of estimating whether a pair passes.'
argument-hint: '<foreground> <background> [--fix]'
allowed-tools: Bash
---

# Contrast

```bash
python3 .claude/skills/ordinary-interfaces/scripts/contrast.py $ARGUMENTS
```

Installed as a plugin, the script is at
`${CLAUDE_PLUGIN_ROOT}/skills/ordinary-interfaces/scripts/contrast.py`.

The script is dependency-free and read-only. It reports the ratio and pass or
fail for normal text, large text and UI components; `--fix` returns the nearest
passing foreground with the hue kept.

When reporting the result:

- **4.5:1 is normal text. 3:1 is large text (≥24px regular, ≥18.66px bold) and UI
  components.** Say which threshold applies to the pair in question rather than
  quoting all three.
- **Measure the rendered value.** A token is not a colour: opacity, a blend mode
  or a gradient beneath it changes what the eye receives. Measure the worst point
  of a gradient, and each theme independently.
- **4.5:1 is a `[spec]` value, not a preference.** Do not hedge it, and do not
  round 4.48 up.

If `$ARGUMENTS` is empty, ask for the two colours rather than guessing.
