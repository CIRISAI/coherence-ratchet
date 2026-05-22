# P_ω on an explicit finite-dimensional tower — results

**Date:** 2026-05-21. **Falsification handle:** F-11 / F-12 (P_ω operator
construction). **Pre-registration:** `PREREGISTRATION.md` (this directory).
**Build script:** `build_tower_pomega.py`. **Raw results:** `results_tower.json`.

---

## VERDICT: DOCUMENTED OBSTRUCTION

The soft backward operator E_ω(β) = exp(−β H_sum) **is constructible on a
genuine finite-dimensional tower** — that part of the pre-registration's
"Constructed" branch is met. But when the tower carries the **cross-rung
penalty terms** ω's property (iii) requires — H_{n,n+1} = (τ_n − τ_c)² coupling
adjacent rungs — the operator is **exponentially suppressed well before the
framework's 9 rungs**. The fixed-space proxy's rung budget R\* ≈ 25–56 was an
artifact of carrying *within-rung penalties only*. The genuine tower with
cross-rung structure re-triggers the dead zone.

This is a specific, characterised wall — an F-11/F-12 documented obstruction —
not a "the soft route works" success. It is reported as a result.

---

## What was built (the construction is genuine)

A genuine tower, **not** a relabelled fixed-space proxy:

- **A sequence of finite-dimensional spaces** H₀, H₁, …, H_{R−1}, each a qutrit
  (dim d = 3 — the minimum with a genuine spectral *interior* for a [0,1]
  correlation operator). The tower was built to depth **R = 160**.
- **Explicit coarse-graining maps** W_n : H_n → H_{n+1} — square unitary RG
  steps (mix-and-relabel). Rung n+1's correlation operator ρ_{n+1} is the
  genuine W_n **push-forward** of ρ_n (+ a 15% RG perturbation so adjacent
  rungs are coupled-but-distinct, Piece 6). Not independent random draws.
- **Within-rung terms** H_n^within = (ρ_n − ρ_c)² on site n.
- **Cross-rung terms** H_{n,n+1} = (τ_n − τ_c)² on the bond (n,n+1), where τ_n
  is built **through** the coarse-graining map W_n (direct product correlation
  ρ_n ⊗ ρ_{n+1} plus a through-the-map term that vanishes if W_n is not used —
  so τ_n genuinely depends on the RG map). These terms make H_sum
  **non-factorising** — a genuine 1D nearest-neighbour rung-chain Hamiltonian.
- **E_ω,R(β_pin) = exp(−β_pin H_sum)** assembled as a matrix-product operator
  (MPO) of bond dimension 11 — the transfer-network object the rung-chain's
  1D-locality affords.

**The dimension wall is tamed by the tower structure.** A faithful nested
P_ω has dim ~ 2^(2^R) — doubly exponential, which capped the prior faithful
model at 3 rungs. Here H_sum is 1D-local, so h_min(R) = λ_min(H_sum) is a 1D
ground-state problem:
- **Exact** sparse Lanczos for R ≤ 13 (full d^R up to 1.6M-dim, GPU);
- **DMRG** (two-site, MPO-based, GPU) for R = 9…56 — cost *linear* in R.
- DMRG validated against exact: |Δh_min| = 6×10⁻¹¹ (R=9), 2×10⁻⁹ (R=13).

CUDA throughout: cupy / complex128, 1 device. Runtime ~6 min. Results flushed
to JSON per rung-depth (incremental).

---

## What the genuine tower showed that the fixed-space proxy could not

The pre-registration's two named gaps, both closed — and the closing is the
obstruction:

### 1. The cross-rung terms impose a non-dilutable per-rung penalty floor

Controlled diagnostic — the *same* genuine tower, cross terms ON vs OFF
(`cross_on_off_diagnostic` in the JSON; OFF = exactly the proxy's H_sum):

| R  | within-only h_min/R | within+cross h_min/R | ratio |
|----|--------------------|---------------------|-------|
| 3  | 0.057              | 0.156               | 2.7   |
| 8  | 0.054              | 0.191               | 3.5   |
| 13 | 0.041              | 0.175               | 4.3   |

- **Within-only** (the proxy's regime): h_min/R **decreases** with R — the
  within-rung penalty *dilutes*. The per-rung-dimension scan shows it is also
  highly instance-dependent and *can* fall into the proxy regime: across
  d = 2…5 (one tower instance each) within-only h_min/R ranged 0.0017–0.25 —
  e.g. 0.0017 at d=4, within reach of the proxy's measured 0.00081/rung. The
  proxy was not wrong that within-only penalties can be made small.
- **Within+cross**: h_min/R **plateaus at ≈ 0.17–0.19** with R, and across the
  same d = 2…5 scan stayed in the band **0.059–0.33** — never near the proxy's
  0.0008, never near zero. The cross-rung terms install a per-rung floor that
  does not collapse: at d=4, where within-only fell to 0.0017, within+cross was
  still 0.059 (a ~35× gap). The cross floor is the robust signal; the exact
  per-instance number is noisy, but it is always O(0.05–0.3).

### 2. The floor is genuine 1D-chain frustration, not a rescaling artifact

Frustration test (`frustration_test` in the JSON):

- A **single isolated** cross term reaches h_min ≈ 2×10⁻⁶ — one bond's
  corridor penalty is satisfiable.
- **Two adjacent** cross terms sharing a middle rung reach h_min ≈ 0.096 > 0 —
  they **cannot be jointly satisfied**.

The penalty is per *shared rung*. Adjacent cross-rung corridor penalties
compete for the rung between them; that competition is irreducible and
accumulates linearly down the chain. This is the mechanism the within-only
fixed-space proxy structurally could not exhibit — it had no cross terms, hence
no shared-rung competition.

---

## What happens at the framework's 9 rungs, and at R ≥ R\*

h_min(R) grows **linearly in R** with per-rung energy density
**e_∞ ≈ 0.19** (exact data R=2…13; DMRG R=9…56 consistent, h_min/R ∈
[0.17, 0.19] throughout).

The soft weight at the framework-referenced β_pin = 1/2w²:

| corridor w | β_pin | soft weight at R=9 | R\*(e⁻¹) |
|------------|-------|--------------------|----------|
| 0.15       | 22.2  | **4.4 × 10⁻¹⁷**    | **≈ 0.2 rungs** |
| 0.10       | 50.0  | ~10⁻³⁷             | ≈ 0.1 rungs |

The fixed-space proxy's budget R\* ≈ 25–56 came from a per-rung slope of
0.00081 (within-only). The genuine tower's slope is e_∞ ≈ 0.19 — **~230×
larger** — because the cross-rung terms add the non-dilutable frustration
floor. At that slope, R\* (the e⁻¹ death rung) is **below 1**: the soft
operator is dead-zoned *before the first rung*, not at rung 25–56.

- **At the framework's 9 rungs** (Ph0…A5): soft weight ≈ 10⁻¹⁷. Dead.
- **At R ≥ R\* (25–56)**: the regime the proxy declared the budget ceiling is
  far past the actual collapse; every R ≥ 1 is already in the dead zone.

The pre-registration anticipated this exact failure mode: *"cross-rung terms
re-trigger the dead zone."* They do.

---

## The cosmological-scale (R → ∞) limit

With h_min(R) = e_∞·R + O(1), e_∞ > 0:

  E_ω,R(β_pin) total weight scale = exp(−β_pin·h_min(R))
                                  = exp(−β_pin·e_∞·R)  →  0   as R → ∞.

So the **strict R → ∞ limit of the soft backward operator is the zero
operator** (unnormalised); as a TSVF post-selection effect, the post-selection
amplitude of any fixed forward history vanishes in the inductive limit. The
cosmological-scale soft P_ω does **not** exist as a non-trivial operator at
fixed β.

It can be rescued *only* by β-renormalisation β_R ∝ 1/R — but β_pin = 1/2w² is
**framework-referenced to the corridor width**, a fixed physical quantity, not
a free knob. Sending β_R → 0 with R is equivalent to letting the corridor
constraint *widen without bound* with rung count — i.e. the corridor becomes
vacuous at cosmological scale. Both horns are an obstruction:

- **β pinned** → E_ω → 0 in the inductive limit (cosmological soft P_ω trivial);
- **β renormalised β ∝ 1/R** → the post-selected corridor is unbounded
  (cosmological soft P_ω non-selective).

And the limit is **not moot for the finite physical rung count**: "moot"
would require the framework's 9 rungs to sit below R\*. They do not — R\* ≈ 0.2.
The obstruction bites at the framework's actual rung count, not only in the
idealised limit.

---

## Scope — what this touches and what it does not

**Touched.** The *multi-rung backward soft P_ω* carrying cross-rung structure —
the object D1 (Penrose past) and the asymptotic-conditioning theorem
post-select through. On a genuine tower with ω's property (iii), it is
dead-zoned at the framework's rung count. F-11/F-12 territory: a documented
obstruction in the universal-scale construction. The prior session's
"R\* ≈ 25–56, F-11 does not fire" rested on a within-only fixed-space proxy;
the genuine tower with cross-rung terms overturns the *margin*, not by a
calibration shift but by a structural mechanism (shared-rung frustration) the
proxy could not see.

**Not touched.** The within-rung corridor (F-10, single-rung, empirically
supported across five substrates). The engineering tier. The soft *forward*
P_ω (ρ_ss, the open-system steady state) — that is a forward dissipative
construction with no cross-rung intersection problem. The Kish identity and the
corridor-as-attractor empirical content. This is a squeeze on the multi-rung
*joint* backward object specifically.

**Honest limits of this construction.**
1. Rung spaces are qutrits (d = 3); the per-rung-dimension scan (d = 2…5, one
   tower instance each) shows the within-only penalty is noisy and can fall to
   the proxy regime (0.0017 at d=4), while the cross floor stayed 0.059–0.33
   across all four d — so the obstruction is dimension-robust over the tested
   range, but d ≤ 5 and a per-d ensemble average is not computed.
2. The coarse-graining maps W_n are square unitaries (mix-and-relabel RG
   steps); a dimension-shrinking rectangular isometry is supported by the code
   but not run here.
3. DMRG is cross-validated to ~10⁻⁹ for R ≤ 13 and stays consistent through
   R = 56; beyond R ≈ 56 a fixed-bond (χ=48) MPS is not fully relaxed
   end-to-end, so the R → ∞ statement is made **analytically** (h_min linear
   with slope e_∞ > 0, already proven by the exact R ≤ 13 data), not by deep
   DMRG points.
4. β_pin = 1/2w² is framework-*referenced*, not framework-*derived* — the same
   standing caveat the soft route has carried throughout.

The obstruction does not depend on these: it is driven by the cross-rung
frustration floor e_∞ > 0, which the exact (un-approximated) R ≤ 13 data alone
establishes.
