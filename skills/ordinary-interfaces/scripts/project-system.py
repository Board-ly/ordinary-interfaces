#!/usr/bin/env python3
"""Read a project's existing design system before advising on it.

    project-system.py [path]        # default: current directory

Reports what the codebase already decided: token names, radius and spacing
scales, colour notation, type sizes, motion conventions, and which libraries are
in play, so a review can match the project instead of imposing generic values.

Also flags a few things that are findings regardless of the project's system:
`transition: all`, bare `:focus` with no `:focus-visible`, `outline: none`,
missing `prefers-reduced-motion`.

Reads only. No dependencies.
"""
import json
import os
import re
import sys
from collections import Counter

CODE_EXT = {'.css', '.scss', '.sass', '.less', '.js', '.jsx', '.ts', '.tsx',
            '.vue', '.svelte', '.astro', '.html'}
SKIP_DIR = {'node_modules', '.git', 'dist', 'build', '.next', 'out', 'vendor',
            '__pycache__', '.venv', 'venv', 'coverage', '.svelte-kit'}
MAX_FILES = 4000
MAX_BYTES = 2_000_000


def walk(root):
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR and not d.startswith('.')]
        for f in files:
            if os.path.splitext(f)[1].lower() in CODE_EXT:
                yield os.path.join(base, f)


def head(counter, n=12):
    return ', '.join(f'{k}' + (f' ({v}×)' if v > 1 else '')
                     for k, v in counter.most_common(n)) or 'none'


def section(title):
    print(f"\n{title}\n{'─' * len(title)}")


def main(root):
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        print(f"error: not a directory: {root}")
        return 2

    print(f"\n  Design system detected in {root}")

    # ---- libraries and config -------------------------------------------
    signals = []
    pkg_path = os.path.join(root, 'package.json')
    deps = {}
    if os.path.isfile(pkg_path):
        try:
            pkg = json.load(open(pkg_path, encoding='utf-8'))
            deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
        except Exception:
            pass
    known = {
        'tailwindcss': 'Tailwind', 'motion': 'Motion', 'framer-motion': 'Framer Motion',
        'lucide-react': 'Lucide icons', '@heroicons/react': 'Heroicons',
        'react-icons': 'react-icons', '@phosphor-icons/react': 'Phosphor',
        'sonner': 'Sonner', 'vaul': 'Vaul', 'next': 'Next.js', 'react': 'React',
        'vue': 'Vue', 'svelte': 'Svelte',
    }
    for dep, label in known.items():
        if dep in deps:
            signals.append(f'{label} ({deps[dep]})')
    for cfg, label in [('components.json', 'shadcn/ui (components.json)'),
                       ('tailwind.config.js', 'tailwind.config.js'),
                       ('tailwind.config.ts', 'tailwind.config.ts')]:
        if os.path.isfile(os.path.join(root, cfg)):
            signals.append(label)

    radix = sorted({d for d in deps if d.startswith('@radix-ui/')})
    if radix:
        signals.append(f'Radix ({len(radix)} packages)')

    section('Stack')
    print('  ' + ('\n  '.join(signals) if signals else 'nothing detected'))

    if os.path.isfile(os.path.join(root, 'components.json')):
        try:
            cj = json.load(open(os.path.join(root, 'components.json'), encoding='utf-8'))
            print(f"\n  components.json: style={cj.get('style')} "
                  f"baseColor={cj.get('tailwind', {}).get('baseColor')} "
                  f"cssVariables={cj.get('tailwind', {}).get('cssVariables')}")
            print("  → run `npx shadcn@latest info --json` for resolved paths "
                  "and installed components")
        except Exception:
            pass

    # ---- scan source -----------------------------------------------------
    tokens, radii, spacing, fontsize, notation = Counter(), Counter(), Counter(), Counter(), Counter()
    fonts, durations, easings, breakpoints = Counter(), Counter(), Counter(), Counter()
    findings = Counter()
    finding_files = {}
    scanned = 0

    for path in walk(root):
        if scanned >= MAX_FILES:
            break
        try:
            if os.path.getsize(path) > MAX_BYTES:
                continue
            text = open(path, encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        scanned += 1
        rel = os.path.relpath(path, root)

        tokens.update(re.findall(r'(--[a-zA-Z][\w-]*)\s*:', text))
        radii.update(re.findall(r'border-radius\s*:\s*([^;{}]+)', text))
        spacing.update(re.findall(r'(?:gap|padding|margin)\s*:\s*([0-9.]+(?:px|rem))\b', text))
        fontsize.update(re.findall(r'font-size\s*:\s*([0-9.]+(?:px|rem|em))', text))
        fonts.update(f.strip() for f in re.findall(r'font-family\s*:\s*([^;{}]+)', text))
        durations.update(re.findall(r'(?:transition-duration|duration)\s*:\s*(\d+m?s)', text))
        durations.update(re.findall(r'transition\s*:[^;{}]*?(\d+m?s)', text))
        easings.update(re.findall(r'(cubic-bezier\([^)]*\))', text))
        breakpoints.update(re.findall(r'@media[^{]*?\(\s*(?:min|max)-width\s*:\s*([0-9.]+(?:px|rem|em))', text))

        for name, pat in [('oklch', r'oklch\('), ('hsl', r'hsl\('),
                          ('rgb', r'rgba?\('), ('hex', r'#[0-9a-fA-F]{3,8}\b')]:
            n = len(re.findall(pat, text))
            if n:
                notation[name] += n

        for label, pat in [
            ('transition: all', r'transition:\s*all\b|\btransition-all\b'),
            ('outline: none', r'outline:\s*(?:none|0)\b'),
            ('!important', r'!important'),
            ('fixed height on text', r'\bheight:\s*\d+(?:px|rem)'),
        ]:
            n = len(re.findall(pat, text))
            if n:
                findings[label] += n
                finding_files.setdefault(label, set()).add(rel)

        if ':focus-visible' in text:
            findings['has :focus-visible'] += text.count(':focus-visible')
        if 'prefers-reduced-motion' in text:
            findings['has prefers-reduced-motion'] += text.count('prefers-reduced-motion')
        if 'tabular-nums' in text or 'tnum' in text:
            findings['has tabular-nums'] += 1

    section(f'Tokens  ({len(tokens)} custom properties across {scanned} files)')
    if tokens:
        groups = Counter()
        for t in tokens:
            groups[t.split('-')[2] if t.count('-') >= 2 else t.lstrip('-')] += 1
        print(f'  families: {head(groups, 14)}')
        print(f'  sample:   {", ".join(sorted(tokens)[:14])}')
    else:
        print('  none. Values are literal; introducing tokens is a real change, not a tidy-up.')

    section('Scales')
    print(f'  radius:      {head(radii, 8)}')
    print(f'  spacing:     {head(spacing, 10)}')
    print(f'  font-size:   {head(fontsize, 10)}')
    print(f'  breakpoints: {head(breakpoints, 8)}')
    print(f'  font-family: {head(fonts, 3)}')

    section('Colour notation')
    if notation:
        total = sum(notation.values())
        for k, v in notation.most_common():
            print(f'  {k:6} {v:5}  ({100 * v // total}%)')
        if len(notation) > 1:
            print(f'\n  → Mixed notation. Match the dominant one ({notation.most_common(1)[0][0]}).')
            print('    A consistent hex system beats hex with oklch() scattered through it.')
    else:
        print('  none found')

    section('Motion')
    print(f'  durations: {head(durations, 10)}')
    print(f'  curves:    {head(easings, 4)}')

    section('Flags')
    for label in ['has :focus-visible', 'has prefers-reduced-motion', 'has tabular-nums']:
        print(f"  {'✓' if findings.get(label) else '✗'} {label[4:]}")
    hard = {k: v for k, v in findings.items() if not k.startswith('has ')}
    if hard:
        print()
        for k, v in sorted(hard.items(), key=lambda kv: -kv[1]):
            files = sorted(finding_files.get(k, []))[:3]
            print(f'  {v:4}× {k:24} {", ".join(files)}'
                  f'{" …" if len(finding_files.get(k, [])) > 3 else ""}')

    print("""
  ─────────────────────────────────────────────────────────────────
  Use this before quoting any default. Where the project has a
  scale, match it. Where it has none, the reference values apply.
  A finding is "this breaks the project's own system" first, and
  "this differs from the reference" only second.
""")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '.'))
