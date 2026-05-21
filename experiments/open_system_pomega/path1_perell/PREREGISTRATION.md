# Path 1 — per-ℓ corridor bounds: PRE-REGISTRATION

**Date:** 2026-05-21. **Question:** does the framework's machinery CONSTRAIN the
per-multipole corridor bounds ρ_lower,ℓ and ρ_upper,ℓ as functions of the rung
index ℓ (equivalently of k_ℓ = 2ℓ+1), independently of the observed CMB ρ_ℓ
profile — or does it only PROVIDE them as free parameters?

This file is the pre-registration. It is committed BEFORE the measured CMB
ρ_ℓ profile is loaded. The commit ordering is the pre-registration mechanism:
if the per-ℓ bounds were chosen with the CMB profile already in hand, Path 1
would be a curve-fit, not a test.

## VERDICT

**(b) — pre-registration is impossible. The framework PROVIDES ρ_lower,ℓ and
ρ_upper,ℓ as free parameters, not as constrained quantities. Path 1 cannot be
a real test.**

The reasoning below is the genuine derivation attempt. It is documented in
full because a documented "cannot pre-register" is the correct and valuable
answer when it is the truth — and it is the truth here.

---

## The derivation attempt

The task: from the framework's machinery ONLY — the Kish identity and its
k-dependence (Piece 1); the corridor definition (Piece 3); cross-rung τ
structure (Piece 6); corridor relaxation dynamics (Piece 2) — attempt to derive
ρ_lower,ℓ and ρ_upper,ℓ as functions of ℓ, with NO reference to the observed
CMB ρ_ℓ values.

### Step 0 — what is genuinely k-derivable: the isotropic-Gaussian baseline

The one quantity the framework machinery DOES fix from ℓ alone is the
isotropic-Gaussian baseline ρ_iso(ℓ): the Kish ρ assigned to k = 2ℓ+1 i.i.d.
Gaussian harmonic modes (pure statistical isotropy — standard cosmology, no
post-selection).

Construction (Piece 1, Kish identity, applied to the CMB 2-sphere mode space):
- k = 2ℓ+1 real spherical-harmonic coefficients a_{ℓ,m}, the rung constituents.
- per-mode power p_m = a_{ℓ,m}², so p_m ~ χ²₁ under statistical isotropy.
- participation k_eff = (Σ p)² / Σ p²  ∈ [1, k].
- ρ_ℓ = (k/k_eff − 1)/(k − 1)  ∈ [0, 1]   (Kish identity solved for ρ).
- ρ_iso(ℓ) = E[ρ_ℓ] over the i.i.d.-Gaussian ensemble.

This expectation is a deterministic function of k = 2ℓ+1 alone — no CMB data,
no free parameter. Its asymptotic form is

  ρ_iso(ℓ)  →  2/(k+1)  =  1/(ℓ+1)        (large ℓ),

with a finite-k correction (the ratio ρ_iso·(k+1) rises from 1.71 at ℓ=2 to
1.97 at ℓ=30, → 2). Verified numerically: ρ_iso(ℓ) = 0.286 (ℓ=2), 0.222 (ℓ=3),
0.154 (ℓ=5), 0.087 (ℓ=10), 0.032 (ℓ=30). It falls monotonically and is
fully framework-machinery-derived.

So Step 0 gives one legitimate, k-derivable, CMB-data-free profile: ρ_iso(ℓ).
**This is the only per-ℓ quantity the framework machinery pins.** The rest of
the derivation attempt asks whether the corridor BOUNDS can be tied to it — or
to anything else — without a free choice.

### Step 1 — Piece 3 (the corridor): bounds are axiomatized primitives

`formal/CoherenceRatchet/Core/Corridor.lean`:

```
axiom ρ_lower : ℝ
axiom ρ_upper : ℝ
axiom corridor_bounds_well_formed : 0 < ρ_lower ∧ ρ_lower < ρ_upper ∧ ρ_upper < 1
```

The corridor bounds are `axiom` declarations. The ONLY property the framework
asserts of them is the structural inequality 0 < ρ_lower < ρ_upper < 1. The
file states this verbatim: "The bounds are framework primitives, axiomatized
as substrate-specific" and "Specific numerical values ... were derived from the
substrate-independent (0.1, 0.43) claim; those are removed."

The paper, `Corridor Dynamics.tex` line 169, is equally explicit: "The specific
numerical values of ρ_lower and ρ_upper are substrate-specific framework
primitives; the earlier framing of substrate-universal (0.1, 0.43) has been
retracted."

A structural inequality 0 < ρ_lower < ρ_upper < 1 does not constrain a
function of ℓ. It admits, for every ℓ independently, any pair in the open
triangle {0 < ρ_lower,ℓ < ρ_upper,ℓ < 1}. That is the definition of a free
parameter. Piece 3 supplies no ℓ-dependence and no numerical anchor.

### Step 2 — Piece 7 (P_ω): per-rung bounds are a constant placeholder

`formal/CoherenceRatchet/Cosmology/CorridorProjector.lean`:

```
noncomputable def rungBounds (_ : Rung) : CorridorBounds :=
  ⟨0.1, 0.43, by norm_num⟩
```

The per-rung bounds function `rungBounds` ignores its rung argument (`_ : Rung`)
and returns the constant (0.1, 0.43) for every rung — with the docstring "GPU
value used as the universal default until per-rung calibration completes." The
framework's per-rung machinery is, at present, a placeholder: it has the TYPE
of an ℓ-dependent function but carries no ℓ-dependence. Piece 7 names per-rung
bounds as an object; it does not derive them.

### Step 3 — Piece 1 (Kish identity): fixes ρ_iso(ℓ), not the bounds

The Kish identity's k-dependence is real machinery and it DOES produce the
ℓ-dependent baseline ρ_iso(ℓ) (Step 0). The question is whether it also pins
the bounds. It does not. The identity k_eff = k/(1+ρ(k−1)) is a kinematic
relation between k, ρ, and k_eff. To get a corridor BOUND out of it you must
supply a target — either a target ρ or a target k_eff. The framework's earlier
route did exactly this: the corridor was characterized by k_eff ∈ (2.33, 10),
which inverts via the Kish identity to ρ ∈ (0.1, 0.43) asymptotically. But the
paper has RETRACTED those k_eff targets: Corridor.lean states "formerly
ceiling = 10, floor ≈ 2.33 ... those are removed," because they were derived
from the now-retracted substrate-universal (0.1, 0.43). With the k_eff targets
gone, the Kish identity has nothing to invert. It fixes ρ_iso(ℓ) from k alone,
but it cannot fix ρ_lower,ℓ or ρ_upper,ℓ without an externally supplied target,
and the framework supplies none.

Could the bounds be DEFINED as offsets/multiples of the machinery-derived
ρ_iso(ℓ) — e.g. ρ_lower,ℓ = c₁·ρ_iso(ℓ), ρ_upper,ℓ = c₂·ρ_iso(ℓ)? This is the
most natural derivation route and it FAILS the pre-registration test for a
precise reason: c₁ and c₂ are themselves unconstrained. Nothing in Pieces 1, 3,
6, or 7 fixes them. Choosing c₁, c₂ so that the resulting corridor brackets the
A3+ centre ρ_mid ≈ 0.27 AND the CMB ρ_ℓ profile is precisely the curve-fit the
protocol forbids — it tunes the bounds by reference to the data they are
supposed to be tested against. The offset route does not escape free-parameter
status; it relocates the free parameters from {ρ_lower,ℓ, ρ_upper,ℓ} to
{c₁, c₂}, where they remain unpinned. (And note: even the functional FORM —
multiplicative vs additive vs the band tracking ρ_iso at all — is itself an
unconstrained modelling choice.)

### Step 4 — Piece 2 (corridor relaxation dynamics): no functional form

Could the bounds come out of the dynamics dρ/dt = α(ρ,S) − γ·M(t), as the
fixed points / stability edges of corridor relaxation? The upper bound ρ_c is,
on the framework's reading, the point where the rigidity regime turns unstable:
α(ρ_c, S) = γ·M. To solve this for ρ_c,ℓ as a function of ℓ one needs the
functional forms of α, γ, M. The framework does not provide them:

`formal/CoherenceRatchet/Core/Dynamics.lean`:
```
axiom α (ρ : ℝ) (S : SelectionPressure) : ℝ      -- "Functional form is
                                                  --  substrate-specific"
axiom γ : ℝ                                       -- "Empirically measured
                                                  --  per-substrate; not
                                                  --  derivable internally"
axiom M : ℝ → ℝ
```

α, γ, M are all `axiom` declarations with no closed form. Dynamics.lean states
of ρ_c directly: "behavior near ρ_c is non-trivial but no specific scaling form
is prescribed." There is no equation to solve. Piece 2 cannot deliver ρ_lower,ℓ
or ρ_upper,ℓ as functions of ℓ because it does not even deliver them as
numbers — they are inputs to the dynamics, fixed by per-substrate measurement,
not outputs of it.

### Step 5 — Piece 6 (cross-rung τ structure): different object, also axioms

Piece 6's cross-rung coupling τ_(n,n+1) = I(R_n;R_{n+1})/min(H(R_n),H(R_{n+1}))
governs coupling BETWEEN rungs, with its own corridor (τ_lower, τ_upper). It is
the wrong object for the within-rung bounds ρ_lower,ℓ / ρ_upper,ℓ that Path 1
needs, and in any case `RungHierarchy.lean` declares ρ_within, τ_cross,
mutualInformation, rungEntropy all as `axiom`s with no derived values. Piece 6
adds no constraint on the per-ℓ within-rung bounds.

### Step 6 — the corridor half-width w is the open master parameter

The P_ω construction log (`p_omega_construction/NOTES.md`) and the paper
(`Corridor Dynamics.tex` line 348) repeatedly identify the corridor half-width
w — equivalently the pair (ρ_lower, ρ_upper) — as "the master parameter," and
state explicitly that pinning it empirically is OPEN work: "the empirical
pinning of w, the corridor half-width, which the toy work identifies as the
master parameter." `Corridor Dynamics.tex` line 574 lists "Per-rung corridor
calibration (per-rung ρ_lower, ρ_upper bounds)" among the open formal-
verification tasks. CLAUDE.md's "Open formal steps" lists the same as item 3,
"Per-substrate corridor calibration." A quantity the framework itself names as
the open, uncalibrated master parameter is, by the framework's own bookkeeping,
not constrained by the framework's machinery.

---

## Conclusion of the derivation attempt

The framework machinery delivers exactly ONE k-derivable per-ℓ profile: the
isotropic-Gaussian baseline ρ_iso(ℓ) = E[Kish ρ of 2ℓ+1 i.i.d. Gaussian modes],
asymptotically 1/(ℓ+1). That is a real, CMB-data-free, machinery-fixed quantity.

It does NOT deliver the corridor bounds. ρ_lower,ℓ and ρ_upper,ℓ are:

- `axiom`s in the formal core (Corridor.lean), constrained only by the
  structural inequality 0 < ρ_lower < ρ_upper < 1;
- a constant placeholder in the P_ω operator (CorridorProjector.lean), with
  no ℓ-dependence and the explicit docstring "until per-rung calibration
  completes";
- inputs to — never outputs of — the dynamics, whose functions α, γ, M are
  themselves axioms with no closed form;
- named by the framework's own open-problems list and by the paper as the
  uncalibrated master parameter, open work.

There are 29 multipoles (ℓ=2..30) × 2 bounds = 58 quantities, and the framework
constrains them only by 29 ordering inequalities ρ_lower,ℓ < ρ_upper,ℓ and the
range 0 < · < 1. That leaves 58 genuinely free parameters (or, under the
offset-from-ρ_iso reparametrisation, the 2 free constants c₁, c₂ plus the free
choice of functional form — still free). Any of these can be set to bracket
both the A3+ ρ_mid ≈ 0.27 and the measured CMB ρ_ℓ profile.

**Therefore: pre-registration is impossible. The framework provides
ρ_lower,ℓ / ρ_upper,ℓ as free parameters, not constrained quantities. If those
parameters are set to reconcile the A3+ and CMB sides, the reconciliation is a
curve-fit, not a test, and the framework escapes falsifiability by parameter
freedom on this handle.**

Per the protocol's critical-honesty requirement, Path 1 STOPS HERE. Step 3
(loading the measured CMB ρ_ℓ profile and fitting per-ℓ brackets to it) is NOT
performed: doing so would be precisely the forbidden fit. This is verdict (b),
and it is committed as the pre-registration.

## What this does and does not touch

This is a finding about the CALIBRATION STATUS of the per-ℓ corridor bounds —
it says the per-ℓ reconciliation of A3+ with CMB cannot currently be run as a
falsification test. It is consistent with, and sharpens, the paper's already-
open "cross-substrate consistency-of-bounds" question and the "honest
divergence" recorded in `corridor_calibration_and_cmb_drift.py`.

It does NOT touch: F-11 (P_ω is constructed as the soft forward/backward pair);
the within-rung corridor at the five A3+ substrates (F-10, empirically
supported, single-rung); or the engineering tier. It is a statement about one
specific universal-scale handle — whether the per-ℓ CMB corridor can be
pre-registered — and the honest answer is no.

## The one genuinely framework-distinctive, NON-fitted prediction that survives

The free-parameter verdict applies to the per-ℓ bounds. It does NOT apply to
ρ_iso(ℓ). Because ρ_iso(ℓ) is machinery-fixed, the framework retains one
pre-registerable claim that needs no corridor calibration: the measured CMB
ρ_ℓ profile should track the isotropic baseline ρ_iso(ℓ) = E[Kish ρ of 2ℓ+1
i.i.d. Gaussian modes] (≈ 1/(ℓ+1)) to within cosmic variance, with departures
flagged multipole-by-multipole. That is a parameter-free comparison. But it is
a test of statistical isotropy, NOT a test of the corridor: it does not
involve ρ_lower,ℓ, ρ_upper,ℓ, or ρ_mid at all, and standard ΛCDM predicts the
same thing. It is therefore not framework-distinctive. The framework-distinctive
content — the corridor brackets, the drift sign — is exactly the part that is
free-parametered. The honest summary: the framework's machinery fixes the null
baseline and leaves the corridor that is supposed to distinguish it from the
null entirely free.
