#!/usr/bin/env python3
"""Measure spacing against padding-gap-ratio, 8pt-grid and 4pt-system.

Two modes:

    spacing.py --pair 16 24        one padding/gap pair, like contrast.py
    spacing.py <path>              every container in a codebase

The scan pairs a container's padding with the gap between its children, which
is decidable without rendering wherever both are declared on the same element:
one class list holding `p-4` and `gap-6`, or one CSS block holding `padding`
and `gap`. Values come back in px; Tailwind steps convert at 4px per step.

padding-gap-ratio is `[convention]`, not a spec. A failure here is a question
worth asking, not a defect, and the rule's own exemptions (full-bleed media,
dense tables, a card that already carries a border or its own background) are
invisible to a static read. Dependency-free and read-only.
"""
import pathlib
import re
import sys

RATIO = 1.5
RATIO_CLEAR = 2.0
STEP_PX = 4.0

CODE = {".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte", ".astro", ".html", ".php", ".erb"}
STYLE = {".css", ".scss", ".sass", ".less"}
SKIP = {"node_modules", ".git", "dist", "build", ".next", "out", "vendor", "coverage", ".venv"}

# class="…", className={cn(…)}, :class="…"
ATTR = re.compile(r"""(?:class|className|:class)\s*=\s*(?:"([^"]*)"|'([^']*)'|\{((?:[^{}]|\{[^{}]*\})*)\})""")
CSS_BLOCK = re.compile(r"([^{}]*)\{([^{}]*)\}")
# No variant may precede it: `md:gap-12` and `hover:p-4` belong to a state or a
# breakpoint this read is not in, and mixing them into one container's numbers
# produces a ratio that is true at no viewport.
UTIL = re.compile(r"(?<![\w:.-])(p|px|py|pt|pr|pb|pl|ps|pe|gap|gap-x|gap-y)-(\[[^\]]+\]|[\d.]+|px)(?![\w-])")
FLEX_COL = re.compile(r"(?<![\w:-])flex-col(?![\w-])|flex-direction\s*:\s*column")
FLEX_ROW = re.compile(r"(?<![\w:-])(?:inline-)?flex(?![\w-])")
GRID = re.compile(r"(?<![\w:-])(?:inline-)?grid(?![\w-])")
DECL = re.compile(r"(?<![\w-])(padding|padding-inline|padding-block|padding-top|padding-right|padding-bottom|padding-left|gap|column-gap|row-gap|grid-gap)\s*:\s*([^;}]+)")
LEN = re.compile(r"(-?[\d.]+)\s*(px|rem|em)")


def px(raw, root_px):
    """One CSS length to px, or None when it is not a plain length."""
    m = LEN.search(raw.strip())
    if not m:
        return None
    n = float(m.group(1))
    return n * (root_px if m.group(2) in ("rem", "em") else 1)


def util_px(token, root_px):
    """A Tailwind spacing step to px. `px` is the 1px literal, not the axis."""
    if token == "px":
        return 1.0
    if token.startswith("["):
        return px(token[1:-1], root_px)
    try:
        return float(token) * STEP_PX
    except ValueError:
        return None


PAD_X = {"px", "pl", "pr", "ps", "pe", "padding-inline", "padding-left", "padding-right"}
PAD_Y = {"py", "pt", "pb", "padding-block", "padding-top", "padding-bottom"}
PAD_ALL = {"p", "padding"}
GAP_X = {"gap-x", "column-gap"}
GAP_Y = {"gap-y", "row-gap"}
GAP_ALL = {"gap", "grid-gap"}


def axes(found):
    """Collapse per-side spacing into an {x, y} padding and an {x, y} gap.

    Padding takes the tightest side, because the shortest distance is where
    containment stops reading. Gap takes the widest, for the same reason from
    the other direction. An axis-specific value wins over the shorthand.
    """
    buckets = {k: [] for k in ("pad_all", "pad_x", "pad_y", "gap_all", "gap_x", "gap_y")}
    for key, value in found:
        if key in PAD_ALL:
            buckets["pad_all"].append(value)
        elif key in PAD_X:
            buckets["pad_x"].append(value)
        elif key in PAD_Y:
            buckets["pad_y"].append(value)
        elif key in GAP_ALL:
            buckets["gap_all"].append(value)
        elif key in GAP_X:
            buckets["gap_x"].append(value)
        elif key in GAP_Y:
            buckets["gap_y"].append(value)

    def pick(specific, shorthand_, fn):
        if buckets[specific]:
            return fn(buckets[specific])
        return fn(buckets[shorthand_]) if buckets[shorthand_] else None

    pad = {"x": pick("pad_x", "pad_all", min), "y": pick("pad_y", "pad_all", min)}
    gap = {"x": pick("gap_x", "gap_all", max), "y": pick("gap_y", "gap_all", max)}
    return pad, gap


def live_axes(body):
    """Which axes a plain `gap` actually separates siblings on.

    A `gap` on a flex row opens space between columns and none between rows, so
    comparing it against the vertical padding compares a number against nothing.
    Returning None means the element declares no layout mode, in which case it
    is not the flex or grid container and its gap does nothing here.
    """
    if GRID.search(body):
        return ("x", "y")
    if FLEX_COL.search(body):
        return ("y",)
    if FLEX_ROW.search(body):
        return ("x",)
    return None


def pairs_from(found, body):
    """Every (axis, padding, gap) a container declares on one element."""
    pad, gap = axes(found)
    explicit = {k for k, _ in found} & (GAP_X | GAP_Y)
    live = live_axes(body)
    if live is None and not explicit:
        return None
    out = []
    for axis in ("x", "y"):
        g, p = gap.get(axis), pad.get(axis)
        if not g or g <= 0 or p is None:
            continue
        # gap-x and gap-y name their own axis and need no layout mode.
        named = (axis == "x" and GAP_X & explicit) or (axis == "y" and GAP_Y & explicit)
        if not named and live is not None and axis not in live:
            continue
        if not named and live is None:
            continue
        out.append((axis, p, g))
    return out


def shorthand(raw, root_px):
    """`padding: 16px 24px` to the tightest value on each axis."""
    parts = [px(p, root_px) for p in raw.split()]
    parts = [p for p in parts if p is not None]
    if not parts:
        return []
    if len(parts) == 1:
        return [("padding", parts[0])]
    if len(parts) == 2:
        return [("padding-block", parts[0]), ("padding-inline", parts[1])]
    if len(parts) == 3:
        return [("padding-top", parts[0]), ("padding-inline", parts[1]), ("padding-bottom", parts[2])]
    return [("padding-top", parts[0]), ("padding-right", parts[1]),
            ("padding-bottom", parts[2]), ("padding-left", parts[3])]


def scan_text(text, suffix, root_px):
    """Yield (line, label, found) for each element declaring spacing."""
    if suffix in CODE:
        for m in ATTR.finditer(text):
            body = m.group(1) or m.group(2) or m.group(3) or ""
            found = []
            for key, token in UTIL.findall(body):
                value = util_px(token, root_px)
                if value is not None:
                    found.append((key, value))
            if found:
                line = text.count("\n", 0, m.start()) + 1
                label = " ".join(f"{k}-{int(v) if v == int(v) else v}px" for k, v in found)
                yield line, label, found, body
    if suffix in STYLE or suffix in CODE:
        for m in CSS_BLOCK.finditer(text):
            selector, body = m.group(1).strip().splitlines()[-1:], m.group(2)
            found = []
            for key, raw in DECL.findall(body):
                if key == "padding":
                    found += shorthand(raw, root_px)
                    continue
                value = px(raw, root_px)
                if value is not None:
                    found.append((key, value))
            if found:
                line = text.count("\n", 0, m.start()) + 1
                yield line, (selector[0] if selector else "").strip()[:40], found, body


def walk(root):
    root = pathlib.Path(root)
    if root.is_file():
        yield root
        return
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in CODE | STYLE:
            continue
        if SKIP & set(path.parts):
            continue
        yield path


def verdict(ratio):
    if ratio >= RATIO_CLEAR:
        return "clear"
    if ratio >= RATIO:
        return "ok"
    return "FAIL"


def report_pair(padding, gap):
    if gap <= 0:
        print("gap must be greater than 0")
        return 2
    ratio = padding / gap
    v = verdict(ratio)
    print(f"padding {padding:g}px  gap {gap:g}px  ratio {ratio:.2f}x  {v}")
    print(f"  padding-gap-ratio  >= {RATIO}x [convention], {RATIO_CLEAR}x reads more clearly")
    if v == "FAIL":
        print(f"  -> {gap * RATIO:g}px padding, or {gap * RATIO_CLEAR:g}px to be unambiguous")
        print("  exempt if this is full-bleed media, a dense table, or a container")
        print("  that already carries a border or its own background")
    off = [("padding", padding), ("gap", gap)]
    bad = [n for n, v2 in off if v2 % STEP_PX]
    if bad:
        print(f"  4pt-system: {', '.join(bad)} is off the 4px step")
    return 1 if v == "FAIL" else 0


def report_scan(root):
    root_px = 16.0
    fails, checked, values, files, unresolved = [], 0, {}, 0, 0
    for path in walk(root):
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        files += 1
        for line, label, found, body in scan_text(text, path.suffix, root_px):
            for _, value in found:
                values[value] = values.get(value, 0) + 1
            pairs = pairs_from(found, body)
            if pairs is None:
                unresolved += 1
                continue
            for axis, p, g in pairs:
                checked += 1
                ratio = p / g
                if ratio < RATIO:
                    fails.append((path, line, label, axis, p, g, ratio))

    if not files:
        print(f"no code or style files under {root}")
        return 2

    print(f"{files} files, {checked} padding/gap pairs on a known axis")
    if unresolved:
        print(f"{unresolved} skipped: padding and a gap, but no flex or grid on the")
        print("same element, so the gap separates nothing here\n")
    else:
        print()

    if values:
        scale = sorted(values, key=lambda v: -values[v])[:12]
        off = sorted(v for v in values if v % STEP_PX and v != 1)
        print("spacing scale, the 12 most used values in order")
        print("  " + "  ".join(f"{v:g}px" if v == int(v) else f"{v}px" for v in sorted(scale)))
        print(f"  {len(values)} distinct values")
        if off:
            shown = "  ".join(f"{v:g}px" for v in off[:8])
            print(f"  off the 4px step (4pt-system): {shown}"
                  + (f"  and {len(off) - 8} more" if len(off) > 8 else ""))
        print()

    if not checked:
        print("Nothing to check. Either spacing lives in tokens or component")
        print("variants rather than on the elements, or padding and gap are")
        print("never declared together, which this read cannot pair.")
        return 0

    if not fails:
        print(f"padding-gap-ratio: all {checked} pass (>= {RATIO}x) [convention]")
        return 0

    print(f"padding-gap-ratio: {len(fails)} of {checked} below {RATIO}x [convention]")
    print("Ordered by how many px of padding are missing, not by the ratio. A")
    print("badge at 2px against an 8px gap has the worse ratio; a card at 8px")
    print("against a 24px gap is the one you can see.\n")
    ranked = sorted(fails, key=lambda f: -(f[5] * RATIO - f[4]))
    for path, line, label, axis, p, g, ratio in ranked[:25]:
        short = g * RATIO - p
        print(f"  {path}:{line}")
        print(f"    {axis}-axis  padding {p:g}px  gap {g:g}px  ratio {ratio:.2f}x"
              f"  -> {g * RATIO:g}px, {short:g}px short")
        if label:
            print(f"    {label[:72]}")
    if len(fails) > 25:
        print(f"\n  and {len(fails) - 25} more")
    print("\nExempt by the rule's own terms: full-bleed media, dense tables, and")
    print("containers with a border or a distinct background. This read cannot")
    print("see which of those apply, so confirm before changing a value.")
    return 1


def main(argv):
    if len(argv) >= 2 and argv[0] == "--pair":
        try:
            return report_pair(float(argv[1]), float(argv[2]))
        except (IndexError, ValueError):
            print("usage: spacing.py --pair <padding-px> <gap-px>")
            return 2
    if not argv or argv[0].startswith("-"):
        print(__doc__.strip().split("\n\n")[1])
        return 2
    return report_scan(argv[0])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
