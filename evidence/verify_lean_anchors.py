#!/usr/bin/env python3
"""
Verify the `lean:` tier of the CC evidence registry (evidence/cc_lean.tsv).

For every row marked `mechanized`, this resolves the anchor THROUGH LEAN
(`#print axioms <lean_name>`), which gives three guarantees a grep cannot:

  1. RESOLUTION  — an anchor that no longer exists is an `unknown identifier`
                   error, so a renamed/deleted theorem fails the build.
  2. NO `sorry`  — a theorem depending on `sorryAx` is reported and fails.
                   ("mechanized" must never mean "stated with sorry".)
  3. AXIOM AUDIT — the axioms each anchor actually depends on are printed, so
                   framework primitives (e.g. λ_geo, κ, corridorBounds, α/γ/M)
                   are surfaced rather than hidden behind the word "mechanized".

Also warns on STALE-OPEN drift: a row marked `open` whose anchor nonetheless
resolves and is sorry-free (the registry is understating what the lake proves).

Exit 0 iff every mechanized in-lake anchor resolves and is sorry-free.
Usage:  python3 evidence/verify_lean_anchors.py [--tsv PATH] [--lake PATH]
"""
from __future__ import annotations
import argparse
import csv
import pathlib
import re
import subprocess
import sys
import tempfile

# Axioms Mathlib itself is built on; not framework commitments.
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
SKIP_PREFIXES = ("RATCHET:",)
SKIP_LITERALS = {"", "—", "-"}


def in_lake(lean_name: str) -> bool:
    return bool(lean_name) and lean_name not in SKIP_LITERALS \
        and not lean_name.startswith(SKIP_PREFIXES)


def read_rows(tsv: pathlib.Path) -> list[dict]:
    with tsv.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def run_lean(lake_dir: pathlib.Path, names: list[str]) -> tuple[int, str]:
    """#print axioms each name against the built lake. Returns (rc, output)."""
    src = "import CoherenceRatchet\n" + "".join(f"#print axioms {n}\n" for n in names)
    with tempfile.NamedTemporaryFile("w", suffix=".lean", dir=lake_dir,
                                     delete=False, encoding="utf-8") as fh:
        fh.write(src)
        tmp = pathlib.Path(fh.name)
    try:
        proc = subprocess.run(
            ["lake", "env", "lean", tmp.name],
            cwd=lake_dir, capture_output=True, text=True, timeout=1800,
        )
        return proc.returncode, proc.stdout + proc.stderr
    finally:
        tmp.unlink(missing_ok=True)


# NOTE: Lean wraps long axiom lists across newlines, so the bracket body must be
# matched with a negated class (which spans newlines), not `.*` (which does not).
AXIOM_RE = re.compile(r"'(?P<name>[^']+)' depends on axioms: \[(?P<axioms>[^\]]*)\]")
NOAXIOM_RE = re.compile(r"'(?P<name>[^']+)' does not depend on any axioms", re.M)


def parse(output: str) -> dict[str, set[str]]:
    """lean_name -> set of axioms it depends on (empty set = none)."""
    found: dict[str, set[str]] = {}
    for m in NOAXIOM_RE.finditer(output):
        found[m.group("name")] = set()
    for m in AXIOM_RE.finditer(output):
        ax = {a.strip() for a in m.group("axioms").split(",") if a.strip()}
        found[m.group("name")] = ax
    return found


def self_test(lake_dir: pathlib.Path) -> bool:
    """Prove the trap fires. A green check that cannot go red is worthless, and the
    lake is currently sorry-free, so we synthesise both failure modes through REAL
    Lean: (a) a theorem proved by `sorry` must be seen to depend on `sorryAx`;
    (b) an unknown identifier must fail to resolve."""
    src = (
        "import CoherenceRatchet\n"
        "theorem _cr_probe_sorry : (1 : ℝ) = 1 := by sorry\n"
        "#print axioms _cr_probe_sorry\n"
        "#print axioms _cr_probe_absent_identifier\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".lean", dir=lake_dir,
                                     delete=False, encoding="utf-8") as fh:
        fh.write(src)
        tmp = pathlib.Path(fh.name)
    try:
        proc = subprocess.run(["lake", "env", "lean", tmp.name], cwd=lake_dir,
                              capture_output=True, text=True, timeout=1800)
        out = proc.stdout + proc.stderr
    finally:
        tmp.unlink(missing_ok=True)

    resolved = parse(out)
    ok = True
    probe = resolved.get("_cr_probe_sorry")
    if probe is None or not any("sorryAx" in a for a in probe):
        print("SELF-TEST FAIL: a `sorry` theorem was NOT detected as sorryAx-dependent",
              file=sys.stderr)
        ok = False
    if "_cr_probe_absent_identifier" in resolved:
        print("SELF-TEST FAIL: an unknown identifier was reported as resolved",
              file=sys.stderr)
        ok = False
    print("self-test: sorryAx trap fires; unknown identifiers do not resolve." if ok
          else "self-test: BROKEN", file=sys.stderr if not ok else sys.stdout)
    return ok


def main() -> int:
    here = pathlib.Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", type=pathlib.Path, default=here / "cc_lean.tsv")
    ap.add_argument("--lake", type=pathlib.Path, default=here.parent / "formal")
    ap.add_argument("--self-test", action="store_true",
                    help="verify the sorryAx/unresolved traps actually fire, then exit")
    args = ap.parse_args()

    if args.self_test:
        return 0 if self_test(args.lake) else 1

    rows = read_rows(args.tsv)
    mech = [r for r in rows if r["status"] == "mechanized" and in_lake(r["lean_name"])]
    opens = [r for r in rows if r["status"] == "open" and in_lake(r["lean_name"])]

    if not mech:
        print("no mechanized in-lake anchors to verify", file=sys.stderr)
        return 1

    names = [r["lean_name"] for r in mech] + [r["lean_name"] for r in opens]
    print(f"resolving {len(names)} anchor(s) through Lean in {args.lake} …\n")
    rc, out = run_lean(args.lake, names)
    resolved = parse(out)

    failures: list[str] = []
    framework_axioms: dict[str, set[str]] = {}

    for r in mech:
        name, cc = r["lean_name"], f"{r['cc_decimal_id']} {r['cc_claim_id']}"
        if name not in resolved:
            failures.append(f"UNRESOLVED  {cc}  {name}  (renamed/deleted, or module not imported)")
            continue
        axioms = resolved[name]
        if any("sorryAx" in a for a in axioms):
            failures.append(f"SORRY       {cc}  {name}  depends on sorryAx — not mechanized")
            continue
        extra = axioms - STANDARD_AXIOMS
        if extra:
            framework_axioms[name] = extra
        print(f"ok    {cc:28s} {name}")

    # STALE-OPEN: registry says open, but the lake actually proves it (warning only).
    stale = [r for r in opens
             if r["lean_name"] in resolved
             and not any("sorryAx" in a for a in resolved[r["lean_name"]])]
    for r in stale:
        print(f"WARN  stale-open: {r['cc_decimal_id']} {r['cc_claim_id']} "
              f"-> {r['lean_name']} resolves and is sorry-free; registry understates it")

    if framework_axioms:
        print("\nframework-primitive axiom dependencies (surfaced, not failures):")
        for name, ax in sorted(framework_axioms.items()):
            print(f"  {name}\n      {', '.join(sorted(ax))}")

    print()
    if failures:
        for f in failures:
            print(f, file=sys.stderr)
        print(f"\nFAIL: {len(failures)}/{len(mech)} mechanized anchor(s) did not verify.",
              file=sys.stderr)
        if rc != 0:
            tail = "\n".join(l for l in out.splitlines() if "error" in l.lower())[:2000]
            if tail:
                print("\nlean errors:\n" + tail, file=sys.stderr)
        return 1

    if rc != 0:
        print("lean exited nonzero despite all anchors resolving:\n" + out[:2000], file=sys.stderr)
        return 1

    print(f"PASS: all {len(mech)} mechanized anchors resolve, none depend on sorryAx.")
    if stale:
        print(f"({len(stale)} stale-open row(s) — update the registry.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
