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

print()
if fails:
    print(f"{len(fails)} check(s) failed")
    sys.exit(1)
print("all checks passed")
