# DR3 shape-test addendum — the framework's w(a) is not CPL, registered before DR3

**Date 2026-07-11. STATUS: PRE-REGISTRATION ADDENDUM. Frozen alongside, never replacing,
`experiments/cosmo_entropic_potential/PREREGISTRATION.md` (frozen `a5beb57`).**

This document registers an *additional* test of the *same* frozen bet. It creates no
alternative claim and switches nothing. The registered DR3 bet remains exactly what the
frozen preregistration and `papers/notes/the_grain_problem.md` §5 state — the corner-rule
B-total pipeline, crossing epoch **z = 0.59 ± 0.03**, losses reported as losses. That
commitment is incorporated here by reference and is unchanged (§4).

What is new: the frozen pipeline does not merely predict a crossing epoch and a `w_today`. The
sign law `1 + w(a) = −⅓·dlnS/dlna` applied to the *frozen* S(a) fixes an entire **shape**
`w(a)` — a specific curve, non-linear in `a`, with **zero free parameters** (κ cancels in the
sign law; `PREREGISTRATION.md` §2 "Sign law"). When DR3 releases, the decisive comparison is a
model comparison between that fixed curve and the two-parameter CPL family on the *same*
likelihood. The point of climbing "the law vs a family member" is parsimony: a zero-parameter
curve that fits as well as best-fit CPL beats CPL on evidence and on AIC/BIC by the parameter
count alone. This document fixes the curve now and states the protocol so a hostile third party
executes it identically.

---

## 1. THE SHAPE, fixed now

### 1.1 The frozen S(a) it is derived from

Source: `experiments/cosmo_entropic_potential/large_volume/results.json`, key
`stage2_primary.records` (the 10-snapshot TNG300-1 corner-rule run, threshold
`stage2_primary.thr = 742530285568.0` M⊙/h). Each row below quotes `records[i].{z, a, S}`
verbatim; `w` is derived by the frozen estimator of §1.2.

| z (`.z`) | a (`.a`) | S = −ln det C (`.S`) | w(a) derived |
|---|---|---|---|
| 3.008 | 0.2495 | 1544.1 | −2.771 |
| 2.316 | 0.3016 | 3533.0 | −2.164 |
| 1.744 | 0.3645 | 5954.1 | −1.695 |
| 1.358 | 0.4242 | 7672.7 | −1.442 |
| 1.036 | 0.4913 | 8983.9 | −1.281 |
| 0.791 | 0.5583 | 9739.5 | −1.129 |
| 0.546 | 0.6467 | 9936.2 | −0.982 |
| 0.329 | 0.7525 | 9711.1 | −0.930 |
| 0.153 | 0.8675 | 9376.1 | −0.899 |
| 0.000 | 1.0000 | 8867.5 | −0.833 |

The S(a) column has an interior maximum at z = 0.590 (`stage5.primary.interior_peak_z =
0.5896633869209742`); w crosses −1 there, thawing to `w_today = −0.833`
(`stage5.primary.w_today = −0.8332054965762254`; jackknife 68% = ±0.057,
`stage5.jackknife.w_today_err68 = 0.057037869923213066`). These reproduce the frozen
preregistration verdicts and are not re-litigated here.

### 1.2 The interpolation rule (the frozen estimator, stated so it is reproducible)

`w(a)` between the tabulated nodes is defined by exactly the frozen pipeline operator, no new
choice:

1. Fit a natural cubic spline to `ln S` against `ln a` on the 10 nodes above
   (`s_of_a.py::dln_dlna`, `CubicSpline(np.log(a_grid), np.log(S))`, frozen `533816f`).
2. `dlnS/dlna(a)` = first derivative of that spline.
3. `w(a) = −1 − ⅓·dlnS/dlna(a)` (`s_of_a.py::w_from_S`; comoving normalization,
   `PREREGISTRATION.md` §2 "Sign law").

κ never enters — the sign law is a log-derivative, so the overall normalization of S (and thus
κ) cancels identically. **The shape carries zero free parameters.** This is the single
property that makes the model comparison of §2 worth running: CPL spends two parameters to
approximate a curve the framework fixes with none.

### 1.3 How it differs from its own best-fit CPL

Best-fit CPL `w(a) = w0 + wa·(1−a)`, uniform-weight least squares over the DESI-sensitive
window a ∈ [0.5, 1] (z ∈ [0, 1]), fit to the §1.2 curve:

> **w0 = −0.800, wa = −0.664**, and over a ∈ [0.5, 1] the shape departs from this best CPL by
> **max|Δw| = 0.130, at a ≈ 0.50 (z ≈ 1.0)**.

Widen the fit window to a ∈ [⅓, 1] (z ≲ 2) and the mismatch grows to **max|Δw| = 0.38 near
z ≈ 2**: the shape plunges well below −1 at high z faster than any straight line in a
(w = −1.28 at z = 1.04, −1.70 at z = 1.74, −2.77 at z = 3.0). The curve is markedly
**super-CPL**: convex-steepening into the past, a shape CPL structurally cannot render.

**So at the level of the w(a) curve the shape is unambiguously non-CPL.** The honest question
for DR3 is whether that curve-level difference survives projection into the actual BAO
observables at DR3 precision. It largely does not, and this is registered plainly:

### 1.4 The observable-level difference — marginal, and this is the make-or-break honesty

Propagating the shape and its best-fit CPL through ρ_DE(a) = exp(3∫(1+w)/a da), H(z), and the
BAO distances (Ω_m = 0.3155 fixed, the `SUMMARY.md` convention), the fractional distance
residuals shape-vs-its-own-CPL are:

| z | ΔD_H/D_H | ΔD_M/D_M |
|---|---|---|
| 0.3 | +0.21% | +0.24% |
| 0.5 | −0.25% | +0.15% |
| 0.7 | −0.45% | +0.02% |
| 1.0 | +0.04% | −0.05% |
| 1.3 | +0.56% | +0.01% |
| 1.6 | +0.88% | +0.10% |
| 2.0 | +1.05% | +0.21% |

The 0.13 pointwise Δw collapses to **sub-percent, largely self-cancelling distance residuals**:
≤ 0.45% in D_H and ≤ 0.24% in D_M across the dark-energy-dominated regime (z ≲ 0.7), rising to
~1% in D_H only by z = 2 **where dark energy is subdominant and BAO leverage on w is weak**.
DESI DR2 per-bin BAO precision is ~1–2% on D_H/r_d; DR3 will sharpen that by perhaps a third.
The shape's non-CPL curvature therefore sits **at or below** DR3's per-bin distance precision
in exactly the regime where DR3 constrains dark energy.

> **Make-or-break verdict: at the w(a)-curve level the shape is distinctly non-CPL
> (max|Δw| = 0.13 over a ∈ [0.5, 1]); at the DR3 distance-observable level it is only
> MARGINALLY distinguishable from best-fit CPL — the residuals are sub-percent and partly
> cancel.** The shape test is therefore **not** expected to win on a distance-shape difference
> DR3 can see directly. Its only real leverage is **parsimony**: the shape fits with zero free
> parameters where CPL spends two. If the fixed curve lands inside the DR3 posterior, the
> evidence/AIC/BIC comparison favors it over CPL by the parameter count; if the fixed curve
> lands outside where CPL's two parameters can reach, CPL buys a real χ² gain and the shape
> loses. That, not a visible kink in w(a), is what §2 tests. The honest registered expectation
> is **weak-to-moderate** evidence, not strong.

---

## 2. THE PROTOCOL — model comparison to run when DR3 drops

Stated so a hostile third party executes it identically. Nothing below is tuned to a result;
it is fixed now.

**Models compared (all on the identical likelihood):**
- **(i) SHAPE** — the §1 tabulated `w(a)` with the §1.2 interpolation rule. **0 free
  cosmological-sector parameters** (κ cancels); Ω_m, H0, r_d, and nuisance/SNe-calibration
  parameters marginalized identically across all three models.
- **(ii) CPL** — `w(a) = w0 + wa(1−a)`, **2 free parameters**, priors w0 ∈ U[−3, 1],
  wa ∈ U[−3, 2] (the standard DESI DR2 w0waCDM priors).
- **(iii) Λ** — `w = −1`, **0 free parameters**.

**Datasets (run three combinations; the split is load-bearing):**
- **A. DESI DR3 BAO + CMB (Planck) only** — the SNe-independent geometry test. This is the leg
  the original kill K1 lives on (§5).
- **B. A + DES-5YR SNe.**
- **C. A + Pantheon+ SNe.**
The evolving-DE preference in DESI is SNe-driven and split-dependent (DES-5YR pulls toward
evolving DE; Planck+BAO alone modestly favors Λ, ln B ≈ −0.57 ± 0.26 in the DR2 analysis of
arXiv:2511.10631). Reporting A, B, C separately is mandatory; a shape "win" that appears only
under one SNe sample is reported as exactly that.

**Statistic:** Bayesian log-evidence ln Z from nested sampling (the DESI-standard estimator),
reported as pairwise log-Bayes-factors ln B_{ij} = ln Z_i − ln Z_j, with **ΔAIC and ΔBIC**
quoted alongside as parametric cross-checks (AIC = 2k − 2ln L_max; BIC = k ln N − 2ln L_max; k
= parameter count, N = data points). The parsimony content lives here: SHAPE and Λ carry k = 0
sector parameters, CPL k = 2, so ΔAIC and ΔBIC already credit SHAPE 4 and 2·lnN over CPL at
equal fit.

**Decision thresholds (Jeffreys / Kass–Raftery bands on |ln B|; Kass & Raftery 1995, Trotta
2008):**

| |ln B| | Evidence |
|---|---|---|
| < 1 | inconclusive / weak (bare mention) |
| 1 – 2.5 | moderate (positive) |
| 2.5 – 5 | strong |
| > 5 | very strong / decisive |

**The two comparisons that decide the addendum:**
1. **SHAPE vs CPL** (`ln B_{SHAPE,CPL}`). > 0 = the zero-parameter law is preferred over the
   two-parameter family — the climb. The pre-registered *expectation* is |ln B| in the weak-to-
   moderate band (§1.4): the shapes are observationally close, so the comparison is dominated by
   the Occam factor CPL pays for its two parameters. SHAPE wins modestly *iff* its fixed curve
   sits inside the DR3 posterior.
2. **SHAPE vs Λ** (`ln B_{SHAPE,Λ}`). Both are zero-parameter, so this is a pure goodness-of-fit
   contest with no Occam term — it directly asks whether the fixed thawing curve beats the
   cosmological constant on DR3 geometry. The grain-problem floor (`the_grain_problem.md` §2)
   already has the frozen pipeline beating ΛCDM on DR2 (1.36σ vs 3.28σ; Δχ² favorable); DR3 is
   the registered re-test of that at higher precision.

**Execution note:** all three models share one pipeline, one set of marginalized nuisance
parameters, one r_d treatment, one Ω_m prior. Any asymmetry in nuisance handling between models
voids the comparison.

---

## 3. THE Σm_ν LEG — direction registered, magnitude deferred

Registered as **direction and sign only. No number is claimed.**

The framework's thawing background (w > −1 today, having crossed from w < −1) supplies less
late-time dark-energy suppression of structure growth than ΛCDM, which **relaxes the
cosmological neutrino-mass bound** relative to the ΛCDM analysis that produces the current
Σm_ν squeeze — the mild tension in which CMB+BAO under ΛCDM press the bound at or below the
minimal normal-ordering oscillation floor Σm_ν ≈ 59 meV. The registered qualitative
expectation:

> Under the framework's background, the minimal-NO value Σm_ν ≈ 59 meV moves from
> *squeezed against the bound* to *comfortable*. The **direction of relief** is registered; the
> **magnitude is not** — the exact relaxed bound requires a full joint DR3 + CMB likelihood run
> with the §1 w(a) inserted, which has not been performed. No relaxed bound in eV is asserted
> here beyond the sign.

This is the same background that (independently of the neutrino sector) is registered as
thawing; the squeeze-relief leg leans only on that thawing, not on any retention-derived κ
(`papers/notes/neutrino_de_prior_art.md` §7c, and its resolution: retention FAILED its audit,
so the fourth-root/composite chain stays circular; this leg is unaffected because it depends
only on the background w(a), not on κ). Cross-referenced kills K-ν1/K-ν2/K-ν3 in that note are
untouched by this addendum.

---

## 4. ANTI-HEDGING, restated

This addendum registers **additional tests of the same frozen bet**. It creates **no**
alternative claim and switches **nothing**.

- The binding commitment of `papers/notes/the_grain_problem.md` §5 is incorporated by
  reference and is **unchanged**: the registered DR3 bet is the frozen corner-rule B-total
  pipeline, crossing epoch **z = 0.59 ± 0.03**; complete-book and galaxy-book reads are logged
  alternatives for understanding the grain problem, **not switchable claims**; if DR3 lands on a
  variant's number and not the registered one, the registered bet **loses and is reported as
  lost**. One bet, placed, held.
- The shape of §1 is **derived from** that same frozen pipeline's frozen S(a) — it is not a new
  object, it is the curve the already-registered sign law was always fixing. Registering it
  explicitly forecloses any post-hoc "we meant the shape, not the epoch" retreat: **both the
  epoch (z = 0.59 ± 0.03) and the shape (§1 table) are fixed now, together.**
- The grain problem (`the_grain_problem.md` §§3–4) is **not** reopened. The shape is the corner-
  rule shape; the amplitude's underived assembly-epoch-sharpness variable stays underived. This
  addendum adds a test, not a resolution.

---

## 5. KILL CONDITIONS for the shape test

Each kill is separable and dated. The original preregistration kills (`PREREGISTRATION.md` §4,
K1–K7) stand unchanged; these are additions specific to the shape claim.

| # | DR3 outcome | Kills | Survives |
|---|---|---|---|
| S1 | **CPL strongly preferred over SHAPE**: `ln B_{CPL,SHAPE} > 5` on the SNe-independent combination A (DESI DR3 BAO + CMB) — CPL's two parameters buy a decisive χ² gain the shape cannot, i.e. the fixed curve lands outside the DR3 posterior. | **The shape claim** (the fixed w(a) is the wrong curve). | The epoch bet (P1) is judged separately by its own criterion; Λ-comparison (S3) separate. |
| S2 | **SHAPE loses to Λ**: `ln B_{Λ,SHAPE} > 2.5` on combination A — the fixed thawing curve fits DR3 geometry worse than a cosmological constant. | **The thawing-shape claim** on geometry, and it drags the whole DE leg (the grain-problem §2 "beats Λ" floor fails at DR3 precision). | Nothing on the DE leg; the two-axis discriminator and other rungs are untouched (ladder independence). |
| S3 | **Robust SNe-independent phantom crossing** `w < −1` at ≥ 4σ from combination A (the original K1, restated by reference). | **The intensive branch / the thawing reading** — the frozen shape has w > −1 today and forbids a robust present phantom; a confirmed SNe-independent phantom crossing kills it. | Extensive branch survives *only if* its computed crossing epoch also matches (K1's original conjunction). |
| S4 | **SHAPE ≈ CPL, inconclusive**: `|ln B_{SHAPE,CPL}| < 1` on all combinations. | Nothing — but the shape test is declared **uninformative** and reported as such. This is the pre-registered honest null (§1.4): the observable-level difference is sub-percent, so DR3 may simply lack the precision to separate a zero-parameter curve from its two-parameter envelope. A null here is a legitimate registered outcome, **not** a loss and **not** a win. | Everything; the epoch bet (P1) and the Λ-comparison (S3) are decided on their own. |

**Pre-registered expectation across S1–S4:** the honest prior is **S4 (weak/inconclusive) or a
modest SHAPE-over-CPL preference in the moderate band** — because the curves are close at the
distance level and the only real lever is the parameter-count Occam factor. A strong result in
*either* direction (S1 or a decisive SHAPE win) would be more informative than expected and is
reported at face value. Over-reading a marginal ln B as a shape victory is the failure mode this
section exists to prevent.

---

## 6. Files and provenance

Reads (unmodified): `experiments/cosmo_entropic_potential/PREREGISTRATION.md` (`a5beb57`),
`experiments/cosmo_entropic_potential/large_volume/{results.json, SUMMARY.md}`,
`experiments/cosmo_entropic_potential/s_of_a.py` (`dln_dlna`, `w_from_S`, `fit_cpl`; `533816f`),
`papers/notes/the_grain_problem.md` §5, `papers/notes/neutrino_de_prior_art.md` §7c.

Every scalar in §1 is quoted against its `results.json` key. Derived `w(a)`, the CPL fit, and
the §1.4 distance propagation were computed with the frozen `s_of_a.py` estimator
(`CubicSpline(ln a, ln S)` → sign law); the propagation used standard FLRW distance integrals
with Ω_m = 0.3155 fixed. Methodology citations verified 2026-07-11: Jeffreys/Kass–Raftery
evidence bands (thresholds 3:1, 12:1, 150:1 → |ln B| ≈ 1, 2.5, 5); DESI DR2 SNe-driven,
split-dependent evolving-DE preference and the Planck+BAO-only ln B ≈ −0.57 ± 0.26 result
(arXiv:2511.10631, arXiv:2511.18657).

This document is frozen on creation. Any change to §1 (the shape) or §2 (the protocol) produces
a *different* test and voids this registration for the changed item.
