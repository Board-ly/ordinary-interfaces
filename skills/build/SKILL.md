---
name: build
description: 'The ordinary-interfaces workflow for building a new screen or component: adopt the project system, let the seven gates constrain the solution space before drawing, work greyscale first, and enumerate the non-happy states before writing markup. Use when starting UI rather than reviewing it.'
argument-hint: '[what you are building]'
disable-model-invocation: true
allowed-tools: Bash Read Glob Grep
---

# Build

Building: `$ARGUMENTS`.

1. **Run `project-system.py`.** Adopt what exists before adding anything.
   `python3 .claude/skills/ordinary-interfaces/scripts/project-system.py .`
2. **Read the seven gates.** They constrain the solution space before you draw,
   which is cheaper than discovering them in review.
3. **Load the reference files for the surfaces involved**, using the routing
   table in the ordinary-interfaces skill.
4. **Take values from the project, then the reference, never from memory.** The
   whole point is that these numbers are checked. Guessing "probably 1.4
   line-height" defeats it.
5. **Work greyscale first.** If hierarchy fails without colour, colour will not
   fix it (`greyscale`). Then apply the 60-30-10 split.
6. **Enumerate the non-happy states before writing markup** (`state-ledger`) and
   build the hardest one first. A layout that survives its worst state survives
   its best; the reverse is not true. `sad-paths` owns that workflow in depth.
7. **Verify contrast with `contrast.py`** before claiming a pair passes.

Numbers here, taste elsewhere. If these values would produce a
competent-but-generic result, that is the skill working as intended. Nothing here
tells you what the design should be: `design-engineering` and `frontend-design`
own that.
