# S(a) — the coordination entropy of the cosmic density field, and the sign of 1+w

**Status: proxy calculation, 2026-07-10. Nothing here is asserted by the lake.**
Reproduce with `python3 s_of_a.py` (seed 20260710, numpy/scipy only, ~4 min).
Outputs: `results.json`, `fig1`–`fig5`.

This is the falsifiability crux of the cosmology tier. The companion note
(`papers/notes/lambda_maintenance_wz.md`; construction in
`papers/notes/entropic_action_bridge.md`, T-E5 in
`formal/CoherenceRatchet/Core/EntropicPotential.lean`) defines

```
S = -Tr ln C = -ln det C = 2 x (Gaussian multi-information)
```

on the **normalized** correlation matrix `C` of a set of comoving coordinating units.
Reading Λ as the maintenance cost of cosmic coordination gives `ρ_Λ ∝ S(a)`, and the
continuity equation `ρ̇ + 3H(1+w)ρ = 0` then yields a parameter-free **sign law** in which
the proportionality constant drops out:

```
1 + w(a) = -(1/3) · d ln S / d ln a
```

So `S` const ⇒ `w = -1`; `S` rising ⇒ `w < -1` (phantom); `S` falling ⇒ `w > -1`.

Until `S(a)` is computed the framework predicts a sign *law* but no *sign*. This note
computes it.

---

## Verdict, up front

| Question | Answer |
|---|---|
| Is `S` invariant under linear growth? | **Yes**, to machine precision (`7.5e-15` analytic, `1.6e-15` numerical). `w = -1` exactly. The ΛCDM fence holds. |
| Sign of the nonlinear (mode-coupling) channel? | **`dlnS/dlna < 0`** ⇒ `w > -1`. *Opposite to the sign anticipated in the task brief and in `lambda_maintenance_wz.md` §3.* |
| Sign of the causal (horizon) channel? | Negative for event/Hubble horizons, positive for the particle horizon — but all are **`~10⁻⁴`–`10⁻²`** of the needed magnitude. Negligible either way. |
| Does `S(a)` peak? | **No.** `S` is monotonically decreasing on `a ∈ [0.3, 1]` in every configuration tested. |
| Does it match DESI? | **Partially. The two CPL *signs* match (`w₀ > -1`, `wₐ < 0`); the *shape* does not.** DESI's CPL best-fit point requires `w < -1` for `z ≳ 0.35`. The framework **structurally forbids** `w < -1` (see §5). |

**The headline is not the lognormal number. It is that the sign is a theorem.**
Section 5 proves that *no local model of nonlinear structure growth* can make `S`
rise. Since `S → S_linear` (a constant) as `a → 0` and `S ≤ S_linear` always, `S` can only
fall, so `1 + w ≥ 0` at all epochs. **This reading of Λ cannot produce phantom dark
energy.** If DESI's phantom epoch is real, the reading is dead — which is what a
falsifiability crux is supposed to look like.

---

## 1. Methods

**Cosmology.** Flat ΛCDM, `Ω_m = 0.315`, `Ω_Λ = 0.685`, `h = 0.674`, `n_s = 0.965`,
`σ₈ = 0.811`. Radiation neglected (irrelevant for `a > 0.1`). Growth factor
`D(a) ∝ H(a)∫₀^a da'/(a'H(a'))³`, normalized `D(1) = 1`; `f ≡ dlnD/dlna = 0.527` today.

**Power spectrum.** `P(k) = A k^{n_s} T(k)²`, with `T` from Eisenstein & Hu (1998,
ApJ 496, 605) zero-baryon "no-wiggle" (Eqs. 26–31); Bardeen, Bond, Kaiser & Szalay (1986)
with the Sugiyama (1995) `Γ` as a cross-check. Normalized to `σ₈` with a top-hat-8 window.

**Coordinating units.** A cubic lattice of `n³` comoving cells of spacing `L`, each
smoothed with a spherical top-hat of equal-volume radius `R = L(3/4π)^{1/3}`
(Gaussian window cross-checked). The cell correlation function
`ξ_R(r) = (2π²r)⁻¹ ∫dk k P(k) W²(kR) sin(kr)` is evaluated with oscillatory-weight
quadrature (exact in the `sin` factor), then `c_ij = ξ_R(r_ij)/σ_R²`, `c_ii = 1`.

**Background scales.** `r_EH(1) = 3447` Mpc/h, `r_PH(1) = 9714` Mpc/h,
Hubble radius `(aH)⁻¹|₁ = 2998` Mpc/h, matter–Λ equality `z = 0.296`,
acceleration onset `z = 0.632`.

**DESI target.** DR2 BAO + CMB + Pantheon+, `w₀ = -0.838`, `wₐ = -0.62`
([arXiv:2503.14738](https://arxiv.org/abs/2503.14738); 2.8–4.2σ preference for dynamical
DE over ΛCDM). This requires `dlnS/dlna|₀ = -3(1+w₀) = -0.486` and an `S` **peak** at
`z = 0.354` (where `w = -1`).

---

## 2. Linear-theory invariance — the ΛCDM fence holds

**Analytically.** In linear theory `δ(x,a) = D(a)δ(x)`, so `Cov_ij(a) = D(a)²Cov_ij(1)`.
The normalization `C_ij = Cov_ij/√(Cov_ii Cov_jj)` divides by `D(a)` twice: the growth
factor cancels **identically**. `C` — and hence `S = -ln det C` — is independent of `a`.
Therefore `Λ = const` and `w = -1` exactly.

**Numerically**, two independent constructions over `a ∈ [0.1, 1]`:

| Construction | `S` | max `|S(a)/S(1) - 1|` |
|---|---|---|
| Analytic `C` from `ξ_R`, scaled by `D(a)²` | 3.7589016914918 | `7.5e-15` |
| Gaussian random field, 500 realizations, 64 cells (2048 Mpc/h box, 128 Mpc/h cells), sample `C` per epoch | 109.6 | `1.6e-15` |

Both at machine precision (fig1). The GRF path required one non-obvious choice: with no
DC mode the cell values sum to exactly zero in every realization, giving `C` an exact null
eigenvector. Keeping a `4³` **sub-block** of the `16³` cell grid removes that constraint
(min eigenvalue 0.0118, condition number 428).

**Conclusion.** The framework reproduces ΛCDM exactly wherever linear theory holds. Any
`w ≠ -1` must come from a change in the **shape** of `C`, not its amplitude. Confirmed, not
falsified.

---

## 3. The nonlinear channel — `S` falls, so `w > -1`

Standard analytic proxy for the nonlinear density field (Coles & Jones 1991): the
lognormal transform `δ = exp(g - σ_g²/2) - 1` with `g` the Gaussian linear field,
`σ_g²(a) = D(a)²σ_R²`. Then `ξ_NL = exp(ξ_g) - 1` and `Var(δ) = exp(σ_g²) - 1`, so the
**normalized** correlation matrix is exact and closed-form:

```
C_NL,ij(a) = [exp(σ_g²(a) · c_ij) - 1] / [exp(σ_g²(a)) - 1]
```

(PSD by the Schur product theorem — a positive-coefficient power series in Hadamard powers
of `c`; `→ c` as `σ_g → 0`; unit diagonal exactly.)

Because `x ↦ e^{σ²x} - 1` is convex with `f(0) = 0`, `f(c) < c·f(1)` for `c ∈ (0,1)`:
**every off-diagonal entry is contracted toward zero**, and more so as `σ_g²` grows.
Physically: nonlinear collapse inflates the cell variance `σ_R²` faster than it inflates
the inter-cell covariance, because it moves power to scales *below* the cell. The field
becomes dominated by rare high peaks and the cells decorrelate. `det C` rises, `S` falls.

| `L` (Mpc/h) | `R` (Mpc/h) | `σ_R` | `S_linear` | `dlnS/dlna|₀` | `w₀` | `wₐ` | `S` monotone ↓ |
|---|---|---|---|---|---|---|---|
| 10 | 6.20 | 0.980 | 58.24 | **−0.787** | −0.706 | −0.291 | yes |
| 20 | 12.41 | 0.564 | 31.71 | **−0.274** | −0.897 | −0.098 | yes |
| 50 | 31.02 | 0.223 | 10.49 | **−0.048** | −0.982 | −0.017 | yes |
| 100 | 62.04 | 0.095 | 3.50 | **−0.009** | −0.996 | −0.003 | yes |

**Analytic cross-check.** To leading order in `σ_g²` (small off-diagonals, `S ≈ Σ_{i<j} C_ij²`):

```
d ln S / d ln a  =  2 f σ_g² ( <c³>/<c²> - 1 )   <  0   since 0 < c < 1
```

At `L = 20`: predicted `-0.265`, exact `-0.274` (3.5% agreement). The sign is analytic.

**Magnitude.** DESI's required `dlnS/dlna|₀ = -0.486` is reproduced at `L ≈ 14` Mpc/h.
This is a **calibration, not a prediction** — the cell scale is a free choice (§6).

---

## 4. The causal channel — real, and irrelevant

The framework's maintenance term `γM` requires *ongoing* causal contact, so "maintainable
coordination" should count only cell pairs still inside a cosmological horizon. Three
candidates are tested: the comoving **event** horizon `r_EH(a) = ∫_a^∞ da'/(a'²H(a'))`
(shrinks under acceleration), the **Hubble radius** `(aH)⁻¹` used by
`lambda_maintenance_wz.md` §2 (peaks at acceleration onset), and the **particle** horizon
(grows).

Implemented on a two-scale point set (a dense `4³` block at 20 Mpc/h spacing, which carries
the correlation, plus a sparse `4³` block at 1200 Mpc/h spacing, which carries the horizon
crossings; 128 cells total). A hard mask `1[r < r_h]` is not positive-definite in general,
so the principled default is a smooth **Gaussian causal taper**
`K_ij = exp(-(r_ij/r_h)²)` — a PD kernel on ℝ³, so `C ∘ K` remains a correlation matrix
with unit diagonal (Schur). Two alternatives (`exp(-r/r_h)`, hard mask) are reported for
sensitivity. **This is a modeling choice, not a derivation.**

| horizon | kernel | PSD? | min eig | `dlnS/dlna|₀` |
|---|---|---|---|---|
| event | gauss | yes | 0.312 | `−1.1e-4` |
| event | exp | yes | 0.314 | `−1.0e-2` |
| event | hard | yes | 0.312 | `−1.7e-15` |
| hubble | gauss | yes | 0.312 | `−9.1e-5` |
| hubble | exp | yes | 0.315 | `−7.2e-3` |
| particle | gauss | yes | 0.312 | `+5.1e-6` |
| particle | exp | yes | 0.313 | `+1.3e-3` |

The signs are as expected — shrinking horizons (event, Hubble) give `S↓ ⇒ w > -1`; the
growing particle horizon gives `S↑ ⇒ w < -1` — but **the magnitudes are 2–5 orders of
magnitude short** of the `-0.486` needed.

**The causal-mask null, quantified.** `S ≈ Σ_{i<j} C_ij²` is dominated by pairs at
`r ≲ 100` Mpc/h; the horizons sit at `~3000` Mpc/h, where `ξ/σ² ~ 10⁻⁸`. So:

| horizon | pairs *beyond* `r_h` today | share of `S` they carry |
|---|---|---|
| event (3447 Mpc/h) | 61% | `2.7e-16` |
| Hubble (2998 Mpc/h) | 62% | `~1e-16` |
| particle (9714 Mpc/h) | 15% | `~1e-16` |

61% of pairs lie beyond the event horizon and carry `3e-16` of `S`. Masking uncorrelated
pairs costs nothing. (The hard mask stayed PSD only *because* it is effectively a no-op.)

**This directly refutes the "extensive beats intensive" argument of
`lambda_maintenance_wz.md` §3.** That note factorizes `S = k_maint · s̄` and argues the
horizon term removes whole causal volumes (extensive) and so should dominate the nonlinear
shape term (intensive). The factorization assumes the mean per-link relative entropy `s̄`
is uniform across links. It is not, by sixteen orders of magnitude: the measured ratio
`s̄(removed)/s̄(retained)` is `1.8e-16` (event), `2.3e-16` (Hubble), `1.1e-18` (particle).
Dropping whole causal volumes removes links of essentially zero relative entropy, so
`dln(k_maint)/dlna` does **not** transfer to `dlnS/dlna`. The extensive argument fails.

The `exp(-r/r_h)` kernel is larger only because it damps *every* pair, including the
correlated ones — it is not really a causal restriction. **No causal-mask variant can
rescue the phantom branch at any grain where `S` is dominated by real correlations.**

---

## 5. The general theorem — phantom is structurally forbidden

The lognormal is one proxy. But the result does not depend on it.

> **Theorem.** Let the linear field be Gaussian with normalized correlation matrix `c`, and
> let `g` be **any** pointwise (local) transform. Then `S(C_g) ≤ S(c)`, with equality iff
> `g` is affine.

*Proof.* By the Mehler/Hermite expansion, `Corr(g(X),g(Y)) = Σ_{n≥1} w_n c^n` with
`w_n ∝ a_n² n!`, `a_n = E[g(Z)He_n(Z)]/n!`, `Σ w_n = 1`. So `C_g = Σ_{n≥1} w_n c^{∘n}` is a
**convex combination of Hadamard powers** of `c`, each PSD with unit diagonal (Schur product
theorem). Oppenheim's inequality with `A = c^{∘(n-1)}` (unit diagonal), `B = c` gives
`det(c^{∘n}) = det(A∘B) ≥ det(B)·Π_i A_ii = det(c)`, hence by induction
`S(c^{∘n}) ≤ S(c)` for all `n ≥ 1`. Finally `-ln det` is convex on the PD cone, so
`S(C_g) = -ln det(Σ_n w_n c^{∘n}) ≤ Σ_n w_n S(c^{∘n}) ≤ S(c)`. ∎

Verified numerically (`S_linear = 31.708`; the Hermite machinery reproduces the exact
lognormal `C_NL` to `1.4e-16`, which validates it):

| transform `g` | `S(C_g)` | `≤ S_linear`? |
|---|---|---|
| lognormal | 24.54 | yes |
| `tanh(2σz)` | 26.62 | yes |
| cube | 12.33 | yes |
| threshold `ν=1` | 8.96 | yes |
| strong `exp(3σz)` | 2.11 | yes |
| square | 1.93 | yes |
| `abs` | 1.51 | yes |

Also checked here: `S(σ_g²)` strictly decreasing over `σ_g² ∈ [0.05, 3]` for **400 random
correlation matrices**, 0 violations. (Needed, because "shrinking every off-diagonal raises
`det`" is *not* a general matrix fact — it holds here because of the Hadamard-power
structure.)

**Independent verification.** A separate implementation (distinct code, orchestrator
session) reproduced the load-bearing inequalities on independent random ensembles:
Oppenheim `det(c^{∘n}) ≥ det(c)` — **0 / 1200** violations; the convex-combination step
`S(Σ w_n c^{∘n}) ≤ Σ w_n S(c^{∘n})` — **0 / 300**; lognormal monotonicity in `σ_g²` —
**0 / 200**. Two codebases, same result.

**Consequence.** `S(a) ≤ S_linear` for all `a`, and `S(a) → S_linear` as `a → 0`. `S` can
only fall. Therefore `1 + w = -(1/3)dlnS/dlna ≥ 0`: **`w ≥ -1` at every epoch, for every
local model of nonlinear growth.** No tuning of `L`, `σ₈`, window, or transfer function can
produce a phantom epoch or a peak in `S`. **No local model of nonlinear growth can produce
a phantom past.**

**Caveat — the class this covers.** Gravitational evolution is *not* a pointwise map of the
linear field: mass is displaced, and the Zel'dovich map is nonlocal. The theorem covers the
broad class of **local density transforms**, of which the lognormal is the standard analytic
member. It does not cover displacement-induced changes in `ξ(r)` shape. **The decisive test
is an N-body measurement of `C_ij(a)` on fixed comoving cells** (§9).

---

## 6. Free choices and the sensitivity of the sign

Every variant below is a nonlinear-channel calculation on `a ∈ [0.3, 1]`.

| variant | `σ_R` | `dlnS/dlna|₀` | `w₀` | `wₐ` | sign | phantom anywhere? |
|---|---|---|---|---|---|---|
| baseline (EH98, top-hat, `n=6`, `L=20`) | 0.564 | −0.274 | −0.897 | −0.098 | − | no |
| transfer = BBKS | 0.589 | −0.281 | −0.894 | −0.101 | − | no |
| window = Gaussian | 0.271 | −0.075 | −0.971 | −0.024 | − | no |
| `n = 4` (64 cells) | 0.564 | −0.274 | −0.897 | −0.098 | − | no |
| `n = 8` (512 cells) | 0.564 | −0.274 | −0.897 | −0.098 | − | no |
| `L = 10` Mpc/h | 0.980 | −0.787 | −0.706 | −0.291 | − | no |
| `L = 50` Mpc/h | 0.223 | −0.048 | −0.982 | −0.017 | − | no |
| `σ₈ = 0.7` | 0.487 | −0.203 | −0.924 | −0.072 | − | no |
| `σ₈ = 0.9` | 0.626 | −0.341 | −0.872 | −0.123 | − | no |

**The sign is invariant across every free choice** (fig5). The magnitude is not.

- **Most sensitive choice: the cell scale `L`** (equivalently `σ_R`). It moves
  `dlnS/dlna|₀` over `[-0.79, -0.01]`, i.e. `w₀ ∈ [-0.71, -1.00]` — the entire
  observationally interesting range. `L` is *not* fixed by the framework: nothing in the
  entropic-action bridge says what a "cosmic coordinating unit" is. **This is the single
  largest unresolved modeling freedom, and any quantitative claim about `w₀` is hostage to
  it.** The leading-order formula shows why: `dlnS/dlna ∝ σ_R²`, and `σ_R²` runs by two
  decades from 6 to 62 Mpc/h.
- The number of cells `n³` is **irrelevant** (identical to 4 digits from 64 to 512 cells) —
  `dlnS/dlna` is a `c`-weighted ratio, not an extensive quantity. This also makes the sign
  law insensitive to whether one uses `S` or the per-unit density `S/k` (T-E3), since `k`
  is fixed: `dln(S/k)/dlna = dlnS/dlna`.
- Transfer function is a ~3% effect. `σ₈` at ±0.1 is a ±25% effect on the magnitude,
  none on the sign.
- The causal kernel choice (§4) changes the magnitude by ~100× and the sign with the
  horizon choice — but every option is negligible.

**A parameter-free by-product.** Across all cell scales, `wₐ/(1+w₀) = -0.954 ± 0.02`, i.e.

```
wₐ ≈ -(1 + w₀)
```

This is forced: `w → -1` as `a → 0` (because `σ_g² → 0`), so the framework's `w(a)` is a
**thawing** trajectory and CPL must fit `w₀ + wₐ = -1`. It predicts a *line* through the
ΛCDM point `(-1, 0)` in the `(w₀, wₐ)` plane, of slope `-1`. DESI's best-fit point has
`wₐ/(1+w₀) = -3.83`, and its degeneracy direction is much steeper than `-1`. The two are
distinguishable in principle; a proper comparison needs the DESI `(w₀,wₐ)` covariance,
which we do not have here.

---

## 7. Combined result vs. DESI

Both channels together (nonlinear + Gaussian event-horizon taper, `L = 20` Mpc/h):

| quantity | framework | DESI DR2 requires |
|---|---|---|
| `dlnS/dlna|₀` | **−0.274** (−0.79 … −0.01 over `L`) | **−0.486** |
| `S` peak | **none** (monotone ↓) | **`z = 0.354`** |
| `w₀` | −0.897 | −0.838 ± 0.055 |
| `wₐ` | −0.099 | −0.62 (+0.18/−0.21) |
| `wₐ/(1+w₀)` | −0.954 | −3.83 |
| `w < -1` anywhere? | **no — forbidden** | **yes, for `z ≳ 0.354`** |
| min eigenvalue of `C` | 0.322 (PSD throughout) | — |

**Reported honestly: this is a directional match and a structural mismatch.**

- **Match.** The framework independently predicts the two signs DESI reports —
  `w₀ > -1` and `wₐ < 0` — from a calculation with no free parameter fitted to DESI.
  It also lands in the right ballpark of magnitude for `w₀` at a plausible cell scale
  (`L ≈ 14` Mpc/h reproduces `-0.486` exactly), and matter–Λ equality (`z = 0.296`) sits
  close to DESI's inferred `S`-peak (`z = 0.354`) — though the framework does not produce
  that peak.
- **Mismatch.** DESI's CPL best-fit point crosses into `w < -1` at `z ≈ 0.35`; the
  framework forbids `w < -1` (§5). The framework's `|wₐ|` is ~4–6× too small, and it
  produces no `S` peak at all. Its `w(a)` is a monotone thawing curve from `-1` toward `w₀`.

We do **not** tune to close this gap.

**Falsification condition, stated plainly.** If `w < -1` at any epoch is established at
high significance — through a parametrization that does not force the crossing — then
`ρ_Λ ∝ S` with `S` the coordination entropy of a locally-transformed Gaussian field is
**false**, and no choice of grain, window, transfer function, or causal kernel can save it.

---

## 8. Honest scope of the DESI comparison

**The comparison target is the CPL best-fit POINT `(w₀, wₐ) = (-0.838, -0.62)`, not the
DESI likelihood.** This distinction is load-bearing and must not be elided:

- Whether DESI's *data* actually excludes the `w ≥ -1` thawing line at high significance is
  **parametrization- and SNe-compilation-dependent** and is **not settled by this
  computation**. The reported 2.8–4.2σ range for dynamical DE spans the choice of supernova
  sample (PantheonPlus / Union3 / DES-Y5); the higher end leans on DES-Y5.
- CPL with `w₀ > -1, wₐ < 0` **forces** a phantom crossing by construction, so DESI's
  evidence for the *crossing itself* is weaker than its evidence for dynamical dark energy
  generally. Non-crossing thawing quintessence — exactly the class the framework predicts —
  is not excluded by the BAO data alone.
- The framework's specific prediction is the **line** `wₐ = -(1+w₀)` (a one-parameter
  thawing family), not a point. A fair test projects the DESI posterior onto that line and
  asks whether the data prefer a point off it. That requires the DESI `(w₀, wₐ)` covariance,
  which is not used here. We report the point-vs-point mismatch and the slope mismatch
  (`-0.95` vs `-3.83`) as the honest available comparison, and flag that a likelihood-level
  test is the correct next statistical step.

In short: the framework predicts thawing quintessence with no phantom crossing. DESI's
best-fit CPL point *has* a crossing. Whether that constitutes a high-significance
falsification is a question about the DESI likelihood and the SNe compilation, and is left
open here.

---

## 9. What this is not

- **Not a simulation of the framework's cosmological dynamics.** No such dynamics exists.
  There is no `dρ/dt = α - γM` evolved on a cosmological substrate here. `S(a)` is computed
  from a *model* of the density field, and `w(a)` from the *assumed* proportionality
  `ρ_Λ ∝ S`.
- **Not a nonlinear calculation of gravity.** The lognormal (and the wider pointwise class
  of §5) is an analytic **proxy** for the nonlinear density field. Its variance
  `e^{σ_g²} - 1` overshoots the true one. Real gravitational evolution displaces mass and
  is nonlocal; §5's theorem does not reach it.
- **Not a derivation of the causal restriction.** §4's horizon masking is a modeling choice
  (which horizon; which kernel), documented as such.
- **Not a fit to DESI.** No parameter was adjusted to match. `L ≈ 14` Mpc/h is reported as
  the scale that *would* reproduce DESI's `dlnS/dlna|₀`, and is labeled a calibration.
- **Not a likelihood-level test** (§8). The comparison is against the CPL best-fit point.
- **Not real data.** §10.
- **Not mechanized.** None of this is in the Lean development. Only `S = -ln det C` and
  its `k,ρ` closed form are theorems there (T-E1–T-E5). The Mehler/Oppenheim argument of §5
  is a candidate for mechanization and is currently a pen-and-paper proof with numerical
  confirmation in two independent codebases.

**The decisive next step is N-body**: measure `C_ij(a)` directly on a fixed comoving cell
grid across snapshots of Quijote or AbacusSummit. It tests §5's theorem outside the
pointwise class, needs no bias model, and settles the sign of the real nonlinear channel in
an afternoon. It is the one calculation that could overturn the verdict, because
displacement is the one thing the theorem does not cover.

---

## 10. Real data: `cosmo_sdss_galaxies.parquet` offers no handle

389,751 galaxies, `z ∈ [0.020, 0.150]`, i.e. `a ∈ [0.87, 0.98]` — a single flux-limited
low-redshift sample. Checked and set aside, for two reasons:

1. The lever arm is `Δln a = 0.12`, over which the predicted change in `S` is `< 2%`.
2. Splitting into `z`-shells makes luminosity-dependent galaxy bias `b(z, L)` evolve with
   the shell. Bias drops out of the *normalized* correlation matrix only if it is scale- and
   epoch-independent — precisely the assumption that fails in a flux-limited sample. The
   bias systematic is degenerate with the signal.

There is no time evolution to extract. Not forced.

**What it would take, in order of decisiveness:**

1. **N-body** (§9). Settles the sign of the real nonlinear channel; no bias model needed.
2. A multi-epoch spectroscopic sample with a controlled, epoch-independent tracer
   (volume-limited, fixed number density), so `b` cancels in `C`.
3. A first-principles statement of what a cosmic "coordinating unit" is, which would fix `L`
   and turn `w₀` from a calibration into a prediction.

---

## Files

| file | contents |
|---|---|
| `s_of_a.py` | everything; `python3 s_of_a.py`, seed 20260710, deterministic |
| `results.json` | all numbers quoted above |
| `fig1_linear_invariance.png` | `S(a)` flat; deviation at machine `ε` |
| `fig2_nonlinear_S.png` | `S(a)` falling; `dlnS/dlna` vs DESI's required band |
| `fig3_w_of_a.png` | `w(a)` vs DESI CPL; the forbidden phantom region |
| `fig4_causal.png` | horizons vs correlation scales; causal channel negligible |
| `fig5_sensitivity.png` | sign invariant across every free choice |

## References

- Bardeen, Bond, Kaiser & Szalay (1986), ApJ 304, 15 — BBKS transfer function.
- Coles & Jones (1991), MNRAS 248, 1 — lognormal model of the density field.
- Eisenstein & Hu (1998), ApJ 496, 605 — no-wiggle transfer function (Eqs. 26–31).
- Horn & Johnson, *Matrix Analysis*, §7.8 — Schur product theorem, Oppenheim's inequality.
- Sugiyama (1995), ApJS 100, 281 — baryon-corrected shape parameter.
- DESI Collaboration (2025), [arXiv:2503.14738](https://arxiv.org/abs/2503.14738) — DR2 BAO.
