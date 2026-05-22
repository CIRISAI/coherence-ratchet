# Robust re-run — S1 neural OUT-corridor (EEG): RESULTS

**Date:** 2026-05-21. **Pre-registration:** `PREREGISTRATION.md` (this
directory), fixed before this computation. **Compute:**
`compute_eeg_robust.py`. **Per-window output:** `results_eeg_robust.json`
(written incrementally, flushed per record).

## Verdict: **PASS**

v1's EEG out-corridor finding reproduces under the robust framing. Under
debiased ρ (phase-randomized surrogate floor) and canonical
participation-ratio k_eff, the pathological displacement direction is
unchanged: seizure and both coma-outcome groups sit rigidity-ward of
healthy interictal EEG. The strict 0.7 mean-pairwise rigidity pole-entry
threshold is still not reached — v1's quantitative-pole-entry caveat also
stands. **The v1 claim stands as written.**

## Data

Same data and same windowing as v1 — the only change is the ρ estimator
(v1 reported raw mean |off-diagonal|; this re-run adds the debiased ρ and
canonical k_eff). CHB-MIT patient chb01, 6 EDF files with seizures
(chb01_15 listed in the summary but absent on disk — skipped, exactly as
v1 skipped it; n_files=6, n_seizures=6 reproduced). I-CARE: the exact 6
patients / 1 EEG file each that v1 used (0342, 0364, 0411, 0474 Poor;
0549, 0571 Good). 10-s non-overlapping windows, 1–40 Hz 4th-order
Butterworth zero-phase band-pass. 20 phase-randomized surrogate draws per
window, seed 0.

(4 further I-CARE patients with valid outcomes — 0284, 0432, 0501, 0526 —
are present on disk but were not in v1's window set; excluded here to keep
the comparison strictly like-for-like. Available for a future extension.)

## Debiased vs raw — the headline numbers

| Group | n win | raw |ρ| mean | **debiased ρ mean** | floor mean | disp_raw | **disp_deb** | k_eff (PR) |
|---|---|---|---|---|---|---|---|---|
| Healthy interictal (CHB-MIT) | 1324 | 0.282 | **0.270** | 0.079 | — (baseline) | — | 6.48 |
| Seizure / ictal (CHB-MIT) | 39 | 0.316 | **0.300** | 0.098 | +0.034 | **+0.030** | 5.61 |
| Coma Good-outcome (I-CARE, CPC 1–2) | 60 | 0.502 | **0.496** | 0.074 | +0.220 | **+0.226** | 3.58 |
| Coma Poor-outcome (I-CARE, CPC 3–5) | 117 | 0.487 | **0.474** | 0.088 | +0.205 | **+0.204** | 3.26 |

`disp` = group mean minus healthy-interictal mean. v1 raw numbers are
reproduced to 3 decimals (v1: interictal 0.282, seizure 0.316, coma
≈0.49/0.50). The interictal window count is 1324 vs v1's 1322 — a
2-window difference from the canonical estimator's ≥4-valid-channel gate;
immaterial to every statistic.

## What debiasing does to the magnitude story — reported honestly

The phase-randomized noise floor is small relative to the signal at every
group: mean floor 0.074–0.098 (median interictal 0.076, range
0.054–0.140). Because `rho_deb = sqrt(rho_raw² − floor²)`, debiasing
subtracts a roughly constant ~0.08 floor in quadrature. The effect:

- **Direction is unchanged.** All three pathological displacements stay
  positive (rigidity-ward) and are essentially identical raw vs debiased:
  seizure +0.034 → +0.030; coma-good +0.220 → +0.226; coma-poor +0.205 →
  +0.204. The floor is comparable across healthy and pathological groups,
  so debiasing nearly cancels in the difference. PASS is unambiguous.
- **Absolute magnitudes shift down slightly.** Interictal 0.282 → 0.270;
  seizure 0.316 → 0.300; coma ~0.49–0.50 → ~0.47–0.50. The shift is
  largest where the floor is largest (seizure floor 0.098, the highest)
  but never exceeds ~0.017. The debiased numbers are marginally cleaner
  but tell the same story.
- **The strict 0.7 pole-entry threshold is still not reached.** No
  seizure window exceeds debiased ρ 0.42; 0% of seizure windows are above
  0.5. For coma, 32% of windows have debiased ρ > 0.5 and 11% > 0.7 — so
  coma is materially closer to the rigidity pole than seizure is, but the
  *group means* (0.47–0.50) sit below the strict 0.7 threshold. v1's
  exact framing — "qualitative direction supported, quantitative
  pole-entry not" — survives debiasing intact.

## Canonical k_eff — corroborates the direction

The participation-ratio k_eff (canonical estimator, replacing v1's
mean-pairwise proxy) moves monotonically with the rigidity-ward
displacement: healthy interictal k_eff ≈ 6.5 → seizure 5.6 → coma 3.3–3.6.
Effective dimensionality collapses toward 1 (the rigidity signature) in
the pathological groups, with coma the most collapsed — the same ordering
the debiased ρ gives. The k_eff evidence is independent of the ρ
estimator and points the same way.

## Verdict detail against the pre-registered criterion

PASS criterion: under debiased ρ, all pathological groups (seizure,
coma-good, coma-poor) displaced rigidity-ward of healthy interictal by
more than ±0.005. Observed displacements +0.030, +0.226, +0.204 — all
positive, all well above the 0.005 indistinguishability band. No group
reverses. **PASS.**

FAIL conditions (direction reverses, or displacement vanishes within
±0.005): none triggered.

## Persistence (unchanged from v1, reported for completeness)

Seizure durations 27, 40, 51, 90, 93, 101 s — median 70.5 s, all <2 min
(Mode i, self-terminating). Comatose state persists only under mechanical
ventilation, targeted temperature management, and sedation (Mode ii by
construction). This re-run does not re-litigate persistence; it concerns
only the ρ estimator. The paper-v1 persistence reading is untouched.

## Bottom line for paper v2

The §sec:corridor-empirical "Substrate 1: neural" out-of-corridor
paragraph requires **no amendment**. Under the structural series' canonical
debiased-ρ + participation-ratio-k_eff estimator, on the identical v1
window set: pathological EEG (seizure, post-cardiac-arrest coma) is
displaced toward rigidity relative to healthy interictal EEG; the strict
0.7 pole-entry magnitude is not reached. v1's qualitative-direction-yes /
quantitative-pole-entry-no finding stands on uniform footing with the rest
of the v2 paired-validation matrix.
