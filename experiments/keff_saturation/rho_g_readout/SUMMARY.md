# 1/√L check — Gate-0 saturation levels are dominantly readouts of the maintained global correlation

**Date 2026-07-10.** Tests the coupled-model prediction
(`../../cosmo_entropic_potential/coupled_model/SUMMARY.md` §3): the saturated participation
ratio `L = k_eff` equals `1/ρ_g²` of the maintained global cross-unit channel, so on any Gate-0
substrate the effective global correlation should read out as `ρ_g ~ 1/√L`. Computed inline by
the orchestrating session from the stored spectra (`spectral_results_*.json`: `top_eigs`, `N`,
`PR_keff`); 15 substrate-analyses.

## The exact statistic (no rank-1 strawman)

For a correlation matrix `Tr = N`, `1/L = Σ pᵢ²` with `pᵢ = λᵢ/N`, `Σpᵢ = 1`. The global-mode
fraction is `f = p₁ = λ₁/N`. Then **`1/√L ≥ f` always** (equality only at rank 1), so
"`1/√L = f`" is not the test — the test is **what fraction of the inverse participation ratio
the global mode carries: `f²·L`**. `f²·L → 1` means the saturation ceiling *is* the global
correlation; `f²·L → 0` means sub-global structure sets it.

## Result

**The two independently-measured quantities co-vary at Spearman(f, 1/√L) = 0.918** across 15
analyses spanning three orders of magnitude in rank (`k_eff/N` from 0.0004 to 0.81). And the
global-mode fraction splits cleanly by rank:

| regime | global-mode fraction `f²·L` (median) | n |
|---|---|---|
| **LOW-rank (coordinating)** — finance, galaxy fields, galaxy gas, immune | **0.60** | 8 |
| **HIGH-rank** — cortical spikes, grayscreen, turbulent/dead-constructed controls | **0.22** | 7 |

In the low-rank coordinating substrates the maintained global mode carries a **median 60%** of
the inverse participation ratio (finance 0.84, galaxy-gas logT 0.80, logρ 0.67, galaxy z-height
0.59) — the saturation ceiling is *dominantly* the global cross-unit correlation, as the
coupled model says. In the high-rank substrates it carries only 22%, and the misses cluster
exactly where the model's own caveat placed them (`ρ_g < 0.3`, no dominant global mode):
cortical spike rasters (0.11–0.14), the turbulent and *dead-constructed* control cells
(0.33, 0.04) — the cells built to have no coordination.

## What this establishes (and does not)

**Establishes:** the catalogued saturation *levels* of coordinating systems are, to leading
order, readouts of one number — the maintained global correlation — as the coupled toy predicts
from the `1/ρ_g²` mechanism. This sharpens the **content-vs-tautology** question (Gate-0 open #5,
"the deepest"): "k_eff saturates" is not near-definitional, because the same k_eff definition on
high-rank substrates does *not* resolve into a dominant global mode. The low/high separation
(0.60 vs 0.22) is a contentful property that tracks whether the substrate coordinates.

**Does not:** `f²·L` is a decomposition, `≤ 1` by construction — the content is *where it lands*
(0.60 vs 0.22, with a clean gap), and the from-scratch cross-substrate prediction is the
Spearman 0.918 co-variation, not the magnitude of any single cell. "Global mode = ρ_g" is the
model's identification, clean only for a single dominant mode. The rank split at `k_eff/N < 0.15`
is a chosen threshold (the separation is clean across it, but it is chosen). No claim about which
partition nature uses — same seeded-block honesty as the coupled model.

## CORRECTION (rho-g-readout agent, full run with raw matrices — supersedes the inline version above)

My inline check used `f = λ₁/N` (top-eigenvalue variance fraction), which makes `f ~ 1/√L`
**near-tautological**: "one dominant mode of fraction f gives PR ~ 1/f²" is spectral algebra,
not a claim about correlation. The agent redid it with the **actual mean off-diagonal
correlation `ρ_dir`** on the same z-scored matrices, and the result is sharper and more
honest:

- **Confirmed, ~10%, ONLY where the global mode is genuinely UNIFORM (equicorrelation — exactly
  what the coupled toy builds).** Finance, both windows: `ρ_dir ≈ 0.9 × 1/√L`, top-eigenvector
  uniformity 0.97–0.99, ~0% negative pairs. The market mode literally *is* the mean
  correlation. This is the single in-hand substrate where the coupled-model reading is
  quantitatively vindicated.
- **FAILS on neural data with the toy's own observable.** C. elegans: `ρ_dir` median 0.067 vs
  `1/√L` = 0.33 — off 3–5×, with ~20% of pairs *negative*. Saturation is real (k_eff ~ 9) but
  it is carried by a **structured/signed** low-rank mode, not a uniform global channel; the
  "maintained global cross-unit correlation" reading does **not** transfer there.
- Exponent correction: the prediction is `k_eff ~ 1/f²` (`f ~ 1/√L`), not `1/f`. Confirmed:
  `L·f²` = 0.46–0.93 across all 7; `L·f` fails (1.6–3.9).

**Honest bottom line (replaces the one-sentence above):** the catalogued saturation level is a
readout of a maintained *uniform* global correlation **only on substrates that have one** —
markets, to ~10%. On neural/genomic substrates the dominant mode is signed and structured, its
mean pairwise correlation sits far below 1/√L, and the coupled-model interpretation is
substrate-conditional. What is substrate-*general* is only the spectral tautology (a dominant
mode of fraction f gives PR ~ 1/f²), which is not the contentful claim. Files:
`rho_g_check.py`, `rho_g_results.json`.
