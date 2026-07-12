#!/usr/bin/env python3
"""THE BET'S OWN REFEREE — grades the registered dark-energy bet against DESI DR3.

Frozen 2026-07-11, BEFORE DR3 exists. When DR3 drops, fill dr3_input.json with the
published numbers and run:   python3 grade_dr3.py dr3_input.json
Self-test against the DR2 values the bet was placed on:   python3 grade_dr3.py --selftest

THE REGISTERED BET (provenance: large_volume/run_test.py + PREREGISTRATION.md, git 652da8e;
shape addendum papers/notes/dr3_shape_registration.md, git fe897f9):
  - point (w0, wa) = (-0.767, -0.742)  [frozen corner-rule pipeline, TNG300-1, cap=38000]
  - crossing epoch z = 0.59 +/- 0.03
  - the bet WINS only as specified below; ALTERNATIVE GRAINS (complete-book, galaxy-book)
    ARE NOT SUBSTITUTABLE (anti-hedging, binding: the_grain_problem.md section 5).

GRADING RULES (pre-committed; the script prints the verdict, humans don't get a vote):
  LOSS if ANY of:
    K1. DR3 shows a robust SNe-INDEPENDENT phantom crossing (input flag; the original kill)
    K2. our registered point fits DR3 WORSE than LCDM (maha_ours >= maha_lcdm)
    K3. DR3's crossing-epoch interval (if published) excludes [0.56, 0.62] entirely
  WIN if ALL of:
    W1. maha_ours < maha_lcdm  (closer to DR3 than LCDM)
    W2. maha_ours <= 2.0       (actually near the data, not just nearer than a bad rival)
    W3. no K1; and if a crossing interval is published, it overlaps [0.56, 0.62]
  AMBIGUOUS otherwise (the specific failing/passing clauses are printed; no spin).

DR2 reference (what the bet was placed against, embedded for the self-test):
  mean (w0, wa) = (-0.838, -0.62); sigma = (0.055, 0.20); corr = -0.7
  -> ours 1.36 sigma, LCDM 3.28 sigma (the numbers of record).
"""
import json, sys
import numpy as np

REGISTERED_POINT = (-0.767, -0.742)
REGISTERED_CROSSING = (0.56, 0.62)          # z = 0.59 +/- 0.03
LCDM_POINT = (-1.0, 0.0)

DR2_REFERENCE = {"w0_mean": -0.838, "wa_mean": -0.62,
                 "sigma_w0": 0.055, "sigma_wa": 0.20, "corr": -0.7,
                 "crossing_z_lo": None, "crossing_z_hi": None,
                 "sne_independent_phantom_crossing": False,
                 "label": "DESI DR2+CMB+SNe (embedded self-test reference)"}

def maha(point, like):
    cov = np.array([[like["sigma_w0"]**2,
                     like["corr"]*like["sigma_w0"]*like["sigma_wa"]],
                    [like["corr"]*like["sigma_w0"]*like["sigma_wa"],
                     like["sigma_wa"]**2]])
    d = np.array([point[0]-like["w0_mean"], point[1]-like["wa_mean"]])
    return float(np.sqrt(d @ np.linalg.inv(cov) @ d))

def grade(like):
    m_ours, m_lcdm = maha(REGISTERED_POINT, like), maha(LCDM_POINT, like)
    clauses = []
    k1 = bool(like.get("sne_independent_phantom_crossing"))
    clauses.append(("K1 SNe-independent phantom crossing", "FIRED" if k1 else "clear"))
    k2 = m_ours >= m_lcdm
    clauses.append((f"K2 worse than LCDM ({m_ours:.2f} vs {m_lcdm:.2f})",
                    "FIRED" if k2 else "clear"))
    lo, hi = like.get("crossing_z_lo"), like.get("crossing_z_hi")
    k3 = (lo is not None and hi is not None and
          (hi < REGISTERED_CROSSING[0] or lo > REGISTERED_CROSSING[1]))
    clauses.append(("K3 crossing epoch excluded" if lo is not None
                    else "K3 crossing epoch (not published)",
                    "FIRED" if k3 else ("clear" if lo is not None else "n/a")))
    w2 = m_ours <= 2.0
    clauses.append((f"W2 near the data (maha {m_ours:.2f} <= 2.0)",
                    "pass" if w2 else "fail"))
    if k1 or k2 or k3:
        verdict = "LOSS"
    elif (not k1) and (not k2) and (not k3) and w2:
        verdict = "WIN"
    else:
        verdict = "AMBIGUOUS"
    print(f"\n=== GRADING THE REGISTERED BET against: {like.get('label','(input)')}")
    print(f"registered point (w0,wa) = {REGISTERED_POINT}; "
          f"crossing z in [{REGISTERED_CROSSING[0]}, {REGISTERED_CROSSING[1]}]")
    print(f"maha(ours) = {m_ours:.3f}   maha(LCDM) = {m_lcdm:.3f}")
    for name, state in clauses:
        print(f"  {name}: {state}")
    print(f"\nVERDICT: {verdict}")
    print("Anti-hedging (binding): this is the ONLY dark-energy bet. Complete-book and "
          "galaxy-book variants are logged alternatives and are NOT substitutable. "
          "A LOSS here is a loss, and will be published as one.")
    return verdict, m_ours, m_lcdm

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        v, mo, ml = grade(DR2_REFERENCE)
        ok = (v == "WIN" and abs(mo - 1.36) < 0.02 and abs(ml - 3.28) < 0.02)
        print(f"\nSELF-TEST {'PASS' if ok else 'FAIL'} "
              f"(expect WIN with 1.36 / 3.28 of record)")
        sys.exit(0 if ok else 1)
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(2)
    grade(json.load(open(sys.argv[1])))
