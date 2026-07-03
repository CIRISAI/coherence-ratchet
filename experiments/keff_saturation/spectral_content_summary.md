# Allen Brain Observatory -- MECHANISM test: does k_eff track the shared driver?

Question (tautology-vs-content crux): is neural effective dimensionality `k_eff` DRIVEN BY the dimensionality of the shared stimulus (a mechanistic LAW -> content), or INTRINSIC / invariant to it (near-tautological)?

**Design.** Within-recording: same neurons, same N, matched (contiguous) T, different stimulus blocks. The absolute k_eff of a cortex patch is grain-confounded, but the RELATIVE change across stimulus types on the SAME neurons is not -- the grain/subsample confound cancels. Driver dimensionality is the WELL-ESTABLISHED stimulus-type ORDERING (not a fragile estimate): spontaneous (0) < gratings (1) < natural scenes (2) < natural movies (3).

**Substrate.** Allen Brain Observatory 2-photon dF/F, mouse visual cortex (VISp/VISl/VISpm/VISal). 21 usable sessions (session-types A/B/C).

**Debiasing.** Raw PR of 2p dF/F is noise-inflated. Two debiased readouts: `eff_rank_dec` (PRIMARY, FAIR) = # correlation eigenvalues above the analytic Marchenko-Pastur white-noise edge AFTER temporally decorrelating each block to ~independent frames -- this removes the autocorrelation asymmetry (natural movies are far smoother than gratings, which otherwise inflates their noise floor and artefactually suppresses their rank). `eff_rank_surr` = # eigenvalues above a phase-randomized floor (autocorrelation-AWARE, reference). `k_eff_cov` = framework's raw covariance participation ratio (variance-weighted).

## Pooled k_eff by stimulus type

| rank | stimulus | n | eff_rank_dec (FAIR) | eff_rank_surr | k_eff_cov (raw PR) |
|------|----------|---|---------------------|---------------|--------------------|
| 0 | spontaneous | 21 | 6.5 +/- 3.1 | 5.6 | 19.6 |
| 1 | drifting_gratings | 21 | 7.0 +/- 3.1 | 7.0 | 13.6 |
| 3 | natural_movie_one | 21 | 6.4 +/- 3.1 | 4.8 | 16.7 |
| 3 | natural_movie_three | 21 | 6.1 +/- 2.8 | 5.9 | 18.3 |

## The test

- **Stimulus-type ordinal Spearman** (stim-dim rank vs mean metric):
    - eff_rank_dec (FAIR): rho = **-0.738** (p=0.262)
    - eff_rank_surr        : rho = -0.211
    - k_eff_cov (raw PR)   : rho = -0.316
- **Within-session Spearman** (each recording its own control):
    - eff_rank_dec (FAIR): mean **-0.255** +/- 0.588 (n=21); frac>0 = 0.33
    - k_eff_cov          : mean +0.206 +/- 0.688; frac>0 = 0.62

### Paired grain-cancelling contrasts (FAIR eff_rank_dec, same neurons)

| contrast | n | hi | lo | delta | frac +Delta | Wilcoxon p |
|----------|---|----|----|-------|-------------|------------|
| natural_vs_gratings | 21 | 6.3 | 7.0 | -0.8 | 0.19 | 0.0123 |
| natural_vs_spont | 21 | 6.3 | 6.5 | -0.2 | 0.33 | 0.418 |
| gratings_vs_spont | 21 | 7.0 | 6.5 | +0.5 | 0.43 | 0.207 |

## VERDICT: MIXED

debiased rank ordinal rho=-0.74, raw k_eff_cov rho=-0.32: partial / metric-dependent driver-tracking.
