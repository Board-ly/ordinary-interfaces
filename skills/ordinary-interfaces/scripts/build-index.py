#!/usr/bin/env python3
"""Regenerate RULE_INDEX.md from the reference files' own headings.

Run after adding, removing or renaming a rule. The index is generated rather
than maintained by hand so it cannot drift from the files it describes.
"""
import pathlib
import re
import sys

ORDER = [
    ("color.md", "Color"), ("typography.md", "Typography"),
    ("spacing-layout.md", "Spacing & Layout"),
    ("interaction.md", "Controls, Forms & Navigation"),
    ("overlays.md", "Overlays & Dialogs"), ("surfaces.md", "Surfaces"),
    ("interface-craft.md", "System Craft"), ("depth-and-icons.md", "Depth & Icons"),
    ("motion.md", "Motion"), ("states.md", "Non-Happy States"),
    ("data-display.md", "Tables & Dense Data"),
    ("a11y-implementation.md", "Accessibility in Practice"),
    ("writing.md", "Interface Copy"), ("composition.md", "Hierarchy & Emphasis"),
    ("ux-laws.md", "Cognition & Behaviour"), ("ai-tells.md", "Agent Tells"),
]
HEADING = re.compile(
    r"^## `([a-z0-9-]+)`\s*:\s*(.+?)\s*·\s*(?:\*\*)?(critical|high|medium|low)(?:\*\*)?",
    re.M)


def main(root):
    root = pathlib.Path(root)
    refs = root / "references"
    for fn, _ in ORDER:
        if not (refs / fn).is_file():
            print("error: missing " + fn, file=sys.stderr)
            return 1
    out, total = [], 0
    for fn, title in ORDER:
        rows = HEADING.findall((refs / fn).read_text())
        out += ["\n## " + title + ": `references/" + fn + "`\n",
                "| Id | Rule | Pri |", "|---|---|---|"]
        for rid, desc, pri in rows:
            bang = " !" if pri == "critical" else ""
            out.append("| `" + rid + "`" + bang + " | " + desc.replace("|", "\\|")
                       + " | " + pri + " |")
            total += 1
    header = ("# Rule Index\n\nAll " + str(total) + " rules by id. `!` marks a "
              "critical rule (an accessibility gate).\n\nGenerated from the "
              "reference files' own headings, so it cannot drift from them.\n"
              "Regenerate with `scripts/build-index.py`.\n")
    (root / "RULE_INDEX.md").write_text(header + "\n".join(out) + "\n")
    print("wrote RULE_INDEX.md, " + str(total) + " rules")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1
                  else pathlib.Path(__file__).resolve().parent.parent))
