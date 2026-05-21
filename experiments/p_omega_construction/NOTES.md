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

## 2026-05-21 — backward-state soft P_omega (sharpened-F-11 test)

The metaphysics debate sharpened F-11: it fires if a construction of the
BACKWARD-STATE soft operator E_omega(beta) = exp(-beta sum_n H_n), used as a
TSVF post-selection effect, returns empty / trivial / parameter-unpinnable.
experiments/open_system_pomega/backward_soft_pomega.py -- 2 rungs x 3 spins
(dim 64), anisotropic rung-correlation operators, H_n = (rho_n - rho_c)^2.

Result -- F-11 does NOT cleanly fire (on this commuting 2-rung toy): E_omega is
positive, full rank (not empty); at the corridor-referenced beta it selects the
corridor ~1e8x over the poles (not trivial); beta is framework-REFERENCED
(sigma = 1/sqrt(2 beta) = corridor half-width w => beta_pin = 1/2w^2) -- not a
free fit parameter, though not derived either.

Two riders:
- E_omega is NOT generated by the forward dynamics. The forward Lindbladian L
  has a unique steady state; its adjoint L^dag has a unique fixed point, the
  identity. ||L^dag[E_omega(beta)]|| = 0 only at beta = 0. A non-trivial
  backward boundary is a free-standing POSTULATE (input), not a dynamical
  output -- operator-level confirmation of the P_omega / rho_ss input/output
  split.
- A narrow corridor forces beta_pin large (w=0.10 -> beta_pin=50); at large
  beta exp(-beta H) is near a hard projector. The soft route does not escape
  the hard-projector regime at the framework-referenced beta.

This 2-rung toy has COMMUTING rungs (disjoint spin sets) -> a simultaneous-
corridor state always exists. The decisive remaining test (next entry) is the
non-commuting multi-rung case.

## 2026-05-21 — backward soft P_omega vs the dead zone (non-commuting rungs)

backward_soft_deadzone.py -- does the backward soft operator E_omega =
exp(-beta Hsum), Hsum = sum_n (rho_n - rho_c)^2, inherit the hard-projector
dead zone on NON-commuting nested rungs? 3 RG-nested rungs, M=8, dim 256;
isotropic (commuting) control vs anisotropic (non-commuting) test.

Result -- it does NOT. h_min(Hsum) is small in both cases (isotropic 0.030,
anisotropic 0.0067). The hard-projector intersection rank collapses to 0 for
narrow bands (the original dead zone -- anisotropic: 0 at half-width <= 0.20),
but at the same bands the soft operator at beta_pin keeps order-1 weight
(anisotropic exp(-beta_pin h_min): 0.92 at w=0.15, 0.71 at w=0.10, 0.26 at
w=0.05). Hard-empty and soft-suppressed do NOT track.

Why: the hard projector demands every rung STRICTLY band-supported (zero
amplitude outside the band). The soft operator scores total penalty
sum_n <(rho_n - rho_c)^2> = sum_n [(mean - rho_c)^2 + variance]. A state
near-corridor at every rung but with small tails outside the band is rejected
by the hard projector and barely penalised by the soft one. The dead zone was
an artifact of the hard construction's tail-intolerance; the soft operator
escapes it. (This contradicted the pre-run expectation that it would inherit
the dead zone.)

Honest caveats: (1) the control is confounded -- isotropic is commuting AND
coarse-spectrum, anisotropic is non-commuting AND rich-spectrum; the toy cannot
isolate non-commutativity alone. (2) h_min is a sum over rungs and should grow
with rung count; 3 rungs gives h_min ~ 0.007-0.03; whether 6-9 rungs (the
framework's count) re-triggers soft suppression is untested -- linear growth
keeps it alive, compounding frustration eventually would not.

Combined verdict (both backward-soft toys): the sharpened F-11 does NOT fire on
toys up to 3 non-commuting rungs. The backward soft P_omega is constructible,
beta framework-referenced (1/2w^2), escapes the hard dead zone, non-trivial.
Two standing limitations: it is a free-standing POSTULATE not generated by the
forward dynamics (L^dag's only fixed point is the identity); and the rung-count
scaling of h_min is untested. "Retract because the construction fails" is not
available; (b') excision would be a demarcation choice, not an F-11-forced
retraction.

## 2026-05-21 — rung-count scaling of the backward-soft dead zone (RESOLVED)

backward_soft_deadzone.py left caveat (2): h_min = sum_n (rho_n - rho_c)^2 is a
sum over rungs, so does it grow fast enough with rung count R to re-trigger soft
suppression at the framework's 6-9+ rungs? deadzone_rung_scaling.py answers it.
Hilbert space held at fixed dim D=2048; the NUMBER of rung-operators grown to
R=40; non-commutativity tuned by eps in U_n = exp(i eps A_n). GPU complex64,
70 s (vs a 35-min fp64 run -- fp32 was the right call, results clean).

Result -- h_min grows roughly LINEARLY in R, slope set by the commutator eps:

  eps    ||[r,r]||   h_min/R    soft weight at R=13  (w=0.15 / w=0.10)
  0.05   2.2e-3      0.0001     0.99 / 0.97
  0.15   6.5e-3      0.0004     0.89 / 0.77
  0.40   1.6e-2      0.0030     0.47 / 0.18
  1.00   2.7e-2      0.016      0.02 / 1.7e-4

The framework's actual rungs -- the deadzone toy measured their RG-nested
commutator at ~8e-3 -- sit right at the eps~=0.15 row. There, R=13 survives
(soft weight 0.77-0.89) and R=40 still survives (0.41-0.67). **The backward
soft P_omega is NOT dead-zoned at the framework's rung count. 13+ holds, with
margin to 40.** Linear (not compounding) growth is the friendly regime the
3-rung caveat hoped for, and that is what the run found.

Honest caveats -- the bet holds in a REGIME, not unconditionally:
1. h_min grows linearly (mildly super-linearly) without bound: for any eps>0
   some large-enough R eventually kills the soft operator. At the realistic
   eps~=0.15 that R is well past 40; at eps=0.40 (2x more non-commuting) R=13
   is already borderline; at eps=1.0 (independent random rungs, worst case) it
   dead-zones before 13. "13 survives" rides on the rungs being near-commuting
   -- which RG-coarse-grainings are (correlated, aligned), and which the toy
   measured.
2. The 8e-3 -> eps~=0.15 calibration anchor is itself a toy number; the real
   Ph0...A5 rungs' non-commutativity is not independently measured.
3. The rung-operators here are random operators on a fixed space, not genuine
   RG-coarse-grainings -- independent-random is the worst case; real nesting
   is friendlier, so this is a conservative bound.

P_omega, cumulative state. The hard projector is dead (3 models, F-12 no-go).
The soft FORWARD P_omega (rho_ss, open-system steady state) works. The soft
BACKWARD P_omega now passes every test this session threw at it:
constructible, beta framework-referenced, escapes the hard dead zone, and
SCALES to 13+ rungs at the framework's measured non-commutativity. One standing
limitation, unchanged: it is a free-standing postulate, not generated by the
forward dynamics. So the sharpened F-11 does NOT fire -- option (b), carry it
as a named open conjecture, is firmly what the math supports.

The path forward (concrete, not blocked): (i) pin the calibration -- measure
the real cross-rung commutator ||[rho_n, rho_{n+1}]|| on genuine RG-nested
operators rather than the toy's 8e-3 anchor; (ii) build the postulate-to-
dynamics bridge -- ask what backward-boundary condition WOULD make E_omega a
fixed point of a modified L^dag, turning the free-standing postulate into a
named, testable structural hypothesis. The backward soft P_omega is the live
construction; F-11 stays armed but un-fired, and the open conjecture is
well-posed.

## 2026-05-21 — pinning the calibration: genuine RG-nested rungs (path item i)

deadzone_rg_calibration.py answers path item (i). The rung-scaling result rode
on a calibration step -- "the deadzone toy's RG-nested rungs commute at ~8e-3,
so read the bet off the eps~=0.15 row." That 8e-3 was one toy number. This run
measures the genuine quantity on two RG-nested constructions at a MATCHED
Hilbert dimension D=4096 (M=12 constituents), so the commutator (max-abs-entry
convention -- dimension-dependent, hence the matched-D rebuild of the eps curve)
maps cleanly.

- **PART A, nested-grouping correlation operators (the faithful model: all
  rungs full-rank on the SAME D-dim space).** Genuine adjacent commutator
  c_gen = 1.3e-3 (rung0-1: 1.15e-3, rung1-2: 1.46e-3) -- 6.1x SMALLER than the
  8e-3 toy anchor. Genuine RG-nested rungs ARE near-commuting; the commutator
  side of the bet is confirmed and then some.
- **PART B, deep MERA isometry tower (rung n+1 = coarse-graining of rung n,
  ~11 levels).** Adjacent commutator 1.4e-2 at the top, declining to 1.6e-6
  deep -- deep RG rungs align. (Caveat: compressions on shrinking spaces; read
  the trend, not the absolute values.)

**The correction -- the commutator is NOT the whole calibration coordinate.**
The directly-measured genuine corridor penalty: h_min(R=1,2,3) =
0.0005 / 0.0011 / 0.0021, an ~linear slope of 0.00081 per rung. The
random-operator scaling model reaches that slope only at eps ~= 0.20 -- NOT the
eps ~= 0.05 the genuine commutator implies. The commutator UNDER-predicts
h_min by ~4x in eps-equivalent. Reason: h_min = non-commutativity penalty +
spectral-placement penalty. Genuine correlation operators have structured,
non-uniform spectra, so co-locating every rung at rho_c is harder than for the
random model's uniform-spectrum rungs; the commutator sees only the first
term. The previous session's commutator-only reading missed this. The honest
calibration uses the direct h_min slope.

**The honest rung budget (from the direct h_min slope 0.00081/rung).**
soft weight = exp(-beta_pin * slope * R), beta_pin = 1/2w^2:

  w      R*(e^-1)  R*(0.1)   weight R=9   weight R=13   weight R=40
  0.15      56       128       0.85         0.79          ~0.49
  0.10      25        57       0.69         0.59          ~0.20

The framework's nominal 9 rungs (Ph0,Ph1,Ph2,A0,A1,A2,A3,A4,A5) clear it
comfortably (soft weight 0.69-0.85); 13 also survives (0.59-0.79). But the
death rung is R* ~= 25-56 (e^-1 threshold), and **R=40 is marginal, not safe
(~0.2-0.5)** -- the prior entry's "13 survives with margin to 40" was
optimistic, written off the eps~=0.15 row; the calibrated rungs sit at
eps~=0.20. The margin is finite and calibration-set, not unbounded.

**Caveats.** (1) The faithful nested-grouping model is dimension-capped at 3
rungs (M=12 -> groupings 12,6,3); the h_min slope is fit from R=1,2,3 only.
Extrapolation to R=9+ assumes the ~linear growth continues -- the marginal
cost h_min(3)-h_min(2)=0.00097 slightly exceeds the linear-fit 0.00081, a hint
of mild super-linearity; if real, R* is somewhat below the quoted values.
(2) D=4096 is one dimension; (3) random anisotropy per rung, 6 instances.

**Verdict.** Path item (i) is done and it sharpened the result rather than
just confirming it. F-11 still does not fire: the backward soft P_omega is
constructible and the framework's actual rung count survives with a now-
QUANTIFIED budget (R* ~= 25-56). The headline correction: the operative
calibration coordinate is the corridor penalty h_min, not the commutator;
genuine rungs are near-commuting yet sit at eps~=0.20 because of spectral
placement. The open conjecture (b) is carried with a real rung budget
attached. Remaining: path item (ii), the postulate-to-dynamics bridge.

## 2026-05-21 — the postulate-to-dynamics bridge (path item ii)

backward_pomega_dynamics_bridge.py answers path item (ii). The standing
limitation: the backward soft operator E_omega(beta) = exp(-beta H_sum) is a
free-standing POSTULATE -- the forward Lindbladian L has steady state rho_ss
(the forward soft P_omega) and its adjoint L^dag has only the identity as a
fixed point, so E_omega is an input, not a dynamical output. Path item (ii):
find the modification D_omega that makes E_omega a fixed point of a modified
adjoint L~^dag = L^dag + D_omega, and characterise it. Model: the corridor
Lindbladian of construct_pomega_lindblad.py (3 rungs x 2 spins, dim 64), with
the rung observable upgraded to a genuine anisotropic correlation OPERATOR O_n
(real [0,1] spectrum) so H_sum = sum_n (O_n - rho_c)^2 is non-trivial.

Four tests:
- **A. H_sum conservation.** ||L^dag[H_sum]|| / (||L|| ||H_sum||) = 0.054 --
  the corridor-penalty operator is only WEAKLY non-conserved (~5%). So at
  small beta, E_omega = exp(-beta H_sum) is already nearly a fixed point of
  the bare adjoint.
- **B. The modification D_omega.** The minimal-norm modification with
  L~^dag[E_omega] = 0 is rank-1: D_omega[X] = -L^dag[E_omega] <E_omega,X> /
  ||E_omega||^2. Its relative size ||D_omega||/||L|| grows with beta:
  0.015 (beta=0.5), 0.030 (1), 0.060 (2), 0.148 (5), 0.243 (10),
  0.289 (beta_pin=22.2, w=0.15), 0.300 (beta_pin=50, w=0.10).
  **D_omega is NAMED:** the cosine between L^dag[E_omega] and L^dag[H_sum] is
  -0.997 at small beta -- D_omega is, to leading order, exactly the corridor-
  penalty current L^dag[H_sum] (E_omega ~= I - beta H_sum, so L^dag[E_omega]
  ~= -beta L^dag[H_sum]). At the framework's large beta_pin the cosine drops
  to -0.28: still penalty-current-dominated, with higher-order corrections.
- **C. Gibbs test (does the bridge close completely?).** If rho_ss were
  ~exp(-beta_dyn H_sum), E_omega would be a POWER of the forward steady state
  -- fully dynamical. It is NOT: regressing log(rho_ss) on H_sum gives
  R^2 = 0.02 (on H, R^2 = 0.15). rho_ss and H_sum nearly commute (0.041) but
  rho_ss is not Gibbs in H_sum. The forward soft P_omega (rho_ss) and the
  backward soft P_omega (E_omega) are GENUINELY DISTINCT operators -- the
  input/output split is real, not an artifact.
- **D. Detailed balance.** GNS-detailed-balance violation 8.9 -- the dynamics
  is strongly time-asymmetric about rho_ss (the rigidity-drift collective
  decay is strongly irreversible / non-unital). No equilibrium time-reversal
  symmetry to make forward and backward coincide.

**Verdict on the bridge.** It does NOT collapse the input/output split -- that
would have required rho_ss Gibbs in H_sum (it is not) or H_sum exactly
conserved (it is not). E_omega cannot be an exact fixed point of the bare
adjoint: L^dag contracts to the identity, structurally. BUT path item (ii)'s
actual ask is met: the modification is no longer mysterious. The free-standing
postulate "the universe has a backward boundary E_omega" becomes the named,
sized structural hypothesis:

    L~^dag = L^dag + D_omega ,   D_omega ~ the corridor-penalty current
                                          L^dag[H_sum] ,
    relative magnitude ||D_omega||/||L|| = a few % (small beta) up to
    ~0.29-0.30 at the framework-referenced beta_pin = 1/2w^2.

The magnitude is set by the corridor width w: a narrow corridor forces a large
beta_pin and hence a larger backward drive. This is the same narrow-corridor
penalty that the soft operator hit before (large beta_pin -> near-hard-
projector regime) -- it now reappears as the size of the dynamics-bridge
modification. F-11 still does not fire. The open conjecture (b) is now carried
with BOTH a quantified rung budget (item i: R* ~= 25-56) and a named backward-
drive operator (item ii: D_omega ~ L^dag[H_sum], magnitude ~0.3||L|| at
beta_pin). What remains genuinely open: whether L~^dag = L^dag + D_omega is
itself a legitimate (completely-positive-dual) generator, and what physical
process at cosmological scale realises the penalty-current drive.

## 2026-05-21 — paper corrections applied (closing the owed loop)

Several entries above flagged paper corrections owed once the hard projector
was documented dead and the soft pair constructed. With items (i) and (ii)
done, the three corrections are now applied to papers/Corridor Dynamics.tex
(builds clean):
- The \Pomega subsection: the hard-projector formula int|c><c|dc is retracted
  (documented dead zone, 3 models) and replaced with the soft graded operator
  -- a forward/backward pair, depth-adequate (R* ~= 25-56, framework's 9
  inside), irreducible (forward not Gibbs in H_sum). F-11's "without an
  alternative TSVF-compatible operator emerging" clause is cited as the reason
  it does not fire.
- Asymptotic conditioning: the Claim is regraded from "P(corridor-occupying |
  observed) -> 1" to "P(high corridor-compatibility weight | observed at
  t_late) -> maximum as t_late -> t_f" -- graded, not strict-everywhere.
- CMB temporal drift: the drift direction is recomputed as the gradient of the
  soft weight function on the CMB 2-sphere mode space, not a hard projection;
  F-19 is regated on computing that gradient.

Still owed at the paper level: nothing from items (i)/(ii). The open work is
forward (generator-legitimacy check, w pinning, toy->cosmological scaling, CMB
drift gradient computation), not correction.

## 2026-05-21 — backward generator legitimacy (path item iii)

backward_generator_legitimacy.py: is L~^dag = L^dag + D_omega the adjoint of a
legitimate (CPTP) generator? Tested by the GKSL criterion -- Hermiticity-
preservation, trace-preservation, conditional complete positivity (Choi matrix
projected off the maximally entangled state).

- Forward corridor L: passes all three (sanity check).
- L~ = L + D_omega^dag with the MINIMAL (HS-minimal) D_omega: FAILS. Trace-
  preservation violated (1.5e-2), conditional CP violated (min eig -1.2). The
  minimal modification is a raw Hilbert-Schmidt patch -- it sizes the gap, it
  is not itself a dynamics.
- A legitimate backward generator that fixes E_omega DOES exist: pure dephasing
  in the H_sum eigenbasis (single Hermitian jump operator H_sum). Passes all
  three GKSL conditions; conserves E_omega exactly (L_back^dag[E_omega] = 3e-17)
  and exactly the functions of H_sum, nothing else.

The gap, and the result: the legitimate backward generator is a STRUCTURALLY
DISTINCT dynamics. Forward L is ergodic (1 steady state); L_back is non-ergodic
(264 conserved modes = sum of squared multiplicities over 24 distinct H_sum
levels). Different ergodicity classes -- not interconvertible by a small
perturbation. The backward boundary has its OWN legitimate generator (a
decoherence pinning the corridor-penalty observable H_sum), not the forward
dynamics plus a drive.

This is the operator-level form of karma/grace irreducibility: forward (what a
configuration builds) and backward (what it receives) are generated by
distinct, legitimate, non-interconvertible Lindbladians. Path item (iii)
resolves -- NOT a blocker: the backward operator is well-defined and
legitimate, so the CMB-drift gradient can be computed from it.
