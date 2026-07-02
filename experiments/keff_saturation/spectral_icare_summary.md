# Spectral discriminator — iCARE comatose EEG

**Substrate:** PhysioNet iCARE post-cardiac-arrest comatose scalp EEG (WFDB int16 `.mat`).
**Ran:** 9 of 10 recordings on disk (1 subject/recording each). 0432 excluded — its
mid-segment is isoelectric (suppressed EEG), all channels flat after filtering.
**N:** 18–20 scalp electrodes (small → effective rank is primary, β secondary).
**T/rate/prep:** contiguous 120 s mid-segment at native rate (250/256/500 Hz); per-channel
demean; 4th-order Butterworth 1–40 Hz band-pass; flat/reference channels (e.g. Fpz) dropped.
Synthetics calibrate the estimator only (at N=19: low-rank r=3 β≈0.18, power-law β 0.54–0.77,
noise β≈1.0).

| readout | value |
|---|---|
| median effective rank (spikes > phase-surrogate floor) | **3.0** (range 1–4) |
| mean β (PR subsample exponent) | **0.154**, 95% CI **[0.124, 0.185]**, n=9 |

**VERDICT: LOW-RANK.** A few (2–4) dominant collective modes ride over a flat Marchenko–Pastur
noise bulk; PR is tiny (1.8–5.7) and the subsampling exponent (0.15) sits at/below the low-rank
synthetic and far below the power-law band — no scale-free spectrum.

**Interpretation:** comatose EEG coordination is **low-rank, not critical and not noise-like**.
Even in a degraded/injured cohort a small, size-independent set of shared modes persists — the
control did NOT collapse to chaos. (Individual suppressed segments, e.g. 0432, do go isoelectric.)
