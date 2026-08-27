# Ordinary Interfaces

180 UI rules with hard numbers, each graded by how well it is actually evidenced.
An agent skill for the thousand small decisions underneath a screen: contrast,
type, spacing, hit areas, component states, motion, surfaces, icons, empty and
error states, and the words in the interface.

## Install

```bash
npx skills add Board-ly/ordinary-interfaces
```

Works in Claude Code, Codex, Opencode and other agents. As a Claude Code plugin:

```text
/plugin marketplace add Board-ly/ordinary-interfaces
/plugin install ordinary-interfaces
```

Or by hand. Copy `skills/ordinary-interfaces/` into `.claude/skills/` for one
project, `~/.claude/skills/` for every project.

## Commands

The skill loads itself when a task calls for it. These six run a specific part of
it on demand, so you can reach for one step without pulling in the whole thing.

| Command | Does | Takes |
|---|---|---|
| `/ordinary-interfaces:read-project` | Reads what your codebase already decided about tokens, scales, colour notation and motion, so a review adopts your system instead of overwriting it | `[path]` |
| `/ordinary-interfaces:accessibility` | The seven floors only: contrast, colour, hit areas, alt text, focus, motion, reflow. Pass, fail or unverified, and one verdict | `[file or path]` |
| `/ordinary-interfaces:review` | Full review, ordered critical to low, every finding with a rule id, a measured value and the fix | `[file, component, screenshot]` |
| `/ordinary-interfaces:new-screen` | The workflow for building: adopt the system, let the floors constrain the space, greyscale first, hardest state first | `[what you are building]` |
| `/ordinary-interfaces:contrast` | Measures a colour pair against WCAG; `--fix` returns the nearest passing foreground | `<fg> <bg> [--fix]` |
| `/ordinary-interfaces:find-rule` | One rule by id or topic: the value, its evidence grade, and where it stops applying | `[rule-id or topic]` |

Outside Claude Code the bare names work too, `/review` and `/contrast`,
unless something else already owns them.

Each is its own skill under `skills/`, so `npx skills add` can install one on its
own:

```bash
npx skills add Board-ly/ordinary-interfaces --skill accessibility
```

None of them auto-load. They carry `disable-model-invocation: true` so they stay
out of the way until you type them; the main skill is the one that loads itself
when a task calls for it.

## Why use it?

Ask an agent for a card and it will guess. Probably `1.4` line-height, probably
`rounded-xl`, probably `#777` for the muted label, which is 4.48:1 on white and
fails AA by one hex digit. The guesses are plausible, which is exactly what makes
them expensive: nothing in the output tells you which numbers were checked.

Every value here is checked and carries its grade. `[spec]` is normative and gets
stated as law. `[measured]` comes from a study and gets cited. `[convention]` is
industry practice with no primary source, and never gets quoted as more than
that. A rule you can't check is a rule you shouldn't trust.

And step 0 is always the project itself. The skill reads your codebase before it
quotes any default, so a 7px radius in a system built on 7px stays 7px instead of
being corrected to 8. The most useful finding is "this breaks your own system,"
not "this differs from my reference."

Ordinary is the goal, and it is not the same as generic. An ordinary interface is
unremarkable *in use*. It behaves the way people expect, its hit areas are where
fingers go, its errors appear where the user is looking. Where an interface
should be distinctive, that judgement is yours. This makes sure everything
underneath it is right.

## Reference

`SKILL.md` routes to the one file a task needs; nothing else loads.

- **[color](skills/ordinary-interfaces/references/color.md)**: 21 rules. Ramps, tokens, dark mode, and the two contrast gates.
- **[typography](skills/ordinary-interfaces/references/typography.md)**: 23 rules. Measure, leading, hierarchy, web font details.
- **[motion](skills/ordinary-interfaces/references/motion.md)**: 22 rules. Duration, easing, transitions, gestures.
- **[ux-laws](skills/ordinary-interfaces/references/ux-laws.md)**: 20 rules. The most quoted and worst quoted findings in design.
- **[spacing-layout](skills/ordinary-interfaces/references/spacing-layout.md)**: 17 rules. Padding, gaps, grids, breakpoints, RTL, translation growth.
- **[depth-and-icons](skills/ordinary-interfaces/references/depth-and-icons.md)**: 10 rules. Elevation scale, icon sizing, stroke, optical alignment.
- **[states](skills/ordinary-interfaces/references/states.md)**: 10 rules. Empty, loading, error, partial, overflow, offline.
- **[a11y-implementation](skills/ordinary-interfaces/references/a11y-implementation.md)**: 9 rules. Focus, keyboard, ARIA, live regions, hit areas.
- **[writing](skills/ordinary-interfaces/references/writing.md)**: 9 rules. Button labels, errors, empty-state copy, capitalization.
- **[composition](skills/ordinary-interfaces/references/composition.md)**: 9 rules. Hierarchy, emphasis, focal points, optical center.
- **[interaction](skills/ordinary-interfaces/references/interaction.md)**: 8 rules. Buttons, links, inputs, forms, nav, component states.
- **[interface-craft](skills/ordinary-interfaces/references/interface-craft.md)**: 8 rules. Layering, borders, tokens: system versus a pile of components.
- **[surfaces](skills/ordinary-interfaces/references/surfaces.md)**: 5 rules. Radius, depth, press feedback, theme switch.
- **[beyond-screen](skills/ordinary-interfaces/references/beyond-screen.md)**: 9 rules kept as an appendix, outside the UI focus.
- **[accessibility](skills/ordinary-interfaces/references/accessibility.md)**: the WCAG cross-index. Which success criterion each rule answers, and the audit order.

Every id is listed one line each in
[RULE_INDEX.md](skills/ordinary-interfaces/RULE_INDEX.md).

## Scripts

Dependency-free, read-only, standard library only.

```bash
# Step 0, always: what has this project already decided?
python3 skills/ordinary-interfaces/scripts/project-system.py .

# A colour pair, and the nearest passing value if it fails
python3 skills/ordinary-interfaces/scripts/contrast.py "#777" "#fff" --fix
```

`project-system.py` reports the token families, radius and spacing scales, colour
notation, type sizes, breakpoints and motion curves a codebase already uses, plus
whether `:focus-visible`, `prefers-reduced-motion` and `tabular-nums` appear at
all. `contrast.py` gives the ratio and the AA/AAA verdicts, and `--fix` walks a
foreground to the nearest passing value at constant hue.

[CONTRIBUTING.md](CONTRIBUTING.md) has the rule schema and the evidence bar for
pull requests.

## Licence

[MIT](LICENSE), © 2026 Board-ly.
