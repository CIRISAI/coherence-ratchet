# Robust re-run — Drosophila CX neural in-corridor substrate — RESULTS

**Date:** 2026-05-21. **Verdict: PASS.** v1's Drosophila central-complex
in-corridor finding **reproduces** under the structural-series robust framing
(debiased rho + canonical participation-ratio k_eff). v1's claim stands.

See `PREREGISTRATION.md` (committed before this ran) for protocol, datasets,
estimator, and pre-registered PASS/FAIL thresholds. Computation:
`recompute_robust.py`. Per-recording results: `results.json`.

## Datasets used (real data, located on disk)

| Dataset | Rung(s) | ROIs | Recordings | Design |
|---|---|---|---|---|
| Mussells Pires 2024 (v18) | EPG (`pb_c1`) | 16 | 16 (9 flies) | between-fly |
| Mussells Pires 2024 (v18) | FC2 (`fb_c1`) | 16 | 27 (15 flies) | between-fly |
| Ishida et al 2025 (v19) | EPG (`eb_c1`) | 16 | 7 same-fly | dual-color |
| Ishida et al 2025 (v19) | FC3 (`fb2_c1`+`fb5_c1`) | 32 | 7 same-fly | dual-color |

Total 57 (recording x rung) units across 2 independent CX datasets. The Ishida
recordings are same-fly simultaneous EPG+FC3 dual-color — the two-rung anchor
v1 cited as the headline.

## Result — per rung, walking-only (matched-activity), debiased vs raw

| Rung | n | rho_raw (med) | surrogate floor (med) | **rho_deb (med)** | rho_deb range | k_eff_emp (med) | Verdict |
|---|---|---|---|---|---|---|---|
| v18 EPG | 16 | 0.436 | 0.083 | **0.424** | 0.317–0.456 | 3.45 | PASS |
| v18 FC2 | 27 | 0.343 | 0.098 | **0.331** | 0.265–0.417 | 4.31 | PASS |
| v19 EPG | 7 | 0.092 | 0.023 | **0.089** | 0.072–0.290 | 12.40 | PASS |
| v19 FC3 | 7 | 0.273 | 0.044 | **0.269** | 0.206–0.319 | 6.42 | PASS |

(Full-recording, unconditioned, numbers are within 0.01–0.03 of the
walking-only column — see `results.json` `summary_full`. The activity
conditioning does not move the verdict.)

## Debiased vs raw — explicit comparison

The debiasing **does not change the conclusion at any rung.** The
phase-randomized surrogate floor is small relative to the genuine correlation
everywhere:

- v18 EPG: floor 0.083 -> debiasing shaves rho 0.436 to 0.424 (-2.8%).
- v18 FC2: floor 0.098 -> shaves 0.343 to 0.331 (-3.5%).
- v19 EPG: floor 0.023 -> shaves 0.092 to 0.089 (-3.3%).
- v19 FC3: floor 0.044 -> shaves 0.273 to 0.269 (-1.5%).

The genuine within-rung correlation **survives debiasing intact at all four
rungs.** No rung's correlation was a finite-sample / autocorrelation artifact.
The largest single-recording floor was 0.216 (one v18 EPG recording,
`2022_09_01_0002`); even there debiased rho stayed at 0.394, mid-band. This is
the opposite of the failure mode the wave falsifier names — there is no chaos
pin (rho_deb collapsing to ~0).

## Verdict against pre-registered thresholds

PASS required every CX rung's per-rung-median `rho_deb` off both poles:
off chaos (median >= 0.05) and off rigidity (median <= 0.80, p95 < 0.90).

- **Off chaos:** all four rung medians (0.089, 0.269, 0.331, 0.424) exceed
  0.05. Even the lowest, v19 EPG at 0.089, sits well above its own surrogate
  floor of 0.023 — it is genuine low correlation, not noise-floor zero. PASS.
- **Off rigidity:** the maximum rung-median is 0.424; the maximum single
  recording is 0.456 (v18 EPG). Nothing approaches 0.80, p95 nowhere near
  0.90. No rigidity pin. PASS.
- **Overall: PASS** — all four CX rungs occupy a bounded `rho_deb` band
  strictly off both poles.

## Reading — what reproduces, and an honest calibration note

v1's structural claim — both CX rungs corridor-occupying with bounded
within-rung correlation under matched-activity controls — **reproduces under
debiased rho.** The corridor finding is robust to the estimator upgrade.

The within-rung bands the debiased estimator returns:

- **EPG rung:** 0.089 (Ishida, ellipsoid-body GC7f) to 0.424 (Mussells Pires,
  protocerebral-bridge). The two EPG estimates differ by ~0.33 — the EPG bump
  in the EB ring is spatially compact (one localized activity peak among 16
  ROIs -> lower mean pairwise correlation, higher k_eff ~ 12), whereas the PB
  glomerulus representation is more distributed. Both are off-pole; both are
  genuine. This is a real per-preparation / per-neuropil difference, not a
  debiasing artifact.
- **FC2 / FC3 rung:** 0.269–0.331, tightly banded across both datasets and
  imaging modalities.

This means v1's Figure-1 substrate-local neural band of **0.25–0.75 does not
hold for the Drosophila CX under the canonical debiased estimator** — the CX
rungs sit lower, roughly **0.09–0.46**. Named honestly, exactly as the cancer
substrate's GPU-band mismatch was named: the structural claim (off both poles,
bounded) survives; the specific numeric band is a per-substrate calibration
that v2 should correct. The 0.25–0.75 figure was C. elegans-driven; the CX
data calls for its own band. This is a calibration correction, not a
falsification — per the pre-registration, an off-pole rung outside the stated
band is still a PASS for the structural claim.

`k_eff_emp` (canonical participation ratio) is 3.4–12.4 across the four rungs,
i.e. effective dimensionality well above 1 (not rigidity-collapsed) and well
below the nominal ROI count of 16–32 (not chaos-vacuous) — the same off-both-
poles signature in the dimensionality view.

## Bottom line

**PASS.** Debiased rho changes v1's Drosophila CX numbers by under 3.5% at
every rung; the genuine within-rung correlation survives the surrogate floor
intact; all four CX rungs (two datasets, including the Ishida same-fly
dual-color anchor) occupy a bounded band off rigidity and off chaos. v1's
Drosophila in-corridor finding **stands**. The only amendment for paper v2 is
the substrate-local band: the CX occupies ~0.09–0.46 (debiased), not the
0.25–0.75 stated in v1's Figure 1 — a calibration correction, named.
