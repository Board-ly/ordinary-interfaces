# Contributing

The whole value of this skill is that its numbers are checked. A pull request
that adds a plausible-sounding value without a source makes the skill worse, even
if the value is right. So the bar here is about **evidence**, not style.

## The one rule

**Every number carries an evidence grade, and the grade has to be honest.**

| Tag | Means | You need |
|---|---|---|
| `[spec]` | Normative: WCAG 2.2, ISO, OpenType, a platform HIG minimum | The clause or SC number |
| `[measured]` | From a study | The study, the year, and the sample where the sample matters |
| `[convention]` | Industry practice with no primary source | Say so plainly. Do not dress it up |

Laundering a `[convention]` into a `[spec]` is the failure mode this project
exists to avoid. The 8pt grid and the 1.5× padding ratio are conventions with
good reasoning, not perceptual facts.

## Adding or changing a rule

1. **Find the right file.** Rules live in
   `skills/ordinary-interfaces/references/`, 14 topic files. If your rule needs
   a fifteenth, open an issue first; a new area changes the routing table in
   `SKILL.md`.

2. **Follow the schema.** Every rule is one `##` block, in this order:

   ```markdown
   ## `rule-id`: Human Name · **critical** `[spec]`

   > The ruling. One line, quotable, no hedging.

   **Numbers.** Source, year, then the values, as a table when there is more than one.

   **Why it holds.** The mechanism, with a primary citation.

   **Where it doesn't.** The real exemptions. A rule with no exemptions is
   usually a rule that has not been used yet.

   **In code.** Concrete values, tokens, or a snippet.
   ```

   `· **critical**` marks a gate. There are ten; adding an eleventh is a
   discussion, not a PR.

3. **Cite the primary source.** Not a blog post that paraphrases the study. If
   you cannot reach the primary source, grade it `[convention]` and say where you
   found it.

4. **Regenerate the index.** `RULE_INDEX.md` is generated from the rule
   headings. CI fails on drift:

   ```bash
   python3 skills/ordinary-interfaces/scripts/build-index.py
   ```

5. **Measure anything you claim about contrast.**

   ```bash
   python3 skills/ordinary-interfaces/scripts/contrast.py "#767676" "#fff"
   ```

## Changing the scripts

The three scripts are dependency-free, read-only, and target the Python 3 that
ships with macOS and Ubuntu. Keep all three properties. No `pip install`, no
writes outside the file the user named, no `python3.12`-only syntax.

## What gets rejected

- A number with no source, or a source that is someone else's summary.
- Copied text from another skill, dataset, or documentation set. The facts are
  free; the expression is not. Write it in this schema, in your own words.
- Aesthetic direction. "Use more whitespace, it feels premium" belongs in a
  design skill that owns taste. This one owns thresholds.
- A rule that only restates a neighbouring rule with different words. Cross-
  reference instead.

## Checklist before opening a PR

- [ ] Every new number has a grade and a source
- [ ] The rule follows the five-part schema
- [ ] `build-index.py` re-run, diff committed
- [ ] Contrast claims produced by `contrast.py`, not by eye
- [ ] `SKILL.md` routing updated if you touched which file covers what

## Reporting instead of fixing

A wrong number is worth an issue even without a fix. Use the **Rule correction**
template and paste the source you have. That is the most useful issue this
repository can receive.
