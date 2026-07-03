# TNG50-1-Subbox1 baryon cycle — PROPERLY-POWERED (T=28, 0.94 Gyr)

Update of the earlier T=14/0.44-Gyr result (too short — span, not cadence, was the limiter). Server recovered; rebuilt to T=28 (~1 baryon-cycle period). Gas PartType0, Eulerian disk-aligned 8^3 grid + 12 shells, logrho/logT/v_r, cells x snapshots.

## Saturation: LOW-RANK (robust)
logrho k_eff=3.73 (beta=0.074), logT 2.42, v_r 2.47. Same low-rank result as every prior galaxy/gas test.

## Detailed balance: DB-SATISFYING (bound) — no sustained coordinating cycle
Direct (logrho,logT) circulation vs phase-randomized null (robust at small T; the block-bootstrap winding degenerates here and is not used). Estimator validated at T=28: equilibrium z=0.10, driven z=1.96.
- per-cell z: mean 0.27, 0% of 410 cells significant → null
- global mean-state z = -0.01 → null

The T=14 marginal per-cell signal (−2.28) resolved to NULL once the span doubled to ~1 cycle period. No sustained thermodynamic loop.

## Verdict
The galaxy's gas baryon cycle is LOW-RANK and DETAILED-BALANCE-SATISFYING (bound), no sustained coordinating cycle over ~1 Gyr.

## Caveats
- span 0.94 Gyr ~ 1 baryon-cycle period (better than the T=14/0.44 Gyr; full T=50/~1.65 Gyr = several periods would strengthen)
- estimator dynamic range modest at T=28 (driven calibrator z~2.2): detects a strong cycle, a very weak one could hide
- TNG gas has cooling+feedback by construction -> some irreversibility guaranteed; we find NO net circulation (one-way/transient dissipation, not a sustained loop)
- one galaxy, one subbox; simulation-physics dissipation is NOT the framework's gamma*M maintenance term