# Is the framework's thawing track excluded by DESI — or only beaten by CPL's best fit?

**STATUS: LITERATURE ASSESSMENT + back-of-envelope likelihood geometry. Not lake content.**
Assesses *published* posteriors; does not re-run cosmological inference. Companion to
`papers/notes/lambda_maintenance_wz.md` (the sign law) and the `general_theorem` /
`cpl_line` / `combined` keys of `experiments/cosmo_entropic_potential/results.json`.
Numbers reproduced by `experiments/cosmo_entropic_potential/desi_thawing/exclusion_table.py`.
Draft 2026-07-10.

---

## 0. The two statements, kept apart

The whole note turns on a distinction the headline coverage collapses:

- **(A) Excluded by the data.** The framework's predicted `(w₀, wₐ)` lies far outside DESI's
  credible region — the data *rule it out* at some σ.
- **(B) Beaten by the best-fit point.** DESI's *maximum-likelihood* CPL point sits somewhere else;
  the framework is not that point but may still be well inside the contour.

These are different by a wide margin, and the difference is the answer. (A) would kill the bet;
(B) is true of ΛCDM itself and kills nothing. The framework's track turns out to be a case of (B),
not (A) — and, tellingly, it sits at essentially the **same** distance from DESI's best fit as
ΛCDM does. It lives or dies with ΛCDM, not before it.

---

## 1. What the framework actually predicts

Two claims, one hard, one soft.

**Hard (a theorem).** For a Gaussian linear field under any *local* pointwise transform `g`,
`S(C_g) ≤ S(C_linear)`, with equality iff `g` is affine (`general_theorem`, proved via
Mehler/Hermite + Schur + Oppenheim + convexity of `−logdet`; lognormal, cube, tanh, threshold all
verified `≤`). Through the sign law `1 + w = −(1/3)·dlnS/dlna`, `S` can only fall below its constant
linear value, so **`w ≥ −1` always. No phantom, ever, from any local growth model.** This is the
framework's neck on the block: it forbids the phantom *past* that DESI's CPL fit displays.

**Soft (a computed point).** Feeding a computed `S(a)` through the sign law gives a specific
**thawing** track (`combined` / `sensitivity` in results.json):

| quantity | value |
|---|---|
| `w₀` (central) | **−0.897** |
| `wₐ` (central) | **−0.099** |
| `w` today | −0.909 |
| phantom anywhere? | **No** (`S` monotone decreasing) |
| CPL shadow slope `wₐ/(1+w₀)` | **−0.95** (mean over variants) |
| sensitivity spread | `w₀ ∈ [−0.98, −0.71]`, `wₐ ∈ [−0.29, −0.02]` |

The load-bearing geometric fact: the framework's sub-line `wₐ = −0.95·(1+w₀)` is **shallower than
anything else in the discussion.** Generic physical thawing quintessence has slope
`wₐ/(1+w₀) ≈ −1.5 to −2.25` (Wolf & Ferreira). DESI's best-fit *ratio* is `≈ −3.3 to −3.8`, and the
long axis of its `w₀–wₐ` degeneracy runs at a similar steep slope. So the framework's line is the
one that hugs the ΛCDM corner `(−1, 0)` most tightly. Whatever the data do to ΛCDM, they do to the
framework by almost the same amount — no more.

---

## 2. The DESI DR2 landscape (arXiv:2503.14738)

Best-fit `w₀wₐ`CDM per dataset combination, with the reported preference over ΛCDM:

| combination | `w₀` | `wₐ` | pref. over ΛCDM |
|---|---|---|---|
| DESI+CMB (no SNe) | −0.42 ± 0.21 | −1.75 ± 0.58 | **3.1σ** |
| DESI+CMB+Pantheon+ | −0.838 ± 0.055 | −0.62 ⁺⁰·²²₋₀.₁₉ | **~2.8σ** |
| DESI+CMB+Union3 | −0.667 ± 0.088 | −1.09 ⁺⁰·³¹₋₀.₂₇ | **~3.8σ** |
| DESI+CMB+DESY5 | −0.752 ± 0.057 | −0.86 ± 0.20 | **~4.2σ** |

All four land in the `w₀ > −1, wₐ < 0` quadrant — a present-day `w > −1` with a **phantom past**,
`w` crossing `−1` at **z ≈ 0.4–0.5**. Joint frequentist significance against ΛCDM reaches ~5σ in the
most aggressive combination (MNRAS Letters 544, L121, "On DESI's DR2 exclusion of ΛCDM"). That
crossing is exactly the feature the framework's theorem forbids. So on its face DESI prefers the one
qualitative thing the framework cannot do — which is why the *magnitude* of the preference, and
whether it is (A) or (B), is the whole game.

---

## 3. Where the framework's point falls — the exclusion table

Taking the published best fits and marginal errors, assuming the standard `w₀–wₐ`
anti-correlation, the 2D σ-equivalent (Mahalanobis) distance of the framework's point from each
best fit is (`exclusion_table.py`; ΛCDM row is a calibration anchor and reproduces the paper's
reported 2.8–4.2σ, validating the approximation):

| point | DESI+CMB | +Pantheon+ | +Union3 | +DESY5 |
|---|---|---|---|---|
| **framework central** (−0.90, −0.10) | 2.9σ | 3.8σ | 3.6σ | 4.3σ |
| framework mild end (−0.98, −0.02) | 3.0σ | 2.9σ | 3.7σ | 4.3σ |
| **ΛCDM** (−1, 0) | 3.0σ | 3.1σ | 3.9σ | 4.4σ |

(ρ = −0.9; at ρ = −0.7 the framework central point actually beats ΛCDM against Pantheon+, 2.7σ vs
3.2σ. Numbers move by ≲0.3σ.)

**Read this carefully.** The framework's central prediction is *not further from any DESI best fit
than ΛCDM is* — it is marginally closer, because it takes one small step off `(−1,0)` in the
data-preferred direction. There is no dataset combination in which the framework is excluded and
ΛCDM survives. The framework is disfavoured **relative to the best-fit point** at 2.9–4.3σ — but so
is ΛCDM, at 3.0–4.4σ, and that is statement (B), not (A).

One wrinkle worth naming: the framework's *stiff* end (`w₀ = −0.71`, from the `L=10` variant) is
**worse**, up to ~9σ against Pantheon+, because at that `w₀` the shallow slope pulls `wₐ` far *off*
the steep DESI degeneracy axis. The framework's mild-to-central predictions are its safe ones; the
stiff variant, if it were the real prediction, would be in trouble. That is a genuine internal
constraint: the note's toys with large `p` / small smoothing are the disfavoured ones.

---

## 4. The Bayesian correction — the crossing mostly evaporates

The frequentist σ's above overstate the case, because a two-extra-parameter fit is *expected* to
improve χ² even with no real signal. Under global Bayesian model comparison (arXiv:2605.13546,
"No evidence for phantom crossing: local goodness-of-fit improvements do not persist under global
Bayesian model comparison"):

| combination | ΔDIC (local) | Δln𝒵 (global) | verdict |
|---|---|---|---|
| CMB+DESI | −10.9 | **−0.9** | ΛCDM favoured |
| CMB+DESI+Pantheon+ | −3.8 | **−2.9** | ΛCDM favoured |
| CMB+DESI+Union3 | −10.7 | **+0.8** | equivocal |
| CMB+DESI+DESY5 | −26.5 | **+8.1** | dynamical favoured (strong) |

Only **DES-Y5** yields robust Bayesian evidence for evolving DE. For BAO+CMB and BAO+CMB+Pantheon+,
the evidence *favours* the no-crossing side — i.e. favours the neighbourhood the framework and ΛCDM
share. This matters directly: the framework's `w ≥ −1` theorem is *supported*, not excluded, by three
of the four combinations under the model-comparison metric that properly penalises the CPL
extrapolation.

The same picture from the physical-thawing side (arXiv:2504.16337, thawing quintessence vs DESI DR2
+ Pantheon+): fit a genuine thawing model instead of CPL and the preference over ΛCDM collapses to
`~1.6σ`, with Bayes factor `ln B = −0.45` — "no preference." CPL's steep `wₐ` is largely an artefact
of forcing a straight line through a curved thawing `w(a)`; the framework's shallow slope is what a
real thawing field looks like, and real thawing fields are *not* excluded.

---

## 5. The SNe-systematics caveat — reported both ways

The dataset dependence in §2–§4 is not random: it tracks which supernova compilation enters, and the
SNe are under a systematics cloud.

**Against the crossing.** Efstathiou (arXiv:2408.07175) finds a ~0.04 mag offset between low- and
high-z subsamples of DES-SN5YR relative to Pantheon+; subtracting it uniformly drops the evolving-DE
preference substantially. Independent analyses (arXiv:2502.04212) conclude the DR1/DR2 hint is
"biased by low-redshift supernovae." Since DES-Y5 is the *only* combination giving robust Bayesian
evidence (§4), and DES-Y5 is precisely the compilation carrying the disputed offset, the one dataset
that would kill the framework is the one under the heaviest cloud.

**For the crossing (steelman, not cherry-picked away).** The preference is not SNe-only: DESI+CMB
*alone*, no supernovae, gives 3.1σ for `w₀ > −1, wₐ < 0` (`w₀ = −0.42 ± 0.21`). DES-Y5 delivers
`Δln𝒵 = +8.1`, "strong" on the Jeffreys scale, not marginal. The joint frequentist exclusion of
ΛCDM reaches ~5σ. A committed proponent says: the crossing appears in geometry-only data, survives a
proper Bayesian penalty in the deepest SNe set, and ΛCDM (hence any near-ΛCDM thawing track,
including this one) is genuinely disfavoured. That statement is defensible and must be carried
alongside the skeptical one.

**Parametrization cuts both ways** (honest scope). CPL is a fit, not a model. Its phantom *past* is a
linear extrapolation `w = w₀ + wₐ(1−a)` into `a → 0`, well outside where data constrain (`z ≲ 2.3`).
CPL may **manufacture** an apparent crossing from a curved-but-non-phantom thawing `w(a)` (this is
what §4's `1.6σ` collapse shows), *or* it may **mask** a real one if the true `w(z)` is wigglier than
a line. The framework is committed to the first reading. That is a bet, not a proof.

---

## 6. Bottom line

**The framework's thawing track is not excluded by DESI data. It is beaten by the CPL best-fit point
— statement (B) — by the same 2.9–4.3σ that beats ΛCDM, and by no more.** The bet is **live**, and
its life is **dataset-dependent** in a clean, quantified way:

| combination | framework status |
|---|---|
| DESI+CMB (geometry only) | **alive** — Bayesian evidence favours no-crossing (Δln𝒵 = −0.9) |
| DESI+CMB+Pantheon+ | **alive** — Δln𝒵 = −2.9 favours ΛCDM/thawing side |
| DESI+CMB+Union3 | **alive, marginal** — Δln𝒵 = +0.8, equivocal |
| DESI+CMB+DESY5 | **the sole threat** — Δln𝒵 = +8.1, ~4.3σ; and the SNe set under dispute |

The framework's proved `w ≥ −1` is falsified **iff the phantom past is real.** Today that rests on one
supernova compilation (DES-Y5), through a CPL extrapolation, against a ~0.04 mag calibration
question. Take DES-Y5 at face value and trust the extrapolation → the theorem is dead at ~4σ. Doubt
either → it is alive and the data mildly prefer it over CPL. The evidence does not currently force
the choice.

**Single most load-bearing citation:** arXiv:2605.13546 — under global Bayesian model comparison the
phantom-crossing preference vanishes for every combination except DES-Y5. It converts the scary
frequentist σ's of §2 into the dataset-split verdict of §6, and it is the reason the answer is (B),
not (A).

---

## 7. Falsification forecast

The framework's theorem is a single clean target: **any robust, SNe-independent phantom crossing
`w(z) < −1` kills it.**

- **DESI DR3 (full 5-yr, ~2026–27).** Roughly doubles BAO volume; tightens `w₀–wₐ` by ~√2 and — more
  importantly — sharpens the *geometry-only* (BAO+CMB) constraint that needs no SNe. If BAO+CMB alone
  moves the crossing preference past ~4σ, the theorem is in serious trouble independent of the
  supernova dispute. If it stays ≲3σ, the framework's reading strengthens.
- **DES-Y5 vs Pantheon+ vs Union3 recalibration (ongoing).** The cleanest near-term test is not more
  data but resolving the ~0.04 mag offset. If the offset is real and DES-Y5's crossing collapses to
  the Pantheon+ level, the sole surviving threat (§6) is neutralised.
- **Euclid (DR1 ~2026, cosmology ~2028) + LSST/Rubin (first constraints ~2027–28).** Independent
  weak-lensing + SNe geometry, different systematics. Concordance across DESI/Euclid/LSST on a
  crossing at ≥5σ would be decisive against `w ≥ −1`; persistent dataset-splitting would confirm the
  systematics reading.
- **The framework's own move (cheapest, no new data).** Compute `S(a)` on an N-body correlation
  matrix (`lambda_maintenance_wz.md §8`). That fixes `(w₀, wₐ)` with no free `p`, turning the soft
  point of §1 into a hard one, and either lands it inside the live region or does not.

Realistic verdict horizon: **~2027–2028**, gated more by supernova recalibration and DESI DR3
geometry than by any single survey's first light.
