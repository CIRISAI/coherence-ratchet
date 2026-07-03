# ZAPBench zebrafish -- MECHANISM test: does k_eff track the shared driver?

Question (tautology-vs-content crux): is neural effective dimensionality `k_eff` BOUNDED by the dimensionality of the shared driver (the stimulus) -- the Gao-Ganguli 'dimensionality is task-complexity-bounded' mechanism (=> saturation is a mechanistic LAW, content) -- or is the low-rank INTRINSIC and unrelated to the driver (=> 'coordinating units saturate' is near-tautological)?

**Substrate.** ZAPBench whole-brain larval zebrafish (Immer et al. 2025; Ahrens/Engert), 71,721 neurons x 7,879 volumes, one complete brain, 9 successive visual conditions.

**Shared driver.** ZAPBench `stimuli_features` [7879 x 26]: the experimental stimulus regressors. `driver_dim` = participation ratio of the active-feature covariance within each condition. **Caveat:** these are coarse stimulus *parameters* (1-4 per condition; mostly binary/ternary), a LOWER bound on true perceptual richness (e.g. random-dot motion is one gain regressor here).

**Neural k_eff** = noise-free block-interleaved cross-validated participation ratio at full N (framework's own readout).

## Per-condition

| cond | T | active feats | driver_dim (PR) | neural PR | neural k_eff | stim-locked var frac | residual k_eff (driver projected out) |
|------|---|--------------|-----------------|-----------|--------------|----------------------|----------------------------------------|
| gain | 647 | 1 | 1.00 | 11.6 | 7.57 | 0.146 | 9.52 |
| dots | 1771 | 1 | 1.00 | 46.6 | 17.36 | 0.006 | 17.88 |
| flash | 654 | 1 | 1.00 | 25.8 | 11.06 | 0.100 | 11.71 |
| taxis | 655 | 2 | 1.99 | 29.9 | 10.93 | 0.084 | 11.28 |
| turning | 1310 | 3 | 2.00 | 18.4 | 5.88 | 0.250 | 11.67 |
| position | 589 | 4 | 1.35 | 28.7 | 10.06 | 0.064 | 12.54 |
| cond6 (SPONTANEOUS) | 983 | 0 | 0.00 | 17.4 | 8.64 | -0.000 | 8.64 |
| cond7 | 654 | 1 | 1.00 | 18.9 | 8.85 | 0.137 | 8.12 |
| cond8 (SPONTANEOUS) | 598 | 0 | 0.00 | 14.9 | 8.39 | 0.000 | 8.39 |

## Cross-condition (n=9)

- Pearson r(neural k_eff, driver_dim) = **-0.009**.
- Pearson r(neural k_eff, n_active_feats) = **-0.104**.
- driver_dim range 0.00-2.00; neural k_eff range 5.88-17.36.
- median neural k_eff / driver_dim ratio (driven conditions) = **7.6x**.
- STIMULUS conditions mean k_eff = **10.24**; SPONTANEOUS (cond6, cond8) mean k_eff = **8.52**.
- mean stimulus-locked variance fraction = **0.087** (fraction of neural variance the stimulus subspace, with lags, explains).

## VERDICT: NOT driver-bound (near-tautological / intrinsic): neural k_eff does NOT track the measured shared-driver dimensionality.
