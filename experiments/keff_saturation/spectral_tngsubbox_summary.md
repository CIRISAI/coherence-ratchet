# TNG50-1-Subbox1 baryon cycle — PROPERLY-POWERED (T=43, 1.63 Gyr)

Update of the earlier T=14/0.44-Gyr result (too short — span, not cadence, was the limiter). Server recovered; rebuilt to T=43 (~1 baryon-cycle period). Gas PartType0, Eulerian disk-aligned 8^3 grid + 12 shells, logrho/logT/v_r, cells x snapshots.

## Saturation: LOW-RANK (robust)
logrho k_eff=4.52 (beta=0.080), logT 3.16, v_r 2.83. Same low-rank result as every prior galaxy/gas test.

## Detailed balance: DB-SATISFYING (bound) — no sustained coordinating cycle
Direct (logrho,logT) circulation vs phase-randomized null (robust at small T; the block-bootstrap winding degenerates here and is not used). Estimator validated at T=43: equilibrium z=-1.34, driven z=2.26.
- per-cell z: mean 0.46, 2% of 410 cells significant → null
- global mean-state z = 0.47 → null

The T=14 marginal per-cell signal (−2.28) resolved to NULL once the span doubled to ~1 cycle period. No sustained thermodynamic loop.

## Verdict
The galaxy's gas baryon cycle is LOW-RANK and DETAILED-BALANCE-SATISFYING (bound), no sustained coordinating cycle over ~1 Gyr.

## Caveats
- span 1.63 Gyr ~ several baryon-cycle periods (maximally-powered: 43 clean of the T=50 build; supersedes the T=14/0.44 Gyr and T=28/0.94 Gyr passes -- verdict unchanged across all three)
- estimator dynamic range is MODEST even here (driven calibrator z=2.26, separation from equilibrium ~3.6): it detects a STRONG sustained cycle; a WEAK one (z~1-2) could hide. Real gas z~0.47 sits well below driven, closer to equilibrium.
- TNG gas has cooling+feedback by construction -> some irreversibility guaranteed; we find NO net circulation (one-way/transient dissipation, not a sustained homeostatic loop)
- one galaxy, one subbox; simulation-physics dissipation is NOT the framework's gamma*M maintenance term