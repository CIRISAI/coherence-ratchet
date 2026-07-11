# Corridor-ceiling test — DECISIONS (pre-stated before results are seen)

**Date 2026-07-10.** Tests the orchestrator sideways-pass conjecture in
`papers/notes/sakharov_ledger.md` (final section): does a maintained-correlation
system have a maximum steady-state entropy-production rate `σ_max` that COLLAPSES as
coordination deepens (`k_eff → 1`, `ρ → 1`)? If so, joined to `dρ/dt = α − γM`
(`Core/Dynamics.lean`, corridor sustained only by `M > 0`), the corridor's upper edge
would be the supply=demand crossing `σ_max(ρ) = α(ρ)` — the first mechanistic
derivation of an upper corridor bound.

The flavor-space instance is already proven (`experiments/sakharov_ledger/`):
`|J| ≤ J_max(angles) → 0` at the comonotone pole. This run asks whether the DYNAMICAL
(OU) version holds or **inverts**.

## Object and formula (fixed before computing)

Equicorrelation Ornstein–Uhlenbeck process
`dx = −Bx dt + √(2D) dW`, stationary covariance pinned to the Kish object
`C(ρ,k) = (1−ρ)I + ρ 11ᵀ` (eigenvalues: `λ₁ = 1+ρ(k−1)` uniform mode; `λ₂…ₖ = 1−ρ`,
multiplicity k−1). Lyapunov constraint `BC + CBᵀ = 2D`.

Standard decomposition (Kwon–Ao–Thouless 2005; Godrèche–Luck 2019, arXiv:1807.00694):
`B = (D + Q)C⁻¹` with `D` symmetric PD (the diffusion), `Q` antisymmetric (the
irreversible circulation). This automatically solves the Lyapunov equation. The
steady-state entropy-production rate has the closed form

> **σ = Tr[ Qᵀ D⁻¹ Q C⁻¹ ]**,  Q = ½(BC − CBᵀ) = antisymmetric part of BC.

Equivalently `σ = Tr[D⁻¹ ν C νᵀ]` with `ν = −QC⁻¹` (Godrèche–Luck form; VERIFIED against
a brute-force 2D linear-NESS current integral in `sigma_max.py` before use). σ = 0 iff
Q = 0 (detailed balance). We maximize σ over admissible antisymmetric Q under three
normalizations.

Diagonalizing in C's eigenbasis: with Q antisymmetric and entries `Q_ij`,
`σ = Σ_{i<j} Q_ij² (1/λ_i + 1/λ_j)`. The whole question is which normalization bounds
the free `Q_ij`, because `C⁻¹` has a small eigenvalue `1/λ₁` on the uniform mode and a
LARGE eigenvalue `1/(1−ρ)` (multiplicity k−1) on the collapsed modes that diverges as
ρ→1. Whether σ_max collapses or grows is entirely about whether the normalization "sees"
that `1/(1−ρ)` blow-up as a cost or as free gain.

## The three normalizations (pre-stated) and PREDICTED trend

**N1 — fixed isotropic noise (D=I), bounded ACTUATED drive.** Bound the drive power the
maintenance machinery actually applies to run the circulation: `‖QC⁻¹‖_F² ≤ P`
(the extra drift `B − B₀ = QC⁻¹` beyond the free reversible part `B₀ = C⁻¹`).
Per-pair: cost `Q_ij²(1/λ_i² + 1/λ_j²)`, yield `Q_ij²(1/λ_i + 1/λ_j)`.
**Predicted: COLLAPSE.** Efficiency (yield/cost) of the best pair (two collapsed modes)
= (1−ρ) → 0. σ_max ≈ P·(1−ρ) → 0 as ρ→1.

**N2 — fixed relaxation timescale (spectral bound on the drift, ‖B‖₂ ≤ b).** Caps the
fastest relaxation rate. The reversible part alone has `‖B₀‖₂ = 1/(1−ρ) → ∞`, so beyond
`ρ = 1 − 1/b` the NESS at C(ρ) is INFEASIBLE at fixed timescale.
**Predicted: COLLAPSE with a hard feasibility edge** at `ρ = 1 − 1/b` (b tunable). Note
this edge is partly the reversible-stiffness feasibility limit, conceptually distinct
from N1's genuine circulation-efficiency collapse.

**N3 — fixed maintenance budget as BARE stirring power, `Tr[Qᵀ D⁻¹ Q] ≤ P` (D=I ⇒
Tr[QᵀQ]).** Bounds Q in geometry-blind Frobenius units — ignores the stiffness
amplification of the collapsed modes.
**Predicted: INVERSION.** Best pair = two collapsed modes, σ_max = P/(1−ρ) → ∞ (k≥3);
for k=2, P/(1−ρ²). Grows toward the pole.

## Which is physical (pre-committed, WITH reasoning — not the confirming pick)

**N1 is the physically-motivated normalization for the framework's maintenance reading.**
Reasoning, committed before seeing numbers:

1. A real coherence-management machine (cell, cortex, institution) is limited by the
   **force/drive it can actuate** at a given noise floor, not by an abstract
   geometry-normalized stirring rate. The actuated drift is `B = (D+Q)C⁻¹`; the cost of
   the circulation is the drive `QC⁻¹` it must impose. That is exactly N1.
2. The N1↔N3 difference IS the stiffness gearing `C⁻¹`. Exciting a unit circulation in a
   collapsed (stiff, variance 1−ρ) mode requires a drive amplified by `1/(1−ρ)`, because
   the mode is strongly confined. N3 charges Q in bare units and so does not pay that
   amplification; N1 (and any real actuator) does. Real machines pay the geared cost.
3. **Guard against a false ceiling.** The reversible stiffness `‖C⁻¹‖` also diverges as
   ρ→1, but a stiff EQUILIBRIUM trap has detailed balance and ZERO housekeeping cost — it
   is free. So we must NOT charge the reversible part against the maintenance budget as a
   "cost" (that would manufacture a ceiling artifactually). N1 charges only the
   irreversible actuated drive `QC⁻¹`; N2's feasibility edge is flagged as the
   reversible-stiffness limit precisely so it is not mistaken for the maintenance ceiling.

## Kill condition (staked before results)

- If the PHYSICAL normalization (N1) does NOT collapse — if σ_max saturates or grows as
  ρ→1 under bounded actuated drive — **the ceiling mechanism is KILLED.** A clean kill is
  a fully successful run; write it plainly.
- If N1 collapses but the collapse only begins at ρ ≫ 0.43 (far above the observed
  corridor edge), the mechanism cannot set the corridor edge — report the onset ρ.
- Whether a supply=demand crossing lands in the observed band ρ ∈ (0.1, 0.43) requires
  specifying the budget P and the demand curve α(ρ). State explicitly what must be tuned;
  a crossing achieved only by tuning P to hit 0.43 is NOT a parameter-free derivation.

## Part B (data) — pre-stated read

From the `keff_saturation` catalog assemble per-substrate (k_eff = eff_rank_surr, the
saturating coordinating rank; ρ_proxy = 1/k_eff global-mode reading) vs measured
detailed-balance breaking (circulation |z|, the trustworthy estimator). The mechanism
predicts an OCCUPANCY EDGE: nothing coordinating with high σ near the pole (k_eff→1).
n is small; real systems only (the phase-randomized "dead" cell is a CONSTRUCTED control,
reversible by construction — plotted but flagged, not evidence for the edge). Report the
scatter honestly including any inversion of the within-range trend.

Seed 20260710. CPU only. Incremental flush.
