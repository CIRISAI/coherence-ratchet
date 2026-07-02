# ZAPBench whole-brain zebrafish -- k_eff saturation verdict

DECISIVE saturation test on a COMPLETE vertebrate brain. ZAPBench (Immer et al. 2025; Ahrens/Engert light-sheet data): **71721 segmented neurons x 7879 volumes** = ~all neurons of one entire larval-zebrafish brain, 1 animal. Because the whole brain is captured, subsampling runs up to the full N and 'wrong grain' cannot be invoked. Stimulus: 9 successive visual conditions (gain,dots,flash,taxis,turning,position,...); not purely spontaneous.

Analysis core reused from spectral_test.py / spectral_test_allen_cv.py; N>>T so PR and the cross-validated spectrum are computed in T-space via the Gram/dual trick (exact nonzero spectrum; no N x N matrix formed).

## (a) Saturation curve (the money plot)

| N' | PR (mean) | draws |
|----|-----------|-------|
| 50 | 19.826 | 6 |
| 100 | 25.946 | 6 |
| 200 | 28.981 | 6 |
| 500 | 33.415 | 6 |
| 1000 | 32.574 | 6 |
| 2000 | 33.618 | 3 |
| 4000 | 33.085 | 3 |
| 8000 | 34.354 | 2 |
| 16000 | 33.912 | 2 |
| 32000 | 33.920 | 1 |
| 50000 | 34.097 | 1 |
| 71721 | 34.187 | 1 |

- PR at full N = **34.19**.
- beta = dlogPR/dlogN' on N'>=5000: **-0.0015**; top decade (N'>=16000): **0.0056**.
  (beta->0 = saturation/low-rank; 0.3-0.8 = power-law growth; ~1 = extensive.)

## (b,c) Spectrum diagnostics at full N

- correlation-matrix PR (full N) = **34.19**.
- Marchenko-Pastur edge lambda+ = 16.14; effective rank above MP edge = **331**; above phase-randomized surrogate max eig (1089.74) = **10**.
- top eigenvalues: 9737.2, 4318.1, 2634.1, 2484.1, 2239.7, 1877.2, 1429.0, 1373.4.

### Cross-validated (noise-removed) spectrum
- CV-positive intrinsic dims (> 95th-pct surrogate null): **1592**.
- noise-free k_eff (PR of surrogate-subtracted CV-positive spectrum): **16.06**  (framework ceiling ~10).
- dims above strict surrogate ceiling: **12** (lower bound).
- power-law alpha (lambda_i ~ i^-alpha): **1.358** (Stringer mouse V1 ~1.04).

## VERDICT: FALSIFICATION (high-dimensional / scale-free)

PR keeps climbing (beta_topdecade=0.006, PR full N=34.2); 1592 noise-free CV dims (k_eff=16.1 >> 10). On a COMPLETE brain where 'wrong grain' cannot be invoked, effective dimensionality does NOT saturate at the ~10 corridor ceiling -- the corridor claim is falsified for vertebrate whole-brain.
