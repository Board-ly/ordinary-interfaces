---
name: rule
description: 'Looks up a rule from ordinary-interfaces by id or topic and reports the value, its evidence grade, where it stops applying, and the reference file it lives in. Use to check a single number without loading the whole skill.'
argument-hint: '[rule-id or topic]'
allowed-tools: Read Glob Grep
---

# Look up a rule

Looking for: `$ARGUMENTS`.

1. Search `RULE_INDEX.md` in the ordinary-interfaces skill for the id or the
   topic. Ids look like `touch-target`, `concentric-radius`,
   `padding-gap-ratio`.
2. Open the reference file the index points at and read the whole entry, not the
   headline number. The `When It Breaks` note is usually the part that decides
   whether the rule applies here at all.
3. If nothing matches, say so and name the closest two rules rather than
   inventing a value. A number this skill does not carry is not a number this
   skill should give.

Report:

- **The value**, with its unit and its condition.
- **The evidence grade.** `[spec]` is normative and required, `[measured]` cites
  a study and should carry the sample where it matters, `[convention]` is
  industry practice with no primary source. Speak about each accordingly:
  "required" and "fails AA" for a spec, "measured at" for a study, "convention
  is" for a convention.
- **Where it stops applying**, from the `When It Breaks` note.
- **The rule id in parentheses**, so the reader can check it.
