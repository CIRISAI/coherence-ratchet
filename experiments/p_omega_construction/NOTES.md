# P_omega construction — verification result

**Date:** 2026-05-20. **Falsification handle:** F-11 (P_omega operator construction).

## What was constructed

P_omega, the projector onto multi-rung corridor configurations, built explicitly
as a genuine orthogonal projector for a finite-rung tensor-product model.

**The construction.** rho_n is treated as a self-adjoint *operator* (the
within-rung correlation observable), not a nonlinear functional of the global
state. Then:

- P_n = spectral projection of rho_n onto the corridor band [0.10, 0.43].
  Orthogonal projector by the spectral theorem.
- P_omega = product over rungs of P_n. The rho_n act on distinct tensor
  factors, so the P_n commute, and the product of commuting orthogonal
  projectors is an orthogonal projector onto the intersection of their ranges.

This realizes the paper's "integral of |config><config| dconfig": dconfig is
the joint spectral measure of the rho_n; the binary rung indicator is P_n; the
"set-theoretic intersection vs well-defined projection" problem dissolves.

## Verification (R=3 rungs, N=4 spin-1/2 constituents per rung, dim 4096)

- rho_n spectrum: {0.0 (chaos, mult 2), 0.333 (corridor, mult 9), 1.0
  (rigidity, mult 5)}. The framework corridor band (0.10, 0.43) cleanly
  isolates the interior eigenvalue.
- P_n: rank 9, idempotent and self-adjoint — verified.
- P_n mutually commute: max ||[P_a, P_b]|| = 0.
- **P_omega: idempotent (||P_omega^2 - P_omega|| = 7e-16), self-adjoint
  (0), spectrum {0,1} (6e-16), rank 729 = 9^3. P_omega IS an orthogonal
  projector.**
- TSVF post-selection: corridor-seeded forward history has post-selection
  probability 0.986; corridor-orthogonal history 0.003 (~340x suppression).
  ABL weak value of a rung observable is well-defined for corridor pre/post
  selection (denominator 2.4e-2) and ~18x suppressed for a corridor-orthogonal
  forward history (denominator 1.3e-3). The denominator is suppressed, not
  exactly zero: the backward state at intermediate times is P_omega-supported
  only at t_f, so suppression is dynamical, not exact projection.

## Status of F-11

F-11's documented no-go does **not** fire. The operator form of P_omega is
constructed and verified. The open problem is now sharper and smaller than
"P_omega is unconstructed":

- **(a) Cross-rung non-factorization.** If rungs nest (rung n+1 built from
  rung n's aggregates), the rho_n need not commute and P_omega is not the
  simple product. It remains constructible: by von Neumann's alternating-
  projection theorem, P_omega = lim_k (P_1 P_2 ... P_R)^k is the projector
  onto the intersection of the rung corridor subspaces even for non-commuting
  P_n. Not a no-go; a different (iterative) construction.
- **(b) The cosmological configuration Hilbert space.** This artifact builds
  P_omega's operator form on a finite-rung model. The actual universal-
  configuration space it acts on at cosmological scale is not built. This is
  the genuine remaining frontier.

## 2026-05-20 — P_omega off the SU(2) toy (construct_p_omega_general.py)

Tested the p-omega-debate team's three findings on a non-SU(2) substrate:
anisotropic XYZ correlation operators (a != b != c), random independent
couplings per rung, three RG-nested rungs on one 256-dim space.

- **Non-commutation confirmed.** Anisotropic rungs do not commute
  (||[rho_a, rho_b]|| ~ 1e-3). The earlier nesting-toy commutativity was an
  SU(2) Casimir artifact (debate finding 3).
- **Existence generalizes.** P_omega is constructible for non-commuting
  rungs via the averaged-projector eigenspace method — the eigenvalue-1
  space of (sum P_n)/R, exact and one-shot, valid for non-commuting
  projectors. Halperin alternating projections are the textbook route but
  converge impractically slowly here (20000 iterations, residual still
  1e-6): a numerical-method fact, not a no-go. F-11 existence holds off the
  toy.
- **NEW — the dead zone.** dim(P_omega) vs corridor band half-width w:
  w <= 0.20 -> 0;  w = 0.30 -> 56 (22%);  w = 0.40 -> 135 (53%);
  w = 0.49 -> 232 (91%). On a generic non-commuting substrate the three
  rung-corridor subspaces do not intersect unless each per-rung band is
  wide (> ~0.6 of the spectral range). Narrow per-rung corridors -> empty
  intersection -> P_omega = 0, "corridor at every rung simultaneously" is
  unsatisfiable. Wide bands -> non-empty but generic (> 50%), post-selection
  non-selective.

**What this threatens, and what it does not.** It does not touch the
within-rung corridor (F-10, single-rung, empirically supported) or the
engineering tier. It is a genuine squeeze on the *multi-rung* P_omega: the
asymptotic-conditioning theorem needs P_omega both non-empty and selective,
and on a generic substrate you do not get both.

**Decisive next test.** The toy used rungs in *generic relative position* —
independent random couplings, no cross-rung correlation. Piece 6 of the
framework asserts the opposite: adjacent rungs are coupled, cross-rung tau
in its own corridor. Cross-rung coupling is the hypothesis that rungs are
NOT in generic position — the candidate mechanism for making narrow per-rung
corridor subspaces intersect. Next experiment: introduce cross-rung coupling
(correlated / shared coupling structure) and measure whether the dead zone
shrinks or closes. If it does, Piece 6's tau-coupling becomes load-bearing
and motivated. If it does not, the multi-rung P_omega is in genuine trouble.

## Later

Apply the construction to the CMB 2-sphere mode space — rung = cosmological
2-sphere, constituents = spherical-harmonic modes, rho = a correlation
operator on the a_lm coefficients, P_omega = spectral projection onto the
corridor band. Makes the CMB temporal-drift direction (F-19) computable
rather than order-of-magnitude. Gated behind the cross-rung-coupling test:
a CMB P_omega built with an uncalibrated band reproduces the dead-zone /
generic-zone ambiguity at cosmological scale.

## 2026-05-20 — QG-via-P_omega, gate 1: the dead zone is robust

The QG line takes "QG is a cross-rung interaction" and asks whether the
cross-rung structure makes the multi-rung P_omega viable. Gate 1 — close the
narrow-band dead zone — was tested two ways.

- **Model 1 (construct_p_omega_coupled.py) — additive cross-rung coupling.**
  rho_n(g) = intra_n + g * (nearest-neighbour cross-rung terms). Sweep g x
  band width. Result: at narrow bands (half-width <= 0.15) dim(P_omega) = 0
  for every g up to 1.5. Coupling aligned the rungs slightly (commutator
  4.7e-3 -> 2.5e-3) and lifted mid-band occupancy, but did not close the
  narrow-band dead zone.
- **Model 1' (construct_p_omega_rg.py) — rungs as RG coarse-grainings.** All
  rungs share an RG-inherited coupling; a flow parameter measures distance
  from the RG fixed point. Result: even at the fixed point (flow = 0)
  dim(P_omega) = 0 for half-width <= 0.15. The flow barely moved the
  commutator — rung misalignment is driven by group/coarse-graining
  STRUCTURE, not coupling values.

**The no-go is robust and scale-free.** P_omega as a hard-projector
intersection of per-rung corridor subspaces: three narrow subspaces of
dimension d_n in a D-dim space, in generic position, intersect in dimension
max(0, sum d_n - (R-1)D). For narrow bands d_n/D is small, so the
intersection is generically empty — and this gets worse, not better, at
higher dimension. Not a small-toy artifact.

**The squeeze.** The hard-projector multi-rung P_omega is caught: independent
rungs -> empty intersection (dead zone); rungs nested so the coarse corridor
is by construction the image of the fine corridor -> non-empty but P_omega
collapses to the finest-rung projector, the "every rung" structure doing no
work (trivial). Empty or trivial.

**What it touches.** Not the within-rung corridor (F-10, single-rung,
empirically supported) or the engineering tier. It squeezes specifically the
hard-projector multi-rung P_omega — the object D1 (Penrose past) and the
asymptotic-conditioning theorem post-select through. F-12 territory: a
documented obstruction in the universal-scale construction.

**Reformulation, not dead end.** Piece 7 writes P_omega as "integral of
|config><config| dconfig" — an integral against a MEASURE, naturally graded,
not a hard projector. A soft P_omega — e.g. exp(-beta * sum_n H_n) with H_n
penalising distance from rung n's corridor — is non-zero by construction,
selective without being empty, escapes the empty/trivial squeeze, and is a
genuine TSVF object (soft / non-projective post-selection). Candidate next
model. Second option: the MERA-style isometry tower (rungs on different
spaces) — genuinely open, could land non-empty-and-selective or in either
failure mode.
