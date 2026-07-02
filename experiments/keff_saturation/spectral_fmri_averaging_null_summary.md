# ABIDE-fMRI averaging-null control — is region-level low-rank genuine?

Owed control for the CC200 region-level low-rank result. Reuses the same loaded
ROI×time data (139 controls, DX_GROUP==2; no re-download). k_eff := participation
ratio of the signed 200×200 correlation matrix (same definition as the prior
corridor read). Run `spectral_fmri_averaging_null.py`.

**Two nulls, both destroying cross-region coordination while preserving
per-region temporal structure:**
- `phase_rand` — per-region FFT phase-randomization (exact power spectrum, independent).
- `avg_null` — 200 independent AR(1) series matched to each region's lag-1
  autocorr + variance, same T. The "no-coordination brain": what averaging
  independent autocorrelated sources into 200 regions gives at finite T with
  ZERO coupling.

**Result (median [95% CI] across 139 controls):**

| quantity | median | 95% CI | p5–p95 |
|---|---|---|---|
| real k_eff | **8.02** | [7.24, 8.79] | [3.78, 15.80] |
| phase-randomized null | 41.16 | [39.41, 44.64] | [27.14, 64.95] |
| averaging (AR1) null | 35.25 | [31.69, 37.79] | [22.96, 56.10] |
| ratio phase/real | 5.16 | [4.88, 5.54] | — |
| **ratio avg-null/real** | **4.31** | [3.96, 4.67] | — |

**VERDICT: GENUINE cross-region coordination — NOT an averaging artifact.**
Real k_eff is ~4.3× lower than the averaging null (independent AR(1)-matched
sources at the same N=200, same T, same per-region autocorrelation). The null
already absorbs the coarse-graining + finite-T floor, and the real brain sits
far below it. **139/139 subjects** have real k_eff below BOTH nulls; the CI on
the ratio (lower bound 3.96) never approaches 1. If region-level low dimensionality
were a mechanical consequence of averaging into 200 regions, real ≈ null — it is
not.

**Corridor placement (bonus):** real k_eff median 8.02 sits inside the (2.3, 10)
corridor; 93/139 (67%) strictly in-band, off both poles (well below the null's
~35–41 chaos side and far above the k_eff→1 rigidity pole). The low-rank is
non-trivial: genuine, coordinated, and corridor-occupying.
