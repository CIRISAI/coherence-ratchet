# MEPP-flavor — DECISIONS (pre-registered BEFORE any result is computed)

**Date 2026-07-12.** Turns the one THIN fill-out named in `papers/notes/sm_from_thermodynamics.md`
§4 (couple Maximum-Entropy-Production selection to the mixing rung) into a registered forward
fork, killing each of the four causes of its thinness. This file freezes the σ-map, the σ
observable, and the δ-locator **before** the ensemble is run. Nothing here may be changed after
a result is seen; a null under this registration is reported as a null (the `pandey-crosscheck`
post-hoc-estimator burn is the anti-pattern we are avoiding).

Discipline: this is a **SELECTION** claim, capped at Class V of `sm_escalator_statistics.md`
(selection, never derivation). It earns **nothing** until a distinct-δ forecast is confirmed by
DUNE/Hyper-K. It is registered as a forward fork with its kill; it is **not** married.

---

## 1. THICKENER 1 — the FORCED functional (no retrofit)

We do **not** invent a σ-functional. We use the bench-validated steady-state entropy-production
form already frozen in `experiments/corridor_ceiling/sigma_max.py` (Godrèche–Luck 2019
arXiv:1807.00694; Kwon–Ao–Thouless 2005), verified there two independent ways (Sekimoto analytic
+ Monte-Carlo Stratonovich heat):

> **σ = Tr[ Qᵀ D⁻¹ Q C⁻¹ ]**, N1 normalization: D = I, bounded ACTUATED drive `‖QC⁻¹‖_F² ≤ P`.

In C's eigenbasis this is `σ = Σ_{i<j} Q_ij²(1/λ_i + 1/λ_j)` with cost
`‖QC⁻¹‖_F² = Σ_{i<j} Q_ij²(1/λ_i² + 1/λ_j²)`. The N1-maximum is a linear-fractional program
whose optimum puts all budget on one pair:

> **σ_max(C) = P · max_{i<j} (1/λ_i + 1/λ_j) / (1/λ_i² + 1/λ_j²)**,  P ≡ 1 fixed for all matrices.

This is the exact generalization of `sigma_max.py::sigma_max_N1` to an arbitrary correlation
spectrum {λ_i}. **Provenance check (pre-committed):** our `sigma_max_N1(C)` must reproduce the
frozen `sigma_max.py::sigma_max_N1(rho,k)` on the equicorrelation Kish object
`C=(1−ρ)I+ρ11ᵀ` to machine precision, for a grid of (ρ,k), before any flavor use. If it does
not, the run aborts.

## 2. THICKENER 1 — the map from the flavor copula |V|² to the correlation structure C

The map is **not** chosen freshly; it is the copula→correlation construction already frozen in
`experiments/sm_escalator_mixing/run_mixing.py::functionals` — the same C whose `−ln det C` is the
program's `S_onehot` copula functional (amplitude-blind by clause 3). Given a unitary V:

- `P(i,j) = |V_ij|² / 3` is the flavor copula (doubly-stochastic |V|², uniform 1/3 marginals).
- Build the one-hot indicator correlation matrix `C_copula` (4×4) on indicators
  `1_{X=1},1_{X=2},1_{Y=1},1_{Y=2}` under P — the verbatim construction in `functionals` lines
  40–53. `C_copula` is a genuine correlation matrix (symmetric, unit diagonal, PSD).

**Faithfulness check (pre-committed):** `−ln det C_copula(V)` must equal
`functionals(V)["S_onehot"]` to ~1e−9 on the observed CKM and PMNS matrices. `copula_C` is an
*extraction* of the frozen C, not a reimplementation of the functional; the check enforces that.

**σ observable (frozen):** `σ_flavor(V) = σ_max_N1(C_copula(V))` at P=1. Physical reading: the
flavor copula's correlation structure is the stationary covariance of a maintained OU coordination
process; σ_flavor is the maximum entropy production it can sustain under a common bounded
actuation budget. This is the FORCED functional applied to the FORCED (frozen) flavor object.

## 3. THICKENER 2 — the δ-locator (frozen before computing)

**Ensemble:** the SAME 200k Haar U(3), seed 20260710, `haar_u3` (Mezzadri) reused verbatim from
`run_mixing.py` (rigor pass confirmed bit-identical regeneration). For each matrix compute:
`σ_flavor`, `MI`, `absJ`, the angles (`sin²θ12,23,13`), `J_max(angles)=c12 s12 c23 s23 c13² s13`,
and `|sinδ| = min(absJ / J_max(angles), 1)` (rephasing-invariant CP *usage*). Observables carried
forward: **|J|** (total CP, what DUNE constrains via δ) and **|sinδ|** (CP usage: 0 = CP-conserving,
1 = maximal). `MI` is the coordination/anarchy axis.

**(A) Concentration test.** Report the σ_flavor Haar-percentile of the observed CKM and PMNS
copulas. Report the sign and value of `Spearman(σ_flavor, MI)` over the ensemble — this DECIDES
whether high-σ selects the anarchic pole (negative → PMNS-like) or the comonotone pole
(positive → CKM-like). Report `E[MI | top-q σ]` vs the flat-Haar `E[MI]` and vs the observed
CKM/PMNS MI: does the σ-extremal region concentrate toward an observed copula MORE than the flat
prior? (q = 5% primary; 1%, 10% robustness.)

**(B) Forward δ fork.** Primary selector: **top-q σ_flavor quantile** (q = 5% primary; 1%, 10%
robustness) — a tuning-free "σ-extremal region." Robustness selector: exponential tilt
`w ∝ exp(β · z(σ_flavor))`, z = standardized σ, β ∈ {1,2,5}, plus the moment-matched `β*` for
which `E_w[σ] = σ_flavor(observed PMNS)`. In the selected/tilted sub-ensemble report the **|J|**
and **|sinδ|** distributions with **bootstrap 95% CIs** (1000 resamples).

**(C) Distinctness tests (pre-registered thresholds).**
- **vs flat anarchy (a).** Two-sample KS of σ-selected |J| (and |sinδ|) against the full Haar
  ensemble; plus median-shift with bootstrap 95% CI. **DISTINCT** iff KS p < 0.01 AND the median-
  shift CI excludes 0, for the primary q=5% selector.
- **vs minimization (b).** Thaler–Trifinopoulos (arXiv:2410.23343) predicts *suppressed* leptonic
  CP (|J|, |sinδ| → 0; δ CP-conserving). Surrogate: the bottom-q |J| Haar region (flagged as a
  surrogate, not their computation) and the CP-conserving pole |sinδ|→0. **DISTINCT from
  minimization** iff σ-selected median |sinδ| is CI-separated *above* the minimization surrogate's
  (i.e. σ-max does NOT suppress CP).

**(D) KILL (staked here, before results).** If the σ-selected |J| and |sinδ| distributions are
statistically **indistinguishable from flat anarchy** (KS p > 0.05 AND median-shift CI includes 0),
there is **no distinct fork**: the fill-out stays THIN forever, and we say so plainly. A degenerate
result where σ-max *suppresses* |J| (colliding with minimization) is likewise reported as
"not a distinct third prong."

## 4. THICKENER 4 — the leptogenesis constraint (kills "imported principle")

Reframe: the CP-violation-during-baryogenesis era was literally an out-of-equilibrium
(maximal-dissipation) epoch (Sakharov condition 3). Ask whether the surviving lepton copula is the
one that maximized entropy production. **The honest subtlety (from `sakharov_ledger.md` §2d):**
genuine high-scale leptogenesis (Fukugita–Yanagida) sources CP from the *heavy Majorana* phases,
which are **not** the low-energy PMNS δ; leptogenesis can succeed with δ_PMNS → 0. So the
observable-δ fork can decouple from the selected quantity.

**Pre-registered leptogenesis diagnostic.** σ_flavor acts on the copula through two channels:
- **capacity channel** (angles): `Spearman(σ_flavor, J_max(angles))` and `Spearman(σ_flavor, MI)`.
- **usage channel** (phase): partial correlation of σ_flavor with |sinδ| **controlling for the
  three angles** (rank partial correlation). 

Verdict rule (frozen): if σ_flavor acts **only through the capacity/angle channel** (usage partial
correlation CI includes 0), then the phase/usage is decoupled: σ-max selects the anarchic *angle
structure* but says nothing about low-energy δ — under high-scale leptogenesis the DUNE δ fork is
**weakened** (the selected quantity is the angles, not the observable phase). If σ_flavor **also**
acts through the usage channel (partial correlation CI excludes 0 and points to enhanced |sinδ|),
the observable δ stays coupled to the selected quantity and the DUNE fork survives the leptogenesis
subtlety. Report which.

## 5. Sign-agnostic reporting & discipline

- All correlation signs are reported as found; the pre-registration does NOT assume σ-max selects
  anarchy. If `Spearman(σ_flavor, MI) > 0` (σ-max selects the comonotone/CKM book), that CONFLICTS
  with the leptogenesis reading ("the imbalance posts from the anarchic book") and is reported as a
  tension, not hidden.
- Class V cap: selection, never derivation. No new dimensionless datum is claimed; the mixing
  result is already banked. The ONLY route to earning anything is a confirmed distinct-δ DUNE
  forecast (rule 2).
- Nulls reported as nulls. Verified citations only. Seed 20260712 for bootstrap; ensemble seed
  20260710 (frozen). CPU only. Incremental flush.

## 6. Deliverable verdict template (what the run must answer)

1. Does σ-max concentrate on the observed copula — yes/no, and how much vs the Haar prior (with the
   sign of Spearman(σ_flavor, MI))?
2. The predicted |J| / |sinδ| distribution under σ-max weighting, with error bars — DISTINCT from
   flat anarchy? DISTINCT from minimization? (the 3-way fork verdict).
3. Does the leptogenesis constraint keep δ observable (usage channel live) or decouple it (capacity
   channel only)?
4. THIN or THICKENING: is there now a distinct registered DUNE fork, or does it stay thin?
