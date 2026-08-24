# Security

## What this repository contains

Markdown rules, a static HTML page, and three Python scripts. There is no server,
no build toolchain, no package published to a registry, and **no dependencies**.
The scripts use only the standard library.

## Threat surface, such as it is

| Script | Reads | Writes | Network |
|---|---|---|---|
| `contrast.py` | its arguments | nothing | none |
| `project-system.py` | source files under the path you give it | nothing | none |
| `build-index.py` | `references/*.md` | `RULE_INDEX.md` | none |

`project-system.py` walks a codebase you point it at and prints what it finds. If
you run it on a directory containing secrets, its **output** may include values
from your config files, so treat that output as you would the files themselves. It
never transmits anything.

The skill is also read by an AI agent. Markdown in `references/` is instructions
to that agent, so treat a pull request that edits those files the way you would
treat one that edits executable code.

## Reporting a vulnerability

Email **finn.m.garrels@gmail.com** with "ordinary-interfaces" in the subject.
Please do not open a public issue for anything exploitable. Expect a reply within
a week.

Wrong *numbers* are not security issues. Those go in a public issue, where they
get fixed faster.
