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

## 2026-05-20 — QG-via-P_omega gate 1: the MERA isometry tower (Model 1'')

construct_p_omega_mera.py. Rungs on different Hilbert spaces connected by
coarse-graining isometries that keep each block's low-energy subspace:
H_0 (256) -> H_1 (64) -> H_2 (16). rho_1 = W_0^dag rho_0 W_0, rho_2 =
W_1^dag rho_1 W_1 (genuine RG coarse-graining). P_omega = intersection of the
per-rung corridor projectors pulled back to H_0.

Result: dim(P_omega) = 0 at EVERY band tested, including wide bands. The
coarse-graining compresses the spectrum hard (rho_0 spans 1.7, rho_2 spans
0.48); more fundamentally, the isometry keeps the low-ENERGY subspace while
the corridor is the spectral INTERIOR of the correlation operator -- the
RG-relevant subspace and the corridor subspace are different objects, so the
pulled-back corridors do not overlap.

This instantiates the squeeze rather than escaping it: an RG-physical
isometry (keep low-energy) gives empty; a corridor-aware isometry (keep the
corridor) would make the coarse corridor the image of the fine one and
collapse P_omega to P_0 (trivial). Same empty/trivial squeeze.

**Gate 1 status: the hard-projector multi-rung P_omega is obstructed across
three independent constructions** -- shared-space additive coupling (Model 1),
shared-space RG coarse-graining (Model 1'), and the isometry tower (Model
1''). A robust F-12 no-go for the hard projector. The remaining route is a
SOFT P_omega: a graded operator exp(-beta sum_n H_n), non-zero by
construction, escaping the squeeze.

## 2026-05-20 — soft-vs-hard P_omega debate (team p-omega-debate)

Three-lens debate on what a soft vs hard P_omega means for reading the data.

- **hard-reading** (p ~ 0.4): keep P_omega a hard projector, accept the F-12
  no-go honestly. The hard projector is the crisper reading of Piece 7, not
  the mandated one; exact post-selection and clean Lean are its virtues.
- **soft-reading** (p ~ 0.6): reformulate as soft exp(-beta sum_n H_n).
  Faithful to Piece 7's "integral against a measure"; but D1 survives only
  in graded form (demoted from deriving the Weyl Curvature Hypothesis to
  favouring it); beta is a new unpinned parameter; non-commuting H_n
  re-import the multi-rung problem inside the exponent.
- **data-arbiter** (~0.9): the soft-vs-hard choice is NOT empirically
  decidable now. The entire empirical record (five substrates, F-10/F-20)
  is single-rung; soft and hard differ only as descriptions of the
  multi-rung joint object, which no measured datum touches. The choice is
  FORMAL.

**Correction surfaced in synthesis.** hard-reading and soft-reading both
treated "the cross-rung-coupling test" as the decisive UNRUN experiment,
citing the stale "decisive next test" line in the general.py section above.
That toy test is NOT unrun -- it is Models 1, 1', 1'', all no-go. The stale
line is superseded. What is genuinely unrun is the EMPIRICAL cross-rung
measurement below.

**Decisive measurement (data-arbiter).** Cross-rung mutual information on a
simultaneously-instrumented two-rung system: hard P_omega predicts a sharp
spectral edge in the joint constraint, soft predicts a graded exponential
tail. Cheapest instance -- re-analyse the existing Drosophila dual-colour
EPG+FC3 data (Ishida 2025) for I(EPG; FC3). The paper currently reports only
the two INDEPENDENT within-rung values from that dataset; the cross-rung MI
is the first empirical purchase on the multi-rung object.

**Paper corrections owed (data-arbiter).** (1) F-11 is published as a
conditional ("on a documented no-go") -- the no-go is now documented across
three constructions; book F-11 as fired for the hard projector. (2) Paper
section 6.1 still describes the hard projector ("well-defined projection
rather than set-theoretic intersection") -- the construction that failed.
Flagged for the author; not auto-applied.

## 2026-05-20 — F-11 status check + soft-vs-hard empirical discriminator

**F-11 is NOT fired.** Paper line 461: F-11's trigger is "documented no-go on
formal P_omega operator construction." Paper line 473 (F-17) makes the
P_omega no-go matter only "without an alternative TSVF-compatible operator
emerging." What is documented is a no-go on the HARD-PROJECTOR construction
specifically; the soft P_omega (exp(-beta sum H_n)) is an un-refuted
TSVF-compatible alternative. data-arbiter's "book F-11 as fired" was
overstated. What is owed: paper line 345's "well-defined projection" framing
should record that the projection route is obstructed; F-11 stays armed and
is now sharpened -- it fires if the soft route also fails.

**Soft-vs-hard empirical discriminator -- run, inconclusive.** data-arbiter
proposed: the SHAPE of the cross-rung coupling distribution in a real
two-rung system (sharp edge => hard P_omega; graded exponential tail => soft).
The autonomous loop's v19_biology agent had already fetched the real data
(Ishida et al 2025, Cell; same-fly simultaneous dual-color EPG+FC3 imaging;
Zenodo 17555687; 7 recordings / 4 flies) and already run a cross-rung test --
v19's PRIMARY cross-rung prediction FAILED (pre-registered: no state-dependent
shift). v19 did not characterise the distribution shape.

experiments/cross_rung_shape/analyze_cross_rung_shape.py computes it on the
real v19 data (windowed rho, 30 s windows, 846 windows pooled):
- cross-rung rho_EF: median 0.194, p99 0.364, max 0.416; 0/846 windows exceed
  0.43. Upper tail: Gaussian fit R^2 0.983 BEATS exponential R^2 0.933; cliff
  ratio 0.31 (no hard edge).
- within-EPG rho ~0.38 (28% of windows > 0.43), within-FC3 ~0.23 -- both in
  corridor-like bands (consistent with F-10).

Reading: the cross-rung coupling distribution is Gaussian-like -- it shows
NEITHER the hard-P_omega signature (a cliff) NOR the soft-P_omega signature
(an exponential tail). It is the generic null: a bounded correlation statistic
fluctuating around its mean. The discriminator does not distinguish soft from
hard.

**Bottom line.** The soft-vs-hard P_omega choice remains FORMAL -- now not
merely "unmeasured" but "the proposed empirical proxy was measured and does
not discriminate." The QG-via-P_omega line is stuck at gate 1: the hard
projector is obstructed (3 models), the soft alternative cannot be empirically
grounded via this handle, and the one substrate with real multi-rung data
shows no distinctive corridor-constraint signature in the cross-rung coupling.
Untouched: the engineering tier and the within-rung corridor (F-10), which the
within-rung EPG/FC3 bands here are consistent with.

## 2026-05-20 — P_omega as an open-system steady state (the reframe)

The gate-1 program built P_omega as a projector on a CLOSED Hilbert space and
hit a robust dead zone. But a corridor cannot exist in a closed system; Piece 2
(drho/dt = alpha - gammaM) is an open dissipative equation, and the gate-1
constructions never used it -- only Piece 1 (rho as operator) and Piece 3 (the
band), statically. The reframe: P_omega is the steady state of an open-system
(Lindblad) dynamics whose dissipator is gammaM.

experiments/open_system_pomega/construct_pomega_lindblad.py -- 3 rungs x 2 spins
(dim 64). H = intra-rung Heisenberg + cross-rung ZZ. alpha = per-rung collective
decay (rigidity drift, rates 0.6/1.0/1.5). gammaM = per-spin bit-flip
(maintenance), swept. rho_n = |<Z Z>| of each rung in the steady state.
P_omega = the steady-state density operator rho_ss.

Result:
- rho_ss exists and is a valid density operator (Hermitian, trace 1, positive,
  rank ~63-64) at every gammaM. No intersection -> the closed-system dead zone
  structurally cannot recur.
- A real gammaM window [~0.05, 0.35] puts all three rungs simultaneously in
  (0.1, 0.43): e.g. gammaM=0.10 -> rho = (0.251, 0.318, 0.343). The three rungs
  have different drift rates, so this is a genuine overlap, not a symmetry
  artifact. gammaM -> 0 drives rho_n toward rigidity; large gammaM toward chaos.

Honest scope: steady-state existence is structural (a Lindbladian always has
one), not a discovered corridor -- the contentful result is the non-empty
simultaneous-band window, which holds for rungs whose drifts are not too
disparate. rho_ss is full-rank: the graded object the soft-vs-hard debate
circled. The reframe uses Piece 2 for the first time in the P_omega
construction. CAVEAT: a forward dissipative steady state is not a TSVF backward
post-selection; this reframes the corridor construction, it does not rescue the
cosmological tier (asymptotic conditioning and Penrose-from-P_omega were built
on future-boundary post-selection). F-11 stays armed; the open-system steady
state is the live construction route.
