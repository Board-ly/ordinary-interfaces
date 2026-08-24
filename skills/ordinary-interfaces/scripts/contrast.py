#!/usr/bin/env python3
"""WCAG 2.2 contrast ratio checker.

    contrast.py "#777777" "#ffffff"           ratio + AA/AAA verdicts
    contrast.py "#2066df" "#121212" --large   judge as large text
    contrast.py "#a5a8f0" "#ffffff" --fix     nearest passing foreground

Ratio is (L1 + 0.05) / (L2 + 0.05) on relative luminance, with sRGB
linearized first per WCAG 2.2. No dependencies.

Caveat this tool cannot see: it compares two flat colors. Gradients must be
measured at their worst point, and overlays or opacity must be resolved to a
rendered value before checking. See references/color.md -> wcag-contrast.
"""
import sys

AA_NORMAL, AA_LARGE, AAA_NORMAL, AAA_LARGE, UI = 4.5, 3.0, 7.0, 4.5, 3.0


def parse_hex(s):
    s = s.strip().lstrip('#')
    if len(s) == 3:
        s = ''.join(c * 2 for c in s)
    if len(s) != 6 or any(c not in '0123456789abcdefABCDEF' for c in s):
        raise ValueError(f"not a hex color: {s!r}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def to_hex(rgb):
    return '#%02x%02x%02x' % tuple(max(0, min(255, round(c))) for c in rgb)


def luminance(rgb):
    """Relative luminance Y, sRGB linearized per WCAG 2.2."""
    chan = []
    for c in rgb:
        c = c / 255
        chan.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = chan
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    a, b = luminance(fg), luminance(bg)
    lo, hi = sorted((a, b))
    return (hi + 0.05) / (lo + 0.05)


def scale(rgb, factor):
    """Scale toward black (<1) or white (>1), keeping hue and saturation."""
    if factor <= 1:
        return tuple(c * factor for c in rgb)
    return tuple(c + (255 - c) * (factor - 1) for c in rgb)


def nearest_passing(fg, bg, target):
    """Walk the foreground darker or lighter until the ROUNDED color clears
    `target`. Rounding matters: a float that passes can round to a hex that
    does not, so every candidate is checked after quantizing to 8-bit."""
    best = None
    for direction in (-1, 1):  # -1 darken, +1 lighten
        for step in range(1, 1001):
            factor = 1 - step / 1000 if direction < 0 else 1 + step / 1000
            cand = parse_hex(to_hex(scale(fg, factor)))
            if ratio(cand, bg) >= target:
                delta = sum(abs(a - b) for a, b in zip(cand, fg))
                if best is None or delta < best[0]:
                    best = (delta, cand)
                break
    return best[1] if best else None


def verdict(r, threshold):
    return 'PASS' if r >= threshold else 'FAIL'


def main(argv):
    args = [a for a in argv if not a.startswith('--')]
    flags = {a for a in argv if a.startswith('--')}
    if len(args) != 2:
        print(__doc__)
        return 2
    try:
        fg, bg = parse_hex(args[0]), parse_hex(args[1])
    except ValueError as e:
        print(f"error: {e}")
        return 2

    r = ratio(fg, bg)
    large = '--large' in flags

    print(f"\n  {to_hex(fg)} on {to_hex(bg)}   ratio {r:.2f}:1\n")
    rows = [
        ("AA  normal text  (>=4.5:1)", AA_NORMAL),
        ("AA  large text   (>=3:1)  ", AA_LARGE),
        ("AA  UI component (>=3:1)  ", UI),
        ("AAA normal text  (>=7:1)  ", AAA_NORMAL),
        ("AAA large text   (>=4.5:1)", AAA_LARGE),
    ]
    for label, threshold in rows:
        print(f"    {label}   {verdict(r, threshold)}")
    print("\n  Large text = >=24px regular or >=18.66px bold.")

    target = AA_LARGE if large else AA_NORMAL
    if '--fix' in flags:
        if r >= target:
            print(f"  Already passes {target}:1, no change needed.\n")
        else:
            fixed = nearest_passing(fg, bg, target)
            if fixed is None:
                print(f"  No adjustment of this hue reaches {target}:1 on "
                      f"{to_hex(bg)}. Change the background instead.\n")
            else:
                print(f"  Nearest passing foreground for {target}:1: "
                      f"{to_hex(fixed)} ({ratio(fixed, bg):.2f}:1)\n")
    elif r < target:
        print(f"  Below the {target}:1 floor. Re-run with --fix for a "
              f"nearest passing value.\n")
    else:
        print()
    return 0 if r >= target else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
