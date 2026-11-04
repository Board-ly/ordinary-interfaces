#!/usr/bin/env python3
"""Everything CI checks, runnable locally. No dependencies, no writes left behind.

    python3 scripts/check.py          # report
    python3 scripts/check.py --fix    # regenerate the derived files in place

Checks:
  1. every script compiles
  2. RULE_INDEX.md matches the reference files it is generated from
  3. contrast.py still agrees with the two values WCAG margins hinge on
"""
import py_compile
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "ordinary-interfaces"
FIX = "--fix" in sys.argv
fails = []


def report(ok, label, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
    if not ok:
        fails.append(label)


print("compiles")
for script in sorted(ROOT.glob("**/*.py")):
    try:
        py_compile.compile(str(script), doraise=True, cfile=str(script) + "c")
        report(True, script.relative_to(ROOT).as_posix())
    except py_compile.PyCompileError as exc:
        report(False, script.relative_to(ROOT).as_posix(), str(exc).splitlines()[-1])
    finally:
        Path(str(script) + "c").unlink(missing_ok=True)

print("\nRULE_INDEX.md is current")
for generator, target in (
    (SKILL / "scripts" / "build-index.py", SKILL / "RULE_INDEX.md"),
):
    before = target.read_text()
    result = subprocess.run(
        [sys.executable, str(generator)], cwd=ROOT, capture_output=True, text=True
    )
    name = target.relative_to(ROOT).as_posix()
    if result.returncode != 0:
        report(False, name, f"{generator.name} exited {result.returncode}: {result.stderr.strip()}")
        continue
    after = target.read_text()
    if before == after:
        report(True, name, result.stdout.strip())
    elif FIX:
        report(True, name, "regenerated")
    else:
        target.write_text(before)
        report(False, name, f"stale, run `python3 {generator.relative_to(ROOT).as_posix()}`")

print("\ncontrast.py")
# #777777 on white computes to 4.478 and fails AA; #767676 computes to 4.542 and
# passes. One hex digit apart. contrast.py exits 1 when AA normal text fails, so
# both the verdict line and the exit code are checked here. The rule text in
# references/color.md quotes these two values, and a refactor that moved them
# would make that rule wrong.
for fg, ratio, expect_pass in (("#777777", "4.48", False), ("#767676", "4.54", True)):
    out = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "contrast.py"), fg, "#ffffff"],
        capture_output=True, text=True,
    )
    verdict = next(
        (line for line in out.stdout.splitlines() if "AA  normal text" in line), ""
    )
    ok = (
        f"ratio {ratio}:1" in out.stdout
        and verdict.strip().endswith("PASS" if expect_pass else "FAIL")
        and out.returncode == (0 if expect_pass else 1)
    )
    report(
        ok,
        f"{fg} on #ffffff {'passes' if expect_pass else 'fails'} AA normal text",
        verdict.strip() or out.stderr.strip(),
    )

print("\nspacing.py")
# padding-gap-ratio is >=1.5x, so 24px padding against a 16px gap is the exact
# boundary and must pass, while the 16/24 inversion must fail. references/
# spacing-layout.md quotes both ("a 16px gutter wants >=24px card padding"), so
# a change that moved the threshold would make that rule wrong. The exit code
# carries the verdict, as it does for contrast.py.
for padding, gap, expect_pass in ((24, 16, True), (16, 24, False), (32, 16, True)):
    out = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "spacing.py"), "--pair", str(padding), str(gap)],
        capture_output=True, text=True,
    )
    first = out.stdout.splitlines()[0] if out.stdout else out.stderr.strip()
    ok = out.returncode == (0 if expect_pass else 1) and (
        ("FAIL" not in first) if expect_pass else ("FAIL" in first)
    )
    report(ok, f"padding {padding}px against gap {gap}px "
               f"{'meets' if expect_pass else 'misses'} 1.5x", first)

# The axis rule: a gap on a flex row separates nothing vertically, so a tall
# container with a wide gap must not be reported on the y axis. This is what
# kept the check from flagging most of a real codebase.
probe = ROOT / "scripts" / ".spacing-probe.tsx"
probe.write_text('<div className="px-1 py-8 flex gap-6" />\n')
try:
    out = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "spacing.py"), str(probe)],
        capture_output=True, text=True,
    )
    report("x-axis" in out.stdout and "y-axis" not in out.stdout,
           "a flex row's gap is checked on x only",
           "1 pair on a known axis" if "y-axis" not in out.stdout else "y-axis reported")
finally:
    probe.unlink(missing_ok=True)

print()
if fails:
    print(f"{len(fails)} check(s) failed")
    sys.exit(1)
print("all checks passed")
