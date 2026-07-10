# The copula-invariance remark — the blindness is either a bug or the theory's strangest prediction

**Status:** remark, 2026-07-10, unverified beyond the standard facts cited; flagged by the
operator ("coordination invisible to C would be coordination that doesn't gravitate — either
a bug or the framework's weirdest prediction"), sharpened here. Needs one verification pass.

## 1. The flag

The entropic action, as transferred, is a functional of the pairwise correlation spectrum.
Whatever coordination is invisible to that spectrum sources no action. The quantum-corridor
calibration has already *measured* this blindness concretely: N-qubit GHZ parity coordination
reads ρ̄ ≈ 0 in the X basis — real, maximal, N-body coordination carrying exactly zero
pairwise signal (CALIBRATION.md, the N4 result). Inside the gravity reading this becomes: a
purely higher-order-coordinated matter configuration would not gravitate entropically, while
in GR all stress-energy gravitates unconditionally. That is a structural difference between
the readings — unmeasurable in practice with matter, but a genuine discriminating residue,
and it must be either repaired (wrong functional) or owned (weird prediction).

## 2. The sharpening: the true multi-information is *invariant*, not merely non-increasing

Standard fact: multi-information I(X₁,…,X_k) is a property of the copula — invariant under
any *invertible* per-component transform, strictly decreased by non-invertible ones (DPI).
The lognormal map used as the nonlinear-growth proxy is invertible pointwise. Therefore:

- The **Gaussian-committed** S (what we compute: −ln det of the Pearson correlation matrix)
  *falls* under the lognormal map — the no-phantom theorem.
- The **true** multi-information of the transformed field is **exactly unchanged**.

So the "S declines under local nonlinearity" of the no-phantom computation is, from the
copula viewpoint, an artifact of reading a non-Gaussian field with a Gaussian ruler. Under
the true-multi-information reading, the statement is *stronger and cleaner*:

> **Local (invertible, pointwise) dynamics contributes exactly ZERO to dS — not merely
> dS ≤ 0. All evolution of the coordination content comes from the non-local /
> non-invertible / unit-population channels.**

Consequences, if the verification pass holds:

1. The w(z) pipeline's entire signal is the **unit-formation channel** (halo condensation,
   mergers) plus genuinely non-local dynamics — the halo-grain result is not "a channel that
   escapes the theorem" but *the only channel there is*. The fixed-unit branch's prediction
   sharpens from "thawing, w ≥ −1" to "w = −1 exactly" under the true-MI reading.
2. The Gaussian commitment is now measurable inside the pipeline: compute both the Pearson-S
   and a copula/rank-based S (Spearman/Gaussian-rank correlation gives the copula's Gaussian
   part exactly for pointwise-transformed Gaussian fields) on the same halo data — they
   should differ in the predicted direction, and the rank-based one should be flat under the
   lognormal proxy. A concrete, cheap discriminator between the two functionals.
3. The GHZ-type blindness *survives* the sharpening (higher-order coordination beyond any
   pairwise copula is still invisible), so the bug-or-prediction fork stands — it just moves
   to orders ≥ 3: does coordination carried purely above second order gravitate? The
   entropic reading with the −Tr ln C functional says NO. Owning this means predicting that
   matter configurations with purely ≥3-order structure are entropically dark. Repairing it
   means the action should be the full (all-orders) multi-information — at which point the
   Gaussian identity S = 2I becomes the *small-non-Gaussianity limit* of the theory rather
   than its definition.

## 3. Verification pass needed (one afternoon)

(a) Confirm the invariance numerically: true MI of a k=3..5 Gaussian vs its lognormal image
(k small enough for direct numerical integration or kNN MI estimation). (b) The rank-based S
flatness test on the existing s_of_a.py machinery. (c) Confirm Bianconi's functional is
pairwise-spectral in the relevant sense (her G̃g̃⁻¹ eigenvalues on Dirac-Kähler fields —
whether higher-order field correlations enter her action at all; if they do via the
nonlinearity of ln, characterize).

## 4. Scope

This note modifies no committed result: the no-phantom theorem is true as stated for the
Gaussian-committed functional (independently verified); the halo-grain result computes that
same functional consistently. What this note changes is the *interpretation stack* and it
adds discriminators. The L-01-shaped hole (emergent structure invisible to the instrument's
functional) is hereby carried explicitly into the gravity reading rather than left implicit.
