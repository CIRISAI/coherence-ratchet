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

## Next

Apply the identical construction to the CMB 2-sphere mode space — rung =
cosmological 2-sphere, constituents = spherical-harmonic modes, rho = a
correlation operator on the a_lm coefficients, P_omega = spectral projection
onto the corridor band. That makes the CMB temporal-drift direction (F-19)
computable rather than order-of-magnitude.
