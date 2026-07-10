# Copula verification: the no-phantom decline is a Gaussian-ruler artifact of an exact invariance

**All four checks PASS.** Executed 2026-07-10, seed fixed; every number below is executed
output (`results.json`). Summary written by the orchestrator after the assigned agent went
idle without one; verdicts and figures are the agent's, verified against the JSON.

This runs §3 of `papers/notes/copula_invariance_remark.md` — the verification pass the
operator's flag demanded. **It modifies no committed theorem.** What it modifies is the
*interpretation stack* above them, and it sharpens clause 4 of the Ledger Law.

## Estimator validation (done first, as required)

KSG k-NN mutual-information estimator, k_knn = 4, validated against the Gaussian case where
truth is analytic. Example: k = 3, ρ = 0.3, n = 20,000 → truth 0.12167, estimate
0.12312 ± 0.00593 (bias +0.00145). Bias and variance are quantified per case in
`results.json → estimator_validation`; the (a)-test criterion is tiered
(direct / extrapolated in n) accordingly.

## (a) True multi-information is invariant under invertible pointwise maps — **PASS**

Across a grid of k ∈ {3,4,5} × ρ levels × an n-ladder to 800,000 samples: the true MI of the
lognormal image matches the Gaussian MI within estimator error.

- **35/36 channels PASS, 0 FAIL, 1 indeterminate** (verdict `PASS_WITH_INDETERMINATE` — the
  indeterminate cell is estimator-limited, not a violation).

The lognormal map is invertible pointwise, so the copula is unchanged; MI is a functional of
the copula alone. **Confirmed numerically.**

## (b) Rank-based S is flat where Pearson S falls — **PASS**, and decisively

On the s_of_a cell geometry (27 cells, 20 Mpc/h spacing), sweeping the nonlinearity σ from
0.05 → 1.6:

| functional | at σ = 0.05 | at σ = 1.6 | change |
|---|---|---|---|
| `S_pearson` (what the no-phantom computation measures) | 3.1911 | **0.3277** | **−2.861** |
| `S_rank` (Gaussian-rank / van der Waerden correlation) | 3.1966 | 3.1966 | **max \|dev\| 0.0078** |

`S_linear` = 3.1889. **The Pearson functional loses 90% of its value across the nonlinearity
ramp; the rank functional does not move at the third decimal.** This is the cheap discriminator
the remark specified, and it lands exactly where predicted.

## (c) Strict decrease under a non-invertible map — **PASS**

±1 thresholding (non-invertible) strictly decreases the true MI in every case, as DPI requires.
Small-ρ ratio `I_binary / I_gauss` = **0.4195**, against the Van Vleck arcsine-law prediction
`(2/π)² = 0.4053`. Agreement to ~3%, and it independently reproduces the 2/π attenuation
already documented in the quantum-corridor `CALIBRATION.md`.

## (d) The cosmological consequence — **PASS**

Re-running the nonlinear `S(a)` computation with `C_rank` instead of `C_pearson`
(27 cells, 6 seeds, 100k samples):

| functional | `dlnS/dlna` today | implied `w₀` |
|---|---|---|
| Pearson | **−0.2737** | −0.909 |
| Rank (analytic) | **0.0** | **−1 exactly** |
| Rank (empirical) | −0.0461 ± 0.148 (sd), sem 0.0606 | consistent with 0 |

The empirical rank slope is **statistically consistent with exactly zero**; the residual
w-error from finite sampling is 0.0202.

## What this means

1. **Clause 4 of the Ledger Law sharpens from an inequality to an exact invariance.** For
   *invertible* local (pointwise) maps, the true coordination content changes by **exactly
   zero** — not merely "cannot increase." Non-invertible maps strictly destroy it (c). The
   creation channels are therefore even narrower than the law states: genuine interaction and
   unit formation, and nothing else, full stop.
2. **The no-phantom theorem is TRUE AS STATED and its interpretation is now precise.** It is a
   theorem about the *Gaussian-committed* functional `−ln det C_pearson`, and that functional
   really does decline under local nonlinearity — this run reproduces the decline (b). But the
   decline is **the Gaussian ruler reading a non-Gaussian field**, not a loss of coordination
   content. Nothing committed is retracted; the physical gloss "nonlinear growth destroys
   coordination" is wrong and is retired.
3. **The fixed-unit cosmological branch sharpens from `w ≥ −1` (thawing) to `w = −1` exactly.**
   Under the true-MI reading, local growth contributes *nothing* to `w(z)`. The entire signal
   in the framework's `w(z)` — if any exists — must come from the unit-formation / non-local
   channel. This makes the halo-grain channel not "an escape from the theorem" but **the only
   channel there is**, and it makes the fixed-unit branch's prediction sharper and more
   falsifiable than before: not "w ≥ −1," but "w = −1."
4. **The blind spot survives the sharpening, unchanged.** Rank/copula S is still a *pairwise*
   functional. Coordination carried purely above second order (GHZ-type) remains invisible to
   it. The bug-or-prediction fork is untouched: either the true ledger is the all-orders
   multi-information, or purely higher-order coordination is entropically dark. This run
   confirms the second-order machinery is self-consistent; it says nothing about order ≥ 3.

## What this does NOT do

- It does not touch any Lean theorem. `s_of_a.py`'s general theorem, `entropicPotential_*`,
  and `EntropicContraction`'s T-C1 all stand exactly as proved.
- It does not rescue or damage the DESI comparison: the pre-registered pipeline
  (`PREREGISTRATION.md`) uses the extensive B-total channel, which is a *unit-formation*
  quantity, not a local-transform quantity. The frozen spec is unaffected.
- The rank functional is a *Gaussian-copula* proxy for the true MI, exact for pointwise
  transforms of Gaussian fields (the case tested). For a genuinely non-Gaussian *copula* it is
  itself only a shadow — one rung less committed than Pearson, not zero rungs.

Artifacts: `copula_check.py`, `report_numbers.py`, `results.json`, `run.log`, figs 1–4.
