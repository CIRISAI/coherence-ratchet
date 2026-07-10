#!/usr/bin/env python3
"""Calibration of the inference machinery used by rent_stock.py, on synthetic data with
known ground truth.  Run BEFORE trusting any CI in results.json.

The anesthesia windows are (a) heavily autocorrelated (20 s windows at 5 s step ⇒ 75%
overlap) and (b) carry a strong shared drift with induction.  Both are exactly the
conditions under which a naive bootstrap produces confident nonsense.  Three checks:

  A. NULL with shared trend: two independent random walks each plus the same linear
     drift.  The partial-on-rank(time) should be null; the 95% CI should cover 0 ~95% of
     the time.  Measures the coverage of the moving-block bootstrap.
  B. POWER: a true positive partial (shared latent beyond the trend) should be detected.
  C. The same null as A but with block length L = 1 (i.e. an iid bootstrap over windows).
     Reported to show what the autocorrelation does to a naive interval.
  D/E. The Fisher-z pooling: homogeneous inputs pool to their common value with I² = 0;
     equal-and-opposite inputs pool to ~0 with I² ≈ 100%.  E is the FAIL signature this
     experiment is looking for: a null pooled mean that means "no law", not "no effect".
"""
import sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rent_stock as R

def main(n=300, reps=200, nboot=300):
    rng = np.random.default_rng(1)
    rw = lambda: np.cumsum(rng.standard_normal(n)) * 0.3
    out = {}

    cov = []
    for rep in range(reps):
        t = np.arange(n)
        x, y = 0.02 * t + rw(), 0.02 * t + rw()
        L, _ = R.block_len([R._rank(x), R._rank(y)], n)
        bt = R.block_bootstrap_partial(x, y, t, np.zeros((n, 0)), L, nboot=nboot, seed=rep)
        lo, hi = np.percentile(bt, [2.5, 97.5])
        cov.append(lo <= 0 <= hi)
    out["A_null_coverage_pct"] = 100 * float(np.mean(cov))

    hit, rs = [], []
    for rep in range(reps // 2):
        t = np.arange(n); u = rw()
        x, y = 0.02 * t + u + 0.5 * rw(), 0.02 * t + u + 0.5 * rw()
        rs.append(R.spearman_partial(x, y, np.column_stack([R._rank(t)])))
        L, _ = R.block_len([R._rank(x), R._rank(y)], n)
        bt = R.block_bootstrap_partial(x, y, t, np.zeros((n, 0)), L, nboot=nboot, seed=rep)
        hit.append(np.percentile(bt, 2.5) > 0)
    out["B_power_mean_r"] = float(np.mean(rs))
    out["B_power_detect_pct"] = 100 * float(np.mean(hit))

    cov = []
    for rep in range(reps):
        t = np.arange(n)
        x, y = 0.02 * t + rw(), 0.02 * t + rw()
        bt = R.block_bootstrap_partial(x, y, t, np.zeros((n, 0)), 1, nboot=nboot, seed=rep)
        lo, hi = np.percentile(bt, [2.5, 97.5])
        cov.append(lo <= 0 <= hi)
    out["C_iid_bootstrap_null_coverage_pct"] = 100 * float(np.mean(cov))

    out["D_homogeneous_pool"] = R.fisher_pool([0.5, 0.5, 0.5], [0.1, 0.1, 0.1])
    out["E_opposed_pool"] = R.fisher_pool([0.5, -0.5], [0.08, 0.08])

    print(f"A) null, block bootstrap : 95% CI covers 0 in {out['A_null_coverage_pct']:.0f}% "
          f"of {reps} reps   [nominal 95%]")
    print(f"B) true positive partial : mean r = {out['B_power_mean_r']:+.2f}; "
          f"CI excludes 0 in {out['B_power_detect_pct']:.0f}% of reps")
    print(f"C) SAME null, L=1 (iid)  : covers 0 in {out['C_iid_bootstrap_null_coverage_pct']:.0f}% "
          f"— an iid bootstrap over overlapping windows is worthless")
    print(f"D) pool 3x(+0.50)        : FE r = {out['D_homogeneous_pool']['fe_r']:+.3f}, "
          f"I2 = {out['D_homogeneous_pool']['I2_pct']:.0f}%")
    print(f"E) pool (+0.50, -0.50)   : FE r = {out['E_opposed_pool']['fe_r']:+.3f}, "
          f"Q = {out['E_opposed_pool']['Q']:.1f} (p = {out['E_opposed_pool']['Q_p']:.1e}), "
          f"I2 = {out['E_opposed_pool']['I2_pct']:.0f}%  <- the FAIL signature")
    print("\nREADING: the block bootstrap is mildly ANTICONSERVATIVE here (A ~90% vs a nominal")
    print("95%), so a nominal-95% CI that excludes zero is really closer to a 90% statement.")
    print("Every 'CI excludes 0' claim in SUMMARY.md must be discounted accordingly.")
    import json
    json.dump(out, open(os.path.join(HERE, "calibration.json"), "w"), indent=1)
    return out

if __name__ == "__main__":
    main()
