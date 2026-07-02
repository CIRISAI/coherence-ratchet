# Allen Brain Observatory -- spectral criticality-vs-low-rank verdict

Substrate: mouse visual cortex (VISp/VISl/VISpm/VISal), 2-photon dF/F, spontaneous grey-screen epoch. Real Allen NWB, 21 sessions. N in [21, 240] (median 152), T ~ 8931 frames.

- **k_eff (PR of covariance)**: median **11.7** (range 2.7-59.1) -- the specific owed quantity.
- **Effective rank vs MP edge**: median 11 (surrogate MP rank median 9).
- **Effective rank vs surrogate floor**: median 5 (range 2-27).
- **beta (PR-subsampling exponent)**: mean **0.836** +/- 0.141, 95% CI [0.769, 0.903] (n=17).
- Calibration at N=200: low-rank beta=0.032, power-law(1.0)=0.174, power-law(0.6)=0.584, noise=0.986.

## VERDICT: INCONCLUSIVE

beta CI straddles regime boundaries.
